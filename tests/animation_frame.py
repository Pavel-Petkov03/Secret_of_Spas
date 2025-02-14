import unittest
from unittest.mock import Mock

from player.display_mixins.animation_frame_requester import AnimationFrameRequester, AnimationFrameDoneError


class TestAnimationFrameRequester(AnimationFrameRequester):
    def cleanup_func_after_animation(self, screen, additional_data):
        pass


class TestAnimationFrameRequesterClass(unittest.TestCase):
    def setUp(self):
        self.frames = ["frame1", "frame2", "frame3"]
        self.requester = TestAnimationFrameRequester(
            animation_frame=self.frames,
            frames_count_for_animation_frame=2,
            frames_count_for_animation=3,
            is_repeated=False
        )

    def test_initial_frame(self):
        self.assertEqual(self.requester.current_animation, "frame1")

    def test_change_frame_to_display(self):
        self.requester._change_frame_to_display()
        self.assertEqual(self.requester.current_animation, "frame2")
        self.requester._change_frame_to_display()
        self.assertEqual(self.requester.current_animation, "frame3")
        self.requester._change_frame_to_display()
        self.assertEqual(self.requester.current_animation, "frame1")

    def test_animation_progression__fails(self):
        screen_mock = Mock()
        additional_data = {}
        delta = 1

        with self.assertRaises(AnimationFrameDoneError) as error:
            for _ in range(6):
                self.requester.run(screen_mock, additional_data, delta)
        self.assertEqual(error.exception.next_animation_frame, None)

    def test_animation_progression__doesnt_fail(self):
        screen_mock = Mock()
        additional_data = {}
        delta = 1
        for _ in range(1):
            self.requester.run(screen_mock, additional_data, delta)


if __name__ == "__main__":
    unittest.main()
