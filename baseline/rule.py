"""
根据不同类型设备定义对应的基线扫描项,其中rule字段作为正则匹配判断是否满足基线标准,
可参考以下格式自行新增删除检测项
"""

scan_template = [
    # cisco_ios
    {
        'vendor': 'cisco_ios', 'name': 'ntp', 'desc': '开启ntp时间同步协议', 'level': '中危', 'rule': 'ntp server.+'
    },
    {
        'vendor': 'cisco_ios', 'name': 'syslog', 'desc': '开启syslog日志功能并记录至服务器', 'level': '中危',
        'rule': 'logging.*?\\d+[.]\\d+[.]\\d+[.]\\d+'
    },
    {
        'vendor': 'cisco_ios', 'name': 'aaa', 'desc': '开启3A认证审计', 'level': '高危', 'rule': 'aaa group server tacacs\\+.+'
    },
    {
        'vendor': 'cisco_ios', 'name': 'ssh', 'desc': '开启SSH白名单限制指定客户端登录', 'level': '高危', 'rule': 'access-class.*?in'
    },
    {
        'vendor': 'cisco_ios', 'name': 'snmp', 'desc': '开启网管协议snmp', 'level': '中危',
        'rule': 'snmp-server community .*?RO'
    },
    {
        'vendor': 'cisco_ios', 'name': 'telnet', 'desc': '禁止开启telnet服务', 'level': '严重',
        'rule': 'transport input .*?telnet'
    },
    {
        'vendor': 'cisco_ios', 'name': 'login timeout', 'desc': 'SSH登录在超时时间内无操作将自动登出', 'level': '高危',
        'rule': 'ip ssh time-out.+'
    },
    {
        'vendor': 'cisco_ios', 'name': 'login lock', 'desc': '错误密码尝试登录达到指定次数触发锁定', 'level': '高危',
        'rule': 'login block-for.+'
    },
    # huawei
    {
        'vendor': 'huawei', 'name': 'ntp', 'desc': '开启ntp时间同步协议', 'level': '中危', 'rule': 'ntp.*? unicast-server.+'
    },
    {
        'vendor': 'huawei', 'name': 'syslog', 'desc': '开启syslog日志功能并记录至服务器', 'level': '中危',
        'rule': 'info-center loghost.+'
    },
    {
        'vendor': 'huawei', 'name': 'aaa', 'desc': '开启3A认证审计', 'level': '高危', 'rule': 'authentication-scheme.+'
    },
    {
        'vendor': 'huawei', 'name': 'ssh', 'desc': '开启SSH白名单限制指定客户端登录', 'level': '高危', 'rule': 'acl \\d* inbound'
    },
    {
        'vendor': 'huawei', 'name': 'snmp', 'desc': '开启网管协议snmp', 'level': '中危',
        'rule': 'snmp-agent community.+'
    },
    {
        'vendor': 'huawei', 'name': 'telnet', 'desc': '禁止开启telnet服务', 'level': '严重',
        'rule': '^telnet server enable'
    },
    {
        'vendor': 'huawei', 'name': 'login timeout', 'desc': 'SSH登录在超时时间内无操作将自动登出', 'level': '高危',
        'rule': 'ssh server timeout.+'
    },
    {
        'vendor': 'huawei', 'name': 'login lock', 'desc': '错误密码尝试登录达到指定次数触发锁定', 'level': '高危',
        'rule': 'ssh server authentication-retries.+'
    },
    # cisco_nxos
    {
        'vendor': 'cisco_nxos', 'name': 'ntp', 'desc': '开启ntp时间同步协议', 'level': '中危', 'rule': 'ntp server.+'
    },
    {
        'vendor': 'cisco_nxos', 'name': 'syslog', 'desc': '开启syslog日志功能并记录至服务器', 'level': '中危',
        'rule': 'logging server.+'
    },
    {
        'vendor': 'cisco_nxos', 'name': 'aaa', 'desc': '开启3A认证审计', 'level': '高危', 'rule': 'aaa group server tacacs\\+.+'
    },
    {
        'vendor': 'cisco_nxos', 'name': 'ssh', 'desc': '开启SSH白名单限制指定客户端登录', 'level': '高危', 'rule': 'access-class.*?in'
    },
    {
        'vendor': 'cisco_nxos', 'name': 'snmp', 'desc': '开启网管协议snmp', 'level': '中危',
        'rule': 'snmp-server community.*?group.+'
    },
    {
        'vendor': 'cisco_nxos', 'name': 'telnet', 'desc': '禁止开启telnet服务', 'level': '严重',
        'rule': 'feature telnet'
    },
    {
        'vendor': 'cisco_nxos', 'name': 'login timeout', 'desc': 'SSH登录在超时时间内无操作将自动登出', 'level': '高危',
        'rule': 'exec-timeout.+'
    },
    {
        'vendor': 'cisco_nxos', 'name': 'login lock', 'desc': '错误密码尝试登录达到指定次数触发锁定', 'level': '高危',
        'rule': 'ssh login-attempts.+'
    },
    # h3c
    {
        'vendor': 'hp_comware', 'name': 'ntp', 'desc': '开启ntp时间同步协议', 'level': '中危', 'rule': 'ntp.*? unicast-server.+'
    },
    {
        'vendor': 'hp_comware', 'name': 'syslog', 'desc': '开启syslog日志功能并记录至服务器', 'level': '中危',
        'rule': 'info-center loghost.+'
    },
    {
        'vendor': 'hp_comware', 'name': 'ssh', 'desc': '开启SSH白名单限制指定客户端登录', 'level': '高危', 'rule': 'ssh server acl \\d*'
    },
    {
        'vendor': 'hp_comware', 'name': 'snmp', 'desc': '开启网管协议snmp', 'level': '中危',
        'rule': 'snmp-agent community.+'
    },
    {
        'vendor': 'hp_comware', 'name': 'telnet', 'desc': '禁止开启telnet服务', 'level': '严重',
        'rule': 'telnet server enable'
    },
    {
        'vendor': 'hp_comware', 'name': 'login timeout', 'desc': 'SSH登录在超时时间内无操作将自动登出', 'level': '高危',
        'rule': 'idle-timeout \\d* \\d*'
    },
    {
        'vendor': 'hp_comware', 'name': 'login lock', 'desc': '错误密码尝试登录达到指定次数触发锁定', 'level': '高危',
        'rule': 'password-control login-attempt \\d* exceed lock-time \\d*'
    },
]
