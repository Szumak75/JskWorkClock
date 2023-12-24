# -*- coding: utf-8 -*-
"""
  report.py
  Author : Jacek 'Szumak' Kotlarski --<szumak@virthost.pl>
  Created: 22.12.2023, 15:18:32
  
  Purpose: 
"""

import os
import tkinter as tk

from tkinter import ttk
from time import sleep
from typing import Optional
from PIL import Image, ImageDraw
from time import sleep
from threading import Thread
from inspect import currentframe
from datetime import timedelta

from jsktoolbox.libs.base_data import BData
from jsktoolbox.datetool import DateTime, Timestamp
from jsktoolbox.attribtool import ReadOnlyClass
from jsktoolbox.libs.system import PathChecker, Env
from jsktoolbox.raisetool import Raise
from pytest import Session

from libs.base import TkBase, TtkBase
from libs.ico import ImageBase64
from libs.database import Database, TWorkTime
from libs.keys import Keys
from libs.base import BDbHandler


class ReportDialog(TtkBase, BDbHandler, tk.Toplevel):
    """Modal Dailog box."""

    def __init__(self, parent: tk.Tk, dbh: Database, *args) -> None:
        """Constructor."""
        tk.Toplevel.__init__(self, parent, *args)
        self.title(f"{parent.title()}: Reports")

        # init locals
        self._data[Keys.WCLOSED] = False
        self._db_handler = dbh

        self.__init_ui()

    def __init_ui(self) -> None:
        """Create user interface."""
        self.geometry("400x600")

        ico = tk.PhotoImage(data=ImageBase64.ICO)
        self.wm_iconphoto(False, ico)
        self.columnconfigure(0, weight=1)

        self.protocol("WM_DELETE_WINDOW", self.__on_closing)

    def __on_closing(self) -> None:
        self._data[Keys.WCLOSED] = True
        self.destroy()

    @property
    def is_closed(self) -> bool:
        """The is_closed property."""
        return self._data[Keys.WCLOSED]


# #[EOF]#######################################################################
