# 進捗トラッキング（KPI）

## 仕組み

- `data/config.json`: 目標額・期間の設定
- `data/revenue.csv`: 収益実績の記録（1行 = 1件の入金/確定売上）
- `scripts/progress.py`: 上記2つを読み込み、進捗レポートをコンソールに出力

## revenue.csv のフォーマット

```
date,amount_jpy,source,memo
2026-08-15,50000,note販売,初回販売分
```

- `date`: YYYY-MM-DD
- `amount_jpy`: 円単位の整数（税抜/税込は運用で統一する）
- `source`: 収益源の名称（例: note販売, SaaSサブスク, アフィリエイト）
- `memo`: 任意の補足

## レポートの見方

`python3 scripts/progress.py` を実行すると以下が出力される:

- 累計収益と目標(¥50,000,000)に対する達成率
- 残り期間と、残り期間で目標達成に必要な月次ペース
- 収益源(source)別の内訳

## 運用ルール

1. 収益が確定したら計測・経理AI（または人間）が都度 `data/revenue.csv` に追記する
2. 週次で `scripts/progress.py` を実行し、目標線からの乖離を確認する
3. 乖離が大きい場合はオーケストレーターがリソース配分・施策の見直しを行う
