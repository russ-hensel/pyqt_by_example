#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ---- tof
"""
tab_camera_widget_object.py
self.help_file_name     =  "tab_camera_widget_object.txt"

KEY_WORDS:      WebCam camera still image video qt6 object oop QMediaCaptureSession reusable widget
CLASS_NAME:     QCameraWidgetObjectTab
WIDGETS:        CameraCaptureWidget -- see camera_capture_widget.py, the preview + camera logic
MORE:               QComboBox x2, QPushButton x5, QLabel -- the controls, this tab's own
STATUS:         QT6 ONLY -- will not import under PyQt5, which is what the app runs on today
TAB_TITLE:      Camera / Webcam Object - qt6 only
DESCRIPTION:    same behaviour as tab_camera_widget.py ( webcam preview, stills,
MORE:               video ) but all the camera plumbing has been factored out
                into camera_capture_widget.CameraCaptureWidget, a self
                contained re-usable webcam widget.  that widget is the live
                preview and the camera logic, nothing else -- the device and
                format combos, start / stop, the thumbnail, the status line
                and the snap / record buttons are all built here and drive it
                through its api, and it answers through its signals.  this tab
                also adds the one thing the widget deliberately does not know
                about: where files go, which comes from parameters
HOW_COMPLETE:   22  #  AND A COMMENT -- <10 major probs  <15 runs but <20 fair not finished  <=25 not to shabby
"""
WIKI_LINK      =  "https://github.com/russ-hensel/pyqt_by_example/wiki/Camera Webcam Widget"


# --------------------
if __name__ == "__main__":
    #----- run the full app
    import main   # noqa  stops auto removal by pycln
# --------------------


import os

from qtpy.QtCore   import ( Qt )
from qtpy.QtGui    import ( QPixmap )
from qtpy.QtWidgets import ( QComboBox,
                             QFileDialog,
                             QFrame,
                             QHBoxLayout,
                             QLabel,
                             QPushButton,
                             QVBoxLayout,
                             )

import wat_inspector
import tab_base

from camera_capture_widget import CameraCaptureWidget


# ---- end imports

basedir         = os.path.dirname( os.path.abspath( __file__ ) )

DEFAULT_OUTPUT  = "./output"        # only if parameters is not up, see _start_save_dir
CAMERA_SUB_DIR  = "camera"
THUMB_WIDTH     = 160


