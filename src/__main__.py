#!/usr/bin/python3


# Python imports
import argparse, faulthandler, traceback
from setproctitle import setproctitle

import tracemalloc
tracemalloc.start()

# Lib imports
import gi, faulthandler, signal
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

# Application imports
from app import Application


if __name__ == "__main__":
    try:
        setproctitle('Cornea')
        faulthandler.enable()  # For better debug info

        parser = argparse.ArgumentParser()
        # Add long and short arguments
        parser.add_argument("--file", "-f", default="firefox", help="JUST SOME FILE ARG.")
        # Read arguments (If any...)
        args, unknownargs = parser.parse_known_args()

        Application(args, unknownargs)
        Gtk.main()
    except Exception as e:
        traceback.print_exc()
        quit()
