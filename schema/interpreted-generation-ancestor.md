# 有資格世距解讀及已知近鏈的缺父祖連結

本有限profile只處理《梁書》〈裴子野傳〉固定「康八世孫」與已核子野至昧近鏈。不是所有「世孫」的通則。

來源斷言完整保原：`reported_generation_number: 8`、`source_number: 八`、`generation_distance: null`、`adopted_for_family_tree: false`。新 `editorial_generation_interpretation` 決定採父子距7，另保距8替代；這是中等可信編輯首選。現代研究只記reference及未獨立驗證的reported opinion，不作已驗證原始世系。

`supersedes.kind: source_assertion_assembly_interpretation_only` 只在指定家族新祖連結生效。其 `effective_assembly_interpretation` 不回寫來源，不全域覆寫原斷言，亦不刪除舊未採用判斷的歷史記錄。

祖連結type為 `ancestor_from_interpreted_generation_and_known_descendant_chain`。已知近鏈必須逐邊驗：子野→昭明→駰→松之→珪為四項來源明父；珪→昧仍為既有 `parent_between_consecutive_ancestors`、同段松之父珪／祖昧的編輯父邊。七減五得到昧至康兩邊，一個null槽，父保持未知；不補純、盾或匿名人。

模型須核固定source全文metadata、raw SHA及原行區間、全部37段文字／MIDs位置、六項來源斷言；同名異源、錯主客、改報數、母系、養系、外加具名父祖、錯源或raw co-shift均拒絕。所有AI編輯判斷 `human_reviewed: false`。原斷言ID、來源ID與原字完全不改。

本包prototype使用現行來源人物ID，不是可直接套入的正式family assembly；正式改號和全部引用遷移另階段處理。私有loader測試只用明標synthetic namespace，不能發作正式ID或alias。

祖連結另帶受守衛逐欄核對的 `generation_interpretation` 摘要，匯出profile可直接機讀報數8、首選7、替代8、近鏈5及本祖連結距2；摘要不取代sidecar完整書目，也不把原斷言的false全域改成true。
