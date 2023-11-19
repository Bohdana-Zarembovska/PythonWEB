from app import app
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
from sqlalchemy import Integer, String, Boolean, Date, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from app import db, bcrypt, login_manager
from flask_login import UserMixin
from datetime import datetime
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL", "sqlite:///flaskdb.db")



class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    description = db.Column(db.String(200))
    complete = db.Column(db.Boolean)

with app.app_context():
    db.create_all()

@login_manager.user_loader
def user_loader(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    image: Mapped[str] = mapped_column(String(20), nullable=False, default='image.png')
    password_hash: Mapped[str] = mapped_column(String(60), nullable=False)
    last_seen: Mapped[datetime] = mapped_column(DateTime, nullable=True, default=datetime.now())
    about_me: Mapped[str] = mapped_column(String, nullable=True)
    
    def __init__(self, name, email, password):
        self.username = name
        self.email = email
        self.password = password

    @property
    def password(self):
        return AttributeError("Password is not readable!")

    @password.setter
    def password(self, value):
        self.password_hash = bcrypt.generate_password_hash(value)

    def verify_password(self, value):
        return bcrypt.check_password_hash(self.password_hash, value)
    
    def __repr__(self) -> str:
        return f"User({self.username}, {self.email})"
    
migrate = Migrate(app, db)