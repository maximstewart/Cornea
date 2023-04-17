# Python imports

# Lib imports
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

# Application imports



class RadioButtons(Gtk.Box):
    def __init__(self):
        super(RadioButtons, self).__init__()

        self._setup_styling()
        self._setup_signals()
        self._subscribe_to_events()
        self._load_widgets()

        self.show_all()


    def _setup_styling(self):
        self.set_orientation(Gtk.Orientation.HORIZONTAL)

    def _setup_signals(self):
        ...

    def _subscribe_to_events(self):
        event_system.subscribe("get_screenshot_type", self._get_active_type)

    def _load_widgets(self):
        radio_1 = Gtk.RadioButton(label = "Entire Screen")
        radio_2 = Gtk.RadioButton(label = "Active Window")
        radio_3 = Gtk.RadioButton(label = "Select Region")
        radio_4 = Gtk.RadioButton(label = "Select Monitor")

        self.add(radio_1)
        self.add(radio_2)
        self.add(radio_3)
        self.add(radio_4)

        self._setup_data()

    def _setup_data(self):
        last_child = None
        for child in self.get_children():
            if last_child:
                child.join_group(last_child)
            else:
                last_child = child

    def _get_active_type(self):
        group        = self.get_children()[0].get_group()
        active_radio = [r for r in group if r.get_active()]
        return active_radio[0]
