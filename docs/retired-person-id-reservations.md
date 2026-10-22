# 已知退休人物 ID 的保留

`retired_person_ids(root)` 只回傳禁止重新登記的ID集合，不作alias、redirect或舊新查詢。讀取路徑限於 `source-evidence/*/annotation-chain.json`，且只消費 `editorial_annotation_rekey_receipt`。

namespace型須有合法根 `namespace_id`、`historical_rekey_mapping` 與 `mapping_role=audit_only_not_alias_or_current_person_endpoint`；只取mapping鍵，目的ID必屬該namespace。family型須有合法非空 `family_id`、不重複的 `retired_person_ids` 與 `retirement_policy=audit_only_not_canonical_not_alias_not_reusable`。兩型皆須 `person_aliases_created=false`。未知、混合或格式錯的同型收據拒絕；其他record_type忽略。審查狀態或human_reviewed不能放行。

分配器新增keyword-only `root`，如 `allocate_child_id(parent, existing, root=root)`。明示root才取得該工作樹的退休保留，並拒絕退休分支的上下前綴重配。未傳root的舊API保留，不能宣稱所有外部導入者已受保護；導入者亦可呼叫 `assert_not_retired(person_id, root)`。原生validator拒退休ID作canonical或id_aliases；consolidate保留集加入退休集合，並將收據帶入暫存驗證目錄。

恢復後目前僅核實周namespace的15個退休ID。王祥8人改號收據已隨暫存環境遺失，目前不存在；不重建其史料或冒稱已納入。未來合規family收據會自動消費，無人物或家族白名單。已刪5556別名的完整Git歷史未盤點，故不宣稱覆蓋全部歷史；整份收據若遭刪除，單靠當前檔案無法察覺，須由版本審核保護。
