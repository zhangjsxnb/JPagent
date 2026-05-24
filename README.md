# 竞品广告分析 Agent

> Competitor Ad Intelligence Agent — Mobile Gaming

## 项目概述

基于 Claude Cowork + Claude Code + DeepSeek 搭建的竞品广告分析自动化系统。输入竞品游戏名称，输出素材类型分布、高频视觉元素、文案关键词、推测投放策略。

## 工具链

| 工具 | 用途 |
|------|------|
| **Claude Cowork** | 编排器 + AI 分析引擎。定时任务调度、数据采集执行、策略分析 |
| **Claude Code** | Python 采集脚本开发、API 调试 |
| **DeepSeek AI** | 广告素材策略分析、关键词提取、投放策略推断 |
| **Meta Ad Library API** | 公共广告数据源（需注册 Developer 账号） |
| **Vercel** | 前端展示网站部署 |

## 项目结构

```
ad-analyzer/
├── index.html              # 前端展示页面
├── vercel.json              # Vercel 部署配置
├── data/
│   ├── Last_War_analysis.json
│   ├── Monopoly_Go_analysis.json
│   ├── Whiteout_Survival_analysis.json
│   └── Royal_Match_analysis.json
├── scripts/
│   ├── collect_ads.py       # Meta API 数据采集脚本
│   └── config.json          # 配置文件
└── README.md
```

## 工作流

1. 用户输入竞品名称
2. Python 脚本调用 Meta Ad Library API 采集广告数据
3. DeepSeek AI 分析每条广告（素材类型、关键词、情感、策略）
4. 聚合生成结构化报告
5. 前端网站展示图表和分析结果

## 当前状态

### 已完成
- [x] 数据采集管道（Python 脚本，预留 Meta API 接口）
- [x] 基于公开情报的 4 个竞品广告分析
- [x] 素材类型自动分类与统计
- [x] 高频关键词提取与排序
- [x] 投放策略推断与报告生成
- [x] 可视化前端展示网站
- [x] Vercel 部署配置

### 待完善
- [ ] 接入 Meta Ad Library API（需注册 Facebook Developer 账号）
- [ ] 接入 TikTok Ads 数据
- [ ] 广告素材图片的 Vision 分析
- [ ] 周同比趋势对比

## 部署

本项目为纯静态站点，可直接部署到 Vercel：

```bash
# 1. 推送到 GitHub
git add .
git commit -m "init"
git push

# 2. 在 Vercel 导入仓库，自动部署
# 或使用 Vercel CLI
vercel --prod
```

## 配置说明

`scripts/config.json` 中包含 Meta Token 和 DeepSeek API Key 配置，接入实时数据时填写即可。

## 数据说明

当前 data/ 目录下的分析数据基于 Web Search 公开情报整理。
接入 Meta Ad Library API 后，数据将自动从 API 获取，无需手动更新。
