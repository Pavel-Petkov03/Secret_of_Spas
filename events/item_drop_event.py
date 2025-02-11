from events.base_event import Event
from events.event_types.dungeos import ITEM_DROP
from item_inventory.settings import get_random_drop_data
from item_inventory.inventory import Item


class ItemDropEvent(Event):
    event_type = ITEM_DROP

    def run_event_listener(self, game_state):
        drop_args = get_random_drop_data(self.dungeon_state.name)
        new_item = Item(*self.additional_state.values(),
                        *drop_args,
                        self.dungeon_state.player
                        )
        self.dungeon_state.items.append(new_item)
