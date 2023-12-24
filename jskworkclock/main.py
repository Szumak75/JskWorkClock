#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
  Author:  Jacek 'Szumak' Kotlarski --<szumak@virthost.pl>
  Created: 10.12.2023

  Purpose:

  https://www.pythontutorial.net/tkinter/tkinter-object-oriented-frame/
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


from libs.base import TkBase, TtkBase, BDbHandler
from libs.ico import ImageBase64
from libs.database import Database, TWorkTime
from libs.keys import Keys
from libs.notes import NotesDialog
from libs.report import ReportDialog
from libs.heper import TkPack


class MainFrame(TtkBase, BDbHandler, ttk.Frame):
    """WorkClock main frame class."""

    def __init__(self, parent: tk.Tk, dbh: Database) -> None:
        """Constructor."""
        super().__init__(parent)

        # init locals
        self._data[Keys.FSTOP] = False
        self._data[Keys.DEFNAME] = parent.title()
        self._data[Keys.THCLOCK] = None
        self._db_handler = dbh

        # init ui
        self.__init_ui()

    def __init_ui(self) -> None:
        """Initialize GUI."""
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        self._data[Keys.BTSTART] = ttk.Button(self, text="Start", command=self.bt_start)
        self._data[Keys.BTSTART].grid(column=0, row=0, sticky=tk.EW)
        self._data[Keys.BTSTOP] = ttk.Button(
            self, text="Stop", command=self.bt_stop, state=tk.DISABLED
        )
        self._data[Keys.BTSTOP].grid(column=1, row=0, sticky=tk.EW)

        for widget in self.winfo_children():
            widget.grid(padx=3, pady=3)

    def bt_start(self) -> None:
        """[Start] click."""
        self._data[Keys.FSTOP] = False
        self._data[Keys.THCLOCK] = Thread(
            target=self.th_worker, name="WorkingTime worker", daemon=True
        )
        self._data[Keys.THCLOCK].start()
        self._data[Keys.BTSTART][Keys.STATE] = tk.DISABLED
        self._data[Keys.BTSTOP][Keys.STATE] = tk.NORMAL

    def bt_stop(self) -> None:
        """[Stop] click."""
        self._data[Keys.FSTOP] = True

    def th_worker(self) -> None:
        """Threaded worker."""
        notes: Optional[str] = None
        etime: Optional[timedelta] = None
        start: int = Timestamp.now
        title: str = f"{self._data[Keys.DEFNAME]}"
        while not self._data[Keys.FSTOP]:
            etime = DateTime.elapsed_time_from_seconds(Timestamp.now - start)
            if self.master is not None:
                self.master.title(f"{title}: {etime}")  # type: ignore
            sleep(1)

        self._data[Keys.BTSTART][Keys.STATE] = tk.NORMAL
        self._data[Keys.BTSTOP][Keys.STATE] = tk.DISABLED
        # raise message box for notes
        dialog = NotesDialog(self.master)
        while dialog.dialog_return is None:
            sleep(0.2)
        # get dialog data
        if dialog.dialog_return:
            notes = dialog.get_notes
        # destroy dialog
        dialog.destroy()
        dialog = None
        # insert data to database
        session = self._db_handler.session
        if session:
            obj = TWorkTime()
            obj.start = start
            obj.duration = int(
                DateTime.elapsed_time_from_seconds(
                    Timestamp.now - start
                ).total_seconds()
            )
            if notes:
                obj.notes = notes
            session.add(obj)
            session.commit()
            session.close()

        print(etime)


class WorkClock(TkBase, BDbHandler, tk.Tk):
    """WorkClock main application class."""

    def __init__(self) -> None:
        """Constructor."""
        super().__init__()

        # init locals
        self._data[Keys.WREPORT] = None
        self._data[Keys.CACHEDIR] = ".cache/jskworkclock"
        self._data[Keys.DATABASE] = "data.sqlite"

        # init dirs
        self.__init_dirs()

        # init db
        self.__init_db()

        # init GUI
        self.__init_ui()

    def __init_db(self) -> None:
        """Initialize database connection."""
        tmp: str = os.path.join(
            Env.home, self._data[Keys.CACHEDIR], self._data[Keys.DATABASE]
        )
        db = Database(tmp)
        if db is not None:
            self._db_handler = db
        else:
            raise Raise.error(
                "Init database error.", OSError, self._c_name, currentframe()  # type: ignore
            )

    def __init_dirs(self) -> None:
        """Initialize local path for database."""
        tmp: str = os.path.join(
            Env.home, self._data[Keys.CACHEDIR], self._data[Keys.DATABASE]
        )
        # print(tmp)
        pc = PathChecker(tmp)
        if not pc.exists:
            if not pc.create():
                raise Raise.error(
                    f"Cannot create local database: '{tmp}'",
                    OSError,  # type: ignore
                    self._c_name,
                    currentframe(),
                )

    def __init_ui(self) -> None:
        """Initialize GUI."""
        # init window
        self.title("Working Time")
        self.geometry("300x40")
        self.resizable(False, False)
        ico = tk.PhotoImage(data=ImageBase64.ICO)
        self.wm_iconphoto(False, ico)

        self.protocol("WM_DELETE_WINDOW", self.__quit_window)

        mf = MainFrame(self, self._db_handler)
        # mf.grid(column=0, row=0, sticky=tk.NSEW)
        mf.pack(
            side=TkPack.Side.TOP, fill=TkPack.Fill.BOTH, anchor=TkPack.Anchor.CENTER
        )

        # menu
        menubar = tk.Menu(self)
        # File
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Report", command=self.__report)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=self.__quit_window)
        # Help
        helpmenu = tk.Menu(menubar, tearoff=0)
        helpmenu.add_command(label="About", command=self.__about)
        menubar.add_cascade(label="File", menu=filemenu)
        menubar.add_cascade(label="Help", menu=helpmenu)

        self.config(menu=menubar)

    def __quit_window(self) -> None:
        """Quit sequence."""
        self.destroy()

    def __about(self) -> None:
        """About dialog."""
        pass

    def __report(self) -> None:
        """Report dialog."""
        if self._data[Keys.WREPORT] is None or self._data[Keys.WREPORT].is_closed:
            if self._data[Keys.WREPORT] is not None:
                del self._data[Keys.WREPORT]
                self._data[Keys.WREPORT] = None
            self._data[Keys.WREPORT] = ReportDialog(parent=self, dbh=self._db_handler)


if __name__ == "__main__":
    app = WorkClock()
    app.mainloop()


# #[EOF]#######################################################################
