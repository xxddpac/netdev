"""
根据不同类型设备定义对应的基线扫描项,其中rule字段作为正则匹配判断是否满足基线标准
"""

scan_template = [
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
    }
]
