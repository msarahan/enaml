#------------------------------------------------------------------------------
#  Copyright (c) 2012, Enthought, Inc.
#  All rights reserved.
#------------------------------------------------------------------------------
from .qt.QtGui import QDialog
from .qt.QtCore import Qt
from qt_window import QtWindow

QT_MODALITY = {
    'application_modal' : Qt.ApplicationModal,
    'window_modal' : Qt.WindowModal,
    'non_modal' : Qt.NonModal
}

class QtDialog(QtWindow):
    """ A Qt implementation of a dialog

    """
    def create(self):
        """ Create the underlying widget

        """
        self.widget = QDialog(self.parent_widget)
        self.widget.show()

    def initialize(self, init_attrs):
        """ Initialize the dialog with the given modality. The default value
        is 'non_modal'

        """
        self.set_modality(init_attrs.get('modality', 'non_modal'))

    def bind(self):
        """ Connect the events to the correct slots

        """
        self.widget.opened.connect(self.on_opened)
        self.widget.closed.connect(self.on_closed)

    #--------------------------------------------------------------------------
    # Message Handlers
    #--------------------------------------------------------------------------
    def receive_set_modality(self, ctxt):
        """ Handle a set_modality message

        """
        modality = ctxt.get('value')
        if modality is not None:
            self.set_modality(modality)

    #--------------------------------------------------------------------------
    # Signal Handlers
    #--------------------------------------------------------------------------
    def on_opened(self):
        """ The event handler for the opened event.

        """
        self.send('opened', {})

    def on_closed(self):
        """ The event handler for the closed event.

        """
        self.send('pressed', {})

    #--------------------------------------------------------------------------
    # Widget Update Methods
    #--------------------------------------------------------------------------
    def set_modality(self, modality):
        """ Set the modality of the dialog window.

        """
        self.widget.setWindowModality(QT_MODALITY[modality])
