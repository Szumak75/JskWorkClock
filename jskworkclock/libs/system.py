# -*- coding: utf-8 -*-
"""
  system.py
  Author : Jacek 'Szumak' Kotlarski --<szumak@virthost.pl>
  Created: 29.12.2023, 04:19:32
  
  Purpose: System interaction classes.
"""

from datetime import datetime
import os
from typing import Optional
from l10n import Locale, Locales

from jsktoolbox.libs.system import Env
from jsktoolbox.datetool import DateTime


class MDateTime(DateTime):
    """docstring for MDateTime."""

    @classmethod
    @property
    def short_date(cls) -> str:
        dtn: datetime = DateTime.now()
        return f"{dtn.year}-{dtn.month}-{dtn.day}"


class MEnv(Env):
    """Extended Env version."""

    @classmethod
    @property
    def lang(cls) -> Optional[str]:
        """The lang property."""
        lang: Optional[str] = os.getenv("LANG")
        print(lang)
        if lang is not None:
            if lang.find("_") > -1:
                return lang.split("_")[0]
        return lang


class Translate(object):
    """Locale translate class."""

    __locales: Optional[Locale] = None

    def __init__(self) -> None:
        """Constructor."""
        locales = Locales()
        if MEnv.lang is not None:
            self.__locales = locales[MEnv.lang]
        else:
            self.__locales = locales["C"]

    def get(self, string: str) -> str:
        """Returns translated string."""
        if isinstance(self.__locales, Locale):
            return self.__locales.get(string)
        return string


# #[EOF]#######################################################################
