from flask import Flask, request
import AppConvertReactions as react
import AppDownloadReactions as downloadReact
import json
import memory
import olivia
import traceback

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
        urls = getListParameter('urls')
        if not urls:
            return json.dumps({'success': False, 'message': 'JSON data not provided'})

        ids = getParameter('ids')
        if not ids:
            ids = []

        if len(ids) == 0:
            url_to_id_map = downloadReact.create_ids(urls)
        else:
            url_to_id_map = zip(urls, urls)

        try:
            if olivia.backend == 'gpu':


                result = react.convert_post_gpu(url_to_id_map, True)
                image_vectors = {url.split('#')[0]: result['image_vectors'][url]
                                 for url in result['image_vectors'].keys()
                                 if url.split('#')[1] == 'mid'}

                failed_images = {url.split('#')[0]: result['failed_images'][url]
                                 for url in result['failed_images'].keys()
                                 if url.split('#')[1] == 'mid'}

                result['image_vectors'] = image_vectors
                result['failed_images'] = failed_images
                return json.dumps(result)

            else:
                # Stubbed response
                return json.dumps({'success': False,
                                   'image_vectors': {urls[0]: [0.666] * 1024},
                                   'failed_images': {url: 'This is stubbed, everything is a lie' for url in urls[1:]}})
        except (Exception, BaseException) as ex:
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
        urls = getListParameter('urls')
        if not urls:
            return json.dumps({'success': False, 'message': 'JSON data not provided'})

        ids = getParameter('ids')
        if not ids:
            ids = []

        if len(ids) == 0:
            url_to_id_map = downloadReact.create_ids(urls)
        else:
            url_to_id_map = zip(urls, urls)
        try:
            if olivia.backend == 'gpu':
                return json.dumps(react.convert_post_gpu(url_to_id_map, True))
            else:
                # Stubbed response
                return json.dumps({'success': False,
                                   'image_vectors': {urls[0] + "#" + nsew: [0.666] * 1024
                                                     for nsew in ["NW", "N", "NE", "W", "mid", "E", "SW", "S", "SE"]},
                                   'failed_images': {url: 'This is stubbed, everything is a lie' for url in urls[1:]}})
        except (Exception, BaseException) as ex:
            return handleFailure(ex.message, urls)
    else:
        return react.unknown_method('/convert/nsew')


@app.route('/download', methods=['GET', 'POST'])
def download():
    print "{} /download".format(request.method)

    if request.method == 'GET':
        return downloadReact.download_get()

    elif request.method == 'POST':
        urls = getListParameter('urls')
        if not urls:
            return json.dumps({'success': False, 'message': 'JSON data not provided'})

        ids = getParameter('ids')
        if not ids:
            ids = []

        return json.dumps(downloadReact.download_post(urls, ids))
    else:
        return react.unknown_method('/convert')


@app.route('/seen', methods=['GET', 'POST'])
def seen():
    print "{} /seen".format(request.method)

    if request.method == 'GET':
        return downloadReact.download_get()

    elif request.method == 'POST':
        urls = getListParameter('urls')
        if not urls:
            return json.dumps({'success': False, 'message': 'JSON data not provided'})

        data = {'seen': {}}
        for url in urls:
            id = memory.decode_url_sent_from_gui(url+"#mid")
            data['seen'][url] = not not memory.get_vec(id)
        return json.dumps(data)

    else:
        return react.unknown_method('/convert')
        
@app.route('/clear')
def clear():
    downloadReact.clear_memory()
    data = { 'success': True }
    return json.dumps(data)
        


def getListParameter(key):
    if request.get_json() and key in request.get_json():
        return request.get_json()[key]
    elif request.form and key in request.form:
        raw_list = request.form[key].split(';')
        if '' in raw_list:
            raw_list.remove('')
        return raw_list
    else:
        return False


def getParameter(key):
    if request.get_json() and key in request.get_json():
        return request.get_json()[key]
    elif request.form and key in request.form:
        return request.form[key]
    else:
        return False


def handleFailure(message, urls):
    traceback.print_exc()

    failed_images = {}
    for url in urls:
        failed_images[url] = message
    data = {'success': False,
            'image_vectors': {},
            'failed_images': failed_images}
    return json.dumps(data)


if __name__ == '__main__':
    print 'Log::App:: Starting Olivia server'
    app.run(port=5001)
    print 'Log::App:: Server closing'
