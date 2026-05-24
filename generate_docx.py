#!/usr/bin/env python3
"""生成竞品分析Agent搭建指南 Word 文档"""

from docx import Document
from docx.shared import Inches, Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
import datetime

doc = Document()

# ── 全局样式 ──
style = doc.styles['Normal']
font = style.font
font.name = 'Arial'
font.size = Pt(11)
style.element.rPr.rFonts.set(qn('w:eastAsia'), 'SimSun')
style.paragraph_format.line_spacing = 1.35
style.paragraph_format.space_after = Pt(6)

# 标题样式
for i in range(1, 4):
    hs = doc.styles[f'Heading {i}']
    hs.font.name = 'Arial'
    hs.element.rPr.rFonts.set(qn('w:eastAsia'), 'SimHei')
    hs.font.color.rgb = RGBColor(0x1A, 0x56, 0xDB)
    hs.paragraph_format.space_before = Pt(18 if i == 1 else 12)
    hs.paragraph_format.space_after = Pt(8)

# ── Helper 函数 ──
def add_hint(doc, text):
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Cm(0.8)
    pf = p.paragraph_format
    pf.space_before = Pt(4)
    pf.space_after = Pt(4)
    run = p.add_run(f"\U0001f4a1 {text}")
    run.font.size = Pt(10)
    run.font.italic = True
    run.font.color.rgb = RGBColor(0x66, 0x66, 0x66)

def add_step(doc, number, title):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(6)
    run = p.add_run(f"Step {number}：{title}")
    run.bold = True
    run.font.size = Pt(12)
    run.font.color.rgb = RGBColor(0x2D, 0x2D, 0x2D)

def add_code_block(doc, code_text):
    for line in code_text.strip().split('\n'):
        p = doc.add_paragraph()
        p.paragraph_format.left_indent = Cm(1)
        p.paragraph_format.space_before = Pt(1)
        p.paragraph_format.space_after = Pt(1)
        run = p.add_run(line)
        run.font.name = 'Consolas'
        run.font.size = Pt(9)
        run.font.color.rgb = RGBColor(0x33, 0x33, 0x33)

def add_check(doc, text):
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Cm(0.5)
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(2)
    run = p.add_run(f"☐ {text}")
    run.font.size = Pt(11)

def add_prompt_box(doc, lines):
    """添加灰色背景的 Prompt 框"""
    for line in lines:
        if line == "":
            doc.add_paragraph("")
        else:
            p = doc.add_paragraph(line)
            p.paragraph_format.space_before = Pt(0)
            p.paragraph_format.space_after = Pt(2)
            p.paragraph_format.left_indent = Cm(0.5)
            for run in p.runs:
                run.font.size = Pt(9.5)
                run.italic = True

def add_table_row(table, cells_data, bold_first=True):
    row = table.add_row()
    for i, text in enumerate(cells_data):
        cell = row.cells[i]
        cell.text = ''
        p = cell.paragraphs[0]
        run = p.add_run(text)
        run.font.size = Pt(9)
        run.font.name = 'Arial'
        if bold_first and i == 0:
            run.bold = True

# ══════════════════════════════════════════
# 封面
# ══════════════════════════════════════════
doc.add_paragraph()
doc.add_paragraph()

title = doc.add_paragraph()
title.alignment = WD_ALIGN_PARAGRAPH.CENTER
for ch in "竞品广告素材分析 Agent 搭建全攻略":
    pass
run = title.add_run("竞品广告素材分析 Agent\n搭建全攻略")
run.bold = True
run.font.size = Pt(28)
run.font.color.rgb = RGBColor(0x1A, 0x56, 0xDB)

doc.add_paragraph()

subtitle = doc.add_paragraph()
subtitle.alignment = WD_ALIGN_PARAGRAPH.CENTER
run = subtitle.add_run("用你手头的 AI 工具（Claude Cowork / Claude Code / GPT / Gemini）\n从零搭一个竞品情报自动化系统")
run.font.size = Pt(13)
run.font.color.rgb = RGBColor(0x55, 0x55, 0x55)

doc.add_paragraph()

