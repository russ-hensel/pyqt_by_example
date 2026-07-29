#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ---- tof
"""
tab_q_table_widget.py
self.help_file_name     =  "q_table_widget_tab.txt"

KEY_WORDS:      vlc widget mp4 video python-vlc libvlc
CLASS_NAME:     QWebVlcMediaWidgetTab
WIDGETS:        QFrame ( libvlc renders directly into its native window )
STATUS:         in dev -- plays local files via libvlc, X11 only ( set_xwindow )
TAB_TITLE:      VlcMediaTab / No Object - in test
DESCRIPTION:    play local video files using python-vlc, embedded in a plain QFrame
MORE:                via winId()/set_xwindow() -- libvlc eats almost any
                codec so this is the fallback when QtWebEngine/QMediaPlayer
                choke on a file
HOW_COMPLETE:   20  #  AND A COMMENT -- <10 major probs  <15 runs but <20 fair not finished  <=25 not to shabby
"""
WIKI_LINK      =  "https://github.com/russ-hensel/pyqt_by_example/wiki/VLC Mp4 Media Widget"


# --------------------
if __name__ == "__main__":
    #----- run the full app
    import main   # noqa  stops auto removal by pycln
# --------------------


import os

import vlc

from qtpy.QtCore import (Qt, QTimer, Signal)
from qtpy.QtGui import (QPalette)
from qtpy.QtWidgets import (
                             QFrame,
                             QHBoxLayout,
                             QLabel,
                             QPushButton,
                             QSlider,
                             QVBoxLayout
                             )


import utils_for_tabs as uft
import wat_inspector
import tab_base


# ---- end imports


INDENT          = uft.INDENT
INDENT          = uft.BEGIN_MARK_1
INDENT          = uft.BEGIN_MARK_2
#INDENT          = qt_sql_widgets.

basedir         = os.path.dirname( __file__ )   # vid files live next to this module


