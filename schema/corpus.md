# 卷篇標註格式 0.2

`witness_appended_edict` 保存數位見證附載的詔書文字層；只表示文本層次，不自行確定發布者、發布年或編入者。JSON 與 XML 的文字層必須一致，不能把後附詔書改作收到的篇正文。

第一目標為逐書收錄歷代正史與《資治通鑑》中出現的全部人物。目前只展開《史記》，不以取得一份全文等同完成人物收錄。

## ID 與原文

`registry/works.json` 登記著作 `w-shiji`、原書卷 `b-shiji-001` 與篇 `c-shiji-001-wudi`。卷與篇恰好一對一時仍各有 ID；現代網頁便覽標題不當成古代篇。新增卷先登記歸屬，再錄正文。

`registry/persons.json` 登記永久人物 ID，例如 `cbr-p000001`。標籤可修訂，ID 不改、不重用；它不是權威生平表。每個異稱與人物提及都附正文錨點。分拆或合併須另寫有證據的遷移決定並維護既有引用，不得靜默重指舊 ID。

`corpus/shiji/001.json` 保存正文、見證版本、權利、指紋、審閱狀態與提及位置。`source_id` 為本卷見證識別碼，來源資訊就地保存在 `source`；它目前不引用舊 `sources/` 目錄。這個區別須在舊資料遷移時明確處理。

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

已發布序號ID保留為永久相容別名，不重用；正式人物ID已全面轉換為家族式格式，舊 `next_number` 僅保留序號游標。已發布身份後來合併、分拆或改父系，必須保留舊入口與有證據的遷移決定，不靜默改名。

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
