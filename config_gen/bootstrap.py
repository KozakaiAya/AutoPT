import yaml

deluge_config = {}
deluge_config['rpc_address'] = "127.0.0.1"
deluge_config['rpc_port'] = 58846
deluge_config['username'] = 'localclient or <username>:<password>:xx in ~/.config/deluge/auth'
deluge_config['password'] = 'some_long_password or <username>:<password>:xx in ~/.config/deluge/auth'

with open('./deluge_ex.yaml', 'w') as f:
    yaml.safe_dump(deluge_config, f)

transmission_config = {}
transmission_config['rpc_address'] = '127.0.0.1'
transmission_config['rpc_port'] = 9091
transmission_config['username'] = 'username'
transmission_config['password'] = 'password'
transmission_config['config'] = {'path': '/transmission/rpc'}

with open('./transmission_ex.yaml', 'w') as f:
    yaml.safe_dump(transmission_config, f)

qb_config = {}
qb_config['rpc_address'] = '127.0.0.1'
qb_config['rpc_port'] = 29000
qb_config['username'] = 'username'
qb_config['password'] = 'password'
qb_config['config'] = {'use_https': False}

with open('./qbittorrent_ex.yaml', 'w') as f:
    yaml.safe_dump(qb_config, f)

