# Python imports

# Lib imports
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

# Application imports



class SnapshotButton(Gtk.Button):
    def __init__(self):
        super(SnapshotButton, self).__init__()

        self._setup_styling()
        self._setup_signals()
        self._subscribe_to_events()
        self._load_widgets()

        self.show_all()


    def _setup_styling(self):
        self.set_always_show_image(True)
        self.set_image_position(Gtk.PositionType.LEFT)
        self.set_label("Take Snapshot")

    def _setup_signals(self):
        self.connect("clicked", self._take_snapshot)

    def _subscribe_to_events(self):
        ...

    def _load_widgets(self):
        image = Gtk.Image.new_from_icon_name("gtk-media-play", 3)
        self.set_image(image)

    def _take_snapshot(self, widget = None, eve = None):
        active = event_system.emit_and_await("get_screenshot_type").get_label()
        if "Entire Screen" in active:
            event_system.emit("grab_entire_screen")
        if "Active Window" in active:
            event_system.emit("grab_active_window")
        if "Select Region" in active:
            event_system.emit("pass_to_region_handler")
        if "Select Monitor" in active:
            event_system.emit("grab_selected_monitor")
