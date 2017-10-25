import os, sys, glob
import tarfile
import zipfile
import argparse
import shutil

python_version = sys.version_info.major

#index = 0
ext_list = ['.jpg','.png', '.mat', 'wider_face_split/wider_face_train_bbx_gt']
class Parser(object):
    def __init__(self):
        pass

    def parse(self):
        pass
    
    def archive_members(self, tf, subfolder):
        l = len(subfolder)
        for member in tf.getmembers():
            if member.path.startswith(subfolder):
                member.path = member.path[l:]
                yield member
    
    def extract_zip(self, archive, subfolder, dir_path):
        _archive = zipfile.ZipFile(archive)
        for file in _archive.namelist():
            if file.startswith(subfolder):
                filename, file_extension = os.path.splitext(file)
                if (x for x in ext_list if (x == file_extension or x == filename)):
                    if os.path.exists(dir_path): 
                        _archive.extract(file, dir_path)

    def extract_tar(self, archive, subfolder, dir_path):
        with tarfile.open(archive) as tar:
                if os.path.exists(dir_path):  
                    if subfolder.split(".") != "mat":
                        tar.extractall(members=self.archive_members(tar, subfolder), path = dir_path)
                    else:
                        for entry in tar:
                            fileobj = tf.extractfile(entry)

    def extract(self, archive, subfolder, dir_path): 
        filename, file_extension = os.path.splitext(archive)
        if file_extension == '.zip':
            self.extract_zip(archive, subfolder, dir_path)
        else:
            self.extract_tar(archive, subfolder, dir_path)
            
    
    def make_directories(self, sub_dir):
        if type(sub_dir) != str:
            for i in range(len(sub_dir)):
                if os.path.isdir(sub_dir[i]): shutil.rmtree(sub_dir[i])
            for i in range(len(sub_dir)):
                os.makedirs(sub_dir[i])
        else:
            if os.path.isdir(sub_dir): shutil.rmtree(sub_dir)
            os.makedirs(sub_dir)
  