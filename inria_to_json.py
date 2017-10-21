# Import necessary libraries
import os, sys
import numpy as np
from Parser import *
from PIL import Image
from scipy.io import loadmat
from datetime import datetime

python_version = sys.version_info.major

###########################################################
##########        INRIA PERSON to JSON Convector ##########
###########################################################

# This script is run from  console terminal
# Sample: C:\Users\User>python inria_to_json.py
# You can also specify images or/and annotations subfolder in dataset archive
# you will extract files from wich.
# Sample: python InriaToJson.py --imgs_subfolder INRIAPerson/Train/pos/
# By defoult subfolder path for images extraction: "INRIAPerson/Train/pos/"
#for annotations extraction: "INRIAPerson/Train/annotations/"
    
dataset_archive = "INRIAPerson.tar"
imgs_subfolder = "INRIAPerson/Train/pos/"
anns_subfolder = "INRIAPerson/Train/annotations/"
imgs_destination = 'datasets/INRIA/images/'
anns_destination = 'datasets/INRIA/annotations/'
json_dir = 'datasets/JSON_INRIA/'
directories = [json_dir,imgs_destination, anns_destination]

class InriaToJson(Parser):
   
    def parse(self):
        """
        Definition: Parses label file to extract label and bounding box
        coordintates.
        """
        objects = []   
        object_info = {}
        coords = []
        for f in os.listdir(anns_destination):
            object_info['filename'] = f.split(".")[0]+".jpg"
            object_info['objects'] = []

            with open(anns_destination+f) as f:
                data = f.read()

            import re
            objs = re.findall('\(\d+, \d+\)[\s\-]+\(\d+, \d+\)', data)
            num_objs = len(objs)
            boxes = np.zeros((num_objs, 4), dtype=np.uint16)
            # Load object bounding boxes into a data frame.
            for ix,  obj in enumerate(objs):
                # Make pixel indexes 0-based
                coor = re.findall('\d+', obj)
                x1 = int(coor[0])
                y1 = int(coor[1])
                x2 = int(coor[2])
                y2 = int(coor[3])

                tmp = [x1,y1,x2,y2]
                coords.append(tmp)
                person_info = {'class_name':'Person'}
                person_info ['bounding_box'] = tmp
                object_info['objects'].append(person_info)
                objects.append(object_info.copy())
                tmp = []
        return objects
def main():
    inria =  InriaToJson()
    namespace = Parser.createParser (imgs_subfolder, anns_subfolder, None)
    inria.make_directories(directories)
    inria.extract(dataset_archive, namespace.imgs_subfolder, imgs_destination)
    inria.extract(dataset_archive, namespace.anns_subfolder, anns_destination)
    inria.populate_json_ann(json_dir,inria.parse())

if __name__ == '__main__':
    main()


