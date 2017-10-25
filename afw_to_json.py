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

python_version = sys.version_info.major

###########################################################
##########       AFW to JSON Conversion       ##########
###########################################################

# This script is run from console terminal
# Sample: C:\Users\User>python afw_to_json.py
# You can also specify images and annotations subfolder in dataset archive
# you will extract files from wich.
# Sample: python afw_to_json.py --imgs_and_anns_subfolder testimages/
# By defoult subfolder path for images & annotations extraction: "testimages/"

dataset_archive = "AFW.zip"
imgs_and_anns_subfolder = "testimages/"
imgs_and_anns_destination = 'datasets/AFW/'
json_dir = 'datasets/JSON_AFW/'
directories = [imgs_and_anns_destination, json_dir]
annotations_file ='datasets/AFW/anno.mat'

class AfwToJson(Parser):
    def __init__(self, imgs_and_anns_subfolder):
        self.img_ann = imgs_and_anns_subfolder
        super(AfwToJson, self).__init__()

    def make_directories(self, sub_dir):
        super(AfwToJson, self).make_directories(sub_dir)
    
    def extract(self, archive, subfolder, dir_path):
        super(AfwToJson, self).extract(archive, subfolder, dir_path)
    
    def parse(self, debug=False):
        self.make_directories(directories)
        self.extract(dataset_archive, self.img_ann, imgs_and_anns_destination)
        common.copy(imgs_and_anns_subfolder, imgs_and_anns_destination, names=None)
        with h5py.File(annotations_file) as data:
            
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
                if debug:
                    print ('Processing {0} ({1}/{2})'.format(object_info['filename'], indx + 1, n))
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
                
            for i in objects:
                with open(json_dir+i["filename"].split('.')[0]+".json", "wt") as out_file:
                    out_file.write(str(i))
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--imgs_and_anns_subfolder", default=imgs_and_anns_subfolder, required = False, help = "Images and annotations subfolder to extract from")
    namespace = ap.parse_args(sys.argv[1:])
    afw = AfwToJson(namespace.imgs_and_anns_subfolder)
    afw.parse()
if __name__ == '__main__':
    main()