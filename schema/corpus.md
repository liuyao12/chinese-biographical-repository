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
