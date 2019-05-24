import unittest
import sys
from smoothing_images import noise_removal


class OpenCVTest(unittest.TestCase):
    """ Simple functionality tests. """

    def test_import(self):
        """ Test that the cv2 module can be imported. """
        import cv2

    def noise_removal_test(self):
        import cv2
        actual = cv2.imread(".jpg")
        crop = cv2.imread(".jpg")
        # Visualisation

    def augementator_test(self):
        import cv2
        actual = cv2.imread(".jpg")
        crop = cv2.imread(".jpg")
        # Visualisation