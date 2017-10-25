# Import necessary libraries
import os, sys, shutil, glob, argparse
import numpy as np
import json
import argparse
from Parser import *
from PIL import Image
from lxml import etree

python_version = sys.version_info.major

###########################################################
##########        JSON to VOC Conversion        ##########
###########################################################

# This script is run from  console terminal
# Sample: python json_to_pascalVoc.py --json "datasets/JSON_AFW/" --images "datasets/AFW/"

voc_path = ['datasets/VOC_INRIA/', 'datasets/VOC_AFW/', 'datasets/VOC_WIDER/', 'datasets/VOC_IMDB_WIKI/']
inria_dataset = 'datasets/INRIA/images/'


class JsonToPascalVoc(Parser):
    
    def __init__(self,json_path, imgs_path):
        self.json_path = str(json_path)
        self.imgs_path = imgs_path
        self.image_count = len(glob.glob(os.path.join( self.imgs_path, "*.*")))
        super(JsonToPascalVoc, self).__init__()
    
    def make_directories(self, sub_dir):
        super(JsonToPascalVoc, self).make_directories(sub_dir)
    
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
    
    def voc(self, label=None):
        path = ''
        path =[x for x in voc_path if (x.split("_")[1] == self.json_path.split("_")[1])]
        self.make_directories(path)
        
        print ("Convert json to voc")
        # Iterate through json annotations data
        for f in os.listdir(self.json_path):
            
            fname = self.json_path + f
            if os.path.isfile(fname):
               
                if self.imgs_path ==  inria_dataset:
                    fname = (self.imgs_path + f).split(".json")[0] + ".png"
                    common.png_to_jpg_converter(fname,  self.imgs_path, f.split(".json")[0] + ".png")
                    
                fname = (self.imgs_path + f).split(".json")[0] + ".jpg"
                
                if os.path.isfile(fname):
                    img = Image.open(fname)
                    w, h = img.size
                    img.close()
                    labels, coords, genders, ages = self.parse_json_ann(os.path.join(self.json_path + f))
                    annotation = self.to_pasvoc_xml(fname, labels, coords, w, h, genders, ages)
                    et = etree.ElementTree(annotation)
                    et.write(path[0] + f.split(".json")[0] + ".xml", pretty_print=True)
                    
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", default="JSON_AFW", required = True, help = "Type json folder path to receive annotations from")
    ap.add_argument("--images", default="AFW", required = True, help = "Type images folder path to receive images from")
    namespace = ap.parse_args(sys.argv[1:])
    voc = JsonToPascalVoc(namespace.json, namespace.images)
    voc.voc()
if __name__ == '__main__':
    main() 