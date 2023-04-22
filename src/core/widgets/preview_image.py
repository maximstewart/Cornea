# Python imports
import os

# Lib imports
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from gi.repository import Gio

# Application imports



class PreviewPane(Gtk.Image):
    def __init__(self):
        super(PreviewPane, self).__init__()

        self.pixbuf = None

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
        event_system.subscribe("set_image_to_view", self.set_image_to_view)
        event_system.subscribe("unset_image_preview", self.unset_image_preview)

    def _load_widgets(self):
        self.unset_image_preview()

    def set_image_to_view(self, image_file):
        if not image_file:
            return

        images_dir  = settings.get_screenshots_dir()
        path        = os.path.join(images_dir, image_file)
        self.pixbuf = Gtk.Image.new_from_file(path).get_pixbuf()
        self.set_from_pixbuf( self.scale_to_container(self.pixbuf) )

    def scale_to_container(self, pixbuf):
        rect = self.get_parent().get_parent().get_allocated_size().allocation
        pxw  = pixbuf.get_width()
        pxh  = pixbuf.get_height()
        h    = rect.height
        w    = (pxw * h) / pxh

        return pixbuf.scale_simple(w, h, 2)  # 2 = BILINEAR and is best by default

    def unset_image_preview(self):
        self.pixbuf = None
        pixbuf      = Gtk.Image.new_from_icon_name("gtk-missing-image", 4).get_pixbuf()
        self.set_from_pixbuf(pixbuf)
