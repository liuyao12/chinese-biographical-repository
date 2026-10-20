# 卷篇標註格式 0.2

`chinese_civil_year` 是另列曆法的年度標籤，不是確切公曆日期；可與具不同曆法意義的既有跨年範圍並存。其原紀年、同篇上下文、固定年表見證、數位編者對照及驗證邊界見 [中國曆年欄位](../docs/chinese-civil-years.md)。目前覆核與匯出涵蓋仍屬局部。

`witness_appended_edict` 保存數位見證附載的詔書文字層；只表示文本層次，不自行確定發布者、發布年或編入者。JSON 與 XML 的文字層必須一致，不能把後附詔書改作收到的篇正文。

總目標為逐書、逐篇收錄歷代正史與《資治通鑑》中出現的全部人物。目前依使用者調整的優先次序整理三國、兩晉、南北朝士族的跨史家系；《史記》《漢書》未完成工作仍保留，不以取得一份全文等同完成人物收錄。

## ID 與原文

`registry/works.json` 登記著作 `w-shiji`、原書卷 `b-shiji-001` 與篇 `c-shiji-001-wudi`。卷與篇恰好一對一時仍各有 ID；現代網頁便覽標題不當成古代篇。新增卷先登記歸屬，再錄正文。

`registry/persons.json` 登記現行人物 ID，採 `abc_def_123`、`abc_def_123_A` 等家族形式；字母不是排行，`*` 只標未名中間世代。ID 不重用給另一人；新家世證據需要上溯、合族或接合身份時，須更新全部引用後撤除舊號，保留可追溯的判讀及原文錨點，不設永久舊號別名或把舊號靜默重指另一人。每個異稱與人物提及都附來源；人物登記本身不是權威生平表。

`corpus/shiji/001.json` 保存正文、見證版本、權利、指紋、審閱狀態與提及位置。`source_id` 為本卷見證識別碼，來源資訊就地保存在 `source`；它目前不引用舊 `sources/` 目錄。這個區別須在舊資料遷移時明確處理。同一原卷可以有多個數位見證或選段，沿用原卷 `book_id`，各有獨立 `source_id` 與 `chapter_id`。平行版本不是另一獨立史書，不能當成多份獨立見證投票；引用哪一版就指向哪一版原段，不把另一版字句補進通行正文。

每個段落有唯一 ID，每個提及有唯一 ID、`start`、`end`、`surface`。位置為段落內 Unicode code point，起點含、終點不含；JavaScript 使用 `Array.from(text)`，不可直接把 UTF-16 字串位置當此格式的位置。所有提及不重疊，依起點排列。人物提及含 `person_id`；未定指代的 `person_id` 為 `null`。

## 行內文本

XML 是 JSON 的同步可讀表示，使用本庫自訂的小型格式，不冒稱符合 TEI：

```xml
<text work-id="w-shiji" book-id="b-shiji-001" chapter-id="c-shiji-001-wudi" source-id="s-shiji-001-wudi">
  <p id="c-shiji-001-wudi:p001"><persName ref="cbr-p000001">黃帝</persName>者，……</p>
</text>
```

實際文件另含提及 ID；`persName` 引用人物，`rs type="unresolved"` 保存未定個人、氏族、群體、國號或職稱。去掉標籤後必須逐段精確還原 JSON 正文，標籤不改寫史料。篇的 SHA-256 取各段正文以兩個換行連接後的 UTF-8 位元組，不含結尾換行。

## 身份、群體與傳說

同篇異稱判斷置於 `001-identities.json`，區分 `source_explicit`（原文明示）與 `contextual_provisional`（依上下文暫定）。每項引文連到所屬段落，保留 AI 代理署名；不得冒稱人工審閱。正文中的名稱、國號、姓氏與官職各有語義，不以字面相同強行合併。人名串也可能出現在地名或普通詞中，例如「軒轅之丘」「象以典刑」「九男皆益篤」，不可全域替換。

《五帝本紀》中的上古人物用 `legendary_tradition` 表示其傳說敘事性；孔子與宰予用 `historical`。此欄不是對每條史料內容的真實性背書。無名個人可獲 ID，但未能分辨成員的群體只留未解錨點，不依外部熟知故事補出姓名或人數。羲、和、四嶽、帝鴻氏等仍須專門研究，不提前認定。

## 完成程度與使用端

`named_mentions_first_pass` 只表示首輪明示人名檢視。代詞、官稱、匿名者、群體、版本校勘與跨篇身份比對未完時，進度不得標為完成。未定條目與傳說人物仍保留可追蹤狀態；完成不要求把學術未解問題強行解決，但必須完整記錄審閱結果。

小程式可直接載入 JSON，依 ID 組裝人物及來源陳述，不需把文本交給 AI。XML／JSON 不應作可執行程式。原有唐代 `sources/` 與 `assertions/` 尚待遷移，新進度不將它們計作已完成的卷篇。

執行 `python3 scripts/validate_corpus.py` 檢查字元位置、人物／卷篇引用、證據、指紋與 XML 還原一致性；這些檢查不證明人物比對或古文讀法正確。

## 跨卷身份與來源親屬主張

`002-identities.json` 的 `scope` 區分同篇與跨篇；`chapter_ids` 明列範圍，跨篇判斷須逐篇附原文證據。跨卷連續敘事可暫定共用既有 ID，但不把同名變成全域匹配規則。每項 `surfaces` 必須能在該人物的來源提及中找到。

`002-assertions.json` 保存來源陳述，`subject_person_id`／`object_person_id` 為人物端點；`evidence` 同時連結篇、來源、段落與精確引句。`source_attested` 表示原文記載，並非已證實的生平。`qualifiers` 保留原稱與敘事性；父親、母親、兄弟、配偶、祖父、曾祖父與祖先分開，不從繼位順序推導父子。使用端按已記錄主張組裝，遇異說仍需同範圍的取捨決定。

`next_number` 是單調遞增的 ID 分配游標，允許保留草稿已分配但尚未公開的號碼；不可為消除空號而重編既有 ID。稱號時段另待與 `data/name-history.json` 協調，本批不發布尚未整合的稱號草稿。

以 `python3 scripts/render_corpus.py` 重建 XML；`--check` 只檢查同步，不改檔。JSON 是編輯來源。

## 人物區分與敘事性

`003-distinctions.json` 的 `person_distinction_set` 記錄容易因同字而錯併的不同人物；每項有不同的 `person_ids`、判斷狀態、理由與逐段原文證據。區分判斷可覆核，不能用它反向合併同名者。驗證器要求各端點有來源段落，且端點不得重複。

人物登記的 `historicity: historical_tradition` 只表示來自歷史敘事，不表示身份、生平或世系已獨立確證；商代王名與譜系須另與出土材料及專門研究對讀。`legendary_tradition` 仍保存來源敘事的傳說性。兩者都不替代每項主張的證據與審閱狀態。

## 分段標註進度

長卷可先錄全篇、再逐段標註。採用分段進度的卷篇，每段都有 `annotation_status`：`pending`、`in_progress`、`named_mentions_first_pass` 或 `reviewed`。`pending` 不混入已接受提及；尚有待處理段落時，篇及書目進度都須為 `in_progress`，不得宣稱首輪完成。下一工作位置留在同卷的具體段落，不因取得全文而移往下一卷。XML 的段落同步保存 `annotation-status`，只讀 XML 也能辨別尚未標註的段落。

數位見證的現代校勘符號不當作古文。卷四的 `source.normalization.editorial_readings` 另存見證符號、正文採用的讀法與限制；有成對改讀時保存改讀前的字，不擅以改讀當定論，後續須核對底本及校勘來源。

## 姊妹關係

來源親屬主張可用 `sister` 表示主體為客體的姊或妹；`qualifiers.source_term` 保留「姊」「女弟」等原詞。與 `brother` 一樣，不單據兄弟姊妹稱呼推定同父同母，不補原文未見姓名。

`adoptive_father` 的首種受支援來源形式為明言「出繼伯父」：主體為出繼者，客體為具名出繼父。`adoption_basis: chuji_named_paternal_uncle` 保存此判讀，`source_term` 保留包括名字及其間官稱的完整原詞；`biological_father_assertion_id` 與 `paternal_uncle_assertion_id` 須指向同段、同一主體的生父與伯父記錄。三項證據均須保留具名人物錨點，不覆蓋生父，也不把一般伯父或宗祀承繼一律改作出繼。`modern_legal_status: not_inferred` 表示不推定現代法律地位。其他出繼語式須另行核讀及擴充驗證，不能套用此特定格式。

引語中「下官曾祖」可在人物身份判讀另存 `ancestor_reference.kind: speaker_paternal_great_grandfather`：保存發言人自稱及發言人姓名錨點、所指曾祖錨點、四人的 `person_path` 與三條 `steps`。每條須有明載父子斷言，或已驗證的「同段連續具名祖先」編輯接合；不得從 ID 字母或最近的人名猜測世系。此身份解析不改寫原句，也不把編輯父子推導冒作直接原文。由此記錄「曾祖是某外孫」時，使用母系 `grandfather`，`resolved_subject_identity_decision_id` 連到上述判讀；未名母親保持 `mother_person_id: null`。所指外祖不得併入父系三代。

婚配斷言仍用 `spouse`。目前受驗證的「尚某主……遂離婚」同段格式，另存 `qualifiers.marriage_termination: {kind: "divorce", source_term: "遂離婚", date: null}`；保留婚配原詞及夫妻雙錨點，不以離婚刪去曾有婚姻，也不補年月。人物卡保留可導航的配偶並註明據原文離婚。其他終止形式或有年可考的事件須擴充驗證後另記，不把喪偶或分居自動當作離婚。

相對紀年「明年」「其年」使用 `regnal_year_mapping.kind: relative_ce_regnal_era_span`，保存前述原數詞、`regnal_year`、`target_regnal_year` 及 `year_offset`（分別為一、零）。`source_expression` 保留相對原詞；`relative_year_reference` 保存明示年號、承接年次的原字及各自證據索引，與事件原句一起驗證。不得把補出的完整年號年份寫成原文；跨段須保存連續原段的紀年證據及人物承接。仍按中國曆年度存公元數字，不由報齡倒推出生年，也不以任官背景年填卒年。

本紀在一年的月日條目省略年號時，可用 `regnal_year_mapping.kind: annal_ce_regnal_era_span`。本段原詞仍存於 `source_expression`；`annal_year_reference` 指向原段 ID、原行及 `source.annal_year_sections` 的年段 ID。年段保存固定修訂、首尾行、完整原始上下文及 SHA-256，須同時包含明示年號年次的年段標題、正文相符的年次起點和下一年界線；原段必須逐字位於其間，不能跨年或借用另一篇的年段。`context_reference_index` 指向這份分列的原始來源上下文，`reference_index` 指向現代年號起迄對照。驗證同時核算年份及綁定登記篇章，不能只讓數字算式相合。此上下文不是已完成逐人標記的整年正文，也不會把補出的年號寫回月日原句；仍只存中國曆年度，不推公曆日或出生年。

省略年號而明載「六年」等年次時，`relative_year_reference.kind: omitted_era_regnal_year` 保存原年次，`year_offset: 0`，並引用前文明示年號的原段。事件只採其直接任用語段所屬的年次；後文轉任不一律套同年，跨改元敘事不能反取後段年號。

「年向九十」的 `approximation.kind: approaching_age` 保存 `target: 90`，`value`、`birth_year` 為 `null`，不存嚴格上下界。`speaker_scope` 保存奏表開頭及本人「臣」字錨點，避免把引禮的七十或君主稱謂當作本人報齡；來源的精確或其他約略報齡各自保留，不互相改寫。

同一次授號或追諡事件的跨史紀年取捨，可在首選持職記錄存 `chronology_preference.kind: same_event_source_preference`：`preferred_holding_id` 指本筆，`candidate_holding_ids` 列全部候選持職 ID。各筆須屬同一人物、相同事件種類及稱號，並各存原句與不同數字年份；「鎮／鎭」原字不改。`rationale` 記該事件的來源判斷，`status: editorial_provisional`、`human_reviewed: false` 不冒充終局裁決。人物卡標出首選，人物頁仍呈現另篇原記及取捨理由；此欄不給整部書永久優先權，也不消去其他候選時段。

未受任記錄可用 `role_anchor` 保存原段職稱的獨立字元範圍，免於在人物提及層插入整段職稱，尤其職稱內已有府主的人物標記時。其欄位為 `paragraph_id`、`start`、`end`、`surface`，須逐字等於 `title`；舊有 `role_mention_id` 仍支援。「廬陵王師」等格式另用 `patron_person_mention_ids` 指一位職稱內、前綴位置的具名王號；它是府主而非另一受任者，不能拿來略過任用句中任意其他人物。任用詞、未受詞及本人或前段本人承接錨點仍須完整驗證。未拜的職位與後來實任同職各自記錄，不合成連續任期。

## 數位見證附載文字

有分層需要時，段落保存 `text_layer`，XML 同步 `text-layer`。`received_chapter` 為本篇所錄傳世文本；`witness_appended_bangu_note` 表示數位見證附載的班固記，不能冒稱司馬遷原文。保留原有次序與引用錨點；分層判斷仍需版本核查，不據此宣稱已校定作者或年代。

`witness_appended_suoyin_zan` 保存數位見證以「索隱述贊」標明的附載評論。卷三十六末段用此層次，人物提及及引用仍可追溯；不能將該段當作司馬遷正文或與正文互為獨立證據。標題辨層不表示已核定底本、作者或撰寫年代。JSON 與 XML 的層次須一致，其他未知層次仍拒絕。

`witness_appended_chu_note` 保存數位見證明署「褚先生曰」的附載文字及其中引文。卷四十八第21至26段用此層次，所引「賈生之稱」保持在褚先生文字內，不當成另一份獨立見證。這是按署稱辨層，未宣稱已核定褚氏、賈氏姓名、文本底本或成文年代；原次序、人物錨點與 XML 層次仍須同步。

## 父系叔父

`paternal_uncle` 保存原文明示的父系叔父關係，主體為侄輩、客體為叔父；`qualifiers.source_term` 保留「季父」等原詞。此關係不能改作父親，不推導原文未見的父親身份、同父同母、排行或其他兄弟關係。稱謂是否屬親屬而非尊稱仍須按語境判讀。

`maternal_uncle` 保存「姊子」明示的甥舅關係，主體為甥、客體為舅。`qualifiers` 保存原詞、`lineage: maternal`、`generation_difference: -1`，以及 `mother_person_id: null`；本句未名母親，不因來源別處可識別母親而改寫本句。負世代差表示客體較主體早一代。

`kinship_generation` 保存「大父行」的祖父輩親屬，主體為單于、客體為所述親屬。保存 `source_term: 大父行`、`generation_difference: -2`、`lineage: unspecified`、`direct_ancestor: null`、`exact_distance: null`。此處只記世代，不生成父子路徑、祖父節點或已確定的父系親等。

篇章 `annotation.age_assertions` 保存來源所報年齡，逐人 JSON 同名欄位匯出。數值 `value`、原數詞 `source_number` 與 `source_term` 分開保存；`unit: source_age_years`、`counting: unspecified_source_age`、`birth_year: null` 不推定計歲方式或反推出生年。證據連到人物錨點與原句；`normalized_date` 是報齡所屬事件年，日期索引標 `date_role: age_attestation`，不作出生事件。支援「年」後或「歲／歳」前的一至九十九數詞，保留來源實際字形；其他報齡形式需擴充驗證後保存。

## 同指判斷與已套用的身份整併

`person_equivalence_set` 保存有證據的同指判讀。尚未套用時，`person_ids` 包含兩個或以上候選，`canonical_person_id` 必須屬於其中。按使用者最新要求，全部引用更新且驗證通過後撤除重複人物登記與 JSON，不永久保留舊 ID 別名。

已套用的判斷標 `identity_materialized: true`，`person_ids` 僅含現行人物 ID。判斷 ID、精確引句、各來源提及錨點、理由及暫定狀態仍保留；至少須有兩個不同提及錨點，不能僅把單一提及標為同指。正文、提及 ID 與字元起訖不變，僅人物引用更新。整併不代表人工覆核或消除來源衝突；撤回使用 Git 歷史及相應引用遷移。

原未決案件因已有同指證據收斂為一人時，移至 `annotation.resolved_identity_cases`，保存案件 ID、原段落、人物 ID、同指判斷 ID 與暫定說明；逐人 JSON 同時匯出案件與原段落，不能只留下結論。

## 稱號持有、用稱與有效時段

`007-titles.json` 的 `title_holding_assertion_set` 將來源所述授予、自立、貶降與單純用稱分開。每筆 `holding` 有穩定 ID、人物 ID、原稱、種類、`mode`、來源引句及獨立 `attestations`；每個用稱錨點按 Unicode code point 保存位置，並引用同句／同段的人物提及。此層可與人物文字標註重疊，不能因此改寫原文或換掉人物錨點。

`effective_period.start`／`end` 各為 `unknown` 或 `source_event`。未知端點沒有日期或事件，不表示無限延伸。來源明示事件必須列起訖事件種類及精確證據；`date_expression` 僅在端點引句明見日期時填原表述，否則為null。本批日期皆未換算，來源事件位置只提供敘事中的端點證據，不冒稱某一公曆日或完整數值區間。

授予、自立與貶降可支撐起點；終點須另有廢黜、辭讓、撤銷或明示終止的證據。單純首次用稱不等於持有開始，死亡不自動終止全部爵位。持有模式不自動推定其他官爵同時停止，也不把追稱當成實任或追贈。`kind: unclassified` 保留尚未核定制度種類的稱號。

`attestations.usage` 區分一般敘事、追稱暫解與死後用稱。赤泉侯在卷七第41段先被用稱，第42段才敘封楊喜；保存兩處，授予起點證據仍是後段，不能因文中先出現而前移。魯公葬禮用稱不等於補造追贈事件或以死日截斷持有。韓王成被廢為侯有王號終止及侯號起點的兩筆來源事件，日期仍未定。

官職可另記 `jurisdictions`，以 `source_name` 列出同一原文用稱所屬的歷史地名；`place_id` 與 `modern_identification` 保持 null。卷一百〇九「隴西、北地、鴈門、代郡、雲中太守」保存共享用稱「太守」及五個原地名，並非五次可排序的任官，也不推定連續任期。每個地名須見於該筆來源引句。

