#------------------------------------------------------------------------------
#  Copyright (c) 2012, Enthought, Inc.
#  All rights reserved.
#------------------------------------------------------------------------------
from itertools import izip_longest
from types import MethodType

from enaml.async.async_application import AbstractBuilder, AsyncApplication, \
    AsyncApplicationError

from .mock_test_pipe import MockTestPipe


def make_handler_func(func_name, name, obj):
    func = lambda slf, ctxt: setattr(slf, name, ctxt['value'])
    func.func_name = func_name
    return MethodType(func, obj)


class MockWidget(object):
    """ A mock client UI widget

    """
    def __init__(self, widget_type, parent, send_pipe, recv_pipe):
        self.widget_type = widget_type
        self.parent = parent
        self.send_pipe = send_pipe
        self.recv_pipe = recv_pipe
        self.children = []
        self.attributes = {}
        self.recv_pipe.set_callback(self.recv)
        if parent is not None:
            parent.add_child(self)

    def initialize(self, attributes):
        # Add receive functions for attributes as needed.
        for k in attributes.iterkeys():
            attr_name = 'receive_set_' + k
            recv_func = make_handler_func(attr_name, k, self)
            if not hasattr(self, attr_name):
                setattr(self, attr_name, recv_func)

        self.attributes.update(attributes)

    def add_child(self, widget):
        self.children.append(widget)

    def send(self, msg, ctxt):
        return self.send_pipe.put(msg, ctxt)

    def recv(self, msg, ctxt):
        handler_name = 'receive_' + msg
        handler = getattr(self, handler_name, None)
        if handler is not None:
            return handler(ctxt)
        return NotImplemented


class MockBuilder(AbstractBuilder):
    """ A builder that generates a client-side UI tree.

    """
    def __init__(self):
        self._root = None

    @property
    def root(self):
        return self._root

    def build(self, info):
        info_stack = [(info, None)]
        while info_stack:
            info_dct, parent = info_stack.pop()
            send_pipe = info_dct['send_pipe']
            recv_pipe = info_dct['recv_pipe']
            widget_cls = MockWidget
            # Cross the pipes when hooking the MockWidget up to the server widget
            widget = widget_cls(info_dct['widget'], parent, recv_pipe, send_pipe)
            widget.initialize(info_dct['attrs'])
            children = info_dct['children']
            info_stack.extend(izip_longest(children, [], fillvalue=widget))

            # Store a reference to the root widget to prevent things 
            # from being garbage collected
            if parent is None:
                self._root = widget


class MockApplication(AsyncApplication):
    """ A mock application for testing server widget components.

    """
    def __init__(self):
        self._builder = None

    #--------------------------------------------------------------------------
    # Abstract API implementation
    #--------------------------------------------------------------------------
    def register(self, messenger):
        return (MockTestPipe(), MockTestPipe())

    def builder(self):
        if self._builder is None:
            self._builder = MockBuilder()
        return self._builder
