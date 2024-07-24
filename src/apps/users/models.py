from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTableUUID

from config.db import Base


class User(SQLAlchemyBaseUserTableUUID, Base):
    pass
