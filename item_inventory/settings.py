import random

ITEM_DROP_FOR_MAP = {
    "first_level": {
        "Grapes": (10, ""),
        "Sugar": (40, ""),
        "Yeast": (30, ""),
        "Water": (20, "")
    },
}


def get_random_drop(dungeon_name):
    current_data = ITEM_DROP_FOR_MAP[dungeon_name]
    items = list(current_data.keys())
    weights = [tup[0] for tup in current_data.values()]
    return random.choices(items, weights=weights, k=1)[0]