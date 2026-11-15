# 武英殿宋045選錄人物層

本有限契約覆蓋已轉錄劉粹、劉道濟及劉損15段完整選錄；不表示全卷收錄。`fixed_ner_role_layer` 的固定資格與 `ner-role-contract.json` 逐段文字雜湊、MID、字位、角色相驗；既有外源角色由固定完整段與MID、來源metadata雜湊及registry反向證據動態解析。首次分配的新人物號只屬安裝提案，重播與驗證不以固定UID、owner鍵或ID字母判身份。

原source-only轉錄守門保留。新增層須先驗過自身契約，才移除自身標記與還原原pending/空mentions投影，交原守門驗全文、圖頁位置、原列、raw與取得資格。這不是豁免舊guard；原字、段界、日字及疑字仍固定。

`wyd_relation_binding` 只驗十個具名近親原句。祖/父/弟兄/族弟/從父弟分存；相對年序沒有絕對排行。`庶長子` 保原稱，不賦全體子女ordinal一；`從父弟`保AI詞義路徑但不建立中間父祖。粹—道濟已有宋044明弟，不重複建同書等義斷言。

`contextual_surname_from_wyd_song045_kinship` 保存傳首全名與有限近系鏈的AI氏姓判讀，不從label或家族ID取姓。明文父子與共享父祖只在家族組裝推論層分開：恢—粹明祖孫、道濟共享祖為有資格推論；亮共享曠之父為弟兄/明父合證，不另造明父斷言。損父鎮之另支，不挪給毅、粹或恢。

`personless_namespace`新增獨立型`explicit_received_brothers_parent_unidentified`。本次僅受固定宋045 received全文與已驗`道養弟道助`斷言、完整原段/MID/反向引用、程道養全名與道助氏名橋守門。兩真節點同代_A/_B，namespace不是人，root/共同父姓名/共同父ID全null，兩人parent_person_id亦null；字母不是長幼。已知lt沿原弟稱保存，不推共同父/母，不准注層、泛從弟、冒稱、反向、異代或缺proof。既有unknown_shared_father_from_qualified_first_cousins分支准入完全保留，新型不借用或放寬舊型條件。普通namespace索引/卡片明示「明文弟兄（父未名）」，不標作兩支堂親編輯接合；traceFamily不載入結構namespace為父親。

`庶長子`另存`source_birth_position.reported_ordinal: 1`（整數，不接受布林）、`source_qualifier: 庶`，`accepted_birth_order`及`scope_interpretation`均null。原文所報序數與被接受的全體/庶子內順位不混；不給懷之/曠之造排序。