卷七55項只是可追溯試點，尚未覆蓋全部官稱、日期換算、兼任／檢校／追贈及跨來源衝突。這個格式未冒充既有 `data/name-history.json` 的完整替代，也未接入線上讀者介面。驗證器檢查引用、字元位置、端點及日期表述，不能替代制度史與史料判讀。

卷八另有33項稱號試點，包含劉仲、趙王敖、彭越的明示廢黜終點。第88段高皇帝為死後尊號用稱，第88段承襲皇帝者另連孝惠，不改作高祖繼續在位。卷七韓信自立齊王與卷八漢王遣張良授印之說並存，尚未指定優先來源。

同指決定可明列 `scope: cross_chapter` 及 `chapter_ids`，各篇須有自己的來源、精確引句與端點提及；缺少任一篇證據即拒絕。省略範圍的既有決定仍限所屬單篇。跨篇不改寫任何已發錨點或人物ID。

## 相鄰段落的世系承接

人物陳述預設要求雙端見於每段證據。明名父親在前段、後段以「子某立」承接時，另存 `context: {"kind": "adjacent_paragraphs", "paragraph_ids": [前段ID, 後段ID]}`。兩段必須同篇、依原序直接相鄰，且與證據列表完全一致；前段引句須含客體人物錨點，後段引句須含主體人物錨點。此格式保存有理由的局部承接，不許任取遠段、倒序、只在段落別處出現端點，或補造文字錨點。主張仍須說明子字與世系主語的判讀；通過驗證不證明古文讀法或史實。

稱號來源事件省略人物主語而直接承前段時，證據可另存 `context.kind: previous_paragraph_subject`，附前段 `paragraph_id`、`person_mention_id` 與精確 `quote`。驗證要求前段同篇且直接相鄰、錨點屬於該稱號持有人並在引句內。此為有理由的省略主語判讀，不能任取遠段或以同名套用；事件本段原文不補字。


## 家族式人物 ID

新候選使用 jiapu-mp 的9位隨機小寫英數家族根與單字元世代分支，例如 `abc_def_123`、其子 `abc_def_123_A`、孫 `abc_def_123_AA`。根是目前可建立的局部家族錨點，不表示已知始祖。分支字元是分配槽，不表示長幼排行；排行仍以有來源的結構化約束另存。分配檢查重複及已占用的後代分支。

以來源可靠性及關係判讀配置家族，不限父子。明示祖孫等有世代距離的近親，即使中間缺名亦可同根；例如祖父 `abc_def_123` 與孫 `abc_def_123_*A`。`*` 只標記缺名世代，不建立人物；不同星號位置不自動指同一人。遠祖牽合、親等未定及有爭議世系分存來源主張，是否同族須另作有證據的判讀，不能由編碼自動推定。配偶、母系及收養關係另記。

人物 ID 為目前版本的內部識別碼，不承諾永久外部入口。合併、分拆或改父系需要改號時，須更新全部人物端點、正文提及、來源判讀、家族組裝及衍生索引，驗證後撤除舊登記與舊 JSON；不維護永久別名、轉址或舊號對照表，也不將舊號重用給另一人。外部查詢流程是每次搜尋、辨識並選取目前人物，再使用當前 ID 讀取資料；不以保存的舊查詢或人物 ID 作相容性要求。來源與身份判讀理由仍保留，過往版本由 Git 歷史回查。

關係記錄同時保存 `subject_person_id` 與 `object_person_id`，每人 JSON 由這些來源記錄產生，收錄本人出現在任一端的關係。父子、婚姻等因此可從兩端查閱同一筆來源斷言，不手工維護兩筆互為反向而可能失步的事實。人物登記的提及證據與正文標記也作雙向核對；改號後必須重新生成並檢查全部引用，而不只修改人物自己的 JSON。

## 親屬詮釋分歧

篇章 `annotation.kinship_interpretation_cases` 保存兩端人物ID、原詞、正文證據及各有署名注語支持的 `alternatives`。`default_alternative_id: null` 表示未選定；使用端不得自動轉成確定關係或家族ID路徑。`object_generation_relative_to_subject` 明確標示客體相對主體的世代位置。`reported_variants` 區分已存正文與注家所報、尚未核底本的異文；`adopted: false` 不改正文、不當另一個已核見證。

家族根沒有尾隨分隔符；只有世代路徑前加一個底線。舊格式 ID 已在全部引用更新後撤除，不再匯出相容 JSON。人物包以 `canonical_person_id` 明示現行 ID；歷史對照使用 Git。格式遷移本身不表示新增身份或世系證據。

跨缺名世代的 `family_path` 使用 `ancestor_person_id`、`connection: grandfather`（或相符關係）、`generation_distance` 及全為 null 的 `intermediate_person_ids`；`parent_person_id` 為 null。每條路徑須有同端點、同關係的原始陳述與逐段證據。路徑是 AI 編輯判讀，`human_reviewed: false`；不是由ID推導的新增世系。全庫ID對照及未編入路徑的原因見 `registry/person-id-migrations.json`。


## 預設編輯世系

`family_tree_decision_set` 記錄預設採用的來源陳述ID、排除於預設視圖的陳述ID、父親端點、理由、可信程度與完整證據。原始主張均保留；排除只作用於預設繪圖。`preferred_parent_person_id: null` 表示編輯判斷生父未定，不是遺漏待使用端補猜。

親屬詮釋可由 `default_alternative_id` 配合 `selection` 選定編輯預設；必須匹配已存候選並記理由、可信程度及未經人工覆核。分歧案例本身仍保留。人物包分別匯出原始 `relations` 與 `preferred_relations`，後者套用已存預設判斷、無需 AI；未審閱的其他衝突仍可能存在。

### 稱號事件的數字紀年

`effective_period.start` 或 `end` 的 `status: source_event` 可附 `normalized_date`，格式同地點事件紀年。換算須附本筆事件段落內可找到的 `original_quote`、原始 `date_expression`、換算理由及參考；其他篇章只作紀年承接證據，不能代替本筆事件引句。`status: unknown` 不得附數字日期。天文年編號另以 `era`、`era_year`供一般顯示。

人物ID遷移記錄的 `person_count_scope: at_migration` 表示 `person_count` 是遷移當時的快照，不是此後全庫人數；新增人物仍須通過現行家族ID格式驗證，舊別名映射保留。

地址關係 `ancestral_origin` 保存其先等祖先出身表述。人物ID是敘事所屬人物，`qualifiers.subject_scope: ancestors_unspecified` 明示地點屬未具名祖先；不改作本人籍貫，不指定祖先ID或世代。

`witness_appended_zhengyi_note` 保存數位見證明標〈正義〉的附載文字，與列傳正文、答詔引語及索隱贊分層。這只是見證署稱，不表示已校定作者、篇章原位或版本；XML 必須同步文字層次，不把注釋當另一份獨立正文證據。

## 子女排行範圍

`qualifiers.birth_order.scope` 使用 `sons_of_parent`、`daughters_of_parent` 或 `children_of_parent`，分別表示兒子、女兒或所有子女的排行序列。不得把兒子序號當作所有子女的序號。卷一〇五緹縈的「少女」使用女兒序列，`ordinal: null`、`position: younger_or_youngest`，保留較幼與最幼的歧義；原文五女不單獨證明她是第五女。家族 ID 分支仍不表示排行。

## 用稱年份與授任起訖

`attestations` 可另保存 `date_expression` 與 `normalized_date`，記錄來源在何年使用該稱號。此年不作授爵、任職起點或終點；`effective_period` 仍獨立保存，未知時保持 `unknown`。

稱號可另附 `reported_duration` 保存來源明記的在位年數：`value` 為正整數，`unit: regnal_year`、`counting` 可為 `inclusive_regnal_years` 或 `unspecified_source_years`、`status: source_attested`；`source_number` 保存原數詞，`source_term` 保存含年數的原詞，`evidence` 指向有持有人錨點的篇段。例如「立十三年死」保存數值 13 與原詞「十三」；「立十歳而死」保存數值 10，來源的「年／歲／歳」原字均保留。前者表示有依據的含起年計數；後者保留來源年數但計年方式未定，例如兒單于「立三歳而死」與起訖紀年不直接相合時。兩者均不是完整公曆年長度，不推精確起訖日，也不以死亡自動終止全部官爵。敘事中「立三年」表示在位第三年的時點，不作完整任期；留置或出使年數也不作稱號在位年數。現行驗證支援一至九十九的標準中文數詞，其他形式須先擴充有測試的轉換與驗證，不可略過證據檢查。

若本段沒有明言紀年、而由前文連續事件暫定年份，`date_expression` 為 `null`；`normalized_date.evidence` 同時列本段原句與前文紀年，理由說明承接及限制。不能因檢視到某年稱呼便把官爵起訖填入同年。換算仍為 `editorial_provisional`、年精度及未經人工覆核；只用核讀過的年對照，不默改原文月日。

卷一百零七將恬在元朔三年的武安侯用稱與其春嗣爵分開；其春未定公元年，不能把元朔三年的來源使用當成繼封起點。

### 家族組裝的缺代連接

組裝節點可依正文的 `grandfather`、`great_grandfather` 或已知距離的 `ancestor` 關係接入同一父系。這類節點保留 `parent_person_id: null`，另存 `ancestor_person_id`、`connection`、`generation_distance`、`intermediate_person_ids` 與 `source_assertion_id`；每個未知中間世代是 `null`，ID 對應位置為 `*`，不登記虛構人物。祖先必須是本組裝中的節點，來源斷言的祖先端點須屬於該節點的來源候選，世代距離及 ID 路徑由驗證器核對。

例如卷一百零七「高祖孫」的淮南王安接為 `yqp_nlb_p1p_A*A`，祖先是劉邦 `yqp_nlb_p1p_A`，父親未定。消費 JSON 的程式須讀取祖先與距離，不可把 `parent_person_id: null` 一律當作獨立家族，也不可把星號當成已知父親。

逐人匯出的 `date_normalizations` 亦收錄用稱換年，以 `date_role: attestation` 與 `attestation_id` 區別，不使用授任的 `endpoint`。涉及未決身份時，人物 JSON 附 `unresolved_identity_cases`、所有候選人物及所引用段落；候選只作待辨資訊，不併入 `person_ids`，也不自動選定人物。

未決身份案例的 `paragraph_ids` 可列本篇未決用稱及其他已收錄篇的候選身份證據，但至少須有一段屬於本篇；每位候選都須在所列原文段落有已標註提及。外篇引用不構成同指決定，候選仍不合併。

官職資料可用 `appointment_role: acting` 明標來源所述代理職務，例如「行丞相事」；這與來源用稱的 `mode: attestation` 分開，使用端不必靠自然語言推定代理性質。缺少此欄位不自動表示正式實任。

生卒事件的紀年若承接同篇連續敘事，可記 `date_context.kind: continuous_paragraphs`、依序的 `paragraph_ids` 與具體 `rationale`。證據須含二至四個連續段落，各段都有事件人物在引句內的錨點；日期預設在首段。若後段重新敘述同一事件並補明紀年，須另以 `date_paragraph_id` 明指其中含原日期表述的段落，不得默認後段日期可套前事。數字紀年仍為代理判讀。卷一百〇九李廣自剄以第十二至十四段承接元狩四年，暫換前119年；卷一百一十烏維死亡在第四十八至四十九段重述，第四十九段明言元封六年，記前105年。各原句保留，不以年齡反推生年，也不據卒年截斷全部官爵。

## 生卒事件

親屬陳述可用 `qualifiers.posthumous_birth: true` 保存明示「遺腹子」，父親端點與原詞必須存在；不補出生年或母親。`kinship_unspecified` 保存「有親」但未明種類的親屬陳述，不指定親等、父系或姻親，也不能作家族組裝的父子證據。

`108-life-events.json` 的 `person_life_event_assertion_set` 保存原文明示的 `birth` 或 `death`，每筆 `events` 引用人物、篇及含人物錨點的精確事件引句。`date_expression` 為原文日期或 null；數字年另存 `normalized_date`，保留原句、參考與 AI 判讀。未知日期不補數值，日期精度不高於證據。逐人 JSON 可直接讀 `life_events`，日期索引以 `date_role: life_event` 與 `event_type` 區分；死亡事件不改寫官爵端點。

`stepmother` 表示原文明示的後母：主體為子女，客體為後母，不作生母或自動補父親的婚姻。

`mode: accession` 與稱號起點的 `event_type: accession` 保存來源明示的繼位（例如子稽粥立）；不等於授予或自立，不由前任死亡自動推新任日期。年月未知時保留 `date_expression: null`。

## 原文無明示紀年的平行事件定年

原文日期為空時不得補造日期字串。已核讀他書同事件及其編年時，可在 `normalized_date.basis` 記 `kind: parallel_event`、本篇精確事件引句 `source_event_quote`、參考 URL `reference_url`、他書事件原句 `reference_event_quote` 及紀年標題 `reference_year_quote`。參考列表分別以 `received_parallel_event` 與 `digital_editorial_regnal_year_equivalence_only` 保存兩項引句與相同 URL。年份保持代理暫定並附具體判讀，不暗改來源紀年、事件異說或提高精度。授任與死亡的日期可依此對讀定年，原日期欄仍為空。驗證要求引句、來源錨點、兩層參考與年編號完整；它不證明兩事件同指的學術判讀。

同父的多步兄弟組裝使用 `parent_connection.type: shared_father_through_sibling_chain`，`sibling_person_ids` 與 `sibling_assertion_ids` 依順序一一相接，最後由 `sibling_father_assertion_id` 連到所選父親。每步必須有方向相符的兄弟原始陳述，同族同父候選節點不得重複；終點須有明示父親陳述。此為 `contextual_provisional` 編輯組裝，須保存判讀與補證，`source_assertion_id` 為 null，不能把多步推定抄成原文明記父子或同母。原有單步 `shared_father_through_sibling` 仍可使用。

平行事件參考的紀年若是另一篇古代正文明言，例如大宛列傳「是歲元朔六年也」，使用 `received_regnal_year_attestation`，與 `digital_editorial_regnal_year_equivalence_only` 的數位年標分開。兩者仍須和事件引句分列且連到同一參考 URL；原篇未明日期時保持 `date_expression: null`，數值換算及判讀理由另存。

`reported_duration.unit: title_year` 保存「既侯三歲」等來源明記的持號年數，與君主在位的 `regnal_year` 分開。首批只用 `counting: unspecified_source_years`，原詞、數詞及人物證據俱存，不推定完整公曆年時長或任期終點。

父子承爵原文僅稱「侯」時，可用 `inheritance` 保存獨立的暫定判讀，不擴寫 `title` 或用稱錨點。`predecessor_person_id` 與 `predecessor_holding_id` 指向有來源的父親及其爵位；`resolved_title` 必須等於該爵名，供使用端直接解析。`source_term`、`evidence`、`rationale` 保存承爵原語與理由，`status: contextual_provisional`、`human_reviewed: false`。驗證接受 `noble_rank` 或 `royal_rank` 的 `accession`，全鏈爵位種類須一致，須有同一承爵證據段落的父子陳述，不能按相同「侯」字跨人物匹配。日期、來源年數與國除事件仍各自保存，不能以計年差值倒改明示紀年。此欄位是編輯判讀，並非聲稱原文寫出完整爵名。

`grandmother` 在外孫原句中保存母系祖母：主體為外孫、客體為祖母，原詞 `外孫`、`lineage: maternal`、`generation_difference: -2`、`mother_person_id: null`。本句未名母親不從別段補寫，母系關係不接入父系家族 ID。

`reported_duration.unit: title_month` 保存來源明記的持號月份數，例如「陳勝王凡六月」以 `value: 6`、`source_number: 六` 與 `counting: unspecified_source_months` 記錄。此處是六個月的來源時長，不是曆月六月；來源是否包含起月未知，不推精確起訖日。月份單位只接受含「月」的原詞，與年數計數方式分開驗證。

`mode: posthumous_grant` 及同名起點 `event_type` 表示來源明示的死後追尊，與生前 `grant` 分開。須附 `posthumous_basis`，包含原文含「追尊」的 `source_term` 及與起點完全相符的 `evidence`；未知日期維持空值。安成夫人與父親共同追尊的完整句保留，不由一般用稱或死亡單獨推得追尊。

### 同一生卒事件的回述

同一人物的死亡可在不相鄰段落回述。`date_context.kind: same_event_attestation` 明示這些引句是同一事件的重述，不表示中間段落共享紀年。`paragraph_ids` 必須精確列出事件證據段，`date_paragraph_id` 必須為首筆證據段，且該段同時含原日期與 `source_term` 事件詞句；`rationale` 說明同指及差異。日期不從另人的事件或後段用稱借入；其他引句與不同死亡方式敘述完整保留。原有 `continuous_paragraphs` 承接仍要求連續段落，不因本型別放寬。

### 死後諡名

`mode: posthumous_naming` 與起點 `event_type` 保存來源明示死後諡名，例如「相國何卒，諡為文終侯」。`naming_basis` 明列 `source_term`（含諡／謚為或曰及本筆原稱）、`death_term`（同一證據內的死亡句）與完全相符的起點 `evidence`。它與追尊授號分開；一般死後用稱不自行生成命名事件。原紀年與數字年分存，未見具體日不補日；未知終點不視為無限有效。

### 承爵鏈與跨稱號來源年數

父子連續代侯可沿已記錄的 `inheritance.predecessor_holding_id` 回查前任，直至有原稱的爵位記錄。每一連結仍須有相符父子陳述、原代侯詞及同段證據；循環、缺前任與根爵不符均拒絕。不改原文侯字，`resolved_title` 只表示有限來源範圍的暫定判讀。

`duration_scope` 明示一筆 `reported_duration` 涵蓋多項同人同類稱號，而非本筆單一稱號任期。欄位為 `kind: multiple_holdings`、穩定 `holding_ids`、`relation: successive` 或 `unspecified` 及 `rationale`。例如相齊九年涵蓋齊相國後改齊丞相；將軍中尉凡二歲未明先後或兼任，關係保持未定。使用端須依此範圍讀取年數，不能按每項稱號重複加總或推精確起訖。

死後諡名原詞亦可為「謚懿侯」等省略為／曰的句式，死亡詞、諡詞、本筆原稱與起點證據仍須相符。

