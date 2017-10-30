import os, sys, glob
import shutil
from PIL import Image

def copy_files(from_dir_path, destination_dir_path):
    if os.path.exists(from_dir_path):
        # TODO del if
        if not os.path.exists(destination_dir_path):  make_directory(destination_dir_path)
        for filename in glob.glob(os.path.join( from_dir_path, "*.*")):
            copy_file(filename, destination_dir_path)
    else:  print(from_dir_path + " is not exist!")

def copy_file(file, destination_dir_path):
    if not os.path.exists(destination_dir_path):  make_directory(destination_dir_path)
    if os.path.isfile(file):
        shutil.copy(file, destination_dir_path)
    else:  print(file + " not found!")
    

def remove_directory(directory_path):
    if os.path.isdir(directory_path):
        shutil.rmtree(directory_path)
    else: 
        #TODO: "{0}.format()
        print(directory_path + " is already deleted!")

def remove_directories(dir_list):
    if type(dir_list) == list:
        for i in range(len(dir_list)):
           remove_directory(dir_list[i])
    else:
        print("Type of "+dir_list+" mast be 'list'")
def make_directory(directory_path):
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)

def make_directories(dir_list):
    if type(dir_list) == list:
        for i in range(len(dir_list)):
            make_directory(dir_list[i])
    else:
        #TODO:format
        print("Type of "+dir_list+" mast be 'list'")

def png_to_jpg_converter(destination_path, filename):
    make_directory(destination_path)
    if os.path.isfile(filename):
        im = Image.open(filename)
        #TODO: file = 
        im.save(destination_path + filename.split("/")[-1].split(".png")[0] + ".jpg","jpeg")
    else:
        print(filename + " not found!")
    

