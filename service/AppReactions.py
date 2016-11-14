def unknown_method(endpoint):
    return "<h1>Incorrect Usage</h1> \
    <br> {} does not know what to do with this request type".format(endpoint)


def convert_get():
    return "<h1>Incorrect Usage</h1>\
    <br>/convert only accepts POST\
    <br>POST expects a number of files to be sent to it"


def convert_post():
    return 'Not Implemented Yet'