群體原語「年皆八十有餘」報齡可存 `value: null` 與 `bounds`：`lower: 80`、`lower_inclusive: false`，上限及上限包含性為 `null`。`source_number` 與完整 `source_term` 保持；`group_reference` 保存四人原語、具名名單原語及四個人物ID，須與同段姓名錨點一致且包含本人的ID。每人獨立引句，不把下界當精確歲數，不推出生年。明示「四人從太子」時名單須有四人。另支援「貫髙、趙午等年六十餘」的具名子集：`group_reference.additional_members_unknown: true`，`source_term` 保存含「等」的群體詞，`naming_term` 保存同段具名片語，`person_ids` 僅列該片語實際人物錨點，並包含本筆本人。不能把名單長度當群體總數；年六十餘下界為六十且不含、上界未知，不推出生年或定計歲法。其餘原語形式仍待擴充。

死後諡名的原詞須以諡／謚、可省略的為／爲／曰與該諡名連接，不得僅因同一長引句另處出現此稱號便當作命名依據。原爲異體保持，省略為字的謚懿侯等亦保留。

地址引句省略人物主語時，可另存 `evidence.context`，種類 `previous_paragraph_subject`，含前段 `paragraph_id`、人物 `person_mention_id` 與實際引句 `quote`。只接受同篇緊鄰前段，人物須與地址主體一致且錨點在前段引句中，另有判讀說明；主段地名與行程原詞仍須在本段引句。不在原文插入姓名，不按最近人物自動猜測主語。

稱號來源月數含餘字時，可用 `reported_duration.value: null` 與 `bounds` 保存排他下界及未知上限，單位 `title_month`、計法 `unspecified_source_months`。居月餘下界一，原文未明寫數詞故 `source_number: null`；十餘月下界十、原數詞十。`lower_inclusive: false`，`upper` 及 `upper_inclusive` 均為 `null`。餘字與原引句必須保持，不能補精確月數、上限、出生年或公曆日數。此規則不把授任前的歲餘等待期當成持職任期。

生卒段省略人物主語時，`evidence.context` 可記 `kind: prior_paragraph_subject`、近前同篇的 `paragraph_id`、相符人物 `person_mention_id`、實際原文 `quote` 及 `intervening_paragraph_ids`。只允許緊鄰段或中間一段，須逐項列中間段落、引句涵蓋錨點及當段原事件詞；不補正文名字。這是有來源的編輯主語判讀，距離驗證不表示自動語義辨認，仍須核讀中間敘事。

明示兄弟承爵可在 `inheritance` 加 `predecessor_relation: brother`；省略時仍為 `father`。前任本人、前任及根爵名、同段相符 brother 陳述和原繼位詞都必須存在；不因同國繼位自動補兄弟，不推同父同母或長幼絕對排行。兄弟稱「弟」等原詞由親屬及承爵 source_term 保留，前任連結不等於父系家族 ID。

死後授號亦可保存先死後賜的來源句：posthumous_basis 增列 death_term 及 grant_term，死亡原詞須在完整 source_term 中位於「賜夫人為」與所授稱號之前，起點證據一致。此規則記錄明示句序與編輯判讀，不由某人死亡自動推定所有稱號為追贈；不補來源未見的「追尊」二字。

先死後授號的 grant_term 亦支援「號為」與所授稱號，例如《伯夷列傳》西伯卒後號為文王；死亡與授號原詞須依來源句序保存，不能補來源沒有的諡字。

個人報齡可存餘歲界限與來源傳聞：value及birth_year空，下界不含、上界未知；source_number支援百位，source_term保留餘歲。report_group_id分組，source_qualification、reporting_status、qualified_source_term保存蓋或或言及完整限定語，不當確定壽命。

同組個人報齡須同人物、篇及來源段落；alternative_report須與qualified_report同組。此為來源報說的分組，不合成確知壽命，來源歧說各存。

### 埋葬個人事件

`person_event_assertion_set` 可保存 `burial`，與死亡事件分開。必須原文明示：`source_term` 含葬且完整見於事件證據引句，人物錨點與篇、來源引用沿用個人事件驗證。未知日期不補數值，未記葬地不補地址。逐人 JSON 從 `person_events` 讀取；死亡及葬期不得互相推定。

### 來源相對年齡差

`annotation.age_difference_assertions` 與個人報齡分存。`person_id`、`reference_person_id` 是兩個不同人物；`comparison: younger_than`、`value` 保存原文「少某人若干歲／歳」的差值，`source_number`、`source_term` 保留原字。每筆證據同段含 `person_mention_id` 與 `reference_person_mention_id`，兩人物及原詞必須在引句內。單位為 `source_age_years`，計歲方式保持 `unspecified_source_age`，生年與日期未知，不由參考人物年譜推生年。逐人JSON從雙方皆可讀 `age_difference_assertions`，仍保留來源與篇段；不是本人的年齡。


`reported_duration.approximation` 保存相鄰年數的來源約數，例如「相秦六七年」。`value: null`、`unit: title_year`、`counting: unspecified_source_years`，原數詞為 `source_number: 六七`，約數結構為 `{"kind":"adjacent_year_numbers","numbers":[6,7]}`。兩數是原詞的數字化表示，不是精確值、可選的已確定年數或嚴格上下界；不可同時設 `bounds`，亦不可讀成六十七年。原詞、來源引句及持有人錨點均須保留。首批只支援一至九中遞增相鄰的兩個數詞，其他約數形式須另行擴充。來源敘事時點的持職年數不等於完整任期總長，不推起訖日期。


地址關係 `polity_lineage_affiliation` 保存篇首等來源明記的政體宗族地望，例如「衛之諸庶孽公子」。首批 `qualifiers.affiliation_kind: royal_lineage`，人物 ID 是來源所指公族成員，地名保存原政體名。此類不是出生地、居地或本人籍貫，不據姓氏補具名父母、遠祖或世代；原詞須含政體與公子、公孫或宗室的明示身份。

### 跨段地址主語與未明姻親／官職

地址證據另可使用 `context.kind: prior_paragraph_subject`；人物前錨的 `paragraph_id`、`person_mention_id`、精確 `quote` 及 `intervening_paragraph_ids` 必須保存。中間段清單須按同篇原序完整列出，不得跳段、倒序或借用當地君主錨點。原有 `previous_paragraph_subject` 仍只接受緊鄰前段。驗證證明來源錨點和順序一致，敘事主語是否延續仍是必須說明理由的代理判讀，不由最近人名或段距自動決定。人物 JSON 附全部中間段供複核。

`affinity_unspecified` 保存「婚」所表述的未明姻親，`qualifiers.relationship_basis: marriage_affinity`，`source_term` 保留原句。`spouse_person_ids`、`connecting_person_ids`、`generation_difference` 均為 `null`；不得補女兒、妻子、具體親等或方向，也不得把兩個姻親當作夫妻。

未名官職事件存於 `person_event_assertion_set`：`office_non_reinstatement` 保存「不復官」，`office_restoration` 保存「復就故官」。兩者的 `office_title`、`title_holding_id` 均為 `null`，原句與人物錨點必須可回查。不復任不等於明示免官；未名故官不牽連既有具名官爵時段。


### 授予政體、未赴任與來源地稱

稱號 `granting_polity` 保存 `source_name`、`authority_person_id` 及授予者的來源錨點／引句；`place_id`、`modern_identification` 均為 `null`。相同「上卿」由秦、齊分別授予時分存，不能按同名官爵合為同一次授任。`service_realization` 的首批形式為 `status: not_taken_up`、`source_term` 與 `evidence`，用於「甘茂不往」；保留授予，卻不得顯示為已赴任。未知後續不由此補定終點。

地址 `source_locality_designation` 保存「下蔡史舉先生」等以地名稱人的原詞，`qualifiers.designation_kind: geographical_person_reference`、`origin_or_residence: null`；不將未明的地稱改為籍貫、出生地或居所。`service_location` 保存「下蔡之監門」，`qualifiers.source_position` 保留「監門」，任事地與居所分開。

兄弟／姐妹陳述的 `qualifiers.shared_mother` 必須為布林值且附同母或異母原詞。`false` 不補姓名未知的另一位母親。`kinship_unspecified` 的「外族」保留原詞、未定親屬線與世代，不自行改為表兄弟或舅甥。

來源年齡的 `report_repetition_of` 指向同篇較早、同人同數值的報齡記錄，用以標示敘事與人物自述的重複，不當獨立證據或兩次不同年齡。不推計歲方式或生年。

人物事件 `diplomatic_service` 保存出使任事與 `polity_source_name`；「事燕三年」的 `reported_duration` 為數值3、`unit: service_year`、`source_number: 三`、`source_term: 事燕三年`、`counting: unspecified_source_years`、`status: source_attested`，證據與事件一致。此年數不屬剛成君爵位任期，不推曆日或起訖年。

兄弟／姐妹陳述的 `qualifiers.shared_father` 可為原文明示同父的 `true`、異父的 `false` 或未知的 `null`。布林值須有相符同父／異父原詞與來源引句，不補具名父親；缺欄與 `null` 均不表示同父。異父兄弟姊妹不得僅因兄弟陳述接到同一父系，來源原詞、母系及未明家系仍保留。

## 來源明記的任用次數

`reported_appointment_count` 與任期長度分開：`value` 為正整數、`unit: appointment`、`source_number` 為來源數詞、`source_term` 為「數詞＋為＋本筆稱號」、`status: source_attested`，`evidence` 保存持有人所在篇段的原引句。例如荀卿「三為祭酒」保存數值 3；不表示任職三年，也不生成三段虛構任期。這是來源報告的合計次數，各次起訖與間隔未定；使用端不可把同一合計紀錄當成三個已知日期的授任事件。其他數詞或句式須先擴充驗證及測試。

## 離相與復位的來源次數

`reported_office_event_counts` 用 `departure` 與 `reinstatement` 分存「三去相，三復位」兩類次數。每筆含正整數 `value`、`unit: office_event`、原數詞 `source_number`、原詞 `source_term`、`status: source_attested` 與持有人篇段 `evidence`。離相不表示自願辭職；復位不等於全部任用次數，不據此推初任或逐次任期。當前支援數詞＋去相／復位，其他句式須擴充驗證。聚合次數不作已定日期的個別事件，亦不是持職年數。

## 同一生卒事件的紀年取捨

`life_event_date_decision_set` 保存已判同指人物的同一類生卒事件所記不同年份。`person_ids` 與 `candidate_event_ids` 明列範圍，各事件的原句、人物錨點及 `normalized_date` 不改寫。`preferred_event_id` 在 `editorial_provisional` 時須為其中一項；`unresolved` 時為 null。證據完整保留候選事件的來源證據，署名、理由、人工覆核及模型狀態另存。取捨只適用此事件，不成為全域作品權威排序，也不把同一作品多篇記載當獨立見證投票。

逐人來源包在選用暫同指後匯出 `life_event_date_decisions` 與 `selected_life_event_dates`，後者附 `selection_decision_id`。原 `life_events` 及 `date_normalizations` 保留所有來源；未解決定不產生選定日期，未整理的其他事件不據此猜值。使用端以決定的候選事件 ID 範圍套用預設，撤回決定即可恢復並存。本輪為平原君卒年試點，未聲稱已處理全部紀年衝突。
# 食邑與居留年數

地址陳述的 `relation: fief` 保存食邑來源，不改作籍貫或出生地。`qualifiers.fief_kind` 分為 `tangmu_estate`（原詞須含湯沐邑）及 `maintenance_allocation`（原詞須含奉）。〈魏公子列傳〉鄗湯沐邑與信陵供奉各自保留，未獻的五城不作授邑，食邑記錄不自動新增官爵或其有效時段。

`relation: residence` 的 `reported_duration` 保存來源居留時長：`value` 為數字、`source_number` 為原數詞、`source_term` 為精確原詞，`unit: residence_year`、`counting: unspecified_source_years`、`status: source_attested`，`evidence` 與本地址陳述一致。公子留趙十年記數值10，不當官爵任期，不指定含首尾年或反推精確起訖、曆日。

平行事件換年時，事件與西元對照可能分屬兩個見證。`normalized_date.basis.reference_url` 連事件引句，選填 `reference_year_url` 連數位西元年引句；未填時兩者沿用同一 URL。兩項引句都須出現在各自的 `references` 中，不得為格式便利把引句歸到其他來源。

地望 `relation: fief` 的 `qualifiers.fief_kind` 另支援 `territorial_grant`（保存賜地原詞）與 `approved_enfeoffment`（保存請封及明示許之）。單獨請封不能當准封，地望記錄不自動生成官爵、出生地或葬地；賜地、獻回與就封的時間分別核讀。

食邑的 `qualifiers.fief_kind: household_revenue` 保存「食河南洛陽十萬戶」等食地名與戶數原語。`relation` 為 `fief`，不是籍貫、居住地或人口；本批戶數保留原詞，不推戶均人口或現代邊界。驗證要求完整食地名戶數句式，不能只憑一般食字生成地望。

`adoptive_mother` 主體為子女、客體為原文明示的所母；保留含「所母」的 `qualifiers.source_term` 及逐字引文。這是非生母的來源關係，不推血親或現代法律收養程序，不參與生母欄位及血緣世代推導。

## 著作提及

`kind: work` 表示確定為作品的名稱；保存原提及ID、Unicode位置、原稱、`person_id: null` 及已登記的 `work_id`，XML 對應 `<title ref="…">`。不得以作品名開人物卡，也不能把確定書名假作未定人物。既有誤標轉類時保留原錨點並移除人物別名／證據中的該次引用；其他同字人物提及不變。

僅在來源被提到的作品以 `status: referenced_only`、空 `books` 及 `reference_attestations` 登記。證據含來源、篇、段、書名錨點及完整原文；不表示收錄全文、作者已核定或傳本篇次已校勘。閱讀器以書名呈現，沒有AI辨識或不明確人物卡。

## 每人 JSON 的姓名組件

`person_source_bundle.name_components` 匯出已記錄的 `surname`、`ming`、`additional_names` 及身份辨認用 `title`，直接供家譜程式解析。每項保留原句、篇、段、判讀狀態與未經人工審閱標記，並附 `work_id`、`book_id`、`chapter_id`、`source_id`。其引文及人物須確實出現在所指段落，該段也收進 `passages`；沒有姓名組件時省略此欄，不從名字字數自行拆姓。

姓名組件可另存 `zi`（字），須由本筆原句或明列來源引文中的「字某」支持；不可從顯示名稱推拆，未知本名仍為 `ming: null`，不能把同一個字值冒作名。`additional_names` 可列「字某」供既有閱讀器呈現，結構化 `zi` 供家譜程式直接讀取。例如安國少季據《漢書》師古注「姓安國字少季」，存複姓安國、字少季、名未知；古注與傳世正文分源。


頂部 `title` 只供身份辨認，不代表全部敘事時點都持該稱號。各次授爵、持職與用稱時段仍以 `title_holdings` 為準；多項姓名判讀並存，不能把編者拆分當原文明示或已經人工核定。

`jurisdictions` 亦可用於 `kind: royal_rank`、原稱 `王` 的所王地，例如「更王膠東」。原稱保留王，清單保存膠東及未知今地；驗證須有「王」接原地名的原句，不能從同段任意地名補王國。人物卡及人物頁另示所王地，分組時保留不同範圍，與官職所屬地分開標示。

## 未實行的稱號提議

`annotation.title_proposals` 保存「欲立甲為太子……即止」等未實行提議，與 `holdings` 分開。欄位包括穩定 `id`、受議人物 `person_id`、原稱 `title`、`outcome: not_enacted`、職稱錨點 `role_mention_id`、受議人物錨點 `person_mention_id`、精確 `evidence`、判讀說明及代理署名。不得據此生成年份、已持有稱號或任期。

擬授職稱使用既有非人物錨點格式 `kind: unresolved`、`person_id: null`、`status: unresolved`，保留原錨點與範圍；此類型兼容既有職稱／非人物錨點，不表示尚未判斷提議是否實行。明確的角色及結果由 `title_proposals` 記錄。驗證要求引句同時涵蓋受議人物與職稱，人物錨點須指受議者，職稱不得當成現任者的姓名或異名。

逐人 JSON 另匯出 `title_proposals`；閱讀器在完整人物頁分列「擬議而未授的稱號」，不加入實授稱號或精簡卡片。沒有此資料就不顯示此欄。試點為〈張丞相列傳〉如意擬立太子而止。

## 生卒的跨西元年範圍與直接概數報齡

生卒或人物事件可用 `normalized_date_range` 保存既有相鄰兩年格式，與 `normalized_date` 互斥。十月歲首、月份不明時，年表數位西元欄只是紀年的對照標籤，不自動等於事件的唯一西元年。範圍保留兩端的數字、天文年編號、精度、原句及年欄／數位對照／歲首規則的分層參考；未知曆日不補。

逐人 JSON 將這些範圍另匯為 `date_range_normalizations`，不混入單一年份的 `date_normalizations`。閱讀器生卒列顯示兩年範圍與原紀年，完整頁可展開依據；不選其中一端或由年齡反推出生年。

個人概數如「百有餘歲」可用 `reporting_status: direct_report`、`value: null` 及 `bounds: {lower: 100, lower_inclusive: false, upper: null, upper_inclusive: null}`。`source_number: 百`、`source_term: 百有餘歲` 原字分存，`source_qualification: null` 不補傳聞限定詞，亦不作確切一百歲、上界或已知計歲方式。既有帶蓋／或言的報齡仍另保留限定狀態。

未決身份可保存一個已知候選及未知敘者的可能：`unknown_identity_possible: true` 時仍須至少一個有篇文證據的 `candidate_person_ids`，另以非空且不重複的 `unresolved_mention_ids` 指向所列段落內 `kind: unresolved`、`person_id: null` 的既有錨點。不能用未知可能旗標保留確定人物連結。〈張丞相列傳〉篇末太史公署稱依《索隱》的後人敘論說解除與前段敘者的直接同指，古注說法另存版本固定的 `references`；不因此補出作者姓名或改寫傳世正文。

直接概數報齡亦可保留 `年六十餘` 型原詞：`source_number` 為六十，`source_term` 不補歲字，界限僅記大於六十、上界未知。自報年齡仍是來源主張，不當確切享年，不逆推出生年；各項須有原句與人物錨點。

