import os, sys, glob
import tarfile
import zipfile
import argparse
import shutil

python_version = sys.version_info.major

index = 0
class Parser(object):
    
    #This part is for dataset extracting from archives
    @staticmethod
    def createParser (default_imgs, default_anns, default_imgs_and_anns):
        ap = argparse.ArgumentParser()
        # in case images and annotations are in different folders
        if default_imgs != None and default_anns != None:
            ap.add_argument("--imgs_subfolder", default=default_imgs, required = False, help = "Images subfolder to extract from")
            ap.add_argument("--anns_subfolder", default=default_anns, required = False, help = "Annotations subfolder to extract from")
        # in case images and annotations are in single folder    
        if default_imgs_and_anns != None:
             ap.add_argument("--imgs_and_anns_subfolder", default=default_imgs_and_anns, required = False, help = "Images and annotations subfolder to extract from")
        namespace = ap.parse_args(sys.argv[1:])
        return namespace
    @staticmethod   
    def members( tf, subfolder):
        l = len(subfolder)
        for member in tf.getmembers():
            if member.path.startswith(subfolder):
                member.path = member.path[l:]
                yield member
    @staticmethod
    def extract( archive, subfolder, dir_path): 
       
        filename, file_extension = os.path.splitext(archive)
        if file_extension != ".zip":
            with tarfile.open(archive) as tar:
                if os.path.exists(dir_path):  
                    if subfolder.split(".") != "mat":
                        tar.extractall(members=Parser.members(tar, subfolder), path = dir_path)
                    else:
                        for entry in tar:
                            fileobj = tf.extractfile(entry)
                            print(fileobj)
        if file_extension == '.zip':
            _archive = zipfile.ZipFile(archive)
            for file in _archive.namelist():
                if file.startswith(subfolder):
                    filename, file_extension = os.path.splitext(file)
                    if file_extension == '.jpg' or file_extension == '.mat' or file_extension == '.png' or filename == 'wider_face_split/wider_face_train_bbx_gt':
                        if os.path.exists(dir_path): 
                            _archive.extract(file, dir_path)
    
    #This part is for dataset transformation(copy,rename,shuffle)
    @staticmethod           
    def copy(subfolder, dir_path, names=None):
        global index
        for filename in glob.glob(os.path.join( dir_path + subfolder, "*.*")):
            index += 1
            shutil.copy(filename,  dir_path)
        if os.path.exists(dir_path+subfolder):
            shutil.rmtree( dir_path + subfolder)
            
    # From .png to .jpg converter
    @staticmethod
    def Png_to_jpg_converter(filename, distination_path, img_name):
        im = Image.open(filename)
        im.save(distination_path + img_name.split(".png")[0] + ".jpg","jpeg")
        os.remove(filename)
        
    @staticmethod
    def make_directories(sub_dir):
        if type(sub_dir) != str:
            if os.path.exists(sub_dir[0]):
                if python_version == 3:
                    prompt = input('Directories  already exists. Overwrite? (yes, no): ')
                else:
                    prompt = raw_input('Directoryies already exists. Overwrite? (yes, no): ')
                if prompt == 'no':
                    pass
                if prompt == 'yes':
                    shutil.rmtree(sub_dir[0])
            for i in range(len(sub_dir)):
                os.makedirs(sub_dir[i])
        else:
            os.makedirs(sub_dir)
    @staticmethod                  
    def populate_json_ann(json_path, par ):
        #make & populate json annotation files
        if par != None:
            for i in par:
                f= open(json_path+i["filename"].split('.')[0]+".json","w+")
                f.write(str(i))
                f.close()
        