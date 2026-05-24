#!/usr/bin/env python3
"""
竞品广告数据采集脚本
调用 Meta Ad Library API 拉取竞品广告数据

使用方法：
    python collect_ads.py --name "Last War" --token EAxxxxx --output ./data

前置条件：
    1. 注册 Meta Developer 账号
    2. 创建 App，获取长期 Access Token (ads_read 权限)
    3. pip install requests
"""

import requests
import json
import argparse
import os
import time
from datetime import datetime, timedelta


class MetaAdCollector:
    API_VERSION = "v19.0"
    BASE_URL = f"https://graph.facebook.com/{API_VERSION}/ads_archive"

    def __init__(self, access_token: str):
        self.access_token = access_token
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "AdAnalyzer/1.0"
        })

    def fetch_ads(self, search_terms: str, page_id: str = None,
                  countries: list = None, limit: int = 100,
                  days_back: int = 90) -> list:
        """
        拉取竞品广告数据

        Args:
            search_terms: 竞品名称搜索词
            page_id: Facebook Page ID (可选，更精确)
            countries: 投放国家列表
            limit: 每页数量 (最大 100)
            days_back: 回溯天数

        Returns:
            广告数据列表
        """
        if countries is None:
            countries = ["US"]

        params = {
            "search_terms": f'"{search_terms}"',
            "ad_type": "ALL",
            "ad_reached_countries": json.dumps(countries),
            "fields": ",".join([
                "ad_creative_body",
                "ad_creative_link_title",
                "ad_creative_link_description",
                "ad_creative_link_caption",
                "ad_delivery_start_time",
                "ad_delivery_stop_time",
                "ad_snapshot_url",
                "ad_active_status",
                "publisher_platforms",
                "spend",
                "impressions",
                "page_id"
            ]),
            "limit": min(limit, 100),
            "access_token": self.access_token,
        }

        if page_id:
            params["page_id"] = page_id

        all_ads = []
        seen_urls = set()
        retry_count = 0
        max_retries = 3

        while True:
            try:
                response = self.session.get(self.BASE_URL, params=params, timeout=30)

                # 限流处理
                if response.status_code == 429:
                    retry_count += 1
                    if retry_count > max_retries:
                        print(f"⚠️ 达到最大重试次数 ({max_retries})，跳过")
                        break
                    wait_time = 60 * retry_count
                    print(f"⏳ API 限流，等待 {wait_time} 秒后重试...")
                    time.sleep(wait_time)
                    continue

                response.raise_for_status()
                data = response.json()

                if "error" in data:
                    print(f"❌ API 错误: {data['error'].get('message', '未知错误')}")
                    break

                # 清洗和去重
                for ad in data.get("data", []):
                    # 过滤空文案
                    if not ad.get("ad_creative_body"):
                        continue

                    # 按 ad_snapshot_url 去重
                    url = ad.get("ad_snapshot_url", "")
                    if url and url in seen_urls:
                        continue
                    if url:
                        seen_urls.add(url)

                    # 标准化数据
                    cleaned = {
                        "ad_creative_body": ad.get("ad_creative_body", ""),
                        "ad_creative_link_title": ad.get("ad_creative_link_title", ""),
                        "ad_creative_link_description": ad.get("ad_creative_link_description", ""),
                        "ad_creative_link_caption": ad.get("ad_creative_link_caption", ""),
                        "ad_delivery_start_time": ad.get("ad_delivery_start_time", ""),
                        "ad_delivery_stop_time": ad.get("ad_delivery_stop_time", ""),
                        "ad_snapshot_url": url,
                        "ad_active_status": ad.get("ad_active_status", ""),
                        "publisher_platforms": ", ".join(ad.get("publisher_platforms", [])),
                        "page_id": ad.get("page_id", ""),
                    }

                    # spend 和 impressions 可能是范围值，取平均值
                    spend = ad.get("spend", {})
                    if isinstance(spend, dict):
                        cleaned["spend"] = (spend.get("min", 0) + spend.get("max", 0)) / 2
                    else:
                        cleaned["spend"] = spend

                    impressions = ad.get("impressions", {})
                    if isinstance(impressions, dict):
                        cleaned["impressions"] = (impressions.get("min", 0) + impressions.get("max", 0)) / 2
                    else:
                        cleaned["impressions"] = impressions

                    all_ads.append(cleaned)

                # 处理分页
                paging = data.get("paging", {})
                next_url = paging.get("next")
                if next_url:
                    params = None  # next URL 包含所有参数
                    self.BASE_URL = next_url
                else:
                    break

                retry_count = 0  # 成功后重置重试计数

            except requests.exceptions.Timeout:
                print("⏰ 请求超时，重试...")
                retry_count += 1
                if retry_count > max_retries:
                    break
                time.sleep(5)
            except requests.exceptions.RequestException as e:
                print(f"❌ 请求失败: {e}")
                break

        return all_ads


def print_summary(ads: list, name: str):
    """打印采集摘要"""
    active = [a for a in ads if a.get("ad_active_status") == "ACTIVE"]
    platforms = {}
    for ad in ads:
        for p in ad.get("publisher_platforms", "").split(", "):
            if p:
                platforms[p] = platforms.get(p, 0) + 1

    print(f"\n=== 采集完成 ===")
    print(f"竞品: {name}")
    print(f"共抓取: {len(ads)} 条广告")
    print(f"活跃广告: {len(active)} 条")
    if platforms:
        plat_str = ", ".join([f"{k}: {v}" for k, v in sorted(platforms.items(), key=lambda x: -x[1])])
        print(f"平台分布: {plat_str}")


def main():
    parser = argparse.ArgumentParser(description="Meta 竞品广告数据采集")
    parser.add_argument("--name", required=True, help="竞品名称")
    parser.add_argument("--page-id", default="", help="Facebook Page ID (可选)")
    parser.add_argument("--token", required=True, help="Meta Access Token")
    parser.add_argument("--output", default="./data", help="输出目录")
    parser.add_argument("--days", type=int, default=90, help="回溯天数")
    parser.add_argument("--country", default="US", help="投放国家代码")
    args = parser.parse_args()

    # 创建输出目录
    os.makedirs(args.output, exist_ok=True)

    # 采集数据
    collector = MetaAdCollector(args.token)
    ads = collector.fetch_ads(
        search_terms=args.name,
        page_id=args.page_id or None,
        countries=[args.country],
        days_back=args.days
    )

    # 打印摘要
    print_summary(ads, args.name)

    # 保存
    date_str = datetime.now().strftime("%Y%m%d")
    filename = f"{args.name.replace(' ', '_')}_ads_{date_str}.json"
    filepath = os.path.join(args.output, filename)

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(ads, f, ensure_ascii=False, indent=2)

    print(f"数据已保存: {filepath}")


if __name__ == "__main__":
    main()
