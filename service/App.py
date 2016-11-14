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
    POST: Given a list of URLS, it returns a vector representation of the image
    GET: Friendly HTML error response
    Otherwise: HTML error response

    Expects a set of files to be POST sent to the endpoint


        :return:
    example (successful) return:
    {
        success : True,
        image_vectors :
        [
            { 'url1' : [0.1, 0.0, 0.5, ...] },
            { 'url2' : [0.9, 1.2, 0.6, ...]}
        ],
        failed_images : []
    }
    example (failed) return:
    {
        success : False,
        image_vectors :
        [
            { 'url1' : [0.1, 0.0, 0.5, ...] }
        ],
        failed_images :
        [
            { 'url2' : 'DownloadException: The path url2 does not exist'}
        ]
    }
    """
    print "{} /convert".format(request.method)

    if request.method == 'GET':
        return react.convert_get()

    elif request.method == 'POST':
        urls = request.get_json()['urls']
        return react.convert_post(urls)

    else:
        return react.unknown_method('/convert')


if __name__ == '__main__':
    print 'Log::App:: Starting Olivia server'
    app.run()
    print 'Log::App:: Server closing'
