# Import necessary libraries
import os, sys, shutil, glob, argparse
import numpy as np
import random
from Parser import *

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

class WiderToJson(Parser):
    
    def make_divide_ann(self):
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
    def parse(self):
        """
        Definition: Parses divide_ann file to extract bounding boxcoordintates.
        """
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
        return objects
    
    def rename(self,before,filename,ext,names,root_list,is_list = False):
        if is_list == True:
            for old_name in os.listdir(root_list):
                new_name = old_name.split("--")[0]
                os.rename(os.path.join(root_list, old_name),os.path.join(root_list, new_name))
        else:
            new_filename = before + "{0:0>5}".format(names[index])+ext
            if ext == ".txt":
                 # rename annotations at divide ann folder
                if os.path.isfile(before+filename.split("\\")[1].split(".jpg")[0]+ext):
                    os.rename(before+filename.split("\\")[1].split(".jpg")[0]+ext, new_filename)
            if ext == ".jpg":
                # rename images
                os.rename(filename, new_filename)
            return new_filename
    
    def copy(self, subfolder, dir_path, names=None):
        Parser.copy(subfolder, dir_path, names=None)
        for filename in glob.glob(os.path.join( dir_path + subfolder, "*.*")):
            # rename annotations each in divide_ann folder according to images names
            self.rename(dir_anns_will_be_extracted_to,filename, ".txt",names, None)
            # rename & copy images to one single folder
            shutil.copy(self.rename(dir_path+subfolder,filename, ".jpg",names, None) ,  dir_path)
            #remover folders with images after copies into single folder
            if os.path.exists(dir_path+"WIDER_train"+subfolder):
                shutil.rmtree( dir_path+"WIDER_train"+subfolder)
    def single_folder(self):
        for i in range(subdir_count):
            subdir.append( imgs_subfolder+str(i)+"/")
            self.copy(subdir[i], dir_imgs_will_be_extracted_to, names)
        shutil.rmtree( dir_imgs_will_be_extracted_to+"WIDER_train")

def main():
    namespace = Parser.createParser (imgs_subfolder, anns_subfolder, None)
    wider =  WiderToJson()
    #make wider directories
    wider.make_directories(directories)
    #extract images from wider dataset archive
    wider.extract(imgs_dataset_archive, namespace.imgs_subfolder, dir_imgs_will_be_extracted_to)
    # extract annotations file from annotations dataset archive
    wider.extract(anns_dataset_archive, namespace.anns_subfolder, dir_anns_will_be_extracted_to)
    #copy annotations into annotations folder
    wider.copy(namespace.anns_subfolder, dir_anns_will_be_extracted_to)
    wider.make_divide_ann()
    #rename imgs subfolders to format "1"-"61"
    wider.rename(None,None,None,None,dir_imgs_will_be_extracted_to+namespace.imgs_subfolder,True)
    #Copy images to single folder
    wider.single_folder()
    # make json directory
    wider.populate_json_ann(json_dir, wider.parse())
if __name__ == '__main__':
    main()