---
name: fofa
description: Use FOFA network asset search engine for asset discovery and queries. Use when: (1) domain-related asset queries (2) port/service statistics (3) CVE vulnerability asset mapping (4) enterprise attack surface assessment
metadata: {"openclaw": {"requires": {"env": ["FOFA_EMAIL", "FOFA_API_KEY"]}, "emoji": "🔍"}}
---

# FOFA Asset Query

FOFA is a leading Cyberspace search engine in China, providing complete RESTful API for asset discovery.

## Environment Setup

```bash
# Configure authentication
export FOFA_EMAIL="your@email.com"
export FOFA_API_KEY="your-api-key"
```

## Usage

### Command Line

```bash
python {baseDir}/scripts/fofa_query.py search "domain=example.com"
python {baseDir}/scripts/fofa_query.py stats "port=3306" --field country
python {baseDir}/scripts/fofa_query.py cve redis
python {baseDir}/scripts/fofa_query.py info
```

### Python Import

```python
import sys
sys.path.insert(0, "{baseDir}/scripts")
from fofa_query import FOFA

fofa = FOFA()
result = fofa.search("domain=example.com", size=100)
```

## Commands

| Command | Description |
|---------|-------------|
| `search` | Asset query |
| `host` | Host query |
| `hosts` | Batch query |
| `stats` | Statistics aggregation |
| `count` | Result count |
| `info` | Account info |
| `products` | Product list |
| `cve` | CVE/Product fingerprints |

## Query Syntax

| Syntax | Description | Example |
|--------|-------------|---------|
| `domain=` | Domain | `domain=baidu.com` |
| `port=` | Port | `port=3306` |
| `server=` | Server | `server=nginx` |
| `app=` | Application | `app=MySQL` |
| `title=` | Title | `title=login` |

## Supported Products

- **Database**: MySQL, PostgreSQL, MongoDB, Redis, ElasticSearch
- **Middleware**: WebLogic, Tomcat, JBoss
- **Framework**: Spring, Struts2, Django, Shiro, Fastjson
- **DevOps**: Jenkins, GitLab, Nexus, Jira, Zabbix
- **Cloud Native**: Docker, Kubernetes, MinIO

## Notes

1. API limit: Free tier has daily quota
2. Max results: 10000 per request
3. Use only for authorized security testing
