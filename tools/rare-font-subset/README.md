# 重建七字字型子集

此工具保留字形、原碼點、原作者與完整 APL；移除其他字形、轉為 WOFF2、改名並加入修改日期及方式。產物依原版 APL，而非專案 MIT。公開散布時須同時保留 [完整授權](../../assets/fonts/ARPHICPL.TXT)、[原作者聲明](../../assets/fonts/UPSTREAM-NOTICES.txt) 與修改資訊。

在專案根目錄執行下列步驟，工作檔放暫存目錄。只有下載上游與安裝建置依賴需要網路；網站讀者不會連到字型提供者。

```sh
mkdir -p /tmp/cbr-rare-font-build/upstream
cp tools/rare-font-subset/build_subset.py tools/rare-font-subset/chars.json /tmp/cbr-rare-font-build/
curl -L --fail https://www.babelstone.co.uk/Fonts/Download/BabelStoneHan.ttf -o /tmp/cbr-rare-font-build/upstream/BabelStoneHan.ttf
python3 -m pip install --target /tmp/cbr-rare-font-build/python-packages fonttools==4.60.2 brotli==1.2.0
python3 -B /tmp/cbr-rare-font-build/build_subset.py
cmp /tmp/cbr-rare-font-build/cbr-historical-rare-fallback.woff2 assets/fonts/cbr-historical-rare-fallback.woff2
```

固定上游 SHA 為 `d8bb747b3fdccd84a60bd0aa56bb90937270d0bd15f1101cd8f2a5a3709dd0a3`；子集 SHA 為 `d4c99080f4920c459a1e026008e1847e9decffea06a242817fd3342f37ea54a8`。工具會拒絕不同上游內容，不能把同一下載網址的新版本當作同一見證。

擴充碼點時須同時更新清單、CSS unicode-range、字型內修改聲明、版本／SHA 記錄及實際瀏覽器驗收，並保留原 APL。不要提交 51 MB 的上游字型、Python 套件或暫存試驗檔。
