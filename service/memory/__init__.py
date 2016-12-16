import retainer
from url_decoder import decode_url_sent_from_gui, is_url_from_gui

ret = retainer.Retainer()

"""
:function
        get_vec
:param  
        image_id: A string in the format '<map_id>_<x>_<y>'
           e.g. '10_2_3' would mean 'Map 10, tile coordinates (2,3)'
:return 
        attr_vec or False
:description
        Returns the attribute vector corresponding to an image ID if 
        that image has already been processed, otherwise returns False.
"""
def get_vec(image_id):
    return ret.get_vec(image_id)


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
def remember_vec(image_id,attr_vector):
    ret.remember_vec(image_id,attr_vector)

    
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
def clear():
    ret.clear()

    
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
def remove(map_id):
    ret.remove(map_id)



