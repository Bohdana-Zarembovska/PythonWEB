from flask import Flask
from .extensions import db, migrate, bcrypt, login_manager
from config import config
from app.auth.views import auth_bp
from app.resume.views import resume_bp
from app.cookies.views import cookies_bp
from app.todo.views import todo_bp


def create_app(config_name = 'default'):
    app = Flask(__name__)
    app.config.from_object(config.get(config_name))

    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    with app.app_context():
        app.register_blueprint(auth_bp, url_prefix='/')
        app.register_blueprint(resume_bp, url_prefix='/resume')
        app.register_blueprint(cookies_bp, url_prefix='/cookies')
        app.register_blueprint(todo_bp, url_prefix='/todo')
        return app