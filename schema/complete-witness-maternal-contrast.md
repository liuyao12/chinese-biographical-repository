# 完整見證的母稱對舉與有界細節

`fixed_witness_person_fact_slots` 仍先驗受信完整raw、開閉題界、每段原字、全部人物角色/同指分組及各段source_layer，再產生經review的精確語義槽；record不能提供regexp或改任意角色。ID從穩定MID動態追current，沒有個人ID白名單。

`maternal_context_proofs` 可選 `principal_mother_contrast`，舊proof不帶此欄者語義不變。此欄綁同一完整段的孩子、兩次母稱、明『嫡母某氏』及後文同氏稱；要求母/嫡母/孩子三人不同、兩組各自同指、原位對舉錨與完整段quote。母的birth interpretation只能contextual_preferred/source_explicit_birth=false；嫡母對端必為maternal_role/principal_mother，biological_mother與father_person_id null，不可冒後母/繼母或配偶。這是reviewed完整來源的有資格首選，不是任何母字自動推生母。

非相鄰的 `fixed_complete_witness_role_evidence` 僅在同一完整role-recipe已驗證時成立；須如實列原序的各證據段，前客體、後主體在完整引句可見，不冒相鄰，也不造source father句。一般跨段規則保持原限制。

侯國地望 `fief_kind=complete_witness_marquis_state_locality` 只允許完整受信record且原有『為侯國』；不是普通fief語法放寬，不當出生地/居地。保持原地稱、不現代定位。

`fixed_calendar_era_phase_range` 同時驗固定官方calendar raw row、來源年號初中末原位及既有civil_era_ranges全契約；保整年號最寬界，不選元年、不補月日或所有職期。舊exact-date/parallel分支不放寬。quoted-preface角色仍必在既有完整容器及received_quoted_document層，僅收到引序的見證，不冒獨立史書/原著。
