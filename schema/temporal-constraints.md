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
    "year": 3,
    "inclusive": true,
    "year_system": "regnal",
    "precision": "year",
    "era_id": "example-era-id"
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
      "quote_start": 0,
      "quote_end": 11,
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

若採用原文敘事排列作事件先後依據，仍須保留這是編者採納的條件判讀，而非來源明言的日期。此時 constraint 可用 `assertion_mode: "derived"`、`operator: "after_event"`，並在 `derivation` 明列 `rule_id: "narrative_sequence_implies_event_order"`、`ordering_basis: "narrative_sequence"`、`condition_status: "conditionally_accepted"` 及 `review_status: "agent_reviewed"` 或 `"human_reviewed"`。頂層 `human_reviewed` 必須如實反映是否有真人覆核，AI 代理覆核不得標成真人覆核。其 `target_event_id` 可屬於一人，`related_event_id` 可屬另一人；原始日期及事件關係各自保存在原子約束，不應混成單一來源主張。

日期值須包含 `calendar`、`year_system`、`precision`、整數 `year` 及布林 `inclusive`。歷史年序不得使用不存在的公元零年；年號序數年須為正整數。`year_system` 固定為 `astronomical`（含公元零年的絕對年）、`historical`（不設公元零年的絕對年）或 `regnal`（年號內序數年）；`regnal` 必須另有 `era_id`，此時 `year: 3` 即該年號第三年，不是公元三年。絕對年不得帶 `era_id`。月／日精度時再加入數值 `month`／`day`。比較前要求日曆、年序、年號座標與精度相容；跨曆法或絕對年／年號年的轉換必須另有具來源的映射，不能由消費端猜測。日期區間採閉合或明示開放端點；沒有界限就用 `null`，不可用極小或極大年份代替。

## 引文中的日期詞與正規化

每筆 `evidence` 須有 `quote_start`／`quote_end`，明確錨定原段中的完整引句；其字元切片必須等於 `quote`，且所有人物提及錨點都必須落在該精確字元區間內，以免段內重複語句或人物錯配。另須有 `temporal_claim`，其中 `source_term` 是引句內實際表示日期或事件關係的詞串；`start`／`end` 是其在 `quote` 內的字元位置。它必須原樣等於該位置的文字，不能只引用人物姓名而另填任意年份。

`temporal_claim` 必須且只能含以下一種正規化結果：

- `normalized_date`：單一來源日期；
- `normalized_interval`：原文明示的日期範圍；
- `normalized_relation`：包含 `operator`、`related_event_id` 的事件先後關係。

驗證器要求該正規化結果與 constraint 的運算子及端點完全相符。在世推導的死亡下界還必須與被訪者事件的 `normalized_date` 完全相同；只有日期範圍而沒有精確事件日期時，不可直接取晚端推導死亡下界。年號詞轉為數值年時，`year_system: regnal`、具名 `era_id` 及年號內序數必須一併保存；年號全期需以該年號的首末序數年構成區間。代理判讀仍須保留原詞，不由使用端解析。

`person_alive_at_event_implies_death_not_before` 首版只接受已標為 `event_type: visit`、`participant_role: visited_person` 的在場者事件；目標事件必須為同一人物的死亡事件。輸入事件不得等於目標事件；死亡下界必須等於該訪問事件的精確 `normalized_date`，不可使用晚於訪問的日期，也不可把日期範圍晚端當作下界。日期引文、人物錨點及正規化日期均須可追溯。其他活動類型不自動推定在世。

## 推導規則與證據

`assertion_mode: direct` 表示引文直接給出目標事件的日期或界限。

`assertion_mode: derived` 必須有固定 `rule_id`、輸入事件 ID 及支持該規則的來源引文。規則版本化、語義明確；不得以 `interpretation_note` 自由文字代替。以某人於一時點在世為例，只有編者明確將該人物判為該事件的在世參與者，才可使用 `person_alive_at_event_implies_death_not_before`。單純出現於後出的敘事、後世追稱、死後到訪其宅或未定主語都不觸發此規則。

`narrative_sequence_implies_event_order` 是一項明確有條件的跨人物先後判讀：事件關係 constraint 本身必須保留精確錨定於原段的引文、關係詞錨點及 `normalized_relation`；若引文涉及兩位不同人物，須分別錨定兩個人物提及。 `derivation` 必須標示敘事排序前提、其 `conditionally_accepted` 狀態及代理或真人覆核狀態。前提未採納、來源段落無法定位、較晚事件的界限互相衝突，或兩事件不能映射至相同時間座標時，計算須回報 `incomplete`，不可輸出確定上／下界。

