import requests, urllib3, json, utils
from utils import encode, NetDevException

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class Hillstone(object):
    def __init__(self, host, username, password, path, port='443'):
        self.host = host
        self.username = username
        self.password = password
        self.port = port
        self.path = path
        self.base_url = 'https://%s:%s/rest/' % (self.host, self.port)
        self.cookie, self.token = self.login()
        self.headers = {'Cookie': self.cookie}

    def login(self):
        path = 'api/login'
        data = {
            'lang': 'zh_CN',
            'password': encode(self.password),
            'userName': encode(self.username)
        }
        response = requests.post('%s%s' % (self.base_url, path), data=json.dumps(data), verify=False).json()
        if not response['success']:
            raise NetDevException('err login please check auth info')
        cookie, token = '', ''
        for item in response['result']:
            token = item['token']
            cookie = 'token=%s;username=%s;vsysId=%s;role=%s;fromrootvsys=%s' % (
                token, self.username, item['vsysId'], item['role'], item['fromrootvsys'])
        return cookie, token

    def write(self):
        path = 'api/currentcfg?moduleName=mgmt&operation=save'
        data = {
            'request_type': '0',
            'username': self.username,
            'protocol': 'https'
        }
        response = requests.post('%s%s' % (self.base_url, path), headers=self.headers, data=json.dumps(data),
                                 verify=False).json()
        if response['success'] != 'true':
            raise NetDevException('write config err')

    def export(self):
        path = 'api/currentcfg?moduleName=mgmt&operation=export'
        data = {
            'request_type': '0',
            'alias': ''
        }
        response = requests.post('%s%s' % (self.base_url, path), headers=self.headers, data=json.dumps(data),
                                 verify=False).json()
        if response['success'] != 'true':
            raise NetDevException('err export config')
        return response

    def save(self):
        self.write()
        dat = self.export()['result'][0]['msg']
        file = str(dat).split('/')[-1]
        path = 'https://%s:%s/download/bfm%s/%s/' % (self.host, self.port, dat, file)
        response = requests.get(path, headers=self.headers, verify=False)
        utils.save(self.path, self.host, response.text)
        self.logout()

    def logout(self):
        path = 'api/login'
        data = {
            'username': self.username,
            'protocol': 'https',
            'token': self.token,
            'role': 'admin'
        }
        requests.delete('%s%s' % (self.base_url, path), headers=self.headers, data=json.dumps(data),
                        verify=False)
