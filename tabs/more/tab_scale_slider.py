#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ---- tof
"""
tab_scale_slider.py
self.help_file_name     =  "tab_scale_slider.txt"

KEY_WORDS:      scale slider pointer ruler ticks custom widget paintEvent QAbstractSlider drag mouse textFromValue format
CLASS_NAME:     ScaleSliderTab
WIDGETS:        QAbstractSlider, QSlider, QSpinBox, QCheckBox, QComboBox, QPainter
STATUS:         works, labels and magnifier still to come
TAB_TITLE:      Scale Slider / custom pointer on a scale
DESCRIPTION:    a custom widget: an integer scale with ticks and a pointer you
MORE:               drag, click, key or wheel along it.  subclasses QAbstractSlider
                and paints everything itself.  the widget is scale_slider.ScaleSlider,
                this tab is only controls, with a stock QSlider kept in step for comparison
HOW_COMPLETE:   20  #  AND A COMMENT -- <10 major probs  <15 runs but <20 fair not finished  <=25 not to shabby
"""
WIKI_LINK      =  "https://github.com/russ-hensel/pyqt_by_example/wiki/Scale Slider"


# --------------------
if __name__ == "__main__":
    #----- run the full app
    import main   # noqa  stops auto removal by pycln
# --------------------


from qtpy.QtCore import ( Qt )
from qtpy.QtWidgets import ( QCheckBox,
                             QComboBox,
                             QHBoxLayout,
                             QLabel,
                             QSlider,
                             QSpinBox,
                             QVBoxLayout,
                             )

import wat_inspector
import tab_base

import scale_slider


# ---- end imports

MONTHS          = [ "January", "February", "March",     "April",   "May",      "June",
                    "July",    "August",   "September", "October", "November", "December" ]

NOTES           = [ "C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B" ]


# ---- pointer text functions, int -> str.  each falls back to the plain
#      number outside what it knows, so a range change can not break it

# -------------------------------------
def text_month( value ):
    """ 1 .. 12 -> month name """
    if 1 <= value <= 12:
        return MONTHS[ value - 1 ]
    return ( str( value ) )

# -------------------------------------
def text_note( value ):
    """ midi note number -> name and octave, 60 is middle C, C4 """
    if 0 <= value <= 127:
        return ( f"{NOTES[ value % 12 ]}{value // 12 - 1}" )
    return ( str( value ) )

# -------------------------------------
def text_celsius( value ):
    """ what it says """
    return ( f"{value} \u00b0C" )

# -------------------------------------
def text_hex( value ):
    """ what it says, negatives get a sign """
    sign        = "-" if value < 0 else ""
    return ( f"{sign}0x{abs( value ):02X}" )

# -------------------------------------
def text_hidden( value ):
    """ "" hides the readout """
    return ( "" )


