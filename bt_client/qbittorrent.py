from qbittorrent import Client
from pathlib import Path
import torf
import math

from bt_client.client_base import BTClientBase, TorrentStatus, ClientRet

# Requires: qBittorrent >= v4.1.0 (WebAPI v2+)
class QBittorrentClient(BTClientBase):
    def __init__(self, rpc_address, rpc_port, username, password, config={'use_https': False}):
        self.rpc_address = rpc_address
        self.rpc_port = rpc_port
        self.username = username
        self.password = password

        if 'use_https' in config:
            self.use_https = config['use_https']
        else:
            self.use_https = False

        self.rpc_addr = str(rpc_address) + ':' + str(rpc_port) + '/'
        if self.use_https:
            self.rpc_addr = 'https://' + self.rpc_addr
        else:
            self.rpc_addr = 'http://' + self.rpc_addr

        self.client = Client(self.rpc_addr)
        self.connected = False

    def connect(self):
        login_ret = self.client.login(username=self.username, password=self.password)

        if login_ret is None:
            self.connected = True
            ret = ClientRet(ret_type=2)
        else:
            ret = ClientRet(ret_type=-2)

        return ret

    def add_torrent(self, torrent_path, download_path=None):
        if not self.connected:
            return ClientRet(ret_type=-2)

        abs_torrent_path = str(Path(torrent_path).resolve())
        buf = open(abs_torrent_path, 'rb')

        if download_path is None:
            try:
                api_ret = self.client.download_from_file(buf)
                if 'Ok.' in api_ret:
                    buf.close()
                    info_hash = torf.Torrent.read(abs_torrent_path).infohash

                    ret = ClientRet(ret_type=3, ret_value=info_hash)
                else:
                    ret = ClientRet(ret_type=-3)
            except:
                ret = ClientRet(ret_type=-3)
            finally:
                return ret
        else:
            try:
                abs_download_path = str(Path(download_path).resolve())
                api_ret = self.client.download_from_file(buf, save_path=abs_download_path)
                if 'Ok.' in api_ret:
                    buf.close()
                    info_hash = torf.Torrent.read(abs_torrent_path).infohash

                    ret = ClientRet(ret_type=3, ret_value=info_hash)
                else:
                    ret = ClientRet(ret_type=-3)
            except:
                ret = ClientRet(ret_type=-3)
            finally:
                return ret

    def list_torrents(self):
        if not self.connected:
            return ClientRet(ret_type=-2)

        torrent_list = self.client.torrents()
        session_status = {}
        for torrent in torrent_list:
            is_finished = math.isclose(torrent['progress'], 1)
            torrent_status = TorrentStatus(torrent_id=torrent['hash'], is_finished=is_finished, name=torrent['name'])

            session_status[torrent['hash']] = torrent_status

        ret = ClientRet(ret_type=4, ret_value=session_status)

        return ret

    def get_torrent_status(self, idx):
        if not self.connected:
            return ClientRet(ret_type=-2)

        tlist = self.client.torrents()
        for torrent in tlist:
            if idx == torrent['hash']: # No progress info in get_torrent() method, really...
                is_finished = math.isclose(torrent['progress'], 1)
                torrent_status = TorrentStatus(torrent_id=torrent['hash'], is_finished=is_finished, name=torrent['name'])
                
                ret = ClientRet(ret_type=6, ret_value=torrent_status)
                return ret

        return ClientRet(ret_type=-6)

    def del_torrent(self, idx, remove_data=True):
        if not self.connected:
            return ClientRet(ret_type=-2)

        try:
            if remove_data:
                self.client.delete_permanently(idx)
            else:
                self.client.delete(idx)
            ret = ClientRet(ret_type=5)
        except:
            ret = ClientRet(ret_type=-5)
        finally:
            return ret

    def disconnect(self):
        if self.connected:
            self.client.logout()
            self.connected = False
        ret = ClientRet(ret_type=0)
        return ret

