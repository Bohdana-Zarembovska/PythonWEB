import json
from functools import wraps
from hashlib import sha256
from flask import session, redirect, url_for

"""
The password is encrypted by sha256 algorithm
"""


class UserInputException(Exception):
    def __init__(self, message):
        super().__init__(message)


class AuthService:
    def __init__(self):
        self.json_path = "app/static/json/credentials.json"
        with open(self.json_path) as json_file:
            self.credentials = json.load(json_file)

        self._SESSION_KEY = "user_login"

    def authenticate(self, login: str, password: str) -> bool:
        password = sha256(password.encode()).hexdigest()

        if login == self.credentials["login"] and password == self.credentials["password"]:
            return True
        return False

    def set_session_value(self, value: str) -> None:
        session[self._SESSION_KEY] = value

    def is_pre_authorized(self):
        if session and session[self._SESSION_KEY] == self.credentials["login"]:
            return True
        return False

    def get_session_key(self):
        return session[self._SESSION_KEY]

    def get_pre_login_decorator(self):
        def login_required(f):
            @wraps(f)
            def decorated_function(*args, **kwargs):
                if not self.is_pre_authorized():
                    return redirect(url_for('login_page'))
                return f(*args, **kwargs)

            return decorated_function

        return login_required

    def change_pass(self, old_pass: str, new_pass: str, repeat_pass: str) -> None:
        if sha256(old_pass.encode()).hexdigest() != self.credentials["password"]:
            raise UserInputException("Wrong password!!!")
        if new_pass != repeat_pass:
            raise UserInputException("New password and repeated password are not same!!!")
        if len(new_pass) < 4:
            raise UserInputException("Password must be at least 4 characters long")

        new_pass = sha256(new_pass.encode()).hexdigest()
        self.credentials["password"] = new_pass

        json_cred = json.dumps(self.credentials, indent=2)

        with open(self.json_path, "w") as f:
            f.write(json_cred)


def get_session_dict() -> dict:
    return dict(session)