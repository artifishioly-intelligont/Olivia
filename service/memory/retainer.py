"""
This populates the memory.vectorized_images on startup
"""


class Retainer:

    csv_file = None

    ids_to_vectors = {}
    map_to_image_ids = {}

    def __init__(self, seed_csv="ID_TO_VECTOR.csv"):
    
        self.csv_file = seed_csv
        
        try:
            # Populate ids_to_vectors ids and attribute vectors from the csv file
            with open(seed_csv) as myfile:
                csvread = csv.reader(myfile)
                for row in csvread:
                    vecs = []
                    for val in row[1:]:
                        vecs.append(float(val))
                    self.ids_to_vectors[float(row[0])] = float(vecs)
                    
            # Populate the map_to_image_ids from the 
            for image_id in ids_to_vectors.keys():
                map_id = image_id.split("_")[0]
                if map_id in map_to_image_ids:
                    map_to_image_ids[map_id].append(image_id)
                else:
                    map_to_image_ids = [image_id]
            
        except IOError:
            open(seed_csv, 'a')
            print "Creating file '" + seed_csv + "'"                
        
        
    def seen_image(id):
        map_id = id.split("_")[0]
        
        if map_id in map_to_image_ids.keys():
            return id in map_to_image_ids[map_id]
        else:
            return False

            
    def remember_map(id):
        pass


    def remember(image_id,attr_vector):
        pass

    def clear():
        pass

    def remove(map_id):
        pass


        
    