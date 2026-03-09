# FOFA Skill 🔍

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/)

*阅读其他语言: [English](README.md)*

FOFA（Fingerprinting Organization with Advanced Research）网络资产搜索引擎的命令行工具，为安全专业人员提供强大的网络资产搜索能力。

## 概述

FOFA 是一个商业网络资产搜索引擎，帮助安全研究人员发现、枚举和分析互联网暴露的系统。本工具提供查询 FOFA API 的综合 CLI 接口。

### 什么是 FOFA？

FOFA（Fingerprinting Organization with Advanced Research）是一个网络空间资产搜索引擎，能够：

- 收集和索引互联网暴露的设备
- 提供高级搜索功能
- 支持漏洞研究
- 实现攻击面映射

## 功能特性

### 核心能力

| 功能 | 描述 |
|------|------|
| 资产搜索 | 通过关键词、端口、协议查找目标 |
| CVE 搜索 | 按 CVE ID 搜索漏洞 |
| 主机分析 | 获取详细主机信息 |
| 攻击面 | 绘制组织攻击面 |
| 多格式输出 | JSON、CSV、表格 |
| 批量处理 | 处理多个查询 |

### 支持的查询类型

- **基于域名**：`domain=example.com`
- **基于 IP**：`ip=1.1.1.1`
- **CIDR 表示法**：`ip=192.168.1.0/24`
- **基于端口**：`port=8080`
- **协议识别**：`protocol=http`
- **漏洞搜索**：`cve:CVE-2021-44228`
- **SSL 证书**：`cert=example.com`
- **地理位置**：`country=CN`、`region=Beijing`、`city=Shanghai`
- **组织**：`org=Alibaba`、`org=Tencent`
- **基于产品**：`app=nginx`、`app=Apache`
- **操作系统检测**：`os=Linux`、`os=Windows`

## 安装

### 前置条件

- Python 3.8 或更高版本
- FOFA API 账户（免费或付费）

### 获取 FOFA API 凭据

