# Import necessary libraries
import os, sys
import cv2
from scipy.io import loadmat
from h5py import File
import h5py
from Parser import *
from Utils import common
from PIL import Image
from six.moves import cPickle as pickle

###########################################################
##########       AFW to JSON Conversion       ##########
###########################################################

# This script is run from console terminal
# Sample: C:\Users\User>python afw_to_json.py

dataset_archive = "AFW.zip"
imgs_and_anns_subfolder = "testimages/"
imgs_and_anns_destination = 'datasets/AFW/'
json_dir = 'datasets/JSON_AFW/'
directories = [imgs_and_anns_destination, json_dir]
annotations_file ='datasets/AFW/anno.mat'

ap = argparse.ArgumentParser()
ap.add_argument("--subfolder", default=imgs_and_anns_subfolder, required = False, help = "Images and annotations subfolder to extract from")
namespace = ap.parse_args(sys.argv[1:])

def parse_afw(data):
        
    annotations = data[u'anno']
    '''
        annotations[0] : length of data
    '''
    print ('Found {0} rows '.format(len(annotations[0])))
    n = len(annotations[0])    
    objects = []
    for indx in range(n):
        object_info = {}
        img_info = annotations[1][indx]
        # Image filename
        obj = data[annotations[0][indx]]
        object_info['filename'] = ''.join(chr(i) for i in obj[:])
        object_info['objects'] = []
        for face_indx in range(len(data[img_info])):

            face_info = {'class_name':'face'}

            # bounding box processing
            obj = data[data[img_info][face_indx][0] ]             
            x1, y1 = int(round(obj[0,0])), int(round(obj[1,0]))
            x2, y2 = int(round(obj[0,1])), int(round(obj[1,1]))
            face_info['bounding_box'] = [x1, y1, x2, y2]            

            # pose reading
            obj = data[data[annotations[2][indx]][face_indx][0]]
            yaw, pitch, roll   = float(obj[0]), float(obj[1]), float(obj[2])     
            face_info['pose'] = [yaw, pitch, roll]

            object_info['objects'].append(face_info)

        objects.append(object_info)
        
    return objects

class AfwToJson(Parser):
    def __init__(self):
        common.make_directories(directories)
        extract_archive(dataset_archive, imgs_and_anns_destination)
        common.copy_files(os.path.join(imgs_and_anns_destination,imgs_and_anns_subfolder), imgs_and_anns_destination)
        common.remove_directory(os.path.join(imgs_and_anns_destination,imgs_and_anns_subfolder))
        super(AfwToJson, self).__init__()

    def parse(self, filename):
        with h5py.File(filename) as f:
            self.objects = parse_afw(f)
            for i in self.objects:
                file = os.path.join(json_dir, i["filename"].split('.')[0])
                with open("{}.json".format(file), "wt") as out_file:
                    out_file.write(str(i))

def main():
    afw = AfwToJson()
    afw.parse(annotations_file)
if __name__ == '__main__':
    main()