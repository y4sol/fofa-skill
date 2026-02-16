# FOFA Skill

> FOFA Network Asset Search Engine for OpenClaw/AgentSkills

## Overview

FOFA is a leading Cyberspace search engine in China. This skill provides CLI access to official FOFA API.

## API Endpoints (5)

| Endpoint | Description |
|----------|-------------|
| `/api/v1/search/all` | Asset query |
| `/api/v1/search/stats` | Statistics (VIP only) |
| `/api/v1/host/{host}` | Host aggregation (VIP only) |
| `/api/v1/info/my` | Account info |
| `/api/v1/search/next` | Pagination |

## Requirements

- Python 3.7+
- FOFA API Key

## Authentication

```bash
# Only need API Key (email not required)
export FOFA_API_KEY="your-api-key"

# Or use token format
export FOFA_TOKEN="email:key"
```

## Usage

```bash
# Search
python fofa_query.py search "domain=example.com"

# Statistics (VIP)
python fofa_query.py stats "port=3306" --field country

# Host aggregation (VIP)
python fofa_query.py host 1.1.1.1

# Account info
python fofa_query.py info

# Pagination
python fofa_query.py next <last_id>

# Count
python fofa_query.py count "domain=example.com"
```

## Python Usage

```python
from fofa_query import FOFA

fofa = FOFA()

# Search
result = fofa.search("domain=example.com", size=100)
print(result["results"])

# Info
result = fofa.info()

# Count
count = fofa.count("domain=example.com")
```

## License

MIT
