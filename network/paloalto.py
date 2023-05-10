import requests
from lxml import etree


class Paloalto(object):
    def __init__(self, host, username, password, path, port='443'):
        self.host = host
        self.username = username
        self.password = password
        self.path = path
        self.port = port
        self.base_url = 'https://%s:%s/api/' % (self.host, self.port)
        self.key = self.get_key()

    def get_key(self):
        params = {
            'type': 'keygen',
            'user': self.username,
            'password': self.password
        }
        response = requests.get(self.base_url, params=params, verify=False)
        return etree.HTML(response.content).xpath('//key')[0].text

    def save(self):
        params = {
            'type': 'export',
            'category': 'configuration',
            'key': self.key
        }
        result = requests.get(self.base_url, params=params, verify=False)
        with open(r'%s/%s.xml' % (self.path, self.host), 'w') as files:
            files.write(str(result.content, 'utf-8'))

    def system(self):
        params = {
            'type': 'op',
            'cmd': '<show><system><info></info></system></show>',
            'key': self.key
        }
        response = requests.get(self.base_url, params=params, verify=False)
        return etree.HTML(response.content)
