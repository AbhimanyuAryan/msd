import json
import glob
import io
from noise_removal import noise_removal # for removing noise in image 
from plain_search import template_match_coord # for plain straight iamge search
from augmentation import rotated_skewed_search # for rotation

cropped_images = glob.glob('./crops/*.jpg');
original_images = glob.glob('./images/*.jpg');

cloth_matches = dict() 

def insert_in_cloth_matches(actual_img, crop_img):
    if actual_img.split('/')[-1] not in cloth_matches:
        cloth_matches[actual_img.split('/')[-1]] = [[crop_img.split('/')[-1], coordinates]]
    else:
        cloth_matches[actual_img.split('/')[-1]].append([crop_img.split('/')[-1], coordinates])

if __name__=="__main__":
    cloth_matches = dict()  
    try:
      to_unicode = unicode
    except NameError:
      to_unicode = str

cloth_matches['NA'] = []
# plain image search & noise removal image
for crop in cropped_images:
    for actual in original_images:
        print(actual, crop)
        #cloth_matches[actual.split('/')[-1]] = []
        coordinates = template_match_coord(actual, crop)
        if coordinates != None:
            insert_in_cloth_matches(actual, crop)
            print(cloth_matches)
            break # if match found no need to check for noise & break
        coordinates = noise_removal(actual, crop)
        if coordinates != None:
            insert_in_cloth_matches(actual, crop)
            print(cloth_matches)
            break
        #else:
         #   cloth_matches['NA'].append([crop.split('/')[-1], []])
            

print(type(cloth_matches))

with io.open('res.json', 'w', encoding='utf-8') as outfile:
    str_ = json.dumps(cloth_matches,
                      indent=4, sort_keys=True,
                      separators=(',', ': '), ensure_ascii=False)
    outfile.write(to_unicode(str_))

"""
for crop in cropped_images:
    for actual in original_images:
        print(actual, crop)
        coordinates = rotated_skewed_search(actual, crop)
        if coordinates != None:
            insert_in_cloth_matches(actual, crop)
            print(cloth_matches)
            break
"""

