# AutoPT

Python toolbox for interacting with popular BT clients and PT websites.

This project is currently under development.

## Current Goal

* Provide the infrastructure of the PT users' common operations, for example, BT client interaction, archiving, backup, etc.
* Automate the process of downloading, archiving and making backup with a list of TorrentID.

## Roadmap

### BT Client Interaction

- [x] Definition of base operations
- [x] Deluge interaction
- [x] Transmission interaction
- [x] qBittorrent interaction

### PT Website Interaction

- [x] Definition of base operations
- [x] U2 interaction
- [ ] RSS Feed (maybe...)

### Backup Software Interaction

- [ ] Definition of base operations
- [ ] Rclone/gclone
- [ ] RAR
- [ ] PAR2

### Folder Operations

- [ ] Inter/Intra-seedbox file relocation

### Configuration Files

- [x] Deluge
- [x] Transmission
- [x] qBittorrent
- [ ] Rclone/gclone
- [ ] Cookie management for NexusPHP-based websites
- [ ] Multi-seedbox/client profile management and selection
- [ ] IFTTT, chain of tasks
- [ ] RSS (maybe...)

### Miscellaneous Functions

- [ ] Folder operations
- [ ] Subprocess operations
- [ ] SSH tunnel and port mapping

## References

This project is based on the following open-source projects:
* https://gist.github.com/littleya/86cd895f97b614ebea376a1008291ccf
* https://github.com/JohnDoee/deluge-client
* https://github.com/Trim21/transmission-rpc
* https://pypi.org/project/torf/
* https://pypi.org/project/python-qbittorrent/
* https://github.com/qbittorrent/qBittorrent/wiki/Web-API-Documentation
* https://github.com/BGmi/BGmi
* https://github.com/jerrymakesjelly/autoremove-torrents
* https://github.com/lysssssss/AutoPT