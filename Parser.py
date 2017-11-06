import os, sys, glob
import tarfile
import zipfile
import argparse
import shutil
import logging

def extract_zip(archive, destination):
    if os.path.exists(archive):
        with zipfile.ZipFile(archive, "r") as z:
            z.extractall(destination)
    else:
        logging.error( u'Archive not found!')
        

def extract_tar(archive, destination):
    if os.path.exists(archive):
        with tarfile.open(archive) as tar:
            tar.extractall(path = destination)
    else:
        logging.error( u'Archive not found!')

def extract_archive(archive, destination): 
    filename, file_extension = os.path.splitext(archive)
    if file_extension == '.zip':
        extract_zip(archive, destination)
    elif file_extension == '.tar':
        extract_tar(archive, destination)
    # TODO else: error that file format not supported

class Parser(object):
    def __init__(self):
        pass
    def parse(self):
        raise NotImplementedError("To be implemented")

  
