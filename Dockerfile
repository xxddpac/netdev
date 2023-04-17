FROM python:3.8

WORKDIR ./netdev

ADD . .

RUN pip install -r requirements.txt -i https://pypi.douban.com/simple/

EXPOSE 5000

RUN /bin/cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime && echo 'Asia/Shanghai' > /etc/timezone

CMD ["python", "main.py"]