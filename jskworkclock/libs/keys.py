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

    BTSTART: str = "__btstart__"
    BTSTOP: str = "__btstop__"
    CACHEDIR: str = "__cache__"
    DATABASE: str = "__dbase__"
    DBH: str = "_DBH_"
    DCALENDAR: str = "__dialog_calendar__"
    DDATA: str = "__dialog_return_data__"
    DEFNAME: str = "__dname__"
    DFRAME: str = "__dialog_data_frame__"
    DHOUR: str = "__dialog_hour__"
    DIALOG_RETURN: str = "__dialog_return__"
    DMINUTE: str = "__dialog_minute__"
    DNOTES: str = "__dialog_notes__"
    DRADIO: str = "__dialog_radio_buttons__"
    DREPORT: str = "__report_tree__"
    FSTOP: str = "__stop__"
    STATE: str = "state"
    TEXT: str = "__text__"
    THCLOCK: str = "__thclock__"
    WCLOSED: str = "__wm_closed__"
    WREPORT: str = "__report_window__"


# #[EOF]#######################################################################
