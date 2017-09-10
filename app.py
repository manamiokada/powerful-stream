import os
import conf
import flickrapi
from flask import Flask, render_template, request
app = Flask(__name__)


def init():
    global flickr
    flickr = flickrapi.FlickrAPI(conf.key, conf.secret, format='parsed-json')

@app.route('/')
def index():
    photoset = flickr.photosets.getPhotos(photoset_id='72157688275976596', user_id='97801184@N07')
    return render_template('index.html', user='janedoe', title='HOME', photoset=photoset['photoset']['photo'])

def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()

@app.route('/stop', methods=['GET'])
def shutdown():
    shutdown_server()
    return 'Server shutting down...'


if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    init()
    app.debug = True
    app.run(host='0.0.0.0', port=port)
