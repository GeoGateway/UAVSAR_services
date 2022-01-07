import os,sys

from flask import Flask
from Config import config

from .metadata import metadata

def create_app():
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    
    if app.debug:
        app.config.from_object(config['development'])
    else:
        app.config.from_object(config['production'])

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    with app.app_context():
        app.register_blueprint(metadata,url_prefix="/metadata")

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'
    
    @app.route('/test')
    def test():
        info={}
        info["python"] = sys.version
        info["debugmode"] = app.debug
        return "Python: {}<br>DebugMode: {}".format(info["python"],info["debugmode"])
 
    return app
    