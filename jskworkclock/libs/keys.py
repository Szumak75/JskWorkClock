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
    DCALENDAR = "__dialog_calendar__"
    DDATA = "__dialog_return_data__"
    DEFNAME = "__dname__"
    DFRAME = "__dialog_data_frame__"
    DHOUR = "__dialog_hour__"
    DIALOG_RETURN = "__dialog_return__"
    DMINUTE = "__dialog_minute__"
    DNOTES = "__dialog_notes__"
    DRADIO = "__dialog_radio_buttons__"
    FSTOP = "__stop__"
    STATE = "state"
    TEXT = "__text__"
    THCLOCK = "__thclock__"
    WCLOSED = "__wm_closed__"
    WREPORT = "__report_window__"


# #[EOF]#######################################################################
