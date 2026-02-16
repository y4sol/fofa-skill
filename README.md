# FOFA API 客户端

> FOFA 网络空间资产搜索引擎 Python CLI 工具

## 功能特性

- ✅ 官方 API 完整封装
- ✅ 资产查询与统计聚合
- ✅ CVE/产品特征快速查询
- ✅ 批量处理支持
- ✅ JSON/CSV 导出
- ✅ 零依赖 (仅 Python 标准库)

## 环境要求

- Python 3.7+
- 无需额外安装依赖

## 快速开始

### 1. 配置认证

方式一: 环境变量 (推荐)
```bash
export FOFA_EMAIL="your@email.com"
export FOFA_API_KEY="your-api-key"
```

方式二: 单一变量 (email:key 格式)
```bash
export FOFA_TOKEN="your@email.com:your-api-key"
```

方式三: 命令行参数
```bash
python fofa.py search "domain=example.com" -e your@email.com -k your-api-key
```

### 2. 基本使用

```bash
# 资产查询
python fofa.py search "domain=example.com"

# 统计聚合
python fofa.py stats "port=3306" --field country

# 数量查询
python fofa.py count "domain=target.com"

# 账号信息
python fofa.py info
```

## 命令详解

### search - 资产查询

```bash
python fofa.py search <query> [options]

# 示例
python fofa.py search "domain=baidu.com"
python fofa.py search "port=3306" -s 1000 -p 1
python fofa.py search "server=nginx" -f "host,ip,port,title" -o result.json
python fofa.py search "app=MySQL" -c result.csv
```

| 参数 | 简写 | 说明 |
|------|------|------|
| `--size` | `-s` | 返回数量 (默认 100) |
| `--page` | `-p` | 页码 (默认 1) |
| `--fields` | `-f` | 返回字段 |
| `--limit` | `-l` | 显示数量 (默认 10) |
| `--output` | `-o` | JSON 输出文件 |
| `--csv` | `-c` | CSV 输出文件 |

### stats - 统计聚合

```bash
python fofa.py stats <query> [options]

# 示例
python fofa.py stats "domain=example.com" --field protocol
python fofa.py stats "port=3306" --field country
python fofa.py stats "port=6379" --field server
```

可用字段: `protocol`, `os`, `server`, `port`, `domain`, `country`, `province`, `city`

### host - Host 查询

```bash
# IP 资产查询
python fofa.py host 1.1.1.1

# 域名资产查询
python fofa.py host example.com
```

### hosts - 批量查询

```bash
python fofa.py hosts 1.1.1.1 8.8.8.8 114.114.114.114
python fofa.py hosts 1.1.1.1 8.8.8.8 --simple
```

### count - 数量查询

```bash
python fofa.py count "domain=target.com"
```

### cve - CVE/产品特征

```bash
# 列出所有特征
python fofa.py cve --list

# 查询特定产品
python fofa.py cve redis
python fofa.py cve weblogic
python fofa.py cve mysql

# 查询并执行 FOFA 搜索
python fofa.py cve redis --search -s 20
```

### info - 账号信息

```bash
python fofa.py info
```

### products - 产品列表

```bash
python fofa.py products
```

## 查询语法

### 基础语法

| 语法 | 说明 | 示例 |
|------|------|------|
| `domain=` | 域名 | `domain=baidu.com` |
| `host=` | 主机 | `host=192.168.1.1` |
| `ip=` | IP 范围 | `ip=1.1.1.0/24` |
| `port=` | 端口 | `port=3306` |
| `protocol=` | 协议 | `protocol=http` |
| `server=` | 服务器 | `server=nginx` |
| `app=` | 应用 | `app=MySQL` |
| `title=` | 标题 | `title=后台` |
| `header=` | HTTP 头 | `header=X-Powered-By` |
| `body=` | 页面内容 | `body=password` |

### 组合查询

```bash
# AND (默认)
python fofa.py search "domain=example.com AND port=80"

# OR
python fofa.py search "server=nginx OR server=apache"

# 复杂条件
python fofa.py search "domain=target.com AND (port=80 OR port=443)"
```

## 返回字段

常用字段: `host,ip,port,protocol,server,title,domain,os,asn,country,province,city`

完整字段请参考 [FOFA 官方文档](https://fofa.info/api)。

## Python 调用

```python
from fofa import FOFA

# 初始化
fofa = FOFA()

# 查询
result = fofa.search("domain=example.com", size=100)
print(result["results"])

# 统计
stats = fofa.stats("port=3306", field="country")
print(stats)

# 数量
count = fofa.count("domain=example.com")
print(count)
```

## 支持的产品特征

| 分类 | 产品 |
|------|------|
| 中间件 | WebLogic, Tomcat, JBoss, WebSphere |
| Web 服务器 | Nginx, Apache, IIS |
| 框架 | Spring, Struts2, Django, Flask, Shiro, Fastjson |
| 数据库 | MySQL, PostgreSQL, MongoDB, Redis, ElasticSearch |
| 缓存/消息 | RabbitMQ, Kafka, ActiveMQ |
| 运维工具 | Jenkins, GitLab, Nexus, Jira, Zabbix, Grafana |
| 云原生 | Docker, Kubernetes, MinIO, Harbor |

## 注意事项

1. **API 限制**: 免费会员每日有限额
2. **结果数量**: 单次最大 10000 条
3. **合规使用**: 仅限授权的安全测试和资产梳理

## License

MIT
