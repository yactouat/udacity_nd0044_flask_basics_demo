from flask import Flask, jsonify, request
from logging.config import dictConfig

from routes import init_routes


def create_app(test_config=None):

    dictConfig({
        'version': 1,
        'formatters': {'default': {
            'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
        }},
        'handlers': {'app_logger': {
            'class': 'logging.FileHandler',
            'filename': 'logs.log',
            'formatter': 'default'
        }},
        'root': {
            'level': 'INFO',
            'handlers': ['app_logger']
        }
    })

    # creates an application that is named after the name of the file
    app = Flask(__name__)

    app.config["SECRET_KEY"] = "some_dev_key"
    # alternative configuration based on if is test env or not
    if test_config is None:
        app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://usr:pwd@pgsql:5432/todos"
    elif test_config == "test":
        app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://usr:pwd@pgsql-test:5433/todos"

    @app.errorhandler(404)
    def not_found(error):
        app.logger.info(
            f"404 => user tried to access route {request.full_path}"
        )
        return jsonify({
            "msg": "resource not found, aborting...",
            "success": False,
            "data": None
        }), 404

    # initialisation des routes
    init_routes(app)

    return app
