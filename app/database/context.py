"""MySQL Module."""

import sqlalchemy
import sqlalchemy.orm as orm

from typing import Optional

from common.singleton import Singleton
from common.settings import DatabaseSettings
from database.declarative import create_table


class SQLiteContext(Singleton):
    """SQLite Context Class with Singleton Pattern."""

    session = None

    def __init__(self, database_settings: Optional[DatabaseSettings] = None):
        """Create a new session."""

        if self.session is not None:
            return

        if database_settings is None:
            database_settings = DatabaseSettings()

        self.engine = sqlalchemy.create_engine(
            f'sqlite:///{database_settings.DB_ENDPOINT}',
            pool_recycle=3600,
            echo=True
        )
        create_table(self.engine)
        self.session = orm.sessionmaker(bind=self.engine)
        self.cursor: Optional[orm.session.Session] = None
        self.is_commit = False

    def _commit(self, is_exc=False):
        if self.cursor is None:
            raise Exception("Session is None.")
        try:
            if is_exc:
                self.cursor.rollback()
            else:
                self.cursor.commit()
        except BaseException as e:
            self.cursor.rollback()
            raise e
        finally:
            self.cursor.close()
            self.is_commit = True

    def __enter__(self) -> orm.session.Session:
        return self.begin()

    def __exit__(self, exc_type, exc_value, traceback):
        if self.cursor is None:
            raise Exception("Session is None.")
        if self.is_commit:
            return
        self._commit(exc_type is not None)

    def commit(self):
        self._commit()

    def begin(self) -> orm.session.Session:
        """Get session."""

        if self.session is None:
            raise Exception("Session is None.")
        self.is_commit = False
        self.cursor = self.session()
        return self.cursor

    def dispose(self):

        if self.engine is None:
            return
        self.engine.dispose()
        self.engine = None
        self.session = None
