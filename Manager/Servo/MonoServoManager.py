import RPi.GPIO as GPIO

from .IServoManager import IServoManager


class MonoServoManager(IServoManager):
    def __init__(self, umbrella_holder_list=None):
        """1つのサーボモーターだけを管理するマネージャー。

        Args:
            umbrella_holder_list (list of UmbrellaHolder, optional): 傘立てのホルダーのリスト. Defaults to None.
        """
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(4, GPIO.OUT)
        self.p = GPIO.PWM(4, 50)
        self.p.start(2.5)

    def lock(self):
        """サーボモーターを施錠状態にする。"""
        self.p.ChangeDutyCycle(12.0)

    def unlock_all(self):
        """全てのサーボモーターを解錠状態にする。"""
        self.unlock()
        return True

    def unlock(self, servo_id=4):
        self.p.ChangeDutyCycle(2.5)
        return True

    def __del__(self):
        GPIO.cleanup()
