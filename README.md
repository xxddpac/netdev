# 基于fastapi实现的简单网络自动化后端服务


## 支持功能

- 实现全网多种类型设备配置备份(思科、华为、华三、飞塔、山石、Juniper...)
- 备份任务通知(企业微信、邮件)，展示任务执行详情(设备IP总数、执行失败IP数、执行失败IP列表)
- 安全基线扫描(针对不同类型设备定义安全扫描项，快速输出基线扫描结果应对合规检查要求)
- 配置历史对比(根据不同日期备份配置展示差异对比)
- 配置下载、配置查询等其他API服务

## 功能展示

- (手动)触发异步备份任务
```bash
curl http://127.0.0.1:5000/api/v1/network/config/backup

```

- (计划任务每天)触发异步备份任务
```bash
40 0 * * * curl http://127.0.0.1:5000/api/v1/network/config/backup

```

- 触发异步基线扫描任务(扫描结果.xlsx存放baseline文件夹下)
```bash
curl http://127.0.0.1:5000/api/v1/network/baseline/check
```

- 查询备份成功设备详情

![img](docs/list.png)

- 查询指定设备最新IP配置

![img](docs/query.png)

- 指定日期获取配置差异

![img](docs/diff.png)

- 备份任务通知

![img](docs/webchat.png)

- 安全基线扫描

![img](docs/baseline.png)

- 最新配置下载

![img](docs/download.png)