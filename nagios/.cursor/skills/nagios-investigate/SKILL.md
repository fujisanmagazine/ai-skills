---
name: nagios-investigate
description: 特定ホストを深掘り調査し、現在状態、履歴、フラッピング、可用性、監視ギャップから障害の根本原因を推定する。Nagiosのホスト調査、障害深掘り、原因分析で使う。
user_invocable: true
args: host_name
---

# Nagios ホスト調査

指定されたホストの状態を多角的に調査し、障害の根本原因を推定する。

## 引数

- `host_name` (必須): 調査対象のホスト名

## 手順

### Step 1: 現在の状態把握（並列実行）

以下を並列で呼び出す:

1. **`get_host_status`** (`host_name={{host_name}}`) — ホストの現在状態・plugin_output
2. **`get_service_status`** (`host_name={{host_name}}`) — 全サービスの状態一覧
3. **`get_comments`** (`host_name={{host_name}}`) — acknowledge・コメント状況
4. **`get_downtimes`** (`host_name={{host_name}}`) — ダウンタイム状況
5. **`get_coverage_gaps`** (`hosts=[{{host_name}}]`) — 閾値不足、監視漏れ、サイレント検知

### Step 2: 履歴・依存関係（並列実行）

まず集計済みデータを取得する。

6. **`get_alert_statistics`** (`hours_back=24`, `hosts=[{{host_name}}]`) — 頻出障害、状態変化、自己回復率
7. **`get_service_availability`** (`hours_back=168`, `hosts=[{{host_name}}]`) — サービス可用性、MTTR、SLO逸脱
8. **`get_flapping_report`** (`hours_back=24`, `hosts=[{{host_name}}]`) — フラッピング候補
9. **`get_host_dependencies`** (`host_name={{host_name}}`) — 上位/下位の依存関係

必要に応じて raw 詳細を追加する。

10. **`get_alert_history`** (`host_name={{host_name}}`, `hours_back=24`) — イベント時系列
11. **`get_state_change_history`** (`host_name={{host_name}}`, `hours_back=24`) — host 単位の状態遷移詳細

### Step 3: AI分析

収集したデータから以下を分析:

#### 原因推定ロジック

- **全サービスが同時にcritical/unknown** → ホスト自体の問題（ネットワーク到達不能、OS停止等）
- **特定サービスのみ異常** → そのサービス固有の問題（プロセス停止、ディスク満杯等）
- **親ホストがダウン** → ネットワーク経路の問題（当該ホスト自体は正常の可能性）
- **soft state → hard stateの遷移** → 一時的な問題から恒常的な障害に移行
- **`get_flapping_report` で変化回数が多い** → フラッピング（閾値付近、NRPE timeout、定期処理起因）
- **`get_service_availability` で uptime が低い** → 実害が大きい障害
- **`get_coverage_gaps` で閾値不足** → 監視設定自体の見直しが必要

#### plugin_outputの読み解き

- `PING CRITICAL` → ネットワーク到達不能
- `DISK CRITICAL - free space: /xxx N% free` → ディスク容量
- `PROCS CRITICAL: 0 processes` → プロセス停止
- `HTTP CRITICAL` → Webサービス応答なし
- `Connection refused` → サービス未起動

#### 出力フォーマット

```
## ホスト調査レポート: {{host_name}}

### 現在の状態
- ホスト: [UP/DOWN/UNREACHABLE] (since YYYY-MM-DD HH:MM)
- plugin_output: ...
- サービス: N件中 M件異常

### 異常サービス一覧
| サービス | 状態 | plugin_output | 継続時間 |
|---------|------|---------------|---------|

### 状態遷移（直近24時間）
- HH:MM — OK → WARNING
- HH:MM — WARNING → CRITICAL
- ...

### 依存関係
- 親ホスト: ... (状態: ...)
- 子ホスト: ... (状態: ...)

### 原因推定
- 推定原因: ...
- 根拠: ...

### 推奨アクション
1. ...
2. ...

### 参考情報
- 監視コマンド: ...
- 通知先: ...
- Acknowledge状況: ...
```

## 注意

- 既定 toolset では `get_single_object_config` は出ない前提で進める
- 設定詳細が必要な場合は `get_object_list_config` や status/perfdata から推定し、それでも不足するときだけ full toolset を検討する
