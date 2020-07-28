"""
A module providing commonly used geometry
"""
import array
from typing import Tuple

from arcade.gl import Context, BufferDescription
from arcade.gl.vertex_array import Geometry


def _get_active_context() -> Context:
    ctx = Context.active
    if not ctx:
        raise RuntimeError("No context is currently activated")
    return ctx


def quad_2d_fs() -> Geometry:
    """Creates a screen aligned quad using normalized device coordinates"""
    return quad_2d(size=(2.0, 2.0))


def quad_2d(size: Tuple[float, float] = (1.0, 1.0), pos: Tuple[float, float] = (0.0, 0.0)) -> Geometry:
    """
    Creates 2D quad Geometry using 2 triangle strip with texture coordinates.

    :param tuple size: width and height
    :param float pos: Center position x and y
    :rtype: A :py:class:`~arcade.gl.geometry.Geometry` instance.       
    """
    ctx = _get_active_context()
    width, height = size
    x_pos, y_pos = pos

    data = array.array('f', [
        x_pos - width / 2.0, y_pos + height / 2.0, 0.0, 1.0,
        x_pos - width / 2.0, y_pos - height / 2.0, 0.0, 0.0,
        x_pos + width / 2.0, y_pos + height / 2.0, 1.0, 1.0,
        x_pos + width / 2.0, y_pos - height / 2.0, 1.0, 0.0,
    ])

    return ctx.geometry([BufferDescription(
        ctx.buffer(data=data),
        '2f 2f',
        ['in_vert', 'in_uv'],
    )], mode=ctx.TRIANGLE_STRIP)


def screen_rectangle(bottom_left_x: float, bottom_left_y: float, width: float, height: float) -> Geometry:
    """
    Creates screen rectangle using 2 triangle strip with texture coordinates.
    
    :param float bottom_left_x: Bottom left x position
    :param float bottom_left_y: Bottom left y position
    :param float width: Width of the rectangle
    :param float height: Height of the rectangle   
    """
    ctx = _get_active_context()
    data = array.array('f', [
        bottom_left_x, bottom_left_y + height, 0.0, 1.0,
        bottom_left_x, bottom_left_y, 0.0, 0.0,
        bottom_left_x + width, bottom_left_y + height, 1.0, 1.0,
        bottom_left_x + width, bottom_left_y, 1.0, 0.0,
    ])
    return ctx.geometry([BufferDescription(
        ctx.buffer(data=data),
        '2f 2f',
        ['in_vert', 'in_uv'],
    )], mode=ctx.TRIANGLE_STRIP)
