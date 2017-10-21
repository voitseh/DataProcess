# Import necessary libraries
import os, sys
import cv2
from scipy.io import loadmat
from h5py import File
import h5py
from Parser import *
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
    
    def parse(debug=False):
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
                
            return objects
def main():
    namespace = Parser.createParser (None, None, imgs_and_anns_subfolder)
    afw =  AfwToJson()
    #make afw directory
    afw.make_directories(directories)
    afw.extract(dataset_archive, namespace.imgs_and_anns_subfolder, imgs_and_anns_destination)
    afw.copy(imgs_and_anns_subfolder, imgs_and_anns_destination, names=None)
    afw.populate_json_ann(json_dir, afw.parse())
if __name__ == '__main__':
    main()