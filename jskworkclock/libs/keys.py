# -*- coding: utf-8 -*-
"""
  keys.py
  Author : Jacek 'Szumak' Kotlarski --<szumak@virthost.pl>
  Created: 22.12.2023, 01:23:01
  
  Purpose: Keys container class.
"""

from jsktoolbox.attribtool import ReadOnlyClass


class Keys(object, metaclass=ReadOnlyClass):
    """Keys container class."""

    BTSTART = "__btstart__"
    BTSTOP = "__btstop__"
    CACHEDIR = "__cache__"
    DATABASE = "__dbase__"
    DBH = "_DBH_"
    DEFNAME = "__dname__"
    DIALOG_RETURN = "__dialog_return__"
    DNOTES = "__dialog_notes__"
    FSTOP = "__stop__"
    STATE = "state"
    THCLOCK = "__thclock__"
    WREPORT = "__report_window__"
    WCLOSED = "__wm_closed__"


# #[EOF]#######################################################################
