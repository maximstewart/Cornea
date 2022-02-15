# Python imports
import os

# Lib imports
import gi, cairo
gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')

from gi.repository import Gtk
from gi.repository import Gdk


# Application imports


class Settings:
    def __init__(self):
        self._SCRIPT_PTH     = os.path.dirname(os.path.realpath(__file__))
        self._USER_HOME      = os.path.expanduser('~')
        self._CONFIG_PATH    = f"{self._USER_HOME}/.config/{app_name.lower()}"
        self._GLADE_FILE     = f"{self._CONFIG_PATH}/Main_Window.glade"
        self._CSS_FILE       = f"{self._CONFIG_PATH}/stylesheet.css"
        self._DEFAULT_ICONS  = f"{self._CONFIG_PATH}/icons"
        self._WINDOW_ICON    = f"{self._DEFAULT_ICONS}/{app_name.lower()}.png"
        self._USR_PATH       = f"/usr/share/{app_name.lower()}"
        self.SCREENSHOTS_DIR = f"{self._USER_HOME}/.screenshots"

        if not os.path.exists(self._CONFIG_PATH):
            os.mkdir(self._CONFIG_PATH)
        if not os.path.exists(self._GLADE_FILE):
            self._GLADE_FILE   = f"{self._USR_PATH}/Main_Window.glade"
        if not os.path.exists(self._CSS_FILE):
            self._CSS_FILE     = f"{self._USR_PATH}/stylesheet.css"
        if not os.path.exists(self._WINDOW_ICON):
            self._WINDOW_ICON  = f"{self._USR_PATH}/icons/{app_name.lower()}.png"
        if not os.path.isdir(self.SCREENSHOTS_DIR):
            os.mkdir(self.SCREENSHOTS_DIR)

        # 'Filters'
        self.images = ('.png', '.jpg', '.jpeg', '.gif')

        self.builder = Gtk.Builder()
        self.builder.add_from_file(self._GLADE_FILE)


    def createWindow(self):
        # Get window and connect signals
        window = self.builder.get_object("Main_Window")
        window.connect("delete-event", Gtk.main_quit)
        self.setWindowData(window)
        return window

    def setWindowData(self, window):
        screen = window.get_screen()
        visual = screen.get_rgba_visual()

        if visual != None and screen.is_composited():
            window.set_visual(visual)

        # bind css file
        cssProvider  = Gtk.CssProvider()
        cssProvider.load_from_path(self._CSS_FILE)
        screen       = Gdk.Screen.get_default()
        styleContext = Gtk.StyleContext()
        styleContext.add_provider_for_screen(screen, cssProvider, Gtk.STYLE_PROVIDER_PRIORITY_USER)

    def getMonitorData(self):
        screen      = self.builder.get_object("Main_Window").get_screen()
        wdth        = screen.get_width()
        hght        = screen.get_height()
        mon0        = Gdk.Rectangle()
        mon0.width  = wdth
        mon0.height = hght
        monitors    = []

        monitors.append(mon0)
        for m in range(screen.get_n_monitors()):
            monitors.append(screen.get_monitor_geometry(m))

        return monitors


    def returnBuilder(self):             return self.builder
    def returnScreenshotsDir(self):      return self.SCREENSHOTS_DIR

    # Filter returns
    def returnImagesFilter(self):        return self.images
