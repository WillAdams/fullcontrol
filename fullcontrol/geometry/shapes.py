
from fullcontrol.geometry import Point, arcXY, variable_arcXY
from math import tau


def rectangleXY(start_point: Point, x_size: float, y_size: float, cw: bool = False) -> list:
    '''generate 2d-xy rectangle, starting from a Point, of specified size, defaulting to counter-clockwise. returned 
    list will have five Point since it begins and ends with the same Point
    '''
    point1 = Point(x=start_point.x+x_size*(not cw), y=start_point.y + y_size*cw, z=start_point.z)  # boolean False=0
    point2 = Point(x=start_point.x+x_size, y=start_point.y+y_size, z=start_point.z)
    point3 = Point(x=start_point.x+x_size*cw, y=start_point.y+y_size*(not cw), z=start_point.z)
    return [start_point.copy(), point1, point2, point3, start_point.copy()]


def circleXY(centre: Point, radius: float, start_angle: float, segments: int = 100, cw: bool = False) -> list:
    ''''generate 2d-xy circle with the specified number of segments (defaulting to 100), centred about a Point,
    with the given radius, starting at the specified polar angle (radians), with z-position the same as that
    of the centre Point. return list of Points
    '''
    return arcXY(centre, radius, start_angle, tau*(1-(2*cw)), segments)


def polygonXY(centre: Point, enclosing_radius: float, start_angle: float, sides: int, cw: bool = False) -> list:
    '''generate 2d-xy polygon with the specified number of sides, centred about a Point, sized based on the enclosing radius,
    starting at the specified polar angle (radians), defaulting to counter-clockwise. returned list will have one more Point than
    the number of sides since it begins and ends with the same Point
    '''
    return arcXY(centre, enclosing_radius, start_angle, tau*(1-(2*cw)), sides)  # cw parameter used to achieve +1 or -1


def spiralXY(centre: Point, start_radius: float, end_radius: float, start_angle: float, n_turns: float, segments: int, cw: bool = False) -> list:
    '''generate 2d-xy spiral with the specified number of segments and turns (partial turns permitted), centred about a Point, sized based on the start and end radius,
    starting at the specified polar angle (radians), defaulting to counter-clockwise. returned list will begin with the Point at the start of the first segment 
    and end at the Point at the end of the final segment
    '''
    return variable_arcXY(centre, start_radius, start_angle, arc_angle=n_turns*tau*(1-(2*cw)), segments=segments, radius_change=end_radius-start_radius, z_change=0)


def helixZ(centre: Point, start_radius: float, end_radius: float, start_angle: float, n_turns: float, pitch_z: float, segments: int, cw: bool = False) -> list:
    '''generate a helix in the Z direction with the specified number of segments and turns (partial turns permitted), centred about the Point centre, sized based on the start and end radius,
    starting at the specified polar angle (radians), defaulting to counter-clockwise. returned list will begin with the Point at the start of the first segment 
    and end at the Point at the end of the final segment
    '''
    return variable_arcXY(centre, start_radius, start_angle, arc_angle=n_turns*tau*(1-(2*cw)), segments=segments, radius_change=end_radius-start_radius, z_change=pitch_z*n_turns)
