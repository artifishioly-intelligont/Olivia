import socket
from vectorizer import Vectorizer

# Determine which machine the code is running on
# myrtle is the only machine capable of running on GPU
backend = 'cpu'
if socket.gethostname() == 'myrtle':
    backend = 'gpu'

converter = Vectorizer(backend=backend)


def get_attr_vec(img_path):
    vec = converter.get_attribute_vector(img_path)
    return vec.tolist()


def get_all_vecs(img_paths):
    return converter.get_batch_attribute_vectors(img_path_array=img_paths)
