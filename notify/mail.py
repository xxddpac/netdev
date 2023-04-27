import smtplib, datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from utils import parse_config
from log import logger


def send(subject, body):
    config = parse_config()
    fromaddr = config['mail']['from_addr']
    toaddr = config['mail']['to_addr']
    server = config['mail']['server']
    port = config['mail']['port']
    password = config['mail']['password']
    try:
        msg = MIMEMultipart()
        msg['From'] = fromaddr
        msg['To'] = toaddr
        msg['Subject'] = subject
        body = body
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
