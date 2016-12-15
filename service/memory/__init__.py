import retainer
from url_decoder import decode_url_sent_from_gui, is_url_from_gui

ret = retainer.Retainer()


def seen_image(image_id):
    return ret.seen_image(image_id)


def remember_vec(image_id,attr_vector):
    ret.remember_vec(image_id,attr_vector)

    
def clear():
    ret.clear()

    
def remove(map_id):
    ret.remove(map_id)



