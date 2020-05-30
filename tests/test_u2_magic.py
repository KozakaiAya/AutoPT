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

ret = site.minimize_download_cost(209)
if ret.successful():
    print('Magic succeeded')
else:
    print('Magic failed')
    exit(0)

ret = site.maximize_upload_gain(209)
if ret.successful():
    print('Magic succeeded')
else:
    print('Magic failed')
    exit(0)
