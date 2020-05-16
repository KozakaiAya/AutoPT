from deluge_client import DelugeRPCClient
import base64
import collections

from bt_client.client_base import BTClientBase, ClientRet

torrent_status_key = ['torrent_id', 'is_finished'] # Ref: https://github.com/deluge-torrent/deluge/blob/d62987089e55d6afe7c85addbdcb6ab515db69ea/deluge/core/torrent.py#L646
TorrentStatus = collections.namedtuple('TorrentStatus', torrent_status_key)
SessionStatus = collections.namedtuple('SessionStatus', ['torrent_list']) 

class DelugeClient(BTClientBase):
    def __init__(self, rpc_address, rpc_port, username, password, config=None):
        if config is None:
            self.use_config = False
            self.rpc_address = rpc_address
            self.rpc_port = int(rpc_port)
            self.user = username
            self.password = password

            self.client = DelugeRPCClient(self.rpc_address, self.rpc_port, self.username, self.password, automatic_reconnect=True)
            self.connected = False
        else:
            self.use_config = True
            self.config = config


    def connect(self):
        self.client.connect()
        self.connected = self.client.connected

        if self.connected:
            ret = ClientRet(ret_type=0)
        else:
            ret = ClientRet(ret_type=-2)
        return ret

    def add_torrent(self, torrent_path, download_path=None):
        if not self.connected:
            ret = ClientRet(ret_type=-2)
            return ret

        options = {} # Ref: https://github.com/deluge-torrent/deluge/blob/1.3-stable/deluge/core/torrent.py
        options['add_paused'] = False
        if download_path is not None:
            options['download_location'] = download_path

        torrent_content = open(torrent_path, 'r').read()
        torrent_base64 = base64.b64encode(torrent_content)

        torrent_idx = self.client.core.add_torrent_file(filename=torrent_path, filedump=torrent_base64, options=options)

        if torrent_idx is not None:
            ret = ClientRet(ret_type=3, ret_value=torrent_idx)
        else:
            ret = ClientRet(ret_type=-3)

        return ret


    def list_torrent(self):
        if not self.connected:
            ret = ClientRet(ret_type=-2)
            return ret
        
        torrent_id_list = self.client.core.get_session_state()
        torrent_list = []
        for idx in torrent_id_list:
            torrent_status_raw = self.client.core.get_torrent_status(torrent_id=idx, keys=torrent_status_key)
            torrent_status = TorrentStatus(torrent_id=torrent_status_raw['torrent_id'], is_finished=torrent_status_raw['is_finished'])
            
            torrent_list.append(torrent_status)
        
        session_status = SessionStatus(torrent_list=torrent_list)

        ret = ClientRet(ret_type=4, ret_value=session_status)

        return ret

    def del_torrent(self, idx):
        if not self.connected:
            ret = ClientRet(ret_type=-2)
            return ret

        idx_byte = str(idx).encode()
        torrent_id_list = self.client.core.get_session_state()
        if idx_byte in torrent_id_list:
            self.client.core.remove_torrent(torrent_id=idx_byte, remove_data=True)
            tlist = self.client.core.get_session_state()
            if idx not in tlist:
                ret = ClientRet(ret_value=5)
                return ret
            else:
                ret = ClientRet(ret_value=-5)
                return ret
        else:
            ret = ClientRet(ret_value=-5)
            return ret
    
    
            
    