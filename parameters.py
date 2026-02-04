# -*- coding: utf-8 -*-
# ---- tof

"""
    parameters    for  qt examples
    parameters.PARAMETERS.

"""
# --------------------
if __name__ == "__main__":
    #----- run the full app
    import main
# --------------------

import logging
import os
import sys

# ---- local imports
#import string_util
#from   app_global import AppGlobal
#import running_on  parameters.PARAMETERSdir_for_tabs
import in_spect_env

global PARAMETERS
PARAMETERS   = None


# ========================================
class Parameters( ):
    """
    manages parameter values: use it like an ini file but it is code
    """
    # -------
    def choose_mode( self ):
        """
        typically choose one mode
            and if you wish add the plus_test_mode
            if you comment all out all modes you get the default mode which should
            run, perhaps not in the way you want
        """
        self.mode_dev_debug()
        #self.mode_russ_on_theprof()
        #self.new_user_mode()
        #self.millhouse_1_mode()

        # two of my computers
        #self.mode_millhouse_mint()
        #self.mode_theprof_mint()
        #self.russ_1_mode()

        # --- add on for testing, use as desired edit mode for your needs
        #self.plus_test_mode()


    # ---- ---->> Methods:  one for each mode
    # -------
    def mode_test_win( self ):
        """
        a mode for
        """
        self.mode               = "mode_test_win"
        # but do they use the same units ?QDateEdit
        self.qt_width           = 1500
        self.qt_height          = 600    # 700 most of win height
        self.qt_xpos            = 10
        self.qt_ypos            = 10

        self.wat_qt_width       = 1500
        self.wat_qt_height      = 900
        self.wat_qt_xpos        = 10
        self.wat_qt_ypos        = 10

        self.dir_for_tabs       = [ "./",  ]


    # -------
    def mode_dc_on_linux_mint( self ):
        """

        """
        self.mode               = "mode_dc_on_linux_mint"
        # but do they use the same units ?QDateEdit
        # self.qt_width           = 1500
        # self.qt_height          = 600    # 700 most of win height
        # self.qt_xpos            = 10
        # self.qt_ypos            = 10

        # self.wat_qt_width       = 1500
        # self.wat_qt_height      = 900
        # self.wat_qt_xpos        = 10
        # self.wat_qt_ypos        = 10

        # # self.dir_for_tabs       = [""]
        # # self.dir_for_tabs.append( "./tabs/basic_widgets" )
        # # self.dir_for_tabs.append( "./tabs/sql_widgets" )
        # # self.dir_for_tabs.append( "./tabs/book_fitz" ) #  book_fitz

        # # ---- for sample database
        # self.db_file_name        = "/tmp/ramdisk/qt_sql.db"
        # self.db_file_name        = ":memory:"
        # # in memory is fast
        # # on disk (in "/tmp") is easier to debug

        # # ---- for qt tabs
        # self.tab_db_type         = "QSQLITE"

        # self.default_search     = "dc"
        # self.do_search_on_init  = True

        # # self.min_complete    = 10  # minimum value for HOW_COMPLETE


        # self.logging_level      = logging.DEBUG

    # -------
    def mode_dev_debug( self ):
        """  """
        self.mode               = "mode_dev_debug"
        # expose tabs that are not ready
        self.min_complete    = 0  # minimum value for HOW_COMPLETE

        # ---- search and default
        self.default_search     = "progress"
        self.do_search_on_init  = True


        # ---- need to stop double listing
        #may need to be on path sys.path.insert( 1, f"{src_root}/_projects/stuffdb/qt_tabs" )
        self.dir_for_tabs.append( "./tabs/basic_widgets" )
        self.dir_for_tabs.append( "./tabs/sql_widgets" )
        self.dir_for_tabs.append( "./tabs/book_fitz" ) #  book_fitz
        self.dir_for_tabs.append( "./tabs/more" )
        self.dir_for_tabs.append( "./tabs/real_python" )
        self.dir_for_tabs.append( "./tabs/layouts" )

    # -------
    def mode_russ_on_theprof( self ):
        """
        a mode for the new user, pretty much empty,
        a new user may experiment here.
        """
        self.mode               = "mode_russ_on_theprof"
        # but do they use the same units ?QDateEdit
        self.qt_width           = 1500
        self.qt_height          = 600    # 700 most of win height
        self.qt_xpos            = 10
        self.qt_ypos            = 10

        self.wat_qt_width       = 1500
        self.wat_qt_height      = 900
        self.wat_qt_xpos        = 10
        self.wat_qt_ypos        = 10

        # self.dir_for_tabs       = [
        #                             "/mnt/WIN_D/russ/0000/python00/python3/_projects/stuffdb",
        #                             # "/mnt/WIN_D/russ/0000/python00/python3/_projects/rshlib/test",
        #                             "/mnt/WIN_D/russ/0000/python00/python3/_projects/qt5_by_example/tabs",
        #                             "/mnt/WIN_D/russ/0000/python00/python3/_projects/stuffdb/qt_tabs",
        #                             "/mnt/WIN_D/russ/0000/python00/python3/_projects/rshlib/rshlib_qt",
        #                             ]
        # self.dir_for_tabs.append( "./tabs/basic_widgets" )
        # self.dir_for_tabs.append( "./tabs/sql_widgets" )

        # self.dir_for_tabs.append( "./tabs/book_fitz" ) #  book_fitz
        # self.dir_for_tabs.append( "./tabs/more" )

        # ---- for sample database
        self.db_file_name        = "/tmp/ramdisk/qt_sql.db"
        self.db_file_name        = ":memory:"

        # ---- for qt tabs
        self.tab_db_type         = "QSQLITE"

        # next will blow program if dir does not exist
        self.tab_db_file_name    = "/tmp/ramdisk/tab.db"
        self.tab_db_file_name    = ":memory:"    # ok no disk location needed

        # ---- default
        self.default_search     = "russ"
        self.do_search_on_init  = True

        self.logging_level      = logging.DEBUG
        self.logging_level      = logging.INFO

    # -------
    def new_user_mode( self ):
        """
        a mode for the new user, pretty much empty,
        a new user may experiment here.
        """
        self.mode               = "mode new_user"

        # self.dir_for_tabs       = [ "./tabs",
        #                             "/mnt/WIN_D/russ/0000/python00/python3/_projects/stuffdb",
        #                             # "/mnt/WIN_D/russ/0000/python00/python3/_projects/rshlib/test",
        #                             "/mnt/WIN_D/russ/0000/python00/python3/_projects/qt5_by_example/tabs",
        #                             "/mnt/WIN_D/russ/0000/python00/python3/_projects/stuffdb/qt_tabs",
        #                             "/mnt/WIN_D/russ/0000/python00/python3/_projects/rshlib/rshlib_qt",
        #                             ]

    # -------
    def running_on_tweaks(self,  ):
        """
        this is only for things other than the os typically for
        the computer name or hardware info

        !! would we like to get the window size or number or monitors

        not a mode, a tweak to other modes , see documentation
        you need to customize this for your own computers, what you may
            find here are customization's for russ and his computers
        use running on tweaks as a more sophisticated
            version of os_tweaks and computer name tweaks which
        may replace them
        this is computer name tweaks code,
            !! find run_on on which uses os or put computer name under this
            import in_spect_env
            in_spect_env.InSpectEnv.value
        """
        computer_id    =   in_spect_env.InSpectEnv.computer_id

        print( f"Parameters running_on_tweaks {computer_id = }")
        print( f"Parameters {  in_spect_env.InSpectEnv.__str__()  } ")  #ok
        # print( "------------------------------")
        # print( f"{ str(in_spect_env.InSpectEnv)   } ")       # ng

        # if computer_id == "smithers":
        #     self.win_geometry       = '1450x700+20+20'      # width x height position
        #     self.ex_aleditor          =  r"D:\apps\Notepad++\notepad++.exe"
        #     self.db_file_name       =  "smithers_db.db"

        # # ---- bulldog
        # elif computer_id == "bulldog":
        #     self.ex_editor          =  r"gedit"
        #     self.db_file_name       =  "bulldog_db.db"


        # elif computer_id == "millhouse":
        #     self.ex_editor          =  r"C:\apps\Notepad++\notepad++.exe"
        #     #self.win_geometry   = '1300x600+20+20'
        #     self.db_file_name       =  "millhouse_db.db"

        # ---- 'millhouse-mint'
        if computer_id == 'millhouse-mint':
            self.ex_editor          =  r"C:\apps\Notepad++\notepad++.exe"

            # ---- for sample database
            self.db_type            = "QSQLITE"
                # the type of database, so far we only support sqllite

            self.db_file_name        = ":memory:"     #  = "sample.db"   =  ":memory:"
            #self.db_file_name        = "./qt_sql.db"    #  real files are very slow

            # ---- for qt tabs
            self.tab_db_type         = "QSQLITE"
            self.tab_db_file_name    = ":memory:"

            #self.dir_for_tabs       = [ "./",  ]
            #self.dir_for_tabs       = [    ]
            #self.dir_for_tabs      =  [ "/mnt/WIN_D/russ/0000/python00/python3/_projects/stuffdb/qt_tabs" ]
            self.dir_for_tabs.append(  "/home/russ/sync_with_fattony/python3/_projects/stuffdb/qt_tabs"  )

        # # ---- theprof
        # elif computer_id == "theprof":
        #     self.ex_editor          =  r"C:\apps\Notepad++\notepad++.exe"
        #     self.db_file_name       =  "the_prof_db.db"


        # else:
        #     print( f"In parameters: no special settings for computer_id {computer_id}" )
        #     if self.running_on.os_is_win:
        #         self.ex_editor          =  r"C:\apps\Notepad++\notepad++.exe"
        #     else:
        #         self.ex_editor          =  r"leafpad"    # Linux raspberry pi maybe

    # -------
    def os_tweaks( self ):
        """
        this is an subroutine to tweak the default settings of "default_mode"
        for particular operating systems
        you may need to mess with this based on your os setup
        """
        our_os           = sys.platform
        self.our_os      = our_os
             #testing if our_os == "linux" or our_os == "linux2"  "darwin"  "win32"

        if our_os == "win32":
            self.os_win = True     # the OS is windows any version
        else:
            self.os_win = False    # the OS is not windows

        if  self.os_win:
            self.text_editor        = "notepad"

        else:
            pass
            # print( "os_tweaks for not windows " )

    # ------->> default mode, always call
    def mode_default( self ):
        """
        sets up pretty much all settings
        documents the meaning of the modes
        call first, then override as necessary
        good chance these settings will at least let the app run
        """
        self.mode              = "mode_default"
            # name your config, it will show in app title
            # may be changed later in parameter init

        # #--------------- automatic settings -----------------
        # self.running_on   = running_on.RunningOn
        # self.running_on.gather_data()

        # # some of the next all?? should be moved over to RunningOn
        # self.running_on.log_me( logger = None, logger_level = 10, print_flag = False )

        # # this is the path to the main.py program
        # self.py_path                   = self.running_on.py_path

        # self.set_default_path_here     = True
        #     # to make app location the default path in the app, Think True may always be best.
        #     # above may be tricky to reset, but we may have the original dir in running on
        # # no easy way to override this ??
        # if  self.set_default_path_here:     # Now change the directory to location of this file

        #     py_path    = self.running_on.py_path

        #     print( f"Parameters.py: Directory: (  >>{os.getcwd()}<< switch if not '' to >>{py_path}<<")
        #     if py_path != "":
        #         os.chdir( py_path )

        # # so we know our os  could be "linux" or our_os == "linux2"  "darwin"....
        # self.our_os             = self.running_on.our_os
        # self.os_win             = self.running_on.os_win          # boolean True if some version of windows
        # self.computername       = self.running_on.computername    # a name of the computer if we can get it
        # # directory where app was opened, not where it resides
        # self.opening_dir        = self.running_on.opening_dir     # the opening dir before anyone changes it

        # self.platform           = self.our_os           #  redundant

        # ---- appearance size--

        # control initial size and position with:
        self.qt_width           = 1200
        self.qt_height          = 500
        self.qt_xpos            = 10
        self.qt_ypos            = 10

        self.wat_qt_width       = 1000
        self.wat_qt_height      = 400
        self.wat_qt_xpos        = 10
        self.wat_qt_ypos        = 10



        self.minimun_useful    =  10

        self.icon               = r"./images/icon_red.png"    # icon for running app
        self.icon               = r"./icons/icons/binocular.png"
        self.icon               = r"./misc/computer.ico"


        self.text_editor        = "gedit"
