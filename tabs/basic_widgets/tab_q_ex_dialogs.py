#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ---- tof
"""
# metadata here including WIKI_LINK as Constant ( not comment )
# this material is used for selection access to the tab module which must
# be named tab_....py     among other things

KEY_WORDS:      dialog questionBox  Message Box custom
CLASS_NAME:     QDialogsTab
WIDGETS:        QMessageBox QDialog
STATUS:         2025 dec draft
TAB_TITLE:      QDialogsTab / Various
DESCRIPTION:    A few examples of dialogs simple to custom
HOW_COMPLETE:   20  #  AND A COMMENT -- <10 major probs  <15 runs but <20 fair not finished  <=25 not to shabby
"""
WIKI_LINK      =  "https://github.com/russ-hensel/pyqt_by_example/wiki/What-We-Know-About-Misc-Dialogs"


# --------------------
if __name__ == "__main__":
    #----- run the full app
    import main  # noqa  stops auto removal by pycln
# --------------------------------

# ---- imports

from qtpy.QtWidgets import QPushButton, QVBoxLayout
from qtpy.QtWidgets import ( QHBoxLayout,
                             QCheckBox,
                             QLabel,
                             QLineEdit,
                             QMessageBox,
                             QPushButton,
                             QVBoxLayout )

#import parameters

import utils_for_tabs as uft
import wat_inspector
import tab_base

# ---- end imports

print_func_header   = uft.print_func_header


from qtpy.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QLineEdit

# ---- return codes
# 0 and 1 are what QDialog itself uses for reject and accept, so keeping
# them here means Esc and the window X land on RESULT_CANCEL for free.
# Add your own starting at 2.

RESULT_CANCEL   = 0
RESULT_OK       = 1
RESULT_SKIP     = 2


# ------------------------------------
def ask_user( parent = None, title = "Custom Dialog",
              a_name = "", a_note = "", wants_email = False ):
    """
    build, show and read the dialog in one call
    returns ( result_code, values dict )
    """
    dialog      = ClaudeCustomDialog( parent,
                                title       = title,
                                a_name      = a_name,
                                a_note      = a_note,
                                wants_email = wants_email )

    dialog.exec()       # blocks here until a button closes it
                        # exec() not exec_(), exec_ is gone in PyQt6

    result_code = dialog.result_code
    values      = dialog.get_values()

    return ( result_code, values )



