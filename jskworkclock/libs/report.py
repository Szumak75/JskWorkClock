# -*- coding: utf-8 -*-
"""
  report.py
  Author : Jacek 'Szumak' Kotlarski --<szumak@virthost.pl>
  Created: 22.12.2023, 15:18:32
  
  Purpose: 

  Printers example
  https://gist.github.com/mutaku/1928574
"""


import os
import tkinter as tk

from tkinter import ttk
from tkinter.scrolledtext import ScrolledText
from time import sleep
from turtle import heading
from typing import Optional, Literal, List, Tuple, Any
from PIL import Image, ImageDraw
from time import sleep
from threading import Thread
from inspect import currentframe
from datetime import timedelta, datetime

from tkcalendar import Calendar

from sqlalchemy.orm import Session
from sqlalchemy.sql import func

from jsktoolbox.libs.base_data import BData
from jsktoolbox.datetool import DateTime, Timestamp
from jsktoolbox.attribtool import ReadOnlyClass
from jsktoolbox.libs.system import PathChecker, Env
from jsktoolbox.raisetool import Raise


from libs.base import TkBase, TtkBase
from libs.ico import ImageBase64
from libs.database import Database, TWorkTime
from libs.keys import Keys
from libs.base import BDbHandler
from libs.heper import TkGrid, TkPack


class DataFrame(BData, TtkBase, ttk.Frame):
    """DataFrame for AddDataDialog."""

    def __init__(self, parent, *args) -> None:
        super().__init__(parent, *args)

        # grid configure
        self.columnconfigure(0)
        self.columnconfigure(1)

        self.rowconfigure(0)
        self.rowconfigure(1)

        # labels
        ldate = ttk.LabelFrame(master=self, text=" Date ")
        ldate.grid(
            column=0, row=0, sticky=TkGrid.Sticky.N, padx=5, pady=5, ipadx=5, ipady=5
        )

        ltime = ttk.LabelFrame(master=self, text=" Elapsed time ")
        ltime.grid(
            column=1, row=0, sticky=TkGrid.Sticky.N, padx=5, pady=5, ipadx=5, ipady=5
        )

        lnote = ttk.LabelFrame(master=self, text=" Notes ")
        lnote.grid(
            column=0,
            row=10,
            sticky=TkGrid.Sticky.N,
            columnspan=2,
            padx=5,
            pady=5,
            ipadx=5,
            ipady=5,
        )

        # date
        cal = Calendar(master=ldate)
        cal.pack(side=TkPack.Side.TOP)
        self._data[Keys.DCALENDAR] = cal
        print(cal.selection_get())

        # elapsed time
        self._data[Keys.DRADIO] = tk.StringVar()
        oprs: tuple[
            tuple[Literal["Add"], Literal["+"]],
            tuple[Literal["Subtract"], Literal["-"]],
        ] = (("Add", "+"), ("Subtract", "-"))
        for opr in oprs:
            ttk.Radiobutton(
                ltime, text=opr[0], value=opr[1], variable=self._data[Keys.DRADIO]
            ).pack(side=TkPack.Side.TOP, fill=TkPack.Fill.X, padx=5, pady=2)
        self._data[Keys.DRADIO].set("+")
        self._data[Keys.DHOUR] = tk.DoubleVar(value=0)
        hour = ttk.Spinbox(
            ltime,
            from_=0,
            to=23,
            textvariable=self._data[Keys.DHOUR],
            width=10,
            wrap=True,
            state="readonly",
        )
        self._data[Keys.DHOUR].set(0)
        hour.pack(side=TkPack.Side.TOP, fill=TkPack.Fill.X, padx=5, pady=5)
        self._data[Keys.DMINUTE] = tk.DoubleVar(value=0)
        minute = ttk.Spinbox(
            ltime,
            from_=0,
            to=59,
            textvariable=self._data[Keys.DMINUTE],
            width=10,
            wrap=True,
            state="readonly",
        )
        self._data[Keys.DMINUTE].set(0)
        minute.pack(side=TkPack.Side.TOP, fill=TkPack.Fill.X, padx=5, pady=5)

        # notes
        notes = ScrolledText(lnote, width=46, height=8)
        self._data[Keys.DNOTES] = notes
        notes.pack(side=TkPack.Side.LEFT, fill=TkPack.Fill.BOTH, expand=True)

    @property
    def get_variables(self) -> tuple[Any, Any, Any, Any, Any]:
        """The get property."""
        return (
            self._data[Keys.DCALENDAR].selection_get(),
            self._data[Keys.DRADIO].get(),
            self._data[Keys.DHOUR].get(),
            self._data[Keys.DMINUTE].get(),
            self._data[Keys.DNOTES].get(1.0, tk.END),
        )


