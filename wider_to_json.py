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
# Sample: python wider_to_json.py -- imgs_subfolder WIDER_train/images/
                                  #-- anns_subfolder wider_face_split/
# By defoult subfolder path for images: "WIDER_train/images/"
#for annotations extraction: "subfolder wider_face_split/"

imgs_dataset_archive = "WIDER_train.zip"
anns_dataset_archive = "wider_face_split.zip"
anns_subfolder = "wider_face_split"
imgs_subfolder = "WIDER_train/images/"
subdir_count = 62
subdir = []
#for shuffle
names = random.sample(range(1,100000), 100000-1)
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
        for line in file:
            if line[-5:-1] == ".jpg":
                f= open(divide_ann_folder + line.split("/")[1].split(".jpg")[0]+'.txt',"w+")
            if line[-5:-1] != ".jpg":
                l = line.split(" ")
                if len(l) < 2:
                    file_lines_count =int(line.split("/")[0])
                if len(l) > 2:
                    f.write(line)
        file.close()
def rename(root_list):
    for old_name in os.listdir(root_list):
        new_name = old_name.split("--")[0]
        os.rename(os.path.join(root_list, old_name),os.path.join(root_list, new_name))
        
def copy(subfolder, dir_path, names=None):
    common.copy(subfolder, dir_path, names=None)

def single_folder():
    for i in range(subdir_count):
        subdir.append( imgs_subfolder+str(i)+"/")
        copy(subdir[i], dir_imgs_will_be_extracted_to, names)
    shutil.rmtree( dir_imgs_will_be_extracted_to+"WIDER_train")

class WiderToJson(Parser):
    
    def __init__(self, imgs_subfolder, anns_subfolder):
        self.img = imgs_subfolder
        self.ann = anns_subfolder
        super(WiderToJson, self).__init__()

    def make_directories(self, sub_dir):
        super(WiderToJson, self).make_directories(sub_dir)
    
    def extract(self, archive, subfolder, dir_path):
        super(WiderToJson, self).extract(archive, subfolder, dir_path)

    def parse(self):
        """
        Definition: Parses divide_ann file to extract bounding boxcoordintates.
        """
        self.make_directories(directories)
        self.extract(imgs_dataset_archive, self.img, dir_imgs_will_be_extracted_to)
        self.extract(anns_dataset_archive, self.ann, dir_anns_will_be_extracted_to)
        #copy annotations into annotations folder
        copy(self.ann, dir_anns_will_be_extracted_to)
        make_divide_ann()
        #rename imgs subfolders to format "1"-"61"
        rename(dir_imgs_will_be_extracted_to+self.img)
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
        print(objects)
        return objects
        '''
        for i in objects:
            with open(json_dir+i["filename"].split('.')[0]+".json", "wt") as out_file:
                out_file.write(str(i))
        '''
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--imgs_subfolder", default=imgs_subfolder, required = False, help = "Images subfolder to extract from")
    ap.add_argument("--anns_subfolder", default=anns_subfolder, required = False, help = "Annotations subfolder to extract from")
    namespace = ap.parse_args(sys.argv[1:])
    wider =  WiderToJson(namespace.imgs_subfolder, namespace.anns_subfolder)
    wider.parse()
if __name__ == '__main__':
    main()