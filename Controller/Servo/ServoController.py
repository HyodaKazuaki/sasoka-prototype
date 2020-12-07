import RPi.GPIO as GPIO

from .IServoController import IServoController


class ServoController(IServoController):
    def __init__(self, pin, unlock=2.5, lock=12.0, frequency=50, locked=False):
        """サーボモーターのコントローラー。

        Args:
            pin (int): サーボモーターの制御ピン番号
            unlock (float, optional): 解錠状態のPWM比. Defaults to 2.5.
            lock (float, optional): 施錠状態のPWM比. Defaults to 12.0.
            frequency (int, optional): PWM信号の周波数. Defaults to 50.
            locked (bool, optional): 初期状態で施錠状態か否か. Defaults to False.
        """
        self.lock_pwm = lock
        self.unlock_pwm = unlock
        # gpio_mode = GPIO.getmode() if GPIO.getmode() is not None else GPIO.BCM()
        if GPIO.getmode() is None:
            GPIO.setmode(GPIO.BCM)
        GPIO.setup(pin, GPIO.OUT)
        self.__servo = GPIO.PWM(pin, frequency)
        if locked:
            self.__servo.start(self.lock_pwm)
        else:
            self.__servo.start(self.unlock_pwm)

    def lock(self):
        """施錠する。"""
        self.__servo.ChangeDutyCycle(self.lock_pwm)

    def unlock(self):
        """解錠する。"""
        self.__servo.ChangeDutyCycle(self.unlock_pwm)

    def __del__(self):
        GPIO.cleanup()
