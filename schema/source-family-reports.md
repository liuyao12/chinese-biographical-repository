# 逐字親屬句與來源子數

`qualifiers.literal_source_binding` 分開傳首明父、具名子列表、及子列表、父有若干子而具名者最小、孫嗣後重述父之子列表、具名曾孫六種語法。每筆綁完整來源段、來源revision與逐字raw projection、雙端角色、局部句界。正文與裴注來源層均保原層；其來源聲稱不等於獨立核定世系。名單順序不當出生排行，無名中間父代保持null。

`annotation.family_count_reports` 的 `count_scope: sons_of_parent` 表來源報告兒子數，不是所有子女數。`reported_count` 來自 `source_number`；父名、數詞與已具名最小兒子均有位置。`named_member_person_ids` 是來源中實際具名子集，`complete_named_list:false`，不建立其餘無名人物。另項父子斷言的 `birth_order.position:youngest`、`ordinal:null` 保來源最小，不把總數計算結果冒成原文明載排行。人物bundle按parent_person_id匯出 `family_count_reports`，不塞到孩子的個人報齡。

`literal_source_binding` 於死亡事件綁原紀年與死亡原詞，分具名主語、推舉他人後君主仍確認傳主、依附他人及被召而未赴三種角色語法。不以最近的人名當死者；時間只從原死亡紀年正規化，不當官職始終。既有 `age_context:during_life` 保存幼時而孤報齡，不改卒齡、不推生年。


## 固定標點傳記的親屬角色框架

`received_family_frame.kind = punctuated_received_family_frame` 將完整原段、固定 revision/SHA、有限句法、每一角色的實際 mention 字位與關係方向綁定。中央驗證另重投影完整固定見證；不能只用同段某人作 recipient。保留既有所有親屬契約。

`kinship_basis = bound_collateral_generation_term` 用 `kinship_unspecified` 保存從子／從孫／從曾孫的父系晚一／二／三代，以及從舅的母系上一代。主體為較晚一代者，客體為先輩；`generation_difference` 分別為 -1/-2/-3。`exact_distance`、`common_ancestor_person_id`、`connecting_person_ids` 皆 null；不得改成直接父邊、確定共同祖先或指定唯一母系連接路徑。無 `adopted_for_family_tree`；runtime 不由此生成直系。

`adoption_basis = named_external_grandson_posthumous_heir` 僅具名外孫爲具名死者子之明文；`adoptive_father` 與生父／生母、另立 `ritual_successor_of` 分存。`actual_upbringing`、`modern_legal_status` 均 not_inferred，不把奉後當生育或已實際養育。單獨嗣爵不適用。

前妻生二女的同一完整句，父親判讀用 `interpretation_basis = marital_biographical_birth_context`，`explicit_biological_paternity = false` 表示未逐字明稱生父，並非斷言非生父；妻、生二女、兩組一名、父親及後娶妻父皆須精確綁角色。前妻不自動新增離婚日期。兄弟只保存相對序及原詞；協同列項另存 interpretation_basis，不補絕對排行、同母或父名。

母字不機械轉生母：只有母稱且出生角色未明時用 `maternal_role`、`role=mother_unspecified`，`biological_mother`／`father_person_id` 為 null。`mother` 另保 `birth_mother_interpretation`；「生二女」標 explicit_birth_verb，傳首具名父母與同段婚配或明「某女」之判讀為 contextual_provisional，不能冒稱有生育動詞。這是個別完整語境編輯首選，不是所有母稱的通用生母推斷器。
