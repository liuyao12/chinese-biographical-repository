# 逐字親屬句與來源子數

`qualifiers.literal_source_binding` 分開傳首明父、具名子列表、及子列表、父有若干子而具名者最小、孫嗣後重述父之子列表、具名曾孫六種語法。每筆綁完整來源段、來源revision與逐字raw projection、雙端角色、局部句界。正文與裴注來源層均保原層；其來源聲稱不等於獨立核定世系。名單順序不當出生排行，無名中間父代保持null。

`annotation.family_count_reports` 的 `count_scope: sons_of_parent` 表來源報告兒子數，不是所有子女數。`reported_count` 來自 `source_number`；父名、數詞與已具名最小兒子均有位置。`named_member_person_ids` 是來源中實際具名子集，`complete_named_list:false`，不建立其餘無名人物。另項父子斷言的 `birth_order.position:youngest`、`ordinal:null` 保來源最小，不把總數計算結果冒成原文明載排行。人物bundle按parent_person_id匯出 `family_count_reports`，不塞到孩子的個人報齡。

`literal_source_binding` 於死亡事件綁原紀年與死亡原詞，分具名主語、推舉他人後君主仍確認傳主、依附他人及被召而未赴三種角色語法。不以最近的人名當死者；時間只從原死亡紀年正規化，不當官職始終。既有 `age_context:during_life` 保存幼時而孤報齡，不改卒齡、不推生年。
