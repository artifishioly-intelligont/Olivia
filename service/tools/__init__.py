"""
This module is reserved for arbitrary helper functions
"""
import os

from downloader import DownloadException
import downloader
from image_handler import ImageHandler

images = ImageHandler('%s/SaturnServer/images/' % os.path.expanduser('~'))


def download(url):
    local_img_loc = images.new_location()
    downloader.download(url, local_img_loc)
    return local_img_loc