#-----------------------------------------------
class QWebVlcMediaWidgetTab( tab_base.TabBase ):
    """
    here build a tab in its own class to hide its variables
    """

    # libvlc fires these on its own internal thread, not the Qt main thread --
    # emitting a signal from that thread queues the slot call onto the main
    # thread instead of touching widgets directly from a foreign thread
    vlc_state_signal        = Signal( str )

    def __init__(self, ):
        """
        """
        super().__init__( )

        self.module_file        = __file__      # save for help file usage

        global WIKI_LINK
        self.wiki_link          = WIKI_LINK

        self.mutate_dict[0]     = self.mutate_0
        #self.mutate_dict[1]     = self.mutate_1

        self.vlc_instance       = None
        self.vlc_player         = None
        self.vlc_embedded       = False    # set_xwindow() done lazily, see _ensure_embedded

        self.position_slider_dragging = False    # True while user drags the seek slider, see _update_position

        # vp9/opus webm -- open codecs, QtWebEngine's chromium can decode these
        self.vid_1_file_name    = "/home/russ/Videos/test_clip_vp9.webm"
        # original h.264/aac mp4 -- QtWebEngine's chromium can NOT decode this,
        # kept here, libvlc plays it fine where QtWebEngine/QMediaPlayer choke
        self.vid_2_file_name    = "/home/russ/Videos/40768-Legend_of_the_Ancient_Sword_1540300303.mp4"

        self.vid_2_file_name    = "/mnt/8ball1/first6_root/photos/photos_raw/from_phone/moved_to_computer/older_june23_copy/PXL_20210712_162742457.LS.mp4"


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
        button_layout        = QHBoxLayout(   )

        # ---- the video surface -- libvlc paints directly into this frame's
        # native ( X11 ) window, bypassing Qt's own paint system, so give it
        # a black background rather than leave the default widget fill showing
        # through before playback starts
        video_frame          = QFrame(   )
        video_frame.setMinimumHeight( 300 )
        video_frame.setAutoFillBackground( True )
        a_palette            = video_frame.palette()
        a_palette.setColor( QPalette.Window, Qt.black )
        video_frame.setPalette( a_palette )
        self.video_frame     = video_frame
        layout.addWidget( video_frame )

        # ---- libvlc instance/player -- unlike QMediaPlayer these are not
        # owned/cleaned-up by Qt, see notes at top of file
        vlc_instance         = vlc.Instance()
        vlc_player           = vlc_instance.media_player_new()
        self.vlc_instance    = vlc_instance
        self.vlc_player      = vlc_player

        self.vlc_state_signal.connect( self.on_media_state_changed )

        event_manager        = vlc_player.event_manager()
        event_manager.event_attach( vlc.EventType.MediaPlayerPlaying,          self._vlc_on_playing )
        event_manager.event_attach( vlc.EventType.MediaPlayerPaused,           self._vlc_on_paused )
        event_manager.event_attach( vlc.EventType.MediaPlayerStopped,          self._vlc_on_stopped )
        event_manager.event_attach( vlc.EventType.MediaPlayerEndReached,       self._vlc_on_end_reached )
        event_manager.event_attach( vlc.EventType.MediaPlayerEncounteredError, self._vlc_on_error )

        # ---- status label
        a_widget             = QLabel( "no video loaded" )
        self.media_status_widget   = a_widget
        layout.addWidget( a_widget )

        # ---- position row -- slider + elapsed/total time, like vlc's own seek bar
        position_layout      = QHBoxLayout(   )
        layout.addLayout( position_layout )

        position_slider      = QSlider( Qt.Horizontal )
        position_slider.setRange( 0, 1000 )    # scaled 0-1000, mapped to get_length()/set_time() in ms
        position_slider.sliderPressed.connect(  self._on_position_slider_pressed )
        position_slider.sliderReleased.connect( self._on_position_slider_released )
        self.position_slider = position_slider
        position_layout.addWidget( position_slider )

        a_widget             = QLabel( "00:00 / 00:00" )
        self.time_label      = a_widget
        position_layout.addWidget( a_widget )

        # a timer, not vlc's own MediaPlayerPositionChanged/TimeChanged events --
        # those fire ( often, on the libvlc thread ) many times a second, more
        # marshaling than a seek bar needs. polling from the Qt side is simpler
        position_timer        = QTimer( self )
        position_timer.setInterval( 250 )
        position_timer.timeout.connect( self._update_position )
        position_timer.start()
        self.position_timer   = position_timer

        # ---- volume row
        volume_layout         = QHBoxLayout(   )
        layout.addLayout( volume_layout )

        a_widget              = QLabel( "Volume" )
        volume_layout.addWidget( a_widget )

        volume_slider         = QSlider( Qt.Horizontal )
        volume_slider.setRange( 0, 100 )
        volume_slider.valueChanged.connect( self.on_volume_changed )
        self.volume_slider    = volume_slider
        volume_layout.addWidget( volume_slider )
        volume_slider.setValue( 80 )    # triggers on_volume_changed, sets the initial vlc volume too

        # ---- buttons
        button_layout = QHBoxLayout()
        layout.addLayout( button_layout )

        # --- begin a_widget method
        a_widget           = QPushButton( "Play Vid 1")
        a_widget.clicked.connect( self.play_vid_1 )
        button_layout.addWidget(a_widget)

        # --- begin a_widget method
        a_widget           = QPushButton( "Play Vid 2")
        a_widget.clicked.connect( self.play_vid_2 )
        button_layout.addWidget(a_widget)

        # --- begin a_widget method
        a_widget           = QPushButton( "Pause")
        a_widget.clicked.connect( self.pause_vid )
        button_layout.addWidget(a_widget)

        # --- begin a_widget method
        a_widget           = QPushButton( "Stop")
        a_widget.clicked.connect( self.stop_vid )
        button_layout.addWidget(a_widget)

        self.build_gui_last_buttons( button_layout )

    # -------------------------------------
    def _ensure_embedded( self, ):
        """
        read it -- hook libvlc's rendering into self.video_frame's native
        ( X11 ) window. done lazily on first play rather than at gui-build
        time since winId() should be called after the frame is part of a
        shown widget hierarchy, and this tab's __init__ runs before the
        main window has shown anything
        """
        if self.vlc_embedded:
            return

        win_id              = int( self.video_frame.winId() )
        self.vlc_player.set_xwindow( win_id )
        self.vlc_embedded   = True

    # -------------------------------------
    def _fmt_ms( self, ms ):
        """
        what it says -- ms ( libvlc's time unit ) to a "mm:ss" string,
        treating negative/unknown ( libvlc returns -1 when there is no
        media, or length is not yet known ) as zero
        """
        ms                  = max( ms, 0 )
        total_seconds       = ms // 1000
        minutes             = total_seconds // 60
        seconds             = total_seconds % 60

        return f"{minutes:02d}:{seconds:02d}"

    # -------------------------------------
    def _update_position( self, ):
        """
        read it -- polled by self.position_timer, keeps the seek slider
        and time label in sync with the actual vlc player position
        """
        length              = self.vlc_player.get_length()    # ms, -1 if unknown
        current              = self.vlc_player.get_time()      # ms, -1 if unknown

        if length > 0 and not self.position_slider_dragging:
            slider_value        = int( current * 1000 / length )
            self.position_slider.blockSignals( True )
            self.position_slider.setValue( slider_value )
            self.position_slider.blockSignals( False )

        msg                 = ( f"{self._fmt_ms( current )} / {self._fmt_ms( length )}" )
        self.time_label.setText( msg )

    # -------------------------------------
    def _on_position_slider_pressed( self, ):
        """
        what it says -- stop the timer from fighting the user's drag
        """
        self.position_slider_dragging = True

    # -------------------------------------
    def _on_position_slider_released( self, ):
        """
        what it says -- seek to wherever the user dropped the slider
        """
        length              = self.vlc_player.get_length()

        if length > 0:
            value               = self.position_slider.value()
            new_time            = int( value * length / 1000 )
            self.vlc_player.set_time( new_time )

        self.position_slider_dragging = False

    # -------------------------------------
    def on_volume_changed( self, value ):
        """
        what it says -- value is 0-100, straight from the volume slider
        """
        self.vlc_player.audio_set_volume( value )

    # -------------------------------------
    def _load_and_play( self, file_name ):
        """
        what it says --
        """
        self._ensure_embedded()

        media               = self.vlc_instance.media_new( file_name )
        self.vlc_player.set_media( media )
        self.vlc_player.play()

        msg                 = ( f"playing {file_name = }  " )
        self.append_msg( msg )

        self.media_status_widget.setText( msg )

    # -------------------------------------
    def on_media_state_changed( self, state_text ):
        """
        what it says -- reflect the player state in the status label.
        runs on the Qt main thread ( see vlc_state_signal ), unlike the
        _vlc_on_* callbacks below
        """
        self.media_status_widget.setText( state_text )
        if state_text.startswith( "error" ):
            self.append_msg( state_text )

    # -------------------------------------
    def _vlc_on_playing( self, event ):
        """ called on a libvlc thread -- just marshal to Qt via signal """
        self.vlc_state_signal.emit( "playing" )

    # -------------------------------------
    def _vlc_on_paused( self, event ):
        """ called on a libvlc thread -- just marshal to Qt via signal """
        self.vlc_state_signal.emit( "paused" )

    # -------------------------------------
    def _vlc_on_stopped( self, event ):
        """ called on a libvlc thread -- just marshal to Qt via signal """
        self.vlc_state_signal.emit( "stopped" )

    # -------------------------------------
    def _vlc_on_end_reached( self, event ):
        """ called on a libvlc thread -- just marshal to Qt via signal """
        self.vlc_state_signal.emit( "end reached" )

    # -------------------------------------
    def _vlc_on_error( self, event ):
        """ called on a libvlc thread -- just marshal to Qt via signal """
        err_msg             = vlc.libvlc_errmsg()    # often None, libvlc is inconsistent about setting this
        err_msg             = err_msg.decode() if err_msg else "unknown libvlc error"
        self.vlc_state_signal.emit( f"error: {err_msg}" )

    # -------------------------------------
    def play_vid_1( self, ):
        """
        what it says
        """
        file_name    = self.vid_1_file_name

        msg          = ( f"playing {file_name}" )
        self.append_msg( msg )

        self._load_and_play( file_name )

        self.append_msg( "play_vid_1" )

    # -------------------------------------
    def play_vid_2( self, ):
        """
        what it says
        """
        file_name    = self.vid_2_file_name

        msg          = ( f"playing {file_name}" )
        self.append_msg( msg )

        self._load_and_play( file_name )

        self.append_msg( "play_vid_2" )

    # -------------------------------------
    def pause_vid( self, ):
        """
        what it says -- toggle pause/resume of the media
        ( status label updates via the MediaPlayerPaused/Playing events )
        """
        self.vlc_player.pause()

        self.append_function_msg( "pause_vid" )

    # -------------------------------------
    def stop_vid( self, ):
        """
        what it says -- stop the media
        ( status label updates via the MediaPlayerStopped event )
        """
        self.vlc_player.stop()

        self.append_function_msg( "stop_vid" )

    # ------------------------------------
    def mutate_0( self ):
        """
        read it -- mutate the widgets
        """
        self.append_function_msg( "mutate_0" )

        self.append_function_msg( "no code for mutates so far " )

        self.append_msg( tab_base.DONE_MSG )


    # ------------------------------------
    def mutate_1( self ):
        """
        read it -- mutate the widgets
        """
        self.append_function_msg( "mutate_1" )

        self.append_function_msg( "no code for mutates so far " )

        self.append_msg( tab_base.DONE_MSG )

    # ------------------------
    def inspect(self):
        """
        the usual
        """
        self.append_function_msg( "inspect" )
        # make some locals for inspection

        self_video_frame     = self.video_frame
        self_vlc_instance    = self.vlc_instance
        self_vlc_player      = self.vlc_player
        self_position_slider = self.position_slider
        self_volume_slider   = self.volume_slider

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



