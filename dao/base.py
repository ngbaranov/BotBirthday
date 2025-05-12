from typing import TypeVar, Generic, Type

from aiogram.handlers import message
from pydantic import BaseModel
from sqlalchemy import select, update, delete
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from loguru import logger

from db.db import Base

T = TypeVar("T", bound=Base)


class BaseDAO(Generic[T]):
    model: Type[T] = None

    def __init__(self, session: AsyncSession):
        self._session = session
        if self.model is None:
            raise ValueError("Модель должна быть указана в дочернем классе")


    async def add (self, values: BaseModel):
            values_dict = values.model_dump(exclude_unset=True)
            logger.info(f"Добавление записи {self.model.__name__} с параметрами: {values_dict}")
            try:
                new_instance = self.model(**values_dict)
                self._session.add(new_instance)
                logger.info(f"Запись {self.model.__name__} успешно добавлена.")
                await self._session.commit()
                return new_instance
            except SQLAlchemyError as e:
                logger.error(f"Ошибка при добавлении записи: {e}")
                raise

    async def get_select_by_id(self, user_id: int):
        try:
            result = await self._session.execute(
                select(self.model).where(self.model.user_id == user_id)
            )
            return result.scalars().all()
        except SQLAlchemyError as e:
            logger.error(f"Ошибка при получении записи: {e}")
            raise


    async def get_select_by_fields(self, **kwargs):
        try:
            result = await self._session.execute(
                select(self.model).filter_by(**kwargs)
            )
            return result.scalars().all()
        except SQLAlchemyError as e:
            logger.error(f"Ошибка при получении записи: {e}")
            raise

    async def update_fields(self, entry_id: int, **kwargs):
        try:
            await self._session.execute(
                update(self.model)
                .where(self.model.id == entry_id)
                .values(**kwargs)
            )
            await self._session.commit()
        except SQLAlchemyError as e:
            logger.error(f"Ошибка при обновлении: {e}")
            raise

    async def delete(self, entry_id: int):
        try:
            await self._session.execute(
                delete(self.model).where(self.model.id == entry_id)
            )
            await self._session.commit()
        except SQLAlchemyError as e:
            logger.error(f"Ошибка при удалении: {e}")
            raise