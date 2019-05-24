import cv2
import numpy as np
from plain_search import template_match_coord
from augmentation import rotated_skewed_search

def noise_removal(full, crop):
    """
    Removes noise

    Parameters
    ----------
    :param image : original image
    :param crop: cropped image
    :return: [coordinates] or None
    """
    #averaging = cv2.blur(img, (5,5));
    #gaussian = cv2.GaussianBlur(img, (5,5), 0)
    crop = cv2.imread(crop)
    crop = cv2.medianBlur(crop, 5)
    #bi = cv2.bilateralFilter(img, 5, 75, 75) # Keeping the edges of image like for reading text and stuff & not blur

    cv2.imwrite('denoised.jpg', crop)

    # Then match with template or rotated
    coordinates = template_match_coord(full, 'denoised.jpg')
    #if coordinates == None:    
        #coordinates = rotated_skewed_search(full, 'denoised.jpg')
        #if coordinates == None:
            #return None
    return coordinates