info = doc.add_paragraph()
info.alignment = WD_ALIGN_PARAGRAPH.CENTER
run = info.add_run(f"适用工具：Claude Cowork / Claude Code / GPT / Gemini\n生成日期：{datetime.date.today()}")
run.font.size = Pt(11)
run.font.color.rgb = RGBColor(0x88, 0x88, 0x88)

doc.add_page_break()

# ══════════════════════════════════════════
# 目录
# ══════════════════════════════════════════
doc.add_heading('目录', level=1)

toc_items = [
    "第一章：重新认识你的武器库 — 现有 AI 工具能做什么",
    "第二章：整体设计与数据流",
    "第三章：第一步 — 获取 Meta Ad Library API 访问权限",
    "第四章：第二步 — 用 Claude Code 写数据采集脚本",
    "第五章：第三步 — 手动跑采集 + AI 分析（跑通全流程）",
    "第六章：第四步 — 用 Claude Cowork 搭建自动化工作流",
    "第七章：第五步 — 把报告做得更好看",
    "第八章：第六步 — 测试、迭代、提交产出",
    "附录一：7 个可以直接用的 Prompt 模板",
    "附录二：Checklist — 跟着打勾就行",
]
for item in toc_items:
    p = doc.add_paragraph(item)
    p.paragraph_format.space_after = Pt(4)

doc.add_page_break()

# ══════════════════════════════════════════
# 第一章
# ══════════════════════════════════════════
doc.add_heading('第一章：重新认识你的武器库', level=1)

doc.add_paragraph(
    '在开始之前，先确认一下你手头的工具有多强大。'
    '虽然你没有 n8n、Make 这类低代码自动化平台，但你有的东西可能比它们更灵活。'
)

doc.add_heading('你手头有什么', level=2)

table = doc.add_table(rows=1, cols=3)
table.style = 'Light Grid Accent 1'
hdr = table.rows[0].cells
for i, h in enumerate(['工具', '能做什么', '在本方案中的角色']):
    hdr[i].text = ''
    p = hdr[i].paragraphs[0]
    run = p.add_run(h)
    run.bold = True
    run.font.size = Pt(10)

add_table_row(table, [
    "Claude Cowork\n（当前环境）",
    "• 运行 Python/bash 脚本\n• 读写文件\n• 网页搜索/抓取\n• 定时任务能力\n• AI 分析",
    "⭐ 核心编排器\n自动执行者 + 分析大脑"
])
add_table_row(table, [
    "Claude Code",
    "• 写/改 Python 脚本\n• 终端命令\n• Git 操作",
    "帮你写数据采集脚本\n调试 API 调用"
])
add_table_row(table, [
    "Claude / GPT / Gemini\n（聊天界面）",
    "• 长文本分析\n• 深度推理\n• 文档生成",
    "深度分析广告策略\n撰写报告\n交叉验证发现"
])

doc.add_paragraph()

doc.add_heading('核心思路：Claude Cowork 当总指挥', level=2)
doc.add_paragraph(
    'Claude Cowork 是你唯一一个同时具备"执行代码 + AI 思考 + 定时任务 + 输出文件"能力的工具。'
    '所以整条流水线以它为中心：'
)

doc.add_paragraph(
    '① Claude Code → 帮你写 Python 采集脚本\n'
    '② Claude Cowork → 定时运行脚本，拉取 Meta 广告数据\n'
    '③ Claude Cowork 的 AI → 分析广告数据，归类素材类型、抽取关键词\n'
    '④ Claude Cowork → 生成分析报告，保存到 outputs 文件夹\n'
    '⑤ 你每周打开文件夹就能看到最新报告'
)

add_hint(doc, '这整套流程不需要部署任何服务器，不需要买任何付费服务。全部在 Claude Cowork 的 Linux VM 内完成。你唯一需要的是注册一个免费的 Meta Developer 账号来获取 API Token。')

doc.add_page_break()

# ══════════════════════════════════════════
# 第二章
# ══════════════════════════════════════════
doc.add_heading('第二章：整体设计与数据流', level=1)

doc.add_heading('你要搭建的系统', level=2)

