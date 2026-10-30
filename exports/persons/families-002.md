# 人物 JSON 索引

可重建匯出，涵蓋目前已標註資料，包含明示選用的暫定跨篇同指；原 ID、證據與判讀均保留。並非全部史料或完整覆核。

程式可讀取 [index.json](index.json)，再依各筆 `path` 取得人物資料。重新產生：`python3 scripts/export_person_bundles.py`。

出生排行與籍貫結構化欄位仍在逐篇回填；缺欄位不代表來源沒有此資訊。提及頻次依固定見證的獨立位置計算；原始錨點完整保留，同位置節引重出另列raw／duplicate與對應群組，不代表來源權威度。

已接合父系見 [家族組裝資料](../../registry/family-assemblies.json)。`assembled_identity.person_id` 是共用家族根的組裝 ID，`source_person_ids` 保留各篇候選；父子及同指證據可由記錄 ID 回查。缺代節點另有 `ancestor_person_id`、`generation_distance` 與空值中間世代；父親空值不表示它另成一族。

點選家族標題可展開或收起後代。`*` 表示缺名世代，不建立人物，也不表示不同缺名位置是同一人。表內只列家族根後的 ID 尾碼；根人物以「根」表示，完整 ID 保留於家族標題及 JSON。最多提及來源另列一欄，同數並列；提及次數不代表史料優先權。已完成格式遷移的舊 ID 與 JSON 入口已撤除；待身份覆核的來源候選仍分存。

尚未連入同族的人物見 [獨立人物索引](unconnected.md)。

## 可展開家族


[第1頁](README.md) · [第2頁](families-002.md)

