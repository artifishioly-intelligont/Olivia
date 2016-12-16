import json
from collections import Set

import olivia
import memory
import tools
from tools import DownloadException


def unknown_method(endpoint):
    return "<h1>Incorrect Usage</h1> \
    <br> {} does not know what to do with this request type".format(endpoint)


def convert_get():
    return "<h1>Incorrect Usage</h1>\
    <br>/convert only accepts POST\
    <br>POST expects a number of files to be sent to it"


def convert_post_gpu(url_to_id_map, nsew_mode=False):
    """ Given a list of urls it returns the vectors from memory or direct processing """
    image_vectors = {}
    failed_images = {}

    if nsew_mode:
        nsew_urls_to_ids_map = {url+"#"+nsew : id+"#"+nsew
                                for url, id in url_to_id_map.items()
                                for nsew in ["NW", "N", "NE", "W", "mid", "E", "SW", "S", "SE"]}
        url_to_id_map = nsew_urls_to_ids_map

    urls_to_process = set()
    # Populate the images from knowledge
    for url, id in url_to_id_map.items():
        vector = memory.get_vec(id)
        if not vector:
            urls_to_process.add(url.split('#')[0])
        else:
            image_vectors[url] = vector

    # If the id is unrecognised, do it now!
    if len(urls_to_process) > 0:
        data = convert_post_gpu_raw(urls_to_process, nsew_mode)
        failed_images = data['failed_images']
        image_vectors.update(data['image_vectors'])

        # Remember the result of each of these new images
        for url, vector in data['image_vectors'].items():
            memory.remember_vec(url_to_id_map[url], vector)

    return {'success': len(failed_images) == 0,
            'image_vectors': image_vectors,
            'failed_images': failed_images}


def convert_post_gpu_raw(urls, nsew_mode=False):
    """
    :param urls -- an array of remote urls of the images that we want to convert into vectorsg
    :param nsew_mode -- Extract 9 vectors from one image

    :return:
    example (successful) return:
    {
        success : True,
        image_vectors :
        [
            { 'url1' : [0.1, 0.0, 0.5, ...] },
            { 'url2' : [0.9, 1.2, 0.6, ...]}
        ],
        failed_images : []
    }
    example (failed) return:
    {
        success : False,
        image_vectors :
        [
            { 'url1' : [0.1, 0.0, 0.5, ...] }
        ],
        failed_images :
        [
            { 'url2' : 'DownloadException: The path url2 does not exist'}
        ]
    }
    """
    # Download all the images
    vectorized_remote_urls = {}
    local_urls_to_remote_urls, failed_remote_urls = download_all_images(urls)

    # Ensure we have at least 1 image to process
    if len(local_urls_to_remote_urls) == 0:
        return {'success': False,
                'image_vectors': {},
                'failed_images': failed_remote_urls}

    # Batch them up in the size stored in 'olivia.cores'
    local_url_paths = local_urls_to_remote_urls.keys()
    if nsew_mode:
        batch_size = olivia.cores/9
    else:
        batch_size = olivia.cores

    # no of batches = no of full batches and an extra if the remainder > 0
    no_of_batches = len(local_url_paths)/batch_size + ((len(local_url_paths)%batch_size)>0)

    # Iterate through the batches
    for i in range(no_of_batches+1):
        # Get a batch of 'olivia.cores' (or the remainder) and process them
        startIndex = i * batch_size
        endIndex = min((i+1)*batch_size, len(local_url_paths))
        local_url_batch = local_url_paths[startIndex:endIndex]

        # Vectorize the images at the local urls
        if nsew_mode:
            vectorized_local_urls, failed_local_urls = olivia.get_vecs_with_NSEW(local_url_batch)
            # Update the successfully vectorized urls
            for local_url_with_direction in vectorized_local_urls:
                local_url = local_url_with_direction.split("#")[0]
                direction = local_url_with_direction.split("#")[1]

                vector = vectorized_local_urls[local_url_with_direction]
                remote_url = "{}#{}".format(local_urls_to_remote_urls[local_url], direction)
                vectorized_remote_urls[remote_url] = vector
        else:
            vectorized_local_urls, failed_local_urls = olivia.get_all_vecs(local_url_batch)
            # Update the successfully vectorized urls
            for local_url in vectorized_local_urls:
                vector = vectorized_local_urls[local_url]
                remote_url = local_urls_to_remote_urls[local_url]
                vectorized_remote_urls[remote_url] = vector

        # Update the failed vectorized urls with the recently failed local urls
        for failed_local_url in failed_local_urls:
            error = failed_local_urls[failed_local_url]
            remote_url = local_urls_to_remote_urls[failed_local_url]
            failed_remote_urls[remote_url] = error

    success = len(failed_remote_urls) == 0
    data = {'success': success,
            'image_vectors': vectorized_remote_urls,
            'failed_images': failed_remote_urls}

    return data

def download_all_images(urls):
    """ Given a list of URLS, downloads all retrievable images and returns two dictionaries.

     :returns
     passed_images dict<string,string> -- local urls -> remote url mappings
     failed_images dict<string,string> -- remote url -> failure message mappings
     """
    passed_images = {}
    failed_images = {}
    for url in urls:
        try:
            local_img_loc = tools.download(url)
            passed_images[local_img_loc] = url
        except (DownloadException, Exception) as ex:
            failed_images[url] = ex.message
    return passed_images, failed_images


