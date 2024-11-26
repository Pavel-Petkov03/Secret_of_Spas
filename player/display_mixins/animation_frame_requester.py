from collections import deque
from abc import ABC, abstractmethod


class AnimationFrameDoneError(Exception):
    def __init__(self, message, next_animation_frame):
        super().__init__(message)
        self.next_animation_frame = next_animation_frame


class AnimationFrameRequester(ABC):
    def __init__(self, animation_frame, frames_count_for_animation_frame, frames_count_for_animation, is_repeated=True,
                 next_animation_request=None):
        self.__counter = 0
        self.__frame_counter = 0
        self.__frames_count_for_animation_frame = frames_count_for_animation_frame
        self.__frames_count_for_animation = frames_count_for_animation
        self.__current_animation_frame = deque(animation_frame)
        self.is_repeated = is_repeated
        self.next_animation_request = next_animation_request

    @property
    def current_animation(self):
        return self.__current_animation_frame[0]

    def __change_frame_to_display(self):
        self.__current_animation_frame.append(self.__current_animation_frame.popleft())

    def run(self, screen, additional_data):
        if self.__counter >= self.__frames_count_for_animation_frame:
            self.__counter = 0
            if not self.is_repeated:
                self.cleanup_func_after_animation(screen, additional_data)
                raise AnimationFrameDoneError("Animation done", self.next_animation_request)
        self.__counter += 1
        self.__frame_counter += 1
        if self.__frame_counter >= self.__frames_count_for_animation:
            self.__change_frame_to_display()
            self.__frame_counter = 0
        return self.current_animation_frame

    @property
    def current_animation_frame(self):
        return self.__current_animation_frame

    @current_animation_frame.setter
    def current_animation_frame(self, value):
        self.__current_animation_frame = deque(value)

    @abstractmethod
    def cleanup_func_after_animation(self, screen, additional_data):
        pass


class MoveAnimationFrameRequester(AnimationFrameRequester):
    def cleanup_func_after_animation(self, screen, additional_data):
        pass


class InfantryAttackAnimationFrameRequester(AnimationFrameRequester):
    def cleanup_func_after_animation(self, screen, additional_data):
        pass


class ArcherAttackAnimationFrameRequester(AnimationFrameRequester):
    def cleanup_func_after_animation(self, screen, additional_data):
        pass


class DieEnemyAnimationFrameRequester(AnimationFrameRequester):
    def cleanup_func_after_animation(self, screen, additional_data):
        pass
