import paramiko, time, re, pexpect
from log import logger
from utils import parse_config


class Checkpoint(object):
    def __init__(self, host, username, password, path, port='22'):
        self.host = host
        self.username = username
        self.password = password
        self.port = port
        self.path = path
        self.version_regexp = r'Product.*?Gaia[ ]*(.+)'
        self.migrate_backup_name = '%s_checkpoint_migrate_config.tgz' % self.host

    def __enter__(self):
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh.connect(self.host, int(self.port), self.username, self.password, look_for_keys=False)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.ssh.close()
        info = dict()
        info['username'] = self.username
        info['password'] = self.password
        info['port'] = self.port
        info['version'] = self.version
        info['host'] = self.host
        info['path'] = self.path
        info['migrate_backup_name'] = self.migrate_backup_name
        migrate(**info)

    def save(self):
        # 备份CP防火墙system相关配置,作为基线检查
        conn = self.ssh.invoke_shell()
        conn.recv(65535)
        time.sleep(0.5)
        conn.send('show configuration\n')
        with open('%s/%s.txt' % (self.path, self.host), 'w+', encoding='utf-8') as f:
            while True:
                time.sleep(0.2)
                resp = conn.recv(65535).decode('utf-8')
                f.writelines(resp.replace('-- More --', ''))
                conn.send(' ')
                if len(resp) < 2:
                    break

        # Migrate备份CP其他核心配置(策略/VPN/NAT...)
        conn.send('show version product\n')
        time.sleep(0.5)
        resp = conn.recv(65535).decode('utf-8')
        logger('backup').info('%s cp fw version info:%s' % (self.host, resp))
        self.version = re.search(self.version_regexp, resp).group(1)
        # conn.send('expert\n')
        # time.sleep(0.5)
        # conn.send('%s\n' % self.password)
        # time.sleep(0.5)
        # conn.send('cd /opt/CPsuite-%s/fw1/bin/upgrade_tools/\n' % self.version)
        # time.sleep(0.5)
        # conn.send('./migrate export %s' % self.migrate_backup_name)
        # time.sleep(0.5)
        # conn.send('y\n')
        # time.sleep(5)
        # conn.send('scp ./%s %s@%s:%s' % (self.migrate_backup_name, self.username, self.host, self.path))
        # time.sleep(0.5)
        # conn.send('%s\n' % self.password)
        # time.sleep(3)
        # conn.send('rm -rf %s' % self.migrate_backup_name)
        # time.sleep(0.5)


def migrate(**kwargs):
    config = parse_config()
    scp_host = config['scp']['host']
    scp_user = config['scp']['user']
    scp_pass = config['scp']['pass']
    expert = {'pass': i['expert_password'] for i in config['devices'] if i['host'] == kwargs['host']}
    conn = pexpect.spawn('ssh -p %s %s@%s' % (kwargs['port'], kwargs['username'], kwargs['host']))
    conn.timeout = 600
    conn.maxread = 2000
    conn.expect(['[pP]assword', pexpect.EOF, pexpect.TIMEOUT])
    conn.sendline(kwargs['password'])
    conn.expect('>')
    conn.sendline('expert')
    conn.expect(['[pP]assword', pexpect.EOF, pexpect.TIMEOUT])
    conn.sendline(expert['pass'])
    conn.sendline('cd /opt/CPsuite-%s/fw1/bin/upgrade_tools/' % kwargs['version'])
    conn.sendline('./migrate export %s ' % kwargs['migrate_backup_name'])
    conn.expect('Do you want to continue')
    conn.sendline('y')
    conn.expect('successfully')
    conn.sendline(
        'scp ./%s %s@%s:%s' % (kwargs['migrate_backup_name'], scp_user, scp_host, kwargs['path']))
    conn.expect(['[pP]assword', pexpect.EOF, pexpect.TIMEOUT])
    conn.sendline(scp_pass)
    conn.expect('#')
    conn.sendline('rm -rf %s' % kwargs['migrate_backup_name'])
    conn.expect('#')
    conn.sendline('exit')
    conn.close()
