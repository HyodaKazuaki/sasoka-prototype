class UmbrellaHolder:
    def __init__(self, rfid_controller, servo_controller, is_holding=False):
        """傘立てのホルダー。

        Args:
            rfid_controller (int): RFIDモジュールのコントローラー
            servo_controller (int): サーボモータのコントローラー
        """
        self.__rfid_controller = rfid_controller
        self.__servo_controller = servo_controller

    @property
    def rfid_controller(self):
        """RFIDモジュールのコントローラー。

        Returns:
            RFIDController: RFIDモジュールのコントローラー
        """
        return self.__rfid_controller

    @property
    def servo_controller(self):
        """サーボモータのコントローラー。

        Returns:
            ServoController: サーボモータのコントローラー
        """
        return self.__servo_controller

    @property
    def rfid(self):
        return self.__rfid_controller.get()
