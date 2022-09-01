# Python imports
import inspect, signal
from setproctitle import setproctitle

# Lib imports
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from gi.repository import GLib

# Application imports
from __builtins__ import Builtins
from utils.settings import Settings
from utils.utils import Utils
from core.main_window import MainWindow
from core.drawing_area import DrawingArea
from core.Main_menu_popup import MainMenuPopup


class Application(Builtins):
    def __init__(self, args, unknownargs):
        GLib.unix_signal_add(GLib.PRIORITY_DEFAULT, signal.SIGINT, Gtk.main_quit)

        settings = Settings()
        builder  = settings.get_builder()

        # Gets the methods from the classes and sets to handler.
        # Then, builder connects to any signals it needs.
        utils   = Utils(settings)
        classes = [
                    MainWindow(settings, utils),
                    DrawingArea(settings, utils),
                    MainMenuPopup(settings, utils)
                ]

        handlers = {}
        for c in classes:
            methods = inspect.getmembers(c, predicate=inspect.ismethod)
            handlers.update(methods)

        builder.connect_signals(handlers)
        window = settings.create_window()
        window.show()
