# 人物來源包與家譜檢視器

以穩定人物 ID 讀取所有已標註的來源材料：

```sh
python3 scripts/person_bundle.py cbr-p004937 --output /tmp/mengtian.json
python3 scripts/person_bundle.py cbr-p000537 --include-provisional --output /tmp/lisi.json
```

預設僅讀指定 ID。`--include-provisional` 明示選用庫內暫定同指的傳遞集合；輸出保留每項判讀、原人物 ID 與證據，不以同名自動合併。暫定同指不表示各來源的世系與年代全部一致。輸出涵蓋目前已標註材料，不能代表尚未整理的全部史料。

`mentions` 提供字元錨點；`passages` 保存正文、篇卷著作 ID；`sources` 提供固定版本與來源網址。`relations` 同時包含以此人為主體或客體的直接主張，`persons` 包含直接相連人物，可作家譜節點；沿相鄰人物 ID 再取來源包即可逐步展開。每條線保留主張 ID、方向、狀態及原文，矛盾主張並列，不自動選成唯一父系。

`title_holdings` 保留每次官爵或尊稱主張的 `effective_period`、用稱錨點及事件類型。檢視器應分別呈現「當時任職確定」「任期未定、此處有用稱」「諡號或回顧用稱」，不能把未知起訖當無限期有效，也不能把初見當授予、把死亡當罷免。來源年月原文保留在 `date_expression`；已開始逐條年尺度換算，尚未完成全庫曆法換算與按公曆時間篩選，檢視器不得自行把年號字串當可比較日期。

此匯出是可重建的讀取層，權威資料仍是各篇來源與標註。無 AI 或網路處理需求。尚未接入家譜小程式或公開人物頁。

關係 `agnatic_cousin` 保存正文「從兄」「從弟」等同宗從兄弟稱呼，親等未定時 `qualifiers.degree` 為 `unknown`；不能由此補第一代表親、共同祖父或父子線。與 `brother` 相異的來源主張並列，`discrepancy_group_id` 可供檢視器連結分歧；該群組只提示差異，不自動選定其中一說。

出生排行存於關係主張的 `qualifiers.birth_order` 或 `qualifiers.relative_birth_order`，並直接匯出為 `birth_order_constraints`，消費端不需解析 `source_term`。每項約束保留主張 ID 與證據。

`長子`的 `ordinal` 為1，`scope: sons_of_parent` 表示在該父母的兒子序列中，不表示全部子女的第一名。`少子`暫記 `position: younger_or_youngest`、`ordinal: null`、`interpretation_status: ambiguous`；只有判讀明示最幼才另記 `youngest`。

兄弟相對先後記 `older_person_id`、`younger_person_id`、`operator: lt`；兩人的 `older_ordinal`、`younger_ordinal` 可均為 null。此約束表示先後，不表示相鄰，不推定同母或兩人生年。排序程式應合併所選人物同指，依約束作部分排序；有環則回報衝突，未連通者保持順序未定，不把可行的顯示排列回寫成確定出生排行。來源排行序列與展示排序分開。

目前先標註《秦始皇本紀》的扶蘇、胡亥與兩條弟關係，舊篇其他排行仍待逐條回填；不宣稱全庫已具排行約束。

籍貫與其他地址以 `address_assertions` 匯出，每項保存人物、`relation`、原文地名 `place.source_name`、來源與日期。`native_place` 不等於 `birth_place` 或 `residence`；未知現代對應與地點 ID 留 null，不自動使用現代行政區。地名錨點與地點登記仍待建立。目前先收錄卷九十三盧綰豐人及陳豨宛朐人，其他篇待回填。

早期傳記傳首「某某，某地人也」使用 `biographical_origin`（傳首所述出身地），保存原句；不推定後世制度化籍貫或戶籍。`native_place` 留作有相應來源判讀的籍貫記錄。

`death_place` 與 `burial_place` 分別表示死亡地、葬地，保留原文地名，無須今日行政區對應。始皇出生地邯鄲、死亡地沙丘平臺與葬地酈邑各存原文證據；不能由死亡地推定葬地，預定葬地也不直接作實際安葬。

