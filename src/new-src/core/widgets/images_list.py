# Python imports

# Lib imports
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from gi.repository import Gio
from gi.repository import GLib

# Application imports
from mixins.tree_nixin import TreeMixin



class ImagesList(TreeMixin, Gtk.ScrolledWindow):
    def __init__(self):
        super(ImagesList, self).__init__()

        self._store = None

        self._set_file_watcher()
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

    def _set_file_watcher(self):
        if settings.is_debug():
            logger.debug(f"Watcher Will Not Be Set...")
            return

        images_dir  = settings.get_screenshots_dir()
        dir_watcher = Gio.File.new_for_path(f"{images_dir}") \
                                .monitor_directory(Gio.FileMonitorFlags.WATCH_MOVES, Gio.Cancellable())

        dir_watcher.connect("changed", self._dir_watch_updates)

    def _dir_watch_updates(self, file_monitor, file, other_file = None, eve_type = None, data = None):
        if eve_type in [Gio.FileMonitorEvent.CREATED, Gio.FileMonitorEvent.DELETED,
                        Gio.FileMonitorEvent.RENAMED, Gio.FileMonitorEvent.MOVED_IN,
                        Gio.FileMonitorEvent.MOVED_OUT]:

            self._store.clear()
            self.referesh_directory_list()

    @threaded
    def referesh_directory_list(self):
        images = settings.get_directory_list()
        images.sort()
        for image in images:
            GLib.idle_add(self.add_to_store, (image,))

    def add_to_store(self, image):
        self._store.append(image)
