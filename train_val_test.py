# Import necessary libraries
import os, sys, shutil, glob
import argparse
import random
from Parser import *
from Utils import common
from PIL import Image
from  collections import namedtuple

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
dst_tuple = namedtuple("dst_tuple", "train_dst val_dist test_dist")

directories_list = ["{}/train/images/".format(namespace.annotations.split('single')[0]), "{}/train/annotations/".format(namespace.annotations.split('single')[0]), "{}/val/images/".format(namespace.annotations.split('single')[0]), "{}/val/annotations/".format(namespace.annotations.split('single')[0]), "{}/test/images/".format(namespace.annotations.split('single')[0]), "{}/test/annotations/".format(namespace.annotations.split('single')[0]) ]

def copy_files(files, src, dst):
    for file in files:
        common.copy_file(os.path.join(src, file), dst)

def randomize(items):
    """
        Shuffle data to make records order more random
        Args: 
            items: list
        Returns: 
            Shuffled lists
    """
    shuffled_index = list(range(len(items)))
    random.seed(12345)
    random.shuffle(shuffled_index)
    result = [items[i] for i in shuffled_index]
    return result

def populate_train_test_val(src, dst_tuple):
    files_list = [file for file in os.listdir(src) if (file.endswith(".json") or file.endswith(".xml") or file.endswith(".jpg"))]
    files_count = len(files_list)
    files_list = randomize(files_list)
    files_train_list = files_list[:int(files_count*TRAIN_COEF)]
    copy_files(files_train_list, src, dst_tuple[0])
    files_val_list = files_list[int(files_count*TRAIN_COEF):int(files_count*VAL_COEF)]
    copy_files(files_val_list, src, dst_tuple[1])
    files_test_list = files_list[int(files_count*VAL_COEF):]
    copy_files(files_test_list, src, dst_tuple[2])

def main():
    if not namespace.annotations: 
        print ("Please specify folder with annotations") 
    else:
        if not namespace.images:
            print ("Please specify images folder")  
        else:
            common.make_directories(directories_list)
            #for annotations
            populate_train_test_val(namespace.annotations, (directories_list[1], directories_list[3], directories_list[5]))
            #for images
            populate_train_test_val(namespace.images, (directories_list[0], directories_list[2], directories_list[4]))
        exit(0)
    exit(-1)

if __name__ == '__main__':
    main() 
