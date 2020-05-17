import yaml
import time

if __name__ == '__main__' and __package__ is None:  # WTF is PEP 328
    from os import sys, path
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from bt_client.qbittorrent import QBittorrentClient
from bt_client import client_base

with open('../config/qbittorrent.yaml', 'r') as f:
    config = yaml.safe_load(f)

qb = QBittorrentClient(rpc_address=config['rpc_address'],
                        rpc_port=config['rpc_port'],
                        username=config['username'],
                        password=config['password'],
                        config=config['config'])

ret = qb.connect()
if ret.successful():
    print("Connect Succeeded")
else:
    print(ret.get_error_msg())

with open('./test_download/torrent_id', 'r') as f:
    torrent_idx = f.read()

ret = qb.list_torrents()
if ret.successful():
    tlist = ret.ret_value
else:
    print("Torrent does not exist")
    exit(-1)

if torrent_idx in tlist:
    print(tlist[torrent_idx])
    ret = qb.del_torrent(torrent_idx)
    if ret.successful():
        print("Delete succeeded")
        ret = qb.disconnect()
        if ret.successful():
            print("Disconnect succeeded")
    else:
        print(ret.get_error_msg)

