from .IUmbrellaManager import IUmbrellaManager
from ..RFID import MonoRFIDManager as RFIDManager

class UmbrellaManager(IUmbrellaManager):
    def __init__(self, umbrella_holder_list, rfid_manager, servo_manager):
        self.rfid_manager = rfid_manager
        self.servo_manager = servo_manager
        # 起動時の貸し出し可能な傘を取得
        self.umbrella_holder_list = umbrella_holder_list
    
    def check_umbrella_change(self, umbrella_set):
        """RFIDをチェックして変化を見る。

        Args:
            umbrella_set (set of str): 初期状態でのRFIDタグのIDの集合

        Returns:
            set of str: 取り出されたRFIDタグのIDの集合
        """
        while True:
            # RFIDチェックして、差分を取る
            now_umbrella_set = self.rfid_manager.get_all()
            if len(umbrella_set) < len(now_umbrella_set):
                # 返却されたか増えた
                print("Error: unexpected id is added.")
                continue
            diff_umbrella_set = umbrella_set - now_umbrella_set
            if len(diff_umbrella_set) > 1:
                # 一度に傘が借りられすぎた
                print("Error: Number of umbrellas which are lent are too much at once a time.")
                continue
            if diff_umbrella_set != set():
                # 1つだけ取り出された
                return diff_umbrella_set

    def lend_one(self):
        """傘を貸し出す。

        Returns:
            str: 貸し出された傘のID
        """
        # 現在のRFIDの状態を確認
        umbrella_id_list = self.rfid_manager.get_all()
        # ロックを解除
        if not self.servo_manager.unlock_all():
            # ロックの解除に失敗
            #TODO 何かエラーを出す
            return
        # どの傘を持っていくか判定する
        lent_umbrella_set = self.check_umbrella_change(umbrella_set)
        least_umbrella_set = umbrella_set - lent_umbrella_set
        # 貸してない場所だけ再びロックをする
        self.servo_manager.lock(least_umbrella_set)
        return lent_umbrella_set.pop()
    
    def give_back(self):

        return True