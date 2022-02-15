# Python imports
import os, threading, time, datetime

# Lib imports
from gi.repository import GLib
import pyscreenshot as capture


# Application imports



def threaded(fn):
    def wrapper(*args, **kwargs):
        threading.Thread(target=fn, args=args, kwargs=kwargs).start()

    return wrapper

class CrossClassSignals:
    def __init__(self, settings):
        self.settings        = settings
        self.builder         = self.settings.returnBuilder()
        self.SCREENSHOTS_DIR = self.settings.returnScreenshotsDir()
        self.fileStore       = self.builder.get_object("fileStore")
        self.refreshingState = False


    def returnRefreshingState(self):
        return self.refreshingState

    def setRefreshingState(self, state):
        self.refreshingState = state


    @threaded
    def refereshDirectoryList(self):
        self.refreshingState = True
        images = self.returnDirectoryList()
        images.sort()
        if len(images) != len(self.fileStore):
            self.fileStore.clear()
            for image in images:
                GLib.idle_add(self.addToStore, (image))

        # self.fileStore.sort()
        self.refreshingState = False


    @threaded
    def addToStore(self, image):
        self.fileStore.append([image])

    def returnDirectoryList(self):
        files = []

        for file in os.listdir(self.SCREENSHOTS_DIR):
            if os.path.isfile(os.path.join(self.SCREENSHOTS_DIR, file)):
                files.append(file)

        return files


    def boundingBoxGrab(self, x1, y1, x2, y2):
        # childprocess=False needed to not crash program
        im = capture.grab(bbox=(x1, y1, x2, y2), childprocess=False)
        im.save(self.generateScreenshotName())

    def generateScreenshotName(self):
        return self.SCREENSHOTS_DIR + '/scrshot_' + self.getTime() + '.png'

    def getTime(self):
        now  = datetime.datetime.now()
        return now.strftime("%Y-%m-%d %H:%M:%S")

    def sleep(self, wait=None):
        delayAmount = self.builder.get_object("delayAmount")
        if not wait:
            wait = delayAmount.get_value_as_int()

        time.sleep(wait)


    def getClipboardData(self):
        proc    = subprocess.Popen(['xclip','-selection', 'clipboard', '-o'], stdout=subprocess.PIPE)
        retcode = proc.wait()
        data    = proc.stdout.read()
        return data.decode("utf-8").strip()

    def setClipboardData(self, data):
        proc = subprocess.Popen(['xclip','-selection','clipboard'], stdin=subprocess.PIPE)
        proc.stdin.write(data)
        proc.stdin.close()
        retcode = proc.wait()

    def close(self, widget):
        gtk.main_quit()
