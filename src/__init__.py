# Python imports
import inspect

from setproctitle import setproctitle

# Gtk imports
import gi, faulthandler, signal
gi.require_version('Gtk', '3.0')

from gi.repository import Gtk as gtk
from gi.repository import Gdk as gdk
from gi.repository import GLib

# Application imports
from utils import Settings, CrossClassSignals
from signal_classes import MainWindow, DrawingArea, MainMenuPopup


class Main:
    def __init__(self, args):
        settings = Settings()
        builder  = settings.returnBuilder()

        # Gets the methods from the classes and sets to handler.
        # Then, builder connects to any signals it needs.
        utilsClass = CrossClassSignals(settings)
        classes  = [MainWindow(settings, utilsClass),
                    DrawingArea(settings, utilsClass),
                    MainMenuPopup(settings, utilsClass)]

        handlers = {}
        for c in classes:
            methods = inspect.getmembers(c, predicate=inspect.ismethod)
            handlers.update(methods)

        builder.connect_signals(handlers)
        window = settings.createWindow()
        window.show()
