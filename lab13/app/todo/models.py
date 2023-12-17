from sqlalchemy import Integer, String, Boolean, Date
from sqlalchemy.orm import Mapped, mapped_column
from datetime import date
from ..extensions import db

class Todo(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(100))
    due_date: Mapped[date] = mapped_column(Date, nullable=True) 
    complete: Mapped[bool] = mapped_column(Boolean)
    
    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "due_date": str(self.due_date) if self.due_date else None,
            "complete": self.complete
        }
