import yaml
import time

if __name__ == '__main__' and __package__ is None:  # WTF is PEP 328
    from os import sys, path
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from bt_client.transmission import TransmissionClient
from bt_client import client_base

with open('../config/deluge.yaml', 'r') as f:
    config = yaml.safe_load(f)

tr = TransmissionClient(rpc_address=config['rpc_address'],
                        rpc_port=config['rpc_port'],
                        username=config['username'],
                        password=config['password'],
                        config=config['config'])

ret = tr.connect()
if ret.successful():
    print("Connect Succeeded")
else:
    print(ret.get_error_msg())

ret = tr.add_torrent('./test.torrent', download_path='./test_download')
if ret.successful():
    torrent_idx = ret.ret_value
    print("Torrent ID:", torrent_idx)
    with open('./test_download/torrent_id', 'w') as f:
        f.write(torrent_idx)
else:
    print(ret.get_error_msg())
    exit(-1)

while True:
    ret = tr.list_torrents()
    if ret.successful():
        sess = ret.ret_value
    else:
        print(ret.get_error_msg())
        exit(-1)

    if client_base.is_torrent_finished(sess, torrent_idx):
        print("Download finished")
        print(sess)
        ret = deluge.get_torrent_status(torrent_idx)
        print(ret.ret_value)

        break
    else:
        time.sleep(1)
