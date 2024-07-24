import uuid

from config.db import Base
from sqlalchemy import Column, ForeignKey, String, Uuid
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, relationship


class DigestEntityProperties(Base):
    __tablename__ = "digest_entity_properties"
    uid = Column(Uuid, default=uuid.uuid4, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    type = Column(String, nullable=False)
    rules = Column(JSONB, nullable=False)


class EntityProperties(Base):
    __tablename__ = "entity_properties"
    __allow_unmapped__ = True
    uid = Column(Uuid, default=uuid.uuid4, primary_key=True)
    entity_uid = Column(Uuid, ForeignKey("entity.uid"))

    property_uid = Column(Uuid, ForeignKey("digest_entity_properties.uid"))
    property: DigestEntityProperties = relationship("DigestEntityProperties")


class Entity(Base):
    __tablename__ = "entity"
    __allow_unmapped__ = True
    uid = Column(Uuid, default=uuid.uuid4, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    properties: Mapped[list[EntityProperties]] = relationship("EntityProperties")