lines = [
    "               ┌───── 每周一打开 outputs 文件夹，看到最新报告 ─────┐",
    "               │                                                    │",
    "┌──────────────────────────└──────────────────────────┐",
    "│          Claude Cowork 定时任务（每周一自动运行）               │",
    "│  ① 运行 Python 脚本采集 Meta Ad Library 数据    │",
    "│  ② Claude AI 分析每条广告（素材类型、关键词、策略）   │",
    "│  ③ 聚合分析结果，生成结构化报告         │",
    "│  ④ 保存为 Markdown 文件到 outputs 文件夹    │",
    "└─────────────────────────────────────────────────┘"
]
for line in lines:
    p = doc.add_paragraph(line)
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(0)
    for run in p.runs:
        run.font.name = 'Consolas'
        run.font.size = Pt(9)

doc.add_paragraph()

doc.add_heading('数据流', level=2)
doc.add_paragraph(
    '竞品 App ID → Claude Cowork 定时任务触发\n'
    '  → bash: python3 collect_ads.py --competitor "Game Name"\n'
    '  → Python 调用 Meta Ad Library API\n'
    '  → 返回 JSON 数据，写入本地文件\n'
    '  → Claude 读取 JSON，逐条分析\n'
    '  → 聚合（素材类型分布、关键词 TOP、策略推测）\n'
    '  → 生成 Week_N_Competitor_Report.md\n'
    '  → 报告保存在 outputs 文件夹，你随时查看'
)

doc.add_page_break()

# ══════════════════════════════════════════
# 第三章
# ══════════════════════════════════════════
doc.add_heading('第三章：第一步 — 获取 Meta Ad Library API 权限', level=1)

doc.add_paragraph('这是整个项目的前提条件。没有 API Token 后面什么都做不了。预计耗时 20-30 分钟。')

add_step(doc, 1, '注册 Facebook Developer 账号')
doc.add_paragraph(
    '如果你已经有 Facebook 账号：\n'
    '① 打开 https://developers.facebook.com/\n'
    '② 用你的 Facebook 账号登录\n'
    '③ 点击右上角 "My Apps" → "Create App"\n'
    '④ 选择 "Business" 类型（不是 Consumer）\n'
    '⑤ 填写 App Name（随便写，比如 "Ad Analyzer"），联系邮箱填你的\n'
    '⑥ 创建完成后进入 Dashboard'
)
add_hint(doc, 'App Name 不会对外公开，随便写即可。')

add_step(doc, 2, '获取短期 Access Token（测试用）')
doc.add_paragraph(
    '① 左侧菜单 "Tools" → "Graph API Explorer"\n'
    '② Permissions 搜索添加：ads_read\n'
    '③ API Version 选 v19.0\n'
    '④ 点击 "Generate Access Token"，确认授权\n'
    '⑤ 复制 Token（以 EA 开头的长字符串）'
)
add_hint(doc, '这个 Token 有效期 1-2 小时。先用来测试 API，后面再换长期的。')

add_step(doc, 3, '测试 API（验证一切正常）')
doc.add_paragraph('在浏览器地址栏粘贴以下链接（替换 {TOKEN}）：')
add_code_block(doc,
    'https://graph.facebook.com/v19.0/ads_archive\n'
    '  ?search_terms="Last War"\n'
    '  &ad_type=ALL\n'
    '  &ad_reached_countries=["US"]\n'
    '  &fields=ad_creative_body,ad_creative_link_title,publisher_platforms,\n'
    '          ad_delivery_start_time,ad_snapshot_url\n'
    '  &limit=20\n'
    '  &access_token={YOUR_TOKEN}'
)
doc.add_paragraph('如果返回 JSON 数据（包含 data 数组），说明 API 通了！')
doc.add_paragraph(
    '如果无数据返回：\n'
    '• search_terms 不匹配 → 试着只搜品牌名的核心部分\n'
    '• Token 过期 → 重新生成\n'
    '• 没加 ads_read 权限 → 检查 Permissions'
)

