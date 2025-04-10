# Python imports

# Lib imports
import gi
import cairo
gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')
from gi.repository import Gtk
from gi.repository import Gdk

# Application imports
from .draw_area import DrawArea



class RegionWindow(Gtk.Window):
    def __init__(self):
        super(RegionWindow, self).__init__()

        self._set_window_data()
        self._setup_styling()
        self._setup_signals()
        self._subscribe_to_events()
        self._load_widgets()


    def _setup_styling(self):
        screen = Gdk.Screen.get_default()
        ctx    = self.get_style_context()

        self.set_keep_above(True)
        self.set_deletable(False)
        self.set_decorated(False)
        self.set_resizable(True)
        self.set_skip_pager_hint(True)
        self.set_skip_taskbar_hint(True)
        self.set_has_resize_grip(True)

        self.move(0, 0)
        self.set_size_request(
            *self.get_screen_size(
                Gdk.Display.get_default()
            )
        )


    def _setup_signals(self):
        ...

    def _subscribe_to_events(self):
        event_system.subscribe("show_region_window", self._show_region_window)

    def _load_widgets(self):
        self.add( DrawArea() )

    def _set_window_data(self) -> None:
        screen = self.get_screen()
        visual = screen.get_rgba_visual()

        if visual != None and screen.is_composited():
            self.set_visual(visual)
            self.set_app_paintable(True)

        # bind css file
        cssProvider  = Gtk.CssProvider()
        cssProvider.load_from_path( settings.get_css_file() )
        screen       = Gdk.Screen.get_default()
        styleContext = Gtk.StyleContext()
        styleContext.add_provider_for_screen(screen, cssProvider, Gtk.STYLE_PROVIDER_PRIORITY_USER)

    def get_screen_size(self, display):
        mon_geoms = [
            display.get_monitor(i).get_geometry()
            for i in range(display.get_n_monitors())
        ]

        x0 = min(r.x            for r in mon_geoms)
        y0 = min(r.y            for r in mon_geoms)
        x1 = max(r.x + r.width  for r in mon_geoms)
        y1 = max(r.y + r.height for r in mon_geoms)

        return x1 - x0, y1 - y0

    def _area_draw(self, widget: Gtk.ApplicationWindow, cr: cairo.Context) -> None:
        cr.set_source_rgba( *(0, 0, 0, 0.0) )
        cr.set_operator(cairo.OPERATOR_SOURCE)
        cr.paint()
        cr.set_operator(cairo.OPERATOR_OVER)


    def _show_region_window(self):
        self.show()