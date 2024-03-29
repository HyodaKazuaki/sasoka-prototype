import nfc
from nfc.clf import RemoteTarget

from .ICardScanner import ICardScanner


class CardScanner(ICardScanner):
    def __init__(self, device_name="usb", target_list=["212F", "424F"]):
        """使用するカードスキャナーデバイスを用意し接続ターゲットを決定する。

        Args:
            device_name (str, optional): 使用するカードスキャナーデバイスの名前. Defaults to "usb".
            target_list (list of str, optional): 認識を許容するカードの種類のリスト. Defaults to ["212F","424F"].
        """
        self.clf = nfc.ContactlessFrontend(device_name)
        self.target = [RemoteTarget(target) for target in target_list]

    def scan_no_block(self):
        """カードをスキャンする。カードがあれば返り値にカードのタグ情報が渡される。

        Returns:
            nfc.tag.tt3.Type3Tag : カードのタグ情報。カードがない場合はNone
        """
        target = self.clf.sense(*self.target)
        if target is not None:
            return nfc.tag.activate(self.clf, target)

    def scan_with_block(self):
        """カードをスキャンする。カードのデータが返ってくるまで待ち続ける。

        Returns:
            nfc.tag.tt3.Type3Tag : カードのタグ情報
        """
        tag = None
        while tag is None:
            tag = self.scan_no_block()
        return tag

    def pay_deposit(self, tag):
        """デポジットを払う。

        Args:
            tag (nfc.tag.tt3.Type3Tag): カードのタグ情報

        Raises:
            NotImplementedError: 実装していないため発生する例外

        Returns:
            bool: 処理に成功したか否か
        """
        return True
        raise NotImplementedError("transact is not implemented.")

    def return_deposit(self, tag):
        """デポジットを返金する。

        Args:
            tag (nfc.tag.tt3.Type3Tag): カードのタグ情報

        Raises:
            NotImplementedError: 実装していないため発生する例外

        Returns:
            bool: 処理に成功したか否か
        """
        return True
        raise NotImplementedError("transact is not implemented.")

    def __del__(self):
        self.clf.close()
