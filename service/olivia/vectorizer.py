import numpy as np
import os.path
import os

from neon import NervanaObject
from neon.util.persist import load_obj
from neon.backends import gen_backend
from neon.data import ArrayIterator
from neon.models import Model
from neon.util.argparser import NeonArgparser
from os.path import split, splitext, isfile
from scipy.misc import imread, imsave

default_prm_path = os.path.expanduser('~') + '/SaturnServer/Googlenet_791113_192patch.prm'


class Vectorizer:
    model = None
    layer = None
    patch_width = None
    patch_height = None
    backend = None
    cores = None
    generated_backend_object= None

    def __init__(self, prm_path=default_prm_path, layer=-4, backend='gpu', cores=32):
        print 'Log::Vectorizer:: Initialising Vectorizer'
        self.layer = layer

        if not os.path.isfile(prm_path):
            raise Exception('FileNotFound: Cannot find the file %s' % prm_path)

        print 'Log::Vectorizer:: Generating backend, backend: {}'.format(backend)
        if backend == 'cpu':
            cores = 1
        self.cores = cores
        self.generated_backend_object = gen_backend(batch_size=self.cores, backend=backend)
        self.backend = backend

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

    def get_batch_attribute_vectors(self, img_path_array):
        """
        Given you are running on a GPU, you batch process self.cores number of images at a time.

        :param img_path_array: An array of self.cores number of images
        :return: A dict of the paths and their respective attribute vectors

        :raise GpuNotSupportedException -- This method will only work when your `self.backend == 'gpu'`
        """
        # Ensure that a cpu user is not accessing a GPU command
        if self.backend is not 'gpu':
            raise GpuNotSupportedException(self.backend)

        imgs_to_process, failed_images = self.get_images_to_process(img_path_array)

        # make an image buffer on host, pad out to batch size
        # Note: self.model.be.bsz == self.cores
        host_buf = np.zeros((3 * self.patch_height * self.patch_width, self.model.be.bsz))

        for img_index in range(len(imgs_to_process)):
            im = imread(imgs_to_process[img_index]).astype(float)

            # Fix the image into a flat array organised as [RRRRR..GGGGG..BBBB]
            patch_array = self.patch_image(im)

            # set the first image to be the image data loaded above
            host_buf[:, img_index] = patch_array.copy()

        # make buffer on the device
        dev_buf = self.model.be.zeros((3 * self.patch_height * self.patch_width, self.model.be.bsz))
        # copy host buffer to device buffer
        dev_buf[:] = host_buf

        # Send through the network.
        predictions = self.model.fprop(dev_buf, True).asnumpyarray()[:, 0]
        # print predictions

        # Print the activations of the 4th layer from the end of the model
        # Note 1: model.layers represents a SingleOutputTree when using GoogLeNet;
        # during inference only the main branch (index 0) outputs are considered
        img_vector_dict = {}
        for img_index in range(len(imgs_to_process)):
            img_path = imgs_to_process[img_index]
            img_vect = self.model.layers.layers[0].layers[self.layer].outputs.asnumpyarray()[:, img_index].tolist()
            img_vector_dict[img_path] = img_vect

        return img_vector_dict, failed_images

    def get_NSEW_batch_attribute_vectors(self, img_path_array):
        """
        Given you are running on a GPU, you batch process self.cores number of images at a time.

        :param img_path_array: An array of self.cores number of images
        :return: A dict of the paths and their respective attribute vectors

        :raise GpuNotSupportedException -- This method will only work when your `self.backend == 'gpu'`
        """
        # Ensure that a cpu user is not accessing a GPU command
        if self.backend is not 'gpu':
            raise GpuNotSupportedException(self.backend)

        # Ensure there are enough (& not too many images) that are also available locally
        imgs_to_process, failed_images = self.get_images_to_process_for_NSEW(img_path_array)

        # Shift the focus around the 9 locations with the image
        imgs_urls_with_direction = []
        patches = []
        for local_img_url in imgs_to_process:
            im_data = imread(local_img_url).astype(float)

            # Get each patch around the image: NW, N, NE, W, mid, E, SW, S, SE
            # Fix the image into a flat array organised as [RRRRR..GGGGG..BBBB]
            for direction, patch in self.make_NSEW_image_patches(im_data).items():
                imgs_urls_with_direction.append(local_img_url+direction)
                patches.append(patch)

        # make an image buffer on host, pad out to batch size
        # Note: self.model.be.bsz == self.cores
        # Then fill it with each image patch
        host_buf = np.zeros((3 * self.patch_height * self.patch_width, self.model.be.bsz))
        for img_index in range(len(patches)):
            host_buf[:, img_index] = patches[img_index].copy()

        # make buffer on the device
        dev_buf = self.model.be.zeros((3 * self.patch_height * self.patch_width, self.model.be.bsz))
        # copy host buffer to device buffer
        dev_buf[:] = host_buf

        # Send through the network.
        predictions = self.model.fprop(dev_buf, True).asnumpyarray()[:, 0]
        # print predictions

        # Print the activations of the 4th layer from the end of the model
        # Note 1: model.layers represents a SingleOutputTree when using GoogLeNet;
        # during inference only the main branch (index 0) outputs are considered
        img_vector_dict = {}
        for img_index in range(len(imgs_urls_with_direction)):
            img_path = imgs_urls_with_direction[img_index]
            img_vect = self.model.layers.layers[0].layers[self.layer].outputs.asnumpyarray()[:, img_index].tolist()
            img_vector_dict[img_path] = img_vect

        return img_vector_dict, failed_images

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

    # Expects 256x256
    def make_NSEW_image_patches(self, im):
        # convert to BGR
        im = im[:, :, ::-1]

        # approximately mean-centre it
        im = im - [128, 128, 128]

        # Determine the region of the image not used to process
        image_width = im.shape[1]
        image_height = im.shape[0]

        x_remainder = image_width - 2 * int(self.patch_width / 2.0)
        y_remainder = image_height - 2 * int(self.patch_height / 2.0)

        # Determine the width of the horiz and vertical borders
        west_x = 0
        mid_x = x_remainder / 2
        east_x = image_width - self.patch_width

        north_y = 0
        mid_y = y_remainder / 2
        south_y = image_height - self.patch_height

        print image_width

        # Describe the position of the image (based on its top left point of the patch)
        # Assuming [0,0] is the top left point in the whole image
        factors = {
                   # North Level
                   '#NW': [west_x, north_y],
                   '#N': [mid_x, north_y],
                   '#NE': [east_x, north_y],
                   # Mid Level
                   '#W': [west_x, mid_y],
                   '#mid': [mid_x, mid_y],
                   '#E': [east_x, mid_y],
                   # South Level
                   '#SW': [west_x, south_y],
                   '#S': [mid_x, south_y],
                   '#SE': [east_x, south_y],
                   }
        patch_array_dict = {}
        for direction, coord in factors.items():
            top = coord[1]
            left = coord[0]
            bottom = top + self.patch_height
            right = left + self.patch_width

            # Cropping the image
            patch = im[top:bottom, left:right, :]

            # Neon wants the data as a flat array organised as [RRRRR..GGGGG..BBBB]
            patch_array_dict[direction] = patch.transpose((2, 0, 1)).flatten()

        return patch_array_dict

    def get_images_to_process(self, img_path_array):
        """
        Keeps the first self.cores number of images that can be found locally.

        :param img_path_array:
        :return: passed_images (array<string>) -- Up to self.cores number of images that it can process
         failed_images (dict<string,string>) -- The images that could not be found or excess images
        """
        failed_images = {}
        local_images = []
        for img_path in img_path_array:
            if image_is_local(img_path):
                local_images.append(img_path)
            else:
                failed_images[img_path] = 'Image not found locally'

        # If there are any more than self.cores number of images, ignore them
        for excess_img in local_images[self.cores:]:
            failed_images[excess_img] = 'Skipped, more than {} images'.format(self.cores)

        return local_images[:self.cores], failed_images

    def get_images_to_process_for_NSEW(self, img_path_array):
        """
        Keeps the first number of images that can be found locally.
        Given that there is enough for 9 of them to be processed.

        :param img_path_array:
        :return: passed_images (array<string>) -- Up to self.cores number of images that it can process
         failed_images (dict<string,string>) -- The images that could not be found or excess images
        """
        failed_images = {}
        local_images = []
        for img_path in img_path_array:
            if image_is_local(img_path):
                local_images.append(img_path)
            else:
                failed_images[img_path] = 'Image not found locally'

        # If there are any more than self.cores number of images, ignore them
        max_local_images = self.cores / 9
        for excess_img in local_images[max_local_images:]:
            failed_images[excess_img] = 'Skipped, more than {} images, as ({}+1) > {}' \
                .format(max_local_images, max_local_images, self.cores)

        return local_images[:max_local_images], failed_images


class GpuNotSupportedException(Exception):
    def __init__(self, backend):
        super(GpuNotSupportedException, self).__init__(
            "GpuNotSupportedException: The vectorizer has the backend '{}' not 'gpu'".format(backend))


class ImageNotFoundException(Exception):
    paths = []

    def __init__(self, paths):
        if paths is None or paths == []:
            raise AttributeError("paths is empty")
        self.paths = paths

        str_paths = ""
        for path in paths:
            str_paths += str(path) + os.linesep
        super(ImageNotFoundException, self).__init__(
            "File(s) Not Found: The following images do not exist{}{}".format(os.linesep, str_paths))


def image_is_local(img_path):
    return os.path.isfile(img_path)

