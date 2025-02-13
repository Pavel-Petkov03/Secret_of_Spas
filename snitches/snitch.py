from collections import deque


class Snitch:
    def __init__(self, name, next_snitch):
        self.name = name
        self.missions = deque()
        self.next_snitch = next_snitch

    def __eq__(self, other):
        return self.name == other.name

    def __hash__(self):
        return hash(self.name)

    def add_missions(self, missions):
        self.missions.extend(missions)

    def get_current_mission(self):
        return self.missions[0]

    def change_mission(self):
        self.missions.popleft()
