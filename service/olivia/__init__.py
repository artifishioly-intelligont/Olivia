import socket
from vectorizer import Vectorizer

# Determine which machine the code is running on
# myrtle is the only machine capable of running on GPU
backend = 'cpu'
cores = 1
if socket.gethostname() == 'myrtle':
    backend = 'gpu'
    cores = 16

converter = Vectorizer(backend=backend, cores=cores)


def get_attr_vec(img_path):
    vec = converter.get_attribute_vector(img_path)
    return vec.tolist()


def get_all_vecs(img_paths):
    return converter.get_batch_attribute_vectors(img_path_array=img_paths)


def get_vecs_with_NSEW(img_paths):
    return converter.get_NSEW_batch_attribute_vectors(img_path_array=img_paths)
