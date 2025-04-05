# Python imports

# Lib imports
import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')
from gi.repository import Gtk
from gi.repository import Gdk

# Application imports
from .draw_types.draw_cross import DrawCross
from .draw_types.draw_grab_region import DrawGrabRegion



class DrawArea(Gtk.DrawingArea):
    def __init__(self):
        super(DrawArea, self).__init__()


        self.draw_type: DrawType = DrawCross()
        self.region_mode: bool   = False
        self.grab_mode: bool     = False
        self.mouse_x: int        = 0
        self.mouse_y: int        = 0


        self._setup_style()
        self._setup_signals()
        self._load_widgets()

        self.show()

        self._render_start_cross_hair()


    def _setup_style(self):
        self.set_property("can-focus", True)

    def _setup_signals(self):
        self.add_events( Gdk.EventMask.ALL_EVENTS_MASK )

        self.connect("motion-notify-event", self._motion_notify_event)
        self.connect("button-press-event", self._button_press_event)
        self.connect("button-release-event", self._button_release_event)
        self.connect("realize", self._realize)
        self.connect("draw", self._draw)

    def _load_widgets(self):
        ...

    def _render_start_cross_hair(self):
        self.mouse_x = self.get_allocated_width() / 2
        self.mouse_y = self.get_allocated_height() / 2
        self.queue_draw()

    def _realize(self, widget):
        self._hide_cursor()

    def _draw(self, area, cr):
        self.draw_type.draw(area, cr)

    def _motion_notify_event(self, widget, eve):
        if self.grab_mode: return
        self._set_coords(eve)
        self.queue_draw()

    def _button_press_event(self, widget, eve):
        if self.grab_mode: return
        if not eve.button == 1: return
        self._set_to_region_mode(eve)

    def _button_release_event(self, widget, eve):
        if self.grab_mode and eve.button == 2: # m-click
            self._do_grab()
            return

        if not eve.button in [1, 3]: return # l or r-click

        self._show_cursor()

        if eve.button == 3: # r-click
            event_system.emit("grab_region_hide", (self.get_parent(),))
            return

        if self.grab_mode:
            self._hide_cursor()
            self._unset_grab_mode(eve)
            return

        self._set_to_grab_mode(eve)

    def _show_cursor(self):
        window       = self.get_parent()
        watch_cursor = Gdk.Cursor(Gdk.CursorType.ARROW)
        window.get_window().set_cursor(watch_cursor)

    def _hide_cursor(self):
        window       = self.get_parent()
        watch_cursor = Gdk.Cursor(Gdk.CursorType.BLANK_CURSOR )
        window.get_window().set_cursor(watch_cursor)

    def _set_to_region_mode(self, eve):
        self.region_mode    = True
        self.draw_type      = DrawGrabRegion()
        self._set_coords(eve)

    def _set_to_grab_mode(self, eve):
        self._set_coords(eve)
        self.region_mode  = False
        self.grab_mode    = True

    def _unset_grab_mode(self, eve):
        self.grab_mode   = False
        self.draw_type   = DrawCross()
        self._set_coords(eve)
        self.queue_draw()

    def _set_coords(self, eve):
        if not self.region_mode:
            self.mouse_x        = int(eve.x)
            self.mouse_y        = int(eve.y)
            self.region_start_x = int(eve.x)
            self.region_start_y = int(eve.y)
        else:
            self.region_end_x   = int(eve.x)
            self.region_end_y   = int(eve.y)

    def _do_grab(self):
        sx = self.region_start_x
        sy = self.region_start_y
        ex = self.region_end_x
        ey = self.region_end_y

        x1 = sx
        y1 = sy
        x2 = ex
        y2 = ey

        if sx > ex and sy < ey:               # NE to SW
            x1 = sx - (sx - ex)
            y1 = sy
            x2 = sx
            y2 = sy + (ey - sy)
        elif not ex > sx and not ey > sy:     # SE to NW
            x1 = ex
            y1 = ey
            x2 = sx
            y2 = sy
        elif ex > sx and ey < sy:             # SW to NE
            x1 = ex - (ex - sx)
            y1 = ey
            x2 = ex
            y2 = ey + (sy - ey)

        event_system.emit(
            "grab_region",
            (
                self.get_parent(),
                x1,
                y1,
                x2,
                y2,
            )
        )


