# 既存節錄型事實（有限見證契約）

`fixed_archived_excerpt_fact` 驗證既存帶 SHA256、行號與可見文字投影的選錄；不是完整原始檔、刊本或影像驗證。可信配方另固定全部選錄原字、17段 metadata、人物字位和同指組，候選檔改字/移位後自行重算局部 hash 仍不合配方。不能用此契約替代已有完整 raw 驗證器。

章級 `archived_excerpt_fact_slots_ref` 與每筆 `archived_excerpt_fact_binding` 以 key/slot 對應可信腳本旁 JSON。配方僅資料，不能執行。人物端點由穩定 MID 解析現行 ID；原 MID/引文/原字不改。必須保全部槽，不允許刪章ref降級、漏名、改人物、同段換人或跨段借字。已完整明名的構件標原文明名，不附省姓推定資格。

姓名省姓採 `contextual_surname_from_archived_excerpt_paths`，由同源完整名種子經明示父、祖先、兄弟/父系旁親作有限編輯承姓。最多三步、無循環、不補未名父或共同祖先；配偶、母系、收養、同姓ID與郡望不能當路徑。早段省名若同章已有同人完整姓名，可零步同指thread承姓。只有名而沒有支持路徑者 surname 為 null。`zi` 可由精確原字位綁命名傳主，不需捏造新person MID；不得換成同段旁人或另一段的字。

`kinship_unspecified` 的 `kinship_basis: archived_excerpt_collateral_appellation` 僅保存受信原詞的父系旁系世代。族曾祖/族父不改為直系曾祖/父；`generation_difference` 的負數表示客體較主體早代，共同祖先、精確親等、連接人皆 null，不入父系父邊。從兄保留既有 `agnatic_cousin`、同代、相對年序與未知共祖，不變親兄弟。

本型只核上述收到節錄，未重取完整 raw、未校圖、`human_reviewed` 保 false。現有生卒、報齡、地望及來源限定不因新增姓名改動。
