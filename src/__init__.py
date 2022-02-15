# Python imports
import inspect
from setproctitle import setproctitle

# Lib imports


# Application imports
from __builtins__ import Builtins
from utils import Settings, CrossClassSignals
from signal_classes import MainWindow, DrawingArea, MainMenuPopup


class Main(Builtins):
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
