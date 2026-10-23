# 固定 Kanripo 完整單元的有限生平證據

本契約是既有 `fixed_kanripo_person_fact_slots` 的選用附加證據，不變更未具 `finite_biography_proofs` 的舊 recipe 或日期 API。完整原文仍須通過 `fixed_kanripo_projection`、可信章—見證 pin、全文角色 grammar 及各段層次檢查。

`finite_biography_proofs` 指向程式內固定 SHA256 的來源證據檔。其人物角色由固定提及座標解析當前 ID，不按姓名、家族 ID、郡望或書名搜尋人物。逐槽保存原文字位、原段 SHA256、正文或裴注層、來源指稱及語義資格。此批的報齡、姓名與地望各自保其已有資料模型，不另創生年。

省姓判斷為 `contextual_surname_from_fixed_kanripo_slots`。同來源完整姓名為 seed；每一步須逐項符合已固定的來源關係方向與兩端。最多四步，去環，不可經母、配偶、收養關係或僅共享家族 ID；兄弟及從兄的承姓不能反向宣稱已知父名或精確共同祖先。字中的伯仲叔不推絕對排行。

`fixed_kanripo_body_interval_regnal_year` 只處理此已閱完整單元的省年號。證據保完整、有序的正文區間、前置年號錨、事件錨及後置重設年號；注不承正文年號。原詞仍為「四年」，嘉平及252為有資格編輯首選，教育部表僅供年號對照，不作事件身份權威。錯年、錯年號、調換前後錨、跳過新正文年號、換主體、正文與 pin 一致移位均不得通過。中國曆年不換成翌年西曆，無月日則省略。

報齡保原數與語境；注中神異敘事及書信自述另保資格。來源明卒齡需連同人同段死亡來源；生前年齡不能因鄰近卒事件而變享年，所有報齡不反推出生。

地望允許經本附加完整證據驗證的 `contextual_provisional`，而不改其他地址契約。來源任事活動地可用 `service_location` 加 `qualifiers.location_scope=source_attested_task_activity` 及原活動詞；不是虛造官名。徙所卒地須由同主體、同完整正文的遷徙原地稱回指，不能從任官州郡推死亡地，也不自作現代轄區或實葬地。
