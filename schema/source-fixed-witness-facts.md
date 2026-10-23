# 完整固定見證的來源事實槽

`annotation.fixed_witness_fact_slots_ref` 指向受版本控制的 `scripts/fixed_witness_fact_slots.json` 配方。配方先驗完整原生來源單元、固定 revision、實讀原始檔雜湊、全段原詞與逐人角色位置，才按實際人物錨展開已覆核資料。它不是自然語言解析器，亦不接受來源文字作程式。

每筆 runtime 記錄的 `fixed_source_fact_binding` 含 `kind`、配方 `key`、唯一 `slot`。姓名仍經既有姓名／同源姓氏合約；官稱仍保 `title`、`kind`、`mode`、原詞錨與未知端點；生命事件不因其他事件補年。`person_bundle.load_catalog(root)` 與原生直接 CLI 均檢查配方全部槽存在、無重複且與原角色和語義相同。所有來源讀取必須傳實際 root。

本例的「參鎮西鐘會軍事」以 `title_formation.kind=interleaved_commander_reference` 保留分置的參／軍事與長官鐘會；「復職」以 `same_office_reinstatement` 指回前次中護軍，不稱第二次出現原字中護軍。「在職十三年」為獨立 `office_duration`：連至兩次持職而 `episode_assignment` 未定，不生成端點或每任各十三年。戲言各十年是 `hypothetical_office_request`，不記實任。白衣領護軍為權限與身份；正式復職另記。詔賜為命令而非交付或葬事；「先後之親」只存原稱，親等及中介人物未知。

無來源年月、歲數、籍貫與葬地，仍不產生數值。本例不改已有近親斷言、編輯家族組裝、人物 ID 或原始來源字節。
