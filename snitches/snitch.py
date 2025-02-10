class Snitch:
    def __init__(self, name, player):
        self.player = player
        self.current_mission_menu = None
        self.name = name

    def change_snitch_menu(self, new_menu):
        self.current_mission_menu = new_menu
