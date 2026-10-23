# 同固定傳世見證之有限近系推姓

`contextual_surname_from_bound_received_family_units` 是 `surname_basis` 的獨立分支，不放寬既有同章 named-family path。姓為編輯 `contextual_provisional`，原ming、字、本名及原句不變；人與關係不存在時不由ID、label、郡望、族弟或組裝邊補人／姓。

basis exact fields：kind/status/human_reviewed/rationale/source_name_record_id/source_full_quote/source_units/seed_frame/steps。原全文名seed必有未推導的surname+ming，人物錨原字正好全文名；可在原文引語中，不能用官稱或已推姓者替代。

source_units逐項綁chapter_id/native_path/work_id/book_id/source_id/source_revision/raw_path/raw_file_sha256。1–3個完整原生單元須同作品、同卷、同固定修訂、同全檔raw SHA；各自raw路徑可以不同，但都必實際root讀取、完整單元與投影驗證，不能只比保留片段。native_path拒越界與symlink，實讀原生章必等於所傳catalog。每步段frame含chapter/paragraph/整段SHA/revision/raw SHA，逐步evidence必等於既存source關係完整evidence，原語及人物字位另驗。

最多5步，不重複人物或assertion；generation_before/after為整數。只容：

- `older_to_younger`：既有傳首具名「甲弟乙」契約；或同句精確「乙兄甲」兩個具名角色，原source_term／相對年序／位置與引語外從句界均核對。世代不動。
- `father_to_child`：既有具名父「遣長子／第幾子」全raw契約；或既有qualified相鄰子附傳（含長子），來源父傳首具名弟／族弟可驗，其他具名角色僅可為有來源的父祖角色或明帝號「初」的紀年，不允許引語或未綁來源的主語轉換。世代加1。
- `child_to_father` / `child_to_paternal_grandfather`：同一具名傳首「甲族弟乙」之明祖／父序，必同時有兩項既存source關係與原角色錨，祖非外祖，父非母父；不容插入別人、否定、異說或引語。只准祖官諡從句內明式「諡曰…」；不因此放過其他曰字引語。世代分別減1／2。

明父／祖／兄弟只供推姓。不得使用母、配偶、養、義、同母異父、未知共同父、族弟或editorial assembly推姓，不產生新的source父斷言。編輯家族父邊另外保assembly資格。本分支新增root參數沿validate_corpus、person_bundle、surname_from_father真call site傳入；舊四參數分支維持。
