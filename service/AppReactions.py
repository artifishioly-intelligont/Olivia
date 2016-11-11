def unknown_method(endpoint):
    return "<h1>Incorrect Usage</h1> \
    <br> {} does not know what to do with this request type".format(endpoint)


def learn_get():
    return "<h1>Incorrect Usage</h1>\
    <br>/learn only accepts POST\
    <br>POST expects a number of image files to be sent to it\
    <br>\
    <br>The return is JSON response of the images that failed, fail messages and the overall sucess\
    <br>Note: If one image fails the overall success is False\
    <br>Example Return:\
    <br>{\
    <br>  'success' : True\
    <br>  'failed_images' : []\
    <br>  'failed_messages' : []\
    <br>} "


def guess_get():
    return "<h1>Incorrect Usage</h1>\
    <br>/guess only accepts POST\
    <br>POST expects a number of image files to be sent to it"


def learn_post():
    return 'Not Implemented Yet'


def guess_post():
    return 'Not Implemented Yet'

