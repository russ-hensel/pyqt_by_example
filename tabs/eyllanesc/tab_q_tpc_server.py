#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ---- tof
"""
# metadata here including WIKI_LINK as Constant ( not comment )
# this material is used for selection access to the tab module which should
# be named xxxxTab.py     among other things


KEY_WORDS:      eyllanesc tcp network loopback eyllanesc
CLASS_NAME:     QTcpServerTab
WIDGETS:        QAbstractSocket   QTcpServer  QTcpSocket QProgressBar
STATUS:         works at first blush
TAB_TITLE:      QTcp / Example
DESCRIPTION:    An example of TcpServer... from eyllanesc examples
HOW_COMPLETE:   10  #  AND A COMMENT -- <10 major probs  <15 runs but <20 fair not finished  <=25 not to shabby
"""

WIKI_LINK      =  "https://github.com/russ-hensel/pyqt_by_example/wiki/What-We-Know-About-QTcpServer"

"""
Some Notes:

eyllanesc/QtExamples: Translations of the official Qt examples into PyQt5 (also PySide2) and more. :octocat:
https://github.com/eyllanesc/QtExamples

QtExamples/official/network/loopback/main.py at master · eyllanesc/QtExamples
https://github.com/eyllanesc/QtExamples/blob/master/official/network/loopback/main.py




"""
# next lets us launch the app from the file
# --------------------
if __name__ == "__main__":
    #----- run the full app
    import main  # noqa  stops auto removal by pycln
# --------------------------------


import wat_inspector
from qtpy.QtCore import QByteArray, Qt, Slot
from qtpy.QtGui import QGuiApplication
from qtpy.QtNetwork import (QAbstractSocket,
                            QHostAddress,
                            QTcpServer,
                            QTcpSocket)
from qtpy.QtWidgets import (QApplication,
                            QDialog,
                            QDialogButtonBox,
                            QHBoxLayout,
                            QLabel,
                            QMenu,
                            QMessageBox,
                            QProgressBar,
                            QPushButton,
                            QVBoxLayout,
                            QWidget)

import tab_base
import utils_for_tabs as uft

# ---- end imports

TOTAL_BYTES  = 50 * 1024 * 1024
PAYLOAD_SIZE = 64 * 1024  # 64 KB



# WAS
# class Dialog( QDialog ):
#     def __init__(self, parent: QWidget = None) -> None:
#         super().__init__(parent)

