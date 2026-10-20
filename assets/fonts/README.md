# 歷史文獻罕字補充字型

`cbr-historical-rare-fallback.woff2` 是 CBR Historical Rare Fallback，獨立依同目錄未改動的 [原版 Arphic Public License](ARPHICPL.TXT) 散布，**不適用專案 MIT 授權**。原作者與授權聲明見 [UPSTREAM-NOTICES.txt](UPSTREAM-NOTICES.txt)。修改版字型可依相同 APL 複製、修改及再散布，不另加限制。

來源為 [BabelStone Han 官方頁](https://www.babelstone.co.uk/Fonts/Han.html) 的 16.0.3 版；只保留七個原碼點及原輪廓，轉為 WOFF2 並改名。原字型與子集的 SHA、版本及碼點列於 [rare-subset-manifest.json](rare-subset-manifest.json)。如何及何時修改的聲明亦保存在字型 name table 中。原作及此修改版均無保證。

目前只涵蓋 `𢎞𤓰𤣥𤼵𦙍𦵏𬒳`，檔案 6,300 bytes；並非全部古籍罕字。CSS 只匹配這七個碼點，普通文字沿用既有字型。原文、姓名、JSON 及 Unicode 碼點不替換，也不以今字代換。官方字形採 G-source 排印慣例，不代表已依原刻本影像校勘。

重建工具與固定依賴見 [tools/rare-font-subset](../../tools/rare-font-subset/README.md)。官方下載網址可能更新；重建工具會拒絕與固定上游 SHA 不符的檔案。
