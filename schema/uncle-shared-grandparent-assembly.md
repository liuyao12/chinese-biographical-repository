# 伯叔之父：具名姪父及祖的編輯組裝

`parent_connection.type = parent_from_nephew_named_father_and_grandfather` 僅在同一固定完整傳記已有三條經驗證來源斷言時使用：同一人的父、父系祖、父系伯父或叔父。來源父與祖須共用同段完整引文；伯叔可出現在同一完整本傳的後段，但必須由該完整來源配方驗明主語與角色。不可據近鄰詞猜主語或混不同作品親屬。

欄位：`nephew_person_id`、`nephew_father_person_id`、`paternal_uncle_assertion_id`、`nephew_father_assertion_id`、`nephew_grandfather_assertion_id`；另有 `status: contextual_provisional`、`human_reviewed: false`、`rationale`、各斷言完整原文 `references`。組裝member的 `source_assertion_id` 必須null；不得另造伯叔之父的source斷言。來源伯叔需父系、距一代及原長幼；母舅、泛從弟、養父/義親不得套用。

所有來源透過actual root讀固定完整raw/projection、原角色與typed配方。member、姪、姪父、祖四端互異；姪之明父與祖一致，若伯叔或姪父另有矛盾父證即拒。此方向不同於 `ancestor_through_paternal_uncle` 的缺父姪→叔父明父推祖，兩者不可互套。

閱讀器僅把帶此完整組裝證據的邊呈為 `assembly_inferred`，保原文及可撤回資格；不以此推生母、出生年或絕對排行。

`interpretation_basis: fixed_complete_witness_shared_father` 的兄弟同父及鏈式接合沿既有欄位，但每一步必須由完整fixed witness或位置綁定received_family_frame驗證actual root/raw；明確`same_mother_only`、母系lineage或`shared_father:false`均拒。`shared_mother:true`本身不產生父證；相同父的本傳脈絡首選仍明列編輯資格。
