import unittest
from unittest.mock import Mock, patch
from vehicle.car_display import Car
import settings


class TestCar(unittest.TestCase):
    @patch("vlc.MediaPlayer")
    def setUp(self, mock_media_player):
        self.mock_dungeon_data = Mock()
        self.mock_player = Mock()
        self.mock_dungeon_data.player = self.mock_player
        self.mock_media_player = mock_media_player.return_value

        self.vehicle = Car(dungeon_data=self.mock_dungeon_data, x=0, y=0, current_animation_frame=[],
                           animation_frames=[])

    def test_initial_position(self):
        self.assertEqual(self.vehicle.get_x_y_pos(), (self.vehicle.x, self.vehicle.y))

    def test_change_position(self):
        self.vehicle.change_pos(300, 400)
        self.assertEqual(self.vehicle.get_x_y_pos(), (300, 400))

    def test_is_player_in_car(self):
        self.vehicle.is_mount = True
        self.assertTrue(self.vehicle.is_player_in_car())

        self.vehicle.is_mount = False
        self.assertFalse(self.vehicle.is_player_in_car())

    def test_handle_player_in_car(self):
        self.vehicle.car_switch = True
        self.vehicle.handle_player_in_car()
        self.assertEqual(self.vehicle.get_x_y_pos(), (self.mock_player.x, self.mock_player.y))
        self.mock_media_player.play.assert_called_once()
        self.assertFalse(self.vehicle.car_switch)

    def test_handle_player_out_of_car(self):
        self.vehicle.car_switch = False
        self.mock_player.x = 500
        self.mock_player.y = 600
        self.vehicle.handle_player_out_of_car()
        expected_x = 500 + settings.SCREEN_WIDTH / 2 / settings.SCALE_FACTOR
        expected_y = 600 + settings.SCREEN_WIDTH / 2 / settings.SCALE_FACTOR
        self.assertEqual(self.vehicle.get_x_y_pos(), (expected_x, expected_y))
        self.mock_media_player.stop.assert_called_once()
        self.assertTrue(self.vehicle.car_switch)

    def test_change_stream(self):
        initial_stream = self.vehicle.radio_deque[0]
        self.vehicle.change_stream()
        self.assertNotEqual(self.vehicle.radio_deque[0], initial_stream)
        self.mock_media_player.stop.assert_called_once()
        self.mock_media_player.set_media.assert_called_once()
        self.mock_media_player.play.assert_called_once()


if __name__ == "__main__":
    unittest.main()
