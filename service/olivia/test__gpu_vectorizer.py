import unittest
import os
import csv
from copy import deepcopy
from vectorizer import Vectorizer


class VectorizerTest(unittest.TestCase):
    def setUp(self):
        self.vec = Vectorizer(layer=-1, backend='gpu', cores=32)

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
        
        test_img_locs = [os.path.expanduser("~")+"/SaturnServer/test_resources/NSEW_test_img_1.jpg", os.path.expanduser("~")+"/SaturnServer/test_resources/NSEW_test_img_2.jpg"]
        
        for img in test_img_locs:
            print os.path.isfile(img) 
        

	regular_output = self.vec.get_attribute_vector(test_img_locs[0])
 
	print "regular output: {}".format(regular_output)
       
	NSEW_output, failed_images = self.vec.get_NSEW_batch_attribute_vectors(test_img_locs)
        print "Checking corners of NSEW output are different from regular output, but centre tiles are the same"
        
	corners = ["NE", "NW", "SE", "SW"]
	
	for url in NSEW_output:
		img = url.split("#")[0]
		coord = url.split("#")[1]
		if img == test_img_locs[0]:
			if coord not in corners:
				self.assertItemsEqual(NSEW_output[url], regular_output) 
   			else:	
				identicle = True
				for i in range(0, len(regular_output)):
					self.assertNotEqual(NSEW_output[url][i], regular_output[i])
		elif img == test_img_locs[1]:
			if coord == "NW":
				self.assertItemsEqual(NSEW_output[url], regular_output)
				for i in range(0, len(regular_output)):
					self.assertNotEqual(NSEW_output[url][i], NSEW_output[test_img_locs[0]+"#NW"][i])

if __name__ == '__main__':
    unittest.main()