add_step(doc, 4, '换取长期 Token（有效期 60 天）')
doc.add_paragraph('在 App Dashboard → Settings → Basic 找到 App Secret。然后用浏览器打开：')
add_code_block(doc,
    'https://graph.facebook.com/v19.0/oauth/access_token\n'
    '  ?grant_type=fb_exchange_token\n'
    '  &client_id={你的 App ID}\n'
    '  &client_secret={你的 App Secret}\n'
    '  &fb_exchange_token={短期 Token}'
)
doc.add_paragraph('返回的 JSON 中的 access_token 就是长期的。保存好，后续所有脚本都要用。')
add_hint(doc, '长期 Token 有效期 60 天。建议在手机日历设一个 55 天后的提醒来刷新。')

doc.add_page_break()

# ══════════════════════════════════════════
# 第四章
# ══════════════════════════════════════════
doc.add_heading('第四章：第二步 — 用 Claude Code 写采集脚本', level=1)

doc.add_paragraph(
    '目标：写一个 Python 脚本，它能接收竞品名称，调用 Meta API 拉取广告数据，'
    '保存为结构化的 JSON 文件。'
)

doc.add_heading('打开 Claude Code', level=2)
doc.add_paragraph(
    '在你的工作目录（或新建一个文件夹），在终端运行 claude 命令启动 Claude Code。'
)
add_code_block(doc, 'cd your_project_dir\nclaude')

doc.add_heading('让 Claude Code 写脚本', level=2)
doc.add_paragraph('在 Claude Code 的对话框中，直接输入以下 Prompt：')

prompt_lines = [
    "你是一个 Python 爬虫工程师。帮我写一个脚本 collect_ads.py，功能如下：",
    "",
    "1. 命令行参数：--name（竞品名）、--page-id（可选）、--token（Meta Token）、--output（输出路径，默认 ./data）",
    "",
    "2. 调用 Facebook Graph API v19.0 /ads_archive 端点，查询该竞品最近 90 天的广告",
    "   fields：ad_creative_body, ad_creative_link_title, ad_creative_link_description,",
    "   ad_delivery_start_time, ad_snapshot_url, ad_active_status, publisher_platforms, spend, impressions",
    "   limit=100，处理分页，ad_reached_countries=[\"US\"]",
    "   search_terms 用 --name 参数的值",
    "",
    "3. 数据清洗：",
    "   - publisher_platforms 数组转字符串",
    "   - spend/impressions 范围值取平均",
    "   - 过滤 ad_creative_body 为空的数据",
    "   - 按 ad_snapshot_url 去重",
    "",
    "4. 输出：保存为 JSON 文件，打印摘要统计",
    "5. 错误处理：处理 API 错误、429 限流时等待重试",
    "使用 requests 库，直接生成完整可运行代码。"
]
add_prompt_box(doc, prompt_lines)

doc.add_paragraph()
doc.add_paragraph('Claude Code 生成脚本后，检查确认：')
add_check(doc, '脚本开头有 import requests, json, argparse, os, datetime')
add_check(doc, '有 API 分页处理逻辑（paging.next 循环）')
add_check(doc, '有去重逻辑和错误重试')
add_check(doc, '输出文件名包含日期')

doc.add_heading('安装依赖并测试', level=2)
add_code_block(doc, 'pip install requests --break-system-packages')
doc.add_paragraph('然后用你的长期 Token 做一次测试：')
add_code_block(doc,
    'python collect_ads.py \\\n'
    '  --name "Last War" \\\n'
    '  --token "EAxxxxxxx" \\\n'
    '  --output ./data'
)
doc.add_paragraph('如果跑通，会看到类似输出：')
add_code_block(doc,
    '=== 采集完成 ===\n'
    '竞品: Last War\n'
    '共抓取: 87 条广告\n'
    '活跃广告: 45 条\n'
    '数据已保存: ./data/Last_War_ads_20260524.json'
)

doc.add_heading('找不到竞品的 Facebook Page ID？', level=2)
doc.add_paragraph(
    '方法一：在 Facebook 官网搜索竞品品牌名，进入官方主页，URL 中的数字串就是 Page ID。\n\n'
    '方法二：用 Graph API 搜索：'
)
add_code_block(doc,
    'https://graph.facebook.com/v19.0/pages/search\n'
    '  ?q=Last+War\n'
    '  &access_token={YOUR_TOKEN}'
)

