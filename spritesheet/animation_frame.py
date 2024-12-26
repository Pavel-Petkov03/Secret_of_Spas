import pygame


class AnimationFrame:
    def __init__(self, animations_array, frame_duration):
        self.animations_array = animations_array
        self.frame_duration = frame_duration  # Time per frame in seconds
        self.current_time = 0.0
        self.current_frame_index = 0

    def update(self, time_delta):
        self.current_time += time_delta
        if self.current_time >= self.frame_duration:
            self.current_frame_index = (self.current_frame_index + 1) % len(self.animations_array)
            self.current_time %= self.frame_duration

    @property
    def current_frame(self):
        return self.animations_array[self.current_frame_index]
