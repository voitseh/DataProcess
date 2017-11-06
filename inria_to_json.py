# Import necessary libraries
import os, sys
import numpy as np
from Parser import *
from Utils import common
from PIL import Image
from scipy.io import loadmat
from datetime import datetime

###########################################################
##########        INRIA PERSON to JSON Convector ##########
###########################################################

# This script is run from  console terminal
# Sample: C:\Users\User>python inria_to_json.py 

dataset_archive = "INRIAPerson.tar"
imgs_subfolder = "INRIAPerson/Train/pos/"
anns_subfolder = "INRIAPerson/Train/annotations/"
inria_path = 'datasets/INRIA/'
imgs_destination = os.path.join(inria_path, 'images/')
anns_destination = os.path.join(inria_path, 'annotations/')
json_dir = 'datasets/JSON_INRIA/'
directories = [json_dir,imgs_destination, anns_destination]

ap = argparse.ArgumentParser()
ap.add_argument("--images", default=imgs_subfolder, required = False, help = "Images subfolder to extract from")
ap.add_argument("--annotations", default=anns_subfolder, required = False, help = "Annotations subfolder to extract from")
namespace = ap.parse_args(sys.argv[1:])

class InriaToJson(Parser):
   
    def __init__(self):
        common.make_directories(directories)
        extract_archive(dataset_archive, inria_path)
        for filename in os.listdir(os.path.join(inria_path, namespace.images)):
            common.png_to_jpg_converter('{}{}{}'.format(inria_path,namespace.images,filename), imgs_destination)
        common.copy_files(os.path.join(inria_path, namespace.annotations), anns_destination)
        super(InriaToJson, self).__init__()
    
    def parse(self):
        """
        Definition: Parses label file to extract label and bounding box
        coordintates.
        """
        objects = []   
        object_info = {}
        coords = []
        for f in os.listdir(anns_destination):
            object_info['filename'] = os.path.join(f.split(".")[0],".jpg")
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
                file = os.path.join(json_dir, i["filename"].split('.')[0])
                with open("{}.json".format(file), "wt") as out_file:
                    out_file.write(str(i))
                
def main():
    inria =  InriaToJson()
    inria.parse()
if __name__ == '__main__':
    main()


