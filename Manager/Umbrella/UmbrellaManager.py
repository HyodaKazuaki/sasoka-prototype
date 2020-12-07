import copy

from .IUmbrellaManager import IUmbrellaManager


class UmbrellaManager(IUmbrellaManager):
    def __init__(self, umbrella_holder_list):
        """傘立てのホルダー管理クラス。

        Args:
            umbrella_holder_list (list of UmbrellaHolder): このハードウェアが管理する傘立てのホルダーのリスト
        """
        # 起動時の貸し出し可能な傘を取得
        self.umbrella_holder_list = umbrella_holder_list

    def check_umbrella_change(self, umbrella_holder_list):
        """RFIDをチェックして変化を見る。

        Args:
            umbrella_holder_list (list of UmbrellaHolder): 初期状態で傘が入っているUmbrellaHolderのリスト

        Returns:
            set of str: 取り出されたRFIDタグのIDの集合
        """
        umbrella_id_list = [
            umbrella_holder.rfid for umbrella_holder in umbrella_holder_list
        ]
        umbrella_id_list = filter(
            lambda umbrella_id: umbrella_id is not None, umbrella_id_list
        )
        umbrella_id_set = set(umbrella_id_list)
        while True:
            # RFIDチェックして、差分を取る
            for umbrella_holder in self.umbrella_holder_list:
                umbrella_holder.update_rfid()
            now_umbrella_id_list = [
                umbrella_holder.rfid for umbrella_holder in self.umbrella_holder_list
            ]
            now_umbrella_id_list = filter(
                lambda now_umbrella_id: now_umbrella_id is not None,
                now_umbrella_id_list,
            )
            now_umbrella_id_set = set(now_umbrella_id_list)
            if len(umbrella_id_set) < len(now_umbrella_id_set):
                # 返却されたか増えた
                print("Error: unexpected id is added.")
                # TODO 警告音などを出す
                continue
            lend_umbrella_id_set = umbrella_id_set - now_umbrella_id_set
            if len(lend_umbrella_id_set) > 1:
                # 一度に傘が借りられすぎた
                print(
                    "Error: Number of umbrellas which are lent are too much at once a time."
                )
                # TODO 警告音などを出す
                continue
            # 借りるのと同時に返していないかチェック
            if len(now_umbrella_id_set - umbrella_id_set) > 0:
                # 借りるのと同時に別の傘が返された
                print("Error: The umbrella was returned as soon as it was borrowed.")
                print(now_umbrella_id_set)
                print(umbrella_id_set)
                # TODO 警告音などを出す
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
        for umbrella_holder in self.umbrella_holder_list:
            umbrella_holder.update_rfid()
        # 現在の状態のコピーを取る
        now_umbrella_holder_list = copy.copy(self.umbrella_holder_list)

        print("Umbrella holder copied")

        # ロックを解除
        for umbrella_holder in self.umbrella_holder_list:
            umbrella_holder.unlock()
        # どの傘を持っていくか判定する
        lent_umbrella_id_set = self.check_umbrella_change(now_umbrella_holder_list)
        # 貸してない場所だけ再びロックをする
        for umbrella_holder in self.umbrella_holder_list:
            if umbrella_holder.rfid is not None:
                umbrella_holder.lock()
        return lent_umbrella_id_set.pop()

    def give_back(self):

        return True
