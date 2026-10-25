# 《裴潛傳》phaseB 有限事實契約

既有84槽中83槽逐值保留，pqt049只增補原文有據的end/end_basis；舊68/84封存包不改。追加來源所支持73筆record及兩條共用 `succession_links`。原57項映63筆（多職拆分、一重職合收），7項作品／工程各一筆，另授權黎、康、綽三筆有資格姓氏，原8名已在既存資料不再新增。完整72項研究清單與原始來源角色仍逐項可追；record數不與研究項目數機械對應。

- 姓氏：同源明稱裴楷、兩條明父系至黎／康／綽；原單稱筆保留，`contextual_provisional`，不從family-ID或婚姻、母系、裴凱推姓，不補茂→徽。
- 報齡：8為能屬文時；25為遷黃門侍郎時；48為本來源死亡時。均 `unspecified_source_age`、`birth_year:null`；8不附受辟，無生日、計歲方式推論。
- 姓氏、直接官爵與來源活動仍綁固定全文／角色／有限槽。源稱為、歷、官至等只作attestation，未知任始任終留空；明遷／進／封可記無年的授任事件。p005及p006尚書僕射合收兩用稱，不宣稱中間連任。
- `source_office_prefix_binding`只此p006整組「尚書僕射令光祿大夫」的尚書前綴與令本字，保原attestation「令」；顯示尚書令為有資格形成，不冒連續全銜，不泛作共享後綴。
- `fixed_named_parent_bereavement`以明父茂的原斷言及潛p003「喪父去官」兩端，記茂無年死亡；p006秀「喪父服終」另為服喪報告，不能跨代移用。
- `fixed_peiqian_office_departure`只潛「去官」及秀「爽誅以故吏免」的明示離職動作，父死亡另筆；以實讀事件、固定前職／離職／後職錨只結束潛尚書令與秀本源黄門侍郎；不泛終他職、不覆晉書035同職、不填免官年。
- `fixed_peiqian_recruitment`只曹爽／秀與p006「曹爽辟」，職名、年與受辟齡未知；不冒徵字或假 `lifetime_recruitment_age`。
- `fixed_peiqian_passive_wrongful_killing`只荀綽p007完整源文被枉害，死亡意義是AI上下文判讀；原詞不改，年、地、在任與殺者均不補，不作所有「害」字通則。
- `fixed_parallel_death_era_variant`只同人裴秀之本源秦始七年與晉書035泰始七年／同報48歲的首選271，固定完整兩段、兩MID、原raw SHA及MOE泰始265–274。保秦始原字；非影像校勘、非全域era alias；僅bound life_event接收，反推生日及官爵任期均禁止。
- 建安初、咸熙中、元康末以固定MOE原表作coarse `within_named_era`範圍，保初／中／末。只當筆授爵、用稱或五等制度任務，不灌給此前歷官，不選具體單年。
- 兩承爵只沿曹仁代理共同 `fixed_kanripo_named_father_rank_succession`與實讀reciprocal事件gate，父爵清陽亭侯／鉅鹿公，父子另有明證；原嗣／襲封各保，非承近諡貞侯／元公，未知日期不由父卒補。此包不新增另一承爵dispatcher。
- 開府、假節分作可解析權限報告，監中外營諸軍事為任務；不造開府儀同三司、監軍將軍。未名妻子只集合來源報告，不造人、不算總數、不派生母。
- 配食宗廟為禮制報告，不冒埋葬或虛構廟地。作品／工程保既有work reference與報告動詞、未成資格、地域圖18篇；典治官制不硬當書名，不填撰作日／最早版本，也不稱親見原作品。

`model_plan`和`data_plan`各為有界guarded候選；依賴曹仁共同gate先採。原文、raw、source metadata、MID/span、registry、進度、退休ID不作整份覆回。全庫native CLI/catalog/bundles待根重新交接驗證，稀疏mini不冒全庫資格。

- 明示「改封鉅鹿公」沿共用 `noble_replacement_valid`，廣川侯舊終與鉅鹿公新始同證無年；共用prefix僅有界加入改封，不繞過已知前爵與互鎖。