人物包的 `date_range_normalizations` 同時匯出明示官爵端點範圍：`date_role: title_period`、`record_id`、`endpoint`、`title` 指回原持職記錄。此類不加生卒事件類型，不能當死亡日期；原 `title_holdings` 端點與證據繼續保留。

未決案件可選填布林值 `candidate_list_exhaustive`。`false` 明示已列者不是窮盡名單，即使候選數後來縮為一個，也不得自動當作唯一身份；省略不保證已窮盡。來源局部候選不是額外已證人物，已知可能者與原文證據仍分存，不由候選連結推親屬或日期。

親屬陳述的證據可為 `kind: table_cell`，此時所屬篇使用既有表見證的 `chapter_id`，並記 `work_id`、`book_id`、`source_id`、`source_revision`、`table_id`、`table_cell_id`、完整原格 `quote`，以及該格的 `subject_mention_id`、`object_mention_id`。兩端須為同格逐人錨點，關係原詞須見於原格；不得填 `paragraph_id` 冒作正文或用繼位推父子。表文仍以既有表格檔為單一編輯來源。人物包只在引用表格親屬時附 `table_passages` 與表見證來源；正文 `passages` 不加入虛構段落。家族追溯使用同一可解析關係，引用連回表格原格。

新作品可先錄明示範圍的部分傳文，`source.text_scope: partial_chapter`、`source.extent` 與進度須明示未錄部分；保留古代卷篇ID，不以現代網頁小標另造古篇。未核完整卷目時可令 `expected_books: null`，不得混用篇數與版本卷數冒稱完成。跨作品引文如附 `work_id`、`book_id`，須與實際段落來源相符；表格同指補證亦按該作品目錄核對，不限定《史記》或以同卷號配對。

首選校讀可對應人物稱號錨點。持職仍保存來源字面 `title`；若同一用稱錨點有明示 `preferred_reading` 決定，人物包另附 `preferred_title_readings`，以 `holding_id`、`decision_id`、`source_mention_id` 連起 `source_title` 與 `preferred_title`，並保留暫定狀態及理由。此為編輯選讀，不改寫來源正文或冒稱影像校勘，使用端以ID關聯套用，不需NLU。

### 嗣位省稱與前任爵位連結

當來源只寫「子亭嗣」而未重寫爵名時，父子陳述的 `qualifiers.succession` 保存 `source_term`、`predecessor_person_id`、`predecessor_holding_id`、`status: contextual_provisional`、`rationale` 與 `human_reviewed: false`。前任須與本項明示父親相同，持職記錄須為爵位或王號，不能是官職或死後諡名；同段精確引文須包含父親錨點及嗣詞內的子名錨點。不是所有父子都自動繼承爵位。

此結構不捏造本人曾被原文稱作某爵的 `attestation`，也不儲存推得的祖先清單、爵名副本或起訖日期。使用端按明示持職ID讀取前任原爵與適用的校讀，呈現為承前爵稱的暫定判讀；未能取得前任資料時省略推得欄位。父親有多項爵位時，須逐案說明選定哪一項，不套用全部官爵。辨認用姓名組件中的爵稱仍須另列出處與推定說明，不代表任何時點都持爵。

人物頁的生卒摘要僅合併原紀年字串相同、正規化日期或年範圍事實相同且取捨層級相同的欄位，並保留全部來源引文。未知日期、不同原紀年、不同日期精度及有別的暫定優先層級不合併。原 `life_events` 記錄不改寫，不把來源數當成獨立史實票數。


承爵 `qualifiers.succession` 可沿已驗證的父子斷言跨相鄰兩段讀取：斷言原有 `context.kind: adjacent_paragraphs` 及按原序列出的兩個 `paragraph_ids` 必須明示，前段引句涵蓋前任人物錨點、後段承爵原詞涵蓋子嗣錨點，兩段須同篇且在實際段落次序上直接相鄰。不能由數字段號推相鄰、跳過插入段、跨篇套主語，亦不能只見嗣字而推父子。前任爵位連結仍須屬來源所述父親的爵稱，未知承爵日期不補造。

稱號來源時長界限亦支援 `unit: title_year` 的十餘年、十餘歲、十餘歳，原數詞十存為數字下界10且不含，上限未知；`value: null` 不當精確任期。月份原詞月餘與居月餘均以下界一且不含保存，`source_number: null` 表原文未寫數詞。年、月單位與原字必須相符；不得用授任前等待時長代替持職任期。

生卒原段未載紀年時，`normalized_date_range.parallel_event` 可保存與單年平行事件相同的事件對讀欄位：`kind: parallel_event`、`source_event_quote`、`reference_url`、`reference_event_quote`、`reference_year_quote`，年表網址不同時另列 `reference_year_url`。此時來源 `date_expression: null` 保持，範圍 `basis: regnal_year_crosses_ce_year` 不變，原死亡詞、平行死亡引句、原紀年、數位對照及曆法引文分列。驗證須對應各引文與網址，不得僅憑背景年或空白原日期加入數字；不把平行來源原紀年塞進本文。

來源報齡未滿可用 `reporting_status: upper_bound_report`、`value: null`、`bounds: {lower: null, lower_inclusive: null, upper: 20, upper_inclusive: false}` 保存年未滿二十。原數詞與原詞俱存，`source_qualification: null`，不補確切十九歲、生年或享年；其餘年齡證據、計歲未知及人物錨點檢查不變。

師承使用 `predicate: teacher`，方向為學生至老師；`relationship_basis: teaching`，保存學教受傳、師或弟子原詞及同引句兩方人物錨點 `subject_person_mention_id`、`object_person_mention_id`。師承不是親屬，不參與父祖、生母、配偶或子女推導；學習時長不是官爵任期。

姓名組件亦可用 `kind: table_cell`，保存 `table_id`、`table_cell_id`、`person_mention_id`、`work_id`、`book_id`、`chapter_id`、`source_id`、`source_revision` 與完整 `quote`，不偽造 `paragraph_id`。姓與名拼合須等於同人原名錨點字串，未知姓留空；稱號仍是辨認用稱，不自動成為任職始年。表格姓名來源在人物來源包的 `table_passages` 中回查，人物頁連到原格。

來源報齡亦可附 `normalized_date_range`：格式與生卒跨年範圍相同，保留本筆 `evidence`、`original_quote`、原紀年表述及原年欄／數位對照／曆法來源。不得同時附確定單年 `normalized_date`，不得由報齡推定出生年。

稱號的跨年範圍可用 `parallel_event` 對讀固定年表事件，另存 `table_event`，含完整格文、同人逐人錨點、work/book/chapter/source與固定修訂。王爵授封／即位保留明示初王的規則；官職授任及封侯須有 `title_source_term` 明記為某官／封某侯，不把原有官名、追述或他人授任當本人的始期。端點種類須與本文一致。嗣侯須有同列國名格 `noble_name_cell_id` 與侯某元年；失侯須有同人及國除／失侯原詞。只有明示失爵可補該爵終期，不能由死亡補全部官爵終期。本文未明記端點日期時，`date_expression` 保持null，不能將較前父卒年沿用作兒嗣年。

按年排列的表沿用同列 `regnal_year_cell_id`、`digital_year_cell_id`。按年號分欄的表用 `time_axis: columns`、`era_column_id`、`source_year_term` 保留本格原欄題與年字；另列 `year_mapping`（`kind: table_year_row`），保存紀年對照表的完整來源識別、固定修訂、`era_anchor_cell_id`、原年與數位西元格。對照年號及原年字必須一致，不能將侯某元年的爵年當朝廷元年、只憑同一數字跨年號取值，或把另一列西元數字搬來。西元值與時代依數位欄的已標記年資料核對，不當古籍原文。

`references` 分列事件、原年、原年號欄題、數位對照與歲首曆法。兩表的固定URL、格ID、欄ID及引句分別核對；帶 `table_column_id` 的引文須恰為該原欄題，不造段落。人物來源包補齊稱號紀年所引的原格與各表來源，另以 `table_column_references` 保留原欄物件、位置及來源；這些只是引用證據，不新增人物提及、不影響提及次數或來源頻率。

## 跨書與範圍生卒紀年取捨

`life_event_date_decision_set.work_ids` 在跨書時明列全部證據著作，須含主 `work_id`，並恰好涵蓋各候選的原篇著作。未填沿用單書範圍，不能讓來源自行冒填另一著作。

候選可為原有單一年或已通過驗證的相鄰兩年 `normalized_date_range`；允許範圍相交但端點不同，不因相交抹掉原紀年差異。明示日期及完整平行事件對讀範圍均支援。`selected_life_event_dates` 保存整個首選範圍的 `earliest`、`latest`、精度、來源與決定 ID，不額填單一 `year`。未解仍不產生首選。

決定的選填 `references` 分存古注或研究的標題、HTTP(S)網址、原引句、適用範圍與書影核驗狀態；不得混入候選主證據。原候選事件及本文不改寫，取捨只限該人該次生卒。人物卡標示首選、來源異說或未定，完整頁另列引用依據。

人物來源包與閱讀器人物 JSON 可含 `identity_distinctions`，逐項保留相關的 `person_distinction_set` 判斷、不同人物ID、理由與逐段引文。來源包補齊各引文的作品／卷篇／來源ID，含其他端點標籤及證據段落，但不把其他端點的名字加入本人的提及、別名或家族。無區分記錄時省略此欄；完整人物頁顯示同名異人、另一人物入口及原文依據。


## 明示職終、用稱範圍與原年列綁定

官職持有記錄可用 `end_basis.kind: died_in_named_office` 保存「竟以某官終」這類明指終於此職的原詞。`source_term`、同人逐人錨點與完整 `evidence` 必須與 `effective_period.end` 的 `explicit_end` 一致；官名要匹配持職、人物須在該職終語之前且無別人插入。這不是一般死亡可結束全部官爵的規則，不適用只有卒字或未明其職的材料。

`attestations[].normalized_date_range` 與單年 `normalized_date` 互斥，保存原 `date_expression`、持職原句與證據、兩端數字及三種分層來源。用稱的日期只表該處用稱，不使 `mode: attestation` 變成授任，也不改未知職期。人物包以 `date_role: title_attestation`、`record_id` 指持職記錄、`attestation_id` 指用稱，另存 `title`、`usage`，不加職期 `endpoint`。來源報齡範圍以 `date_role: age_attestation` 匯出，不能當出生年或死亡年。

明載紀年而只借表換算時，可附 `normalized_date_range.regnal_year_table`：`kind: table_year_row`、著作／卷／篇／來源ID及固定修訂、`table_id`、`era_name`、`year_source_term`、`era_anchor_cell_id`、`regnal_year_cell_id`、`digital_year_cell_id` 與 `calendar_rule`。原年號與原年字須匹配本筆 `date_expression`，對照列不能跨另一年號，數位年格須與該列的年資料一致；這些年格不被說成人物事件格。

目前曆制綁定限於已核讀的漢代案例：`han_tenth_month_before_taichu` 用於太初以前、數位年標前104年之前的建亥歲首，數位年標為相鄰範圍較晚端；`han_first_month_after_taichu` 用於太初以後、數位年標前104年之後的正月歲首，數位年標為較早端。太初改曆當年不以此兩種簡式自動換算。兩種都須有相符曆制引文；不推精確公曆日，也不是各時代通用的固定加減法。對照原年字、年號起點、數位格與固定網址分列於 `references`。

人物包補齊這些用稱、生卒及報齡範圍所引的年格與表來源，不新增人物提及或獨立史實證據票數，最多提及來源的計數仍只採實際人物標記。

## 年表原生稱號與分欄紀年

`table_title_holding_assertion_set` 保存直接出自原表的持職／封爵主張，試點檔案為 `020-table-title-events.json`。`chapter_id` 沿用該表已有的來源篇ID，不偽造正文段落。首封試點只處理 `noble_rank`、`grant`，以同列封國、功臣事由、持有人錨點及先前年欄空白核查；嗣侯、失侯與改曆過渡年另待擴充。

持有項保留一般 `title`、`effective_period`，另有 `source_representation: table_cells`。`table_title_basis` 分列 `event`、`noble_name`、`merit` 及 `year_mapping`；各格保存全文、穩定格ID、固定來源修訂與人物錨點。`attestations.kind: table_title` 的 `source_parts` 分存封國字與侯字原格位置，不假稱兩字本來連寫，也不把前置官稱納入姓名。

`date_expression_kind: table_columns_composed` 明示 `date_expression` 由原年號欄題與事件格日期合讀，`date_parts` 保存欄ID、原詞、原格與字元位置。數字紀年的 `original_quote` 仍是完整事件格，不把拼合字串塞回原文。固定原年列與數位西元格分引；漢太初前十月歲首下，已明正月至九月可存該數位年所對照的同一西元年，僅以年為數字精度，不冒作已換算公曆月日。未明閏幾月保跨年範圍。太初元年改曆過渡不套本試點規則。

匯出仍使用 `title_holdings`，另帶所有被引原格、年號欄與來源。紀年格不計作人物提及；人物卡可同時顯示西元年與原表紀年，來源連結返回原格。本傳段首戰役紀年不自動成為段末授爵之年。

姓名組件可另存 `component_alternatives`，每項含 `components`（姓、名、字的獨立值）、`source_terms`、固定來源 `reference`、`status: source_claim_not_selected` 與取捨理由。原注短引須可由保留的排版原句得到，名／字組件原詞與值逐項核查。首選組件與其他來源主張分存，不將兩種分類當作兩個人物或生前更名。試點為顏師古以少季為字、《索隱》以少季為名；原始正文及兩注字句不變。

## 同篇君主錨點限定的紀年帝號對照

`regnal_year_table.era_name` 保存表內帝號；選填 `source_era_name` 保存本文原紀年稱謂，二者不同時須有 `reign_designation`。其 `kind: same_reign_source_designations`、`source_era_name`、`table_era_name`、`person_id`、`person_mention_id`、`source_context_quote`、`status: editorial_provisional`、`rationale` 與 `human_reviewed: false` 綁定同篇已辨人物錨點及限定語境。原 `date_expression` 不改寫成表內稱號。驗證器目前只接受〈南越列傳〉高帝已定天下下的漢／高皇帝，以及孝文帝／孝文兩組明列語境；不作全書通用別名或任意年號替換。

原段未含年號的稱號用稱，可依既有 `normalized_date.basis.kind: parallel_event` 分列本段原事件、平行事件及其原紀年，再附固定數位對照與曆法引用。原 `date_expression: null` 保持。授任起點只有來源已明示授任者才可依同一事件定年；同次用兵的既任官爵只增加用稱日期，不產生持有始期或未知終期。

## 只有原表明名的人物

人物可直接據原表逐人錨點登記，不必偽造正文段落。登記採 `evidence_scope: corpus_and_native_table_mentions`，其 `evidence` 的表格項保存 `kind: table_cell`、表與原格ID、固定著作／卷／篇及來源修訂、`mention_id`、原名 `quote` 與全格 `source_quote`；該人物全部正文及原表提及須與登記證據雙向齊備。未宣告此範圍的既有登記仍以正文提及驗證。別名不得借別人的表格錨點。

原格明列姓名前的王侯稱號可存 `table_title_basis.kind: inline_title_attestation`；用稱只記 `mode: attestation`，起訖未知，不由「來降」變授封。每個稱號分存其同格字元位置與同人名字錨點，不能跨另一人物或敘事句子拼接；原表的編者數位年份不能藉此直接填入任期。原有分欄首封模型保持各自驗證。

## 原表同列分格父子

`relationship_layout: first_holder_with_parent_label` 限明示父子。`table_cell_id`／`quote` 指父系欄原格，`subject_table_cell_id`／`subject_quote` 分別指同列首位持有人姓名原格及其全文，兩端各有 `object_mention_id`／`subject_mention_id`。必須同表同列固定來源，父系欄精確為該人物錨點加「子。」，姓名格為首位同人侯元年，較前持有人欄不得有文字，同格亦不得已有前任侯元年。不能從承爵順序、孫字或別列借父系。 另接受父系欄精確作「以X子侯。」且X有從第一字以後開始的逐人錨點；這仍限同列首封者，不能泛化為以X孫侯、以X弟侯或任意授侯事由。

據原表配置的 `family_path` 另須有相符 `source_assertion_id`、相同父子端點、原格證據與一代距離；缺少任何一項即拒絕。人物匯出及介面保留兩格原文、位置與返回連結，不將分格拼句當原文。

古注連寫 `X姓Y名也` 時，姓名組件異說可分存來源原詞 `X姓`、`Y名也`，但兩者須在同一固定原引文中連成該明示句式；不得從不同句子或不同人物拼姓與名。原始跨行小注與移除已聲明排版記號的短引文同存。所取組件與未取異說各有來源，不把讀法分歧改成正文異名或按字數拆姓。

## 來源帝號的雙人物錨點

`reign_designation.kind: same_person_source_and_table_designations` 只為本次紀年判讀。來源內 `person_mention_id` 與原表紀年起點格的 `table_person_mention_id` 必須連到相同人物，原表錨點精確覆蓋帝號且其後為元年；來源限定引文須包含原日期與該人物稱呼，並在事件原文及同段證據內。`source_era_name` 與 `table_era_name` 分存，不能由此建立全書通用文字別名，亦不能把帝號的回溯紀年當稱帝事件。

`regnal_year_table.season_source_term: 冬` 保留只明冬季的來源日期；它與年號、原年詞組合後須精確對應本筆 `date_expression`。太初前未明月的冬季仍保相鄰公元年，不把秋季誤放成同一跨年模型；有據的秋季數值紀年依原年列與曆法參照另存，原秋字不得刪去。

原表首封日期可只存年詞（例如欄題元封、格內元年），仍以 `table_columns_composed` 與兩份原位置保存，不能補出月日。太初以前未明月時使用既有相鄰兩年範圍；有月份、干支者則完整保留。首封功臣事由可保留以「侯，萬戶」結尾的戶數原句，不能由此推居處、人口或生物子女數。

## 原表死亡與改曆過渡年

`table_person_life_event_assertion_set` 保存原表明記的死亡；本模型要求同格逐人錨點、「名死」原詞、同句前綴紀年、固定修訂及完整原格，拒絕無後／國除推死亡、未死／當死／死罪、借他人或後任紀年。生卒集及人物匯出均使用原表證據，不建立虛擬正文段落。

