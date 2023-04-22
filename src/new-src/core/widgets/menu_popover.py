# Python imports
import os
import subprocess

# Lib imports
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

# Application imports


class MenuPopover(Gtk.Popover):
    def __init__(self):
        super(MenuPopover, self).__init__()

        self._revert_name  = None
        self._rename_entry = None

        self._setup_styling()
        self._setup_signals()
        self._subscribe_to_events()
        self._load_widgets()


    def _setup_styling(self):
        self.set_size_request(360, -1)

    def _setup_signals(self):
        # self.connect("grab-focus", self.set_revert_data)
        ...

    def _subscribe_to_events(self):
        event_system.subscribe("set_revert_data", self.set_revert_data)
        event_system.subscribe("show_menu", self.show_menu)
        event_system.subscribe("open_file", self.open_file)

    def _load_widgets(self):
        box  = Gtk.Box()
        box2 = Gtk.Box()

        self._rename_entry = Gtk.Entry()
        revert_button = Gtk.Button(label = "Revert")
        rename_button = Gtk.Button(label = "Rename")
        open_button   = Gtk.Button(label = "Open")
        delete_button = Gtk.Button(label = "Delete")

        revert_button.set_image( Gtk.Image.new_from_icon_name("gtk-undo", 16) )
        rename_button.set_image( Gtk.Image.new_from_icon_name("gtk-edit", 16) )
        open_button.set_image( Gtk.Image.new_from_icon_name("gtk-open", 16) )
        delete_button.set_image( Gtk.Image.new_from_icon_name("gtk-delete", 16) )

        revert_button.set_always_show_image(True)
        rename_button.set_always_show_image(True)
        open_button.set_always_show_image(True)
        delete_button.set_always_show_image(True)
        box.set_orientation(Gtk.Orientation.VERTICAL)
        box2.set_orientation(Gtk.Orientation.HORIZONTAL)
        self._rename_entry.set_hexpand(True)

        box2.add(self._rename_entry)
        box2.add(revert_button)
        box.add(box2)
        box.add(rename_button)
        box.add(open_button)
        box.add(delete_button)

        revert_button.connect("clicked", self.revert_name)
        rename_button.connect("clicked", self.rename_file)
        open_button.connect("clicked", self.open_file)
        delete_button.connect("clicked", self.delete_file)

        box.show_all()
        self.add(box)


    def set_revert_data(self, name):
        if not name in ("", None):
            self._revert_name = name
            self._rename_entry.set_text(name)

    def show_menu(self, name):
        if not name in ("", None):
            self.set_revert_data(name)
            self.popup()

    def revert_name(self, widget = None, data = None):
        self._rename_entry.set_text(self._revert_name)

    def rename_file(self, widget, data=None):
        dir           = settings.get_screenshots_dir()
        new_name      = self._rename_entry.get_text().strip()

        old_file_path = os.path.join(dir, self._revert_name)
        new_file_path = os.path.join(dir, new_name)

        try:
            if os.path.isfile(old_file_path) and not new_name in ("", None):
                os.rename(old_file_path, new_file_path)
                self._revert_name = new_name
        except Exception as e:
            logger.info(e)

    def open_file(self, widget = None, data = None):
        dir  = settings.get_screenshots_dir()
        file = os.path.join(dir, self._revert_name)
        subprocess.Popen(['xdg-open', file], stdout = subprocess.PIPE)

    def delete_file(self, widget, data=None):
        try:
            dir  = settings.get_screenshots_dir()
            file = os.path.join(dir, self._revert_name)
            if os.path.isfile(file):
                os.remove(file)
                self.popdown()
        except Exception as e:
            logger.info(e)