<details><summary><code>yqp_nlb_p1p</code> 太公（漢王父稱）（125 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 太公（漢王父稱） | [《史記・高祖本紀》][108] | [JSON](yqp_nlb_p1p.json) |
| `A` | 高祖 | [《史記・高祖本紀》][108] | [JSON](yqp_nlb_p1p_A.json) |
| `AA` | 孝惠（本卷稱呼） | [《史記・呂后本紀》][109] | [JSON](yqp_nlb_p1p_AA.json) |
| `AB` | 劉肥 | [《史記・齊悼惠王世家》][134] | [JSON](yqp_nlb_p1p_AB.json) |
| `ABA` | 齊哀王（本卷未名） | [《史記・齊悼惠王世家》][134] | [JSON](yqp_nlb_p1p_ABA.json) |
| `ABB` | 卬（膠西王） | [《史記・吳王濞列傳》][188] | [JSON](yqp_nlb_p1p_ABB.json) |
| `ABBA` | 膠西王太子德 | [《史記・吳王濞列傳》][188] | [JSON](yqp_nlb_p1p_ABBA.json) |
| `ABC` | 興居（齊悼惠王子） | [《史記・齊悼惠王世家》][134] | [JSON](yqp_nlb_p1p_ABC.json) |
| `ABD` | 辟光（濟南王） | [《史記・齊悼惠王世家》][134] | [JSON](yqp_nlb_p1p_ABD.json) |
| `ABE` | 雄渠（膠東王） | [《史記・齊悼惠王世家》][134]、[《史記・吳王濞列傳》][188] | [JSON](yqp_nlb_p1p_ABE.json) |
| `ABF` | 章（城陽景王） | [《史記・齊悼惠王世家》][134] | [JSON](yqp_nlb_p1p_ABF.json) |
| `ABFA` | 喜（城陽共王） | [《史記・齊悼惠王世家》][134]、[《史記・漢興以來諸侯王年表》][261] | [JSON](yqp_nlb_p1p_ABFA.json) |
| `ABFAA` | 延校勘建未定 | [《史記・齊悼惠王世家》][134] | [JSON](yqp_nlb_p1p_ABFAA.json) |
| `ABFAAA` | 義 | [《史記・齊悼惠王世家》][134] | [JSON](yqp_nlb_p1p_ABFAAA.json) |
| `ABFAAAA` | 武城陽惠王 | [《史記・齊悼惠王世家》][134] | [JSON](yqp_nlb_p1p_ABFAAAA.json) |
| `ABFAAAAA` | 順 | [《史記・齊悼惠王世家》][134] | [JSON](yqp_nlb_p1p_ABFAAAAA.json) |
| `ABFAAAAAA` | 恢城陽戴王 | [《史記・齊悼惠王世家》][134] | [JSON](yqp_nlb_p1p_ABFAAAAAA.json) |
| `ABFAAAAAAA` | 景城陽末王 | [《史記・齊悼惠王世家》][134] | [JSON](yqp_nlb_p1p_ABFAAAAAAA.json) |
| `ABFAB` | 劉福 | [《史記・東越列傳》][196]、[《史記・建元以來侯者年表》][264]、[《史記・建元已來王子侯者年表》][265] | [JSON](yqp_nlb_p1p_ABFAB.json) |
| `ABFAC` | 劉齒 | [《史記・建元已來王子侯者年表》][265] | [JSON](yqp_nlb_p1p_ABFAC.json) |
| `ABG` | 賢（菑川王） | [《史記・齊悼惠王世家》][134]、[《史記・吳王濞列傳》][188] | [JSON](yqp_nlb_p1p_ABG.json) |
| `ABH` | 志（濟北王，後王菑川） | [《史記・齊悼惠王世家》][134] | [JSON](yqp_nlb_p1p_ABH.json) |
| `ABHA` | 建菑川靖王 | [《史記・齊悼惠王世家》][134] | [JSON](yqp_nlb_p1p_ABHA.json) |
| `ABHAA` | 遺 | [《史記・齊悼惠王世家》][134] | [JSON](yqp_nlb_p1p_ABHAA.json) |
| `ABHAAA` | 終古 | [《史記・齊悼惠王世家》][134] | [JSON](yqp_nlb_p1p_ABHAAA.json) |
| `ABHAAAA` | 尚菑川孝王 | [《史記・齊悼惠王世家》][134] | [JSON](yqp_nlb_p1p_ABHAAAA.json) |
| `ABHAAAAA` | 橫 | [《史記・齊悼惠王世家》][134] | [JSON](yqp_nlb_p1p_ABHAAAAA.json) |
| `ABI` | 齊孝王將閭 | [《史記・齊悼惠王世家》][134] | [JSON](yqp_nlb_p1p_ABI.json) |
| `AC` | 恒（高祖子） | [《史記・孝文本紀》][110] | [JSON](yqp_nlb_p1p_AC.json) |
| `ACA` | 孝景帝 | [《史記・梁孝王世家》][140] | [JSON](yqp_nlb_p1p_ACA.json) |
| `ACAA` | 孝武皇帝 | [《史記・孝武本紀》][112] | [JSON](yqp_nlb_p1p_ACAA.json) |
| `ACAAA` | 閎（齊王） | [《史記・三王世家》][142] | [JSON](yqp_nlb_p1p_ACAAA.json) |
| `ACAAB` | 旦 | [《史記・三王世家》][142] | [JSON](yqp_nlb_p1p_ACAAB.json) |
| `ACAABA` | 安定侯子 | [《史記・三王世家》][142] | [JSON](yqp_nlb_p1p_ACAABA.json) |
| `ACAABB` | 建 | [《史記・三王世家》][142] | [JSON](yqp_nlb_p1p_ACAABB.json) |
| `ACAAC` | 胥 | [《史記・三王世家》][142] | [JSON](yqp_nlb_p1p_ACAAC.json) |
| `ACAACA` | 朝陽侯子 | [《史記・三王世家》][142] | [JSON](yqp_nlb_p1p_ACAACA.json) |
| `ACAACB` | 平曲侯子 | [《史記・三王世家》][142] | [JSON](yqp_nlb_p1p_ACAACB.json) |
| `ACAACC` | 南利侯子 | [《史記・三王世家》][142] | [JSON](yqp_nlb_p1p_ACAACC.json) |
| `ACAACD` | 弘 | [《史記・三王世家》][142] | [JSON](yqp_nlb_p1p_ACAACD.json) |
| `ACAAD` | 據 | [《史記・田叔列傳》][186] | [JSON](yqp_nlb_p1p_ACAAD.json) |
| `ACAAE` | 昭帝 | [《史記・三王世家》][142] | [JSON](yqp_nlb_p1p_ACAAE.json) |
| `ACAAF` | 昌邑哀王髆 | [《漢書・武五子傳》][12] | [JSON](yqp_nlb_p1p_ACAAF.json) |
| `ACAAFA` | 賀（海昬侯） | [《漢書・武五子傳》][12] | [JSON](yqp_nlb_p1p_ACAAFA.json) |
| `ACAB` | 德 | [《史記・五宗世家》][141] | [JSON](yqp_nlb_p1p_ACAB.json) |
| `ACABA` | 不害 | [《史記・五宗世家》][141] | [JSON](yqp_nlb_p1p_ACABA.json) |
| `ACABAA` | 基 | [《史記・五宗世家》][141] | [JSON](yqp_nlb_p1p_ACABAA.json) |
| `ACABAAA` | 授 | [《史記・五宗世家》][141]、[《史記・漢興以來諸侯王年表》][261] | [JSON](yqp_nlb_p1p_ACABAAA.json) |
| `ACAC` | 閼于 | [《史記・五宗世家》][141] | [JSON](yqp_nlb_p1p_ACAC.json) |
| `ACAD` | 發 | [《史記・五宗世家》][141] | [JSON](yqp_nlb_p1p_ACAD.json) |
| `ACADA` | 庸 | [《史記・五宗世家》][141]、[《史記・漢興以來諸侯王年表》][261] | [JSON](yqp_nlb_p1p_ACADA.json) |
| `ACADAA` | 鮒鮈 | [《史記・五宗世家》][141] | [JSON](yqp_nlb_p1p_ACADAA.json) |
| `ACAE` | 乘 | [《史記・五宗世家》][141] | [JSON](yqp_nlb_p1p_ACAE.json) |
| `ACAF` | 趙王彭祖 | [《史記・五宗世家》][141] | [JSON](yqp_nlb_p1p_ACAF.json) |
| `ACAG` | 舜（景帝子） | [《史記・五宗世家》][141] | [JSON](yqp_nlb_p1p_ACAG.json) |
| `ACAGA` | 棁 | [《史記・五宗世家》][141] | [JSON](yqp_nlb_p1p_ACAGA.json) |
| `ACAGB` | 平 | [《史記・五宗世家》][141] | [JSON](yqp_nlb_p1p_ACAGB.json) |
| `ACAGC` | 商 | [《史記・五宗世家》][141] | [JSON](yqp_nlb_p1p_ACAGC.json) |
| `ACAGCA` | 安世 | [《史記・五宗世家》][141] | [JSON](yqp_nlb_p1p_ACAGCA.json) |
| `ACAH` | 栗太子（本卷未名） | [《史記・五宗世家》][141] | [JSON](yqp_nlb_p1p_ACAH.json) |
| `ACAI` | 勝（景帝子） | [《史記・五宗世家》][141] | [JSON](yqp_nlb_p1p_ACAI.json) |
| `ACAIA` | 昌 | [《史記・五宗世家》][141]、[《史記・漢興以來諸侯王年表》][261] | [JSON](yqp_nlb_p1p_ACAIA.json) |
| `ACAIAA` | 昆侈 | [《史記・五宗世家》][141] | [JSON](yqp_nlb_p1p_ACAIAA.json) |
| `ACAJ` | 越（景帝子） | [《史記・五宗世家》][141] | [JSON](yqp_nlb_p1p_ACAJ.json) |
| `ACAJA` | 齊 | [《史記・五宗世家》][141] | [JSON](yqp_nlb_p1p_ACAJA.json) |
| `ACAK` | 非（汝南王） | [《史記・五宗世家》][141] | [JSON](yqp_nlb_p1p_ACAK.json) |
| `ACAKA` | 建 | [《史記・五宗世家》][141] | [JSON](yqp_nlb_p1p_ACAKA.json) |
| `ACAL` | 餘（淮陽王） | [《史記・田叔列傳》][186] | [JSON](yqp_nlb_p1p_ACAL.json) |
| `ACALA` | 光 | [《史記・五宗世家》][141] | [JSON](yqp_nlb_p1p_ACALA.json) |
| `ACAM` | 寄（景帝子） | [《史記・五宗世家》][141] | [JSON](yqp_nlb_p1p_ACAM.json) |
| `ACAMA` | 賢 | [《史記・五宗世家》][141] | [JSON](yqp_nlb_p1p_ACAMA.json) |
| `ACAMAA` | 膠東慶 | [《史記・五宗世家》][141] | [JSON](yqp_nlb_p1p_ACAMAA.json) |
| `ACAMB` | 六安慶 | [《史記・五宗世家》][141] | [JSON](yqp_nlb_p1p_ACAMB.json) |
| `ACAN` | 端 | [《史記・五宗世家》][141] | [JSON](yqp_nlb_p1p_ACAN.json) |
| `ACB` | 梁懷王 | [《史記・屈原賈生列傳》][166] | [JSON](yqp_nlb_p1p_ACB.json) |
| `ACC` | 參 | [《史記・梁孝王世家》][140] | [JSON](yqp_nlb_p1p_ACC.json) |
| `ACCA` | 登 | [《史記・梁孝王世家》][140] | [JSON](yqp_nlb_p1p_ACCA.json) |
| `ACCAA` | 義 | [《史記・梁孝王世家》][140] | [JSON](yqp_nlb_p1p_ACCAA.json) |
| `ACD` | 勝 | [《史記・梁孝王世家》][140] | [JSON](yqp_nlb_p1p_ACD.json) |
| `ACE` | 孝文帝女公主 | [《史記・絳侯周勃世家》][139] | [JSON](yqp_nlb_p1p_ACE.json) |
| `ACF` | 嫖（長公主） | [《史記・外戚世家》][131] | [JSON](yqp_nlb_p1p_ACF.json) |
| `ACG` | 梁孝王武 | [《史記・梁孝王世家》][140] | [JSON](yqp_nlb_p1p_ACG.json) |
| `ACGA` | 買 | [《史記・梁孝王世家》][140] | [JSON](yqp_nlb_p1p_ACGA.json) |
| `ACGAA` | 襄 | [《史記・梁孝王世家》][140] | [JSON](yqp_nlb_p1p_ACGAA.json) |
| `ACGAAA` | 無傷 | [《史記・梁孝王世家》][140] | [JSON](yqp_nlb_p1p_ACGAAA.json) |
| `ACGB` | 明 | [《史記・梁孝王世家》][140] | [JSON](yqp_nlb_p1p_ACGB.json) |
| `ACGC` | 彭離 | [《史記・梁孝王世家》][140] | [JSON](yqp_nlb_p1p_ACGC.json) |
| `ACGD` | 定 | [《史記・梁孝王世家》][140] | [JSON](yqp_nlb_p1p_ACGD.json) |
| `ACGE` | 不識 | [《史記・梁孝王世家》][140] | [JSON](yqp_nlb_p1p_ACGE.json) |
| `AD` | 恢（高祖子） | [《史記・呂后本紀》][109] | [JSON](yqp_nlb_p1p_AD.json) |
| `AE` | 友（高祖子） | [《史記・呂后本紀》][109] | [JSON](yqp_nlb_p1p_AE.json) |
| `AEA` | 遂（趙幽王子） | [《史記・楚元王世家》][132] | [JSON](yqp_nlb_p1p_AEA.json) |
| `AEB` | 辟彊（趙幽王子） | [《史記・孝文本紀》][110]、[《史記・楚元王世家》][132]、[《史記・漢興以來諸侯王年表》][261] | [JSON](yqp_nlb_p1p_AEB.json) |
| `AEBA` | 福 | [《史記・楚元王世家》][132]、[《史記・漢興以來諸侯王年表》][261] | [JSON](yqp_nlb_p1p_AEBA.json) |
| `AF` | 長（高祖子） | [《史記・淮南衡山列傳》][200] | [JSON](yqp_nlb_p1p_AF.json) |
| `AFA` | 淮南王安 | [《史記・淮南衡山列傳》][200] | [JSON](yqp_nlb_p1p_AFA.json) |
| `AFAA` | 陵（淮南王女） | [《史記・淮南衡山列傳》][200] | [JSON](yqp_nlb_p1p_AFAA.json) |
| `AFAB` | 不害 | [《史記・淮南衡山列傳》][200] | [JSON](yqp_nlb_p1p_AFAB.json) |
| `AFABA` | 建（不害子） | [《史記・淮南衡山列傳》][200] | [JSON](yqp_nlb_p1p_AFABA.json) |
| `AFAC` | 淮南太子遷 | [《史記・淮南衡山列傳》][200] | [JSON](yqp_nlb_p1p_AFAC.json) |
| `AFB` | 濟北王勃 | [《史記・淮南衡山列傳》][200] | [JSON](yqp_nlb_p1p_AFB.json) |
| `AFC` | 衡山王賜 | [《史記・淮南衡山列傳》][200] | [JSON](yqp_nlb_p1p_AFC.json) |
| `AFCA` | 爽（衡山太子） | [《史記・淮南衡山列傳》][200] | [JSON](yqp_nlb_p1p_AFCA.json) |
| `AFCB` | 孝（衡山王子） | [《史記・淮南衡山列傳》][200] | [JSON](yqp_nlb_p1p_AFCB.json) |
| `AFCC` | 無采 | [《史記・淮南衡山列傳》][200] | [JSON](yqp_nlb_p1p_AFCC.json) |
| `AFD` | 東城侯良 | [《史記・淮南衡山列傳》][200]、[《史記・惠景間侯者年表》][263] | [JSON](yqp_nlb_p1p_AFD.json) |
| `AG` | 建（高祖子） | [《史記・高祖本紀》][108]、[《史記・呂后本紀》][109]、[《史記・漢興以來諸侯王年表》][261] | [JSON](yqp_nlb_p1p_AG.json) |
| `AH` | 如意（高祖子） | [《史記・呂后本紀》][109] | [JSON](yqp_nlb_p1p_AH.json) |
| `AI` | 魯元（本卷稱呼） | [《史記・呂后本紀》][109] | [JSON](yqp_nlb_p1p_AI.json) |
| `B` | 伯 | [《史記・楚元王世家》][132] | [JSON](yqp_nlb_p1p_B.json) |
| `BA` | 信羹頡侯 | [《史記・楚元王世家》][132] | [JSON](yqp_nlb_p1p_BA.json) |
| `C` | 仲 | [《史記・高祖本紀》][108]、[《史記・吳王濞列傳》][188] | [JSON](yqp_nlb_p1p_C.json) |
| `CA` | 劉濞 | [《史記・吳王濞列傳》][188] | [JSON](yqp_nlb_p1p_CA.json) |
| `CAA` | 吳太子被殺未名 | [《漢書・荊燕吳傳》][8]、[《史記・吳王濞列傳》][188] | [JSON](yqp_nlb_p1p_CAA.json) |
| `CAB` | 吳王少子未名 | [《漢書・荊燕吳傳》][8]、[《史記・吳王濞列傳》][188] | [JSON](yqp_nlb_p1p_CAB.json) |
| `CAD` | 子華 | [《史記・吳王濞列傳》][188] | [JSON](yqp_nlb_p1p_CAD.json) |
| `CAE` | 駒（吳王太子；《史記》作子駒） | [《漢書・荊燕吳傳》][8]、[《史記・吳王濞列傳》][188] | [JSON](yqp_nlb_p1p_CAE.json) |
| `D` | 劉交 | [《史記・楚元王世家》][132] | [JSON](yqp_nlb_p1p_D.json) |
| `DA` | 藝（楚元王子） | [《史記・孝景本紀》][111] | [JSON](yqp_nlb_p1p_DA.json) |
| `DB` | 禮（楚元王子） | [《史記・楚元王世家》][132] | [JSON](yqp_nlb_p1p_DB.json) |
| `DBA` | 道 | [《史記・楚元王世家》][132] | [JSON](yqp_nlb_p1p_DBA.json) |
| `DBAA` | 注 | [《史記・楚元王世家》][132] | [JSON](yqp_nlb_p1p_DBAA.json) |
| `DBAAA` | 純 | [《史記・楚元王世家》][132] | [JSON](yqp_nlb_p1p_DBAAA.json) |
| `DC` | 郢 | [《史記・儒林列傳》][203] | [JSON](yqp_nlb_p1p_DC.json) |
| `DCA` | 戊（楚王） | [《史記・吳王濞列傳》][188] | [JSON](yqp_nlb_p1p_DCA.json) |

