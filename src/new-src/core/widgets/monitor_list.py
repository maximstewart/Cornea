# Python imports

# Lib imports
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

# Application imports
from mixins.tree_nixin import TreeMixin



class MonitorList(TreeMixin, Gtk.Box):
    def __init__(self):
        super(MonitorList, self).__init__()

        self._store = None

        self._setup_styling()
        self._setup_signals()
        self._subscribe_to_events()
        self._load_widgets()

        self.show_all()


    def _setup_styling(self):
        self.set_hexpand(False)

    def _setup_signals(self):
        ...

    def _subscribe_to_events(self):
        ...

    def _load_widgets(self):
        grid, self._store = self._create_treeview_widget("Monitors")
        self._load_monitor_store()

        grid.set_hexpand(True)
        self.add(grid)

    def _load_monitor_store(self):
        MONITORS = settings.get_monitor_data()
        i = 0
        for monitor in MONITORS:
            if i > 0:
                mon = str(monitor.width) + "x" + str(monitor.height) + "+" + str(monitor.x) + "+" + str(monitor.y)
                self._store.append([mon])
            i += 1
