---
name: fofa
description: |
  使用 FOFA 官方 API 进行网络空间资产发现、查询和统计。适用于:
  (1) 域名相关资产查询
  (2) IP/主机资产获取
  (3) 端口/服务统计分析
  (4) CVE 漏洞资产快速定位
  (5) 企业攻击面评估
---

# FOFA 资产查询

FOFA 是国内领先的网络空间资产搜索引擎,提供完整的 RESTful API。

## 环境设置

```bash
# 配置认证 (二选一)
export FOFA_EMAIL="your@email.com"
export FOFA_API_KEY="your-api-key"

# 或
export FOFA_TOKEN="your@email.com:your-api-key"
```

## 命令行用法

```bash
# 资产查询
python scripts/fofa_query.py search "domain=example.com"

# 统计聚合
python scripts/fofa_query.py stats "port=3306" --field country

# 数量查询
python scripts/fofa_query.py count "domain=target.com"

# CVE/产品特征
python scripts/fofa_query.py cve redis
python scripts/fofa_query.py cve --list

# 账号信息
python scripts/fofa_query.py info
```

## 官方 API 接口

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

| 语法 | 说明 |
|------|------|
| `domain=` | 域名 |
| `host=` | 主机 |
| `ip=` | IP 范围 |
| `port=` | 端口 |
| `server=` | 服务器 |
| `app=` | 应用 |

## Python 调用

```python
from scripts.fofa_query import FOFA

fofa = FOFA()
result = fofa.search("domain=example.com", size=100)
print(result["results"])
```

## 注意事项

1. API 限制: 免费会员每日有限额
2. 结果数量: 单次最大 10000 条
3. 合规使用: 仅限授权的安全测试
