from flask import Flask, url_for
from .extensions import db, migrate, bcrypt, login_manager, jwt_manager
from config import config
from app.auth.views import auth_bp
from app.resume.views import resume_bp
from app.cookies.views import cookies_bp
from app.todo.views import todo_bp
from app.posts.views import posts_bp
from app.todo_api.routes import todo_api_bp
from app.auth_api.routes import auth_api_bp
from .extensions import db, migrate, bcrypt, login_manager, jwt_manager, ma
from app.swagger import swagger_bp
from app.user_api import user_api_bp

def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config.get(config_name))

    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    jwt_manager.init_app(app)
    ma.init_app(app)

    @app.before_request
    def before_request():
        print("URL for /api/todos:", url_for('todo_api_bp.get_all_todos_api'))

    with app.app_context():
        app.register_blueprint(auth_bp, url_prefix='/')
        app.register_blueprint(resume_bp, url_prefix='/resume')
        app.register_blueprint(cookies_bp, url_prefix='/cookies')
        app.register_blueprint(todo_bp, url_prefix='/todo')
        app.register_blueprint(posts_bp, url_prefix='/posts')
        app.register_blueprint(todo_api_bp, url_prefix='/api/todos')
        app.register_blueprint(auth_api_bp, url_prefix='/api/auth')
        app.register_blueprint(swagger_bp, url_prefix='/swagger')
        app.register_blueprint(user_api_bp, url_prefix='/api')

        return app