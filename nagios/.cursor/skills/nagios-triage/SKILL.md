---
name: nagios-triage
description: Nagios全体のアラート状況を把握し、未処理問題、頻出障害、フラッピング、慢性アラート、監視ギャップを優先度付きでトリアージする。全体俯瞰や優先順位付けで使う。
user_invocable: true
---

# Nagios トリアージ

現在のNagios監視状況を全体把握し、優先度付きのトリアージレポートを生成する。

## 手順

以下のMCPツールを順番に呼び出してデータを収集し、AI分析を行う。

### Step 1: データ収集（並列実行）

以下のツールを並列で呼び出す:

1. **`get_overall_health_summary`** — ホスト/サービスの全体カウント
2. **`get_unhandled_problems`** — 未acknowledge・非ダウンタイムの問題一覧
3. **`get_downtimes`** — 現在のダウンタイム一覧
4. **`get_alert_statistics`** (`hours_back=24`, `min_alert_count=2`) — 頻出障害、自己回復率、状態変化
5. **`get_flapping_report`** (`hours_back=6`, `min_state_changes=3`) — フラッピング候補
6. **`get_neglected_objects`** (`min_neglect_days=7`) — 長期放置アラート
7. **`get_coverage_gaps`** — 監視漏れ・閾値不足
8. **`get_notification_analysis`** (`hours_back=24`) — 通知過多、ノイズ候補

### Step 2: 追加データ収集

Step 1の結果を踏まえて:

9. **`get_alert_history`** (`hours_back=6`) — 直近6時間のアラート推移（悪化/改善判断）
10. **`get_host_dependencies`** — ホスト依存関係（障害波及の分析用）
11. **`get_service_availability`** (`hours_back=168`, `hosts=[上位ホスト群]`) — 実害の大きい対象を確認

### Step 3: AI分析・レポート生成

収集したデータから以下の観点で分析し、レポートを生成する:

#### 優先度分類

| 優先度 | 条件 | アクション |
|--------|------|-----------|
| P1 Critical | ホストダウン、可用性低下、外部公開系の監視ギャップ | 即時対応 |
| P2 High | criticalサービス、深刻なフラッピング、慢性未対応 | 要対応 |
| P3 Medium | warningサービス、ノイズ候補、閾値見直し候補 | 監視継続 |
| P4 Low | acknowledge済み、ダウンタイム中、軽微な一時スパイク | 情報のみ |

#### 分析の観点

- **根本原因推定**: 親ホストがダウンしている場合、子ホスト/サービスの障害は派生的
- **フラッピング検出**: `get_flapping_report` を優先し、必要時のみ raw 履歴で補足
- **影響範囲**: 依存関係から、1つのホストダウンが何台に影響するか
- **傾向**: 直近で悪化中か改善中か
- **慢性化**: `get_neglected_objects` で長期放置のノイズ源を抽出
- **監視品質**: `get_coverage_gaps` で偽陰性リスクを抽出
- **通知負荷**: `get_notification_analysis` でアラート疲れリスクを評価

#### 出力フォーマット

```
## Nagios トリアージレポート

### 全体サマリ
- ホスト: X台中 Y台ダウン
- サービス: X件中 Y件異常

### P1 Critical（即時対応）
- [ホスト名] — plugin_output — 影響範囲: N台/Nサービス

### P2 High（要対応）
- [ホスト名/サービス名] — plugin_output — 継続時間

### P3 Medium（監視継続）
- ...

### P4 Low（情報のみ）
- ダウンタイム中: ...
- Acknowledge済み: ...

### 推奨アクション
1. ...
2. ...
```
