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
from typing import Optional, Union
from time import sleep
from threading import Thread
from inspect import currentframe
from datetime import timedelta
from jsktoolbox.datetool import DateTime, Timestamp
from jsktoolbox.systemtool import PathChecker, Env
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
        self._set_data(key=Keys.F_STOP, value=False, set_default_type=bool)
        self._set_data(key=Keys.DEF_NAME, value=master.title(), set_default_type=str)
        self._set_data(key=Keys.TH_CLOCK, value=None, set_default_type=Optional[Thread])
        self._db_handler = dbh

        # init ui
        self.__init_ui()

    def __init_ui(self) -> None:
        """Initialize GUI."""
        # loc = Translate()
        self._set_data(
            key=Keys.BT_START,
            value=ttk.Button(
                # self, text=loc.get("Start"), command=self.__bt_start, width=15
                self,
                text="Start",
                command=self.__bt_start,
                width=15,
            ),
            set_default_type=ttk.Button,
        )
        self._get_data(key=Keys.BT_START).pack(  # type: ignore
            side=Pack.Side.LEFT, expand=True, fill=Pack.Fill.BOTH, padx=4, pady=4
        )
        self._set_data(
            key=Keys.BT_STOP,
            value=ttk.Button(
                self, text="Stop", command=self.__bt_stop, width=15, state=tk.DISABLED
            ),
            set_default_type=ttk.Button,
        )
        self._get_data(key=Keys.BT_STOP).pack(  # type: ignore
            side=Pack.Side.RIGHT, expand=True, fill=Pack.Fill.BOTH, padx=4, pady=4
        )

    def __bt_start(self) -> None:
        """[Start] click."""
        self._set_data(key=Keys.F_STOP, value=False)
        self._set_data(
            key=Keys.TH_CLOCK,
            value=Thread(
                target=self.__th_worker, name="WorkingTime worker", daemon=True
            ),
        )
        self._get_data(key=Keys.TH_CLOCK).start()  # type: ignore
        self._get_data(key=Keys.BT_START)[Keys.STATE] = tk.DISABLED  # type: ignore
        self._get_data(key=Keys.BT_STOP)[Keys.STATE] = tk.NORMAL  # type: ignore

    def __bt_stop(self) -> None:
        """[Stop] click."""
        self._set_data(key=Keys.F_STOP, value=True)

    def __th_worker(self) -> None:
        """Threaded worker."""
        notes: Optional[str] = None
        elapsed_time: Optional[timedelta] = None
        start: Union[int, float] = Timestamp.now()
        title: str = f"{self._get_data(key=Keys.DEF_NAME)}"
        while not self._get_data(key=Keys.F_STOP):
            elapsed_time = DateTime.elapsed_time_from_seconds(Timestamp.now() - start)
            if self.master is not None:
                self.master.title(f"{title}: {elapsed_time}")  # type: ignore
            sleep(1)

        self._get_data(key=Keys.BT_START)[Keys.STATE] = tk.NORMAL  # type: ignore
        self._get_data(key=Keys.BT_STOP)[Keys.STATE] = tk.DISABLED  # type: ignore
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
        self._set_data(
            key=Keys.W_REPORT, value=None, set_default_type=Optional[ReportDialog]
        )
        self._set_data(
            key=Keys.CACHE_DIR, value=".cache/jskworkclock", set_default_type=str
        )
        self._set_data(key=Keys.DATABASE, value="data.sqlite", set_default_type=str)

        # init dirs
        self.__init_dirs()

        # init db
        self.__init_db()

        # init GUI
        self.__init_ui()

    @property
    def __db_path(self) -> str:
        """Return database path."""
        return os.path.join(
            Env().home,
            f"{self._get_data(key=Keys.CACHE_DIR)}",
            f"{self._get_data(key=Keys.DATABASE)}",
        )

    def __init_db(self) -> None:
        """Initialize database connection."""
        db = Database(self.__db_path)
        if db is not None:
            self._db_handler = db
        else:
            raise Raise.error(
                "Init database error.", OSError, self._c_name, currentframe()
            )

    def __init_dirs(self) -> None:
        """Initialize local path for database."""
        pc = PathChecker(self.__db_path)
        if not pc.exists:
            if not pc.create():
                raise Raise.error(
                    f"Cannot create local database: '{self.__db_path}'",
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
        # TODO: implement about dialog
        pass

    def __report(self) -> None:
        """Report dialog."""
        wr: Optional[ReportDialog] = self._get_data(key=Keys.W_REPORT)
        if wr is None or wr.is_closed:
            if wr is not None:
                del wr
                self._set_data(key=Keys.W_REPORT, value=None)
            self._set_data(
                key=Keys.W_REPORT, value=ReportDialog(master=self, dbh=self._db_handler)
            )


if __name__ == "__main__":
    app = WorkClock()
    app.mainloop()


# #[EOF]#######################################################################
