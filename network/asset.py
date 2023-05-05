"""
    获取设备:
    IP、主机名、序列号、系统版本、系统版本号、型号
"""

import re

asset_list = []


def parse(ip, vendor, data):
    hostname = ''
    version = ''
    sn = ''
    image = ''
    model = ''
    if vendor == 'cisco_ios':
        hostname = re.compile(r'(\S+)\suptime').findall(data)
        version = re.compile(r'Cisco\sIOS\sSoftware.+Version\s([^,]+)').findall(data)
        sn = re.compile(r'System serial number.*?:.*?(\w+)').findall(data)
        image = re.compile(r'System\simage\sfile\sis\s"([^ "]+)').findall(data)
        model = re.compile(r'[Cc]isco\s(\S+).*memory.').findall(data)
    elif vendor == 'cisco_asa':
        pass
    elif vendor == 'cisco_nxos':
        pass
    elif vendor == 'huawei':
        pass
    elif vendor == 'hillstone':
        pass
    elif vendor == 'fortigate':
        pass
    elif vendor == 'junos':
        pass
    asset_list.append({
        '设备IP': ip, '主机名': ','.join(hostname), '设备类型': vendor,
        '系统镜像': ','.join(image), '系统版本': ','.join(version), '序列号': ','.join(sn), '型号': ','.join(model)
    })
