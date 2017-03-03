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

    def __init__(self, seed_csv=os.path.expanduser("~/IDS_TO_VECTORS.csv")):
    
        self.csv_file = seed_csv
        
        try:
            # Populate ids_to_vectors ids and attribute vectors from the csv file
            with open(seed_csv) as myfile:
                csvread = csv.reader(myfile)
                for row in csvread:
                    vecs = []
                    for val in row[1:]:
                        vecs.append(float(val))
                    self.ids_to_vectors[row[0]] = vecs
                    
            self.update_map_to_image_ids()

        except IOError:
            open(seed_csv, 'a')
            print "Creating file '" + seed_csv + "'"                
        
            
    """
    :function
            get_vec
    :param  
            id: A string in the format '<map_id>_<x>_<y>'
               e.g. '10_2_3' would mean 'Map 10, tile coordinates (2,3)'
    :return 
            attr_vec or False
    :description
            Returns the attribute vector corresponding to an image ID if 
            that image has already been processed, otherwise returns False.
    """
    def get_vec(self, id):
        if self.seen_image(id):
            return self.ids_to_vectors[id]
        else:
            return False

    """
    :function
            remember_vec
    :param  
            image_id: A string in the format '<map_id>_<x>_<y>'
               e.g. '10_2_3' would mean 'Map 10, tile coordinates (2,3)'
               
            attr_vector: The attribute vector corresponding to the image ID
    :return 
            None
    :description
            Takes a matching image id and attribute vector, and stores them
            in a csv file, so that image doesn't need to be processed again
    """
    def remember_vec(self, image_id, attr_vector):
        self.ids_to_vectors[image_id] = attr_vector
        self.update_map_to_image_ids()
        self.save()
            
    """
    :function
            clear
    :param  
            None
    :return 
            None
    :description
            Clears the csv file mapping image ids to attribute vectors
    """
    def clear(self):
        self.ids_to_vectors = {}
        self.map_to_image_ids = {}
        
    """
    :function
            remove
    :param  
            map_id: A String containing the ID of the map to be removed
               e.g. '10' = delete all entries for map 10
    :return 
            None
    :description
            Takes a map ID in string format, and deletes all entries corresponding
            to that map from the csv file. 
            (To be used if a map is deleted from history so its ID can be re-used)
    """
    def remove(self, map_id):    
        ids = self.map_to_image_ids[map_id]
        
        for id in ids:
            del self.ids_to_vectors[id]
            
        del self.map_to_image_ids[map_id]
          
            
    """
    :function
            save
    :param  
            None
    :return 
            None
    :description
            Stores all current entries in ids_to_vectors
            into a csv file.
    """
    def save(self):
        data = deepcopy(self.ids_to_vectors)

        # Save it locally
        with open(self.csv_file, 'wb') as f:
            wtr = csv.writer(f, delimiter= ',')
            for id, vec in data.items():
                wtr.writerow([id] + list(vec))
        
    """
    Auxiliary function for checking if an image has already been processed
    """    
    def seen_image(self, id):
        return id in self.ids_to_vectors.keys()
    
    """
    Auxiliary function for storing an image_id in map_to_image_ids
    """ 
    def remember_map(self, image_id):
        map_id = image_id.split("_")[0]
        if map_id in self.map_to_image_ids:
            if image_id not in self.map_to_image_ids[map_id]:
                self.map_to_image_ids[map_id].append(image_id)
        else:
            self.map_to_image_ids[map_id] = [image_id]
            
        
    """
    Auxiliary function for updating map_to_image_ids whenever a new image is added
    """ 
    def update_map_to_image_ids(self):
        # Populate the map_to_image_ids from the ids_to_vectors
        for image_id in self.ids_to_vectors.keys():
            self.remember_map(image_id)
            
            
        
    def __del__(self):
        self.save()


if __name__ == "__main__":

    r = Retainer()
    
    r.remember_vec('1_1_1', [0,1,2,3])
    r.remember_vec('2_2_2', [0,2,4,6])
    
    print r.seen_image('1_1_1') == True
    print r.seen_image('2_2_2') == True
    print r.seen_image('3_3_3') == False
    
    print r.get_vec('1_1_1')
    print r.get_vec('2_2_2')
    print r.get_vec('3_3_3') == False
    
#    r.remove('1')
    
#    print r.seen_image('1_1_1') == False
    
#    r.clear()
    
#    print r.seen_image('2_2_2') == False

