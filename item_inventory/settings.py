import random

ITEM_DROP_FOR_MAPS = {
    "first_level": {
        "Grapes": (10, "src/images/food/fruit/grapes.png"),
        "Apples": (40, "src/images/food/fruit/apple.png"),
        "Cherries": (30, "src/images/food/fruit/cherries.png"),
        "Blueberries": (20, "src/images/food/fruit/blueberries.png")
    },
}


def get_random_drop_data(dungeon_name):
    current_data = ITEM_DROP_FOR_MAPS[dungeon_name]
    items = list(current_data.keys())
    weights = [tup[0] for tup in current_data.values()]
    item_drop_name = random.choices(items, weights=weights, k=1)[0]
    return item_drop_name, ITEM_DROP_FOR_MAPS[dungeon_name][item_drop_name][1]
