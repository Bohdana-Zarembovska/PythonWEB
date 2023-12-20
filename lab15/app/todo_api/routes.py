from flask import  request, jsonify
from app.todo.models import Todo
from app.todo.forms import TodoForm
from ..extensions import db
from .service import TodoMapper, TodoValidator
from . import todo_api_bp
from flask import Blueprint
from flask_jwt_extended import jwt_required

todo_api_bp = Blueprint('todo_api_bp', __name__)

@todo_api_bp.route('/', methods=['GET'])
@jwt_required()
def get_all_todos_api():
    todos = Todo.query.all()
    todos_dict = [todo.to_dict() for todo in todos]
    return jsonify(todos_dict)

@todo_api_bp.route('/<int:id>', methods=['GET'])
@jwt_required()
def get_todo_api(id):
    todo = Todo.query.get_or_404(id)
    return jsonify(todo.to_dict())

@todo_api_bp.route('/', methods=['POST'])
@jwt_required()
def create_todo_api():
    data = request.get_json()
    form = TodoForm(data=data)

    if form.validate():
        new_todo = Todo(
            title=form.title.data,
            due_date=form.due_date.data,
            complete=False
        )

        try:
            db.session.add(new_todo)
            db.session.commit()
            return jsonify(new_todo.to_dict()), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({"message": f"Error: {e}"}), 500
    else:
        return jsonify({"message": "Validation error", "errors": form.errors}), 400

@todo_api_bp.route('/<int:id>', methods=['PUT'])
@jwt_required()
def update_todo_api(id):
    todo = Todo.query.get_or_404(id)
    data = request.get_json()
    form = TodoForm(data=data)

    if form.validate():
        todo.title = form.title.data
        todo.due_date = form.due_date.data
        todo.complete = not todo.complete

        try:
            db.session.commit()
            return jsonify(todo.to_dict()), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({"message": f"Error: {e}"}), 500
    else:
        return jsonify({"message": "Validation error", "errors": form.errors}), 400

@todo_api_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_todo_api(id):
    todo = Todo.query.get_or_404(id)

    try:
        db.session.delete(todo)
        db.session.commit()
        return '', 204
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"Error: {e}"}), 500