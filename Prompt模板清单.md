# Prompt 模板清单 — 竞品广告分析 Agent

> 可直接复制使用的 Prompt 模板。
> 使用时将 `{占位符}` 替换为实际数据。

---

## 一、单条广告分析 Prompt（供工作流的 AI 节点使用）

```markdown
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
  "ad_type": "video/image/carousel/text/interactive",
  "creative_strategy": "",
  "target_audience": "",
  "emotional_appeal": "urgency/social_proof/functional/emotional/benefit",
  "call_to_action": "",
  "unique_selling_point": "",
  "visual_keywords": [],
  "copy_keywords": [],
  "tone": "紧迫感/社交证明/功能导向/情感共鸣/利益导向/恐惧驱动",
  "quality_assessment": "high/medium/low",
  "recommended_action": ""
}
```

> PS: 如果是在 n8n/Make 中调用，将 `{占位符}` 替换为工作流的变量引用语法
```

---

## 二、聚合分析 Prompt（多条广告 → 策略洞察）

```markdown
你是一个手游广告策略分析师。

以下是本周竞品 {COMPETITOR_NAME} 在 Meta 平台的广告投放数据汇总：

## 基础数据
- 抓取的活跃广告总数：{TOTAL_ADS}
- 数据周期：{START_DATE} ~ {END_DATE}

## 广告数据列表
{ADS_DATA}

## 分析要求
请从以下维度进行分析，以 JSON 格式输出：

{
  "overall_strategy": "本周竞品的核心策略是什么，50 字以内",
  "strategy_shift": "与上一期相比是否有策略变化，重点说明变化方向",
  "ad_type_breakdown": {
    "video": {"count": 0, "percentage": 0},
    "image": {"count": 0, "percentage": 0},
    "carousel": {"count": 0, "percentage": 0},
    "text": {"count": 0, "percentage": 0}
  },
  "top_copy_keywords": [{"keyword": "", "frequency": 0, "example_ad": ""}],
  "top_visual_elements": [{"element": "", "frequency": 0}],
  "dominant_tones": [{"tone": "", "ads_count": 0}],
  "noteworthy_ads": [
    {
      "body": "广告文案前 100 字",
      "why_noteworthy": "为什么这条广告值得关注",
      "inferred_strategy": "推测的策略目的"
    }
  ],
  "team_recommendations": [
    "建议 1：具体说明",
    "建议 2：具体说明",
    "建议 3：具体说明"
  ]
}
```

---

## 三、周报生成 Prompt（最终输出给团队的版本）

```markdown
你是一位资深手游市场分析师。以下是本周竞品 {COMPETITOR_NAME} 
在 Meta 广告平台的投放数据汇总：

素材类型分布：{AD_TYPE_DIST}
高频视觉元素 TOP10：{VISUAL_ELEMENTS}
高频文案关键词 TOP15：{KEYWORDS}
策略分布：{STRATEGIES}
抓取广告总数：{TOTAL_COUNT}

请生成一份投放团队晨会可用的竞品情报简报，使用以下结构：

---

【本周策略重点】
（2-3 句话概括竞品核心打法）

【素材方向变化】
• 变化 1（数据支撑）
• 变化 2（数据支撑）

【值得关注的新动向】
• 发现 + 为什么值得关注

【团队行动建议】
• 建议 1（具体可执行）
• 建议 2（具体可执行）
• 建议 3（具体可执行）

---

写作原则：
1. 每条结论都要有数据支撑
2. 建议必须具体可执行
3. 语言简洁直接，适合晨会阅读
4. 总字数控制在 300-500 字
5. 中文输出
```

---

## 四、Meta API 测试 Prompt（在 Claude/Cursor 中运行）

```markdown
你是一个 API 调试助手。

帮我生成 curl 命令来测试 Facebook Ad Library API。

