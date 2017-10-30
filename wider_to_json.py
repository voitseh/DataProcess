# Import necessary libraries
import os, sys, shutil, glob, argparse
import numpy as np
import random
from Parser import *
from Utils import common

###########################################################
##########       WIDER to JSON_WIDER Conversion       ##########
###########################################################

# This script is run from console terminal
# Sample: C:\Users\User>python wider_to_json.py
# You can also specify images and annotations subfolder in dataset archive
# you will extract files from wich.

wider_dir = 'datasets/WIDER/'
imgs_dataset_archive = "WIDER_train.zip"
anns_dataset_archive = "wider_face_split.zip"
anns_subfolder = os.path.join(wider_dir, "wider_face_split/")
imgs_subfolder = "WIDER_train/images/"
subdir_count = 62
subdir = []

dir_imgs_will_be_extracted_to = os.path.join(wider_dir, 'images/')
divide_ann_folder = os.path.join(wider_dir, 'divide_ann/')

json_dir = 'datasets/JSON_WIDER/'
directories = [dir_imgs_will_be_extracted_to, anns_subfolder, divide_ann_folder, json_dir ]

ap = argparse.ArgumentParser()
ap.add_argument("--images", default=imgs_subfolder, required = False, help = "Images subfolder to extract from")
ap.add_argument("--annotations", default=anns_subfolder, required = False, help = "Annotations subfolder to extract from")
namespace = ap.parse_args(sys.argv[1:])

def make_divide_ann():
        """
        Definition: Populate divide_ann with separate ann files.
        Returns: None
        """
        filename = os.path.join(anns_subfolder, 'wider_face_train_bbx_gt.txt') 
        file = open(filename)
        # Iterate through wider annotation data
        for line in file:
            if line[-5:-1] == ".jpg":
                f= open(divide_ann_folder + line.split("/")[1].split(".jpg")[0]+'.txt',"w+")
            else:
                l = line.split(" ")
                file_lines_count =int(line.split("/")[0]) if len(l) < 2 else  f.write(line)
        file.close()

def rename_files(folder_path):
    if os.path.exists(folder_path):
        for old_name in os.listdir(folder_path):
            new_name = old_name.split("--")[0]
            os.rename(os.path.join(folder_path, old_name),os.path.join(folder_path, new_name))
    else:  print(folder_path + " is not exist!")

def single_folder():
    for i in range(subdir_count):
        subdir.append( imgs_subfolder+str(i)+"/")
        common.copy_files(dir_imgs_will_be_extracted_to+subdir[i], dir_imgs_will_be_extracted_to)

class WiderToJson(Parser):
    
    def __init__(self):
       super(WiderToJson, self).__init__()

    def parse(self):
        """
        Definition: Parses divide_ann file to extract bounding boxcoordintates.
        """
        common.remove_directories(directories)
        common.make_directories(directories)
        extract_archive(imgs_dataset_archive, dir_imgs_will_be_extracted_to)
        extract_archive(anns_dataset_archive, wider_dir)
        make_divide_ann()
        #rename imgs subfolders to format "1"-"61"
        rename_files(os.path.join(dir_imgs_will_be_extracted_to+imgs_subfolder))
        #Copy images to single folder
        single_folder()
        common.remove_directory(os.path.join(dir_imgs_will_be_extracted_to,"WIDER_train"))

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