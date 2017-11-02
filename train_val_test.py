# Import necessary libraries
import os, sys, shutil, glob
import argparse
import random
from Parser import *
from Utils import common
from PIL import Image

###########################################################
##########        train/test/val separate        ##########
###########################################################
# This script is run from  console terminal
# Sample: python train_val_test.py --annotations "datasets/VOC_AFW/single/" --images "datasets/AFW/"

ap = argparse.ArgumentParser()
ap.add_argument("--annotations", required = True, help = "Type annotations folder path to receive annotations from")
ap.add_argument("--images", required = True, help = "Type images folder path to receive images from")
namespace = ap.parse_args(sys.argv[1:])

TRAIN_COEF = 0.6
VAL_COEF = 0.8

directories_list = ["{}/train/images/".format(namespace.annotations.split('single')[0]), "{}/train/annotations/".format(namespace.annotations.split('single')[0]), "{}/val/images/".format(namespace.annotations.split('single')[0]), "{}/val/annotations/".format(namespace.annotations.split('single')[0]), "{}/test/images/".format(namespace.annotations.split('single')[0]), "{}/test/annotations/".format(namespace.annotations.split('single')[0]) ]

def copy_files(from_dir_path, files_list, destination_dir_path):
    for file in files_list:
        common.copy_file(os.path.join(from_dir_path, file), destination_dir_path)
 
def populate_train_test_val_annotations(annotations_path):
    annotations_list = os.listdir(annotations_path)
    annotations_count = len(annotations_list)
    
    annotations_train_list = annotations_list[:int(annotations_count*TRAIN_COEF)]
    copy_files(annotations_path, annotations_train_list, directories_list[1])
    annotations_val_list = annotations_list[int(annotations_count*TRAIN_COEF):int(annotations_count*VAL_COEF)]
    copy_files(annotations_path, annotations_val_list, directories_list[3])
    annotations_test_list = annotations_list[int(annotations_count*VAL_COEF):]
    copy_files(annotations_path, annotations_test_list, directories_list[5])

def populate_train_test_val_images(images_path):
    images_list = os.listdir(images_path)
    images_count = len(images_list)
    
    images__train_list = images_list[:int(images_count*TRAIN_COEF)]
    copy_files(images_path, images__train_list, directories_list[0])
    images__val_list = images_list[int(images_count*TRAIN_COEF):int(images_count*VAL_COEF)]
    copy_files(images_path, images__val_list, directories_list[2])
    images__test_list = images_list[int(images_count*VAL_COEF):]
    copy_files(images_path, images__test_list, directories_list[4])


def main():
    if not namespace.annotations: 
        print ("Please specify folder with annotations") 
    else:
        if not namespace.images:
            print ("Please specify images folder")  
        else:
            common.make_directories(directories_list)
            populate_train_test_val_annotations(namespace.annotations)
            populate_train_test_val_images(namespace.images)
        exit(0)
    exit(-1)

if __name__ == '__main__':
    main() 
