# Python imports

# Lib imports
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

# Application imports
from mixins.tree_nixin import TreeMixin



class ImagesList(TreeMixin, Gtk.ScrolledWindow):
    def __init__(self):
        super(ImagesList, self).__init__()

        self._store = None

        self._setup_styling()
        self._setup_signals()
        self._subscribe_to_events()
        self._load_widgets()

        self.show_all()


    def _setup_styling(self):
        self.set_size_request(200, -1)
        self.set_hexpand(False)
        self.set_vexpand(True)
        self.set_margin_top(15)

    def _setup_signals(self):
        ...

    def _subscribe_to_events(self):
        ...

    def _load_widgets(self):
        grid, self._store = self._create_treeview_widget("Images")
        self.referesh_directory_list()
        self.add(grid)

    @threaded
    def referesh_directory_list(self):
        images = settings.get_directory_list()
        images.sort()
        if len(images) != len(self._store):
            self._store.clear()
            for image in images:
                GLib.idle_add(self.add_to_store, (image,))

    def add_to_store(self, image):
        self._store.append(image)
