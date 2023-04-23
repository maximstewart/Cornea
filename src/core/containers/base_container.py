# Python imports

# Lib imports
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

# Application imports
from .left_box import LeftBox
from .right_box import RightBox



class BaseContainer(Gtk.Box):
    def __init__(self):
        super(BaseContainer, self).__init__()

        self._builder = settings.get_builder()

        self._setup_styling()
        self._setup_signals()
        self._load_widgets()

        self.show_all()


    def _setup_styling(self):
        self.set_orientation(Gtk.Orientation.HORIZONTAL)

    def _setup_signals(self):
        ...

    def _load_widgets(self):
        self.add(LeftBox())
        self.add(RightBox())
