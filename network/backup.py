import datetime
import os
import threading

from utils import parse_config, save
from netmiko import ConnectHandler
from queue import Queue
from .fortigate import FortiGate
from .hillstone import Hillstone
from .checkpoint import Checkpoint
from .paloalto import Paloalto
from log import logger
from notify import webchat, mail

failed_list = []


def run():
    failed_list.clear()
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

    if len(failed_list) == 0:
        logger('backup').info('success backup all devices')
        return
    # 仅备份失败发送通知
    if config['webhook']['enable']:
        webchat.send(failed_list)

    if config['mail']['enable']:
        mail.send(failed_list)


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
                FortiGate(host, username, password, path, port=port).save()
            elif vendor == 'hillstone':
                Hillstone(host, username, password, path, port=port).save()
            elif vendor == 'checkpoint':
                with Checkpoint(host, username, password, path, port=port) as cp:
                    cp.save()
            elif vendor == 'paloalto':
                Paloalto(host, username, password, path, port=port).save()
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
            failed_list.append(host)
            logger('config_backup').error('host:%s error:%s\n' % (host, err))
        finally:
            q.task_done()
