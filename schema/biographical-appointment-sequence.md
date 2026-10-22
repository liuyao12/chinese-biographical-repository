# 本傳官序與受任者續述

`source_role_sequence`保存完整局部語法框架、逐字scope_anchor、已標人物的role/mid、原位title/date/place/number fields、原版修訂及段落hash。受任者由同一biography_subject首名與具名／續述角色鏈確認，不以同段出現或最近人名判定。每個人物slot有字位；府主官名可嵌於屬官全題，須屬先述任用者；同人官名指代與別人官名不可混。完整原文及XML不改。

`source_role_slot`決定該稱號的原字位及授任／轉任／兼領／歷任／續領語法。`appointment_role`細分`recruitment`、`appointment`、`transfer`、`concurrent`、`previously_held`、`enfeoffment`、`advancement`、`military_command`、`official_duty`、`continued_official_duty`、`military_authorization`、`institutional_privilege`、`posthumous_name`。後兩授權／特權暫用既有coarse kind honorific，不能作普通本官或封爵處理；錄尚書事為職務，不稱獨立爵。授任記載不額外聲稱實際赴任已獨立證實；柘令不行只有unassumed notice。

`source_time_scope`只存原時序表述，年份不明時normalized_start_year/end_year均null。及即王位、及踐阼、明帝即位、頃之是不同節點，不把明帝即位冒作太和元年。不以卒年截止官爵。青龍四年明卒可依獨立年號表換年，月份、日期、生年、卒齡未載不補。司空前後雖在本傳續述，未有卒官字樣，不能新增卒官斷言。

`source_role_year_bridge`可為個別官序節點補上已覆讀外證：`kind: reviewed_archived_role_event`綁定持職記錄、本人、君主具名先行錨、原段雜湊、固定修訂與外部帝紀事件。外證保存本庫相對路徑、完整原文雜湊、版面投影規則、年題與事件字位；年號表只提供年號對應，不作任官史料。精確年寫入`effective_period.start.normalized_date`，兩界範圍寫入`normalized_date_range`，不能同時存在。範圍的上界可為已持有的時間，不冒稱當年始授；`source_time_scope.normalized_start_year`仍為null。

即位子句的日期只給該角色，後續轉任、加官、開府與續錄尚書事不自動承年。另有帝紀具名任命可獨立補該職年份；不得把即位日搬成授官日。跨篇橋不生成未曾匯入的整篇正文，外證與原生來源範圍分別記錄。所有任職終期仍按各自原證，不由卒年填補。驗證入口為`scripts/role_event_year_bridge.py`，原有無日期官序驗證保持適用。

`shared_title_suffix`只為收到三地名共享令字的展開，保存component_anchor、suffix_anchor、編者首選資格、原序及次要分詞參考。title是展開顯示值，attestation.surface保收到的地名字串；兩端逐字驗證，既有相等規則僅在本契約通過時例外。原文不添字。除蕭贊長平令依源次序分錄三職，unknown年；父卒去官只繫最後長平令的explicit_end，不一齊截止三職。

`biographical_source_detail_set`的本契約三種：official_duty（共同受遺詔輔政）、office_departure（父卒去官）、fief_household_count（增邑與合計的原數/數值，實收收入null）。保source_term/source_anchor和同一角色鏈，府主／同受命者／嗣者不得移成受任者；明細不生成親屬、稱號或生母。

驗證只套已記錄語法，不做NLU。範圍外句式另研究，不退回全段人物白名單。引用受領者、嵌入引語、紀年與其他角色不可跨越；既有其他型別仍走原契約。所有判讀human_reviewed false，原圖未核維持未核。來源reader、single-person bundle／profile以既有生卒／稱號／source_details路徑讀取，無需NLU。
