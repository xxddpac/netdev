import datetime
import os
import threading

from utils import parse_config, save
from netmiko import ConnectHandler
from queue import Queue
from .fortigate import FortiGate
from log import logger


def run():
    config = parse_config()
    time_now = datetime.datetime.now().strftime('%Y-%m-%d')
    path = '%s%s' % (config['config_path'], time_now)
    if not os.path.exists(path):
        os.makedirs(path)
    q = Queue()
    for item in config['devices']:
        q.put({**item, 'path': path})
    for i in range(config['max_workers']):
        t = threading.Thread(target=do, args=(q,))
        t.setDaemon(True)
        t.start()
    q.join()


def do(q):
    while True:
        info = q.get()
        host = info['host']
        port = info['port']
        vendor = info['vendor']
        username = info['username']
        password = info['password']
        command = info['command']
        path = info['path']
        try:
            if vendor == 'fortigate':
                pass
                FortiGate(host, username, password, path, port=port).save()
            else:
                connect = ConnectHandler(
                    device_type=vendor,
                    host=host,
                    username=username,
                    password=password,
                    conn_timeout=160,  # ssh连接超时时间
                    port=port
                )
                result = connect.send_command(command, read_timeout=160)  # 读取配置超时时间
                connect.disconnect()
                save(path, host, result)
        except Exception as err:
            logger('config_backup').error('host:%s error:%s\n' % (host, err))
        finally:
            q.task_done()
