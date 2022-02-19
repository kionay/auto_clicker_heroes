from typing import Tuple
import colorsys

from PIL import ImageGrab, Image

from bounding_box import BoundingBox

UPGRADABLE_HERO_COLOR = (153, 213, 255)
HEALTH_BAR_BACKGROUND_COLOR = (65, 63, 63)
TIME_UP_ORANGE = (255, 153, 51)
TIME_UP_BLACK = (51, 51, 51)


def _screen_grab(bbox: BoundingBox) -> Image:
    pil_bbox = bbox.to_pil_bbox()
    image = ImageGrab.grab(
        bbox=pil_bbox, include_layered_windows=True, all_screens=True
    )
    return image


def _rgb_to_hsv(r, g, b) -> Tuple[int, int, int]:
    r /= 255
    g /= 255
    b /= 255
    h, s, v = colorsys.rgb_to_hsv(r, g, b)
    h = int(h * 255)
    s = int(s * 255)
    v = int(v * 255)
    return h, s, v


def _is_close_to_color(rgb: Tuple, color: Tuple) -> bool:
    color_difference = sum(list(rgb)) - sum(list(color))
    if abs(color_difference) <= 2:
        return True
    else:
        return False


def find_upgradable_heroes(bbox: BoundingBox) -> Tuple:
    image = _screen_grab(bbox)
    for i in range(image.height - 1):
        pixel_color = image.getpixel((142, i))
        if _is_close_to_color(pixel_color, UPGRADABLE_HERO_COLOR):
            yield (142 + bbox.x, i + bbox.y)
            break


def get_approx_hp_state(bbox: BoundingBox) -> float:
    image = _screen_grab(bbox)
    health_bar_size = 136
    health_bar_start = 795
    health_bar_end = health_bar_start + health_bar_size
    grey_pixel_count = 0  # to 133
    for i in range(health_bar_start, health_bar_end + 1):
        this_pixel = image.getpixel((i, 582))
        if _is_close_to_color(this_pixel, HEALTH_BAR_BACKGROUND_COLOR):
            grey_pixel_count += 1
    if grey_pixel_count == 0:
        return 1
    else:
        return 1 - (grey_pixel_count / 133)


def find_is_timed_out(bbox: BoundingBox) -> bool:
    image = _screen_grab(bbox)
    has_orange = False
    has_black = False
    for i in range(image.height - 1):
        r, g, b = image.getpixel((785, i))
        if (r, g, b) == TIME_UP_ORANGE:
            has_orange = True
        if (r, g, b) == TIME_UP_BLACK:
            has_black = True
        if has_orange and has_black:
            return True
    return False
