# FOFA API Endpoints

> Reference: https://fofa.info

| Endpoint | Description |
|----------|-------------|
| `https://fofa.info/api/v1/search/all` | Search query |
| `https://fofa.info/api/v1/search/stats` | Statistics aggregation |
| `https://fofa.info/api/v1/host/{host}` | Host aggregation |
| `https://fofa.info/api/v1/info/my` | Account info |
| `https://fofa.info/api/v1/search/next` | Pagination API |

## Notes

- Stats endpoint requires FOFA VIP (returns 403 for free tier)
- Host endpoint may have issues (returns 404)
