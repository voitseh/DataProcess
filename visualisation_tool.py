'''
Visualise images bounding boxes, genders and ages

Usage :
    - .jpg images, annotations (Json format)  
<<<<<<< HEAD
    python visualisation_tool.py --annotations datasets/JSON_INRIA/  --images datasets/INRIA/images/ --index 5
    python visualisation_tool.py --annotations datasets/JSON_IMDB-WIKI/  --images datasets/IMDB-WIKI/ --index 5
=======
    python visualisation_tool.py --ann_dir datasets/JSON_INRIA/  --images_dir datasets/INRIA/images/ --index 5
    python visualisation_tool.py --ann_dir datasets/JSON_IMDB-WIKI/  --images_dir datasets/IMDB-WIKI/ --index 5
>>>>>>> 2067067238b2eb474f4592ef58f7cbc5841d628b
'''
import numpy as np
import cv2
import pandas as pd
import json
import os, glob
import matplotlib.image as mpimg
import argparse
import xml.etree.cElementTree as etree
from  collections import namedtuple

##################################################################################
##########       VISUALISATION TOOLS FOR BOUNDING BOXES AND LABELS   #############
#################################################################################

ap = argparse.ArgumentParser()
<<<<<<< HEAD
ap.add_argument("--images", required = True, help = "Directory of images")
ap.add_argument("--annotations", required = True, help = "Directory with annotations")
ap.add_argument("--index", default='0',required = True, help = "Label index in CSV file to display (-1 to show all)")
args = vars(ap.parse_args())

=======
ap.add_argument("--images_dir", required = True, help = "Directory of images")
ap.add_argument("--ann_dir", required = True, help = "Directory with annotations")
ap.add_argument("--index", default='0',required = True, help = "Label index in CSV file to display (-1 to show all)")
args = vars(ap.parse_args())

# tuple for x and y coordinates
x_y_tuple = namedtuple("x_y_tuple", "x y")
>>>>>>> 2067067238b2eb474f4592ef58f7cbc5841d628b
# struct for bound boxes, gender and age
class BdgBoxAndLabelsArgs:
    bound_boxes = None
    gender = None
    age = None
   
def list_files(folder, file_format='.jpg'):
    """
       Returns:
            filenames: list of strings
    """
    pattern = '{0}/*{1}'.format(folder, file_format)
    filenames = glob.glob(pattern)    
    return filenames

def get_filename(path):
    with_extension = os.path.basename(path)
    return os.path.splitext(with_extension)[0]

