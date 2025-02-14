import unittest
from unittest import mock
from unittest.mock import Mock, patch

from snitches.base_mission import MissionState, ActionMission, InfoMessage


class TestActionMission(unittest.TestCase):
    def setUp(self):
        self.snitch = Mock(name="Vili")
        self.snitch.name = "Vili"
        self.mission = ActionMission(self.snitch, ingredient_name="Potatoes(for gin)", ingredient_quantity=5)
        self.mock_inventory_has_needed_quantity = Mock()
        self.mock_inventory__doesnt_have_needed_quantity = Mock()
        self.mock_inventory_has_needed_quantity.items = {"Potatoes(for gin)": 5}
        self.mock_inventory__doesnt_have_needed_quantity.items = {"Potatoes(for gin)": 4}

    @patch("pygame_menu.Menu")
    def test_get_modal_not_taken(self, mock_menu):
        self.mission.state = MissionState.NOT_TAKEN
        menu = self.mission.get_modal(snitch_name="Vili", dungeon_state=Mock(),
                                      inventory=self.mock_inventory_has_needed_quantity)
        menu.add.button.assert_any_call("Accept", mock.ANY)

    @patch("pygame_menu.Menu")
    def test_get_modal_in_progress(self, mock_menu):
        self.mission.state = MissionState.IN_PROGRESS
        menu = self.mission.get_modal(snitch_name="Vili", dungeon_state=Mock(),
                                      inventory=self.mock_inventory__doesnt_have_needed_quantity)
        menu.add.button.assert_any_call("Continue", mock.ANY)

    @patch("pygame_menu.Menu")
    def test_get_modal_done(self, mock_menu):
        self.mission.state = MissionState.IN_PROGRESS
        menu = self.mission.get_modal(snitch_name="Vili", dungeon_state=Mock(),
                                      inventory=self.mock_inventory_has_needed_quantity)
        menu.add.button.assert_any_call("Done", mock.ANY)

    def test_accept_mission(self):
        mock_dungeon_state = Mock()
        self.mission.accept_mission(mock_dungeon_state)
        self.assertEqual(self.mission.state, MissionState.IN_PROGRESS)

    def test_mission_done(self):
        mock_dungeon_state = Mock()
        self.mission.mission_done(mock_dungeon_state, self.mock_inventory_has_needed_quantity)
        self.assertTrue(self.mission.state == MissionState.NOT_TAKEN)
        self.mock_inventory_has_needed_quantity.remove_items_from_mission.assert_called_once_with(self.mission)
        self.snitch.change_mission.assert_called_once()


class TestInfoMessage(unittest.TestCase):
    def setUp(self):
        self.snitch = Mock(name="Vili")
        self.snitch.name = "Vili"
        self.text = "This is a long message that should be split into several rows"
        self.info_message = InfoMessage(self.snitch, self.text)
        self.mock_dungeon_state = Mock()

    @patch("pygame_menu.Menu")
    def test_get_modal(self, mock_menu):
        menu = self.info_message.get_modal(snitch_name="Vili", dungeon_state=self.mock_dungeon_state, inventory=Mock())
        menu.add.button.assert_any_call("Continue", mock.ANY)
        grouped_text = self.info_message.group_words()
        for text_row in grouped_text:
            menu.add.label.assert_any_call(text_row, font_size=self.info_message.LABEL_FONT_SIZE)

    def test_group_words(self):
        grouped_text = self.info_message.group_words()
        expected_grouped_text = ['This is a long', 'message that should be', 'split into several rows']
        self.assertEqual(grouped_text, expected_grouped_text)

    def test_continue_mission(self):
        self.info_message.continue_mission(self.mock_dungeon_state)
        self.snitch.change_mission.assert_called_once()
        self.assertIsNone(self.mock_dungeon_state.popup_menu)


if __name__ == "__main__":
    unittest.main()
