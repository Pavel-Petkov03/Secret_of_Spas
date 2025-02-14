import random

ITEM_DROP_FOR_MAPS = {
    "first_level": {
        "Grapes(for rakiq)": (40, "src/images/food/fruit/grapes.png"),
        "Apples(for rakiq)": (40, "src/images/food/fruit/apple.png"),
        "Cherries(for rakiq)": (30, "src/images/food/fruit/cherries.png"),
        "Blueberries(for rakiq)": (20, "src/images/food/fruit/blueberries.png")
    },
    "second_level": {
        "Grapes(for wine)": (40, "src/images/food/fruit/grapes.png"),
        "Bananas(for wine)": (20, "src/images/food/fruit/banana.png"),
        "Pears(for wine)": (30, "src/images/food/fruit/pear.png"),
        "Potatoes(for wine)": (10, "src/images/food/vegetable/potato.png"),
    },
    "third_level": {
        "Pineapples(for gin)": (40, "src/images/food/fruit/pineapple_01.png"),
        "Cucumbers(for gin)": (30, "src/images/food/vegetable/cucumber.png"),
        "Lemons(for gin)": (10, "src/images/food/fruit/lemon.png"),
        "Carrots(for gin)": (20, "src/images/food/vegetable/carrot.png")
    },
    "fourth_level": {
        "Potatoes(for vodka)": (40, "src/images/food/vegetable/potato.png"),
        "Bananas(for vodka)": (30, "src/images/food/fruit/banana.png"),
        "Plums(for vodka)": (20, "src/images/food/fruit/plum.png"),
        "Pears(for vodka)": (10, "src/images/food/fruit/pear.png"),
    },
}


def get_random_drop_data(dungeon_name):
    current_data = ITEM_DROP_FOR_MAPS[dungeon_name]
    items = list(current_data.keys())
    weights = [tup[0] for tup in current_data.values()]
    item_drop_name = random.choices(items, weights=weights, k=1)[0]
    return item_drop_name, ITEM_DROP_FOR_MAPS[dungeon_name][item_drop_name][1]
