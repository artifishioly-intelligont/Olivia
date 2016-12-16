"""
Given a URL from the GUI this will decode it to "<map_id>_<X>_<y>"
"""

def decode_url_sent_from_gui(url):
    """ Given a URL sent from the GUI, we can extract the image id
    e.g. http://svm-ec6g13-gdp.ecs.soton.ac.uk/maps/4/actual/actual_files/12/5_7sel.jpg
    becomes 4_5_7 """
    url_sections = url.split("/")
    map_id = url_sections[4]
    x_y = url_sections[-1].split(".")[0][:-3]
    if '#' in url_sections[-1]:
        direction = url_sections[-1].split('#')[-1]
        x_y += '#'+direction
    return map_id+"_"+x_y


def is_url_from_gui(url):
    return url.split("/")[2] == "svm-ec6g13-gdp.ecs.soton.ac.uk"
