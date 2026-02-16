# FOFA Skill

> FOFA Network Asset Search Engine for OpenClaw/AgentSkills

## Overview

FOFA is a leading Cyberspace search engine in China. This skill provides CLI access to official FOFA API.

## API Endpoints (Only 5)

| Endpoint | Description |
|----------|-------------|
| `/api/v1/search/all` | Asset query |
| `/api/v1/search/stats` | Statistics (VIP only) |
| `/api/v1/host/{host}` | Host aggregation |
| `/api/v1/info/my` | Account info |
| `/api/v1/search/next` | Pagination |

## Requirements

- Python 3.7+
- FOFA API Key

## Authentication

```bash
export FOFA_EMAIL="your@email.com"
export FOFA_API_KEY="your-api-key"

# Or use single token
export FOFA_TOKEN="email:key"
```

## Usage

```bash
# Search
python fofa_query.py search "domain=example.com"

# Statistics (VIP)
python fofa_query.py stats "port=3306" --field country

# Host aggregation
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

# Stats
result = fofa.stats("port=3306", field="country")

# Host
result = fofa.host("1.1.1.1")

# Info
result = fofa.info()

# Count
count = fofa.count("domain=example.com")
```

## License

MIT
