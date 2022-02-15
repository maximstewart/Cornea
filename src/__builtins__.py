import builtins

# Python imports
import builtins

# Lib imports

# Application imports



class Builtins:
    """Docstring for __builtins__ extender"""

    def __init__(self):
        pass

# NOTE: Just reminding myself we can add to builtins two different ways...
# __builtins__.update({"event_system": Builtins()})
builtins.app_name          = "Cornea"
