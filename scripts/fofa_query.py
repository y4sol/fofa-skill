#!/usr/bin/env python3
"""
FOFA API 客户端 - 官方 API 完整封装
功能: 资产查询、统计聚合、批量处理、CVE 特征关联
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
from typing import Optional, List, Dict, Any
from collections import Counter


# ========== 配置 ==========
TOKEN = os.environ.get("FOFA_TOKEN")  # 兼容: FOFA_TOKEN = email:key
FOFA_EMAIL = os.environ.get("FOFA_EMAIL")
FOFA_API_KEY = os.environ.get("FOFA_API_KEY")
BASE_URL = "https://fofa.info/api/v1"


def get_credentials() -> tuple:
    """获取认证信息"""
    # 优先使用 FOFA_TOKEN (email:key 格式)
    if TOKEN:
        if ":" in TOKEN:
            email, key = TOKEN.split(":", 1)
            return email, key
    
    if FOFA_EMAIL and FOFA_API_KEY:
        return FOFA_EMAIL, FOFA_API_KEY
    
    raise ValueError("请设置 FOFA_EMAIL + FOFA_API_KEY 或 FOFA_TOKEN (email:key)")


def get_script_dir():
    """获取脚本目录"""
    return os.path.dirname(os.path.realpath(__file__))


def api_request(endpoint: str, params: dict = None) -> dict:
    """发送 API 请求"""
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
        raise Exception(f"请求失败: {str(e)}")


# ========== FOFA API 类 ==========

class FOFA:
    """FOFA API 客户端"""
    
    def search(self, query: str, size: int = 100, page: int = 1, fields: str = None) -> dict:
        """资产查询"""
        qbase64 = base64.b64encode(query.encode()).decode()
        params = {"qbase64": qbase64, "size": min(size, 10000), "page": page}
        if fields:
            params["fields"] = fields
        return api_request("/search/all", params)
    
    def host(self, host: str) -> dict:
        """Host 查询"""
        return api_request("/search/host", {"host": host})
    
    def hosts(self, host_list: List[str], simple: bool = False) -> dict:
        """批量 Host"""
        return api_request("/search/hosts", {
            "hosts": ",".join(host_list),
            "simple": "1" if simple else "0"
        })
    
    def stats(self, query: str, field: str = "protocol") -> dict:
        """统计聚合"""
        qbase64 = base64.b64encode(query.encode()).decode()
        return api_request("/search/stats", {"qbase64": qbase64, "field": field})
    
    def user_info(self) -> dict:
        """账号信息"""
        return api_request("/info/my")
    
    def products(self) -> dict:
        """产品列表"""
        return api_request("/info/products")
    
    def apps(self) -> dict:
        """应用指纹"""
        return api_request("/info/apps")
    
    def count(self, query: str) -> int:
        """结果数量"""
        result = self.search(query, size=1)
        return result.get("total", 0)


# ========== CVE 特征库 ==========

CVE_SIGNATURES = {
    # 中间件
    "weblogic": 'app="Oracle WebLogic Server"',
    "weblogic_cve-2020-14882": 'title="WebLogic"',
    "tomcat": 'app="Apache Tomcat" || server="Tomcat"',
    "jboss": 'app="JBoss"',
    "websphere": 'app="WebSphere"',
    
    # Web 服务器
    "nginx": 'server="Nginx"',
    "apache": 'server="Apache"',
    "iis": 'server="Microsoft-IIS"',
    
    # 框架
    "spring": 'app="Spring" || header="Spring"',
    "struts": 'app="Apache Struts"',
    "django": 'app="Django"',
    "flask": 'app="Flask"',
    "shiro": 'app="Apache Shiro"',
    "fastjson": 'app="Fastjson"',
    
    # 数据库
    "mysql": 'port="3306" && app="MySQL"',
    "postgresql": 'port="5432"',
    "mongodb": 'port="27017"',
    "redis": 'port="6379"',
    "elasticsearch": 'port="9200"',
    "memcached": 'port="11211"',
    
    # 缓存/消息
    "rabbitmq": 'port="15672"',
    "kafka": 'port="9092"',
    "activemq": 'port="8161"',
    
    # 运维工具
    "jenkins": 'title="Jenkins"',
    "gitlab": 'title="GitLab"',
    "nexus": 'title="Nexus"',
    "jira": 'title="Jira"',
    "confluence": 'title="Confluence"',
    "zabbix": 'app="Zabbix"',
    "grafana": 'title="Grafana"',
    
    # 云原生
    "docker": 'port="2375" || port="2376"',
    "kubernetes": 'port="6443"',
    "minio": 'title="MinIO"',
    "harbor": 'title="Harbor"',
    
    # 其他服务
    "zookeeper": 'port="2181"',
    "hadoop": 'port="50070"',
    "jupyter": 'title="Jupyter"',
    "phpmyadmin": 'title="phpMyAdmin"',
}


def cve_lookup(keyword: str = None) -> List[Dict]:
    """CVE/产品特征查询"""
    if not keyword:
        return [{"name": k, "query": v} for k, v in CVE_SIGNATURES.items()]
    
    keyword = keyword.lower()
    matches = [(k, v) for k, v in CVE_SIGNATURES.items() if keyword in k]
    return [{"name": k, "query": v} for k, v in matches] if matches else [{"error": f"未找到: {keyword}"}]


# ========== 命令行 ==========

def cmd_search(args):
    fofa = FOFA()
    fields = args.fields or "host,ip,port,protocol,server,title,domain"
    
    print(f"[FOFA] 查询: {args.query}")
    print(f"[FOFA] 数量: {args.size}, 页码: {args.page}")
    
    result = fofa.search(args.query, size=args.size, page=args.page, fields=fields)
    results = result.get("results", [])
    total = result.get("total", 0)
    
    print(f"[FOFA] 总计: {total}, 返回: {len(results)}")
    
    for i, r in enumerate(results[:args.limit], 1):
        print(f"  {i}. {r}")
    
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        print(f"[FOFA] 已保存: {args.output}")
    
    if args.csv:
        with open(args.csv, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(fields.split(","))
            for r in results:
                writer.writerow(r if isinstance(r, list) else [r.get(f, "") for f in fields.split(",")])
        print(f"[FOFA] CSV: {args.csv}")


def cmd_host(args):
    fofa = FOFA()
    result = fofa.host(args.host)
    print(json.dumps(result, ensure_ascii=False, indent=2))


def cmd_hosts(args):
    fofa = FOFA()
    result = fofa.hosts(args.hosts, simple=args.simple)
    print(json.dumps(result, ensure_ascii=False, indent=2))


def cmd_stats(args):
    fofa = FOFA()
    result = fofa.stats(args.query, args.field)
    
    print(f"[FOFA] 查询: {args.query}")
    print(f"[FOFA] 字段: {args.field}")
    print("\n=== 统计结果 ===")
    
    stat = result.get("stat", {})
    if args.field in stat:
        data = stat[args.field]
        for value, count in sorted(data.items(), key=lambda x: x[1], reverse=True)[:args.limit]:
            print(f"  {value}: {count}")
    
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        print(f"\n[FOFA] 已保存: {args.output}")


def cmd_info(args):
    fofa = FOFA()
    result = fofa.user_info()
    print(json.dumps(result, ensure_ascii=False, indent=2))


def cmd_products(args):
    fofa = FOFA()
    result = fofa.products()
    print(json.dumps(result, ensure_ascii=False, indent=2))


def cmd_count(args):
    fofa = FOFA()
    count = fofa.count(args.query)
    print(f"[FOFA] 查询: {args.query}")
    print(f"[FOFA] 总数: {count}")


def cmd_cve(args):
    results = cve_lookup(args.keyword)
    
    if args.list:
        print(f"共 {len(CVE_SIGNATURES)} 个特征:\n")
        for k, v in CVE_SIGNATURES.items():
            print(f"  {k}: {v}")
    else:
        for r in results:
            if "error" in r:
                print(f"Error: {r['error']}")
            else:
                print(f"[{r['name']}] {r['query']}")
                
                if args.search:
                    print(f"  -> 执行 FOFA 查询...")
                    fofa = FOFA()
                    try:
                        data = fofa.search(r["query"], size=args.size)
                        print(f"  -> 找到 {len(data.get('results', []))} 条结果")
                        for item in data.get("results", [])[:3]:
                            print(f"     {item}")
                    except Exception as e:
                        print(f"  -> 错误: {e}")


def main():
    parser = argparse.ArgumentParser(description="FOFA API 客户端")
    subparsers = parser.add_subparsers(dest="cmd")
    
    # search
    p = subparsers.add_parser("search", help="资产查询")
    p.add_argument("query", help="FOFA 查询语法")
    p.add_argument("--size", "-s", type=int, default=100)
    p.add_argument("--page", "-p", type=int, default=1)
    p.add_argument("--fields", "-f")
    p.add_argument("--limit", "-l", type=int, default=10)
    p.add_argument("--output", "-o")
    p.add_argument("--csv", "-c")
    
    # host
    p = subparsers.add_parser("host", help="Host 查询")
    p.add_argument("host")
    
    # hosts
    p = subparsers.add_parser("hosts", help="批量 Host")
    p.add_argument("hosts", nargs="+")
    p.add_argument("--simple", action="store_true")
    
    # stats
    p = subparsers.add_parser("stats", help="统计聚合")
    p.add_argument("query")
    p.add_argument("--field", "-t", default="protocol")
    p.add_argument("--limit", "-l", type=int, default=20)
    p.add_argument("--output", "-o")
    
    # info
    subparsers.add_parser("info", help="账号信息")
    
    # products
    subparsers.add_parser("products", help="产品列表")
    
    # count
    p = subparsers.add_parser("count", help="数量查询")
    p.add_argument("query")
    
    # cve
    p = subparsers.add_parser("cve", help="CVE/产品特征")
    p.add_argument("keyword", nargs="?", help="关键词")
    p.add_argument("--list", "-l", action="store_true", help="列出所有")
    p.add_argument("--search", action="store_true", help="执行查询")
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