class TcpWidget( QWidget ):
    def __init__(self, parent: QWidget = None) -> None:
        super().__init__(parent)

        self.tcpServer          = QTcpServer()
        self.tcpClient          = QTcpSocket()
        self.tcpServerConnection: QTcpSocket = None

        self.bytesToWrite       = 0
        self.bytesWritten       = 0
        self.bytesReceived      = 0

        self.clientProgressBar  = QProgressBar()
        self.clientStatusLabel  = QLabel(self.tr("Client ready"))
        self.serverProgressBar  = QProgressBar()
        self.serverStatusLabel  = QLabel(self.tr("Server ready"))

        self.startButton        = QPushButton(self.tr("&Start"))
        self.quitButton         = QPushButton(self.tr("&Quit"))

        self.buttonBox          = QDialogButtonBox()
        self.buttonBox.addButton( self.startButton, QDialogButtonBox.ButtonRole.ActionRole )
        #self.buttonBox.addButton( self.quitButton,  QDialogButtonBox.ButtonRole.RejectRole  )

        self.startButton.clicked.connect(self.start)
        # self.quitButton.clicked.connect(self.close)
        self.tcpServer.newConnection.connect(self.acceptConnection)
        self.tcpClient.connected.connect(self.startTransfer)
        self.tcpClient.bytesWritten.connect(self.updateClientProgress)
        self.tcpClient.errorOccurred.connect(self.displayError)

        mainLayout = QVBoxLayout(self)
        mainLayout.addWidget( self.clientProgressBar )
        mainLayout.addWidget( self.clientStatusLabel )
        mainLayout.addWidget( self.serverProgressBar )
        mainLayout.addWidget( self.serverStatusLabel )
        mainLayout.addStretch( 1 )
        mainLayout.addSpacing( 10 )
        mainLayout.addWidget( self.buttonBox )

    @Slot()
    def start(self):
        self.startButton.setEnabled(False)

        QGuiApplication.setOverrideCursor( Qt.CursorShape.WaitCursor )

        self.bytesWritten = 0
        self.bytesReceived = 0

        while not self.tcpServer.isListening() and not self.tcpServer.listen():
            ret = QMessageBox.critical(
                self,
                self.tr("Loopback"),
                self.tr(
                    "Unable to start the test: %s" % (self.tcpServer.errorString())
                ),
                QMessageBox.StandardButton.Retry | QMessageBox.StandardButton.Cancel,
            )
            if ret == QMessageBox.StandardButton.Cancel:
                return

        self.serverStatusLabel.setText( self.tr("Listening"))
        self.clientStatusLabel.setText( self.tr("Connecting"))
        self.tcpClient.connectToHost(
            QHostAddress(QHostAddress.SpecialAddress.LocalHost),
            self.tcpServer.serverPort(),
        )

    @Slot()
    def acceptConnection(self):
        self.tcpServerConnection = self.tcpServer.nextPendingConnection()
        if not self.tcpServerConnection:
            self.serverStatusLabel.setText(
                self.tr("Error: got invalid pending connection!")
            )
            return

        self.tcpServerConnection.readyRead.connect(self.updateServerProgress)
        self.tcpServerConnection.errorOccurred.connect(self.displayError)
        self.tcpServerConnection.disconnected.connect(
            self.tcpServerConnection.deleteLater
        )

        self.serverStatusLabel.setText(self.tr("Accepted connection"))
        self.tcpServer.close()

    @Slot()
    def startTransfer(self):
        # called when the TCP client connected to the loopback server
        self.bytesToWrite = TOTAL_BYTES - int(
            self.tcpClient.write(QByteArray(PAYLOAD_SIZE, b"@"))
        )
        self.clientStatusLabel.setText(self.tr("Connected"))

    @Slot()
    def updateServerProgress(self):
        self.bytesReceived += int(self.tcpServerConnection.bytesAvailable())
        self.tcpServerConnection.readAll()

        self.serverProgressBar.setMaximum(TOTAL_BYTES)
        self.serverProgressBar.setValue(self.bytesReceived)
        self.serverStatusLabel.setText(
            self.tr("Received %dMB" % (self.bytesReceived / (1024 * 1024),))
        )

        if self.bytesReceived == TOTAL_BYTES:
            self.tcpServerConnection.close()
            self.startButton.setEnabled(True)

            QGuiApplication.restoreOverrideCursor()

    @Slot("qint64")
    def updateClientProgress(self, numBytes):
        self.bytesWritten += int(numBytes)

        if self.bytesToWrite > 0 and self.tcpClient.bytesToWrite() <= 4 * PAYLOAD_SIZE:
            self.bytesToWrite -= self.tcpClient.write(
                QByteArray(min(self.bytesToWrite, PAYLOAD_SIZE), b"@")
            )

        self.clientProgressBar.setMaximum(TOTAL_BYTES)
        self.clientProgressBar.setValue(self.bytesWritten)
        self.clientStatusLabel.setText(
            self.tr("Sent %dMB" % (self.bytesWritten / (1024 * 1024),))
        )

    @Slot(QAbstractSocket.SocketError)
    def displayError(self, socketError):
        if socketError == QAbstractSocket.SocketError.RemoteHostClosedError:
            return

        # this slot serves both sockets, so report the one that actually failed
        socket   = self.sender()
        a_errmsg = socket.errorString() if socket else self.tcpClient.errorString()

        QMessageBox.information(
            self,
            self.tr("Network error"),
            self.tr("The following error occurred: {}.".format(a_errmsg)),
        )
        self.tcpClient.close()
        self.tcpServer.close()
        self.clientProgressBar.reset()
        self.serverProgressBar.reset()
        self.clientStatusLabel.setText(self.tr("Client ready"))
        self.serverStatusLabel.setText(self.tr("Server ready"))
        self.startButton.setEnabled(True)
        QGuiApplication.restoreOverrideCursor()






print_func_header   = uft.print_func_header

