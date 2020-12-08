import copy

from .IUmbrellaManager import IUmbrellaManager


class UmbrellaManager(IUmbrellaManager):
    def __init__(self, umbrella_holder_list, buzzer_controller):
        """傘立てのホルダー管理クラス。

        Args:
            umbrella_holder_list (list of UmbrellaHolder): このハードウェアが管理する傘立てのホルダーのリスト
            buzzer_controller (IBuzzerController): ブザーコントローラー
        """
        # 起動時の貸し出し可能な傘を取得
        self.umbrella_holder_list = umbrella_holder_list
        self.buzzer_controller = buzzer_controller

    def lock_all(self):
        """全ての傘立てのホルダーを施錠する。"""
        for umbrella_holder in self.umbrella_holder_list:
            umbrella_holder.lock()

    def lock_least_umbrellas(self):
        """傘が入っている傘立てのホルダーを施錠する。"""
        for umbrella_holder in self.umbrella_holder_list:
            if umbrella_holder.rfid is not None:
                umbrella_holder.lock()

    def unlock_all(self):
        """全ての傘立てのホルダーを解錠する。"""
        for umbrella_holder in self.umbrella_holder_list:
            umbrella_holder.unlock()

    def update_all_umbrella_id(self):
        for umbrella_holder in self.umbrella_holder_list:
            umbrella_holder.update_rfid()

    def __create_umbrella_id_set(self, umbrella_holder_list):
        """傘立てのリストから、傘のRFIDタグのIDの集合を作る。

        Args:
            umbrella_holder_list (list of UmbrellaHolder): 傘立てのリスト

        Returns:
            set of str: 傘のRFIDタグのIDの集合
        """
        umbrella_id_list = [
            umbrella_holder.rfid for umbrella_holder in umbrella_holder_list
        ]
        umbrella_id_list = filter(
            lambda umbrella_id: umbrella_id is not None, umbrella_id_list
        )
        umbrella_id_set = set(umbrella_id_list)
        return umbrella_id_set

    def __check_umbrella_was_taken(self, umbrella_holder_list):
        """RFIDをチェックして傘が取られたか確認する。

        Args:
            umbrella_holder_list (list of UmbrellaHolder): 初期状態で傘が入っているUmbrellaHolderのリスト

        Returns:
            set of str: 取り出されたRFIDタグのIDの集合
        """
        umbrella_id_set = self.__create_umbrella_id_set(umbrella_holder_list)
        while True:
            # RFIDチェックして、差分を取る
            self.update_all_umbrella_id()
            now_umbrella_id_set = self.__create_umbrella_id_set(
                self.umbrella_holder_list
            )
            if len(umbrella_id_set) < len(now_umbrella_id_set):
                # 返却されたか増えた
                print("Error: unexpected id is added.")
                self.buzzer_controller.inpulse(sound_time=0.05)
                continue
            lend_umbrella_id_set = umbrella_id_set - now_umbrella_id_set
            if len(lend_umbrella_id_set) > 1:
                # 一度に傘が借りられすぎた
                print(
                    "Error: Number of umbrellas which are lent are too much at once a time."
                )
                self.buzzer_controller.inpulse(sound_time=0.05)
                continue
            # 借りるのと同時に返していないかチェック
            if len(now_umbrella_id_set - umbrella_id_set) > 0:
                # 借りるのと同時に別の傘が返された
                print("Error: The umbrella was returned as soon as it was borrowed.")
                print(now_umbrella_id_set)
                print(umbrella_id_set)
                self.buzzer_controller.inpulse(sound_time=0.05)
                continue
            if lend_umbrella_id_set != set():
                # 1つだけ取り出された
                return lend_umbrella_id_set

    def rent_one(self):
        """傘を貸し出す。

        Returns:
            str: 貸し出された傘のID
        """
        # 現在のRFIDの状態を更新
        self.update_all_umbrella_id()
        # 現在の状態のコピーを取る
        now_umbrella_holder_list = copy.copy(self.umbrella_holder_list)
        print("Umbrella holder copied")

        # ロックを解除
        self.unlock_all()
        # どの傘を持っていくか判定する
        lent_umbrella_id_set = self.__check_umbrella_was_taken(now_umbrella_holder_list)
        # 貸してない場所だけ再びロックをする
        self.lock_least_umbrellas()
        return lent_umbrella_id_set.pop()

    def check_umbrella_was_returned(self):
        """RFIDタグが挿入されたか判定する。

        Returns:
            UmbrellaHolder: RFIDタグが挿入された傘立て
        """
        # 初期状態の傘立てのリストから、傘が入っているもののリストを作る
        umbrella_id_set = self.__create_umbrella_id_set(self.umbrella_holder_list)
        self.update_all_umbrella_id()
        returned_umbrella_id_set = set()
        while True:
            now_umbrella_id_set = self.__create_umbrella_id_set(
                self.umbrella_holder_list
            )
            returned_umbrella_id_set = now_umbrella_id_set - umbrella_id_set
            if len(returned_umbrella_id_set) > 1:
                # 一度に複数のRFIDタグが挿入された
                print(
                    "Error: Number of umbrellas which are returned are too much at once a time."
                )
                self.buzzer_controller.inpulse(sound_time=0.05)
                continue
            break
        if len(returned_umbrella_id_set) == 0:
            # 集合の長さが0 = 何も挿入していない場合はNoneを返す
            return None
        returned_umbrella_id = returned_umbrella_id_set.pop()
        # 該当の傘立てをフィルターで割り出す
        returned_umbrella_holder = filter(
            lambda umbrella_holder: umbrella_holder.rfid == returned_umbrella_id,
            self.umbrella_holder_list,
        )
        # filterオブジェクトのままでは扱いづらいため、listに変換する
        returned_umbrella_holder_list = list(returned_umbrella_holder)
        # listから先頭の傘立てを取り出す
        returned_umbrella_holder = returned_umbrella_holder_list[0]
        # 施錠する
        returned_umbrella_holder.lock()
        return returned_umbrella_holder

    def unlock_umbrella_for_failsafe(self, umbrella_holder):
        """なんらかのシステム障害により傘の返却処理が失敗した場合に、一旦傘をユーザーに返す。

        Args:
            umbrella_holder (UmbrellaHolder): 傘立て
        """
        # 傘をすでにロックしているので、ロックを解除して取り出されるまで待つ
        umbrella_holder.unlock()
        while umbrella_holder.rfid is not None:
            self.buzzer_controller.alert(sound_time=0.08, interval_time=0.08)
            # TODO 何か警告などを表示する
            umbrella_holder.update_rfid()
