#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May  1 09:14:48 2025

@author: russ
"""


# ---- tof

# ---- imports

# ---- end imports


#-------------------------------

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLineEdit, QVBoxLayout, QWidget

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Simple Qt5 App")
        self.setFixedSize(300, 100)


        # Create central widget
        a_central_widget = QWidget()

        self.setCentralWidget(a_central_widget)

        # Set up layout and to central widget
        a_layout = QVBoxLayout()

        a_central_widget.setLayout( a_layout )

        # Create other widgets
        widget = QLineEdit()
        self.line_edit = widget
        a_layout.addWidget( widget )

        widget  = QPushButton( "Click Me" )
        self.button = widget
        a_layout.addWidget( widget )

        # Connect button click to function
        self.button.clicked.connect( self.on_button_click )

    def on_button_click(self):
        # Simple action: set text in line edit when button is clicked
        self.line_edit.setText("Button Clicked!")

if __name__ == '__main__':
    args       = sys.argv
    # or
    args       = []
    app = QApplication( args )
    window      = MainWindow()
    window.show()
    code        = app.exec_()
    #sys.exit( code )




# ---- eof