# 宋063首批有限資料與編輯顯示

本源以具名階段 `fixed_wyd063_basic_facts` 綁完整已收武英殿選錄與各資料集。既有原文／NER／反向及投影守衛保留；只在此前提驗確定近親、單名原值與有資格姓氏、籍貫、元嘉七年卒及太保弘用稱。省年號沿既有 `relative_ce_regnal_era_span`、`omitted_era_regnal_year` 算術；額外固定死亡scope區分主敘元嘉四年與啟語回述二年，原表述仍七年。

`cross_chapter_same_person_source_variant` 是明示的編輯姓名讀法，不合併人物。它要求兩種實存 `ming`、至少兩篇、每個現役record的完整唯一locator（可為合法legacy `id:null`）、完整段及精確同canonical人物MID，且列盡該人目前兩種拼法的全部record。首選值只能取其中之一；限定 `listed_records_only`，不對未列第三字形生效。原 `same_paragraph_mixed_name_spellings` 分支的單字／同段規則不變。

`profile_title_preference_set` 沿已審的來源holding＋attestation契約：每canonical唯一明示選擇、`timeless_profile_heading`、`temporal_claim:none`、AI暫定。稱號必為同人已驗holding的原值；未就proposal、錯人、任意拼名、無見證語法、爭議用稱不能偷渡。來源用稱可用 `mode:attestation`，不假造grant或任期。此例太保由宋063太保弘的固定角色證明；日期始終仍未知。

每次 `load_catalog` 建不可變 `PreferenceCatalog` 交易索引，無跨root／跨載入全域快取；普通複本不帶索引，選擇時完整重驗。已選記錄與明列來源檔閉包變更即拒。無偏好不新增欄位、既有標頭fallback及順位不變；有偏好才穿透bundle、table profile與一般人物卡／頁，常顯來源用稱／追贈等mode及編輯選稱，保原names.title資料。沒有runtime AI或最高官推斷。
