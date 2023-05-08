"""
    获取设备:
    IP、主机名、序列号、系统版本、系统版本号、型号
"""

import re

asset_list = []


def cisco_ios_parse(data):
    hostname = re.compile(r'(\S+)\suptime').findall(data)
    version = re.compile(r'Cisco\sIOS\sSoftware.+Version\s([^,]+)').findall(data)
    sn = re.compile(r'System serial number.*?:.*?(\w+)').findall(data)
    image = re.compile(r'System\simage\sfile\sis\s"([^ "]+)').findall(data)
    model = re.compile(r'[Cc]isco\s(\S+).*memory.').findall(data)
    return hostname, version, sn, image, model


def cisco_nxos_parse(data):
    hostname = re.compile(r'Device name.*?(\w.+)').findall(data)
    version = re.compile(r'System version.*?(\w.+)').findall(data)
    sn = re.compile(r'Processor Board ID.*?(\w+)').findall(data)
    image = re.compile(r'[n|N]XOS image file is.*?(\w.+)').findall(data)
    model = re.compile(r'(cisco.*?[n|N]exus.+)').findall(data)
    return hostname, version, sn, image, model


def cisco_asa_parse(data):
    hostname = re.compile(r'(.*?)[ ]*up[ ]*\d.*?').findall(data)
    if len(hostname) == 2:
        hostname.pop(1)
    version = re.compile(r'Cisco Adaptive Security.*?Version[ ]*(\w.+)').findall(data)
    sn = re.compile(r'Serial Number.*?(\w+)').findall(data)
    image = re.compile(r'System image.*?"(.+)"').findall(data)
    model = re.compile(r'Hardware:[ ]*(\w+),').findall(data)
    return hostname, version, sn, image, model


def hp_comware_parse(data):
    hostname = re.compile(r'sysname[ ]*(\S+)').findall(data)
    version = re.compile(r'System image version:.*?(\d.+)').findall(data)
    sn = re.compile(r'DEVICE_SERIAL_NUMBER.*?[:][ ]*(.+)').findall(data)
    if len(sn) != 0:
        sn = [sn[0]]
    image = re.compile(r'System image:[ ]*(.+)').findall(data)
    model = re.compile(r'H3C[ ]*(\S+).*?uptime').findall(data)
    return hostname, version, sn, image, model


asset_map = {
    'cisco_ios': cisco_ios_parse,
    'cisco_nxos': cisco_ios_parse,
    'cisco_asa': cisco_asa_parse,
    'hp_comware': hp_comware_parse
}


def parse(ip, vendor, data):
    hostname, version, sn, image, model = asset_map[vendor](data)
    asset_list.append({
        'ip': ip, 'hostname': ','.join(hostname), 'vendor': vendor,
        'os': ','.join(image), 'version': ','.join(version), 'sn': ','.join(sn), 'model': ','.join(model)
    })
