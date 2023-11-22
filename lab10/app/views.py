from flask import Flask, flash, render_template, request, redirect, url_for, json, make_response, session
import os
from datetime import datetime
from app import app
from app.forms import LoginForm, ChangePasswordForm, CreateTodo, RegistrationForm, UpdateAccountForm
from app.models import db, Todo
import random
from flask_login import login_user, current_user, logout_user, login_required
from app.models import User
from datetime import datetime
import os
import secrets
from PIL import Image

my_skills = ["Data Science/Machine Learning", "Pandas/NumPy/SciPy/Matplotlib", "MySQL", "HTML & CSS", "Jupyter Notebook", "Python", "OpenCV", "Deep Learning"]

def save_picture(form_picture):
    hex_token = secrets.token_hex(8)
    _, ext = os.path.splitext(form_picture.filename)
    picture_fn = hex_token + ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)
    image = Image.open(form_picture)
    image.thumbnail((150, 150))
    image.save(picture_path)

    return picture_fn

def get_user_info():
    user_os = os.name
    user_agent = request.headers.get('User-Agent')
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return user_os, user_agent, current_time

@app.route('/base')
def index():
    user_os, user_agent, current_time = get_user_info()
    return render_template('base.html', user_os=user_os, user_agent=user_agent, current_time=current_time)

@app.route('/home')
@app.route('/')
def home():
    user_os, user_agent, current_time = get_user_info()
    return render_template('home.html', user_os=user_os, user_agent=user_agent, current_time=current_time)

@app.route('/education')
def education():
    return render_template('education.html')

@app.route('/skills')
def cv():
    return render_template('skills.html')

