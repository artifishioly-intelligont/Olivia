"""Takes an image patch and sends it through a network to the specified layer"""

import numpy as np

from neon import NervanaObject
from neon.util.persist import load_obj
from neon.backends import gen_backend
from neon.data import ArrayIterator
from neon.models import Model
from neon.util.argparser import NeonArgparser
from os.path import split, splitext, isfile
from scipy.misc import imread, imsave

#pretty printing full ndarrays
def ndprint(a, format_string ='{0:.5f}'):
    print [format_string.format(v,i) for i,v in enumerate(a)]


model_path = 'Googlenet_791113_192patch.prm'
model_URL = 'http://degas.ecs.soton.ac.uk/~productizer/Googlenet_791113_192patch.prm'

parser = NeonArgparser(__doc__)

parser.add_argument('--image', dest='image',
					help="A string path to the location of an image readable by scipy's imread")
parser.add_argument('--prm-name', dest='prm_name', default= model_path,
					help="The name of the prm to use as a model")
parser.add_argument('--layer', dest='layer_index', default=-4,
					help="The index of the layer to extract the activations from")

args = parser.parse_args()

# load the cnn model
gen_backend(batch_size=1, backend='cpu')
# gen_backend(batch_size=32, backend='gpu')

model_dict = load_obj(args.prm_name)
model = Model(model_dict)

# now we are going to extract the middle patch from the image, 
# based on the size used to train the model
patch_height = model_dict['train_input_shape'][1]
patch_width = model_dict['train_input_shape'][2]

# initialise the model so that internally the arrays are allocated to the correct size
model.initialize(model_dict['train_input_shape'])


# load the image
im = imread(args.image).astype(float)

# convert to BGR
im = im[:, :, ::-1]

# approximately mean-centre it
im = im - [128,128,128]

# Finding the co-ordinates for each corner of the centre patch
padY = int(patch_height / 2.0)
padX = int(patch_width / 2.0)
y = im.shape[0] - 2 * padY
x = im.shape[1] - 2 * padX
col = int(x / 2)
row = int(y / 2)

right = col + patch_width
left = col
top = row
bottom = row + patch_height

# Cropping the image
patch = im[top:bottom, left:right, :]

# Neon wants the data as a flat array organised as [RRRRR...GGGGG...BBBB]
patch_array = patch.transpose((2, 0, 1)).flatten()

# make an image buffer on host, pad out to batch size
host_buf = np.zeros((3*patch_height*patch_width, model.be.bsz))
# set the first image to be the image data loaded above
host_buf[:, 0] = patch_array.copy()

# make buffer on the device
dev_buf = model.be.zeros((3*patch_height*patch_width, model.be.bsz))
# copy host buffer to device buffer
dev_buf[:] = host_buf

# Send through the network. Note that in the returned array there 
# will be one column for each item in the batch; as we only put data
# in the first item, we only want the first column
predictions = model.fprop(dev_buf, True).asnumpyarray()[:,0]
# print predictions

# Print the activations of the 4th layer from the end of the model
# Note 1: model.layers represents a SingleOutputTree when using GoogLeNet;
# during inference only the main branch (index 0) outputs are considered
# Note 2: in the returned array there will be one column for each item 
# in the batch; as we only put data in the first item, we only want the 
# first column
ndprint(model.layers.layers[0].layers[int(args.layer_index)].outputs.asnumpyarray()[:,0])

