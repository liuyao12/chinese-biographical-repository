# 固定本紀即位年與本傳三筆官爵

`fixed_kanripo_accession_ce_year` 只允許本傳原官爵起點的同一君主即位事件。原本傳引文、date_expression、受任者及原官名不改；新增normalized_date的數值年、精度year、固定本紀事件及現代年號換算依據。未知任終仍空，不選授官日或首次受任日。

`source_accession_year_binding` 綁holding/person、君主原提及、完整原任用句及來源revision；本紀完整固定原檔、姓名傳首、年號／年數／即位事件依原錨驗。黃初七年即位226與後太和元227分界，禁止錯挪。文帝紀受禪正文庚午與古注辛未原字分層；只定220，不裁日。受禪前古注已稱魏王侍中辛毗，層次差異明記，不宣稱首次入侍日獲解。

原69槽仍逐值驗，本次只三筆start.normalized_date新增；其餘66筆及sister憲英→敞不改。元資料JSON SHA、raw SHA／commit與路徑實體包含關係皆驗，固定本紀可解析原證不是AI即時推論。年份外參只支持黃初220–226年號換算，人物事件證據仍是本紀／本傳。
