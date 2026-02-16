#!/usr/bin/env python3
"""
FOFA API Client - Official API Complete Wrapper
Features: Asset Query, Statistics, Batch Processing, CVE Fingerprint Lookup
"""

import os
import sys
import json
import argparse
import urllib.parse
import urllib.request
import base64
import csv
import subprocess
from typing import List, Dict, Optional, Tuple


# ========== Configuration ==========

FOFA_EMAIL = os.environ.get("FOFA_EMAIL")
FOFA_API_KEY = os.environ.get("FOFA_API_KEY")
BASE_URL = "https://fofa.info/api/v1"


def get_credentials() -> tuple:
    """Get authentication credentials"""
    if FOFA_EMAIL and FOFA_API_KEY:
        return FOFA_EMAIL, FOFA_API_KEY
    
    # Try FOFA_TOKEN format: email:key
    token = os.environ.get("FOFA_TOKEN")
    if token and ":" in token:
        email, key = token.split(":", 1)
        return email, key
    
    raise ValueError("Please set FOFA_EMAIL + FOFA_API_KEY or FOFA_TOKEN (email:key)")


def get_script_dir() -> str:
    """Get script directory"""
    return os.path.dirname(os.path.realpath(__file__))


def api_request(endpoint: str, params: dict = None) -> dict:
    """Send API request"""
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
                raise Exception(result["error"])
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


# ========== FOFA API Class ==========

class FOFA:
    """FOFA API Client"""
    
    def search(self, query: str, size: int = 100, page: int = 1, fields: str = None) -> dict:
        """Asset search query"""
        qbase64 = base64.b64encode(query.encode()).decode()
        params = {"qbase64": qbase64, "size": min(size, 10000), "page": page}
        if fields:
            params["fields"] = fields
        return api_request("/search/all", params)
    
    def host(self, host: str) -> dict:
        """Host query"""
        return api_request("/search/host", {"host": host})
    
    def hosts(self, host_list: List[str], simple: bool = False) -> dict:
        """Batch host query"""
        return api_request("/search/hosts", {
            "hosts": ",".join(host_list),
            "simple": "1" if simple else "0"
        })
    
    def stats(self, query: str, field: str = "protocol") -> dict:
        """Statistics aggregation"""
        qbase64 = base64.b64encode(query.encode()).decode()
        return api_request("/search/stats", {"qbase64": qbase64, "field": field})
    
    def user_info(self) -> dict:
        """Get account information"""
        return api_request("/info/my")
    
    def products(self) -> dict:
        """Get product list"""
        return api_request("/info/products")
    
    def apps(self) -> dict:
        """Get application fingerprints"""
        return api_request("/info/apps")
    
    def count(self, query: str) -> int:
        """Get result count"""
        result = self.search(query, size=1)
        return result.get("total", 0)


# ========== CVE Fingerprint Library ==========

CVE_SIGNATURES = {
    # Middleware
    "weblogic": 'app="Oracle WebLogic Server"',
    "weblogic_cve-2020-14882": 'title="WebLogic"',
    "tomcat": 'app="Apache Tomcat" || server="Tomcat"',
    "jboss": 'app="JBoss"',
    "websphere": 'app="WebSphere"',
    
    # Web Server
    "nginx": 'server="Nginx"',
    "apache": 'server="Apache"',
    "iis": 'server="Microsoft-IIS"',
    
    # Framework
    "spring": 'app="Spring" || header="Spring"',
    "struts": 'app="Apache Struts"',
    "django": 'app="Django"',
    "flask": 'app="Flask"',
    "shiro": 'app="Apache Shiro"',
    "fastjson": 'app="Fastjson"',
    
    # Database
    "mysql": 'port="3306" && app="MySQL"',
    "postgresql": 'port="5432"',
    "mongodb": 'port="27017"',
    "redis": 'port="6379"',
    "elasticsearch": 'port="9200"',
    "memcached": 'port="11211"',
    
    # Cache/Message Queue
    "rabbitmq": 'port="15672"',
    "kafka": 'port="9092"',
    "activemq": 'port="8161"',
    
    # DevOps Tools
    "jenkins": 'title="Jenkins"',
    "gitlab": 'title="GitLab"',
    "nexus": 'title="Nexus"',
    "jira": 'title="Jira"',
    "confluence": 'title="Confluence"',
    "zabbix": 'app="Zabbix"',
    "grafana": 'title="Grafana"',
    
    # Cloud Native
    "docker": 'port="2375" || port="2376"',
    "kubernetes": 'port="6443"',
    "minio": 'title="MinIO"',
    "harbor": 'title="Harbor"',
    
    # Other Services
    "zookeeper": 'port="2181"',
    "hadoop": 'port="50070"',
    "jupyter": 'title="Jupyter"',
    "phpmyadmin": 'title="phpMyAdmin"',
}


def cve_lookup(keyword: str = None) -> List[Dict]:
    """CVE/Product fingerprint lookup"""
    if not keyword:
        return [{"name": k, "query": v} for k, v in CVE_SIGNATURES.items()]
    
    keyword = keyword.lower()
    matches = [(k, v) for k, v in CVE_SIGNATURES.items() if keyword in k]
    return [{"name": k, "query": v} for k, v in matches] if matches else [{"error": f"Not found: {keyword}"}]


# ========== Command Line Interface ==========

