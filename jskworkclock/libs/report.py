# -*- coding: utf-8 -*-
"""
  report.py
  Author : Jacek 'Szumak' Kotlarski --<szumak@virthost.pl>
  Created: 22.12.2023, 15:18:32
  
  Purpose: Classes for report dialog.

  Printers example
  https://gist.github.com/mutaku/1928574
"""


import tkinter as tk
import pickle

from tkinter import StringVar, ttk
from tkinter.scrolledtext import ScrolledText
from tkinter.filedialog import asksaveasfile, askopenfile

from typing import Optional, Literal, List, Tuple, Any
from datetime import timedelta, datetime, date

from tkcalendar import Calendar

from sqlalchemy.orm import Session
from sqlalchemy.sql import func, and_

from jsktoolbox.basetool.data import BData
from jsktoolbox.datetool import DateTime, Timestamp
from jsktoolbox.systemtool import Env
from jsktoolbox.tktool.layout import Grid, Pack
from jsktoolbox.tktool.base import TkBase

from libs.ico import ImageBase64
from libs.database import Database, TWorkTime
from libs.keys import Keys
from libs.base import BDbHandler
from libs.system import MDateTime


class DataFrame(BData, TkBase, ttk.Frame):
    """DataFrame for AddDataDialog."""

    def __init__(self, master, **args) -> None:
        super().__init__(master, **args)

        # grid configure
        self.columnconfigure(0)
        self.columnconfigure(1)

        self.rowconfigure(0)
        self.rowconfigure(1)

        # labels
        label_date = ttk.LabelFrame(master=self, text=" Date ")
        label_date.grid(
            column=0, row=0, sticky=Grid.Sticky.N, padx=5, pady=5, ipadx=5, ipady=5
        )

        label_time = ttk.LabelFrame(master=self, text=" Elapsed time ")
        label_time.grid(
            column=1, row=0, sticky=Grid.Sticky.N, padx=5, pady=5, ipadx=5, ipady=5
        )

        label_note = ttk.LabelFrame(master=self, text=" Notes ")
        label_note.grid(
            column=0,
            row=10,
            sticky=Grid.Sticky.N,
            columnspan=2,
            padx=5,
            pady=5,
            ipadx=5,
            ipady=5,
        )

        # date
        cal = Calendar(master=label_date)
        cal.pack(side=Pack.Side.TOP)
        self._set_data(key=Keys.D_CALENDAR, value=cal, set_default_type=Calendar)

        # elapsed time
        self._set_data(
            key=Keys.D_RADIO, value=tk.StringVar(), set_default_type=tk.StringVar
        )
        oprs: tuple[
            tuple[Literal["Add"], Literal["+"]],
            tuple[Literal["Subtract"], Literal["-"]],
        ] = (("Add", "+"), ("Subtract", "-"))
        for opr in oprs:
            ttk.Radiobutton(
                label_time, text=opr[0], value=opr[1], variable=self._get_data(key=Keys.D_RADIO)  # type: ignore
            ).pack(side=Pack.Side.TOP, fill=Pack.Fill.X, padx=5, pady=2)
        self._get_data(key=Keys.D_RADIO).set("+")  # type: ignore
        self._set_data(
            key=Keys.D_HOUR, value=tk.DoubleVar(value=0), set_default_type=tk.DoubleVar
        )
        hour = ttk.Spinbox(
            label_time,
            from_=0,
            to=23,
            textvariable=self._get_data(key=Keys.D_HOUR),  # type: ignore
            width=10,
            wrap=True,
            state="readonly",
        )
        self._get_data(key=Keys.D_HOUR).set(0)  # type: ignore
        hour.pack(side=Pack.Side.TOP, fill=Pack.Fill.X, padx=5, pady=5)
        self._set_data(
            key=Keys.D_MINUTE,
            value=tk.DoubleVar(value=0),
            set_default_type=tk.DoubleVar,
        )
        minute = ttk.Spinbox(
            label_time,
            from_=0,
            to=59,
            textvariable=self._get_data(key=Keys.D_MINUTE),  # type: ignore
            width=10,
            wrap=True,
            state="readonly",
        )
        self._get_data(key=Keys.D_MINUTE).set(0)  # type: ignore
        minute.pack(side=Pack.Side.TOP, fill=Pack.Fill.X, padx=5, pady=5)

        # notes
        notes = ScrolledText(label_note, width=46, height=8)
        self._set_data(key=Keys.D_NOTES, value=notes, set_default_type=ScrolledText)
        notes.pack(side=Pack.Side.LEFT, fill=Pack.Fill.BOTH, expand=True)

    @property
    def get_variables(self) -> tuple[Any, Any, Any, Any, Any]:
        """The get property."""
        return (
            self._get_data(key=Keys.D_CALENDAR).selection_get(),  # type: ignore
            self._get_data(key=Keys.D_RADIO).get(),  # type: ignore
            self._get_data(key=Keys.D_HOUR).get(),  # type: ignore
            self._get_data(key=Keys.D_MINUTE).get(),  # type: ignore
            self._get_data(key=Keys.D_NOTES).get(1.0, tk.END),  # type: ignore
        )


