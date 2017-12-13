import requests
from urlparse import urljoin

class QBClient():
    def __init__(self, url):
        self.main_url = url
        self.sess = self.create_session()

    def create_session(self):
        return requests.Session()

    def login(self, username, password):
        url = urljoin(self.main_url, '/login')
        auth = {'username':username, 'password':password}
        result = self.sess.post(url, data=auth)
        print result.text

    def delete_torrent(self, param=None):
        url = urljoin(self.main_url, '/command/delete')
        """
        param = { 'hash' : '1111111111111'}
        """
        result = self.sess.post(url, data=param)
        return result

    def get_torrent_list(self, param=None):
        url = urljoin(self.main_url, '/query/torrents' + (param if param else ''))
        result = self.sess.get(url)
        return result.json()
