# 人物來源包與家譜檢視器

以穩定人物 ID 讀取所有已標註的來源材料：

```sh
python3 scripts/person_bundle.py cbr-p004937 --output /tmp/mengtian.json
python3 scripts/person_bundle.py cbr-p000537 --include-provisional --output /tmp/lisi.json
```

預設僅讀指定 ID。`--include-provisional` 明示選用庫內暫定同指的傳遞集合；輸出保留每項判讀、原人物 ID 與證據，不以同名自動合併。暫定同指不表示各來源的世系與年代全部一致。輸出涵蓋目前已標註材料，不能代表尚未整理的全部史料。

`mentions` 提供字元錨點；`passages` 保存正文、篇卷著作 ID；`sources` 提供固定版本與來源網址。`relations` 同時包含以此人為主體或客體的直接主張，`persons` 包含直接相連人物，可作家譜節點；沿相鄰人物 ID 再取來源包即可逐步展開。每條線保留主張 ID、方向、狀態及原文，矛盾主張並列，不自動選成唯一父系。

`title_holdings` 保留每次官爵或尊稱主張的 `effective_period`、用稱錨點及事件類型。檢視器應分別呈現「當時任職確定」「任期未定、此處有用稱」「諡號或回顧用稱」，不能把未知起訖當無限期有效，也不能把初見當授予、把死亡當罷免。來源年月原文保留在 `date_expression`；尚未實作統一曆法換算與按公曆時間篩選，檢視器不得自行把年號字串當可比較日期。

此匯出是可重建的讀取層，權威資料仍是各篇來源與標註。無 AI 或網路處理需求。尚未接入家譜小程式或公開人物頁。

關係 `agnatic_cousin` 保存正文「從兄」「從弟」等同宗從兄弟稱呼，親等未定時 `qualifiers.degree` 為 `unknown`；不能由此補第一代表親、共同祖父或父子線。與 `brother` 相異的來源主張並列，`discrepancy_group_id` 可供檢視器連結分歧；該群組只提示差異，不自動選定其中一說。
