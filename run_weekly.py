#!/usr/bin/env python3
"""
run_weekly.py — 全量流水线入口脚本

执行流程：
  1. 确认运行环境与项目完整性
  2. 读取 data/ 下各竞品分析 JSON
  3. 生成多竞品对比分析报告 (data/comparison_report.md)
  4. 自动调用 auto_push.py 推送到 GitHub → Vercel 自动部署

用法：
  python run_weekly.py
"""

import subprocess
import sys
import os
import json
from datetime import date
from pathlib import Path


def step(msg: str):
    print(f"[{date.today()}] {msg}")


def load_json(path: str) -> dict | None:
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        step(f"  读取失败 {Path(path).name}: {e}")
        return None


def fmt_pct(val: float) -> str:
    return f"{val:.1f}%"


def generate_comparison_report(data_dir: str, index_html: str) -> str:
    """
    聚合所有竞品分析 JSON，生成多竞品对比分析报告。
    语义对齐 Prompt模板清单.md 中的【五、多竞品对比分析 Prompt】。
    """
    # 扫描 data/ 下所有 *_analysis.json 文件
    json_files = sorted(Path(data_dir).glob("*_analysis.json"))

    records = []
    for f in json_files:
        record = load_json(str(f))
        if record:
            records.append(record)

    if not records:
        step("  ⚠️ 未找到有效的竞品分析数据，跳过对比报告")
        return ""

    today = date.today().isoformat()
    lines = []
    lines.append(f"# 多竞品对比分析报告 — {today}\n")
    lines.append(f"> 基于 {len(records)} 个竞品的广告素材情报聚合生成\n")
    lines.append("---\n")

    # ── 策略对比表 ──
    lines.append("## 1. 竞品策略对比矩阵\n")
    lines.append("| 维度 | " + " | ".join(r["game_name"] for r in records) + " |")
    lines.append("|" + "|".join("------" for _ in range(len(records) + 1)) + "|")

    # 广告总量
    row = "| 广告总量 "
    for r in records:
        row += f"| {r.get('total_ads_analyzed', 'N/A')} "
    lines.append(row + "|")

    # 主要素材类型
    row = "| 主要素材类型 "
    for r in records:
        ad_types = r.get("ad_type_distribution", {})
        # 取占比最高的类型
        best = max(ad_types.items(), key=lambda x: x[1].get("percentage", 0) if isinstance(x[1], dict) else 0)
        label = best[0]
        pct = best[1].get("percentage", 0) if isinstance(best[1], dict) else 0
        row += f"| {label}({fmt_pct(pct)}) "
    lines.append(row + "|")

    # 核心关键词（取前 3）
    row = "| 核心关键词 "
    for r in records:
        kws = r.get("top_keywords", [])
        top3 = ", ".join(k["keyword"] for k in kws[:3]) if kws else "N/A"
        row += f"| {top3} "
    lines.append(row + "|")

    # 主要策略
    row = "| 主要策略 "
    for r in records:
        strats = r.get("creative_strategies", [])
        top = strats[0] if strats else "N/A"
        if isinstance(top, dict):
            top = top.get("name", str(top))
        row += f"| {top} "
    lines.append(row + "|")

    # 核心受众
    row = "| 核心受众 "
    for r in records:
        row += f"| {r.get('target_audience', 'N/A')} "
    lines.append(row + "|")

    # 预算
    row = "| 预估预算 "
    for r in records:
        row += f"| {r.get('budget_estimate', 'N/A')} "
    lines.append(row + "|")

    lines.append("")

    # ── 各竞品核心打法 ──
    lines.append("---\n")
    lines.append("## 2. 各竞品核心打法\n")
    for r in records:
        name = r["game_name"]
        total = r.get("total_ads_analyzed", "?")
        strats = r.get("creative_strategies", [])
        best_strat = strats[0] if strats else {}
        if isinstance(best_strat, dict):
            strat_name = best_strat.get("name", "未知")
            strat_pct = best_strat.get("percentage", "")
        else:
            strat_name = str(best_strat)
            strat_pct = ""

        emotions = r.get("dominant_emotional_appeals", [])
        top_emotion = emotions[0] if emotions else {}
        if isinstance(top_emotion, dict):
            emo_name = top_emotion.get("appeal", top_emotion.get("emotion", ""))
        else:
            emo_name = str(top_emotion)

        lines.append(f"### {name}")
        lines.append(f"- **广告投放量**: {total} 条")
        lines.append(f"- **核心策略**: {strat_name} ({strat_pct})" if strat_pct else f"- **核心策略**: {strat_name}")
        lines.append(f"- **主导情感诉求**: {emo_name}")
        audience = r.get("target_audience", "N/A")
        lines.append(f"- **目标受众**: {audience}")
        budget = r.get("budget_estimate", "N/A")
        lines.append(f"- **预算规模**: {budget}")
        lines.append("")

    # ── 差异化分析 ──
    lines.append("---\n")
    lines.append("## 3. 差异化打法与机会点\n")
    lines.append("### 打法差异\n")
    for r in records:
        name = r["game_name"]
        strats = r.get("creative_strategies", [])
        if len(strats) >= 2:
            s2 = strats[1]
            s2_name = s2.get("name", str(s2)) if isinstance(s2, dict) else str(s2)
            lines.append(f"- **{name}** 差异化打法: {s2_name}")
    lines.append("")

    # 机会点
    lines.append("### 机会点")
    # 找出视频占比最低的竞品
    if len(records) >= 2:
        video_pcts = {}
        for r in records:
            ad_types = r.get("ad_type_distribution", {})
            video_data = ad_types.get("video", {})
            if isinstance(video_data, dict):
                video_pcts[r["game_name"]] = video_data.get("percentage", 0)
        if video_pcts:
            min_game = min(video_pcts, key=video_pcts.get)
            lines.append(f"- 视频素材仍有提升空间: {min_game} 视频占比仅 {video_pcts[min_game]:.1f}%，建议关注其是否在测试新素材格式")
        max_game = max(video_pcts, key=video_pcts.get)
        lines.append(f"- {max_game} 视频占比最高 ({video_pcts[max_game]:.1f}%)，建议持续跟进其视频创意方向")
    lines.append("")

    # 建议优先级
    lines.append("---\n")
    lines.append("## 4. 建议优先级\n")
    lines.append("| 优先级 | 行动项 | 预期收益 |")
    lines.append("|--------|--------|----------|")
    lines.append(f"| P0 | 跟进 {records[0]['game_name'] if records else '头部'} 本周新素材 | 及时掌握头部竞品创意方向 |")
    lines.append("| P1 | 对比各竞品关键词策略调整 | 发现新的切词/定位机会 |")
    lines.append("| P2 | 关注预算变化趋势 | 判断竞品买量力度变化 |")
    lines.append("")

    output = "\n".join(lines)
    report_path = os.path.join(data_dir, "comparison_report.md")
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(output)
    step(f"  对比报告已生成: {report_path}")
    return report_path


