import os, sys, glob
import shutil
from PIL import Image


def copy(subfolder, dir_path, names=None):
    index = 0
    for filename in glob.glob(os.path.join( dir_path + subfolder, "*.*")):
        index += 1
        shutil.copy(filename,  dir_path)
    if os.path.exists(dir_path+subfolder):
        shutil.rmtree( dir_path + subfolder)
            
    
def png_to_jpg_converter(filename, distination_path, img_name):
    im = Image.open(filename)
    im.save(distination_path + img_name.split(".png")[0] + ".jpg","jpeg")
    os.remove(filename)