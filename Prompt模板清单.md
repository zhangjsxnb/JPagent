# Prompt 模板清单 — 竞品广告分析 Agent

> 可直接复制使用的 Prompt 模板。
> 使用时将 `{占位符}` 替换为实际数据。

---

## 一、精准微观情报检索 Prompt（替换旧版宏观搜索）

```markdown
你是竞品广告素材情报分析师。

请对以下竞品进行精准微观情报检索，**禁止搜索任何宏观数据**（收入、下载量、市场份额等）。

## 竞品信息
- 竞品名称：{COMPETITOR_NAME}
- 搜索语言：中文 + 英文

## 强制检索方向（必须全部执行）

### 1. 广告文案素材搜索
搜索以下关键词组合，寻找真实的广告文案案例：
- `"{COMPETITOR_NAME}" ad copy examples`
- `"{COMPETITOR_NAME}" 广告文案 拆解`
- `"{COMPETITOR_NAME}" creative strategy ads`

### 2. 素材套路分析平台搜索
在以下素材情报平台站内搜索：
- `site:appgrowing.net {COMPETITOR_NAME}`
- `site:socialpeta.com {COMPETITOR_NAME}`

### 3. 投放策略线索搜索
- `"{COMPETITOR_NAME}" retargeting strategy`
- `"{COMPETITOR_NAME}" UA strategy 2025`

### 4. 最新素材变化搜索
- `"{COMPETITOR_NAME}" new ad creative 2025`
- `"{COMPETITOR_NAME}" latest ad campaign`

## 输出格式
请将搜索结果整理为以下 JSON：

{
  "game_name": "{COMPETITOR_NAME}",
  "search_date": "YYYY-MM-DD",
  "found_ad_count": 0,
  "ad_types_inferred": {
    "video": {"count": 0, "percentage": 0},
    "image": {"count": 0, "percentage": 0},
    "carousel": {"count": 0, "percentage": 0},
    "text": {"count": 0, "percentage": 0}
  },
  "copy_keywords": [{"keyword": "", "frequency": 0, "source_url": ""}],
  "visual_elements_inferred": ["元素1", "元素2"],
  "emotional_appeal_inferred": {"诉求类型": "强度百分比"},
  "strategy_inferred": "基于素材文本描述的推测策略",
  "noteworthy_ads": [
    {"source": "来源", "copy_excerpt": "文案片段", "analysis": "分析"}
  ],
  "sources": ["来源URL1", "来源URL2"]
}

## 规则
1. 所有数据必须基于搜索到的文本信息合理推算
2. 标注每条数据的来源URL
3. 没有搜到就如实标注"未找到"，不要编造
4. 禁止编造具体的广告文案内容
```

---

## 二、聚合分析 Prompt（多条广告 → 策略洞察）

```markdown
你是一个手游广告策略分析师。

以下是本周竞品 {COMPETITOR_NAME} 的广告投放数据汇总：

## 基础数据
- 分析周期：{START_DATE} ~ {END_DATE}
- 素材数据来源：WebSearch 公开情报检索

## 结构化数据
{STRUCTURED_DATA}

## 分析要求
请从以下维度进行分析，以 JSON 格式输出：

{
  "overall_strategy": "本周竞品的核心素材策略是什么，50 字以内",
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
的广告素材情报汇总：

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
2. 建议必须具体可执行，聚焦素材层面
3. 语言简洁直接，适合晨会阅读
4. 总字数控制在 300-500 字
5. 中文输出
```

---

## 四、素材截图视觉分析 Prompt（对接多模态模型）

```markdown
分析这张游戏广告图片/视频封面，请识别以下内容：

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

## 五、多竞品对比分析 Prompt

```markdown
你是一位竞品策略分析师。以下是本周手游竞品广告素材对比数据：

## 竞品对比数据

| 维度 | {COMP_A} | {COMP_B} | {COMP_C} |
|------|----------|----------|----------|
| 活跃广告数 | {a_count} | {b_count} | {c_count} |
| 主要素材类型 | {a_types} | {b_types} | {c_types} |
| 核心关键词 | {a_kws} | {b_kws} | {c_kws} |
| 主要策略 | {a_strats} | {b_strats} | {c_strats} |

## 分析要求

1. 制作竞品素材策略对比矩阵
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

## 快速使用指南

| 场景 | 用哪个 Prompt | 调用位置 |
|------|---------------|----------|
| 每周定时检索素材情报 | Prompt 1 | 定时任务 Agent 第二步 |
| 聚合多条素材出洞察 | Prompt 2 | 数据汇总后的 AI 分析 |
| 生成最终团队周报 | Prompt 3 | 最终输出前的 AI 调用 |
| 分析素材截图 | Prompt 4 | Claude Vision / GPT-4V / Gemini |
| 多竞品对比 | Prompt 5 | 周报增强版 |

## 搜索关键词速查表

| 目标 | 搜索模板 |
|------|----------|
| 广告文案案例 | `"{竞品名}" ad copy` / `"{竞品名}" 广告文案` |
| 素材套路平台 | `site:appgrowing.net {竞品名}` / `site:socialpeta.com {竞品名}` |
| 投放策略推断 | `"{竞品名}" UA strategy` / `"{竞品名}" retargeting` |
| 最新素材变化 | `"{竞品名}" new creative` / `"{竞品名}" latest ad` |
