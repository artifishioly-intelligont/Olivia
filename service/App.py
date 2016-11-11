from flask import Flask, request
import AppReactions as react

app = Flask(__name__)

@app.route('/')
def show_endpoints():
    print "{} /".format(request.method)
    return 'Endpoints: <br>' \
           '\t/ -- List All Endpoints<br>' \
           '\t/guess/ -- Add the new feature<br>'


@app.route('/learn')
def learn():
    print "{} /learn".format(request.method)

    if request.method == 'GET':
        return react.learn_get()
    elif request.method == 'POST':
        return react.learn_post()
    else:
        return react.unknown_method('/learn')


@app.route('/guess')
def guess():
    print "{} /guess".format(request.method)

    if request.method == 'GET':
        return react.guess_get()
    elif request.method == 'POST':
        return react.guess_post()
    else:
        return react.unknown_method('/guess')


if __name__ == '__main__':
    print 'Log::App:: Starting server'
    app.run()
    print 'Log::App:: Server closing'
