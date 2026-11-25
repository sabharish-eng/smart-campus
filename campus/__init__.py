import os
from flask import Flask
from . import db
from .views import bp


def create_app(test_config=None):
    app = Flask(__name__, template_folder="../templates", static_folder="../static")
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev-only-change-me")
    app.config["DATABASE"] = os.path.join(app.root_path, "..", "campus.db")
    if test_config:
        app.config.update(test_config)

    db.init_app(app)
    with app.app_context():
        db.init_db()
    app.register_blueprint(bp)
    return app
