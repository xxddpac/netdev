import tomli,datetime,os
import pandas as pd

def parse_config() -> dict:
    with open('config.toml', encoding='utf-8') as c:
        return tomli.loads(c.read())


def save(path, ip, result):
    with open('%s/%s.txt' % (path, ip), 'w+', encoding='utf-8') as f:
        f.writelines(result)

def write_to_xlsx(result):
    df = pd.DataFrame.from_dict(result)
    os.path.join(os.path.abspath(os.path.join(os.getcwd(), "..")),'')
    df.to_excel('./baseline/baseline_%s.xlsx'%datetime.datetime.now().strftime('%Y-%m-%d'))