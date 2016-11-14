import urllib, imghdr, os


def download(file_name, local_dest):
    """
    Downloads a file from any location on http://degas.ecs.soton.ac.uk/~productizer/

    :param file_name: where in the productizer space it is stored e.g. 'images/map1.jpg' that we want to download
    :param local_dest: Where the file should be saved to e.g. ~/SaturnServer/images/map__20.10.2016_20.32.45.jpg
    """
    url = "http://degas.ecs.soton.ac.uk/~productizer/%s" % file_name
    urllib.urlretrieve(url, local_dest)
    if not was_image_found(local_dest):
        os.remove(local_dest)
        raise Exception('There was no file at the location:  %s \n'
                        'Deleting the file at %s' % (url, local_dest))



def download_image(image_name, local_dest):
    """
    Downloads a file from any location on http://degas.ecs.soton.ac.uk/~productizer/

    :param image_name: Which image  in the productizer images folder to download
    :param local_dest: Where the file should be saved to e.g. ~/SaturnServer/images/map__20.10.2016_20.32.45.jpg
    """
    download('images/' + image_name, local_dest)



def was_image_found(local_dest):
    """
    Determines if the file at the path is an image

    :param local_dest: The location of the file under question

    :return <boolean> true if the download was an image
    """
    # This function returns null if the file is not an image or returns a string if it is
    return not not imghdr.what(local_dest)