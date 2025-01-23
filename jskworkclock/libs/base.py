# -*- coding: UTF-8 -*-
"""
  Author:  Jacek 'Szumak' Kotlarski --<szumak@virthost.pl>
  Created: 10.12.2023

  Purpose: Sets of base classes.
"""


from jsktoolbox.basetool.data import BData

from libs.keys import Keys
from libs.database import Database


class BDbHandler(BData):
    """BDbHandler base class."""

    @property
    def _db_handler(self) -> Database:
        """The _db_handler property."""
        return self._get_data(key=Keys.DBH)  # type: ignore

    @_db_handler.setter
    def _db_handler(self, value: Database) -> None:
        """The _db_handler setter."""
        self._set_data(key=Keys.DBH, value=value, set_default_type=Database)


# #[EOF]#######################################################################
