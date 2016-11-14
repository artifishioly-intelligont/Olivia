from flask import Flask, request
import AppReactions as react

app = Flask(__name__)


@app.route('/')
def show_endpoints():
    print "{} /".format(request.method)
    return 'Endpoints: <br>' \
           '\t/ -- List All Endpoints<br>' \
           '\t/convert -- Convert each given file a vector<br>'


@app.route('/convert', methods=['GET', 'POST'])
def convert():
    """
    Given a file, it returns a vector representation of the image

    Expects a set of files to be POST sent to the endpoint
    """
    print "{} /convert".format(request.method)

    if request.method == 'GET':
        return react.convert_get()
    elif request.method == 'POST':
        return react.convert_post()
    else:
        return react.unknown_method('/convert')


if __name__ == '__main__':
    print 'Log::App:: Starting Olivia server'
    app.run()
    print 'Log::App:: Server closing'
