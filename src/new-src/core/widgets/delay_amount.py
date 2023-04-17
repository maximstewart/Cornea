# Python imports

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
        self._load_widgets()

        self.show_all()


    def _setup_styling(self):
        self.set_orientation(Gtk.Orientation.HORIZONTAL)
        self.set_margin_top(5)
        self.set_margin_bottom(5)

    def _setup_signals(self):
        ...

    def _load_widgets(self):
        label   = Gtk.Label("Timeout:  ")
        spinner = Gtk.SpinButton()

        spinner.set_hexpand(True)
        spinner.set_numeric(True)
        spinner.set_snap_to_ticks(True)
        spinner.set_digits(0)
        spinner.set_range(1, 120)
        spinner.set_increments(1, 5)

        self.add(label)
        self.add(spinner)
