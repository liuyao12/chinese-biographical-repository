# 收到傳文的具名承嗣、報齡與奏請

`source_fact_frame` 是可選且失配即拒的來源角色框架。固定 Kanripo 完整單元的 raw、SHA、逐字投影、正文/古注層先由實際 root 讀取驗證；各框架再按原段位、revision、完整段落雜湊、局部句界、人物/引書角色與字段位置逐詞重建。模板不含人物名、人物/篇章ID白名單，也不執行來源文字。

父/祖、承嗣事件、死亡報告、報齡、諡號與官爵各存其既有型別。祖孫不得改父子、不得補中間父親；嗣未重出爵名時承嗣事件 `title:null`、`holding_id:null`。死亡沒有原紀年不得把軍行年填入。報齡以 `during_life` 或同人同源死亡事件 `at_death` 分時點；`年不滿N` 是來源開放上界，`value:null`，不推生年。

`office_nomination` 的機讀值明存奏薦職稱、`appointment_stage:memorial_nomination`、`assumption_attested_by_this_clause:false`。後續持職用稱可另存；司徒府辟召不作司徒持職。

`fief_household_count` 分 `memorial_request` 與 `reported_memorial_submission`，保各自對象、原增數、原總數和原單位；`enactment_status:memorial_report_not_independent_confirmation` 及 `actual_revenue:null` 不作實授或實收。`尸`、`户` 各保原字。

`reported_service_duration` 區分從征、軍旅、與書信作者交往；確數存 `value`，餘數存開放 `lower_exclusive`。`office_tenure:false` 不把服務/交往年數當某官任期，也不由卒年倒算。

姓名的 `contextual_surname_from_received_fact_chain` 只沿同單元明姓種子及最多三條已由上述框架驗證的直接父/祖斷言；不依結構ID、標籤、配偶或組裝推父。祖孫可傳同源姓氏但原未名父仍null。原始人名與字號不因此改寫。
