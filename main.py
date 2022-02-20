import pyautogui
import keyboard
import ctypes
from datetime import datetime

import screen_scraping
from bounding_box import BoundingBox
from state import State

AREAS = {
    "main": (850, 400),
    "cid": (88, 257),
    "next level": (917, 73),
    "previous level": (790, 73),
}

RUN_UPGRADES = True
ADVANCING_STAGES = True


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

def main(starting_level: int, starting_kills: int):
    state = State(starting_level, starting_kills)
    bbox = get_window_rect_from_name("Clicker Heroes")
    while not keyboard.is_pressed("q"):
        click_area("main", bbox)
        if RUN_UPGRADES:
            run_upgrades(bbox)

        current_health = screen_scraping.get_approx_hp_state(bbox)
        #print(f"health changed from {state.enemy_health:.0%} to {current_health:.0%}")
        if current_health > .90 and state.enemy_health < .01:
            # assume monster killed
            # there is a chance that we can come SO close to killing a boss when it resets
            #   that the health bar looks just like we killed it
            #   this causes us to try to level up when we can't and desyncs the state from the actual game
            #   i don't know how to solve this yet.
            state.killed_monster()

        elif current_health > .90 and current_health > state.enemy_health and state.is_fighting_boss:
            # current > previous means it gained health
            # assume boss timeout
            state.boss_timed_out()

        state.enemy_health = current_health
        if state.due_to_advance:
            click_area("next level", bbox)
            state.advanced_level()
        if state.due_to_retreat:
            click_area("previous level", bbox)
            state.retreated_level()
        if state.is_delayed_advancement:
            state.delay_looped()



if __name__ == "__main__":
    starting_level = 64
    starting_kills = 7
    main(starting_level, starting_kills)
