# -*- coding: UTF-8 -*-
"""
  Author:  Jacek 'Szumak' Kotlarski --<szumak@virthost.pl>
  Created: 11.12.2023

  Purpose: database classes
"""

from inspect import currentframe
from typing import Optional

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.engine import Engine
from sqlalchemy.orm.session import Session
from sqlalchemy.dialects.sqlite import INTEGER, TEXT

from jsktoolbox.basetool.data import BData
from jsktoolbox.attribtool import ReadOnlyClass
from jsktoolbox.raisetool import Raise


class _Keys(object, metaclass=ReadOnlyClass):
    """Local keys."""

    DB_PATH: str = "_db_path_"
    DEBUG: str = "_debug_"
    DBH: str = "_db_handler_"


class LocalBase(DeclarativeBase):
    """DeclarativeBase local class."""


# db models
class TWorkTime(LocalBase):
    """WorkTime table."""

    __tablename__: str = "worktime"

    id: Mapped[int] = mapped_column(
        INTEGER, primary_key=True, nullable=False, autoincrement=True
    )
    start: Mapped[int] = mapped_column(INTEGER, nullable=False)
    duration: Mapped[int] = mapped_column(INTEGER, nullable=False)
    notes: Mapped[str] = mapped_column(TEXT, default="")

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(id='{self.id}', start='{self.start}', duration='{self.duration}', notes='{self.notes}')"


class Database(BData):
    """Database class engine for local data."""

    def __init__(self, path: str, debug: bool = False) -> None:
        """Constructor."""
        self._set_data(key=_Keys.DB_PATH, value=path, set_default_type=str)
        self._set_data(key=_Keys.DEBUG, value=debug, set_default_type=bool)
        self._set_data(key=_Keys.DBH, value=None, set_default_type=Optional[Engine])

        # create engine
        if self.__create_engine():
            base = LocalBase()
            base.metadata.create_all(self._get_data(key=_Keys.DBH))  # type: ignore

    def __create_engine(self) -> bool:
        """Create Engine for sqlite database."""
        engine: Optional[Engine] = None
        try:
            engine = create_engine(
                f"sqlite:///{self._get_data(key=_Keys.DB_PATH)}",
                echo=self._get_data(key=_Keys.DEBUG),
            )
        except Exception as ex:
            raise Raise.error(f"{ex}", OSError, self._c_name, currentframe())
        if engine is not None:
            self._set_data(key=_Keys.DBH, value=engine)
            return True
        return False

    @property
    def session(self) -> Optional[Session]:
        """Create Session from Database Engine."""
        session = None
        if self._get_data(key=_Keys.DBH) is None:
            return None
        try:
            session = Session(bind=self._get_data(key=_Keys.DBH))
        except Exception as ex:
            raise Raise.error(f"{ex}", OSError, self._c_name, currentframe())
        return session


# #[EOF]#######################################################################
