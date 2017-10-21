import sys
from scipy.io import loadmat
from datetime import datetime
from Parser import *

python_version = sys.version_info.major

###########################################################
#####   IMDB-WIKI to JSON_INDB_WIKI Convector    ##########
###########################################################
#This script is run from console terminal
#Sample: C:\Users\User>python imdb_wiki_to_json.py
#You can also specify images and annotations subfolder in dataset archive
#you will extract files from wich.
#Sample: python imdb_wiki_to_json.py --subfolder  wiki_crop/
#By defoult subfolder path for images & annotations extraction: "wiki_crop/"

dataset_archive = "wiki_crop.tar"
imgs_and_anns_subfolder = "wiki_crop/"
imgs_and_anns_destination = 'datasets/IMDB-WIKI/'
json_dir = 'datasets/JSON_IMDB-WIKI/'
annotations_file = 'datasets/IMDB-WIKI/wiki.mat'
directories = [imgs_and_anns_destination, json_dir]
db = "wiki"
subdir_count = 100
subdir = []

class ImdbWikiToJson(Parser):
    
    def __init__(self):
        self.objects = []   
        self.object_info = {}
        self.coords = []
        
    def calc_age(self, taken, dob):
        birth = datetime.fromordinal(max(int(dob) - 366, 1))
        # assume the photo was taken in the middle of the year
        if birth.month < 7:
            return taken - birth.year
        else:
            return taken - birth.year - 1
        
    def parse(self):
        """
            Definition: Make annotations directory for wiki annotations and populate it with separate ann files.
            Returns: None
        """
        meta = loadmat(annotations_file)
        full_path = meta[db][0, 0]["full_path"][0]
        dob = meta[db][0, 0]["dob"][0]  # Matlab serial date number
        gender = meta[db][0, 0]["gender"][0]
        name = meta[db][0, 0]["name"][0]
        face_location = meta[db][0, 0]["face_location"][0]
        photo_taken = meta[db][0, 0]["photo_taken"][0]  # year
        face_score = meta[db][0, 0]["face_score"][0]
        second_face_score = meta[db][0, 0]["second_face_score"][0]
        age = [self.calc_age(photo_taken[i], dob[i]) for i in range(len(dob))]
        ind = -1
        
        for i in range(len(dob)):
            self.object_info['filename'] = str(full_path[i]).split("/")[1].split("'")[0]
            self.object_info['objects'] = []
            self.face_info = {'class_name':'face'}
            for row in face_location[i]:
                for j in row:
                    self.coords.append(int(j))
                self.face_info['bounding_box'] = self.coords
                self.coords = []

            self.face_info['gender'] = gender[i]
            self.face_info['age'] = age[i]
            self.object_info['objects'].append(self.face_info)
                
            self.objects.append(self.object_info.copy())
                
        return self.objects
    
def main():
    namespace = Parser.createParser (None, None, imgs_and_anns_subfolder)
    imdb_wiki = ImdbWikiToJson()
    #make imdb-wiki directories
    imdb_wiki.make_directories(directories)
    imdb_wiki.extract(dataset_archive, namespace.imgs_and_anns_subfolder, imgs_and_anns_destination)
    #Copy images to single folder and remove old folders
    for i in range(subdir_count):
        if i < 10:
            subdir.append("0"+str(i)+"/")
        if i >= 10:
            subdir.append(str(i)+"/")
        imdb_wiki.copy(subdir[i], imgs_and_anns_destination, None)
    # make json directory
    imdb_wiki.populate_json_ann(json_dir, imdb_wiki.parse())

if __name__ == '__main__':
    main()