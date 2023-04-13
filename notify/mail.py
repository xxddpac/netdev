import smtplib, datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from utils import parse_config
from log import logger


def send(failed_list):
    now = datetime.datetime.now().strftime('%Y-%m-%d')
    config = parse_config()
    fromaddr = config['mail']['from_addr']
    toaddr = config['mail']['to_addr']
    server = config['mail']['server']
    port = config['mail']['port']
    devices = config['devices']
    password = config['mail']['password']
    try:
        msg = MIMEMultipart()
        msg['From'] = fromaddr
        msg['To'] = toaddr
        msg['Subject'] = "网络自动化备份任务通知"
        body = "备份日期:%s\n备份设备总数:%d\n备份失败总数:%d\n备份失败设备列表:%s" % (
            now, len(devices), len(failed_list), failed_list)
        msg.attach(MIMEText(body, 'plain'))
        server = smtplib.SMTP(server, port)
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(fromaddr, password)
        text = msg.as_string()
        server.sendmail(fromaddr, toaddr.split(','), text)
        server.quit()
    except Exception as err:
        logger('mail').error('err send mail --> %s', err)
