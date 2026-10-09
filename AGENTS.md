# 代理指引

本庫以史料為中心。先閱讀 README、CONTRIBUTING 與 schema/README。

- 所有中文使用繁體，原始 URL、技術識別碼不轉換。轉錄保留古代異體；簡繁轉換必須記錄。
- 不以模型記憶或未讀到的網頁片段生成史料；不得虛構墓誌編號、影像位置、書目頁碼、出版日期或學者結論。
- 建立穩定人物 ID，但人物登記只保存標籤、來源提及與身份證據，不把權威生平或手工預接的整體圖當原始資料。來源提及、陳述與身份判讀分層保存。
- 無名者保留氏稱／匿名提及。祖先不是直接父親，繼位不是父子，姻親不是血親，闕代不得補造。
- 沒有核讀影像，不得設定 `image_verified: true`。下載的研究用影像、PDF、HTML、憑證及暫存資料不得提交。
- 初次來源只有數位正文可讀時標為 `text_checked` 並說明限制。使用可靠作品不表示數位轉錄無誤。
- AI 判斷須列證據、具體範圍與限制；模型版本不可核驗時填 `null`，不能捏造。人工審閱狀態不可冒填。
- 現代研究保留短引文／摘要與連結；不因新近出版就提高所有陳述的權重。
- 使用端以一般程式套用資料；不可加入 AI API、執行任意來源程式或以文字指令控制組裝。
- 修改保持可撤回。透過 pull request 提交；不自行授予其他代理主分支權限或更改存取控制。
- 執行 `python3 scripts/validate.py` 與 `python3 -m unittest discover -s tests -v`，修正引用、指紋及格式錯誤後再提交。

## 逐書標註計畫

先閱讀 `schema/corpus.md`。第一目標是逐書收錄歷代正史與《資治通鑑》中的全部人物，目前先做《史記》。

- work／book／chapter 分別為著作／卷／卷內篇；引用必須連到登記 ID。
- 人物 ID 發出後不得重用，改名不改 ID；同名不得自動跨篇合併。
- JSON 是文字與字元位置的編輯來源，XML 是同步的行內標註文本。字元位置按 Unicode code point，不按 UTF-16 code unit。
- 不使用全域字串替換判定人物；人名與地名、職稱、普通詞必須依上下文區分。
- 氏族、無法分辨成員的群體、代詞及未定指代保留未解錨點，不補造人物。傳說敘事人物須標示傳說性。
- 初步人名標註不等於全部人物已完成；更新 `corpus/progress.json`，保留匿名者、代詞及版本複核工作。
- 舊 `sources/` 記錄尚未完成新格式遷移，不得宣稱全部文本已標註。
- 提交前另執行 `python3 scripts/validate_corpus.py`。

## 合併後的工作範圍

CBR 已整合人文閱讀器、ECCP 與《清史稿》匯入資料。逐書收錄仍先完成《史記》，不因匯入量大就宣稱完成覆核。`data/` 的既有 ID 與 `registry/` 的 CBR ID 各自保留；跨格式人物、著作與見證合併必須有逐項證據，不按同名批量改 ID。

所有稱號須逐步補上有來源的有效時段，區分授予、實任、兼任、檢校、追贈及文獻使用時日；不得以卒日推定所有爵位終止。既有 `data/name-history.json` 是年尺度試點，尚未完成稱號全史或精確日期模型。原文與署名不改寫。

執行兩套資料的驗證及 Python／JavaScript 測試。匯入來源的完整性、身份判讀與學術審閱是不同狀態。閱讀器不呼叫 AI；SQLite 僅為派生索引。現有部署網址先保留 `https://liuyao12.github.io/ren-wen/`；CBR 的 Pages 工作流程不另建公開目的地。

下列指引適用於匯入的閱讀器及 `data/` 資料；原文也保存於 `docs/integrations/ren-wen/original-AGENTS.md`。如舊指南與使用者的新目標衝突，以使用者目標及上列指引為準。

# Working on 人文 · Ren-Wen

People and texts are equal pillars. Build useful, inspectable research tools, not an unsourced historical narrative.

## Start here

