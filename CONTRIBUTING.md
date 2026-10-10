# 貢獻規範

歡迎人與 AI 代理提交可核查的小批修改。使用分支與 pull request；已合併內容仍可由後續提交修正或撤回。

## 收錄邊界

收錄公開歷史史料中的古代人物，不收錄在世人物的傳記或親屬資料、私人家譜、聯絡方式、帳號憑證。現代學者姓名只作書目署名，並非建立其傳記記錄。第一個完整收錄目標為歷代正史與《資治通鑑》中的人物，逐書完成；目前以《史記》為先。原有唐代小型起始集保留並待遷移。傳說人物另標示敘事性，不能當作已確證的古代生平。

正史的首輪整理以本紀、世家、列傳等傳記體裁為主，非傳記卷篇可先跳過；這是整理優先次序，不是永久排除其中的人物。唐代及以後史書的世系、宗室與宰相世系資料是重要例外，應列入整理。《資治通鑑》仍按卷整理。

## 史表與世系表的連續閱讀

表格閱讀器應把同一張表跨頁的內容接成可連續捲動的表格，不以掃描頁界中斷。保留原頁碼、影像 URL、儲存格位置與來源提及 ID，讓每項內容可以回到原頁查核。重複表頭只在閱讀層處理；表格的方向、合併儲存格、空格、闕文、續表與世系支線須按原文明確銜接，不因相鄰位置推造親屬關係。寬表可橫向捲動，表頭應保持可見；原始轉錄及頁界另存，不被現代排版覆寫。此項是後續閱讀器功能規格，目前尚未實作。

## 新增史料

1. 查驗作品、作者、出版物及具體位置。墓誌需辨別文集傳本、石刻、拓本、照片、發掘報告與再刊文本；同一作品的不同載體不是獨立作品。
2. 給出可直接查閱的個別記錄網址或固定版本。影像記錄包括機構、記錄編號、頁／葉／版、必要時的行與圖像區域。無法找到時如實留空，列入待查工作。
3. 先錄文本，保留闕字、異體、疑讀與分段。排除介面、註號與未明示的現代校註；不可把註釋當成古文。節錄須明示範圍，不稱全文。
4. 中文以繁體顯示。簡體來源的短引文如需轉換，明記 `character_conversion`；不得暗改人名、異體或歷史讀法。原圖 URL 與技術檔名不更動。
5. 核實權利。古代原文與現代點校、標點、轉錄、照片的權利分開記錄。現代研究以書目、短引文及自行撰寫摘要為主，未獲授權不得複製全文。
6. 每個名字與關係以來源內的提及識別碼記錄，附精確原文引句和判讀理由。氏稱不補造名字，「某」不當作姓名；不同女性的相同氏稱不能合併。

## 修訂身份與優先次序

- 每項身份比對列出來源提及、證據及限制；同名不充分。
- 逐篇整理時可查閱維基百科人物條目，作為異名、爭議、相關人物與書目搜尋線索。維基百科及其鏡像不作人物身分、親屬、稱號、紀年或來源優先次序的權威證據。
- 百科線索與已核讀證據分層記錄；沿註腳核讀原史料或現代研究後，引用實際材料及具體位置。未取得或未核讀的材料標為待查，不把百科摘要轉寫為學者已核實結論。
- 世系表及譜系材料中的親屬關係逐項保留來源，不當作無爭議事實。遇到衝突，直接相關的傳世或出土一手材料原則上優先於後出世系編纂；核實成文時代、傳承、真偽與具體證據，不因材料出土便一律視為可靠。
- 優先判斷記入資料，連同支持與反對的原文、適用陳述、判斷理由及覆核狀態；保留不同主張，供無 AI 的閱讀器依已記錄規則處理。
- 每項取捨限特定身份組與陳述類型，保留候選及相反意見。未解時 `preferred_assertion_id` 必須為 `null`。
- 現代學者意見須記篇名、作者、出版日期、頁碼、具體結論及證據。不將「或誤」提升成已證實錯誤，不將一位學者提升成共識。
- 找不到出版年不得以網站上傳日期代替。「最新意見」須說明搜尋範圍與查閱日期；不能保證窮盡時不作此稱。
- 修正轉錄仍須留存舊版本的 Git 歷史；移除或改名識別碼時同步處理所有引用。

