# Python imports

# Lib imports

# Application imports
from .draw_type_base import DrawTypeBase



class DrawGrabRegion(DrawTypeBase):
    def __init__(self):
        super(DrawGrabRegion, self).__init__()


    def draw(self, area, cr):
        cr.set_source_rgba(1.0, 1.0, 0.0, 1.0)
        cr.set_line_width(1.0)
        cr.set_line_cap(2)       # 0 = BUTT, 1 = ROUND, 2 = SQUARE
        cr.set_line_join(1)      # 0 = BEVEL, 1 = MITER, 2 = ROUND

        self._draw_start_cross(area, cr)
        self._draw_end_cross(area, cr)

    def _draw_start_cross(self, area, cr):
        # Horizon
        cr.move_to(0, area.region_start_y)
        cr.line_to(area.get_allocated_width(), area.region_start_y)
        cr.stroke()

        # Vertical
        cr.move_to(area.region_start_x, 0)
        cr.line_to(area.region_start_x, area.get_allocated_height())
        cr.stroke()

    def _draw_end_cross(self, area, cr):
        # Horizon
        cr.move_to(0, area.region_end_y)
        cr.line_to(area.get_allocated_width(), area.region_end_y)
        cr.stroke()

        # Vertical
        cr.move_to(area.region_end_x, 0)
        cr.line_to(area.region_end_x, area.get_allocated_height())
        cr.stroke()




