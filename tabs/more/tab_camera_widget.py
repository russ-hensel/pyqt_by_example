#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ---- tof
"""
tab_camera_widget.py
self.help_file_name     =  "tab_camera_widget.txt"

KEY_WORDS:      WebCam camera still image video qt6 QMediaCaptureSession QImageCapture QMediaRecorder
CLASS_NAME:     QCameraWidgetTab
WIDGETS:        QVideoWidget,
STATUS:         QT6 ONLY -- will not import under PyQt5, which is what the app runs on today
TAB_TITLE:      Camera / Webcam - qt6 only
DESCRIPTION:    webcam: live preview, still shots to a file, and video recording,
MORE:               built on the Qt6 QMediaCaptureSession.  the Qt5 camera api
                shares no classes with this one, so this tab can not run until
                the whole app moves to Qt6.  clicking it under PyQt5 raises
                ImportError on QMediaCaptureSession -- that is expected
HOW_COMPLETE:   22  #  AND A COMMENT -- <10 major probs  <15 runs but <20 fair not finished  <=25 not to shabby
"""
WIKI_LINK      =  "https://github.com/russ-hensel/pyqt_by_example/wiki/Camera Webcam Widget"


# --------------------
if __name__ == "__main__":
    #----- run the full app
    import main   # noqa  stops auto removal by pycln
# --------------------


import os
from   datetime import datetime

# !! this has to happen BEFORE QtMultimedia is imported, the ffmpeg backend
# reads it while starting up.  without it recording fails on this machine:
# qt finds a vaapi device and insists on the gpu encoders, but the driver has
# no working encode entrypoint --
#     Couldn't open video encoder "h264_vaapi" ; result: Function not implemented
#     No valid video codecs found          -> ResourceError, a 0 byte file
# empty means software encoding only, which works.  ?? in a tab this is a bit
# late -- if some other tab has already pulled in QtMultimedia the backend is
# up and this does nothing.  main.py may be the honest place for it
os.environ.setdefault( "QT_FFMPEG_ENCODING_HW_DEVICE_TYPES", "" )

from qtpy.QtCore import ( Qt, QTimer, QUrl )
from qtpy.QtGui  import ( QPixmap )
from qtpy.QtMultimedia import ( QCamera,
                                QImageCapture,
                                QMediaCaptureSession,
                                QMediaDevices,
                                QMediaFormat,
                                QMediaRecorder,
                                )

from qtpy.QtMultimediaWidgets import QVideoWidget

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
import parameters


# ---- end imports

#basedir         = os.path.dirname( os.path.abspath( __file__ ) )

NO_CAMERA_MSG   = ( "no camera found -- is one plugged in ?" )
THUMB_WIDTH     = 160


# -----------------------------------------------
def enum_name( a_value ):
    """
    what it says -- a readable name out of a qt enum member, PyQt6 gives
    python enums ( .name ), PySide6 does not always, so fall back to the
    tail of str()
    """
    a_name              = getattr( a_value, "name", None )

    if a_name is not None:
        return a_name

    return str( a_value ).split( "." )[ -1 ]


