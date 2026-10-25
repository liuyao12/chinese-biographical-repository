# 有資格的外部編年推繫

biographical_source_detail_set 新 kind compiler_chronological_placement：由可信固定見證契約驗證。placement.year 為數值，精度year、中國曆年、原紀年與 received_compiler_editorial_placement / preferred_provisional / human_reviewed:false 必填。linked_life_event_id 連同人、已驗且日期未知死亡事件。timeline_use 必填 required_qualification / must_display_qualification:true / replace_source_event_date:false / birth_year_inference_permitted:false。不得改原事件日期、倒算出生或挪作授爵任期。

外證含固定URL、revision、完整raw SHA、完整相關敘事、年題、死亡事件及完整考證引文；層次、位置與未圖校資格分存。trusted pin 修改屬程式審查邊界，不可由來源傳 regex。官方年號表hash/列與原數字必須算得同一年。

load_catalog 於載入交易驗新型細節，個人bundle只驗自身該型，不每人掃全庫、不跨root快取。原primary/date_decision契約不變。profile沿source_details原值輸出；compilerChronologyPlacements(person) 回傳有資格時間軸資料，不改直接死亡年scalar。full頁呈現年數、原紀年、暫定首選、考異及外鏈；compact生命摘要保持。
