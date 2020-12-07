# from multiprocessing import Process, Pipe
import RPi.GPIO as GPIO

from .Controller import CardScanner, RFIDController, ServoController
from .Database import DummyManager as DatabaseManager
from .Manager import MonoRFIDManager, MonoServoManager, UmbrellaManager
from .UmbrellaHolder import UmbrellaHolder


def rental(card_scanner, db_manager, umbrella_manager):
    """貸し出し処理"""
    tag = card_scanner.scan()
    if tag is None:
        # カードなし
        return
    idm = tag.idm
    # カードの情報をデータベースに問い合わせ
    if db_manager.is_rental(idm):
        # 貸し出し中なので貸し出さない
        # TODO すでに貸し出し中であることを示す
        return

    # 決済を行う
    if not card_scanner.transact(idm):
        # 決済失敗
        # TODO 何か警告などを表示する
        return

    # 傘を貸す
    umbrella_id = umbrella_manager.rent_one()

    # データベースにIDmと貸した傘の情報を記録する
    if not db_manager.regist(idm, umbrella_id):
        # 登録失敗
        # TODO 何か警告などを表示する
        return
    # 貸し出し処理終了


def coming_back(card_scanner, db_manager, umbrella_manager):
    """返却処理"""
    pass


if __name__ == "__main__":
    # 初期化処理
    card_scanner = CardScanner()
    db_manager = DatabaseManager()

    rfid_controller = RFIDController(None, 2)
    is_holding = True if rfid_controller.get() is not None else False
    servo_controller = ServoController(4, locked=is_holding)
    umbrella_holder = UmbrellaHolder(rfid_controller, servo_controller)
    umbrella_holder_list = [umbrella_holder]

    rfid_manager = MonoRFIDManager(umbrella_holder_list=umbrella_holder_list)
    servo_manager = MonoServoManager(umbrella_holder_list=umbrella_holder_list)
    umbrella_manager = UmbrellaManager(
        umbrella_holder_list=umbrella_holder_list,
    )

    while True:
        # 貸し出し
        rental(card_scanner, db_manager, umbrella_manager)
        # 返却
        coming_back(card_scanner, db_manager, umbrella_manager)
