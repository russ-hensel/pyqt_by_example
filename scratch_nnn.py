#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul  1 11:03:24 2025

@author: russ
"""


# ---- tof

# ---- imports

# ---- end imports


#-------------------------------






# ---- eof

# signals_slots.py

"""Signals and slots example."""

import sys

from PyQt5.QtWidgets import (
    QApplication,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

def greet(self ):
    if self.msgLabel.text():
        self.msgLabel.setText("")
    else:
        self.msgLabel.setText("Hello, World!")


window.setWindowTitle("Signals and slots")


layout = QVBoxLayout()
add here
widget = QPushButton("Greet")
widget.clicked.connect(greet)

layout.addWidget(widget)
widget = QLabel("")
self.msgLabel = widget
layout.addWidget( widget )
