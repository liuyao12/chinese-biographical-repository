# 來源日期約束與時間交集

> 本文件提出 CBR 日期約束的資料契約；目前主分支的人物包與驗證器尚未實作此結構。本文不是已收錄的個案資料。

## 目的

每一項來源時間事實都應同時保留：

- 可定位的原文引句、作品／卷／篇／段及人物錨點；
- 該事實對目標事件施加的機器可讀日期約束；
- 約束是原文明言，還是依明確規則從另一項來源事實推得。

消費端只按事件 ID、約束運算子、日曆精度與引用來源運算，不讀自然語言、不呼叫 NLU。原始主張不得因計算結果而改寫。

## 既有欄位與缺口

現有 `life_events`、`age_assertions`、`normalized_date`、`normalized_date_range` 和 `source_temporal_attestation_set` 已能分別保存事件日期、報齡、日期範圍或來源中的時間語境及其引文。人物包可匯出上述資料。

目前沒有通用記錄表示「來源事實 A 限定人物事件 B 不早於某日期」，也沒有通用引用把這種推導連回來源段落。只匯出「永徽三年仍在世」與「永徽年間卒」兩段自然語言，仍要求使用端知道其歷史語義，違反無 NLU 的使用目標。

## 建議的記錄形式

逐篇新檔可採：

`corpus/{work}/{book}-temporal-constraints.json`

根物件：

```json
{
  "format_version": "0.1",
  "record_type": "temporal_constraint_set",
  "work_id": "w-example",
  "book_id": "b-example-001",
  "source_id": "s-example-001",
  "chapter_id": "c-example-001",
  "constraints": []
}
```

每個 constraint 至少包括：

```json
{
  "id": "tc-example-death-lower-bound",
  "person_id": "person-id",
  "target_event_id": "death-event-id",
  "operator": "not_before",
  "bound": {
    "calendar": "chinese_civil",
    "year": 652,
    "inclusive": true,
    "year_system": "astronomical",
    "precision": "year"
  },
  "assertion_mode": "derived",
  "derivation": {
    "rule_id": "person_alive_at_event_implies_death_not_before",
    "input_event_id": "visit-event-id"
  },
  "evidence": [
    {
      "work_id": "w-example",
      "book_id": "b-example-001",
      "source_id": "s-example-001",
      "chapter_id": "c-example-001",
      "paragraph_id": "c-example-001:p001",
      "quote": "來源原文引句",
      "person_mention_id": "c-example-001:p001:m0001"
    }
  ],
  "human_reviewed": false
}
```

此處的例子只說明欄位，不是已登記史料或可用的人物 ID。

## 最小運算語彙

首版只需支援以下目標事件日期運算子：

- `equals`：單一日期值；
- `within_interval`：含明確上下端點的封閉或開放區間；
- `not_before`：下界，可明確設定端點是否包含；
- `not_after`：上界，可明確設定端點是否包含；
- `after_event`、`not_before_event`：相對於另一個有日期事件的限制。

所有時間值須明示日曆、精度及端點包含性。年尺度日期用既有的中國曆年正規化慣例；不可把未知月日補成公曆日。端點須可表達無上界或無下界，不得以虛構年份代替未知值。

## 推導規則與證據

`assertion_mode: direct` 表示引文直接給出目標事件的日期或界限。

`assertion_mode: derived` 必須有固定 `rule_id`、輸入事件 ID 及支持該規則的來源引文。規則版本化、語義明確；不得以 `interpretation_note` 自由文字代替。以某人於一時點在世為例，只有編者明確將該人物判為該事件的在世參與者，才可使用 `person_alive_at_event_implies_death_not_before`。單純出現於後出的敘事、後世追稱、死後到訪其宅或未定主語都不觸發此規則。

每項約束獨立保留來源和判讀狀態。不同作品若彼此矛盾，分別輸出；不能把矛盾來源平均化或靜默刪除。可依既有 precedence 決定為某一計算視圖選定來源，但原始約束仍可取回。

## 人物包與計算結果

人物 JSON 應另行匯出 `temporal_constraints`，每筆包括約束 ID、目標人物及事件、運算子、端點、來源引句、引文位置、推導規則和來源狀態。不得只輸出合併後的摘要日期。

使用端可對同一目標事件、同一計時座標中相容的封閉區間求交。例如，若一來源給死亡年範圍 `[650, 655]`，另一來源證明人物至少活到第 3 年、正規化下界為 652，則：

\[
D = [650, 655] \cap [652, +\infty) = [652, 655].
\]

這是可計算的容許年範圍，不是單一年份估計。若交集為空，使用端應回報來源衝突並保留各來源約束，不得自動挑選一方。若兩項日期使用不同日曆或精度，必須先經有來源的明確轉換；不得直接比較。

## 驗證要求

實作時的驗證器應檢查：

1. person、event、work、book、chapter、paragraph 與 mention ID 均存在且互相一致；
2. 每個引用含精確原文，人物錨點與段落文字匹配；
3. `direct` 與 `derived` 欄位組合正確，推導規則在登記表中存在；
4. 端點順序、包含性、日曆、精度及日期系統完整；
5. 衍生人物 JSON 保留原始約束與來源，計算結果可由原約束重現；
6. 撤回來源、身份或推導決定後，所有依賴結果可重建，且不需永久保存 ID 改名歷史。

此文件提出介面契約；新增 validator、人物包匯出及個案資料前仍須實作並核驗。
