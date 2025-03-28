from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from db.db import Base


class Birthday(Base):
    __tablename__ = "birthdays"

    user_id: Mapped[int] = mapped_column(primary_key=True)
    full_name: Mapped[str]
    birth_date: Mapped[str]

    user = relationship("User", back_populates="birthdays")

    def __repr__(self):
        return f"User(id={self.user_id}, full_name={self.full_name}, date={self.birth_date})"