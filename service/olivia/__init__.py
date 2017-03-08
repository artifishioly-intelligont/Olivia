import socket
from vectorizer import Vectorizer
from Lock import Lock


# Determine which machine the code is running on
# myrtle is the only machine capable of running on GPU
backend = 'cpu'
cores = 1

if socket.gethostname() == 'myrtle':
    backend = 'gpu'
    cores = 16

converter = Vectorizer(backend=backend, cores=cores)
backend_lock = Lock()


def get_all_vecs(img_paths):
    if backend_lock.is_locked():
        backend_lock.lock()
        img_vector_dict, failed_images = converter.get_batch_attribute_vectors(img_path_array=img_paths)
        backend_lock.unlock()
        return img_vector_dict, failed_images
    else:
        return {}, {img: 'Backend busy: Request ignored' for img in img_paths}


def get_vecs_with_NSEW(img_paths):
    if backend_lock.is_locked():
        backend_lock.lock()
        img_vector_dict, failed_images = converter.get_NSEW_batch_attribute_vectors(img_path_array=img_paths)
        backend_lock.unlock()
        return img_vector_dict, failed_images
    else:
        return {}, {img: 'Backend busy: Request ignored' for img in img_paths}