</details>

<details><summary><code>z0l_1wp_de1</code> 趙破奴（匈奴列傳第44段）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 趙破奴（匈奴列傳第44段） | [《史記・匈奴列傳》][192] | [JSON](z0l_1wp_de1.json) |
| `A` | 安國（趙破奴子） | [《史記・衛將軍驃騎列傳》][193] | [JSON](z0l_1wp_de1_A.json) |

</details>

<details><summary><code>z8l_wje_08d</code> 卜商（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 卜商 | [《史記・仲尼弟子列傳》][149] | [JSON](z8l_wje_08d.json) |
| `A` | 卜商之子 | [《史記・仲尼弟子列傳》][149] | [JSON](z8l_wje_08d_A.json) |

</details>

<details><summary><code>z9d_qn5_wg8</code> 路人（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 路人 | [《史記・朝鮮列傳》][197] | [JSON](z9d_qn5_wg8.json) |
| `A` | 最 | [《史記・建元以來侯者年表》][264] | [JSON](z9d_qn5_wg8_A.json) |

</details>

<details><summary><code>zan_qcc_jy5</code> 陳文公（田世家候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 陳文公 | [《史記・田敬仲完世家》][128] | [JSON](zan_qcc_jy5.json) |
| `A` | 陳厲公他 | [《史記・田敬仲完世家》][128] | [JSON](zan_qcc_jy5_A.json) |