<<<<<<< HEAD
def draw_text(image,text,point,font=cv2.FONT_HERSHEY_SIMPLEX,size=0.5,color=[0, 100, 0]):
    thick = int(sum(image.shape[:2]) // 600)
    cv2.putText(image,text,(point[0]-thick, point[1] -thick),font,size,color,thick)

def show_gender(image,gender,point):
    text = "{}".format("M" if float(gender)>0.5 else "NAN" if gender == "nan"  else "F")
    draw_text(image,text,point)

def show_age(image,age,point):
    text = "{}".format(int(age))
    draw_text(image,text,point)

def show_image(image):
    img = 'Image'
    cv2.imshow(img, image)
    while cv2.getWindowProperty(img, 0) >= 0 :
        val = cv2.waitKey(100)
        if val != 255:
            break
    cv2.destroyWindow(img)
=======
def draw_text(image,Text,x_y_tuple,font=cv2.FONT_HERSHEY_SIMPLEX,size=0.5,color=[0, 100, 0]):
    thick = int(sum(image.shape[:2]) // 600)
    cv2.putText(image,Text,(x_y_tuple[0]-thick, x_y_tuple[1]-thick),font,size,color,thick)

def show_gender(image,gender,x_y_tuple):
    Text = "{}".format("M" if float(gender)>0.5 else "NAN" if gender == "nan"  else "F")
    draw_text(image,Text,x_y_tuple)

def show_age(image,age,x_y_tuple):
    Text = "{}".format(int(age))
    draw_text(image,Text,x_y_tuple)

def show_image(image):
    cv2.imshow('Image', image)
    while cv2.getWindowProperty('Image', 0) >= 0 :
        val = cv2.waitKey(100)
        if val != 255:
            break
    cv2.destroyWindow('Image')
>>>>>>> 2067067238b2eb474f4592ef58f7cbc5841d628b
    
def draw_rectangle(image,rectangle, center_with_size=False, color=[0, 255, 0]):
    if center_with_size:
        cx, cy, w, h = rectangle
        left, right = int(cx - w/2), int(cx + w/2)
        top, bottom = int(cy - h/2), int(cy + h/2)
    else:
        left, top, right, bottom = rectangle
        thick = int(sum(image.shape[:2]) // 300)
        
    return cv2.rectangle(image, (left,top),(right, bottom),color,thick)

def draw_bounding_box(image, bound_box, center_with_size=True, color=(0,255,0)):
    result = draw_rectangle(image, bound_box, center_with_size, color)
    return result

def load_image(filename, flags=-1):
    if not os.path.exists(filename):
        return None
    return cv2.imread(filename, flags)
<<<<<<< HEAD

# shows labels:gender and/or age.Paremeters:image,BdgBoxAndLabelsArgs.Returns:None
def show_labels(image,annotation) :
    deltaX = 20
    deltaY = 5
    xn, yn, xx, yx = annotation.bound_boxes[0]
    if annotation.gender != None:
        show_gender(image,annotation.gender,(xn,yn-deltaY))
    if annotation.age != None:
        show_age(image,annotation.age,(xn+deltaX,yn-deltaY))

# shows bounding box or several bounding boxes and labels:gender and/or age.
# paremeters:filename,annotation.Returns:None
def show_annotation(filename, annotation):
    image = load_image(filename, cv2.IMREAD_COLOR)
    if image is None:
        return
    # here! we showing  bounding boxes +  labels:gender and/or age
    for bound_box in annotation.bound_boxes:
        result = draw_bounding_box(image, bound_box, center_with_size=False)
        show_labels(image,annotation)
=======
# shows labels:gender and/or age.Paremeters:image,BdgBoxAndLabelsArgs.Returns:None
def show_labels(image,BdgBoxAndLabelsArgs) :
    deltaX = 20
    deltaY = 5
    xn, yn, xx, yx = BdgBoxAndLabelsArgs.bound_boxes[0]
    if BdgBoxAndLabelsArgs.gender != None:
        show_gender(image,BdgBoxAndLabelsArgs.gender,(xn,yn-deltaY))
    if BdgBoxAndLabelsArgs.age != None:
        show_age(image,BdgBoxAndLabelsArgs.age,(xn+deltaX,yn-deltaY))

def show_bound_box_and_labels(filename, BdgBoxAndLabelsArgs):
    image = load_image(filename, cv2.IMREAD_COLOR)
    if image is None:
        return
    if type(BdgBoxAndLabelsArgs.bound_boxes[0]) ==  list:
        for bound_box in BdgBoxAndLabelsArgs.bound_boxes:
            result = draw_bounding_box(image, bound_box, center_with_size=False)
            show_labels(image,BdgBoxAndLabelsArgs)
    else:
        result = draw_bounding_box(image, BdgBoxAndLabelsArgs.bound_boxes, center_with_size=False)
        show_labels(image, BdgBoxAndLabelsArgs)
>>>>>>> 2067067238b2eb474f4592ef58f7cbc5841d628b
    show_image(result)

def parse_from_pascal_voc_format(filename):
    """
       Returns: 
            Bounding box: ints xmin, ymin, xmax, ymax - 
                          represents bounding box cornets coordinates
    """
    bounding_box = []
    in_file = open(filename)
    tree=etree.parse(in_file)
    root = tree.getroot()
<<<<<<< HEAD
    objects = BdgBoxAndLabelsArgs()
    objects.bound_boxes = []
=======
>>>>>>> 2067067238b2eb474f4592ef58f7cbc5841d628b
    for obj in root.iter('object'):
        current = list()              
        xmlbox = obj.find('bndbox')
        xn = int(float(xmlbox.find('xmin').text))
        xx = int(float(xmlbox.find('xmax').text))
        yn = int(float(xmlbox.find('ymin').text))
        yx = int(float(xmlbox.find('ymax').text))
        bounding_box = [xn,yn,xx,yx]
<<<<<<< HEAD
        objects.bound_boxes.append(bounding_box)
        gender = obj.find('gender')
        if gender != None:
            if gender.text != "None":
                objects.gender = gender
            else:
                objects.gender = "nan"
            objects.age = float(obj.find('age').text)
    in_file.close()
    return objects
   
def parse_json_annotation(filename):
    f= open(filename)
    objects = BdgBoxAndLabelsArgs()
    objects.bound_boxes = []
=======
        objects = BdgBoxAndLabelsArgs()
        objects.bound_boxes = []
        objects.bound_boxes.append(bounding_box)
        if obj.find('gender') != None:
            if obj.find('gender').text != "None":
                objects.gender = float(obj.find('gender').text)
            else:
                objects.gender = "nan"
            objects.age = float(obj.find('age').text)
    return objects
    in_file.close()
   
    
def parse_json_annotation(filename):
    f= open(filename)
>>>>>>> 2067067238b2eb474f4592ef58f7cbc5841d628b
    for line in f:
        line = line.replace("'", '"')
        line = line.replace("nan", 'null')
        my_dict = json.loads(line)
        for obj in my_dict["objects"]:
<<<<<<< HEAD
=======
            objects = BdgBoxAndLabelsArgs()
            objects.bound_boxes = []
>>>>>>> 2067067238b2eb474f4592ef58f7cbc5841d628b
            objects.bound_boxes.append(obj["bounding_box"])
            if "gender" in obj:
                if obj["gender"] != None:
                    objects.gender = float(obj["gender"])
                else:
                    objects.gender = "nan"
            if "age" in obj:
                objects.age = float(obj["age"])
<<<<<<< HEAD
    f.close()
    return objects
 
def _process_dir(annotations_folder, images_folder, index=-1):
    images = sorted(list_files(images_folder, '.jpg'))
    if annotations_folder.split('_')[0] == 'datasets/JSON':
        annotations_xml = sorted(list_files(annotations_folder, '.xml'))
        if annotations_xml != []:
            annfile = "{}{}.xml".format(annotations_folder,get_filename(images[index]))
            if os.path.isfile(annfile) and os.path.isfile(images[index]):
                objects = parse_from_pascal_voc_format(annfile)
        else:
            annotations_json = sorted(list_files(annotations_folder, '.json'))
            if annotations_json != []:
                annfile = "{}{}.json".format(annotations_folder,get_filename(images[index]))
                if os.path.isfile(annfile) and os.path.isfile(images[index]):
                    objects = parse_json_annotation( annfile)
    show_annotation(images[index], objects)

def main(): 
    
    if not args['annotations']: 
        print ("Please specify folder with annotations") 
    else:
        if not args['images']:
            print ("Please specify images folder")  
        else:
            index = int(args['index']) if args['index'] else 0  
            if args['annotations'] and os.path.exists(args['annotations']):
                _process_dir(args['annotations'], args['images'], index)
=======
        return objects
    f.close()
   

def process_xml_ann(annotations_folder, images, index):
    annotations_xml = sorted(list_files(annotations_folder, '.xml'))
    if annotations_xml != []:
        annfile = "{}{}.xml".format(annotations_folder,get_filename(images[index]))
        if os.path.isfile(annfile) and os.path.isfile(images[index]):
            objects = parse_from_pascal_voc_format(annfile)
            return images[index], objects

def process_json_ann(annotations_folder, images, index):
    annotations_json = sorted(list_files(annotations_folder, '.json'))
    if annotations_json != []:
        annfile = "{}{}.json".format(annotations_folder,get_filename(images[index]))
        if os.path.isfile(annfile) and os.path.isfile(images[index]):
            objects = parse_json_annotation( annfile)
            return images[index], objects

def process_single(annotations_folder, images_folder, index):
    images = sorted(list_files(images_folder, '.jpg'))
    if annotations_folder.split('_')[0] == 'datasets/JSON':
        filename, obj = process_json_ann(annotations_folder, images, index)
    else:
        filename, obj = process_xml_ann(annotations_folder, images, index)
    show_bound_box_and_labels(filename, obj)

def _process_dir(annotations_folder, images_folder, index=-1):
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
>>>>>>> 2067067238b2eb474f4592ef58f7cbc5841d628b
        exit(0)
    exit(-1)
    
if __name__ == '__main__':
    main()