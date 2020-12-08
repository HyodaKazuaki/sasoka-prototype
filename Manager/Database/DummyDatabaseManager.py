from .IDatabaseManager import IDatabaseManager


class DummyDatabaseManager(IDatabaseManager):
    """ダミーデータベースマネージャー

    データベースとの通信を偽装する。いずれの場合も成功が返ってくる。
    """

    def __init__(self, host, port, user_name, user_password, db_name):
        """初期化処理

        Args:
            host (str): データベースのホスト名
            port (int): データベースのポート番号
            user_name (str): データベースに接続するユーザー名
            user_password (str): データベースに接続するユーザーのパスワード
            db_name (str): データベース名
        """
        pass

    def is_rental_idm(self, idm):
        """貸し出し中のICカードか判定する。

        Args:
            idm (str): 判定するIDm

        Returns:
            bool: 貸し出し中か否か
        """
        return False

    def is_rental_umbrella_id(self, umbrella_id):
        """貸し出し中の傘のIDか判定する。

        Args:
            umbrella_id (str): 傘のID

        Returns:
            bool: 貸し出し中か否か
        """
        return True

    def is_rental_umbrella_with_idm(self, umbrella_id, idm):
        """貸し出した傘と貸出先のカードの情報が一致しているか判定する。

        Args:
            umbrella_id (str): 傘のID
            idm (str): カードのIDm

        Returns:
            bool: 一致しているか否か
        """
        return True

    def record_rental(self, idm, umbrella_id):
        """傘が借りられたことをカードの情報と傘のIDで記録する。

        Args:
            idm (str): 記録するカードのIDm
            umbrella_id (str): 記録する傘のID

        Returns:
            bool: 記録に成功したか否か
        """
        return True

    def record_return(self, idm, umbrella_id):
        """傘が返却されたことをカードの情報と傘のIDで記録する。

        Args:
            idm (str): 記録するカードのIDm
            umbrella_id (str): 記録する傘のID

        Returns:
            bool: 記録に成功したか否か
        """
        return True

    def __del__(self):
        pass
