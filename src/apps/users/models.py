from config.db import Base
from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTableUUID
from sqlalchemy.orm import relationship, Mapped


class UserModel(SQLAlchemyBaseUserTableUUID, Base):
    __tablename__ = "users"
    tasks: Mapped[list['TaskModel']] = relationship("TaskModel", back_populates="owner")
