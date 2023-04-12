import tomli, os


def parse_config() -> dict:
    with open('config.toml', encoding='utf-8') as c:
        return tomli.loads(c.read())


def save(path, ip, result):
    with open('%s/%s.txt' % (path, ip), 'w+', encoding='utf-8') as f:
        f.writelines(result)
