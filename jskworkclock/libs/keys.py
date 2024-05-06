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

    BT_START: str = "__bt_start__"
    BT_STOP: str = "__bt_stop__"
    BT_SWITCH: str = "__bt_switch__"
    CACHE_DIR: str = "__cache__"
    DATABASE: str = "__database__"
    DBH: str = "_DBH_"
    DEF_NAME: str = "__def_name__"
    DIALOG_RETURN: str = "__dialog_return__"
    D_CALENDAR: str = "__dialog_calendar__"
    D_DATA: str = "__dialog_return_data__"
    D_FRAME: str = "__dialog_data_frame__"
    D_HOUR: str = "__dialog_hour__"
    D_MINUTE: str = "__dialog_minute__"
    D_NOTES: str = "__dialog_notes__"
    D_RADIO: str = "__dialog_radio_buttons__"
    D_REPORT: str = "__report_tree__"
    F_STOP: str = "__stop__"
    STATE: str = "state"
    SWITCH_FLAG: str = "__switch_flag__"
    TEXT: str = "__text__"
    TH_CLOCK: str = "__th_clock__"
    W_CLOSED: str = "__wm_closed__"
    W_REPORT: str = "__report_window__"


# #[EOF]#######################################################################
