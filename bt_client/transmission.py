from pathlib import Path
import torf
from transmission_rpc import Client
import math

from bt_client.client_base import BTClientBase, TorrentStatus, ClientRet
from utils.cmd import execute


# Note: Please modify the 'User' in /lib/systemd/system/transmission-daemon.service to 'root'
# Note: Please follow https://help.ubuntu.com/community/TransmissionHowTo to set the 'rpc-whitelist' and change the 'umask' to 2
class TransmissionClient(BTClientBase):
    def __init__(self, rpc_address, rpc_port, username, password, config={'path': '/transmission/rpc'}):
        """
        Transmission Client for AutoPT

        config: dict
            {path: '/transmission/'}
        """

        self.rpc_address = rpc_address
        self.rpc_port = int(rpc_port)
        self.username = username
        self.password = password
        self.path = config['path']  # For now, only consider path

        self.connected = False
        self.client = None

    def connect(self):
        try:
            self.client = Client(host=self.rpc_address,
                                 port=self.rpc_port,
                                 username=self.username,
                                 password=self.password,
                                 path=self.path)
            self.connected = True
            ret = ClientRet(ret_type=2)
        except:
            ret = ClientRet(ret_type=-2)
        finally:
            return ret

    def add_torrent(self, torrent_path, download_path=None):
        if not self.connected:
            ret = ClientRet(ret_type=-2)
            return ret

        abs_torrent_path = str(Path(torrent_path).resolve())
        try:
            if download_path is None:
                torrent_obj = self.client.add_torrent(abs_torrent_path, paused=False)
            else:
                download_path = str(Path(download_path).resolve())
                torrent_obj = self.client.add_torrent(abs_torrent_path, download_dir=download_path,
                                                      paused=False)  # Must be absolute path
            if torrent_obj is not None:
                ret = ClientRet(ret_type=3, ret_value=torrent_obj.hashString)
        except:
            ret = ClientRet(ret_type=-3)
        finally:
            return ret

    def list_torrents(self):
        if not self.connected:
            ret = ClientRet(ret_type=-2)
            return ret

        try:
            torrent_obj_list = self.client.get_torrents()
            session_status = {}
            for torrent_obj in torrent_obj_list:
                is_finished = math.isclose(torrent_obj.progress, 100)
                torrent_status = TorrentStatus(torrent_id=torrent_obj.hashString,
                                               is_finished=is_finished,
                                               name=torrent_obj.name)

                session_status[torrent_obj.hashString] = torrent_status

            ret = ClientRet(ret_type=4, ret_value=session_status)
        except:
            ret = ClientRet(ret_type=-4)
        finally:
            return ret

    def get_torrent_status(self, idx):
        if not self.connected:
            ret = ClientRet(ret_type=-2)
            return ret

        try:
            torrent_obj = self.client.get_torrent(idx)
            is_finished = math.isclose(torrent_obj.progress, 100)
            torrent_status = TorrentStatus(torrent_id=torrent_obj.hashString,
                                           is_finished=is_finished,
                                           name=torrent_obj.name)

            ret = ClientRet(ret_type=6, ret_value=torrent_status)
        except:
            ret = ClientRet(ret_type=-6)
        finally:
            return ret

    def del_torrent(self, idx):
        if not self.connected:
            ret = ClientRet(ret_type=-2)
            return ret

        try:
            torrent_obj = self.client.get_torrent(idx)
            torrent_exist = True
        except:
            torrent_exist = False

        if torrent_exist:
            try:
                self.client.remove_torrent(idx, delete_data=True)
                ret = ClientRet(ret_type=5)
            except:
                ret = ClientRet(ret_type=-5)
            finally:
                return ret
        else:
            ret = ClientRet(ret_type=-5)
            return ret

    def disconnect(self):
        self.connected = False
        self.client = None
        ret = ClientRet(ret_type=0)
        return ret
