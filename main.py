import time

from Controller import BuzzerController, CardScanner, RFIDController, ServoController
from Manager import DummyDatabaseManager as DatabaseManager
from Manager import UmbrellaManager
from UmbrellaHolder import UmbrellaHolder


def rental(
    card_scanner, db_manager, umbrella_manager, buzzer_controller, wait_seconds=3.0
):
    """貸し出し処理。

    Args:
        card_scanner (ICardScanner): カードスキャナー
        db_manager (IDatabaseManager): データベースマネージャー
        umbrella_manager (IUmbrellaManager): 傘マネージャー
        buzzer_controller (IBuzzerController): ブザーコントローラー
        wait_seconds (float, optional): 成功時の待機時間. Defaults to 3.0.
    """
    tag = card_scanner.scan_no_block()
    if tag is None:
        # カードなし
        return
    buzzer_controller.inpulse()
    print("Rental process start")

    if umbrella_manager.is_empty():
        # 傘が全て貸し出し中なので貸し出せない
        print("Error: All umbrella holder are empty.")
        buzzer_controller.bell()
        # TODO 傘立てが空っぽであることを示す
        return

    idm = tag.idm
    # カードの情報をデータベースに問い合わせ
    if db_manager.is_rental_idm(idm):
        # 貸し出し中なので貸し出さない
        print("Error: Already rent.")
        buzzer_controller.bell()
        # TODO すでに貸し出し中であることを示す
        return

    # 決済を行う
    if not card_scanner.pay_deposit(tag):
        # 決済失敗
        print("Error: Failed to pay deposit.")
        buzzer_controller.alert()
        # TODO 何か警告などを表示する
        return

    # 傘を貸す
    umbrella_id = umbrella_manager.rent_one()
    print("Umbrella taken")

    # データベースにIDmと貸した傘の情報を記録する
    if not db_manager.record_rental(idm, umbrella_id):
        # 登録失敗
        print("Error: Failed to record in database.")
        buzzer_controller.alert()
        # TODO 何か警告などを表示する
        return
    # 貸し出し処理終了
    buzzer_controller.inpulse()
    print("Rental process finished")
    print("Wait a few second...")
    time.sleep(wait_seconds)
    print("Restored.")
    for umbrella_holder in umbrella_manager.umbrella_holder_list:
        print(umbrella_holder.rfid)


def coming_back(
    card_scanner, db_manager, umbrella_manager, buzzer_controller, wait_seconds=3.0
):
    """返却処理。

    Args:
        card_scanner (ICardScanner): カードスキャナー
        db_manager (IDatabaseManager): データベースマネージャー
        umbrella_manager (IUmbrellaManager): 傘マネージャー
        buzzer_controller (IBuzzerController): ブザーコントローラー
        wait_seconds (float, optional): 成功時の待機時間. Defaults to 3.0.
    """
    returned_umbrella_holder = umbrella_manager.check_umbrella_was_returned()
    if returned_umbrella_holder is None:
        # 挿入されたRFIDなし
        return
    buzzer_controller.inpulse()
    # 挿入されたRFIDタグが正規のものか、貸し出し中の傘のものかデータベース問い合わせ
    if not db_manager.is_rental_umbrella_id(returned_umbrella_holder.rfid):
        print("Error: Illigal umbrella id found.")
        buzzer_controller.alert()
        # TODO 何か警告などを表示する
        return

    print("Return process start")
    # 傘をロックする
    returned_umbrella_holder.lock()
    tag = card_scanner.scan_with_block()
    idm = tag.idm
    buzzer_controller.inpulse()
    print("Card touched.")

    if not db_manager.is_rental_umbrella_with_idm(returned_umbrella_holder.rfid, idm):
        print("Error: Illigal umbrella and card pair.")
        # TODO 何か警告などを表示する
        # 傘をすでにロックしているので、ロックを解除して取り出されるまで待つ
        umbrella_manager.unlock_umbrella_for_failsafe(returned_umbrella_holder)
        return

    # 決済を行う
    if not card_scanner.return_deposit(tag):
        print("Error: Failed to return deposit.")
        # TODO 何か警告などを表示する
        # 傘をすでにロックしているので、ロックを解除して取り出されるまで待つ
        umbrella_manager.unlock_umbrella_for_failsafe(returned_umbrella_holder)
        return

    # データベースに返却処理を記録する
    if not db_manager.record_return(idm, returned_umbrella_holder.rfid):
        print("Error: Failed to record in database.")
        buzzer_controller.alert()
        # TODO 何か警告などを表示する
        # 傘をロックしているが、返金処理は成功しているのでそのまま終了する
        return

    buzzer_controller.inpulse()
    print("Return process finished")
    print("Wait a few second...")
    time.sleep(wait_seconds)
    print("Restored.")


if __name__ == "__main__":
    # 初期化処理
    buzzer = BuzzerController(18)
    card_scanner = CardScanner()
    db_manager = DatabaseManager(None, None, None, None, None)

    rfid_controller = RFIDController(None, 2)
    is_holding = True if rfid_controller.get() is not None else False
    print(is_holding)
    servo_controller = ServoController(4, 7, locked=is_holding)
    umbrella_holder = UmbrellaHolder(rfid_controller, servo_controller)
    umbrella_holder_list = [umbrella_holder]

    umbrella_manager = UmbrellaManager(
        umbrella_holder_list=umbrella_holder_list, buzzer_controller=buzzer
    )

    print("Loop start.")
    while True:
        # 貸し出し
        rental(card_scanner, db_manager, umbrella_manager, buzzer)
        # 返却
        coming_back(card_scanner, db_manager, umbrella_manager, buzzer)