#-----------------------------------------------
class ScaleSliderTab( tab_base.TabBase ):
    """
    here build a tab in its own class to hide its variables

    this tab is controls only.  the widget, scale_slider.ScaleSlider, does
    all the painting and mouse work.  a stock QSlider sits under it on the
    same range, kept in step both ways, to show the custom widget speaks the
    same api and signals as the stock one

    the controls are always filled FROM the widget, see _sync_controls, so
    whatever a mutate or a clamp did to the widget is what they show
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
        self.mutate_dict[2]     = self.mutate_2
        self.mutate_dict[3]     = self.mutate_3
        self.mutate_dict[4]     = self.mutate_4

        self.scale              = None      # ScaleSlider, made in _build_gui_widgets

        self.help_file_name     =  "tab_scale_slider.txt"
        self._build_gui()

    #----------------------------
    def _build_gui_widgets(self, main_layout  ):
        """
        the usual, build the gui with the widgets of interest
        and the buttons for examples
        """
        layout              = QVBoxLayout(   )
        main_layout.addLayout( layout )

        # ---- the widget of interest
        a_widget            = QLabel( "ScaleSlider -- drag the pointer, click the track, "
                                      "arrows pgup pgdn home end, wheel, escape cancels a drag" )
        layout.addWidget( a_widget )

        a_widget            = scale_slider.ScaleSlider(   )
        a_widget.valueChanged.connect(   self.on_value_changed )
        a_widget.sliderMoved.connect(    self.on_slider_moved )
        a_widget.sliderPressed.connect(  self.on_slider_pressed )
        a_widget.sliderReleased.connect( self.on_slider_released )
        self.scale          = a_widget
        layout.addWidget( a_widget )

        # ---- stock QSlider for comparison, same range, kept in step
        a_widget            = QLabel( "stock QSlider on the same range, kept in step both ways" )
        layout.addWidget( a_widget )

        a_widget            = QSlider( Qt.Orientation.Horizontal )
        a_widget.setTickPosition( QSlider.TickPosition.TicksBelow )
        a_widget.valueChanged.connect( self.on_qslider_changed )
        self.qslider        = a_widget
        layout.addWidget( a_widget )

        # ---- readouts
        row_layout          = QHBoxLayout(   )
        layout.addLayout( row_layout )

        a_widget            = QLabel( "" )
        self.readout_label  = a_widget
        row_layout.addWidget( a_widget )
        row_layout.addStretch( 1 )

        # ---- pointer text
        row_layout          = QHBoxLayout(   )
        layout.addLayout( row_layout )

        a_widget            = QLabel( "Pointer text" )
        row_layout.addWidget( a_widget )

        a_widget            = QComboBox(   )
        a_widget.setToolTip( "set_text_function( fn ), fn takes the int under the pointer "
                             "and returns its text" )
        for i_format in self._text_formats():
            a_widget.addItem( i_format[ 0 ] )
        a_widget.currentIndexChanged.connect( self.on_text_format_changed )
        self.format_combo   = a_widget
        row_layout.addWidget( a_widget )
        row_layout.addStretch( 1 )

        # ---- range and steps
        row_layout          = QHBoxLayout(   )
        layout.addLayout( row_layout )

        self.min_spin       = self._add_spin( row_layout, "Min",        self.on_range_spin_changed )
        self.max_spin       = self._add_spin( row_layout, "Max",        self.on_range_spin_changed )
        self.page_spin      = self._add_spin( row_layout, "Page step",  self.on_step_spin_changed,  lo = 1 )
        self.major_spin     = self._add_spin( row_layout, "Major tick", self.on_tick_spin_changed,  lo = 0 )
        self.minor_spin     = self._add_spin( row_layout, "Minor tick", self.on_tick_spin_changed,  lo = 0 )
        row_layout.addStretch( 1 )

        # ---- switches
        row_layout          = QHBoxLayout(   )
        layout.addLayout( row_layout )

        a_widget            = QCheckBox( "Tracking" )
        a_widget.setToolTip( "off: value only changes on release, the pointer still follows the mouse" )
        a_widget.toggled.connect( self.on_tracking_toggled )
        self.tracking_check = a_widget
        row_layout.addWidget( a_widget )

        a_widget            = QCheckBox( "Click jumps" )
        a_widget.setToolTip( "on: a track click jumps there and drags\n"
                             "off: a track click pages toward it, hold to repeat" )
        a_widget.toggled.connect( self.on_click_jumps_toggled )
        self.jumps_check    = a_widget
        row_layout.addWidget( a_widget )

        a_widget            = QCheckBox( "Enabled" )
        a_widget.toggled.connect( self.on_enabled_toggled )
        self.enabled_check  = a_widget
        row_layout.addWidget( a_widget )

        a_widget            = QCheckBox( "Log every signal" )
        a_widget.setToolTip( "log each sliderMoved and valueChanged, noisy during a drag, "
                             "but it shows the signal order" )
        self.log_all_check  = a_widget
        row_layout.addWidget( a_widget )

        row_layout.addStretch( 1 )

        # ---- buttons
        button_layout       = QHBoxLayout(   )
        layout.addLayout( button_layout )

        self.build_gui_last_buttons( button_layout )

    # -------------------------------------
    def _add_spin( self, row_layout, label, connect_to, lo = -100000 ):
        """
        a label and a spin box in the row, returns the spin box
        """
        a_widget            = QLabel( label )
        row_layout.addWidget( a_widget )

        a_widget            = QSpinBox(   )
        a_widget.setRange( lo, 100000 )
        a_widget.valueChanged.connect( connect_to )
        row_layout.addWidget( a_widget )

        return a_widget

    # ---- keeping things in step ---------------------------------------------

    # -------------------------------------
    def _sync_controls( self, ):
        """
        read it -- fill every control and the stock QSlider from the scale.
        signals blocked while doing it, or each setValue would fire back into
        the scale and round we go
        """
        scale               = self.scale

        for i_widget, i_value in ( ( self.min_spin,   scale.minimum() ),
                                   ( self.max_spin,   scale.maximum() ),
                                   ( self.page_spin,  scale.pageStep() ),
                                   ( self.major_spin, scale.major_tick_interval ),
                                   ( self.minor_spin, scale.minor_tick_interval ), ):
            i_widget.blockSignals( True )
            i_widget.setValue( i_value )
            i_widget.blockSignals( False )

        for i_widget, i_checked in ( ( self.tracking_check, scale.hasTracking() ),
                                     ( self.jumps_check,    scale.click_jumps ),
                                     ( self.enabled_check,  scale.isEnabled() ), ):
            i_widget.blockSignals( True )
            i_widget.setChecked( i_checked )
            i_widget.blockSignals( False )

        qslider             = self.qslider
        qslider.blockSignals( True )
        qslider.setRange( scale.minimum(), scale.maximum() )
        qslider.setPageStep( scale.pageStep() )
        qslider.setTickInterval( scale.major_tick_interval )
        qslider.setValue( scale.value() )
        qslider.setEnabled( scale.isEnabled() )
        qslider.blockSignals( False )

        self._update_readout()

    # -------------------------------------
    def _update_readout( self, ):
        """
        what it says -- value and sliderPosition differ during a drag with
        tracking off, which is the one time it is worth watching both
        """
        scale               = self.scale
        msg                 = ( f"value {scale.value()}     "
                                f"sliderPosition {scale.sliderPosition()}     "
                                f"isSliderDown {scale.isSliderDown()}" )
        self.readout_label.setText( msg )

    # ---- scale signals ------------------------------------------------------

    # -------------------------------------
    def on_value_changed( self, value ):
        """
        what it says -- keep the stock slider in step, blocked so it does not
        echo back
        """
        self.qslider.blockSignals( True )
        self.qslider.setValue( value )
        self.qslider.blockSignals( False )

        self._update_readout()
        if self.log_all_check.isChecked():
            self.append_msg( f"valueChanged {value}" )

    # -------------------------------------
    def on_slider_moved( self, position ):
        """ what it says """
        self._update_readout()
        if self.log_all_check.isChecked():
            self.append_msg( f"sliderMoved {position}" )

    # -------------------------------------
    def on_slider_pressed( self, ):
        """ what it says -- logged always, one line per drag """
        self._update_readout()
        self.append_msg( f"sliderPressed at {self.scale.sliderPosition()}" )

    # -------------------------------------
    def on_slider_released( self, ):
        """
        what it says -- with tracking off, valueChanged comes after this,
        so the value shown here may still be the old one
        """
        self._update_readout()
        self.append_msg( f"sliderReleased at {self.scale.sliderPosition()}, "
                         f"value {self.scale.value()}" )

    # -------------------------------------
    def on_qslider_changed( self, value ):
        """ what it says -- the stock slider drives the scale too """
        self.scale.setValue( value )

    # ---- pointer text -------------------------------------------------------

    # -------------------------------------
    def _text_formats( self, ):
        """
        the formats the combo offers:
            ( name, text function, ( lo, hi, value, page, major, minor ) or None )
        a range tuple is set along with the format, None keeps the current range.
        percent is a bound method -- it needs the scale's range, which a
        plain function would not know
        """
        return [ ( "Plain number ( default )",   None,              None ),
                 ( "Percent of range",           self.text_percent, None ),
                 ( "Temperature \u00b0C",       text_celsius,      ( -20, 40,  20,  5, 10, 1 ) ),
                 ( "Month names",                text_month,        (   1, 12,   3,  3,  3, 1 ) ),
                 ( "Musical notes ( midi )",     text_note,         (  21, 108, 60, 12, 12, 1 ) ),
                 ( "Hex",                        text_hex,          (   0, 255, 128, 16, 16, 4 ) ),
                 ( "Hidden ( returns \"\" )",  text_hidden,       None ),
                 ]

    # -------------------------------------
    def text_percent( self, value ):
        """ where value sits in the range, 0 .. 100 % """
        lo          = self.scale.minimum()
        hi          = self.scale.maximum()
        if hi == lo:
            return ( "100 %" )
        return ( f"{round( 100 * ( value - lo ) / ( hi - lo ) )} %" )

    # -------------------------------------
    def on_text_format_changed( self, ix ):
        """
        read it -- hand the scale a new text function, and set the range
        that goes with it if the format has one
        """
        formats             = self._text_formats()
        if ix < 0 or ix >= len( formats ):
            return

        name, function, a_range     = formats[ ix ]
        self.scale.set_text_function( function )

        fn_name             = "None" if function is None else function.__name__
        self.append_msg( f"set_text_function( {fn_name} )    -- {name}" )

        if a_range is not None:
            lo, hi, value, page, major, minor   = a_range
            self._apply( lo, hi, value, page, major, minor,
                         tracking    = self.scale.hasTracking(),
                         click_jumps = self.scale.click_jumps,
                         keep_text   = True )
        self.scale.update()

    # ---- the controls -------------------------------------------------------

    # -------------------------------------
    def on_range_spin_changed( self, value ):
        """
        what it says -- if min goes above max QAbstractSlider pulls max up to
        meet it, so re-read the spins from the widget afterwards
        """
        self.scale.setRange( self.min_spin.value(), self.max_spin.value() )
        self._sync_controls()

    # -------------------------------------
    def on_step_spin_changed( self, value ):
        """ what it says """
        self.scale.setPageStep( value )
        self._sync_controls()

    # -------------------------------------
    def on_tick_spin_changed( self, value ):
        """ what it says -- value is unused, both spins are read """
        self.scale.set_major_tick_interval( self.major_spin.value() )
        self.scale.set_minor_tick_interval( self.minor_spin.value() )
        self._sync_controls()

    # -------------------------------------
    def on_tracking_toggled( self, is_checked ):
        """ what it says """
        self.scale.setTracking( is_checked )
        self.append_msg( f"setTracking( {is_checked} )" )

    # -------------------------------------
    def on_click_jumps_toggled( self, is_checked ):
        """ what it says -- a plain attribute, not a Qt property """
        self.scale.click_jumps  = is_checked
        self.append_msg( f"click_jumps = {is_checked}" )

    # -------------------------------------
    def on_enabled_toggled( self, is_checked ):
        """ what it says """
        self.scale.setEnabled( is_checked )
        self._sync_controls()

    # ---- mutates ------------------------------------------------------------

    # -------------------------------------
    def _apply( self, lo, hi, value, page, major, minor,
                tracking = True, click_jumps = True, keep_text = False ):
        """
        set the scale up in one go, log what was done, refresh the controls.
        unless keep_text, back to the plain number -- the mutates call this
        and should each start clean
        """
        scale               = self.scale
        if not keep_text:
            scale.set_text_function( None )
            self.format_combo.blockSignals( True )
            self.format_combo.setCurrentIndex( 0 )
            self.format_combo.blockSignals( False )
        scale.setEnabled( True )
        scale.setRange( lo, hi )
        scale.setValue( value )
        scale.setPageStep( page )
        scale.set_major_tick_interval( major )
        scale.set_minor_tick_interval( minor )
        scale.setTracking( tracking )
        scale.click_jumps   = click_jumps

        msg                 = ( f"setRange( {lo}, {hi} )  setValue( {value} )  setPageStep( {page} )\n"
                                f"set_major_tick_interval( {major} )  set_minor_tick_interval( {minor} )\n"
                                f"setTracking( {tracking} )  click_jumps = {click_jumps}" )
        self.append_msg( msg )
        self._sync_controls()

    # ------------------------------------
    def mutate_0( self ):
        """
        read it -- the defaults
        """
        self.append_function_msg( "mutate_0" )
        self.append_msg( "the defaults, 0 .. 100" )

        self._apply( 0, 100, 50, 10, 10, 1 )

        self.append_msg( tab_base.DONE_MSG )

    # ------------------------------------
    def mutate_1( self ):
        """
        read it -- odd range ends, ticks still land on multiples of 5
        """
        self.append_function_msg( "mutate_1" )
        self.append_msg( "odd ends -- ticks land on multiples of the interval, not on the ends" )

        self._apply( 3, 47, 3, 5, 5, 1 )

        self.append_msg( tab_base.DONE_MSG )

    # ------------------------------------
    def mutate_2( self ):
        """
        read it -- a big range, minor ticks too dense so they are skipped
        """
        self.append_function_msg( "mutate_2" )
        self.append_msg( "0 .. 1000 -- minor ticks every 1 would crowd, so they are not drawn" )

        self._apply( 0, 1000, 500, 100, 100, 1 )

        self.append_msg( tab_base.DONE_MSG )

    # ------------------------------------
    def mutate_3( self ):
        """
        read it -- negative range, tracking off
        """
        self.append_function_msg( "mutate_3" )
        self.append_msg( "-50 .. 50, tracking off -- drag and watch value hold "
                         "until release, while sliderPosition follows" )

        self._apply( -50, 50, 0, 10, 10, 2, tracking = False )

        self.append_msg( tab_base.DONE_MSG )

    # ------------------------------------
    def mutate_4( self ):
        """
        read it -- QSlider style paging on a track click
        """
        self.append_function_msg( "mutate_4" )
        self.append_msg( "click_jumps off -- a track click pages toward it, "
                         "hold the button and it repeats until it reaches the mouse" )

        self._apply( 0, 100, 50, 10, 10, 1, click_jumps = False )

        self.append_msg( tab_base.DONE_MSG )

    # ------------------------
    def inspect(self):
        """
        the usual
        """
        self.append_function_msg( "inspect" )
        # make some locals for inspection

        self_scale              = self.scale
        self_qslider            = self.qslider
        self_scale_value        = self.scale.value()
        self_scale_position     = self.scale.sliderPosition()
        self_scale_click_jumps  = self.scale.click_jumps

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