紀年換算在編輯階段記為 `normalized_date`，並匯出到 `date_normalizations`。`year` 是整數，採天文年編號：公元1年為1、公元前1年為0、公元前259年為-258；`era: BCE` 與 `era_year: 259` 同時供顯示。不可把-258顯示成公元前258年。`original_quote` 是原文日期完整引句，另有篇段證據、跨段紀年承接、換算理由與參考資料。

目前先補始皇出生與死亡事件年份；葬地段落沒有明示日期，不自動用卒年填入葬年。年份換算不代表月日已換算，秦漢十月歲首可能跨公曆年；相對年份與疑年須各自判讀，未定者保留候選或不填單一年。換算是 AI 編輯判讀，人工覆核仍為 false，使用端不呼叫 AI。

「從弟」在 CBR 以 `qualifiers.kinship_structure` 拆記：`lineage: paternal`、`generation_difference: 0`、`collateral: true`、`distance: null`、`common_ancestor_person_id: null`、`subject_relative_age: younger`；原 `source_term` 與引句仍保留。現有 `agnatic_cousin` 識別碼在此表示廣義同世代父系旁親，不限定第一代表親。相對出生先後另有 older／younger 人物 ID，不能拿兩個家支的排行數字直接互比；跨家支排序的是出生先後約束，不是各父親兒子序列的同一排行。


## 各來源提及次數

`source_mention_summary` 按 `source_id` 統計本人物來源包內已標註的提及，列出 `mention_count`、`passage_count` 及可覆核的錨點與段落 ID，依次數由多至少排列。`most_mentioned_source_ids` 保留所有並列最多的來源；沒有提及則為空陣列。範圍遵循人物包的 `identity_policy`，採暫定同指時包含其候選 ID，但不計關係人物的提及。這是目前標註範圍的統計，不表示史料全文已標完，也不代表可信度、獨立見證數或來源優先次序。

`family_paths` 匯出有來源親屬陳述支持的家族ID路徑及其原文依據；分支字元不是出生排行。已發布序號ID仍永久有效。


`kinship_interpretation_cases` 分存有歧說的親屬詮釋，各候選包含可解析的關係、世代與長幼資訊及注家引句。`default_alternative_id: null` 表示尚未選定；使用端不得自行當成已確定關係或家族路徑。`reported_variants` 保存注家所報異文，`adopted: false` 表示未採入正文或關係，並非已完成底本校勘。


家族ID例：根 `abc_def_123`、子 `abc_def_123_A`、孫 `abc_def_123_AA`。`canonical_person_id` 是現行ID；`requested_person_id` 保留呼叫的舊或新入口。舊連字號ID列於 `id_aliases`，相容JSON入口保留；`index.json` 的 `persons` 只計現行人物，另有 `id_aliases` 對照。Markdown索引的ID用等寬字體。

`abc_def_123_*A` 表示源文明示的孫子、中間父親缺名。`family_paths` 另存祖父端點、世代距離及 null 中間世代；星號不代表實際人物、不合併不同缺名位置。Markdown索引以家族 `<details>` 區塊展開／收起後代，所有正式ID以等寬字體顯示；JSON索引完整列出人物，不受展開狀態影響。


`family_tree_decisions` 是可修訂的編輯判斷；`preferred_relations` 供預設繪圖，依決定選取來源主張或已選親屬詮釋，原始 `relations` 及其他詮釋不刪除。`editorial_preferred` 不冒作正文已明示或人工覆核。生父未定可明確採不畫生父線；不能由承爵或舍人控告直接補血親。此層不需執行時AI；尚未覆核的其他衝突仍可能存在。

`preferred_birth_order_constraints` 對應預設關係的排行約束，與原始 `birth_order_constraints` 並列；丁公弟解只提供相對長幼，序號仍為 null，不需NLU解析。

王室或法定父子可在預設視圖使用 `parentage_role: legal_or_dynastic`，並明示 `biological_parent_status: unknown`；不能把這種線當已核血親。跨候選人物的預設判斷須另列已有同指決定，仍保留該判斷的暫定身份狀態。

稱號有效期間端點若已有 `normalized_date`，同時匯入 `date_normalizations`，附 `record_id`、`person_id`、`endpoint` 與 `title`；原始端點及引句仍保存在 `title_holdings`，證據段落亦納入來源集合。未知端點不生成數字日期。