class AddDataDialog(BData, TkBase, tk.Toplevel):
    """Modal Dialog Box."""

    def __init__(self, master, **args) -> None:
        """Constructor."""
        # tk.Toplevel.__init__(self, master, *args)
        super().__init__(master, **args)
        self.title(f"{master.title()}: Add Record")

        # bind events
        self.protocol("WM_DELETE_WINDOW", self.__bt_close)

        # init locals
        self._set_data(key=Keys.W_CLOSED, value=False, set_default_type=bool)
        self._set_data(
            key=Keys.DIALOG_RETURN, value=None, set_default_type=Optional[bool]
        )
        self._set_data(key=Keys.D_DATA, value=None, set_default_type=Optional[Tuple])

        self.__init_ui()

        # modal?
        # self.root.wait_visibility()
        self.grab_set()
        # self.root.transient(parent)

    def __init_ui(self) -> None:
        """Create user interface."""
        # main window
        # self.geometry("400x300")
        self.resizable(False, False)

        ico = tk.PhotoImage(data=ImageBase64.ICO)
        self.wm_iconphoto(True, ico)

        # content
        # ttk.Spinbox

        # data frame
        data_frame = DataFrame(self)
        data_frame.pack(side=Pack.Side.TOP, fill=Pack.Fill.BOTH, expand=True)
        self._set_data(
            key=Keys.D_FRAME,
            value=data_frame,
            set_default_type=DataFrame,
        )

        # separator
        sep = ttk.Separator(self, orient=tk.HORIZONTAL)
        sep.pack(fill=Pack.Fill.X)

        # button frame
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
        self._set_data(key=Keys.DIALOG_RETURN, value=True)
        self._set_data(
            key=Keys.D_DATA,
            value=self._get_data(key=Keys.D_FRAME).get_variables,  # type: ignore
        )
        self.destroy()

    def __bt_close(self) -> None:
        """Button 'Close' Event."""
        self._set_data(key=Keys.DIALOG_RETURN, value=False)
        self.destroy()

    @property
    def dialog_return(self) -> Optional[bool]:
        """Returns notes dialog decision."""
        return self._get_data(key=Keys.DIALOG_RETURN)

    @property
    def dialog_data(self) -> Optional[Tuple]:
        """The dialog_data property."""
        return self._get_data(key=Keys.D_DATA)


