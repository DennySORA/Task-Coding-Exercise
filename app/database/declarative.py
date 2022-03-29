"""Declarative Module"""

import os

from sqlalchemy import Column, String, Integer, DateTime, inspect
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base

from common.settings import DatabaseSettings

Base = declarative_base()


class TaskDeclarative(Base):
    __tablename__ = 'task'

    id = Column('id', Integer, primary_key=True)
    name = Column('name', String(64))
    status = Column('status', Integer)

    create_time = Column('create_time', DateTime, server_default=func.now())
    update_time = Column('update_time', DateTime, onupdate=func.now())


def create_table(engine):
    if not os.path.isfile(DatabaseSettings().DB_ENDPOINT) or not inspect(engine).has_table('task'):
        Base.metadata.create_all(engine)


def drop_all_table(engine):
    Base.metadata.drop_all(engine)
