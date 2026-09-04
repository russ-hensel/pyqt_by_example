#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ---- tof



"""

KEY_WORDS:      Radio Button Reference
CLASS_NAME:     QRadioButtonTab
WIDGETS:        QRadioButton QButtonGroup QGroupBox
STATUS:         works ??
TAB_TITLE:      QRadioButton / Reference
DESCRIPTION:    Reference for QRadioButton
HOW_COMPLETE:   10  #  AND A COMMENT

"""
WIKI_LINK      =  "https://github.com/russ-hensel/pyqt_by_example/wiki/Documentation-Not-Written"

# --------------------
if __name__ == "__main__":
    #----- run the full app
    pass
    #main.main()
# --------------------------------


# sql
# widgets biger
# widgets -- small
# layouts
from qtpy.QtWidgets import (
                             QHBoxLayout,
                             QGroupBox,
                             QButtonGroup,
                             QLabel,
                             QRadioButton,
                             QVBoxLayout)

#import parameters

import utils_for_tabs as uft
import wat_inspector
import tab_base

# ---- end imports

print_func_header   = uft.print_func_header

#  --------
class QRadioButtonTab(  tab_base.TabBase  ):
    def __init__(self):
        """
        some content from and there may be more
        /mnt/WIN_D/Russ/0000/python00/python3/_projects/rshlib/gui_qt_ext.py
        tab_misc_widgets.py
        """
        super().__init__()

        self.module_file        = __file__      # save for help file usage
        self.help_file_name     =  "misc_widget_tab.txt"

        global WIKI_LINK
        self.wiki_link          = WIKI_LINK

        self.mutate_dict[0]    = self.mutate_0
        self.mutate_dict[1]    = self.mutate_1
        # self.mutate_dict[2]    = self.mutate_2
        # self.mutate_dict[3]    = self.mutate_3
        # self.mutate_dict[4]    = self.mutate_4
        self._build_gui()

    def _build_gui_widgets(self, main_layout  ):
        """
        the usual, build the gui with the widgets of interest
        and the buttons for examples
        """
        layout              = QVBoxLayout(   )

        main_layout.addLayout( layout )
        button_layout        = QHBoxLayout(   )


        # ---- new row
        row_layout          = QHBoxLayout(   )
        layout.addLayout( row_layout )


        widget          = QLabel("radio_buttons 1-3 -> ")
        row_layout.addWidget( widget )

        widget        = QRadioButton("rb_1")
        self.rb_1     = widget
        row_layout.addWidget( widget )

        widget        = QRadioButton("rb_2")
        self.rb_2     = widget
        row_layout.addWidget( widget )

        widget        = QRadioButton("rb_3")
        self.rb_3    = widget
        row_layout.addWidget( widget )

        row_layout.addStretch( 1 )

        # ---- new Row
        row_layout          = QHBoxLayout(   )
        layout.addLayout( row_layout )


        group           = QButtonGroup( self )          # parent keeps it alive
        self.rb_group   = group
        small           = QRadioButton("Small")
        medium          = QRadioButton("Medium")
        large           = QRadioButton("Large")

        group.addButton( small,  1 )          # (button, id)
        group.addButton( medium, 2 )
        group.addButton( large,  3 )
        small.setChecked( True )              # set a default

        #layout = QVBoxLayout(self)
        for b in (small, medium, large):
            row_layout.addWidget( b )

        self.build_rb_in_groupbox( row_layout )

        # widget = QPushButton("clear_\nvalues")
        # a_widget        = widget
        # widget.clicked.connect(  self.clear_values  )
        # button_layout.addWidget( widget )

        # widget = QPushButton("set_values\n")
        # widget.clicked.connect( lambda: self.set_values( ) )
        # button_layout.addWidget( widget )

        # widget = QPushButton("clip\n")
        # widget.clicked.connect( lambda: self.clip( ) )
        # button_layout.addWidget( widget )

        # ---- new row, standard buttons
        button_layout = QHBoxLayout(   )
        layout.addLayout( button_layout,  )

        self.build_gui_last_buttons( button_layout )

    # ---------------------------
    def build_rb_in_groupbox( self, layout ):
        """
        this is a bit of gui built inside another groupbos = QGroupBox()
        """
        # ---- QGroupBox
        groupbox   = QGroupBox( "QGroupBox 1" )   # version with title

        groupbox.setStyleSheet("""
            QGroupBox {
                border: 2px solid blue;
                border-radius: 10px;
                margin-top: 15px;
            }

            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top center;
                padding: 0 3px;
                background-color: white;
            }
        """)

        # layout the groupbox and make
        # another layout inside it

        layout.addWidget( groupbox )
        layout_g     = QHBoxLayout( groupbox  )

        widget        = QRadioButton("rb_1g")

        layout_g.addWidget( widget )

        widget        = QRadioButton("rb_2g")
        #self.rb_2     = widget
        layout_g.addWidget( widget )

        widget        = QRadioButton("rb_3g")
        #self.rb_3    = widget
        layout_g.addWidget( widget )


    # ------------------------------------
    def signal_sent( self, msg ):
        """
        when a signal is sent, use find
        """
        self.append_function_msg( "signal_sent" )
        # msg   = f"{function_nl}signal_sent"
        # print( msg )
        self.append_msg(  f"signal_sent {msg}" )

        self.append_msg( "<<-- done" )



    # ------------------------------------
    def clear_values( self ):
        """
        There is much more info to show
        """

    # ------------------------------------
    def set_values( self ):
        """
        What it says
        """
        self.append_function_msg( "set_values" )

        self.append_msg(  "set_values  self.line_edit_1 " )  # setText()   ??
        self.line_edit_1.setText( "xxxxx" )
        # print( f"{self.little_widget_line_edit_1.isEnabled() = }" )  # setEnabled()
        # print( f"{self.little_widget_qlabel_1.text() = }" )  # setText() ??
        self.append_msg( "<<-- done" )




    # ------------------------------------
    def mutate_0( self ):
        """
        read it -- mutate the widgets
        """
        self.append_function_msg( "mutate_0" )

        msg    = "currently a pass, try mutate_..."
        self.append_msg( msg, clear = False )

        self.append_msg( tab_base.DONE_MSG )

    # ------------------------------------
    def mutate_1( self ):
        """
        read it -- mutate the widgets
        """
        self.append_function_msg( "mutate_1" )

        msg    = "so far not implemented "
        self.append_msg( msg, clear = False )

        group      = self.rb_group
        # group.checkedId()        # -> 2   (the id, or -1 if none checked)
        # group.checkedButton()    # -> the QRadioButton object (or None)
        # group.checkedButton().text()   # -> "Medium"

        self.append_msg( f"{group.checkedId() = }" )

        self.append_msg( f"{group.checkedButton() = }" )
        self.append_msg( f"{group.checkedButton().text() = }" )

        self.append_msg( "<<-- done" )


    # ---- signals sent -----------------------
    # --------------------------
    def on_editing_finished(self):
        """
        what is says
        """
        self.append_function_msg( "on_editing_finished" )

        self.append_msg( "<<-- done" )

    # --------------------------
    def return_pressed( self ):
        """
        what is says
        """
        self.append_function_msg( "return_pressed" )

        self.append_msg( "<<-- done" )



    # ------------------------
    def show_values(self):
        """
        the usual sort of thing, just read it
        """
        self.append_function_msg( "inspect" )

        # self.append_msg( f"{self.qwidget_1 = }")
        # #print( f"{self.qwidget_1 = }")

        # self.append_msg( f"{self.line_edit_1.text() = }" )  # setText()   ??
        # self.append_msg( f"{self.line_edit_1.isEnabled() = }" )  # setEnabled() no focus
        # self.append_msg( f"{self.line_edit_1.isReadOnly() = }" )

        # self.append_msg( f"{self.qlabel_1.text() = }" )  # setText() ??
        # self.append_msg( f"{self.qlabel_2.text() = }" )

        # self.append_msg( f"{str(self.cbox_1.isChecked()) = }" )

        self.append_msg( "<<-- done" )

    # ------------------------
    def inspect(self):
        """
        the usual
        """
        self.append_function_msg( "inspect" )

        # !! add pushbuttons here

        #my_tab_widget = self
        #parent_window = self.parent( ).parent( ).parent().parent()

        wat_inspector.go(
             msg            = "tbd add more locals",
             a_locals       = locals(),
             a_globals      = globals(), )

        self.append_msg( "<<-- done" )

    # ------------------------
    def breakpoint(self):
        """
        each tab gets its own function so we break in that
        tabs code
        """
        self.append_function_msg( "breakpoint" )

        breakpoint()

        self.append_msg( tab_base.DONE_MSG )

# ---- eof
