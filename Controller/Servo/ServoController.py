import RPi.GPIO as GPIO

from .IServoController import IServoController


class ServoController(IServoController):
    def __init__(
        self, bcm_pin, board_pin, unlock_degree=0.0, lock_degree=143.0, min_dc=2.5, max_dc=12.0, frequency=50, locked=False
    ):
        """サーボモーターのコントローラー。

        Args:
            bcm_pin (int): サーボモーターの制御ピンのGPIOピン番号
            board_pin (int): サーボモーターの制御ピンのボード上ピン番号
            unlock_degree (float, optional): 解錠状態の角度. Defaults to 0.
            lock_degree (float, optional): 施錠状態の角度. Defaults to 143.0.
            min_dc (float, optional): サーボモーターの最小デューティー比. Defaults to 2.5.
            max_dc (float, optional): サーボモーターの最大デューティー比. Defaults to 12.0.
            frequency (int, optional): PWM信号の周波数. Defaults to 50.
            locked (bool, optional): 初期状態で施錠状態か否か. Defaults to False.
        """
        self.min_dc = min_dc
        self.max_dc = max_dc
        self.lock_dc = self.calc_duty_cycle_from_degree(lock)
        self.unlock_dc = self.calc_duty_cycle_from_degree(unlock)
        if GPIO.getmode() is None:
            GPIO.setmode(GPIO.BCM)
            pin = bcm_pin
        else:
            pin = board_pin
        GPIO.setup(pin, GPIO.OUT)
        self.__servo = GPIO.PWM(pin, frequency)
        if locked:
            self.__servo.start(self.lock_dc)
        else:
            self.__servo.start(self.unlock_dc)

    def calc_duty_cycle_from_degree(self, degree):
        """度数法の角度からデューティー比を計算する。

        Args:
            degree (float): 度数法の角度

        Returns:
            float: デューティー比
        """
        dc = 2.5 + (self.max_dc - self.min_dc) / 180.0 * degree
        return dc

    def lock(self):
        """施錠する。"""
        self.__servo.ChangeDutyCycle(self.lock_dc)

    def unlock(self):
        """解錠する。"""
        self.__servo.ChangeDutyCycle(self.unlock_dc)

    def __del__(self):
        GPIO.cleanup()
