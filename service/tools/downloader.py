import urllib, imghdr, os


def download(url, local_dest):
    """
    Downloads a file from any URL path

    :param url: where in the file is stored on another machine
    :param local_dest: Where the file should be saved to e.g. ~/SaturnServer/images/map__20.10.2016_20.32.45.jpg
    """
    try:
        urllib.urlretrieve(url, local_dest)
    except IOError as ex:
        raise DownloadException(url, local_dest, exception=ex)

    if not was_image_found(local_dest):
        os.remove(local_dest)
        raise DownloadException(url, local_dest,
                        message='There was no file at the location:  %s \n'
                        'Deleting the file at %s' % (url, local_dest))


def was_image_found(local_dest):
    """
    Determines if the file at the path is an image

    :param local_dest: The location of the file under question

    :return <boolean> true if the download was an image
    """
    # This function returns null if the file is not an image or returns a string if it is
    return not not imghdr.what(local_dest)

class DownloadException(Exception):
    def __init__(self, url, local_dest, message=None, exception=None):
        extra = ''
        if message:
            extra ="\n\tMessage: {}".format(message)

        super(DownloadException, self).__init__(
            "DownloadException: Cannot download \'{}\' and store it in \'{}\'".format(url,local_dest,message)+extra)

        self.url = url
        self.local_dest = local_dest
        self.exception = exception