`normalized_date_range.basis: calendar_reform_transition_year` 目前僅處理太初元年。其 `calendar_reform` 保存十五個月過渡年、復原表天文年、首末月原符號、儒略曆及事件月未知；公元前105至103年屬暫定整年範圍。須有固定《漢書》歲首原文、固定復原表首末月與符號說明、原年表太初元年欄與數位104參照。這不放寬一般相鄰兩年模型，也不表示確切死亡年份。事件 `study_references` 保留現代研究的書目、連結、已閱範圍及未驗證意見狀態。

原表首封日期若只有月份而沒有干支，`date_parts` 精確保存原月詞，日部分省略；不得為適配格式補日。年精度的公元換算仍由原欄題、原年列及歲首來源判定。

原表死亡格在日期前有計數、人物前有侯字時，`date_layout` 可記 `kind: after_cell_count_and_title`、`cell_count_source_term`（如二。）、`title_source_term: 侯`。格首至姓名的原文須精確等於計數、日期、逗號與侯字，不可借其他人物紀年；計數只是原詞，不在此推算任期。直接以紀年起句的舊模型保持原限制。

地址 `capital_location` 表示所都之地，與個人 `residence`、籍貫分存；`source_term` 精確保存「都」加原地名，`qualifiers.seat_kind: royal_capital`、`source_action: 都`。不由建都推個人出生、居留年月或死亡地，不補現代轄區。

稱號提議另容 `proposal_kind: agreed_appointment`、`outcome: not_reported`，保存任官約定而不聲稱已授或未實行。`agreement_anchor` 與 `role_anchor` 為同段原字元錨點，前者須保存約詞，後者須指原職稱；`person_mention_id` 連到約定對象，`source_term` 精確記「使某人為職」。引句須同時涵蓋前置約詞、對象與職稱。不把此記錄列入已持有稱號，已有 `not_enacted` 記錄仍須維持其原本的未實行判讀。

所報異文可附 `reported_relationship` 保存未採納的古注親屬主張；目前弟說限定 `predicate: brother`、同輩數值0、主體為弟而客體為兄，並須保存 `commentary_claim_not_adopted`、原數位注語詞頭及弟字所指對象。它不加入實際親屬陳述或家族邊；原文與古注的不同說法不靠改寫源字解決。異文的 `study_references` 僅列後出考證書目，未知出版年不補，閱讀範圍及未獨立驗證狀態分記。


姓名組件可附明示的 `zi` 與 `former_ming`。`zi` 須有字某的引文；初版 `former_ming` 僅接受同一引句同時有名之曰某、以及更名為目前 `ming` 的明示敘述，不由一般別名猜初名、不補改名年。`additional_names` 仍保存原名字串，閱讀器只按這些有據欄位加字或初名標籤。古注的名／字異說使用既有 `component_alternatives`，不覆寫預設，附固定提交、原引文、範圍指紋及未採納狀態。

## 人物、泛稱與神話角色的指稱異說

`annotation.referent_interpretations` 用於同一原稱的古注解釋不全是人物身份的情形。例如陽子有伯樂與仙人陽陵子等說，鄭女曼姬亦有群體泛稱與個別典故的不同解法。案件連到本篇未連人物的 `target_mention_ids`，`source_terms` 逐一保存原稱，`evidence` 保存 work／book／chapter／source、原段及確切引句。

各 `alternatives` 有署名、`referent_kind`、可能為空的 `candidate_person_ids`、解釋與 `source_reference_ids`。人物、傳說人物、身份未定人物、群體泛稱、多個典故、神祇、自然現象與神話生靈分存；不為配合人物模型而補造 ID。古注 `references` 固定提交、blob、實讀行範圍、回應快取雜湊與未核書影狀態。未決案件為 `unresolved`，`default_alternative_id: null`，不自動選唯一候選。非個人指稱可用 `editorial_provisional` 暫採神祇、自然現象、神話生靈或群體讀法：指定 `default_alternative_id`，以 `selection` 保留理由與該說的來源 ID，所選讀法不得帶人物候選。個人身份仍須另有身份判斷及正文標記，不能藉此欄位逕行採納。`witness_wording` 分存本篇與平行見證的確切片語、參考 ID 及 `adopted_as_text_correction: false`，不改寫正文。

候選人物 JSON 可附此項判讀及原段，供查閱候選依據；不將候選提及加入已採納 `mentions`、出現次數、`person_ids`、世系或生平。閱讀器在正文段落之外顯示「編者指稱判讀」，完整人物頁另顯示候選來源；姓名卡的簡要生平不混入異說。此欄位與 `unresolved_identity_cases` 分開，後者處理已具人物候選的身份待辨，不能迫使泛稱或神祇讀法只剩人物候選。

神話生靈讀法用 `referent_kind: mythical_creature`，例如《漢書》顏師古解長離為靈鳥；與《集解》陸離神名讀法分存，不據此改寫本篇原字。此類讀法的 `candidate_person_ids` 必為空，不憑生靈稱呼建立人類世系。

## 已辨明的非人物用字

既有誤標可保留提及ID、位置與原字，改為 `kind: non_person`、`person_id: null`、`status: contextual_provisional`。`lexical_role` 目前支援 `verb` 與 `reciprocal_adverb`；`basis_quote` 須包含該次錨點及實際原文語境，另有判讀理由、代理署名及 `human_reviewed: false`。它與仍待辨識的人物分開，不能暗連人物或作品。XML 使用 `<seg type="non-person" subtype="…">`；閱讀器保留原錨點、原字及判讀說明，不畫人名底線或開人物卡。首例為〈淮南衡山列傳〉王濟北、王江北的王與數使使相交的相，不能按王、相單字全域套用。

## 相鄰數詞的群體約數報齡

`age_assertions[].approximation` 可保存 `kind: adjacent_age_numbers` 與整數原數詞 `numbers: [7, 8]`。原 `source_number: 七八`、`source_term: 皆七八歲` 保留，`value: null`、`reporting_status: approximate_report`，不能同時設 `bounds` 或由此推出生年、確歲或計歲制度。編者判讀另列 `approximation_interpretation`。首例為本篇完整具名四子：`group_reference` 明列原群體詞、名單、成員ID、原人數詞與 `declared_member_count`，須與同段逐人錨點全部相合；不能暗補第五人或把不完全名單當全部。報齡可保存有據的原紀年與公元年，其日期不當出生日期。重述報齡亦須與原筆約數一致。

## 未分拆的姓名全稱

姓名組件可用 `full_name` 保存有來源的完整讀法，並明留 `surname: null`、`ming: null`，不按字數拆姓與名。`full_name_basis` 保存收到原稱、`kind: received_parallel_spelling`、理由及未經人工審閱狀態，須有固定原文短引支持整體讀法，且收到原稱確實是本人物在引用段落中的錨點。原字與提及ID不變，舊讀法留 `additional_names`。人物卡以整體名稱顯示，其他有據組件與原稱依舊可查。首例為收到本文救赫、平行《史記集解》《漢書》作枚赫；沒有據此斷言姓枚名赫。

## 徙王與新舊王號的時段

`mode: transfer` 與起點 `event_type: transfer` 明示徙封，`transfer_basis` 指同人的 `previous_holding_id`、原詞、`title_source_term`、原王號人物錨點及原文證據。前王號須以同一事件和日期記 `explicit_end`，不能由死亡或別人的繼位補終點，也不能把追諡當作在位王號轉封。首版核驗徙為某王，以及徙某王王某地兩種實際句式。後者保存原字王與既有 `jurisdictions`，不在正文虛構重排的國名王錨點；王字在文法上是動詞，仍可作本次王國授任的原詞，與人物錨點分類分層。

原年格附記其他事件時，`regnal_year_table.regnal_year_span` 可用明示位置引用格首年數，後必接原句號；整格仍完整引用，不能借附記事件的月日。首例格首四、後接四月己巳立太子；徙王只知景四年，故存兩年範圍。太初前十月歲首的來源亦可用固定《曆書》本文以十月、故襲秦正朔的相連說明，與古注建亥讀法分源，不要求只能引用某一注本。


### 缺位與所求身分的非人物用語

既有 `kind: non_person` 可用 `lexical_role: vacant_office` 保存明說無太子的太子，用 `sovereign_status` 保存刻天子璽、求即天子位中的天子。這些是逐處判讀的來源用語，不建立缺位人物、假定在位者或已授官事件；原詞、上下文、提及ID及編者理由保留。驗證須限定相應原句與字元範圍，人物／作品ID留空。原有動詞與交互副詞分類不變。具體謀議中事大將軍、刺殺大將軍青所指的人物，另按明名與同一敘事鏈記身份判斷，不因同一段有偽印清單而混為一類。


### 官職句讀與代理歸屬

`punctuation_attribution` 分存收到標點所成片段、首選分讀、同段首選與另一讀法的人物錨點、固定平行原文及編者理由。首例依《漢書》同次奏議及《史記集解》未句讀文字，暫取馮敬行御史大夫事；不改收到的典客臣馮敬、行御史大夫事宗正臣逸。此筆官職仍為 `mode: attestation`、`appointment_role: acting`，未知起訖不補，宋祁注語所記任官年不當正文日期。人物頁展示代理標籤與分讀證據；代理與未分代理性的同名持職不在畫面上合併。原宗正逸記錄不因此刪除，也不把句讀差異誤記為兩書所記史事矛盾。


### 復故王地與稱號紀年來源首選

徙王可以返回先前王地，而來源省略新王號。`resumption_basis` 連到此前同人的 `earlier_holding_id`，保存目前原稱、`return_source_term`、未經人工審閱的編者理由。首例「徙淮南王喜復故城陽」：稱號用原王字，王地另存城陽；原王字屬 `context_role: pre_transfer_rank`，不虛構城陽王連續字串。前段城陽王、徙淮南王地、復故城陽為三段持爵，兩次轉封前後共享事件及日期；原有循環、同人與不借死亡補終期的檢查仍適用。

`chronology_source_choice` 明列首選篇、日期原詞、另篇原記與同人原文，以及固定平行見證及理由。喜的本筆按118篇帝年暫存時段；52篇喜王年八／四及漢書38十二／五分列，不冒稱已消除差異。月份未知的轉封不借同段其他受封者月日。本筆未知初授與末終留空，不由父親死年、諡號或續計王年補全。人物頁展示暫取來源及另篇原句，引用顯示可去數位排版標記，原排版另存。

### 原表的始封者世代欄

`relationship_layout: founder_generation_column` 用於保留原表「號謚姓名／子／孫／曾孫／玄孫」欄式。兩端必須是同一原列的始封者格與實際具名後裔格，兩格全文、固定 work／book／chapter／source／revision 及逐人錨點均須保存。`generation_source_term` 必須等於原欄題；`generation_distance` 分別為 1、2、3、4，對應 `father`、`grandfather`、`great_grandfather`、`ancestor`。陳述的限定詞、家族路徑與原格世代距離必須一致。

子、孫等欄的首位具名「侯／矦某嗣」可作本欄後裔，不將同格後世或另一人套入欄題；位於前面的帝王紀年錨點不算前任嗣侯。玄孫另須本格祖名及玄孫原詞，不從相鄰欄推中間三代。空的曾孫欄題不建立人物。既有 `first_holder_with_parent_label` 的直接父子驗證保持原規則。

其他著作的原表由原生表格索引供應，閱讀目錄的 `available: table` 指向 `table_id`，不建立虛構段落檔。`text_scope: partial_table` 與 `scope_note` 明列實錄範圍。人物提及與人物頁來源返回連結保留明確 work／book／chapter／table／cell，不能只憑卷號推著作；沒有來源西元紀年的世系表不補造年列。

### 身份已暫定、爵年仍有衝突

身份判讀可附 `chronology_caution`：`kind: unresolved_title_chronology`、`status: unresolved`、`identity_basis: explicit_commentary`、`no_tenure_interpolation: true`。本事須有固定篇文全文、日期及事件原詞、同人提及錨點；`table_accounts` 逐項保存至少兩個不重複原格的完整文字、固定來源、同人錨點與封免原詞。它通知一般程式不可把此身份判讀當作已證明事件當時在爵，既不生成持職時段，也不消去不同來源紀年。原表疑字保持原字，引用注家明名不等於年表任期已獲調和；人工審閱仍為 `false`。

這類判讀的 Kanripo 注說可另存 `quote_format: kanripo_line_wrapped` 與 `display_quote`。原 `quote` 不改；顯示字串只可去除頁標、分行斜線、`¶` 與空白，須與原字逐字相符且引用固定提交。一般引文及未標格式的斜線不得套用此清理，顯示端遇不相符字串回退原文。人物卡僅在已記錄的未定警示存在時顯示爵年提示，不從文字臆測新增警示。

### 固定版本古注節錄

`text_layer: witness_duyu_annotation_excerpt` 表示節錄杜預注原句；`witness_received_text_and_duyu_annotation_excerpt` 表示原文與所附杜注同錄，保留「注」標記。這兩層必須有 `source_excerpt.kind: fixed_git_literal_span`，保存固定提交、blob、全文SHA-256、原行號、原行全文、Unicode code point的 `start`／`end`，以及連續的署注上下行與原年次題頭。節錄文字須逐字等於原行的該字元範圍，作品／卷篇另有實際登記。

來源 `text_scope: partial_chapter` 及 `extent` 明示只錄古注片段，不冒作全年、整卷或全書正文；此型目前未核影像，人工審閱為false。原年次題頭用於定位，不自動轉作人物出生年或父子關係始年。署名、數位轉錄與是否親見影像分開記錄。

來源父系與編輯首選仍各存一層。例如《史記》成公少子說保留為原陳述，杜注子國說有獨立來源陳述；`family_tree_decision_set` 選擇預設父邊，不改寫受傳字句，也不把被排除來源的「少子」套到首選父親家中的排行。

### 人物公開 JSON 的逐項來源範圍

`data/corpus/profiles/` 的正文 `occurrences` 一律保存實際來源段落的 `work_id`、`book_id`、`chapter_id`、`source_id`，包括《史記》。另列全部 `paragraph_ids`、`mention_ids`，`count` 等於該篇提及錨點數。既有 `number`、`category`、首段 `paragraph_id` 及短引 `quote` 仍供閱讀器呈現；它們不能代替完整引用範圍，也不能用卷號推算著作或篇 ID。

`table_occurrences` 一律附原表的作品、卷篇、見證 ID 及 `source_revision`，包含《史記》原表；`table_id`、`cell_id`、原格 `quote` 與逐人 `mention` 保持可回查。人物資料匯出遇未登記於閱讀目錄的提及篇須失敗，不默默略去該來源。

## 帝紀在位語境的冊后關係

`context.kind: regnal_empress_context` 僅用於帝紀明書冊立皇后的配偶關係。兩條完整證據分別連到即位者與皇后，並保存 `monarch_mention_id`、`empress_mention_id`、即位及冊后原詞、原段順序與固定數位見證。`witness_interval` 保存兩段及省略部分的全部原行、提交、blob、行號、原文字串與指紋，古注及頁標與正文分層；它不是兩段原文相鄰的宣稱。首例《昭帝紀》為第21至69行。

驗證核對原詞內的兩端人物、已登記選錄與區間對應、行號及版本，並拒絕在位區間內另見即位、崩等更替用語。這是附證的編者判讀，不是自動判定歷史真相；狀態保持 `contextual_provisional`、`human_reviewed: false`，不補婚日、子女或生母。其他親屬不能套用此模型。已知原行有省略的選錄，也不能只把種類改成 `adjacent_paragraphs` 來略過此證據。

### 連續具名祖先的中間父子推導

`parent_connection.type: parent_between_consecutive_ancestors` 是編輯組裝，不能另造一條 `source_attested` 的父子陳述。它引用同一已錄正文段落、同一後裔人物的兩項父系祖先陳述；`father`、`grandfather`、`great_grandfather` 所示距離必須恰差一代。`chain_subject_person_id` 指共同後裔，`nearer_ancestor_assertion_id` 與 `farther_ancestor_assertion_id` 指較近與較遠祖先的來源斷言；本組裝人物須是較近祖先，組裝父親須是較遠祖先。不得跨缺代、混用母系、跨不同來源段落或默蓋明載另一父親。

兩份 `references` 各明指斷言 ID，保存同段完整引文、work／book／chapter／source／paragraph ID、固定來源 URL 與限定範圍。段落須有共同後裔及兩位祖先的逐人錨點。`status: contextual_provisional`、`human_reviewed: false`、具體 `rationale` 必備，組裝節點的 `source_assertion_id` 留空。人物頁據此追父祖及反向列子女，標為推導；不儲存手工三代名單。

《晉書》荀勖選段明記父肸、祖棐、曾祖爽。本次將肸—棐與棐—爽作此種推導，三項原始世次陳述各自保留；不是把原文改寫為兩句父子記載。

### 明載年號的中國曆年度換算

除原有年表試點外，`normalized_date.calendar: chinese_civil` 可明示原紀年對應的中國曆年度；`year`、`era_year` 是年度標號，不是精確公曆日期。當前新增的 `regnal_year_mapping.kind: ce_regnal_era_span` 限於正公元年的年號起迄對照，保存 `era_name`、`source_number`、`regnal_year`、`start_ce_year`、`end_ce_year` 及 `reference_index`。原紀年必須見於 `source_expression` 與原文引句，年序及換算結果須落在所引起迄範圍。 原文年號字形與對照表不同時，`regnal_year_mapping.source_era_name` 可分存原字形；目前僅明確容許正文「昇平」對照表「升平」，不改正文或偽造對照表引句。原文紀年以 `source_era_name` 組成，表格名稱仍以 `era_name` 核對；其他字形差異須另核並增補規則。

引用的現代對照須標 `scope: modern_era_year_equivalence_only`，保留其 `columns.era_name`、`first_year`、`last_year`、URL及實際閱覽日；不能把對照表的數字冒作古代正文。`status: editorial_provisional`、原句、事件證據、換算理由與未人工審閱狀態仍必備。未明示 `calendar` 的舊數字或跨年範圍，不因此自動改標中國曆年。

本批荀淑卒年以原文建和三年，配教育部年號表建和元年147、末年149，暫存149。未換算日月，不由六十七歲倒推生日。原有前公元紀年與跨公曆年範圍的處理不由此正公元年模式取代。

