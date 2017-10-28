# Import necessary libraries
import os, sys
import numpy as np
from Parser import *
from Utils import common
from PIL import Image
from scipy.io import loadmat
from datetime import datetime

python_version = sys.version_info.major

###########################################################
##########        INRIA PERSON to JSON Convector ##########
###########################################################

# This script is run from  console terminal
# Sample: C:\Users\User>python inria_to_json.py 

dataset_archive = "INRIAPerson.tar"
imgs_subfolder = "INRIAPerson/Train/pos/"
anns_subfolder = "INRIAPerson/Train/annotations/"
imgs_destination = 'datasets/INRIA/images/'
anns_destination = 'datasets/INRIA/annotations/'
json_dir = 'datasets/JSON_INRIA/'
directories = [json_dir,imgs_destination, anns_destination]


class InriaToJson(Parser):
   
    def __init__(self):
        # TODO asked you to move arguments parse from here. They should not be here
        self.ap = argparse.ArgumentParser()
        self.ap.add_argument("--images", default=imgs_subfolder, required = False, help = "Images subfolder to extract from")
        self.ap.add_argument("--annotations", default=anns_subfolder, required = False, help = "Annotations subfolder to extract from")
        self.namespace = self.ap.parse_args(sys.argv[1:])
        super(InriaToJson, self).__init__()
    
    def parse(self):
        """
        Definition: Parses label file to extract label and bounding box
        coordintates.
        """
        make_directories(directories)
        extract(dataset_archive, self.namespace.images, imgs_destination)
        extract(dataset_archive, self.namespace.annotations, anns_destination)
        common.png_to_jpg_converter(imgs_destination)
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
                tmp =list(map( lambda x:int(x), coor))
                coords.append(tmp)
                person_info = {'class_name':'Person'}
                person_info ['bounding_box'] = tmp
                object_info['objects'].append(person_info)
                objects.append(object_info.copy())
                tmp = []
            for i in objects:
                with open(json_dir+i["filename"].split('.')[0]+".json", "wt") as out_file:
                    out_file.write(str(i))

def main():
    inria =  InriaToJson()
    inria.parse()
if __name__ == '__main__':
    main()


