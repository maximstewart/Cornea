# Python imports
import time

# Lib imports
import gi
gi.require_version('Gdk', '3.0')
from gi.repository import Gdk
from gi.repository import GLib

import pyscreenshot as capture

# Application imports
from .widgets.region.window import RegionWindow



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
        event_system.subscribe("grab_region_hide", self._grab_region_hide)
        event_system.subscribe("grab_region", self._grab_region)
        event_system.subscribe("grab_selected_monitor", self.grab_selected_monitor)

    def _load_widgets(self):
        RegionWindow()


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
        logger.info("Passing to Region Handler...")
        window = settings.get_main_window()
        window.hide()
        event_system.emit("show_region_window")

    def _grab_region_hide(self, region_window):
        region_window.hide()
        window = settings.get_main_window()
        window.show()

    def _grab_region(self, region_window, x1, y1, x2, y2):
        def show_region_window():
            # NOTE: No clue why showing window has it move outta prior place.
            #       So, move back to original spot before showing...
            region_window.move(0, 0)
            region_window.show()

        @daemon_threaded
        def do_bounding_box_grab(x1, y1, x2, y2):
            while region_window.is_visible():
                ...

            time.sleep(0.5)
            im = capture.grab(bbox = (x1, y1, x2, y2), childprocess = False)
            im.save( settings.generate_screenshot_name() )
            GLib.idle_add(show_region_window)

        region_window.hide()
        offset = 1
        do_bounding_box_grab(x1 - offset, y1 - offset, x2 + offset, y2 + offset)

    def _old_grab_region(self, region_window):
        logger.info("Grabbing Selected Region...")
        x1, y1 = region_window.get_position()
        w, h = region_window.get_size()
        x2   = x + w
        y2   = y + h

        def show_region_window():
            # NOTE: No clue why showing window has it move outta prior place.
            #       So, move back to original spot before showing...
            region_window.move(x, y)
            region_window.show()

        @daemon_threaded
        def do_bounding_box_grab(x1, y1, x2, y2):
            while region_window.is_visible():
                ...

            time.sleep(0.5)
            im = capture.grab(bbox = (x1, y1, x2, y2), childprocess = False)
            im.save( settings.generate_screenshot_name() )
            GLib.idle_add(show_region_window)

        region_window.hide()
        offset = 1
        do_bounding_box_grab(x1 - offset, y1 - offset, x2 + offset, y2 + offset)


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