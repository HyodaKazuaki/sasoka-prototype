import time

import pigpio

from .IBuzzerController import IBuzzerController


class BuzzerController(IBuzzerController):
    def __init__(self, bcm_pin):
        self.pin = bcm_pin
        self.pi = pigpio.pi()
        self.pi.set_mode(self.pin, pigpio.OUTPUT)

    def sound(self, frequency=440, sound_time=0.5):
        self.pi.hardware_PWM(self.pin, frequency, 500000)
        time.sleep(sound_time)
        self.pi.hardware_PWM(self.pin, frequency, 0)

    def inpulse(self, frequency=2960, sound_time=0.1):
        self.sound(frequency, sound_time)

    def bell(
        self,
        frequency_1=725,
        frequency_2=576,
        sound_time_1=0.3,
        sound_time_2=0.7,
    ):
        self.sound(frequency_1, sound_time_1)
        self.sound(frequency_2, sound_time_2)

    def alert(self, frequency=2960, sound_time=0.1, interval_time=0.02, num_repeat=10):
        for _ in range(num_repeat):
            self.inpulse(frequency, sound_time)
            time.sleep(interval_time)

    def __del__(self):
        self.pi.stop()
