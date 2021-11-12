from flask import Flask
from bd_project.config import Config
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from playhouse.sqliteq import SqliteQueueDatabase
import atexit

db = SqliteQueueDatabase('bd_project/DB/project.db', use_gevent=False, autostart=True, queue_max_size=64,
                         results_timeout=5.0, pragmas={'foreign_keys': 1})
login_manager = LoginManager()
bcrypt = Bcrypt()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    bcrypt.init_app(app)
    login_manager.init_app(app)

    from bd_project.main.routes import main
    from bd_project.users.routes import users
    from bd_project.admin.routes import admin
    app.register_blueprint(main)
    app.register_blueprint(users)
    app.register_blueprint(admin)

    return app


@atexit.register
def _stop_worker_threads():
    db.stop()
