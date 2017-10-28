# Import necessary libraries
import os, sys, shutil, glob, argparse
import numpy as np
import random
from Parser import *
from Utils import common

python_version = sys.version_info.major

###########################################################
##########       WIDER to JSON_WIDER Conversion       ##########
###########################################################

# This script is run from console terminal
# Sample: C:\Users\User>python wider_to_json.py
# You can also specify images and annotations subfolder in dataset archive
# you will extract files from wich.

imgs_dataset_archive = "WIDER_train.zip"
anns_dataset_archive = "wider_face_split.zip"
anns_subfolder = "wider_face_split"
imgs_subfolder = "WIDER_train/images/"
subdir_count = 62
subdir = []
dir_imgs_will_be_extracted_to = 'datasets/WIDER/images/'
dir_anns_will_be_extracted_to = 'datasets/WIDER/annotations/'
divide_ann_folder = 'datasets/WIDER/divide_ann/'
json_dir = 'datasets/JSON_WIDER/'
directories = [dir_imgs_will_be_extracted_to, dir_anns_will_be_extracted_to, divide_ann_folder, json_dir ]

def make_divide_ann():
        """
        Definition: Populate divide_ann with separate ann files.
        Returns: None
        """
        filename = os.path.join(dir_anns_will_be_extracted_to+ 'wider_face_train_bbx_gt.txt') 
        file = open(filename)
        # Iterate through wider annotation data
        
        # TODO same problem with if
        for line in file:
            if line[-5:-1] == ".jpg":
                f= open(divide_ann_folder + line.split("/")[1].split(".jpg")[0]+'.txt',"w+")
            if line[-5:-1] != ".jpg":
                l = line.split(" ")
                file_lines_count =int(line.split("/")[0]) if len(l) < 2 else  f.write(line)
        file.close()
def rename(root_list):
    for old_name in os.listdir(root_list):
        new_name = old_name.split("--")[0]
        os.rename(os.path.join(root_list, old_name),os.path.join(root_list, new_name))

def single_folder():
    for i in range(subdir_count):
        subdir.append( imgs_subfolder+str(i)+"/")
        common.copy(dir_imgs_will_be_extracted_to+subdir[i], dir_imgs_will_be_extracted_to)
    common.delete_dir(dir_imgs_will_be_extracted_to+"WIDER_train")

class WiderToJson(Parser):
    
    def __init__(self):
        self.ap = argparse.ArgumentParser()
        self.ap.add_argument("--images", default=imgs_subfolder, required = False, help = "Images subfolder to extract from")
        self.ap.add_argument("--annotations", default=anns_subfolder, required = False, help = "Annotations subfolder to extract from")
        self.namespace = self.ap.parse_args(sys.argv[1:])
        super(WiderToJson, self).__init__()

   
    def parse(self):
        """
        Definition: Parses divide_ann file to extract bounding boxcoordintates.
        """
        make_directories(directories)
        extract(imgs_dataset_archive, self.namespace.images, dir_imgs_will_be_extracted_to)
        extract(anns_dataset_archive, self.namespace.annotations, dir_anns_will_be_extracted_to)
        #copy annotations into annotations folder
        common.copy(dir_anns_will_be_extracted_to+anns_subfolder, dir_anns_will_be_extracted_to)
        common.delete_dir(dir_anns_will_be_extracted_to+anns_subfolder)
        make_divide_ann()
        #rename imgs subfolders to format "1"-"61"
        rename(dir_imgs_will_be_extracted_to+imgs_subfolder)
        #Copy images to single folder
        single_folder()
        objects = []   
        object_info = {}
        for f in os.listdir(divide_ann_folder):
            lfile = open(divide_ann_folder+f)
            object_info['filename'] = f.split(".")[0]+".jpg"
            object_info['objects'] = []
            coords = []
            coor = []
            # Load object bounding boxes.
            for line in lfile:
                coor = line.split(" ")[0:4]
                x1 = int(coor[0])
                y1 = int(coor[1])
                x2 = int(coor[0])+int(coor[2])
                y2 = int(coor[1])+int(coor[3])
                tmp = [x1,y1,x2,y2]
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
    wider =  WiderToJson()
    wider.parse()
if __name__ == '__main__':
    main()