add_hint(doc, '如果不是特别大的品牌，也可以只用 search_terms 参数，不传 page_id 也能搜到广告。两种方式各有优劣，page_id 更精确，search_terms 覆盖更广。')

doc.add_page_break()

# ══════════════════════════════════════════
# 第五章
# ══════════════════════════════════════════
doc.add_heading('第五章：第三步 — 手动跑采集 + AI 分析', level=1)

doc.add_paragraph('脚本写好了。先手动跑一次全流程，确认每步都走得通。')

add_step(doc, 1, '采集真实数据')
doc.add_paragraph('选择你关注的竞品运行脚本：')
add_code_block(doc,
    '# 采集竞品 A\n'
    'python collect_ads.py --name "Last War" --token "EAxxx" --output ./data\n\n'
    '# 采集竞品 B\n'
    'python collect_ads.py --name "Monopoly Go" --token "EAxxx" --output ./data'
)
doc.add_paragraph('检查 JSON 文件是否正常生成：')
add_code_block(doc, 'ls -la ./data/')

add_step(doc, 2, '用 AI 分析数据')
doc.add_paragraph('将 JSON 数据复制到 Claude（或 GPT），使用以下 Prompt：')

prompt_lines2 = [
    "你是一个手游广告策略分析师。下面是一个竞品最近 90 天在 Meta 平台投放的广告数据。",
    "",
    "【数据】",
    "{把 JSON 数据粘贴在这里}",
    "",
    "请完成以下分析：",
    "1. 素材类型分布（视频/图片/轮播/纯文字各占比多少）",
    "2. 文案关键词 TOP 10（提取高频推广词）",
    "3. 核心卖点归纳（福利？玩法？社交？）",
    "4. 情感诉求分析（紧迫感？社交证明？娱乐性？）",
    "5. 推测的投放策略（基于投放时间和文案风格）",
    "6. 值得关注的广告案例（2-3 条）",
    "",
    "输出格式：先文字分析，再汇总为 JSON。"
]
add_prompt_box(doc, prompt_lines2)

add_hint(doc, '如果数据量太大（超过 30 条），可以分批分析，每批 20-30 条，最后再让 AI 帮你聚合。')

add_step(doc, 3, '生成周报')
doc.add_paragraph('分析出结果后，让 AI 帮你生成一份给团队的简报：')

prompt_lines3 = [
    "基于你的分析结果，请生成一份给投放团队的竞品情报简报，要求：",
    "",
    "【本周策略重点】",
    "（2-3 句话概括竞品核心打法）",
    "",
    "【素材方向变化】",
    "• 变化点（有数据支撑）",
    "",
    "【值得关注的新动向】",
    "",
    "【团队行动建议】",
    "• 建议 1（具体可执行）",
    "• 建议 2",
    "• 建议 3",
    "",
    "原则：每条结论都有数据支撑，语言简洁直接，适合晨会阅读。"
]
add_prompt_box(doc, prompt_lines3)

doc.add_page_break()

# ══════════════════════════════════════════
# 第六章
# ══════════════════════════════════════════
doc.add_heading('第六章：第四步 — 用 Claude Cowork 搭建自动化工作流', level=1)

doc.add_paragraph(
    '手动跑通之后，现在把整套流程交给 Claude Cowork 来自动执行。\n'
    '这是整个方案的核心：利用 Cowork 的定时任务 + 代码执行 + AI 分析能力。'
)

doc.add_heading('Step 1：准备文件', level=2)
doc.add_paragraph('在你的工作目录准备好以下文件：')
add_check(doc, 'collect_ads.py — 数据采集脚本（第四章已生成）')
add_check(doc, 'config.json — 竞品配置和 Token')

doc.add_paragraph()
doc.add_paragraph('创建 config.json：')
add_code_block(doc,
    '{\n'
    '  "meta_token": "EAxxxxxxxxxxxxxxxxxxxxxxxxxxx",\n'
    '  "competitors": [\n'
    '    {"name": "Last War", "app_id": "com.lastwar.game", "country": "US"},\n'
    '    {"name": "Monopoly Go", "app_id": "com.monopolygo.game", "country": "US"},\n'
    '    {"name": "Whiteout Survival", "app_id": "com.whiteout.survival", "country": "US"}\n'
    '  ],\n'
    '  "output_dir": "./reports"\n'
    '}'
)