需要的参数：
- App ID: {YOUR_APP_ID}
- Access Token: {YOUR_TOKEN}
- 竞品名称: {COMPETITOR_NAME}（例如 "Last War"）
- 地区: US

需要生成以下 3 个测试命令：

1. 搜索竞品的 Facebook Page ID
2. 查询该竞品最近的活跃广告（前 50 条）
3. 查询该竞品指定时间范围内的所有广告

对每个命令，请说明：
- 预期输出结构
- 常见错误及解决方法
- 最小化请求的方法（避免浪费 API 配额）
```

---

## 五、素材截图分析 Prompt（进阶 — 调用 Claude Vision）

```markdown
分析这张游戏广告图片，请识别以下内容：

1. 画面主体元素（角色/场景/UI/文字/特效）
2. 色彩风格和色调
3. 文字内容与排版方式
4. 广告类型（玩法展示/角色展示/活动公告/激励视频/社交证明）

输出格式：
{
  "main_elements": [{"element": "描述", "prominence": "high/medium/low"}],
  "color_palette": ["主要颜色1", "主要颜色2"],
  "text_overlay": "图片上的文字内容",
  "text_position": "top/middle/bottom/fullscreen",
  "ad_subtype": "玩法展示/角色展示/活动公告/激励视频/社交证明/其他",
  "quality_impression": "high/medium/low",
  "would_click": true/false,
  "why": "原因说明"
}
```

---

## 六、多竞品对比分析 Prompt（进阶）

```markdown
你是一位竞品策略分析师。以下是本周 {COUNTRY} 市场手游竞品广告投放数据对比：

## 竞品对比数据

| 维度 | {COMP_A} | {COMP_B} | {COMP_C} |
|------|----------|----------|----------|
| 活跃广告数 | {a_count} | {b_count} | {c_count} |
| 主要素材类型 | {a_types} | {b_types} | {c_types} |
| 核心关键词 | {a_kws} | {b_kws} | {c_kws} |
| 主要策略 | {a_strats} | {b_strats} | {c_strats} |

## 分析要求

1. 制作竞品策略对比矩阵
2. 识别每个竞品的差异化打法
3. 指出市场空白点或机会点
4. 给出优先级排序的行动建议

请用以下结构输出：
1. 策略对比表
2. 各竞品核心打法（各 2-3 句话）
3. 机会点分析
4. 建议优先级排序
```

---

## 七、浏览器自动化采集 Prompt（TikTok 数据）

```markdown
你是爬虫专家，用 Python + Playwright 实现以下功能：

1. 打开 TikTok Creative Center (https://ads.tiktok.com/business/creativecenter/)
2. 在搜索框输入关键词 "{竞品名称}"
3. 等待搜索结果加载（最多 10 秒）
4. 抓取前 20 条广告的以下信息：
   - 广告文案 (ad_text)
   - 视频时长 (video_duration)
   - 点赞数 (likes_count)
   - 投放地区 (delivery_locations)
5. 输出为 CSV 文件保存到 outputs/ 目录

注意：
- 如果出现登录弹窗，尝试点击关闭按钮
- 添加随机的 User-Agent
- 每次请求间隔 2-3 秒
- 用 try-catch 处理元素定位失败的情况
- 输出完整的错误日志
```

---

## 快速使用指南

| 场景 | 用哪个 Prompt | 调用位置 |
|------|---------------|----------|
| 测试 API 是否通 | Prompt 4 | Claude/Cursor 对话 |
| 分析单条广告 | Prompt 1 | n8n AI 节点 / Make / 代码 |
| 聚合多条广告出洞察 | Prompt 2 | n8n AI 节点 / Make / 代码 |
| 生成最终周报 | Prompt 3 | 最终输出前的 AI 调用 |
| 分析素材截图 | Prompt 5 | Claude Vision / GPT-4V |
| 多竞品对比 | Prompt 6 | 周报增强版 |
| 采集 TikTok 数据 | Prompt 7 | Python 脚本 |
