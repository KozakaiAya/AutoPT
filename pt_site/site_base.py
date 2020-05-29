class PTSiteBase():
    def __init__(self, config=None):
        raise NotImplementedError

    def get_torrent_by_id(self, torrent_id):
        raise NotImplementedError

    # Available target: 'ALL', 'SELF', and '<uid>'
    # Duration: int
    def minimize_download_cost(self, torrent_id, duration=24, target='SELF'):
        raise NotImplementedError

    def maximize_upload_gain(self, torrent_id, duration=24, target='SELF'):
        raise NotImplementedError


class SiteRet():
    def __init__(self, ret_type, ret_value=None):
        self.ret_type = ret_type  # Error: <0
        self.ret_value = ret_value

        self.ret_dict = {
            6: "Torrent Info",
            5: "Delete Torrent Successful",
            4: "Torrent List",
            3: "Torrent ID",
            2: "Client Connected",
            0: "All Green",
            -2: "Client Not Connected",
            -3: "Torrent Add Error",
            -4: "Torrent List Error",
            -5: "Delete Torrent Error",
            -6: "Torrent Info Error"
        }

    def get_error_msg(self):
        if self.ret_type < 0:
            return self.ret_dict[self.ret_type]
        else:
            return "All Green"

    def successful(self):
        return self.ret_type >= 0

