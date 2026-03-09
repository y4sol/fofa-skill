# FOFA Skill 🔍

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/)

*Read this in other languages: [中文](README_zh-CN.md)*

A command-line interface for FOFA (Fingerprinting Organization with Advanced Research), a powerful network asset search engine for security professionals.

## Overview

FOFA is a commercial network asset search engine that helps security researchers discover, enumerate, and analyze internet-facing systems. This tool provides a comprehensive CLI interface for querying the FOFA API.

### What is FOFA?

FOFA (Fingerprinting Organization with Advanced Research) is a network space asset search engine that:

- Collects and indexes internet-facing devices
- Provides advanced search capabilities
- Supports vulnerability research
- Enables attack surface mapping

## Features

### Core Capabilities

| Feature | Description |
|---------|-------------|
| Asset Search | Find targets by keywords, ports, protocols |
| CVE Search | Search vulnerabilities by CVE ID |
| Host Analysis | Get detailed host information |
| Attack Surface | Map organization attack surface |
| Multiple Formats | JSON, CSV, table output |
| Batch Processing | Process multiple queries |

### Supported Query Types

- **Domain-based**: `domain=example.com`
- **IP-based**: `ip=1.1.1.1`
- **CIDR notation**: `ip=192.168.1.0/24`
- **Port-based**: `port=8080`
- **Protocol identification**: `protocol=http`
- **Vulnerability search**: `cve:CVE-2021-44228`
- **SSL certificate**: `cert=example.com`
- **Geographic**: `country=CN`, `region=Beijing`, `city=Shanghai`
- **Organization**: `org=Alibaba`, `org=Tencent`
- **Product-based**: `app=nginx`, `app=Apache`
- **OS detection**: `os=Linux`, `os=Windows`

## Installation

### Prerequisites

- Python 3.8 or higher
- FOFA API account (free or paid)

### Get FOFA API Credentials