#  --------
class ClaudeCustomDialog( QDialog ):
    """
    vibe coded with light editing
    this is how claude responds
    a modal dialog that returns one of the RESULT_* codes above
    """

    # -----------------------
    def __init__( self, parent = None, title = "Custom Dialog",
                  a_name = "", a_note = "", wants_email = False ):
        """
        build the dialog, the a_* arguments are the starting values
        shown in the fields
        """
        super().__init__( parent )

        self.setWindowTitle( title )
        self.setModal( True )

        self.start_name     = a_name
        self.start_note     = a_note
        self.start_email    = wants_email

        self.result_code    = RESULT_CANCEL   # until a button says otherwise

        self._build_gui()

    # -----------------------
    def _build_gui( self ):
        """
        the whole layout, in the same shape as a tab: widgets then buttons
        """
        layout      = QVBoxLayout( self )

        self._build_gui_widgets( layout )
        self._build_gui_msg(     layout )
        self._build_gui_buttons( layout )

        self.setMinimumWidth( 400 )

    # -----------------------
    def _build_gui_widgets( self, layout ):
        """
        the fields, replace these with your own
        """
        # ---- name
        row_layout      = QHBoxLayout()
        layout.addLayout( row_layout )

        widget          = QLabel( "name  " )
        row_layout.addWidget( widget )

        widget          = QLineEdit( self.start_name )
        self.name_edit  = widget
        widget.setMinimumWidth( 250 )
        row_layout.addWidget( widget )

        # ---- note
        row_layout      = QHBoxLayout()
        layout.addLayout( row_layout )

        widget          = QLabel( "note  " )
        row_layout.addWidget( widget )

        widget          = QLineEdit( self.start_note )
        self.note_edit  = widget
        widget.setMinimumWidth( 250 )
        row_layout.addWidget( widget )

        # ---- check box
        row_layout  = QHBoxLayout()
        layout.addLayout( row_layout )

        widget          = QCheckBox( "wants email" )
        self.email_check    = widget
        widget.setChecked( self.start_email )
        row_layout.addWidget( widget )

    # -----------------------
    def _build_gui_msg( self, layout ):
        """
        the line validate() writes its complaint on, empty most of the time
        """
        widget          = QLabel( "" )
        self.msg_widget = widget
        widget.setWordWrap( True )
        widget.setStyleSheet( "color: red;" )
        layout.addWidget( widget )

    # -----------------------
    def _build_gui_buttons( self, layout ):
        """
        plain push buttons, one method each, add your own here
        """
        row_layout  = QHBoxLayout()
        layout.addLayout( row_layout )

        row_layout.addStretch( 1 )      # push the buttons to the right

        widget          = QPushButton( "ok" )
        self.ok_button  = widget
        widget.setDefault( True )       # the return key presses this one
        widget.clicked.connect( self.on_ok )
        row_layout.addWidget( widget )

        widget      = QPushButton( "skip" )
        widget.clicked.connect( self.on_skip )
        row_layout.addWidget( widget )

        widget      = QPushButton( "cancel" )
        widget.clicked.connect( self.on_cancel )
        row_layout.addWidget( widget )

    # ---- what the buttons do

    # -----------------------
    def on_ok( self ):
        """
        validate first, a complaint keeps the dialog open
        """
        complaint   = self.validate()

        if complaint != "":
            self.msg_widget.setText( complaint )
            return

        self.finish( RESULT_OK )

    # -----------------------
    def on_skip( self ):
        """
        close with the skip code, no validation
        """
        self.finish( RESULT_SKIP )

    # -----------------------
    def on_cancel( self ):
        """
        close with the cancel code, no validation
        """
        self.finish( RESULT_CANCEL )

    # -----------------------
    def finish( self, result_code ):
        """
        remember the code and close, done() is what ends exec()
        """
        self.result_code    = result_code
        self.done( result_code )

    # -----------------------
    def validate( self ):
        """
        what counts as a good answer, return "" for good or the
        complaint to show the user
        """
        a_name      = self.name_edit.text().strip()

        if a_name == "":
            return ( "name cannot be empty" )

        return ( "" )

    # ---- reading the answer

    # -----------------------
    def get_values( self ):
        """
        the fields as a dict, valid whatever button was pressed
        """
        values      = { "name"          : self.name_edit.text().strip(),
                        "note"          : self.note_edit.text().strip(),
                        "wants_email"   : self.email_check.isChecked(), }

        return values

    # -----------------------
    def reject( self ):
        """
        Esc and the window X come here, not through a button, so make
        them mean cancel rather than leaving result_code stale
        """
        self.result_code    = RESULT_CANCEL
        super().reject()

#-----------------------------
class ExQDialog( QDialog ):
    """
    An example dialog from chat then edited """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUI()

    #-----------------------------
    def setupUI(self):
        # Set the dialog title
        self.setWindowTitle("My Custom Dialog")

        # Explicitly set the size (width, height)
        self.resize(400, 250)

        # Optional: Set minimum and maximum sizes
        self.setMinimumSize(300, 200)
        self.setMaximumSize(600, 400)

        # Create layout
        layout = QVBoxLayout()

        # Add some widgets
        label               = QLabel("Enter your name:")
        self.name_input     = QLineEdit()

        # Add buttons
        ok_button           = QPushButton("OK")
        cancel_button       = QPushButton("Cancel")

        # Connect buttons
        ok_button.clicked.connect(self.accept)
        cancel_button.clicked.connect(self.reject)

        # Add widgets to layout
        layout.addWidget(label)
        layout.addWidget(self.name_input)
        layout.addWidget(ok_button)
        layout.addWidget(cancel_button)

        # Set the layout
        self.setLayout(layout)

    #-----------------------------
    def get_name(self):
        """Return the entered name"""
        return self.name_input.text()