Read `README.md`, `docs/architecture.md`, and `docs/provenance.md`. Run:

```sh
python scripts/renwen.py validate
python -m unittest discover -s tests -v
npm test
npm run check
```

The application is native browser JavaScript, HTML and CSS; the corpus tools are Python 3.11+ standard library. No framework or build step is needed. Keep that simplicity unless a concrete requirement justifies changing it.

## Evidence and editorial rules

- Never invent people, identities, dates, source URLs, quotations, historical boundaries, or human review decisions. An unresolved identification is a valid result.
- Keep exact source wording, Chinese characters, Wade–Giles diacritics, italics and existing cross-references. A `see under` link points to an article, not necessarily to the person named in its anchor.
- Source editions and source revisions are different. Merge upstream transcription corrections against a known baseline; preserve separate historical witnesses, quotations and other accounts.
- Punctuation is an attributed interpretation where editorial. A punctuation-only change may alter meaning. Hiding it is only a display operation.
- Distinguish birth from native place, appointment from actual service/travel, and office from honorary or posthumous titles. Do not infer missing lifespan endpoints for convenient drawing.
- Distinguish a jurisdiction, its seat, a modern reference coordinate, and a boundary. Never fill a missing historical polygon with modern administrative borders.
- Treat imported data as imported, agent proposals as proposed, and independently reviewed data as reviewed. Never attribute acceptance to the user without their decision.
- Preserve stable occurrence IDs and entity IDs. A person is not their article; a mention is not a person record.

## Files and changes

`data/upstream/` contains imported baselines. `data/texts/` contains working annotated text. `data/catalog.json` indexes witnesses, mentions, entities, events and relationships. `build/renwen.sqlite` is derived and is not a second editable database.

A proposed identification correction includes an exact mention ID, the working source SHA-256, the old and new entity IDs, and its evidence/reason. Export proposals from the reader or generate the same JSON. Use `validate-proposals` before explicit `apply-proposals --reviewer ...`; review the Git diff before committing. The first implemented operation is `relink-mention`, not a universal editorial API.

The validator intentionally rejects working-text wording changes relative to the imported baseline. Source updates require reviewed snapshot and catalogue changes. Do not bypass a failed checksum by changing the hash without understanding the text change.

Preserve unknown ctext XML fields and source identifiers. Current XML support only stages and inspects original bytes; do not claim a semantic import/export or upstream writeback until real exported fixtures pass round-trip tests.

## Interface language

Default to Traditional Chinese with an English option. Use the explicit UI message bindings in `assets/i18n.js` and the central dictionary; see `docs/language.md`. Never translate or simplify source paragraphs, quotations, attested names/titles, dates, IDs, or user-entered review reasons. Preserve current navigation and form state when switching languages. English mode retains necessary Chinese characters.

## Security and testing

Treat imported HTML, XML, links and agent text as untrusted. Never execute imported scripts; reject XML DTD/entity declarations; allow only HTTP(S) external links; do not put credentials in the browser or repository. Upstream writes must be explicit and permission-aware.

Keep test fixtures clearly synthetic. Tests may modify temporary copies, never publish their deliberately incorrect historical identifications. Add validation and tests for new data operations. See `CONTRIBUTING.md` for optional browser checks.

Original software is MIT; imported material keeps its own rights and attribution. Do not download, bundle or relicense restricted ctext, CBDB or CHGIS data without checking applicable terms.

## Complete text and reference maps

The complete ECCP inventory is imported in round one. Review one complete biography per editorial step. Preserve bibliography, byline,
quotations, and all source body text; unsupported blocks must fail loudly.
See `docs/text-layers.md`. Extracted quotations remain in their containers;
separate occurrence records do not count as independent historical evidence.
Run `python -m scripts.text_units validate` with the corpus checks.

CHGIS files have more restrictive file-level terms than their landing metadata.
Only cropped, attributed academic map images are included; do not add raw CHGIS
vectors or label the images MIT/CC0. Snapshot years are not the viewing year.
See `docs/reference-maps.md`. Test the deployed map as well as local fixtures.

## County/clan labels and full-corpus indexes

