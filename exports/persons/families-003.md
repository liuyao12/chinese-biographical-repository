# 人物 JSON 索引

可重建匯出，涵蓋目前已標註資料，包含明示選用的暫定跨篇同指；原 ID、證據與判讀均保留。並非全部史料或完整覆核。

程式可讀取 [index.json](index.json)，再依各筆 `path` 取得人物資料。重新產生：`python3 scripts/export_person_bundles.py`。

出生排行與籍貫結構化欄位仍在逐篇回填；缺欄位不代表來源沒有此資訊。提及頻次依固定見證的獨立位置計算；原始錨點完整保留，同位置節引重出另列raw／duplicate與對應群組，不代表來源權威度。

已接合父系見 [家族組裝資料](../../registry/family-assemblies.json)。`assembled_identity.person_id` 是共用家族根的組裝 ID，`source_person_ids` 保留各篇候選；父子及同指證據可由記錄 ID 回查。缺代節點另有 `ancestor_person_id`、`generation_distance` 與空值中間世代；父親空值不表示它另成一族。

點選家族標題可展開或收起後代。`*` 表示缺名世代，不建立人物，也不表示不同缺名位置是同一人。表內只列家族根後的 ID 尾碼；根人物以「根」表示，完整 ID 保留於家族標題及 JSON。最多提及來源另列一欄，同數並列；提及次數不代表史料優先權。已完成格式遷移的舊 ID 與 JSON 入口已撤除；待身份覆核的來源候選仍分存。

尚未連入同族的人物見 [獨立人物索引](unconnected.md)。

## 可展開家族


[第1頁](README.md) · [第2頁](families-002.md) · [第3頁](families-003.md)

<details><summary><code>zwr_jel_e3l</code> 齊宣公（田世家候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 齊宣公 | [《史記・田敬仲完世家》][1176] | [JSON](zwr_jel_e3l.json) |
| `A` | 康公貸 | [《史記・田敬仲完世家》][1176] | [JSON](zwr_jel_e3l_A.json) |

</details>

<details><summary><code>zyu_yrx_2pz</code> 宇文述（宇文化及父）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 宇文述（宇文化及父） | [《隋書・列傳第50 序言 宇文化及 王充》][1593] | [JSON](zyu_yrx_2pz.json) |
| `A` | 宇文化及（宇文述子） | [《陳書・皇后》][29]、[《隋書・列傳第50 序言 宇文化及 王充》][1593] | [JSON](zyu_yrx_2pz_A.json) |

</details>

<details><summary><code>zz1_0tr_xni</code> 夏侯詳（字叔業，夏侯亶父）（7 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 夏侯詳（字叔業，夏侯亶父） | [《梁書・裴邃 兄子之高 之平 之橫 夏侯亶 弟夔 魚弘附 韋放》][441] | [JSON](zz1_0tr_xni.json) |
| `A` | 夏侯亶（字世龍，夏侯詳長子） | [《梁書・裴邃 兄子之高 之平 之橫 夏侯亶 弟夔 魚弘附 韋放》][441] | [JSON](zz1_0tr_xni_A.json) |
| `AA` | 夏侯誼（夏侯亶子，襲豐城公） | [《梁書・裴邃 兄子之高 之平 之橫 夏侯亶 弟夔 魚弘附 韋放》][441] | [JSON](zz1_0tr_xni_AA.json) |
| `AB` | 夏侯損（夏侯誼弟） | [《梁書・裴邃 兄子之高 之平 之橫 夏侯亶 弟夔 魚弘附 韋放》][441] | [JSON](zz1_0tr_xni_AB.json) |
| `B` | 夏侯夔（字季龍，夏侯亶弟） | [《梁書・裴邃 兄子之高 之平 之橫 夏侯亶 弟夔 魚弘附 韋放》][442] | [JSON](zz1_0tr_xni_B.json) |
| `BA` | 夏侯撰（夏侯夔子，太僕卿） | [《梁書・裴邃 兄子之高 之平 之橫 夏侯亶 弟夔 魚弘附 韋放》][442] | [JSON](zz1_0tr_xni_BA.json) |
| `BB` | 夏侯譒（夏侯撰弟） | [《梁書・裴邃 兄子之高 之平 之橫 夏侯亶 弟夔 魚弘附 韋放》][442] | [JSON](zz1_0tr_xni_BB.json) |

</details>

[29]: https://zh.wikisource.org/w/index.php?oldid=2015446
[441]: https://zh.wikisource.org/w/index.php?oldid=1511902
[442]: https://zh.wikisource.org/w/index.php?oldid=1511902
[1176]: https://zh.wikisource.org/w/index.php?title=史記/卷046&oldid=2560838
[1593]: https://zh.wikisource.org/w/index.php?oldid=2180348