1. Register at [fofa.info](https://fofa.info)
2. Go to "My Info" → "API"
3. Copy your email and API key

### Setup

```bash
# Clone repository
git clone https://github.com/y4sol/fofa-skill.git
cd fofa-skill

# Install dependencies
pip install -r requirements.txt

# Configure environment variables
export FOFA_EMAIL="your@email.com"
export FOFA_API_KEY="your_api_key"

# Verify configuration
python scripts/fofa_cli.py info
```

## Usage

### Basic Commands

```bash
# View help
python scripts/fofa_cli.py --help

# Check account info
python scripts/fofa_cli.py info
```

### Search Commands

```bash
# Basic asset search
python scripts/fofa_cli.py search "domain=example.com"

# Search with filters
python scripts/fofa_cli.py search "port=443 && country=US"

# Limit results (default: 100)
python scripts/fofa_cli.py search "keyword" --limit 500

# Output to file
python scripts/fofa_cli.py search "keyword" --output results.json

# Different output formats
python scripts/fofa_cli.py search "keyword" --format json
python scripts/fofa_cli.py search "keyword" --format csv
python scripts/fofa_cli.py search "keyword" --format table
```

### CVE Search

```bash
# Search for vulnerable targets by CVE
python scripts/fofa_cli.py cve log4j
python scripts/fofa_cli.py cve CVE-2021-44228
python scripts/fofa_cli.py cve CVE-2019-0708

# Search by vulnerability name
python scripts/fofa_cli.py cve redis-unauth
python scripts/fofa_cli.py cve mysql-unauth
python scripts/fofa_cli.py cve docker-api-unauth

# Verbose output
python scripts/fofa_cli.py cve log4j --verbose
```

### Statistics

```bash
# Count results
python scripts/fofa_cli.py count "port=3306"
python scripts/fofa_cli.py count "country=US && port=22"

# Get host details
python scripts/fofa_cli.py host 1.1.1.1
python scripts/fofa_cli.py host 8.8.8.8 --verbose
```

### Pagination

```bash
# Get first page
python scripts/fofa_cli.py search "keyword" --page 1

# Get specific page
python scripts/fofa_cli.py search "keyword" --page 5
```

## Query Syntax

### Basic Operators

| Operator | Description | Example |
|----------|-------------|---------|
| `=` | Equals | `domain=example.com` |
| `==` | Exact match | `ip==1.1.1.1` |
| `&&` | AND | `port=80 && country=US` |
| `\|\|` | OR | `org=Google \|\| org=Microsoft` |
| `!=` | Not equal | `country!=CN` |
| `()` | Grouping | `(port=80 \|\| port=443) && country=US` |

### Field Reference

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `domain` | String | Domain name | `domain=example.com` |
| `ip` | IP/CIDR | IP address or range | `ip=192.168.1.0/24` |
| `port` | Integer | Port number | `port=8080` |
| `protocol` | String | Protocol name | `protocol=http` |
| `country` | String | Country code | `country=CN` |
| `region` | String | Region name | `region=Beijing` |
| `city` | String | City name | `city=Shanghai` |
| `org` | String | Organization | `org=Alibaba` |
| `cert` | String | SSL certificate | `cert=example.com` |
| `title` | String | Page title | `title=login` |
| `header` | String | HTTP header | `header=server` |
| `body` | String | Page content | `body=password` |
| `app` | String | Application | `app=nginx` |
| `os` | String | Operating system | `os=Linux` |
| `vuln` | String | Vulnerability | `vuln=CVE-2021-44228` |

### Search Examples

#### Find All HTTPS Services

```bash
python scripts/fofa_cli.py search "port=443 && protocol=https"
```

#### Find Redis Instances

```bash
python scripts/fofa_cli.py search "port=6379"
```

#### Find Docker APIs

```bash
python scripts/fofa_cli.py search '"Docker" && port=2375'
```

#### Find Jenkins Servers

```bash
python scripts/fofa_cli.py search '"Jenkins" && port=8080'
```

#### Find Log4j Vulnerable Servers

```bash
python scripts/fofa_cli.py cve log4j
```

#### Find VPN Services

```bash
python scripts/fofa_cli.py search "port=1194 || port=1723"
```

#### Find IoT Devices

```bash
python scripts/fofa_cli.py search "app=GoAhead && country=US"
```

## Configuration

### Environment Variables

```bash
# Required
export FOFA_EMAIL="your@email.com"
export FOFA_API_KEY="your_api_key"

# Optional
export FOFA_SIZE=100
export FOFA_FORMAT="json"
```

### Config File

Edit `config/config.json`:

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

## Output Formats

### JSON Output

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

### CSV Output

```bash
python scripts/fofa_cli.py search "keyword" --format csv --output results.csv
```

### Table Output (Default)

```
+--------+-------------+-------+----------+----------+
| IP          | Port | Protocol | Domain        | Country |
+-------------+------+---------+---------------+---------+
| 1.1.1.1    | 443  | https   | example.com   | US      |
| 1.1.1.2    | 80   | http    | test.com      | CN      |
+-------------+------+---------+---------------+---------+
```

## Rate Limits

| Tier | Daily Queries | Rate |
|------|---------------|------|
| Free | 100 | 1 req/sec |
| VIP1 | 10,000 | 10 req/sec |
| VIP2 | 100,000 | 50 req/sec |
| VIP3 | Unlimited | 100 req/sec |

### Handle Rate Limits

```python
# Automatic retry
import time

def query_with_retry(query, max_retries=3):
    for i in range(max_retries):
        try:
            result = fofa.search(query)
            return result
        except RateLimitError:
            wait = 2 ** i
            print(f"Rate limited, waiting {wait}s...")
            time.sleep(wait)
```

## Examples

### Complete Workflow

```bash
# 1. Check account quota
python scripts/fofa_cli.py info

# 2. Search for targets
python scripts/fofa_cli.py search "port=3306" --limit 1000

# 3. Analyze specific host
python scripts/fofa_cli.py host 192.168.1.1

# 4. Export results
python scripts/fofa_cli.py search "domain=target.com" --format csv --output targets.csv
```

### Security Assessment

```bash
# Find exposed databases
python scripts/fofa_cli.py search "port=27017 || port=5432 || port=3306"

# Find vulnerable Log4j
python scripts/fofa_cli.py cve log4j

# Find expired certificates
python scripts/fofa_cli.py search "certIssuer=Let's Encrypt" --format json
```

## Directory Structure

```
fofa-skill/
├── scripts/
│   └── fofa_cli.py           # Main CLI tool
├── config/
│   └── config.json           # Configuration
├── tests/
│   ├── test_fofa.py          # Unit tests
│   └── __init__.py
├── SKILL.md                  # Skill documentation
├── API.md                   # API reference
├── CONTRIBUTING.md          # Contribution guidelines
├── README.md                 # English version
├── README_zh-CN.md          # 中文版本
├── requirements.txt         # Dependencies
└── .gitignore               # Git ignore rules
```

## Troubleshooting

### Authentication Errors

```bash
# Verify credentials
python scripts/fofa_cli.py info

# Check environment variables
echo $FOFA_EMAIL
echo $FOFA_API_KEY
```

### No Results

- Check query syntax
- Try broader search terms
- Verify API key has remaining quota
- Try different keywords

### Connection Errors

```bash
# Check network
ping fofa.info

# Check API status
curl -s "https://fofa.info/api/v1/info/my_info"
```

### Rate Limit Errors

```bash
# Wait and retry
sleep 60
python scripts/fofa_cli.py search "keyword"
```

## Development

### Run Tests

```bash
pytest tests/
```

### Add New Commands

1. Edit `scripts/fofa_cli.py`
2. Add argparse subcommand
3. Implement logic
4. Add tests

## License

MIT License - see [LICENSE](LICENSE) for details.
