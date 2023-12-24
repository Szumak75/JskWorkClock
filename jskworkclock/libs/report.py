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
        # main window
        self.geometry("600x600")

        ico = tk.PhotoImage(data=ImageBase64.ICO)
        self.wm_iconphoto(False, ico)
        self.columnconfigure(0, weight=1)

        self.protocol("WM_DELETE_WINDOW", self.__on_closing)

        # content
        main_frame = tk.Frame(self, borderwidth=2, relief=tk.RAISED)
        main_frame.pack(expand=True, fill=tk.BOTH)
        sub_frame = tk.Frame(main_frame, borderwidth=2, relief=tk.SUNKEN)
        sub_frame.place(relx=2, rely=2, anchor=tk.CENTER)
        sub_frame.pack(expand=True, fill=tk.BOTH)

        # Button Frame
        bt_frame = tk.Frame(
            sub_frame, background="red", borderwidth=4, relief=tk.SUNKEN
        )
        bt_frame.place(anchor=tk.CENTER, relx=4, rely=4, height=20)
        bt_frame.pack(expand=True)
        # Data Frame

    def __on_closing(self) -> None:
        self._data[Keys.WCLOSED] = True
        self.destroy()

    @property
    def is_closed(self) -> bool:
        """The is_closed property."""
        return self._data[Keys.WCLOSED]


# #[EOF]#######################################################################
