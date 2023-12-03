from flask import render_template, request
from datetime import datetime
import os
from . import resume_bp

skills = ["Data Science/Machine Learning", "Pandas/NumPy/SciPy/Matplotlib", "MySQL", "HTML & CSS", "Jupyter Notebook", "Python", "OpenCV", "Deep Learning"]

@resume_bp.route('/')
@resume_bp.route('/about')
def about_page():
    return render_template('resume/home.html', os=os.name, user_agent=request.headers.get('User-Agent'), time=datetime.now())

@resume_bp.route('/skills')
@resume_bp.route('/skills/<int:id>')
def skills_page(id=None):
    if id is not None and id < len(skills):
        return render_template('resume/skill.html', skill=skills[id])
    else:
        return render_template('resume/skills.html', skills=skills)

@resume_bp.route('/hobbies')
def hobbies_page():
    return render_template('resume/hobbies.html')

@resume_bp.route('/education')
def education_page():
    return render_template('resume/education.html')