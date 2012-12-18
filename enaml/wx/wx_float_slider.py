#------------------------------------------------------------------------------
#  Copyright (c) 2012, Enthought, Inc.
#  All rights reserved.
#------------------------------------------------------------------------------
from .wx_slider import WxSlider, wxProperSlider, EVT_SLIDER


class WxFloatSlider(WxSlider):
    """ A Wx implementation of an Enaml FloatSlider.

    """

    #: Minimum value for the slider (float). This is used to compute
    #: an integer value for the underlying widget.
    _minimum = 0.0

    #: Maximum value for the slider (float). This is used to compute
    #: an integer value for the underlying widget.
    _maximum = 1.0

    #: Precision of the slider (int). This is used to compute an
    #: integer value for the underlying widget.
    _precision = 100

    #--------------------------------------------------------------------------
    # Setup Methods
    #--------------------------------------------------------------------------
    def create_widget(self, parent, tree):
        """ Create the underlying wxProperSlider widget.

        """
        return wxProperSlider(parent)

    def create(self, tree):
        """ Create and initialize the slider control.

        """
        # NOTE: The tick interval must be set *after* the tick position
        # or Wx will ignore the tick interval. grrr...
        # NOTE: The tick interval and value must be set after precision,
        # minimum and maximum.
        super(WxSlider, self).create(tree)
        self.set_value(tree['value'])
        self.set_maximum(tree['maximum'])
        self.set_minimum(tree['minimum'])
        self.set_orientation(tree['orientation'])
        self.set_page_step(tree['page_step'])
        self.set_single_step(tree['single_step'])
        self.set_tick_position(tree['tick_position'])
        self.set_tick_interval(tree['tick_interval'])
        self.set_tracking(tree['tracking'])
        self.widget().Bind(EVT_SLIDER, self.on_value_changed)

    #--------------------------------------------------------------------------
    # Message Handlers
    #--------------------------------------------------------------------------
    def on_action_set_precision(self, content):
        """ Handle the 'set_precision' action from the Enaml widget.

        """
        self.set_precision(content['precision'])

    #--------------------------------------------------------------------------
    # Event Handlers
    #--------------------------------------------------------------------------
    def on_value_changed(self, event):
        """ Send the 'value_changed' action to the Enaml widget when the
        slider value has changed.

        """
        int_value = self.widget().value()
        float_value = self.int_to_float(int_value)
        content = {'value': float_value}
        self.send_action('value_changed', content)

    #--------------------------------------------------------------------------
    # Widget Update Methods
    #--------------------------------------------------------------------------
    def set_value(self, value):
        """ Set the value of the underlying widget.

        Overloaded to convert the float value used by the Enaml widget
        to the integer value needed by the wxProperSlider.

        """
        int_value = self.float_to_int(value)
        self.widget().setValue(int_value)

    def set_precision(self, precision):
        """ Set the precision of the underlying widget.

        """
        self._precision = precision
        self.widget().SetRange(0, precision)

    def set_maximum(self, maximum):
        """ Set the maximum value of the underlying widget.

        """
        self._maximum = maximum

    def set_minimum(self, minimum):
        """ Set the minimum value of the underlying widget.

        """
        self._minimum = minimum

    def set_tick_interval(self, interval):
        """ Set the tick interval of the underlying widget.

        Overloaded to convert the float tick_interval used by the Enaml
        widget to the integer tick_interval needed by the
        wxProperSlider.

        """
        int_interval = self.float_to_int(interval + self._minimum)
        self.widget().SetTickFreq(int_interval)

    #--------------------------------------------------------------------------
    # Utility Methods
    #--------------------------------------------------------------------------
    def float_to_int(self, value):
        """ Convert a float value to an int value.

        """
        u = (value - self._minimum) / (self._maximum - self._minimum)
        i = int(round(u * self._precision))
        return i

    def int_to_float(self, value):
        """ Convert an int value to a float value.

        """
        u = float(value) / self._precision
        x = u * self._maximum + (1.0 - u) * self._minimum
        return x