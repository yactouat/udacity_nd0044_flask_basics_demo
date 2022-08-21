from flask import Flask, jsonify

from routes import init_routes


def create_app(test_config=None):

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
        return jsonify({
            "msg": "resource not found, aborting...",
            "success": False,
            "data": None
        }), 404

    # initialisation des routes
    init_routes(app)

    return app
