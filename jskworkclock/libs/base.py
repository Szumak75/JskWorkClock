# -*- coding: UTF-8 -*-
"""
  Author:  Jacek 'Szumak' Kotlarski --<szumak@virthost.pl>
  Created: 10.12.2023

  Purpose: Sets of base classes.
"""

from inspect import currentframe

from jsktoolbox.basetool.data import BData
from jsktoolbox.raisetool import Raise

from libs.keys import Keys
from libs.database import Database


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
                TypeError,
                self._c_name,
                currentframe(),
            )
        self._data[Keys.DBH] = value


# #[EOF]#######################################################################
