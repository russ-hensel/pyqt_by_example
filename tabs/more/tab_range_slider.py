#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ---- tof
"""
tab_range_slider.py
self.help_file_name     =  "tab_range_slider.txt"

KEY_WORDS:      range slider two handles pointers low high superqt QRangeSlider QLabeledRangeSlider tuple bar
CLASS_NAME:     RangeSliderTab
WIDGETS:        QRangeSlider, QLabeledRangeSlider, QSpinBox, QCheckBox
STATUS:         new, works
TAB_TITLE:      Range Slider Superqt / with andles
DESCRIPTION:    superqt.QRangeSlider, a QSlider with two ( or more ) handles.
MORE:               value() is a tuple, one int per handle.  drag a handle, or
                drag the bar between them to move the whole range.  a
                QLabeledRangeSlider sits under it, kept in step, to show the
                labelled version.  needs superqt installed: pip install superqt
HOW_COMPLETE:   20  #  AND A COMMENT -- <10 major probs  <15 runs but <20 fair not finished  <=25 not to shabby
"""
WIKI_LINK      =  "https://github.com/russ-hensel/pyqt_by_example/wiki/Range Slider"


# --------------------
if __name__ == "__main__":
    #----- run the full app
    import main   # noqa  stops auto removal by pycln
# --------------------


from qtpy.QtCore import ( Qt )
from qtpy.QtWidgets import ( QCheckBox,
                             QHBoxLayout,
                             QLabel,
                             QSpinBox,
                             QVBoxLayout,
                             )

from superqt         import QRangeSlider, QLabeledRangeSlider

import wat_inspector
import tab_base


# ---- end imports


