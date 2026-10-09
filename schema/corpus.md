# 卷篇標註格式 0.2

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