#-----------------------------------------------
class QCameraWidgetObjectTab( tab_base.TabBase ):
    """
    here build a tab in its own class to hide its variables

    the object version of tab_camera_widget.py.  that tab has every bit of the
    camera inline -- session, camera, image capture, recorder, the device and
    format combos, the poll timer, the lot -- about 500 lines of it.  here the
    camera *machinery* lives in camera_capture_widget.CameraCaptureWidget and
    this tab is the part you can see: the combos, the buttons, the thumbnail,
    the status line, and where files go.

    the division of labour is the interesting bit.  the widget knows about
    cameras and nothing about this application -- no parameters, no
    global_vars, no tab_base -- which is exactly what makes it re-usable.  the
    tab knows about the application and almost nothing about cameras: it calls
    methods on the widget and it listens to signals, it never touches a
    QCamera.  where captures land is an application question, so it is
    answered here and handed over with set_save_dir

    the widget used to bring its own controls, so this tab was much thinner.
    the controls moved out here because a host normally wants to lay them out
    its own way -- and one host may not want half of them at all
    """

    def __init__(self, ):
        """
        """
        super().__init__( )

        self.module_file        = __file__      # save for help file usage

        global WIKI_LINK
        self.wiki_link          = WIKI_LINK

        self.mutate_dict[0]     = self.mutate_0
        #self.mutate_dict[1]     = self.mutate_1

        self.camera_widget      = None      # CameraCaptureWidget, made in _build_gui_widgets

        self.help_file_name     =  "tab_camera_widget_object.txt"
        self._build_gui()

        # only now -- TabBase builds msg_widget in _build_gui_bot, so nothing
        # before this may call append_msg
        self._apply_save_dir( self._start_save_dir() )

    #----------------------------
    def _build_gui_widgets(self, main_layout  ):
        """
        the usual, build the gui with the widgets of interest
        and the buttons for examples
        """
        layout              = QVBoxLayout(   )
        main_layout.addLayout( layout )

        self._build_device_row( layout )

        # ---- preview + last still, side by side
        view_layout         = QHBoxLayout(   )
        layout.addLayout( view_layout )

        # ---- the widget of interest.  all it puts on screen is the live
        # preview -- everything that works it is built by this tab and talks
        # to the widget through its api and its signals
        a_widget            = CameraCaptureWidget(   )
        a_widget.status_message_signal.connect( self.append_msg )
        a_widget.status_text_signal.connect( self.on_status_text )
        a_widget.image_saved_signal.connect( self.on_image_saved )
        a_widget.video_saved_signal.connect( self.on_video_saved )
        a_widget.still_image_signal.connect( self.on_still_image )
        a_widget.camera_list_signal.connect( self.on_camera_list )
        a_widget.format_list_signal.connect( self.on_format_list )
        a_widget.ready_for_capture_signal.connect( self.on_ready_for_capture )
        a_widget.recording_signal.connect( self.on_recording_changed )
        self.camera_widget  = a_widget
        view_layout.addWidget( a_widget, 1 )

        self._build_thumb_column( view_layout )

        # ---- status line
        a_widget            = QLabel( "no camera" )
        self.status_widget  = a_widget
        layout.addWidget( a_widget )

        self._build_camera_buttons( layout )

        # ---- the combos were built before the widget existed, and the widget
        # emitted its first camera_list_signal in its own __init__, before
        # anything above was connected.  so fill them once, by hand, from the
        # widget.  after this the signals keep them up to date
        self.on_camera_list( self.camera_widget.camera_descriptions(),
                             self.camera_widget.device_ix() )
        self.on_format_list( self.camera_widget.format_descriptions(),
                             self.camera_widget.format_ix() )
        self.on_ready_for_capture( self.camera_widget.is_ready_for_capture() )

        # ---- where the files go.  the ONE thing the widget does not decide,
        # because it is an application question, not a camera question
        dir_layout          = QHBoxLayout(   )
        layout.addLayout( dir_layout )

        a_widget            = QLabel( "Save to: ( not set yet )" )
        self.save_dir_widget = a_widget
        dir_layout.addWidget( a_widget )

        a_widget            = QPushButton( "Change..." )
        a_widget.clicked.connect( self.on_change_save_dir )
        dir_layout.addWidget( a_widget )

        a_widget            = QPushButton( "Default" )
        a_widget.clicked.connect( self.on_default_save_dir )
        dir_layout.addWidget( a_widget )

        dir_layout.addStretch( 1 )

        # ---- buttons
        button_layout       = QHBoxLayout(   )
        layout.addLayout( button_layout )

        self.build_gui_last_buttons( button_layout )

    # ---- the camera controls, all of them this tab's ------------------------

    # -------------------------------------
    def _build_device_row( self, layout ):
        """
        what it says -- pick a camera, pick a format, start, stop.  the combos
        are filled from the widget, see on_camera_list / on_format_list
        """
        device_layout       = QHBoxLayout(   )
        layout.addLayout( device_layout )

        a_widget            = QLabel( "Camera" )
        device_layout.addWidget( a_widget )

        a_widget            = QComboBox(   )
        a_widget.setMinimumWidth( 240 )
        a_widget.currentIndexChanged.connect( self.on_device_combo_changed )
        self.device_combo   = a_widget
        device_layout.addWidget( a_widget )

        a_widget            = QLabel( "Format" )
        device_layout.addWidget( a_widget )

        a_widget            = QComboBox(   )
        a_widget.setMinimumWidth( 220 )
        a_widget.currentIndexChanged.connect( self.on_format_combo_changed )
        self.format_combo   = a_widget
        device_layout.addWidget( a_widget )

        device_layout.addStretch( 1 )

        a_widget            = QPushButton( "Start" )
        a_widget.clicked.connect( self.on_start_camera )
        device_layout.addWidget( a_widget )

        a_widget            = QPushButton( "Stop" )
        a_widget.clicked.connect( self.on_stop_camera )
        device_layout.addWidget( a_widget )

    # -------------------------------------
    def _build_thumb_column( self, layout ):
        """
        what it says -- the last still, beside the preview.  the widget hands
        over a QImage and this decides how big to show it, see on_still_image
        """
        thumb_layout        = QVBoxLayout(   )
        layout.addLayout( thumb_layout )

        a_widget            = QLabel( "last still" )
        thumb_layout.addWidget( a_widget )

        a_widget            = QLabel( "( none yet )" )
        a_widget.setFrameShape( QFrame.Shape.Box )
        a_widget.setAlignment( Qt.AlignmentFlag.AlignCenter )
        a_widget.setMinimumWidth( THUMB_WIDTH )
        self.thumb_widget   = a_widget
        thumb_layout.addWidget( a_widget )

        thumb_layout.addStretch( 1 )

    # -------------------------------------
    def _build_camera_buttons( self, layout ):
        """
        what it says -- snap and record.  the enabled state is not this tab's
        guess, it follows ready_for_capture_signal and recording_signal
        """
        button_layout       = QHBoxLayout(   )
        layout.addLayout( button_layout )

        # ---- "Snap Still"
        a_widget            = QPushButton( "Snap Still" )
        a_widget.clicked.connect( self.on_snap_still )
        self.snap_button    = a_widget
        button_layout.addWidget( a_widget )

        a_widget            = QPushButton( "Record Video" )
        a_widget.clicked.connect( self.on_record_video )
        self.record_button  = a_widget
        button_layout.addWidget( a_widget )

        a_widget            = QPushButton( "Stop Record" )
        a_widget.clicked.connect( self.on_stop_record )
        a_widget.setEnabled( False )
        self.stop_record_button = a_widget
        button_layout.addWidget( a_widget )

        button_layout.addStretch( 1 )

    # ---- controls -> widget ------------------------------------------------

    # -------------------------------------
    def on_device_combo_changed( self, ix ):
        """
        what it says -- the widget ignores an index it is already on, so a
        combo re-fill does not restart the camera
        """
        self.camera_widget.set_device_ix( ix )

    # -------------------------------------
    def on_format_combo_changed( self, ix ):
        """ what it says """
        self.camera_widget.set_format_ix( ix )

    # -------------------------------------
    def on_start_camera( self, ):
        """ what it says """
        self.camera_widget.start_camera()

    # -------------------------------------
    def on_stop_camera( self, ):
        """ what it says """
        self.camera_widget.stop_camera()

    # -------------------------------------
    def on_snap_still( self, ):
        """ what it says """
        self.camera_widget.snap_still()

    # -------------------------------------
    def on_record_video( self, ):
        """ what it says """
        self.camera_widget.record_video()

    # -------------------------------------
    def on_stop_record( self, ):
        """ what it says """
        self.camera_widget.stop_record()

    # ---- widget -> controls ------------------------------------------------

    # -------------------------------------
    def on_camera_list( self, a_list, ix ):
        """
        read it -- the cameras changed, or this is the first fill.  signals are
        blocked while the combo is loaded or setCurrentIndex would run back
        into the widget and restart a camera that is already right
        """
        self.device_combo.blockSignals( True )
        self.device_combo.clear()
        self.device_combo.addItems( a_list )
        self.device_combo.setCurrentIndex( ix )
        self.device_combo.blockSignals( False )

    # -------------------------------------
    def on_format_list( self, a_list, ix ):
        """ what it says -- as on_camera_list, for the format combo """
        self.format_combo.blockSignals( True )
        self.format_combo.clear()
        self.format_combo.addItems( a_list )
        self.format_combo.setCurrentIndex( ix )
        self.format_combo.blockSignals( False )

    # -------------------------------------
    def on_status_text( self, msg ):
        """ what it says -- one line of current state, not the msg log """
        self.status_widget.setText( msg )

    # -------------------------------------
    def on_still_image( self, a_image ):
        """
        what it says -- a QImage, in hand before the file is written, so the
        thumbnail can go up right away
        """
        a_pixmap            = QPixmap.fromImage( a_image )
        a_pixmap            = a_pixmap.scaledToWidth( THUMB_WIDTH,
                                                      Qt.TransformationMode.SmoothTransformation )
        self.thumb_widget.setPixmap( a_pixmap )

    # -------------------------------------
    def on_ready_for_capture( self, is_ready ):
        """ what it says -- no point offering a snap the backend would drop """
        self.snap_button.setEnabled( is_ready )

    # -------------------------------------
    def on_recording_changed( self, is_recording ):
        """ what it says """
        self.record_button.setEnabled( not is_recording )
        self.stop_record_button.setEnabled( is_recording )

    # ---- where files go ----------------------------------------------------

    # -------------------------------------
    def _start_save_dir( self, ):
        """
        read it -- the app's own output directory, parameters.PARAMETERS.output_dir
        ( "./output" as it stands ), with a camera sub directory under it.

        imported and read lazily rather than at module import time: PARAMETERS
        is built while the app starts, and this module gets imported by the tab
        machinery, so reading it at import time is asking for a None.  the
        fallback keeps the tab usable outside the app, eg in a test harness
        """
        output_dir          = DEFAULT_OUTPUT

        try:
            import parameters
            if parameters.PARAMETERS is not None:
                output_dir          = parameters.PARAMETERS.output_dir
        except Exception:
            pass            # no app around, the default will do

        return os.path.join( output_dir, CAMERA_SUB_DIR )

    # -------------------------------------
    def _apply_save_dir( self, a_dir ):
        """
        what it says -- tell the widget, then say so.  the widget makes the
        directory if it is missing and hands back what it used
        """
        a_dir               = self.camera_widget.set_save_dir( a_dir )

        self.save_dir_widget.setText( f"Save to: {a_dir}" )
        self.append_msg( f"captures will be saved to {os.path.abspath( a_dir )}" )

    # -------------------------------------
    def on_change_save_dir( self, ):
        """ what it says """
        a_dir               = QFileDialog.getExistingDirectory( self, "Save captures to",
                                                                self.camera_widget.save_dir() )
        if not a_dir:
            return

        self._apply_save_dir( a_dir )

    # -------------------------------------
    def on_default_save_dir( self, ):
        """ what it says -- back to the one from parameters """
        self._apply_save_dir( self._start_save_dir() )

    # ---- what the widget tells us ------------------------------------------

    # -------------------------------------
    def on_image_saved( self, file_name ):
        """
        what it says -- the widget already said "saved: ..." through
        status_message_signal, this is the hook for anything the APPLICATION
        wants to do with a new still.  nothing yet

        ?? add it to a gallery, or to the project's db, or show it in the
           image overlay tab as a base image ?
        """
        pass

    # -------------------------------------
    def on_video_saved( self, file_name ):
        """
        what it says -- as on_image_saved, for recordings

        ?? hand it to tab_vlc_qt_widget to play back ?
        """
        pass

    # ------------------------------------
    def mutate_0( self ):
        """
        read it -- mutate the widgets
        """
        self.append_function_msg( "mutate_0" )

        self.append_function_msg( "no code for mutates so far " )

        self.append_msg( tab_base.DONE_MSG )

    # ------------------------
    def inspect(self):
        """
        the usual
        """
        self.append_function_msg( "inspect" )
        # make some locals for inspection

        self_camera_widget   = self.camera_widget
        self_save_dir        = self.camera_widget.save_dir()
        self_camera_count    = self.camera_widget.camera_count()
        self_camera_desc     = self.camera_widget.current_camera_description()
        self_last_file       = self.camera_widget.last_file_name()
        self_is_recording    = self.camera_widget.is_recording()

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
