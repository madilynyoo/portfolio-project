import os
from flask import Flask
def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='27a798b430da3eb2fb1ece01fed4c6d142d16ea1bd572ab590e8a7e5a1b4461d',
        DATABASE=os.path.join(app.instance_path, 'flaskblog.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'
    
    from db import init_app
    db = init_app(app)

    from auth import auth
    app.register_blueprint(auth.bp)

    from blog import blog
    app.register_blueprint(blog.bp)
    app.add_url_rule('/', endpoint='index')

    return app