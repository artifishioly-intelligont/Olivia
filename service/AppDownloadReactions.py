import memory
import random
import AppConvertReactions as react
import json

def download_get():
    return "<h1>Incorrect Usage</h1>\
        <br>/download only accepts POST\
        <br>POST expects list of urls and optionally an id for each of them"


def download_post(urls, ids):
    #Genereate the map of ids to urls
    if len(ids) == 0:
        url_to_id_map = create_ids(urls)
    else:
        url_to_id_map = zip(urls, urls)

    try:
        data = react.convert_post_gpu(urls)
        passed_images = data["image_vectors"]
        failed_images = data["failed_images"]

    except Exception as e:
        return {'success': False,
                'downloaded_vectors': [],
                'failed_images': {url: e.message for url in urls}}

    for url, vector in passed_images.items():
        image_id = url_to_id_map[url]
        print url, image_id, vector[0:3]
        memory.remember(image_id, vector)

    data = {'success': len(failed_images) == 0,
            'downloaded_vectors': passed_images.keys(),
            'failed_images': failed_images}
    return data


def create_ids(urls):
    """ Take a list of urls and return a list corresponding ids
     An ID can be extracted from urls sent from the GUI server
     """
    url_to_decoded_id_map = {}
    for url in urls:
        if memory.is_url_from_gui(url):
            decoded_id = memory.decode_url_sent_from_gui(url)
        else:
            # Random id
            decoded_id = str(-random.uniform(1000, 9999)) + \
                         "_"+str(random.uniform(1000, 9999))+"_"+str(random.uniform(1000, 9999))
        url_to_decoded_id_map[url] = decoded_id
    return url_to_decoded_id_map

