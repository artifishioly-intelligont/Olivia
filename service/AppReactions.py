import json
import olivia
import tools
from tools import DownloadException


def unknown_method(endpoint):
    return "<h1>Incorrect Usage</h1> \
    <br> {} does not know what to do with this request type".format(endpoint)


def convert_get():
    return "<h1>Incorrect Usage</h1>\
    <br>/convert only accepts POST\
    <br>POST expects a number of files to be sent to it"


def convert_post(urls):
    """
    :param urls -- an array of urls of the images that we want to convert into vectors

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
    """
    image_vectors = {}
    failed_images = {}
    for url in urls:
        try:
            # Download image from URL
            local_img_loc = tools.download(url)
            print 'Downloaded image'

            # Convert local image to vector
            image_vectors[url] = olivia.get_attr_vec(local_img_loc)
            print 'arr({}): {}'.format(type(image_vectors[url]), image_vectors[url])


        except DownloadException as ex:
            failed_images[url] = ex.message
            print 'Fails: {}'.format(ex.message)

    success = len(failed_images) == 0
    data = {'success': success, 'image_vectors': image_vectors, 'failed_images': failed_images}

    return json.dumps(data)

