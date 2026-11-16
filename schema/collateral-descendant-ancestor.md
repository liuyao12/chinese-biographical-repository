# 未名兄後裔的上一代祖先：編輯路徑

`ancestor_connection.type = ancestor_above_unnamed_sibling_descendant` 是有限傳世親屬角色配方的衍生，不新增來源父祖斷言。member的 `parent_person_id` 與 `source_assertion_id` 均null；`connection: ancestor`，`generation_distance: 6`，五個null `intermediate_person_ids`。最近已知祖先是reference人物的明父，而非reference本人。reference父系祖父亦必須源證核對，以維持同根結構。

本分支原族系角色為未名older_brother、玄孫四代加之子一代，父系解釋為received_family_context_provisional；五代後裔上溯reference父即六代。來源未名兄person_id須null，不能選其他具名兄弟；原connecting_person_ids/exact_distance均null。所有三條來源斷言同完整fixed-witness配方、父祖共用原段、actual root/raw/projection/每一角色錨點均由既有slot validator驗。用詞及數值限定在這個已覆核配方語義，不以人物ID或章ID白名單通過。

`reference_person_id`、`reference_grandfather_person_id`、`collateral_descendant_assertion_id`、`reference_father_assertion_id`、`reference_grandfather_assertion_id`、三條完整references；`status: contextual_provisional`、`human_reviewed: false`及rationale須明示。母系、收養、義親、僅同母、具名替代、角色倒置、已知另一父、異來源／原文漂移及不一致世代均拒。未知父不產生匿名人物；不得將來源族系報告改為明祖斷言。

現production traceFamily只顯三代，六代ancestor不塞進父／祖／曾祖欄；完整path留在assembled_identity供族系／API處理。部署後需完整重建public輸出，舊人物入口404，不保alias。
