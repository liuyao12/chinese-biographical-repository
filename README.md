# Chinese Biographical Repository（CBR）

以史料為中心、由人與 AI 代理共同維護的中國歷史人物資料庫。CBR 已整合 **人文 · Ren-Wen** 的資料、閱讀器與 Git 歷史。

[開啟人文閱讀器](https://liuyao12.github.io/ren-wen/) · [人物](https://liuyao12.github.io/ren-wen/profiles.html) · [著作](https://liuyao12.github.io/ren-wen/works.html) · [傳記目錄](https://liuyao12.github.io/ren-wen/library.html)

## 收錄目標與目前範圍

第一目標是逐書收錄歷代正史與《資治通鑑》中出現的全部人物，辨認異稱並逐段連結人物 ID、著作／卷／篇 ID。目前先處理《史記》，卷一〈五帝本紀〉已有 28 段正文、57 個人物 ID、412 個人名或未定稱呼錨點及 12 項異稱判斷；仍待指代、身份與版本複核。卷二〈夏本紀〉新增 35 段正文、235 處人名或未定稱呼錨點、20 個人物 ID、21 項異稱／跨卷判斷與 26 項來源親屬主張；卷三〈殷本紀〉新增 33 段、384 處錨點、79 個人物 ID、22 項身份／異稱判斷、50 項來源親屬主張及 3 項人物區分記錄。前三卷合計 156 個人物 ID，仍不是完成覆核的史實名單。卷四〈周本紀〉86 段已有首輪明示人名標註，798 處人物或未定錨點、40 項身份／異稱判斷、69 項來源親屬主張及 6 項人物區分；人物登記合計 310 個。「周最／周聚」及匿名指代等仍待覆核，不稱全部人物已完成。卷五〈秦本紀〉77段已有首輪標註，946處錨點、46項身份判讀、76項來源親屬主張、7項人物區分及3項未決身份候選記錄；人物登記合計534個。未決候選ID不等於確證不同人物，稱號時段與版本、匿名指代覆核仍待完成。卷六〈秦始皇本紀〉127個文字區塊含16個刻辭／嵌入引文及分層的附載班固記，已有823處首輪錨點、34項身份判讀與39項親屬主張，登記合計647個人物候選。卷末相反世系分存，全部身份、校勘及稱號時段覆核尚未完成。卷七〈項羽本紀〉45段已有986處首輪錨點、50項身份判讀、14項親屬主張、2項人物區分及1項已發ID同指決定；本卷累計新增98個候選人物，登記合計745筆。另保存55項稱號持有／用稱與有效時段證據試點，未知曆日與終點不補造，並未完成本卷全部稱號史。身份、代詞、匿名者、版本及研究覆核仍未完成。

本次整合保留 Ren-Wen 的 ECCP 全書首輪匯入與 235 卷《清史稿》數位文字，以及來源、人物、著作、地名、引文、覆核紀錄與年代工具。其來源目錄目前有 1,244 項見證、67,131 處標註、16,190 項人物／著作等實體。這些是既有資料量，不是已人工消歧的不同人物總數，也不代表《清史稿》已完整收錄或學術審訂。

稱號須保存各自有來源的有效時段，包括爵位、官職、兼任、檢校和追贈；有效期間與文獻何時用該稱號稱呼某人分開。現有 `data/name-history.json` 保留曾國藩的年尺度試點，仍須擴充完整的起訖、日期精度與不確定性。`corpus/shiji/007-titles.json` 另保存卷七的來源事件及用稱錨點，尚未與舊年尺度試點或線上閱讀器統一。

公開史料中的歷史人物可收錄；不收錄在世人物的私人傳記、私人家譜或聯絡資料。傳說敘事另標示，不把記載當作已證實的史實。

卷八〈高祖本紀〉已保存固定版本的91段正文；第1至40段有489處人物或未定指稱錨點、30個新增候選、64項身份判讀與11項來源親屬主張。全庫目前775個人物候選；第41至91段仍待標註，尚未連接線上閱讀器。

## 來源與人物 ID

兩套已發布格式先完整保留，避免在整合時改壞引用：

- `corpus/`、`registry/`：CBR 的卷篇 JSON／XML、穩定人物 ID 與逐書進度。
- `sources/`、`assertions/`、`decisions/`：原有唐代史料、精確引句、身份與取捨判斷。
- `data/upstream/`、`data/texts/`、`data/imports/`：Ren-Wen 的來源基線、行內標註文本與匯入見證。
- `data/catalog.json`、`data/people/`、`data/works/`：來源目錄、人物／著作記錄與提及。
- `data/name-history.json`：已有據的姓名／稱號時段及文獻用稱。
- `assets/` 與根目錄 HTML：無 AI、無後端相依的閱讀器。

`cbr-p000001` 等 CBR ID 與 `person-*` 等原有 ID 均保持不變；**同名不自動合併**。跨格式對應仍需逐項證據，格式統一與文字覆核列入[整合紀錄](docs/ren-wen-integration.md)。原有段落、出現位置、版本指紋及署名不因匯入而改寫。

SQLite 只是可重建的派生索引，不是另一個可編輯的權威資料庫。使用端以一般程式讀取已記錄的識別、取捨與時段，不把史料交給 AI 處理。

## 檢查

Python 3.11+ 與 Node.js 可執行離線檢查；閱讀器是原生 HTML／CSS／JavaScript。

```sh
python3 scripts/validate.py
python3 scripts/validate_corpus.py
python3 scripts/render_corpus.py --check
python3 scripts/renwen.py validate
python3 scripts/profiles.py validate
python3 scripts/works.py validate
python3 -m scripts.text_units validate
python3 -m scripts.round1_validate
python3 -m scripts.name_history validate
python3 -m unittest discover -s tests -v
npm test
npm run check
```

派生索引：`python3 scripts/renwen.py build-db`，再執行人物、著作、文本層次及姓名時段的 `index-db`。網站發布仍經過既有 Pages 的實際 HTTP／瀏覽器檢查，部署記錄標示所用 CBR 提交。

## 貢獻與權利

請閱讀 [代理指引](AGENTS.md)、[貢獻規範](CONTRIBUTING.md)、[CBR 卷篇格式](schema/corpus.md)、[人文資料架構](docs/architecture.md)與[來源說明](docs/provenance.md)。人與其他 AI 代理透過 PR 貢獻，可由 Git 修正或撤回；不得冒稱人工覆核。

原有 Ren-Wen 軟體保持 MIT 授權，史料、數位轉錄、標註與地圖各依其記錄的授權，MIT 不重新授權它們。參見 [權利說明](RIGHTS.md)、[歷史地圖範圍與條款](docs/reference-maps.md)。墓誌以轉錄文字及影像來源連結為主；匯入的裁切參考地圖是既有閱讀器資產，不是墓誌影像庫。