</details>

<details><summary><code>zk0_g6b_nbq</code> 伍奢（楚篇候選）（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 伍奢 | [《史記・楚世家》][122] | [JSON](zk0_g6b_nbq.json) |
| `A` | 伍尚 | [《史記・楚世家》][122] | [JSON](zk0_g6b_nbq_A.json) |
| `B` | 伍胥 | [《史記・楚世家》][122] | [JSON](zk0_g6b_nbq_B.json) |

</details>

<details><summary><code>zql_k3t_8ro</code> 先軫（重耳五士）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 先軫（重耳五士） | [《史記・晉世家》][121] | [JSON](zql_k3t_8ro.json) |
| `A` | 先縠（右行將） | [《史記・晉世家》][121] | [JSON](zql_k3t_8ro_A.json) |

</details>

<details><summary><code>zrx_2ip_d1p</code> 張負（陳丞相世家候選）（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 張負 | [《史記・陳丞相世家》][138] | [JSON](zrx_2ip_d1p.json) |
| `*A` | 張氏女 | [《史記・陳丞相世家》][138] | [JSON](zrx_2ip_d1p_%2AA.json) |
| `A` | 張仲 | [《史記・陳丞相世家》][138] | [JSON](zrx_2ip_d1p_A.json) |

</details>

<details><summary><code>zwr_jel_e3l</code> 齊宣公（田世家候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 齊宣公 | [《史記・田敬仲完世家》][128] | [JSON](zwr_jel_e3l.json) |
| `A` | 康公貸 | [《史記・田敬仲完世家》][128] | [JSON](zwr_jel_e3l_A.json) |

