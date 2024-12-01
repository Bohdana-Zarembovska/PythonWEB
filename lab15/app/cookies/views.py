from flask import render_template, request, redirect, url_for, make_response, flash
from flask_login import login_required
from datetime import datetime
from . import cookies_bp


@cookies_bp.route('/')
@login_required
def info_page():
    return render_template('cookies/info.html', cookies=request.cookies)

@cookies_bp.route('/', methods=["POST"])
@login_required
def add():
    key = request.form.get("key")
    value = request.form.get("value")
    exp_date = request.form.get("date")

    if key and value and exp_date:
        response = make_response(redirect(url_for("cookies.info_page")))
        response.set_cookie(key, value, expires=datetime.strptime(exp_date, "%Y-%m-%dT%H:%M"))
        flash(f"Success! {key} : {value} was added.", category="success")
        return response

    flash("Failed!", category="danger")
    return redirect(url_for("cookies.info_page"))

@cookies_bp.route('/delete', methods=["POST"])
@cookies_bp.route('/delete/<key>', methods=["POST"])
@login_required
def delete(key = None):
    response = make_response(redirect(url_for("cookies.info_page")))

    if key:
        response.delete_cookie(key)
        flash(f"Success! Cookie: {key} was deleted.", category="success")
    else:
        for key in request.cookies.keys():
            response.delete_cookie(key)
    
    return response