# -----------------------------------------------
class QCameraWidgetTab( tab_base.TabBase ):
    """
    here build a tab in its own class to hide its variables

    the Qt6 shape of a camera is a QMediaCaptureSession in the middle with
    everything else hung off it:

        QCamera ---> QMediaCaptureSession ---> QVideoWidget   ( preview )
                          |    |
                          |    +-----------> QImageCapture    ( stills )
                          +----------------> QMediaRecorder   ( video )

    the session is built once and lives for the life of the tab, only the
    QCamera is swapped when the device or the format changes.  unlike Qt5
    there is no capture *mode* -- stills and recording are separate objects on
    the same session, so a still can be grabbed while recording runs
    """

    def __init__( self, ):
        """
        """
        super().__init__( )

        self.module_file        = __file__      # save for help file usage

        global WIKI_LINK
        self.wiki_link          = WIKI_LINK

        self.mutate_dict[0]     = self.mutate_0
        #self.mutate_dict[1]     = self.mutate_1

        self.capture_session    = None      # QMediaCaptureSession, the hub, built once
        self.camera             = None      # QCamera, made fresh when the device changes
        self.image_capture      = None      # QImageCapture, built once
        self.media_recorder     = None      # QMediaRecorder, built once

        self.camera_devices     = []        # QCameraDevice list, index matches the device combo
        self.camera_formats     = []        # QCameraFormat list, index matches the format combo

        self.is_recording       = False
        self.last_file_name     = ""

        # what _poll_recorder has already reported, so it only speaks on a change
        self.last_recorder_state = None
        self.last_recorder_error = None

        # QMediaDevices has to be kept alive to get its hot plug signal, a
        # temporary would emit nothing
        self.media_devices      = QMediaDevices( self )
        self.media_devices.videoInputsChanged.connect( self.on_video_inputs_changed )

        # claude, and I changed
        #self.save_dir           = os.path.join( basedir, "output", "camera" )
        self.save_dir           = os.path.join( parameters.PARAMETERS.output_dir )
        os.makedirs( self.save_dir, exist_ok = True )

        self.help_file_name     =  "tab_camera_widget.txt"
        self._build_gui()

        # only now, TabBase builds msg_widget in _build_gui_bot, so anything
        # that calls append_msg has to wait until _build_gui has finished
        self._load_camera_list()

        # and start a beat later still -- the video widget wants to be a real,
        # shown widget before the backend renders into it, and this __init__
        # runs before the main window has shown anything
        QTimer.singleShot( 0, self.start_camera )

    #----------------------------
    def _build_gui_widgets( self, main_layout ):
        """
        the usual, build the gui with the widgets of interest
        and the buttons for examples
        """
        layout              = QVBoxLayout(   )
        main_layout.addLayout( layout )

        # ---- device row
        device_layout       = QHBoxLayout(   )
        layout.addLayout( device_layout )

        a_widget            = QLabel( "Camera" )
        device_layout.addWidget( a_widget )

        a_widget            = QComboBox(   )
        a_widget.setMinimumWidth( 240 )
        a_widget.currentIndexChanged.connect( self.on_device_changed )
        self.device_combo   = a_widget
        device_layout.addWidget( a_widget )

        a_widget            = QLabel( "Format" )
        device_layout.addWidget( a_widget )

        a_widget            = QComboBox(   )
        a_widget.setMinimumWidth( 220 )
        a_widget.currentIndexChanged.connect( self.on_format_changed )
        self.format_combo   = a_widget
        device_layout.addWidget( a_widget )

        device_layout.addStretch( 1 )

        a_widget            = QPushButton( "Start" )
        a_widget.clicked.connect( self.start_camera )
        device_layout.addWidget( a_widget )

        a_widget            = QPushButton( "Stop" )
        a_widget.clicked.connect( self.stop_camera )
        device_layout.addWidget( a_widget )

        # ---- preview + last still, side by side
        view_layout         = QHBoxLayout(   )
        layout.addLayout( view_layout )

        # the backend paints into this one, it is not an ordinary qt painted
        # surface, so there is no point styling it
        a_widget            = QVideoWidget(   )
        a_widget.setMinimumSize( 480, 360 )
        self.video_widget   = a_widget
        view_layout.addWidget( a_widget, 1 )

        thumb_layout        = QVBoxLayout(   )
        view_layout.addLayout( thumb_layout )

        a_widget            = QLabel( "last still" )
        thumb_layout.addWidget( a_widget )

        a_widget            = QLabel( "( none yet )" )
        a_widget.setFrameShape( QFrame.Shape.Box )
        a_widget.setAlignment( Qt.AlignmentFlag.AlignCenter )
        a_widget.setMinimumWidth( THUMB_WIDTH )
        self.thumb_widget   = a_widget
        thumb_layout.addWidget( a_widget )

        thumb_layout.addStretch( 1 )

        # ---- the capture session, hub of the whole thing.  built once, the
        # camera is what gets swapped later, see start_camera
        capture_session     = QMediaCaptureSession( self )
        capture_session.setVideoOutput( self.video_widget )
        self.capture_session = capture_session

        image_capture       = QImageCapture( self )
        image_capture.imageCaptured.connect( self.on_image_captured )
        image_capture.imageSaved.connect( self.on_image_saved )
        image_capture.errorOccurred.connect( self.on_capture_error )
        image_capture.readyForCaptureChanged.connect( self.on_ready_for_capture_changed )
        capture_session.setImageCapture( image_capture )
        self.image_capture  = image_capture

        # !! QMediaRecorder.recorderStateChanged and .errorOccurred can NOT be
        # connected in this env -- PyQt6 6.11.0 bindings against PyQt6-Qt6
        # 6.11.1 libs, and QMediaRecorder gained a signal in that patch release,
        # so PyQt's signal lookups for this one class miss:
        #     connect() failed between (QMediaRecorder::RecorderState) and unislot()
        # every other signal used here connects fine, including the enum
        # carrying QCamera.errorOccurred and QImageCapture.errorOccurred.
        # so recorder state and error are polled instead, see _poll_recorder --
        # same trick tab_vlc_qt_widget.py uses for the position slider.
        # fix the env and the two connects can replace the timer:
        #     uv pip install "PyQt6-Qt6==6.11.0"
        media_recorder      = QMediaRecorder( self )
        media_recorder.durationChanged.connect( self.on_duration_changed )
        media_recorder.actualLocationChanged.connect( self.on_actual_location_changed )
        capture_session.setRecorder( media_recorder )
        self.media_recorder = media_recorder

        # only runs while recording, see on_record_video
        recorder_timer      = QTimer( self )
        recorder_timer.setInterval( 250 )
        recorder_timer.timeout.connect( self._poll_recorder )
        self.recorder_timer = recorder_timer

        # ---- status line
        a_widget            = QLabel( "no camera" )
        self.status_widget  = a_widget
        layout.addWidget( a_widget )

        # ---- where the files go
        dir_layout          = QHBoxLayout(   )
        layout.addLayout( dir_layout )

        a_widget            = QLabel( f"Save to: {self.save_dir}" )
        self.save_dir_widget = a_widget
        dir_layout.addWidget( a_widget )

        a_widget            = QPushButton( "Change..." )
        a_widget.clicked.connect( self.on_change_save_dir )
        dir_layout.addWidget( a_widget )

        dir_layout.addStretch( 1 )

        # ---- buttons
        button_layout       = QHBoxLayout(   )
        layout.addLayout( button_layout )

        a_widget            = QPushButton( "Snap\nStill" )
        a_widget.clicked.connect( self.on_snap_still )
        self.snap_button    = a_widget
        button_layout.addWidget( a_widget )

        a_widget            = QPushButton( "Record\nVideo" )
        a_widget.clicked.connect( self.on_record_video )
        self.record_button  = a_widget
        button_layout.addWidget( a_widget )

        a_widget            = QPushButton( "Stop\nRecord" )
        a_widget.clicked.connect( self.on_stop_record )
        a_widget.setEnabled( False )
        self.stop_record_button = a_widget
        button_layout.addWidget( a_widget )

        self.build_gui_last_buttons( button_layout )

    # ---- devices and formats -----------------------------------------------

    # -------------------------------------
    def _load_camera_list( self, ):
        """
        what it says -- fill the device combo from QMediaDevices.videoInputs().
        signals are blocked so filling it does not trip on_device_changed
        before there is anything to change to
        """
        camera_devices      = QMediaDevices.videoInputs()
        self.camera_devices = camera_devices

        self.device_combo.blockSignals( True )
        self.device_combo.clear()

        default_ix          = 0
        for ix, i_device in enumerate( camera_devices ):
            self.device_combo.addItem( i_device.description() )
            if i_device.isDefault():
                default_ix          = ix

        self.device_combo.setCurrentIndex( default_ix )
        self.device_combo.blockSignals( False )

        if not camera_devices:
            self.append_msg( NO_CAMERA_MSG )
            self.status_widget.setText( NO_CAMERA_MSG )
            self.snap_button.setEnabled( False )
            self.record_button.setEnabled( False )
            self.format_combo.clear()
            return

        msg                 = ( f"found {len( camera_devices )} camera(s)" )
        self.append_msg( msg )

        self._load_format_list()

    # -------------------------------------
    def _load_format_list( self, ):
        """
        read it -- a QCameraDevice carries a list of QCameraFormat, each one a
        resolution + pixel format + frame rate range the device really supports.
        the webcam this was written against offers 14 of them.  biggest first,
        they read better that way

        ?? worth filtering the silly ones, 1920x1080 YUYV runs at 5 fps
        """
        camera_device       = self._current_camera_device()

        self.format_combo.blockSignals( True )
        self.format_combo.clear()

        if camera_device is None:
            self.camera_formats = []
            self.format_combo.blockSignals( False )
            return

        camera_formats      = list( camera_device.videoFormats() )
        camera_formats.sort( key = lambda a_format: ( a_format.resolution().width()
                                                      * a_format.resolution().height(),
                                                      a_format.maxFrameRate() ),
                             reverse = True )
        self.camera_formats = camera_formats

        for i_format in camera_formats:
            a_size              = i_format.resolution()
            msg                 = ( f"{a_size.width()}x{a_size.height()}  "
                                    f"{enum_name( i_format.pixelFormat() ).replace( 'Format_', '' )}  "
                                    f"{i_format.maxFrameRate():.0f} fps" )
            self.format_combo.addItem( msg )

        self.format_combo.blockSignals( False )

    # -------------------------------------
    def _current_camera_device( self, ):
        """
        what it says -- the QCameraDevice the combo points at, or None
        """
        ix                  = self.device_combo.currentIndex()

        if ix < 0 or ix >= len( self.camera_devices ):
            return None

        return self.camera_devices[ ix ]

    # -------------------------------------
    def _current_camera_format( self, ):
        """
        what it says -- the QCameraFormat the combo points at, or None
        """
        ix                  = self.format_combo.currentIndex()

        if ix < 0 or ix >= len( self.camera_formats ):
            return None

        return self.camera_formats[ ix ]

    # ---- camera ------------------------------------------------------------

    # -------------------------------------
    def start_camera( self, ):
        """
        read it -- a QCamera is bound to one device for its life, so changing
        device means a new one.  the session, the image capture and the
        recorder all survive that, only setCamera() changes
        """
        camera_device       = self._current_camera_device()

        if camera_device is None:
            self.append_msg( NO_CAMERA_MSG )
            return

        self.stop_camera()

        camera              = QCamera( camera_device, self )
        camera.errorOccurred.connect( self.on_camera_error )
        camera.activeChanged.connect( self.on_camera_active_changed )

        camera_format       = self._current_camera_format()
        if camera_format is not None:
            camera.setCameraFormat( camera_format )

        self.capture_session.setCamera( camera )
        self.camera         = camera

        camera.start()

        msg                 = ( f"started {camera_device.description()}" )
        self.append_msg( msg )

    # -------------------------------------
    def stop_camera( self, ):
        """
        what it says -- also drops the QCamera, see start_camera
        """
        if self.camera is None:
            return

        if self.is_recording:
            self.on_stop_record()

        self.camera.stop()
        self.capture_session.setCamera( None )      # or the session holds a dead camera
        self.camera.deleteLater()
        self.camera         = None

        self.status_widget.setText( "camera stopped" )

    # -------------------------------------
    def on_device_changed( self, ix ):
        """
        what it says -- ix is the combo index, unused, the getters read it back.
        a new device means a new format list too
        """
        self._load_format_list()
        self.start_camera()

    # -------------------------------------
    def on_format_changed( self, ix ):
        """
        what it says -- ix is the combo index, unused.  the format is handed to
        the camera at construction time, so this is a restart
        """
        if self.camera is not None:
            self.start_camera()

    # -------------------------------------
    def on_video_inputs_changed( self, ):
        """
        what it says -- a camera was plugged in or pulled out.  rebuild the
        list, and restart only if the selected device actually changed
        """
        self.append_msg( "video inputs changed -- re-reading the camera list" )

        old_id              = None
        camera_device       = self._current_camera_device()
        if camera_device is not None:
            old_id              = camera_device.id()

        self._load_camera_list()

        camera_device       = self._current_camera_device()
        new_id              = camera_device.id() if camera_device is not None else None

        if new_id != old_id:
            self.start_camera()

    # -------------------------------------
    def on_camera_active_changed( self, is_active ):
        """
        what it says --
        """
        msg                 = "camera active" if is_active else "camera inactive"
        self.status_widget.setText( msg )

    # -------------------------------------
    def on_camera_error( self, error, error_string ):
        """
        what it says --
        """
        msg                 = ( f"camera error {enum_name( error )}: {error_string}" )
        self.append_msg( msg )
        self.status_widget.setText( msg )

    # ---- still images ------------------------------------------------------

    # -------------------------------------
    def on_snap_still( self, ):
        """
        read it -- the capture is asynchronous.  captureToFile() only asks, and
        answers come back twice: imageCaptured with the image itself ( good for
        a thumbnail, it arrives first ) and then imageSaved once the file is
        really on disk.  no extension is given, the backend picks one
        """
        if self.camera is None:
            self.append_msg( "no camera running -- click Start" )
            return

        if not self.image_capture.isReadyForCapture():
            self.append_msg( "camera not ready for capture yet -- try again in a moment" )
            return

        file_name           = os.path.join( self.save_dir, f"still_{self._time_stamp()}" )
        capture_id          = self.image_capture.captureToFile( file_name )

        msg                 = ( f"capture {capture_id} asked for: {file_name}" )
        self.append_msg( msg )

    # -------------------------------------
    def on_image_captured( self, capture_id, a_image ):
        """
        what it says -- a_image is a QImage, in hand before the file is written,
        so the thumbnail can go up right away
        """
        a_pixmap            = QPixmap.fromImage( a_image )
        a_pixmap            = a_pixmap.scaledToWidth( THUMB_WIDTH,
                                                      Qt.TransformationMode.SmoothTransformation )
        self.thumb_widget.setPixmap( a_pixmap )

    # -------------------------------------
    def on_image_saved( self, capture_id, file_name ):
        """
        what it says -- the file is on disk by now, file_name is the real one
        the backend chose, extension and all
        """
        self.last_file_name = file_name

        msg                 = ( f"saved: {file_name}" )
        self.append_msg( msg )
        self.status_widget.setText( msg )

    # -------------------------------------
    def on_capture_error( self, capture_id, error, error_string ):
        """
        what it says --
        """
        msg                 = ( f"capture error {enum_name( error )}: {error_string}" )
        self.append_msg( msg )
        self.status_widget.setText( msg )

    # -------------------------------------
    def on_ready_for_capture_changed( self, is_ready ):
        """
        what it says -- the snap button follows the camera, a capture asked for
        while the backend is not ready is just dropped
        """
        self.snap_button.setEnabled( is_ready )

    # ---- video -------------------------------------------------------------

    # -------------------------------------
    def on_record_video( self, ):
        """
        read it -- no capture mode to switch, unlike Qt5: the recorder is its
        own object on the session and stills keep working while it runs.
        the extension is left off, actualLocation() reports what was really used
        """
        if self.camera is None:
            self.append_msg( "no camera running -- click Start" )
            return

        if self.is_recording:
            self.append_msg( "already recording" )
            return

        # asking for h264 in an mp4 is the safe pick, but the ffmpeg qt ships
        # is LGPL and has no h264 encoder, so qt quietly substitutes MPEG4 (
        # part 2 ) -- still an .mp4, still plays anywhere.  the log line
        # "Recording new media with muxer ..." says what was really used
        a_format            = QMediaFormat( QMediaFormat.FileFormat.MPEG4 )
        a_format.setVideoCodec( QMediaFormat.VideoCodec.H264 )
        self.media_recorder.setMediaFormat( a_format )

        file_name           = os.path.join( self.save_dir, f"video_{self._time_stamp()}" )
        self.media_recorder.setOutputLocation( QUrl.fromLocalFile( file_name ) )
        self.media_recorder.record()

        self.is_recording   = True
        self.record_button.setEnabled( False )
        self.stop_record_button.setEnabled( True )

        self.last_recorder_state = None     # so the first poll reports whatever it finds
        self.last_recorder_error = None
        self.recorder_timer.start()

        msg                 = ( f"record asked for: {file_name}" )
        self.append_msg( msg )

    # -------------------------------------
    def on_stop_record( self, ):
        """
        what it says --
        """
        if not self.is_recording:
            return

        self.media_recorder.stop()

        self.is_recording   = False
        self.record_button.setEnabled( True )
        self.stop_record_button.setEnabled( False )

        # the timer runs on a little past the stop, the backend needs a moment
        # to finalize the file and only then does the state settle
        QTimer.singleShot( 1500, self.recorder_timer.stop )

    # -------------------------------------
    def _poll_recorder( self, ):
        """
        read it -- stands in for recorderStateChanged and errorOccurred, which
        can not be connected in this env ( see the !! note in _build_gui_widgets ).
        only speaks when something actually changed, or the msg box would fill
        with the same line four times a second
        """
        state               = self.media_recorder.recorderState()

        if state != self.last_recorder_state:
            self.last_recorder_state = state
            self.on_recorder_state_changed( state )

        error               = self.media_recorder.error()

        if error != QMediaRecorder.Error.NoError and error != self.last_recorder_error:
            self.last_recorder_error = error
            self.on_recorder_error( error, self.media_recorder.errorString() )

    # -------------------------------------
    def on_recorder_state_changed( self, state ):
        """
        what it says -- state is a QMediaRecorder.RecorderState.  called from
        _poll_recorder, not from a signal, see the !! note in _build_gui_widgets
        """
        msg                 = ( f"recorder: {enum_name( state )}" )
        self.append_msg( msg )
        self.status_widget.setText( msg )

    # -------------------------------------
    def on_actual_location_changed( self, a_url ):
        """
        what it says -- the backend reports the file it really wrote, extension
        and all, once it has settled on one
        """
        file_name           = a_url.toLocalFile()

        if not file_name:
            return

        self.last_file_name = file_name
        self.append_msg( f"recorded: {file_name}" )

    # -------------------------------------
    def on_duration_changed( self, duration ):
        """
        what it says -- duration is ms, only interesting while recording
        """
        if not self.is_recording:
            return

        self.status_widget.setText( f"recording  {duration / 1000:.1f} sec" )

    # -------------------------------------
    def on_recorder_error( self, error, error_string ):
        """
        what it says --
        """
        msg                 = ( f"recorder error {enum_name( error )}: {error_string}" )
        self.append_msg( msg )
        self.status_widget.setText( msg )

    # ---- odds and ends -----------------------------------------------------

    # -------------------------------------
    def _time_stamp( self, ):
        """
        what it says -- sortable, no characters that annoy a file system
        """
        return datetime.now().strftime( "%Y%m%d_%H%M%S" )

    # -------------------------------------
    def on_change_save_dir( self, ):
        """
        what it says --
        """
        a_dir               = QFileDialog.getExistingDirectory( self, "Save captures to", self.save_dir )

        if not a_dir:
            return

        self.save_dir       = a_dir
        self.save_dir_widget.setText( f"Save to: {a_dir}" )

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

        self_capture_session = self.capture_session
        self_camera          = self.camera
        self_image_capture   = self.image_capture
        self_media_recorder  = self.media_recorder
        self_camera_devices  = self.camera_devices
        self_camera_formats  = self.camera_formats
        self_video_widget    = self.video_widget

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
