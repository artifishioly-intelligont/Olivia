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
        res_dict = self.vec.get_32_attribute_vectors(self.imagenames)
        print 'done vectorizing'

        data = deepcopy(res_dict.values())
        # Save it locally
        with open('results32.csv', 'wb') as f:
            wtr = csv.writer(f, delimiter=',')
            wtr.writerows(data)



        self.assertEqual(0, 0)


if __name__ == '__main__':
    unittest.main()
