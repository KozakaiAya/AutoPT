import yaml
import time

if __name__ == '__main__' and __package__ is None:  # WTF is PEP 328
    from os import sys, path
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from bt_client.deluge import DelugeClient
import bt_client.deluge

with open('../config/deluge.yaml', 'r') as f:
    deluge_config = yaml.load(f)

deluge = DelugeClient(rpc_address=deluge_config['rpc_address'],
                      rpc_port=deluge_config['rpc_port'],
                      username=deluge_config['username'],
                      password=deluge_config['password'])

ret = deluge.connect()
if ret.successful():
    print("Connect Succeeded")
else:
    print(ret.get_error_msg())

with open('./test_download/torrent_id', 'r') as f:
    torrent_idx = f.read()

ret = deluge.list_torrent()
if ret.successful():
    tlist = ret.ret_value
else:
    print("Torrent does not exist")
    exit(-1)

if torrent_idx in tlist:
    print(tlist[torrent_idx])
    ret = deluge.del_torrent(torrent_idx)
    if ret.successful():
        print("Delete succeeded")
        ret = deluge.disconnect()
        if ret.successful():
            print("Disconnect succeeded")
    else:
        print(ret.get_error_msg)

