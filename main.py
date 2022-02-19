import pyautogui
import keyboard
import ctypes

import screen_scraping
from bounding_box import BoundingBox

AREAS = {
    "main": (850, 400),
    "cid": (88, 257),
    "next level": (917, 73),
    "previous level": (790, 73),
}

RUN_UPGRADES = False
ADVANCING_STAGES = False


def get_window_rect_from_name(name: str) -> BoundingBox:
    hwnd = ctypes.windll.user32.FindWindowW(0, name)
    rect = ctypes.wintypes.RECT()
    ctypes.windll.user32.GetWindowRect(hwnd, ctypes.pointer(rect))
    return BoundingBox(rect.left, rect.top, rect.right, rect.bottom)


def click_area(area_name: str, bbox: BoundingBox) -> None:
    x_offset = bbox.x
    y_offset = bbox.y
    area_x = AREAS[area_name][0]
    area_y = AREAS[area_name][1]
    click_x = x_offset + area_x
    click_y = y_offset + area_y
    pyautogui.click(click_x, click_y)


def run_upgrades(bbox: BoundingBox) -> None:
    for clickable_upgrade in screen_scraping.find_upgradable_heroes(bbox):
        pyautogui.click(clickable_upgrade[0], clickable_upgrade[1])
        click_area("main", bbox)


def main():
    bbox = get_window_rect_from_name("Clicker Heroes")
    counter = 1
    previous_health = 0
    while not keyboard.is_pressed("q"):
        if RUN_UPGRADES:
            run_upgrades(bbox)
        if ADVANCING_STAGES and counter % 20 == 0:
            click_area("next level", bbox)
        if counter % 2 == 0:
            current_health = screen_scraping.get_approx_hp_state(bbox)
            hp_delta = abs(current_health - previous_health)
            print(f"health @ {current_health:.0%}")
            if hp_delta > 0.7:
                print(f"monster killed")
            previous_health = current_health
        click_area("main", bbox)
        counter += 1


if __name__ == "__main__":
    main()
