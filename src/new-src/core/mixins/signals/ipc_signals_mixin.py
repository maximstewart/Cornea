# Python imports

# Lib imports

# Application imports




class IPCSignalsMixin:
    """ IPCSignalsMixin handle messages from another starting solarfm process. """

    def print_to_console(self, message=None):
        print(message)

    def handle_file_from_ipc(self, path: str) -> None:
        print(f"File From IPC: {path}")

    def handle_dir_from_ipc(self, path: str) -> None:
        print(f"Dir From IPC: {path}")
