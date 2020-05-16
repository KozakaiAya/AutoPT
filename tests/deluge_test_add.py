import yaml
import time

if __name__ == '__main__' and __package__ is None: # WTF is PEP 328
    from os import sys, path
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from bt_client.deluge import DelugeClient
import bt_client.deluge

with open('../config/deluge.yaml', 'r') as f:
    deluge_config = yaml.load(f)

deluge = DelugeClient(rpc_address=deluge_config['rpc_address'], rpc_port=deluge_config['rpc_port'], username=deluge_config['username'], password=deluge_config['password'])

ret = deluge.connect()
if ret.successful():
    print("Connect Succeeded")
else:
    print(ret.get_error_msg())


ret = deluge.add_torrent('./test.torrent', download_path='./test_download')
if ret.successful():
    torrent_idx = ret.ret_value
    print("Torrent ID:", torrent_idx)
    with open('./test_download/torrent_id', 'w') as f:
        f.write(torrent_idx)
else:
    print(ret.get_error_msg())
    exit(-1)


while True:
    ret = deluge.list_torrent()
    if ret.successful():
        sess = ret.ret_value
    else:
        print(ret.get_error_msg())
        exit(-1)
    
    if bt_client.deluge.is_torrent_finished(sess, torrent_idx):
        print("Download finished")
        break
    else:
        time.sleep(1)

