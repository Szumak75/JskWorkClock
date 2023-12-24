# -*- coding: UTF-8 -*-
"""
  Author:  Jacek 'Szumak' Kotlarski --<szumak@virthost.pl>
  Created: 11.12.2023

  Purpose:
"""

from inspect import currentframe
from typing import Optional

from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    String,
    create_engine,
    Text,
)
from sqlalchemy.schema import SchemaConst
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.engine import Engine
from sqlalchemy.orm.session import Session
from sqlalchemy.dialects.sqlite import INTEGER, TEXT

from jsktoolbox.libs.base_data import BData
from jsktoolbox.attribtool import ReadOnlyClass
from jsktoolbox.raisetool import Raise


class _Keys(object, metaclass=ReadOnlyClass):
    """Local keys."""

    DBPATH = "_db_path_"
    DEBUG = "_debug_"
    DBH = "_db_handler_"


class LocalBase(DeclarativeBase):
    """DeclarativeBase local class."""


# db models
class TWorkTime(LocalBase):
    """Worktime table."""

    __tablename__: str = "worktime"

    id: Mapped[int] = mapped_column(
        INTEGER, primary_key=True, nullable=False, autoincrement=True
    )
    start: Mapped[int] = mapped_column(INTEGER, nullable=False)
    duration: Mapped[int] = mapped_column(INTEGER, nullable=False)
    notes: Mapped[str] = mapped_column(TEXT, default="")


class Database(BData):
    """Database class engine for local data."""

    def __init__(self, path: str, debug: bool = False) -> None:
        """Constructor."""
        self._data[_Keys.DBPATH] = path
        self._data[_Keys.DEBUG] = debug
        self._data[_Keys.DBH] = None

        # create engine
        if self.__create_engine():
            base = LocalBase()
            base.metadata.create_all(self._data[_Keys.DBH])

    def __create_engine(self) -> bool:
        """Create Engine for sqlite database."""
        engine: Optional[Engine] = None
        try:
            engine = create_engine(
                f"sqlite:///{self._data[_Keys.DBPATH]}",
                echo=self._data[_Keys.DEBUG],
            )
        except Exception as ex:
            raise Raise.error(f"{ex}", OSError, self._c_name, currentframe())  # type: ignore
        if engine is not None:
            self._data[_Keys.DBH] = engine
            return True
        return False

    @property
    def session(self) -> Optional[Session]:
        """Create Session from Database Engine."""
        session = None
        if self._data[_Keys.DBH] is None:
            return None
        try:
            session = Session(bind=self._data[_Keys.DBH])
        except Exception as ex:
            raise Raise.error(f"{ex}", OSError, self._c_name, currentframe())  # type: ignore
        return session


# #[EOF]#######################################################################
