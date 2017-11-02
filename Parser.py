import os, sys, glob
import tarfile
import zipfile
import argparse
import shutil
import logging

def extract_zip(archive, dir_path):
    if os.path.exists(archive):
        with zipfile.ZipFile(archive, "r") as z:
            z.extractall(dir_path)
    else:
        logging.error( u'Archive not found!')
        

def extract_tar(archive, dir_path):
    if os.path.exists(archive):
        with tarfile.open(archive) as tar:
            tar.extractall(path = dir_path)
    else:
        logging.error( u'Archive not found!')

def extract_archive(archive, dir_path): 
    filename, file_extension = os.path.splitext(archive)
    if file_extension == '.zip':
        extract_zip(archive, dir_path)
    elif file_extension == '.tar':
        extract_tar(archive, dir_path)

class Parser(object):
    def __init__(self):
        pass
    def parse(self):
        raise NotImplementedError("To be implemented")

  