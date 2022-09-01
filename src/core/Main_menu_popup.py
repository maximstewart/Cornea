# Python imports
import os, subprocess

# lib imports


# Application imports


class MainMenuPopup:
    def __init__(self, _settings, _utils):
        self.settings        = _settings
        self.utils           = _utils

        self.builder         = self.settings.get_builder()
        self.file_name_entry = self.builder.get_object("fileNameEntry")
        self.SCREENSHOTS_DIR = self.settings.get_screenshots_dir()
        self.backup_name     = None


    def rename_file(self, widget, data=None):
        new_name      = self.file_name_entry.get_text().strip()
        old_file_path = f"{self.SCREENSHOTS_DIR}/{self.backup_name}"
        new_file_path = f"{self.SCREENSHOTS_DIR}/{new_name}"
        try:
            if os.path.isfile(old_file_path) and new_name:
                os.rename(old_file_path, new_file_path)
                self.backup_name = new_name
                self.utils.referesh_directory_list()
        except Exception as e:
            print(repr(e))

    def open_file(self, widget, data=None):
        file = f"{self.SCREENSHOTS_DIR}/{self.backup_name}"
        subprocess.Popen(['xdg-open', file], stdout=subprocess.PIPE)

    def delete_file(self, widget, data=None):
        try:
            file = f"{self.SCREENSHOTS_DIR}/{self.backup_name}"
            if os.path.isfile(file):
                os.remove(file)
                self.builder.get_object("mainMenu").popdown()
                self.utils.referesh_directory_list()
        except Exception as e:
            print(repr(e))


    def reset_name(self, widget, data=None):
        self.file_name_entry.set_text(self.backup_name)

    def set_backup_var(self, widget):
        self.backup_name = self.file_name_entry.get_text()