class AddDataDialog(BData, TtkBase, tk.Toplevel):
    """Modal Dialog Box."""

    def __init__(self, parent: tk.Toplevel, *args) -> None:
        """Constructor."""
        tk.Toplevel.__init__(self, parent, *args)
        self.title(f"{parent.title()}: Add Record")

        # bind events
        self.protocol("WM_DELETE_WINDOW", self.__bt_close)

        # init locals
        self._data[Keys.WCLOSED] = False
        self._data[Keys.DIALOG_RETURN] = None

        self.__init_ui()

        # modal?
        # self.root.wait_visibility()
        self.grab_set()
        # self.root.transient(parent)

    def __init_ui(self) -> None:
        """Create user interface."""
        # main window
        # self.geometry("400x300")
        self.update()
        self.resizable(False, False)

        ico = tk.PhotoImage(data=ImageBase64.ICO)
        self.wm_iconphoto(False, ico)

        # content
        # ttk.Spinbox

        # data frame
        data_frame = DataFrame(self)
        data_frame.pack(side=TkPack.Side.TOP, fill=TkPack.Fill.BOTH, expand=True)
        self._data[Keys.DFRAME] = data_frame

        # separator
        sep = ttk.Separator(self, orient=tk.HORIZONTAL)
        sep.pack(fill=TkPack.Fill.X)

        # button frame
        # add button frame
        bt_frame = ttk.Frame(self)
        bt_frame.pack(side=TkPack.Side.TOP, fill=TkPack.Fill.X, padx=5, pady=5)
        # add close button
        close_button = ttk.Button(bt_frame, text="Close", command=self.__bt_close)
        close_button.pack(side=TkPack.Side.RIGHT, padx=2)
        # add ok buton
        ok_button = ttk.Button(bt_frame, text="Ok", command=self.__bt_ok)
        ok_button.pack(side=TkPack.Side.RIGHT, padx=2)

    def __bt_ok(self) -> None:
        """Button OK handler."""
        self._data[Keys.DIALOG_RETURN] = True
        print(self._data[Keys.DFRAME].get_variables)
        self.destroy()

    def __bt_close(self) -> None:
        """Button 'Close' Event."""
        self._data[Keys.DIALOG_RETURN] = False
        self.destroy()

    @property
    def dialog_return(self) -> Optional[bool]:
        """Returns notes dialog decision."""
        return self._data[Keys.DIALOG_RETURN]

    @property
    def dialog_data(self) -> str:
        """The dialog_data property."""
        return "test"


