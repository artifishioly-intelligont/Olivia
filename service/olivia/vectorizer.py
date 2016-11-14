import numpy as np
import os.path

from neon import NervanaObject
from neon.util.persist import load_obj
from neon.backends import gen_backend
from neon.data import ArrayIterator
from neon.models import Model
from neon.util.argparser import NeonArgparser
from os.path import split, splitext, isfile
from scipy.misc import imread, imsave


default_prm_path = os.path.expanduser('~')+'/SaturnServer/Googlenet_791113_192patch.prm'

def image_is_local(img_path):
    return os.path.isfile(img_path)

class Vectorizer:
    model = None
    layer = None
    patch_width = None
    patch_height = None

    def __init__(self, prm_path=default_prm_path, layer=-4, backend='gpu'):
        print 'Log::Vectorizer:: Initialising Vectorizer'
        self.layer = layer

        if not os.path.isfile(prm_path):
            raise Exception('FileNotFound: Cannot find the file %s' % prm_path)

        print 'Log::Vectorizer:: Generating backend, backend: {}'.format(backend)
        cores = 32
        if backend == 'cpu':
            cores = 1
        gen_backend(batch_size=cores, backend=backend)


        print 'Log::Vectorizer:: Loading model from %s' % prm_path
        model_dict = load_obj(prm_path)

        print 'Log::Vectorizer:: Generating model with loaded file'
        self.model = Model(model_dict)

        # now we are going to extract the middle patch from the image,
        # based on the size used to train the model
        self.patch_height = model_dict['train_input_shape'][1]
        self.patch_width = model_dict['train_input_shape'][2]

        print 'Log::Vectorizer:: Initialising Model'
        # initialise the model so that internally the arrays are allocated to the correct size
        self.model.initialize(model_dict['train_input_shape'])
        print 'Log::Vectorizer:: DONE!'

    def get_attribute_vector(self, img_path):
        if not image_is_local(img_path):
            print 'Error::Vectorizer:: File Not Found: The image at %s does not exist' % img_path
            return -1

        im = imread(img_path).astype(float)

        # Fix the image into a flat array organised as [RRRRR..GGGGG..BBBB]
        patch_array = self.patch_image(im)

        # make an image buffer on host, pad out to batch size
        host_buf = np.zeros((3 * self.patch_height * self.patch_width, self.model.be.bsz))
        # set the first image to be the image data loaded above
        host_buf[:, 0] = patch_array.copy()

        # make buffer on the device
        dev_buf = self.model.be.zeros((3 * self.patch_height * self.patch_width, self.model.be.bsz))
        # copy host buffer to device buffer
        dev_buf[:] = host_buf

        # Send through the network. Note that in the returned array there
        # will be one column for each item in the batch; as we only put data
        # in the first item, we only want the first column
        predictions = self.model.fprop(dev_buf, True).asnumpyarray()[:, 0]
        # print predictions

        # Print the activations of the 4th layer from the end of the model
        # Note 1: model.layers represents a SingleOutputTree when using GoogLeNet;
        # during inference only the main branch (index 0) outputs are considered
        # Note 2: in the returned array there will be one column for each item
        # in the batch; as we only put data in the first item, we only want the
        # first column
        return self.model.layers.layers[0].layers[self.layer].outputs.asnumpyarray()[:, 0]

    # Expects 256x256
    def patch_image(self, im):
        # convert to BGR
        im = im[:, :, ::-1]

        # approximately mean-centre it
        im = im - [128, 128, 128]

        # Finding the co-ordinates for each corner of the centre patch
        padY = int(self.patch_height / 2.0)
        padX = int(self.patch_width / 2.0)
        y = im.shape[0] - 2 * padY
        x = im.shape[1] - 2 * padX
        col = int(x / 2)
        row = int(y / 2)

        right = col + self.patch_width
        left = col
        top = row
        bottom = row + self.patch_height

        # Cropping the image
        patch = im[top:bottom, left:right, :]

        # Neon wants the data as a flat array organised as [RRRRR..GGGGG..BBBB]
        patch_array = patch.transpose((2, 0, 1)).flatten()

        return patch_array