## 提交前

執行 README 的離線檢查及測試。提交說明列明新增／改動史料、實際查閱頁面、核驗方法、權利及仍未解決的問題。程式檢查證明格式與引用一致，不證明史料真實或學術判斷正確。

## 行內標註與穩定識別碼

新增逐卷正文使用 [卷篇格式](schema/corpus.md)。每個人名提及連到人物 ID，篇連到卷與著作 ID。身份合併要附本文明示或上下文證據，未明示者標為暫定；官職與同名人物不得混淆。正文修改必須同步字元錨點、XML 及指紋。執行 `python3 scripts/validate_corpus.py`。

## 人文閱讀器與匯入資料

所有提交同時保持 `sources/`、`corpus/` 與既有 `data/` 的來源、ID、文字錨點和版權。軟體的 MIT 授權不適用於史料、數位轉錄或地圖。資料合併與人物身份合併分開審閱。原有貢獻流程如下，初期限制須結合目前 README 的範圍閱讀。

# Contributing

Use a branch and pull request for substantial changes. Small evidence-backed data patches are preferable to opaque wholesale rewrites. Describe what changed, its evidence, and any affected interpretations.

## Run and test

```sh
python -m http.server 8000
python scripts/renwen.py validate
python -m unittest discover -s tests -v
npm test
npm run check
python scripts/renwen.py build-db
```

The reader works without installing Python or JavaScript packages. Optional browser tests need Playwright and Chromium:

```sh
python -m pip install playwright
python -m playwright install chromium
python tests/browser_smoke.py http://127.0.0.1:8000
```

`CHROMIUM_EXECUTABLE` selects an existing Chromium executable. `RENWEN_OFFLINE=1` uses an in-memory local fixture instead of navigating to a server; this checks interactions, not HTTP loading. `RENWEN_SCREENSHOT=build/reader.png` saves a desktop screenshot. The normal server-based mode remains the deployment-relevant smoke test.

## Identification proposals

Select an annotated occurrence, inspect its evidence, choose a candidate, and explain the correction. The browser queues a proposal; it does not edit the accepted corpus or publish upstream. Export the queue as JSON.

```sh
python scripts/renwen.py validate-proposals proposals.json
python scripts/renwen.py apply-proposals proposals.json --reviewer "Actual reviewer"
python scripts/renwen.py validate
git diff
```

Only claim a human review when that person actually reviewed it. A source hash, the original identification, existing target ID and meaningful explanation are required. Stale or competing changes are refused. Accepted changes update working HTML, the mention index, checksums and `data/reviews.jsonl`; imported baselines stay untouched. Multi-file writes are not a filesystem transaction: work in a branch and use a reviewed Git commit as the publication boundary.

## Sources, editions and punctuation

Record bibliographical identity, the actual import method, source URL/revision, retrieval date, rights and punctuation provenance. Never label manually prepared excerpts as a raw API export or a complete biography. When the printed base edition is unknown, say so.

Compare incoming source corrections with the saved unannotated baseline and our working version. The `merge` command makes a candidate file, never silently applies it. Different historical editions and quotations are separate witnesses; a biography in another work is another account, not automatically a textual variant.

## Present limits

The seed annotations and events are proposals, not independently human-reviewed facts. No historical jurisdiction geometry is included. ctext XML support is raw staging/inspection only; submit a legally reusable real export fixture and its provenance before adding semantic mapping. Never commit API tokens or third-party data with unresolved redistribution rights.
