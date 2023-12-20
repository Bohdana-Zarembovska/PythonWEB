from flask import render_template, redirect, url_for, flash
from ..extensions import db
from .forms import TodoForm
from .models import Todo
from . import todo_bp


@todo_bp.route('/', methods=["GET"])
def todo_page():
    form=TodoForm()
    return render_template("todo/todo.html", todo_list=Todo.query.all(), form=form)
 
@todo_bp.route("/", methods=["POST"])
def add():
    form=TodoForm()

    new_todo = Todo(
        title = form.title.data, 
        due_date = form.due_date.data, 
        complete = False
    )
    try: 
        db.session.add(new_todo)
        db.session.commit()
        flash('Todo added!', category='success')
    except:
        db.session.rollback()
        flash('Error!', category='danger')
    return redirect(url_for("todo.todo_page"))
 
@todo_bp.route("/update/<int:id>")
def update(id):
    todo = Todo.query.get_or_404(id)
    todo.complete = not todo.complete   
    try: 
        db.session.commit()
        flash(f'Todo({todo.id}) updated!', category='success')
    except:
        db.session.rollback()
        flash('Error!', category='danger')    
    return redirect(url_for("todo.todo_page"))
 
@todo_bp.route("/delete/<int:id>")
def delete(id):
    todo = Todo.query.get_or_404(id)
    try: 
        db.session.delete(todo)
        db.session.commit()
        flash(f'Todo({todo.id}) deleted!', category='success')
    except:
        db.session.rollback()
        flash('Error!', category='danger')    
    return redirect(url_for("todo.todo_page"))


