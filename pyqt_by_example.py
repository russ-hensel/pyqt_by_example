
# ---- tof
"""

an app that demonstrates the uses
of qt5 in python
see the wiki at

Home · russ-hensel/pyqt_by_example Wiki
https://github.com/russ-hensel/pyqt_by_example/wiki


"""

# --------------------
if __name__ == "__main__":
    #----- run the full app
    import main   # noqa  stops auto removal by pycln
# --------------------


# ---- imports
import logging
import psutil

import os
import sys

import functools
import subprocess
#import sys
from functools import partial
#from platform import python_version
#from subprocess import PIPE, STDOUT, Popen, run

#from app_global import AppGlobal
from qtpy import QtGui
from qtpy.QtCore import (QDate,
                          QModelIndex,
                          QSize,
                          QSortFilterProxyModel,
                          Qt,
                          QTimer)
# sql
from qtpy.QtSql import (QSqlDatabase,
                         QSqlField,
                         QSqlQuery,
                         QSqlQueryModel,
                         QSqlRecord,

                         QSqlRelationalDelegate,
                         QSqlRelationalTableModel,
                         QSqlTableModel)

from qtpy.QtWidgets import (QAbstractItemView,
                             QAction,
                             QApplication,
                             QButtonGroup,
                             QCheckBox,
                             QComboBox,
                             QDataWidgetMapper,
                             QDateEdit,
                             QDialog,
                             QDoubleSpinBox,
                             QFormLayout,
                             QGridLayout,
                             QGroupBox,
                             QHBoxLayout,
                             QHeaderView,
                             QLabel,
                             QLineEdit,
                             QListWidget,
                             QListWidgetItem,
                             QMainWindow,
                             QMenu,
                             QMessageBox,
                             QPushButton,
                             QRadioButton,
                             QSpinBox,
                             QStyledItemDelegate,
                             QTableView,
                             QTableWidget,
                             QTableWidgetItem,
                             QTabWidget,
                             QTextEdit,
                             QVBoxLayout,
                             QWidget)

#  ---- local imports
#import adjust_path
import app_services
import global_vars
import index_and_search
import parameters

import tab_qsql_database
import tab_select_tab

import utils_for_tabs as uft
import wat_inspector
import show_parameters
import tab_base
import tab_re_base
from   app_global import AppGlobal
# import app_logging    # /mnt/WIN_D/russ/0000/python00/python3/_projects/rshlib/app_services/app_logging.py
import app_logging    # /mnt/WIN_D/russ/0000/python00/python3/_projects/rshlib/app_services/app_logging.py


#logger   = logging.getLogger()

# ---- end imports

INDENT          = uft.INDENT
BEGIN_MARK_1    = uft.BEGIN_MARK_2
BEGIN_MARK_2    = uft.BEGIN_MARK_2

print_func_header  = uft.print_func_header

__VERSION__  = "ver_001 - 2026 02 04.01"

