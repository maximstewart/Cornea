# Gtk imports
import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')

from gi.repository import Gtk as gtk
from gi.repository import Gdk as gdk
from gi.repository import GLib as glib

# Python imports
import threading, subprocess, os
import pyscreenshot as capture

# Application imports


def threaded(fn):
    def wrapper(*args, **kwargs):
        threading.Thread(target=fn, args=args, kwargs=kwargs).start()

    return wrapper

class MouseButtons:
    LEFT_BUTTON  = 1
    RIGHT_BUTTON = 3


class MainWindow:
    def __init__(self, settings, utilsClass):
        self.settings     = settings
        self.utilsClass   = utilsClass
        self.builder      = self.settings.returnBuilder()

        self.mainWindow   = self.builder.get_object('Main_Window')
        self.regionWindow = self.builder.get_object('Region_Window')
        self.monitorStore = self.builder.get_object("monitorStore")
        self.MONITORS     = self.settings.getMonitorData()

        # Not adding the reference monitor
        i = 0
        for monitor in self.MONITORS:
            if i > 0:
                mon = str(monitor.width) + "x" + str(monitor.height) + "+" + str(monitor.x) + "+" + str(monitor.y)
                self.monitorStore.append([mon])
            i += 1

        monitorsView = self.builder.get_object("monitorsView")
        monitorsView.set_cursor(1)

        self.SCREENSHOTS_DIR = self.settings.returnScreenshotsDir()
        self.utilsClass.refereshDirectoryList()



    def take_screenshot(self, widget):
        active_radio = self.getActiveRadio()
        active       = active_radio.get_children()[0].get_text()

        if "Entire screen" in active:
            self.getEntireScreen()
            self.utilsClass.refereshDirectoryList()
        if "Active window" in active:
            self.getActiveWindow()
            self.utilsClass.refereshDirectoryList()
        if "Select a region" in active:
            self.regionWindow.show_all()
        if "Select a monitor" in active:
            self.snapshotMonitor()
            self.utilsClass.refereshDirectoryList()


    def getEntireScreen(self):
        self.utilsClass.sleep()
        # childprocess=False needed to not crash program
        im = capture.grab(childprocess=False)
        im.save(self.utilsClass.generateScreenshotName())

    def getActiveWindow(self):
        self.utilsClass.sleep()

        screen = gdk.get_default_root_window().get_screen()
        w      = screen.get_active_window()
        pb     = gdk.pixbuf_get_from_window(w, *w.get_geometry())
        pb.savev(self.utilsClass.generateScreenshotName(), "png", (), ())

    def snapshotMonitor(self):
        monitorsView = self.builder.get_object("monitorsView")
        iterator     = monitorsView.get_selection().get_selected()[1]
        path         = self.monitorStore.get_path(iterator)
        # Slot 0 is ref monitor. Need to add 1 to get proper slot
        monitor      = self.MONITORS[int(str(path)) + 1]

        self.utilsClass.sleep()

        x2 = monitor.x + monitor.width
        y2 = monitor.y + monitor.height
        self.utilsClass.boundingBoxGrab(monitor.x, monitor.y, x2, y2)

    def toggleRadioBttn(self, widget):
        monitorsView  = self.builder.get_object('monitorsView')
        delayAmount   = self.builder.get_object('delayAmount')
        snapshotBttn  = self.builder.get_object('snapshotBttn')
        active        = self.getActiveRadio().get_children()[0].get_text()

        self.regionWindow.hide()
        monitorsView.set_sensitive(False)
        delayAmount.set_sensitive(True)
        snapshotBttn.set_sensitive(True)
        delayAmount.set_value(0)

        if "Active window" in active:
            delayAmount.set_value(4)
        if "Select a region" in active:
            delayAmount.set_sensitive(False)
        if "Select a monitor" in active:
            monitorsView.set_sensitive(True)

    def setImage(self, user_data):
        # We need the refresh state for the files list b/c GtkTreeSelection
        # is calling this method b/c caling this too quickly causes issues...
        if self.utilsClass.returnRefreshingState() == False:
            selected  = user_data.get_selected()[1]
            if selected:
                fileNameEntry = self.builder.get_object("fileNameEntry")
                imageView     = self.builder.get_object("imageView")
                file          = self.builder.get_object("fileStore").get_value(selected, 0)
                fullPath      = self.SCREENSHOTS_DIR + "/" + file

                try:
                    if os.path.isfile(fullPath):
                        fileNameEntry.set_text(file)
                        pixbuf       = gtk.Image.new_from_file(fullPath).get_pixbuf()
                        scaledPixBuf = pixbuf.scale_simple(480, 320, 2)  # 2 = BILINEAR and is best by default
                        imageView.set_from_pixbuf(scaledPixBuf)
                except Exception as e:
                    print(e)



    def getActiveRadio(self):
        master_radio = self.builder.get_object('entireScrnToggle')
        active_radio = next((
            radio for radio in master_radio.get_group()
                if radio.get_active()
        ))
        return active_radio

    def showMainMenu(self, w, e):
        if e.type == gdk.EventType.BUTTON_PRESS and e.button == MouseButtons.RIGHT_BUTTON:
            self.builder.get_object("mainMenu").popup()

    def close(self, widget):
        gtk.main_quit()
