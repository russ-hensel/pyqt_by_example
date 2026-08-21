#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ---- tof
# we do not run from here, run the tab
#   /pyqt_by_example/tabs/more/tab_camera_widget_object.py
"""
camera_capture_widget.py

a self contained webcam widget: the live preview and nothing else on screen.
everything about *driving* a camera lives in here -- device list, format list,
start, stop, stills, recording -- but the controls that work it belong to the
host, which builds its own combos and buttons and calls the methods below.

    what is on screen
        one QVideoWidget, the preview.  that is all.

        it used to bring its own device and format combos, start / stop, a
        thumbnail of the last still, a status line and three action buttons.
        that made it easy to drop in but gave every host the same gui whether
        it wanted it or not, so the controls moved out to the host and only
        the camera logic stayed.  the host drives it through the api and hears
        back through the signals

this is the object pulled out of tab_camera_widget.py -- that tab does the
same job with all this plumbing inline.  same pattern as vlc_widget.VlcVideoWidget
behind tab_vlc_qt_object_widget.py.

NOT called camera_widget.py on purpose: there is already a camera_widget.py in
the project root ( the stand alone Qt6 version ) and two modules of the same
name on the path would be a coin toss as to which one gets imported.

    the api
        start_camera()  stop_camera()
        snap_still()
        record_video()  stop_record()   is_recording()
        set_save_dir( a_dir )  /  save_dir()
        camera_count()  current_camera_description()
        last_file_name()

        -- for the host's combos
        camera_descriptions()  /  device_ix()  /  set_device_ix( ix )
        format_descriptions()  /  format_ix()  /  set_format_ix( ix )
        is_ready_for_capture()

    the signals -- a host wires these to its own gui
        status_message_signal( str )    anything worth saying out loud
        status_text_signal( str )       one line of current state, for a status label
        image_saved_signal( str )       a still landed, arg is the file name
        video_saved_signal( str )       a recording landed, arg is the file name
        still_image_signal( QImage )    the still itself, in hand before the file is
        camera_list_signal( list, int ) device descriptions changed, and which to show
        format_list_signal( list, int ) format descriptions changed, and which to show
        ready_for_capture_signal( bool )  enable / disable a snap button
        recording_signal( bool )        recording started / stopped

    a host that connects its signals AFTER construction ( the normal case ) has
    missed the first camera_list_signal, so it fills its combos from
    camera_descriptions() / format_descriptions() once, then follows the signals

QT6 ONLY.  QMediaCaptureSession, QImageCapture and QVideoWidget do not exist in
Qt5, whose camera api shares no classes with this one.  the app is PyQt5 today,
so importing this raises ImportError there -- expected, see the tab's .txt

the widget deliberately knows nothing about the app: no parameters, no
global_vars, no tab_base.  where captures are saved is the host's business,
handed in with set_save_dir
"""

import os
from   datetime import datetime

# !! this has to happen BEFORE QtMultimedia is imported, the ffmpeg backend
# reads it while starting up.  without it recording fails on this machine:
# qt finds a vaapi device and insists on the gpu encoders, but the driver has
# no working encode entrypoint --
#     Couldn't open video encoder "h264_vaapi" ; result: Function not implemented
#     No valid video codecs found          -> ResourceError, a 0 byte file
# empty means software encoding only, which works.  ?? still a bit late if
# some other tab pulled in QtMultimedia first -- main.py is the honest place
os.environ.setdefault( "QT_FFMPEG_ENCODING_HW_DEVICE_TYPES", "" )

from qtpy.QtCore import ( QTimer, QUrl, Signal )
from qtpy.QtGui  import ( QImage )
from qtpy.QtMultimedia import ( QCamera,
                                QImageCapture,
                                QMediaCaptureSession,
                                QMediaDevices,
                                QMediaFormat,
                                QMediaRecorder,
                                )
from qtpy.QtMultimediaWidgets import QVideoWidget
from qtpy.QtWidgets import ( QVBoxLayout,
                             QWidget,
                             )