def cmd_search(args):
    """Search command"""
    fofa = FOFA()
    fields = args.fields or "host,ip,port,protocol,server,title,domain"
    
    print(f"[FOFA] Query: {args.query}")
    print(f"[FOFA] Size: {args.size}, Page: {args.page}")
    
    result = fofa.search(args.query, size=args.size, page=args.page, fields=fields)
    results = result.get("results", [])
    total = result.get("total", 0)
    
    print(f"[FOFA] Total: {total}, Returned: {len(results)}")
    
    for i, r in enumerate(results[:args.limit], 1):
        print(f"  {i}. {r}")
    
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        print(f"[FOFA] Saved: {args.output}")
    
    if args.csv:
        with open(args.csv, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(fields.split(","))
            for r in results:
                writer.writerow(r if isinstance(r, list) else [r.get(f, "") for f in fields.split(",")])
        print(f"[FOFA] CSV: {args.csv}")


def cmd_host(args):
    """Host query command"""
    fofa = FOFA()
    result = fofa.host(args.host)
    print(json.dumps(result, ensure_ascii=False, indent=2))


def cmd_hosts(args):
    """Batch hosts command"""
    fofa = FOFA()
    result = fofa.hosts(args.hosts, simple=args.simple)
    print(json.dumps(result, ensure_ascii=False, indent=2))


def cmd_stats(args):
    """Statistics command"""
    fofa = FOFA()
    result = fofa.stats(args.query, args.field)
    
    print(f"[FOFA] Query: {args.query}")
    print(f"[FOFA] Field: {args.field}")
    print("\n=== Statistics ===")
    
    stat = result.get("stat", {})
    if args.field in stat:
        data = stat[args.field]
        for value, count in sorted(data.items(), key=lambda x: x[1], reverse=True)[:args.limit]:
            print(f"  {value}: {count}")
    
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        print(f"\n[FOFA] Saved: {args.output}")


def cmd_info(args):
    """Account info command"""
    fofa = FOFA()
    result = fofa.user_info()
    print(json.dumps(result, ensure_ascii=False, indent=2))


def cmd_products(args):
    """Products list command"""
    fofa = FOFA()
    result = fofa.products()
    print(json.dumps(result, ensure_ascii=False, indent=2))


def cmd_count(args):
    """Count command"""
    fofa = FOFA()
    count = fofa.count(args.query)
    print(f"[FOFA] Query: {args.query}")
    print(f"[FOFA] Total: {count}")


def cmd_cve(args):
    """CVE/Product fingerprint command"""
    results = cve_lookup(args.keyword)
    
    if args.list:
        print(f"Total {len(CVE_SIGNATURES)} fingerprints:\n")
        for k, v in CVE_SIGNATURES.items():
            print(f"  {k}: {v}")
    else:
        for r in results:
            if "error" in r:
                print(f"Error: {r['error']}")
            else:
                print(f"[{r['name']}] {r['query']}")
                
                if args.search:
                    print(f"  -> Executing FOFA search...")
                    fofa = FOFA()
                    try:
                        data = fofa.search(r["query"], size=args.size)
                        print(f"  -> Found {len(data.get('results', []))} results")
                        for item in data.get("results", [])[:3]:
                            print(f"     {item}")
                    except Exception as e:
                        print(f"  -> Error: {e}")


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description="FOFA API Client")
    subparsers = parser.add_subparsers(dest="cmd")
    
    # search
    p = subparsers.add_parser("search", help="Asset query")
    p.add_argument("query", help="FOFA query syntax")
    p.add_argument("--size", "-s", type=int, default=100)
    p.add_argument("--page", "-p", type=int, default=1)
    p.add_argument("--fields", "-f")
    p.add_argument("--limit", "-l", type=int, default=10)
    p.add_argument("--output", "-o")
    p.add_argument("--csv", "-c")
    
    # host
    p = subparsers.add_parser("host", help="Host query")
    p.add_argument("host")
    
    # hosts
    p = subparsers.add_parser("hosts", help="Batch host query")
    p.add_argument("hosts", nargs="+")
    p.add_argument("--simple", action="store_true")
    
    # stats
    p = subparsers.add_parser("stats", help="Statistics aggregation")
    p.add_argument("query")
    p.add_argument("--field", "-t", default="protocol")
    p.add_argument("--limit", "-l", type=int, default=20)
    p.add_argument("--output", "-o")
    
    # info
    subparsers.add_parser("info", help="Account info")
    
    # products
    subparsers.add_parser("products", help="Product list")
    
    # count
    p = subparsers.add_parser("count", help="Count query")
    p.add_argument("query")
    
    # cve
    p = subparsers.add_parser("cve", help="CVE/Product fingerprints")
    p.add_argument("keyword", nargs="?", help="Keyword")
    p.add_argument("--list", "-l", action="store_true", help="List all")
    p.add_argument("--search", action="store_true", help="Execute search")
    p.add_argument("--size", "-s", type=int, default=10)
    
    args = parser.parse_args()
    
    if not args.cmd:
        parser.print_help()
        return
    
    try:
        if args.cmd == "search":
            cmd_search(args)
        elif args.cmd == "host":
            cmd_host(args)
        elif args.cmd == "hosts":
            cmd_hosts(args)
        elif args.cmd == "stats":
            cmd_stats(args)
        elif args.cmd == "info":
            cmd_info(args)
        elif args.cmd == "products":
            cmd_products(args)
        elif args.cmd == "count":
            cmd_count(args)
        elif args.cmd == "cve":
            cmd_cve(args)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
