'''
Visualise images bounding boxes, genders and ages

Usage :
    - .jpg images, annotations (Json format)  
    python visualisation_tool.py --ann_dir datasets/JSON_INRIA/  --images_dir datasets/INRIA/images/ --index 5
'''
import cv2
from PIL import Image
import pandas as pd
import json
import os, glob
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import argparse
import xml.etree.cElementTree as etree

##################################################################################
##########       VISUALISATION TOOLS FOR BOUNDING BOXES AND LABELS   #############
#################################################################################

ap = argparse.ArgumentParser()
ap.add_argument("--images_dir", required = True, help = "Directory of images")
ap.add_argument("--ann_dir", required = False, 
                help = "Directory with annotations")
ap.add_argument("--index", default='0',
                required = True, help = "Label index in CSV file to display (-1 to show all)")

args = vars(ap.parse_args())

def list_files(folder, file_format='.jpg'):
    """
        List files in directory of specific format
        Args: 
            folder: dirname where to search files
            file_format: file extension to search
        
        Returns:
            filenames: list of strings
    """
    pattern = '{0}/*{1}'.format(folder, file_format)
    filenames = glob.glob(pattern)    
    return filenames

def get_filename(path):
    with_extension = os.path.basename(path)

    return os.path.splitext(with_extension)[0]

def show_image(image):
    cv2.imshow('Image', image)
    while cv2.getWindowProperty('Image', 0) >= 0 :
        val = cv2.waitKey(100)
        if val != 255:
            break
    cv2.destroyWindow('Image') 

def draw_rectangle(filename,image,rectangle, center_with_size=False, color=[0, 255, 0]):
    if center_with_size:
        cx, cy, w, h = rectangle
        left, right = int(cx - w/2), int(cx + w/2)
        top, bottom = int(cy - h/2), int(cy + h/2)
    else:
        left, top, right, bottom = rectangle
        img = Image.open(filename)
        w, h = img.size
        if w > 650:
            k = 10
        else:
            k = 2
    return cv2.rectangle(image,(left,top),(right, bottom),color,int(k))

def draw_bounding_box(filename,image, bound_box, center_with_size=True, color=(0,255,0)):
    bb_denormalized = bound_box#denormalize_box(bound_box, image.shape[:2])
    result = draw_rectangle(filename,image, bb_denormalized, center_with_size=center_with_size, color=color)
    return result

    
def load_image(filename, flags=-1):
    if not os.path.exists(filename):
        #print (\"file {0} not exists\".format(filename))
        return None
    return cv2.imread(filename, flags)

def draw_age_gender(filename, image, bound_boxes, gender=None, age=None):
    for bound_box in bound_boxes:
        result = draw_bounding_box(filename,image, bound_box, center_with_size=False)
        plt.title("{}, {}".format(int(age),"M" if float(gender)>0.5 else "NAN" if gender == "nan"  else "F"))
        plt.imshow(result)
        plt.show()

def show_bound_box(filename, bound_boxes, gender=None, age=None):
    image = load_image(filename, cv2.IMREAD_COLOR)
    if image is None:
        return
    if age == None:
        #for bound in  bound_box:
        if type(bound_boxes) != int:
            for bound_box in bound_boxes:
                result = draw_bounding_box(filename,image, bound_box, center_with_size=False)
        else:
             result = draw_bounding_box(filename,image, bound_boxes, center_with_size=False)
        #show_image(result)
        plt.imshow(result)
        plt.show()
    else:
        draw_age_gender(filename, image, bound_boxes, gender, age)
    