### 未採入家族的遠祖聲稱

來源確有「某十一世孫」而未採用其遠祖系時，仍可保存 `ancestor` 陳述，以 `qualifiers.adopted_for_family_tree: false` 明示。`source_number`及`reported_generation_number`保存原世孫數；`generation_distance: null`不把來源世次直接當已採納的精確父系距離。原詞、逐人錨點及引文照存，人物JSON可讀此來源聲稱；家族路徑、組裝與閱讀器追祖均不得採用這筆未採聲稱。家族根仍依可接合的近支資料決定，不補遠祖間的缺名人物。

### 年號內未定年與爵號改封（荀氏跨史試點）

`normalized_date_range.basis: within_named_era` 專記「咸熙中」等年號內未定年。`calendar: chinese_civil`、`precision: year_range`；`earliest`／`latest` 是該年號中國曆年度的外界，沒有單一 `year`，也不表示整段任期。`era_span_mapping` 保存政體、年號、年號起迄數字及對照來源索引；來源須分列政體與年號，以免把西晉泰始與劉宋泰始混用。現先接受「年號＋中」，不將「中」硬分成中央一年或中間三分之一。這與原有中國曆歲首跨公曆年的兩年投影是不同類型。

爵位 `mode: transfer` 可使用 `transfer_basis.kind: noble_rank_change`，保存「改封」原詞、持有人錨點、起點引文、判讀及前爵狀態。前爵可確定時，以 `previous_holding_id` 接同人的實際爵位；前爵明示終點與新爵始點須同證、同日期。前爵未確定時為 `null` 且 `previous_title_status: not_identified`，不得借父親諡號補成所承前爵。「荀崧改封曲陵公」與「改封愷南頓子」各自存證，不強迫兩者同樣具備已名的前爵。王號徙封仍用既有規則。

明記「追贈＋稱號」可作 `posthumous_grant`；其 `posthumous_basis` 須保存相符原詞及同一授予起點證據。不是以死後出現一次稱呼推定曾有追贈。

`clan_style` 用於本名未知的氏稱顯示，不能濫用未分姓名 `full_name`。`ming` 保持null，`value`須為已記姓加氏。`received_clan_appellation` 要求原文人物錨點直接作該氏稱；`sibling_clan_appellation` 為代理依具名兄弟之妹暫稱，須引用同段的姊妹陳述ID及原詞，且不得有已知異父限定。兩者保存判讀、狀態及未人工審閱標記。鍾氏字琰的琰在 `zi`，不填入 `ming`；荀霬妻暫稱司馬氏，不補本名或子女生母關係。

## 完整傳文的子嗣承接與省略主語

`context.kind: biographical_child_continuation` 用於原段連續敘傳主、卒官、再以段首「子某」附載子嗣。只接受父親斷言；`paragraph_ids` 與全部證據段完全一致、依正文順序連續，各證據引用完整原段，原行與固定修訂也須連續。`parent_mention_id` 位於首段，`child_mention_id` 位於末段「子」後；另列暫定狀態、判讀理由及非人工審閱。不得跳過中間段、截句掩去主語轉換、跨版本或向正文添父名。這是可覆核的閱讀判斷，不是驗證器自動理解古文。

報齡原段省略姓名時，可在證據用 `prior_paragraph_subject`，保留前段原引句、人物錨點及全部中間段（最多一段）；有原行位置的選錄不得跳行冒作連續。來源報齡與出生年仍分開。

稱號用稱的姓名省略時，`attestations.context` 可用 `previous_paragraph_subject`，同時必須與該持職本段來源證據的承接完全一致。用稱字元位置仍在實際官稱所在段，人物錨點另指直接前段；不得把前段姓名偽作官稱本段原字。

`agnatic_cousin` 的 `qualifiers.mourning_separation` 保存「絕服五世」之類的服制原數：`value`、`source_number`、`source_term`、`unit: reported_mourning_generations`、`common_ancestor_distance: null`。不能以服制世數填共同祖先親等。

未名妻由「妻弟謝晦」辨氏時，姓名資料可用 `clan_style.kind: wife_sibling_clan_appellation`。須有本段具名妻弟錨點、相符的姊弟斷言與原詞，並保持 `ming: null`；不據此新增孩子的生母關係。

`end_basis.kind: died_in_last_named_office` 限定原文在該官名後直接接「。某年，卒官」；完整原詞、同一持職證據、人物主語錨點及官名字元位置須相合。僅此最後明示官職可有 `explicit_end`，日期另附原紀年及換算證據；其他先前官職不得一併取此卒年為終點。

來源只有「吉之後」之類泛稱而未採為父系時，另用 `qualifiers.ancestry_precision: unspecified_descent`，`source_number`、`reported_generation_number`及`generation_distance`均明列null，`adopted_for_family_tree: false`。原詞「某之後」須逐字連到客體人物錨點及引句；不能由未知變成任意世數，也不生成缺代路徑。原有明載十一世孫等數字的未採主張，仍必須保留其原數。

`stepmother` 可保存原文「後母」或「繼母」，兩者均須有相符引句。繼母角色不轉成生母；同一人物在另一子女傳中明載為母時，各條關係分開保存。

`source.normalization.omitted_digital_paratext` 分存固定數位見證中的節題與相鄰空行：`kind: digital_section_heading`、`not_received_text: true`、`source_lines`、`source_revision`、`raw_quote`、`raw_quote_sha256`。只容許維基式節題與空行，雜湊及行數須相符，不能與已錄正文原行重疊。`biographical_child_continuation` 可跨這些逐行完整記錄的數位節題，不能跨未記錄文字或拿節題本身證父子。正文段落的原行界線及實際文字不改。

`parent_connection.type: parent_through_paternal_uncle` 是可撤回的父系組裝，須同時引用具名侄的父親、同段叔父及叔父父親三項正文斷言。`nephew_person_id`、`uncle_person_id` 與三個 `*_assertion_id` 必須和各節點的已選直接父系吻合，三份補證逐項連回原文；四個人物身份不可重疊，不能默蓋另一個明載父親。組裝邊的 `source_assertion_id` 保持 null，不能另外創造明載父子的假斷言。此處不以數位「安兄據子朗」標題證謝據為謝裒子。

`maternal_uncle` 除原有「姊子」格式，也可由明示「舅某」保存甥舅：同一證據有 `subject_person_mention_id`、`object_person_mention_id`，前者指甥、後者指接在舅字後的具名人物，`source_term` 為舅加原稱。未名舅以原字「舅」作人物錨點、`source_term: 舅`、`object_name_status: not_recorded`；不補姓名。兩種格式均保留 `lineage: maternal`、`generation_difference: -1`、`mother_person_id: null`，不能把兩代不同舅父或外祖父混為同人。

反向原句「綏，玄之外甥」亦可保存同一方向的 `maternal_uncle`，主體為綏、客體為玄。`source_term` 保留客體原稱加「之外甥」，兩端錨點須相鄰（可隔原逗號或頓號），並逐字綁定完整「之外甥」與句界；不將泛稱「甥」或同段任意兩人自動轉成母舅。母系世代與未名母親欄位要求不變。

`maternal_cousin` 目前保存明示「姨弟」：`kinship_structure.lineage: maternal`、`generation_difference: 0`、`collateral: true`、`maternal_path: mother_sister_son`、`subject_relative_age: younger`。原路徑與長幼分存，未名母親及共同祖先不填身份，`distance`、`common_ancestor_person_id` 保持null；不能誤作父系從弟或接進共同父系。證據含主客體人物雙錨點，原詞須緊接客體原稱；相對排行使用 `scope: maternal_cousins`，不推絕對排行。

姓名組件的 `zi_basis.kind: biographical_subject_called_by_courtesy_name` 保存傳首明言「故稱字」的情形。`subject_anchor` 指傳首姓加字，`marker_anchor` 指同段「故稱字」，兩者均保留段落ID及Unicode位置；附 `status: source_attested`、`human_reviewed: false`、理由，不將字冒作名。直接「字某」仍依原格式。平行正文補定本名的參考用 `scope: primary_parallel_explicit_given_name_and_same_named_ancestors`，保存完整姓加名、以此首名後接字的 `raw_context_quote` 及其雜湊、原行字元位置、固定修訂與全文雜湊；所選名必須逐字相符，不從「同諱」截出一個字，也不能用數位章題冒作正文。未親核圖像須保留false。

先敘死亡、後明言「贈某官」可存 `posthumous_basis.kind: death_then_explicit_gift`，不替正文補追字。保存完整同段 `source_term`、`death_term`、`grant_term`、`recipient_person_mention_id` 及與持職起點相同的 `evidence`。受贈者須為死亡原詞前最後具名人物，授贈在死亡後、每筆官稱屬明贈清單且與同人職稱錨點相合；未知年份不補。此型與僅死後被用稱不同，不把全人生官職一律視為追贈。

`title_proposals` 另容 `proposal_kind: unassumed_appointment`、`outcome: not_assumed`，區分「任用而未受／未赴」與原有 `not_enacted` 的未實行立號提議。`appointment_anchor`、`non_assumption_anchor` 分別保存任用詞與「並不行」「苦讓，遂不受」「以疾固辭，未行而卒」等已核原詞；職稱仍是非人物錨點，當事人、任用詞、職稱及未任原詞都須在同一完整引句中。`non_assumption_kind: declined` 或 `did_not_take_up` 分存辭讓與未赴，不能由此推為已任職期。人物頁以「辭讓／未赴任記錄」另列；同名來源用稱僅提示另見未赴任記載，不將一次未赴擴成此人所有任期的判斷。


## 父系晚一代旁親

`agnatic_senior_kin` 以晚輩為 `subject_person_id`、長一代旁親為 `object_person_id`，例如劉傭指向劉隗。`kinship_structure.generation_difference: -1` 表示主體比對象晚一代，`lineage: paternal`、`collateral: true`；`distance` 與 `common_ancestor_person_id` 留 `null`，`subject_relative_age: unknown`。晚輩不必年齡較小；`從子` 不等於兒子，也不單獨證明其父或共同祖先。用雙人物錨點及本段「隗舉其從子傭」核定說話／敘事主體，這項關係不直接組裝父子。

母舅的人名之前可以夾地望，例如 `舅濮陽吳氏`。`intervening_place_name: 濮陽` 必須逐字綁定舅字與同一人名之間的片段，不能跨過另一人物提及；原母名仍空，不自行接舅之女為表親。

## 來源所列姊妹群的排行

`qualifiers.source_sibling_group` 記錄 `id`、`count_scope: reported_sisters`、原字 `source_number`、數值 `reported_count`、`member_person_ids` 及各人的 `member_roles`。群組原詞有 `source_anchor`；每位成員有同段人物錨點、`source_term`、`ordinal`、`position` 與判讀狀態。它是該段所列的姊妹群，不宣稱父母一生全部子女數。

`relative_birth_order.ordinal_scope: reported_sibling_group` 與 `group_id` 指明序號屬哪個來源群。鄭阿春段的 `后最長` 存第1，`第三者` 存第3；`中者` 不直接存第2，`小者` 只作語境最幼、序號留空，不直接存第4。來源人數與序號約束可以交由處理演算法求解，不能把求解結果冒作原文明載。姊妹的同父接合另用可撤回的編輯推導，不把本群排行混成獨立父子原句。

## 未採遠祖的報稱世數

遠祖報稱若作「自某八世，生某」，`ancestor` 陳述可用 `ancestry_precision: reported_generation_formula`、`source_number: 八`、`reported_generation_number: 8` 保存原數；`generation_distance: null`、`adopted_for_family_tree: false` 保留世數口徑未定及未採樹狀態。完整原段須綁定自字後祖先與生字後後裔的實際人物錨點。這與同段明言「鈞生量、量生儁、儁生防」的逐代父子分開，不補中間七代，也不按同姓接上古族源。

## 撫養與宗祀承繼

`raised_by` 的主體是被撫養者，客體是撫養人；`care_basis` 區分 `explicit_yang`（養之）、`speaker_recalls_rearing`（本人詔語追述撫育）及 `welcomed_like_children`（迎與共居、恩同其子）。須保存完整原段、雙人錨點、`source_term`；詔語另綁 `speaker_identity_mention_id`，不能將前後不同皇帝混為同一個「朕」。

`ritual_successor_of` 的主體是承繼者，客體是所繼者，分存 `succession_kind: ji_named_relative` 或 `si_named_predecessor_hou`。`legal_adoption_status: not_stated` 表示本項沒有明言法定收養，並非斷言歷史上不存在收養；`parentage_inference: not_inferred` 不從此項產生生父、養父或祖先。撫養與宗祀都不改寫另有來源的父母，也不參與父系三代推導。

死亡事件的 `reported_reign_interval` 可記「某立，未逾年薨」：`reference_event: accession`、`upper_years: 1`、`upper_inclusive: false`、`unit: source_year`、`counting: unspecified_source_years`、`normalized_years: null`。這是承位後的來源年數上界，須綁定本人名字後的原句；不是生齡，也不能借父親卒年補此人的確切卒年。

## 來源群組的匿名氏稱

匿名姊妹的氏稱另可用 `clan_style.kind: source_sibling_group_appellation`，狀態限 `editorial_provisional`、本名保持 `null`。它須綁定該人的姊妹斷言及完整來源群，核驗群組人數、各成員錨點和排行，並從同段已具名姊妹的「某氏」或「某氏女」提及取得姓氏；不能只據四人同列、丈夫姓氏或郡望補姓。氏稱的編輯推導不等於每位姊妹都在原文明書此氏稱，也不產生新的父子斷言。

## 省略主語與固定底本空行

未受任另保留「不拜」「皆不就」「讓不拜」原詞；前二者作 `did_not_take_up`，明載讓不拜作 `declined`，不得截掉讓字改列原因未明。任用詞與拒受詞各有同段字元錨點，職稱錨點不連人物，也不列入實任持職。

未受任的 `appointment_stage` 可分為 `invitation` 與 `appointment`；既有未分類記錄可省略。明載「請為／請爲」須標 `invitation`，不能改稱已授官；「命為／命爲」等原詞另保留任用錨點。邀請與任用後「並不就」均不列實任，所有當事人與職稱位置檢查照常執行。省稱「庶子」保留實際徵召原詞，前奏文「太子庶子」留在同段引文及判讀說明，不把建議本身當授官。

省略受任者時，`evidence.context` 可引用相鄰前段具名主語，保存段落、人物錨點及引文。若固定底本只隔空行，`source.normalization.verified_blank_line_gaps` 保存 `source_lines`、`raw_quote`、`raw_quote_sha256`、`revision_id`，核對空行數、空白字元、雜湊及修訂。這是核讀固定原文後錄入的證據，不能代替未讀正文，也不能跨過標題、古注或其他非空文字。持職見證用 `previous_paragraph_subject`；未受任證據用 `prior_paragraph_subject` 並列中間段落。

完整官名中的「太子」可用 `kind: non_person`、`lexical_role: office_title_component`，以 `basis_quote` 綁定已核官名及同一起點，例如「太子太傅」。不能據官名片段推定某位皇太子的人物提及；既有錨點及原字保留。


### 傳主承接的死後贈號

`posthumous_basis.kind: biography_topic_death_then_gift` 用於同一原段中編者已辨定傳主，但贈號前穿插他人的敘事。須明存 `topic_person_mention_id`、`recipient_person_mention_id`、`death_event_id`、完整 `source_term`、精確 `death_term`、`grant_term` 與共用來源證據。傳主、受贈人及死亡事件必須同人，死亡事件亦須連同一原段；不能因最近出現另一位君主或妃而改換受贈人。

`grant_recipient_kind` 分為 `topic_continuation`（如「贈車騎大將軍，加侍中」）、`named_recipient`（如「贈裒太保」）及 `deictic_recipient`（如「其贈豫章郡君」）。這是有明示錨點的編輯判讀，不是把每段第一個人自動當作全文主語；驗證要求段首傳主錨點與已錄死亡事件相合，各贈號均落在其精確贈句內。所引「建武元年薨」證明死亡，不直接證明後來穆帝更贈之年。每次贈號另立記錄，未知起年保留空值。原有 `death_then_explicit_gift` 的近接主語規則維持不變。


### 更封目的地省略爵字

`transfer_basis.kind: elided_rank_regrant` 保存「更封裒琅邪」等沒有重寫王字的原句。新記錄以 `title: 王`、`jurisdictions[].source_name: 琅邪` 分存爵與封地；`actor_mention_id` 指更封句受封人，`rank_mention_id` 指同人的實存爵字原稱，`realm_source_start`／`realm_source_end` 指目的地的實際字位。不能在正文或用稱錨點補造「琅邪王」。若爵字取自「琅邪孝王裒」等敘事原稱，王字用稱標為 `retrospective`、不附授號年，孝字不併入生前授號。

這一類更封必須連同人的前爵 `previous_holding_id`，前爵明示終點與新爵起點共用原文證據及同一日期精度；未知日期維持未知。「徙封宣城郡公」則可使用既有 `noble_rank_change`，前爵未辨明時 `previous_holding_id: null`、`previous_title_status: not_identified`。不能借用叔父爵位填補空白。


### 人物頁子女次序

閱讀器由實際載入的父母、子女 JSON 套用長幼約束，不從家族 ID 字母取排行。`relative_birth_order` 只在 `scope: siblings`、`operator: lt` 且兩端確在子女列表時加入先後約束；絕對排行僅比較同父母、同 `sons_of_parent`／`daughters_of_parent`／`children_of_parent` 範圍的數字。未記性別或排行者不因鄰人的長子記錄而補數字。

完整的小型 `source_sibling_group` 可結合明載排行、最長／最幼及相對次序計算必然的顯示先後，例如四姊妹中的一、三及最幼。推導只影響顯示，不寫回來源排行。缺員、重複身份或互異群體報告不作完整槽位推導。相互矛盾的有向約束折為衝突組，保留組內輸入次序與所有人物，於 `child_order_conflicts` 回傳成員，其他可確定的先後仍有效。無約束的平手沿用輸入次序。

「年出十歲」等直接報齡用 `reporting_status: direct_report`、`value: null` 及 `bounds` 保存嚴格開放下界：`lower: 10`、`lower_inclusive: false`，上界兩欄為空值。`source_term` 必須逐字為「年出」加原數詞及歲／歳，不能把「未出」反作下界；不補確切年齡、出生年或敘事年月。引語發言人與報齡對象仍依人物錨點分開。

