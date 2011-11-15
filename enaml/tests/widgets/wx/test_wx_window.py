#------------------------------------------------------------------------------
#  Copyright (c) 2011, Enthought, Inc.
#  All rights reserved.
#------------------------------------------------------------------------------
from .wx_test_assistant import WXTestAssistant
from .. import window

class TestWXWindow(WXTestAssistant, window.TestWindow):
    """ WXWindow tests. """

    def get_title(self, widget):
        """ Get a window's title.

        """
        frame = widget.GetParent()
        return frame.GetTitle()

