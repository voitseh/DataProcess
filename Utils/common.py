import os, sys, glob
import shutil
from PIL import Image

def copy_files(from_dir_path, destination_dir_path):
    if os.path.exists(from_dir_path):
        for filename in glob.glob(os.path.join( from_dir_path, "*.*")):
            copy_file(filename, destination_dir_path)
    else: 
         print("{} is not exist!".format(from_dir_path))

def copy_file(file, destination_dir_path):
    if os.path.isfile(file):
        shutil.copy(file, destination_dir_path)
    else:  
        print("{} not found!".format(file))

def remove_directory(directory_path):
    if os.path.isdir(directory_path):
        shutil.rmtree(directory_path)
    else: 
         print("{} is already deleted!".format(directory_path))

def remove_directories(dir_list):
    if type(dir_list) == list:
        for dir in dir_list:
            remove_directory(dir)
    else:
        print("Type of {} mast be 'list'".format(dir_list))

def make_directory(directory_path):
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)

def make_directories(dir_list):
    if type(dir_list) == list:
        for dir in dir_list:
            make_directory(dir)
    else:
        print("Type of {} mast be 'list'".format(dir_list))

def png_to_jpg_converter(filename, destination_path):
    if os.path.isfile(filename):
        im = Image.open(filename)
        file = os.path.join(destination_path , filename.split("/")[-1].split(".png")[0])
        im.save("{}.jpg".format(file),"jpeg")
    else: 
        print("{} not found!".format(filename))
    

