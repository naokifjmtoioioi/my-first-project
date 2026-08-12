#!/usr/bin/env python3
"""
年間収益目標（デフォルト: ¥50,000,000）に対する進捗レポートを出力する。

使い方:
    python3 scripts/progress.py
    python3 scripts/progress.py --config data/config.json --revenue data/revenue.csv
"""
from __future__ import annotations

import argparse
import csv
import json
import sys
from collections import defaultdict
from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_CONFIG = REPO_ROOT / "data" / "config.json"
DEFAULT_REVENUE = REPO_ROOT / "data" / "revenue.csv"


@dataclass
class Entry:
    entry_date: date
    amount_jpy: int
    source: str
    memo: str


def load_config(path: Path) -> dict:
    with path.open(encoding="utf-8") as f:
        return json.load(f)


def load_revenue(path: Path) -> list[Entry]:
    entries: list[Entry] = []
    if not path.exists():
        return entries
    with path.open(encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            raw_date = (row.get("date") or "").strip()
            raw_amount = (row.get("amount_jpy") or "").strip()
            if not raw_date or not raw_amount:
                continue
            entries.append(
                Entry(
                    entry_date=datetime.strptime(raw_date, "%Y-%m-%d").date(),
                    amount_jpy=int(float(raw_amount)),
                    source=(row.get("source") or "未分類").strip() or "未分類",
                    memo=(row.get("memo") or "").strip(),
                )
            )
    return entries


def fmt_yen(amount: float) -> str:
    return f"¥{amount:,.0f}"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
    parser.add_argument("--revenue", type=Path, default=DEFAULT_REVENUE)
    args = parser.parse_args()

    config = load_config(args.config)
    target = config["target_revenue_jpy"]
    start = datetime.strptime(config["start_date"], "%Y-%m-%d").date()
    end = datetime.strptime(config["end_date"], "%Y-%m-%d").date()
    today = date.today()

    entries = load_revenue(args.revenue)
    total = sum(e.amount_jpy for e in entries)

    total_days = max((end - start).days, 1)
    elapsed_days = min(max((today - start).days, 0), total_days)
    remaining_days = max((end - today).days, 0)

    progress_ratio = total / target if target else 0
    time_ratio = elapsed_days / total_days

    by_source: dict[str, int] = defaultdict(int)
    for e in entries:
        by_source[e.source] += e.amount_jpy

    remaining_amount = max(target - total, 0)
    months_remaining = max(remaining_days / 30.4375, 0.001)
    required_monthly_pace = remaining_amount / months_remaining if remaining_days > 0 else remaining_amount

    print("=" * 56)
    print(" 年間収益目標 進捗レポート")
    print("=" * 56)
    print(f"期間        : {start} 〜 {end}")
    print(f"基準日      : {today}")
    print(f"目標額      : {fmt_yen(target)}")
    print(f"累計実績    : {fmt_yen(total)}")
    print(f"達成率      : {progress_ratio * 100:.1f}%")
    print(f"時間経過率  : {time_ratio * 100:.1f}%（この時点での基準線: {fmt_yen(target * time_ratio)}）")

    if progress_ratio + 1e-9 >= time_ratio:
        print("判定        : 基準線を上回っています（順調）")
    else:
        print("判定        : 基準線を下回っています（要テコ入れ）")

    print("-" * 56)
    print(f"残り日数    : {remaining_days}日")
    print(f"残り目標額  : {fmt_yen(remaining_amount)}")
    if remaining_days > 0:
        print(f"必要月次ペース: {fmt_yen(required_monthly_pace)}/月")
    else:
        print("期間が終了しています。")

    print("-" * 56)
    if by_source:
        print("収益源別内訳:")
        for source, amount in sorted(by_source.items(), key=lambda x: -x[1]):
            share = amount / total * 100 if total else 0
            print(f"  - {source}: {fmt_yen(amount)} ({share:.1f}%)")
    else:
        print("収益実績はまだ記録されていません（data/revenue.csv に追記してください）。")
    print("=" * 56)

    return 0


if __name__ == "__main__":
    sys.exit(main())