#  --------
class QTcpServerTab( tab_base.TabBase ):
    """
    Reference examples for QPushButton

        this is also the place for documentation on the methods normally found
        in a tab_....py file and should comment these naming and other coding conventions.
        Other tab_xxx.py files may not be as well commented for the framework type code,
        you should be familiar with the conventions here and be able to read the code elsewehre.
    """
    def __init__(self):
        """
        set up the tab

        this is pretty much boiler plate for a tab
        """
        super().__init__()
        self.module_file        = __file__      # save for help file usage

        global WIKI_LINK
        self.wiki_link          = WIKI_LINK     # helps the link to the wiki

        # modify to match the number of mutate methods in this module
        self.mutate_dict[0]     = self.mutate_0
        # self.mutate_dict[1]     = self.mutate_1
        # self.mutate_dict[2]     = self.mutate_2
        # self.mutate_dict[3]     = self.mutate_3
        # self.mutate_dict[4]     = self.mutate_4

        self._build_gui()

    #--------------------------
    def _build_gui_widgets( self, main_layout ):
        """
        the usual, build the gui with the widgets of interest

        main_layout will be a QVBoxLayout
        this just does a basic build -- the framework will then automatically
        call mutate_0()

        This code is important content for the widgets referenced on this tab

        """
        layout              = QHBoxLayout()
        main_layout.addLayout( layout )

        # too clever ??
        main_layout.addLayout( layout := QVBoxLayout() )

        # # ---- new row c -- testing never used
        # row_layout          = QHBoxLayout(   )
        # layout.addLayout( row_layout )

        # ---- New Row button_1 and _2 ....
        # make a layout to put the buttons in
        row_layout          = QHBoxLayout(   )
        layout.addLayout( row_layout )

        # # a label that points to q_pbutton_1
        # widget          = QLabel( "q_pbutton_1 -> ", alignment=Qt.AlignRight )
        #     # no instance variable as we will not use after __init__

        # # layout ( add to the windows ) the widget
        # row_layout.addWidget( widget )

        # # we use a local variable, widget, because it reduces the amount of code
        #     # and does not run any slower
        #     # we use this local variable idea in many places
        #     # if we need an instance variable we do an assignment as here
        # widget                  = QPushButton( "q_pbutton_1" )
        # self.q_push_button_1    = widget
        #     # save a reference for later use

        # # this function, the "connect_to" will be called when the button is clicked
        # # the code is a little indirect, do on one line if you wish
        # connect_to              = self.pb_1_clicked
        # widget.clicked.connect( connect_to )
        # row_layout.addWidget( widget )

        # widget                  = QLabel( "q_pbutton_2 -> ", alignment=Qt.AlignRight )
        # row_layout.addWidget( widget )

        # widget                  = QPushButton( "q_pbutton_2" )
        # self.q_push_button_2    = widget
        # connect_to              = self.pb_2_clicked
        # widget.clicked.connect( connect_to )
        # row_layout.addWidget( widget, )

        widget                  = TcpWidget()
        row_layout.addWidget( widget, )


        # ---- new row, for build_gui_last_buttons
        button_layout           = QHBoxLayout(   )
        layout.addLayout( button_layout, )


        # our ancestor finishes off the tab with some
        # standard buttons
        self.build_gui_last_buttons( button_layout )

    #----------------------------
    def get_button_style_sheetxxx( self ):
        """
        what it says

        when applied to a button changes a bit of its appearance

        this is important content for the widgets referenced on this tab
        """
        return """
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: 2px solid #4CAF50;
                border-radius: 8px;
                padding: 8px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #3e8e41;
            }
        """
        # i do not know what the default state, perhaps wat_inspector can tell

    # ------------------------------------
    def signal_sent( self, msg ):
        """
        when a signal is sent, use find ???

        this is important content for the widgets referenced on this tab
        """
        self.append_msg( "signal_sent()" )
        # msg   = f"{function_nl}signal_sent"
        # print( msg )
        self.append_msg( f"signal_sent {msg}" )

        self.append_msg( tab_base.DONE_MSG )

    # ---- connects signals...   --------
    # --------------------------
    def return_pressedxxx( self ):
        """
        what is says  -- not connected, delete?

        this is important content for the widgets referenced on this tab
        """
        self.append_msg( "return_pressed()" )

        self.append_msg( tab_base.DONE_MSG )


    # ------------------------------------
    def mutate_0( self ):
        """
        read it -- mutate the widgets
            these mutations will try to mimic a typical default state
            of a widget for the first push button the
            second will not be modified by mutate_0

        this is important content for the widgets referenced on this tab
        read the code for more insight, note messages to app and comments
        """
        self.append_function_msg( "mutate_0()" )

        # ---- change widget
        msg    = "this example has no instructive mutations"
        self.append_msg( msg, clear = False )
            # we use a local variable because it reduces the amount of code
            # and does not run any slower
            # we use this local variable idea in many places
        # widget          = self.q_push_button_1
        # widget.setText( "text set in mutate_0()" )
        # widget.width    = 300
        # widget.setToolTip( None )
        # widget.setStyleSheet( "" )

        self.append_msg( tab_base.DONE_MSG )



    # ------------------------
    def inspect(self):
        """
        the usual

        Allows the user to inspect local and global variables using
        the wat_inspector

        this is pretty much boiler plate for a tab
        """
        self.append_function_msg( tab_base.INSPECT_MSG )

        # we set local variables to make it handy to inspect them
        # self_q_push_button_1    = self.q_push_button_1
        # self_q_push_button_2    = self.q_push_button_1

        wat_inspector.go(
             msg            = "for your inspection, some locals and globals",
             a_locals       = locals(),
             a_globals      = globals(), )

        self.append_msg( tab_base.DONE_MSG )

    # ------------------------
    def breakpoint(self):
        """
        each tab gets its own function so we break in that
        tab's code

        this is pretty much boiler plate for a tab
        """
        self.append_function_msg( tab_base.BREAK_MSG )

        breakpoint()

        self.append_msg( tab_base.DONE_MSG )

# ---- eof
