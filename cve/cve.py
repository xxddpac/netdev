"""
    获取阿里云关于网络设备的CVE漏洞公告(作为计划任务执行,每一小时检测一次);
    每次都会请求第一页最新数据(30条),结果将存在当前目录下的result.txt;
    因未引入数据库/缓存等中间件,该文件将作为缓存用,已存在忽略,新增追加写入;
    新增CVE漏洞将会通过邮件发送通知;
"""

import random, urllib3, requests, datetime, re
from notify import mail

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class Cve(object):
    def __init__(self, verify):
        self.path = './cve/result.txt'
        self.avd_list_url = 'https://avd.aliyun.com/nvd/list'
        self.avd_detail_url = 'https://avd.aliyun.com/detail'
        self.headers = {'User-Agent': self.get_user_agent()}
        self.regexp = '<a.*?(CVE-\d*-\d*).*?<td>(.*?)</td>.*?(\d{4}-\d{2}-\d{2}).*?</td>'
        self.verify = verify

    def get_user_agent(self) -> str:
        user_agent_list = [
            'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.7113.93 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4482.0 Safari/537.36 Edg/92.0.874.0'
        ]
        return user_agent_list[random.randint(0, 2)]

    def __enter__(self):
        try:
            with open(self.path, encoding='utf-8') as f:
                self.cve_list = f.read()
        except FileNotFoundError:
            self.cve_list = ''
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.result == 0:
            return
        notify_cve_list = []
        with open(self.path, 'a', encoding='utf-8') as f:
            for item in self.result:
                if len(item) != 3:
                    continue
                cve_num = item[0]
                cve_desc = item[1]
                cve_date = item[2]
                if '空标题' in cve_desc:
                    # 偶尔会先录入CVE编号占位,标题和描述未录入，这种情况先忽略,后续继续同步
                    continue
                if cve_num in self.cve_list:
                    # 本地已存在CVE编号忽略
                    continue
                f.writelines('%s\n' % str(item))
                if not self.cve_list and cve_date < datetime.datetime.now().strftime('%Y-%m-%d'):
                    # 首次同步30条CVE缓存在本地不发送通知
                    continue
                notify_cve_list.append(item)
        if not notify_cve_list:
            return
        for item in notify_cve_list:
            avd = item[0].replace('CVE', 'AVD')
            detail_query_url = '%s?id=%s' % (self.avd_detail_url, avd)
            subject = '漏洞预警'
            body = 'CVE编号:%s\nCVE描述:%s\n发布日期:%s\n详情查询:%s' % (
                item[0], item[1], item[2], detail_query_url)
            mail.send(subject, body)

    def do(self):
        params = {
            'type': '硬件设备',
            'page': 1
        }
        response = requests.get(self.avd_list_url, headers=self.headers, params=params, verify=self.verify)
        self.result = re.findall(self.regexp, response.text, re.DOTALL)


def sync():
    with Cve(False) as c:
        c.do()
