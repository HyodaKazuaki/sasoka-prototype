from .IManager import IManager

class DummyManager(IManager):
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

    def is_lending(self, idm):
        """貸し出し中か判定する

        Args:
            idm (str): 判定するIDm

        Returns:
            bool: 貸し出し中か否か
        """
        return True
    
    def regist(self, idm, umbrella_id):
        """IDmと傘のIDを登録する

        Args:
            idm (str): 登録するIDm
            umbrella_id (str): 登録する傘のID

        Returns:
            bool: 登録に成功したか否か
        """
        return True
    
    def __del__(self):
        pass