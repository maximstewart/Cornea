# Python imports

# Lib imports
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

# Application imports
from ..widgets.snapshot_button import SnapshotButton
from ..widgets.monitor_list import MonitorList
from ..widgets.images_list import ImagesList



class RightBox(Gtk.Box):
    def __init__(self):
        super(RightBox, self).__init__()

        self._setup_styling()
        self._setup_signals()
        self._load_widgets()

        self.show_all()


    def _setup_styling(self):
        self.set_orientation(Gtk.Orientation.VERTICAL)

    def _setup_signals(self):
        ...

    def _load_widgets(self):
        self.add(SnapshotButton())
        self.add(MonitorList())
        self.add(ImagesList())
