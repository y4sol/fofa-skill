# FOFA Skill

> FOFA Network Asset Search Engine for OpenClaw/AgentSkills

## Overview

FOFA is a leading Cyberspace search engine in China. This skill provides a complete CLI tool for asset discovery, query, and statistics.

## Features

- Complete official API wrapper
- Asset query and statistics aggregation
- CVE/Product fingerprint quick lookup
- Batch processing support
- JSON/CSV export
- Zero dependencies (Python standard library only)

## Requirements

- Python 3.7+
- FOFA API Key

## Quick Start

### 1. Configure Authentication

```bash
export FOFA_EMAIL="your@email.com"
export FOFA_API_KEY="your-api-key"
```

### 2. Basic Usage

```bash
# Asset query
python fofa_query.py search "domain=example.com"

# Statistics
python fofa_query.py stats "port=3306" --field country

# CVE fingerprints
python fofa_query.py cve redis

# Account info
python fofa_query.py info
```

## Commands

### search - Asset Query

```bash
python fofa_query.py search <query> [options]

# Examples
python fofa_query.py search "domain=baidu.com"
python fofa_query.py search "port=3306" -s 1000
python fofa_query.py search "server=nginx" -o result.json
```

### stats - Statistics Aggregation

```bash
python fofa_query.py stats <query> --field <field>

# Available fields
# protocol, os, server, port, domain, country, province, city
```

### cve - CVE/Product Fingerprints

```bash
# List all fingerprints
python fofa_query.py cve --list

# Query specific product
python fofa_query.py cve redis
python fofa_query.py cve weblogic

# Query and execute search
python fofa_query.py cve redis --search
```

## Query Syntax

### Basic Syntax

| Syntax | Description | Example |
|--------|-------------|---------|
| `domain=` | Domain | `domain=baidu.com` |
| `host=` | Host | `host=192.168.1.1` |
| `ip=` | IP Range | `ip=1.1.1.0/24` |
| `port=` | Port | `port=3306` |
| `server=` | Server | `server=nginx` |
| `app=` | Application | `app=MySQL` |
| `title=` | Title | `title=login` |

### Combined Queries

```bash
# AND
python fofa_query.py search "domain=example.com AND port=80"

# OR
python fofa_query.py search "server=nginx OR server=apache"
```

## Python Usage

```python
from fofa_query import FOFA

fofa = FOFA()

# Query
result = fofa.search("domain=example.com", size=100)
print(result["results"])

# Statistics
stats = fofa.stats("port=3306", field="country")
print(stats)

# Count
count = fofa.count("domain=example.com")
print(count)
```

## Dependencies

This skill uses Python standard library only. No additional dependencies required.

## License

MIT
