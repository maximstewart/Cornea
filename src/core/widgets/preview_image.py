# Python imports
import os

# Lib imports
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from gi.repository import Gio

# Application imports



class PreviewPane(Gtk.AspectFrame):
    def __init__(self):
        super(PreviewPane, self).__init__()

        self._preview_image = None

        self._setup_styling()
        self._setup_signals()
        self._subscribe_to_events()
        self._load_widgets()

        self.show_all()


    def _setup_styling(self):
        self.set_size_request(312, 312)

    def _setup_signals(self):
        ...

    def _subscribe_to_events(self):
        event_system.subscribe("set_image_to_view", self.set_image_to_view)
        event_system.subscribe("unset_image_preview", self.unset_image_preview)

    def _load_widgets(self):
        self._preview_image = Gtk.Image()
        self.unset_image_preview()
        self.add(self._preview_image)

    def set_image_to_view(self, image_file):
        if not image_file:
            return

        images_dir   = settings.get_screenshots_dir()
        path         = os.path.join(images_dir, image_file)

        pixbuf       = Gtk.Image.new_from_file(path).get_pixbuf()
        scaledPixBuf = pixbuf.scale_simple(480, 320, 2)  # 2 = BILINEAR and is best by default
        self._preview_image.set_from_pixbuf(scaledPixBuf)

    def unset_image_preview(self):
        pixbuf = Gtk.Image.new_from_icon_name("gtk-missing-image", 4).get_pixbuf()
        self._preview_image.set_from_pixbuf(pixbuf)
