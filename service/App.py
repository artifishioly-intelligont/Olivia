from flask import Flask, request
import AppReactions as react

app = Flask(__name__)

@app.route('/')
def show_endpoints():
    print "{} /".format(request.method)
    return 'Endpoints: <br>' \
           '\t/ -- List All Endpoints<br>' \
           '\t/convert -- Convert each given file a vector<br>'


@app.route('/convert')
def learn():
    print "{} /convert".format(request.method)

    if request.method == 'GET':
        return react.convert_get()
    elif request.method == 'POST':
        return react.conver_post()
    else:
        return react.unknown_method('/convert')


if __name__ == '__main__':
    print 'Log::App:: Starting Olivia server'
    app.run()
    print 'Log::App:: Server closing'
