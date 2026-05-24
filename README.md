# 竞品广告分析 Agent

> Competitor Ad Intelligence Agent — Mobile Gaming

## 项目概述

基于 Claude Cowork + 定时任务调度 + Vercel 部署的竞品广告素材自动化分析系统。每周一自动检索竞品广告素材情报，结构化输出后自动推送部署。

## Quick Start

```bash
# 1. 安装依赖
pip install -r scripts/requirements.txt

# 2. 手动触发全量流水线（数据检索 → 分析 → 报告 → 自动推送部署）
python run_weekly.py

# 3. 或等待定时任务自动执行（每周一 09:09）
```

## 工具链

| 工具 | 用途 |
|------|------|
| **Claude Cowork** | 流程编排、定时任务调度、AI 情报检索与结构化分析 |
| **Claude Code** | 脚本开发 |
| **WebSearch** | 精准微观广告素材情报检索 |
| **Chart.js** | 前端数据可视化 |
| **Vercel + 自定义域名** | 前端展示网站部署 |
| **GitHub Actions** | 自动推送与持续部署 |

## 项目结构

```
ad-analyzer/
├── index.html                    # 前端展示页面（内嵌 ALL_DATA + Chart.js 图表）
├── auto_push.py                  # 自动提交推送脚本
├── run_weekly.py                 # 全量流水线入口脚本
├── Prompt模板清单.md             # Agent 检索与分析 Prompt 模板库
├── scripts/
│   └── requirements.txt          # Python 依赖
├── data/
│   ├── Last_War_analysis.json    # 竞品历史分析数据
│   ├── Monopoly_Go_analysis.json
│   ├── Whiteout_Survival_analysis.json
│   ├── Royal_Match_analysis.json
│   └── weekly_report_*.md        # 定时任务生成的周报
├── README.md
└── 提交说明.md
```

## 自动化流程

```
每周一 09:09 定时触发
       │
       ▼
① 读取 index.html 解析当前竞品名单
       │
       ▼
② 逐个竞品执行精准微观情报检索
   · 搜索 ad copy examples / 广告文案拆解
   · 站内搜索 appgrowing.net / socialpeta.com
   · 搜索 UA strategy / retargeting 策略线索
       │
       ▼
③ 基于搜索文本合理推算结构化数据（素材类型、关键词、情感诉求等）
       │
       ▼
④ 添加新快照到 index.html + 生成 markdown 周报
       │
       ▼
⑤ 自动执行 python auto_push.py → GitHub → Vercel 自动部署
```

## 当前能力

- 自动定时任务：每周一执行完整情报检索 → 分析 → 部署链路
- 多周期视图：近7天/30天/90天数据切换
- 趋势折线图：广告量、