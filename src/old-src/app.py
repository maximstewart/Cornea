# Python imports
import inspect
from setproctitle import setproctitle

# Lib imports
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

# Application imports
from core.main_window import MainWindow
from core.drawing_area import DrawingArea
from core.main_menu_popup import MainMenuPopup


class Application:
    def __init__(self, args, unknownargs):
        builder  = settings.get_builder()

        # Gets the methods from the classes and sets to handler.
        # Then, builder connects to any signals it needs.
        classes = [
                    MainWindow(),
                    DrawingArea(),
                    MainMenuPopup()
                ]

        handlers = {}
        for c in classes:
            methods = inspect.getmembers(c, predicate=inspect.ismethod)
            handlers.update(methods)

        builder.connect_signals(handlers)
        window = settings.create_window()
        window.show()
