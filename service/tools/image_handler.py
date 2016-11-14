
import os
from datetime import datetime


def get_datetime():
    return str(datetime.now().strftime('%d.%m.%Y_%H.%M.%S'))


class ImageHandler:
    imageDir = '!Image Dir Not Set!'

    def __init__(self, loc):
        self.imageDir = loc

    def get_image_dir(self):
        return self.imageDir

    def new_location(self):
        """
        Creates a new filename for a .jpg image in the image directory on the Saturn Server based purely on the time asked

        :return: new unique file path
        """
        n = 0
        new_path = '%smap__%s__%d.jpg' % (self.get_image_dir(), get_datetime(),n)
        while os.path.isfile(new_path):
            n += 1
            new_path = '%smap__%s__%d.jpg' % (self.get_image_dir(), get_datetime(), n)
        return new_path