def main():
    step("开始执行全量流水线...")

    # Step 1: 确认运行环境
    project_root = os.path.dirname(os.path.abspath(__file__))
    os.chdir(project_root)
    step(f"项目根目录: {project_root}")

    # Step 2: 检查数据目录
    data_dir = os.path.join(project_root, "data")
    os.makedirs(data_dir, exist_ok=True)
    step("数据目录已就绪")

    # Step 3: 检查 index.html
    index_path = os.path.join(project_root, "index.html")
    if not os.path.exists(index_path):
        step("错误: index.html 不存在，请确认项目完整性")
        sys.exit(1)
    step("index.html 已就绪")

    # Step 4: 生成多竞品对比分析报告
    step("生成多竞品对比分析报告...")
    generate_comparison_report(data_dir, index_path)
    step("对比分析报告生成完成 ✓")

    # Step 5: 执行自动推送
    step("调用 auto_push.py 推送更新到 GitHub...")
    try:
        subprocess.run([sys.executable, "auto_push.py"], check=True)
        step("推送完成 ✓")
    except subprocess.CalledProcessError as e:
        step(f"推送过程遇到问题: {e}")
        step("提示：可能是没有新的数据更改，或 Git 凭证未配置")

    step("全量流水线执行完毕 ✓")


if __name__ == "__main__":
    main()