#        self.text_editor        = "xed"

        # ---- logging
        self.pylogging_fn       = "./app.py_log"   # file name for the python logging


        self.log_mode               = "w"    # "a" append "w" truncate and write
        self.delete_log_on_start    = True

        self.logging_level      = logging.DEBUG         # may be very verbose
        self.logging_level      = logging.INFO
        #self.logging_level      = logging.INFO

        self.logger_id          = "qt_ex"         # id of app in logging file


        self.breakpoint_ok      = True  # enable breakpoin button



        self.auto_run           = True


        # ---- database there are 2 ........

        self.db_type            = "QSQLITE"
            # the type of database, so far we only support sqllite

        # ---- for sample database
        self.db_file_name        = "/tmp/ramdisk/qt_sql.db"
        self.db_file_name        = ":memory:"     #  = "sample.db"   =  ":memory:"
        #self.db_file_name        = "./qt_sql.db"    #  real files are very slow

        # ---- for qt tabs
        self.tab_db_type         = "QSQLITE"
        self.tab_db_file_name    = "/tmp/ramdisk/tab.db"
        self.tab_db_file_name    = "./tab.db"
        self.tab_db_file_name    = ":memory:"

        # this is the name of a program: its executable with path info.
        # to be used in opening an external editor
        #self.db_file_name        = "sample2.db"   #  = "sample.db"   =  ":memory:"

        # ---- file names -- but not db
        # control button for editing the readme file
        self.readme_fn      = "readme_rsh.txt"   # or None to suppress in gui
            # a readme file accessable from the main menu

        # or anything else ( will try to shell out may or may not work )
        self.help_fn        =  "./docs/help.txt"   #  >>. this is the path to our main .py file self.py_path + "/" +

        self.help_path      =  "./docs"
        self.help_path      =  "/mnt/WIN_D/russ/0000/python00/python3/_projects/qt5_by_example/docs/"
            # path leading to all docs and help

        # ---- dir_for_tabs
        self.dir_for_tabs       = [ "./",  ]
        self.dir_for_tabs       = [    ]
        self.dir_for_tabs       = [ "/mnt/WIN_D/russ/0000/python00/python3/_projects/stuffdb/qt_tabs" ]
        #may need to be on path sys.path.insert( 1, f"{src_root}/_projects/stuffdb/qt_tabs" )
        self.dir_for_tabs.append( "./tabs/basic_widgets" )
        self.dir_for_tabs.append( "./tabs/sql_widgets" )
        self.dir_for_tabs.append( "./tabs/book_fitz" ) #  book_fitz
        self.dir_for_tabs.append( "./tabs/more" )
        self.dir_for_tabs.append( "./tabs/real_python" )
        self.dir_for_tabs.append( "./tabs/layouts" )

        # ---- min_complete
        self.min_complete    = 10  # minimum value for HOW_COMPLETE

        # ---- search and default
        self.default_search     = ""
        self.do_search_on_init  = False

        # probably not used ??
        # ---- systems for helpdb ??alpha  to sort make all quotes the same
        self.systems_list      =  [    '',
                            'Bash',
                            'CAD/Print',
                            'Delete',
                            'Electronics',
                            'House',
                            'Linux',
                            'Powerbuilder',
                            'Programming',
                            'Python',
                            'RasPi',
                            'RshPy',              # subsystem the project
                            'Russ',
                            'StuffDB',
                            'TBD',
                            'Tools',

                        ]




    # -------
    def __init__( self, ):
        """
        Init for instance, usually not modified, except perhaps debug stuff
        ( if any )... but use plus_test_mode()
        may be down in listing because it should not be messed with.
        """
        self.mode_default()
        self.os_tweaks()
        self.running_on_tweaks()
        self.choose_mode()

        # next lets you use  parameters.PARAMETERS as a global
        global PARAMETERS
        if not PARAMETERS:
            print( "creating global parameters.PARAMETERS")
            PARAMETERS    = self
        else:
            print( "__init__ probably an error")

        #rint( self ) # for debugging
    # ---------------------
    def to_columns( self, current_str, item_list, format_list = [ "{: <30}", "{:<30}" ], indent = "    "  ):
        """
        for __str__  probably always default format_list
        """
        #rint ( f"item_list {item_list}.............................................................. " )
        line_out  = ""
        for i_item, i_format in zip( item_list, format_list ):
            a_col  = i_format.format( i_item )
            line_out   = f"{indent}{line_out}{a_col}"
        ret_str  = f"{current_str}\n{line_out}"
        return ret_str

    # -----------------------------------
    def __str__( self,   ):
        """
        sometimes it is hard to see where values have come out this may help if printed.
        not complete, add as needed -- compare across applications and code above
        """
        # new_indented    = "\n    "   # but it nice to have some whitespace to see ...


        a_str   = ""
        a_str   = ">>>>>>>>>>* Parameters *<<<<<<<<<<<<"

        a_str   = self.to_columns( a_str, ["mode",
                                           f"{self.mode}" ] )


        a_str   = self.to_columns( a_str, ["our_os",
                                           f"{self.our_os}" ] )

        a_str   = self.to_columns( a_str, ["db_type",
                                           f"{self.db_type}" ] )
        a_str   = self.to_columns( a_str, ["db_file_name",
                                           f"{self.db_file_name}" ] )


        a_str   = self.to_columns( a_str, ["tab_db_type",
                                           f"{self.tab_db_type}" ] )
        a_str   = self.to_columns( a_str, [ "tab_db_file_name",
                                            f"{self.tab_db_file_name}" ] )

        a_str   = self.to_columns( a_str, ["help_fn",
                                           f"{self.help_fn}" ] )
        a_str   = self.to_columns( a_str, ["help_path",
                                           f"{self.help_path}" ] )
        a_str   = self.to_columns( a_str, ["icon",
                                           f"{self.icon}" ] )

        a_str   = self.to_columns( a_str, ["logger_id",
                                           f"{self.logger_id}" ] )

        a_str   = self.to_columns( a_str, ["logging_level",
                                           f"{self.logging_level}" ] )

        a_str   = self.to_columns( a_str, ["pylogging_fn",
                                                  f"{self.pylogging_fn}" ] )

        a_str   = self.to_columns( a_str, [ "log_mode",
                                                  f"{self.log_mode}" ] )


        a_str   = self.to_columns( a_str, ["minimun_useful",
                                           f"{self.minimun_useful}" ] )

        a_str   = self.to_columns( a_str, ["breakpoint_ok",
                                           f"{self.breakpoint_ok}" ] )


        a_str   = self.to_columns( a_str, ["pylogging_fn",
                                           f"{self.pylogging_fn}" ] )


        a_str   = self.to_columns( a_str, ["qt_height",
                                           f"{self.qt_height}" ] )
        a_str   = self.to_columns( a_str, ["qt_width",
                                           f"{self.qt_width}" ] )
        a_str   = self.to_columns( a_str, ["qt_xpos",
                                           f"{self.qt_xpos}" ] )
        a_str   = self.to_columns( a_str, ["qt_ypos",
                                           f"{self.qt_ypos}" ] )
        a_str   = self.to_columns( a_str, ["readme_fn",
                                           f"{self.readme_fn}" ] )
        a_str   = self.to_columns( a_str, ["text_editor",
                                           f"{self.text_editor}" ] )
        a_str   = self.to_columns( a_str, ["wat_qt_height",
                                           f"{self.wat_qt_height}" ] )
        a_str   = self.to_columns( a_str, ["wat_qt_width",
                                           f"{self.wat_qt_width}" ] )
        a_str   = self.to_columns( a_str, ["wat_qt_xpos",
                                           f"{self.wat_qt_xpos}" ] )
        a_str   = self.to_columns( a_str, ["wat_qt_ypos",
                                           f"{self.wat_qt_ypos}" ] )
        a_str   = self.to_columns( a_str, ["self.dir_for_tabs",
                                           f"{self.dir_for_tabs}" ] )

        return a_str

# # something like this for creating on import
# # ---------------
# def create_if_needed( ):
#     global PARAMETERS
#     if not PARAMETERS:

#          print( "creating global parameters.PARAMETERS")
#          PARAMETERS    = Parameters()

# # --------------------
# create_if_needed()




# ---- eof ==============================
