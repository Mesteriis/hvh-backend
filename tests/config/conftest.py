from datetime import datetime

import pytest
from sqlalchemy import DateTime, String, Integer, Boolean
from sqlalchemy.orm import mapped_column, Mapped

from core.config.db import BaseModel, Base
from tests.conftest import engine


@pytest.fixture(scope="function")
async def model_for_test():
    class TestModel(BaseModel):
        __tablename__ = "test_model"
        string: Mapped[str] = mapped_column(String(50), nullable=True)
        integer: Mapped[int] = mapped_column(Integer, nullable=True)
        datetime: Mapped[datetime] = mapped_column(DateTime, nullable=True)
        bool: Mapped[bool] = mapped_column(Boolean, nullable=True)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all, tables=[TestModel.__table__])

    yield TestModel

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all, tables=[TestModel.__table__])
