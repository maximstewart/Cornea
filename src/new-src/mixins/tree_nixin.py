# Python imports

# Lib imports
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

# Application imports



class TreeMixin:
    def _create_treeview_widget(self, title = "Not Set"):
        scroll = Gtk.ScrolledWindow()
        grid   = Gtk.TreeView()
        store  = Gtk.ListStore(str)
        column = Gtk.TreeViewColumn(title)
        name   = Gtk.CellRendererText()
        selec  = grid.get_selection()

        grid.set_model(store)
        selec.set_mode(2)
        scroll.set_size_request(145, 96)

        column.pack_start(name, True)
        column.add_attribute(name, "text", 0)
        column.set_expand(False)

        grid.append_column(column)
        grid.set_search_column(0)
        grid.set_headers_visible(True)
        grid.set_enable_tree_lines(False)

        grid.show_all()
        scroll.add(grid)
        grid.columns_autosize()
        return scroll, store
