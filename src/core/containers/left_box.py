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



class PreviewScroll(Gtk.ScrolledWindow):
    def __init__(self):
        super(PreviewScroll, self).__init__()

        self._setup_styling()
        self._setup_signals()
        self._subscribe_to_events()
        self._load_widgets()

        self.show_all()


    def _setup_styling(self):
        self.set_vexpand(True)
        self.set_hexpand(True)

    def _setup_signals(self):
        ...

    def _subscribe_to_events(self):
        ...

    def _load_widgets(self):
        viewport = Gtk.Viewport()
        eve_box  = Gtk.EventBox()

        eve_box.add(PreviewPane())
        viewport.add(eve_box)
        self.add(viewport)

        eve_box.connect("button-release-event", self._handle_clicks)
        viewport.connect("size-allocate", self._scale_image)

    def _scale_image(self, widget = None, allocation = None):
        preview_image = widget.get_children()[0].get_children()[0]

        if not preview_image.pixbuf in ("", None):
            pixbuf = preview_image.scale_to_container(preview_image.pixbuf)
            preview_image.set_from_pixbuf(pixbuf)

    def _handle_clicks(self, widget = None, eve = None):
        preview_image = widget.get_children()[0]

        if eve.button == 3 and not preview_image.file_name in ("", None):
            event_system.emit("set_revert_data", (preview_image.file_name,))
            event_system.emit("show_menu", (preview_image.file_name,))


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
        self.add(PreviewScroll())
