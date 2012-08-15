#------------------------------------------------------------------------------
#  Copyright (c) 2012, Enthought, Inc.
#  All rights reserved.
#------------------------------------------------------------------------------
import wx

from .wx_menu import EVT_MENU_CHANGED
from .wx_widget_component import WxWidgetComponent


class wxMenuBar(wx.MenuBar):
    """ A wx.MenuBar subclass which exposes a more convenient api for
    working with wxMenu children.

    """
    def __init__(self, *args, **kwargs):
        """ Initialize a wxMenuBar.

        Parameters
        ----------
        *args, **kwargs
            The positional and keyword arguments needed to initialize
            a wx.MenuBar.

        """
        super(wxMenuBar, self).__init__(*args, **kwargs)
        self._menus = []
        self._visible_menus = []
        self._enabled = True

    #--------------------------------------------------------------------------
    # Private API
    #--------------------------------------------------------------------------
    def OnMenuChanged(self, event):
        """ The event handler for the EVT_MENU_CHANGED event.

        This event handler will synchronize the menu changes with
        the menu bar.

        """
        event.Skip()
        if self.IsAttached():
            menu = event.GetEventObject()

            # First, check for a visibility change. This requires adding
            # or removing the menu from the menu bar.
            visible = menu.IsVisible()
            was_visible = menu in self._visible_menus
            if visible != was_visible:
                if visible:
                    index = self._menus.index(menu)
                    index = min(index, len(self._visible_menus))
                    self._visible_menus.insert(index, menu)
                    self.Insert(index, menu, menu.GetTitle())
                    self.EnableTop(index, menu.IsEnabled())
                else:
                    index = self._visible_menus.index(menu)
                    self._visible_menus.pop(index)
                    self.Remove(index)
                return

            # If the menu isn't visible, there's nothing to do.
            if not visible:
                return

            # For all other state, the menu can be updated in-place.
            index = self._visible_menus.index(menu)
            self.SetMenuLabel(index, menu.GetTitle())
            self.EnableTop(index, menu.IsEnabled())

    #--------------------------------------------------------------------------
    # Public API
    #--------------------------------------------------------------------------
    def IsEnabled(self):
        """ Get whether or not the menu bar is enabled.

        Returns
        -------
        result : bool
            Whether or not the menu bar is enabled.

        """
        return self._enabled

    def SetEnabled(self, enabled):
        """ Set whether or not the menu bar is enabled.

        Parameters
        ----------
        enabled : bool
            Whether or not the menu bar is enabled.

        """
        # Wx does not provide a means for disabling the entire menu
        # bar, so we must do it manually by disabling each menu.
        if self._enabled != enabled:
            self._enabled = enabled
            for menu in self._menus:
                menu._SetBarEnabled(enabled)

    def AddMenu(self, menu):
        """ Add a wxMenu to the menu bar.

        If the menu already exists in the menu bar, this is a no-op.

        Parameters
        ----------
        menu : wxMenu
            The wxMenu instance to add to the menu bar.

        """
        menus = self._menus
        if menu not in menus:
            menus.append(menu)
            if menu.IsVisible():
                self._visible_menus.append(menu)
                self.Append(menu, menu.GetTitle())
            menu.Bind(EVT_MENU_CHANGED, self.OnMenuChanged)
            menu._SetBarEnabled(self._enabled)

    def Update(self):
        """ A method which can be called to update the menu bar.

        Calling this method will manually refresh the state of the
        items in the menu bar. This is useful to call just after 
        attaching the menu bar to a frame, since the menu bar state
        cannot be updated prior to being attached.

        """
        if self.IsAttached():
            for index, menu in enumerate(self._visible_menus):
                self.SetMenuLabel(index, menu.GetTitle())
                if not menu.IsEnabled():
                    self.EnableTop(index, False)


class WxMenuBar(WxWidgetComponent):
    """ A Wx implementation of an Enaml MenuBar.

    """
    #: Storage for the menu ids.
    _menu_ids = []

    #--------------------------------------------------------------------------
    # Setup Methods
    #--------------------------------------------------------------------------
    def create_widget(self, parent, tree):
        """ Create the underlying menu bar widget.

        """
        return wxMenuBar()

    def create(self, tree):
        """ Create and initialize the underlying control.

        """
        super(WxMenuBar, self).create(tree)
        self.set_menu_ids(tree['menu_ids'])

    def init_layout(self):
        """ Initialize the layout for the underlying control.

        """
        super(WxMenuBar, self).init_layout()
        widget = self.widget()
        find_child = self.find_child
        for menu_id in self._menu_ids:
            child = find_child(menu_id)
            if child is not None:
                widget.AddMenu(child.widget())
    
    #--------------------------------------------------------------------------
    # Widget Update Methods
    #--------------------------------------------------------------------------
    def set_menu_ids(self, menu_ids):
        """ Set the menu ids for the underlying control.

        """
        self._menu_ids = menu_ids

    def set_enabled(self, enabled):
        """ Overridden parent class method.

        This properly sets the enabled state on a menu bar.

        """
        self.widget().SetEnabled(enabled)

    def set_visible(self, visible):
        """ Overrdden parent class method.

        This method is a no-op, since a MenuBar cannot change it's
        visibility under Wx.

        """
        pass

