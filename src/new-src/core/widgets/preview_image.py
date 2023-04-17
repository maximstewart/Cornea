# Python imports

# Lib imports
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

# Application imports



class PreviewPane(Gtk.AspectFrame):
    def __init__(self):
        super(PreviewPane, self).__init__()

        self._preview_image = None

        self._setup_styling()
        self._setup_signals()
        self._load_widgets()

        self.show_all()


    def _setup_styling(self):
        self.set_size_request(312, 312)

    def _setup_signals(self):
        ...

    def _load_widgets(self):
        self._preview_image = Gtk.Image()
        self.add(self._preview_image)
