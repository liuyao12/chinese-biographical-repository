# 完整固定見證的來源事實槽

`annotation.fixed_witness_fact_slots_ref` 指向受版本控制的 `scripts/fixed_witness_fact_slots.json` 配方。配方先驗完整原生來源單元、固定 revision、實讀原始檔雜湊、全段原詞與逐人角色位置，才按實際人物錨展開已覆核資料。它不是自然語言解析器，亦不接受來源文字作程式。

每筆 runtime 記錄的 `fixed_source_fact_binding` 含 `kind`、配方 `key`、唯一 `slot`。姓名仍經既有姓名／同源姓氏合約；官稱仍保 `title`、`kind`、`mode`、原詞錨與未知端點；生命事件不因其他事件補年。`person_bundle.load_catalog(root)` 與原生直接 CLI 均檢查配方全部槽存在、無重複且與原角色和語義相同。所有來源讀取必須傳實際 root。

本例的「參鎮西鐘會軍事」以 `title_formation.kind=interleaved_commander_reference` 保留分置的參／軍事與長官鐘會；「復職」以 `same_office_reinstatement` 指回前次中護軍，不稱第二次出現原字中護軍。「在職十三年」為獨立 `office_duration`：連至兩次持職而 `episode_assignment` 未定，不生成端點或每任各十三年。戲言各十年是 `hypothetical_office_request`，不記實任。白衣領護軍為權限與身份；正式復職另記。詔賜為命令而非交付或葬事；「先後之親」只存原稱，親等及中介人物未知。

無來源年月、歲數、籍貫與葬地，仍不產生數值。本例不改已有近親斷言、編輯家族組裝、人物 ID 或原始來源字節。

## 固定本傳的原紀年及父系姓氏承接

同一固定見證配方可列 `calendar_references` 與 `date_proofs`。只允許被逐槽列明的 `normalized_date` 位置：原紀年須在指定段落字位；來源數詞、年號、現代年號表原行、首末年與數字換算一致；實際 root 的原HTML須符合已記雜湊及行ID。沒有日期證明的槽仍不可出現數字日期或範圍。生年只允許未知null，不以歲數倒算。

后母後置「邕之女」的主體仍是母親，兩段娶／復納各自有受者；配方全部角色與原句固定，親屬逐槽保存實際主客。`contextual_surname_from_fixed_witness_slots` 只允許同配方明姓種子及已錄直接father斷言的逆向姓氏首選；不調用編輯組裝或preferred父系。原名茞保留，跨本傳道字差異與同指首選另有完整兩端來源。

「追贈…，諡曰…」明示已故受者但未另載卒詞時，可用 `explicit_posthumous_grant_then_naming`：保追贈/命名錨、同一受者及全句，不借下一人物死亡詞造死年。既有明載死亡後命名分支不變。出生、缺代、女兒數與數字官期仍不補。

### 完整固定傳記與平行本紀紀年（羊祜後繼）

`fixed_archived_parallel_year` 綁定完整收到傳記的事實槽、真實受領人／職名／死亡角色，以及另一固定原始見證的完整年度單元。獨立固定 raw SHA、修訂與書目 URL；不能由自填 metadata 重新授權位移後的 raw。`fixed_witness_parallel_primary_ce_year` 在原生 validator 與 exporter 共用契約，檢查實際 bound record、端點角色與 date path，不能整塊挪用別人的合法日期。五等建置、即位、具名同職除授、同句連授及具名死亡各有有限分支；新年界限不可跳過。版本只證數位見證，非刊本或影像校勘。

本批保留未知持職起終；死亡年不自動終止任何職任，未就／不許辭／拒爵／詔稱／復本封分別保存。右僕射未知始年與本紀左僕射268年分開存，尚不假定同一除授或互斥異文。洛陽卒地是兩段連續病中敘事的 `contextual_provisional`，並非原文明載「卒於洛陽」。十二與五十八只存來源報齡；預言、五歲再生故事與墓地徵兆是來源敘事，不反推生年。賜葬地不等於已完成葬地。原37親屬／家族報告不改。