</details>

[8]: https://zh.wikisource.org/w/index.php?title=漢書/卷035&oldid=2605377
[12]: https://github.com/kanripo/KR2a0007/blob/683113d4baf6febecaf2ccb7913df87c4d68d454/KR2a0007_063.txt
[108]: https://zh.wikisource.org/w/index.php?title=史記/卷008&oldid=2440965
[109]: https://zh.wikisource.org/w/index.php?title=史記/卷009&oldid=2087062
[110]: https://zh.wikisource.org/w/index.php?title=史記/卷010&oldid=2599229
[111]: https://zh.wikisource.org/w/index.php?title=史記/卷011&oldid=2520527
[112]: https://zh.wikisource.org/w/index.php?title=史記/卷012&oldid=8733061
[121]: https://zh.wikisource.org/w/index.php?title=史記/卷039&oldid=2588534
[122]: https://zh.wikisource.org/w/index.php?title=史記/卷040&oldid=8736796
[128]: https://zh.wikisource.org/w/index.php?title=史記/卷046&oldid=2560838
[131]: https://zh.wikisource.org/w/index.php?title=史記/卷049&oldid=7903610
[132]: https://zh.wikisource.org/w/index.php?title=史記/卷050&oldid=8737728
[134]: https://zh.wikisource.org/w/index.php?title=史記/卷052&oldid=5977113
[138]: https://zh.wikisource.org/w/index.php?title=史記/卷056&oldid=1961615
[139]: https://zh.wikisource.org/w/index.php?title=史記/卷057&oldid=1569360
[140]: https://zh.wikisource.org/w/index.php?title=史記/卷058&oldid=8735555
[141]: https://zh.wikisource.org/w/index.php?title=史記/卷059&oldid=2621125
[142]: https://zh.wikisource.org/w/index.php?title=史記/卷060&oldid=7909290
[149]: https://zh.wikisource.org/w/index.php?title=史記/卷067&oldid=7869003
[166]: https://zh.wikisource.org/w/index.php?title=史記/卷084&oldid=1568305
[186]: https://zh.wikisource.org/w/index.php?title=史記/卷104&oldid=8739534
[188]: https://zh.wikisource.org/w/index.php?title=史記/卷106&oldid=405869
[192]: https://zh.wikisource.org/w/index.php?title=史記/卷110&oldid=8735645
[193]: https://zh.wikisource.org/w/index.php?title=史記/卷111&oldid=8730225
[196]: https://zh.wikisource.org/w/index.php?title=史記/卷114&oldid=8735633
[197]: https://zh.wikisource.org/w/index.php?title=史記/卷115&oldid=439220
[200]: https://zh.wikisource.org/w/index.php?title=史記/卷118&oldid=7904122
[203]: https://zh.wikisource.org/w/index.php?title=史記/卷121&oldid=8735621
[261]: https://zh.wikisource.org/w/index.php?title=史記/卷017&oldid=2607010
[263]: https://zh.wikisource.org/w/index.php?title=史記/卷019&oldid=6359260
[264]: https://zh.wikisource.org/w/index.php?title=史記/卷020&oldid=2607036
[265]: https://zh.wikisource.org/w/index.php?title=史記/卷021&oldid=2607037