doc.add_heading('Step 2：写主控脚本 run_weekly.py', level=2)
doc.add_paragraph('在 Claude Code 中用以下 Prompt 生成：')

prompt_lines4 = [
    "写一个 Python 脚本 run_weekly.py：",
    "1. 读取 config.json 获取竞品列表和 Token",
    "2. 遍历 competitors，对每个竞品：",
    "   a. subprocess.run 调用 collect_ads.py",
    "   b. 读取输出的 JSON 文件",
    "3. 本地统计分析（不用外部 API）：",
    "   - 按 publisher_platforms 统计平台分布",
    "   - 按 ad_active_status 统计活跃/非活跃",
    "   - collections.Counter 统计高频词",
    "4. 生成汇总 Markdown 报告",
    "5. 打印报告保存路径"
]
add_prompt_box(doc, prompt_lines4)

doc.add_heading('Step 3：在 Claude Cowork 中创建定时任务', level=2)
doc.add_paragraph('回到 Claude Cowork 对话界面，使用 schedule 技能。执行以下步骤：')

doc.add_paragraph('① 输入 /schedule 或直接输入：')
p = doc.add_paragraph()
p.paragraph_format.left_indent = Cm(0.5)
run = p.add_run('"帮我创建一个每周一早上 9 点运行的定时任务，用于竞品广告分析"')
run.font.size = Pt(10)
run.italic = True

doc.add_paragraph()
doc.add_paragraph('② 在任务 Prompt 中填写以下内容（这是一份完整的任务指令）：')

task_prompt_lines = [
    "你现在是一个竞品广告分析系统。你的任务：",
    "",
    "【数据采集】",
    "1. 运行 python3 ./data/run_weekly.py 采集本周竞品广告数据",
    "2. 读取生成的 JSON 文件",
    "",
    "【AI 分析】",
    "对每个竞品的数据：",
    "3. 分析素材类型分布",
    "4. 提取文案高频关键词 TOP 10",
    "5. 提炼核心卖点和情感诉求",
    "6. 推测投放策略",
    "7. 选出 2-3 条值得关注的广告",
    "",
    "【报告生成】",
    "8. 生成结构化周报：竞品策略对比 + 各竞品详细分析 + 建议",
    "9. 保存为 Week_{周数}_Competitor_Report.md",
    "",
    "【输出要求】",
    "- 中文报告",
    "- 每条结论有数据支撑",
    "- 行动建议具体可执行"
]
add_prompt_box(doc, task_prompt_lines)

doc.add_paragraph()
add_hint(doc, '创建定时任务后，第一次可以手动触发测试。如果跑通了，后续每周一它会自动运行，你到 outputs 文件夹看报告就行。')

doc.add_page_break()

# ══════════════════════════════════════════
# 第七章
# ══════════════════════════════════════════
doc.add_heading('第七章：第五步 — 把报告做得更好看', level=1)

doc.add_paragraph(
    '目前定时任务生成的是 Markdown 格式报告。想让团队看得更爽，可以进一步优化。'
)

doc.add_heading('方案一：让 Claude 转换为 PPT 大纲', level=2)
doc.add_paragraph('把 Markdown 报告粘贴到 Claude/GPT，用这个 Prompt：')
prompt_lines5 = [
    "以下是一份竞品广告分析报告，请转换为 6-8 页的 PPT 大纲：",
    "",
    "{报告内容}",
    "",
    "要求：每页一个标题 + 3-5 个要点，每要点不超过 30 字，",
    "标注每页的配图建议。"
]
add_prompt_box(doc, prompt_lines5)

doc.add_heading('方案二：用 Claude Code 生成可视化 HTML 看板', level=2)
doc.add_paragraph('在 Claude Code 中使用这个 Prompt：')
prompt_lines6 = [
    "我有竞品广告分析数据（JSON），生成单 HTML 文件的可视化看板：",
    "- 使用 Chart.js CDN",
    "- 素材类型分布饼图、关键词柱状图",
    "- 简洁美观，适合团队内部共享"
]
add_prompt_box(doc, prompt_lines6)

