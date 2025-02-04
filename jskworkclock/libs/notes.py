# -*- coding: utf-8 -*-
"""
  notes.py
  Author : Jacek 'Szumak' Kotlarski --<szumak@virthost.pl>
  Created: 22.12.2023, 01:22:15
  
  Purpose: Notes dialog class.
"""

import tkinter as tk

from tkinter import ttk
from tkinter.scrolledtext import ScrolledText
from typing import Optional

from jsktoolbox.basetool.data import BData
from jsktoolbox.tktool.base import TkBase
from jsktoolbox.tktool.layout import Pack


from libs.ico import ImageBase64
from libs.keys import Keys


class NotesDialog(BData, TkBase, tk.Toplevel):
    """Modal Dialog box."""

    def __init__(self, master, **args) -> None:
        """Constructor."""
        super().__init__(master, **args)
        self.title(f"{master.title()}: Notes")
        self.minsize(600, 400)

        # bind events
        self.protocol("WM_DELETE_WINDOW", self.__bt_close)

        # init locals
        self._set_data(key=Keys.DIALOG_RETURN,value=None, set_default_type=Optional[bool])
        self._set_data(key=Keys.TEXT,value="",set_default_type=str)

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
        self.wm_iconphoto(True, ico)

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
        self._set_data(key=Keys.D_NOTES,value=notes,set_default_type=ScrolledText)
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
        # add ok button
        ok_button = ttk.Button(bt_frame, text="Ok", command=self.__bt_ok)
        ok_button.pack(side=Pack.Side.RIGHT, padx=2)
        self.update()

    def __bt_ok(self) -> None:
        """Button OK handler."""
        self._set_data(key=Keys.DIALOG_RETURN,value=True)
        notes: tk.Text = self._get_data(key=Keys.D_NOTES)  # type: ignore
        self._set_data(key=Keys.TEXT,value=notes.get(1.0,tk.END))
        self.destroy()

    def __bt_close(self) -> None:
        """Button CLOSE handler."""
        self._set_data(key=Keys.DIALOG_RETURN,value=False)
        self.destroy()

    @property
    def dialog_return(self) -> Optional[bool]:
        """Returns notes dialog decision."""
        return self._get_data(key=Keys.DIALOG_RETURN) # type: ignore

    @property
    def get_notes(self) -> str:
        """Returns notes text."""
        return self._get_data(key=Keys.TEXT) # type: ignore


# #[EOF]#######################################################################
