# 人物來源包與家譜檢視器

以穩定人物 ID 讀取所有已標註的來源材料：

```sh
python3 scripts/person_bundle.py cbr-p004937 --output /tmp/mengtian.json
python3 scripts/person_bundle.py cbr-p000537 --include-provisional --output /tmp/lisi.json
```

預設僅讀指定 ID。`--include-provisional` 明示選用庫內暫定同指的傳遞集合；輸出保留每項判讀、原人物 ID 與證據，不以同名自動合併。暫定同指不表示各來源的世系與年代全部一致。輸出涵蓋目前已標註材料，不能代表尚未整理的全部史料。

`mentions` 提供字元錨點；`passages` 保存正文、篇卷著作 ID；`sources` 提供固定版本與來源網址。`relations` 同時包含以此人為主體或客體的直接主張，`persons` 包含直接相連人物，可作家譜節點；沿相鄰人物 ID 再取來源包即可逐步展開。每條線保留主張 ID、方向、狀態及原文，矛盾主張並列，不自動選成唯一父系。

`title_holdings` 保留每次官爵或尊稱主張的 `effective_period`、用稱錨點及事件類型。檢視器應分別呈現「當時任職確定」「任期未定、此處有用稱」「諡號或回顧用稱」，不能把未知起訖當無限期有效，也不能把初見當授予、把死亡當罷免。來源年月原文保留在 `date_expression`；尚未實作統一曆法換算與按公曆時間篩選，檢視器不得自行把年號字串當可比較日期。

此匯出是可重建的讀取層，權威資料仍是各篇來源與標註。無 AI 或網路處理需求。尚未接入家譜小程式或公開人物頁。

關係 `agnatic_cousin` 保存正文「從兄」「從弟」等同宗從兄弟稱呼，親等未定時 `qualifiers.degree` 為 `unknown`；不能由此補第一代表親、共同祖父或父子線。與 `brother` 相異的來源主張並列，`discrepancy_group_id` 可供檢視器連結分歧；該群組只提示差異，不自動選定其中一說。

出生排行存於關係主張的 `qualifiers.birth_order` 或 `qualifiers.relative_birth_order`，並直接匯出為 `birth_order_constraints`，消費端不需解析 `source_term`。每項約束保留主張 ID 與證據。

`長子`的 `ordinal` 為1，`scope: sons_of_parent` 表示在該父母的兒子序列中，不表示全部子女的第一名。`少子`暫記 `position: younger_or_youngest`、`ordinal: null`、`interpretation_status: ambiguous`；只有判讀明示最幼才另記 `youngest`。

兄弟相對先後記 `older_person_id`、`younger_person_id`、`operator: lt`；兩人的 `older_ordinal`、`younger_ordinal` 可均為 null。此約束表示先後，不表示相鄰，不推定同母或兩人生年。排序程式應合併所選人物同指，依約束作部分排序；有環則回報衝突，未連通者保持順序未定，不把可行的顯示排列回寫成確定出生排行。來源排行序列與展示排序分開。

目前先標註《秦始皇本紀》的扶蘇、胡亥與兩條弟關係，舊篇其他排行仍待逐條回填；不宣稱全庫已具排行約束。

籍貫與其他地址以 `address_assertions` 匯出，每項保存人物、`relation`、原文地名 `place.source_name`、來源與日期。`native_place` 不等於 `birth_place` 或 `residence`；未知現代對應與地點 ID 留 null，不自動使用現代行政區。地名錨點與地點登記仍待建立。目前先收錄卷九十三盧綰豐人及陳豨宛朐人，其他篇待回填。

早期傳記傳首「某某，某地人也」使用 `biographical_origin`（傳首所述出身地），保存原句；不推定後世制度化籍貫或戶籍。`native_place` 留作有相應來源判讀的籍貫記錄。

`death_place` 與 `burial_place` 分別表示死亡地、葬地，保留原文地名，無須今日行政區對應。始皇出生地邯鄲、死亡地沙丘平臺與葬地酈邑各存原文證據；不能由死亡地推定葬地，預定葬地也不直接作實際安葬。
