# 固定完整傳記姓名構件

沿用 `person_name_component_set`。`fixed_biography_name_binding` 將原段 SHA／固定 revision、人物稱名錨、緊接的「字」與同人字名錨、同人「一名」兩端綁定。模式為原全名、原省名、氏稱、角色未名、姓＋后稱或公／王侯爵稱＋稱名；不把爵稱、公旦之公或字充作姓／本名。推姓全名不宣稱原文逐字明載；未知名為 null。

`additional_name_components` 保存一名的 value/kind/source_marker、兩端原錨及 `chronology=unspecified`；`additional_names` 只作相應可讀顯示。不是 former_ming、改名日期或全庫preferred。不同收到字形（如本源裴顗）仍原字記錄，不裁其他來源的頠。

`contextual_surname_from_fixed_biography_family` 只同一完整固定單元的明全名／氏稱種子，以及已驗父、兄弟、明父系祖／曾祖、從子／從孫／從曾孫原文陳述。最多五步，逐步校from/to、世代差、去環／去重；每邊重驗原句與角色。從親只攜帶有資格姓氏，不生成中間父、父系組裝或絕對排行。不走母、配偶、承嗣／收養、母系旁親、未知世距或編者assembly；不讀ID字母、label、郡望推姓。

`source_name_usage` 分存同人生家外孫稱用及承嗣家稱用、原提及與既有承嗣陳述。change_year 為 null、preferred 為 false；不是互斥異說或改姓時點。現有source-scoped preferred僅處理特定ming字形，不能套用兩姓。本包不新增全庫姓氏預設；顯示共識保兩姓而不按第一筆選一姓。
