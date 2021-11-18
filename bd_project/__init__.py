from flask import Flask
from bd_project.config import Config
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from playhouse.sqliteq import SqliteQueueDatabase
import atexit

db = SqliteQueueDatabase('bd_project/DB/project.db', use_gevent=False, autostart=True, queue_max_size=64,
                         results_timeout=5.0, pragmas={'foreign_keys': 1})
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'
bcrypt = Bcrypt()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    bcrypt.init_app(app)
    login_manager.init_app(app)

    from bd_project.main.routes import main
    from bd_project.users.routes import users
    from bd_project.admin_users_table.routes import admin_users_table
    from bd_project.admin_couriers_table.routes import admin_couriers_table
    from bd_project.admin_products_table.routes import admin_products_table
    app.register_blueprint(main)
    app.register_blueprint(users)
    app.register_blueprint(admin_users_table)
    app.register_blueprint(admin_couriers_table)
    app.register_blueprint(admin_products_table)

    return app


@atexit.register
def _stop_worker_threads():
    db.stop()
