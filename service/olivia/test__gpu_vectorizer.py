import unittest
import os
from vectorizer import Vectorizer


class VectorizerTest(unittest.TestCase):

    def setUp(self):
        self.vec = Vectorizer()

        # Generate a list of images
        base_image = os.path.expanduser('~') + '/SaturnServer/test_resources/map_image'
        self.imagenames = []
        for i in range(1, 33):
            self.imagenames.append("{}{}.jpg".format(base_image, i))

    def test_32_image_processing(self):
        print 'About to vectorize'
        self.vec.get_32_attribute_vectors(self.imagenames)
        print 'done vectorizing'
        self.assertEqual(0, 1)


if __name__ == '__main__':
    unittest.main()
