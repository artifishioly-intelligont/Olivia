from flask import Flask, request
import AppReactions as react
import json
import olivia

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
        {
            'url1' : [0.1, 0.0, 0.5, ...],
            'url2' : [0.9, 1.2, 0.6, ...]
        },
        failed_images : []
    }
    example (failed) return:
    {
        success : False,
        image_vectors :
        {
             'url1' : [0.1, 0.0, 0.5, ...]
        },
        failed_images :
        {
             'url2' : 'DownloadException: The path url2 does not exist'
        }
    }
    """
    print "{} /convert".format(request.method)

    if request.method == 'GET':
        return react.convert_get()

    elif request.method == 'POST':
        try:
            urls = request.get_json()['urls']
        except TypeError:
            return json.dumps({'success': False, 'message': 'JSON data not provided'})
        try:
            if olivia.backend == 'gpu':
                return react.convert_post_gpu(urls)
            else:
                # Stubbed response
                return json.dumps({'success': False,
                                   'image_vectors': {urls[0]: [0.666]*1024},
                                   'failed_images': {url: 'This is stubbed, everything is a lie' for url in urls[1:]}})
        except (Exception, BaseException) as ex:
	    import traceback
	    traceback.print_exc()
            return handleFailure(ex.message, urls)
    else:
        return react.unknown_method('/convert')

@app.route('/convert/nsew', methods=['GET', 'POST'])
def nsew_convert():
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
        {
            'url1#NW' : [0.1, 0.0, 0.5, ...],
            'url1#N' : [0.1, 0.0, 0.5, ...],
            'url1#NE' : [0.1, 0.0, 0.5, ...],
            'url1#W' : [0.1, 0.0, 0.5, ...],
            'url1#mid' : [0.1, 0.0, 0.5, ...],
            'url1#E' : [0.1, 0.0, 0.5, ...],
            'url1#SW' : [0.1, 0.0, 0.5, ...],
            'url1#S' : [0.1, 0.0, 0.5, ...],
            'url1#E' : [0.1, 0.0, 0.5, ...],
        },
        failed_images : []
    }
    example (failed) return:
    {
        success : False,
        image_vectors :
        {
            'url1#NW' : [0.1, 0.0, 0.5, ...],
            'url1#N' : [0.1, 0.0, 0.5, ...],
            'url1#NE' : [0.1, 0.0, 0.5, ...],
            'url1#W' : [0.1, 0.0, 0.5, ...],
            'url1#mid' : [0.1, 0.0, 0.5, ...],
            'url1#E' : [0.1, 0.0, 0.5, ...],
            'url1#SW' : [0.1, 0.0, 0.5, ...],
            'url1#S' : [0.1, 0.0, 0.5, ...],
            'url1#E' : [0.1, 0.0, 0.5, ...],
        },
        failed_images :
        {
             'url2' : 'DownloadException: The path url2 does not exist'
        }
    }
    """
    print "{} /convert/nsew".format(request.method)

    if request.method == 'GET':
        return react.convert_get()

    elif request.method == 'POST':
        try:
            urls = request.get_json()['urls']
        except TypeError:
            return json.dumps({'success': False, 'message': 'JSON data not provided'})
        try:
            if olivia.backend == 'gpu':
                return react.convert_post_gpu(urls, True)
            else:
                # Stubbed response
                return json.dumps({'success': False,
                                   'image_vectors': {urls[0]+"#"+nsew: [0.666]*1024
                                                     for nsew in ["NW", "N", "NE", "W", "mid", "E", "SW", "S", "SE"]},
                                   'failed_images': {url: 'This is stubbed, everything is a lie' for url in urls[1:]}})
        except (Exception, BaseException) as ex:
            return handleFailure(ex.message, urls)
    else:
        return react.unknown_method('/convert/nsew')


def handleFailure(message, urls):
    failed_images = {}
    for url in urls:
        failed_images[url] = message
    data = {'success' : False,
            'image_vectors': {},
            'failed_images' : failed_images}
    return json.dumps(data)


if __name__ == '__main__':
    print 'Log::App:: Starting Olivia server'
    app.run(port=5001)
    print 'Log::App:: Server closing'