#-----------------------------
class QDialogsTab( tab_base.TabBase ):
    """
    Reference examples for QFileDialogTab and
    """
    def __init__(self):
        """
        set up the tab

        this is pretty much boiler plate for a tab
        """
        super().__init__()
        self.module_file            = __file__      # save for help file usage

        global WIKI_LINK
        self.wiki_link              = WIKI_LINK

        # modify to match the number of mutate methods in this module
        self.mutate_dict[0]         = self.mutate_0
        #self.mutate_dict[1]         = self.mutate_1
        self.current_default_dir    = "~"       # change as dilog used -- seems not to work
        self.current_default_dir    = "../"     # seems to work "

        self._build_gui()

    #---------------------------
    def _build_gui_widgets( self, main_layout ):
        """
        the usual, build the gui with the widgets of interest

        main_layout will be a QVBoxLayout
        this just does a basic build -- the framework will then automatically
        call mutate_0()

        this is important content for the widgets referenced on this tab

        """
        layout              = QHBoxLayout()
        main_layout.addLayout( layout )

        # too clever ??
        main_layout.addLayout( layout := QVBoxLayout() )

        # ---- new row
        row_layout          = QHBoxLayout(   )
        layout.addLayout( row_layout )

        # ---- New Row buttons
        # make a layout to put the buttons in
        row_layout          = QHBoxLayout(   )
        layout.addLayout( row_layout )

        # we use a local variable because it reduces the amount of code
        # and does not run any slower
        # we use this local variable idea in many places
        # because we will refer to the bu
        widget              = QPushButton( "open_message_box" )
        connect_to          = self.open_message_box
        widget.clicked.connect( connect_to )
        row_layout.addWidget( widget )

        widget              = QPushButton( "open_ex_qdialog" )
        connect_to          = self.open_ex_qdialog
        widget.clicked.connect( connect_to    )
        row_layout.addWidget( widget,  )

        widget              = QPushButton( "open_claude_custom_dialog" )
        connect_to          = self.open_claude_custom_dialog
        widget.clicked.connect( connect_to )
        row_layout.addWidget( widget,  )

        # ---- new row, for build_gui_last_buttons
        button_layout = QHBoxLayout( )
        layout.addLayout( button_layout, )

        # our ancestor finishes off the tab with some
        # standard buttons
        self.build_gui_last_buttons( button_layout )

    # ------------------------------------
    def open_ex_qdialog( self ):
        """
        What it says

        """
        dialog = ExQDialog()

        if dialog.exec_() == QDialog.Accepted:
            name = dialog.get_name()
            msg     = (f"Name entered: {name}")
            self.append_msg( msg )

        else:
            msg     = ("Dialog cancelled")
            self.append_msg( msg )


    # ------------------------------------
    def open_claude_custom_dialog( self ):
        """
        What it says

        """
        result_code, values = ask_user( a_name  = "start value",
                                        a_note  = "edit me" )

        msg     = ( f"{result_code = }" )
        self.append_msg( msg )

        msg     = ( f"{values      = }" )
        self.append_msg( msg )

    # ------------------------------------
    def open_message_box( self ):
        """
        What it says
            add some returns
        """
        msg_box_msg     = "this is a message"
        msg_box         = QMessageBox()
        msg_box.setIcon( QMessageBox.Information )
        msg_box.setText(  msg_box_msg  )
        msg_box.setWindowTitle( "Sorry that is a No Go " )
        msg_box.setStandardButtons( QMessageBox.Ok )

        ret             = msg_box.exec_()
        msg             =( f"{ret = }" )
        self.append_msg( msg )

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

        msg    = ( "mutates not a feature of this tab")
        self.append_msg( msg )

        self.append_msg( tab_base.DONE_MSG )

    # ------------------------------------
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
