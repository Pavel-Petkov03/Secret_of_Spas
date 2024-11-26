from collections import deque


class AnimationFrameDoneError(Exception):
    def __init__(self, message, next_animation_frame):
        super().__init__(message)
        self.next_animation_frame = next_animation_frame


class AnimationFrameRequester:
    def __init__(self, animation_frame, frames_count_for_animation_frame, frames_count_for_animation, is_repeated=True ,
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

    def run(self):
        if self.__counter >= self.__frames_count_for_animation_frame:
            self.__counter = 0
            if not self.is_repeated:
                raise AnimationFrameDoneError("Animation done", self.next_animation_request)
        self.__counter += 1
        self.__frame_counter += 1
        if self.__frame_counter >= self.__frames_count_for_animation:
            self.__change_frame_to_display()
            self.__frame_counter = 0
        return self.current_animation_frame

    def __reset(self):
        self.counter = 0

    @property
    def current_animation_frame(self):
        return self.__current_animation_frame

    @current_animation_frame.setter
    def current_animation_frame(self, value):
        self.__current_animation_frame = deque(value)
