# Import necessary libraries
import os, sys, shutil, glob, argparse
import numpy as np
import json
import argparse
import random
from Parser import *
from PIL import Image
from lxml import etree

python_version = sys.version_info.major

###########################################################
##########        JSON to VOC Conversion        ##########
###########################################################

# This script is run from  console terminal
# Sample: C:\Users\User>python json_to_pascalVoc.py
# You can also specify dataset  from wich you copy images as:
# INRIA,AFW,WIDER,IMDB_WIKI
# Sample: python json_to_pascalVoc.py --dataset "INRIA"

TRAIN_COEF = 0.6
VAL_COEF = 0.2
TEST_COEF = 0.2

json_path = ""
inria_dataset = 'datasets/INRIA/images/'
voc_train_ann = 'datasets/VOC/train/annotations/'
voc_train_img = 'datasets/VOC/train/images/'
voc_val_ann = 'datasets/VOC/val/annotations/'
voc_val_img = 'datasets/VOC/val/images/'
voc_test_ann = 'datasets/VOC/test/annotations/'
voc_test_img = 'datasets/VOC/test/images/'
image_count = 0
parent_dir = {0: "train/", 1: "val/", 2: "test/" }
child_dir = {0: '', 1: 'images/', 2: 'annotations/'}
subdir = []

class JsonToPascalVoc(Parser):
    
    def __init__(self,dataset):
        global image_count, json_path
        json_path = 'datasets/JSON_'+str(dataset)+'/'
        self.dataset_imgs_path = "datasets/"+str(dataset)+"/"
        image_count = len(glob.glob(os.path.join('datasets/'+dataset+'/', "*.*")))
        if str(dataset) == "WIDER" or str(dataset) == "INRIA":
            self.dataset_imgs_path = "datasets/"+str(dataset)+"/images/"
            image_count = len(glob.glob(os.path.join('datasets/'+dataset+'/images/', "*.*")))
        
    def to_pasvoc_xml(self, fname, labels, coords, img_width, img_height, genders = None,ages = None):
        
        annotation = etree.Element('annotation')
        filename = etree.Element('filename')
        f = fname.split("/")
        filename.text = f[-1]
        annotation.append(filename)
        folder = etree.Element('folder')
        folder.text = "/".join(f[:-1])
        annotation.append(folder)
        for i in range(len(coords)):
            object = etree.Element('object')
            annotation.append(object)
            name = etree.Element('name')
            name.text = labels[i]
            object.append(name)
            if genders != []:
                name = etree.Element('gender')
                name.text = str(genders[i])
                object.append(name)
                name = etree.Element('age')
                name.text = str(ages[i])
                object.append(name)
            
            bndbox = etree.Element('bndbox')
            object.append(bndbox)
            xmax = etree.Element('xmax')
            xmax.text = str(coords[i][2])
            bndbox.append(xmax)
            xmin = etree.Element('xmin')
            xmin.text = str(coords[i][0])
            bndbox.append(xmin)
            ymax = etree.Element('ymax')
            ymax.text = str(coords[i][3])
            bndbox.append(ymax)
            ymin = etree.Element('ymin')
            ymin.text = str(coords[i][1])
            bndbox.append(ymin)
            difficult = etree.Element('difficult')
            difficult.text = '0'
            object.append(difficult)
            occluded = etree.Element('occluded')
            occluded.text = '0'
            object.append(occluded)
            pose = etree.Element('pose')
            pose.text = 'Unspecified'
            object.append(pose)
            truncated = etree.Element('truncated')
            truncated.text = '1'
            object.append(truncated)
        img_size = etree.Element('size')
        annotation.append(img_size)
        depth = etree.Element('depth')
        depth.text = '3'
        img_size.append(depth)
        height = etree.Element('height')
        height.text = str(img_height)
        img_size.append(height)
        width = etree.Element('width')
        width.text = str(img_width)
        img_size.append(width)

        return annotation

    def parse_json_ann(self, filename):
        """
        Definition: Parses json annotation file to extract bounding box coordintates.

        Returns: all_clases - contains a list of clases
                     all_coords - contains a list of bdn_bxs
        """
        lfile = open(filename)
        classes = []
        bdn_bxs = []
        genders = []
        ages = []
        f= open(filename)
        for line in f:
            line = line.replace("'", '"')
            line = line.replace("nan", 'null')
            my_dict = json.loads(line)
            for obj in my_dict["objects"]:
                classes.append(obj["class_name"])
                bdn_bxs.append(obj["bounding_box"])
                if "gender" in obj:
                    genders.append(obj["gender"])
                    ages.append(obj["age"])
        return  classes,bdn_bxs,genders,ages
    
    # make voc directories
    for i in range(len(parent_dir)):
        for j in range(len(child_dir)):
            parent_dir[i]+=child_dir[j]
            subdir.append("datasets/VOC/"+parent_dir[i])
            parent_dir[i] =  parent_dir[i].split("/")[0]+"/"
    # populate voc folders
    def populate(self,et,f,dataset_imgs,fname,anns_dir,imgs_dir):
        et.write(anns_dir + f.split(".json")[0] + ".xml", pretty_print=True)
        if dataset_imgs == inria_dataset:
            im = Image.open(fname)
            im.save(imgs_dir + (f.split(".json")[0] + ".jpg"),"jpeg")
        else:
            shutil.copy(fname,imgs_dir)
    def voc(self, label=None):
        print ("Convert json to voc")
        ind = 0
        # Iterate through json annotations data
        #Copy all images from datasets to voc training, validation and test image folders.
        for f in os.listdir(json_path):
            
            fname = json_path + f
            if os.path.isfile(fname):
               
                if self.dataset_imgs_path ==  inria_dataset:
                    fname = (self.dataset_imgs_path + f).split(".json")[0] + ".png"
                    
                else:
                    fname = (self.dataset_imgs_path + f).split(".json")[0] + ".jpg"
                
                if os.path.isfile(fname):
                    ind += 1
                    img = Image.open(fname)
                    w, h = img.size
                    img.close()
                    fname = (json_path + f).split(".json")[0] + ".jpg"
                    labels, coords, genders, ages = self.parse_json_ann(os.path.join(json_path + f))
                    annotation = self.to_pasvoc_xml(fname, labels, coords, w, h, genders, ages)
                    et = etree.ElementTree(annotation)
                    if self.dataset_imgs_path == inria_dataset:
                        fname = (self.dataset_imgs_path + f).split(".json")[0] + ".png"
                    else:
                        fname = (self.dataset_imgs_path + f).split(".json")[0] + ".jpg"
                    if ind <= image_count*TRAIN_COEF:
                        self.populate(et,f,self.dataset_imgs_path,fname,voc_train_ann,voc_train_img)
                    if image_count*TRAIN_COEF < ind <= image_count*(TRAIN_COEF+VAL_COEF):
                        self.populate(et,f,self.dataset_imgs_path,fname,voc_val_ann,voc_val_img)
                    
                    if ind > image_count*(TRAIN_COEF+VAL_COEF):
                        self.populate(et,f,self.dataset_imgs_path,fname,voc_test_ann,voc_test_img)
                        
def main():
    
    ap = argparse.ArgumentParser()
    ap.add_argument("--dataset", default="INRIA", required = True, help = "Type dataset to receive images from")
    namespace = ap.parse_args(sys.argv[1:])
    
    voc = JsonToPascalVoc(namespace.dataset)
    voc.make_directories(subdir)
    voc.voc()
if __name__ == '__main__':
    main() 