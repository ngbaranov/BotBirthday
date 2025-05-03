from pydantic import BaseModel
from datetime import date


class BirthdayCreate(BaseModel):
    user_id: int
    full_name: str
    birth_date: date

class BirthdayOut(BaseModel):
    full_name: str
    birth_date: date
