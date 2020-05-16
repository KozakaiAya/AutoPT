from deluge_client import DelugeRPCClient
import base64
import collections
from pathlib import Path

from bt_client.client_base import BTClientBase, ClientRet, TorrentStatus
import bt_client.client_base


def is_torrent_finished(session_status, torrent_idx):
    if torrent_idx in session_status:
        return session_status[torrent_idx].is_finished
    else:
        return False


class DelugeClient(BTClientBase):
    def __init__(self, rpc_address, rpc_port, username, password, config=None):
        if config is None:
            self.use_config = False
            self.rpc_address = rpc_address
            self.rpc_port = int(rpc_port)
            self.username = username
            self.password = password

            self.client = DelugeRPCClient(self.rpc_address,
                                          self.rpc_port,
                                          self.username,
                                          self.password,
                                          automatic_reconnect=True)
            self.connected = False
        else:
            self.use_config = True
            self.config = config

    def connect(self):
        self.client.connect()
        self.connected = self.client.connected

        if self.connected:
            ret = ClientRet(ret_type=2)
        else:
            ret = ClientRet(ret_type=-2)
        return ret

    def add_torrent(self, torrent_path, download_path=None):
        if not self.connected:
            ret = ClientRet(ret_type=-2)
            return ret

        options = {}  # Ref: https://github.com/deluge-torrent/deluge/blob/1.3-stable/deluge/core/torrent.py
        options['add_paused'] = False
        if download_path is not None:
            options['download_location'] = str(Path(download_path).resolve())

        abs_torrent_path = str(Path(torrent_path).resolve())
        torrent_content = open(abs_torrent_path, 'rb').read()
        torrent_base64 = base64.b64encode(torrent_content)

        torrent_idx = self.client.core.add_torrent_file(filename=abs_torrent_path,
                                                        filedump=torrent_base64,
                                                        options=options)

        if torrent_idx is not None:
            ret = ClientRet(ret_type=3, ret_value=torrent_idx.decode())
        else:
            ret = ClientRet(ret_type=-3)

        return ret

    def list_torrents(self):
        if not self.connected:
            ret = ClientRet(ret_type=-2)
            return ret

        torrent_id_list = self.client.core.get_session_state()
        session_status = {}
        for idx in torrent_id_list:
            torrent_status_raw = self.client.core.get_torrent_status(torrent_id=idx,
                                                                     keys=bt_client.client_base.torrent_status_key)
            torrent_status = TorrentStatus(torrent_id=idx.decode(),
                                           is_finished=torrent_status_raw['is_finished'.encode()],
                                           name=torrent_status_raw['name'.encode()].decode())
            session_status[torrent_status.torrent_id] = torrent_status

        ret = ClientRet(ret_type=4, ret_value=session_status)

        return ret

    def get_torrent_status(self, idx):  # All the value inputted and returned back should be string, not bytearray
        if not self.connected:
            ret = ClientRet(ret_type=-2)
            return ret

        idx = idx.encode() # Convert to byte array for Deluge
        torrent_status_raw = self.client.core.get_torrent_status(torrent_id=idx,
                                                                 keys=bt_client.client_base.torrent_status_key)
        torrent_status = TorrentStatus(torrent_id=idx.decode(),
                                       is_finished=torrent_status_raw['is_finished'.encode()],  # Decode bytearray to string
                                       name=torrent_status_raw['name'.encode()].decode())       # Decode bytearray to string 

        ret = ClientRet(ret_type=6, ret_value=torrent_status)
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
                ret = ClientRet(ret_type=5)
                return ret
            else:
                ret = ClientRet(ret_type=-5)
                return ret
        else:
            ret = ClientRet(ret_type=-5)
            return ret

    def disconnect(self):
        if self.connected:
            self.client.disconnect()
            self.connected = False
        ret = ClientRet(ret_type=0)
        return ret