# ---- end imports

NO_CAMERA_MSG   = ( "no camera found -- is one plugged in ?" )


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
class CameraCaptureWidget( QWidget ):
    """
    the whole camera, in one widget -- the machinery, not the control panel.

    the Qt6 shape of a camera is a QMediaCaptureSession in the middle with
    everything else hung off it:

        QCamera ---> QMediaCaptureSession ---> QVideoWidget   ( preview )
                          |    |
                          |    +-----------> QImageCapture    ( stills )
                          +----------------> QMediaRecorder   ( video )

    the session is built once and lives for the life of the widget, only the
    QCamera is swapped when the device or the format changes.  unlike Qt5
    there is no capture *mode* -- stills and recording are separate objects on
    the same session, so a still can be grabbed while recording runs

    the selected device and format are plain ints here ( a_device_ix,
    a_format_ix ), not the current index of some combo box the widget owns.
    a host combo writes them with set_device_ix / set_format_ix and reads the
    lists out of camera_descriptions() / format_descriptions()
    """

    status_message_signal   = Signal( str )
    status_text_signal      = Signal( str )
    image_saved_signal      = Signal( str )
    video_saved_signal      = Signal( str )
    still_image_signal      = Signal( QImage )
    camera_list_signal      = Signal( list, int )
    format_list_signal      = Signal( list, int )
    ready_for_capture_signal = Signal( bool )
    recording_signal        = Signal( bool )

    def __init__( self, parent = None ):
        """
        """
        super().__init__( parent )

        self.capture_session    = None      # QMediaCaptureSession, the hub, built once
        self.camera             = None      # QCamera, made fresh when the device changes
        self.image_capture      = None      # QImageCapture, built once
        self.media_recorder     = None      # QMediaRecorder, built once

        self.camera_devices     = []        # QCameraDevice list, index matches a_device_ix
        self.camera_formats     = []        # QCameraFormat list, index matches a_format_ix

        self.a_device_ix        = -1        # what used to be device_combo.currentIndex()
        self.a_format_ix        = -1        # what used to be format_combo.currentIndex()

        self.is_recording_now   = False
        self.last_file          = ""

        # what _poll_recorder has already reported, so it only speaks on a change
        self.last_recorder_state = None
        self.last_recorder_error = None

        # where captures go.  the host is expected to set this, see set_save_dir
        self.a_save_dir         = os.getcwd()

        # QMediaDevices has to be kept alive to get its hot plug signal, a
        # temporary would emit nothing
        self.media_devices      = QMediaDevices( self )
        self.media_devices.videoInputsChanged.connect( self.on_video_inputs_changed )

        self._build_gui()
        self._build_capture_session()
        self._load_camera_list()

        # start a beat later -- the video widget wants to be a real, shown
        # widget before the backend renders into it, and a host's __init__
        # usually runs before anything has been shown
        QTimer.singleShot( 0, self.start_camera )

    # -------------------------------
    def _say( self, msg ):
        """
        what it says -- one place, so every message leaves by the same door.
        a host connects status_message_signal to its own msg area
        """
        self.status_message_signal.emit( msg )

    # -------------------------------
    def _status( self, msg ):
        """
        what it says -- what used to be status_widget.setText().  the status
        label belongs to the host now, so this is a signal like everything else
        """
        self.status_text_signal.emit( msg )

    # ---- gui ---------------------------------------------------------------

    # -------------------------------
    def _build_gui( self, ):
        """
        the usual, build the gui -- which is now one QVideoWidget and no more.
        the layout is kept ( rather than making this class a QVideoWidget )
        so the widget stays an ordinary QWidget a host can subclass or add to

        the margins are zeroed: the host has its own spacing around this and a
        second set of margins just wastes preview area
        """
        layout              = QVBoxLayout( self )
        layout.setContentsMargins( 0, 0, 0, 0 )

        # ---- QVideoWidget
        # the backend paints into this one, it is not an ordinary qt painted
        # surface, so there is no point styling it
        a_widget            = QVideoWidget(   )
        a_widget.setMinimumSize( 480, 360 )
        self.video_widget   = a_widget
        layout.addWidget( a_widget, 1 )

    # -------------------------------
    def _build_capture_session( self, ):
        """
        read it -- no gui here, this is the qt multimedia object graph in the
        class doc string.  built once, the QCamera is what gets swapped later,
        see start_camera
        """
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
        # so recorder state and error are polled instead, see _poll_recorder.
        # fix the env and the two connects can replace the timer:
        #     uv pip install "PyQt6-Qt6==6.11.0"
        media_recorder      = QMediaRecorder( self )
        media_recorder.durationChanged.connect( self.on_duration_changed )
        media_recorder.actualLocationChanged.connect( self.on_actual_location_changed )
        capture_session.setRecorder( media_recorder )
        self.media_recorder = media_recorder

        # only runs while recording, see record_video
        recorder_timer      = QTimer( self )
        recorder_timer.setInterval( 250 )
        recorder_timer.timeout.connect( self._poll_recorder )
        self.recorder_timer = recorder_timer

    # ---- where files go ----------------------------------------------------

    # -------------------------------
    def set_save_dir( self, a_dir ):
        """
        read it -- the host says where captures land.  the widget has no
        opinion and no access to the app's parameters, which is what keeps it
        re-usable.  the directory is made if it is missing.

        !! the abspath is NOT tidiness, it is required.  hand qt a relative
        path and both of these fail, even though the directory exists:
            QImageCapture  -> ResourceError "Cannot open device for writing"
            QMediaRecorder -> LocationNotWritable
        QUrl.fromLocalFile() on a relative path does not make a usable file
        url, and captureToFile() is no better.  the app's own output_dir is
        "./output", ie relative, so any host passing it straight through would
        hit this.  normalised here, once, so no host has to remember

        returns the directory actually used, absolute
        """
        a_dir               = os.path.abspath( str( a_dir ) )
        os.makedirs( a_dir, exist_ok = True )

        self.a_save_dir     = a_dir

        return a_dir

    # -------------------------------
    def save_dir( self, ):
        """
        what it says
            better might be just to read it
            or @property
        """
        return self.a_save_dir

    # -------------------------------
    def last_file_name( self, ):
        """
        what it says -- the most recent still or recording, "" if none
            better might be just to read it
            or @property
        """
        return self.last_file

    # ---- devices and formats -----------------------------------------------

    # -------------------------------
    def _load_camera_list( self, ):
        """
        what it says -- re-read QMediaDevices.videoInputs() and tell the host
        what is there now, with the index it should show.  the default device
        is picked, which is what the old combo did while its signals were
        blocked
        """
        camera_devices      = QMediaDevices.videoInputs()
        self.camera_devices = camera_devices

        default_ix          = 0
        for ix, i_device in enumerate( camera_devices ):
            if i_device.isDefault():
                default_ix          = ix

        if not camera_devices:
            self.a_device_ix    = -1
            self.camera_formats = []
            self.a_format_ix    = -1

            self.camera_list_signal.emit( [], -1 )
            self.format_list_signal.emit( [], -1 )
            self.ready_for_capture_signal.emit( False )

            self._say( NO_CAMERA_MSG )
            self._status( NO_CAMERA_MSG )
            return

        self.a_device_ix    = default_ix
        self.camera_list_signal.emit( self.camera_descriptions(), default_ix )

        self._say( f"found {len( camera_devices )} camera(s)" )

        self._load_format_list()

    # -------------------------------
    def _load_format_list( self, ):
        """
        read it -- a QCameraDevice carries a list of QCameraFormat, each one a
        resolution + pixel format + frame rate range the device really supports.
        the webcam this was written against offers 14 of them.  biggest first,
        they read better that way

        ?? worth filtering the silly ones, 1920x1080 YUYV runs at 5 fps
        """
        camera_device       = self._current_camera_device()

        if camera_device is None:
            self.camera_formats = []
            self.a_format_ix    = -1
            self.format_list_signal.emit( [], -1 )
            return

        camera_formats      = list( camera_device.videoFormats() )
        camera_formats.sort( key = lambda a_format: ( a_format.resolution().width()
                                                      * a_format.resolution().height(),
                                                      a_format.maxFrameRate() ),
                             reverse = True )
        self.camera_formats = camera_formats
        self.a_format_ix    = 0 if camera_formats else -1

        self.format_list_signal.emit( self.format_descriptions(), self.a_format_ix )

    # -------------------------------
    def camera_descriptions( self, ):
        """
        what it says -- one string per camera, in a_device_ix order, ready for
        a host combo box
        """
        return [ i_device.description() for i_device in self.camera_devices ]

    # -------------------------------
    def format_descriptions( self, ):
        """
        what it says -- one string per format of the current camera, in
        a_format_ix order, ready for a host combo box
        """
        a_list              = []

        for i_format in self.camera_formats:
            a_size              = i_format.resolution()
            msg                 = ( f"{a_size.width()}x{a_size.height()}  "
                                    f"{enum_name( i_format.pixelFormat() ).replace( 'Format_', '' )}  "
                                    f"{i_format.maxFrameRate():.0f} fps" )
            a_list.append( msg )

        return a_list

    # -------------------------------
    def device_ix( self, ):
        """ what it says -- which camera is selected, -1 for none """
        return self.a_device_ix

    # -------------------------------
    def format_ix( self, ):
        """ what it says -- which format is selected, -1 for none """
        return self.a_format_ix

    # -------------------------------
    def set_device_ix( self, ix ):
        """
        read it -- the host's camera combo lands here.  a new device means a
        new format list too, and a restart, so it is the expensive one.

        the no-op guard matters: a host that re-fills its combo will fire
        currentIndexChanged for the same index, and without this every rebuild
        of the list would restart the camera
        """
        if ix == self.a_device_ix:
            return

        if ix < 0 or ix >= len( self.camera_devices ):
            return

        self.a_device_ix    = ix

        self._load_format_list()
        self.start_camera()

    # -------------------------------
    def set_format_ix( self, ix ):
        """
        what it says -- the host's format combo lands here.  the format is
        handed to the camera at construction time, so this is a restart
        """
        if ix == self.a_format_ix:
            return

        if ix < 0 or ix >= len( self.camera_formats ):
            return

        self.a_format_ix    = ix

        if self.camera is not None:
            self.start_camera()

    # -------------------------------
    def _current_camera_device( self, ):
        """ what it says -- the QCameraDevice a_device_ix points at, or None """
        ix                  = self.a_device_ix

        if ix < 0 or ix >= len( self.camera_devices ):
            return None

        return self.camera_devices[ ix ]

    # -------------------------------
    def _current_camera_format( self, ):
        """ what it says -- the QCameraFormat a_format_ix points at, or None """
        ix                  = self.a_format_ix

        if ix < 0 or ix >= len( self.camera_formats ):
            return None

        return self.camera_formats[ ix ]

    # -------------------------------
    def camera_count( self, ):
        """ what it says """
        return len( self.camera_devices )

    # -------------------------------
    def current_camera_description( self, ):
        """ what it says -- "" if there is no camera """
        camera_device       = self._current_camera_device()

        if camera_device is None:
            return ""

        return camera_device.description()

    # ---- camera ------------------------------------------------------------

    # -------------------------------
    def start_camera( self, ):
        """
        read it -- a QCamera is bound to one device for its life, so changing
        device means a new one.  the session, the image capture and the
        recorder all survive that, only setCamera() changes
        """
        camera_device       = self._current_camera_device()

        if camera_device is None:
            self._say( NO_CAMERA_MSG )
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

        self._say( f"started {camera_device.description()}" )

    # -------------------------------
    def stop_camera( self, ):
        """ what it says -- also drops the QCamera, see start_camera """
        if self.camera is None:
            return

        if self.is_recording_now:
            self.stop_record()

        self.camera.stop()
        self.capture_session.setCamera( None )      # or the session holds a dead camera
        self.camera.deleteLater()
        self.camera         = None

        self._status( "camera stopped" )

    # -------------------------------
    def on_video_inputs_changed( self, ):
        """
        what it says -- a camera was plugged in or pulled out.  rebuild the
        list, and restart only if the selected device actually changed
        """
        self._say( "video inputs changed -- re-reading the camera list" )

        old_id              = None
        camera_device       = self._current_camera_device()

        if camera_device is not None:
            old_id          = camera_device.id()

        self._load_camera_list()

        camera_device       = self._current_camera_device()
        new_id              = camera_device.id() if camera_device is not None else None

        if new_id != old_id:
            self.start_camera()

    # -------------------------------
    def on_camera_active_changed( self, is_active ):
        """ what it says """
        self._status( "camera active" if is_active else "camera inactive" )

    # -------------------------------
    def on_camera_error( self, error, error_string ):
        """ what it says """
        msg                 = ( f"camera error {enum_name( error )}: {error_string}" )
        self._say( msg )
        self._status( msg )

    # ---- still images ------------------------------------------------------

    # -------------------------------
    def _time_stamp( self, ):
        """ what it says -- sortable, no characters that annoy a file system """
        return datetime.now().strftime( "%Y%m%d_%H%M%S" )

    # -------------------------------
    def snap_still( self, file_name = None ):
        """
        read it -- the capture is asynchronous.  captureToFile() only asks, and
        answers come back twice: imageCaptured with the image itself ( good for
        a thumbnail, it arrives first ) and then imageSaved once the file is
        really on disk.  no extension is given, the backend picks one
            file_name  seems it needs to be a string and fully resolved or None

        """
        if self.camera is None:
            self._say( "no camera running -- click Start" )
            return

        if not self.image_capture.isReadyForCapture():
            self._say( "camera not ready for capture yet -- try again in a moment" )
            return

        if file_name is None:
            file_name           = os.path.join( self.a_save_dir, f"still_{self._time_stamp()}" )

        else:
            pass

        capture_id          = self.image_capture.captureToFile( file_name )

        print( f"{capture_id}")

        # self._say( f"capture {capture_id} asked for: {file_name}" )
        msg      = ( f"capture {capture_id} asked for: {file_name}" )
        print( msg )
        print( "!! fix say or maybe ok if not subscribe?" )

    # -------------------------------
    def is_ready_for_capture( self, ):
        """
        what it says -- so a host can set the initial state of its snap button
        instead of waiting for the first ready_for_capture_signal
        """
        if self.image_capture is None:
            return False

        return self.image_capture.isReadyForCapture()

    # -------------------------------
    def on_image_captured( self, capture_id, a_image ):
        """
        what it says -- a_image is a QImage, in hand before the file is written,
        so a host thumbnail can go up right away.  the scaling is the host's,
        it is the one that knows how big its label is
        """
        self.still_image_signal.emit( a_image )

    # -------------------------------
    def on_image_saved( self, capture_id, file_name ):
        """
        what it says -- the file is on disk by now, file_name is the real one
        the backend chose, extension and all
        """
        self.last_file      = file_name

        self._say( f"saved: {file_name}" )
        self._status( f"saved: {file_name}" )
        self.image_saved_signal.emit( file_name )

    # -------------------------------
    def on_capture_error( self, capture_id, error, error_string ):
        """ what it says """
        msg                 = ( f"capture error {enum_name( error )}: {error_string}" )
        self._say( msg )
        self._status( msg )

    # -------------------------------
    def on_ready_for_capture_changed( self, is_ready ):
        """
        what it says -- a host snap button follows the camera, a capture asked
        for while the backend is not ready is just dropped
        """
        self.ready_for_capture_signal.emit( is_ready )

    # ---- video -------------------------------------------------------------

    # -------------------------------
    def is_recording( self, ):
        """ what it says """
        return self.is_recording_now

    # -------------------------------
    def record_video( self, ):
        """
        read it -- no capture mode to switch, unlike Qt5: the recorder is its
        own object on the session and stills keep working while it runs.
        the extension is left off, actualLocation() reports what was really used
        """
        if self.camera is None:
            self._say( "no camera running -- click Start" )
            return

        if self.is_recording_now:
            self._say( "already recording" )
            return

        # asking for h264 in an mp4 is the safe pick, but the ffmpeg qt ships
        # is LGPL and has no h264 encoder, so qt quietly substitutes MPEG4 (
        # part 2 ) -- still an .mp4, still plays anywhere.  the log line
        # "Recording new media with muxer ..." says what was really used
        a_format            = QMediaFormat( QMediaFormat.FileFormat.MPEG4 )
        a_format.setVideoCodec( QMediaFormat.VideoCodec.H264 )
        self.media_recorder.setMediaFormat( a_format )

        file_name           = os.path.join( self.a_save_dir, f"video_{self._time_stamp()}" )
        self.media_recorder.setOutputLocation( QUrl.fromLocalFile( file_name ) )
        self.media_recorder.record()

        self.is_recording_now = True
        self.recording_signal.emit( True )

        self.last_recorder_state = None     # so the first poll reports whatever it finds
        self.last_recorder_error = None
        self.recorder_timer.start()

        self._say( f"record asked for: {file_name}" )

    # -------------------------------
    def stop_record( self, ):
        """ what it says """
        if not self.is_recording_now:
            return

        self.media_recorder.stop()

        self.is_recording_now = False
        self.recording_signal.emit( False )

        # the timer runs on a little past the stop, the backend needs a moment
        # to finalize the file and only then does the state settle
        QTimer.singleShot( 1500, self.recorder_timer.stop )

    # -------------------------------
    def _poll_recorder( self, ):
        """
        read it -- stands in for recorderStateChanged and errorOccurred, which
        can not be connected in this env ( see the !! note in
        _build_capture_session ).  only speaks when something actually changed,
        or the msg area would fill with the same line four times a second
        """
        state               = self.media_recorder.recorderState()

        if state != self.last_recorder_state:
            self.last_recorder_state = state
            self.on_recorder_state_changed( state )

        error               = self.media_recorder.error()

        if error != QMediaRecorder.Error.NoError and error != self.last_recorder_error:
            self.last_recorder_error = error
            self.on_recorder_error( error, self.media_recorder.errorString() )

    # -------------------------------
    def on_recorder_state_changed( self, state ):
        """
        what it says -- state is a QMediaRecorder.RecorderState.  called from
        _poll_recorder, not from a signal, see the !! note in
        _build_capture_session
        """
        msg                 = ( f"recorder: {enum_name( state )}" )
        self._say( msg )
        self._status( msg )

    # -------------------------------
    def on_actual_location_changed( self, a_url ):
        """
        what it says -- the backend reports the file it really wrote, extension
        and all, once it has settled on one
        """
        file_name           = a_url.toLocalFile()

        if not file_name:
            return

        self.last_file      = file_name
        self._say( f"recorded: {file_name}" )
        self.video_saved_signal.emit( file_name )

    # -------------------------------
    def on_duration_changed( self, duration ):
        """ what it says -- duration is ms, only interesting while recording """
        if not self.is_recording_now:
            return

        self._status( f"recording  {duration / 1000:.1f} sec" )

    # -------------------------------
    def on_recorder_error( self, error, error_string ):
        """ what it says """
        msg                 = ( f"recorder error {enum_name( error )}: {error_string}" )
        self._say( msg )
        self._status( msg )

    # -------------------------------
    def closeEvent( self, event ):
        """
        what it says -- let go of the device, an abandoned camera can keep
        /dev/video0 busy for the next program that wants it
        """
        self.stop_camera()
        super().closeEvent( event )

# ---- eof
