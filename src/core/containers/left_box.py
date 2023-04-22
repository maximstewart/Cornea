# Python imports

# Lib imports
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

# Application imports
from ..widgets.radio_buttons import RadioButtons
from ..widgets.delay_amount import DelayAmount
from ..widgets.preview_image import PreviewPane
from ..widgets.menu_popover import MenuPopover


class LeftBox(Gtk.Box):
    def __init__(self):
        super(LeftBox, self).__init__()

        self._setup_styling()
        self._setup_signals()
        self._load_widgets()

        self.show_all()


    def _setup_styling(self):
        self.set_orientation(Gtk.Orientation.VERTICAL)

    def _setup_signals(self):
        ...

    def _load_widgets(self):
        menu         = MenuPopover()
        delay_amount = DelayAmount()
        menu.set_relative_to(delay_amount)
        menu.set_position(Gtk.PositionType.BOTTOM)

        self.add(RadioButtons())
        self.add(delay_amount)
        self.add(PreviewPane())