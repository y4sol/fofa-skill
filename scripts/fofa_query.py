#!/usr/bin/env python3
"""
FOFA API Client
Only 5 endpoints: search, stats, host, info, next
"""

import os
import sys
import json
import argparse
import urllib.parse
import urllib.request
import base64


FOFA_EMAIL = os.environ.get("FOFA_EMAIL")
FOFA_API_KEY = os.environ.get("FOFA_API_KEY")
BASE_URL = "https://fofa.info/api/v1"


def get_credentials():
    if FOFA_EMAIL and FOFA_API_KEY:
        return FOFA_EMAIL, FOFA_API_KEY
    token = os.environ.get("FOFA_TOKEN")
    if token and ":" in token:
        return token.split(":", 1)
    raise ValueError("Set FOFA_EMAIL+FOFA_API_KEY or FOFA_TOKEN")


def api_request(endpoint: str, params: dict = None):
    email, key = get_credentials()
    url = f"{BASE_URL}{endpoint}"
    
    if params:
        params["email"] = email
        params["key"] = key
        query_string = "&".join([f"{k}={urllib.parse.quote(str(v))}" for k, v in params.items()])
        url = f"{url}?{query_string}"
    
    try:
        with urllib.request.urlopen(url, timeout=30) as response:
            result = json.loads(response.read().decode("utf-8"))
            if result.get("error"):
                raise Exception(result.get("errmsg", "Unknown error"))
            return result
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8")
        try:
            error_data = json.loads(error_body)
            raise Exception(error_data.get("errmsg", str(e)))
        except:
            raise Exception(f"HTTP {e.code}: {error_body}")
    except Exception as e:
        raise Exception(f"Request failed: {str(e)}")


class FOFA:
    def search(self, query: str, size: int = 100, page: int = 1):
        qbase64 = base64.b64encode(query.encode()).decode()
        return api_request("/search/all", {"qbase64": qbase64, "size": min(size, 10000), "page": page})
    
    def stats(self, query: str, field: str = "protocol"):
        qbase64 = base64.b64encode(query.encode()).decode()
        return api_request("/search/stats", {"qbase64": qbase64, "field": field})
    
    def host(self, host: str):
        return api_request(f"/host/{host}")
    
    def info(self):
        return api_request("/info/my")
    
    def next(self, last_id: str, size: int = 100):
        return api_request("/search/next", {"last_id": last_id, "size": min(size, 10000)})
    
    def count(self, query: str) -> int:
        result = self.search(query, size=1, page=1)
        return result.get("total", 0)


def cmd_search(args):
    fofa = FOFA()
    result = fofa.search(args.query, size=args.size, page=args.page)
    results = result.get("results", [])
    total = result.get("total", 0)
    print(f"Query: {args.query}")
    print(f"Total: {total}, Returned: {len(results)}")
    for i, r in enumerate(results[:args.limit], 1):
        print(f"  {i}. {r}")
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        print(f"Saved: {args.output}")


def cmd_stats(args):
    fofa = FOFA()
    result = fofa.stats(args.query, args.field)
    print(f"Query: {args.query}")
    print(f"Field: {args.field}")
    stat = result.get("stat", {})
    if args.field in stat:
        data = stat[args.field]
        for value, count in sorted(data.items(), key=lambda x: x[1], reverse=True)[:args.limit]:
            print(f"  {value}: {count}")


def cmd_host(args):
    fofa = FOFA()
    result = fofa.host(args.host)
    print(json.dumps(result, ensure_ascii=False, indent=2))


def cmd_info(args):
    fofa = FOFA()
    result = fofa.info()
    print(json.dumps(result, ensure_ascii=False, indent=2))


def cmd_next(args):
    fofa = FOFA()
    result = fofa.next(args.last_id, size=args.size)
    results = result.get("results", [])
    print(f"Last ID: {args.last_id}")
    print(f"Returned: {len(results)}")
    for i, r in enumerate(results[:args.limit], 1):
        print(f"  {i}. {r}")


def cmd_count(args):
    fofa = FOFA()
    count = fofa.count(args.query)
    print(f"Query: {args.query}")
    print(f"Total: {count}")


def main():
    parser = argparse.ArgumentParser(description="FOFA API Client")
    subparsers = parser.add_subparsers(dest="cmd")
    
    p = subparsers.add_parser("search", help="Asset query")
    p.add_argument("query")
    p.add_argument("--size", "-s", type=int, default=100)
    p.add_argument("--page", "-p", type=int, default=1)
    p.add_argument("--limit", "-l", type=int, default=10)
    p.add_argument("--output", "-o")
    
    p = subparsers.add_parser("stats", help="Statistics")
    p.add_argument("query")
    p.add_argument("--field", "-t", default="protocol")
    p.add_argument("--limit", "-l", type=int, default=20)
    
    p = subparsers.add_parser("host", help="Host aggregation")
    p.add_argument("host")
    
    subparsers.add_parser("info", help="Account info")
    
    p = subparsers.add_parser("next", help="Pagination")
    p.add_argument("last_id")
    p.add_argument("--size", "-s", type=int, default=100)
    p.add_argument("--limit", "-l", type=int, default=10)
    
    p = subparsers.add_parser("count", help="Count query")
    p.add_argument("query")
    
    args = parser.parse_args()
    
    if not args.cmd:
        parser.print_help()
        return
    
    try:
        if args.cmd == "search":
            cmd_search(args)
        elif args.cmd == "stats":
            cmd_stats(args)
        elif args.cmd == "host":
            cmd_host(args)
        elif args.cmd == "info":
            cmd_info(args)
        elif args.cmd == "next":
            cmd_next(args)
        elif args.cmd == "count":
            cmd_count(args)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
