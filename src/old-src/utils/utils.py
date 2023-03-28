# Python imports
import os, time, datetime

# Lib imports
from gi.repository import GLib
import pyscreenshot as capture

# Application imports




class Utils:
    def __init__(self):
        self.builder          = settings.get_builder()

        self.SCREENSHOTS_DIR  = settings.get_screenshots_dir()
        self.file_store       = self.builder.get_object("fileStore")
        self.refreshing_state = False


    def get_refreshing_state(self):
        return self.refreshing_state

    def set_refreshing_state(self, state):
        self.refreshing_state = state


    @threaded
    def referesh_directory_list(self):
        self.refreshing_state = True

        images = self.get_directory_list()
        images.sort()
        if len(images) != len(self.file_store):
            self.file_store.clear()
            for image in images:
                GLib.idle_add(self.add_to_store, (image))

        self.refreshing_state = False


    def add_to_store(self, image):
        self.file_store.append([image])

    def get_directory_list(self):
        files = []

        for file in os.listdir(self.SCREENSHOTS_DIR):
            if os.path.isfile(os.path.join(self.SCREENSHOTS_DIR, file)):
                files.append(file)

        return files


    def do_bounding_box_grab(self, x1, y1, x2, y2):
        # childprocess=False needed to not crash program
        im = capture.grab(bbox=(x1, y1, x2, y2), childprocess=False)
        im.save(self.generate_screenshot_name())

    def generate_screenshot_name(self):
        return f"{self.SCREENSHOTS_DIR}/scrshot_{self.get_time()}.png"

    def get_time(self):
        now  = datetime.datetime.now()
        return now.strftime("%Y-%m-%d %H:%M:%S")

    def sleep(self, wait=None):
        delay_amount = self.builder.get_object("delayAmount")
        if not wait:
            wait = delay_amount.get_value_as_int()

        time.sleep(wait)


    def get_clipboard_data(self):
        proc    = subprocess.Popen(['xclip','-selection', 'clipboard', '-o'], stdout=subprocess.PIPE)
        retcode = proc.wait()
        data    = proc.stdout.read()
        return data.decode("utf-8").strip()

    def set_clipboard_data(self, data):
        proc = subprocess.Popen(['xclip','-selection','clipboard'], stdin=subprocess.PIPE)
        proc.stdin.write(data)
        proc.stdin.close()
        retcode = proc.wait()

    def close(self, widget):
        gtk.main_quit()