@app.route('/hobbies')
def hobbies():
    return render_template('hobbies.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('info'))
    
    form = RegistrationForm()
    
    if form.validate_on_submit():
        new_user = User(name=form.username.data, email=form.email.data, password=form.password.data)
        try:
            db.session.add(new_user)
            db.session.commit()
            flash(f"Account created for {form.username.data}!", "success")
        except:
            db.session.rollback()
            flash("Something went wrong!", category="danger")
        return redirect(url_for("login"))
    
    return render_template('register.html', form=form)

@app.route('/account')
@login_required
def account():
    password_form = ChangePasswordForm()
    info_form = UpdateAccountForm()
    return render_template('account.html', password_form=password_form, info_form=info_form)

@app.after_request
def after_request(response):
    if current_user:
        current_user.last_seen = datetime.now()
        try:
            db.session.commit()
        except:
            flash('Error while update user last seen!', 'danger')
    return response

@app.route('/login', methods=['GET', 'POST'])
def login():

    if current_user.is_authenticated:
        return redirect(url_for('info'))
    
    form = LoginForm()


    if form.validate_on_submit(): 
        user = User.query.filter_by(email=form.email.data).first()
        
        if user and user.verify_password(form.password.data): 
            if form.remember.data:
                login_user(user, remember=form.remember.data)
                flash("Logged in successfully!", category="success")
                return redirect(url_for("info"))
                
            flash("Logged in successfully to about!!", category="success")
            return redirect(url_for("about_page"))

        flash("Wrong data! Try again!", category="danger")
        return redirect(url_for("login"))
    
    return render_template('login.html', form=form)

@app.route('/update-user', methods=["POST"])
@login_required
def update_user():
    form = UpdateAccountForm(current_user=current_user)

    if form.validate_on_submit():
        try:
            if form.picture.data:
                picture_path = save_picture(form.picture.data)
                if picture_path:
                    current_user.image = picture_path
                else:
                    flash('Failed to save the profile picture.', 'danger')
                    return redirect(url_for("account"))
            
            current_user.username = form.username.data
            current_user.email = form.email.data
            current_user.about_me = form.about_me.data

            db.session.commit()
            print(f"current_user.image after commit: {current_user.image}")  # Додайте цей вивід
            flash("Info updated!", category="success")
            return redirect(url_for("account"))
            
            current_user.username = form.username.data
            current_user.email = form.email.data
            current_user.about_me = form.about_me.data

            db.session.commit()
            flash("Info updated!", category="success")
            return redirect(url_for("account"))
        except Exception as e:
            db.session.rollback()
            flash(f"Failed: {str(e)}", category="danger")

    flash("Validation error!", category="danger")
    return render_template('account.html', password_form=ChangePasswordForm(), info_form=form)

@app.route('/logout', methods=["GET", "POST"])
def logout():
    if request.method == 'POST':
        session.clear()
        flash("Logged out successfully!", category="success")
        return redirect(url_for("login"))
    else:
        # Handle the case where the user accesses the /logout URL directly
        flash("To log out, please use the provided logout link.", category="warning")
        return redirect(url_for("login"))

@app.route('/users')
def users():
    return render_template('users.html', users=User.query.all())


@app.route('/info', methods=['GET'])
def info():
    cookies = request.cookies
    form = ChangePasswordForm()

    return render_template('info.html', cookies=cookies, form=form)

@app.route('/skills/')
@app.route('/skills/<int:id>')
def skills(id=None):
    if id is not None:
        if 0 <= id < len(my_skills):
            skill = my_skills[id]
            return render_template('skills.html', skill=skill)
        else:
            return render_template('skills.html')
    else:
        return render_template('skills.html', skills=my_skills, total_skills=len(my_skills))

def set_cookie(key, value, max_age):
    response = make_response(redirect('info'))
    response.set_cookie(key, value, max_age=max_age)
    return response

def delete_cookie(key):
    response = make_response(redirect('info'))
    response.delete_cookie(key)
    return response

@app.route('/add_cookie', methods=['POST'])
def add_cookie():
    key = request.form.get('key')
    value = request.form.get('value')
    max_age = int(request.form.get('max_age'))

    flash("Cookie додано", category=("success"))
    return set_cookie(key, value, max_age)

@app.route('/remove_cookie/', methods=['GET'])
@app.route('/remove_cookie/<key>', methods=['GET'])
def remove_cookie():

    key = request.args.get('key')

    if key:
        flash("Cookie видалено", category=("dark"))
        response = make_response(redirect(url_for('info')))
        response.delete_cookie(key)
        return response
    else:
        flash("Error", category=("info"))
        response = make_response(redirect(url_for('info')))
        return response

@app.route('/remove_all_cookies', methods=['GET'])
def remove_all_cookies():
    flash("Cookies видалено", category=("danger"))
    response = make_response(redirect(url_for('info')))
    cookies = request.cookies

    for key in cookies.keys():
        if key != 'session':
            response.delete_cookie(key)

    return response

@app.route('/change-password', methods=["POST"])
@login_required
def change_password():
    form = ChangePasswordForm()

    if form.validate_on_submit():
        if current_user.verify_password(form.old_password.data):
            try:
                current_user.password = form.new_password.data
                db.session.commit()
                logout_user()
                flash("Password changed!", category="success")
                return redirect(url_for("login"))
            except:
                db.session.rollback()
                flash("Failed!", category="danger")
        else:
            flash("Wrong data! Try again!", category="danger")
        return redirect(url_for("account"))
    
    flash("Validation error!", category="danger")
    return render_template('account.html', password_form=form, info_form=UpdateAccountForm())

@app.route("/todo")
def todo():
    todo_form = CreateTodo()
    todo_list = db.session.query(Todo).all()

    return render_template('todo.html', todo_form=todo_form, todo_list=todo_list)

@app.route("/create_todo", methods=['POST'])
def create_todo():
    todo_form = CreateTodo()

    if todo_form.validate_on_submit():
        new_task = todo_form.new_task.data
        description = todo_form.description.data
        new_todo = Todo(title=new_task, description=description, complete=False)
        db.session.add(new_todo)
        db.session.commit()
        flash("Створення виконано", category=("success"))
        return redirect(url_for("todo"))
    
    flash("Помилка при створенні", category=("danger"))
    return redirect(url_for("todo"))

@app.route("/read_todo/<int:todo_id>")
def read_todo(todo_id=None):
    todo = Todo.query.get_or_404(todo_id)
    return redirect(url_for("todo"))

@app.route("/update_todo/<int:todo_id>")
def update_todo(todo_id=None):
    todo = Todo.query.get_or_404(todo_id)

    todo.complete = not todo.complete
    db.session.commit()
    flash("Оновлення виконано", category=("success"))
    return redirect(url_for("todo"))

@app.route("/delete_todo/<int:todo_id>")
def delete_todo(todo_id=None):
    todo = Todo.query.get_or_404(todo_id)

    db.session.delete(todo)
    db.session.commit()
    flash("Видалення виконано", category=("success"))
    return redirect(url_for("todo"))


@app.route("/main")
def main():
    return redirect(url_for("home"))