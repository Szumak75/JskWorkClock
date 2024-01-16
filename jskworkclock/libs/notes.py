# -*- coding: utf-8 -*-
"""
  notes.py
  Author : Jacek 'Szumak' Kotlarski --<szumak@virthost.pl>
  Created: 22.12.2023, 01:22:15
  
  Purpose: Notes dialog class.
"""

import os
import tkinter as tk

from tkinter import Scrollbar, ttk
from tkinter.scrolledtext import ScrolledText
from time import sleep
from turtle import width
from typing import Optional
from PIL import Image, ImageDraw
from time import sleep
from threading import Thread
from inspect import currentframe
from datetime import timedelta
from click import command

from jsktoolbox.libs.base_data import BData
from jsktoolbox.datetool import DateTime, Timestamp
from jsktoolbox.attribtool import ReadOnlyClass
from jsktoolbox.libs.system import PathChecker, Env
from jsktoolbox.raisetool import Raise
from jsktoolbox.tktool.base import TkBase


from libs.ico import ImageBase64
from libs.database import Database, TWorkTime
from libs.keys import Keys
from jsktoolbox.tktool.layout import Pack


class NotesDialog(BData, TkBase, tk.Toplevel):
    """Modal Dailog box."""

    def __init__(self, master, **args) -> None:
        """Constructor."""
        # tk.Toplevel.__init__(self, parent, *args)
        super().__init__(master, **args)
        self.title(f"{master.title()}: Notes")
        self.minsize(600, 400)

        # bind events
        self.protocol("WM_DELETE_WINDOW", self.__bt_close)

        # init locals
        self._data[Keys.DIALOG_RETURN] = None
        self._data[Keys.TEXT] = ""

        self.__init_ui()

        # modal?
        # self.root.wait_visibility()
        self.grab_set()
        # self.root.transient(parent)

    def __init_ui(self) -> None:
        """Create user interface."""
        self.geometry("500x400")
        self.resizable(True, True)

        ico = tk.PhotoImage(data=ImageBase64.ICO)
        self.wm_iconphoto(False, ico)

        # Sizegrip
        sizegrip = ttk.Sizegrip(self)
        sizegrip.pack(side=Pack.Side.BOTTOM, anchor=Pack.Anchor.E)

        # add frame
        notes_frame = ttk.Frame(self)
        notes_frame.pack(
            side=Pack.Side.TOP, fill=Pack.Fill.BOTH, padx=5, pady=5, expand=True
        )
        # add entry
        notes = ScrolledText(notes_frame, width=50, height=10)
        self._data[Keys.DNOTES] = notes
        notes.pack(side=Pack.Side.LEFT, fill=Pack.Fill.BOTH, expand=True)

        # separator
        sep = ttk.Separator(self, orient=tk.HORIZONTAL)
        sep.pack(fill=Pack.Fill.X)

        # add button frame
        bt_frame = ttk.Frame(self)
        bt_frame.pack(side=Pack.Side.TOP, fill=Pack.Fill.X, padx=5, pady=5)
        # add close button
        close_button = ttk.Button(bt_frame, text="Close", command=self.__bt_close)
        close_button.pack(side=Pack.Side.RIGHT, padx=2)
        # add ok buton
        ok_button = ttk.Button(bt_frame, text="Ok", command=self.__bt_ok)
        ok_button.pack(side=Pack.Side.RIGHT, padx=2)
        self.update()

    def __bt_ok(self) -> None:
        """Button OK handler."""
        self._data[Keys.DIALOG_RETURN] = True
        notes: tk.Text = self._data[Keys.DNOTES]
        self._data[Keys.TEXT] = notes.get(1.0, tk.END)
        self.destroy()

    def __bt_close(self) -> None:
        """Button CLOSE handler."""
        self._data[Keys.DIALOG_RETURN] = False
        self.destroy()

    @property
    def dialog_return(self) -> Optional[bool]:
        """Returns notes dialog decision."""
        return self._data[Keys.DIALOG_RETURN]

    @property
    def get_notes(self) -> str:
        """Returns notes text."""
        return self._data[Keys.TEXT]


# #[EOF]#######################################################################