def parse_from_pascal_voc_format(filename):
    """
        Look to Pascal VOC 2007 XML format http://host.robots.ox.ac.uk/pascal/VOC/voc2007/guidelines.html
        Args: 
            filename: *.xml file with data according to Pascal VOC 2007 XML format

        Returns: 
            Bounding box: ints xmin, ymin, xmax, ymax - 
                          represents bounding box cornets coordinates
    """
    bounding_boxes = []
    bounding_box = []
    gender = None
    age = None
    in_file = open(filename)
    tree=etree.parse(in_file)
    root = tree.getroot()
    for obj in root.iter('object'):
        current = list()              
        xmlbox = obj.find('bndbox')
        xn = int(float(xmlbox.find('xmin').text))
        xx = int(float(xmlbox.find('xmax').text))
        yn = int(float(xmlbox.find('ymin').text))
        yx = int(float(xmlbox.find('ymax').text))
        bounding_box = [xn,yn,xx,yx]
        bounding_boxes.append( bounding_box)
        if obj.find('gender') != None:
            if obj.find('gender').text != "None":
                gender = float(obj.find('gender').text)
            else:
                gender = "nan"
            age = float(obj.find('age').text)
    in_file.close()
    if gender != None:
        return (bounding_boxes,gender,age)
    else:
        #return (xn,yn,xx,yx)
        return(bounding_boxes)
    
def parse_json_annotation(filename):
        
    bdn_bxs = []
    gender = None
    age = None
    f= open(filename)
    for line in f:
        line = line.replace("'", '"')
        line = line.replace("nan", 'null')
        my_dict = json.loads(line)
        for obj in my_dict["objects"]:
            bdn_bxs.append(obj["bounding_box"])
            if "gender" in obj:
                if obj["gender"] != None:
                    gender = float(obj["gender"])
                else:
                    gender = "nan"
                age = float(obj["age"])
                f.close()
                return  (bdn_bxs, gender, age)
    f.close()
    return  bdn_bxs
def process_xml_ann(annotations_folder, images, index):
    bounding_box = []
    gender = None
    age = None
    annotations_xml = sorted(list_files(annotations_folder, '.xml'))
    if annotations_xml != []:
        annfile = annotations_folder+get_filename(images[index])+".xml"
        if os.path.isfile(annfile) and os.path.isfile(images[index]):
            if type(parse_from_pascal_voc_format(annfile)[-1]) != float:
                bounding_box = parse_from_pascal_voc_format(annfile)
            else:
                bounding_box, gender, age = parse_from_pascal_voc_format(annfile)
            show_bound_box(images[index], bounding_box, gender, age)

def process_json_ann(annotations_folder, images, index):
    bounding_box = []
    gender = None
    age = None
    annotations_json = sorted(list_files(annotations_folder, '.json'))
    if annotations_json != []:
        annfile = annotations_folder+get_filename(images[index])+".json"
        if os.path.isfile(annfile) and os.path.isfile(images[index]):
            if type(parse_json_annotation( annfile)[-1]) != float:
                bounding_box = parse_json_annotation( annfile)
            else:
                bounding_box, gender, age = parse_json_annotation( annfile)
            show_bound_box(images[index], bounding_box, gender, age)
            
def process_single(annotations_folder, images_folder, index):
    if any(File.endswith(".png") for File in os.listdir(images_folder)):
        images = sorted(list_files(images_folder, '.png'))
    else:
        images = sorted(list_files(images_folder, '.jpg'))
    process_xml_ann(annotations_folder, images, index)
    process_json_ann(annotations_folder, images, index)

def _process_dir(annotations_folder, images_folder, index=-1):
    
    filescount = len(os.listdir(annotations_folder))
    if index == -1:
        for i in range(filescount):
            process_single(images_folder,annotations_folder, i)
    else:
        process_single(annotations_folder,images_folder,  index)

def main(): 
    
    if not args['ann_dir']: 
        print ("Please specify folder with annotations") 
    else:
        if not args['images_dir']:
            print ("Please specify images folder")  
        else:
            index = int(args['index']) if args['index'] else 0  
            if args['ann_dir'] and os.path.exists(args['ann_dir']):
                _process_dir(args['ann_dir'], args['images_dir'], index)
        exit(0)
    exit(-1)
    
if __name__ == '__main__':
    main()