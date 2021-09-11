# -*- coding: UTF-8 -*-

# stdlib
from typing import Iterator, Optional

# external
# FIXME missing type stubs for some external libraries
from Xlib import X, Xutil  # type: ignore
from Xlib.display import Display  # type: ignore
from Xlib.protocol.event import ClientMessage  # type: ignore
from Xlib.xobject.drawable import Window  # type: ignore

# internal
from . import log


# TODO tests
class Xlib:
    def __init__(self, display: Optional[Display] = None):
        self.logger = log.create_logger('xlib')

        self.display = display or Display()
        self.logger.debug('Display: %s', self.display)

        self.root_window = self.display.screen().root
        self.logger.debug('Root window: %s', self.root_window)

    def iter_windows(
            self, instance_name: str, class_name: str) \
            -> Iterator[Window]:

        for window in self.root_window.query_tree().children:
            instance_class_name = window.get_wm_class() or (None, None)

            if instance_class_name == (instance_name, class_name):
                self.logger.debug('Matched window: %s', window)
                yield window

    # TODO iconify window is currently broken (use python-libxdo?)
    def iconify_window(self, window: Window) -> None:
        # https://tronche.com/gui/x/xlib/ICC/client-to-window-manager/XIconifyWindow.html
        # https://babbage.cs.qc.cuny.edu/courses/GUIDesign/motif-faq.html

        iconic_state_message = ClientMessage(
            window=window,
            client_type=self.display.intern_atom('WM_CHANGE_STATE'),
            # TODO named constant for `32`?
            data=(32, [Xutil.IconicState] + 4 * [Xutil.NoValue]))

        self.logger.debug('Iconic state message: %s', iconic_state_message)

        window.send_event(
            event=iconic_state_message,
            event_mask=X.SubstructureNotifyMask | X.SubstructureRedirectMask)

    def iconify_windows(self, instance_name: str, class_name: str) -> None:
        for window in self.iter_windows(instance_name, class_name):
            self.iconify_window(window)

    def has_window(self, instance_name: str, class_name: str) -> bool:
        for _ in self.iter_windows(instance_name, class_name):
            return True
        else:
            return False