from collections import deque

from snitches.base_mission import BaseMission


class Snitch:
    def __init__(self, name, next_snitch):
        self.name = name
        self.missions = deque()
        self.next_snitch = next_snitch

    def add_missions(self, missions: [BaseMission]):
        self.missions.extend(missions)

    def get_current_mission(self):
        return self.missions[0]

    def change_mission(self):
        self.missions.popleft()
