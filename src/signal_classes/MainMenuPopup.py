# Gtk imports

# Python imports
import os, subprocess

# Application imports


class MainMenuPopup:
    def __init__(self, settings, utilsClass):
        self.settings        = settings
        self.utilsClass      = utilsClass

        self.builder         = self.settings.returnBuilder()
        self.fileNameEntry   = self.builder.get_object("fileNameEntry")
        self.SCREENSHOTS_DIR = self.settings.returnScreenshotsDir()
        self.backupName      = None


    def renameFile(self, widget, data=None):
        newName     = self.fileNameEntry.get_text().strip()
        oldFilePath = self.SCREENSHOTS_DIR + '/' + self.backupName
        newFilePath = self.SCREENSHOTS_DIR + '/' + newName
        try:
            if os.path.isfile(oldFilePath) and newName:
                os.rename(oldFilePath, newFilePath)
                self.backupName = newName
                self.utilsClass.refereshDirectoryList()
        except Exception as e:
            print(str(e))

    def openFile(self, widget, data=None):
        filePath = self.SCREENSHOTS_DIR + '/' + self.backupName
        subprocess.Popen(['xdg-open', filePath], stdout=subprocess.PIPE)

    def deleteFile(self, widget, data=None):
        try:
            filePath = self.SCREENSHOTS_DIR + '/' + self.backupName
            if os.path.isfile(filePath):
                os.remove(filePath)
                self.builder.get_object("mainMenu").popdown()
                self.utilsClass.refereshDirectoryList()
        except Exception as e:
            print(str(e))


    def resetName(self, widget, data=None):
        self.fileNameEntry.set_text(self.backupName)

    def setBackupVar(self, widget):
        self.backupName = self.fileNameEntry.get_text()