對於年精度同座標約束 \(A < B\) 且已知 \(B \leq y\)，可條件式推出 \(A \leq y\)；同年內的先後仍容許 A、B 同年，故衍生上界包含該年。計算結果須列出形成上界的來源約束及整條事件先後鏈中各關係約束的實際 ID，不得以內部暫存 ID 取代來源 ID；並保留 `ordering_basis` 與 `condition_status`。人物包應同時帶回依賴約束、跨人物事件及其來源段落。這種計算輸出是可重建的推論，不得回寫成原文直接記載的卒年。

每項約束獨立保留來源和判讀狀態。不同作品若彼此矛盾，分別輸出；不能把矛盾來源平均化或靜默刪除。可依既有 precedence 決定為某一計算視圖選定來源，但原始約束仍可取回。

## 人物包與計算結果

`scripts/person_bundle.py` 在人物來源包中匯出 `temporal_constraints` 原記錄、跨人物 `temporal_constraint_events`、可重建的 `temporal_constraint_results`，並將相關約束所引段落加入 `passages`；不得只輸出合併後的摘要日期。結果的端點列出貢獻約束 ID；條件式先後推導另列輸入約束 ID 及排序前提。`scripts/temporal_constraints.py` 提供年精度同座標界限交集與條件式事件先後傳播。此 PR 尚未收錄任何同安公主或其他實際日期約束資料。

使用端可對同一目標事件、同一計時座標中相容的日期界限求交。例如，一來源記人物卒於永徽年間，形成年號序數年 1 至 6 的封閉區間；另一來源記永徽三年仍在世，形成死亡年不早於年號序數年 3 的下界。兩者使用同一永徽年號座標，故：

\[
D = [1, 6] \cap [3, +\infty) = [3, 6].
\]

此處的 1 至 6 是假設來源明確記載「卒於永徽年間」時，`within_interval` 所表達的示例；不能把它套用到只記永徽年間曾賜戶、另記享年而未繫卒年的材料。**此公式是通用示例，不是同安公主的實際結論。**就同安公主而言，《舊唐書》卷四永徽三年所記為幸同安大長公主第；若編者採納該事為公主在世事件，只導出死亡不早於永徽三年。《新唐書》卷八十三的「永徽初，賜實戶三百。薨，年八十六」沒有明載薨年，不能由相鄰句把薨繫於永徽初。該卷稍後另有「永徽六年主薨」之語，屬高密公主，不能移接同安公主。因此目前這兩項所據史文沒有同安公主死亡的上界；使用端應保存永徽三年下界及 `latest: null`，不得輸出永徽三年至六年或猜作四年。若交集為空，結果明確標記 `status: "conflict"`，使用端應回報來源衝突並保留各來源約束，不得自動挑選一方。若兩項日期使用不同日曆或精度，必須先經有來源的明確轉換；不得直接比較。0.1 版尚無可驗證的跨座標映射欄位，因此不得把年號序數轉寫成天文年後當作同座標輸入；遇到此情形須保留原始約束，讓交集結果標記為未完成，待映射結構實作後再計算。等值約束必須是含端點的單一日期。`intersect_year_constraints` 只計算年精度、同一座標的絕對界限；`calculate_temporal_constraint_results` 另處理明確條件且經代理或真人覆核、並如實標示覆核者的 `narrative_sequence_implies_event_order` 年精度上界傳播。其他相對事件關係、未採納排序前提或缺乏可比較上界時，結果須回傳 `status: incomplete` 及未處理約束 ID，禁止使用端把未計算誤當成無界或無衝突結果。

## 驗證要求

`scripts/validate_corpus.py` 現已呼叫日期約束驗證器，檢查以下基本結構：

1. person、event、work、book、chapter、paragraph 與 mention ID 均存在且互相一致；
2. 每個引用含精確原文的段內字元位置、日期詞字元錨點及位於該精確引文範圍內的人物錨點；正規化日期或範圍須與 constraint 端點完全相符；
3. `direct` 與 `derived` 欄位組合正確；在世推導只接受同一人物的死亡目標，以及有日期、原文引用和 `participant_role: visited_person` 的訪問事件；
4. 端點順序、包含性、日曆、絕對年／年號序數年座標及精度完整；歷史年序無公元零年，年號序數為正整數；
5. 衍生人物 JSON 保留原始約束與來源，計算結果可由原約束重現；
6. 撤回來源、身份或推導決定後，所有依賴結果可重建，且不需永久保存 ID 改名歷史。

此 PR 實作了初版結構驗證、人物包原記錄匯出、年精度絕對界限交集及條件式敘事次序上界傳播。傳播按無循環事件圖的反向拓撲次序計算至固定點，不受記錄排列順序影響；事件次序成環或上界來源互相衝突時保留為不完整，不輸出可疑界限。跨曆法換算、同安公主個案資料與完整來源覆核仍未實作或收錄；草案欄位須隨實際個案持續核驗。
