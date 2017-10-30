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
# Sample: python train_val_test.py --voc "datasets/VOC_AFW/" --images "datasets/AFW/"

TRAIN_COEF = 0.6
VAL_COEF = 0.8
TEST_COEF = 1.0
parent_dir = {0: "train/", 1: "val/", 2: "test/" }
child_dir = {0: '', 1: 'images/', 2: 'annotations/'}
subdir = []

ap = argparse.ArgumentParser()
ap.add_argument("--voc", default="VOC_AFW", required = True, help = "Type voc folder path to receive annotations from")
ap.add_argument("--images", default="AFW", required = True, help = "Type images folder path to receive images from")
namespace = ap.parse_args(sys.argv[1:])
TODO: make_dir
def make_voc_dir(voc_path):
    for i in range(len(parent_dir)):
        for j in range(len(child_dir)):
            parent_dir[i]+=child_dir[j]
            subdir.append(voc_path+parent_dir[i])
            parent_dir[i] =  parent_dir[i].split("/")[0]+"/"
    return subdir
TODO: список файлів які і куди
def copy_anns_imgs(voc_path,ind, imgs_path, file):
    _voc_path = voc_path + 'single/'
    common.copy_file(_voc_path + file, voc_path+parent_dir[ind]+child_dir[2])
    common.copy_file(imgs_path + file.split('.')[0]+".jpg", voc_path+parent_dir[ind]+child_dir[1])
    
def populate_train_test_val(voc_path, imgs_path):
    _voc_path = voc_path + 'single/'
    counter = 0
    voc_anns_list = os.listdir( _voc_path )
    voc_anns_count = len(voc_anns_list)
    random.shuffle(voc_anns_list)
    for file in  voc_anns_list:
        counter +=1
        if counter <=  voc_anns_count*TRAIN_COEF:
            copy_anns_imgs(voc_path,0, imgs_path, file)
        if voc_anns_count*TRAIN_COEF < counter <= voc_anns_count*VAL_COEF:
            copy_anns_imgs(voc_path,1, imgs_path, file)   
        if voc_anns_count*VAL_COEF < counter <= voc_anns_count*TEST_COEF:
            copy_anns_imgs(voc_path,2, imgs_path, file)   
            

class Separator():
    def __init__(self):
        super(Separator, self).__init__()
   
    def separate(self):
        common.make_directories(make_voc_dir(namespace.voc))
        populate_train_test_val(namespace.voc,namespace.images)
        
def main():
    sep = Separator()
    sep.separate()
if __name__ == '__main__':
    main() 
