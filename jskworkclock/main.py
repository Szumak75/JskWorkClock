#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
  Author:  Jacek 'Szumak' Kotlarski --<szumak@virthost.pl>
  Created: 10.12.2023

  Purpose: main project classes.

  https://www.pythontutorial.net/tkinter/tkinter-object-oriented-frame/
  https://ttkbootstrap.readthedocs.io/en/version-0.5/widgets/spinbox.html
"""

import os
import tkinter as tk

from tkinter import ttk
from time import sleep
from typing import Optional,Union
from time import sleep
from threading import Thread
from inspect import currentframe
from datetime import timedelta
from jsktoolbox.datetool import DateTime, Timestamp
from jsktoolbox.libs.system import PathChecker, Env
from jsktoolbox.raisetool import Raise
from jsktoolbox.tktool.base import TkBase
from jsktoolbox.tktool.layout import Pack
from sqlalchemy.orm import Session

from libs.base import BDbHandler
from libs.ico import ImageBase64
from libs.database import Database, TWorkTime
from libs.keys import Keys
from libs.notes import NotesDialog
from libs.report import ReportDialog


class MainFrame(TkBase, BDbHandler, ttk.Frame):
    """WorkClock main frame class."""

    def __init__(self, master, dbh: Database, **args) -> None:
        """Constructor."""
        super().__init__(master, **args)

        # init locals
        self._data[Keys.F_STOP] = False
        self._data[Keys.DEF_NAME] = master.title()
        self._data[Keys.TH_CLOCK] = None
        self._db_handler = dbh

        # init ui
        self.__init_ui()

    def __init_ui(self) -> None:
        """Initialize GUI."""
        # loc = Translate()
        self._data[Keys.BT_START] = ttk.Button(
            # self, text=loc.get("Start"), command=self.__bt_start, width=15
            self,
            text="Start",
            command=self.__bt_start,
            width=15,
        )
        self._data[Keys.BT_START].pack(
            side=Pack.Side.LEFT, expand=True, fill=Pack.Fill.BOTH, padx=4, pady=4
        )
        self._data[Keys.BT_STOP] = ttk.Button(
            self, text="Stop", command=self.__bt_stop, width=15, state=tk.DISABLED
        )
        self._data[Keys.BT_STOP].pack(
            side=Pack.Side.RIGHT, expand=True, fill=Pack.Fill.BOTH, padx=4, pady=4
        )

    def __bt_start(self) -> None:
        """[Start] click."""
        self._data[Keys.F_STOP] = False
        self._data[Keys.TH_CLOCK] = Thread(
            target=self.__th_worker, name="WorkingTime worker", daemon=True
        )
        self._data[Keys.TH_CLOCK].start()
        self._data[Keys.BT_START][Keys.STATE] = tk.DISABLED
        self._data[Keys.BT_STOP][Keys.STATE] = tk.NORMAL

    def __bt_stop(self) -> None:
        """[Stop] click."""
        self._data[Keys.F_STOP] = True

    def __th_worker(self) -> None:
        """Threaded worker."""
        notes: Optional[str] = None
        elapsed_time: Optional[timedelta] = None
        start: Union[int,float] = Timestamp.now()
        title: str = f"{self._data[Keys.DEF_NAME]}"
        while not self._data[Keys.F_STOP]:
            elapsed_time = DateTime.elapsed_time_from_seconds(Timestamp.now() - start)
            if self.master is not None:
                self.master.title(f"{title}: {elapsed_time}")  # type: ignore
            sleep(1)

        self._data[Keys.BT_START][Keys.STATE] = tk.NORMAL
        self._data[Keys.BT_STOP][Keys.STATE] = tk.DISABLED
        # raise message box for notes
        dialog = NotesDialog(self.master)
        dialog.wait_window()
        # get dialog data
        if dialog.dialog_return:
            notes = dialog.get_notes
        del dialog
        dialog = None
        # insert data to database
        session: Optional[Session] = self._db_handler.session
        if session:
            obj = TWorkTime()
            obj.start = int(start)
            obj.duration = int(
                DateTime.elapsed_time_from_seconds(
                    Timestamp.now() - start
                ).total_seconds()
            )
            if notes:
                obj.notes = notes
            session.add(obj)
            session.commit()
            session.close()

        print(elapsed_time)


class WorkClock(tk.Tk, TkBase, BDbHandler):
    """WorkClock main application class."""

    def __init__(self) -> None:
        """Constructor."""
        super().__init__()

        # init locals
        self._data[Keys.W_REPORT] = None
        self._data[Keys.CACHE_DIR] = ".cache/jskworkclock"
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
            Env().home, self._data[Keys.CACHE_DIR], self._data[Keys.DATABASE]
        )
        db = Database(tmp)
        if db is not None:
            self._db_handler = db
        else:
            raise Raise.error(
                "Init database error.", OSError, self._c_name, currentframe()
            )

    def __init_dirs(self) -> None:
        """Initialize local path for database."""
        tmp: str = os.path.join(
            Env().home, self._data[Keys.CACHE_DIR], self._data[Keys.DATABASE]
        )
        # print(tmp)
        pc = PathChecker(tmp)
        if not pc.exists:
            if not pc.create():
                raise Raise.error(
                    f"Cannot create local database: '{tmp}'",
                    OSError,
                    self._c_name,
                    currentframe(),
                )

    def __init_ui(self) -> None:
        """Initialize GUI."""
        # init window
        self.title("Working Time")
        # self.geometry("300x40")
        self.resizable(False, False)
        ico = tk.PhotoImage(data=ImageBase64.ICO)
        self.wm_iconphoto(True, ico)

        self.protocol("WM_DELETE_WINDOW", self.__quit_window)

        mf = MainFrame(self, self._db_handler)
        # mf.grid(column=0, row=0, sticky=tk.NSEW)
        mf.pack(side=Pack.Side.TOP, fill=Pack.Fill.BOTH, anchor=Pack.Anchor.CENTER)

        # menu
        menubar = tk.Menu(self)
        # File
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Report", command=self.__report)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.__quit_window)
        # Help
        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="About", command=self.__about)
        menubar.add_cascade(label="File", menu=file_menu)
        menubar.add_cascade(label="Help", menu=help_menu)

        self.config(menu=menubar)
        self.update()

    def __quit_window(self) -> None:
        """Quit sequence."""
        self.destroy()

    def __about(self) -> None:
        """About dialog."""
        pass

    def __report(self) -> None:
        """Report dialog."""
        if self._data[Keys.W_REPORT] is None or self._data[Keys.W_REPORT].is_closed:
            if self._data[Keys.W_REPORT] is not None:
                del self._data[Keys.W_REPORT]
                self._data[Keys.W_REPORT] = None
            self._data[Keys.W_REPORT] = ReportDialog(master=self, dbh=self._db_handler)


if __name__ == "__main__":
    app = WorkClock()
    app.mainloop()


# #[EOF]#######################################################################
