# 人物來源包與家譜檢視器

以穩定人物 ID 讀取所有已標註的來源材料：

```sh
python3 scripts/person_bundle.py udu_dyy_4wd --output /tmp/jibu.json
python3 scripts/person_bundle.py jx9_cov_qe0 --include-provisional --output /tmp/luanbu.json
```

預設僅讀指定 ID。`--include-provisional` 明示選用庫內暫定同指的傳遞集合；輸出保留每項判讀、原人物 ID 與證據，不以同名自動合併。暫定同指不表示各來源的世系與年代全部一致。輸出涵蓋目前已標註材料，不能代表尚未整理的全部史料。

`mentions` 提供字元錨點；`passages` 保存正文、篇卷著作 ID；`sources` 提供固定版本與來源網址。`relations` 同時包含以此人為主體或客體的直接主張，`persons` 包含直接相連人物，可作家譜節點；沿相鄰人物 ID 再取來源包即可逐步展開。每條線保留主張 ID、方向、狀態及原文，矛盾主張並列，不自動選成唯一父系。

`title_holdings` 保留每次官爵或尊稱主張的 `effective_period`、用稱錨點及事件類型。檢視器應分別呈現「當時任職確定」「任期未定、此處有用稱」「諡號或回顧用稱」，不能把未知起訖當無限期有效，也不能把初見當授予、把死亡當罷免。來源年月原文保留在 `date_expression`；已開始逐條年尺度換算，尚未完成全庫曆法換算與按公曆時間篩選，檢視器不得自行把年號字串當可比較日期。

此匯出是可重建的讀取層，權威資料仍是各篇來源與標註。無 AI 或網路處理需求。閱讀器人物頁使用另行生成的顯示資料；本來源包供程式解析與下載，尚未改接家譜小程式。

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

`family_paths` 匯出有來源親屬陳述支持的家族ID路徑及其原文依據；分支字元不是出生排行。完成引用遷移的舊ID已撤除，歷史回查使用Git。


`kinship_interpretation_cases` 分存有歧說的親屬詮釋，各候選包含可解析的關係、世代與長幼資訊及注家引句。`default_alternative_id: null` 表示尚未選定；使用端不得自行當成已確定關係或家族路徑。`reported_variants` 保存注家所報異文，`adopted: false` 表示未採入正文或關係，並非已完成底本校勘。


家族ID例：根 `abc_def_123`、子 `abc_def_123_A`、孫 `abc_def_123_AA`。`canonical_person_id` 是現行ID；`requested_person_id` 保留呼叫的舊或新入口。完成遷移的舊序號或連字號ID不再提供永久相容入口；未完成身份覆核的來源候選仍各自保留。`index.json` 的 `persons` 列現行人物。Markdown索引的ID用等寬字體。

`abc_def_123_*A` 表示源文明示的孫子、中間父親缺名。`family_paths` 另存祖父端點、世代距離及 null 中間世代；星號不代表實際人物、不合併不同缺名位置。Markdown索引以家族 `<details>` 區塊展開／收起後代，所有正式ID以等寬字體顯示；JSON索引完整列出人物，不受展開狀態影響。


`family_tree_decisions` 是可修訂的編輯判斷；`preferred_relations` 供預設繪圖，依決定選取來源主張或已選親屬詮釋，原始 `relations` 及其他詮釋不刪除。`editorial_preferred` 不冒作正文已明示或人工覆核。生父未定可明確採不畫生父線；不能由承爵或舍人控告直接補血親。此層不需執行時AI；尚未覆核的其他衝突仍可能存在。

`preferred_birth_order_constraints` 對應預設關係的排行約束，與原始 `birth_order_constraints` 並列；丁公弟解只提供相對長幼，序號仍為 null，不需NLU解析。

王室或法定父子可在預設視圖使用 `parentage_role: legal_or_dynastic`，並明示 `biological_parent_status: unknown`；不能把這種線當已核血親。跨候選人物的預設判斷須另列已有同指決定，仍保留該判斷的暫定身份狀態。

稱號有效期間端點若已有 `normalized_date`，同時匯入 `date_normalizations`，附 `record_id`、`person_id`、`endpoint` 與 `title`；原始端點及引句仍保存在 `title_holdings`，證據段落亦納入來源集合。未知端點不生成數字日期。

程式索引的列可另含 `preferred_parent_status: unresolved` 與 `parent_decision_ids`，指明相關編輯決定暫不採用此候選的父系線。Markdown 同列標「來源候選；預設不接父系」，仍保留原 ID 及 JSON。家族式 ID 與表列人數包含來源候選，不代替預設世系；繪圖須讀 `preferred_relations` 並套用有證據的同指決定，不按 ID 前綴推造父子。`relations` 繼續保存被排除的原始主張。


## 年表逐人提及

`mentions` 繼續保存正文段落錨點。`table_occurrences` 另列全部目前已標註、符合本包身份範圍的年表人物提及，包含原提及 `id`、`person_id`、`surface`、`start`、`end`，以及 `table_id`、`table_fragment_id`、`table_row_id`、`table_cell_id`、work／book／chapter／source ID、`source_revision` 及完整原格 `quote`。同格多人、多次出現逐一保存，不把整格當成人物，不把格位偽裝成正文段落。

`table_passages` 按原格ID去重，附原格文字與全部標記、分表原欄題 `source_header`、表列座標及 `row_year`。後者保留既有年表的數位編者西元對照與其狀態，不是自動推得的生卒、授爵或官爵起訖。`sources` 同時包含提及及親屬證據所用表格的固定修訂、見證與核讀限制。未標註或未決指代不冒充已辨識人物。

`source_mention_summary` 的提及次數合計正文及年表逐人錨點；`paragraph_ids` 與 `table_cell_ids` 分列，`passage_count` 為不同正文段落與原格的總數。同格兩次出現算兩次提及、一個格位；其他人物在同格的標記不計入本人物頻次。`most_mentioned_source_ids` 仍保留所有並列最多來源，頻次不作史料權重。索引 `mention_count` 合計兩類，另列 `paragraph_mention_count`、`table_mention_count`，可檢查計數。

尚未完成CBR人物登記的年表獨立候選仍在閱讀器人物資料中分存；本來源包不因同名自動建立同指或家族，不能把此次匯出視為年表全部人物身份覆核完成。

### 固定來源合稱的普通 API

`person_bundle.load_catalog(root)` 與 `bundle(..., catalog=...)` 均驗證 `source_person_reference_group_set`。對具有已驗成員的本人 bundle，`source_person_groups` 保留完整來源合稱及成員 refs；對候選或編輯解讀涉及的本人，`source_reference_readings` 保留限定。這兩欄有資料才出現，`table_person_profiles` 只傳遞已驗 bundle 的原結構。個人 mentions／獨立出現頻次不加入群體詞；related people 不等於同場或親屬。

晉036為固定 WS2108231 rendered 比較單元，未知印本，非武英殿、非 preferred。21段7129字及唯一現代數位紀年腳注均保原層次。姓名中 literal 與有資格的來源內復姓分行，本源未明本名／字的稱法不機械拆分；文舒／左子邑的參校首選張昶／左伯另在來源閱讀保存，不冒本源字面。NER 首輪完成不等於本傳生平、親屬或爵年已全部型別化。
