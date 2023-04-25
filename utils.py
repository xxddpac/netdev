import tomli, datetime, base64
import pandas as pd


def parse_config() -> dict:
    with open('config.toml', encoding='utf-8') as c:
        return tomli.loads(c.read())


def save(path, ip, result):
    with open('%s/%s.txt' % (path, ip), 'w+', encoding='utf-8') as f:
        f.writelines(result)


def write_to_xlsx(result):
    config = parse_config()
    time_now = datetime.datetime.now().strftime('%Y-%m-%d')
    path = '%s%s' % (config['config_path'], time_now)
    df = pd.DataFrame.from_dict(result)
    df.to_excel('%s/baseline.xlsx' % path)


def encode(string):
    bytes = string.encode('utf-8')
    base64_bytes = base64.b64encode(bytes)
    base64_string = base64_bytes.decode('utf-8')
    return base64_string


class NetDevException(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)
