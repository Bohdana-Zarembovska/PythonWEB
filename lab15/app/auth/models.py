from sqlalchemy import Integer, String, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from flask_login import UserMixin
from datetime import datetime
from ..extensions import db, bcrypt, login_manager

@login_manager.user_loader
def user_loader(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    image_file: Mapped[str] = mapped_column(String(20), nullable=False, default='default.png')
    password_hash: Mapped[str] = mapped_column(String(60), nullable=False)
    last_seen: Mapped[datetime] = mapped_column(DateTime, nullable=True, default=datetime.now())
    about_me: Mapped[str] = mapped_column(String, nullable=True)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password


    @property
    def password(self):
        return AttributeError("Password is not readable!!")

    @password.setter
    def password(self, value):
        self.password_hash = bcrypt.generate_password_hash(value)

    def verify_password(self, value):
        return bcrypt.check_password_hash(self.password_hash, value)
    
    def __repr__(self) -> str:
        return f"User({self.username}, {self.email})"