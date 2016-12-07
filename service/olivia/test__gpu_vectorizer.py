import unittest
import os
import csv
from copy import deepcopy
from vectorizer import Vectorizer


class VectorizerTest(unittest.TestCase):
    def setUp(self):
        self.vec = Vectorizer(layer=-1, backend='gpu', cores=512)

        # Generate a list of images
        base_image = os.path.expanduser('~') + '/SaturnServer/test_resources/map_image'
        self.imagenames = []
        for i in range(1, self.vec.cores+1):
            self.imagenames.append("{}{}.jpg".format(base_image, i))

    def test_32_image_processing(self):
        print 'About to vectorize'
        res_dict, failed_imgs = self.vec.get_batch_attribute_vectors(self.imagenames)

        print 'done vectorizing, results'
        print '-[Passed Images]-----'
        for url, vec in res_dict.items():
            print "{}- {}".format(url.split("/")[-1], vec)

        print '-[Failed Images]-----'
        for url, issue in failed_imgs.items():
            print "{}- {}".format(url, issue)
        print '------'

        self.assertEqual(len(res_dict), len(self.imagenames),
                         "There number of outputs ({}) should match the number of inputs: {}"
                         .format(len(res_dict),len(self.imagenames)))
        self.assertEqual(len(failed_imgs), 0, "There should be no failed images")
        print 'done vectorizing, results'
        print '------'
        i = 1
        for vec in res_dict.values():
            print "map_image{}- {}".format(i, vec)
            i += 1
        print '------'
        
    def test_NSEW(self):
        vec = Vectorizer(prm_path=default_prm_path, backend='gpu')
        
        test_img_locs = ["../../test_resources/NSEW_test_img_1.jpg", "../../test_resources/NSEW_test_img_1.jpg"]
        
        for img in test_img_locs:
            print os.path.isfile(img)
        
        print "Determining regular output"
        
        regular_output = vec.get_attribute_vector(test_img_locs)
        
        print "Regular output: "
        print regular_output[0:3]
        
        print "Now getting NSEW output"
        NSEW_output, failed_images = vec.get_NSEW_batch_attribute_vectors(test_img_locs)
        print "NSEW output received. Checking corners"
        
        for name, vec in NSEW_output:
            print name
            
        print failed_images

        self.assertEqual(True, True)


if __name__ == '__main__':
    unittest.main()
