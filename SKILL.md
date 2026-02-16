---
name: fofa
description: 使用 FOFA 网络空间资产搜索引擎进行资产发现和查询。适用于: (1) 域名相关资产查询 (2) 端口/服务统计 (3) CVE 漏洞资产定位 (4) 企业攻击面评估
metadata: {"openclaw": {"requires": {"env": ["FOFA_EMAIL", "FOFA_API_KEY"]}, "emoji": "🔍"}}
---

# FOFA 资产查询

FOFA 是国内领先的网络空间资产搜索引擎,提供完整的 RESTful API。

## 环境设置

```bash
# 配置认证
export FOFA_EMAIL="your@email.com"
export FOFA_API_KEY="your-api-key"
```

## 使用方法

### 命令行

```bash
python {baseDir}/scripts/fofa_query.py search "domain=example.com"
python {baseDir}/scripts/fofa_query.py stats "port=3306" --field country
python {baseDir}/scripts/fofa_query.py cve redis
python {baseDir}/scripts/fofa_query.py info
```

### Python 调用

```python
import sys
sys.path.insert(0, "{baseDir}/scripts")
from fofa_query import FOFA

fofa = FOFA()
result = fofa.search("domain=example.com", size=100)
```

## 命令列表

| 命令 | 功能 |
|------|------|
| `search` | 资产查询 |
| `host` | Host 查询 |
| `hosts` | 批量查询 |
| `stats` | 统计聚合 |
| `count` | 结果数量 |
| `info` | 账号信息 |
| `products` | 产品列表 |
| `cve` | CVE/产品特征 |

## 查询语法

| 语法 | 说明 | 示例 |
|------|------|------|
| `domain=` | 域名 | `domain=baidu.com` |
| `port=` | 端口 | `port=3306` |
| `server=` | 服务器 | `server=nginx` |
| `app=` | 应用 | `app=MySQL` |
| `title=` | 标题 | `title=后台` |

## 支持的产品特征

- **数据库**: MySQL, PostgreSQL, MongoDB, Redis, ElasticSearch
- **中间件**: WebLogic, Tomcat, JBoss
- **框架**: Spring, Struts2, Django, Shiro, Fastjson
- **运维**: Jenkins, GitLab, Nexus, Jira, Zabbix
- **云原生**: Docker, Kubernetes, MinIO

## 注意事项

1. API 限制: 免费会员每日有限额
2. 结果数量: 单次最大 10000 条
3. 合规使用: 仅限授权的安全测试
