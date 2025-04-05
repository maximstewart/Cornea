# Python imports

# Lib imports

# Application imports
from .draw_type_base import DrawTypeBase



class DrawCross(DrawTypeBase):
    def __init__(self):
        super(DrawCross, self).__init__()


    def draw(self, area, cr):
        if not area.mouse_x or not area.mouse_y: return

        cr.set_source_rgba(1.0, 1.0, 1.0, 1.0)
        cr.set_line_width(1.0)
        cr.set_line_cap(2)       # 0 = BUTT, 1 = ROUND, 2 = SQUARE
        cr.set_line_join(1)      # 0 = BEVEL, 1 = MITER, 2 = ROUND

        # Horizon
        cr.move_to(0, area.mouse_y)
        cr.line_to(area.get_allocated_width(), area.mouse_y)
        cr.stroke()

        # Vertical
        cr.move_to(area.mouse_x, 0)
        cr.line_to(area.mouse_x, area.get_allocated_height())
        cr.stroke()