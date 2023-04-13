import datetime, requests, json
from utils import parse_config
from log import logger


def send(failed_list):
    config = parse_config()
    now = datetime.datetime.now().strftime('%Y-%m-%d')
    url = config['webhook']['url']
    devices = config['devices']
    data = {
        'msgtype': 'markdown',
        'markdown': {
            'content': '<font color=\"warning\">网络自动化备份任务通知</font>'
                       '\n><font color=\"info\">备份日期</font>: %s'
                       '\n><font color=\"info\">备份设备总数</font>: %s'
                       '\n><font color=\"info\">备份失败总数</font>: %s'
                       '\n><font color=\"info\">备份失败设备列表</font>: %s'
                       % (now, len(devices), len(failed_list), failed_list)
        }
    }
    resp = requests.post(url, data=json.dumps(data))
    if resp.json()['errcode'] != 0:
        logger('webhook').error(resp.json()['errmsg'])
