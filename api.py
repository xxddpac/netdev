import datetime, os, re, difflib
from fastapi import FastAPI, BackgroundTasks
from network.backup import run
from utils import parse_config
from log import logger
from fastapi.responses import FileResponse, Response
from baseline.baseline import check

app = FastAPI()


# 异步执行备份任务
@app.get('/api/v1/network/config/backup')
async def backup(background_tasks: BackgroundTasks):
    background_tasks.add_task(run)
    return {'msg': 'success', 'code': 200, 'data': None}


# 根据日期获取相同设备配置差异对比
@app.get('/api/v1/network/config/diff')
async def diff(_date: str, date: str, host: str):
    filename = host + '.txt'
    path = parse_config()['config_path']
    try:
        with open('%s%s/%s' % (path, _date, filename), encoding='utf-8') as f:
            _date_config = f.read().split('\n')
        with open('%s%s/%s' % (path, date, filename), encoding='utf-8') as f:
            date_config = f.read().split('\n')
        diff = difflib.HtmlDiff()
        htmlContent = diff.make_file(_date_config, date_config)
        response = Response(htmlContent)
        return response
    except Exception as err:
        logger('api for diff').error(err)
        return {'msg': err, 'code': 400, 'data': None}


# 获取设备最新配置
@app.get('/api/v1/network/config/query')
async def query(host: str):
    filename = host + '.txt'
    path = parse_config()['config_path']
    now = datetime.datetime.now().strftime('%Y-%m-%d')
    try:
        files = os.listdir('%s%s' % (path, now))
    except Exception as err:
        logger('api for query').error(err)
        return {'msg': err, 'code': 400, 'data': None}
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
    try:
        files = os.listdir('%s%s' % (path, now))
    except Exception as err:
        logger('api for query').error(err)
        return {'msg': err, 'code': 400, 'data': None}
    result = [re.search(pattern, item).group() for item in files]
    return {'msg': 'success', 'code': 200, 'data': {
        'total': len(result),
        'list': result
    }}


# 异步执行基线扫描
@app.get('/api/v1/network/baseline/check')
async def baseline(background_tasks: BackgroundTasks):
    background_tasks.add_task(check)
    return {'msg': 'success', 'code': 200, 'data': None}


# 下载设备最新配置
@app.get('/api/v1/network/config/download')
async def query(host: str):
    filename = host + '.txt'
    path = parse_config()['config_path']
    now = datetime.datetime.now().strftime('%Y-%m-%d')
    try:
        files = os.listdir('%s%s' % (path, now))
    except Exception as err:
        logger('api for download').error(err)
        return {'msg': err, 'code': 400, 'data': None}
    if filename not in files:
        logger('api for download').error('config with %s not found' % host)
        return {'msg': 'config with %s not found' % host, 'code': 400, 'data': None}
    return FileResponse('%s/%s/%s' % (path, now, filename), media_type='application/octet-stream', filename=filename)
