# Elec Room Info: SCUT 宿舍水电空调余额提醒

🥵你还在因半夜空调欠费被热醒没到服务时间无法充值所困扰吗？

😣你还在因忘充电费突然停电Boss快通关了实验跑到一半主机却关机了而痛苦吗？

🌟🌟你一定会需要的宿舍水电空调余额提醒程序！实时跟踪余额、多方式预警推送（微信、邮件）、充值检测、每日用电统计！再也不用定时检查余额啦！

---

如果你对我们的工作感兴趣，欢迎联系并加入后续开发！We Neeeed You!

## 功能

### v0.3.0

- [x] Wxpusher 微信推送

### v0.2.0

- [x] 新一卡通系统适配
- [x] Pushplus 微信推送

### v0.1.0

- [x] 水电空调余额跟踪
- [x] 余额不足报警
- [x] 充值检测
- [x] 邮件消息订阅

## 准备

- 一台长期运行的计算机，保持联网即可，不需要校园网
- 已在一卡通界面绑定电费、空调、水费的宿舍情况
- 抓包企业微信一卡通网页请求，或使用浏览器F12打开一卡通 H5 页面抓取 `cookies`、`bearer_token`

## 快速开始

### 方式一：docker部署 (或使用 docker compose)

构建docker镜像

`docker build -t elec_room_info:latest .`

创建运行目录

`mkdir project_dir && cd project_dir`

`mkdir data && cd data`

`mkdir configs && cd configs`

将配置文件 `sample_config.yaml` 重命名为 `config.yaml` 并放于`project_dir/data/configs`目录下（`sample_config.ini` 不被程序默认使用，请使用 `config.yaml`）

运行docker容器，替换容器映射路径

`docker compose build && docker compose up -d` 或 `docker run -v ./data:/app/data`

### 方式二：部署源代码

开发基于python 3.8，请使用python 3.8 版本。

`pip install -r requirement.txt`

生成默认配置文件，须编辑完善后方可正常运行：

`python3 elec_room_info/utils/config/config_omega.py`

运行程序

`python3 elec_room_info/main.py`

## 定时启动/暂停

由于接口可能有时效限制，所以建议手动设置 crontab 来定时启动/暂停容器
```
30 8 * * * docker start elec_room_info
55 23 * * * docker stop elec_room_info
```

## Config 文件

### 1. `addon` - 功能模块开关
| 参数                | 类型    | 说明                     | 默认值  |
|---------------------|---------|--------------------------|---------|
| `balance_monitor`   | boolean | 启用余额监控功能         | `true`  |
| `deposit_monitor`   | boolean | 启用充值监控功能         | `true`  |

---

### 2. `query` - 数据查询配置
| 参数            | 类型   | 说明                          | 必填  |
|-----------------|--------|-------------------------------|-------|
| `bearer_token`  | string | Bearer Token       | 是    |
| `auth_link`     | string | 认证 URL（暂被弃用）                  | 否    |
| `session_id`    | string | 会话 ID  （暂被弃用）                     | 否    |

---

### 3. `record_csv` - 数据记录配置
| 参数                | 类型   | 说明                          | 默认值       |
|---------------------|--------|-------------------------------|-------------|
| `csv_file_path`     | string | CSV 数据存储路径（相对路径）  | `../data/records/query_data.csv` |
| `query_interval`    | int    | 数据查询间隔（秒）            | `1200` (20分钟) |

---

### 4. `email` - 邮件通知配置
| 参数              | 类型    | 说明                          | 默认值               |
|-------------------|---------|-------------------------------|---------------------|
| `enable`          | boolean | 启用邮件通知功能              | `false`            |
| `sender_email`    | string  | 发件邮箱地址                  | `mail@example.com` |
| `sender_name`     | string  | 发件人名称                    | `root`             |
| `smtp_server`     | string  | SMTP 服务器地址               | `smtp.example.com` |
| `smtp_port`       | int     | SMTP 服务器端口               | `587`              |
| `smtp_user`       | string  | SMTP 登录用户名               | `mail@example.com` |
| `smtp_password`   | string  | SMTP 登录密码                 | `<passwd>`         |

---

### 5. `pushplus` - pushplus 微信推送配置 (详细参数请移步[官网文档](https://www.pushplus.plus/push2.html)了解)
| 参数            | 类型    | 说明                          | 示例值       |
|-----------------|---------|-------------------------------|-------------|
| `enable`        | boolean | 启用 PushPlus 推送            | `false`     |
| `token`         | string  | PushPlus 令牌（官网获取）     | `<token>`   |
| `topic`         | string  | 推送分组 ID（可选）           | 留空        |
| `channel`       | string  | 推送渠道（默认微信）          | `wechat`    |
| `max_attempts`  | int     | 失败重试次数                  | `3`         |

---

### 6. `wxpusher` - Wxpusher 微信推送配置
| 参数            | 类型    | 说明                          | 示例值       |
|-----------------|---------|-------------------------------|-------------|
| `enable`        | boolean | 启用 Wxpusher 推送            | `false`     |
| `spt  `         | string  | Wxpusher SPT 令牌（[获取链接](https://wxpusher.zjiecode.com/docs/#/?id=%e8%8e%b7%e5%8f%96spt)）     | `<spt>`   |
| `app_token`         | string  | Wxpusher APP 令牌（官网获取）     | `<app_token>`   |
| `topic_ids`         | list  | 主题 id（官网获取）     | `[12345]`   |
| `max_attempts`  | int     | 失败重试次数                  | `3`         |

---

### 7. `balance_monitor` - 余额监控配置
| 参数                          | 类型   | 说明                          | 示例值               |
|-------------------------------|--------|-------------------------------|---------------------|
| `to_emails`                   | string | 告警接收邮箱（若邮箱推送未启用将被忽略）                  | `mail@example.com` |
| `threshold.water_balance`     | int    | 水费余额告警阈值（单位：元）  | `5`                |
| `threshold.electricity_balance` | int  | 电费余额告警阈值（单位：元）  | `5`                |
| `threshold.air_conditioner_balance` | int | 空调余额告警阈值（单位：元） | `8`                |

---

## 注意事项
1. 暂不支持环境变量传参
2. 文件路径需确保程序有读写权限

--- 

## Todos

- [ ] 用电日报
- [ ] 剩余水电时间估计
- [ ] 后端api
- [ ] 提供微信小程序服务
- [ ] 大学城、五山校区适配
