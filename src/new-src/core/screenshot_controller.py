# Python imports

# Lib imports
import gi
gi.require_version('Gdk', '3.0')
from gi.repository import Gdk as Gdk
from gi.repository import GLib

import pyscreenshot as capture

# Application imports



class ScreenshotController:
    def __init__(self):
        super(ScreenshotController, self).__init__()

        self._setup_styling()
        self._setup_signals()
        self._subscribe_to_events()
        self._load_widgets()


    def _setup_styling(self):
        ...

    def _setup_signals(self):
        ...

    def _subscribe_to_events(self):
        event_system.subscribe("grab_entire_screen", self.grab_entire_screen)
        event_system.subscribe("grab_active_window", self.grab_active_window)
        event_system.subscribe("pass_to_region_handler", self.pass_to_region_handler)
        event_system.subscribe("grab_selected_monitor", self.grab_selected_monitor)

    def _load_widgets(self):
        ...

    def grab_entire_screen(self):
        logger.info("Grabbing Entire Screen...")
        window = settings.get_main_window()

        @daemon_threaded
        def do_grab():
            im     = capture.grab(childprocess = False)
            im.save( settings.generate_screenshot_name() )
            GLib.idle_add(window.show)

        window.hide()
        do_grab()


    def grab_active_window(self):
        logger.info("Grabbing Active Window...")

        event_system.emit("grab_delay")
        screen = Gdk.get_default_root_window().get_screen()
        w      = screen.get_active_window()
        pb     = Gdk.pixbuf_get_from_window(w, *w.get_geometry())
        pb.savev(settings.generate_screenshot_name(), "png", (), ())

    def pass_to_region_handler(self):
        logger.info("Grabbing Selected Region Stub...")
        # window  = settings.get_main_window()
        # window.hide()

    def grab_selected_monitor(self):
        logger.info("Grabbing Monitor...")

        window  = settings.get_main_window()
        monitor = event_system.emit_and_await("get_selected_monitor")
        x2      = monitor.x + monitor.width
        y2      = monitor.y + monitor.height

        @daemon_threaded
        def do_bounding_box_grab(x1, y1, x2, y2):
            im = capture.grab(bbox = (x1, y1, x2, y2), childprocess = False)
            im.save( settings.generate_screenshot_name() )
            GLib.idle_add(window.show)

        event_system.emit("grab_delay")
        window.hide()
        do_bounding_box_grab(monitor.x, monitor.y, x2, y2)