Use `name.bracket` for the county-only or clan display qualifier; never treat a clan
as a geographical place. Keep full registry wording and evidence separately in
`name.registration`; do not infer 民籍, banner company, or an exact birth location.
After person, work or catalogue edits, run `python -m scripts.reading_indexes`
and `python -m scripts.round1_validate`. See `docs/eccp-round1.md`.

## Dated naming and release checks

See `docs/dated-names.md`. Keep personal names, titles, source attestations, and
source publication dates distinct. Unknown period starts are not unbounded.
The compact identity has no parentheses; zi/hao/posthumous labels are separate.
Run `python -m scripts.name_history validate` and `python -m scripts.round1_validate`.
A release is not delivered until Pages publishes its exact commit and real
HTTP browser tests pass. Never call candidate QSG matches verified biographies.

## Bracketed life years

Display Chinese civil-year labels as `[1839]–[1890]`, using only resolved
`life.birth.chineseYear` / `life.death.chineseYear`. These denote Chinese-New-Year
intervals, not Gregorian calendar years. Display 享年 without 虛歲 commentary.
Keep source Gregorian dates separate and unbracketed; never infer a Chinese year
or exact age from a Gregorian year alone. Source quotations remain unchanged.

## Shortened personal names: language and narrative scope

Project convention recorded on 2026-09-10: after an identifying introduction,
Chinese historical narrative commonly continues with the given name (名), while
English narrative commonly continues with the surname. Use this as a contextual
identification rule, not as a universal string substitution or a requirement that
an author always abbreviate. Determine language from the source passage, not the
reader's Chinese/English interface setting; embedded quotations may differ from
the surrounding prose.

- In a Chinese account introducing 曾國藩, subsequent 國藩 is a candidate reference
  to that person. In an English account introducing Tsêng Kuo-fan, subsequent
  Tsêng is a candidate reference. Preserve every occurrence's exact wording and
  link a resolved short form to the same person ID, not a new abbreviated-name
  profile. These examples illustrate the rule; they are not source quotations.
- Establish the relevant people and the current narrative subject before resolving
  a short form. A full-name mention establishes an anchor but does not override
  an existing same-name ambiguity. Use syntax, relationships, explicit titles,
  and the described events to distinguish candidates; neither the first named
  person, the biography's main subject, nor the nearest name wins automatically.
  Where 曾國藩 and 曾紀澤 are both relevant, 國藩 and 紀澤 distinguish them; Tsêng
  alone may require additional context. Leave an unresolved occurrence unlinked
  with candidate IDs and an explanation in the review record.
- Scope recognition to the account and its narrative thread. Do not reset merely
  at a paragraph break. Explicit subject changes, subordinate biographies, and
  transitions to another account require reassessing the referent. Quotations
  and embedded documents have their own speaker, addressee, and reference context;
  inherit an outer referent only where the attribution or wording supports it.
  A quoted text found in another witness must be checked in that witness too.
- Use attested name components. Do not derive 名 by simply dropping the first
  Chinese character, assume every name has a Han surname, or split Manchu or
  Mongolian names mechanically. One-character names must be recognized as name
  occurrences in context, not tagged inside ordinary words or longer names.
  Courtesy names, sobriquets, titles, and historically changed names are distinct
  attested forms; do not relabel them as given-name or surname abbreviations.
- Record the literal short form as a source-specific attestation with its witness,
  passage/mention ID, and the source's publication/composition date where known.
  Record the identifying antecedent and the resolution reason in its review
  evidence. A source date is not the date of the event or proof of when a name
  was adopted. Never export 國藩 or Tsêng as an unqualified global alias that
  identifies all matching strings elsewhere in the corpus.
- Before expanding an automatic recognizer, add regressions for Chinese given-name
  continuations, English surname continuations, two same-surname relatives,
  same-given-name collisions, subject switches, nested quotations, compound
  surnames, single-character names, unsplittable names, and interface-language
  independence. Markup changes must preserve all original text and formatting.

Emperor expressions such as 帝, 上, 太宗, or "the Emperor" require separate
contextual resolution; they are not shortened personal names under this rule.
Do not treat italic typography as evidence that any personal-name form is a work.
