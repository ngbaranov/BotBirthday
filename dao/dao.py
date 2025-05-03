from datetime import date

from sqlalchemy import func, case, select

from dao.base import BaseDAO
from models import Birthday


class BirthdayDAO(BaseDAO[Birthday]):
    model = Birthday

    async def get_sorted_by_user_id(self, user_id: int):
        today_mmdd = date.today().strftime("%m-%d")

        # Используем CASE для сортировки от сегодняшней даты
        today_sort_expr = case(
            (
                func.to_char(Birthday.birth_date, 'MM-DD') < today_mmdd, 1
            ),
            else_=0
        )

        stmt = (
            select(Birthday)
            .where(Birthday.user_id == user_id)
            .order_by(today_sort_expr, func.to_char(Birthday.birth_date, 'MM-DD'))
        )
        result = await self._session.execute(stmt)
        return result.scalars().all()