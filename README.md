# FOFA Skill

> OpenClaw/AgentSkills 兼容的 FOFA 资产查询技能

## 简介

FOFA 是国内领先的网络空间资产搜索引擎,本 Skill 提供完整的 CLI 工具用于资产发现、查询和统计。

## 功能特性

- ✅ 官方 API 完整封装
- ✅ 资产查询与统计聚合
- ✅ CVE/产品特征快速查询
- ✅ 批量处理支持
- ✅ JSON/CSV 导出
- ✅ 零依赖 (仅 Python 标准库)

## 环境要求

- Python 3.7+
- FOFA API 密钥

## 快速开始

### 1. 配置认证

```bash
export FOFA_EMAIL="your@email.com"
export FOFA_API_KEY="your-api-key"
```

### 2. 基本使用

```bash
# 资产查询
python fofa_query.py search "domain=example.com"

# 统计聚合
python fofa_query.py stats "port=3306" --field country

# CVE 特征
python fofa_query.py cve redis

# 账号信息
python fofa_query.py info
```

## 命令详解

### search - 资产查询

```bash
python fofa_query.py search <query> [options]

# 示例
python fofa_query.py search "domain=baidu.com"
python fofa_query.py search "port=3306" -s 1000
python fofa_query.py search "server=nginx" -o result.json
```

### stats - 统计聚合

```bash
python fofa_query.py stats <query> --field <field>

# 可用字段
# protocol, os, server, port, domain, country, province, city
```

### cve - CVE/产品特征

```bash
# 列出所有特征
python fofa_query.py cve --list

# 查询特定产品
python fofa_query.py cve redis
python fofa_query.py cve weblogic

# 查询并执行搜索
python fofa_query.py cve redis --search
```

## 查询语法

### 基础语法

| 语法 | 说明 | 示例 |
|------|------|------|
| `domain=` | 域名 | `domain=baidu.com` |
| `host=` | 主机 | `host=192.168.1.1` |
| `ip=` | IP 范围 | `ip=1.1.1.0/24` |
| `port=` | 端口 | `port=3306` |
| `server=` | 服务器 | `server=nginx` |
| `app=` | 应用 | `app=MySQL` |
| `title=` | 标题 | `title=后台` |

### 组合查询

```bash
# AND
python fofa_query.py search "domain=example.com AND port=80"

# OR
python fofa_query.py search "server=nginx OR server=apache"
```

## Python 调用

```python
from fofa_query import FOFA

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

## 依赖

本技能使用 Python 标准库,无需额外安装依赖。

## 许可证

MIT
