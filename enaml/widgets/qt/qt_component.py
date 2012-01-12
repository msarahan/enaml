#------------------------------------------------------------------------------
#  Copyright (c) 2011, Enthought, Inc.
#  All rights reserved.
#------------------------------------------------------------------------------
import weakref

from .qt import QtGui
from .styling import q_color_from_color, q_font_from_font

from ..component import AbstractTkComponent


class QtComponent(AbstractTkComponent):
    """ Base component object for the Qt based backend.

    """
    #: The a reference to the shell object. Will be stored as a weakref.
    _shell_obj = lambda self: None

    #: The Qt widget created by the component
    widget = None

    #--------------------------------------------------------------------------
    # Setup Methods
    #--------------------------------------------------------------------------
    def create(self, parent):
        """ Creates the underlying Qt widget. As necessary, subclasses
        should reimplement this method to create different types of
        widgets.

        """
        self.widget = QtGui.QFrame(parent)

    def initialize(self):
        """ Initializes the attributes of the the Qt widget.

        """
        shell = self.shell_obj
        if shell.bg_color:
            self.set_bg_color(shell.bg_color)
        if shell.fg_color:
            self.set_fg_color(shell.fg_color)
        if shell.font:
            self.set_font(shell.font)
        self.set_enabled(shell.enabled)
    
    def bind(self):
        """ Bind any event/signal handlers for the Qt Widget. By default,
        this is a no-op. Subclasses should reimplement this method as
        necessary to bind any widget event handlers or signals.

        """
        pass

    #--------------------------------------------------------------------------
    # Teardown Methods
    #--------------------------------------------------------------------------
    def destroy(self):
        """ Destroys the underlying Qt widget.

        """
        widget = self.widget
        if widget:
            # On Windows, it's not sufficient to simply destroy the
            # widget. It appears that this only schedules the widget 
            # for destruction at a later time. So, we need to explicitly
            # unparent the widget as well.
            widget.setParent(None)
            widget.destroy()
        self.widget = None

    #--------------------------------------------------------------------------
    # Abstract Implementation
    #--------------------------------------------------------------------------
    @property
    def toolkit_widget(self):
        """ A property that returns the toolkit specific widget for this
        component.

        """
        return self.widget

    def _get_shell_obj(self):
        """ Returns a strong reference to the shell object.

        """
        return self._shell_obj()
    
    def _set_shell_obj(self, obj):
        """ Stores a weak reference to the shell object.

        """
        self._shell_obj = weakref.ref(obj)
    
    #: A property which gets a sets a reference (stored weakly)
    #: to the shell object
    shell_obj = property(_get_shell_obj, _set_shell_obj)
        
    def disable_updates(self):
        """ Disable rendering updates for the underlying Qt widget.

        """
        self.widget.setUpdatesEnabled(False)

    def enable_updates(self):
        """ Enable rendering updates for the underlying Wx widget.

        """
        self.widget.setUpdatesEnabled(True)

    #--------------------------------------------------------------------------
    # Shell Object Change Handlers 
    #--------------------------------------------------------------------------
    def shell_enabled_changed(self, enabled):
        """ The change handler for the 'enabled' attribute on the shell
        object.

        """
        self.set_enabled(enabled)

    def shell_bg_color_changed(self, color):
        """ The change handler for the 'bg_color' attribute on the shell
        object. Sets the background color of the internal widget to the 
        given color.
        
        """
        self.set_bg_color(color)
    
    def shell_fg_color_changed(self, color):
        """ The change handler for the 'fg_color' attribute on the shell
        object. Sets the foreground color of the internal widget to the 
        given color.

        """
        self.set_fg_color(color)

    def shell_font_changed(self, font):
        """ The change handler for the 'font' attribute on the shell 
        object. Sets the font of the internal widget to the given font.

        """
        self.set_font(font)

    #--------------------------------------------------------------------------
    # Widget Update Methods
    #--------------------------------------------------------------------------
    def set_enabled(self, enabled):
        """ Enable or disable the widget.

        """
        self.widget.setEnabled(enabled)

    def set_visible(self, visible):
        """ Show or hide the widget.

        """
        self.widget.setVisible(visible)

    def set_bg_color(self, color):
        """ Sets the background color of the widget to an appropriate
        QColor given the provided Enaml Color object.

        """
        widget = self.widget
        role = widget.backgroundRole()
        if not color:
            palette = QtGui.QApplication.instance().palette(widget)
            qcolor = palette.color(role)
            # On OSX, the default color is rendered *slightly* off
            # so a simple workaround is to tell the widget not to
            # auto fill the background.
            widget.setAutoFillBackground(False)
        else:
            qcolor = q_color_from_color(color)
            # When not using qt style sheets to set the background
            # color, we need to tell the widget to auto fill the 
            # background or the bgcolor won't render at all.
            widget.setAutoFillBackground(True)
        palette = widget.palette()
        palette.setColor(role, qcolor)
        widget.setPalette(palette)
    
    def set_fg_color(self, color):
        """ Sets the foreground color of the widget to an appropriate
        QColor given the provided Enaml Color object.

        """
        widget = self.widget
        role = widget.foregroundRole()
        if not color:
            palette = QtGui.QApplication.instance().palette(widget)
            qcolor = palette.color(role)
        else:
            qcolor = q_color_from_color(color)
        palette = widget.palette()
        palette.setColor(role, qcolor)
        widget.setPalette(palette)

    def set_font(self, font):
        """ Sets the font of the widget to an appropriate QFont given 
        the provided Enaml Font object.

        """
        q_font = q_font_from_font(font)
        self.widget.setFont(q_font)

