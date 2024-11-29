from base_menu import BaseMenu

class AcceptMissionMenu(BaseMenu):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._menu.add.image("some path", )
