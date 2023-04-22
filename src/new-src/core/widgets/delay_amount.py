# Python imports
import time

# Lib imports
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

# Application imports



class DelayAmount(Gtk.Box):
    def __init__(self):
        super(DelayAmount, self).__init__()

        self._setup_styling()
        self._setup_signals()
        self._subscribe_to_events()
        self._load_widgets()

        self.show_all()


    def _setup_styling(self):
        self.set_orientation(Gtk.Orientation.HORIZONTAL)
        self.set_margin_top(5)
        self.set_margin_bottom(5)

    def _setup_signals(self):
        ...

    def _subscribe_to_events(self):
        event_system.subscribe("set_grab_delay", self.set_grab_delay)
        event_system.subscribe("grab_delay", self.grab_delay)

    def _load_widgets(self):
        label   = Gtk.Label("Timeout:  ")
        spinner = Gtk.SpinButton()

        spinner.set_hexpand(True)
        spinner.set_numeric(True)
        spinner.set_snap_to_ticks(True)
        spinner.set_digits(0)
        spinner.set_range(0, 120)
        spinner.set_increments(1, 5)

        self.add(label)
        self.add(spinner)

    def set_grab_delay(self, wait = 0.0):
        delay_amount = self.get_children()[1]
        delay_amount.set_value(wait)


    def grab_delay(self, wait = None):
        delay_amount = self.get_children()[1]
        if not wait:
            wait = delay_amount.get_value_as_int()

        time.sleep(wait)
