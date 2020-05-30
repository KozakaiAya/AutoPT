import requests
import bs4
import math
import tempfile
from pathlib import Path

from pt_site.site_base import PTSiteBase, SiteRet


class U2Site(PTSiteBase):
    def __init__(self, config):
        '''
        config: {
            url: https://example.com
            passkey: '<passkey>'
            cookie: {key: value}
            uid: '<uid>'
        }
        '''
        self.url = config['url']
        self.passkey = str(config['passkey'])
        self.cookie_dict = config['cookie']
        self.uid = str(config['uid'])

        self.cookie_string = ''
        for idx, key, value in enumerate(self.cookie_dict.items()):
            if idx > 0:
                self.cookie_string += '; '
            self.cookie_string += key + '=' + value

        self.header = {
            'dnt': '1',
            'accept-encoding': 'gzip, deflate',
            'accept-language': 'zh-CN,zh;q=0.8',
            'upgrade-insecure-requests': '1',
            'user-agent':
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'cache-control': 'max-age=0',
            'authority': 'u2.dmhy.org',
            'cookie': self.cookie_string
        }

        self.tmpdir = tempfile.mkdtemp(prefix='AutoPT_U2_')

    def get_torrent_by_id(self, torrent_id):
        link = "https://u2.dmhy.org/download.php?id=" + str(torrent_id) + "&passkey=" + self.passkey + "&http=1"
        torrent_content = requests.get(link).content

        torrent_path = Path(self.tmpdir, str(torrent_id) + '.torrent')
        with open(torrent_path, 'wb') as f:
            f.write(torrent_content)

        ret = SiteRet(ret_type=2, ret_value=torrent_path)
        return ret

    def _send_u2_magic(self, torrent_id, duration, target, upload=1, download=1):
        url = 'https://u2.dmhy.org/promotion.php?action=magic&torrent=' + str(torrent_id)
        page = requests.get(url, headers=self.header).text
        soup = bs4.BeautifulSoup(page, 'lxml')

        data = {}
        data['action'] = soup.find('input', {'name': 'action'})['value']
        data['divergence'] = soup.find('input', {'name': 'divergence'})['value']
        data['base_everyone'] = soup.find('input', {'name': 'base_everyone'})['value']
        data['base_self'] = soup.find('input', {'name': 'base_self'})['value']
        data['base_other'] = soup.find('input', {'name': 'base_other'})['value']
        data['torrent'] = soup.find('input', {'name': 'torrent'})['value']
        data['tsize'] = soup.find('input', {'name': 'tsize'})['value']
        data['ttl'] = soup.find('input', {'name': 'ttl'})['value']

        # user: 'ALL', 'SELF', or 'OTHER' (user_other required)
        # user_other: UID for 'OTHER', empty otherwise
        if (target == 'ALL') or (target == 'SELF'):
            data['user'] = target
            data['user_other'] = ''
        else:
            data['user'] = 'OTHER'
            data['user_other'] = str(target)
        data['start'] = 0  # in effect immediately
        data['hours'] = int(duration)

        if math.isclose(upload, 1) and math.isclose(download, 0):  # Free
            data['promotion'] = 2
        elif math.isclose(upload, 2) and math.isclose(download, 1):  # 2x
            data['promotion'] = 3
        elif math.isclose(upload, 2) and math.isclose(download, 0):  # 2xFree
            data['promotion'] = 4
        elif math.isclose(upload, 1) and math.isclose(download, 0.5):  # 50%
            data['promotion'] = 5
        elif math.isclose(upload, 2) and math.isclose(download, 0.5):  # 2x50%
            data['promotion'] = 6
        elif math.isclose(upload, 1) and math.isclose(download, 0.3):  # 30%
            data['promotion'] = 7
        else:  # Other
            data['promotion'] = 8
            data['ur'] = upload
            data['dr'] = download
        data['comment'] = ''

        url = 'https://u2.dmhy.org/promotion.php?test=1'
        page = requests.post(url, headers=self.header, data=data).text
        soup = bs4.BeautifulSoup(page, 'lxml')
        ucoin_cost = soup.find('span', {'class': '\\"ucoin-notation\\"'})['title'][2:-2]

        # Magic
        url = 'https://u2.dmhy.org/promotion.php?action=magic&torrent=' + str(torrent_id)
        page = requests.post(url, headers=self.header, data=data)
        if page.status_code == 200:
            return ucoin_cost
        else:
            return -1

    def minimize_download_cost(self, torrent_id, duration=24, target='SELF'):
        ucoin_cost = self._send_u2_magic(torrent_id, duration, target, download=0)

        if (ucoin_cost != -1):
            ret = SiteRet(3, ret_value=ucoin_cost)
        else:
            ret = SiteRet(-3)

        return ret

    def maximize_upload_gain(self, torrent_id, duration=24, target='SELF'):
        ucoin_cost = self._send_u2_magic(torrent_id, duration, target, upload=2.33)

        if (ucoin_cost != -1):
            ret = SiteRet(3, ret_value=ucoin_cost)
        else:
            ret = SiteRet(-3)

        return ret
