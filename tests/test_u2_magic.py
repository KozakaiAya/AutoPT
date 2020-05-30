import yaml
import time
import shutil

if __name__ == '__main__' and __package__ is None:  # WTF is PEP 328
    from os import sys, path
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from pt_site.u2 import U2Site

with open('../config/u2.yaml', 'r') as f:
    config = yaml.safe_load(f)

site = U2Site(config=config)

ret = site.get_torrent_by_id(209)
if ret.successful():
    torrent_path = ret.ret_value
    shutil.copy(torrent_path, './test_download')
else:
    print("Get torrent failed")
    exit(0)

time.sleep(1)

ret = site.minimize_download_cost(209)
if ret.successful():
    print('Download magic succeeded')
    print('Ucoin used:', ret.ret_value)
else:
    print('Download magic failed')
    exit(0)

time.sleep(1)

ret = site.maximize_upload_gain(209)
if ret.successful():
    print('Upload magic succeeded')
    print('Ucoin used:', ret.ret_value)
else:
    print('Upload magic failed')
    exit(0)

time.sleep(1)

ret = site.minimize_download_cost(209, target='ALL')
if ret.successful():
    print('Global download magic succeeded')
    print('Ucoin used:', ret.ret_value)
else:
    print('Global download magic failed')
    exit(0)

time.sleep(1)

ret = site.maximize_upload_gain(209, target='ALL')
if ret.successful():
    print('Global upload magic succeeded')
    print('Ucoin used:', ret.ret_value)
else:
    print('Global upload magic failed')
    exit(0)

time.sleep(1)

ret = site.minimize_download_cost(209, target=44998)
if ret.successful():
    print('Other download magic succeeded')
    print('Ucoin used:', ret.ret_value)
else:
    print('Other download magic failed')
    exit(0)

time.sleep(1)

ret = site.maximize_upload_gain(209, target=44998)
if ret.successful():
    print('Other upload magic succeeded')
    print('Ucoin used:', ret.ret_value)
else:
    print('Other upload magic failed')
    exit(0)

from bt_client.deluge import DelugeClient

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

ret = deluge.add_torrent('./test_download/209.torrent', download_path='./test_download')
if ret.successful():
    torrent_idx = ret.ret_value
    print("Torrent ID:", torrent_idx)
    with open('./test_download/torrent_id', 'w') as f:
        f.write(torrent_idx)
else:
    print(ret.get_error_msg())
    exit(-1)