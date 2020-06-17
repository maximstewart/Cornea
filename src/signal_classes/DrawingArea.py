# Gtk imports
import gi, cairo
gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')

from gi.repository import Gtk as gtk
from gi.repository import Gdk as gdk
from gi.repository import GLib as glib


# Python imports
import threading, html

import pyscreenshot as capture

# Application imports



def threaded(fn):
    def wrapper(*args, **kwargs):
        threading.Thread(target=fn, args=args, kwargs=kwargs).start()

    return wrapper

class MouseButtons:
    LEFT_BUTTON  = 1
    RIGHT_BUTTON = 3


class DrawingArea:
    def __init__(self, settings, utilsClass):
        self.settings     = settings
        self.utilsClass   = utilsClass
        self.builder      = self.settings.returnBuilder()

        self.mainWindow   = self.builder.get_object('Main_Window')
        self.regionWindow = self.builder.get_object('Region_Window')
        self.regionMenu   = self.builder.get_object('regionMenu')
        self.messageLabel = self.builder.get_object('messageLabel')
        MONITOR           = self.settings.getMonitorData()

        self.settings.setWindowData(self.regionWindow)
        self.regionWindow.set_default_size(MONITOR[0].width, MONITOR[0].height)
        self.regionWindow.set_size_request(MONITOR[0].width, MONITOR[0].height)
        self.regionWindow.set_keep_above(True)

        self.DRAW_AREA = self.builder.get_object("selectionArea")
        self.DRAW_AREA.add_events(gdk.EventMask.BUTTON_PRESS_MASK)
        self.DRAW_AREA.add_events(gdk.EventMask.BUTTON_RELEASE_MASK)
        self.DRAW_AREA.add_events(gdk.EventMask.BUTTON1_MOTION_MASK)
        self.DRAW_AREA.connect("button-press-event", self.on_button_press)
        self.DRAW_AREA.connect("button-release-event", self.on_button_release)
        self.DRAW_AREA.connect("motion-notify-event", self.on_mouse_move)
        self.DRAW_AREA.connect("draw", self.on_draw)

        area                 = self.settings.getMonitorData()[0]
        self.SCREENSHOTS_DIR = self.settings.returnScreenshotsDir()
        self.WIN_REC         = [area.x, area.y, area.width, area.height]
        self.coords          = [[0.0, 0.0], [0.0, 0.0]] # point1 and point2
        self.BORDER_COLOR    = [255, 0, 0, 0.84]
        self.TRANS_COLOR     = [0, 0, 0, 0.0]
        self.BG_COLOR        = [0, 0, 0, 0.4]
        self.success         = "#88cc27"
        self.warning         = "#ffa800"
        self.error           = "#ff0000"
        self.rec             = None
        self.cr              = None

        self.regionWindow.set_default_size(area.width, area.height)
        self.regionWindow.set_size_request(area.width, area.height)
        self.regionWindow.move(area.x, area.y)
        self.regionWindow.set_resizable(False)
        self.regionWindow.set_keep_above(True)



    def on_button_press(self, w, e):
        self.messageLabel.set_markup("")
        if e.type == gdk.EventType.BUTTON_PRESS and e.button == MouseButtons.LEFT_BUTTON:
            self.coords[0] = [e.x, e.y]
            self.regionMenu.hide()

            # This will reset draw area initially. No further use
            if self.cr:
                self.draw(self.cr, self.WIN_REC, self.BG_COLOR)
                self.DRAW_AREA.queue_draw()
        if e.type == gdk.EventType.BUTTON_PRESS and e.button == MouseButtons.RIGHT_BUTTON:
            self.regionMenu.show()

    # Update second set of coords.
    def on_mouse_move(self, w, e):
        self.coords[1] = [e.x, e.y]
        self.DRAW_AREA.queue_draw()

    @threaded
    def on_button_release(self, w, e):
        if e.type == gdk.EventType.BUTTON_RELEASE and e.button == MouseButtons.LEFT_BUTTON:
            glib.idle_add(self.regionMenu.show)


    @threaded
    def grabRegion(self, widget):
        glib.idle_add(self.regionMenu.hide)
        glib.idle_add(self.mainWindow.hide)
        self.boundingBoxGrab(self.rec[0], self.rec[1], self.rec[2], self.rec[3])
        glib.idle_add(self.regionMenu.show)
        glib.idle_add(self.mainWindow.show)
        self.utilsClass.refereshDirectoryList()

    @threaded
    def returnToMainWindow(self, widget):
        glib.idle_add(self.regionWindow.hide)
        glib.idle_add(self.regionMenu.hide)
        glib.idle_add(self.mainWindow.show)


    def on_draw(self, wid, cr):
        if not self.cr: self.cr = cr
        # Reset the screen with transparent view
        self.draw(cr, self.WIN_REC, self.BG_COLOR)

        point1   = self.coords[0]
        point2   = self.coords[1]
        x1       = point1[0]
        y1       = point1[1]
        x2       = point2[0]
        y2       = point2[1]
        w        = x2 - x1
        h        = y2 - y1

        # Rectangle information for region and screen grab
        self.rec = [int(x1), int(y1), int(x2), int(y2)]
        # Draw the new selection region
        self.selectionDraw(cr, [x1, y1, w, h], self.BORDER_COLOR, self.TRANS_COLOR)


    def draw(self, cr, x1y1wh, rgba):
        cr.set_source_rgba(rgba[0], rgba[1], rgba[2], rgba[3])
        cr.rectangle(x1y1wh[0], x1y1wh[1], x1y1wh[2], x1y1wh[3])
        cr.set_operator(1);
        cr.fill()

    def selectionDraw(self, cr, x1y1wh, brdrcol, transclr):
        # Clear the region
        cr.set_source_rgba(transclr[0], transclr[1], transclr[2], transclr[3])
        cr.rectangle(x1y1wh[0], x1y1wh[1], x1y1wh[2], x1y1wh[3])
        cr.set_operator(0);
        cr.fill()

        # Draw a border
        cr.set_source_rgba(brdrcol[0], brdrcol[1], brdrcol[2], brdrcol[3])
        cr.rectangle(x1y1wh[0] - 2, x1y1wh[1] - 2, x1y1wh[2] + 4, x1y1wh[3] + 4)
        cr.set_operator(1);
        cr.stroke()

    # Actual region grab
    def boundingBoxGrab(self, x1, y1, x2, y2):
        self.utilsClass.sleep(0.4)
        try:
            temp = 0;
            if x2 < x1:
                temp = x1
                x1   = x2
                x2   = temp

            if y2 < y1:
                temp = y1
                y1   = y2
                y2   = temp


            self.utilsClass.boundingBoxGrab(x1, y1, x2, y2)
            markup = "<span foreground='" + self.success + "'>Grabbed region successfully...</span>"
            glib.idle_add(self.messageLabel.set_markup, markup)
        except Exception as e:
            print(e)
            markup = "<span foreground='" + self.warning + "' >Oops...</span>" + \
                    "\n<span foreground='" + self.error + "'>" + html.escape( str(e) ) + "</span>"
            glib.idle_add(self.messageLabel.set_markup, markup)