#-----------------------------------------------
class RangeSliderTab( tab_base.TabBase ):
    """
    here build a tab in its own class to hide its variables

    the widget is superqt.QRangeSlider, a QSlider subclass, so the usual
    setRange, setPageStep, setTracking ... all work, but value() and the
    valueChanged / sliderMoved signals carry a tuple, one int per handle.
    the number of handles is just the length of the tuple you setValue with

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

        self.range_slider       = None      # QRangeSlider, made in _build_gui_widgets

        self.help_file_name     =  "tab_range_slider.txt"
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
        a_widget            = QLabel( "QRangeSlider -- drag a handle, or drag the bar "
                                      "between handles to move the whole range" )
        layout.addWidget( a_widget )

        a_widget            = QRangeSlider( Qt.Orientation.Horizontal )
        a_widget.setTickPosition( QRangeSlider.TickPosition.TicksBelow )
        a_widget.valueChanged.connect(   self.on_value_changed )
        a_widget.sliderMoved.connect(    self.on_slider_moved )
        a_widget.sliderPressed.connect(  self.on_slider_pressed )
        a_widget.sliderReleased.connect( self.on_slider_released )
        self.range_slider   = a_widget
        layout.addWidget( a_widget )

        # ---- labelled version for comparison, same range, kept in step
        a_widget            = QLabel( "QLabeledRangeSlider on the same range, kept in step both ways, "
                                      "type in a label box too" )
        layout.addWidget( a_widget )

        a_widget            = QLabeledRangeSlider( Qt.Orientation.Horizontal )
        a_widget.valueChanged.connect( self.on_labeled_changed )
        self.labeled_slider = a_widget
        layout.addWidget( a_widget )

        # ---- readouts
        row_layout          = QHBoxLayout(   )
        layout.addLayout( row_layout )

        a_widget            = QLabel( "" )
        self.readout_label  = a_widget
        row_layout.addWidget( a_widget )
        row_layout.addStretch( 1 )

        # ---- range, steps, handles
        row_layout          = QHBoxLayout(   )
        layout.addLayout( row_layout )

        self.min_spin       = self._add_spin( row_layout, "Min",        self.on_range_spin_changed )
        self.max_spin       = self._add_spin( row_layout, "Max",        self.on_range_spin_changed )
        self.page_spin      = self._add_spin( row_layout, "Page step",  self.on_step_spin_changed,  lo = 1 )
        self.tick_spin      = self._add_spin( row_layout, "Tick",       self.on_tick_spin_changed,  lo = 0 )
        self.handles_spin   = self._add_spin( row_layout, "Handles",    self.on_handles_spin_changed,
                                              lo = 1, hi = 6 )
        self.handles_spin.setToolTip( "the length of the tuple given to setValue, "
                                      "handles are spread evenly over the range" )
        row_layout.addStretch( 1 )

        # ---- switches
        row_layout          = QHBoxLayout(   )
        layout.addLayout( row_layout )

        a_widget            = QCheckBox( "Tracking" )
        a_widget.setToolTip( "off: value only changes on release, the handles still follow the mouse" )
        a_widget.toggled.connect( self.on_tracking_toggled )
        self.tracking_check = a_widget
        row_layout.addWidget( a_widget )

        a_widget            = QCheckBox( "Bar visible" )
        a_widget.setToolTip( "setBarVisible -- the coloured bar between the handles" )
        a_widget.toggled.connect( self.on_bar_visible_toggled )
        self.bar_visible_check  = a_widget
        row_layout.addWidget( a_widget )

        a_widget            = QCheckBox( "Bar moves all handles" )
        a_widget.setToolTip( "setBarMovesAllHandles\n"
                             "on: dragging the bar moves the whole range\n"
                             "off: a bar click moves the nearest handle there" )
        a_widget.toggled.connect( self.on_bar_moves_toggled )
        self.bar_moves_check    = a_widget
        row_layout.addWidget( a_widget )

        a_widget            = QCheckBox( "Bar is rigid" )
        a_widget.setToolTip( "setBarIsRigid\n"
                             "on: dragging the bar into an end stops, the spacing is kept\n"
                             "off: the far handle keeps going and the range squeezes" )
        a_widget.toggled.connect( self.on_bar_rigid_toggled )
        self.bar_rigid_check    = a_widget
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
    def _add_spin( self, row_layout, label, connect_to, lo = -100000, hi = 100000 ):
        """
        a label and a spin box in the row, returns the spin box
        """
        a_widget            = QLabel( label )
        row_layout.addWidget( a_widget )

        a_widget            = QSpinBox(   )
        a_widget.setRange( lo, hi )
        a_widget.valueChanged.connect( connect_to )
        row_layout.addWidget( a_widget )

        return a_widget

    # ---- keeping things in step ---------------------------------------------

    # -------------------------------------
    def _sync_controls( self, ):
        """
        read it -- fill every control and the labelled slider from the range
        slider.  signals blocked while doing it, or each setValue would fire
        back into the range slider and round we go.
        minimum() etc come back as floats from superqt, hence the int()
        """
        slider              = self.range_slider

        for i_widget, i_value in ( ( self.min_spin,     slider.minimum() ),
                                   ( self.max_spin,     slider.maximum() ),
                                   ( self.page_spin,    slider.pageStep() ),
                                   ( self.tick_spin,    slider.tickInterval() ),
                                   ( self.handles_spin, len( slider.value() ) ), ):
            i_widget.blockSignals( True )
            i_widget.setValue( int( i_value ) )
            i_widget.blockSignals( False )

        for i_widget, i_checked in ( ( self.tracking_check,    slider.hasTracking() ),
                                     ( self.bar_visible_check, slider.barIsVisible() ),
                                     ( self.bar_moves_check,   slider.barMovesAllHandles() ),
                                     ( self.bar_rigid_check,   slider.barIsRigid() ),
                                     ( self.enabled_check,     slider.isEnabled() ), ):
            i_widget.blockSignals( True )
            i_widget.setChecked( i_checked )
            i_widget.blockSignals( False )

        labeled             = self.labeled_slider
        labeled.blockSignals( True )
        labeled.setRange( slider.minimum(), slider.maximum() )
        labeled.setPageStep( slider.pageStep() )
        labeled.setValue( slider.value() )
        labeled.setEnabled( slider.isEnabled() )
        labeled.blockSignals( False )

        self._update_readout()

    # -------------------------------------
    def _update_readout( self, ):
        """
        what it says -- value and sliderPosition differ during a drag with
        tracking off, which is the one time it is worth watching both
        """
        slider              = self.range_slider
        position            = tuple( int( i_pos ) for i_pos in slider.sliderPosition() )
        msg                 = ( f"value {slider.value()}     "
                                f"sliderPosition {position}     "
                                f"isSliderDown {slider.isSliderDown()}" )
        self.readout_label.setText( msg )

    # ---- range slider signals -----------------------------------------------

    # -------------------------------------
    def on_value_changed( self, value ):
        """
        what it says -- value is a tuple.  keep the labelled slider in step,
        blocked so it does not echo back
        """
        self.labeled_slider.blockSignals( True )
        self.labeled_slider.setValue( value )
        self.labeled_slider.blockSignals( False )

        self._update_readout()
        if self.log_all_check.isChecked():
            self.append_msg( f"valueChanged {value}" )

    # -------------------------------------
    def on_slider_moved( self, position ):
        """ what it says -- position is a tuple too """
        self._update_readout()
        if self.log_all_check.isChecked():
            self.append_msg( f"sliderMoved {position}" )

    # -------------------------------------
    def on_slider_pressed( self, ):
        """ what it says -- logged always, one line per drag """
        self._update_readout()
        self.append_msg( f"sliderPressed, value {self.range_slider.value()}" )

    # -------------------------------------
    def on_slider_released( self, ):
        """
        read it -- with tracking off QSlider would commit the position to
        the value on release.  superqt 0.8.2 does not: setSliderDown is the
        C++ one, which commits Qt's own position, not superqt's.  so the
        value would never change.  do it ourselves here
        """
        slider              = self.range_slider
        self.append_msg( f"sliderReleased, value {slider.value()}" )

        if not slider.hasTracking():
            new_value       = tuple( round( i_pos ) for i_pos in slider.sliderPosition() )
            self.append_msg( f"tracking off, commit by hand: setValue( {new_value} )" )
            slider.setValue( new_value )

        self._update_readout()

    # -------------------------------------
    def on_labeled_changed( self, value ):
        """ what it says -- the labelled slider drives the range slider too """
        self.range_slider.setValue( value )

    # ---- the controls -------------------------------------------------------

    # -------------------------------------
    def on_range_spin_changed( self, value ):
        """
        what it says -- handles outside the new range are clamped into it,
        so re-read the spins from the widget afterwards
        """
        self.range_slider.setRange( self.min_spin.value(), self.max_spin.value() )
        self._sync_controls()

    # -------------------------------------
    def on_step_spin_changed( self, value ):
        """ what it says """
        self.range_slider.setPageStep( value )
        self._sync_controls()

    # -------------------------------------
    def on_tick_spin_changed( self, value ):
        """ what it says -- 0 lets Qt pick the interval """
        self.range_slider.setTickInterval( value )
        self._sync_controls()

    # -------------------------------------
    def on_handles_spin_changed( self, value ):
        """
        read it -- the handle count is just the length of the tuple
        """
        new_value           = self._spread( value )
        self.range_slider.setValue( new_value )
        self.append_msg( f"setValue( {new_value} )    -- {value} handles" )
        self._sync_controls()

    # -------------------------------------
    def _spread( self, count ):
        """
        count values spread evenly inside the range, as a tuple
        """
        lo                  = int( self.range_slider.minimum() )
        hi                  = int( self.range_slider.maximum() )
        return tuple( lo + round( ( hi - lo ) * ( ix + 1 ) / ( count + 1 ) )
                      for ix in range( count ) )

    # -------------------------------------
    def on_tracking_toggled( self, is_checked ):
        """ what it says """
        self.range_slider.setTracking( is_checked )
        self.append_msg( f"setTracking( {is_checked} )" )

    # -------------------------------------
    def on_bar_visible_toggled( self, is_checked ):
        """ what it says """
        self.range_slider.setBarVisible( is_checked )
        self.append_msg( f"setBarVisible( {is_checked} )" )

    # -------------------------------------
    def on_bar_moves_toggled( self, is_checked ):
        """ what it says """
        self.range_slider.setBarMovesAllHandles( is_checked )
        self.append_msg( f"setBarMovesAllHandles( {is_checked} )" )

    # -------------------------------------
    def on_bar_rigid_toggled( self, is_checked ):
        """ what it says """
        self.range_slider.setBarIsRigid( is_checked )
        self.append_msg( f"setBarIsRigid( {is_checked} )" )

    # -------------------------------------
    def on_enabled_toggled( self, is_checked ):
        """ what it says """
        self.range_slider.setEnabled( is_checked )
        self._sync_controls()

    # ---- mutates ------------------------------------------------------------

    # -------------------------------------
    def _apply( self, lo, hi, value, page, tick,
                tracking = True, bar_visible = True, bar_moves = True, bar_rigid = True ):
        """
        set the range slider up in one go, log what was done, refresh the controls
        """
        slider              = self.range_slider
        slider.setEnabled( True )
        slider.setRange( lo, hi )
        slider.setValue( value )
        slider.setPageStep( page )
        slider.setTickInterval( tick )
        slider.setTracking( tracking )
        slider.setBarVisible( bar_visible )
        slider.setBarMovesAllHandles( bar_moves )
        slider.setBarIsRigid( bar_rigid )

        msg                 = ( f"setRange( {lo}, {hi} )  setValue( {value} )  "
                                f"setPageStep( {page} )  setTickInterval( {tick} )\n"
                                f"setTracking( {tracking} )  setBarVisible( {bar_visible} )  "
                                f"setBarMovesAllHandles( {bar_moves} )  setBarIsRigid( {bar_rigid} )" )
        self.append_msg( msg )
        self._sync_controls()

    # ------------------------------------
    def mutate_0( self ):
        """
        read it -- the defaults, two handles
        """
        self.append_function_msg( "mutate_0" )
        self.append_msg( "0 .. 100, two handles, value() is a 2-tuple" )

        self._apply( 0, 100, ( 20, 80 ), 10, 10 )

        self.append_msg( tab_base.DONE_MSG )

    # ------------------------------------
    def mutate_1( self ):
        """
        read it -- three handles, just a longer tuple
        """
        self.append_function_msg( "mutate_1" )
        self.append_msg( "three handles -- setValue with a 3-tuple, there is no handle count property" )

        self._apply( 0, 100, ( 25, 50, 75 ), 10, 10 )

        self.append_msg( tab_base.DONE_MSG )

    # ------------------------------------
    def mutate_2( self ):
        """
        read it -- negative range, tracking off
        """
        self.append_function_msg( "mutate_2" )
        self.append_msg( "-50 .. 50, tracking off -- drag and watch value hold "
                         "until release, while sliderPosition follows" )

        self._apply( -50, 50, ( -20, 20 ), 10, 10, tracking = False )

        self.append_msg( tab_base.DONE_MSG )

    # ------------------------------------
    def mutate_3( self ):
        """
        read it -- bar does not move the range, and is hidden
        """
        self.append_function_msg( "mutate_3" )
        self.append_msg( "bar hidden and bar moves all handles off -- "
                         "a click between the handles moves the nearest one" )

        self._apply( 0, 100, ( 30, 60 ), 10, 10, bar_visible = False, bar_moves = False )

        self.append_msg( tab_base.DONE_MSG )

    # ------------------------------------
    def mutate_4( self ):
        """
        read it -- bar not rigid
        """
        self.append_function_msg( "mutate_4" )
        self.append_msg( "bar is rigid off -- drag the bar into an end and keep going, "
                         "the range squeezes instead of stopping" )

        self._apply( 0, 1000, ( 400, 600 ), 100, 100, bar_rigid = False )

        self.append_msg( tab_base.DONE_MSG )

    # ------------------------
    def inspect(self):
        """
        the usual
        """
        self.append_function_msg( "inspect" )
        # make some locals for inspection

        self_range_slider           = self.range_slider
        self_labeled_slider         = self.labeled_slider
        self_range_slider_value     = self.range_slider.value()
        self_range_slider_position  = self.range_slider.sliderPosition()

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