1. 在 [fofa.info](https://fofa.info) 注册
2. 转到"我的信息"→"API"
3. 复制您的邮箱和 API 密钥

### 安装步骤

```bash
# 克隆仓库
git clone https://github.com/y4sol/fofa-skill.git
cd fofa-skill

# 安装依赖
pip install -r requirements.txt

# 配置环境变量
export FOFA_EMAIL="your@email.com"
export FOFA_API_KEY="your_api_key"

# 验证配置
python scripts/fofa_cli.py info
```

## 使用方法

### 基本命令

```bash
# 查看帮助
python scripts/fofa_cli.py --help

# 查看账户信息
python scripts/fofa_cli.py info
```

### 搜索命令

```bash
# 基础资产搜索
python scripts/fofa_cli.py search "domain=example.com"

# 带过滤条件的搜索
python scripts/fofa_cli.py search "port=443 && country=US"

# 限制结果数量（默认：100）
python scripts/fofa_cli.py search "keyword" --limit 500

# 输出到文件
python scripts/fofa_cli.py search "keyword" --output results.json

# 不同的输出格式
python scripts/fofa_cli.py search "keyword" --format json
python scripts/fofa_cli.py search "keyword" --format csv
python scripts/fofa_cli.py search "keyword" --format table
```

### CVE 搜索

```bash
# 按 CVE 搜索存在漏洞的目标
python scripts/fofa_cli.py cve log4j
python scripts/fofa_cli.py cve CVE-2021-44228
python scripts/fofa_cli.py cve CVE-2019-0708

# 按漏洞名称搜索
python scripts/fofa_cli.py cve redis-unauth
python scripts/fofa_cli.py cve mysql-unauth
python scripts/fofa_cli.py cve docker-api-unauth

# 详细输出
python scripts/fofa_cli.py cve log4j --verbose
```

### 统计

```bash
# 统计结果数量
python scripts/fofa_cli.py count "port=3306"
python scripts/fofa_cli.py count "country=US && port=22"

# 获取主机详细信息
python scripts/fofa_cli.py host 1.1.1.1
python scripts/fofa_cli.py host 8.8.8.8 --verbose
```

### 分页

```bash
# 获取第一页
python scripts/fofa_cli.py search "keyword" --page 1

# 获取指定页面
python scripts/fofa_cli.py search "keyword" --page 5
```

## 查询语法

### 基本运算符

| 运算符 | 描述 | 示例 |
|----------|-------------|---------|
| `=` | 等于 | `domain=example.com` |
| `==` | 精确匹配 | `ip==1.1.1.1` |
| `&&` | 与 | `port=80 && country=US` |
| `\|\|` | 或 | `org=Google \|\| org=Microsoft` |
| `!=` | 不等于 | `country!=CN` |
| `()` | 分组 | `(port=80 \|\| port=443) && country=US` |

### 字段参考

| 字段 | 类型 | 描述 | 示例 |
|-------|------|-------------|---------|
| `domain` | 字符串 | 域名 | `domain=example.com` |
| `ip` | IP/CIDR | IP 地址或范围 | `ip=192.168.1.0/24` |
| `port` | 整数 | 端口号 | `port=8080` |
| `protocol` | 字符串 | 协议名称 | `protocol=http` |
| `country` | 字符串 | 国家代码 | `country=CN` |
| `region` | 字符串 | 地区名称 | `region=Beijing` |
| `city` | 字符串 | 城市名称 | `city=Shanghai` |
| `org` | 字符串 | 组织 | `org=Alibaba` |
| `cert` | 字符串 | SSL 证书 | `cert=example.com` |
| `title` | 字符串 | 页面标题 | `title=login` |
| `header` | 字符串 | HTTP 头 | `header=server` |
| `body` | 字符串 | 页面内容 | `body=password` |
| `app` | 字符串 | 应用程序 | `app=nginx` |
| `os` | 字符串 | 操作系统 | `os=Linux` |
| `vuln` | 字符串 | 漏洞 | `vuln=CVE-2021-44228` |

### 搜索示例

#### 查找所有 HTTPS 服务

```bash
python scripts/fofa_cli.py search "port=443 && protocol=https"
```

#### 查找 Redis 实例

```bash
python scripts/fofa_cli.py search "port=6379"
```

#### 查找 Docker API

```bash
python scripts/fofa_cli.py search '"Docker" && port=2375'
```

#### 查找 Jenkins 服务器

```bash
python scripts/fofa_cli.py search '"Jenkins" && port=8080'
```

#### 查找 Log4j 漏洞服务器

```bash
python scripts/fofa_cli.py cve log4j
```

#### 查找 VPN 服务

```bash
python scripts/fofa_cli.py search "port=1194 || port=1723"
```

#### 查找 IoT 设备

```bash
python scripts/fofa_cli.py search "app=GoAhead && country=US"
```

## 配置

### 环境变量

```bash
# 必需
export FOFA_EMAIL="your@email.com"
export FOFA_API_KEY="your_api_key"

# 可选
export FOFA_SIZE=100
export FOFA_FORMAT="json"
```

### 配置文件

编辑 `config/config.json`:

```json
{
  "fofa": {
    "email": "${FOFA_EMAIL}",
    "key": "${FOFA_API_KEY}",
    "size": 100,
    "format": "json",
    "timeout": 30
  },
  "output": {
    "default_format": "table",
    "color": true,
    "quiet": false
  },
  "search": {
    "default_limit": 100,
    "max_limit": 10000
  }
}
```

## 输出格式

### JSON 输出

```bash
python scripts/fofa_cli.py search "keyword" --format json
```

```json
{
  "results": [
    {
      "ip": "1.1.1.1",
      "port": 443,
      "protocol": "https",
      "domain": "example.com",
      "country": "US",
      "org": "Cloudflare"
    }
  ],
  "count": 100
}
```

### CSV 输出

```bash
python scripts/fofa_cli.py search "keyword" --format csv --output results.csv
```

### 表格输出（默认）

```
+--------+-------------+-------+----------+----------+
| IP          | Port | Protocol | Domain        | Country |
+-------------+------+---------+---------------+---------+
| 1.1.1.1    | 443  | https   | example.com   | US      |
| 1.1.1.2    | 80   | http    | test.com      | CN      |
+-------------+------+---------+---------------+---------+
```

## 速率限制

| 级别 | 每日查询 | 速率 |
|------|---------------|------|
| 免费 | 100 | 1 请求/秒 |
| VIP1 | 10,000 | 10 请求/秒 |
| VIP2 | 100,000 | 50 请求/秒 |
| VIP3 | 无限 | 100 请求/秒 |

### 处理速率限制

```python
# 自动重试
import time

def query_with_retry(query, max_retries=3):
    for i in range(max_retries):
        try:
            result = fofa.search(query)
            return result
        except RateLimitError:
            wait = 2 ** i
            print(f"速率受限，等待 {wait}秒...")
            time.sleep(wait)
```

## 使用示例

### 完整工作流程

```bash
# 1. 检查账户配额
python scripts/fofa_cli.py info

# 2. 搜索目标
python scripts/fofa_cli.py search "port=3306" --limit 1000

# 3. 分析特定主机
python scripts/fofa_cli.py host 192.168.1.1

# 4. 导出结果
python scripts/fofa_cli.py search "domain=target.com" --format csv --output targets.csv
```

### 安全评估

```bash
# 查找暴露的数据库
python scripts/fofa_cli.py search "port=27017 || port=5432 || port=3306"

# 查找 Log4j 漏洞
python scripts/fofa_cli.py cve log4j

# 查找过期证书
python scripts/fofa_cli.py search "certIssuer=Let's Encrypt" --format json
```

## 目录结构

```
fofa-skill/
├── scripts/
│   └── fofa_cli.py           # 主 CLI 工具
├── config/
│   └── config.json           # 配置文件
├── tests/
│   ├── test_fofa.py          # 单元测试
│   └── __init__.py
├── SKILL.md                   # Skill 文档
├── API.md                     # API 参考
├── CONTRIBUTING.md            # 贡献指南
├── README.md                  # English version
├── README_zh-CN.md           # 中文版本
├── requirements.txt           # 依赖
└── .gitignore                # Git 忽略规则
```

## 故障排除

### 认证错误

```bash
# 验证凭据
python scripts/fofa_cli.py info

# 检查环境变量
echo $FOFA_EMAIL
echo $FOFA_API_KEY
```

### 无结果

- 检查查询语法
- 尝试更宽泛的搜索词
- 确认 API 密钥有剩余配额
- 尝试不同的关键词

### 连接错误

```bash
# 检查网络
ping fofa.info

# 检查 API 状态
curl -s "https://fofa.info/api/v1/info/my_info"
```

### 速率限制错误

```bash
# 等待后重试
sleep 60
python scripts/fofa_cli.py search "keyword"
```

## 开发

### 运行测试

```bash
pytest tests/
```

### 添加新命令

1. 编辑 `scripts/fofa_cli.py`
2. 添加 argparse 子命令
3. 实现逻辑
4. 添加测试

## 许可证

MIT 许可证 - 详见 [LICENSE](LICENSE)。
