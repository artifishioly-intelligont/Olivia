import unittest
import os
import csv
from copy import deepcopy
from vectorizer import Vectorizer


class VectorizerTest(unittest.TestCase):

    def setUp(self):
        self.vec = Vectorizer(layer=-1)

        # Generate a list of images
        base_image = os.path.expanduser('~') + '/SaturnServer/test_resources/map_image'
        self.imagenames = []
        for i in range(1, 33):
            self.imagenames.append("{}{}.jpg".format(base_image, i))

    def test_32_image_processing(self):
        print 'About to vectorize'
        res_dict, failed_imgs = self.vec.get_32_attribute_vectors(self.imagenames)

        self.assertEqual(len(res_dict), len(self.imagenames), "There should be no failed images")
        self.assertEqual(len(failed_imgs), 0, "There should be no failed images")
        print 'done vectorizing, results'
        print '------'
	i = 1
        for vec in res_dict.values():
            print "map_image{}- {}".format(i,vec)
	    i += 1
        print '------'


if __name__ == '__main__':
    unittest.main()
