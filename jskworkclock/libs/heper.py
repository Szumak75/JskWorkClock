# -*- coding: UTF-8 -*-
"""
  heper.py
  Author : Jacek 'Szumak' Kotlarski --<szumak@virthost.pl>
  Created: 24.12.2023, 06:10:21
  
  Purpose: 
"""

import tkinter as tk

from jsktoolbox.attribtool import ReadOnlyClass


class TkPack(object, metaclass=ReadOnlyClass):
    """docstring for TkPack."""

    class Anchor(object, metaclass=ReadOnlyClass):
        NW = tk.NW
        N = tk.N
        NE = tk.NE
        W = tk.W
        CENTER = tk.CENTER
        E = tk.E
        SW = tk.SW
        S = tk.S
        SE = tk.SE

    class Side(object, metaclass=ReadOnlyClass):
        TOP = tk.TOP
        BOTTOM = tk.BOTTOM
        LEFT = tk.LEFT
        RIGHT = tk.RIGHT

    class Fill(object, metaclass=ReadOnlyClass):
        NONE = tk.NONE
        X = tk.X
        Y = tk.Y
        BOTH = tk.BOTH


class TkGrid(object, metaclass=ReadOnlyClass):
    """docstring for TkPack."""

    class Sticky(object, metaclass=ReadOnlyClass):
        NW = tk.NW
        N = tk.N
        NE = tk.NE
        W = tk.W
        CENTER = tk.CENTER
        E = tk.E
        SW = tk.SW
        S = tk.S
        SE = tk.SE


class TkPlace(object, metaclass=ReadOnlyClass):
    class Anchor(object, metaclass=ReadOnlyClass):
        NW = tk.NW
        N = tk.N
        NE = tk.NE
        W = tk.W
        CENTER = tk.CENTER
        E = tk.E
        SW = tk.SW
        S = tk.S
        SE = tk.SE


# #[EOF]#######################################################################
