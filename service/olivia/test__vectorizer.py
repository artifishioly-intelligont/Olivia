import unittest
from vectorizer import Vectorizer
import os
from time import gmtime, strftime

def roundArray(arr, places=4):
    return [float(int(10**places * n))/10**places for n in arr]

default_prm_path = os.path.expanduser('~')+'/SaturnServer/Googlenet_791113_192patch.prm'

image_loc =  os.path.expanduser('~')+'/SaturnServer/test_resources/test_tile.jpg'

class VectorizerTest(unittest.TestCase):

    def test_regression__vectorizer_layer_minus_one_behaves_same(self):
        # GIVEN a layer to test
        layer_under_test = -1

        # AND a vectorizer that uses that layer
        vec = Vectorizer(layer=layer_under_test, prm_path=default_prm_path, backend='cpu')

        # AND an expected output
        expected_output = [0.0016, 0.9883, 0.0099, 0.00]

        #
        # WHEN extracting the attributes from an image
        print 'This test has not stalled, it takes 20-40 seconds on an fast-ish computer (%s)' % strftime("%H:%M:%S", gmtime())
        actual_output = roundArray(vec.get_attribute_vector(image_loc))

        #
        # THEN the output is as expected
        self.assertEqual(expected_output, actual_output, 'The output %s, does not match the expected output of %s' % (str(actual_output), str(expected_output)))

    def test_regression__vectorizer_layer_minus_four_behaves_same(self):
        # GIVEN a layer to test
        layer_under_test = -4

        # AND a vectorizer that uses that layer
        vec = Vectorizer(layer=layer_under_test, prm_path=default_prm_path, backend='cpu')

        # AND an expected output stored in a file
        expected_output_file_path = os.path.expanduser('~')+'/SaturnServer/test_resources/layer4results.txt'

        #
        # WHEN extracting the attributes from an image
        print 'This test has not stalled, it takes 20-40 seconds on an fast-ish computer (%s)' % strftime("%H:%M:%S", gmtime())
        actual_output = roundArray(vec.get_attribute_vector(image_loc))

        #
        # THEN each element of the actual output array must match each element of the expected results
        with open(expected_output_file_path, 'r') as expected_output_file:
            element_no = 0
            for expected_element in expected_output_file:
                self.assertEqual(float(expected_element), actual_output[element_no],
                                 'The output (element %d) %s, does not match the expected output of %s'
                                 % (element_no, str(actual_output[element_no]), str(expected_element)))
                element_no += 1



if __name__ == '__main__':
    unittest.main()