`age_context.kind: during_life` 標明生前報齡；`at_death` 另以 `life_event_id` 連到同人、同來源段及同原句的死亡事件。不可只因同一人物就把生前二十歲接到七十三歲卒年；舊記錄沒有此欄時仍是未分類報齡，不自動當享年。數值、計歲法、原句及出生年限制不變。

「某官。卒官」未載紀年時，`died_in_last_named_office` 亦可保留該最後明示官職的 `explicit_end`，`date_expression` 為空；原詞須精確相合，不把不載年份誤成可補卒年，更不能套到其他官爵。「徙某官，未之職」及「召為某官……不就」分錄未受任，保留原任用詞與未受詞，不能作實任。

官職 `mode: transfer` 使用 `office_transfer_basis.kind: explicit_office_transfer`，保存任用動詞、原序官職列表、逐字原詞及同一筆證據；「遷甲、乙」可分錄兩職，但兩筆均引用原完整列舉，不拼造「遷乙」。它與王爵 `transfer_basis` 徙封分開驗證，亦不由轉任補前官終期或曆年。

身後明贈官號可按原文「贈甲、乙，加丙」逐項保存；保留完整並列贈授句、同段死亡詞與受贈人物標記。特進等榮號列 `honorific`，不得因此將未受任或生前見稱改為贈官，亦不據死亡自動補授贈年份。

省略主語的「即以某官為贈」以 `continued_subject_death_then_gift` 連結同人同段死亡事件及緊接前段人物標記；須保留兩段引文、原死亡紀年與完整贈官句。不得將前段別人的死亡、較遠段落主語或生前未拜的其他並列官號套入贈授。

「年垂五十」等傳文報齡沿用 `approximation.kind: approaching_age`、數值 `target` 及 `approximate_report`，確歲與生年留空，不改為嚴格上下界。`subject_scope.kind: named_subject_in_biography` 連到本段具名人物，須與報齡前最近具名人物一致，完整原段與本人錨點同存；不可把祖先報齡移給傳主，也不可套入奏表自報。

原紀年前明記朝代（如「宋元嘉十三年」）時，`regnal_year_mapping.source_polity_prefix` 保存宋，`era_name` 仍為元嘉，`source_expression` 保留完整朝代加紀年；前綴須與現代對照表的 dynasty 欄一致，不能靜默刪去宋或把宋充作年號的一部分。

暫定身份判斷可用 `alternatives` 保存仍未排除的其他人物，每項明記不同的 `person_id`、`status: not_preferred_but_not_excluded` 與理由。主項 `person_id` 是首選，狀態維持 `contextual_provisional`、`human_reviewed: false`；候選不是同指合併。主項與候選各自的人物來源包均收錄該判斷及原段，但不把候選當確定提及、親屬或身份別名。

`maternal_role` 保存原文母親稱謂，方向為子女至被稱母者。`role: mother_unspecified` 保留「母某」；`role: prior_mother` 保留「前母」。兩者均須具同段雙人物錨點，`biological_mother: null`、`father_person_id: null`，不列入生母或自動生成配偶／父系。前母不可直接改作後母、繼母或生母；原文追贈提議是否採納另記。

`context.kind: biographical_children_list` 保存完整傳主單元末的「有幾子：甲、乙。」明列名單。`father` 仍為子女至父親，原詞保留於 `qualifiers.source_term`、父系 `lineage: paternal`。名單順序只對照來源字位，不自動生成出生排行；另有長子、第幾子等明文應另記。

`paragraph_ids` 依完整原序列出從正文開首具名傳主至名單的所有段；`evidence` 一段一個完整引文。`parent_mention_id` 必須是首段字位零的傳主，`child_mention_id` 是名單中的本子女；`list_member_mention_ids` 依原字位完整列出所有不同子女。各段同一 `unit_id`、固定修訂、原行與傳世正文文字層必須一致。

`opening_heading_source_lines` 引用 `source.normalization.omitted_digital_paratext` 中同名數位節題的固定原行，節題緊接正文傳首。這只驗證單元邊界，父親身份仍來自正文人物錨點。中段同名人物或其他王侯不能替換傳主。

段間只能直接相鄰，或由已核純空行 `verified_blank_line_gaps`、純數位節題補足；兩者均須有原行、原字、雜湊及同一修訂號，不能將被略正文改標空行或節題。`context` 另有 `rationale`、`status: contextual_provisional`、`human_reviewed: false`。本類型不處理不完整名單、未明示人數的泛稱或跨世系推測。


### 明列子名單的完整單元證據

`context.kind: biographical_children_list` 保存完整傳主單元末的「有幾子：甲、乙。」明列名單。`father` 仍為子女至父親，原詞保留於 `qualifiers.source_term`、父系 `lineage: paternal`。名單順序只對照來源字位，不自動生成出生排行；另有長子、第幾子等明文應另記。

`paragraph_ids` 依完整原序列出從正文開首具名傳主至名單的所有段；`evidence` 一段一個完整引文。`parent_mention_id` 必須是首段字位零的傳主，`child_mention_id` 是名單中的本子女；`list_member_mention_ids` 依原字位完整列出所有不同子女。各段同一 `unit_id`、固定修訂、原行與傳世正文文字層必須一致。

`opening_heading_source_lines` 引用 `source.normalization.omitted_digital_paratext` 中同名數位節題的固定原行，節題緊接正文傳首。這只驗證單元邊界，父親身份仍來自正文人物錨點。中段同名人物或其他王侯不能替換傳主。

段間只能直接相鄰，或由已核純空行 `verified_blank_line_gaps`、純數位節題補足；兩者均須有原行、原字、雜湊及同一修訂號，不能將被略正文改標空行或節題。`context` 另有 `rationale`、`status: contextual_provisional`、`human_reviewed: false`。本類型不處理不完整名單、未明示人數的泛稱或跨世系推測。

### 具名弟子承嗣

保留現有 `adoptive_father` 謂詞及原「出繼伯父」分支，僅另增 `qualifiers.adoption_basis: named_younger_brother_son_as_heir`。這是來源所述承嗣父角色，不推現代法律資格，也不由「嗣爵」「奉祀」推父親。

新式必須同時具有：正文段首具名承嗣父；同段其「無子」與「以弟〔具名生父〕子〔具名承嗣者〕爲嗣／為嗣」完整原詞；兩端及生父各自精確人物錨點；同段既有、有據的父親陳述ID，並保留其孩子／父親錨點。source term中的生父與子名必須恰好接於「弟」「子」之後，末詞必須確為爲嗣／為嗣。數位題頭不滿足來源層要求，從弟亦不冒充弟。

兩項父親角色並存，`modern_legal_status: not_inferred`；此型別不決定人物ID應置於生父或嗣父分支。

## 年號中之後明載年序的直接相鄰段承接（庾杲之試點）

`normalized_date.regnal_year_mapping.kind: era_only_antecedent_ce_span` 保存前段「永明中」、直接後段「九年，卒」的紀年。`era_only_context` 包含前段完整`antecedent_evidence`、同傳主`subject_person_id`、兩段ID、原年號中詞與年數；不是把中換為元年。日期本身`evidence`只含實際死亡／報齡段，前段紀年證據獨立保存。

validator核同篇同source、直接相鄰段、原行只隔一空行、同固定修訂、兩段同人錨點、全文引句及後段首部明年序與卒詞，再核現代年號表數值。未知月日不補，年度是中國曆年；前段任職不自動套此年，也不以卒年終止全部官職。新模型可撤回，狀態仍editorial_provisional、human_reviewed:false。首例僅庾杲之永明九年491死亡及同段五十一報齡，不一般化其他含混年號或跳段。


## 裴松之注的固定見證文字層

`text_layer: witness_appended_pei_songzhi_note` 保存已固定數位見證中的裴注所引文字、裴案與引書，不冒作陳壽正文。`received_authority`為該選段可見的引書／作者標記，七個編輯分段不宣稱底本原有七段。來源原行、外層括號、頁標與編輯去排版步驟完整另存；引書中的再引、書信與自稱依完整敘事單元判讀，不能以段落字面最近人名自動掛號。沒有親見影像，仍image_verified:false。

### 明示主題下的死亡贈官

`posthumous_basis.kind: explicit_topic_scoped_gift` 不按最近人物推受贈者。
`topic_person_mention_id` 可在非零字位，但必須是句界後的明示主語，前面只可有已列時序詞；`topic_span`、`death_anchor`、`gift_anchor` 均保存實際字元。
同人死亡事件須已有記錄，死亡先於贈官，贈官清單必須逐字包含本稱號。
中間他人只可逐項列為 `sovereign_replies`，並須是「上／帝／天子」的孤立不許／許之答覆，不能含死亡或代換主題；未列出的其他人物使驗證失敗。
這是經編者標定的局部主語承接，並非任意略過帝王或自動將傳主套進所有贈官句。

### 傳紀年語境與事件原句分層

`calendar_context_assertion_set` 新增 `basis.kind: biographical_regnal_context`。
固定見證、原行雜湊、單元數位題頭與明示傳主錨點保存於 context；數位題頭不是正文。
`timeline.paragraph_ids` 必須完整列入該單元從開頭至本事件的所有既有段落，不得跳段、倒序或越過另一傳題。
`accession_anchor` 必須明示即位主語；獨立 `era_context` 必須以來源人物錨點指向同一君主，並包含明文年號。
即位至事件間若有相競年號即拒絕；現代年號表只供數值換算，不能代替古代來源的君主／事件判讀。
`event_binding` 綁定單一既有death或posthumous_enfeoffment記錄、人物及其實際事件詞字位。
事件 `normalized_date.evidence` 與 `original_quote` 仍只留實際事件原段，年號支持另存context，不把遠段年號拼進事件引句，也不改報齡的死亡時點或倒算生年。
所有判讀為 `editorial_provisional`，數值是中國曆年，不改為公曆月日。

### 追封與追贈分開

`mode: posthumous_enfeoffment` 與同名起點事件表示明文「追封＋原爵號」。
只限noble_rank，須有同人同段先前已記死亡、精確追封詞及爵號字位，`enfeoffment_basis` 保存death_event_id與相同授封證據。
一般封、死後一次用稱、追贈官職均不能改當追封；此類爵不得作生前轉封的前職。
未知終點仍為unknown，不因死亡自動截斷其他官職。

傳紀年另核 `subject_death_anchor` 的局部死亡主語：同段最後明示回到傳主後，其他具名者只能是上述孤立君主答覆；若事件段未具名傳主，僅接受段首原年詞後直接卒／薨的省主語形態。正文若明記另一死者，不得只憑傳題覆寫。`death_event_id` 必須綁定本死亡；追封語境必須再連至同人已驗的死亡context支持，不可援引另一人的死亡。


### 從叔無後具名為嗣，連續本傳另明出繼

`adoptive_father` 增加 `adoption_basis: named_agnatic_senior_no_heir_as_successor`，不改既有伯父或弟子為嗣分支。具名「從叔」須與「無後以〔子名〕為嗣」同段，次段須明言「年〔報齡〕歲／嵗出繼」及「所繼父於〔子名〕本緦麻」。兩段均須完整正文引文、同篇同修訂及相連原行，逐人錨點一致，不得跳過正文或跨傳主。報齡只留原詞，不倒推生年。

`biological_father_assertion_id` 必須指向首段明文生父；`biological_father_preserved: true` 保留生父，不以嗣父取代。`source_term` 和 `chuji_source_term` 保留兩項原詞；`modern_legal_status: not_inferred` 不作現代法律判定。只嗣爵、只同族、無出繼、錯名或錯版本均拒絕。本型別不產生生母、嗣母或排行。


### 明言反向從子句（局部模型擴充）

`agnatic_senior_kin` 原語義不變：主體晚一代父系旁親，`generation_difference: -1`，親等及共同祖先為 null，年齡先後未知。新增 `source_clause_binding` 的 `pattern: biographical_subject_courtesy_senior_congzi` 與 `courtesy_name_mention_id`，只認雙端人物錨點加同一主體的字號錨點，精確原句「主體字字號對象從子也」。不依同姓或同名猜身份、不補中介父親；不同代與同代不得互換。「彞于彧為從祖兄弟」仍獨立為同輩父系旁親，不能改成親兄弟。此句型不擴及族父、姑子或未知其他倒裝句。


### 固定見證同位置對應

`source_occurrence_concordance_set` 以sources/witnesses內固定UTF-8 raw檔（URL、revision、SHA256、git blob）和雙端原Unicode錨點記錄同位置重出。`resolved_person_occurrence_alias`雙端須同一現行person ID；`unresolved_text_span_correspondence`僅存未解文本位置，不當個人。兩端各自以literal witness_fragments或已存Kanripo括注正文節引投影到同一原行欄位，不准跨source／revision／位置。單一canonical與duplicate一對一、無自連、重用、鏈或循環。原段、提及、引用不改。

bundle的mention_count為獨立位置，raw_mention_count與duplicate_mention_count及occurrence_groups保存原始錨點與對應；most-mentioned依獨立數並列。source_count仍是來源記錄數，passage_count仍是註記容器數。來源頻次不是權威度。未解合稱不投入人物頻次。


### 元年承前與固定本傳嵌入引語的省年號語境

`relative_regnal_year_valid` 只在紀年解析將「元」讀為一年，不修改報齡 `source_age_number`。新增元年承前必須提供 `narrative_era_scope`，明年/其年仍分別偏移一/零年；「次年」原詞未建模型，不靜默等同明年。既有非元年分支保留。

`narrative_era_scope.kind: same_biographical_timeline_with_embedded_quotations` 保存同篇固定修訂、傳主段首錨點、完整相鄰段序及各段原文/原行位置、年號與事件日期獨立錨點、具名君主參考與受檢的君主/年號清單。引語或賦文的確切範圍另列 `embedded_quotation_scopes`；其中引古不改敘事年號。不得跳正文、改版本、取後出的年號、跨傳主或換君主；事件引文仍為原事件完整段，不把年號語境拼進原文。這是有理由且可撤回的語境判讀，不是通用自然語言斷代器；來源的引語邊界和君主指涉仍須核讀。

新資料省略年號採此較嚴格語境；年號名稱清單及公元起迄對照來自固定保存的教育部年號表，只作換年，不聲稱該現代表驗證古代事件。所有數值為中國曆年，年精度不生成月日、生日或全部任職終期。


### 原生reading_layout

version 1以primary_paragraph_ids及archival_excerpts完整、不重複分割所有paragraph IDs。原JSON paragraphs／text_sha256仍存原實體順序；不刪任何錨點。archival只允許同fixedraw完整逐字range對應，含原行／SHA／revision及concordance，不能憑文字相似封存。XML以主文後archival順序序列化原p及行內ID，reading-role/index可追溯；無layout章位元輸出不變。runtime封存區預設摺疊、舊paragraph／mention深連結先展開再定位，人物返回鏈保留原ID。


### 年號初中末與原行內主語承接（受限結構）

`relative_year_reference.kind: omitted_era_regnal_year_after_era_stage` 可讓明示「年號＋初／中／末」僅提供年號，不把初定為元年。仍須 `relative_ce_regnal_era_span`、原年序數字及現代對照。`narrative_era_scope` 保留完整固定附傳、連續段列、原字位、君主、明名傳主與嵌入引語；另列 `quotation_introducers` 精確到曰，引用末須緊接主敘事年詞。`event_binding` 綁實際record/person、同段明名主語、日期後的授/卒觸發及逐職錨點；驗證不接受任意最近人名、跳段、換題、換年號或用後出年詞回填。初中末的本身日期不會成為確年。

相鄰編輯段若同用一原行，可在 `prior_paragraph_subject.source_continuity` 明列 `kind: same_raw_line_nonoverlapping_fragments`、固定修訂、共享原行、首段無競爭人名的事件prefix與後段首個同人具名恢復。來源normalization兩完整抽取單元必須相鄰，正文全量雜湊、body字位及每個原行內片段原字位均相接且不重疊。只有相同raw行號不能證連續，也不能當作一律拒絕依據；缺字、倒序、重疊、他人或換題都拒絕。

未拜原詞 `固辭不拜` 以整詞記 `non_assumption_kind: declined`，不能截成不拜而移除辭讓。報齡原字 `數詞＋嵗` 與歲/歳並存，數值須由原數詞驗證；不藉報齡推生年或改作死亡年齡。

新原詞「固辭不拜」若隔直接對話，`refusal_subject_scope` 必須為 `same_named_speaker_after_direct_speech`，保留 `subject_mention_id`、`speech_introducer_anchor`、`speech_anchor`、`resumption_anchor` 及 `human_reviewed: false`。任職角色後的同人具名「某謂…曰」、引語及「乃固辭不拜」必須逐字相接；不接受把對話受話者當辭授者。沒有這種明確speaker/speech/resumption鏈時，只容無曰字且沒有其他具名主語介入的直接辭授。


### 共同侍從後的事件時間語與贈官

`posthumous_basis.kind: coordinated_attendance_death_then_gift` 只承載已標明「A與B、C並侍D于E。X平後卒，贈T」的受限形狀。subject_context分清傳首明名主題、恢復的A、共同參與者、所侍對象與亂事X；作亂的全名與平後的省稱須同一既有身份。角色、原句、動作、處所與標點須逐字相接；不能因最近出現X、D或C就改死亡／受贈者。本分支沒有引語scope例外，傳首至時間句若有曰或中文引號須另案，不讓引語繼承外層傳主。死亡須連既有同人原生death事件，death/grant各有精確字位與全段hash、固定修訂，贈號用稱必須恰在贈詞之後。原文全段及全部其他人物保留，不將贈改寫成追贈，不填確年或終止其他持職。

## Phase38 fixed-paragraph era-stage

`narrative_era_scope.kind: same_fixed_paragraph_era_stage` 僅為同一固定完整段、同傳主的「年號初／中／末→明數年→除官」提供年號。保留source_id、revision_id、witness_sha256、full_paragraph、source_position、傳主原mention及精確era/event/verb/title錨點；不填君主，不容任意ruler欄。必須無主語切換、插敘/引語、其他年號或介入數年；binding另驗實際record/person/title與授任起點。本分支不放寬既有跨段且須君主的timeline模型。

