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

        self.MONITORS: []   = None
        self._monitors_view = None
        self._store         = None

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
        event_system.subscribe("get_selected_monitor", self.get_selected_monitor)
        event_system.subscribe("set_monitor_sensitive", self.set_monitor_sensitive)

    def _load_widgets(self):
        grid, self._store   = self._create_treeview_widget("Monitors")
        self._monitors_view = grid.get_children()[0]

        self._load_monitor_store()

        self.set_monitor_sensitive()
        grid.set_hexpand(True)
        self.add(grid)

    def _load_monitor_store(self):
        self.MONITORS = settings.get_monitor_data()
        i = 0
        for monitor in self.MONITORS:
            if i > 0:
                mon = str(monitor.width) + "x" + str(monitor.height) + "+" + str(monitor.x) + "+" + str(monitor.y)
                self._store.append([mon])
            i += 1

        self._monitors_view.set_cursor(0)

    def get_selected_monitor(self):
        iter = self._monitors_view.get_selection().get_selected()[1]
        path = self._store.get_path(iter)

        # Slot 0 is ref monitor. Need to add 1 to get proper slot
        return self.MONITORS[int(str(path)) + 1]

    def set_monitor_sensitive(self, isSensitive = False):
        self._monitors_view.set_sensitive(isSensitive)
