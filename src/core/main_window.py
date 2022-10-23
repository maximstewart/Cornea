# Python imports
import os, signal, time
import pyscreenshot as capture

# Lib imports
import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')

from gi.repository import Gtk as Gtk
from gi.repository import Gdk as Gdk
from gi.repository import GLib

# Application imports



class MouseButtons:
    LEFT_BUTTON  = 1
    RIGHT_BUTTON = 3


class MainWindow:
    def __init__(self):
        self.builder       = settings.get_builder()
        self.main_window   = self.builder.get_object('Main_Window')
        self.region_window = self.builder.get_object('Region_Window')
        self.monitors_view = self.builder.get_object("monitorsView")
        self.monitor_store = self.builder.get_object("monitorStore")
        self.MONITORS      = settings.get_monitor_data()

        # Not adding the reference monitor
        i = 0
        for monitor in self.MONITORS:
            if i > 0:
                mon = str(monitor.width) + "x" + str(monitor.height) + "+" + str(monitor.x) + "+" + str(monitor.y)
                self.monitor_store.append([mon])
            i += 1

        self.monitors_view.set_cursor(1)

        self.SCREENSHOTS_DIR = settings.get_screenshots_dir()
        utils.referesh_directory_list()

        GLib.unix_signal_add(GLib.PRIORITY_DEFAULT, signal.SIGINT, Gtk.main_quit)


    def take_screenshot(self, widget):
        active_radio = self.get_active_radio()
        active       = active_radio.get_children()[0].get_text()

        if "Entire screen" in active:
            self.grab_entire_screen()
        if "Active window" in active:
            self.get_active_window()
        if "Select a region" in active:
            self.region_window.show_all()
        if "Select a monitor" in active:
            self.snapshot_monitor()


    def grab_entire_screen(self):
        self.main_window.hide()
        self.get_entire_screen()

    def get_entire_screen(self):
        # childprocess=False needed to not crash program
        im = capture.grab(childprocess=False)
        im.save(utils.generate_screenshot_name())
        self.main_window.show()
        utils.referesh_directory_list()

    def get_active_window(self):
        utils.sleep()

        screen = Gdk.get_default_root_window().get_screen()
        w      = screen.get_active_window()
        pb     = Gdk.pixbuf_get_from_window(w, *w.get_geometry())
        pb.savev(utils.generate_screenshot_name(), "png", (), ())
        utils.referesh_directory_list()



    @daemon_threaded
    def snapshot_monitor(self):
        GLib.idle_add(self.main_window.hide)

        while self.main_window.is_visible():
            ...

        time.sleep(0.05)
        GLib.idle_add(self.do_snapshot_monitor)


    def do_snapshot_monitor(self):
        iterator      = self.monitors_view.get_selection().get_selected()[1]
        path          = self.monitor_store.get_path(iterator)
        # Slot 0 is ref monitor. Need to add 1 to get proper slot
        monitor       = self.MONITORS[int(str(path)) + 1]

        utils.sleep()

        x2 = monitor.x + monitor.width
        y2 = monitor.y + monitor.height
        utils.do_bounding_box_grab(monitor.x, monitor.y, x2, y2)
        utils.referesh_directory_list()
        self.main_window.show()

    def toggle_radio_bttn(self, widget):
        delay_amount   = self.builder.get_object('delayAmount')
        snapshot_bttn  = self.builder.get_object('snapshotBttn')
        active         = self.get_active_radio().get_children()[0].get_text()

        self.region_window.hide()
        self.monitors_view.set_sensitive(False)
        delay_amount.set_sensitive(True)
        snapshot_bttn.set_sensitive(True)
        delay_amount.set_value(0)

        if "Active window" in active:
            delay_amount.set_value(4)
        if "Select a region" in active:
            delay_amount.set_sensitive(False)
        if "Select a monitor" in active:
            self.monitors_view.set_sensitive(True)

    def set_image(self, user_data):
        # We need the refresh state for the files list b/c GtkTreeSelection
        # is calling this method b/c caling this too quickly causes issues...
        if utils.get_refreshing_state() == False:
            selected  = user_data.get_selected()[1]
            if selected:
                fileNameEntry = self.builder.get_object("fileNameEntry")
                imageView     = self.builder.get_object("imageView")
                file          = self.builder.get_object("fileStore").get_value(selected, 0)
                fullPath      = f"{self.SCREENSHOTS_DIR}/{file}"

                try:
                    if os.path.isfile(fullPath):
                        fileNameEntry.set_text(file)
                        pixbuf       = Gtk.Image.new_from_file(fullPath).get_pixbuf()
                        scaledPixBuf = pixbuf.scale_simple(480, 320, 2)  # 2 = BILINEAR and is best by default
                        imageView.set_from_pixbuf(scaledPixBuf)
                except Exception as e:
                    print(e)

    def get_active_radio(self):
        master_radio = self.builder.get_object('entireScrnToggle')
        active_radio = next((
            radio for radio in master_radio.get_group()
                if radio.get_active()
        ))
        return active_radio

    def show_main_menu(self, w, e):
        if e.type == Gdk.EventType.BUTTON_PRESS and e.button == MouseButtons.RIGHT_BUTTON:
            self.builder.get_object("mainMenu").popup()

    def close(self, widget):
        Gtk.main_quit()
