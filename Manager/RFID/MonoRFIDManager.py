from .IRFIDManager import IRFIDManager
from mfrc522 import SimpleMFRC522
import RPi.GPIO as GPIO

class MonoRFIDManager(IRFIDManager):
    def __init__(self, umbrella_holder_list=None, num_try_to_get=2):
        """1つのRFIDモジュールだけを管理するマネージャー。

        Args:
            umbrella_holder_list (list of UmbrellaHolder, optional): 傘立てのホルダーのリスト. Defaults to None.
            num_try_to_get (int, optional): ID取得試行回数. Defaults to 2.
        """
        self.reader = SimpleMFRC522()
        self.num_try_to_get = num_try_to_get
    
    def get_all(self):
        """全てのRFIDタグのIDを取得する。

        Returns:
            str: RFIDタグのIDのリスト
        """
        rfid = self.get()
        return [rfid]
    
    def get(self, number_rfid_reader=None):
        """指定したRFIDリーダーが認識するタグのIDを取得する。

        Args:
            number_rfid_reader (int, optional): RFIDリーダーの番号. Defaults to None.

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