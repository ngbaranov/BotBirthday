from datetime import date
from sqlalchemy import Date
from sqlalchemy.orm import Mapped, mapped_column, relationship
from db.db import Base


class Birthday(Base):
    __tablename__ = "birthdays"

    user_id: Mapped[int] = mapped_column(primary_key=True)
    full_name: Mapped[str]
    birth_date: Mapped[date] = mapped_column(Date)



    def __repr__(self):
        return f"User(id={self.user_id}, full_name={self.full_name}, date={self.birth_date})"