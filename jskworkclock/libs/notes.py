# -*- coding: utf-8 -*-
"""
  notes.py
  Author : Jacek 'Szumak' Kotlarski --<szumak@virthost.pl>
  Created: 22.12.2023, 01:22:15
  
  Purpose: Notes dialog class.
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


class NotesDialog(BData, TtkBase, tk.Toplevel):
    """Modal Dailog box."""

    def __init__(self, parent, *args) -> None:
        """Constructor."""
        tk.Toplevel.__init__(self, parent, *args)
        self.title(f"{parent.title()}: Notes")

        # init locals
        self._data[Keys.DIALOG_RETURN] = None

        self.__init_ui()

    def __init_ui(self) -> None:
        """Create user interface."""
        self.geometry("400x200")

        ico = tk.PhotoImage(data=ImageBase64.ICO)
        self.wm_iconphoto(False, ico)
        self.columnconfigure(0, weight=1)
        # add frame
        frame = ttk.Frame(self)
        frame.grid(column=0, row=0, padx=5, pady=5, sticky=tk.NSEW)
        frame.columnconfigure(0, weight=4)
        frame.columnconfigure(1, weight=1)
        frame.columnconfigure(2, weight=1)
        # add entry
        notes = tk.Text(frame, height=8)
        notes.grid(column=0, row=0, columnspan=3, sticky=tk.EW)
        self._data[Keys.DNOTES] = notes
        # add button frame
        bt_frame = ttk.Frame(frame)
        bt_frame.grid(column=0, row=1, columnspan=3, sticky=tk.E, padx=1, pady=1)
        bt_frame.columnconfigure(0)
        bt_frame.columnconfigure(1)
        # add ok buton
        ok_button = ttk.Button(bt_frame, text="Ok", command=self.__bt_ok)
        ok_button.grid(column=0, row=0, sticky=tk.E)
        # add close button
        close_button = ttk.Button(bt_frame, text="Close", command=self.__bt_close)
        close_button.grid(column=1, row=0, sticky=tk.E)

        # modal?
        # self.root.wait_visibility()
        self.grab_set()
        # self.root.transient(parent)

    def __bt_ok(self) -> None:
        """Button OK handler."""
        self._data[Keys.DIALOG_RETURN] = True
        self.withdraw()

    def __bt_close(self) -> None:
        """Button CLOSE handler."""
        self._data[Keys.DIALOG_RETURN] = False
        self.withdraw()

    @property
    def dialog_return(self) -> Optional[bool]:
        """Returns notes dialog decision."""
        return self._data[Keys.DIALOG_RETURN]

    @property
    def get_notes(self) -> str:
        """Returns notes text."""
        notes: tk.Text = self._data[Keys.DNOTES]
        text: str = notes.get(1.0, tk.END)
        return text


# #[EOF]#######################################################################
