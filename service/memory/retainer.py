"""
This populates the memory.vectorized_images on startup
"""

from copy import deepcopy
from itertools import izip
import os
import csv


class Retainer:

    csv_file = None

    ids_to_vectors = {}
    map_to_image_ids = {}

    def __init__(self, seed_csv="IDS_TO_VECTORS.csv"):
    
        self.csv_file = seed_csv
        
        try:
            # Populate ids_to_vectors ids and attribute vectors from the csv file
            with open(seed_csv) as myfile:
                csvread = csv.reader(myfile)
                for row in csvread:
                    vecs = []
                    for val in row[1:]:
                        vecs.append(val)
                    self.ids_to_vectors[row[0]] = vecs
                    
            self.update_map_to_image_ids()

        except IOError:
            open(seed_csv, 'a')
            print "Creating file '" + seed_csv + "'"                
        
        
    def seen_image(self, id):
        map_id = id.split("_")[0]
        
        if map_id in self.map_to_image_ids.keys():
            return id in self.map_to_image_ids[map_id]
        else:
            return False

            
    def remember_vec(self, image_id, attr_vector):
        self.ids_to_vectors[image_id] = attr_vector
        self.update_map_to_image_ids()


    def remember_map(self, image_id):
        map_id = image_id.split("_")[0]
        if map_id in self.map_to_image_ids:
            self.map_to_image_ids[map_id].append(image_id)
        else:
            self.map_to_image_ids[map_id] = [image_id]
            

    def clear(self):
        self.ids_to_vectors = {}
        self.map_to_image_ids = {}
        

    def remove(self, map_id):
        del self.ids_to_vectors[self.map_to_image_ids[map_id]]
        del self.map_to_image_ids[map_id]
        
        
    def update_map_to_image_ids(self):
        # Populate the map_to_image_ids from the ids_to_vectors
        for image_id in self.ids_to_vectors.keys():
            self.remember_map(image_id)
        
        
    def save(self):
        ids = deepcopy(self.ids_to_vectors.keys())
        vecs = deepcopy(self.ids_to_vectors.values())
        
        print ids
        print vecs
        print self.csv_file
        
        # Save it locally
        # TODO - check this doesn't mess up the order!
        try:
            with open(self.csv_file, 'wb') as f:
                wtr = csv.writer(f, delimiter= ',')
                wtr.writerows([[ids[index], vecs[index]] for index in range(len(ids))])
        except IOError:
            print "Could not open csv file to save data"

    def __del__(self):
        self.save()

        
if __name__ == "__main__":

    r = Retainer()
    
    r.remember_vec('1_1_1', [0,1,2,3])
    r.remember_vec('2_2_2', [0,2,4,6])
    
    print r.ids_to_vectors
    print r.map_to_image_ids
    
    r.save()
    print "----"