doc.add_page_break()

# ══════════════════════════════════════════
# 第八章
# ══════════════════════════════════════════
doc.add_heading('第八章：第六步 — 测试、迭代、提交产出', level=1)

doc.add_heading('三轮测试计划', level=2)

doc.add_paragraph('第一轮：单次手动验证（30 分钟）')
add_check(doc, '选择 1 个竞品，运行 python3 collect_ads.py')
add_check(doc, '检查 JSON 输出字段是否齐全')
add_check(doc, '把数据贴到 Claude 做一轮人工分析')
add_check(doc, '调整 Prompt 直到分析结果合理')

doc.add_paragraph()
doc.add_paragraph('第二轮：全量运行（1 小时）')
add_check(doc, '扩展到 3-5 个竞品')
add_check(doc, '运行 run_weekly.py 全量采集')
add_check(doc, '检查报告可读性和完整性')

doc.add_paragraph()
doc.add_paragraph('第三轮：定时任务测试（30 分钟）')
add_check(doc, '在 Claude Cowork 中手动触发定时任务')
add_check(doc, '观察任务是否完整执行')
add_check(doc, '检查 outputs 文件夹是否生成报告')

doc.add_heading('迭代方向（有时间再做）', level=2)

table2 = doc.add_table(rows=1, cols=3)
table2.style = 'Light Grid Accent 1'
hdr = table2.rows[0].cells
for i, h in enumerate(['迭代方向', '优先级', '怎么做']):
    hdr[i].text = ''
    p = hdr[i].paragraphs[0]
    run = p.add_run(h)
    run.bold = True
    run.font.size = Pt(10)

add_table_row(table2, ["TikTok 数据接入", "⭐⭐⭐", "手动从 TikTok Creative Center 补充"])
add_table_row(table2, ["素材截图分析", "⭐⭐⭐", "下载 ad_snapshot_url 图片，传给 Claude Vision"])
add_table_row(table2, ["周同比趋势", "⭐⭐", "缓存上周数据做对比"])
add_table_row(table2, ["多竞品对比矩阵", "⭐⭐", "3 个以上竞品并列对比"])

doc.add_paragraph()

doc.add_heading('提交产出清单', level=2)
doc.add_paragraph('最终提交时包含以下内容：')
add_check(doc, '实际运行截图或录屏（必须能看到真实数据输入和输出）')
add_check(doc, '工具说明（用了 Claude Code / Cowork / GPT 哪些工具、怎么用的）')
add_check(doc, '一份真实的竞品分析报告（Agent 产出的原稿）')
add_check(doc, '当前局限说明（现在做到了什么、还差什么）')
add_check(doc, '后续优化计划（下一步打算怎么补）')

doc.add_page_break()

# ══════════════════════════════════════════
# 附录一
# ══════════════════════════════════════════
doc.add_heading('附录一：7 个可以直接用的 Prompt 模板', level=1)