class ReportDialog(TkBase, BDbHandler, tk.Toplevel):
    """Dialog box."""

    def __init__(self, master, dbh: Database, **args) -> None:
        """Constructor."""
        # tk.Toplevel.__init__(self, master, **args)
        super().__init__(master, **args)
        self.title(f"{master.title()}: Reports")
        self.minsize(800, 500)

        # init locals
        self._set_data(key=Keys.W_CLOSED, value=False, set_default_type=bool)
        self._db_handler = dbh

        self.__init_ui()

    def __init_ui(self) -> None:
        """Create user interface."""
        # set initial flags
        self._set_data(key=Keys.SWITCH_FLAG, value=False, set_default_type=bool)

        # main window
        self.geometry("700x600")

        ico = tk.PhotoImage(data=ImageBase64.ICO)
        self.wm_iconphoto(True, ico)

        self.protocol("WM_DELETE_WINDOW", self.__on_closing)

        # content

        # Sizegrip
        sizegrip = ttk.Sizegrip(self)
        sizegrip.pack(side=Pack.Side.BOTTOM, anchor=Pack.Anchor.E)

        # Data Frame
        data_frame = ttk.Frame(self)
        data_frame.pack(
            side=Pack.Side.TOP, expand=True, fill=Pack.Fill.BOTH, padx=5, pady=5
        )

        # treeview
        columns: tuple[Literal["date"], Literal["elapsed_time"], Literal["note"]] = (
            "date",
            "elapsed_time",
            "note",
        )
        tree = ttk.Treeview(data_frame, columns=columns, show="headings")
        tree.heading(columns[0], text="Date")
        tree.column(columns[0], minwidth=0, width=200, stretch=False)
        tree.heading(columns[1], text="Elapsed time")
        tree.column(columns[1], minwidth=0, width=160, stretch=False)
        tree.heading(columns[2], text="Note")
        tree.column(columns[2], minwidth=0, width=400)

        tree.pack(side=Pack.Side.LEFT, fill=Pack.Fill.BOTH, expand=True)
        self._set_data(
            key=Keys.D_REPORT,
            value=tree,
            set_default_type=type(tree),
        )

        # add a scrollbar
        scrollbar = ttk.Scrollbar(data_frame, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=Pack.Side.RIGHT, fill=Pack.Fill.Y)

        # tree data
        self.__tree_reload()

        # separator
        sep = ttk.Separator(self, orient=tk.HORIZONTAL)
        sep.pack(fill=Pack.Fill.X)

        # Button Frame
        bt_frame = ttk.Frame(self)
        bt_frame.pack(side=Pack.Side.TOP, fill=Pack.Fill.X, padx=5, pady=5)

        # add close button
        close_button = ttk.Button(bt_frame, text="Close", command=self.__bt_close)
        close_button.pack(side=Pack.Side.RIGHT, padx=2)

        # add record button
        add_button = ttk.Button(bt_frame, text="Add Data", command=self.__bt_add)
        add_button.pack(side=Pack.Side.RIGHT, padx=2)

        # add save button
        save_button = ttk.Button(bt_frame, text="Save", command=self.__bt_save)
        save_button.pack(side=Pack.Side.RIGHT, padx=2)

        # add previous/current month
        switch_button = ttk.Button(
            bt_frame, text="Switch to previous month", command=self.__bt_switch
        )
        switch_button.pack(side=Pack.Side.RIGHT, padx=2)
        self._set_data(
            key=Keys.BT_SWITCH,
            value=switch_button,
            set_default_type=type(switch_button),
        )

        # add export button
        export_button = ttk.Button(bt_frame, text="Export", command=self.__bt_export)
        export_button.pack(side=Pack.Side.RIGHT, padx=2)

        # add import button
        import_button = ttk.Button(bt_frame, text="Import", command=self.__bt_import)
        import_button.pack(side=Pack.Side.RIGHT, padx=2)

    def __tree_reload(self) -> None:
        tree: ttk.Treeview = self._get_data(key=Keys.D_REPORT)  # type: ignore
        # emptying tree
        for item in tree.get_children():
            tree.delete(item)
        # fill tree
        for item in self.__get_data():
            tree.insert("", tk.END, values=item)

    def __bt_export(self) -> None:
        """On Export Event."""
        file = asksaveasfile(
            parent=self,
            initialfile=f"WorkClock-export-{MDateTime.short_date()}.wrk",
            defaultextension=".wrk",
            filetypes=[("WorkClock export file", "*.wrk")],
            initialdir=Env().home,
        )
        self.focus()
        if file is not None:
            file.close()
            # dump data
            tmp = []
            session: Optional[Session] = self._db_handler.session
            if session is not None:
                rows = session.query(TWorkTime).all()
                for item in rows:
                    tmp.append(item)
                # pickle list
                # print(file.name)
                with open(file.name, "wb") as outfile:
                    pickle.dump(tmp, outfile)

                session.close()

    def __bt_import(self) -> None:
        """On Import Event."""
        file = askopenfile(
            parent=self,
            defaultextension=".wrk",
            filetypes=[("WorkClock export file", "*.wrk")],
            initialdir=Env().home,
        )
        self.focus()
        if file is not None:
            file.close()
            tmp: List[TWorkTime] = []
            with open(file.name, "rb") as in_file:
                tmp = pickle.load(in_file)
            if tmp:
                # import procedure
                session: Optional[Session] = self._db_handler.session
                if session is not None:
                    for item in tmp:
                        row = (
                            session.query(TWorkTime)
                            .filter(
                                TWorkTime.start == item.start,
                                TWorkTime.duration == item.duration,
                                TWorkTime.notes == item.notes,
                            )
                            .first()
                        )
                        if not row:
                            data = TWorkTime()
                            data.start = item.start
                            data.duration = item.duration
                            data.notes = item.notes
                            session.add(data)
                            session.commit()
                    session.close()
                    self.__tree_reload()

    def __on_closing(self) -> None:
        """On Closing Event."""
        self._set_data(key=Keys.W_CLOSED, value=True)
        self.destroy()

    def __bt_switch(self) -> None:
        """Button 'Switch' Event."""
        bt: ttk.Button = self._get_data(key=Keys.BT_SWITCH)  # type: ignore
        self._set_data(
            key=Keys.SWITCH_FLAG, value=(not self._get_data(key=Keys.SWITCH_FLAG))
        )

        if self._get_data(key=Keys.SWITCH_FLAG):
            bt["text"] = "Switch to current month"
        else:
            bt["text"] = "Switch to previous month"

        # reload data
        self.__tree_reload()

    def __bt_close(self) -> None:
        """Button 'Close' Event."""
        self.__on_closing()

    def __bt_add(self) -> None:
        """Button 'Add Data' Event."""
        dialog = AddDataDialog(self)
        dialog.wait_window()
        if dialog.dialog_return == True:
            if dialog.dialog_data:
                # add record
                self.__add_record(dialog.dialog_data)
                # reload data
                self.__tree_reload()
        dialog.destroy()

    def __bt_save(self) -> None:
        """Button 'Save' Event."""
        # sfd = SaveFileDialog(master=self)
        file = asksaveasfile(
            parent=self,
            initialfile=f"Report-{MDateTime.short_date()}.txt",
            defaultextension=".txt",
            filetypes=[("All Files", "*.*"), ("Text Documents", "*.txt")],
            initialdir=Env().home,
        )
        self.focus()
        if file is not None:
            tree: ttk.Treeview = self._get_data(key=Keys.D_REPORT)  # type: ignore
            for child in tree.get_children():
                list_data: List = tree.item(child)["values"]  # type: ignore
                start = list_data[0]
                duration = list_data[1]
                notes = list_data[2]
                file.write(f"{start}\t{duration}\t{notes}\n")
            file.close()

    def __add_record(self, arg: Tuple) -> None:
        """Add record to database."""
        rec_date: date = arg[0]
        rec_opr: str = arg[1]
        rec_hour: float = arg[2]
        rec_minute: float = arg[3]
        rec_note: str = arg[4]

        rec = TWorkTime()
        rec.start = int(
            datetime(
                year=rec_date.year, month=rec_date.month, day=rec_date.day
            ).timestamp()
        )
        multi: Literal[-1, 1] = -1 if rec_opr == "-" else 1
        rec.duration = int(multi * (rec_hour * 3600 + rec_minute * 60))
        rec.notes = rec_note.strip("\n")
        session: Optional[Session] = self._db_handler.session
        if session:
            session.add(rec)
            session.commit()
            session.close()

    def __get_data(self):  # -> tuple[Any, ...]:
        """Gets data for reports."""
        session: Optional[Session] = self._db_handler.session

        if session is None:
            return tuple()

        # cleanup garbage
        dataset = (
            session.query(TWorkTime)
            .filter(and_(TWorkTime.duration <= 120, TWorkTime.duration >= -120))
            .all()
        )
        for item in dataset:
            session.delete(item)
        if dataset:
            session.commit()

        # getting report
        date_sum = 0
        out = list()
        tmp: datetime = DateTime.now()
        if self._get_data(key=Keys.SWITCH_FLAG):
            # reset initial time to previous month
            tmp2 = datetime(year=tmp.year, month=tmp.month, day=1)
            tmp = DateTime.datetime_from_timestamp(tmp2.timestamp() - 1)
        # beginning of the month timestamp
        beginning_month: int = int(
            datetime(year=tmp.year, month=tmp.month, day=1).timestamp()
        )
        row = (
            session.query(func.sum(TWorkTime.duration))
            .filter(TWorkTime.start < beginning_month)
            .order_by(TWorkTime.start)
            .first()
        )
        if row and row[0] is not None:
            date_sum += row[0]
            out.append(
                (
                    DateTime.datetime_from_timestamp(beginning_month),
                    self.__format_time(
                        DateTime.elapsed_time_from_seconds(date_sum).total_seconds()
                    ),
                    "Balance of the previous month",
                )
            )

        # getting data for the current month
        dataset: List[TWorkTime] = (
            session.query(TWorkTime)
            .filter(TWorkTime.start > beginning_month)
            .order_by(TWorkTime.start)
            .all()
        )
        for item in dataset:
            item_date: datetime = DateTime.datetime_from_timestamp(item.start)
            item_dur: timedelta = DateTime.elapsed_time_from_seconds(abs(item.duration))
            opr: Literal["-", ""] = "-" if item.duration < 0 else ""
            date_sum += item.duration
            out.append((item_date, f"{opr}{item_dur}", item.notes))

        if dataset:
            out.append(
                (
                    DateTime.datetime_from_timestamp(Timestamp.now()),
                    self.__format_time(
                        DateTime.elapsed_time_from_seconds(date_sum).total_seconds()
                    ),
                    "Current Balance",
                )
            )

        session.close()
        return tuple(out)

    def __format_time(self, total_seconds: float) -> str:
        """Returns formatted time string."""
        hours: float
        reminder: float
        minutes: float
        seconds: float
        hours, reminder = divmod(total_seconds, 3600)
        minutes, seconds = divmod(reminder, 60)
        return f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}"

    @property
    def is_closed(self) -> bool:
        """The is_closed property."""
        return self._get_data(key=Keys.W_CLOSED)  # type: ignore


# #[EOF]#######################################################################
