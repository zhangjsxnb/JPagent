# 竞品广告素材分析 Agent — 完整搭建指南

> 本文档为测试题第二题的操作指南，带你从零搭建一个可运行的竞品广告分析 Agent。
> 预计耗时：2-4 小时（视工具熟悉程度和 API 审核速度而定）

---

## 目录

1. [整体架构概览](#1-整体架构概览)
2. [技术选型指南](#2-技术选型指南)
3. [Phase 1：数据源接入](#3-phase-1数据源接入)
4. [Phase 2：搭建 Agent 工作流](#4-phase-2搭建-agent-工作流)
5. [Phase 3：分析与报告生成](#5-phase-3分析与报告生成)
6. [Phase 4：自动化与调度](#6-phase-4自动化与调度)
7. [Phase 5：测试与迭代](#7-phase-5测试与迭代)
8. [附录 A：Prompt 模板库](#附录-aprompt-模板库)
9. [附录 B：常见问题排查](#附录-b常见问题排查)
10. [附录 C：产出物清单](#附录-c产出物清单)

---

## 1. 整体架构概览

### 你要搭建什么

```
输入：竞品游戏名称 / App ID
                  │
                  ▼
        ┌─────────────────────┐
        │   数据采集层          │
        │  · Meta Ad Library   │
        │  · TikTok Ad Data     │
        │  · SensorTower(可选)  │
        └────────┬────────────┘
                 │
                 ▼
        ┌─────────────────────┐
        │   数据分析层          │
        │  · 素材类型分类       │
        │  · 视觉元素提取       │
        │  · 文案关键词抽取     │
        │  · 投放策略推断       │
        └────────┬────────────┘
                 │
                 ▼
        ┌─────────────────────┐
        │   报告输出层          │
        │  · 结构化报告         │
        │  · 趋势可视化         │
        │  · 策略建议           │
        └─────────────────────┘
                 │
                 ▼
输出：竞品广告分析报告（可分享给投放团队）
```

### 核心数据流

```
竞品 App ID → 查询 Meta Ad Library API
            → 拉取活跃广告列表
            → 提取素材 URL / 文案 / 投放信息
            → AI 分析素材类型 + 视觉元素 + 关键词
            → 聚合生成结构化报告
            → 推送到指定输出（飞书/钉钉/Slack/本地文件）
```

---

## 2. 技术选型指南

### 方案对比

| 方案 | 优点 | 缺点 | 适合谁 |
|------|------|------|--------|
| **n8n** (自部署) | 完全可控，支持复杂分支逻辑，免费 | 需要服务器，学习曲线中等 | 有技术背景，希望完全掌控 |
| **Make** (原 Integromat) | 操作简单，内置 HTTP 模块，免费额度够用 | 复杂逻辑受限，付费功能多 | 非技术人员，快速搭建 |
| **Coze** | 自带 Bot 能力，中文友好，插件生态 | 自定义逻辑受限，数据保密性 | 想做对话式分析 |
| **Dify** | RAG 能力强，支持工作流编排 | 需要部署，API 集成稍复杂 | 有技术背景，需要灵活定制 |
| **Claude Projects + 脚本** | 分析质量高，灵活 | 需手动跑脚本，自动化程度低 | 想快速出分析结果 |
| **推荐方案：Make + Claude API** | - | - | **最佳平衡点** |
| **推荐方案：n8n + Claude API** | - | - | **技术向首选** |

### 我的推荐

**首选：n8n（自部署） + Claude API / OpenAI API**

理由：
- HTTP Request 节点直接调用 Meta Ad Library API
- AI 节点做分析，支持 Claude/OpenAI
- 可以设置每周自动运行
- 完全本地/私有服务器部署，数据安全
- 免费且功能完整

**备选：Make + Claude API**

如果不想自己部署服务器，Make 是最快的选择。

---

## 3. Phase 1：数据源接入

### 3.1 Meta Ad Library API — 这是核心数据源

#### 你需要准备

| 物料 | 说明 | 获取方式 |
|------|------|----------|
| Facebook App ID | 用于调用 Meta API | https://developers.facebook.com/ 创建应用 |
| Access Token | API 调用凭证 | 在 Meta Developer 后台生成 |
| 竞品 App ID 或 Page ID | 要查询的竞品标识 | 从 App Store / Google Play 获取 |

#### 第一步：注册 Meta Developer 账号

1. 打开 https://developers.facebook.com/
2. 用你的 Facebook 账号登录
3. 点击 **My Apps** → **Create App**
4. 选择 **Business** 类型
5. 填写应用名称和邮箱
6. 创建成功后，进入 Dashboard

#### 第二步：获取 Access Token

有两种方式：

**方式 A：短期 Token（测试用，1-2 小时过期）**

```
1. 进入你的 App Dashboard
2. 左侧菜单 → Tools → Graph API Explorer
3. 在 Permissions 中选择：ads_read
4. 点击 Generate Access Token
5. 复制 Token（注意：这个 Token 有效期短，仅用于测试）
```

**方式 B：长期 Token（推荐，有效期 60 天）**

在 Graph API Explorer 获取短期 Token 后，调用以下 API 换取长期 Token：

```
GET https://graph.facebook.com/v19.0/oauth/access_token
  ?grant_type=fb_exchange_token
  &client_id={你的 App ID}
  &client_secret={你的 App Secret}
  &fb_exchange_token={短期 Token}
```

> 你可以在 App Dashboard → Settings → Basic 找到 App Secret

#### 第三步：测试 API 调用

用浏览器或 Postman 测试以下请求：

```
GET https://graph.facebook.com/v19.0/ads_archive
  ?search_terms='"game name"'
  &ad_type=ALL
  &ad_reached_countries=['US']
  &fields=ad_creative_body,ad_creative_link_caption,ad_creative_link_description,
          ad_creative_link_title,ad_delivery_start_time,ad_delivery_stop_time,
          ad_snapshot_url,ad_active_status,bylines,demographic_distribution,
          impressions,page_id,publisher_platforms,spend
  &limit=100
  &access_token={YOUR_TOKEN}
```

**如何找到竞品的 Page ID？**

方法 1：直接在 Facebook 搜索竞品品牌名，进入其主页，URL 中的数字串就是 Page ID
方法 2：用这个查询：

```
GET https://graph.facebook.com/v19.0/pages/search
  ?q={品牌名}
  &access_token={YOUR_TOKEN}
```

> **重要注意事项：**
> - `search_terms` 最少 2 个字符
> - 每次请求最多返回 100 条广告
> - `ad_reached_countries` 限制 1-2 个国家即可，数据太多不好处理
> - 如果想查特定竞品的所有广告，用 `page_id` 参数比 `search_terms` 更准

### 3.2 TikTok Ads 数据

TikTok 没有完全公开的 Ad Library API，但有几种替代方案：

#### 方案 A：TikTok Creative Center（免费，免 API）

1. 打开 https://ads.tiktok.com/business/creativecenter/
2. 搜索竞品品牌名
3. 查看其 Top Ads
4. **手动采集或用浏览器自动化抓取**

**浏览器自动化采集 Prompt（在 Claude/Cursor 中使用）：**

```
你是爬虫专家，用 Python + Playwright/Selenium 实现以下功能：

1. 打开 TikTok Creative Center (https://ads.tiktok.com/business/creativecenter/)
2. 搜索关键词 "{竞品名}"
3. 等待搜索结果加载
4. 抓取前 20 条广告的以下信息：
   - 广告文案 (ad_text)
   - 视频时长 (video_duration)
   - 点赞数 (likes)
   - 投放地区 (location)
5. 输出为 CSV 文件保存

注意：
- 处理登录弹窗
- 添加随机的 User-Agent
- 控制请求频率避免被 ban
- 加 try-catch 处理元素找不到的情况
```

#### 方案 B：BigSpy 第三方（付费，有免费试用）

- https://www.bigspy.com/
- 覆盖 Meta + TikTok + 更多平台
- 有 API（付费）
- 免费版可以手工查

#### 方案 C：手动替代方案

如果不想搞 TikTok API，可以直接：
1. 用 [TikTok Creative Center](https://ads.tiktok.com/business/creativecenter/) 手动搜索
2. 或者用 **TikTok 官方广告资料库**（部分国家有）：https://www.tiktok.com/ads/library/

### 3.3 辅助数据源（可选但推荐）

| 数据源 | 用途 | 免费程度 |
|--------|------|----------|
| **SensorTower** | App 下载量、收入估算、广告渠道 | 有限免费，完整版付费 |
| **data.ai (App Annie)** | App 排名、竞品对比 | 有限免费 |
| **Apptica** | 广告渠道分析，展示哪些广告网络在用 | 有限免费 |
| **App Growing** | 广告素材库，直接展示竞品素材 | 付费为主 |

**建议：先用 Meta Ad Library API + TikTok Creative Center 免费数据做第一版。有了基础产出后再考虑是否补充付费数据源。**

---

## 4. Phase 2：搭建 Agent 工作流

这一节以 **n8n** 为例，同时给出 **Make** 和 **纯代码** 两种替代方案。

### 4.1 n8n 搭建步骤

#### 第一步：部署 n8n

```bash
# 使用 Docker 部署（最简单）
docker run -d \
  --name n8n \
  -p 5678:5678 \
  -v ~/.n8n:/home/node/.n8n \
  -e N8N_SECURE_COOKIE=false \
  n8nio/n8n

# 部署完成后访问 http://localhost:5678
```

#### 第二步：创建基础工作流

工作流结构（共 6 个节点）：

```
[Schedule Trigger]
       │
[HTTP Request] ← 调用 Meta Ad Library API
       │
[Code Node] ← 解析 & 清洗数据
       │
[HTTP Request] ← 下载广告素材缩略图（可选）
       │
[AI Node] ← Claude/OpenAI 分析
       │
[Output] ← 生成报告 + 通知
```

#### 第三步：各节点配置

**节点 1：Schedule Trigger（定时触发）**

```
Trigger Type: Cron
Expression: 0 9 * * 1  (每周一早上 9 点)
或者：0 9 * * 1,4  (每周一和周四早上 9 点)
```

**节点 2：HTTP Request（调用 Meta API）**

```
Method: GET
URL: https://graph.facebook.com/v19.0/ads_archive

Parameters:
  search_terms: "{{$json.searchTerms}}"
  ad_type: ALL
  ad_reached_countries: ['US', 'GB', 'JP']
  fields: ad_creative_body,ad_creative_link_caption,ad_creative_link_description,ad_creative_link_title,ad_delivery_start_time,ad_snapshot_url,ad_active_status,publisher_platforms,spend,impressions
  limit: 200
  access_token: {{$env.META_ACCESS_TOKEN}}

Authentication: None（Token 在参数里传递）
```

**节点 3：Code Node（数据清洗）**

```javascript
// 清洗和标准化数据
const ads = $input.all();
const results = [];

for (const ad of ads) {
  const data = ad.json.data || [];
  
  for (const item of data) {
    results.push({
      platform: item.publisher_platforms || [],
      body: item.ad_creative_body || '',
      title: item.ad_creative_link_title || '',
      description: item.ad_creative_link_description || '',
      caption: item.ad_creative_link_caption || '',
      startDate: item.ad_delivery_start_time || '',
      endDate: item.ad_delivery_stop_time || '',
      snapshotUrl: item.ad_snapshot_url || '',
      spend: item.spend || 'unknown',
      impressions: item.impressions || 'unknown',
      isActive: item.ad_active_status === 'ACTIVE',
    });
  }
}

return results;
```

**节点 4：AI 分析节点**

连接到 Claude API 或 OpenAI API 进行分析。以下是调用 Claude 的 Prompt：

```
你是一个竞品广告分析专家。以下是从 Meta Ad Library 获取的竞品广告数据，
请对每条广告进行以下分析：

广告数据：
{{
  "platforms": "{platform}",
  "body": "{body}",
  "title": "{title}",
  "description": "{description}",
  "caption": "{caption}",
  "snapshotUrl": "{snapshotUrl}",
  "spend": "{spend}",
  "impressions": "{impressions}",
  "isActive": "{isActive}"
}}

请分析并返回以下 JSON 格式：

{{
  "adType": "视频/图片/轮播/纯文字/互动广告",
  "visual_elements": ["元素1","元素2"], // 分析文案中提到的视觉元素
  "keywords": ["关键词1","关键词2"], // 提炼的核心推广词
  "call_to_action": "下载/注册/试玩/购买",
  "targeting_strategy": "推测的目标策略：如 ROAS 优化/品牌曝光/节日促销/活动导流",
  "usp": "核心卖点，用一句话概括这条广告在强调什么",
  "tone": "紧迫感/社交证明/功能导向/情感共鸣/利益导向"
}}
```

**如果使用 n8n 的 AI 节点（OpenAI）：**

```
Model: gpt-4o-mini（性价比高）或 claude-sonnet-4-20250514
Endpoint: https://api.anthropic.com/v1/messages 或 OpenAI 标准 endpoint
API Key: 在 n8n Credentials 中设置
```

#### 第四步：聚合输出

**节点 5：Code Node — 聚合分析结果**

```javascript
// 聚合所有广告的分析结果
const analyses = $input.all().map(item => item.json);

const summary = {
  totalAds: analyses.length,
  platformDistribution: {},
  adTypeDistribution: {},
  topKeywords: {},
  topVisualElements: {},
  strategyInsights: [],
};

// 计算分布
analyses.forEach(ad => {
  // 素材类型分布
  if (ad.adType) {
    summary.adTypeDistribution[ad.adType] = (summary.adTypeDistribution[ad.adType] || 0) + 1;
  }
  
  // 关键词频率
  if (ad.keywords) {
    ad.keywords.forEach(kw => {
      summary.topKeywords[kw] = (summary.topKeywords[kw] || 0) + 1;
    });
  }
  
  // 视觉元素频率
  if (ad.visual_elements) {
    ad.visual_elements.forEach(el => {
      summary.topVisualElements[el] = (summary.topVisualElements[el] || 0) + 1;
    });
  }
  
  // 策略信息
  if (ad.targeting_strategy) {
    summary.strategyInsights.push(ad.targeting_strategy);
  }
});

// 排序取 Top
const sortByValue = (obj, n = 10) =>
  Object.entries(obj).sort((a, b) => b[1] - a[1]).slice(0, n);

summary.topKeywords = sortByValue(summary.topKeywords, 15);
summary.topVisualElements = sortByValue(summary.topVisualElements, 10);

return summary;
```

**节点 6：输出**

可选方式：
1. **发送到飞书/钉钉/Slack Bot** — 用 Webhook 节点
2. **写入 Google Sheets** — 供团队查看
3. **发送邮件** — 用 SMTP 节点
4. **保存为本地文件** — 用 Write File 节点

### 4.2 Make 替代方案

如果你选择 Make，操作步骤类似：

1. **注册/登录** https://www.make.com
2. **创建 Scenario**
3. **添加 Schedule 模块** → Set as Trigger
4. **添加 HTTP 模块** → 调用 Meta Ad Library API
5. **添加 Text Parser 或 Tools 模块** → 处理数据
6. **添加 OpenAI / Claude 模块** → 分析广告内容
7. **添加 Google Sheets / Slack 模块** → 输出报告

### 4.3 纯 Python 代码方案（最灵活）

如果你会写 Python，这是最快的方案，适合先跑通再迁移到 n8n/Make。

**项目结构：**

```
ad_analyzer/
├── main.py              # 主流程
├── config.py            # 配置（API Key、竞品列表）
├── collectors/
│   ├── meta_ads.py      # Meta Ad Library 采集器
│   └── tiktok_ads.py    # TikTok 采集器
├── analyzers/
│   └── ad_analyzer.py   # AI 分析模块
├── reporters/
│   └── report_generator.py  # 报告生成
└── outputs/             # 输出目录
```

**需要你准备的：**

```bash
pip install requests anthropic openai pandas pyyaml --break-system-packages
```

**`config.py` 模板：**

```python
# config.py
META_APP_ID = "your_app_id"
META_ACCESS_TOKEN = "your_long_lived_token"

# 可选：Claude API
ANTHROPIC_API_KEY = "sk-ant-xxx"

# 可选：OpenAI API
OPENAI_API_KEY = "sk-xxx"

# 竞品配置
COMPETITORS = [
    {
        "name": "Game A",
        "app_id": "com.example.gamea",
        "page_id": "123456789",  # Facebook Page ID
    },
    {
        "name": "Game B",
        "app_id": "com.example.gameb",
        "page_id": "987654321",
    },
]

# 每周一早上 9 点运行
SCHEDULE_CRON = "0 9 * * 1"
```

---

## 5. Phase 3：分析与报告生成

### 5.1 分析维度详解

| 分析维度 | 具体内容 | 数据来源 |
|----------|----------|----------|
| **素材类型分布** | 视频/图片/轮播/互动广告的比例 | Meta API 的 publisher_platforms 和 ad_snapshot_url |
| **高频视觉元素** | 角色、场景、UI、色彩等 | AI 分析素材 URL 截图 / 文案描述 |
| **文案关键词** | 核心卖点词、行动号召、情感词 | AI 分析 ad_creative_body |
| **投放策略推测** | 基于投放时间、文案、素材的综合判断 | AI 综合推断 |

### 5.2 报告模板

**每周竞品广告情报 — 输出格式示例：**

```
═══════════════════════════════════════
  竞品广告周报
  竞品：{Game Name}
  分析周期：2026-05-18 ~ 2026-05-24
  抓取广告数：{total_ads}
═══════════════════════════════════════

一、素材类型分布
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
• 视频广告：{video_pct}%（{video_count} 条）
• 图片广告：{image_pct}%（{image_count} 条）
• 轮播广告：{carousel_pct}%（{carousel_count} 条）

趋势判断：{trend_summary}

二、高频视觉元素 TOP 10
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. {element_1}（出现 {count} 次）
2. {element_2}（出现 {count} 次）
...

三、文案关键词 TOP 15
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. {keyword_1}（{count} 次）
2. {keyword_2}（{count} 次）
...

四、投放策略分析
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
策略类型分布：
• {strategy_type}：{strategy_pct}%
• {strategy_type}：{strategy_pct}%

洞察：{insight_summary}

五、值得关注的广告
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[广告 1]
- 类型：{type}
- 文案：{body_preview}
- 推测策略：{strategy}
- 链接：{snapshot_url}

[广告 2]
...

六、团队建议
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. {建议 1}
2. {建议 2}
3. {建议 3}
```

### 5.3 AI 报告生成 Prompt

```markdown
你是一个手游广告策略分析师。以下是本周竞品 {Competitor Name} 
在 Meta 平台的广告投放数据汇总。

=== 原始数据 ===
素材类型分布：{ad_type_distribution}
高频视觉元素：{top_visual_elements}
高频文案关键词：{top_keywords}
推测投放策略：{strategy_breakdown}
抓取广告总数：{total_count}

=== 你的任务 ===
基于以上数据，生成一份给投放团队的竞品分析报告。
报告需要包含：

1. 本周策略重点（用 2-3 句话概括竞品核心打法）
2. 素材方向变化（与上周相比的明显差异）
3. 值得特别注意的新素材方向
4. 我们的可借鉴点（具体建议，不要空话）
5. 风险提示（竞品可能在哪些方面有大的动作）

格式要求：
- 总分总结构
- 每条建议都要有数据支撑
- 语言简洁直接，适合投放团队晨会阅读
- 控制在 500 字以内
```

---

## 6. Phase 4：自动化与调度

### 6.1 n8n 自动调度

n8n 本身就支持 Cron 调度，配置好 Schedule Trigger 即可。

**推荐执行频率：**
- **每周一早上**：发送上周的完整报告（正式）
- **每周一 + 周四**：发送增量更新（快速响应）

### 6.2 Make 自动调度

Make Scenario 自带 Schedule 模块，设置方式同上。

### 6.3 纯代码方案 — 用系统 Cron

```bash
# 编辑 crontab
crontab -e

# 添加以下行（每周一早上 9 点执行）
0 9 * * 1 cd /path/to/ad_analyzer && python main.py >> logs/output.log 2>&1
```

### 6.4 推送渠道配置

**飞书 Bot Webhook：**

```bash
# 飞书机器人消息
curl -X POST https://open.feishu.cn/open-apis/bot/v2/hook/{YOUR_WEBHOOK_URL} \
  -H "Content-Type: application/json" \
  -d '{
    "msg_type": "interactive",
    "card": {
      "header": {"title": {"tag": "plain_text", "content": "📊 竞品广告周报"},
      "elements": [{"tag": "markdown", "content": "{REPORT_CONTENT}"}]
    }
  }'
```

**钉钉 Bot Webhook：**

```bash
curl -X POST https://oapi.dingtalk.com/robot/send?access_token={TOKEN} \
  -H "Content-Type: application/json" \
  -d '{"msgtype": "markdown", "markdown": {"title": "竞品广告周报", "text": "{REPORT_CONTENT}"}}'
```

**Slack Webhook：**

```bash
curl -X POST https://hooks.slack.com/services/{YOUR_WEBHOOK} \
  -H "Content-Type: application/json" \
  -d '{"text": "{REPORT_CONTENT}"}'
```

---

## 7. Phase 5：测试与迭代

### 7.1 测试流程

**第一轮：单次手动运行**

```
1. 选择 1 个竞品
2. 执行一次数据采集
3. 检查数据是否完整（有没有字段缺失？）
4. 检查 AI 分析结果是否合理（有没有明显误判？）
5. 调整 Prompt 直到输出稳定
```

**第二轮：多竞品运行**

```
1. 扩展竞品列表到 3-5 个
2. 运行全量采集
3. 检查超时/限流问题
4. 检查报告可读性
```

**第三轮：模拟真实调度**

```
1. 让 Agent 按计划时间运行一次
2. 检查推送是否正常到达
3. 找团队成员看一下报告，收集反馈
```

### 7.2 迭代方向

| 迭代方向 | 优先级 | 说明 |
|----------|--------|------|
| 增加 TikTok 数据 | ⭐⭐⭐ | 完善数据覆盖面 |
| 素材截图分析 | ⭐⭐⭐ | 不只是文案分析，直接分析图片内容 |
| 周同比趋势 | ⭐⭐ | 对比上周/上月变化 |
| 多竞品对比 | ⭐⭐ | 多个竞品并列对比 |
| 自动预警 | ⭐ | 竞品有新素材方向时自动通知 |

### 7.3 素材截图分析进阶（可选）

如果你想让 AI 直接分析广告素材图片，可以：

1. 从 ad_snapshot_url 下载广告截图
2. 用 Base64 编码传给 Claude Vision / GPT-4V

```python
import requests
import base64
from anthropic import Anthropic

# 下载图片
response = requests.get(ad_snapshot_url)
image_data = base64.b64encode(response.content).decode('utf-8')

# 传给 Claude Vision
client = Anthropic(api_key="sk-ant-xxx")
response = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1000,
    messages=[{
        "role": "user",
        "content": [
            {
                "type": "text",
                "text": "分析这张游戏广告图片，提取：1.画面主体元素 2.色彩风格 3.文字排版方式 4.整体调性（激励/玩法展示/角色展示/活动公告）"
            },
            {
                "type": "image",
                "source": {
                    "type": "base64",
                    "media_type": "image/jpeg",
                    "data": image_data
                }
            }
        ]
    }]
)
```

---

## 8. 附录 A：Prompt 模板库

### Prompt 1：单条广告分析（供 AI 节点使用）

```
你是一个广告创意分析专家。请分析以下游戏广告数据，识别其创意策略。

## 广告信息
- 文案：{ad_creative_body}
- 标题：{ad_creative_link_title}
- 描述：{ad_creative_link_description}
- 投放平台：{publisher_platforms}
- 投放时间：{ad_delivery_start_time}

## 分析要求
请输出以下分析结果（严格使用 JSON 格式）：

{
  "ad_type": "video/image/carousel/text/interactive"，  // 素材形式
  "creative_strategy": "",  // 50 字以内总结创意策略
  "target_audience": "",  // 推测的目标用户画像
  "emotional_appeal": "urgency/social_proof/functional/emotional/benefit"，  // 情感诉求类型
  "call_to_action": "",  // 行动号召内容
  "unique_selling_point": "",  // 核心卖点
  "visual_keywords": [],  // 从文案中提取的视觉相关关键词
  "copy_keywords": [],  // 从文案中提取的核心推广词（5-10 个）
  "tone": "紧迫感/社交证明/功能导向/情感共鸣/利益导向/恐惧驱动",
  "quality_assessment": "high/medium/low",  // 素材质量评估
  "recommended_action": ""  // 为了应对这个竞品策略，我们应该怎么做
}
```

### Prompt 2：周报聚合分析（用于最终报告生成）

```
你是一位资深手游市场分析师。以下是本周竞品 {COMPETITOR_NAME} 
在 Meta 广告平台的投放数据汇总：

## 原始数据
广告总数：{TOTAL_ADS}
素材类型分布：{AD_TYPE_DIST}
高频视觉元素 TOP10：{VISUAL_ELEMENTS}
高频文案关键词 TOP15：{KEYWORDS}
策略分布：{STRATEGIES}

## 需要你完成
基于以上数据，生成一份给投放团队阅读的竞品情报简报。

### 格式要求
使用以下结构：

【本周策略重点】
（2-3 句话概括）

【素材方向变化】
• 主要变化点
• 数据支撑

【值得关注的新动向】
• 具体发现
• 为什么值得关注

【团队行动建议】
• 建议 1（可执行的具体行动）
• 建议 2
• 建议 3

### 写作原则
1. 每条结论都要有数据支撑
2. 建议必须具体可执行
3. 语言简洁直接，适合晨会阅读
4. 总字数控制在 300-500 字
5. 中文输出
```

### Prompt 3：多竞品对比分析（进阶）

```
你是一位竞品策略分析师。以下是本周 {COUNTRY} 市场 
手游竞品广告投放数据对比：

## 竞品数据

{competitor1_name}（{competitor1_ads_count} 条活跃广告）：
- 素材类型：{competitor1_types}
- 核心关键词：{competitor1_keywords}
- 主要策略：{competitor1_strategies}

{competitor2_name}（{competitor2_ads_count} 条活跃广告）：
- 素材类型：{competitor2_types}
- 核心关键词：{competitor2_keywords}
- 主要策略：{competitor2_strategies}

## 分析要求
1. 制作一个竞品策略对比矩阵
2. 识别每个竞品的差异化打法
3. 指出市场空白点或机会点
4. 给出优先级排序的行动建议

用表格 + 文字说明的形式输出。
```

---

## 9. 附录 B：常见问题排查

### API 返回空数据

```
可能原因：
1. Token 过期 → 刷新长期 Token
2. search_terms 匹配不到 → 换用 page_id 查询
3. 竞品没有在该地区投放 → 更换 ad_reached_countries
4. 广告已被删除 → 不加 ad_active_status 过滤

快速诊断：
用 Facebook 官方的 Ad Library 网页版（https://www.facebook.com/ads/library/）
手动搜索确认竞品是否有活跃广告
```

### 请求被限流

```
- Meta API 速率：200 calls/hour/user（标准层）
- 解决方案：
  1. 每次请求用最大 limit=200
  2. 缓存结果，避免重复请求
  3. 多个竞品串行处理，间隔 1-2 秒
  4. 考虑申请更高 API 层级
```

### AI 分析结果不稳定

```
- 将分析 Prompt 中的 JSON 格式约束写得更严格
- 尝试让 AI 先思考再输出（chain-of-thought）
- 如果结构不稳定，用代码层做后处理解析
- 从 gpt-4o-mini 升级到 claude-sonnet 提升稳定性
```

### n8n 常见问题

```
- 环境变量加载失败：检查 docker run 的 -e 参数
- Webhook 收不到消息：检查防火墙和端口
- AI 节点报错：检查 API Key 和 endpoint URL
```

---

## 10. 附录 C：产出物清单

提交时请确保包含以下内容：

| # | 产出物 | 说明 |
|---|--------|------|
| 1 | **运行截图/录屏** | Agent 实际运行的全流程截图，必须能看到真实的数据输入和输出 |
| 2 | **架构说明** | 用了什么工具、各模块怎么连接、数据怎么流转 |
| 3 | **报告样例** | Agent 生成的一份真实竞品分析报告 |
| 4 | **当前局限** | 诚实说明现在能做到什么、做不到什么 |
| 5 | **后续优化计划** | 如果有更多时间/资源，你打算怎么改进 |

---

## 快速启动 Checklist

拿到这份指南后，按以下顺序执行：

- [ ] **第 1 步**：确定工具选型（推荐 n8n 或 Make）
- [ ] **第 2 步**：注册 Meta Developer 账号，获取 Token
- [ ] **第 3 步**：用浏览器/Postman 测试 Meta Ad Library API 是否通
- [ ] **第 4 步**：部署工具（n8n docker / Make 注册）
- [ ] **第 5 步**：搭建基础数据采集 → AI 分析 → 报告输出流程
- [ ] **第 6 步**：选 1 个竞品跑一次全流程，调通
- [ ] **第 7 步**：扩展到 3-5 个竞品
- [ ] **第 8 步**：设置自动调度
- [ ] **第 9 步**：配置推送渠道（飞书/Slack/邮件）
- [ ] **第 10 步**：写提交文档 + 录屏

---

> 遇到问题不知怎么推进？随时把报错信息或截图发给我，我来帮你调。