prompts_data = [
    ("Prompt 1：让 Claude Code 写采集脚本",
     "在 Claude Code 中执行",
     "你是一个 Python 爬虫工程师。帮我写一个 Python 脚本 collect_ads.py，调用 Facebook Graph API v19.0 的 /ads_archive 端点拉取竞品广告数据。输入参数：--name（竞品名）、--token、--output。API 参数：fields 包括 ad_creative_body、ad_creative_link_title、ad_delivery_start_time、ad_snapshot_url、ad_active_status、publisher_platforms、spend、impressions。limit=100，处理分页，使用 requests 库。"),

    ("Prompt 2：单条广告分析",
     "在 Claude/GPT 中执行，传入单条广告数据",
     "你是一个广告创意分析专家。分析以下游戏广告数据：文案：{body}，标题：{title}，投放平台：{platforms}。请输出 JSON：ad_type, creative_strategy, target_audience, call_to_action, copy_keywords, tone, quality_assessment。"),

    ("Prompt 3：批量数据聚合分析",
     "在 Claude/GPT 中执行，传入全部广告 JSON",
     "你是一个手游广告策略分析师。以下是竞品 {name} 最近 90 天的广告数据。请分析：1.素材类型分布 2.高频关键词 TOP10 3.核心卖点 4.情感诉求分布 5.推测投放策略 6.值得关注的广告案例。输出文字分析 + JSON 汇总。"),

    ("Prompt 4：周报生成",
     "在 Claude/GPT 中执行",
     "基于以下竞品广告分析结果，生成一份给投放团队的竞品情报简报。格式：【本周策略重点】【素材方向变化】【值得关注的新动向】【团队行动建议】。每条结论要有数据支撑，语言简洁。"),

    ("Prompt 5：素材截图分析（Vision）",
     "在 Claude/GPT（支持图片）中执行",
     "分析这张游戏广告图片：1.画面主体元素 2.色彩风格 3.文字内容 4.广告类型（玩法展示/角色展示/活动公告）。输出 JSON 格式。"),

    ("Prompt 6：多竞品对比",
     "在 Claude/GPT 中执行",
     "以下是本周 3 个竞品的广告投放数据，请制作策略对比矩阵，识别差异化打法，指出机会点，给出行动建议。"),

    ("Prompt 7：HTML 可视化看板",
     "在 Claude Code 中执行",
     "我有竞品广告分析数据（JSON），生成单 HTML 文件的可视化看板，使用 Chart.js CDN。包含饼图、柱状图，简洁美观。"),
]

for title, context, prompt_text in prompts_data:
    doc.add_heading(title, level=2)
    p = doc.add_paragraph()
    run = p.add_run(f"✦ {context}")
    run.bold = True
    run.font.size = Pt(10)
    p2 = doc.add_paragraph()
    p2.paragraph_format.left_indent = Cm(0.5)
    run2 = p2.add_run(prompt_text)
    run2.font.size = Pt(9.5)
    run2.italic = True
    doc.add_paragraph()

doc.add_page_break()

# ══════════════════════════════════════════
# 附录二
# ══════════════════════════════════════════
doc.add_heading('附录二：Checklist — 跟着打勾就行', level=1)

doc.add_paragraph('把下面的清单打出来或存下来，做一项勾一项 ☑，不容易漏。')

sections = [
    ("❖ 准备阶段", [
        "注册 Meta Developer 账号",
        "创建 App，获取 App ID 和 App Secret",
        "获取短期 Token，测试 API 返回数据",
        "换取长期 Token（60 天有效）",
        "确认至少 3 个竞品名称",
    ]),
    ("❖ 脚本搭建阶段", [
        "用 Claude Code 生成 collect_ads.py",
        "测试 collect_ads.py 运行成功",
        "创建 config.json 配置文件",
        "生成 run_weekly.py 主控脚本",
        "测试 run_weekly.py 全流程跑通",
    ]),
    ("❖ 分析验证阶段", [
        "采集 1 个竞品数据，粘贴到 Claude 分析",
        "验证分析结果是否合理",
        "调整 Prompt 直到输出稳定",
        "扩展到 3 个竞品",
    ]),
    ("❖ 自动化阶段", [
        "在 Claude Cowork 创建定时任务",
        "手动触发一次测试",
        "确认 outputs 文件夹生成报告",
        "确认报告内容完整",
    ]),
    ("❖ 提交阶段", [
        "录制全流程运行截图/录屏",
        "写工具使用说明",
        "整理一份真实产出的竞品报告",
        "列出局限和后续计划",
        "提交所有产出物",
    ]),
]

for section_title, items in sections:
    doc.add_heading(section_title, level=2)
    for item in items:
        add_check(doc, item)
    doc.add_paragraph()

# ── 结尾 ──
doc.add_paragraph()
p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
run = p.add_run('— END —')
run.font.color.rgb = RGBColor(0xAA, 0xAA, 0xAA)
run.font.size = Pt(14)

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
run = p.add_run(f'生成日期：{datetime.date.today()}  │  有问题随时问我')
run.font.color.rgb = RGBColor(0xAA, 0xAA, 0xAA)
run.font.size = Pt(10)

# ── 保存 ──
output_path = '/sessions/funny-gracious-pascal/mnt/outputs/竞品分析Agent搭建攻略.docx'
doc.save(output_path)
print(f"✅ 文档已生成: {output_path}")
