---
name: fofa
description: Use FOFA network asset search engine for asset discovery and queries. Use when performing domain-related asset queries, port/service statistics, CVE vulnerability asset mapping or enterprise attack surface assessment.
metadata: {"openclaw": {"requires": {"env": ["FOFA_EMAIL", "FOFA_API_KEY"]}, "emoji": "🔍"}}
---

# FOFA Asset Query

FOFA is a leading Cyberspace search engine in China, providing complete RESTful API for asset discovery.

## Environment Setup

```bash
export FOFA_EMAIL="your@email.com"
export FOFA_API_KEY="your-api-key"
```

## Usage

```bash
python {baseDir}/scripts/fofa_query.py search "domain=example.com"
python {baseDir}/scripts/fofa_query.py stats "port=3306" --field country
python {baseDir}/scripts/fofa_query.py cve redis
python {baseDir}/scripts/fofa_query.py info
```

## Commands

| Command | Description |
|---------|-------------|
| search | Asset query |
| host | Host query |
| hosts | Batch query |
| stats | Statistics aggregation (requires VIP) |
| count | Result count |
| info | Account info |
| cve | CVE/Product fingerprints |

## Notes

- API limit: Free tier has daily quota
- Max results: 10000 per request
- stats requires VIP membership
- Use only for authorized security testing
