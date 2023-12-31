# -*- coding: UTF-8 -*-
"""
  Author:  Jacek 'Szumak' Kotlarski --<szumak@virthost.pl>
  Created: 10.12.2023

  Purpose: Sets of base classess.
"""

from inspect import currentframe

from jsktoolbox.libs.base_data import BClasses, BData
from jsktoolbox.raisetool import Raise

from libs.keys import Keys
from libs.database import Database


class TkBase(BClasses):
    """Base class for classess derived from Tk."""

    _tkloaded = None
    _windowingsystem_cached = None
    child = None
    children = None
    master = None
    tk = None


class TtkBase(BClasses):
    """Base class for classess derived from Ttk."""

    _name = None
    _w = None
    children = None
    master = None
    tk = None
    widgetName = None


class BDbHandler(BData):
    """BDbHandler base class."""

    @property
    def _db_handler(self) -> Database:
        """The _db_handler property."""
        if Keys.DBH not in self._data:
            self._data[Keys.DBH] = None
        return self._data[Keys.DBH]

    @_db_handler.setter
    def _db_handler(self, value: Database) -> None:
        if not isinstance(value, Database):
            raise Raise.error(
                f"Expected Database type, received '{type(value)}'.",
                TypeError,  # type: ignore
                self._c_name,
                currentframe(),
            )
        self._data[Keys.DBH] = value


# #[EOF]#######################################################################
