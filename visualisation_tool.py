'''
Visualise images bounding boxes, genders and ages

Usage :
    - .jpg images, annotations (Json format)  
    python visualisation_tool.py --ann_dir datasets/JSON_INRIA/  --images_dir datasets/INRIA/images/ --index 5
    python visualisation_tool.py --ann_dir datasets/JSON_IMDB-WIKI/  --images_dir datasets/IMDB-WIKI/ --index 5
'''
import numpy as np
import cv2
from PIL import Image
import pandas as pd
import json
import os, glob
import matplotlib.image as mpimg
import argparse
import xml.etree.cElementTree as etree

##################################################################################
##########       VISUALISATION TOOLS FOR BOUNDING BOXES AND LABELS   #############
#################################################################################

ap = argparse.ArgumentParser()
ap.add_argument("--images_dir", required = True, help = "Directory of images")
ap.add_argument("--ann_dir", required = False, help = "Directory with annotations")
ap.add_argument("--index", default='0',required = True, help = "Label index in CSV file to display (-1 to show all)")
args = vars(ap.parse_args())

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

def show_image_with_label(title, image):
    cv2.imshow(title, image)
    while cv2.getWindowProperty(title, 0) >= 0 :
        val = cv2.waitKey(100)
        if val != 255:
            break
    cv2.destroyWindow(title)

def draw_text(dict):
    if dict['Text'] is not None:
       cv2.putText(dict['vcat'],dict['Text'],(dict['w'],dict['h']),dict['font'],dict['size'],dict['thickness'])

def show_image(image, gender=None, age=None):
    # image without labels
    if age == None:
        show_image_with_label('Image',image)
    # image with gender & age labels
    else:
        Text = "{}, {}".format(int(age),"M" if float(gender)>0.5 else "NAN" if gender == "nan"  else "F")
        height, width, ch = image.shape
        #--- Here I am creating the border---
        black = [0,0,0]     #---Color of the border---
        constant=cv2.copyMakeBorder(image,5,5,5,5,cv2.BORDER_CONSTANT,value=black )
        #--- Here I created a violet background to include the text ---
        violet= np.zeros((30, constant.shape[1], 3), np.uint8)
        violet[:] = (255, 0, 180) 
        #--- I then concatenated it vertically to the image with the border ---
        vcat = cv2.vconcat((violet, constant))
        #--- Now I included some text ---
        font = cv2.FONT_HERSHEY_SIMPLEX
        dict = {'vcat':vcat,'Text':Text, 'w':int((width-15)/2),'h':20, 'font':font, 'size':0.5, 'thickness':2}
        draw_text(dict)
        show_image_with_label('Image',vcat)
    
def draw_rectangle(args):
    if args['center_with_size']:
        cx, cy, w, h = args['bound_box']
        left, right = int(cx - w/2), int(cx + w/2)
        top, bottom = int(cy - h/2), int(cy + h/2)
    else:
        left, top, right, bottom = args['bound_box']
        h, w, c = args['image'].shape
        if w > 650:
            k = 10
        else:
            k = 2
    return cv2.rectangle(args['image'],(left,top),(right, bottom),args['color'],int(k))

def draw_bounding_box(args):
    result = draw_rectangle(args)
    return result

def load_image(filename, flags=-1):
    if not os.path.exists(filename):
        #print (\"file {0} not exists\".format(filename))
        return None
    return cv2.imread(filename, flags)
#Parameters:  Args[0]-filename,Args[1]-bounding boxes, Args[2]-gender, Args[3]-age
def show_bound_box(Args):
    image = load_image(Args[0], cv2.IMREAD_COLOR)
    objInfo = {'image':image, 'bound_box':Args[1], 'center_with_size':True, 'color':(0,255,0)}
    if image is None:
        return
    if type(Args[1]) != int:
        objInfo['center_with_size'] = False
        for bound_box in Args[1]:
            objInfo['bound_box'] = bound_box  
            result = draw_bounding_box(objInfo)
    else:
        objInfo['center_with_size'] = False
        result = draw_bounding_box(objInfo)
    show_image(result, Args[2], Args[3])
    
def parse_from_pascal_voc_format(filename):
    """
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
            return images[index],bounding_box,gender, age

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
            return images[index],bounding_box,gender, age

def process_single(annotations_folder, images_folder, index):
    images = sorted(list_files(images_folder, '.jpg'))
    objects = process_xml_ann(annotations_folder, images, index)
    objects = process_json_ann(annotations_folder, images, index)
    show_bound_box(objects)

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
        exit(0)
    exit(-1)
    
if __name__ == '__main__':
    main()