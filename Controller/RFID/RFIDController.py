from .IRFIDController import IRFIDController
from mfrc522 import SimpleMFRC522
import RPi.GPIO as GPIO

class RFIDController(IRFIDController):
    def __init__(self, pin, num_try_to_get=2):
        """RFIDモジュールのコントローラー。

        Args:
            pin (int): RFIDモジュールのピン番号
            num_try_to_get (int, optional): ID取得試行回数. Defaults to 2.
        """
        #TODO ピン番号を元に決定する
        self.reader = SimpleMFRC522()
        self.num_try_to_get = num_try_to_get

    def get(self):
        """RFIDリーダーが認識するタグのIDを取得する。

        Returns:
            str: RFIDタグのID
        """
        rfid = None
        for _ in range(self.num_try_to_get):
            rfid_in_loop = self.reader.read_id_no_block()
            if rfid_in_loop is not None:
                rfid = rfid_in_loop
        return rfid

    def __del__(self):
        GPIO.cleanup()