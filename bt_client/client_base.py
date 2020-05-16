import collections


class BTClientBase():
    def __init__(self, rpc_address, rpc_port, username, password, config=None):
        raise NotImplementedError

    def connect(self):
        raise NotImplementedError

    def add_torrent(self, torrent_path, download_path=None):
        raise NotImplementedError

    def list_torrents(self):
        raise NotImplementedError

    def get_torrent_status(self, idx):
        raise NotImplementedError

    def del_torrent(self, idx):
        raise NotImplementedError

    def disconnect(self):
        raise NotImplementedError


class ClientRet():
    def __init__(self, ret_type, ret_value=None):
        self.ret_type = ret_type  # Error: <0
        self.ret_value = ret_value

        self.ret_dict = {
            6: "Torrent Info",
            5: "Delete Torrent Successful",
            4: "Torrent List",
            3: "Torrent ID",
            2: "Client Connected",
            0: "All Green",
            -2: "Client Not Connected",
            -3: "Torrent Add Error",
            -4: "Torrent List Error", 
            -5: "Delete Torrent Error",
            -6: "Torrent Info Error"
        }

    def get_error_msg(self):
        if self.ret_type < 0:
            return self.ret_dict[self.ret_type]
        else:
            return "All Green"

    def successful(self):
        return self.ret_type >= 0


torrent_status_key = [
    'name', 'torrent_id', 'is_finished'
]  # Ref: https://github.com/deluge-torrent/deluge/blob/d62987089e55d6afe7c85addbdcb6ab515db69ea/deluge/core/torrent.py#L646
TorrentStatus = collections.namedtuple('TorrentStatus', torrent_status_key)