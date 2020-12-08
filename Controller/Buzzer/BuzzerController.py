import time

import pigpio

from .IBuzzerController import IBuzzerController


class BuzzerController(IBuzzerController):
    def __init__(self, bcm_pin):
        """ブザーのコントローラー。

        Args:
            bcm_pin (int): PWMで再生するブザーのGPIOピン番号
        """
        self.pin = bcm_pin
        self.pi = pigpio.pi()
        self.pi.set_mode(self.pin, pigpio.OUTPUT)

    def sound(self, frequency=440, sound_time=0.5):
        """音を鳴らす。

        Args:
            frequency (int, optional): 音の周波数. Defaults to 440.
            sound_time (float, optional): 音を再生する時間. Defaults to 0.5.
        """
        self.pi.hardware_PWM(self.pin, frequency, 500000)
        time.sleep(sound_time)
        self.pi.hardware_PWM(self.pin, frequency, 0)

    def inpulse(self, frequency=2960, sound_time=0.1):
        """インパルスを再生する。

        Args:
            frequency (int, optional): 音の周波数. Defaults to 2960.
            sound_time (float, optional): 音を再生する時間. Defaults to 0.1.
        """
        self.sound(frequency, sound_time)

    def bell(
        self,
        frequency_1=725,
        frequency_2=576,
        sound_time_1=0.3,
        sound_time_2=0.7,
    ):
        """2音のベルを鳴らす。

        Args:
            frequency_1 (int, optional): 1音目の周波数. Defaults to 725.
            frequency_2 (int, optional): 2音目の周波数. Defaults to 576.
            sound_time_1 (float, optional): 1音目を再生する時間. Defaults to 0.3.
            sound_time_2 (float, optional): 2音目を再生する時間. Defaults to 0.7.
        """
        self.sound(frequency_1, sound_time_1)
        self.sound(frequency_2, sound_time_2)

    def alert(self, frequency=2960, sound_time=0.1, interval_time=0.02, num_repeat=10):
        """アラートを鳴らす。

        Args:
            frequency (int, optional): 音の周波数. Defaults to 2960.
            sound_time (float, optional): 音を再生する時間. Defaults to 0.1.
            interval_time (float, optional): 次の音を再生するまでの時間. Defaults to 0.02.
            num_repeat (int, optional): 繰り返し回数. Defaults to 10.
        """
        for _ in range(num_repeat):
            self.inpulse(frequency, sound_time)
            time.sleep(interval_time)

    def __del__(self):
        self.pi.stop()
