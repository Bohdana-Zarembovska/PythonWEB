from flask import Blueprint

todo_api_bp = Blueprint('todo_api', __name__, url_prefix="/api/todos")