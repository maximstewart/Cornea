# Python imports

# Lib imports
import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')
from gi.repository import Gtk
from gi.repository import Gdk

# Application imports


class BodyGrid(Gtk.Grid):
    def __init__(self):
        super(BodyGrid, self).__init__()

        self._drag_start_x = 0
        self._drag_start_y = 0

        self._setup_styling()
        self._setup_signals()
        self._subscribe_to_events()
        self._load_widgets()

        self.show_all()


    def _setup_styling(self):
        ctx = self.get_style_context()
        ctx.add_class("region-window")
        self.set_vexpand(True)
        self.set_hexpand(True)

    def _setup_signals(self):
        ...

    def _subscribe_to_events(self):
        ...


    def _load_widgets(self):
        top_left     = Gtk.Button("")
        top_right    = Gtk.Button("")
        bottom_left  = Gtk.Button("")
        bottom_right = Gtk.Button("")
        box          = Gtk.Box()
        box2         = Gtk.Box()
        box3         = Gtk.Box()

        ctx1 = top_left.get_style_context()
        ctx1.add_class("expand-button")
        ctx2 = top_right.get_style_context()
        ctx2.add_class("expand-button")
        ctx3 = bottom_left.get_style_context()
        ctx3.add_class("expand-button")
        ctx4 = bottom_right.get_style_context()
        ctx4.add_class("expand-button")

        width, height = 1, 1
        row, col      = 1, 1
        self.attach(top_left, col, row, width, height)
        row, col      = 1, 5
        self.attach(top_right, col, row, width, height)
        row, col      = 5, 1
        self.attach(bottom_left, col, row, width, height)
        row, col      = 5, 5
        self.attach(bottom_right, col, row, width, height)

        row, col      = 1, 2
        self.attach(box, col, row, 1, 1)
        row, col      = 2, 1
        self.attach(box2, col, row, 4, 2)
        row, col      = 5, 2
        self.attach(box3, col, row, 1, 1)

        box.set_vexpand(True)
        box.set_hexpand(True)
        box2.set_vexpand(True)
        box2.set_hexpand(True)
        box3.set_vexpand(True)
        box3.set_hexpand(True)


        top_left.connect("button-press-event", self._press_event)
        top_right.connect("button-press-event", self._press_event)
        bottom_left.connect("button-press-event", self._press_event)
        bottom_right.connect("button-press-event", self._press_event)

        top_left.connect("motion-notify-event", self._resize_motion_event_tl)
        top_right.connect("motion-notify-event", self._resize_motion_event_tr)
        bottom_left.connect("motion-notify-event", self._resize_motion_event_bl)
        bottom_right.connect("motion-notify-event", self._resize_motion_event_br)

        top_left.connect("button-release-event", self._release_event)
        top_right.connect("button-release-event", self._release_event)
        bottom_left.connect("button-release-event", self._release_event)
        bottom_right.connect("button-release-event", self._release_event)



    def _press_event(self, widget = None, eve = None):
        window = self.get_parent()
        cursor = Gdk.Cursor(Gdk.CursorType.CROSSHAIR)

        window.get_window().set_cursor(cursor)
        self.is_dragging   = True
        self._drag_start_x = eve.x
        self._drag_start_y = eve.y

    def _resize_motion_event_tl(self, widget = None, eve = None):
        # if self.is_dragging:
        #     offset_x = eve.x - self._drag_start_x
        #     self._current_w += offset_x
        #     if self._current_w < 0:
        #         self._current_w = -1
        #
        #     self.set_size_request(self._current_w, self._current_h)
        #     self.get_parent().save_needed = True
        ...

    def _resize_motion_event_tr(self, widget = None, eve = None):
        # if self.is_dragging:
        #     offset_x = eve.x - self._drag_start_x
        #     self._current_w += offset_x
        #     if self._current_w < 0:
        #         self._current_w = -1
        #
        #     self.set_size_request(self._current_w, self._current_h)
        #     self.get_parent().save_needed = True
        ...

    def _resize_motion_event_bl(self, widget = None, eve = None):
        # if self.is_dragging:
        #     offset_x = eve.x - self._drag_start_x
        #     self._current_w += offset_x
        #     if self._current_w < 0:
        #         self._current_w = -1
        #
        #     self.set_size_request(self._current_w, self._current_h)
        #     self.get_parent().save_needed = True
        ...

    def _resize_motion_event_br(self, widget = None, eve = None):
        # if self.is_dragging:
        #     offset_x = eve.x - self._drag_start_x
        #     self._current_w += offset_x
        #     if self._current_w < 0:
        #         self._current_w = -1
        #
        #     self.set_size_request(self._current_w, self._current_h)
        #     self.get_parent().save_needed = True
        ...

    def _release_event(self, widget = None, eve = None):
        window       = self.get_parent()
        watch_cursor = Gdk.Cursor(Gdk.CursorType.ARROW)
        window.get_window().set_cursor(watch_cursor)

        self.is_dragging   = False
        self._drag_start_x = 0
        self._drag_start_y = 0
