import os, sys, glob
import shutil
from PIL import Image

def copy(from_dir_path, destination_dir_path, file = None):
  
    if file == None:
        #copy files from directory
        for filename in glob.glob(os.path.join( from_dir_path, "*.*")):
            
    
            shutil.copy(filename,destination_dir_path)
    else:
        shutil.copy(file, destination_dir_path)

def delete_dir(dir_path):
    if os.path.exists(dir_path):
        shutil.rmtree( dir_path)
        
def delete_file(filename):
    os.remove(filename)
    
def png_to_jpg_converter( distination_path, filename=None, img_name=None,):
    if filename != None:
        im = Image.open(filename)
        im.save(distination_path + img_name.split(".png")[0] + ".jpg","jpeg")
        #os.remove(filename)
    else:
        #convert to same folder
        for old_name in os.listdir(distination_path):
            new_name = old_name.split(".")[0]+".jpg"
            os.rename(os.path.join(distination_path, old_name),os.path.join(distination_path, new_name))
            