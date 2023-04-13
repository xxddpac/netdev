import os, datetime, re
from log import logger
from utils import parse_config, write_to_xlsx
from .rule import scan_template

pattern = r'\d*[.]\d*[.]\d*[.]\d*'
result = []

def get_vendor(devices, host) -> str:
    for device in devices:
        if host == device['host']:
            return device['vendor']

    return ''


def get_config(file, path, date) -> str:
    with open('%s%s/%s' % (path, date, file), encoding='utf-8') as f:
        return f.read()


def scan(host, vendor, config):
    for item in scan_template:
        if item['vendor'] != vendor:
            continue
        if not bool(re.search(item['rule'], config)):
            result.append({
                '设备地址': host, '设备类型': vendor, '检查项': item['name'],
                '检查项描述': item['desc'], '风险级别': item['level'], '检测结果': '未通过',
                '启用/禁用表达式参考': item['rule']
            })


def check():
    result.clear()
    now = datetime.datetime.now().strftime('%Y-%m-%d')
    config = parse_config()
    devices = config['devices']
    path = config['config_path']
    try:
        files = os.listdir('%s%s' % (path, now))
    except Exception as err:
        logger('baseline').error(err)
        return
    for file in files:
        host = re.search(pattern, file).group()
        vendor = get_vendor(devices, host)
        device_config = get_config(file, path, now)
        scan(host, vendor, device_config)
    write_to_xlsx(result)
