# Python imports

# Lib imports
import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')
from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import GLib

# Application imports



class BodyGrid(Gtk.Grid):
    def __init__(self, window, gdk_window):
        super(BodyGrid, self).__init__()

        self._gdk_window   = gdk_window
        self._window       = window
        self._is_dragging  = False
        self._update_block = False
        self._drag_start_x = 0
        self._drag_start_y = 0
        self._current_x    = 0
        self._current_y    = 0
        self._w1           = 0.0
        self._h1           = 0.0

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
        drag_button  = Gtk.Button("")
        close_button = Gtk.Button("x")
        grab_button  = Gtk.Button("Grab")
        bottom_right = Gtk.Button("")
        box2         = Gtk.Box()
        box3         = Gtk.Box()
        box4         = Gtk.Box()
        box5         = Gtk.Box()

        ctx  = drag_button.get_style_context()
        ctx.add_class("expand-button")
        ctx2 = bottom_right.get_style_context()
        ctx2.add_class("expand-button")

        col, row = 1, 1
        self.attach(drag_button, col, row, 11, 1)
        col, row = 12, 1
        self.attach(close_button, col, row, 1, 1)
        col, row = 1, 2
        self.attach(box2, col, row, 5, 3)
        col, row = 1, 5
        self.attach(box3, col, row, 4, 1)
        col, row = 1, 12
        self.attach(box4, col, row, 3, 1)
        col, row = 5, 12
        self.attach(grab_button, col, row, 3, 1)
        col, row = 9, 12
        self.attach(box5, col, row, 3, 1)
        col, row = 12, 12
        self.attach(bottom_right, col, row, 1, 1)

        close_button.set_vexpand(False)
        close_button.set_hexpand(False)
        box2.set_vexpand(True)
        box2.set_hexpand(True)
        box3.set_vexpand(True)
        box3.set_hexpand(True)
        box4.set_vexpand(False)
        box4.set_hexpand(True)
        box5.set_vexpand(False)
        box5.set_hexpand(True)

        drag_button.connect("button-press-event", self._press_event)
        drag_button.connect("motion-notify-event", self._move_motion_event)
        drag_button.connect("button-release-event", self._release_event)
        close_button.connect("button-release-event", self._region_close)
        grab_button.connect("button-release-event", self._region_grab)
        bottom_right.connect("button-press-event", self._press_event)
        bottom_right.connect("motion-notify-event", self._resize_motion_event)
        bottom_right.connect("button-release-event", self._release_event)


    def _region_close(self, widget = None, eve = None):
        event_system.emit("grab_region_hide", (self._window,))

    def _region_grab(self, widget = None, eve = None):
        event_system.emit("grab_region", (self._window,))

    def _press_event(self, widget = None, eve = None):
        window = self.get_parent()
        cursor = Gdk.Cursor(Gdk.CursorType.CROSSHAIR)
        window.get_window().set_cursor(cursor)

        self._is_dragging  = True
        self._drag_start_x = eve.x_root
        self._drag_start_y = eve.y_root

        if self._current_x == 0:
            self._current_x, self._current_y = self._window.get_position()

        self._w1, self._h1 = self._window.get_size()

    def _resize_motion_event(self, widget = None, eve = None):
        if self._update_block: return

        x1 = self._drag_start_x
        y1 = self._drag_start_y
        x2 = eve.x_root
        y2 = eve.y_root
        w  = 0
        h  = 0

        if x2 > x1: # Is growing
            w = self._w1 + (x2 - x1)
        else:       # Is shrinking
            w = self._w1 - (x1 - x2)

        if y2 > y1: # Is growing
            h = self._h1 + (y2 - y1)
        else:       # Is shrinking
            h = self._h1 - (y1 - y2)

        self._update_block = True
        self._window.resize(w, h)
        self._update_block = False

    def _move_motion_event(self, widget = None, eve = None):
        if self._is_dragging:
            if eve.x_root > self._drag_start_x:
                self._current_x += (eve.x_root - self._drag_start_x)
            elif eve.x_root < self._drag_start_x:
                self._current_x -= (self._drag_start_x - eve.x_root)
            else:
                self._current_x = self._current_x

            if eve.y_root > self._drag_start_y:
                self._current_y += (eve.y_root - self._drag_start_y)
            elif eve.y_root < self._drag_start_y:
                self._current_y -= (self._drag_start_y - eve.y_root)
            else:
                self._current_y = self._current_y

            self._drag_start_x = eve.x_root
            self._drag_start_y = eve.y_root

            self._update_block = True
            self._window.move(self._current_x, self._current_y)
            self._update_block = False

    def _release_event(self, widget = None, eve = None):
        window       = self.get_parent()
        watch_cursor = Gdk.Cursor(Gdk.CursorType.ARROW)
        window.get_window().set_cursor(watch_cursor)

        self._is_dragging   = False
        self._drag_start_x = 0
        self._drag_start_y = 0