`within_named_era` 範圍可保存初／中／末；初、末須另有相符`source_stage`，仍只給整個年號範圍，不將初定元年或量化為前若干年。中原有資料保持可讀。所有端點、政體、參考表及原句守衛維持。


後漢書固定見證分層：`witness_appended_lixian_note`（唐李賢注）、`witness_appended_liuban_collation`（宋劉攽校）、`witness_appended_qing_siku_collation`（清四庫考證）。三層必備 `layer_attribution` 的 `attributed_author`、`period`、`received_authority`、`quotation_dependencies` 及 false 覆核資格；清層 `scope` 限 `independent_volume_appendix`，署名館臣／被引何焯分存。轉引不當獨立原著核讀；原文 p 之外標層，不改 Unicode 字位。

## Phase39 named recipient gift

`posthumous_basis.kind: named_recipient_after_same_paragraph_death` 僅支持同一完整固定原段已綁同人死亡、後「明年」及「贈＋明名受者＋官」的追贈。保存source_clause_anchor的原「其贈」，不補追字；grant_anchor完整含贈、名及官，recipient mention緊隨贈且緊接title原字。保死亡事件ID／原詞／字位、明年字位、修訂與全文SHA及全文證據；生前任職、錯死者、段首帝、泛稱或最近人名均不能替代受者。日期須通過既有relative_regnal_year模型且為同人死亡年後一年，證據相同；不改死亡或其他任期。舊biography_topic、coordinated attendance及subject continuation分支維持。

### 具名施號者追號具名死者

`mode: posthumous_naming` 可另用 `naming_basis.kind: named_recipient_after_death`，只接受同完整來源段中的 `施號者 + 追號 + 受者 + 曰 + 本筆title`。不將一般「號」、自號、名譽用稱或在世授號當死後命名，與原有諡／謚／立號曰分支分開。

此型別的 `naming_basis` 必含且僅含 `kind`、`source_term`（完整段）、`death_event_id`、`death_anchor`、`death_subject_mention_id`、`naming_anchor`、`issuer_person_mention_id`、`recipient_person_mention_id`、`evidence`。兩個anchor皆為 `{start,end,surface}`，使用Unicode code point。死亡anchor只接受卒／薨／死及前置「及」，死亡前最近的具體人物mention須是同一死者；施號者與受者須為不同person。施號者mention末端緊接追號，受者mention須恰在追號之後，隨後曰與完整title；title attestation須精確對齊，usage為posthumous_usage且person_mention_id指受者。不可以施號者官名當受號者。

`death_event_id`須指同person的已驗證death事件，且事件evidence含同完整段／同source_id；命名evidence須等於holding及起點evidence。事件的主source_term可以來自同死的另一正文證據，不強迫抹除主證或造第二次死亡；此helper不豁免現有life-event及age-context驗證。未載年日維持null，不由追號倒推出卒年。原始𤣥等字形不得改寫。

## 同一死亡事件的多來源報齡證據

`age_context.kind: at_death` 仍以 `life_event_id` 指向同人且 `source_attested` 的唯一死亡事件。每一項報齡證據的 `source_id`、`chapter_id`、`paragraph_id`、完整 `quote` 必須出現在該死亡事件的證據中；報齡證據集合非空，但死亡事件可另有未載年齡的來源附證。這只允許報齡範圍是同一死亡事件證據的非空子集，不允許跨人、跨事件或改換引句。各報齡的原數詞、人物錨點與數值仍由原生驗證器逐項核對；不從年齡倒推生年，也不拆出重複死亡事件。


## 局部死亡證據與完整敘事紀年鏈

死亡`event.evidence`可保存實際死亡與同人主語的局部原句；`normalized_date.evidence`另保存固定同篇完整敘事段序。此窄型別只支援既有`relative_ce_regnal_era_span`及`same_biographical_timeline_with_embedded_quotations`，不是任意擴大日期證據。

採用時新增`normalized_date.event_evidence_binding`，`kind: local_death_in_fixed_narrative_year_chain`。必填`life_event_id`、`person_id`、`source_term`、`source_fingerprint`（source_id/source_commit/source_blob_sha/response_sha256）、`event_evidence_index:0`、最後一段的`date_evidence_index`、`event_person_mention_id`。`death_subject_scope`另限具名死亡原詞起首主語，或同一主語「有疾…遂薨／卒／死」完整子句，防止把同段其他人物借作死者；不是只要段中出現人物便可。三個精確錨點`event_quote_anchor`、`event_term_anchor`、`event_date_expression_anchor`均含paragraph_id/start/end/surface；分別保存局部原句、死亡原詞及本事件原日期（可含季/月），不改原字。

當前首批只處理一份局部死亡證據；原同死多來源模型不變，不將其他時代或篇章硬併入本鏈。日期鏈全段逐字、順序不跳段、同固定commit與raw SHA、同事件ID及人物，並仍受既有年號／相對年／君主及引語範圍驗證。傳主可與所記死亡人物不同，但事件及日期的具名錨點必指同一人（王凌傳敘司馬懿死亡即例）。這是可追溯的編輯身份判讀，非自動NLU、人工核定或權威度提升。

未用此binding的舊模型繼續要求原有證據一致；無效binding不回退舊寬鬆路徑。此型別不自動授權跨篇或本紀年單元橋接；相關能力須另有原生模型與固定來源。

`death_subject_scope`恰含`kind`與`clause_anchor`。`named_subject_in_death_term`要求子句錨點等於死亡原詞，死者具名提及在原詞起首；`illness_clause_ending_in_death`要求子句從同人提及起首接「有疾」，以所錨定「遂薨／薨／遂卒／卒／遂死／死」結束。夢中或敘事中插入的其他人物不能取代起首患病者。


## 來源明示中國曆月的獨立構件

死亡事件`source_date_parts`可保存原文明示月份，和`normalized_date.precision:year`分開。首批只支援45型別同版本／同事件的完整敘事日期鏈，不能借別人的月、跨篇補月或由春夏秋冬推月。

欄位恰為`kind:explicit_chinese_calendar_month`、`calendar:chinese_civil`、`precision:month`、`life_event_id`、`person_id`、`month`（1–12整數）、`source_number`、`source_term`、`leap_month`、`source_anchor`、`evidence`、`status:source_attested`、`reviewer`、`human_reviewed:false`，可另有`day:null`，未知日亦可省略。沒有數字日或西曆日期換算。

`source_anchor`具paragraph_id/start/end/surface，原月詞只收明示數詞月（含正月、明示閏月）。錨點須完全位於45的本事件原日期範圍，`evidence`恰為日期鏈中完整事件段及同人mention。明文「閏八月」為month8、leap_month:true；未標閏的「八月」存month8、leap_month:null，表示只記未標，不另推曆法是否置閏。不得把明載八月寫成史實未明，也不得當公曆八月。

本型別不改年精度或人物／事件身份。JSON bundle的life_events保留整個source_date_parts供無NLU消費；既有年份date_normalizations不改定義。未帶新欄的舊事件不變，錯誤新欄必拒，不能以已存在正確年份略過月份驗證。

### 完整紀年段與殷浩來源事實的窄邊界

`age_assertions.source_term` 可用逐字 `年登`＋`source_number` 表達原報齡；僅沿既有歲數解析，`元` 仍不是報齡數字。`age_context: during_life` 不作享年或倒推出生。

`unassumed_appointment` 的 `稱疾不起` 僅適用「除甲、乙，並稱疾不起」完整連列，須有既有完整前段主語及同人後續明示承接。每職保存任用、職稱與拒任三錨點，不生成 active holding。不能泛把「不起」或其他人的疾辭套到同段所有任官。

`office_restoration` 新窄分支 `restoration_kind: posthumous_restore_unnamed_office` 綁定 `death_event_id` 與逐字「詔追復某本官」。受者必為本句具名人物，同人來源死亡須在同篇前段；`office_title`、`title_holding_id` 均為 `null`，日期未知。請求「若使…崇復本官」不符合詔准，不填全部已知舊官。

既有 `annal_ce_regnal_era_span` 新容 `annal_year_reference.format: kanripo_continuous_year`：固定 raw 起年到下年完整引文、行號、修訂、雜湊、同年全段投影及連續年號鏈均須相符；完整 section 同存原生 chapter.source.annal_year_sections，原正文仍保「五年」。原 Wiki 單行節題分支不改。年度數值屬中國曆年；attestation 的年度只放用稱，不替未知起點填授任年。

上述事實形狀由 `validate_corpus.py` 與窄 helper 驗證；通用 `records.schema.json` 未列這些事實型別，沒有移除其既有規則。

「請為某職」經完整長書後，關引號再具名同人「固辭不起」，可用 `appointment_stage: invitation`、`non_assumption_kind: declined`。須驗前段主題、請為與職稱緊接，以及拒絕前一字位恰為同一具名受邀人。不得把邀請改成除授，或套到插入書信中其他人的官稱。

### 同固定作品跨篇同一事件的年段日期／祖母原稱

`normalized_date.cross_chapter_event_binding.kind = same_event_fixed_work_annal_date`僅支援已存death或已存grant的start：必須有原record ID、同person ID、同作品同固定revision但各自raw SHA/blob、兩個原文人物mention、原事件詞與受控主語句、完整received_annal正文及其原年詞精確字位。原event／holding evidence不替換成全年；date.evidence獨立保存完整全年。死亡annal句型為具名人物緊接薨；授官為具名人物緊接為某官，原傳進拜同一官。這是可撤回編輯same-event判斷，不是NLU、名人名單或年份白名單。跨篇日期不可增加第二次死亡。`source_date_parts`仍使用中國曆月明文，day/leap不明保持null；可依該已驗binding的annal date_clause_anchor驗月詞。

`grandmother`的限定新分支以`relationship_basis=literal_grandmother_title_clause`驗「具名子孫尊祖母具名祖母」雙人物原字。保`lineage=unspecified`、`generation_difference=-2`及`parent_person_id=null`，不當外祖母，不填中介父母；原外孫分支不變。

母稱的另兩個限定分支：同一已標人物緊接「尊母具名母親」；或本傳開篇「傳主諱…中子也母具名母親」。必須保雙mention、完整原段、mother_unspecified、biological_mother=null及father_person_id=null，不將先前其他帝王錯接為孩子，也不自動加入生母或配偶。一般直接子母／封母及前母舊分支保留。報齡仍可沿既有「九嵗」原詞，完整年九嵗句在證據中，不改報齡模型。

叔父原模型另加兩個倒裝小分支：「具名叔＋具名侄＋之叔父」兩名緊接；以及具名伯父開篇字…（已標同人字及侄的官銜）具名侄伯父也。詞序按叔侄端點驗，保未名父親為null；不把伯父視為生父，不給父親排行或新中介人。原季父／叔父／兄子等分支及根端浩叔父融範圍不變。

同次授官不能僅憑同人同官：另綁原生用稱occurrence ID及該官字位、前官（勲／勳字形分存）、視事三日進拜的完整episode、其後因從遷都長安，與009次年完整年段遷都長安相對照，次年以已讀年號參考獨立驗算。原傳或年段有第二次相同進拜、原生用稱指向另一次官字位、失去這個共同事件序列都拒絕。死亡另限既有傳主病薨原詞；未／欲／疑等不當已死。明月限定完整單一「季節＋月＋官銜＋具名人物＋薨」句，不能跨另一紀年、另一人或借前句月份。

三后授號新增`posthumous_basis.named_parent_honorific.kind=retrospective_parent_empress_honorific`，保具名授予者／受者mention、母或祖母原詞、尊…曰…皇后全句及后號精確錨點。此為後出唐注所記親尊后號授予，mode=posthumous_grant、kind=honorific，未知授號年／死亡年維持null；原詞尊不補追，無新增死亡事件。不能改成在世皇后實任、太后位、任意他人或不具名授號。

父母／祖母后號的 `named_parent_honorific.primary_context` 必有同固定公開primary見證的完整單元：原raw全文與SHA、精確原行投影及單元SHA、subject/death/grant/identity逐字錨點，明示先死後尊。009單獨的尊母／祖母稱句不能證死後；缺此橋拒絕。完整橋只資格性地支持posthumous，不建立新死亡、死亡年或授號年。敬隠后／敬隱皇后保原源字形，以明示同人完整慶傳的編輯橋解釋，不改正文。所有橋AI provisional、human=false、image=false。


## 未決同人配偶指涉組

`annotation.unresolved_relation_identity_groups` 僅將同一共同配偶之多個來源人物槽分組；status=unresolved、predicate=spouse、same_person=null、distinct_people=null。候選ID與原spouse assertion端點精確聯集；每項reference有完整原段與局部span、原主張雙人錨點，不能用分組捏造婚配。原relations、mentions及ID不變；preferred_relations排除此組具名主張，另輸出完整組。traceFamily/card以同一未決組列各來源稱法，明言不判一人或多人，不建立確定配偶項目。無case之既有行為不變，其他親屬類型不適用此契約。


## 同傳主死亡後無標點贈官與年號省稱橋

`bound_death_serial_gift`只綁已驗同人死亡事件、傳主起首（可有原紀年或長子前綴）及同固定全段；贈官title_parts逐字連續分段，不改正文標點。死亡到贈之間只容明列直接承接、無他人錨點的議者評語／下詔痛惜，或完整臨沒遺言—請葬—詔許之結構；不以最近人名決定受者，不補授者人名或贈年。`era_name_bridge`同work/commit固定帝紀raw SHA及原字位年號全稱與皇帝本紀標題，對讀傳內原短稱及現代年號表，源字不更動；不能將初中範圍硬定點或任意省字當元年。


### 正文與所附裴注的連續祖先

`parent_connection.type: parent_between_body_and_attached_note_ancestors` 為可撤回編輯父系邊，`source_assertion_id` 必須為 null，不生成直接父子來源陳述。它僅消費已驗證同一後裔的父與父系祖父兩條來源斷言：父在完整正文、祖父在該段明確所附的裴注。兩段須有同一 `source_position.source_unit_id` 與 `biography_subject_person_id`、注的 `attached_note_to_paragraph_id` 明確指向正文；身份錨點與父／祖父錨點須各自在原文有確切人物提及，不接受未決候選。

`chain_subject_person_id`、兩個祖先 assertion IDs、四個 `*_mention_id`、`source_revision`、雙來源完整 `references` 與理由均必填。`raw_projection_ref` 指向具有 `raw_file`（同目錄檔名）、raw SHA、完整 raw 行窗、分層 unit 與逐字投影的證據；正文與注的 raw 投影緊接，不得跨另一人物單元、跳過正文或版本。當前此窄型只接受 `witness_appended_pei_songzhi_note`，不能冒用唐注或一般附錄。父系不明、族父歧義、另父衝突、身份未定或循環均拒絕。

API `scripts.body_note_ancestry.body_note_ancestor_parent_valid(member, rows, assertions, chapters, root)` 由原生 family assembly validator 消費；瀏覽器 `person-family.js` 只增加此已驗證型別白名單，顯示 `assembly_inferred` 及雙引文，不能顯示為原文明父。舊 `parent_between_consecutive_ancestors` 同段規則維持不變；family assembly 尚無獨立 JSON schema enum，結構契約在本節及原生 validator，不需要放寬一般來源 schema。

## 局部母稱子句

`maternal_role` 的 `mother_unspecified` 可另帶 `qualifiers.maternal_clause`，其 `kind`、`start`、`end` 固定原段內原詞位置；仍須 `biological_mother: null`、`father_person_id: null`、完整原段引文、同段雙人物錨點及 `human_reviewed: false`。不得由這些母稱生成生母、父親或配偶。

支援的限定語式為：傳首「甲乙孫也母丙」的甲至丙；具名子女緊接「亦隨母」；具名子女緊接「賢謂其母丙」；具名子女緊接「於是竊入寢室以刀斷鼻䝉被而卧其母呼與語不應」。最後一類只處理已核完整行為子句，不按最近的其他姓名猜主體。各型須精確驗證相應字串、兩端人物及原詞位置，插入否定或截引文即拒絕。傳首所稱祖父不是子女主體，亦不因此補闕名父親。一般直接母稱、封母及前母舊分支保持。

## 授經與別祖為親的限定子句

師承的學生至教師方向不變。`teaching_clause_binding` 可保存傳首具名教師、「太宗初拜博士祭酒賜爵武城子」之朝代轉承錨點，以及緊接「常授太宗經書」的完整原詞字位。學生錨點須位於授經賓語，教師為傳首主體；不能把前一句授官的君主當教師，也不按最近姓名決定方向。全文、字位或角色不符即拒絕，不概括放寬所有「授」字為師承。

`kinship_unspecified` 的 `kinship_basis: explicit_weiqin_pair` 僅支援「三人别祖而甲乙為親」之兩具名連續人物。`kinship_clause_binding` 保存原詞字位。`generation_difference`、`exact_distance`、`lineage`、`common_ancestor_person_id`、`connecting_person_ids` 均為 null，不能由別祖、為親或相次年齡推造世代、父系、共祖或接樹。兩類均須完整原段、雙人物錨點與 AI 審閱限定；既有師承及其他未定親屬分支保持。

## 明示収養、族孫奉後與從弟子句

`adoptive_father` 可由 `adoption_basis: explicit_shouyang`、`adoption_kind: historical_shouyang` 保存原文明言収養，子女至養父；`modern_legal_status: not_inferred`、`parentage_inference: not_inferred`。不覆寫生父或將納母推成生父。限定「養者哀子女少孤収養」與「養者為司空時納子女母并収養子女」，後者須指向収養賓語而非嵌套母稱中的子女；同住、寵如公子、複數未定承受者不可套用。

`ritual_successor_of` 的 `succession_kind: named_zusun_feng_hou` 保「封前人族孫承繼者為新昌亭侯邑三百戸以奉前人後」，不推父子、法定收養或族孫精確世數。`legal_adoption_status: not_stated`、`parentage_inference: not_inferred`。

`agnatic_cousin` 的具名「客體從弟主體」保父系同輩且主體年幼，親等及共祖 null；不補共同父親。三類均用 `source_clause_binding` 的 `kind/start/end`、完整原段及精確雙人物錨點；奉後另有前人 antecedent 錨點，不能以該前文位置替換奉後賓語。原文未知與異說不變。
