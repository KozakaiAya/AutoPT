# AutoPT

Python toolbox for interacting with popular BT clients and PT websites.

This project is currently under development.

## Current Goal

* Provide the infrastructure for PT users' common operations, for example, BT client interaction, archiving, backup, etc.
* Automate the process of download and backup with a list of TorrentID.

## Roadmap

### BT Client Interaction

- [x] Definition of base operations
- [x] Deluge interaction
- [ ] Transmission interaction
- [ ] qBittorrent interaction

### PT Website Interaction

- [ ] Definition of base operations
- [ ] U2 interaction
- [ ] RSS Feed (maybe...)

### Backup Software Interaction

- [ ] Definition of base operations
- [ ] Rclone/gclone
- [ ] RAR
- [ ] PAR2

### Configuration Format Definition

- [x] Deluge
- [ ] Transmission
- [ ] qBittorrent
- [ ] Rclone/gclone
- [ ] Cookie management for NexusPHP-based websites
- [ ] RSS (maybe...)

### Miscellaneous Functions

- [ ] Folder operations
- [ ] Subprocess operations

## References

This project is based on the following open-source projects:
* https://gist.github.com/littleya/86cd895f97b614ebea376a1008291ccf
* https://github.com/JohnDoee/deluge-client
