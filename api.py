import datetime, os, re
from fastapi import FastAPI, BackgroundTasks
from network.backup import run
from utils import parse_config
from log import logger
from fastapi.responses import FileResponse

app = FastAPI()


# 异步执行备份任务
@app.get('/api/v1/network/config/backup')
async def backup(background_tasks: BackgroundTasks):
    background_tasks.add_task(run)
    return {'msg': 'success', 'code': 200, 'data': None}


# 根据日期获取相同设备配置差异对比
@app.get('/api/v1/network/config/diff')
async def diff():
    # todo
    return {'msg': 'success', 'code': 200, 'data': None}


# 获取设备最新配置
@app.get('/api/v1/network/config/query')
async def query(host: str):
    filename = host + '.txt'
    path = parse_config()['config_path']
    now = datetime.datetime.now().strftime('%Y-%m-%d')
    files = os.listdir('%s%s' % (path, now))
    if filename not in files:
        logger('api for query').error('config with %s not found' % host)
        return {'msg': 'config with %s not found' % host, 'code': 400, 'data': None}
    return FileResponse('%s/%s/%s' % (path, now, filename))


# 获取最新备份成功设备(ip)列表
@app.get('/api/v1/network/config/list')
async def list():
    pattern = r'\d*[.]\d*[.]\d*[.]\d*'
    path = parse_config()['config_path']
    now = datetime.datetime.now().strftime('%Y-%m-%d')
    files = os.listdir('%s%s' % (path, now))
    result = [re.search(pattern, item).group() for item in files]
    return {'msg': 'success', 'code': 200, 'data': {
        'total': len(result),
        'list': result
    }}
