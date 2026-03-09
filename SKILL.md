---
name: fofa
description: FOFA 网络资产搜索引擎查询。使用语义边界清晰的词汇，确保输出可控。
metadata: {"openclaw": {"requires": {"env": ["FOFA_EMAIL", "FOFA_API_KEY"]}, "emoji": "🔍"}}
---

# FOFA 资产查询

## ⚠️ 语义边界声明

本 Skill 仅执行以下**明确限定**的操作：

1. **查询 (search)** - 根据 FOFA 语法查询资产
2. **统计 (stats)** - 统计聚合（需 VIP）
3. **主机 (host)** - 主机详情查询
4. **账户信息 (info)** - 查询账户状态
5. **CVE 指纹 (cve)** - 列出对应产品的 CVE

**不执行**：
- ❌ 不进行"分析"（语义过宽）
- ❌ 不给出"建议"（超出范围）
- ❌ 不做"评估"（主观判断）
- ❌ 不输出"风险等级"（自行发明）

## 📋 结构化工作流

```
STEP 1: 验证 FOFA 账户状态 (info 命令)
STEP 2: 执行查询 (search/host/cve 命令)
STEP 3: 格式化输出结果
```

每一步都有明确的**输入 → 执行 → 输出**，不允许跳过。

## 🔧 强制输出格式

查询结果的输出必须严格按以下 JSON 格式，禁止自行添加"分析"、"建议"等内容：

```json
{
  "total": 0,
  "results": [
    {
      "host": "192.168.1.1",
      "port": 443,
      "protocol": "https"
    }
  ]
}
```

## 🎯 词汇选择（避免语义陷阱）

| ❌ 禁用词汇 | ✅ 替换为 |
|-----------|----------|
| 分析 | 查询 |
| 评估 | 列出 |
| 建议 | - (不输出) |
| 风险 | - (不输出) |
| 描述 | 列出 |

## 环境设置

```bash
export FOFA_EMAIL="your@email.com"
export FOFA_API_KEY="your-api-key"
```

## 使用方法

```bash
# 资产查询
python {baseDir}/scripts/fofa_query.py search "domain=example.com"

# 主机详情
python {baseDir}/scripts/fofa_query.py host "192.168.1.1"

# CVE 指纹
python {baseDir}/scripts/fofa_query.py cve redis

# 账户信息
python {baseDir}/scripts/fofa_query.py info
```

## 命令说明

| 命令 | 功能 | 输出格式 |
|-----|------|---------|
| search | 资产查询 | JSON 列表 |
| host | 主机详情 | JSON 对象 |
| stats | 统计聚合 | JSON 对象(需VIP) |
| count | 结果计数 | 数字 |
| info | 账户信息 | JSON 对象 |
| cve | CVE 指纹 | JSON 列表 |

## 注意事项

- API 限制：免费账户有每日配额
- 最大结果：每次请求 10000 条
- stats 功能需 VIP 会员
- 仅用于授权的安全测试
