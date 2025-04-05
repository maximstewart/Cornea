# Python imports

# Lib imports

# Application imports



class OverrideExceptionw(Exception):
    ...


class DrawTypeBase:
    def draw(self, widget, cr):
        raise OverrideException("Method hasn't been overriden...")