# 作品年代、版本與出土履歷

編輯來源為 `registry/work-provenance.json`；由閱讀目錄匯出為 `data/corpus/work-provenance.json`，`data/corpus/works.json` 的 `work_provenance_path` 提供入口。作品沿用各自登記 ID，不以書名合併舊資料與原生資料。

每部作品分開記錄：

- `composition`：撰作、編纂或完成時間；後人續補、古注與原作須分項說明。
- `earliest_extant_edition`：現存見證及其範圍。殘卷、補配本、完整本及某種注本的最早版本不得互換。
- `text_bases`：每一正文來源實際所據版本，以及可確認的最早底本。未能建立版本鏈時留空；一個古本的存在不證明本站轉錄出自該本。
- `burial`、`excavation`：埋藏或下葬、首次發現、所報出土、發掘工作的日期與地點分開。死日不能直接作葬日或刻誌日。

`not_researched` 是尚未查考；`unknown` 是現有已讀依據未能確定；`reported` 是有來源報告；`disputed` 保存歧說。缺值不填推測年。數值日期須聲明曆法、紀年編碼及精度；只知朝代可保留 `period_label` 與 `date: null`，不得造起訖年。數位修訂號與存取日仍在各正文 source，並不代表成書或版本年代。

每項肯定斷言均須有 `reference_ids`、範圍與資格說明；代理覆核不等於人工覆核。現代書目或論文所報古本，不冒作親見該古本；圖片和PDF不入庫。

新增作品／正文來源後執行 `python3 scripts/work_provenance.py --scaffold` 補未知欄位，再逐項研究；執行不帶參數的同一命令檢查全量覆蓋。閱讀目錄匯出也會驗證履歷，不能發布遺漏新增原生作品或正文來源的履歷。

初次建立欄位只表示有待辦與可解析契約，不表示全部九千餘項舊作品已完成書目考證。王閩之誌的出土日目前據2009年後出研究；1972年原發掘報告尚待核讀。
