#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ---- tof
"""
tab_vlc_qt_object_widget.py
self.help_file_name     =  "tab_vlc_qt_object_widget.txt"

KEY_WORDS:      vlc widget mp4 video python-vlc libvlc QFrame object oop
CLASS_NAME:     QWebVlcMediaObjectWidgetTab
WIDGETS:        VlcVideoFrame/VlcVideoWidget -- see vlc_widget.py, this tab just uses them
STATUS:         in dev -- same behavior as tab_vlc_qt_widget.py
TAB_TITLE:      VlcMediaObjectTab / Object - in test
DESCRIPTION:    VLC in an Object
MORE:           same as tab_vlc_qt_widget.py ( play local video via python-vlc ),
                but all the vlc plumbing/controls have been factored out into
                vlc_widget.VlcVideoWidget, a self-contained, reusable "video
                player" widget -- this tab just drops it in and adds the
                demo-specific "Play Vid 1/2" buttons that pick a file and
                call VlcVideoWidget.play().
HOW_COMPLETE:   20  #  AND A COMMENT -- <10 major probs  <15 runs but <20 fair not finished  <=25 not to shabby
"""
WIKI_LINK      =  "https://github.com/russ-hensel/pyqt_by_example/wiki/VLC Mp4 Media Widget"


# --------------------
if __name__ == "__main__":
    #----- run the full app
    import main   # noqa  stops auto removal by pycln
# --------------------


import os

from qtpy.QtWidgets import (
                             QHBoxLayout,
                             QPushButton,
                             QVBoxLayout
                             )


import utils_for_tabs as uft
import wat_inspector
import tab_base
from   vlc_widget    import VlcVideoWidget
from video_thumbnail import get_thumbnail

# ---- end imports


INDENT          = uft.INDENT
INDENT          = uft.BEGIN_MARK_1
INDENT          = uft.BEGIN_MARK_2
#INDENT          = qt_sql_widgets.

basedir         = os.path.dirname( __file__ )   # vid files live next to this module


#-----------------------------------------------
class QWebVlcMediaObjectWidgetTab( tab_base.TabBase ):
    """
    here build a tab in its own class to hide its variables

    same as QWebVlcMediaWidgetTab ( tab_vlc_qt_widget.py ), but all the vlc
    plumbing/controls live in vlc_widget.VlcVideoWidget instead of inline
    here -- this class only drops in a VlcVideoWidget and adds the
    demo-specific "Play Vid 1/2" buttons that call self.video_widget.play()
    """

    def __init__(self, ):
        """
        """
        super().__init__( )

        self.module_file        = __file__      # save for help file usage

        global WIKI_LINK
        self.wiki_link          = WIKI_LINK

        self.mutate_dict[0]     = self.mutate_0
        self.mutate_dict[1]     = self.mutate_1

        # vp9/opus webm -- open codecs, QtWebEngine's chromium can decode these
        self.vid_1_file_name    = "/home/russ/Videos/test_clip_vp9.webm"
        # original h.264/aac mp4 -- QtWebEngine's chromium can NOT decode this,
        # kept here, libvlc plays it fine where QtWebEngine/QMediaPlayer choke
        self.vid_2_file_name    = "/home/russ/Videos/40768-Legend_of_the_Ancient_Sword_1540300303.mp4"

        self.vid_2_file_name    = "/mnt/8ball1/first6_root/photos/photos_raw/from_phone/moved_to_computer/older_june23_copy/PXL_20210712_162742457.LS.mp4"

        file_name               = self.vid_2_file_name
        self.current_vid        = file_name

        self.help_file_name     =  "no_help_file.txt"
        self._build_gui()

    #----------------------------
    def _build_gui_widgets(self, main_layout  ):
        """
        the usual, build the gui with the widgets of interest
        and the buttons for examples
        """
        layout              = QVBoxLayout(   )

        main_layout.addLayout( layout )

        # ---- the video player -- VlcVideoWidget bundles the video surface
        # with all its playback controls ( status, seek, volume, pause/stop ).
        # forward its status_message_signal into this tab's own msg widget
        video_widget          = VlcVideoWidget(   )
        video_widget.status_message_signal.connect( self.append_msg )
        self.video_widget     = video_widget
        layout.addWidget( video_widget )

        # ---- buttons -- just the demo-specific "which file" choice, the
        # rest of the controls live inside video_widget
        button_layout = QHBoxLayout()
        layout.addLayout( button_layout )

        # ---- "Play\n Vid 1"
        a_widget           = QPushButton( "Play\n Vid 1" )
        a_widget.clicked.connect( self.play_vid_1 )
        button_layout.addWidget( a_widget )

        # ---- "Play\n Vid 2"
        a_widget           = QPushButton( "Play\n Vid 2" )
        a_widget.clicked.connect( self.play_vid_2 )
        button_layout.addWidget( a_widget )

        # # ---- Make\nThumb
        # a_widget           = QPushButton( "Make\nThumb" )
        # a_widget.clicked.connect( self.make_thumb )
        # button_layout.addWidget( a_widget )

        self.build_gui_last_buttons( button_layout )



    # -------------------------------------
    def play_vid_1( self, ):
        """
        what it says
        """
        file_name           = self.vid_1_file_name
        self.current_vid    = file_name

        msg          = ( f"playing {file_name}" )
        self.append_msg( msg )

        self.video_widget.play( file_name )

        self.append_msg( "play_vid_1" )

    # -------------------------------------
    def play_vid_2( self, ):
        """
        what it says
        """
        file_name           = self.vid_2_file_name
        self.current_vid    = file_name

        msg          = ( f"playing {file_name}" )
        self.append_msg( msg )

        self.video_widget.play( file_name )

        self.append_msg( "play_vid_2" )

    # ------------------------------------
    def mutate_0( self ):
        """
        read it -- mutate the widgets
        """
        self.append_function_msg( "mutate_0" )

        self.append_function_msg( "no code for mutate_0 so far " )

        self.append_msg( tab_base.DONE_MSG )


    # ------------------------------------
    def mutate_1( self ):
        """
        read it -- mutate the widgets
        """
        self.append_function_msg( "mutate_1" )

        self.append_function_msg( "make thumbnail thumb.png " )
        get_thumbnail( self.current_vid , "thumb.jpg", timestamp = "50%", size = 320, quality = 8 )

        self.append_msg( tab_base.DONE_MSG )

    # ------------------------
    def inspect(self):
        """
        the usual
        """
        self.append_function_msg( "inspect" )
        # make some locals for inspection

        self_video_widget      = self.video_widget
        self_video_frame       = self.video_widget.video_frame
        self_position_slider   = self.video_widget.position_slider
        self_volume_slider     = self.video_widget.volume_slider

        wat_inspector.go(
             msg            = "inspect...",
             a_locals       = locals(),
             a_globals      = globals(), )

        self.append_msg(  tab_base.DONE_MSG )

    # ------------------------
    def breakpoint(self):
        """
        the usual
        """
        self.append_function_msg( "breakpoint" )

        breakpoint()

        self.append_msg(  tab_base.DONE_MSG )

# ---- eof
