# 父系家族組裝

來源內人物候選與使用端人物節點分層保存。`registry/family-assemblies.json` 記錄編輯選定的父系組裝；並非按姓氏合併。現有漢劉氏版本從太公起，納入已具跨篇同指判讀及正文父親陳述的 110 個節點、256 個來源候選。其他尚未連通的劉氏候選仍待逐項判讀，不表示同姓者都是此族。

每個成員的 `person_id` 是組裝 ID，共用家族根。`representative_source_person_id` 是來源包的查詢入口，`source_person_ids` 是選用同指決定連接的來源候選。`identity_equivalence_decision_ids` 列同人證據；`source_assertion_id` 列接至 `parent_person_id` 的父親陳述。劉邦兄弟接回太公的節點另有 `parent_connection`：保存兄弟陳述、劉邦父親陳述及補證；不把原文兄弟關係改寫成明示父子。劉交另引《漢書・楚元王傳》「高祖同父少弟也」，保留《史記》原稱「同母少弟」；伯、仲則依兄弟四人的家庭敘事作暫定父系判讀。分支字元不表示出生順序。

人物匯出的 `assembled_identity` 保存上述欄位。使用端以 `assembled_identity.person_id` 畫單一節點、以 `parent_person_id` 接父系；來源陳述內的 ID 透過 `source_person_ids` 映射，原文、異說、來源 ID 及 `canonical_person_id` 不改寫。沒有組裝欄位的人物仍以原 ID 使用。`exports/persons/index.json` 的 `id_aliases` 將舊入口對應至組裝 ID，各舊 JSON 路徑仍可讀。

此版本沿用已記錄的暫定同指，未經人工覆核。原始資料中的其他父親候選及同指判讀仍保留；組裝選用的父親陳述不代表其他說法已刪除或全部已覆核。組裝由資料決定，執行不呼叫 AI。

`load_assemblies` 核對每個來源候選的同指連通性、父親陳述端點及家族 ID 世代，拒絕沒有證據的合併、重複人物或 ID 碰撞。重新產生人物 JSON 與 Markdown 表：

```sh
python3 scripts/export_person_bundles.py
```

吳王支系另據《史記・吳王濞列傳》開篇「高帝兄劉仲之子也」及已記跨篇同指接回劉仲。未名少子、戰時太子、子華及子駒保留不同候選節點，不代表已證實互為不同人物。
