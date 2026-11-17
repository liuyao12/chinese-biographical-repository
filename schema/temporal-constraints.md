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
      "quote": "某帝永徽三年幸某公主第",
      "person_mention_id": "c-example-001:p001:m0001",
      "temporal_claim": {
        "source_term": "永徽三年",
        "start": 2,
        "end": 6,
        "normalized_date": {
          "calendar": "chinese_civil",
          "year_system": "regnal",
          "era_id": "example-era-id",
          "precision": "year",
          "year": 3,
          "inclusive": true
        }
      }
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

## 運算子欄位形狀

運算子採固定欄位，不以自由文字表示端點：

- `equals`、`not_before`、`not_after` 使用 `bound`。例如 `not_before` 的 `bound` 是最早容許日期；`inclusive: true` 表示該年／月／日仍可取。
- `within_interval` 使用 `interval`，內含 `earliest` 與 `latest` 兩個完整日期值；任一端點可為 `null` 表示無界。每個非空端點各有自己的 `inclusive`，不可只給一個共用端點旗標。
- `after_event` 與 `not_before_event` 使用 `related_event_id`，分別表示嚴格晚於及不早於該事件。兩事件需能映射到同一比較座標；不可從敘事順序自行假定間隔。

日期值須包含 `calendar`、`year_system`、`precision`、整數 `year` 及布林 `inclusive`。`year_system` 固定為 `astronomical`（含公元零年的絕對年）、`historical`（不設公元零年的絕對年）或 `regnal`（年號內序數年）；`regnal` 必須另有 `era_id`，此時 `year: 3` 即該年號第三年，不是公元三年。絕對年不得帶 `era_id`。月／日精度時再加入數值 `month`／`day`。比較前要求日曆、年序、年號座標與精度相容；跨曆法或絕對年／年號年的轉換必須另有具來源的映射，不能由消費端猜測。日期區間採閉合或明示開放端點；沒有界限就用 `null`，不可用極小或極大年份代替。

## 引文中的日期詞與正規化

每筆 `evidence` 須有 `temporal_claim`，其中 `source_term` 是原引句內實際表示日期或事件關係的詞串；`start`／`end` 是其在 `quote` 內的字元位置。它必須原樣等於該位置的文字，不能只引用人物姓名而另填任意年份。

`temporal_claim` 必須且只能含以下一種正規化結果：

- `normalized_date`：單一來源日期；
- `normalized_interval`：原文明示的日期範圍；
- `normalized_relation`：包含 `operator`、`related_event_id` 的事件先後關係。

驗證器要求該正規化結果與 constraint 的運算子及端點完全相符。年號詞轉為數值年時，`year_system: regnal`、具名 `era_id` 及年號內序數必須一併保存；年號全期需以該年號的首末序數年構成區間。代理判讀仍須保留原詞，不由使用端解析。

`person_alive_at_event_implies_death_not_before` 首版只接受已標為 `event_type: visit`、`participant_role: visited_person` 的在場者事件；目標事件必須為同一人物的死亡事件。輸入事件不得等於目標事件，且日期引文、人物錨點及正規化日期均須可追溯。其他活動類型不自動推定在世。

## 推導規則與證據

`assertion_mode: direct` 表示引文直接給出目標事件的日期或界限。

`assertion_mode: derived` 必須有固定 `rule_id`、輸入事件 ID 及支持該規則的來源引文。規則版本化、語義明確；不得以 `interpretation_note` 自由文字代替。以某人於一時點在世為例，只有編者明確將該人物判為該事件的在世參與者，才可使用 `person_alive_at_event_implies_death_not_before`。單純出現於後出的敘事、後世追稱、死後到訪其宅或未定主語都不觸發此規則。

每項約束獨立保留來源和判讀狀態。不同作品若彼此矛盾，分別輸出；不能把矛盾來源平均化或靜默刪除。可依既有 precedence 決定為某一計算視圖選定來源，但原始約束仍可取回。

## 人物包與計算結果

`scripts/person_bundle.py` 在人物來源包中匯出 `temporal_constraints` 原記錄，並將約束所引段落加入 `passages`；不得只輸出合併後的摘要日期。`scripts/temporal_constraints.py` 提供年精度絕對界限交集函式，回傳端點及貢獻該端點的約束 ID。此 PR 尚未收錄任何同安公主或其他實際日期約束資料。

使用端可對同一目標事件、同一計時座標中相容的封閉區間求交。例如，若一來源給死亡年範圍 `[650, 655]`，另一來源證明人物至少活到第 3 年、正規化下界為 652，則：

\[
D = [650, 655] \cap [652, +\infty) = [652, 655].
\]

這是可計算的容許年範圍，不是單一年份估計。若交集為空，使用端應回報來源衝突並保留各來源約束，不得自動挑選一方。若兩項日期使用不同日曆或精度，必須先經有來源的明確轉換；不得直接比較。等值約束必須是含端點的單一日期。初版交集函式只計算絕對日期運算子；含相對事件運算子的輸入會回傳 `status: incomplete` 及未處理約束 ID，禁止使用端把未計算誤當成無界或無衝突結果。

## 驗證要求

`scripts/validate_corpus.py` 現已呼叫日期約束驗證器，檢查以下基本結構：

1. person、event、work、book、chapter、paragraph 與 mention ID 均存在且互相一致；
2. 每個引用含精確原文、日期詞字元錨點及人物錨點；正規化日期或範圍須與 constraint 端點完全相符；
3. `direct` 與 `derived` 欄位組合正確；在世推導只接受同一人物的死亡目標，以及有日期、原文引用和 `participant_role: visited_person` 的訪問事件；
4. 端點順序、包含性、日曆、絕對年／年號序數年座標及精度完整；
5. 衍生人物 JSON 保留原始約束與來源，計算結果可由原約束重現；
6. 撤回來源、身份或推導決定後，所有依賴結果可重建，且不需永久保存 ID 改名歷史。

此 PR 實作了初版結構驗證、人物包原記錄匯出及年精度絕對界限交集。跨曆法換算、相對事件約束的計算、同安公主個案資料與完整來源覆核仍未實作或收錄；草案欄位須隨實際個案持續核驗。
