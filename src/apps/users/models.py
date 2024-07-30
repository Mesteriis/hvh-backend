from config.db import Base
from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTableUUID
from sqlalchemy.orm import relationship


class User(SQLAlchemyBaseUserTableUUID, Base):
    __tablename__ = "users"
    tasks = relationship("Tasks", back_populates="owner")
