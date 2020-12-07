# from multiprocessing import Process, Pipe

from Controller import CardScanner, RFIDController, ServoController
from Database import DummyManager as DatabaseManager
from Manager import UmbrellaManager
from UmbrellaHolder import UmbrellaHolder


def rental(card_scanner, db_manager, umbrella_manager):
    """貸し出し処理"""
    tag = card_scanner.scan()
    if tag is None:
        # カードなし
        return
    print("Rental process start")
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

    print("Umbrella taken")

    # データベースにIDmと貸した傘の情報を記録する
    if not db_manager.regist(idm, umbrella_id):
        # 登録失敗
        # TODO 何か警告などを表示する
        return
    # 貸し出し処理終了
    print("Rental process finished.")


def coming_back(card_scanner, db_manager, umbrella_manager):
    """返却処理"""
    pass


if __name__ == "__main__":
    # 初期化処理
    card_scanner = CardScanner()
    db_manager = DatabaseManager(None, None, None, None, None)

    rfid_controller = RFIDController(None, 2)
    is_holding = True if rfid_controller.get() is not None else False
    print(is_holding)
    servo_controller = ServoController(7, locked=is_holding)
    umbrella_holder = UmbrellaHolder(rfid_controller, servo_controller)
    umbrella_holder_list = [umbrella_holder]

    umbrella_manager = UmbrellaManager(
        umbrella_holder_list=umbrella_holder_list,
    )

    print("Loop start.")
    while True:
        # 貸し出し
        rental(card_scanner, db_manager, umbrella_manager)
        # 返却
        coming_back(card_scanner, db_manager, umbrella_manager)
