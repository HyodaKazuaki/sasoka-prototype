# from multiprocessing import Process, Pipe
import RPi.GPIO as GPIO
from Database import DummyManager as DatabaseManager
from Controller import CardScanner, RFIDController, ServoController
from Manager import UmbrellaManager, MonoRFIDManager, MonoServoManager
from UmbrellaHolder import UmbrellaHolder

def lending(card_scanner, db_manager, umbrella_manager):
    """貸し出し処理
    """
    tag = card_scanner.scan()
    if tag is None:
        # カードなし
        return
    # カードの情報をデータベースに問い合わせ
    if(db_manager.is_lending(idm)):
        # 貸し出し中なので貸し出さない
        #TODO すでに貸し出し中であることを示す
        return
    
    # 決済を行う
    if(not card_scanner.transact(idm)):
        # 決済失敗
        #TODO 何か警告などを表示する
        return

    # 傘を貸す
    umbrella_id = umbrella_manager.lend_one()

    # データベースにIDmと貸した傘の情報を記録する
    if(not db_manager.regist(idm, umbrella_id)):
        # 登録失敗
        #TODO 何か警告などを表示する
        return

def coming_back(card_scanner, db_manager, umbrella_manager):
    """返却処理
    """
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
    umbrella_manager = UmbrellaManager(umbrella_holder_list=umbrella_holder_list, rfid_manager=rfid_manager, servo_manager=servo_manager)

    while True:
        # 貸し出し
        lending(card_scanner, db_manager, umbrella_manager)
        # 返却
        coming_back(card_scanner, db_manager, umbrella_manager)