class ReportDialog(TtkBase, BDbHandler, tk.Toplevel):
    """Dailog box."""

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
        self.geometry("700x600")

        ico = tk.PhotoImage(data=ImageBase64.ICO)
        self.wm_iconphoto(False, ico)

        self.protocol("WM_DELETE_WINDOW", self.__on_closing)

        # content

        # Sizegrip
        sizegrip = ttk.Sizegrip(self)
        sizegrip.pack(side=TkPack.Side.BOTTOM, anchor=TkPack.Anchor.E)

        # Data Frame
        data_frame = ttk.Frame(self)
        data_frame.pack(
            side=TkPack.Side.TOP, expand=True, fill=TkPack.Fill.BOTH, padx=5, pady=5
        )

        # treeview
        columns: tuple[Literal["date"], Literal["elapsed_time"], Literal["note"]] = (
            "date",
            "elapsed_time",
            "note",
        )
        tree = ttk.Treeview(data_frame, columns=columns, show="headings")
        tree.heading(columns[0], text="Date")
        tree.column(columns[0], minwidth=0, width=150, stretch=False)
        tree.heading(columns[1], text="Elapsed time")
        tree.column(columns[1], minwidth=0, width=100, stretch=False)
        tree.heading(columns[2], text="Note")
        tree.column(columns[2], minwidth=0, width=400)

        tree.pack(side=TkPack.Side.LEFT, fill=TkPack.Fill.BOTH, expand=True)

        # add a scrollbar
        scrollbar = ttk.Scrollbar(data_frame, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=TkPack.Side.RIGHT, fill=TkPack.Fill.Y)

        # tree data
        for item in self.__get_data():
            tree.insert("", tk.END, values=item)

        # separator
        sep = ttk.Separator(self, orient=tk.HORIZONTAL)
        sep.pack(fill=TkPack.Fill.X)

        # Button Frame
        bt_frame = ttk.Frame(self)
        bt_frame.pack(side=TkPack.Side.TOP, fill=TkPack.Fill.X, padx=5, pady=5)

        # add close button
        close_button = ttk.Button(bt_frame, text="Close", command=self.__bt_close)
        close_button.pack(side=TkPack.Side.RIGHT, padx=2)

        # add record button
        add_button = ttk.Button(bt_frame, text="Add Data", command=self.__bt_add)
        add_button.pack(side=TkPack.Side.RIGHT, padx=2)

        # add save button
        save_button = ttk.Button(bt_frame, text="Save", command=self.__bt_save)
        save_button.pack(side=TkPack.Side.RIGHT, padx=2)

    def __on_closing(self) -> None:
        """On Closing Event."""
        self._data[Keys.WCLOSED] = True
        self.destroy()

    def __bt_close(self) -> None:
        """Button 'Close' Event."""
        self.__on_closing()

    def __bt_add(self) -> None:
        """Button 'Add Data' Event."""
        dialog = AddDataDialog(self)
        dialog.wait_window()

    def __bt_save(self) -> None:
        """Button 'Save' Event."""
        pass

    def __get_data(self):  # -> tuple[Any, ...]:
        session: Session | None = self._db_handler.session

        if session is None:
            return tuple()

        # cleanup garbage
        dataset = session.query(TWorkTime).filter(TWorkTime.duration <= 120).all()
        for item in dataset:
            session.delete(item)
        if dataset:
            session.commit()

        # getting report
        dsum = 0
        out = list()
        tmp: datetime = DateTime.now()
        # beginning of the month timestamp
        bmonth: int = int(datetime(year=tmp.year, month=tmp.month, day=1).timestamp())
        row = (
            session.query(func.sum(TWorkTime.duration))
            .filter(TWorkTime.start < bmonth)
            .first()
        )
        if row and row[0] is not None:
            dsum += row[0]
            out.append(
                (
                    DateTime.datetime_from_timestamp(bmonth),
                    DateTime.elapsed_time_from_seconds(dsum),
                    "Balance of the previous month",
                )
            )

        # getting data for the current month
        dataset: List[TWorkTime] = (
            session.query(TWorkTime)
            .filter(TWorkTime.start > bmonth)
            .order_by(TWorkTime.id)
            .all()
        )
        for item in dataset:
            idate: datetime = DateTime.datetime_from_timestamp(item.start)
            idur: timedelta = DateTime.elapsed_time_from_seconds(item.duration)
            dsum += item.duration
            out.append((idate, idur, item.notes))

        if dataset:
            out.append(
                (
                    DateTime.datetime_from_timestamp(Timestamp.now),
                    DateTime.elapsed_time_from_seconds(dsum),
                    "Current Balance",
                )
            )

        session.close()
        return tuple(out)

    @property
    def is_closed(self) -> bool:
        """The is_closed property."""
        return self._data[Keys.WCLOSED]


# #[EOF]#######################################################################
