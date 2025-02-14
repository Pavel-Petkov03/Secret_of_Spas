import unittest
from unittest.mock import Mock
from events.base_event import EventManager


class TestEventManager(unittest.TestCase):
    def setUp(self):
        self.event_manager = EventManager()
        self.mock_event = Mock()
        self.mock_event.event_type = Mock(type=12)
        self.mock_event.run_event_listener = Mock()

    def test_register_event(self):
        self.event_manager.register_event(self.mock_event)
        self.assertIn(self.mock_event.event_type, self.event_manager.events)
        self.assertEqual(self.event_manager.events[self.mock_event.event_type], self.mock_event)


if __name__ == "__main__":
    unittest.main()
