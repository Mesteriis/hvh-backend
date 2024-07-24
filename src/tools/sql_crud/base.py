from sqlalchemy.orm import DeclarativeBase


class BaseCRUD(DeclarativeBase):
    __abstract__ = True

    def create(self, session, **kwargs):
        instance = self(**kwargs)
        session.add(instance)
        session.commit()
        session.refresh(instance)
        return instance

    def read(self, session, uid):
        return session.query(self).get(uid)

    def update(self, session, uid, **kwargs):
        instance = session.query(self).get(uid)
        for key, value in kwargs.items():
            setattr(instance, key, value)
        session.commit()
        session.refresh(instance)
        return instance

    def delete(self, session, uid):
        instance = session.query(self).get(uid)
        session.delete(instance)
        session.commit()
        return instance

    def list(self, session):
        return session.query(self).all()

    def filter(self, session, **kwargs):
        return session.query(self).filter_by(**kwargs).all()
