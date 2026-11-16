# 固定作者連結節題與引錄文書的完整本傳

`fixed_wikisource_linked_heading_quote_biography` 只接受「== [[作者:傳主|傳主]] ==」至下一同級人物節題。標題連結是paratext，不能成為正文人物提及。固定修訂/完整raw SHA/傳題由獨立可信pins資料約束，不能靠共移raw offsets並重hash冒成同見證。

逐字投影僅排版空白、quote模板外殼、單純wiki連結、YL與粗體；quote原引奏疏/箋/策仍為收到本傳原文，不標成後人古注。每一個選定raw codepoint必屬可見字或有類別的排除位，無漏段/漏家屬續敘。未知markup拒絕；章內原字/標點/順序、全段數/邊界與每字原位皆驗。raw/receipt須實體路徑，symlink逃逸拒絕。

此契約只證明數位見證完整與原字，不證身份/家譜或已親核古本。作品成書metadata、最早現存版本、數位實際底本另存，未知不填。人物與作品判讀另有逐錨閱讀記錄，仍human_reviewed=false。

### 卷末附傳與共評贊

固定 linked-heading 見證 pin 可明示 `selection_mode: through_final_criticism_to_footer`。此窄分支要求主傳後緊接的同級節題正為 `【評贊】`，其後不得再有另一節題，並須有完整標準卷末 footer 與作品分類；只在固定 raw SHA／revision／題名校驗下啟用。選段包括附傳、全部文書與共評贊，footer 不當傳文。舊 pin 不帶此鍵時仍在下一同級節題前終止，既有來源範圍不變。

新分支將來源位置的 `source_layer` 分為 received_biography、received_quoted_document（網站quote模板整行）與 received_criticism；正文混合內嵌奏議／遺令仍保完整原行，文書與說話者範圍另見逐段閱讀判斷，不冒古注。所有可見字原位與排除位的聯集須恰覆完整選段；不是以摘要代替長篇文書，也不能在附傳或共評前提前停止。
