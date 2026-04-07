---
name: nagios-tune
description: Nagiosアラートのノイズ、フラッピング、慢性未対応、偽陰性リスクを分析し、設定変更案を生成する。アラートチューニング、通知削減、監視品質改善、Alert Fatigue対策で使う。
user_invocable: true
args: hours host_name
---

# Nagios アラートチューニング

アラート品質を評価し、ノイズ削減と偽陰性抑制の両方を考慮した設定変更案を作る。

## 引数

- `hours` (任意, デフォルト: 72): 分析期間
- `host_name` (任意): 特定ホストだけ調べる場合

## 基本方針

- まず集計済み tool を使い、raw 履歴は理由確認に限定する
- `host_name` がある場合は `hosts=[{{host_name}}]` で必ず絞る
- 「通知削減」だけでなく「監視漏れ防止」も同時に評価する
- 廃止・削除・無効化は断定しすぎず、必要ならレビュー前提で提案する

## Step 1: データ収集（並列実行）

以下を並列で呼び出す。

1. **`get_alert_statistics`** (`hours_back={{hours}}`, `min_alert_count=2`, `hosts=[{{host_name}}]` を必要に応じて指定)
2. **`get_service_availability`** (`hours_back=max({{hours}}, 24)`, `hosts=[{{host_name}}]` を必要に応じて指定)
3. **`get_flapping_report`** (`hours_back=min({{hours}}, 24)`, `min_state_changes=3`, `hosts=[{{host_name}}]` を必要に応じて指定)
4. **`get_neglected_objects`** (`min_neglect_days=7`, `hosts=[{{host_name}}]` を必要に応じて指定)
5. **`get_coverage_gaps`** (`hosts=[{{host_name}}]` を必要に応じて指定)
6. **`get_notification_analysis`** (`hours_back={{hours}}`, `hosts=[{{host_name}}]` を必要に応じて指定)
7. **`get_unhandled_problems`**
8. **`get_overall_health_summary`**

## Step 2: 補足データ（必要時のみ）

集計結果の理由を説明したいときだけ raw を追加する。

9. **`get_alert_history`** (`hours_back={{hours}}`, `host_name={{host_name}}` または上位ホスト)
10. **`get_notification_history`** (`hours_back={{hours}}`, `host_name={{host_name}}` または上位ホスト)
11. **`get_comments`** (`host_name={{host_name}}` または上位ホスト)
12. **`get_downtimes`** (`host_name={{host_name}}` または上位ホスト)

## Step 3: ルールベース分類

各 host/service について、まず以下で一次分類する。

| classification | 条件 |
|---|---|
| `NOISE` | `auto_recovery_rate > 0.9` かつ `alert_count > 10` かつ 通知に対して action が少ない |
| `FLAPPING` | `state_changes_window > 10` または `classification_hint=FLAPPING` |
| `NEGLECTED` | `neglect_days > 30` かつ `acknowledged=false` |
| `THRESHOLD_WRONG` | `gap_type=THRESHOLD_TOO_LATE` |
| `FALSE_NEGATIVE_RISK` | `get_coverage_gaps` で高リスク項目あり |
| `ACTIONABLE` | 自動回復率が低く、可用性低下や継続時間が大きい |
| `REQUIRES_REVIEW` | 上記に単純に当てはまらない複合ケース |

## Step 4: 提案パターン

### フラッピング

- `max_check_attempts` を 3-5 に引き上げる
- `check_interval` / `retry_interval` を延ばす
- `notification_interval` を延ばす
- NRPE timeout 系なら timeout を延長する
- バッチ起因なら timeperiod で除外を検討する

### 慢性アラート

- 廃止済み疑い: 削除または `checks_enabled=false`
- 既知障害: `acknowledge` または downtime 設定
- 復旧見込みなし: 通知抑制またはチェック停止を提案

### 閾値不足

- disk は WARNING を早める
- SSL は 60日前 / 30日前の段階警告を入れる
- trend がある対象は静的閾値だけでなく増加率監視を提案する

### 通知過多

- `notification_interval=0` または `1440`
- `notification_options` を `c,r` などに絞る
- WARNING 通知を止め、CRITICAL と recovery のみにする

## Step 5: レポートの出し方

以下の形式で返す。

```markdown
## Nagios アラートチューニングレポート

### サマリ
- 偽陽性候補: N件
- フラッピング: N件
- 慢性アラート: N件
- 偽陰性リスク: N件
- 推定通知削減: 約X件/日

### 即時対応
| ホスト/サービス | 問題 | 推奨変更 | 期待効果 |

### 今週中の改善
| ホスト/サービス | 問題 | 推奨変更 | 注意点 |

### 監視追加を推奨
| 対象 | 欠けている監視 | 推奨追加 | リスク |

### 削除/無効化候補
| ホスト/サービス | 理由 | 推奨対応 | 推定削減通知数/日 |
```

## レポートの優先順位

- まず `P1`: 実害が大きい、または偽陰性リスクが高いもの
- 次に `P2`: フラッピングや慢性ノイズで通知負荷が大きいもの
- 次に `P3`: 閾値最適化や通知間隔調整で改善できるもの

## 注意

- ビジネス重要度はデータだけでは決め切れないので、外部公開、決済、DB クラスタなどは明示的に注記する
- 自動提案はそのまま適用前提ではなく、レビュー前提で書く
- 通知削減だけを目的にせず、偽陰性リスクも必ず併記する
