# 固定 Kanripo 來源事實：多配方

`scripts/fixed_kanripo_fact_slots.json` 保留既有025單配方與API。其他已完整核讀單元由受信程式資料 `scripts/fixed_kanripo_additional_fact_slots.json` 的 `recipes`（key→配方）選取。卷篇以 `annotation.fixed_kanripo_fact_slots_ref` 指明kind/key，資料不能指定可執行模組、函式或任意recipe檔路徑。

額外配方必存完整人物角色模板、全段層次、固定提交/原檔SHA、既有witness key及事實slots。`$person`/`$mention`只按固定段與人物角色位置解析；它不是按人名猜測的NLU。來源原字與全人物錨均須符合完整模板；實際root讀獨立pin、全原檔與逐字projection，pin chapter binding不可缺。

額外配方的raw path/SHA來自既有獨立pin projection，不必補造chapter.source欄位。既有025仍驗其原source.raw_path/raw_file_sha256；025完整配方檔不重寫。`valid_from_paragraphs`按斷言binding key找相應完整章，核所有段與收到的paragraph index精確相同。

父子、兄弟、從兄、繼母、女壻分型。純弟不添加source同父或母名；從兄距離/共祖未知；繼母不是生母；女壻未名之妻不等於來源出現具名公主。推定同父家族組裝另行，不能把編輯父系當新source father。
