import cv2
import numpy as np
import os
import logging 

def template_match_coord(image, crop):
    """
    Matches straight images and return coordinates
    Parameters
    ----------
    :param image : original image
    :param crop: cropped image
    :return: None or Coordinates
    """
    image = cv2.imread(image)
    crop = cv2.imread(crop)

    h1, w1, c1 = image.shape
    h2, w2, c2 = crop.shape

    if h1 > h2 and w1 > w2:
        w, h = crop.shape[:-1]
        res = cv2.matchTemplate(image, crop, cv2.TM_CCOEFF_NORMED)
        threshold = .8
        loc = np.where(res >= threshold)
        if loc:
            for pt in zip(*loc[::-1]):  # Switch collumns and rows
              #  cv2.rectangle(image, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)
                coord = [pt[0], pt[1], pt[0]+w, pt[1]+h]
                coord = [float(np_float) for np_float in coord]
                return coord
    
    return None