# ---- main window ===================================================================
class PyqtByExample( QMainWindow ):
    def __init__(self):
        """
        the usual
        """
        super().__init__()

        global_vars.set_controller( self )  # import global_vars

        my_parameters       = parameters.Parameters()
        self.parameters     = my_parameters
        uft.parameters      = my_parameters
        #my_parameters.PARAMETERS = my_parameters
        AppGlobal.parameters  = my_parameters

        # kluge untill better fix

        uft.main_window     = self

        qt_xpos             = my_parameters.qt_xpos
        qt_ypos             = my_parameters.qt_ypos
        qt_width            = my_parameters.qt_width
        qt_height           = my_parameters.qt_height

        # ---- tweak the path
        for i_path in my_parameters.dir_for_tabs:
            unsafe   = f'sys.path.insert( 1, "{i_path}" ) '
            #rint( unsafe )
            eval( unsafe, globals(), locals()  )

        uft.TEXT_EDITOR     = my_parameters.text_editor

        global DB_FILE
        DB_FILE             = my_parameters.db_file_name


        app_logging.init()

        # next builds and populates the db, or may depending on refactor
        self.index_search    =  index_and_search.IndexSearch()

        self.tab_dict        = {}    # key class name, contents for now just index
                                     # {'QSqlDatabaseTab': 1, 'Dock_10_Tab': 2, 'Fitz_22_Tab': 2}
                                     # but index is unstable
        self.tab_help_dict   = {}
        self.setGeometry(  qt_xpos,
                           qt_ypos ,
                           qt_width,
                           qt_height  )

        self.doc_dir             = my_parameters.help_path

        self.build_gui()

        self.current_tab_index   = 0   # I need to track in changed
        self.tab_widget.setCurrentIndex( 0 )

        # ---- breakpoint -- not overrid of sys.argv
        # argv not gettin passed in reliably put in parameters for now
        # if sys.argv[1] = "breakpoint_ok"
        # self.breakpoint_ok
        if len( sys.argv ) > 1:
            self.breakpoint_ok = sys.argv[1] ==  "breakpoint_ok"
        else:
            self.breakpoint_ok = False

        self.breakpoint_ok = parameters.PARAMETERS.breakpoint_ok

        if parameters.PARAMETERS.do_search_on_init:
            self.search_tab.criteria_select()

    # ------------------
    def build_gui( self ):
        """
        main gui build method -- for some sub layout use other methods
        """
        self.setWindowTitle( f"PyqtByExample  {__VERSION__}" )
        self.build_menu( )

        icon    = QtGui.QIcon(  "./misc/broom_edit_2.png"  )
        #/  !! move to parameters
        self.setWindowIcon(icon)

        central_widget          = QWidget()
        self.setCentralWidget(central_widget)

        central_widget_layout   =  QVBoxLayout( central_widget )

        # --- out main layout
        layout          = QVBoxLayout(   )
        central_widget_layout.addLayout( layout )

        # ---- Create tabs
        self.tab_widget = QTabWidget()   # really the folder for the tabs
                                         # tabs themselves are just Widgets
        # there is another approach using a style sheet acording to chat
        self.tab_widget.setTabsClosable(True)
        self.tab_widget.tabCloseRequested.connect( self.close_tab )
        # Set custom height for the tabs
        self.tab_widget.setStyleSheet("QTabBar::tab { height: 60px; }")

        self.tab_widget.currentChanged.connect( self.on_tab_changed )
        self.tab_widget.tabBarClicked.connect(  self.on_tab_clicked )

        # self.tab_widget.tabCloseRequested.connect( self.on_tab_close_requested )
        # self.tab_widget.setTabsClosable( False )
            # Allows you to enable or disable the close button on tabs.
        self.tab_widget.setMovable( True )
            # what it says

        layout.addWidget( self.tab_widget   )

        title                   = "Select\nTab"
        tab                     = tab_select_tab.Search_Tab()
        self.search_tab         = tab
        self.tab_widget.addTab( tab, title  )
        self.tab_help_dict[ title ] = "select_tab.txt"

        #self.open_tab_select( "tab_base", "TabBase", "TabBase the base tab", widgets = "" )
        self.open_tab_select( "tab_qsql_database", "QSqlDatabaseTab", "QSqlDatabase / QSqlQuery", "web_link", widgets = ""  )
        #open_tab_select( self, module_name, class_name, title  ):

        button_layout = QHBoxLayout(   )
        central_widget_layout.addLayout( button_layout )

    # ------------------------
    def switch_to_tab_by_class_name( self, class_name,   ):
        """
        do action

        return tab index or -1
        tab_dict will not work as index is not stable
        """
        tab_index   = -1
        #print( f"looking for {class_name} = " )
        tab            =  self.tab_widget
        for ix_tab in range( tab.count() ):
            tab_page       = tab.widget( ix_tab )
            full_type      = type( tab_page )
            i_class_name   = full_type.__name__

            #rint( f"found for {class_name =}   " )
            if class_name == i_class_name:
                tab_index   = ix_tab
                break

        if tab_index >= 0:
            self.tab_widget.setCurrentIndex( tab_index )

        return tab_index

    # ------------------------
    def open_tab_select( self, module_name, class_name, title, web_link,  widgets  ):
        """
        open_tab_select( self, module_name, class_name, title,  web_link, widgets = widgets  ) ):
        widget          = self.selected_widget
        row             = widget.row( item )
        qt5_by_example.open_tab_select( )
        text            = item.text()
        """
        tab             = app_services.create_instance( module_name, class_name, )

        tab_index       = self.tab_widget.indexOf( tab  )

        title           = title.replace( r" / ", "\n" )

        self.tab_widget.addTab( tab, title  )
        tab_index       = self.tab_widget.indexOf( tab  )
        self.tab_widget.setCurrentIndex( tab_index )
        self.tab_dict[  class_name  ]  = tab_index    # depricate i think
        #breakpoint()
        # very messy, web links could just be in class this
        # is nonsense
        if   isinstance( tab, tab_base.TabBase ):
            #rint( f"yes widgets ==================={widgets}" )
            msg       = f"Widget of interest >> {widgets}"
            tab.class_widget.setText( msg )

            #tab.set_web_link( web_link )

        elif isinstance( tab, tab_re_base.TabReBase ):
            # need to poatpone for ReBase
            msg       = f"Widget of interest >> {widgets}"
            tab.class_widget_text =   msg

    # ------------------------------------
    def build_menu( self,  ):
        """
        what it says:
        """
        menubar         = self.menuBar()
        self.menubar    = menubar
        # ---- Configuration
        a_menu          = menubar.addMenu("Configuration")

        open_action     = QAction( "Open Log", self )
        connect_to      = functools.partial( self.open_txt_file,
                                              parameters.PARAMETERS.pylogging_fn  )
        open_action.triggered.connect( connect_to )
        a_menu.addAction( open_action )

        #---------------
        open_action     = QAction( "Show Parameters", self )
        connect_to      = self.show_parameters
        open_action.triggered.connect( connect_to )
        a_menu.addAction( open_action )

        #---------------
        open_action     = QAction( "Open Parameters", self )
        connect_to      = partial( self.open_txt_file, "./parameters.py" )
        open_action.triggered.connect( connect_to )
        a_menu.addAction( open_action )

        # ----
        action          = QAction( "Add to Log", self )
        connect_to      = app_logging.add_to_log
        action.triggered.connect( connect_to )
        a_menu.addAction(  action )

        a_menu.addSeparator()

        # ---- Help
        menu_help       = menubar.addMenu( "Help/Notes" )

        action          = QAction( "README.md...", self )
        connect_to      = partial( self.open_txt_file, "README.md" )
        action.triggered.connect( connect_to )
        menu_help.addAction( action )

        action          = QAction( "General Notes/Help...", self )
        connect_to      = partial( self.open_txt_file, "./misc/general_help.txt" )
        action.triggered.connect( connect_to )
        menu_help.addAction( action )

        action          = QAction( "Current Tab Notes...", self )
        connect_to      = self.open_tab_help
        action.triggered.connect( connect_to )
        menu_help.addAction( action )

        action          = QAction( "Developer Notes...", self )
        connect_to      = partial( self.open_txt_file, "readme_rsh.txt" )
        action.triggered.connect( connect_to )
        menu_help.addAction( action )

        about_action1 = QAction( "About...", self )
        about_action1.triggered.connect( self.show_about_box )
        menu_help.addAction( about_action1 )   # action is added directly to menu

    #----------------------------
    def close_tab( self, index  ):
        """
        what it says read:

        but moving around causes index change
        do not close needed tabs
        """
        tab         = self.tab_widget
        widget      = tab.widget(index)
        text        = tab.tabText(index)
        tooltip     = tab.tabToolTip(index)
        icon        = tab.tabIcon(index)

        if ( isinstance( widget,  tab_select_tab.Search_Tab ) or
             isinstance( widget,  tab_qsql_database.QSqlDatabaseTab )
            ):
            print(f"Tab {index} {type( widget )=} cannot be closed because it is key to the operation of this app")
            return

        # if index in [0, 1]:  # Allow closing the first tab
        #     print(f"Tab {index} cannot be closed.")
        else:
            #rint(f"Tab {index} will be closed.")
            self.tab_widget.removeTab(index)

    #----------------------------
    def not_implemented( self,   ):
        """
        what it says read:
        """
        QMessageBox.information(self, "Not Implemented", "Working on this...")

    #-------
    def open_general_help( self,   ):
        """
        what it says read:
        """
        doc_name            = f"{self.doc_dir}qt_widgets_help.txt"
        ex_editor           = r"xed"
        proc                = subprocess.Popen( [ ex_editor, doc_name ] )

    # ---- events ------------------------------------------
    #----------------------------
    def on_tab_changed(self, index):
        """
        what it says, read it
        """
        #rint(f"on_tab_changed from { self.current_tab_index = } to {index = }")
        # !! THINK the widge does this itself
        self.current_tab_index   = index
        self.tab_page_info()

    # #----------------------------
    # def on_tab_close_requested( self, index):
    #     self.tab_widget.removeTab(index)

    #----------------------------
    def on_tab_clicked(self, index):
        """ """
        return    # return to silence
        #rint(f"Tab {index} clicked.")

    #----------------------------
    def tab_page_info( self ):
        """
        what it says, read it
        """
        return    # return to silence
        # nb    = self.tab_widget
        # print(f"nb.select()  >>{nb.currentIndex() = }<<")
        # print(f'>>{nb.tabText(nb.currentIndex()) = }<<')
        # # print(f'{ nb.index("current" ) = }' )

    # ----
    def iconify( self ):
        """
        what it says
        """
        self.showMinimized()

    #-------
    def open_tab_help( self,   ):
        """
        what it says read:
        """
        current_tab     = self.tab_widget.currentWidget()
        doc_name        = current_tab.help_file_name

        # tab_index           = self.tab_widget.currentIndex()
        # tab_title           = self.tab_widget.tabText( self.tab_widget.currentIndex())
        # doc_name            = self.tab_help_dict.get( tab_title, "no_specific_help.txt")
        #doc_name            = f"{self.doc_dir}{doc_name}"
        #rint( f"open_tab_help {doc_name = }")

        self.open_txt_file( doc_name )

    #-------
    def open_txt_file( self, file_name  ):
        """
        what it says read
        """
        proc               = subprocess.Popen( [ uft.TEXT_EDITOR, file_name ] )

    # -----------------------
    def show_about_box(self):
        """
        what it says, but !! more inf
        russ-hensel/qt5_by_example: examples of qt5 code ready for copy and paste
        https://github.com/russ-hensel/pyqt_by_example/tree/main

        """
        mode        = parameters.PARAMETERS.mode
        version     = f"Version = {__VERSION__}"
        process_pid = psutil.Process(os.getpid())
        #rint( f"process.memory_info().rss >>{process.memory_info().rss}<<")  # in bytes

        msg      =  "get the size this process thru its pid "
        memory   = process_pid.memory_info().rss/1_000_000
        memory   = f"Memory = {memory} Mbytes"
        repo     = "Repo: https://github.com/russ-hensel/pyqt_by_example/tree/main"
        msg      = ( f"Pyqt By Example {version} {mode}"
                     f"\n{memory}"
                     f"\n{repo}"
                     "\nSee the book at the repo wiki!"
                     )

        QMessageBox.about(self, "About", msg )

    # -----------------------
    def show_parameters(self):
        """
        what it says,
        """
        dialog     = show_parameters.DisplayParameters( parent = self )
        if dialog.exec_() == QDialog.Accepted:
            #self.model.submitAll()
            # ok     = stuffdb_tabbed_sub_window.model_submit_all(
            #            model,  f"StuffEventsSubTab.add_record " )
            # model.select()
            pass

    # ------------------------
    def inspect(self):
        """
        the usual
        """
        print_func_header( "inspect" )

        # make some locals for inspection

        self_parameters    = self.parameters
        self_menubar       = self.menubar

        self_tab_dict      = self.tab_dict

        self_tab_widget     = self.tab_widget

        wat_inspector.go(
             msg            = "inspect !! more locals would be nice ",
             # inspect_me     = self.people_model,
             a_locals       = locals(),
             a_globals      = globals(), )

    # ------------------------
    def breakpoint(self):
        """
        keep this in each object so user breaks into that object
        """
        print_func_header( "breakpoint" )

        print( __file__ )

        breakpoint()

# -----------------------------------
def main():
    """
    yes this is the main app
    """
    app                 = QApplication( [] )
    #dialog          = wat_inspector.DisplayWat( app )  # Create an instance of your custom QDialog
    a_wat_inspector     = wat_inspector.WatInspector( app )
    window              = PyqtByExample()
    window.show()

    app.exec()

    #sys.exit( 0 )

# --------------------
if __name__ == "__main__":
    main()

# ---- eof
