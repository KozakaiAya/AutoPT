class BTClientBase():
    def __init__(self, rpc_address, rpc_port, username, password, config=None):
        raise NotImplementedError

    def connect(self):
        raise NotImplementedError

    def add_torrent(self, torrent_path, download_path=None):
        raise NotImplementedError

    def list_torrent(self):
        raise NotImplementedError

    def del_torrent(self, idx):
        raise NotImplementedError

class ClientRet():
    def __init__(self, ret_type, ret_value=None):
        self.ret_type = ret_type # Error: <0
        self.ret_value = ret_value

        self.ret_dict = {
            5: "Delete Torrent Successful",
            4: "Torrent List",
            3: "Torrent ID",
            2: "Client Connected",
            0: "All Green",
            -2: "Client Not Connected",
            -3: "Torrent Add Error",
            -5: "Delete Torrent Error"
        }

    def get_error_msg(self):
        if  self.ret_type < 0:
            return self.ret_dict[self.ret_type]
        else:
            return "All Green"
    
    def successful(self):
        return self.ret_type >= 0
