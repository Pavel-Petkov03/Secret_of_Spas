import unittest
from unittest.mock import Mock, patch
import pygame
import settings
from item_inventory.inventory import Inventory, Item

from utils.singeton_meta import SingletonMeta


class TestInventory(unittest.TestCase):
    def setUp(self):
        pygame.init()
        pygame.display.set_mode((settings.SCREEN_WIDTH, settings.SCREEN_WIDTH))
        self.inventory = Inventory()
        self.mock_item = Mock()
        self.mock_item.name = "Apple"

    def test_add_item(self):
        self.inventory.add_item(self.mock_item)
        self.assertEqual(self.inventory.items["Apple"], 1)

    def test_add_multiple_items(self):
        self.inventory.add_item(self.mock_item)
        self.inventory.add_item(self.mock_item)
        self.assertEqual(self.inventory.items["Apple"], 2)

    def test_remove_items_from_mission(self):
        self.inventory.add_item(self.mock_item)
        self.inventory.add_item(self.mock_item)
        mock_mission = Mock()
        mock_mission.ingredient_name = "Apple"
        mock_mission.ingredient_quantity = 1
        self.inventory.remove_items_from_mission(mock_mission)
        self.assertEqual(self.inventory.items["Apple"], 1)

    def tearDown(self) -> None:
        SingletonMeta.clear_state()


class TestItem(unittest.TestCase):
    @patch("pygame.image.load")
    @patch("pygame.transform.scale")
    def setUp(self, mock_scale, mock_load):
        pygame.init()
        pygame.display.set_mode((1, 1))

        mock_surface = Mock()
        mock_surface.get_width.return_value = 100
        mock_surface.get_height.return_value = 100

        mock_load.return_value = mock_surface
        mock_scale.return_value = mock_surface

        self.mock_player = Mock()
        self.mock_player.x = 100
        self.mock_player.y = 100
        self.item = Item(200, 200, "Apple", "image.png", self.mock_player)

    def test_get_map_position(self):
        settings.TILE_WIDTH = 32
        tile_x, tile_y = self.item.get_map_position(Mock())
        self.assertEqual(tile_x, 200 // 32)
        self.assertEqual(tile_y, 200 // 32)

    def test_get_distance_to_player(self):
        settings.TILE_WIDTH = 32
        self.mock_player.get_map_position.return_value = (3, 3)
        self.assertAlmostEqual(self.item.get_distance_to_player(Mock()), 4.24, places=2)

    def test_item_blit(self):
        mock_screen = Mock()
        self.item.blit(mock_screen)
        mock_screen.blit.assert_called()


if __name__ == "__main__":
    unittest.main()
