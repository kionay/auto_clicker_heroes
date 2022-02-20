
class State:
    def __init__(self, starting_level: int, starting_monsters_killed: 10):
        self.current_level = starting_level
        self.monsters_killed_this_level = starting_monsters_killed
        self.is_delayed_advancement = False
        self.loops_left_in_delay = 0
        self.enemy_health = 1
        self.due_to_advance = False
        self.due_to_retreat = False
    
    @property
    def is_fighting_boss(self):
        return self.current_level % 5 == 0
    
    def killed_monster(self) -> None:
        print("killed monster")
        self.monsters_killed_this_level += 1
        if self.is_fighting_boss:
            print("\tit was a boss, so advancing")
            self.due_to_advance = True
        elif self.monsters_killed_this_level >= 10 and not self.is_delayed_advancement:
            print("\tit was a monster and we will advance")
            self.due_to_advance = True
    
    def advanced_level(self) -> None:
        self.due_to_advance = False
        self.current_level += 1
        self.monsters_killed_this_level = 0
        # to compensate advancing level between an injured monster and a full health boss tripping boss timout detection
        self.enemy_health = 1
        print(f"advanced to level {self.current_level}")

    def retreated_level(self) -> None:
        self.due_to_retreat = False
        self.current_level -= 1
        self.monsters_killed_this_level = 10
        print(f"retreated to level {self.current_level}")

    def boss_timed_out(self) -> None:
        print("boss timed out, retreating")
        self.due_to_retreat = True
        self.is_delayed_advancement = True
        self.loops_left_in_delay = 500

    def delay_looped(self) -> None:
        if self.loops_left_in_delay > 0:
            self.loops_left_in_delay -= 1
        else:
            print("done delaying, can now advance")
            self.is_delayed_advancement = False
        
