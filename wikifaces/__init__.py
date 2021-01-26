"importing Flask class"
"render_template allows to return html templates in our routes"
from flask import Flask
from wikifaces.config import Config
#== Parameters =======================================================================



"creates instance of app | takes Config(app configuration we imported as param)"
def create_app(config_class=Config):

    "creating Flask variable and setting it as instance of flask class"
    app = Flask(__name__) # when run script directly( so flask knows where are scripts and stat files)

    "we pass this object as configuration"
    app.config.from_object(Config)

    "errors handling"
    from wikifaces.routes import routes
    app.register_blueprint(routes)
    "register routes"
    from wikifaces.errors.handlers import errors
    app.register_blueprint(errors)

    # from wikifaces import routes

    return app
