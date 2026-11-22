# 人物 JSON 索引

可重建匯出，涵蓋目前已標註資料，包含明示選用的暫定跨篇同指；原 ID、證據與判讀均保留。並非全部史料或完整覆核。

程式可讀取 [index.json](index.json)，再依各筆 `path` 取得人物資料。重新產生：`python3 scripts/export_person_bundles.py`。

出生排行與籍貫結構化欄位仍在逐篇回填；缺欄位不代表來源沒有此資訊。提及頻次依固定見證的獨立位置計算；原始錨點完整保留，同位置節引重出另列raw／duplicate與對應群組，不代表來源權威度。

已接合父系見 [家族組裝資料](../../registry/family-assemblies.json)。`assembled_identity.person_id` 是共用家族根的組裝 ID，`source_person_ids` 保留各篇候選；父子及同指證據可由記錄 ID 回查。缺代節點另有 `ancestor_person_id`、`generation_distance` 與空值中間世代；父親空值不表示它另成一族。

點選家族標題可展開或收起後代。`*` 表示缺名世代，不建立人物，也不表示不同缺名位置是同一人。表內只列家族根後的 ID 尾碼；根人物以「根」表示，完整 ID 保留於家族標題及 JSON。最多提及來源另列一欄，同數並列；提及次數不代表史料優先權。已完成格式遷移的舊 ID 與 JSON 入口已撤除；待身份覆核的來源候選仍分存。

尚未連入同族的人物見 [獨立人物索引](unconnected.md)。

## 可展開家族


[第1頁](README.md) · [第2頁](families-002.md)

<details><summary><code>03n_n2r_8rt</code> 阮裕（韜玄祖）（9 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 阮裕（韜玄祖） | [《晉書・阮籍 嵇康 向秀 劉伶 謝鯤 胡毋輔之 畢卓 王尼 羊曼 光逸》][190]、[《晉書・王羲之》][251] | [JSON](03n_n2r_8rt.json) |
| `***A` | 阮韜 | [《南史・王裕之　王鎮之　王韶之　王悅之　王准之》][677]、[《南史・王裕之　王鎮之　王韶之　王悅之　王准之》][676] | [JSON](03n_n2r_8rt_%2A%2A%2AA.json) |
| `A` | 阮傭 | [《晉書・阮籍 嵇康 向秀 劉伶 謝鯤 胡毋輔之 畢卓 王尼 羊曼 光逸》][190] | [JSON](03n_n2r_8rt_A.json) |
| `AA` | 阮歆之 | [《晉書・阮籍 嵇康 向秀 劉伶 謝鯤 胡毋輔之 畢卓 王尼 羊曼 光逸》][190] | [JSON](03n_n2r_8rt_AA.json) |
| `AAA` | 阮彌之 | [《晉書・阮籍 嵇康 向秀 劉伶 謝鯤 胡毋輔之 畢卓 王尼 羊曼 光逸》][190] | [JSON](03n_n2r_8rt_AAA.json) |
| `B` | 阮寧（阮萬齡父） | [《晉書・阮籍 嵇康 向秀 劉伶 謝鯤 胡毋輔之 畢卓 王尼 羊曼 光逸》][190] | [JSON](03n_n2r_8rt_B.json) |
| `BA` | 阮腆 | [《晉書・阮籍 嵇康 向秀 劉伶 謝鯤 胡毋輔之 畢卓 王尼 羊曼 光逸》][190] | [JSON](03n_n2r_8rt_BA.json) |
| `BB` | 阮萬齡 | [《南史・王裕之　王鎮之　王韶之　王悅之　王准之》][659]、[《宋書・隱逸》][1133]、[《宋書・隱逸》][1132] | [JSON](03n_n2r_8rt_BB.json) |
| `C` | 阮普 | [《晉書・阮籍 嵇康 向秀 劉伶 謝鯤 胡毋輔之 畢卓 王尼 羊曼 光逸》][190] | [JSON](03n_n2r_8rt_C.json) |

</details>

<details><summary><code>04u_gq0_nke</code> 鼂錯父未名（袁盎鼂錯列傳候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 鼂錯父未名 | [《史記・袁盎鼂錯列傳》][892] | [JSON](04u_gq0_nke.json) |
| `A` | 鼂錯 | [《史記・袁盎鼂錯列傳》][892] | [JSON](04u_gq0_nke_A.json) |

</details>

<details><summary><code>069_dn8_o4r</code> 江遵（江祏祖）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 江遵（江祏祖） | [《南史・荀伯玉　崔祖思　蘇侃　虞悰　胡諧之　虞玩之　劉休　江祏》][710] | [JSON](069_dn8_o4r.json) |
| `A` | 江氏（齊景皇后，蕭鸞母） | [《南史・荀伯玉　崔祖思　蘇侃　虞悰　胡諧之　虞玩之　劉休　江祏》][710] | [JSON](069_dn8_o4r_A.json) |

</details>

<details><summary><code>06i_k5v_922</code> 申侯（鄭世家武姜父候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 申侯 | [《史記・鄭世家》][833] | [JSON](06i_k5v_922.json) |
| `A` | 武姜 | [《史記・鄭世家》][833] | [JSON](06i_k5v_922_A.json) |

</details>

<details><summary><code>076_097_db5</code> 張闓（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 張闓 | [《晉書・王舒 王廙 虞潭 顧眾 張闓》][246] | [JSON](076_097_db5.json) |
| `A` | 張混 | [《晉書・王舒 王廙 虞潭 顧眾 張闓》][246] | [JSON](076_097_db5_A.json) |

</details>

<details><summary><code>0ad_dbw_97q</code> 晉昭公（4 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 晉昭公 | [《史記・晉世家》][830] | [JSON](0ad_dbw_97q.json) |
| `A` | 雍（戴子晉昭公子） | [《史記・晉世家》][830] | [JSON](0ad_dbw_97q_A.json) |
| `AA` | 忌（戴子子） | [《史記・晉世家》][830] | [JSON](0ad_dbw_97q_AA.json) |
| `AAA` | 驕（晉哀公） | [《史記・晉世家》][830] | [JSON](0ad_dbw_97q_AAA.json) |

</details>

<details><summary><code>0bu_skv_qsr</code> 呂青（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 呂青 | [《史記・項羽本紀》][815]、[《史記・高祖本紀》][816] | [JSON](0bu_skv_qsr.json) |
| `A` | 呂臣 | [《史記・項羽本紀》][815]、[《史記・高祖本紀》][816] | [JSON](0bu_skv_qsr_A.json) |

</details>

<details><summary><code>0c1_b9d_9c2</code> 楊彪（7 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 楊彪 | [《後漢書・孝獻帝紀》][74] | [JSON](0c1_b9d_9c2.json) |
| `A` | 楊脩 | [《三國志・任城陳蕭王傳》][748] | [JSON](0c1_b9d_9c2_A.json) |
| `AA` | 楊囂 | [《三國志・任城陳蕭王傳》][748] | [JSON](0c1_b9d_9c2_AA.json) |
| `AAA` | 楊準 | [《三國志・任城陳蕭王傳》][748] | [JSON](0c1_b9d_9c2_AAA.json) |
| `AAAA` | 楊嶠 | [《三國志・任城陳蕭王傳》][748] | [JSON](0c1_b9d_9c2_AAAA.json) |
| `AAAB` | 楊髦 | [《三國志・任城陳蕭王傳》][748] | [JSON](0c1_b9d_9c2_AAAB.json) |
| `AAAC` | 楊俊 | [《三國志・任城陳蕭王傳》][748] | [JSON](0c1_b9d_9c2_AAAC.json) |

</details>

<details><summary><code>0db_22c_332</code> 何進（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 何進 | [《後漢書・荀韓鍾陳列傳》][76] | [JSON](0db_22c_332.json) |
| `*A` | 何晏 | [《三國志・諸夏侯曹傳》][734] | [JSON](0db_22c_332_%2AA.json) |
| `*AA` | 晏未名男 | [《三國志・諸夏侯曹傳》][734] | [JSON](0db_22c_332_%2AAA.json) |

</details>

<details><summary><code>0ej_lsn_fpk</code> 路道慶（路瓊之父）（4 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 路道慶（路瓊之父） | [《南史・后妃上》][534]、[《宋書・后妃》][1015] | [JSON](0ej_lsn_fpk.json) |
| `A` | 路休之（路瓊之弟） | [《宋書・后妃》][1015] | [JSON](0ej_lsn_fpk_A.json) |
| `B` | 路茂之（路瓊之弟） | [《宋書・后妃》][1015] | [JSON](0ej_lsn_fpk_B.json) |
| `C` | 路氏（宋前廢帝皇后，道慶女） | [《宋書・前廢帝》][1005] | [JSON](0ej_lsn_fpk_C.json) |

</details>

<details><summary><code>0hs_fg6_1qj</code> 田榮（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 田榮 | [《史記・田儋列傳》][885] | [JSON](0hs_fg6_1qj.json) |
| `A` | 廣（田榮子） | [《史記・酈生陸賈列傳》][888] | [JSON](0hs_fg6_1qj_A.json) |
| `B` | 田廣 | [《史記・田儋列傳》][885] | [JSON](0hs_fg6_1qj_B.json) |

</details>

<details><summary><code>0lf_ggf_5xo</code> 張弘策（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 張弘策 | [《南史・謝晦　謝裕　謝方明　謝靈運》][590] | [JSON](0lf_ggf_5xo.json) |
| `A` | 張緬（字元長） | [《梁書・張緬 弟纘 綰》][365] | [JSON](0lf_ggf_5xo_A.json) |

</details>

<details><summary><code>0s7_r72_j8q</code> 魯武公（4 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 魯武公 | [《史記・魯周公世家》][824] | [JSON](0s7_r72_j8q.json) |
| `A` | 括（魯武公長子） | [《史記・魯周公世家》][824] | [JSON](0s7_r72_j8q_A.json) |
| `AA` | 伯御（魯君） | [《史記・魯周公世家》][824] | [JSON](0s7_r72_j8q_AA.json) |
| `B` | 戲（魯懿公） | [《史記・魯周公世家》][824] | [JSON](0s7_r72_j8q_B.json) |

</details>

<details><summary><code>0us_j8h_to7</code> 假（老韓列傳候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 假 | [《史記・老子韓非列傳》][854] | [JSON](0us_j8h_to7.json) |
| `A` | 解 | [《史記・老子韓非列傳》][854] | [JSON](0us_j8h_to7_A.json) |

</details>

<details><summary><code>0va_s3x_wb4</code> 蕭統（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 蕭統 | [《梁書・昭明太子 哀太子 愍懷太子》][320]、[《南史・王曇首》][629]、[《南史・王曇首》][628] | [JSON](0va_s3x_wb4.json) |
| `A` | 蕭譽（梁河東王） | [《陳書・列傳第十一: 王沖 王通 袁敬》][30] | [JSON](0va_s3x_wb4_A.json) |

</details>

<details><summary><code>0xt_iyn_d3t</code> 趙夙（趙世家候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 趙夙 | [《史記・趙世家》][834] | [JSON](0xt_iyn_d3t.json) |
| `A` | 共孟 | [《史記・趙世家》][834] | [JSON](0xt_iyn_d3t_A.json) |

</details>

<details><summary><code>0zd_9uz_t7m</code> 臧汪（5 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 臧汪 | [《南史・后妃上》][553] | [JSON](0zd_9uz_t7m.json) |
| `A` | 臧儁 | [《南史・后妃上》][550]、[《南史・后妃上》][552]、[《南史・后妃上》][553]、[《宋書・后妃》][1021] | [JSON](0zd_9uz_t7m_A.json) |
| `AA` | 臧愛親 | [《南史・后妃上》][553]、[《南史・范泰　荀伯子　徐廣　鄭鮮之　裴松之　何承天》][696]、[《宋書・鄭鮮之 裴松之 何承天》][1074] | [JSON](0zd_9uz_t7m_AA.json) |
| `AB` | 臧熹（字義和） | [《宋書・臧質 魯爽 沈攸之》][1086] | [JSON](0zd_9uz_t7m_AB.json) |
| `ABA` | 臧質（字含文） | [《宋書・臧質 魯爽 沈攸之》][1086]、[《宋書・朱脩之 宗愨 王玄謨》][1089]、[《宋書・良吏》][1122] | [JSON](0zd_9uz_t7m_ABA.json) |

</details>

<details><summary><code>113_odk_emq</code> 衞綰（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 衞綰 | [《史記・萬石張叔列傳》][894] | [JSON](113_odk_emq.json) |
| `A` | 信（衞綰子） | [《史記・萬石張叔列傳》][894] | [JSON](113_odk_emq_A.json) |

</details>

<details><summary><code>128_4ab_z34</code> 熊延（楚君）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 熊延（楚君） | [《史記・楚世家》][831] | [JSON](128_4ab_z34.json) |
| `A` | 熊勇（楚君） | [《史記・楚世家》][831] | [JSON](128_4ab_z34_A.json) |

</details>

<details><summary><code>12u_910_czm</code> 潘詞（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 潘詞 | [《宋書・良吏》][1129] | [JSON](12u_910_czm.json) |
| `A` | 潘亮〔潘詞子〕 | [《宋書・良吏》][1129] | [JSON](12u_910_czm_A.json) |

</details>

<details><summary><code>16c_0og_lvl</code> 沈叔仁（沈攸之父）（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 沈叔仁（沈攸之父） | [《宋書・臧質 魯爽 沈攸之》][1084]、[《宋書・臧質 魯爽 沈攸之》][1085] | [JSON](16c_0og_lvl.json) |
| `A` | 沈攸之（字仲達） | [《南齊書・王奐 從弟繢 張沖》][497]、[《南史・王誕　王華　王惠　王彧》][640]、[《宋書・臧質 魯爽 沈攸之》][1084]、[《宋書・臧質 魯爽 沈攸之》][1085] | [JSON](16c_0og_lvl_A.json) |
| `AA` | 沈文和（攸之第三子） | [《南史・沈慶之　宗愨》][701] | [JSON](16c_0og_lvl_AA.json) |

</details>

<details><summary><code>16y_k92_fmm</code> 張敦〔字叔方〕（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 張敦〔字叔方〕 | [《三國志・張顧諸葛步傳》][775] | [JSON](16y_k92_fmm.json) |
| `A` | 張純〔吳太子輔義都尉，字元基〕 | [《三國志・吳主五子傳》][805] | [JSON](16y_k92_fmm_A.json) |

</details>

<details><summary><code>175_99c_b41</code> 柔（王沈祖）（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 柔（王沈祖） | [《三國志・徐胡二王傳》][754] | [JSON](175_99c_b41.json) |
| `A` | 機（王沈父） | [《晉書・王沈 荀顗 荀勖 馮紞》][158] | [JSON](175_99c_b41_A.json) |
| `AA` | 王沈 | [《晉書・王沈 荀顗 荀勖 馮紞》][158] | [JSON](175_99c_b41_AA.json) |

</details>

<details><summary><code>1a3_b0c_e6d</code> 謝沖（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 謝沖 | [《南史・謝晦　謝裕　謝方明　謝靈運》][578] | [JSON](1a3_b0c_e6d.json) |
| `A` | 謝明慧 | [《晉書・謝尚 謝安》][250] | [JSON](1a3_b0c_e6d_A.json) |

</details>

<details><summary><code>1ay_9qe_u4h</code> 荀馗（5 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 荀馗 | [《晉書・王湛 荀崧 范汪 劉惔 張憑 韓伯》][235] | [JSON](1ay_9qe_u4h.json) |
| `A` | 荀序 | [《晉書・王沈 荀顗 荀勖 馮紞》][158]、[《晉書・王湛 荀崧 范汪 劉惔 張憑 韓伯》][235] | [JSON](1ay_9qe_u4h_A.json) |
| `AA` | 恆（荀序子） | [《晉書・王沈 荀顗 荀勖 馮紞》][158] | [JSON](1ay_9qe_u4h_AA.json) |
| `AAA` | 龍符（恆子） | [《晉書・王沈 荀顗 荀勖 馮紞》][158] | [JSON](1ay_9qe_u4h_AAA.json) |
| `B` | 荀廞 | [《晉書・王湛 荀崧 范汪 劉惔 張憑 韓伯》][235] | [JSON](1ay_9qe_u4h_B.json) |

</details>

<details><summary><code>1b1_d4d_bb8</code> 謝鐵（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 謝鐵 | [《南史・謝晦　謝裕　謝方明　謝靈運》][578] | [JSON](1b1_d4d_bb8.json) |
| `A` | 謝邈 | [《晉書・謝尚 謝安》][250] | [JSON](1b1_d4d_bb8_A.json) |

</details>

<details><summary><code>1b7_36b_29b</code> 徐邈（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 徐邈 | [《晉書・王導》][212]、[《晉書・王羲之》][251]、[《宋書・良吏》][1128] | [JSON](1b7_36b_29b.json) |
| `A` | 徐豁（字萬同，徐邈子） | [《宋書・良吏》][1128] | [JSON](1b7_36b_29b_A.json) |

</details>

<details><summary><code>1dq_vh2_eru</code> 張華（7 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 張華 | [《晉書・忠義》][257] | [JSON](1dq_vh2_eru.json) |
| `*****A` | 張穆之（字思靜） | [《梁書・皇后》][317] | [JSON](1dq_vh2_eru_%2A%2A%2A%2A%2AA.json) |
| `*****AA` | 張尚柔（梁太祖獻皇后） | [《梁書・皇后》][317]、[《南史・后妃下》][561]、[《南史・后妃下》][562] | [JSON](1dq_vh2_eru_%2A%2A%2A%2A%2AAA.json) |
| `*****AB` | 張弘籍（字真藝） | [《南史・后妃下》][562] | [JSON](1dq_vh2_eru_%2A%2A%2A%2A%2AAB.json) |
| `A` | 張禕（張華子，字彥仲） | [《晉書・衞瓘 張華》][155] | [JSON](1dq_vh2_eru_A.json) |
| `AA` | 張輿（字公安） | [《晉書・衞瓘 張華》][155] | [JSON](1dq_vh2_eru_AA.json) |
| `B` | 張韙（張華子） | [《晉書・衞瓘 張華》][155] | [JSON](1dq_vh2_eru_B.json) |

</details>

<details><summary><code>1ec_i30_u8n</code> 溫恭〔濟南太守〕（6 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 溫恭〔濟南太守〕 | [《新唐書・宰相世系二中》][1189] | [JSON](1ec_i30_u8n.json) |
| `A` | 溫羨 | [《晉書・鄭袤 李胤 盧欽 華表 石鑒 溫羨》][185] | [JSON](1ec_i30_u8n_A.json) |
| `AA` | 溫允〔溫羨子〕 | [《晉書・鄭袤 李胤 盧欽 華表 石鑒 溫羨》][176]、[《晉書・鄭袤 李胤 盧欽 華表 石鑒 溫羨》][185] | [JSON](1ec_i30_u8n_AA.json) |
| `AB` | 溫祗 | [《晉書・鄭袤 李胤 盧欽 華表 石鑒 溫羨》][185] | [JSON](1ec_i30_u8n_AB.json) |
| `AC` | 溫裕〔字敬嗣〕 | [《晉書・鄭袤 李胤 盧欽 華表 石鑒 溫羨》][185] | [JSON](1ec_i30_u8n_AC.json) |
| `B` | 溫襜〔本傳憺〕 | [《新唐書・宰相世系二中》][1189] | [JSON](1ec_i30_u8n_B.json) |

</details>

<details><summary><code>1ex_se1_yef</code> 張湯父（未名）（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 張湯父（未名） | [《漢書・張湯傳》][68]、[《史記・酷吏列傳》][913] | [JSON](1ex_se1_yef.json) |
| `A` | 張湯 | [《史記・酷吏列傳》][913] | [JSON](1ex_se1_yef_A.json) |
| `AA` | 張安世 | [《漢書・張湯傳》][68] | [JSON](1ex_se1_yef_AA.json) |

</details>

<details><summary><code>1g3_02y_oor</code> 太公望（5 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 太公望 | [《史記・齊太公世家》][823] | [JSON](1g3_02y_oor.json) |
| `A` | 丁公呂伋 | [《史記・齊太公世家》][823] | [JSON](1g3_02y_oor_A.json) |
| `AA` | 得（齊乙公） | [《史記・齊太公世家》][823] | [JSON](1g3_02y_oor_AA.json) |
| `AAA` | 慈母（齊癸公） | [《史記・齊太公世家》][823] | [JSON](1g3_02y_oor_AAA.json) |
| `AAAA` | 不辰（齊哀公） | [《史記・齊太公世家》][823] | [JSON](1g3_02y_oor_AAAA.json) |

</details>

<details><summary><code>1h3_vs7_t8h</code> 齊湣王（燕篇）（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 齊湣王（燕篇） | [《史記・燕召公世家》][825] | [JSON](1h3_vs7_t8h.json) |
| `A` | 襄王（齊湣王子） | [《史記・田敬仲完世家》][837] | [JSON](1h3_vs7_t8h_A.json) |
| `AA` | 齊王建 | [《史記・田敬仲完世家》][837] | [JSON](1h3_vs7_t8h_AA.json) |

</details>

<details><summary><code>1hf_1k0_bnj</code> 夷仲年（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 夷仲年 | [《史記・齊太公世家》][823]、[《史記・十二諸侯年表》][1223] | [JSON](1hf_1k0_bnj.json) |
| `A` | 公孫無知 | [《史記・齊太公世家》][823] | [JSON](1hf_1k0_bnj_A.json) |

</details>

<details><summary><code>1kj_vhc_cx9</code> 上官桀（三王世家候選）（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 上官桀 | [《漢書・昭帝紀》][64] | [JSON](1kj_vhc_cx9.json) |
| `A` | 上官安 | [《漢書・昭帝紀》][64] | [JSON](1kj_vhc_cx9_A.json) |
| `AA` | 上官氏（孝昭皇后） | [《漢書・昭帝紀》][64] | [JSON](1kj_vhc_cx9_AA.json) |

</details>

<details><summary><code>1l4_2pq_e7w</code> 熊通（楚武王候選）（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 熊通 | [《史記・楚世家》][831] | [JSON](1l4_2pq_e7w.json) |
| `A` | 熊貲（楚文王） | [《史記・楚世家》][831] | [JSON](1l4_2pq_e7w_A.json) |
| `AA` | 熊艱（莊敖） | [《史記・楚世家》][831] | [JSON](1l4_2pq_e7w_AA.json) |

</details>

<details><summary><code>1pc_mnq_z0c</code> 懿公（燕文公後）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 懿公（燕文公後） | [《史記・燕召公世家》][825] | [JSON](1pc_mnq_z0c.json) |
| `A` | 惠公（燕懿公子） | [《史記・燕召公世家》][825] | [JSON](1pc_mnq_z0c_A.json) |

</details>

<details><summary><code>1tc_q18_x7v</code> 王彧（8 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 王彧 | [《南史・王誕　王華　王惠　王彧》][654] | [JSON](1tc_q18_x7v.json) |
| `A` | 王絢（字長素，王彧長子） | [《南史・王誕　王華　王惠　王彧》][652] | [JSON](1tc_q18_x7v_A.json) |
| `AA` | 王婼（王絢子） | [《宋書・謝莊 王景文》][1105] | [JSON](1tc_q18_x7v_AA.json) |
| `B` | 王繢（字叔素，王彧子） | [《南史・王誕　王華　王惠　王彧》][641] | [JSON](1tc_q18_x7v_B.json) |
| `BA` | 王雋（王繢長子） | [《南史・王誕　王華　王惠　王彧》][641] | [JSON](1tc_q18_x7v_BA.json) |
| `BAA` | 王克（王雋子） | [《南史・王誕　王華　王惠　王彧》][641] | [JSON](1tc_q18_x7v_BAA.json) |
| `BB` | 王繢女（齊安陸王子敬妃） | [《南齊書・王奐 從弟繢 張沖》][501]、[《南史・王誕　王華　王惠　王彧》][641] | [JSON](1tc_q18_x7v_BB.json) |
| `C` | 王約（王繢弟） | [《南史・王誕　王華　王惠　王彧》][641] | [JSON](1tc_q18_x7v_C.json) |

</details>

<details><summary><code>1up_vyo_s9g</code> 徐榮祖（徐夤父）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 徐榮祖（徐夤父） | [《南史・江淹　任昉　王僧孺》][722] | [JSON](1up_vyo_s9g.json) |
| `A` | 徐夤（高平，徐榮祖子） | [《南史・江淹　任昉　王僧孺》][722] | [JSON](1up_vyo_s9g_A.json) |

</details>

<details><summary><code>1y5_eke_4gl</code> 陽慶（扁鵲倉公列傳候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 陽慶 | [《史記・扁鵲倉公列傳》][896] | [JSON](1y5_eke_4gl.json) |
| `A` | 殷（慶子） | [《史記・扁鵲倉公列傳》][896] | [JSON](1y5_eke_4gl_A.json) |

</details>

<details><summary><code>1za_blw_7lb</code> 伯魯（趙世家候選）（6 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 伯魯 | [《史記・趙世家》][834] | [JSON](1za_blw_7lb.json) |
| `A` | 周 | [《史記・趙世家》][834] | [JSON](1za_blw_7lb_A.json) |
| `AA` | 浣 | [《史記・趙世家》][834] | [JSON](1za_blw_7lb_AA.json) |
| `AAA` | 籍 | [《史記・趙世家》][834] | [JSON](1za_blw_7lb_AAA.json) |
| `AAAA` | 章 | [《史記・趙世家》][834] | [JSON](1za_blw_7lb_AAAA.json) |
| `AAAAA` | 種 | [《史記・趙世家》][834] | [JSON](1za_blw_7lb_AAAAA.json) |

</details>

<details><summary><code>1zh_x1q_p1x</code> 袁瑰（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 袁瑰 | [《資治通鑑・晉紀十九》][1201] | [JSON](1zh_x1q_p1x.json) |
| `A` | 袁喬 | [《資治通鑑・晉紀十九》][1201] | [JSON](1zh_x1q_p1x_A.json) |

</details>

<details><summary><code>23q_wcp_hny</code> 崔道固（7 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 崔道固 | [《魏書・燕鳳 許謙 張衮 崔玄伯 鄧淵》][1164] | [JSON](23q_wcp_hny.json) |
| `A` | 崔景微 | [《宋書・薛安都 沈文秀 崔道固》][1112]、[《宋書・薛安都 沈文秀 崔道固》][1113] | [JSON](23q_wcp_hny_A.json) |
| `B` | 崔景徽 | [《魏書・燕鳳 許謙 張衮 崔玄伯 鄧淵》][1164] | [JSON](23q_wcp_hny_B.json) |
| `BA` | 崔休纂 | [《北史・崔光 崔亮》][6]、[《魏書・燕鳳 許謙 張衮 崔玄伯 鄧淵》][1164] | [JSON](23q_wcp_hny_BA.json) |
| `C` | 崔景業 | [《魏書・燕鳳 許謙 張衮 崔玄伯 鄧淵》][1164] | [JSON](23q_wcp_hny_C.json) |
| `CA` | 崔休緒 | [《魏書・燕鳳 許謙 張衮 崔玄伯 鄧淵》][1164] | [JSON](23q_wcp_hny_CA.json) |
| `D` | 崔景淵 | [《魏書・燕鳳 許謙 張衮 崔玄伯 鄧淵》][1164] | [JSON](23q_wcp_hny_D.json) |

</details>

<details><summary><code>258_ae3_26e</code> 傅暢（4 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 傅暢 | [《晉書・鄭袤 李胤 盧欽 華表 石鑒 溫羨》][171]、[《晉書・鄭袤 李胤 盧欽 華表 石鑒 溫羨》][178]、[《三國志・任城陳蕭王傳》][748]、[《宋書・朱齡石 毛脩之 傅弘之》][1044] | [JSON](258_ae3_26e.json) |
| `A` | 傅洪（傅暢子） | [《宋書・朱齡石 毛脩之 傅弘之》][1044] | [JSON](258_ae3_26e_A.json) |
| `AA` | 傅韶（梁州刺史，傅洪子） | [《宋書・朱齡石 毛脩之 傅弘之》][1044] | [JSON](258_ae3_26e_AA.json) |
| `AAA` | 傅弘之（字仲度） | [《宋書・朱齡石 毛脩之 傅弘之》][1044] | [JSON](258_ae3_26e_AAA.json) |

</details>

<details><summary><code>262_b8f_4ie</code> 裴朴之（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 裴朴之 | [《南齊書・皇后》][413]、[《南史・后妃上》][536] | [JSON](262_b8f_4ie.json) |
| `A` | 裴璣之 | [《南齊書・皇后》][413]、[《南史・后妃上》][536] | [JSON](262_b8f_4ie_A.json) |
| `AA` | 裴惠昭 | [《南齊書・高帝下》][395]、[《南齊書・皇后》][413]、[《南齊書・皇后》][415]、[《南齊書・皇后》][414]、[《南史・后妃上》][536] | [JSON](262_b8f_4ie_AA.json) |

</details>

<details><summary><code>27j_f4p_jwp</code> 李廣（7 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 李廣 | [《史記・李將軍列傳》][900] | [JSON](27j_f4p_jwp.json) |
| `A` | 李敢 | [《史記・李將軍列傳》][900] | [JSON](27j_f4p_jwp_A.json) |
| `AA` | 李敢女（未名） | [《史記・李將軍列傳》][900] | [JSON](27j_f4p_jwp_AA.json) |
| `AB` | 禹（李敢男） | [《史記・李將軍列傳》][900] | [JSON](27j_f4p_jwp_AB.json) |
| `B` | 當戸 | [《史記・李將軍列傳》][900] | [JSON](27j_f4p_jwp_B.json) |
| `BA` | 李陵 | [《史記・李將軍列傳》][900] | [JSON](27j_f4p_jwp_BA.json) |
| `C` | 椒 | [《史記・李將軍列傳》][900] | [JSON](27j_f4p_jwp_C.json) |

</details>

<details><summary><code>2a3_ci1_y4y</code> 元湛（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 元湛 | [《北史・道武七王 明元六王 太武五王》][1]、[《冊府元龜・宗室部·承襲第三》][7]、[《元湛墓誌・節錄》][56]、[《魏書・太武五王》][1163] | [JSON](2a3_ci1_y4y.json) |
| `A` | 元法輪 | [《北史・道武七王 明元六王 太武五王》][1]、[《冊府元龜・宗室部·承襲第三》][7]、[《魏書・太武五王》][1163] | [JSON](2a3_ci1_y4y_A.json) |

</details>

<details><summary><code>2bc_992_946</code> 謝靜（4 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 謝靜 | [《晉書・謝尚 謝安》][250] | [JSON](2bc_992_946.json) |
| `A` | 謝肅 | [《晉書・謝尚 謝安》][250] | [JSON](2bc_992_946_A.json) |
| `B` | 謝虔 | [《晉書・謝尚 謝安》][250] | [JSON](2bc_992_946_B.json) |
| `BA` | 謝靈佑 | [《晉書・謝尚 謝安》][250] | [JSON](2bc_992_946_BA.json) |

</details>

<details><summary><code>2c3_7e0_16b</code> 卞範之（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 卞範之 | [《晉書・叛臣二》][285] | [JSON](2c3_7e0_16b.json) |
| `A` | 卞範之女（拒婚對象，未名） | [《宋書・張茂度 庾登之 謝方明 江夷》][1056] | [JSON](2c3_7e0_16b_A.json) |

</details>

<details><summary><code>2d3_fsd_1dh</code> 楚成王（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 楚成王 | [《史記・晉世家》][830] | [JSON](2d3_fsd_1dh.json) |
| `A` | 楚商臣 | [《史記・陳杞世家》][827] | [JSON](2d3_fsd_1dh_A.json) |

</details>

<details><summary><code>2d4_2ed_646</code> 席恭穆（安定焉氏人，鎮西司馬）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 席恭穆（安定焉氏人，鎮西司馬） | [《南齊書・王奐 從弟繢 張沖》][503] | [JSON](2d4_2ed_646.json) |
| `A` | 席謙（新蔡太守，席恭穆子） | [《南齊書・王奐 從弟繢 張沖》][503] | [JSON](2d4_2ed_646_A.json) |

</details>

<details><summary><code>2id_twi_nzj</code> 苻健（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 苻健 | [《晉書・陸曄 何充 褚翜 蔡謨 諸葛恢 殷浩》][248] | [JSON](2id_twi_nzj.json) |
| `A` | 苻萇 | [《晉書・苻洪 苻健 苻生》][293] | [JSON](2id_twi_nzj_A.json) |

</details>

<details><summary><code>2mj_6rl_6xs</code> 陳廢帝伯宗（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 陳廢帝伯宗 | [《陳書・本紀第四: 廢帝》][12] | [JSON](2mj_6rl_6xs.json) |
| `A` | 陳至澤（臨海嗣王） | [《陳書・皇后》][17]、[《南史・后妃下》][554] | [JSON](2mj_6rl_6xs_A.json) |

</details>

<details><summary><code>2n6_7xk_5ov</code> 江夏王義恭（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 江夏王義恭 | [《宋書・殷淳 張暢 何偃 江智淵》][1063] | [JSON](2n6_7xk_5ov.json) |
| `A` | 王僧虔妻（江夏王女，未名） | [《南齊書・王僧虔 張緒》][453] | [JSON](2n6_7xk_5ov_A.json) |

</details>

<details><summary><code>2pg_br4_mcl</code> 王濛（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 王濛 | [《晉書・謝尚 謝安》][250] | [JSON](2pg_br4_mcl.json) |
| `A` | 王修 | [《晉書・謝尚 謝安》][250] | [JSON](2pg_br4_mcl_A.json) |

</details>

<details><summary><code>2v5_rhh_fd6</code> 檀韶（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 檀韶 | [《南齊書・王僧虔 張緒》][453] | [JSON](2v5_rhh_fd6.json) |
| `*A` | 檀珪 | [《南齊書・王僧虔 張緒》][453] | [JSON](2v5_rhh_fd6_%2AA.json) |

</details>

<details><summary><code>2v6_0g1_ve2</code> 衍（宋微仲）（12 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 衍（宋微仲） | [《史記・宋微子世家》][829] | [JSON](2v6_0g1_ve2.json) |
| `A` | 稽（宋公） | [《史記・宋微子世家》][829] | [JSON](2v6_0g1_ve2_A.json) |
| `AA` | 申（宋丁公） | [《史記・宋微子世家》][829] | [JSON](2v6_0g1_ve2_AA.json) |
| `AAA` | 共（宋湣公） | [《史記・宋微子世家》][829] | [JSON](2v6_0g1_ve2_AAA.json) |
| `AAAA` | 鮒祀（宋厲公） | [《史記・宋微子世家》][829] | [JSON](2v6_0g1_ve2_AAAA.json) |
| `AAAAA` | 舉（宋釐公） | [《史記・宋微子世家》][829] | [JSON](2v6_0g1_ve2_AAAAA.json) |
| `AAAAAA` | 覵（宋惠公） | [《史記・宋微子世家》][829] | [JSON](2v6_0g1_ve2_AAAAAA.json) |
| `AAAAAAA` | 哀公（宋惠公子） | [《史記・宋微子世家》][829] | [JSON](2v6_0g1_ve2_AAAAAAA.json) |
| `AAAAAAAA` | 戴公（宋哀公子） | [《史記・宋微子世家》][829] | [JSON](2v6_0g1_ve2_AAAAAAAA.json) |
| `AAAAAAAAA` | 司空（宋武公） | [《史記・宋微子世家》][829] | [JSON](2v6_0g1_ve2_AAAAAAAAA.json) |
| `AAAAAAAAAA` | 宋女（魯惠公夫人） | [《南史・后妃上》][551]、[《史記・宋微子世家》][829]、[《宋書・禮四》][1011]、[《宋書・孝武十四王》][1095]、[《宋書・孝武十四王》][1097] | [JSON](2v6_0g1_ve2_AAAAAAAAAA.json) |
| `AAAAAAAAAB` | 力（宋宣公） | [《史記・宋微子世家》][829] | [JSON](2v6_0g1_ve2_AAAAAAAAAB.json) |

</details>

<details><summary><code>2we_3ll_c5i</code> 裴順宗（裴叔業父）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 裴順宗（裴叔業父） | [《魏書・裴叔業 夏侯道遷 李元護 席法友 王世弼 江悦之 淳于誕 李苗》][1179] | [JSON](2we_3ll_c5i.json) |
| `A` | 裴叔業（河東聞喜人） | [《南齊書・王奐 從弟繢 張沖》][508] | [JSON](2we_3ll_c5i_A.json) |

</details>

<details><summary><code>2xr_pu0_m3d</code> 錢蕆（陳留太守，永世公主夫）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 錢蕆（陳留太守，永世公主夫） | [《陳書・列傳第十一: 王沖 王通 袁敬》][34] | [JSON](2xr_pu0_m3d.json) |
| `A` | 錢岊（永世公主子） | [《陳書・列傳第十一: 王沖 王通 袁敬》][34] | [JSON](2xr_pu0_m3d_A.json) |

</details>

<details><summary><code>2ya_f42_kcq</code> 荀昶（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 荀昶 | [《宋書・范泰 王准之 王韶之 荀伯子》][1067] | [JSON](2ya_f42_kcq.json) |
| `A` | 荀萬秋 | [《宋書・范泰 王准之 王韶之 荀伯子》][1067] | [JSON](2ya_f42_kcq_A.json) |

</details>

<details><summary><code>2zn_kvj_dmy</code> 丁仲遷（南史作道遷，丁令光父）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 丁仲遷（南史作道遷，丁令光父） | [《梁書・皇后》][311]、[《南史・后妃下》][555] | [JSON](2zn_kvj_dmy.json) |
| `A` | 丁令光（梁穆太后） | [《梁書・皇后》][311]、[《南史・后妃下》][555] | [JSON](2zn_kvj_dmy_A.json) |

</details>

<details><summary><code>30f_353_0e8</code> 崔鴻（7 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 崔鴻 | [《魏書・崔光》][1178] | [JSON](30f_353_0e8.json) |
| `A` | 崔子文 | [《崔鴻墓誌・節錄》][43] | [JSON](30f_353_0e8_A.json) |
| `B` | 崔子真 | [《崔鴻墓誌・節錄》][43] | [JSON](30f_353_0e8_B.json) |
| `C` | 崔子長 | [《崔鴻墓誌・節錄》][43] | [JSON](30f_353_0e8_C.json) |
| `D` | 崔子發 | [《崔鴻墓誌・節錄》][43] | [JSON](30f_353_0e8_D.json) |
| `E` | 崔子房 | [《崔鴻墓誌・節錄》][43] | [JSON](30f_353_0e8_E.json) |
| `F` | 崔元華 | [《崔鴻墓誌・節錄》][43] | [JSON](30f_353_0e8_F.json) |

</details>

<details><summary><code>30k_jzz_tpd</code> 邵（9 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 邵 | [《三國志・諸夏侯曹傳》][734] | [JSON](30k_jzz_tpd.json) |
| `A` | 曹真 | [《三國志・諸夏侯曹傳》][734] | [JSON](30k_jzz_tpd_A.json) |
| `AA` | 曹爽 | [《三國志・諸夏侯曹傳》][734] | [JSON](30k_jzz_tpd_AA.json) |
| `AB` | 曹羲 | [《三國志・諸夏侯曹傳》][734] | [JSON](30k_jzz_tpd_AB.json) |
| `AC` | 曹訓 | [《三國志・諸夏侯曹傳》][734] | [JSON](30k_jzz_tpd_AC.json) |
| `AD` | 曹則 | [《三國志・諸夏侯曹傳》][734] | [JSON](30k_jzz_tpd_AD.json) |
| `AE` | 曹彦 | [《三國志・諸夏侯曹傳》][734] | [JSON](30k_jzz_tpd_AE.json) |
| `AF` | 曹皚 | [《三國志・諸夏侯曹傳》][734] | [JSON](30k_jzz_tpd_AF.json) |
| `B` | 曹彬 | [《三國志・諸夏侯曹傳》][734] | [JSON](30k_jzz_tpd_B.json) |

</details>

<details><summary><code>315_3d4_416</code> 任旐（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 任旐 | [《三國志・徐胡二王傳》][754] | [JSON](315_3d4_416.json) |
| `A` | 任嘏 | [《三國志・徐胡二王傳》][754] | [JSON](315_3d4_416_A.json) |

</details>

<details><summary><code>318_d06_496</code> 黃祖（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 黃祖 | [《三國志・二荀賈傳》][735] | [JSON](318_d06_496.json) |
| `A` | 黃射 | [《三國志・二荀賈傳》][735] | [JSON](318_d06_496_A.json) |

</details>

<details><summary><code>326_faf_cd3</code> 王羲之（8 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 王羲之 | [《晉書・王羲之》][251] | [JSON](326_faf_cd3.json) |
| `*A` | 王靜之 | [《宋書・良吏》][1126] | [JSON](326_faf_cd3_%2AA.json) |
| `*AA` | 王悅之（字少明，宋書作悅） | [《南史・王裕之　王鎮之　王韶之　王悅之　王准之》][674]、[《宋書・良吏》][1126] | [JSON](326_faf_cd3_%2AAA.json) |
| `A` | 王玄之 | [《晉書・王羲之》][251]、[《晉書・王羲之》][252] | [JSON](326_faf_cd3_A.json) |
| `B` | 王徽之 | [《晉書・王羲之》][251] | [JSON](326_faf_cd3_B.json) |
| `BA` | 王楨之 | [《晉書・王羲之》][251] | [JSON](326_faf_cd3_BA.json) |
| `C` | 王操之 | [《晉書・王羲之》][251] | [JSON](326_faf_cd3_C.json) |
| `D` | 王肅之 | [《世說新語・排調》][984] | [JSON](326_faf_cd3_D.json) |

</details>

<details><summary><code>344_68f_98e</code> 郭嘉（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 郭嘉 | [《三國志・二荀賈傳》][736] | [JSON](344_68f_98e.json) |
| `A` | 郭奕（字伯益，郭嘉子） | [《三國志・徐胡二王傳》][754] | [JSON](344_68f_98e_A.json) |

</details>

<details><summary><code>36u_j3u_i3z</code> 陸瑁（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 陸瑁 | [《三國志・虞陸張駱陸吾朱傳》][791] | [JSON](36u_j3u_i3z.json) |
| `A` | 陸喜 | [《三國志・虞陸張駱陸吾朱傳》][791] | [JSON](36u_j3u_i3z_A.json) |

</details>

<details><summary><code>37j_16p_7n8</code> 曹參（6 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 曹參 | [《史記・曹相國世家》][845] | [JSON](37j_16p_7n8.json) |
| `A` | 窋 | [《史記・曹相國世家》][845] | [JSON](37j_16p_7n8_A.json) |
| `AA` | 奇 | [《史記・曹相國世家》][845] | [JSON](37j_16p_7n8_AA.json) |
| `AAA` | 時 | [《史記・曹相國世家》][845] | [JSON](37j_16p_7n8_AAA.json) |
| `AAAA` | 襄 | [《史記・衛將軍驃騎列傳》][902] | [JSON](37j_16p_7n8_AAAA.json) |
| `AAAAA` | 宗 | [《史記・曹相國世家》][845] | [JSON](37j_16p_7n8_AAAAA.json) |

</details>

<details><summary><code>3b9_b07_bdb</code> 馮紞（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 馮紞 | [《晉書・王沈 荀顗 荀勖 馮紞》][158] | [JSON](3b9_b07_bdb.json) |
| `A` | 播（馮紞子） | [《晉書・王沈 荀顗 荀勖 馮紞》][158] | [JSON](3b9_b07_bdb_A.json) |
| `B` | 熊（馮紞子） | [《晉書・王沈 荀顗 荀勖 馮紞》][158] | [JSON](3b9_b07_bdb_B.json) |

</details>

<details><summary><code>3bh_k4m_fg4</code> 宋太祖義隆（9 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 宋太祖義隆 | [《宋書・王華 王曇首 殷景仁 沈演之》][1071] | [JSON](3bh_k4m_fg4.json) |
| `A` | 東陽獻公主 | [《南史・后妃上》][552]、[《宋書・后妃》][1021]、[《宋書・徐湛之 江湛 王僧綽》][1081] | [JSON](3bh_k4m_fg4_A.json) |
| `B` | 劉英媛（臨川長公主） | [《南史・王誕　王華　王惠　王彧》][656]、[《宋書・后妃》][1017] | [JSON](3bh_k4m_fg4_B.json) |
| `C` | 長城公主（宋文帝第五女，謝緯妻） | [《宋書・庾悅 王誕 謝景仁 袁湛 褚叔度》][1054] | [JSON](3bh_k4m_fg4_C.json) |
| `D` | 琅邪貞長公主（宋文帝女，褚曖妻） | [《南史・褚裕之》][687]、[《宋書・庾悅 王誕 謝景仁 袁湛 褚叔度》][1048] | [JSON](3bh_k4m_fg4_D.json) |
| `E` | 劉休祐（晉平剌王） | [《宋書・文九王》][1082] | [JSON](3bh_k4m_fg4_E.json) |
| `F` | 劉英媚（新蔡公主） | [《南史・后妃上》][529]、[《宋書・后妃》][1013] | [JSON](3bh_k4m_fg4_F.json) |
| `G` | 海鹽公主（宋文帝第四女，趙倩妻） | — | [JSON](3bh_k4m_fg4_G.json) |
| `H` | 尋陽公主（宋文帝女，郗徽母） | [《梁書・皇后》][315] | [JSON](3bh_k4m_fg4_H.json) |

</details>

<details><summary><code>3c9_d1d_870</code> 王謐（5 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 王謐 | [《晉書・王導》][212] | [JSON](3c9_d1d_870.json) |
| `*A` | 王履（王謐孫，王球兄子） | [《南史・王誕　王華　王惠　王彧》][648] | [JSON](3c9_d1d_870_%2AA.json) |
| `A` | 王瓘 | [《晉書・王導》][212] | [JSON](3c9_d1d_870_A.json) |
| `B` | 王球 | [《南史・王誕　王華　王惠　王彧》][648] | [JSON](3c9_d1d_870_B.json) |
| `C` | 王琇 | [《晉書・王導》][212] | [JSON](3c9_d1d_870_C.json) |

</details>

<details><summary><code>3ea_uzt_2n2</code> 何准（15 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 何准 | [《晉書・外戚》][264] | [JSON](3ea_uzt_2n2.json) |
| `A` | 何法倪 | [《晉書・后妃下》][146] | [JSON](3ea_uzt_2n2_A.json) |
| `B` | 何澄（字季玄，何准子） | [《晉書・外戚》][264] | [JSON](3ea_uzt_2n2_B.json) |
| `BA` | 何融（晉元熙大司農，何澄次子） | [《晉書・外戚》][264]、[《宋書・后妃》][1013]、[《宋書・后妃》][1014] | [JSON](3ea_uzt_2n2_BA.json) |
| `BA*A` | 何瑀（字稚玉，何融孫） | [《南史・后妃上》][529] | [JSON](3ea_uzt_2n2_BA%2AA.json) |
| `BA*AA` | 何令婉（宋前廢帝獻皇后） | [《南史・后妃上》][529]、[《宋書・后妃》][1013] | [JSON](3ea_uzt_2n2_BA%2AAA.json) |
| `BA*AB` | 何邁（何瑀子，新蔡公主夫） | [《宋書・后妃》][1013] | [JSON](3ea_uzt_2n2_BA%2AAB.json) |
| `BA*ABA` | 何曼倩（何邁子） | [《宋書・后妃》][1013] | [JSON](3ea_uzt_2n2_BA%2AABA.json) |
| `BB` | 何籍（何澄長子） | [《晉書・外戚》][264] | [JSON](3ea_uzt_2n2_BB.json) |
| `C` | 何放（何准子，繼何充） | [《晉書・外戚》][264] | [JSON](3ea_uzt_2n2_C.json) |
| `D` | 何惔（何准子） | [《晉書・外戚》][264] | [JSON](3ea_uzt_2n2_D.json) |
| `DA` | 何叔度（何惔子） | [《晉書・外戚》][265]、[《南齊書・江斆 何昌㝢 謝𤅢 王思遠》][479]、[《宋書・王敬弘 何尚之》][1075] | [JSON](3ea_uzt_2n2_DA.json) |
| `DAA` | 何佟之（何昌宇父） | [《南齊書・江斆 何昌㝢 謝𤅢 王思遠》][479]、[《南史・何尚之》][690] | [JSON](3ea_uzt_2n2_DAA.json) |
| `DAAA` | 何昌宇（字儼望） | [《南齊書・江斆 何昌㝢 謝𤅢 王思遠》][479]、[《南史・何尚之》][690] | [JSON](3ea_uzt_2n2_DAAA.json) |
| `DB` | 何元度（何惔子） | [《晉書・外戚》][265] | [JSON](3ea_uzt_2n2_DB.json) |

</details>

<details><summary><code>3eu_ixs_h1w</code> 霸先〔新唐陳氏序〕（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 霸先〔新唐陳氏序〕 | [《陳書・列傳第十一: 王沖 王通 袁敬》][27]、[《陳書・列傳第十一: 王沖 王通 袁敬》][30]、[《陳書・列傳第十一: 王沖 王通 袁敬》][34] | [JSON](3eu_ixs_h1w.json) |
| `A` | 永世公主（陳高祖長女，《南史》作永嗣） | [《陳書・列傳第十一: 王沖 王通 袁敬》][34] | [JSON](3eu_ixs_h1w_A.json) |

</details>

<details><summary><code>3fq_v2q_2xv</code> 屈晃（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 屈晃 | [《三國志・吳主五子傳》][805] | [JSON](3fq_v2q_2xv.json) |
| `A` | 屈緒 | [《三國志・吳主五子傳》][805] | [JSON](3fq_v2q_2xv_A.json) |

</details>

<details><summary><code>3hi_dur_mak</code> 徐陵〔吳太末，字元大〕（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 徐陵〔吳太末，字元大〕 | [《三國志・虞陸張駱陸吾朱傳》][795] | [JSON](3hi_dur_mak.json) |
| `A` | 徐平〔徐陵子，字伯先〕 | [《三國志・虞陸張駱陸吾朱傳》][795] | [JSON](3hi_dur_mak_A.json) |

</details>

<details><summary><code>3jf_ce1_jy2</code> 昆莫父（未名）（大宛列傳候選）（5 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 昆莫父（未名） | [《史記・大宛列傳》][914] | [JSON](3jf_ce1_jy2.json) |
| `A` | 昆莫 | [《史記・大宛列傳》][914] | [JSON](3jf_ce1_jy2_A.json) |
| `AA` | 大祿 | [《史記・大宛列傳》][914] | [JSON](3jf_ce1_jy2_AA.json) |
| `AB` | 大祿兄（未名太子） | [《史記・大宛列傳》][914] | [JSON](3jf_ce1_jy2_AB.json) |
| `ABA` | 岑娶 | [《史記・大宛列傳》][914] | [JSON](3jf_ce1_jy2_ABA.json) |

</details>

<details><summary><code>3qs_nqa_ioa</code> 混〔靖父；武原令〕（15 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 混〔靖父；武原令〕 | [《宋書・武帝上》][999] | [JSON](3qs_nqa_ioa.json) |
| `A` | 靖〔翹父；東安太守〕 | [《宋書・武帝上》][999] | [JSON](3qs_nqa_ioa_A.json) |
| `AA` | 翹〔孝皇帝；高祖之父〕 | [《宋書・后妃》][1016] | [JSON](3qs_nqa_ioa_AA.json) |
| `AAA` | 宋高祖裕 | [《魏書・崔浩》][1167] | [JSON](3qs_nqa_ioa_AAA.json) |
| `AAAA` | 劉榮男（吳興長公主） | [《南史・王誕　王華　王惠　王彧》][634]、[《南史・王誕　王華　王惠　王彧》][633]、[《宋書・后妃》][1017] | [JSON](3qs_nqa_ioa_AAAA.json) |
| `AAAB` | 宋新安公主（劉裕第五女） | [《南史・王誕　王華　王惠　王彧》][654] | [JSON](3qs_nqa_ioa_AAAB.json) |
| `AAAC` | 劉欣男（豫章康長公主，南史作次男） | [《南史・后妃上》][529]、[《宋書・后妃》][1013] | [JSON](3qs_nqa_ioa_AAAC.json) |
| `AAB` | 道憐 | [《宋書・張茂度 庾登之 謝方明 江夷》][1058] | [JSON](3qs_nqa_ioa_AAB.json) |
| `AABA` | 劉義融（桂陽恭侯） | [《南史・宋宗室及諸王上》][564]、[《宋書・宗室》][1046] | [JSON](3qs_nqa_ioa_AABA.json) |
| `AABAA` | 劉覬（桂陽孝侯） | [《南史・宋宗室及諸王上》][564] | [JSON](3qs_nqa_ioa_AABAA.json) |
| `AABAB` | 劉襲（字茂德，臨澧忠侯） | [《南史・宋宗室及諸王上》][564] | [JSON](3qs_nqa_ioa_AABAB.json) |
| `AABABA` | 劉晃（宋宗室） | [《南史・后妃上》][547]、[《南史・后妃上》][548]、[《南史・宋宗室及諸王上》][564]、[《宋書・后妃》][1018] | [JSON](3qs_nqa_ioa_AABABA.json) |
| `AABB` | 劉義宗（新渝惠侯，字伯奴） | [《宋書・宗室》][1047] | [JSON](3qs_nqa_ioa_AABB.json) |
| `AABBA` | 劉遐（字彦道，吳郡太守） | [《宋書・宗室》][1047] | [JSON](3qs_nqa_ioa_AABBA.json) |
| `AAC` | 臨川王道規 | [《晉書・叛臣二》][285] | [JSON](3qs_nqa_ioa_AAC.json) |

</details>

<details><summary><code>3te_z66_d5a</code> 張敖（外戚世家候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 張敖 | [《史記・外戚世家》][840] | [JSON](3te_z66_d5a.json) |
| `A` | 孝惠皇后 | [《史記・外戚世家》][840] | [JSON](3te_z66_d5a_A.json) |

</details>

<details><summary><code>3tg_h3n_iou</code> 樂玄（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 樂玄 | [《南齊書・王琨 張岱 褚炫 何戢 王延之 阮韜》][446]、[《南史・王誕　王華　王惠　王彧》][643] | [JSON](3tg_h3n_iou.json) |
| `A` | 樂玄女〔王懌妻〕 | — | [JSON](3tg_h3n_iou_A.json) |

</details>

<details><summary><code>3tt_4ey_uti</code> 袁湛（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 袁湛 | [《晉書・謝尚 謝安》][250] | [JSON](3tt_4ey_uti.json) |
| `A` | 袁齊媯 | [《南史・后妃上》][552]、[《宋書・后妃》][1021] | [JSON](3tt_4ey_uti_A.json) |

</details>

<details><summary><code>3tw_nq2_gyn</code> 霍去病（外戚世家候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 霍去病 | [《史記・衛將軍驃騎列傳》][902] | [JSON](3tw_nq2_gyn.json) |
| `A` | 嬗 | [《史記・衛將軍驃騎列傳》][902] | [JSON](3tw_nq2_gyn_A.json) |

</details>

<details><summary><code>3xx_gdy_or6</code> 裴〔周浚父〕等兩支（共同父未名；編輯接合）（15 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `A` | 裴〔周浚父〕 | [《晉書・周浚 成公簡 苟晞 華軼 劉喬》][204] | [JSON](3xx_gdy_or6_A.json) |
| `AA` | 周浚 | [《晉書・周浚 成公簡 苟晞 華軼 劉喬》][204] | [JSON](3xx_gdy_or6_AA.json) |
| `AAA` | 周顗 | [《晉書・劉隗 刁協 戴若思 周顗》][224] | [JSON](3xx_gdy_or6_AAA.json) |
| `AAAA` | 周閔 | [《晉書・劉隗 刁協 戴若思 周顗》][224] | [JSON](3xx_gdy_or6_AAAA.json) |
| `AAAB` | 周恬 | [《晉書・劉隗 刁協 戴若思 周顗》][224] | [JSON](3xx_gdy_or6_AAAB.json) |
| `AAAC` | 周頤 | [《晉書・劉隗 刁協 戴若思 周顗》][224] | [JSON](3xx_gdy_or6_AAAC.json) |
| `AAACA` | 周琳 | [《晉書・劉隗 刁協 戴若思 周顗》][224] | [JSON](3xx_gdy_or6_AAACA.json) |
| `AAACAA` | 周文 | [《晉書・劉隗 刁協 戴若思 周顗》][224] | [JSON](3xx_gdy_or6_AAACAA.json) |
| `AAB` | 周嵩 | [《晉書・周浚 成公簡 苟晞 華軼 劉喬》][204] | [JSON](3xx_gdy_or6_AAB.json) |
| `AABA` | 王應之嫂〔嵩之女，未名〕 | [《晉書・周浚 成公簡 苟晞 華軼 劉喬》][204] | [JSON](3xx_gdy_or6_AABA.json) |
| `AAC` | 周謨 | [《晉書・周浚 成公簡 苟晞 華軼 劉喬》][204] | [JSON](3xx_gdy_or6_AAC.json) |
| `B` | 蕤〔周馥父〕 | [《晉書・周浚 成公簡 苟晞 華軼 劉喬》][204] | [JSON](3xx_gdy_or6_B.json) |
| `BA` | 周馥 | [《晉書・周浚 成公簡 苟晞 華軼 劉喬》][204] | [JSON](3xx_gdy_or6_BA.json) |
| `BAA` | 密〔周馥子〕 | [《晉書・周浚 成公簡 苟晞 華軼 劉喬》][204] | [JSON](3xx_gdy_or6_BAA.json) |
| `BAB` | 周矯 | [《晉書・周浚 成公簡 苟晞 華軼 劉喬》][204] | [JSON](3xx_gdy_or6_BAB.json) |

</details>

<details><summary><code>408_ce3_5d8</code> 沈慶之（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 沈慶之 | [《南史・王弘》][603]、[《宋書・王僧達 顏竣》][1087] | [JSON](408_ce3_5d8.json) |
| `A` | 沈文季 | [《梁書・王亮 張稷 王瑩》][329]、[《南齊書・徐孝嗣 沈文季》][485]、[《南史・王曇首》][618] | [JSON](408_ce3_5d8_A.json) |

</details>

<details><summary><code>40p_eb9_ggr</code> 陸抗〔字幼節〕（5 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 陸抗〔字幼節〕 | [《三國志・陸遜傳》][799] | [JSON](40p_eb9_ggr.json) |
| `A` | 陸景 | [《三國志・陸遜傳》][799] | [JSON](40p_eb9_ggr_A.json) |
| `B` | 陸晏 | [《三國志・陸遜傳》][799] | [JSON](40p_eb9_ggr_B.json) |
| `C` | 陸玄 | [《三國志・陸遜傳》][799] | [JSON](40p_eb9_ggr_C.json) |
| `D` | 陸雲 | [《三國志・陸遜傳》][799] | [JSON](40p_eb9_ggr_D.json) |

</details>

<details><summary><code>418_c91_b6b</code> 華廙（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 華廙 | [《晉書・鄭袤 李胤 盧欽 華表 石鑒 溫羨》][175] | [JSON](418_c91_b6b.json) |
| `A` | 華混〔字敬倫，裴注作昆〕 | [《晉書・鄭袤 李胤 盧欽 華表 石鑒 溫羨》][175] | [JSON](418_c91_b6b_A.json) |
| `AA` | 華陶〔鞏令〕 | [《晉書・鄭袤 李胤 盧欽 華表 石鑒 溫羨》][175] | [JSON](418_c91_b6b_AA.json) |

</details>

<details><summary><code>42z_cse_1ka</code> 熊良夫（楚宣王）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 熊良夫（楚宣王） | [《史記・楚世家》][831] | [JSON](42z_cse_1ka.json) |
| `A` | 熊商（楚威王） | [《史記・楚世家》][831] | [JSON](42z_cse_1ka_A.json) |

</details>

<details><summary><code>46a_tvp_dq9</code> 秦獻公（魏世家候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 秦獻公 | [《史記・魏世家》][835] | [JSON](46a_tvp_dq9.json) |
| `A` | 秦孝公 | [《史記・魏世家》][835] | [JSON](46a_tvp_dq9_A.json) |

</details>

<details><summary><code>47p_kjh_ez7</code> 齊太祖道成（6 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 齊太祖道成 | [《梁書・謝朏 弟子覽》][323] | [JSON](47p_kjh_ez7.json) |
| `A` | 臨海長公主（齊高帝女） | [《南史・王曇首》][612] | [JSON](47p_kjh_ez7_A.json) |
| `B` | 江夏王鋒 | [《南齊書・高祖十二王》][459] | [JSON](47p_kjh_ez7_B.json) |
| `C` | 蕭映（臨川獻王，字宣光） | [《南齊書・高祖十二王》][458] | [JSON](47p_kjh_ez7_C.json) |
| `D` | 蕭鉉（齊河東王，字宣胤） | [《南齊書・高祖十二王》][457] | [JSON](47p_kjh_ez7_D.json) |
| `E` | 蕭暠（安成恭王，字宣曜） | [《南齊書・高祖十二王》][456] | [JSON](47p_kjh_ez7_E.json) |

</details>

<details><summary><code>49g_7az_e4i</code> 李斯（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 李斯 | [《史記・李斯列傳》][878] | [JSON](49g_7az_e4i.json) |
| `A` | 李由 | [《史記・李斯列傳》][878] | [JSON](49g_7az_e4i_A.json) |
| `B` | 李斯中子未名 | [《史記・李斯列傳》][878] | [JSON](49g_7az_e4i_B.json) |

</details>

<details><summary><code>4ag_yml_73x</code> 休（平原劉氏父）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 休（平原劉氏父） | [《崔混墓誌・節錄》][44] | [JSON](4ag_yml_73x.json) |
| `A` | 劉氏（崔敬友妻） | [《崔混墓誌・節錄》][44] | [JSON](4ag_yml_73x_A.json) |

</details>

<details><summary><code>4c2_19b_bf4</code> 沈充（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 沈充 | [《晉書・叛臣一》][284] | [JSON](4c2_19b_bf4.json) |
| `A` | 沈勁〔字世堅、沈充子〕 | [《晉書・忠義》][256]、[《晉書・叛臣一》][284] | [JSON](4c2_19b_bf4_A.json) |

</details>

<details><summary><code>4c2_763_efd</code> 謝喻（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 謝喻 | [《晉書・謝尚 謝安》][250] | [JSON](4c2_763_efd.json) |
| `A` | 謝暠 | [《晉書・謝尚 謝安》][250] | [JSON](4c2_763_efd_A.json) |

</details>

<details><summary><code>4ij_7ik_fgy</code> 謝鯤（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 謝鯤 | [《晉書・謝尚 謝安》][250] | [JSON](4ij_7ik_fgy.json) |
| `A` | 謝尚 | [《晉書・謝尚 謝安》][250] | [JSON](4ij_7ik_fgy_A.json) |

</details>

<details><summary><code>4kt_0ar_aqo</code> 裴壽孫（前軍長史）（4 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 裴壽孫（前軍長史） | [《梁書・裴邃 兄子之高 之平 之橫 夏侯亶 弟夔 魚弘附 韋放》][353] | [JSON](4kt_0ar_aqo.json) |
| `A` | 裴仲穆（驍騎將軍） | [《梁書・裴邃 兄子之高 之平 之橫 夏侯亶 弟夔 魚弘附 韋放》][353] | [JSON](4kt_0ar_aqo_A.json) |
| `AA` | 裴髦（中散大夫） | [《梁書・裴邃 兄子之高 之平 之橫 夏侯亶 弟夔 魚弘附 韋放》][353] | [JSON](4kt_0ar_aqo_AA.json) |
| `AAA` | 裴之高（字如山） | [《梁書・韋粲 江子一 弟子四 子五 張嵊 沈浚 柳敬禮》][377] | [JSON](4kt_0ar_aqo_AAA.json) |

</details>

<details><summary><code>4mr_j4p_k5h</code> 到洽（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 到洽 | [《陳書・列傳第十四: 到仲舉 韓子高 華皎》][37]、[《梁書・王僧孺 張率 劉孝綽 王筠》][363]、[《梁書・王僧孺 張率 劉孝綽 王筠》][362]、[《南史・王曇首》][629]、[《南史・王曇首》][628]、[《南史・王誕　王華　王惠　王彧》][650] | [JSON](4mr_j4p_k5h.json) |
| `A` | 到仲舉（陳尚書僕射，字德言） | [《陳書・列傳第十四: 到仲舉 韓子高 華皎》][37] | [JSON](4mr_j4p_k5h_A.json) |

</details>

<details><summary><code>4qr_wrk_3vd</code> 庾琛（32 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 庾琛 | [《晉書・庾亮》][230] | [JSON](4qr_wrk_3vd.json) |
| `A` | 庾文君 | [《晉書・后妃下》][150]、[《晉書・庾亮》][230] | [JSON](4qr_wrk_3vd_A.json) |
| `B` | 庾亮 | [《晉書・庾亮》][230] | [JSON](4qr_wrk_3vd_B.json) |
| `BA` | 庾彬 | [《晉書・庾亮》][230] | [JSON](4qr_wrk_3vd_BA.json) |
| `BB` | 庾羲 | [《晉書・庾亮》][230] | [JSON](4qr_wrk_3vd_BB.json) |
| `BBA` | 庾准 | [《晉書・庾亮》][230] | [JSON](4qr_wrk_3vd_BBA.json) |
| `BBAA` | 庾悅 | [《晉書・庾亮》][230] | [JSON](4qr_wrk_3vd_BBAA.json) |
| `BBB` | 庾楷 | [《晉書・叛臣二》][285] | [JSON](4qr_wrk_3vd_BBB.json) |
| `BC` | 庾龢 | [《晉書・庾亮》][230] | [JSON](4qr_wrk_3vd_BC.json) |
| `BCA` | 庾恆 | [《晉書・庾亮》][230] | [JSON](4qr_wrk_3vd_BCA.json) |
| `C` | 庾懌 | [《晉書・庾亮》][229] | [JSON](4qr_wrk_3vd_C.json) |
| `CA` | 庾統 | [《晉書・庾亮》][229] | [JSON](4qr_wrk_3vd_CA.json) |
| `CAA` | 庾玄之 | [《晉書・庾亮》][229] | [JSON](4qr_wrk_3vd_CAA.json) |
| `D` | 庾冰 | [《晉書・庾亮》][229] | [JSON](4qr_wrk_3vd_D.json) |
| `DA` | 庾希 | [《晉書・庾亮》][229] | [JSON](4qr_wrk_3vd_DA.json) |
| `DAA` | 庾攸之 | [《晉書・庾亮》][229] | [JSON](4qr_wrk_3vd_DAA.json) |
| `DB` | 庾襲 | [《晉書・庾亮》][229] | [JSON](4qr_wrk_3vd_DB.json) |
| `DC` | 庾友 | [《晉書・庾亮》][229] | [JSON](4qr_wrk_3vd_DC.json) |
| `DCA` | 庾叔宣 | [《晉書・庾亮》][229] | [JSON](4qr_wrk_3vd_DCA.json) |
| `DD` | 庾蘊 | [《晉書・庾亮》][229] | [JSON](4qr_wrk_3vd_DD.json) |
| `DDA` | 庾廓之 | [《晉書・庾亮》][229] | [JSON](4qr_wrk_3vd_DDA.json) |
| `DDB` | 庾廓（宋書原稱） | [《宋書・張茂度 庾登之 謝方明 江夷》][1057] | [JSON](4qr_wrk_3vd_DDB.json) |
| `DDBA` | 庾登之 | [《宋書・張茂度 庾登之 謝方明 江夷》][1057] | [JSON](4qr_wrk_3vd_DDBA.json) |
| `DDBAA` | 庾沖遠 | [《宋書・后妃》][1017]、[《宋書・張茂度 庾登之 謝方明 江夷》][1057] | [JSON](4qr_wrk_3vd_DDBAA.json) |
| `DDBB` | 庾炳之 | [《宋書・張茂度 庾登之 謝方明 江夷》][1057] | [JSON](4qr_wrk_3vd_DDBB.json) |
| `DDBBA` | 庾季遠 | [《宋書・張茂度 庾登之 謝方明 江夷》][1057] | [JSON](4qr_wrk_3vd_DDBBA.json) |
| `DDBBB` | 庾弘遠 | [《宋書・張茂度 庾登之 謝方明 江夷》][1057] | [JSON](4qr_wrk_3vd_DDBBB.json) |
| `DE` | 庾倩 | [《晉書・庾亮》][229] | [JSON](4qr_wrk_3vd_DE.json) |
| `DF` | 庾邈 | [《晉書・庾亮》][229] | [JSON](4qr_wrk_3vd_DF.json) |
| `DG` | 庾柔 | [《晉書・庾亮》][229] | [JSON](4qr_wrk_3vd_DG.json) |
| `E` | 庾條 | [《晉書・庾亮》][229] | [JSON](4qr_wrk_3vd_E.json) |
| `F` | 庾翼 | [《晉書・謝尚 謝安》][250] | [JSON](4qr_wrk_3vd_F.json) |

</details>

<details><summary><code>4w5_b4e_vf5</code> 王翁孺（14 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 王翁孺 | [《漢書・元后傳》][73] | [JSON](4w5_b4e_vf5.json) |
| `A` | 王禁 | [《漢書・元后傳》][73] | [JSON](4w5_b4e_vf5_A.json) |
| `AA` | 君俠 | [《漢書・元后傳》][73] | [JSON](4w5_b4e_vf5_AA.json) |
| `AB` | 政君 | [《漢書・元后傳》][73] | [JSON](4w5_b4e_vf5_AB.json) |
| `AC` | 君力 | [《漢書・元后傳》][73] | [JSON](4w5_b4e_vf5_AC.json) |
| `AD` | 君弟 | [《漢書・元后傳》][73] | [JSON](4w5_b4e_vf5_AD.json) |
| `AE` | 鳳 | [《漢書・元后傳》][73] | [JSON](4w5_b4e_vf5_AE.json) |
| `AF` | 曼 | [《漢書・元后傳》][73] | [JSON](4w5_b4e_vf5_AF.json) |
| `AG` | 譚 | [《漢書・元后傳》][73] | [JSON](4w5_b4e_vf5_AG.json) |
| `AH` | 崇 | [《漢書・元后傳》][73] | [JSON](4w5_b4e_vf5_AH.json) |
| `AI` | 商 | [《漢書・元后傳》][73] | [JSON](4w5_b4e_vf5_AI.json) |
| `AJ` | 立 | [《漢書・元后傳》][73] | [JSON](4w5_b4e_vf5_AJ.json) |
| `AK` | 根 | [《漢書・元后傳》][73] | [JSON](4w5_b4e_vf5_AK.json) |
| `AL` | 逢時 | [《漢書・元后傳》][73] | [JSON](4w5_b4e_vf5_AL.json) |

</details>

<details><summary><code>4wv_6og_mwb</code> 申無宇（芋尹）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 申無宇（芋尹） | [《史記・楚世家》][831] | [JSON](4wv_6og_mwb.json) |
| `A` | 申亥（收葬楚靈王者） | [《史記・楚世家》][831] | [JSON](4wv_6og_mwb_A.json) |

</details>

<details><summary><code>4xe_ms4_pr9</code> 夢者（曹亡敘事未名）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 夢者（曹亡敘事未名） | [《史記・管蔡世家》][826] | [JSON](4xe_ms4_pr9.json) |
| `A` | 夢者子（未名） | [《史記・管蔡世家》][826] | [JSON](4xe_ms4_pr9_A.json) |

</details>

<details><summary><code>4xl_1hw_6cg</code> 孫宏（許邁妻父）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 孫宏（許邁妻父） | [《真誥・卷二十》][1191] | [JSON](4xl_1hw_6cg.json) |
| `A` | 孫氏（許邁妻） | [《晉書・王羲之》][251] | [JSON](4xl_1hw_6cg_A.json) |

</details>

<details><summary><code>4yg_ete_09a</code> 柴武（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 柴武 | [《史記・韓信盧綰列傳》][884] | [JSON](4yg_ete_09a.json) |
| `A` | 奇（柴武子） | [《史記・淮南衡山列傳》][909] | [JSON](4yg_ete_09a_A.json) |

</details>

<details><summary><code>505_n4y_p39</code> 秦開（匈奴列傳候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 秦開 | [《史記・匈奴列傳》][901] | [JSON](505_n4y_p39.json) |
| `*A` | 秦舞陽 | [《史記・刺客列傳》][877] | [JSON](505_n4y_p39_%2AA.json) |

</details>

<details><summary><code>50h_gqe_1p1</code> 具（魯獻公）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 具（魯獻公） | [《史記・魯周公世家》][824] | [JSON](50h_gqe_1p1.json) |
| `A` | 濞（魯真公） | [《史記・魯周公世家》][824]、[《史記・三代世表》][1222] | [JSON](50h_gqe_1p1_A.json) |

</details>

<details><summary><code>512_1cd_a4b</code> 諸葛恪（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 諸葛恪 | [《三國志・吳主五子傳》][803]、[《三國志・吳主五子傳》][805] | [JSON](512_1cd_a4b.json) |
| `A` | 諸葛建 | [《三國志・虞陸張駱陸吾朱傳》][795] | [JSON](512_1cd_a4b_A.json) |

</details>

<details><summary><code>572_278_cba</code> 孫仲謀（引古）（14 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 孫仲謀（引古） | [《三國志・張顧諸葛步傳》][782] | [JSON](572_278_cba.json) |
| `A` | 孫和〔字子孝〕 | [《三國志・吳主五子傳》][805] | [JSON](572_278_cba_A.json) |
| `AA` | 孫德 | [《三國志・吳主五子傳》][805] | [JSON](572_278_cba_AA.json) |
| `AB` | 孫謙〔孫和子、永安侯〕 | [《三國志・吳主五子傳》][805] | [JSON](572_278_cba_AB.json) |
| `AC` | 孫俊〔張承外孫、孫和子〕 | [《三國志・吳主五子傳》][805] | [JSON](572_278_cba_AC.json) |
| `B` | 孫霸〔魯王〕 | [《三國志・吳主五子傳》][802] | [JSON](572_278_cba_B.json) |
| `BA` | 孫基 | [《三國志・吳主五子傳》][802] | [JSON](572_278_cba_BA.json) |
| `BB` | 孫壹〔孫霸子，吳志考證疑名字〕 | [《三國志・吳主五子傳》][802] | [JSON](572_278_cba_BB.json) |
| `C` | 孫登〔吳太子，字子高〕 | [《三國志・吳主五子傳》][803] | [JSON](572_278_cba_C.json) |
| `CA` | 孫璠 | [《三國志・吳主五子傳》][803] | [JSON](572_278_cba_CA.json) |
| `CB` | 孫希 | [《三國志・吳主五子傳》][803] | [JSON](572_278_cba_CB.json) |
| `CC` | 孫英〔孫登子、吳侯〕 | [《三國志・吳主五子傳》][803] | [JSON](572_278_cba_CC.json) |
| `D` | 孫慮〔建昌侯，字子智〕 | [《三國志・吳主五子傳》][806] | [JSON](572_278_cba_D.json) |
| `E` | 孫奮〔齊王，字子揚〕 | [《三國志・吳主五子傳》][804] | [JSON](572_278_cba_E.json) |

</details>

<details><summary><code>573_104_0c1</code> 李崇（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 李崇 | [《魏書・刁雍 王慧龍 韓延之 袁式》][1168] | [JSON](573_104_0c1.json) |
| `A` | 李世哲 | [《魏書・刁雍 王慧龍 韓延之 袁式》][1168] | [JSON](573_104_0c1_A.json) |
| `B` | 青肫〔李崇子〕 | [《魏書・刁雍 王慧龍 韓延之 袁式》][1168] | [JSON](573_104_0c1_B.json) |

</details>

<details><summary><code>591_360_8ca</code> 樂廣（7 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 樂廣 | [《晉書・山濤 王戎 郭舒 樂廣》][163] | [JSON](591_360_8ca.json) |
| `*****A` | 樂藹（字蔚遠） | [《梁書・宗夬 劉坦 樂藹》][332] | [JSON](591_360_8ca_%2A%2A%2A%2A%2AA.json) |
| `A` | 樂凱〔字弘緒〕 | [《晉書・山濤 王戎 郭舒 樂廣》][163] | [JSON](591_360_8ca_A.json) |
| `B` | 樂肇〔字弘茂〕 | [《晉書・山濤 王戎 郭舒 樂廣》][163] | [JSON](591_360_8ca_B.json) |
| `C` | 樂謨〔字弘範〕 | [《晉書・山濤 王戎 郭舒 樂廣》][163] | [JSON](591_360_8ca_C.json) |
| `D` | 樂廣女〔成都王妃〕 | [《晉書・山濤 王戎 郭舒 樂廣》][163]、[《世說新語・言語》][929]、[《資治通鑑・晉紀七》][1199] | [JSON](591_360_8ca_D.json) |
| `E` | 樂廣女〔衛玠妻〕 | [《晉書・衞瓘 張華》][153]、[《世說新語・言語》][929] | [JSON](591_360_8ca_E.json) |

</details>

<details><summary><code>59d_72d_924</code> 王雅（4 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 王雅 | [《晉書・王湛 荀崧 范汪 劉惔 張憑 韓伯》][233] | [JSON](59d_72d_924.json) |
| `A` | 王准之（東海，王雅子） | [《梁書・王僧孺 張率 劉孝綽 王筠》][361]、[《南史・江淹　任昉　王僧孺》][721]、[《南史・江淹　任昉　王僧孺》][722] | [JSON](59d_72d_924_A.json) |
| `AA` | 王延年（王僧孺父） | [《南史・江淹　任昉　王僧孺》][721]、[《南史・江淹　任昉　王僧孺》][722] | [JSON](59d_72d_924_AA.json) |
| `AAA` | 王僧孺 | [《南史・江淹　任昉　王僧孺》][722] | [JSON](59d_72d_924_AAA.json) |

</details>

<details><summary><code>5bo_dxd_69k</code> 冉雍父（弟子列傳候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 冉雍父 | [《史記・仲尼弟子列傳》][858] | [JSON](5bo_dxd_69k.json) |
| `A` | 冉雍 | [《史記・仲尼弟子列傳》][858] | [JSON](5bo_dxd_69k_A.json) |

</details>

<details><summary><code>5dd_l1c_6g8</code> 衛青（5 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 衛青 | [《史記・衛將軍驃騎列傳》][902] | [JSON](5dd_l1c_6g8.json) |
| `A` | 衛青子陰安侯 | [《史記・衛將軍驃騎列傳》][902] | [JSON](5dd_l1c_6g8_A.json) |
| `B` | 衛青子發干侯 | [《史記・衛將軍驃騎列傳》][902] | [JSON](5dd_l1c_6g8_B.json) |
| `C` | 衛青子宜春侯（來源候選；預設不接父系） | [《史記・外戚世家》][840] | [JSON](5dd_l1c_6g8_C.json) |
| `D` | 衛伉 | [《史記・衛將軍驃騎列傳》][902] | [JSON](5dd_l1c_6g8_D.json) |

</details>

<details><summary><code>5dm_e40_rqh</code> 古公亶父（28 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 古公亶父 | [《史記・周本紀》][812] | [JSON](5dm_e40_rqh.json) |
| `A` | 仲雍 | [《史記・吳太伯世家》][822] | [JSON](5dm_e40_rqh_A.json) |
| `AA` | 季簡 | [《史記・吳太伯世家》][822] | [JSON](5dm_e40_rqh_AA.json) |
| `AAA` | 叔達 | [《史記・吳太伯世家》][822] | [JSON](5dm_e40_rqh_AAA.json) |
| `AAAA` | 周章（吳君） | [《史記・吳太伯世家》][822] | [JSON](5dm_e40_rqh_AAAA.json) |
| `AAAAA` | 熊遂 | [《史記・吳太伯世家》][822] | [JSON](5dm_e40_rqh_AAAAA.json) |
| `AAAAAA` | 柯相 | [《史記・吳太伯世家》][822] | [JSON](5dm_e40_rqh_AAAAAA.json) |
| `AAAAAAA` | 彊鳩夷 | [《史記・吳太伯世家》][822] | [JSON](5dm_e40_rqh_AAAAAAA.json) |
| `AAAAAAAA` | 餘橋疑吾 | [《史記・吳太伯世家》][822] | [JSON](5dm_e40_rqh_AAAAAAAA.json) |
| `AAAAAAAAA` | 柯盧 | [《史記・吳太伯世家》][822] | [JSON](5dm_e40_rqh_AAAAAAAAA.json) |
| `AAAAAAAAAA` | 周繇 | [《史記・吳太伯世家》][822] | [JSON](5dm_e40_rqh_AAAAAAAAAA.json) |
| `AAAAAAAAAAA` | 屈羽 | [《史記・吳太伯世家》][822] | [JSON](5dm_e40_rqh_AAAAAAAAAAA.json) |
| `AAAAAAAAAAAA` | 夷吾（吳君） | [《史記・吳太伯世家》][822] | [JSON](5dm_e40_rqh_AAAAAAAAAAAA.json) |
| `AAAAAAAAAAAAA` | 禽處 | [《史記・吳太伯世家》][822] | [JSON](5dm_e40_rqh_AAAAAAAAAAAAA.json) |
| `AAAAAAAAAAAAAA` | 轉（吳君） | [《史記・吳太伯世家》][822] | [JSON](5dm_e40_rqh_AAAAAAAAAAAAAA.json) |
| `AAAAAAAAAAAAAAA` | 頗髙 | [《史記・吳太伯世家》][822] | [JSON](5dm_e40_rqh_AAAAAAAAAAAAAAA.json) |
| `AAAAAAAAAAAAAAAA` | 句卑 | [《史記・吳太伯世家》][822] | [JSON](5dm_e40_rqh_AAAAAAAAAAAAAAAA.json) |
| `AAAAAAAAAAAAAAAAA` | 去齊 | [《史記・吳太伯世家》][822] | [JSON](5dm_e40_rqh_AAAAAAAAAAAAAAAAA.json) |
| `AAAAAAAAAAAAAAAAAA` | 壽夢 | [《史記・吳太伯世家》][822] | [JSON](5dm_e40_rqh_AAAAAAAAAAAAAAAAAA.json) |
| `AAAAAAAAAAAAAAAAAAA` | 諸樊 | [《史記・吳太伯世家》][822] | [JSON](5dm_e40_rqh_AAAAAAAAAAAAAAAAAAA.json) |
| `AAAAAAAAAAAAAAAAAAAA` | 闔閭 | [《史記・吳太伯世家》][822] | [JSON](5dm_e40_rqh_AAAAAAAAAAAAAAAAAAAA.json) |
| `AAAAAAAAAAAAAAAAAAAAA` | 夫差 | [《史記・越王勾踐世家》][832] | [JSON](5dm_e40_rqh_AAAAAAAAAAAAAAAAAAAAA.json) |
| `AAAAAAAAAAAAAAAAAAB` | 餘祭 | [《史記・吳太伯世家》][822] | [JSON](5dm_e40_rqh_AAAAAAAAAAAAAAAAAAB.json) |
| `AAAAAAAAAAAAAAAAAAC` | 餘眛 | [《史記・吳太伯世家》][822] | [JSON](5dm_e40_rqh_AAAAAAAAAAAAAAAAAAC.json) |
| `AAAAAAAAAAAAAAAAAACA` | 僚（吳王） | [《史記・吳太伯世家》][822] | [JSON](5dm_e40_rqh_AAAAAAAAAAAAAAAAAACA.json) |
| `AAAAAAAAAAAAAAAAAAD` | 季札 | [《史記・吳太伯世家》][822] | [JSON](5dm_e40_rqh_AAAAAAAAAAAAAAAAAAD.json) |
| `B` | 太伯 | [《史記・吳太伯世家》][822] | [JSON](5dm_e40_rqh_B.json) |
| `C` | 虞仲 | [《史記・周本紀》][812] | [JSON](5dm_e40_rqh_C.json) |

</details>

<details><summary><code>5if_pf6_zos</code> 郭解父（未名）（游俠列傳候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 郭解父（未名） | [《史記・游俠列傳》][915] | [JSON](5if_pf6_zos.json) |
| `A` | 郭解 | [《史記・游俠列傳》][915] | [JSON](5if_pf6_zos_A.json) |

</details>

<details><summary><code>5is_zik_jbp</code> 劉弘〔荊州刺史〕（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 劉弘〔荊州刺史〕 | [《晉書・劉弘 陶侃》][213] | [JSON](5is_zik_jbp.json) |
| `A` | 劉璠〔劉弘子〕 | [《晉書・山濤 王戎 郭舒 樂廣》][162]、[《晉書・劉弘 陶侃》][213] | [JSON](5is_zik_jbp_A.json) |

</details>

<details><summary><code>5jc_z9b_i2n</code> 柳卓（12 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 柳卓 | [《宋書・柳元景 顏師伯 沈慶之》][1091] | [JSON](5jc_z9b_i2n.json) |
| `A` | 柳恬 | [《宋書・柳元景 顏師伯 沈慶之》][1091] | [JSON](5jc_z9b_i2n_A.json) |
| `AA` | 柳憑 | [《南齊書・柳世隆 張瑰》][424]、[《宋書・柳元景 顏師伯 沈慶之》][1091] | [JSON](5jc_z9b_i2n_AA.json) |
| `AAA` | 柳叔宗 | [《南齊書・柳世隆 張瑰》][424] | [JSON](5jc_z9b_i2n_AAA.json) |
| `AAAA` | 柳世隆 | [《南齊書・柳世隆 張瑰》][424] | [JSON](5jc_z9b_i2n_AAAA.json) |
| `AAB` | 柳元景 | [《宋書・朱脩之 宗愨 王玄謨》][1089] | [JSON](5jc_z9b_i2n_AAB.json) |
| `AAC` | 柳僧景（柳元景弟） | [《宋書・朱脩之 宗愨 王玄謨》][1089] | [JSON](5jc_z9b_i2n_AAC.json) |
| `AAD` | 柳叔珍（義陽內史） | [《南史・柳元景》][702] | [JSON](5jc_z9b_i2n_AAD.json) |
| `AADA` | 柳慶遠（字文和） | [《南史・柳元景》][702] | [JSON](5jc_z9b_i2n_AADA.json) |
| `AADAA` | 柳津（字元舉） | [《南史・柳元景》][702] | [JSON](5jc_z9b_i2n_AADAA.json) |
| `AADAAA` | 柳仲禮（司州刺史） | [《梁書・韋粲 江子一 弟子四 子五 張嵊 沈浚 柳敬禮》][375]、[《梁書・韋粲 江子一 弟子四 子五 張嵊 沈浚 柳敬禮》][377] | [JSON](5jc_z9b_i2n_AADAAA.json) |
| `AADAAB` | 柳敬禮（柳仲禮弟） | [《梁書・韋粲 江子一 弟子四 子五 張嵊 沈浚 柳敬禮》][375] | [JSON](5jc_z9b_i2n_AADAAB.json) |

</details>

<details><summary><code>5km_89r_9jr</code> 元君（衛嗣君弟）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 元君（衛嗣君弟） | [《史記・衛康叔世家》][828] | [JSON](5km_89r_9jr.json) |
| `A` | 衛君角 | [《史記・衛康叔世家》][828] | [JSON](5km_89r_9jr_A.json) |

</details>

<details><summary><code>5pw_05i_uhv</code> 平（本文燕昭王）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 平（本文燕昭王） | [《史記・樂毅列傳》][871] | [JSON](5pw_05i_uhv.json) |
| `A` | 惠王（燕昭王子） | [《史記・樂毅列傳》][871] | [JSON](5pw_05i_uhv_A.json) |

</details>

<details><summary><code>5ql_hfz_086</code> 房叔安（字子仁）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 房叔安（字子仁） | [《南史・王鎮惡　朱齡石　毛脩之　傅弘之　朱脩之　王玄謨》][568]、[《南史・王鎮惡　朱齡石　毛脩之　傅弘之　朱脩之　王玄謨》][570] | [JSON](5ql_hfz_086.json) |
| `A` | 房長瑜（房叔安子） | [《南齊書・王奐 從弟繢 張沖》][495]、[《南史・王鎮惡　朱齡石　毛脩之　傅弘之　朱脩之　王玄謨》][566]、[《南史・王鎮惡　朱齡石　毛脩之　傅弘之　朱脩之　王玄謨》][567] | [JSON](5ql_hfz_086_A.json) |

</details>

<details><summary><code>5we_446_pbb</code> 荀永（荀伯玉祖）（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 荀永（荀伯玉祖） | [《南齊書・江謐 荀伯玉》][438] | [JSON](5we_446_pbb.json) |
| `A` | 荀闡之（荀伯玉父） | [《南齊書・江謐 荀伯玉》][438] | [JSON](5we_446_pbb_A.json) |
| `AA` | 荀伯玉（字弄璋） | [《南齊書・江謐 荀伯玉》][438] | [JSON](5we_446_pbb_AA.json) |

</details>

<details><summary><code>5xt_rg8_7zs</code> 項燕（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 項燕 | [《史記・秦始皇本紀》][814]、[《史記・六國年表》][1224] | [JSON](5xt_rg8_7zs.json) |
| `A` | 項梁 | [《史記・項羽本紀》][815] | [JSON](5xt_rg8_7zs_A.json) |

</details>

<details><summary><code>5ye_fwj_neh</code> 陳文帝蒨（4 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 陳文帝蒨 | [《陳書・列傳第十一: 王沖 王通 袁敬》][27] | [JSON](5ye_fwj_neh.json) |
| `A` | 陳伯山（鄱陽王） | [《陳書・列傳第二十二: 世祖九王 高宗二十九王 後主諸子》][42] | [JSON](5ye_fwj_neh_A.json) |
| `B` | 陳伯信（衡陽王） | [《陳書・列傳第八: 衡陽獻王昌 南康愍王曇朗》][24]、[《陳書・列傳第二十二: 世祖九王 高宗二十九王 後主諸子》][42] | [JSON](5ye_fwj_neh_B.json) |
| `C` | 陳伯智（永陽王） | [《陳書・列傳第二十二: 世祖九王 高宗二十九王 後主諸子》][42] | [JSON](5ye_fwj_neh_C.json) |

</details>

<details><summary><code>603_131_11e</code> 楊駿（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 楊駿 | [《晉書・汝南王亮 楚王瑋 趙王倫 齊王冏 長沙王乂 成都王潁 河間王顒 東海王越》][202] | [JSON](603_131_11e.json) |
| `A` | 楊芷〔武悼楊皇后〕 | [《晉書・后妃上》][142] | [JSON](603_131_11e_A.json) |

</details>

<details><summary><code>62o_3do_q72</code> 游幼（游明根父）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 游幼（游明根父） | [《魏書・游明根 劉芳》][1170] | [JSON](62o_3do_q72.json) |
| `A` | 游明根（字志遠） | [《魏書・游明根 劉芳》][1170] | [JSON](62o_3do_q72_A.json) |

</details>

<details><summary><code>684_eaa_511</code> 謝景仁（5 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 謝景仁 | [《宋書・庾悅 王誕 謝景仁 袁湛 褚叔度》][1053] | [JSON](684_eaa_511.json) |
| `A` | 謝恂 | [《南史・謝晦　謝裕　謝方明　謝靈運》][591] | [JSON](684_eaa_511_A.json) |
| `AA` | 謝孺子 | [《南史・謝晦　謝裕　謝方明　謝靈運》][591] | [JSON](684_eaa_511_AA.json) |
| `AAA` | 謝璟 | [《梁書・文學下》][391]、[《梁書・文學下》][390] | [JSON](684_eaa_511_AAA.json) |
| `AAAA` | 謝微 | [《梁書・文學下》][391]、[《梁書・文學下》][390] | [JSON](684_eaa_511_AAAA.json) |

</details>

<details><summary><code>696_456_df6</code> 荀曇（6 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 荀曇 | [《三國志・二荀賈傳》][736] | [JSON](696_456_df6.json) |
| `A` | 荀彞 | [《三國志・二荀賈傳》][736] | [JSON](696_456_df6_A.json) |
| `AA` | 荀攸 | [《三國志・二荀賈傳》][736] | [JSON](696_456_df6_AA.json) |
| `AA*A` | 荀彪 | [《三國志・二荀賈傳》][736] | [JSON](696_456_df6_AA%2AA.json) |
| `AAA` | 荀緝 | [《三國志・二荀賈傳》][736] | [JSON](696_456_df6_AAA.json) |
| `AAB` | 荀適 | [《三國志・二荀賈傳》][736] | [JSON](696_456_df6_AAB.json) |

</details>

<details><summary><code>69x_se2_859</code> 邴吉（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 邴吉 | [《史記・張丞相列傳》][887] | [JSON](69x_se2_859.json) |
| `A` | 邴顯 | [《史記・張丞相列傳》][887] | [JSON](69x_se2_859_A.json) |

</details>

<details><summary><code>6bn_yfc_lzi</code> 田叔（梁孝王世家候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 田叔 | [《史記・田叔列傳》][895] | [JSON](6bn_yfc_lzi.json) |
| `A` | 田仁 | [《史記・田叔列傳》][895] | [JSON](6bn_yfc_lzi_A.json) |

</details>

<details><summary><code>6d6_eg1_o3a</code> 王仲（外戚世家候選）（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 王仲 | [《史記・外戚世家》][840] | [JSON](6d6_eg1_o3a.json) |
| `A` | 王太后 | [《史記・外戚世家》][840] | [JSON](6d6_eg1_o3a_A.json) |
| `B` | 王信 | [《史記・絳侯周勃世家》][848] | [JSON](6d6_eg1_o3a_B.json) |

</details>

<details><summary><code>6di_ywz_ju4</code> 莊伯（晉曲沃弒君記事）（13 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 莊伯（晉曲沃弒君記事） | [《史記・晉世家》][830] | [JSON](6di_ywz_ju4.json) |
| `A` | 稱（曲沃／晉武公） | [《史記・晉世家》][830] | [JSON](6di_ywz_ju4_A.json) |
| `AA` | 晉獻公 | [《史記・晉世家》][830] | [JSON](6di_ywz_ju4_AA.json) |
| `AAA` | 晉文公 | [《史記・晉世家》][830] | [JSON](6di_ywz_ju4_AAA.json) |
| `AAAA` | 伯鯈（重耳子） | [《史記・晉世家》][830] | [JSON](6di_ywz_ju4_AAAA.json) |
| `AAAB` | 叔劉（重耳子） | [《史記・晉世家》][830] | [JSON](6di_ywz_ju4_AAAB.json) |
| `AAAC` | 黑臀（晉成公） | [《史記・晉世家》][830] | [JSON](6di_ywz_ju4_AAAC.json) |
| `AAAD` | 晉襄公 | [《史記・晉世家》][830] | [JSON](6di_ywz_ju4_AAAD.json) |
| `AAADA` | 捷（晉襄公少子桓叔） | [《史記・晉世家》][830] | [JSON](6di_ywz_ju4_AAADA.json) |
| `AAADAA` | 談（惠伯） | [《史記・晉世家》][830] | [JSON](6di_ywz_ju4_AAADAA.json) |
| `AAADAAA` | 晉悼公 | [《史記・晉世家》][830] | [JSON](6di_ywz_ju4_AAADAAA.json) |
| `AAB` | 申生 | [《史記・晉世家》][830] | [JSON](6di_ywz_ju4_AAB.json) |
| `AAC` | 奚齊 | [《史記・晉世家》][830] | [JSON](6di_ywz_ju4_AAC.json) |

</details>

<details><summary><code>6f6_d1e_11a</code> 道素（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 道素 | [《晉書・王沈 荀顗 荀勖 馮紞》][158] | [JSON](6f6_d1e_11a.json) |
| `A` | 崇之 | [《晉書・王沈 荀顗 荀勖 馮紞》][158] | [JSON](6f6_d1e_11a_A.json) |

</details>

<details><summary><code>6fg_r6l_5a5</code> 嵇康（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 嵇康 | [《晉書・忠義》][257] | [JSON](6fg_r6l_5a5.json) |
| `A` | 嵇紹 | [《晉書・忠義》][257] | [JSON](6fg_r6l_5a5_A.json) |
| `AA` | 嵇軫 | [《晉書・忠義》][257] | [JSON](6fg_r6l_5a5_AA.json) |

</details>

<details><summary><code>6fs_tis_zoa</code> 褚湛之（字休玄，褚淵、褚澄父）（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 褚湛之（字休玄，褚淵、褚澄父） | [《南史・褚裕之》][688]、[《宋書・庾悅 王誕 謝景仁 袁湛 褚叔度》][1049] | [JSON](6fs_tis_zoa.json) |
| `A` | 褚澄（褚湛之子，吳郡太守） | [《南史・后妃上》][524]、[《南史・后妃上》][525]、[《南史・王誕　王華　王惠　王彧》][655] | [JSON](6fs_tis_zoa_A.json) |
| `AA` | 褚令璩（齊東昏侯皇后） | [《南齊書・皇后》][407]、[《南齊書・皇后》][406]、[《南史・后妃上》][524]、[《南史・后妃上》][525] | [JSON](6fs_tis_zoa_AA.json) |

</details>

<details><summary><code>6i2_3jw_38a</code> 何瑀兄（何亮父，未名）（5 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 何瑀兄（何亮父，未名） | — | [JSON](6i2_3jw_38a.json) |
| `A` | 何亮（何瑀兄子） | [《宋書・后妃》][1013] | [JSON](6i2_3jw_38a_A.json) |
| `B` | 何恢（何亮弟） | [《宋書・后妃》][1013] | [JSON](6i2_3jw_38a_B.json) |
| `C` | 何誕（何恢弟，司徒右長史） | [《宋書・后妃》][1013] | [JSON](6i2_3jw_38a_C.json) |
| `D` | 何衍（何瑀兄子） | [《南史・后妃上》][529]、[《宋書・后妃》][1013] | [JSON](6i2_3jw_38a_D.json) |

</details>

<details><summary><code>6ks_x4x_dbf</code> 臧荼（外戚世家候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 臧荼 | [《史記・外戚世家》][840] | [JSON](6ks_x4x_dbf.json) |
| `*A` | 臧兒 | [《史記・外戚世家》][840] | [JSON](6ks_x4x_dbf_%2AA.json) |

</details>

<details><summary><code>6lr_zci_i0j</code> 郗鑒（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 郗鑒 | [《晉書・溫嶠 郗鑒》][216] | [JSON](6lr_zci_i0j.json) |
| `A` | 郗璿 | [《世說新語・雅量》][947] | [JSON](6lr_zci_i0j_A.json) |

</details>

<details><summary><code>6nu_h6f_w7t</code> 范慎〔吳太尉〕（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 范慎〔吳太尉〕 | [《三國志・吳主五子傳》][803] | [JSON](6nu_h6f_w7t.json) |
| `A` | 范耀 | [《三國志・吳主五子傳》][803] | [JSON](6nu_h6f_w7t_A.json) |

</details>

<details><summary><code>6oy_t19_ywe</code> 秦惠王（蘇秦列傳候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 秦惠王 | [《史記・蘇秦列傳》][860] | [JSON](6oy_t19_ywe.json) |
| `A` | 秦惠王女 | [《史記・蘇秦列傳》][860] | [JSON](6oy_t19_ywe_A.json) |

</details>

<details><summary><code>6v8_pk9_7k5</code> 溫嶠（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 溫嶠 | [《晉書・溫嶠 郗鑒》][214] | [JSON](6v8_pk9_7k5.json) |
| `A` | 溫放之 | [《晉書・溫嶠 郗鑒》][214] | [JSON](6v8_pk9_7k5_A.json) |
| `B` | 溫式之 | [《溫嶠墓誌・節錄》][53] | [JSON](6v8_pk9_7k5_B.json) |

</details>

<details><summary><code>6wx_fr3_b2e</code> 滿（陳胡公）（8 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 滿（陳胡公） | [《史記・陳杞世家》][827] | [JSON](6wx_fr3_b2e.json) |
| `A` | 犀侯（陳申公） | [《史記・陳杞世家》][827] | [JSON](6wx_fr3_b2e_A.json) |
| `AA` | 突（陳孝公） | [《史記・陳杞世家》][827] | [JSON](6wx_fr3_b2e_AA.json) |
| `AAA` | 圉戎（陳慎公） | [《史記・陳杞世家》][827] | [JSON](6wx_fr3_b2e_AAA.json) |
| `AAAA` | 寧（陳幽公） | [《史記・陳杞世家》][827] | [JSON](6wx_fr3_b2e_AAAA.json) |
| `AAAAA` | 孝（陳釐公） | [《史記・陳杞世家》][827] | [JSON](6wx_fr3_b2e_AAAAA.json) |
| `AAAAAA` | 靈（陳武公） | [《史記・陳杞世家》][827] | [JSON](6wx_fr3_b2e_AAAAAA.json) |
| `AAAAAAA` | 說（陳夷公） | [《史記・陳杞世家》][827] | [JSON](6wx_fr3_b2e_AAAAAAA.json) |

</details>

<details><summary><code>70o_j6h_wpc</code> 鄭旻（鄭萬頃父）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 鄭旻（鄭萬頃父） | [《陳書・列傳第八: 衡陽獻王昌 南康愍王曇朗》][25] | [JSON](70o_j6h_wpc.json) |
| `A` | 鄭萬頃（豐州刺史） | [《陳書・列傳第八: 衡陽獻王昌 南康愍王曇朗》][24] | [JSON](70o_j6h_wpc_A.json) |

</details>

<details><summary><code>719_b25_cc3</code> 庾深之（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 庾深之 | [《南齊書・虞玩之 劉休 沈沖 庾杲之 王諶》][455] | [JSON](719_b25_cc3.json) |
| `A` | 庾粲 | [《南齊書・虞玩之 劉休 沈沖 庾杲之 王諶》][455] | [JSON](719_b25_cc3_A.json) |
| `AA` | 庾杲之 | [《南齊書・虞玩之 劉休 沈沖 庾杲之 王諶》][455] | [JSON](719_b25_cc3_AA.json) |

</details>

<details><summary><code>72e_1a7_3ac</code> 王准之（7 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 王准之 | [《宋書・范泰 王准之 王韶之 荀伯子》][1066] | [JSON](72e_1a7_3ac.json) |
| `A` | 王興之（王准之子） | [《南史・王裕之　王鎮之　王韶之　王悅之　王准之》][661]、[《南史・王裕之　王鎮之　王韶之　王悅之　王准之》][675]、[《宋書・范泰 王准之 王韶之 荀伯子》][1066] | [JSON](72e_1a7_3ac_A.json) |
| `AA` | 王進之（王輿之子） | [《南史・王裕之　王鎮之　王韶之　王悅之　王准之》][661] | [JSON](72e_1a7_3ac_AA.json) |
| `AAA` | 王清（王進之子，中廬公） | [《南史・王裕之　王鎮之　王韶之　王悅之　王准之》][664] | [JSON](72e_1a7_3ac_AAA.json) |
| `AAAA` | 王猛（字世雄，本名勇） | [《南史・王裕之　王鎮之　王韶之　王悅之　王准之》][663] | [JSON](72e_1a7_3ac_AAAA.json) |
| `AAAAA` | 王繕（王猛長子） | [《南史・王裕之　王鎮之　王韶之　王悅之　王准之》][663] | [JSON](72e_1a7_3ac_AAAAA.json) |
| `AAAAB` | 王續（王繕弟） | [《南史・王裕之　王鎮之　王韶之　王悅之　王准之》][663] | [JSON](72e_1a7_3ac_AAAAB.json) |

</details>

<details><summary><code>766_5dq_zws</code> 朱家（季布欒布列傳候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 朱家 | [《史記・季布欒布列傳》][891] | [JSON](766_5dq_zws.json) |
| `A` | 朱家子未名 | [《史記・季布欒布列傳》][891] | [JSON](766_5dq_zws_A.json) |

</details>

<details><summary><code>77h_id3_a0i</code> 陸邵（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 陸邵 | [《南齊書・劉瓛 弟璡 陸澄》][464]、[《南史・陸澄　陸慧曉　陸杲》][712] | [JSON](77h_id3_a0i.json) |
| `A` | 陸瑗 | [《南齊書・劉瓛 弟璡 陸澄》][464]、[《南史・陸澄　陸慧曉　陸杲》][712] | [JSON](77h_id3_a0i_A.json) |
| `AA` | 陸澄 | [《南齊書・褚淵 淵弟澄 徐嗣 王儉》][423]、[《南史・王曇首》][618] | [JSON](77h_id3_a0i_AA.json) |

</details>

<details><summary><code>77n_qzq_xi3</code> 石鑒〔西晉太尉，字林伯〕（6 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 石鑒〔西晉太尉，字林伯〕 | [《晉書・鄭袤 李胤 盧欽 華表 石鑒 溫羨》][183] | [JSON](77n_qzq_xi3.json) |
| `A` | 石尠〔城陽簡侯，字處約〕 | [《晉城陽簡侯石尠墓誌・節錄》][48] | [JSON](77n_qzq_xi3_A.json) |
| `AA` | 石定〔字庶公〕 | [《處士石定墓誌・節錄》][47] | [JSON](77n_qzq_xi3_AA.json) |
| `AB` | 石邁〔字庶昆〕 | [《晉城陽簡侯石尠墓誌・節錄》][48] | [JSON](77n_qzq_xi3_AB.json) |
| `AC` | 石恭〔石尠庶子〕 | [《晉城陽簡侯石尠墓誌・節錄》][48] | [JSON](77n_qzq_xi3_AC.json) |
| `AD` | 石氏〔字令脩〕 | [《晉城陽簡侯石尠墓誌・節錄》][48] | [JSON](77n_qzq_xi3_AD.json) |

</details>

<details><summary><code>78u_8ii_bnr</code> 專諸（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 專諸 | [《史記・刺客列傳》][877] | [JSON](78u_8ii_bnr.json) |
| `A` | 專諸子（本卷未名） | [《史記・吳太伯世家》][822]、[《史記・刺客列傳》][877] | [JSON](78u_8ii_bnr_A.json) |

</details>

<details><summary><code>796_nkw_0jz</code> 張蒼父未名（張丞相列傳候選）（4 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 張蒼父未名 | [《史記・張丞相列傳》][887] | [JSON](796_nkw_0jz.json) |
| `A` | 張蒼 | [《史記・張丞相列傳》][887] | [JSON](796_nkw_0jz_A.json) |
| `AA` | 張蒼子未名（康侯） | [《史記・張丞相列傳》][887] | [JSON](796_nkw_0jz_AA.json) |
| `AAA` | 張類 | [《史記・張丞相列傳》][887] | [JSON](796_nkw_0jz_AAA.json) |

</details>

<details><summary><code>7a0_95e_c4a</code> 王敬則（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 王敬則 | [《南齊書・王融 謝朓》][493] | [JSON](7a0_95e_c4a.json) |
| `A` | 王敬則女（謝朓妻，未名） | — | [JSON](7a0_95e_c4a_A.json) |

</details>

<details><summary><code>7ad_718_47c</code> 王慧龍（8 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 王慧龍 | [《魏書・刁雍 王慧龍 韓延之 袁式》][1168] | [JSON](7ad_718_47c.json) |
| `A` | 王寶興 | [《魏書・刁雍 王慧龍 韓延之 袁式》][1168] | [JSON](7ad_718_47c_A.json) |
| `AA` | 王瓊 | [《魏書・刁雍 王慧龍 韓延之 袁式》][1168] | [JSON](7ad_718_47c_AA.json) |
| `AAA` | 王遵業 | [《魏書・刁雍 王慧龍 韓延之 袁式》][1168] | [JSON](7ad_718_47c_AAA.json) |
| `AAAA` | 王松年 | [《魏書・刁雍 王慧龍 韓延之 袁式》][1168] | [JSON](7ad_718_47c_AAAA.json) |
| `AAB` | 王瓊長女〔入嬪，未名〕 | [《魏書・刁雍 王慧龍 韓延之 袁式》][1168] | [JSON](7ad_718_47c_AAB.json) |
| `AAC` | 王瓊女〔盧道亮妻，未名〕 | [《魏書・刁雍 王慧龍 韓延之 袁式》][1168] | [JSON](7ad_718_47c_AAC.json) |
| `B` | 王慧龍女〔未名〕 | [《魏書・刁雍 王慧龍 韓延之 袁式》][1168] | [JSON](7ad_718_47c_B.json) |

</details>

<details><summary><code>7b9_110_008</code> 韋端（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 韋端 | [《三國志・二荀賈傳》][736] | [JSON](7b9_110_008.json) |
| `A` | 韋康 | [《三國志・二荀賈傳》][736] | [JSON](7b9_110_008_A.json) |

</details>

<details><summary><code>7du_pfa_2s5</code> 蹇叔（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 蹇叔 | [《史記・秦本紀》][813] | [JSON](7du_pfa_2s5.json) |
| `A` | 西乞術 | [《史記・秦本紀》][813]、[《史記・晉世家》][830] | [JSON](7du_pfa_2s5_A.json) |
| `B` | 白乙丙 | [《史記・秦本紀》][813]、[《史記・晉世家》][830] | [JSON](7du_pfa_2s5_B.json) |

</details>

<details><summary><code>7dv_lqp_y4z</code> 靳歙（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 靳歙 | [《漢書・樊酈滕灌傅靳周傳》][66] | [JSON](7dv_lqp_y4z.json) |
| `A` | 靳亭 | [《史記・高祖功臣侯者年表》][1227] | [JSON](7dv_lqp_y4z_A.json) |

</details>

<details><summary><code>7ec_qvv_x1c</code> 陸績（4 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 陸績 | [《三國志・虞陸張駱陸吾朱傳》][790] | [JSON](7ec_qvv_x1c.json) |
| `A` | 陸宏 | [《三國志・虞陸張駱陸吾朱傳》][790] | [JSON](7ec_qvv_x1c_A.json) |
| `B` | 陸睿 | [《三國志・虞陸張駱陸吾朱傳》][790] | [JSON](7ec_qvv_x1c_B.json) |
| `C` | 陸鬱生 | [《三國志・虞陸張駱陸吾朱傳》][790] | [JSON](7ec_qvv_x1c_C.json) |

</details>

<details><summary><code>7hw_8jq_c1e</code> 楊暉〔鈞祖，弘農簡公原記〕（9 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 楊暉〔鈞祖，弘農簡公原記〕 | [《魏書・楊播》][1173] | [JSON](7hw_8jq_c1e.json) |
| `A` | 楊恩〔鈞父〕 | [《魏書・楊播》][1173] | [JSON](7hw_8jq_c1e_A.json) |
| `AA` | 楊鈞〔恒州刺史〕 | [《魏書・楊播》][1173] | [JSON](7hw_8jq_c1e_AA.json) |
| `AAA` | 楊暄〔鈞長子〕 | [《魏書・楊播》][1173] | [JSON](7hw_8jq_c1e_AAA.json) |
| `AAAA` | 楊敷（楊素父） | [《隋書・列傳第13 楊素》][1145] | [JSON](7hw_8jq_c1e_AAAA.json) |
| `AAAAA` | 楊素（字處道） | [《隋書・列傳第13 楊素》][1145] | [JSON](7hw_8jq_c1e_AAAAA.json) |
| `AAB` | 楊穆〔暄弟〕 | [《魏書・楊播》][1173] | [JSON](7hw_8jq_c1e_AAB.json) |
| `AAC` | 楊儉〔穆弟〕 | [《魏書・楊播》][1173] | [JSON](7hw_8jq_c1e_AAC.json) |
| `AAD` | 楊寬〔儉弟〕 | [《魏書・楊播》][1173] | [JSON](7hw_8jq_c1e_AAD.json) |

</details>

<details><summary><code>7l6_9t8_q1p</code> 莊王（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 莊王 | [《史記・周本紀》][812] | [JSON](7l6_9t8_q1p.json) |
| `A` | 胡〔張昭論所稱周莊王子〕 | [《三國志・張顧諸葛步傳》][782] | [JSON](7l6_9t8_q1p_A.json) |

</details>

<details><summary><code>7mz_d13_9ka</code> 田氏（外戚世家候選）（4 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 田氏 | [《史記・外戚世家》][840] | [JSON](7mz_d13_9ka.json) |
| `A` | 田蚡 | [《史記・魏其武安列傳》][898] | [JSON](7mz_d13_9ka_A.json) |
| `AA` | 恬（田蚡子） | [《史記・魏其武安列傳》][898] | [JSON](7mz_d13_9ka_AA.json) |
| `B` | 勝 | [《史記・外戚世家》][840]、[《史記・魏其武安列傳》][898] | [JSON](7mz_d13_9ka_B.json) |

</details>

<details><summary><code>7r6_k52_qji</code> 王仁（161 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 王仁 | [《晉書・王祥 鄭沖 何曾 石苞》][151] | [JSON](7r6_k52_qji.json) |
| `A` | 王融 | [《晉書・王祥 鄭沖 何曾 石苞》][151]、[《世說新語・德行》][922] | [JSON](7r6_k52_qji_A.json) |
| `AA` | 王祥 | [《晉書・王祥 鄭沖 何曾 石苞》][151] | [JSON](7r6_k52_qji_AA.json) |
| `AAA` | 王肇 | [《晉書・王祥 鄭沖 何曾 石苞》][151] | [JSON](7r6_k52_qji_AAA.json) |
| `AAAA` | 王俊 | [《晉書・王祥 鄭沖 何曾 石苞》][151] | [JSON](7r6_k52_qji_AAAA.json) |
| `AAAAA` | 王遐 | [《晉書・王祥 鄭沖 何曾 石苞》][151] | [JSON](7r6_k52_qji_AAAAA.json) |
| `AAB` | 王夏 | [《晉書・王祥 鄭沖 何曾 石苞》][151] | [JSON](7r6_k52_qji_AAB.json) |
| `AAC` | 王馥 | [《晉書・王祥 鄭沖 何曾 石苞》][151] | [JSON](7r6_k52_qji_AAC.json) |
| `AACA` | 王根 | [《晉書・王祥 鄭沖 何曾 石苞》][151] | [JSON](7r6_k52_qji_AACA.json) |
| `AAD` | 王烈 | [《晉書・王祥 鄭沖 何曾 石苞》][151] | [JSON](7r6_k52_qji_AAD.json) |
| `AAE` | 王芬 | [《晉書・王祥 鄭沖 何曾 石苞》][151] | [JSON](7r6_k52_qji_AAE.json) |
| `AB` | 王覽 | [《晉書・王祥 鄭沖 何曾 石苞》][151] | [JSON](7r6_k52_qji_AB.json) |
| `ABA` | 王裁 | [《晉書・王祥 鄭沖 何曾 石苞》][151] | [JSON](7r6_k52_qji_ABA.json) |
| `ABAA` | 王導 | [《晉書・王導》][212] | [JSON](7r6_k52_qji_ABAA.json) |
| `ABAAA` | 王洽 | [《晉書・王導》][212] | [JSON](7r6_k52_qji_ABAAA.json) |
| `ABAAAA` | 王珣 | [《晉書・王導》][212] | [JSON](7r6_k52_qji_ABAAAA.json) |
| `ABAAAAA` | 王弘 | [《宋書・劉穆之 王弘》][1022] | [JSON](7r6_k52_qji_ABAAAAA.json) |
| `ABAAAAAA` | 王錫 | [《宋書・王僧達 顏竣》][1087] | [JSON](7r6_k52_qji_ABAAAAAA.json) |
| `ABAAAAAAA` | 王僧亮 | [《南史・王弘》][606] | [JSON](7r6_k52_qji_ABAAAAAAA.json) |
| `ABAAAAAAB` | 王僧衍 | [《陳書・列傳第十一: 王沖 王通 袁敬》][27]、[《南史・王弘》][597]、[《南史・王弘》][606] | [JSON](7r6_k52_qji_ABAAAAAAB.json) |
| `ABAAAAAABA` | 王茂璋 | [《南史・王弘》][597] | [JSON](7r6_k52_qji_ABAAAAAABA.json) |
| `ABAAAAAABAA` | 王沖〔字長深〕 | [《陳書・列傳第十一: 王沖 王通 袁敬》][27] | [JSON](7r6_k52_qji_ABAAAAAABAA.json) |
| `ABAAAAAABAAA` | 王瑒 | [《南史・王弘》][607] | [JSON](7r6_k52_qji_ABAAAAAABAAA.json) |
| `ABAAAAAABAAB` | 王瑜〔陳使齊者〕 | [《南史・王弘》][608] | [JSON](7r6_k52_qji_ABAAAAAABAAB.json) |
| `ABAAAAAB` | 王僧達 | [《宋書・王僧達 顏竣》][1087] | [JSON](7r6_k52_qji_ABAAAAAB.json) |
| `ABAAAAABA` | 王道琰 | [《南齊書・王融 謝朓》][492]、[《南齊書・王融 謝朓》][491]、[《南史・王弘》][598]、[《宋書・王僧達 顏竣》][1087] | [JSON](7r6_k52_qji_ABAAAAABA.json) |
| `ABAAAAB` | 王虞 | [《南史・王弘》][599] | [JSON](7r6_k52_qji_ABAAAAB.json) |
| `ABAAAABA` | 王深 | [《南史・王弘》][599] | [JSON](7r6_k52_qji_ABAAAABA.json) |
| `ABAAAAC` | 王柳 | [《南史・王弘》][599]、[《南史・王弘》][610]、[《宋書・劉穆之 王弘》][1022] | [JSON](7r6_k52_qji_ABAAAAC.json) |
| `ABAAAACA` | 王猷（字世倫） | [《南史・王弘》][610] | [JSON](7r6_k52_qji_ABAAAACA.json) |
| `ABAAAACAA` | 王瞻 | [《梁書・王瞻 王志 王峻 王暕 子訓 王泰 王份 孫鍚 僉 張充 柳惲 蔡撙 江蒨》][341]、[《梁書・王瞻 王志 王峻 王暕 子訓 王泰 王份 孫鍚 僉 張充 柳惲 蔡撙 江蒨》][340] | [JSON](7r6_k52_qji_ABAAAACAA.json) |
| `ABAAAACAAA` | 王長玄 | [《梁書・王瞻 王志 王峻 王暕 子訓 王泰 王份 孫鍚 僉 張充 柳惲 蔡撙 江蒨》][341]、[《梁書・王瞻 王志 王峻 王暕 子訓 王泰 王份 孫鍚 僉 張充 柳惲 蔡撙 江蒨》][340]、[《南史・王弘》][610] | [JSON](7r6_k52_qji_ABAAAACAAA.json) |
| `ABAAAAD` | 王孺 | [《南史・王弘》][599]、[《宋書・劉穆之 王弘》][1022] | [JSON](7r6_k52_qji_ABAAAAD.json) |
| `ABAAAADA` | 王微 | [《宋書・羊欣 張敷 王微》][1069] | [JSON](7r6_k52_qji_ABAAAADA.json) |
| `ABAAAAE` | 王曇首 | [《宋書・王華 王曇首 殷景仁 沈演之》][1071] | [JSON](7r6_k52_qji_ABAAAAE.json) |
| `ABAAAAEA` | 王僧綽 | [《宋書・徐湛之 江湛 王僧綽》][1081] | [JSON](7r6_k52_qji_ABAAAAEA.json) |
| `ABAAAAEAA` | 王儉 | [《南史・王曇首》][618] | [JSON](7r6_k52_qji_ABAAAAEAA.json) |
| `ABAAAAEAA*A` | 王蕣華〔齊和帝皇后〕 | [《南齊書・皇后》][419]、[《南齊書・皇后》][418]、[《南史・后妃上》][543]、[《南史・后妃上》][544] | [JSON](7r6_k52_qji_ABAAAAEAA%2AA.json) |
| `ABAAAAEAAA` | 王騫 | [《南史・王曇首》][619] | [JSON](7r6_k52_qji_ABAAAAEAAA.json) |
| `ABAAAAEAAAA` | 王規 | [《南史・王曇首》][615] | [JSON](7r6_k52_qji_ABAAAAEAAAA.json) |
| `ABAAAAEAAAAA` | 王褒 | [《舊唐書・列傳第三十九: 狄仁傑 王方慶 姚璹》][297]、[《梁書・王規 劉瑴 宗懍 王承 褚翔 蕭介 從父兄洽 褚球 劉孺 弟覽 遵 劉潛 弟孝勝 孝威 孝先 殷芸 蕭幾》][367]、[《周書・列傳第33 王襃 庾信》][1192] | [JSON](7r6_k52_qji_ABAAAAEAAAAA.json) |
| `ABAAAAEAAAAAA` | 王鼒 | [《舊唐書・列傳第三十九: 狄仁傑 王方慶 姚璹》][297]、[《周書・列傳第33 王襃 庾信》][1192] | [JSON](7r6_k52_qji_ABAAAAEAAAAAA.json) |
| `ABAAAAEAAAAAAA` | 王弘直 | [《舊唐書・列傳第三十九: 狄仁傑 王方慶 姚璹》][297]、[《新唐書・王綝　韋思謙　陸元方　王及善　李日知　杜景佺　李懷遠》][1190] | [JSON](7r6_k52_qji_ABAAAAEAAAAAAA.json) |
| `ABAAAAEAAAAAAAA` | 王方慶 | [《舊唐書・列傳第三十九: 狄仁傑 王方慶 姚璹》][297]、[《新唐書・王綝　韋思謙　陸元方　王及善　李日知　杜景佺　李懷遠》][1190] | [JSON](7r6_k52_qji_ABAAAAEAAAAAAAA.json) |
| `ABAAAAEAAAAAAAAA` | 王光輔 | [《舊唐書・列傳第三十九: 狄仁傑 王方慶 姚璹》][297] | [JSON](7r6_k52_qji_ABAAAAEAAAAAAAAA.json) |
| `ABAAAAEAAAAAAAAB` | 王晙 | [《舊唐書・列傳第三十九: 狄仁傑 王方慶 姚璹》][297] | [JSON](7r6_k52_qji_ABAAAAEAAAAAAAAB.json) |
| `ABAAAAEAAAB` | 王靈賓（梁簡文帝皇后） | [《梁書・皇后》][313]、[《南史・后妃下》][558] | [JSON](7r6_k52_qji_ABAAAAEAAAB.json) |
| `ABAAAAEAAB` | 王暕（字思晦） | [《梁書・王瞻 王志 王峻 王暕 子訓 王泰 王份 孫鍚 僉 張充 柳惲 蔡撙 江蒨》][336] | [JSON](7r6_k52_qji_ABAAAAEAAB.json) |
| `ABAAAAEAABA` | 王承（字安期，王暕子） | [《南史・王曇首》][613] | [JSON](7r6_k52_qji_ABAAAAEAABA.json) |
| `ABAAAAEAABB` | 王幼（王承弟） | [《梁書・王瞻 王志 王峻 王暕 子訓 王泰 王份 孫鍚 僉 張充 柳惲 蔡撙 江蒨》][336]、[《南史・王曇首》][613]、[《南史・王曇首》][617] | [JSON](7r6_k52_qji_ABAAAAEAABB.json) |
| `ABAAAAEAABC` | 王訓（字懷範） | [《南史・王曇首》][626] | [JSON](7r6_k52_qji_ABAAAAEAABC.json) |
| `ABAAAAEAABD` | 王訏（王暕子） | [《梁書・王瞻 王志 王峻 王暕 子訓 王泰 王份 孫鍚 僉 張充 柳惲 蔡撙 江蒨》][336] | [JSON](7r6_k52_qji_ABAAAAEAABD.json) |
| `ABAAAAEAB` | 王遜 | [《南齊書・褚淵 淵弟澄 徐嗣 王儉》][423]、[《南史・王曇首》][618] | [JSON](7r6_k52_qji_ABAAAAEAB.json) |
| `ABAAAAEB` | 王僧虔 | [《南齊書・王僧虔 張緒》][453] | [JSON](7r6_k52_qji_ABAAAAEB.json) |
| `ABAAAAEBA` | 王慈 | [《南史・王曇首》][614] | [JSON](7r6_k52_qji_ABAAAAEBA.json) |
| `ABAAAAEBAA` | 王泰（字仲通） | [《南史・王曇首》][623] | [JSON](7r6_k52_qji_ABAAAAEBAA.json) |
| `ABAAAAEBAAA` | 王廓（王泰子） | [《梁書・王瞻 王志 王峻 王暕 子訓 王泰 王份 孫鍚 僉 張充 柳惲 蔡撙 江蒨》][338]、[《南史・王曇首》][623] | [JSON](7r6_k52_qji_ABAAAAEBAAA.json) |
| `ABAAAAEBAB` | 王觀（王慈子） | [《南史・王曇首》][614] | [JSON](7r6_k52_qji_ABAAAAEBAB.json) |
| `ABAAAAEBAC` | 王慈女（江夏王鋒妃） | — | [JSON](7r6_k52_qji_ABAAAAEBAC.json) |
| `ABAAAAEBAD` | 王韶明〔齊海陵王妃〕 | [《南齊書・皇后》][417]、[《南齊書・皇后》][416]、[《南史・后妃上》][541]、[《南史・后妃上》][542] | [JSON](7r6_k52_qji_ABAAAAEBAD.json) |
| `ABAAAAEBB` | 王寂 | [《南齊書・王僧虔 張緒》][453] | [JSON](7r6_k52_qji_ABAAAAEBB.json) |
| `ABAAAAEBC` | 王志 | [《南史・王曇首》][631] | [JSON](7r6_k52_qji_ABAAAAEBC.json) |
| `ABAAAAEBCA` | 王緝 | [《梁書・王瞻 王志 王峻 王暕 子訓 王泰 王份 孫鍚 僉 張充 柳惲 蔡撙 江蒨》][343]、[《梁書・王瞻 王志 王峻 王暕 子訓 王泰 王份 孫鍚 僉 張充 柳惲 蔡撙 江蒨》][342]、[《南史・王曇首》][631]、[《南史・王曇首》][630] | [JSON](7r6_k52_qji_ABAAAAEBCA.json) |
| `ABAAAAEBCB` | 王休 | [《梁書・王瞻 王志 王峻 王暕 子訓 王泰 王份 孫鍚 僉 張充 柳惲 蔡撙 江蒨》][343]、[《梁書・王瞻 王志 王峻 王暕 子訓 王泰 王份 孫鍚 僉 張充 柳惲 蔡撙 江蒨》][342]、[《南史・王曇首》][631]、[《南史・王曇首》][630] | [JSON](7r6_k52_qji_ABAAAAEBCB.json) |
| `ABAAAAEBCC` | 王諲 | [《梁書・王瞻 王志 王峻 王暕 子訓 王泰 王份 孫鍚 僉 張充 柳惲 蔡撙 江蒨》][343]、[《梁書・王瞻 王志 王峻 王暕 子訓 王泰 王份 孫鍚 僉 張充 柳惲 蔡撙 江蒨》][342]、[《南史・謝晦　謝裕　謝方明　謝靈運》][590]、[《南史・王曇首》][631]、[《南史・王曇首》][630] | [JSON](7r6_k52_qji_ABAAAAEBCC.json) |
| `ABAAAAEBCD` | 王操 | [《梁書・王瞻 王志 王峻 王暕 子訓 王泰 王份 孫鍚 僉 張充 柳惲 蔡撙 江蒨》][343]、[《梁書・王瞻 王志 王峻 王暕 子訓 王泰 王份 孫鍚 僉 張充 柳惲 蔡撙 江蒨》][342]、[《南史・王曇首》][631]、[《南史・王曇首》][630] | [JSON](7r6_k52_qji_ABAAAAEBCD.json) |
| `ABAAAAEBCE` | 王素 | [《梁書・王瞻 王志 王峻 王暕 子訓 王泰 王份 孫鍚 僉 張充 柳惲 蔡撙 江蒨》][343]、[《梁書・王瞻 王志 王峻 王暕 子訓 王泰 王份 孫鍚 僉 張充 柳惲 蔡撙 江蒨》][342]、[《南史・王曇首》][631]、[《南史・王曇首》][630] | [JSON](7r6_k52_qji_ABAAAAEBCE.json) |
| `ABAAAAEBD` | 王彬（字思文） | [《南史・王曇首》][612] | [JSON](7r6_k52_qji_ABAAAAEBD.json) |
| `ABAAAB` | 王瑉 | [《晉書・王導》][212] | [JSON](7r6_k52_qji_ABAAAB.json) |
| `ABAAABA` | 王朗（王瑉子） | [《晉書・王導》][212] | [JSON](7r6_k52_qji_ABAAABA.json) |
| `ABAAABB` | 王練 | [《宋書・劉穆之 王弘》][1022] | [JSON](7r6_k52_qji_ABAAABB.json) |
| `ABAAABBA` | 王釗 | [《宋書・劉穆之 王弘》][1022] | [JSON](7r6_k52_qji_ABAAABBA.json) |
| `ABAAB` | 王悅 | [《晉書・王導》][212] | [JSON](7r6_k52_qji_ABAAB.json) |
| `ABAAC` | 王恬 | [《晉書・王導》][212] | [JSON](7r6_k52_qji_ABAAC.json) |
| `ABAACA` | 王琨 | [《世說新語・排調》][986] | [JSON](7r6_k52_qji_ABAACA.json) |
| `ABAACAA` | 王嘏 | [《南史・王誕　王華　王惠　王彧》][634]、[《南史・王誕　王華　王惠　王彧》][633] | [JSON](7r6_k52_qji_ABAACAA.json) |
| `ABAACAAA` | 王恢（王嘏子） | [《晉書・王導》][212]、[《南史・王誕　王華　王惠　王彧》][634]、[《南史・王誕　王華　王惠　王彧》][633] | [JSON](7r6_k52_qji_ABAACAAA.json) |
| `ABAACAAB` | 王偃（字子游，王嘏子） | [《南史・王誕　王華　王惠　王彧》][634]、[《南史・王誕　王華　王惠　王彧》][633] | [JSON](7r6_k52_qji_ABAACAAB.json) |
| `ABAACAABA` | 王憲嫄（孝武文穆王皇后） | [《南史・后妃上》][545]、[《南史・后妃上》][546] | [JSON](7r6_k52_qji_ABAACAABA.json) |
| `ABAACAABB` | 王藻（王偃長子） | [《南史・王誕　王華　王惠　王彧》][656]、[《宋書・后妃》][1017] | [JSON](7r6_k52_qji_ABAACAABB.json) |
| `ABAACAABC` | 王懋（字昌業，王藻弟） | [《南史・王誕　王華　王惠　王彧》][653] | [JSON](7r6_k52_qji_ABAACAABC.json) |
| `ABAACAABCA` | 王瑩（字奉光，王懋子） | [《南史・王誕　王華　王惠　王彧》][653] | [JSON](7r6_k52_qji_ABAACAABCA.json) |
| `ABAACAABCAA` | 王實（王瑩少子） | [《南史・王誕　王華　王惠　王彧》][653] | [JSON](7r6_k52_qji_ABAACAABCAA.json) |
| `ABAACAABD` | 王攸（王懋弟） | [《南史・王誕　王華　王惠　王彧》][644] | [JSON](7r6_k52_qji_ABAACAABD.json) |
| `ABAACAABDA` | 王亮（字奉叔，王攸子） | [《南史・王誕　王華　王惠　王彧》][644] | [JSON](7r6_k52_qji_ABAACAABDA.json) |
| `ABAACAABE` | 王臻（王攸弟） | [《宋書・后妃》][1017] | [JSON](7r6_k52_qji_ABAACAABE.json) |
| `ABAAD` | 王協 | [《晉書・王導》][212] | [JSON](7r6_k52_qji_ABAAD.json) |
| `ABAAE` | 王邵 | [《晉書・王導》][212] | [JSON](7r6_k52_qji_ABAAE.json) |
| `ABAAED` | 王穆（王劭子） | [《晉書・王導》][212] | [JSON](7r6_k52_qji_ABAAED.json) |
| `ABAAEDA` | 王簡 | [《晉書・王導》][212] | [JSON](7r6_k52_qji_ABAAEDA.json) |
| `ABAAEDB` | 王智 | [《南史・王誕　王華　王惠　王彧》][654] | [JSON](7r6_k52_qji_ABAAEDB.json) |
| `ABAAEDC` | 王超 | [《晉書・王導》][212] | [JSON](7r6_k52_qji_ABAAEDC.json) |
| `ABAAEE` | 王默（王劭子） | [《晉書・王導》][212] | [JSON](7r6_k52_qji_ABAAEE.json) |
| `ABAAEEA` | 王鑒（王默子） | [《南史・王誕　王華　王惠　王彧》][642] | [JSON](7r6_k52_qji_ABAAEEA.json) |
| `ABAAEEB` | 王惠 | [《南史・王誕　王華　王惠　王彧》][642] | [JSON](7r6_k52_qji_ABAAEEB.json) |
| `ABAAEF` | 王恢（王劭子） | [《晉書・王導》][212] | [JSON](7r6_k52_qji_ABAAEF.json) |
| `ABAAF` | 王薈 | [《晉書・王導》][212] | [JSON](7r6_k52_qji_ABAAF.json) |
| `ABAAFA` | 王廞 | [《宋書・王華 王曇首 殷景仁 沈演之》][1071] | [JSON](7r6_k52_qji_ABAAFA.json) |
| `ABAAFAA` | 王泰 | [《晉書・王導》][212]、[《南史・王誕　王華　王惠　王彧》][639]、[《宋書・王華 王曇首 殷景仁 沈演之》][1071]、[《宋書・王華 王曇首 殷景仁 沈演之》][1072] | [JSON](7r6_k52_qji_ABAAFAA.json) |
| `ABAAFAB` | 王華 | [《宋書・王華 王曇首 殷景仁 沈演之》][1071] | [JSON](7r6_k52_qji_ABAAFAB.json) |
| `ABAAFABA` | 王嗣 | [《宋書・徐湛之 江湛 王僧綽》][1081] | [JSON](7r6_k52_qji_ABAAFABA.json) |
| `ABAAFABAA` | 王長 | [《南齊書・王琨 張岱 褚炫 何戢 王延之 阮韜》][444]、[《南史・王誕　王華　王惠　王彧》][643]、[《宋書・王華 王曇首 殷景仁 沈演之》][1071]、[《宋書・王華 王曇首 殷景仁 沈演之》][1072] | [JSON](7r6_k52_qji_ABAAFABAA.json) |
| `ABAAFAC` | 王廞女 | [《宋書・王華 王曇首 殷景仁 沈演之》][1071]、[《宋書・王華 王曇首 殷景仁 沈演之》][1072] | [JSON](7r6_k52_qji_ABAAFAC.json) |
| `ABAAFB` | 王懌 | [《南史・王誕　王華　王惠　王彧》][643] | [JSON](7r6_k52_qji_ABAAFB.json) |
| `ABAAFBA` | 王琨〔王懌子〕 | [《南史・王誕　王華　王惠　王彧》][643] | [JSON](7r6_k52_qji_ABAAFBA.json) |
| `ABAB` | 王穎 | [《世說新語・品藻》][968] | [JSON](7r6_k52_qji_ABAB.json) |
| `ABAC` | 王敞 | [《世說新語・品藻》][968] | [JSON](7r6_k52_qji_ABAC.json) |
| `ABB` | 王基 | [《晉書・王祥 鄭沖 何曾 石苞》][151] | [JSON](7r6_k52_qji_ABB.json) |
| `ABC` | 王會 | [《晉書・王祥 鄭沖 何曾 石苞》][151] | [JSON](7r6_k52_qji_ABC.json) |
| `ABD` | 王正 | [《晉書・王祥 鄭沖 何曾 石苞》][151] | [JSON](7r6_k52_qji_ABD.json) |
| `ABDA` | 王廙 | [《晉書・王舒 王廙 虞潭 顧眾 張闓》][247] | [JSON](7r6_k52_qji_ABDA.json) |
| `ABDAA` | 王頤之 | [《晉書・王舒 王廙 虞潭 顧眾 張闓》][247] | [JSON](7r6_k52_qji_ABDAA.json) |
| `ABDAB` | 王胡之 | [《晉書・王舒 王廙 虞潭 顧眾 張闓》][247] | [JSON](7r6_k52_qji_ABDAB.json) |
| `ABDABA` | 王茂之 | [《晉書・王舒 王廙 虞潭 顧眾 張闓》][247]、[《南史・范泰　荀伯子　徐廣　鄭鮮之　裴松之　何承天》][696]、[《宋書・鄭鮮之 裴松之 何承天》][1074]、[《宋書・王敬弘 何尚之》][1077]、[《宋書・王敬弘 何尚之》][1076] | [JSON](7r6_k52_qji_ABDABA.json) |
| `ABDABAA` | 王敬弘 | [《南史・王裕之　王鎮之　王韶之　王悅之　王准之》][677] | [JSON](7r6_k52_qji_ABDABAA.json) |
| `ABDABAAA` | 王恢之 | [《宋書・王敬弘 何尚之》][1077] | [JSON](7r6_k52_qji_ABDABAAA.json) |
| `ABDABAAB` | 王瓚之 | [《南史・王裕之　王鎮之　王韶之　王悅之　王准之》][677] | [JSON](7r6_k52_qji_ABDABAAB.json) |
| `ABDABAABA` | 王秀之 | [《南齊書・王秀之 王慈 蔡約 陸慧曉 顧憲之 蕭惠基》][490] | [JSON](7r6_k52_qji_ABDABAABA.json) |
| `ABDABAABAA` | 王峻 | [《梁書・王瞻 王志 王峻 王暕 子訓 王泰 王份 孫鍚 僉 張充 柳惲 蔡撙 江蒨》][337] | [JSON](7r6_k52_qji_ABDABAABAA.json) |
| `ABDABAABAAA` | 王琮 | [《梁書・王瞻 王志 王峻 王暕 子訓 王泰 王份 孫鍚 僉 張充 柳惲 蔡撙 江蒨》][337]、[《南史・王裕之　王鎮之　王韶之　王悅之　王准之》][677]、[《南史・王裕之　王鎮之　王韶之　王悅之　王准之》][662] | [JSON](7r6_k52_qji_ABDABAABAAA.json) |
| `ABDABAABAAB` | 王玩（王峻子） | [《梁書・王瞻 王志 王峻 王暕 子訓 王泰 王份 孫鍚 僉 張充 柳惲 蔡撙 江蒨》][337] | [JSON](7r6_k52_qji_ABDABAABAAB.json) |
| `ABDABAAC` | 王昇之 | [《南史・王裕之　王鎮之　王韶之　王悅之　王准之》][677]、[《宋書・王敬弘 何尚之》][1077] | [JSON](7r6_k52_qji_ABDABAAC.json) |
| `ABDABAACA` | 王延之 | [《南齊書・王琨 張岱 褚炫 何戢 王延之 阮韜》][452] | [JSON](7r6_k52_qji_ABDABAACA.json) |
| `ABDABAACAA` | 王倫之 | [《南史・王裕之　王鎮之　王韶之　王悅之　王准之》][677]、[《南史・王裕之　王鎮之　王韶之　王悅之　王准之》][676] | [JSON](7r6_k52_qji_ABDABAACAA.json) |
| `ABDABAACAAA` | 王昕（綸之子） | [《南史・王裕之　王鎮之　王韶之　王悅之　王准之》][677]、[《南史・王裕之　王鎮之　王韶之　王悅之　王准之》][676] | [JSON](7r6_k52_qji_ABDABAACAAA.json) |
| `ABDABAAD` | 王敬弘女（何述之妻，未名） | — | [JSON](7r6_k52_qji_ABDABAAD.json) |
| `ABDABAAE` | 王敬弘女（孔尚妻） | [《宋書・隱逸》][1138] | [JSON](7r6_k52_qji_ABDABAAE.json) |
| `ABDABB` | 王和之（字興道） | [《世說新語・輕詆》][987] | [JSON](7r6_k52_qji_ABDABB.json) |
| `ABDAC` | 王耆之 | [《世說新語・賞譽》][962] | [JSON](7r6_k52_qji_ABDAC.json) |
| `ABDACA` | 王隨之 | [《南史・王裕之　王鎮之　王韶之　王悅之　王准之》][677]、[《宋書・良吏》][1131]、[《宋書・良吏》][1127] | [JSON](7r6_k52_qji_ABDACA.json) |
| `ABDACAA` | 王鎮之 | [《宋書・良吏》][1131]、[《宋書・良吏》][1127] | [JSON](7r6_k52_qji_ABDACAA.json) |
| `ABDACAAA` | 王標之 | [《南史・王裕之　王鎮之　王韶之　王悅之　王准之》][677]、[《宋書・良吏》][1131]、[《宋書・良吏》][1127] | [JSON](7r6_k52_qji_ABDACAAA.json) |
| `ABDACAB` | 王弘之 | [《宋書・隱逸》][1138] | [JSON](7r6_k52_qji_ABDACAB.json) |
| `ABDACABA` | 王曇生 | [《宋書・隱逸》][1138] | [JSON](7r6_k52_qji_ABDACABA.json) |
| `ABDACABB` | 王普曜（王晏父） | [《南史・王裕之　王鎮之　王韶之　王悅之　王准之》][673] | [JSON](7r6_k52_qji_ABDACABB.json) |
| `ABDACABBA` | 王詡（王晏弟） | [《南齊書・王晏 蕭諶 蕭坦之 江祏》][474] | [JSON](7r6_k52_qji_ABDACABBA.json) |
| `ABDACABC` | 王羅雲（王思遠父） | [《古今姓氏書辯證・卷十四》][61]、[《南齊書・江斆 何昌㝢 謝𤅢 王思遠》][482]、[《南齊書・江斆 何昌㝢 謝𤅢 王思遠》][483]、[《南史・王裕之　王鎮之　王韶之　王悅之　王准之》][669] | [JSON](7r6_k52_qji_ABDACABC.json) |
| `ABDACABCA` | 王思玄（王思遠長兄） | [《南齊書・江斆 何昌㝢 謝𤅢 王思遠》][483]、[《南史・王裕之　王鎮之　王韶之　王悅之　王准之》][669] | [JSON](7r6_k52_qji_ABDACABCA.json) |
| `ABDACABCB` | 王思微（南史作思征） | [《南齊書・江斆 何昌㝢 謝𤅢 王思遠》][481]、[《南齊書・江斆 何昌㝢 謝𤅢 王思遠》][483]、[《南史・王裕之　王鎮之　王韶之　王悅之　王准之》][669] | [JSON](7r6_k52_qji_ABDACABCB.json) |
| `ABDAD` | 王羨之（鎮軍掾） | [《南史・王裕之　王鎮之　王韶之　王悅之　王准之》][668]、[《南史・王裕之　王鎮之　王韶之　王悅之　王准之》][667]、[《宋書・范泰 王准之 王韶之 荀伯子》][1065] | [JSON](7r6_k52_qji_ABDAD.json) |
| `ABDADA` | 王偉之（王韶之父） | [《南史・王裕之　王鎮之　王韶之　王悅之　王准之》][668]、[《南史・王裕之　王鎮之　王韶之　王悅之　王准之》][667]、[《宋書・范泰 王准之 王韶之 荀伯子》][1065] | [JSON](7r6_k52_qji_ABDADA.json) |
| `ABDB` | 王彬 | [《晉書・王舒 王廙 虞潭 顧眾 張闓》][240] | [JSON](7r6_k52_qji_ABDB.json) |
| `ABDBA` | 王彭之 | [《世說新語・輕詆》][988] | [JSON](7r6_k52_qji_ABDBA.json) |
| `ABDBAA` | 王建之（字榮妣） | [《王建之墓誌・全文》][49] | [JSON](7r6_k52_qji_ABDBAA.json) |
| `ABDBAAA` | 王玉龜（王建之大女） | [《劉媚子石墓誌・全文》][46]、[《王建之墓誌・全文》][49] | [JSON](7r6_k52_qji_ABDBAAA.json) |
| `ABDBAAB` | 王道末（王建之次女） | [《劉媚子石墓誌・全文》][46]、[《王建之墓誌・全文》][49] | [JSON](7r6_k52_qji_ABDBAAB.json) |
| `ABDBAAC` | 王張願（王建之小女） | [《劉媚子磚墓誌・現可釋讀部分》][45]、[《劉媚子石墓誌・全文》][46]、[《王建之墓誌・全文》][49] | [JSON](7r6_k52_qji_ABDBAAC.json) |
| `ABDBAAD` | 王紀之（字元萬） | [《劉媚子磚墓誌・現可釋讀部分》][45]、[《劉媚子石墓誌・全文》][46]、[《王建之墓誌・全文》][49] | [JSON](7r6_k52_qji_ABDBAAD.json) |
| `ABDBAB` | 王翹之（廬陵太守） | [《王建之墓誌・全文》][49] | [JSON](7r6_k52_qji_ABDBAB.json) |
| `ABDBAC` | 王朔之（王建之弟） | [《王建之墓誌・全文》][49] | [JSON](7r6_k52_qji_ABDBAC.json) |
| `ABDBB` | 王彪之 | [《晉書・王舒 王廙 虞潭 顧眾 張闓》][239] | [JSON](7r6_k52_qji_ABDBB.json) |
| `ABDBBA` | 王越之 | [《晉書・王舒 王廙 虞潭 顧眾 張闓》][239] | [JSON](7r6_k52_qji_ABDBBA.json) |
| `ABDBBB` | 王臨之 | [《宋書・范泰 王准之 王韶之 荀伯子》][1066] | [JSON](7r6_k52_qji_ABDBBB.json) |
| `ABDBBBA` | 王訥之（字永言） | [《宋書・范泰 王准之 王韶之 荀伯子》][1066] | [JSON](7r6_k52_qji_ABDBBBA.json) |
| `ABDBBBB` | 王瑰之（字道茂） | [《南史・王裕之　王鎮之　王韶之　王悅之　王准之》][666] | [JSON](7r6_k52_qji_ABDBBBB.json) |
| `ABDBC` | 興之〔本誌贛令〕 | [《王閩之墓誌・全文》][51] | [JSON](7r6_k52_qji_ABDBC.json) |
| `ABDBCA` | 王閩之 | [《王閩之墓誌・全文》][51] | [JSON](7r6_k52_qji_ABDBCA.json) |
| `ABE` | 王彥 | [《晉書・叛臣一》][282] | [JSON](7r6_k52_qji_ABE.json) |
| `ABF` | 王琛 | [《晉書・王祥 鄭沖 何曾 石苞》][151] | [JSON](7r6_k52_qji_ABF.json) |
| `ABFA` | 王棱 | [《晉書・王舒 王廙 虞潭 顧眾 張闓》][241] | [JSON](7r6_k52_qji_ABFA.json) |
| `ABFB` | 王侃 | [《晉書・王舒 王廙 虞潭 顧眾 張闓》][241] | [JSON](7r6_k52_qji_ABFB.json) |

</details>

<details><summary><code>7s2_h0m_msl</code> 蘇（曹戴伯）（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 蘇（曹戴伯） | [《史記・管蔡世家》][826] | [JSON](7s2_h0m_msl.json) |
| `A` | 兕（曹惠伯） | [《史記・管蔡世家》][826] | [JSON](7s2_h0m_msl_A.json) |
| `AA` | 石甫（曹惠伯子） | [《史記・管蔡世家》][826] | [JSON](7s2_h0m_msl_AA.json) |

</details>

<details><summary><code>7tc_utz_m7l</code> 駱統（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 駱統 | [《三國志・虞陸張駱陸吾朱傳》][792] | [JSON](7tc_utz_m7l.json) |
| `A` | 駱秀 | [《三國志・陸遜傳》][800] | [JSON](7tc_utz_m7l_A.json) |

</details>

<details><summary><code>7tm_3ss_4on</code> 周苛（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 周苛 | [《史記・張丞相列傳》][887] | [JSON](7tm_3ss_4on.json) |
| `*A` | 平（周苛孫） | [《史記・孝景本紀》][819] | [JSON](7tm_3ss_4on_%2AA.json) |
| `A` | 周成 | [《史記・張丞相列傳》][887] | [JSON](7tm_3ss_4on_A.json) |

</details>

<details><summary><code>7uk_oqn_ymk</code> 陳宣公杵臼（田世家候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 陳宣公杵臼 | [《史記・田敬仲完世家》][837] | [JSON](7uk_oqn_ymk.json) |
| `A` | 御寇 | [《史記・田敬仲完世家》][837] | [JSON](7uk_oqn_ymk_A.json) |

</details>

<details><summary><code>7zi_5gs_mq2</code> 華歆（12 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 華歆 | [《三國志・虞陸張駱陸吾朱傳》][795] | [JSON](7zi_5gs_mq2.json) |
| `A` | 華表〔字偉容〕 | [《晉書・鄭袤 李胤 盧欽 華表 石鑒 溫羨》][172] | [JSON](7zi_5gs_mq2_A.json) |
| `AA` | 華岑〔華表子〕 | [《晉書・鄭袤 李胤 盧欽 華表 石鑒 溫羨》][172] | [JSON](7zi_5gs_mq2_AA.json) |
| `AB` | 華嶠〔字叔駿〕 | [《晉書・鄭袤 李胤 盧欽 華表 石鑒 溫羨》][174] | [JSON](7zi_5gs_mq2_AB.json) |
| `ABA` | 華頤〔長樂內史〕 | [《晉書・鄭袤 李胤 盧欽 華表 石鑒 溫羨》][174] | [JSON](7zi_5gs_mq2_ABA.json) |
| `ABB` | 華徹〔華嶠中子〕 | [《晉書・鄭袤 李胤 盧欽 華表 石鑒 溫羨》][174] | [JSON](7zi_5gs_mq2_ABB.json) |
| `ABC` | 華暢〔華嶠少子〕 | [《晉書・鄭袤 李胤 盧欽 華表 石鑒 溫羨》][174] | [JSON](7zi_5gs_mq2_ABC.json) |
| `AC` | 華鑒〔華表子〕 | [《晉書・鄭袤 李胤 盧欽 華表 石鑒 溫羨》][172] | [JSON](7zi_5gs_mq2_AC.json) |
| `AD` | 華澹〔字玄駿〕 | [《晉書・鄭袤 李胤 盧欽 華表 石鑒 溫羨》][172]、[《晉書・周浚 成公簡 苟晞 華軼 劉喬》][203] | [JSON](7zi_5gs_mq2_AD.json) |
| `AE` | 華簡〔華表子〕 | [《晉書・鄭袤 李胤 盧欽 華表 石鑒 溫羨》][172] | [JSON](7zi_5gs_mq2_AE.json) |
| `B` | 華博〔華歆中子〕 | [《三國志・鍾繇華歆王朗傳》][740] | [JSON](7zi_5gs_mq2_B.json) |
| `C` | 華周〔華歆少子〕 | [《三國志・鍾繇華歆王朗傳》][740] | [JSON](7zi_5gs_mq2_C.json) |

</details>

<details><summary><code>82k_3oi_qf8</code> 山簡〔吊王衍幼子者〕（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 山簡〔吊王衍幼子者〕 | [《晉書・山濤 王戎 郭舒 樂廣》][164] | [JSON](82k_3oi_qf8.json) |
| `A` | 山遐〔字彥林〕 | [《晉書・山濤 王戎 郭舒 樂廣》][166] | [JSON](82k_3oi_qf8_A.json) |

</details>

<details><summary><code>85g_yq3_0w6</code> 王宰（王玄載祖）（4 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 王宰（王玄載祖） | [《南齊書・劉懷珍 李安民 王玄載》][433] | [JSON](85g_yq3_0w6.json) |
| `A` | 王蕤（王玄載父，東莞太守） | [《南齊書・劉懷珍 李安民 王玄載》][433]、[《南史・王鎮惡　朱齡石　毛脩之　傅弘之　朱脩之　王玄謨》][573] | [JSON](85g_yq3_0w6_A.json) |
| `AA` | 王玄載（字彥休） | [《南齊書・劉懷珍 李安民 王玄載》][433] | [JSON](85g_yq3_0w6_AA.json) |
| `AB` | 王玄邈〔齊安北將軍〕 | [《南齊書・劉懷珍 李安民 王玄載》][432] | [JSON](85g_yq3_0w6_AB.json) |

</details>

<details><summary><code>865_b69_cb0</code> 袁術（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 袁術 | [《三國志・二荀賈傳》][736] | [JSON](865_b69_cb0.json) |
| `A` | 袁氏〔袁術女、孫權夫人〕 | [《三國志・妃嬪傳》][765] | [JSON](865_b69_cb0_A.json) |

</details>

<details><summary><code>866_0fd_205</code> 劉表（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 劉表 | [《三國志・二荀賈傳》][736] | [JSON](866_0fd_205.json) |
| `A` | 劉脩 | [《三國志・任城陳蕭王傳》][748] | [JSON](866_0fd_205_A.json) |
| `B` | 劉琮 | [《三國志・二荀賈傳》][736]、[《三國志・吳主五子傳》][805] | [JSON](866_0fd_205_B.json) |

</details>

<details><summary><code>882_bd1_ca9</code> 李胤（5 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 李胤 | [《晉書・鄭袤 李胤 盧欽 華表 石鑒 溫羨》][177] | [JSON](882_bd1_ca9.json) |
| `A` | 李固〔字萬基〕 | [《晉書・鄭袤 李胤 盧欽 華表 石鑒 溫羨》][177] | [JSON](882_bd1_ca9_A.json) |
| `AA` | 李志〔字彥道〕 | [《晉書・鄭袤 李胤 盧欽 華表 石鑒 溫羨》][177] | [JSON](882_bd1_ca9_AA.json) |
| `B` | 李真長〔太僕卿〕 | [《晉書・鄭袤 李胤 盧欽 華表 石鑒 溫羨》][177] | [JSON](882_bd1_ca9_B.json) |
| `C` | 李修〔太弟中庶子〕 | [《晉書・鄭袤 李胤 盧欽 華表 石鑒 溫羨》][177] | [JSON](882_bd1_ca9_C.json) |

</details>

<details><summary><code>89c_afa_3eb</code> 單固父伯龍（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 單固父伯龍 | [《三國志・王毌丘諸葛鄧鍾傳》][756] | [JSON](89c_afa_3eb.json) |
| `A` | 單固 | [《三國志・王毌丘諸葛鄧鍾傳》][756] | [JSON](89c_afa_3eb_A.json) |

</details>

<details><summary><code>8c4_l2o_krm</code> 沈說道（巴西、梓潼二郡太守）（4 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 沈說道（巴西、梓潼二郡太守） | [《南齊書・良政》][517] | [JSON](8c4_l2o_krm.json) |
| `A` | 沈璞之（北中郎行參軍） | [《南齊書・良政》][517] | [JSON](8c4_l2o_krm_A.json) |
| `AA` | 沈憲（字彥璋） | [《南齊書・良政》][517] | [JSON](8c4_l2o_krm_AA.json) |
| `AA*A` | 沈浚（字叔源） | [《梁書・韋粲 江子一 弟子四 子五 張嵊 沈浚 柳敬禮》][376] | [JSON](8c4_l2o_krm_AA%2AA.json) |

</details>

<details><summary><code>8dg_6jb_3j5</code> 石靈寶（阮令嬴父）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 石靈寶（阮令嬴父） | [《梁書・皇后》][312]、[《南史・后妃下》][557] | [JSON](8dg_6jb_3j5.json) |
| `A` | 阮令嬴（本姓石，梁文宣太后） | [《梁書・元帝》][308]、[《梁書・皇后》][312]、[《南史・后妃下》][557] | [JSON](8dg_6jb_3j5_A.json) |

</details>

<details><summary><code>8e8_ca8_29d</code> 王佑（4 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 王佑 | [《晉書・王湛 荀崧 范汪 劉惔 張憑 韓伯》][233] | [JSON](8e8_ca8_29d.json) |
| `A` | 王嶠 | [《晉書・王湛 荀崧 范汪 劉惔 張憑 韓伯》][233] | [JSON](8e8_ca8_29d_A.json) |
| `AA` | 王淡 | [《晉書・王湛 荀崧 范汪 劉惔 張憑 韓伯》][233] | [JSON](8e8_ca8_29d_AA.json) |
| `AAA` | 王度世 | [《晉書・王湛 荀崧 范汪 劉惔 張憑 韓伯》][233] | [JSON](8e8_ca8_29d_AAA.json) |

</details>

<details><summary><code>8fx_ugl_pnj</code> 侯弘遠（侯瑱父）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 侯弘遠（侯瑱父） | [《陳書・列傳第三: 侯瑱 歐陽頠 吳明徹 裴子烈》][19] | [JSON](8fx_ugl_pnj.json) |
| `A` | 侯瑱（字伯玉） | [《陳書・列傳第三: 侯瑱 歐陽頠 吳明徹 裴子烈》][19] | [JSON](8fx_ugl_pnj_A.json) |

</details>

<details><summary><code>8im_m5e_cpy</code> 甘茂（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 甘茂 | [《史記・樗里子甘茂列傳》][862] | [JSON](8im_m5e_cpy.json) |
| `*A` | 甘羅 | [《史記・樗里子甘茂列傳》][862] | [JSON](8im_m5e_cpy_%2AA.json) |

</details>

<details><summary><code>8rw_c97_jpz</code> 梁伯（晉惠公外家）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 梁伯（晉惠公外家） | [《史記・晉世家》][830] | [JSON](8rw_c97_jpz.json) |
| `A` | 梁伯女（圉母） | [《史記・晉世家》][830] | [JSON](8rw_c97_jpz_A.json) |

</details>

<details><summary><code>8uz_r1g_a0f</code> 溫恕（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 溫恕 | [《三國志・劉司馬梁張溫賈傳》][744] | [JSON](8uz_r1g_a0f.json) |
| `A` | 溫恢 | [《三國志・劉司馬梁張溫賈傳》][744] | [JSON](8uz_r1g_a0f_A.json) |
| `AA` | 溫生 | [《三國志・劉司馬梁張溫賈傳》][744] | [JSON](8uz_r1g_a0f_AA.json) |

</details>

<details><summary><code>8xz_mlj_r3c</code> 韓千秋（南越列傳候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 韓千秋 | [《史記・南越列傳》][904] | [JSON](8xz_mlj_r3c.json) |
| `A` | 延年 | [《史記・建元以來侯者年表》][1229] | [JSON](8xz_mlj_r3c_A.json) |

</details>

<details><summary><code>932_46f_026</code> 明帝（魏，荀勖引古）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 明帝（魏，荀勖引古） | [《三國志・諸夏侯曹傳》][734] | [JSON](932_46f_026.json) |
| `A` | 淑（平原懿公主） | [《三國志・桓二陳徐衞盧傳》][750] | [JSON](932_46f_026_A.json) |

</details>

<details><summary><code>96a_987_925</code> 山濤（7 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 山濤 | [《晉書・山濤 王戎 郭舒 樂廣》][165] | [JSON](96a_987_925.json) |
| `A` | 山該〔字伯倫〕 | [《晉書・山濤 王戎 郭舒 樂廣》][165] | [JSON](96a_987_925_A.json) |
| `AA` | 山瑋〔字彥祖〕 | [《晉書・山濤 王戎 郭舒 樂廣》][165] | [JSON](96a_987_925_AA.json) |
| `AB` | 山世回 | [《晉書・山濤 王戎 郭舒 樂廣》][165] | [JSON](96a_987_925_AB.json) |
| `B` | 山淳〔字子玄〕 | [《晉書・山濤 王戎 郭舒 樂廣》][165] | [JSON](96a_987_925_B.json) |
| `C` | 山允〔字叔真〕 | [《晉書・山濤 王戎 郭舒 樂廣》][165] | [JSON](96a_987_925_C.json) |
| `D` | 山謨〔字季長〕 | [《晉書・山濤 王戎 郭舒 樂廣》][165] | [JSON](96a_987_925_D.json) |

</details>

<details><summary><code>984_9e1_5e9</code> 全琮（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 全琮 | [《三國志・陸遜傳》][800] | [JSON](984_9e1_5e9.json) |
| `A` | 全寄 | [《三國志・張顧諸葛步傳》][776] | [JSON](984_9e1_5e9_A.json) |
| `B` | 全緒 | [《三國志・張顧諸葛步傳》][776] | [JSON](984_9e1_5e9_B.json) |

</details>

<details><summary><code>989_en9_fv0</code> 陳金寶（宋明帝陳貴妃父）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 陳金寶（宋明帝陳貴妃父） | [《宋書・后妃》][1012] | [JSON](989_en9_fv0.json) |
| `A` | 陳妙登（宋後廢帝母） | [《梁書・皇后》][311]、[《宋書・后妃》][1012] | [JSON](989_en9_fv0_A.json) |

</details>

<details><summary><code>98i_dd4_aof</code> 多同（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 多同 | [《史記・西南夷列傳》][907] | [JSON](98i_dd4_aof.json) |
| `A` | 多同子 | [《史記・西南夷列傳》][907] | [JSON](98i_dd4_aof_A.json) |

</details>

<details><summary><code>98q_mll_d6v</code> 蕭道生（6 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 蕭道生 | [《南史・齊宗室》][703] | [JSON](98q_mll_d6v.json) |
| `A` | 蕭鳳 | [《南齊書・宗室》][486]、[《南齊書・宗室》][487]、[《南史・齊宗室》][703] | [JSON](98q_mll_d6v_A.json) |
| `AA` | 蕭遙光 | [《南齊書・王融 謝朓》][493] | [JSON](98q_mll_d6v_AA.json) |
| `AB` | 蕭遙昌（字季暉，豐城公） | [《南齊書・宗室》][488]、[《南齊書・王奐 從弟繢 張沖》][508] | [JSON](98q_mll_d6v_AB.json) |
| `B` | 蕭緬（字景業，安陸昭王） | [《南史・齊宗室》][703] | [JSON](98q_mll_d6v_B.json) |
| `BA` | 蕭寶晊（安陸王緬子，湘東王） | [《南史・王誕　王華　王惠　王彧》][644]、[《南史・齊宗室》][703] | [JSON](98q_mll_d6v_BA.json) |

</details>

<details><summary><code>995_xas_r98</code> 申（蔡昭侯）（6 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 申（蔡昭侯） | [《史記・管蔡世家》][826] | [JSON](995_xas_r98.json) |
| `A` | 朔（蔡成侯） | [《史記・管蔡世家》][826] | [JSON](995_xas_r98_A.json) |
| `AA` | 產（蔡聲侯） | [《史記・管蔡世家》][826]、[《史記・六國年表》][1224] | [JSON](995_xas_r98_AA.json) |
| `AAA` | 元侯（蔡君） | [《史記・管蔡世家》][826] | [JSON](995_xas_r98_AAA.json) |
| `AAAA` | 齊（蔡末侯） | [《史記・管蔡世家》][826] | [JSON](995_xas_r98_AAAA.json) |
| `B` | 蔡昭侯質吳子（未名） | [《史記・管蔡世家》][826] | [JSON](995_xas_r98_B.json) |

</details>

<details><summary><code>9ac_ddl_9iz</code> 殷元素（殷寧父，宋南康相）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 殷元素（殷寧父，宋南康相） | [《南齊書・王奐 從弟繢 張沖》][505]、[《南史・范岫　傅昭　孔休源　江革　徐勉　許懋　殷鈞》][723] | [JSON](9ac_ddl_9iz.json) |
| `A` | 殷寧（殷元素子、殷叡父） | [《南史・范岫　傅昭　孔休源　江革　徐勉　許懋　殷鈞》][723] | [JSON](9ac_ddl_9iz_A.json) |

</details>

<details><summary><code>9c5_a31_807</code> 武沈（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 武沈 | [《晉書・庾亮》][229] | [JSON](9c5_a31_807.json) |
| `A` | 武遵 | [《晉書・庾亮》][229] | [JSON](9c5_a31_807_A.json) |

</details>

<details><summary><code>9fa_127_a71</code> 務勿塵（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 務勿塵 | [《晉書・王沈 荀顗 荀勖 馮紞》][158] | [JSON](9fa_127_a71.json) |
| `A` | 疾陸眷 | [《晉書・王沈 荀顗 荀勖 馮紞》][158] | [JSON](9fa_127_a71_A.json) |

</details>

<details><summary><code>9nr_qwg_vuf</code> 叔孫宣伯（魯）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 叔孫宣伯（魯） | [《史記・齊太公世家》][823] | [JSON](9nr_qwg_vuf.json) |
| `A` | 景公母（叔孫宣伯女） | [《史記・齊太公世家》][823] | [JSON](9nr_qwg_vuf_A.json) |

</details>

<details><summary><code>9oa_4bh_lmd</code> 鄭伯（楚莊王圍鄭時）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 鄭伯（楚莊王圍鄭時） | [《史記・鄭世家》][833] | [JSON](9oa_4bh_lmd.json) |
| `A` | 沸 | [《史記・鄭世家》][833] | [JSON](9oa_4bh_lmd_A.json) |

</details>

<details><summary><code>9v9_cj5_dor</code> 虞潭〔本紀來源局部〕（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 虞潭〔本紀來源局部〕 | [《晉書・王舒 王廙 虞潭 顧眾 張闓》][244] | [JSON](9v9_cj5_dor.json) |
| `A` | 虞仡 | [《晉書・王舒 王廙 虞潭 顧眾 張闓》][244] | [JSON](9v9_cj5_dor_A.json) |
| `B` | 虞楚 | [《晉書・列女》][268] | [JSON](9v9_cj5_dor_B.json) |

</details>

<details><summary><code>9w2_c77_53m</code> 齊桓公（12 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 齊桓公 | [《史記・齊太公世家》][823] | [JSON](9w2_c77_53m.json) |
| `A` | 元（齊惠公） | [《史記・齊太公世家》][823] | [JSON](9w2_c77_53m_A.json) |
| `AA` | 無野（齊頃公） | [《史記・齊太公世家》][823] | [JSON](9w2_c77_53m_AA.json) |
| `AAA` | 環（齊靈公） | [《史記・齊太公世家》][823] | [JSON](9w2_c77_53m_AAA.json) |
| `AAAA` | 齊莊公（崔杼時） | [《史記・齊太公世家》][823] | [JSON](9w2_c77_53m_AAAA.json) |
| `B` | 無詭（齊桓公子） | [《史記・齊太公世家》][823] | [JSON](9w2_c77_53m_B.json) |
| `C` | 昭（齊孝公） | [《史記・齊太公世家》][823] | [JSON](9w2_c77_53m_C.json) |
| `D` | 潘（齊昭公） | [《史記・齊太公世家》][823] | [JSON](9w2_c77_53m_D.json) |
| `DA` | 舍（齊昭公子） | [《史記・齊太公世家》][823] | [JSON](9w2_c77_53m_DA.json) |
| `E` | 商人（齊懿公） | [《史記・齊太公世家》][823] | [JSON](9w2_c77_53m_E.json) |
| `F` | 雍（齊桓公子） | [《史記・齊太公世家》][823]、[《史記・楚世家》][831] | [JSON](9w2_c77_53m_F.json) |
| `G` | 齊姜（申生母） | [《史記・晉世家》][830] | [JSON](9w2_c77_53m_G.json) |

</details>

<details><summary><code>9w8_tqh_ysn</code> 陳寔（17 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 陳寔 | [《後漢書・荀韓鍾陳列傳》][76] | [JSON](9w8_tqh_ysn.json) |
| `A` | 紀（陳羣父） | [《後漢書・荀韓鍾陳列傳》][76]、[《三國志・桓二陳徐衞盧傳》][750] | [JSON](9w8_tqh_ysn_A.json) |
| `AA` | 陳群 | [《三國志・桓二陳徐衞盧傳》][750] | [JSON](9w8_tqh_ysn_AA.json) |
| `AAA` | 陳泰 | [《三國志・桓二陳徐衞盧傳》][750] | [JSON](9w8_tqh_ysn_AAA.json) |
| `AAAA` | 恂（陳泰子） | [《三國志・桓二陳徐衞盧傳》][750] | [JSON](9w8_tqh_ysn_AAAA.json) |
| `AAB` | 陳羣未名另封子 | [《三國志・桓二陳徐衞盧傳》][750] | [JSON](9w8_tqh_ysn_AAB.json) |
| `B` | 諶（陳羣叔父） | [《三國志・桓二陳徐衞盧傳》][750] | [JSON](9w8_tqh_ysn_B.json) |
| `B*A` | 佐（陳諶孫）（來源候選；預設不接父系） | [《三國志・桓二陳徐衞盧傳》][750] | [JSON](9w8_tqh_ysn_B%2AA.json) |
| `B*AA` | 凖（陳佐子） | [《新唐書・宰相世系一下》][1188] | [JSON](9w8_tqh_ysn_B%2AAA.json) |
| `B*AA*A` | 逵（字林道） | [《三國志・桓二陳徐衞盧傳》][750] | [JSON](9w8_tqh_ysn_B%2AAA%2AA.json) |
| `B*AB` | 戴（凖弟） | [《三國志・桓二陳徐衞盧傳》][750] | [JSON](9w8_tqh_ysn_B%2AAB.json) |
| `B*AC` | 徵（凖弟） | [《三國志・桓二陳徐衞盧傳》][750] | [JSON](9w8_tqh_ysn_B%2AAC.json) |
| `B*B` | 坦（陳佐弟） | [《三國志・桓二陳徐衞盧傳》][750] | [JSON](9w8_tqh_ysn_B%2AB.json) |
| `C` | 夔〔新唐陳氏序〕 | [《新唐書・宰相世系一下》][1188] | [JSON](9w8_tqh_ysn_C.json) |
| `D` | 洽〔新唐陳氏序〕 | [《新唐書・宰相世系一下》][1188] | [JSON](9w8_tqh_ysn_D.json) |
| `E` | 休〔新唐陳氏序〕 | [《新唐書・宰相世系一下》][1188] | [JSON](9w8_tqh_ysn_E.json) |
| `F` | 光〔新唐陳氏序〕 | [《新唐書・宰相世系一下》][1188] | [JSON](9w8_tqh_ysn_F.json) |

</details>

<details><summary><code>9yf_c3t_x2w</code> 衛君父引古未名（李斯列傳候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 衛君父引古未名 | [《史記・李斯列傳》][878] | [JSON](9yf_c3t_x2w.json) |
| `A` | 衛君引古未名 | [《史記・李斯列傳》][878] | [JSON](9yf_c3t_x2w_A.json) |

</details>

<details><summary><code>9zj_vf7_86a</code> 薄氏〔薄太后之父；靈文侯〕（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 薄氏〔薄太后之父；靈文侯〕 | [《史記・外戚世家》][840] | [JSON](9zj_vf7_86a.json) |
| `A` | 薄太后（孝文帝母） | [《史記・外戚世家》][840] | [JSON](9zj_vf7_86a_A.json) |

</details>

<details><summary><code>a02_614_f84</code> 曹欣之（宋徐州刺史）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 曹欣之（宋徐州刺史） | [《梁書・王茂 曹景宗 柳慶遠》][321] | [JSON](a02_614_f84.json) |
| `A` | 曹景宗（字子震，曹欣之子） | [《梁書・王茂 曹景宗 柳慶遠》][321]、[《南齊書・王奐 從弟繢 張沖》][508] | [JSON](a02_614_f84_A.json) |

</details>

<details><summary><code>a04_d8f_416</code> 王允之（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 王允之 | [《晉書・王舒 王廙 虞潭 顧眾 張闓》][242] | [JSON](a04_d8f_416.json) |
| `A` | 王晞之 | [《晉書・王舒 王廙 虞潭 顧眾 張闓》][242] | [JSON](a04_d8f_416_A.json) |
| `AA` | 王肇之 | [《晉書・王舒 王廙 虞潭 顧眾 張闓》][242] | [JSON](a04_d8f_416_AA.json) |

</details>

<details><summary><code>a13_5fp_pek</code> 梁襄王（趙世家候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 梁襄王 | [《史記・趙世家》][834] | [JSON](a13_5fp_pek.json) |
| `A` | 嗣 | [《史記・趙世家》][834] | [JSON](a13_5fp_pek_A.json) |

</details>

<details><summary><code>a1f_f17_ccb</code> 荀衢（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 荀衢 | [《三國志・二荀賈傳》][736] | [JSON](a1f_f17_ccb.json) |
| `A` | 荀祈 | [《三國志・二荀賈傳》][736] | [JSON](a1f_f17_ccb_A.json) |

</details>

<details><summary><code>a28_f5c_105</code> 曹洪（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 曹洪 | [《三國志・二荀賈傳》][736] | [JSON](a28_f5c_105.json) |
| `A` | 曹氏（荀粲妻，曹洪女） | [《三國志・二荀賈傳》][736] | [JSON](a28_f5c_105_A.json) |

</details>

<details><summary><code>a7k_sl0_d7u</code> 金王孫（外戚世家候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 金王孫 | [《史記・外戚世家》][840] | [JSON](a7k_sl0_d7u.json) |
| `A` | 修成君 | [《史記・外戚世家》][840]、[《史記・淮南衡山列傳》][909] | [JSON](a7k_sl0_d7u_A.json) |

</details>

<details><summary><code>a8f_ec8_e74</code> 王澤（18 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 王澤 | [《三國志・徐胡二王傳》][754] | [JSON](a8f_ec8_e74.json) |
| `A` | 王昶 | [《三國志・徐胡二王傳》][754] | [JSON](a8f_ec8_e74_A.json) |
| `AA` | 王湛 | [《晉書・王湛 荀崧 范汪 劉惔 張憑 韓伯》][233] | [JSON](a8f_ec8_e74_AA.json) |
| `AAA` | 王承 | [《晉書・王湛 荀崧 范汪 劉惔 張憑 韓伯》][233] | [JSON](a8f_ec8_e74_AAA.json) |
| `AAAA` | 王述 | [《晉書・王湛 荀崧 范汪 劉惔 張憑 韓伯》][233] | [JSON](a8f_ec8_e74_AAAA.json) |
| `AAAAA` | 王坦之 | [《晉書・王湛 荀崧 范汪 劉惔 張憑 韓伯》][233] | [JSON](a8f_ec8_e74_AAAAA.json) |
| `AAAAAA` | 王愷 | [《晉書・王湛 荀崧 范汪 劉惔 張憑 韓伯》][233] | [JSON](a8f_ec8_e74_AAAAAA.json) |
| `AAAAAB` | 王愉 | [《晉書・王湛 荀崧 范汪 劉惔 張憑 韓伯》][233] | [JSON](a8f_ec8_e74_AAAAAB.json) |
| `AAAAABA` | 王綏 | [《晉書・王湛 荀崧 范汪 劉惔 張憑 韓伯》][233] | [JSON](a8f_ec8_e74_AAAAABA.json) |
| `AAAAAC` | 王國寶 | [《晉書・王湛 荀崧 范汪 劉惔 張憑 韓伯》][233] | [JSON](a8f_ec8_e74_AAAAAC.json) |
| `AAAAAD` | 王忱 | [《晉書・王湛 荀崧 范汪 劉惔 張憑 韓伯》][233] | [JSON](a8f_ec8_e74_AAAAAD.json) |
| `AB` | 王渾 | [《晉書・王渾 王濬 唐彬》][160] | [JSON](a8f_ec8_e74_AB.json) |
| `ABA` | 王尚 | [《晉書・王渾 王濬 唐彬》][160] | [JSON](a8f_ec8_e74_ABA.json) |
| `ABB` | 王濟 | [《晉書・王渾 王濬 唐彬》][160] | [JSON](a8f_ec8_e74_ABB.json) |
| `ABBA` | 王卓 | [《晉書・王渾 王濬 唐彬》][160] | [JSON](a8f_ec8_e74_ABBA.json) |
| `ABBB` | 王聿 | [《晉書・王渾 王濬 唐彬》][160] | [JSON](a8f_ec8_e74_ABBB.json) |
| `ABC` | 王澄〔王濟弟〕 | [《晉書・王渾 王濬 唐彬》][160] | [JSON](a8f_ec8_e74_ABC.json) |
| `AC` | 王深（字道冲，王昶子） | [《三國志・徐胡二王傳》][754] | [JSON](a8f_ec8_e74_AC.json) |

</details>

<details><summary><code>a9m_987_rss</code> 叔牙（莊公弟）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 叔牙（莊公弟） | [《史記・魯周公世家》][824] | [JSON](a9m_987_rss.json) |
| `A` | 叔牙子（未名） | [《史記・魯周公世家》][824] | [JSON](a9m_987_rss_A.json) |

</details>

<details><summary><code>a9v_t0d_3va</code> 晉惠公（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 晉惠公 | [《史記・晉世家》][830] | [JSON](a9v_t0d_3va.json) |
| `A` | 晉懷公 | [《史記・晉世家》][830] | [JSON](a9v_t0d_3va_A.json) |
| `B` | 妾（梁伯女所生女） | [《史記・晉世家》][830] | [JSON](a9v_t0d_3va_B.json) |

</details>

<details><summary><code>aa6_83c_juy</code> 謝裒（65 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 謝裒 | [《南史・謝晦　謝裕　謝方明　謝靈運》][587] | [JSON](aa6_83c_juy.json) |
| `A` | 謝據 | [《南史・謝晦　謝裕　謝方明　謝靈運》][587] | [JSON](aa6_83c_juy_A.json) |
| `AA` | 謝朗 | [《晉書・謝尚 謝安》][250] | [JSON](aa6_83c_juy_AA.json) |
| `AAA` | 謝重 | [《晉書・謝尚 謝安》][250] | [JSON](aa6_83c_juy_AAA.json) |
| `AAA*A` | 謝紹 | [《南史・謝晦　謝裕　謝方明　謝靈運》][587]、[《宋書・謝晦》][1023]、[《宋書・謝晦》][1024] | [JSON](aa6_83c_juy_AAA%2AA.json) |
| `AAA*B` | 謝世猷 | [《宋書・謝晦》][1023]、[《宋書・謝晦》][1024] | [JSON](aa6_83c_juy_AAA%2AB.json) |
| `AAAA` | 謝晦 | [《宋書・謝晦》][1023] | [JSON](aa6_83c_juy_AAAA.json) |
| `AAAAA` | 謝世休 | [《宋書・謝晦》][1023]、[《宋書・謝晦》][1024] | [JSON](aa6_83c_juy_AAAAA.json) |
| `AAAAB` | 謝晦女（彭城王義康妃） | [《南史・謝晦　謝裕　謝方明　謝靈運》][587] | [JSON](aa6_83c_juy_AAAAB.json) |
| `AAAB` | 謝絢 | [《晉書・謝尚 謝安》][250]、[《南史・謝晦　謝裕　謝方明　謝靈運》][587] | [JSON](aa6_83c_juy_AAAB.json) |
| `AAABA` | 謝世基 | [《宋書・謝晦》][1023]、[《宋書・謝晦》][1024] | [JSON](aa6_83c_juy_AAABA.json) |
| `AAAC` | 謝氏（荀伯子妻） | [《宋書・范泰 王准之 王韶之 荀伯子》][1067] | [JSON](aa6_83c_juy_AAAC.json) |
| `AAAD` | 謝瞻 | [《宋書・謝瞻 孔琳之》][1059] | [JSON](aa6_83c_juy_AAAD.json) |
| `AAAE` | 㬭 | [《宋書・謝瞻 孔琳之》][1059] | [JSON](aa6_83c_juy_AAAE.json) |
| `AAAEA` | 世平 | [《南史・謝晦　謝裕　謝方明　謝靈運》][587]、[《宋書・謝晦》][1023]、[《宋書・謝晦》][1024]、[《宋書・謝瞻 孔琳之》][1059] | [JSON](aa6_83c_juy_AAAEA.json) |
| `AAAF` | 謝遯 | [《宋書・謝晦》][1023]、[《宋書・謝晦》][1024] | [JSON](aa6_83c_juy_AAAF.json) |
| `AB` | 謝允 | [《南史・謝晦　謝裕　謝方明　謝靈運》][591] | [JSON](aa6_83c_juy_AB.json) |
| `ABA` | 謝純 | [《宋書・庾悅 王誕 謝景仁 袁湛 褚叔度》][1052] | [JSON](aa6_83c_juy_ABA.json) |
| `ABA*A` | 謝沈（謝純孫） | [《宋書・庾悅 王誕 謝景仁 袁湛 褚叔度》][1052] | [JSON](aa6_83c_juy_ABA%2AA.json) |
| `ABB` | 謝甝 | [《南史・謝晦　謝裕　謝方明　謝靈運》][589] | [JSON](aa6_83c_juy_ABB.json) |
| `ABC` | 謝述 | [《宋書・庾悅 王誕 謝景仁 袁湛 褚叔度》][1054] | [JSON](aa6_83c_juy_ABC.json) |
| `ABCA` | 謝約 | [《宋書・庾悅 王誕 謝景仁 袁湛 褚叔度》][1054] | [JSON](aa6_83c_juy_ABCA.json) |
| `ABCB` | 謝緯 | [《宋書・庾悅 王誕 謝景仁 袁湛 褚叔度》][1054] | [JSON](aa6_83c_juy_ABCB.json) |
| `ABCBA` | 謝朓 | [《南史・謝晦　謝裕　謝方明　謝靈運》][590] | [JSON](aa6_83c_juy_ABCBA.json) |
| `ABCBAA` | 謝謨 | [《南史・謝晦　謝裕　謝方明　謝靈運》][590] | [JSON](aa6_83c_juy_ABCBAA.json) |
| `B` | 謝安 | [《晉書・謝尚 謝安》][250] | [JSON](aa6_83c_juy_B.json) |
| `B*A` | 謝璞 | [《南史・謝晦　謝裕　謝方明　謝靈運》][588] | [JSON](aa6_83c_juy_B%2AA.json) |
| `BA` | 謝琰 | [《晉書・謝尚 謝安》][250] | [JSON](aa6_83c_juy_BA.json) |
| `BAA` | 謝肇 | [《晉書・謝尚 謝安》][250] | [JSON](aa6_83c_juy_BAA.json) |
| `BAB` | 謝峻 | [《晉書・謝尚 謝安》][250] | [JSON](aa6_83c_juy_BAB.json) |
| `BAC` | 謝混 | [《南史・謝弘微》][594] | [JSON](aa6_83c_juy_BAC.json) |
| `BACA` | 謝氏（殷叡妻） | [《宋書・王惠 謝弘微 王球》][1062] | [JSON](aa6_83c_juy_BACA.json) |
| `BB` | 謝氏（王瑉妻） | [《晉書・謝尚 謝安》][250] | [JSON](aa6_83c_juy_BB.json) |
| `C` | 謝奕 | [《晉書・謝尚 謝安》][250] | [JSON](aa6_83c_juy_C.json) |
| `CA` | 謝康 | [《晉書・謝尚 謝安》][250] | [JSON](aa6_83c_juy_CA.json) |
| `CB` | 謝泉 | [《晉書・謝尚 謝安》][250] | [JSON](aa6_83c_juy_CB.json) |
| `CC` | 謝靖 | [《晉書・謝尚 謝安》][250] | [JSON](aa6_83c_juy_CC.json) |
| `CD` | 謝玄 | [《晉書・謝尚 謝安》][250] | [JSON](aa6_83c_juy_CD.json) |
| `CDA` | 謝瑍 | [《晉書・謝尚 謝安》][250] | [JSON](aa6_83c_juy_CDA.json) |
| `CDAA` | 謝靈運 | [《宋書・謝靈運》][1078] | [JSON](aa6_83c_juy_CDAA.json) |
| `CDAAA` | 鳯（謝靈運子） | [《宋書・謝靈運》][1078] | [JSON](aa6_83c_juy_CDAAA.json) |
| `CDAAB` | 謝鳳 | [《南史・謝晦　謝裕　謝方明　謝靈運》][576] | [JSON](aa6_83c_juy_CDAAB.json) |
| `CDAABA` | 謝超宗 | [《南齊書・謝超宗 劉祥》][462]、[《南齊書・謝超宗 劉祥》][461] | [JSON](aa6_83c_juy_CDAABA.json) |
| `CDAABAA` | 謝才卿 | [《南齊書・謝超宗 劉祥》][460]、[《南齊書・謝超宗 劉祥》][462]、[《南齊書・謝超宗 劉祥》][461]、[《南史・謝晦　謝裕　謝方明　謝靈運》][584] | [JSON](aa6_83c_juy_CDAABAA.json) |
| `CDAABAAA` | 謝藻 | [《梁書・文學下》][387]、[《梁書・文學下》][388]、[《梁書・文學下》][389]、[《南史・謝晦　謝裕　謝方明　謝靈運》][592] | [JSON](aa6_83c_juy_CDAABAAA.json) |
| `CDAABAB` | 謝幾卿 | [《梁書・文學下》][387]、[《梁書・文學下》][388] | [JSON](aa6_83c_juy_CDAABAB.json) |
| `CE` | 謝道韞 | [《晉書・列女》][274]、[《晉書・列女》][275] | [JSON](aa6_83c_juy_CE.json) |
| `D` | 謝萬 | [《晉書・謝尚 謝安》][250] | [JSON](aa6_83c_juy_D.json) |
| `DA` | 謝氏（王珣妻） | [《晉書・謝尚 謝安》][250] | [JSON](aa6_83c_juy_DA.json) |
| `DB` | 謝韶 | [《晉書・謝尚 謝安》][250] | [JSON](aa6_83c_juy_DB.json) |
| `DBA` | 謝思 | [《南史・謝弘微》][594]、[《宋書・王惠 謝弘微 王球》][1062] | [JSON](aa6_83c_juy_DBA.json) |
| `DBAA` | 謝曜 | [《南史・謝弘微》][594] | [JSON](aa6_83c_juy_DBAA.json) |
| `DBAB` | 謝弘微 | [《宋書・王惠 謝弘微 王球》][1062] | [JSON](aa6_83c_juy_DBAB.json) |
| `DBABA` | 謝莊 | [《宋書・謝莊 王景文》][1107] | [JSON](aa6_83c_juy_DBABA.json) |
| `DBABAA` | 謝颺 | [《南齊書・江斆 何昌㝢 謝𤅢 王思遠》][484]、[《南史・后妃上》][549]、[《宋書・謝莊 王景文》][1107] | [JSON](aa6_83c_juy_DBABAA.json) |
| `DBABAAA` | 謝梵境〔宋順帝皇后〕 | [《南史・后妃上》][549]、[《宋書・后妃》][1020]、[《宋書・后妃》][1019]、[《宋書・謝莊 王景文》][1107] | [JSON](aa6_83c_juy_DBABAAA.json) |
| `DBABAB` | 謝朏 | [《梁書・謝朏 弟子覽》][323] | [JSON](aa6_83c_juy_DBABAB.json) |
| `DBABABA` | 諼〔謝朏子〕 | [《梁書・謝朏 弟子覽》][323] | [JSON](aa6_83c_juy_DBABABA.json) |
| `DBABABB` | 篹〔謝朏次子〕 | [《梁書・謝朏 弟子覽》][323] | [JSON](aa6_83c_juy_DBABABB.json) |
| `DBABAC` | 謝𤅢〔字義潔〕 | [《南齊書・江斆 何昌㝢 謝𤅢 王思遠》][484] | [JSON](aa6_83c_juy_DBABAC.json) |
| `DBABACA` | 謝舉（字言揚） | [《梁書・王僧孺 張率 劉孝綽 王筠》][363]、[《梁書・王僧孺 張率 劉孝綽 王筠》][362]、[《南史・謝弘微》][595] | [JSON](aa6_83c_juy_DBABACA.json) |
| `DBABAD` | 顥〔謝𤅢兄，字仁悠〕 | [《南齊書・江斆 何昌㝢 謝𤅢 王思遠》][484] | [JSON](aa6_83c_juy_DBABAD.json) |
| `DBABAE` | 嵷〔謝𤅢兄〕 | [《南齊書・江斆 何昌㝢 謝𤅢 王思遠》][484] | [JSON](aa6_83c_juy_DBABAE.json) |
| `E` | 謝石 | [《晉書・謝尚 謝安》][250] | [JSON](aa6_83c_juy_E.json) |
| `EA` | 謝汪 | [《晉書・謝尚 謝安》][250] | [JSON](aa6_83c_juy_EA.json) |

</details>

<details><summary><code>aa9_7e9_5b9</code> 魯宗之（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 魯宗之 | [《晉書・桓彝》][231] | [JSON](aa9_7e9_5b9.json) |
| `A` | 魯軌 | [《魏書・刁雍 王慧龍 韓延之 袁式》][1168] | [JSON](aa9_7e9_5b9_A.json) |

</details>

<details><summary><code>acg_se3_w5x</code> 周呂侯（呂后兄）（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 周呂侯（呂后兄） | [《史記・呂后本紀》][817] | [JSON](acg_se3_w5x.json) |
| `A` | 呂台 | [《史記・呂后本紀》][817] | [JSON](acg_se3_w5x_A.json) |
| `B` | 呂產 | [《史記・呂后本紀》][817] | [JSON](acg_se3_w5x_B.json) |

</details>

<details><summary><code>acp_3ec_zvn</code> 李頡（李郃父）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 李頡（李郃父） | [《後漢書・方術列傳》][81] | [JSON](acp_3ec_zvn.json) |
| `A` | 李郃（字孟節） | [《後漢書・方術列傳》][81] | [JSON](acp_3ec_zvn_A.json) |

</details>

<details><summary><code>ae2_620_2bc</code> 袁渙（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 袁渙 | [《三國志・袁張涼國田王邴管傳》][738] | [JSON](ae2_620_2bc.json) |
| `A` | 袁㝢 | [《三國志・袁張涼國田王邴管傳》][738] | [JSON](ae2_620_2bc_A.json) |
| `B` | 袁準 | [《三國志・袁張涼國田王邴管傳》][738] | [JSON](ae2_620_2bc_B.json) |

</details>

<details><summary><code>ae4_588_bdb</code> 鄭泰（7 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 鄭泰 | [《晉書・鄭袤 李胤 盧欽 華表 石鑒 溫羨》][186] | [JSON](ae4_588_bdb.json) |
| `A` | 鄭袤〔字林叔〕 | [《晉書・鄭袤 李胤 盧欽 華表 石鑒 溫羨》][186] | [JSON](ae4_588_bdb_A.json) |
| `AA` | 鄭質〔鄭袤子〕 | [《晉書・鄭袤 李胤 盧欽 華表 石鑒 溫羨》][186] | [JSON](ae4_588_bdb_AA.json) |
| `AB` | 鄭舒〔鄭袤子〕 | [《晉書・鄭袤 李胤 盧欽 華表 石鑒 溫羨》][186] | [JSON](ae4_588_bdb_AB.json) |
| `AC` | 鄭詡〔鄭袤子〕 | [《晉書・鄭袤 李胤 盧欽 華表 石鑒 溫羨》][186] | [JSON](ae4_588_bdb_AC.json) |
| `AD` | 鄭稱〔鄭袤子〕 | [《晉書・鄭袤 李胤 盧欽 華表 石鑒 溫羨》][186] | [JSON](ae4_588_bdb_AD.json) |
| `AE` | 鄭予〔鄭袤子〕 | [《晉書・鄭袤 李胤 盧欽 華表 石鑒 溫羨》][186] | [JSON](ae4_588_bdb_AE.json) |

</details>

<details><summary><code>ae7_dcf_084</code> 范汪（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 范汪 | [《晉書・庾亮》][229]、[《晉書・謝尚 謝安》][250]、[《世說新語・方正》][943]、[《宋書・范泰 王准之 王韶之 荀伯子》][1064] | [JSON](ae7_dcf_084.json) |
| `A` | 范蓋（范汪女，王坦之妻） | [《世說新語・方正》][943] | [JSON](ae7_dcf_084_A.json) |

</details>

<details><summary><code>afj_vl8_7fu</code> 安丘侯説（萬石張叔列傳候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 安丘侯説 | [《史記・萬石張叔列傳》][894] | [JSON](afj_vl8_7fu.json) |
| `A` | 張歐 | [《史記・萬石張叔列傳》][894] | [JSON](afj_vl8_7fu_A.json) |

</details>

<details><summary><code>agx_sqm_4ou</code> 張耳（5 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 張耳 | [《史記・張耳陳餘列傳》][880] | [JSON](agx_sqm_4ou.json) |
| `A` | 張敖 | [《史記・張耳陳餘列傳》][880] | [JSON](agx_sqm_4ou_A.json) |
| `AA` | 張偃 | [《史記・呂后本紀》][817]、[《史記・張耳陳餘列傳》][880] | [JSON](agx_sqm_4ou_AA.json) |
| `AB` | 張壽 | [《史記・張耳陳餘列傳》][880] | [JSON](agx_sqm_4ou_AB.json) |
| `AC` | 張侈 | [《史記・張耳陳餘列傳》][880] | [JSON](agx_sqm_4ou_AC.json) |

</details>

<details><summary><code>ant_dk4_dds</code> 張稷（4 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 張稷 | [《梁書・王亮 張稷 王瑩》][329] | [JSON](ant_dk4_dds.json) |
| `A` | 張楚瑗（張稷長女） | [《梁書・王亮 張稷 王瑩》][327]、[《梁書・王亮 張稷 王瑩》][328] | [JSON](ant_dk4_dds_A.json) |
| `B` | 張嵊（字四山） | [《梁書・韋粲 江子一 弟子四 子五 張嵊 沈浚 柳敬禮》][380] | [JSON](ant_dk4_dds_B.json) |
| `C` | 張伊（字懷尹，張嵊弟） | [《南史・張裕》][694] | [JSON](ant_dk4_dds_C.json) |

</details>

<details><summary><code>ao3_0fy_d45</code> 秦昭王（6 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 秦昭王 | [《史記・范睢蔡澤列傳》][870] | [JSON](ao3_0fy_d45.json) |
| `A` | 秦孝文王 | [《史記・呂不韋列傳》][876] | [JSON](ao3_0fy_d45_A.json) |
| `AA` | 秦莊襄王 | [《史記・呂不韋列傳》][876] | [JSON](ao3_0fy_d45_AA.json) |
| `AAA` | 秦始皇帝 | [《史記・秦始皇本紀》][814] | [JSON](ao3_0fy_d45_AAA.json) |
| `AAAA` | 胡亥 | [《史記・秦始皇本紀》][814] | [JSON](ao3_0fy_d45_AAAA.json) |
| `AAAB` | 扶蘇 | [《史記・李斯列傳》][878] | [JSON](ao3_0fy_d45_AAAB.json) |

</details>

<details><summary><code>aoz_jaz_82c</code> 馮朝（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 馮朝 | [《三國志・妃嬪傳》][762] | [JSON](aoz_jaz_82c.json) |
| `A` | 馮純 | [《三國志・妃嬪傳》][762] | [JSON](aoz_jaz_82c_A.json) |

</details>

<details><summary><code>apr_7dg_tdd</code> 謝方明（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 謝方明 | [《宋書・張茂度 庾登之 謝方明 江夷》][1056] | [JSON](apr_7dg_tdd.json) |
| `A` | 惠連 | [《宋書・謝靈運》][1078] | [JSON](apr_7dg_tdd_A.json) |

</details>

<details><summary><code>ath_xsq_n4i</code> 魯定公（11 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 魯定公 | [《史記・魯周公世家》][824] | [JSON](ath_xsq_n4i.json) |
| `A` | 魯哀公 | [《史記・魯周公世家》][824] | [JSON](ath_xsq_n4i_A.json) |
| `AA` | 寧（魯悼公） | [《史記・魯周公世家》][824] | [JSON](ath_xsq_n4i_AA.json) |
| `AAA` | 嘉（魯元公） | [《史記・魯周公世家》][824] | [JSON](ath_xsq_n4i_AAA.json) |
| `AAAA` | 顯（魯穆公） | [《史記・魯周公世家》][824] | [JSON](ath_xsq_n4i_AAAA.json) |
| `AAAAA` | 奮（魯共公） | [《史記・魯周公世家》][824] | [JSON](ath_xsq_n4i_AAAAA.json) |
| `AAAAAA` | 屯（魯康公） | [《史記・魯周公世家》][824] | [JSON](ath_xsq_n4i_AAAAAA.json) |
| `AAAAAAA` | 匽（魯景公） | [《史記・魯周公世家》][824] | [JSON](ath_xsq_n4i_AAAAAAA.json) |
| `AAAAAAAA` | 叔（魯平公） | [《史記・魯周公世家》][824] | [JSON](ath_xsq_n4i_AAAAAAAA.json) |
| `AAAAAAAAA` | 賈（魯文公） | [《史記・魯周公世家》][824] | [JSON](ath_xsq_n4i_AAAAAAAAA.json) |
| `AAAAAAAAAA` | 讎（魯頃公） | [《史記・魯周公世家》][824] | [JSON](ath_xsq_n4i_AAAAAAAAAA.json) |

</details>

<details><summary><code>axs_5y7_p7w</code> 韋玄（韋叡祖）（10 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 韋玄（韋叡祖） | [《梁書・柳惔 弟忱 席闡文 韋叡 族弟愛》][322] | [JSON](axs_5y7_p7w.json) |
| `A` | 韋祖歸（寧遠長史） | [《梁書・柳惔 弟忱 席闡文 韋叡 族弟愛》][322] | [JSON](axs_5y7_p7w_A.json) |
| `AA` | 韋叡（字懷文） | [《梁書・柳惔 弟忱 席闡文 韋叡 族弟愛》][322] | [JSON](axs_5y7_p7w_AA.json) |
| `AAA` | 韋放（字元直） | [《梁書・裴邃 兄子之高 之平 之橫 夏侯亶 弟夔 魚弘附 韋放》][353] | [JSON](axs_5y7_p7w_AAA.json) |
| `AAAA` | 韋粲（《梁書》字長蒨） | [《梁書・韋粲 江子一 弟子四 子五 張嵊 沈浚 柳敬禮》][377] | [JSON](axs_5y7_p7w_AAAA.json) |
| `AAAAA` | 韋臧（字君理） | [《梁書・韋粲 江子一 弟子四 子五 張嵊 沈浚 柳敬禮》][378]、[《梁書・韋粲 江子一 弟子四 子五 張嵊 沈浚 柳敬禮》][379] | [JSON](axs_5y7_p7w_AAAAA.json) |
| `AAAAB` | 韋尼（韋粲子） | [《梁書・韋粲 江子一 弟子四 子五 張嵊 沈浚 柳敬禮》][377] | [JSON](axs_5y7_p7w_AAAAB.json) |
| `AAAB` | 韋助（韋粲弟） | [《梁書・韋粲 江子一 弟子四 子五 張嵊 沈浚 柳敬禮》][377] | [JSON](axs_5y7_p7w_AAAB.json) |
| `AAAC` | 韋警（韋粲弟） | [《梁書・韋粲 江子一 弟子四 子五 張嵊 沈浚 柳敬禮》][377] | [JSON](axs_5y7_p7w_AAAC.json) |
| `AAAD` | 韋構（韋粲弟） | [《梁書・韋粲 江子一 弟子四 子五 張嵊 沈浚 柳敬禮》][377] | [JSON](axs_5y7_p7w_AAAD.json) |

</details>

<details><summary><code>b0c_13f_c3a</code> 王衍（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 王衍 | [《晉書・山濤 王戎 郭舒 樂廣》][169] | [JSON](b0c_13f_c3a.json) |
| `A` | 王衍長女〔賈后為謐聘之〕 | — | [JSON](b0c_13f_c3a_A.json) |

</details>

<details><summary><code>b1r_inb_fts</code> 樊噲（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 樊噲 | [《史記・樊酈滕灌列傳》][886] | [JSON](b1r_inb_fts.json) |
| `A` | 樊市人 | [《史記・樊酈滕灌列傳》][886] | [JSON](b1r_inb_fts_A.json) |
| `B` | 樊伉 | [《史記・樊酈滕灌列傳》][886] | [JSON](b1r_inb_fts_B.json) |

</details>

<details><summary><code>b21_e55_8bd</code> 劉琨（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 劉琨 | [《晉書・溫嶠 郗鑒》][214] | [JSON](b21_e55_8bd.json) |
| `A` | 劉群〔劉琨子〕 | [《晉書・劉琨 祖逖》][205] | [JSON](b21_e55_8bd_A.json) |

</details>

<details><summary><code>b59_d2b_609</code> 陳伯之（濟陰睢陵人）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 陳伯之（濟陰睢陵人） | [《梁書・劉季連 陳伯之》][333]、[《南齊書・江斆 何昌㝢 謝𤅢 王思遠》][481]、[《南齊書・王奐 從弟繢 張沖》][503] | [JSON](b59_d2b_609.json) |
| `A` | 陳虎牙（陳伯之子） | [《梁書・劉季連 陳伯之》][333]、[《南齊書・王奐 從弟繢 張沖》][508] | [JSON](b59_d2b_609_A.json) |

</details>

<details><summary><code>b7k_v7g_vfe</code> 杜元（寧浦太守，杜慧度曾祖）（8 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 杜元（寧浦太守，杜慧度曾祖） | [《南史・循吏》][727]、[《宋書・良吏》][1115] | [JSON](b7k_v7g_vfe.json) |
| `*A` | 杜瑗（字道言，交州刺史） | [《宋書・良吏》][1116] | [JSON](b7k_v7g_vfe_%2AA.json) |
| `*AA` | 杜玄之（杜瑗第三子） | [《宋書・良吏》][1116] | [JSON](b7k_v7g_vfe_%2AAA.json) |
| `*AB` | 杜慧度（交州刺史） | [《宋書・良吏》][1115] | [JSON](b7k_v7g_vfe_%2AAB.json) |
| `*ABA` | 杜弘文（杜慧度長子） | [《宋書・良吏》][1114] | [JSON](b7k_v7g_vfe_%2AABA.json) |
| `*ABB` | 杜弘猷（杜弘文弟） | [《宋書・良吏》][1114] | [JSON](b7k_v7g_vfe_%2AABB.json) |
| `*AC` | 杜慧期（交阯太守） | [《宋書・良吏》][1115] | [JSON](b7k_v7g_vfe_%2AAC.json) |
| `*AD` | 杜章民（九真太守） | [《宋書・良吏》][1115] | [JSON](b7k_v7g_vfe_%2AAD.json) |

</details>

<details><summary><code>bdx_txf_e62</code> 垣敞（垣護之祖）（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 垣敞（垣護之祖） | [《宋書・胡藩 劉康祖 垣護之 張興世》][1045] | [JSON](bdx_txf_e62.json) |
| `A` | 垣苗（垣護之父） | [《宋書・胡藩 劉康祖 垣護之 張興世》][1045] | [JSON](bdx_txf_e62_A.json) |
| `AA` | 垣護之（字彥宗） | [《宋書・朱脩之 宗愨 王玄謨》][1089] | [JSON](bdx_txf_e62_AA.json) |

</details>

<details><summary><code>bm8_bzq_1ee</code> 觀起（蔡大夫）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 觀起（蔡大夫） | [《史記・楚世家》][831] | [JSON](bm8_bzq_1ee.json) |
| `A` | 觀從（楚變亂謀者） | [《史記・楚世家》][831] | [JSON](bm8_bzq_1ee_A.json) |

</details>

<details><summary><code>bn4_lhp_9h1</code> 姑容（杞桓公）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 姑容（杞桓公） | [《史記・陳杞世家》][827] | [JSON](bn4_lhp_9h1.json) |
| `A` | 丐（杞孝公） | [《史記・陳杞世家》][827] | [JSON](bn4_lhp_9h1_A.json) |

</details>

<details><summary><code>buv_igi_gpn</code> 帝乙（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 帝乙 | [《史記・殷本紀》][811] | [JSON](buv_igi_gpn.json) |
| `A` | 微子啓 | [《史記・宋微子世家》][829] | [JSON](buv_igi_gpn_A.json) |

</details>

<details><summary><code>bvb_d1z_fd0</code> 尉佗（6 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 尉佗 | [《史記・南越列傳》][904] | [JSON](bvb_d1z_fd0.json) |
| `*A` | 胡 | [《史記・南越列傳》][904] | [JSON](bvb_d1z_fd0_%2AA.json) |
| `*AA` | 嬰齊 | [《史記・南越列傳》][904] | [JSON](bvb_d1z_fd0_%2AAA.json) |
| `*AAA` | 興 | [《史記・南越列傳》][904] | [JSON](bvb_d1z_fd0_%2AAAA.json) |
| `*AAB` | 次公 | [《史記・南越列傳》][904] | [JSON](bvb_d1z_fd0_%2AAAB.json) |
| `*AAC` | 建德 | [《史記・南越列傳》][904] | [JSON](bvb_d1z_fd0_%2AAAC.json) |

</details>

<details><summary><code>bwv_ob8_6xi</code> 共敖（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 共敖 | [《史記・項羽本紀》][815]、[《史記・秦楚之際月表》][1225] | [JSON](bwv_ob8_6xi.json) |
| `A` | 共尉 | [《史記・荊燕世家》][842]、[《史記・秦楚之際月表》][1225] | [JSON](bwv_ob8_6xi_A.json) |

</details>

<details><summary><code>c0i_eah_y59</code> 咎（韓世家釐王候選）（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 咎 | [《史記・韓世家》][836] | [JSON](c0i_eah_y59.json) |
| `A` | 桓惠王 | [《史記・韓世家》][836] | [JSON](c0i_eah_y59_A.json) |
| `AA` | 韓王安 | [《史記・韓世家》][836]、[《史記・六國年表》][1224] | [JSON](c0i_eah_y59_AA.json) |

</details>

<details><summary><code>c19_xxo_r8f</code> 直不疑（萬石張叔列傳候選）（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 直不疑 | [《史記・萬石張叔列傳》][894] | [JSON](c19_xxo_r8f.json) |
| `*A` | 望（直不疑孫） | [《史記・萬石張叔列傳》][894] | [JSON](c19_xxo_r8f_%2AA.json) |
| `A` | 相如（直不疑子） | [《史記・萬石張叔列傳》][894] | [JSON](c19_xxo_r8f_A.json) |

</details>

<details><summary><code>c1t_5mz_5ia</code> 晉昭公（趙世家候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 晉昭公 | [《史記・趙世家》][834] | [JSON](c1t_5mz_5ia.json) |
| `**A` | 驕 | [《史記・趙世家》][834] | [JSON](c1t_5mz_5ia_%2A%2AA.json) |

</details>

<details><summary><code>c27_590_7e3</code> 賈充（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 賈充 | [《晉書・王沈 荀顗 荀勖 馮紞》][158] | [JSON](c27_590_7e3.json) |
| `A` | 賈充女（荀顗薦選太子妃者） | [《晉書・王沈 荀顗 荀勖 馮紞》][158] | [JSON](c27_590_7e3_A.json) |

</details>

<details><summary><code>c2w_s7g_en0</code> 楚懷王（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 楚懷王 | [《史記・楚世家》][831] | [JSON](c2w_s7g_en0.json) |
| `*A` | 楚懷王心 | [《史記・高祖本紀》][816] | [JSON](c2w_s7g_en0_%2AA.json) |
| `A` | 子蘭（楚懷王子） | [《史記・屈原賈生列傳》][875] | [JSON](c2w_s7g_en0_A.json) |

</details>

<details><summary><code>c46_2c9_597</code> 唐衡（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 唐衡 | [《三國志・二荀賈傳》][736] | [JSON](c46_2c9_597.json) |
| `A` | 唐氏（荀彧妻，唐衡女） | [《三國志・二荀賈傳》][736] | [JSON](c46_2c9_597_A.json) |

</details>

<details><summary><code>c9d_jla_uhp</code> 吳景安（吳明徹祖）（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 吳景安（吳明徹祖） | [《陳書・列傳第三: 侯瑱 歐陽頠 吳明徹 裴子烈》][21] | [JSON](c9d_jla_uhp.json) |
| `A` | 吳樹（吳明徹父） | [《陳書・列傳第三: 侯瑱 歐陽頠 吳明徹 裴子烈》][21] | [JSON](c9d_jla_uhp_A.json) |
| `AA` | 吳明徹（字通昭） | [《陳書・列傳第三: 侯瑱 歐陽頠 吳明徹 裴子烈》][21] | [JSON](c9d_jla_uhp_AA.json) |

</details>

<details><summary><code>ccd_af3_98e</code> 建平王宏（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 建平王宏 | [《南齊書・王琨 張岱 褚炫 何戢 王延之 阮韜》][452]、[《南史・王曇首》][621]、[《南史・王曇首》][620]、[《宋書・后妃》][1015]、[《宋書・徐湛之 江湛 王僧綽》][1081]、[《宋書・徐湛之 江湛 王僧綽》][1079]、[《宋書・徐湛之 江湛 王僧綽》][1080]、[《資治通鑑・宋紀十五》][1213] | [JSON](ccd_af3_98e.json) |
| `A` | 劉景素（宋建平王，劉宏子） | [《南齊書・江斆 何昌㝢 謝𤅢 王思遠》][483]、[《南史・王裕之　王鎮之　王韶之　王悅之　王准之》][669] | [JSON](ccd_af3_98e_A.json) |
| `AA` | 劉景素女（建平王女） | — | [JSON](ccd_af3_98e_AA.json) |

</details>

<details><summary><code>ce8_yhf_283</code> 楊鉉（《隋書》高祖世系）（7 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 楊鉉（《隋書》高祖世系） | [《隋書・帝紀第1 高祖上》][1140] | [JSON](ce8_yhf_283.json) |
| `A` | 楊元壽（《隋書》高祖世系） | [《隋書・帝紀第1 高祖上》][1140] | [JSON](ce8_yhf_283_A.json) |
| `AA` | 楊惠嘏（《隋書》高祖世系） | [《隋書・帝紀第1 高祖上》][1140] | [JSON](ce8_yhf_283_AA.json) |
| `AAA` | 楊烈（楊禎父） | [《隋書・帝紀第1 高祖上》][1140] | [JSON](ce8_yhf_283_AAA.json) |
| `AAAA` | 楊禎（楊忠父） | [《隋書・帝紀第1 高祖上》][1140] | [JSON](ce8_yhf_283_AAAA.json) |
| `AAAAA` | 楊忠（隋文帝父） | [《隋書・帝紀第1 高祖上》][1140] | [JSON](ce8_yhf_283_AAAAA.json) |
| `AAAAAA` | 楊堅（隋文帝） | [《隋書・帝紀第1 高祖上》][1140] | [JSON](ce8_yhf_283_AAAAAA.json) |

</details>

<details><summary><code>cek_1yy_pne</code> 奄父（趙世家候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 奄父 | [《史記・趙世家》][834] | [JSON](cek_1yy_pne.json) |
| `A` | 叔帶 | [《史記・趙世家》][834] | [JSON](cek_1yy_pne_A.json) |

</details>

<details><summary><code>ceq_pnr_q0e</code> 殷叡〔齊，殷鈞父〕（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 殷叡〔齊，殷鈞父〕 | [《南齊書・王奐 從弟繢 張沖》][505]、[《南史・王誕　王華　王惠　王彧》][640] | [JSON](ceq_pnr_q0e.json) |
| `A` | 殷鈞 | [《南史・王曇首》][629]、[《南史・王曇首》][628] | [JSON](ceq_pnr_q0e_A.json) |

</details>

<details><summary><code>chi_c64_eif</code> 徐真（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 徐真 | [《三國志・妃嬪傳》][770] | [JSON](chi_c64_eif.json) |
| `A` | 徐琨 | [《三國志・妃嬪傳》][770] | [JSON](chi_c64_eif_A.json) |

</details>

<details><summary><code>cjd_ybv_2wu</code> 蜚廉（趙世家祖系候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 蜚廉 | [《史記・趙世家》][834] | [JSON](cjd_ybv_2wu.json) |
| `A` | 惡來 | [《史記・趙世家》][834] | [JSON](cjd_ybv_2wu_A.json) |

</details>

<details><summary><code>cti_o52_4nz</code> 宋明帝彧（6 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 宋明帝彧 | [《魏書・燕鳳 許謙 張衮 崔玄伯 鄧淵》][1164] | [JSON](cti_o52_4nz.json) |
| `A` | 陽羨公主 | [《文獻通考・卷二百五十八》][1180] | [JSON](cti_o52_4nz_A.json) |
| `B` | 劉伯姒（晉陵長公主） | [《南史・后妃上》][547]、[《南史・后妃上》][548]、[《宋書・后妃》][1018] | [JSON](cti_o52_4nz_B.json) |
| `C` | 劉伯媛（建安長公主） | [《南史・后妃上》][547]、[《南史・后妃上》][548]、[《宋書・后妃》][1018] | [JSON](cti_o52_4nz_C.json) |
| `D` | 臨淮公主（南朝宋，王瑩妻） | [《南史・王誕　王華　王惠　王彧》][653]、[《文獻通考・卷二百五十八》][1180] | [JSON](cti_o52_4nz_D.json) |
| `E` | 劉贊（字仲敷，宋武陵王） | [《宋書・孝武十四王》][1099] | [JSON](cti_o52_4nz_E.json) |

</details>

<details><summary><code>d50_8f5_wul</code> 嘉〔張茂度高祖〕（29 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 嘉〔張茂度高祖〕 | [《宋書・張茂度 庾登之 謝方明 江夷》][1058] | [JSON](d50_8f5_wul.json) |
| `A` | 澄〔張茂度曾祖〕 | [《宋書・張茂度 庾登之 謝方明 江夷》][1058] | [JSON](d50_8f5_wul_A.json) |
| `AA` | 彭祖〔張茂度祖〕 | [《宋書・張茂度 庾登之 謝方明 江夷》][1058] | [JSON](d50_8f5_wul_AA.json) |
| `AAA` | 張敞〔邵父〕 | [《宋書・趙倫之 王懿 張邵》][1033] | [JSON](d50_8f5_wul_AAA.json) |
| `AAAA` | 張裕〔字茂度〕 | [《宋書・張茂度 庾登之 謝方明 江夷》][1058] | [JSON](d50_8f5_wul_AAAA.json) |
| `AAAAA` | 張演〔046／053父系歧異〕 | [《宋書・張茂度 庾登之 謝方明 江夷》][1058] | [JSON](d50_8f5_wul_AAAAA.json) |
| `AAAAB` | 張鏡〔046／053父系歧異〕 | [《南齊書・王琨 張岱 褚炫 何戢 王延之 阮韜》][448]、[《南齊書・王琨 張岱 褚炫 何戢 王延之 阮韜》][449] | [JSON](d50_8f5_wul_AAAAB.json) |
| `AAAAC` | 張寅 | [《南齊書・王琨 張岱 褚炫 何戢 王延之 阮韜》][448] | [JSON](d50_8f5_wul_AAAAC.json) |
| `AAAACA` | 張緒 | [《南齊書・王僧虔 張緒》][454]、[《南史・張裕》][693] | [JSON](d50_8f5_wul_AAAACA.json) |
| `AAAACAA` | 張充（字延符） | [《梁書・王亮 張稷 王瑩》][329]、[《梁書・王瞻 王志 王峻 王暕 子訓 王泰 王份 孫鍚 僉 張充 柳惲 蔡撙 江蒨》][344] | [JSON](d50_8f5_wul_AAAACAA.json) |
| `AAAAD` | 張岱（字景山，張茂度子） | [《南齊書・王琨 張岱 褚炫 何戢 王延之 阮韜》][448] | [JSON](d50_8f5_wul_AAAAD.json) |
| `AAAAE` | 張永（字景雲） | [《梁書・王亮 張稷 王瑩》][329]、[《南齊書・王琨 張岱 褚炫 何戢 王延之 阮韜》][448]、[《南齊書・王奐 從弟繢 張沖》][508]、[《南史・王誕　王華　王惠　王彧》][654] | [JSON](d50_8f5_wul_AAAAE.json) |
| `AAAAEA` | 張瑰（字祖逸） | [《南齊書・王琨 張岱 褚炫 何戢 王延之 阮韜》][450]、[《南史・張裕》][691] | [JSON](d50_8f5_wul_AAAAEA.json) |
| `AAAAEAA` | 張率（字士簡） | [《梁書・王僧孺 張率 劉孝綽 王筠》][364] | [JSON](d50_8f5_wul_AAAAEAA.json) |
| `AAAAF` | 張辨（廣州刺史，宋書作辯） | [《南齊書・王琨 張岱 褚炫 何戢 王延之 阮韜》][448] | [JSON](d50_8f5_wul_AAAAF.json) |
| `AAAAG` | 張恕（張岱弟、張瓌叔） | [《南齊書・王琨 張岱 褚炫 何戢 王延之 阮韜》][450] | [JSON](d50_8f5_wul_AAAAG.json) |
| `AAAB` | 張褘〔059亦禕，046偉；張暢父〕 | [《宋書・殷淳 張暢 何偃 江智淵》][1063] | [JSON](d50_8f5_wul_AAAB.json) |
| `AAABA` | 張暢 | [《宋書・殷淳 張暢 何偃 江智淵》][1063] | [JSON](d50_8f5_wul_AAABA.json) |
| `AAABAA` | 張浩〔張暢子〕 | [《宋書・殷淳 張暢 何偃 江智淵》][1063] | [JSON](d50_8f5_wul_AAABAA.json) |
| `AAABAB` | 張淹〔張暢子〕 | [《宋書・殷淳 張暢 何偃 江智淵》][1063] | [JSON](d50_8f5_wul_AAABAB.json) |
| `AAABAC` | 張融（字思光） | [《梁書・王亮 張稷 王瑩》][329]、[《南齊書・張融 周顒》][472] | [JSON](d50_8f5_wul_AAABAC.json) |
| `AAABB` | 張牧〔張暢弟〕 | [《宋書・趙倫之 王懿 張邵》][1028]、[《宋書・殷淳 張暢 何偃 江智淵》][1063] | [JSON](d50_8f5_wul_AAABB.json) |
| `AAABC` | 張說〔046作悦〕 | [《宋書・趙倫之 王懿 張邵》][1037] | [JSON](d50_8f5_wul_AAABC.json) |
| `AAAC` | 張邵 | [《宋書・趙倫之 王懿 張邵》][1033] | [JSON](d50_8f5_wul_AAAC.json) |
| `AAACA` | 張敷 | [《宋書・趙倫之 王懿 張邵》][1033] | [JSON](d50_8f5_wul_AAACA.json) |
| `AAACB` | 張柬〔敷弟〕 | [《宋書・趙倫之 王懿 張邵》][1031]、[《宋書・趙倫之 王懿 張邵》][1033] | [JSON](d50_8f5_wul_AAACB.json) |
| `AAACBA` | 張式〔柬子〕 | [《宋書・趙倫之 王懿 張邵》][1033]、[《宋書・趙倫之 王懿 張邵》][1034] | [JSON](d50_8f5_wul_AAACBA.json) |
| `AAACBB` | 張沖（字思約，張柬子，出繼張敷） | [《南齊書・王奐 從弟繢 張沖》][508] | [JSON](d50_8f5_wul_AAACBB.json) |
| `AAACBBA` | 張孜（郢州刺史張沖子） | [《南齊書・王奐 從弟繢 張沖》][508] | [JSON](d50_8f5_wul_AAACBBA.json) |

</details>

<details><summary><code>d5x_77n_qxq</code> 陸閑（字遐業）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 陸閑（字遐業） | [《梁書・陸倕 到洽 明山賓 殷鈞 陸襄》][350] | [JSON](d5x_77n_qxq.json) |
| `A` | 陸襄（字師卿） | [《梁書・陸倕 到洽 明山賓 殷鈞 陸襄》][350] | [JSON](d5x_77n_qxq_A.json) |

</details>

<details><summary><code>d7u_bgr_wdi</code> 蟲達（史表作蠱逢）（4 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 蟲達（史表作蠱逢） | [《漢書・髙惠髙后文功臣表》曲成列][1232] | [JSON](d7u_bgr_wdi.json) |
| `***A` | 宣（蟲達玄孫） | [《漢書・髙惠髙后文功臣表》曲成列][1232] | [JSON](d7u_bgr_wdi_%2A%2A%2AA.json) |
| `*A` | 皇柔（史表作皋柔） | [《史記・高祖功臣侯者年表》][1227] | [JSON](d7u_bgr_wdi_%2AA.json) |
| `A` | 捷（曲城侯） | [《漢書・髙惠髙后文功臣表》曲成列][1232]、[《史記・高祖功臣侯者年表》][1227] | [JSON](d7u_bgr_wdi_A.json) |

</details>

<details><summary><code>d96_1fa_e9a</code> 劉聰（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 劉聰 | [《晉書・王沈 荀顗 荀勖 馮紞》][158]、[《晉書・山濤 王戎 郭舒 樂廣》][164]、[《晉書・鄭袤 李胤 盧欽 華表 石鑒 溫羨》][173]、[《晉書・鄭袤 李胤 盧欽 華表 石鑒 溫羨》][178]、[《晉書・汝南王亮 楚王瑋 趙王倫 齊王冏 長沙王乂 成都王潁 河間王顒 東海王越》][200]、[《晉書・汝南王亮 楚王瑋 趙王倫 齊王冏 長沙王乂 成都王潁 河間王顒 東海王越》][201]、[《晉書・溫嶠 郗鑒》][214]、[《晉書・列女》][271]、[《晉書・列女》][270]、[《晉書・劉聰》][290]、[《太平御覽・宗親部九》][1158] | [JSON](d96_1fa_e9a.json) |
| `A` | 劉粲〔字士光〕 | [《晉書・鄭袤 李胤 盧欽 華表 石鑒 溫羨》][178] | [JSON](d96_1fa_e9a_A.json) |

</details>

<details><summary><code>dad_b77_b38</code> 魏武（引古）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 魏武（引古） | [《三國志・二荀賈傳》][736] | [JSON](dad_b77_b38.json) |
| `A` | 安陽公主 | [《三國志・二荀賈傳》][736] | [JSON](dad_b77_b38_A.json) |

</details>

<details><summary><code>djo_u3b_i9w</code> 殷羨（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 殷羨 | [《晉書・陸曄 何充 褚翜 蔡謨 諸葛恢 殷浩》][248] | [JSON](djo_u3b_i9w.json) |
| `A` | 殷浩 | [《晉書・陸曄 何充 褚翜 蔡謨 諸葛恢 殷浩》][248] | [JSON](djo_u3b_i9w_A.json) |
| `AA` | 殷涓 | [《晉書・叛臣一》][281] | [JSON](djo_u3b_i9w_AA.json) |

</details>

<details><summary><code>dkn_ge4_286</code> 司馬鈞（53 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 司馬鈞 | [《晉書・高祖宣帝》][85] | [JSON](dkn_ge4_286.json) |
| `A` | 司馬量 | [《晉書・高祖宣帝》][85] | [JSON](dkn_ge4_286_A.json) |
| `AA` | 司馬儁 | [《晉書・高祖宣帝》][85] | [JSON](dkn_ge4_286_AA.json) |
| `AAA` | 司馬防 | [《晉書・高祖宣帝》][85] | [JSON](dkn_ge4_286_AAA.json) |
| `AAAA` | 司馬懿 | [《三國志・諸夏侯曹傳》][734] | [JSON](dkn_ge4_286_AAAA.json) |
| `AAAAA` | 司馬伷 | [《晉書・宣五王 文六王》][157] | [JSON](dkn_ge4_286_AAAAA.json) |
| `AAAAAA` | 司馬覲 | [《晉書・宣五王 文六王》][157] | [JSON](dkn_ge4_286_AAAAAA.json) |
| `AAAAAAA` | 晉元帝 | [《晉書・王導》][212] | [JSON](dkn_ge4_286_AAAAAAA.json) |
| `AAAAAAAA` | 晉明帝 | [《晉書・庾亮》][230] | [JSON](dkn_ge4_286_AAAAAAAA.json) |
| `AAAAAAAAA` | 晉成帝 | [《晉書・庾亮》][230] | [JSON](dkn_ge4_286_AAAAAAAAA.json) |
| `AAAAAAAB` | 琅邪孝王裒 | [《晉書・武十三王 元四王 簡文三子》][209] | [JSON](dkn_ge4_286_AAAAAAAB.json) |
| `AAAAAAABA` | 司馬安國 | [《晉書・武十三王 元四王 簡文三子》][209] | [JSON](dkn_ge4_286_AAAAAAABA.json) |
| `AAAAAAAC` | 東海哀王沖 | [《晉書・庾亮》][229] | [JSON](dkn_ge4_286_AAAAAAAC.json) |
| `AAAAAAAD` | 武陵威王晞 | [《晉書・王舒 王廙 虞潭 顧眾 張闓》][239] | [JSON](dkn_ge4_286_AAAAAAAD.json) |
| `AAAAAAAE` | 琅邪悼王煥 | [《晉書・后妃下》][150]、[《晉書・武十三王 元四王 簡文三子》][209] | [JSON](dkn_ge4_286_AAAAAAAE.json) |
| `AAAAAAAF` | 晉簡文帝 | [《晉書・叛臣一》][281] | [JSON](dkn_ge4_286_AAAAAAAF.json) |
| `AAAAAAAFA` | 司馬道子 | [《晉書・王湛 荀崧 范汪 劉惔 張憑 韓伯》][233] | [JSON](dkn_ge4_286_AAAAAAAFA.json) |
| `AAAAAAAFB` | 司馬道福 | [《太平御覽・皇親部十五》][1150] | [JSON](dkn_ge4_286_AAAAAAAFB.json) |
| `AAAAAAAG` | 尋陽公主 | [《晉書・后妃下》][150] | [JSON](dkn_ge4_286_AAAAAAAG.json) |
| `AAAAAAB` | 司馬渾 | [《晉書・宣五王 文六王》][157]、[《晉書・武十三王 元四王 簡文三子》][209] | [JSON](dkn_ge4_286_AAAAAAB.json) |
| `AAAAAB` | 司馬澹 | [《晉書・孝懷帝 孝愍帝》][96]、[《晉書・宣五王 文六王》][157] | [JSON](dkn_ge4_286_AAAAAB.json) |
| `AAAAAC` | 司馬繇 | [《晉書・山濤 王戎 郭舒 樂廣》][169] | [JSON](dkn_ge4_286_AAAAAC.json) |
| `AAAAAD` | 司馬漼 | [《晉書・宣五王 文六王》][157] | [JSON](dkn_ge4_286_AAAAAD.json) |
| `AAAAB` | 司馬幹 | [《晉書・王沈 荀顗 荀勖 馮紞》][158] | [JSON](dkn_ge4_286_AAAAB.json) |
| `AAAAC` | 司馬亮 | [《晉書・汝南王亮 楚王瑋 趙王倫 齊王冏 長沙王乂 成都王潁 河間王顒 東海王越》][202] | [JSON](dkn_ge4_286_AAAAC.json) |
| `AAAACA` | 司馬粹 | [《晉書・汝南王亮 楚王瑋 趙王倫 齊王冏 長沙王乂 成都王潁 河間王顒 東海王越》][202] | [JSON](dkn_ge4_286_AAAACA.json) |
| `AAAACB` | 司馬矩 | [《晉書・汝南王亮 楚王瑋 趙王倫 齊王冏 長沙王乂 成都王潁 河間王顒 東海王越》][202] | [JSON](dkn_ge4_286_AAAACB.json) |
| `AAAACC` | 司馬羕 | [《晉書・汝南王亮 楚王瑋 趙王倫 齊王冏 長沙王乂 成都王潁 河間王顒 東海王越》][202] | [JSON](dkn_ge4_286_AAAACC.json) |
| `AAAACC*A` | 瑉（羕孫） | [《晉書・汝南王亮 楚王瑋 趙王倫 齊王冏 長沙王乂 成都王潁 河間王顒 東海王越》][202] | [JSON](dkn_ge4_286_AAAACC%2AA.json) |
| `AAAACC*B` | 崧（羕孫、生父未名） | [《晉書・汝南王亮 楚王瑋 趙王倫 齊王冏 長沙王乂 成都王潁 河間王顒 東海王越》][202]、[《資治通鑑・晉紀十六》][1200] | [JSON](dkn_ge4_286_AAAACC%2AB.json) |
| `AAAACCA` | 播（羕世子） | [《晉書・汝南王亮 楚王瑋 趙王倫 齊王冏 長沙王乂 成都王潁 河間王顒 東海王越》][202] | [JSON](dkn_ge4_286_AAAACCA.json) |
| `AAAACCB` | 充（羕子、播弟） | [《晉書・汝南王亮 楚王瑋 趙王倫 齊王冏 長沙王乂 成都王潁 河間王顒 東海王越》][202]、[《資治通鑑・晉紀十六》][1200] | [JSON](dkn_ge4_286_AAAACCB.json) |
| `AAAACD` | 司馬宗 | [《晉書・庾亮》][230] | [JSON](dkn_ge4_286_AAAACD.json) |
| `AAAACE` | 司馬熙 | [《晉書・汝南王亮 楚王瑋 趙王倫 齊王冏 長沙王乂 成都王潁 河間王顒 東海王越》][202] | [JSON](dkn_ge4_286_AAAACE.json) |
| `AAAAD` | 司馬京 | [《晉書・宣五王 文六王》][157] | [JSON](dkn_ge4_286_AAAAD.json) |
| `AAAAE` | 司馬駿 | [《晉書・宣五王 文六王》][157]、[《晉書・王沈 荀顗 荀勖 馮紞》][158]、[《晉書・王渾 王濬 唐彬》][160] | [JSON](dkn_ge4_286_AAAAE.json) |
| `AAAAF` | 司馬肜 | [《晉書・山濤 王戎 郭舒 樂廣》][169] | [JSON](dkn_ge4_286_AAAAF.json) |
| `AAAAG` | 司馬倫 | [《晉書・汝南王亮 楚王瑋 趙王倫 齊王冏 長沙王乂 成都王潁 河間王顒 東海王越》][200] | [JSON](dkn_ge4_286_AAAAG.json) |
| `AAAAH` | 司馬景王 | [《晉書・山濤 王戎 郭舒 樂廣》][165]、[《三國志・諸夏侯曹傳》][734] | [JSON](dkn_ge4_286_AAAAH.json) |
| `AAAAI` | 司馬文王 | [《晉書・王沈 荀顗 荀勖 馮紞》][158] | [JSON](dkn_ge4_286_AAAAI.json) |
| `AAAAJ` | 高陵宣公主（晉宣帝第二女，杜預妻） | [《陳書・列傳第十一: 王沖 王通 袁敬》][34] | [JSON](dkn_ge4_286_AAAAJ.json) |
| `AAAB` | 司馬朗 | [《晉書・高祖宣帝》][85] | [JSON](dkn_ge4_286_AAAB.json) |
| `AAAC` | 孚（安平獻王） | [《晉書・宗室》][156] | [JSON](dkn_ge4_286_AAAC.json) |
| `AAAD` | 馗（宣帝弟、權父） | [《晉書・宗室》][156] | [JSON](dkn_ge4_286_AAAD.json) |
| `AAADA` | 彭城穆王權 | [《晉書・宗室》][156] | [JSON](dkn_ge4_286_AAADA.json) |
| `AAADAA` | 彭城元王植 | [《晉書・宗室》][156] | [JSON](dkn_ge4_286_AAADAA.json) |
| `AAADAAA` | 彭城康王釋 | [《晉書・宗室》][156] | [JSON](dkn_ge4_286_AAADAAA.json) |
| `AAADAAAA` | 彭城王雄 | [《晉書・宗室》][156]、[《資治通鑑・晉紀十六》][1200] | [JSON](dkn_ge4_286_AAADAAAA.json) |
| `AAADAAAB` | 紘（釋子） | [《晉書・宗室》][156] | [JSON](dkn_ge4_286_AAADAAAB.json) |
| `AAAE` | 恂（八達之一） | [《晉書・宗室》][156] | [JSON](dkn_ge4_286_AAAE.json) |
| `AAAF` | 進（八達之一） | [《晉書・宗室》][156] | [JSON](dkn_ge4_286_AAAF.json) |
| `AAAG` | 通（八達之一） | [《晉書・宗室》][156] | [JSON](dkn_ge4_286_AAAG.json) |
| `AAAH` | 敏（八達之一） | [《晉書・宗室》][156] | [JSON](dkn_ge4_286_AAAH.json) |

</details>

<details><summary><code>dm0_58v_50i</code> 趙衰（5 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 趙衰 | [《史記・晉世家》][830] | [JSON](dm0_58v_50i.json) |
| `A` | 趙盾 | [《史記・晉世家》][830] | [JSON](dm0_58v_50i_A.json) |
| `B` | 趙同 | [《史記・趙世家》][834] | [JSON](dm0_58v_50i_B.json) |
| `C` | 趙括 | [《史記・趙世家》][834] | [JSON](dm0_58v_50i_C.json) |
| `D` | 趙嬰齊 | [《史記・趙世家》][834] | [JSON](dm0_58v_50i_D.json) |

</details>

<details><summary><code>dq6_ovk_58c</code> 張釋之（張釋之馮唐列傳候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 張釋之 | [《史記・張釋之馮唐列傳》][893] | [JSON](dq6_ovk_58c.json) |
| `A` | 張摯 | [《史記・張釋之馮唐列傳》][893] | [JSON](dq6_ovk_58c_A.json) |

</details>

<details><summary><code>e00_pe1_zri</code> 無諸（東越列傳候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 無諸 | [《史記・東越列傳》][905] | [JSON](e00_pe1_zri.json) |
| `*A` | 丑 | [《史記・東越列傳》][905] | [JSON](e00_pe1_zri_%2AA.json) |

</details>

<details><summary><code>e1z_w57_m3h</code> 滕牧（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 滕牧 | [《三國志・妃嬪傳》][767] | [JSON](e1z_w57_m3h.json) |
| `A` | 滕氏〔孫皓皇后、滕牧女〕 | [《三國志・妃嬪傳》][767] | [JSON](e1z_w57_m3h_A.json) |

</details>

<details><summary><code>e2r_5iw_ui0</code> 劉穎之（4 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 劉穎之 | [《宋書・殷孝祖 劉勔》][1108] | [JSON](e2r_5iw_ui0.json) |
| `A` | 劉勔 | [《宋書・薛安都 沈文秀 崔道固》][1110] | [JSON](e2r_5iw_ui0_A.json) |
| `AA` | 劉繪（字士章） | [《梁書・王僧孺 張率 劉孝綽 王筠》][360] | [JSON](e2r_5iw_ui0_AA.json) |
| `AAA` | 劉潛（字孝儀） | [《梁書・韋粲 江子一 弟子四 子五 張嵊 沈浚 柳敬禮》][377] | [JSON](e2r_5iw_ui0_AAA.json) |

</details>

<details><summary><code>e5k_f2i_cog</code> 郗曇（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 郗曇 | [《晉書・溫嶠 郗鑒》][219]、[《晉書・溫嶠 郗鑒》][218] | [JSON](e5k_f2i_cog.json) |
| `A` | 郗道茂 | [《世說新語・德行》][927] | [JSON](e5k_f2i_cog_A.json) |

</details>

<details><summary><code>e8h_aeo_zy8</code> 孫輔〔孫權從兄、駱統妻父〕（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 孫輔〔孫權從兄、駱統妻父〕 | [《三國志・虞陸張駱陸吾朱傳》][792] | [JSON](e8h_aeo_zy8.json) |
| `A` | 孫氏〔孫輔女、駱統妻〕 | [《三國志・虞陸張駱陸吾朱傳》][792] | [JSON](e8h_aeo_zy8_A.json) |

</details>

<details><summary><code>e9c_070_567</code> 孫策（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 孫策 | [《三國志・虞陸張駱陸吾朱傳》][795] | [JSON](e9c_070_567.json) |
| `A` | 孫氏〔孫策女、顧邵妻〕 | [《三國志・張顧諸葛步傳》][775] | [JSON](e9c_070_567_A.json) |
| `B` | 孫氏〔孫策女、陸遜妻〕 | [《三國志・陸遜傳》][800] | [JSON](e9c_070_567_B.json) |

</details>

<details><summary><code>ea5_zvr_hlp</code> 張良（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 張良 | [《史記・留侯世家》][846] | [JSON](ea5_zvr_hlp.json) |
| `A` | 張辟彊 | [《史記・呂后本紀》][817] | [JSON](ea5_zvr_hlp_A.json) |
| `B` | 不疑 | [《史記・留侯世家》][846] | [JSON](ea5_zvr_hlp_B.json) |

</details>

<details><summary><code>eaj_zin_zxy</code> 休先〔新唐陳氏序〕（4 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 休先〔新唐陳氏序〕 | [《陳書・列傳第八: 衡陽獻王昌 南康愍王曇朗》][23]、[《新唐書・宰相世系一下》][1188] | [JSON](eaj_zin_zxy.json) |
| `A` | 陳曇朗（南康愍王） | [《陳書・列傳第八: 衡陽獻王昌 南康愍王曇朗》][23] | [JSON](eaj_zin_zxy_A.json) |
| `AA` | 陳方泰（陳曇朗子） | [《陳書・列傳第八: 衡陽獻王昌 南康愍王曇朗》][23] | [JSON](eaj_zin_zxy_AA.json) |
| `AB` | 陳方慶（臨汝縣侯） | [《陳書・列傳第八: 衡陽獻王昌 南康愍王曇朗》][24] | [JSON](eaj_zin_zxy_AB.json) |

</details>

<details><summary><code>ebb_5a7_96e</code> 郗恢（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 郗恢 | [《晉書・溫嶠 郗鑒》][219] | [JSON](ebb_5a7_96e.json) |
| `A` | 郗循 | [《晉書・溫嶠 郗鑒》][219] | [JSON](ebb_5a7_96e_A.json) |

</details>

<details><summary><code>egx_xax_4ic</code> 蕭承之（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 蕭承之 | [《南史・后妃上》][522]、[《南史・后妃上》][523] | [JSON](egx_xax_4ic.json) |
| `A` | 蕭道度 | [《南齊書・高帝下》][394]、[《南齊書・皇后》][405]、[《南齊書・皇后》][404]、[《南史・后妃上》][522]、[《南史・后妃上》][523] | [JSON](egx_xax_4ic_A.json) |

</details>

<details><summary><code>ei2_qej_czn</code> 公乘氏（張耳陳餘列傳候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 公乘氏 | [《史記・張耳陳餘列傳》][880] | [JSON](ei2_qej_czn.json) |
| `A` | 陳餘妻未名 | [《史記・張耳陳餘列傳》][880] | [JSON](ei2_qej_czn_A.json) |

</details>

<details><summary><code>ei7_fai_lvy</code> 丑（鄭世家共公候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 丑 | [《史記・鄭世家》][833] | [JSON](ei7_fai_lvy.json) |
| `A` | 已 | [《史記・鄭世家》][833] | [JSON](ei7_fai_lvy_A.json) |

</details>

<details><summary><code>ejj_vdz_hxw</code> 朱據（4 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 朱據 | [《三國志・虞陸張駱陸吾朱傳》][797] | [JSON](ejj_vdz_hxw.json) |
| `A` | 朱熊〔朱據子〕 | [《三國志・妃嬪傳》][771]、[《三國志・虞陸張駱陸吾朱傳》][797] | [JSON](ejj_vdz_hxw_A.json) |
| `AA` | 朱宣〔朱熊子〕 | [《三國志・虞陸張駱陸吾朱傳》][797] | [JSON](ejj_vdz_hxw_AA.json) |
| `B` | 朱損〔朱據子〕 | [《三國志・妃嬪傳》][771] | [JSON](ejj_vdz_hxw_B.json) |

</details>

<details><summary><code>em3_mum_s8d</code> 朱愷之（晉右衞將軍）（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 朱愷之（晉右衞將軍） | [《宋書・隱逸》][1137] | [JSON](em3_mum_s8d.json) |
| `A` | 朱濤（揚州主簿） | [《宋書・隱逸》][1137] | [JSON](em3_mum_s8d_A.json) |
| `AA` | 朱百年（會稽山陰人） | [《宋書・隱逸》][1135]、[《宋書・隱逸》][1137] | [JSON](em3_mum_s8d_AA.json) |

</details>

<details><summary><code>eom_42c_5zd</code> 華恆〔廷尉〕（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 華恆〔廷尉〕 | [《晉書・鄭袤 李胤 盧欽 華表 石鑒 溫羨》][173] | [JSON](eom_42c_5zd.json) |
| `A` | 華俊〔華恆子〕 | [《晉書・鄭袤 李胤 盧欽 華表 石鑒 溫羨》][173] | [JSON](eom_42c_5zd_A.json) |
| `AA` | 華仰之〔大長秋〕 | [《晉書・鄭袤 李胤 盧欽 華表 石鑒 溫羨》][173] | [JSON](eom_42c_5zd_AA.json) |

</details>

<details><summary><code>ere_ume_47r</code> 吳景〔吳夫人弟〕（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 吳景〔吳夫人弟〕 | [《三國志・妃嬪傳》][768] | [JSON](ere_ume_47r.json) |
| `A` | 吳奮 | [《三國志・妃嬪傳》][768] | [JSON](ere_ume_47r_A.json) |
| `AA` | 吳安 | [《三國志・妃嬪傳》][768]、[《三國志・吳主五子傳》][802] | [JSON](ere_ume_47r_AA.json) |

</details>

<details><summary><code>esh_e0a_jrw</code> 石奮父未名（萬石張叔列傳候選）（7 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 石奮父未名 | [《史記・萬石張叔列傳》][894] | [JSON](esh_e0a_jrw.json) |
| `A` | 石奮 | [《史記・萬石張叔列傳》][894] | [JSON](esh_e0a_jrw_A.json) |
| `AA` | 建（石奮長子） | [《史記・萬石張叔列傳》][894] | [JSON](esh_e0a_jrw_AA.json) |
| `AB` | 甲（石奮次子失名佔位） | [《史記・萬石張叔列傳》][894] | [JSON](esh_e0a_jrw_AB.json) |
| `AC` | 乙（石奮次子失名佔位） | [《史記・萬石張叔列傳》][894] | [JSON](esh_e0a_jrw_AC.json) |
| `AD` | 慶（石奮子） | [《史記・萬石張叔列傳》][894] | [JSON](esh_e0a_jrw_AD.json) |
| `ADA` | 德（石慶中子） | [《史記・萬石張叔列傳》][894] | [JSON](esh_e0a_jrw_ADA.json) |

</details>

<details><summary><code>eva_gs1_9n5</code> 魏文侯（趙世家候選）（7 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 魏文侯 | [《史記・趙世家》][834] | [JSON](eva_gs1_9n5.json) |
| `A` | 撃 | [《史記・魏世家》][835] | [JSON](eva_gs1_9n5_A.json) |
| `AA` | 罃 | [《史記・魏世家》][835] | [JSON](eva_gs1_9n5_AA.json) |
| `AAA` | 襄王 | [《史記・魏世家》][835] | [JSON](eva_gs1_9n5_AAA.json) |
| `AAAA` | 哀王 | [《史記・魏世家》][835] | [JSON](eva_gs1_9n5_AAAA.json) |
| `AAAAA` | 昭王 | [《史記・魏世家》][835] | [JSON](eva_gs1_9n5_AAAAA.json) |
| `AAAAAA` | 安釐王 | [《史記・魏公子列傳》][868] | [JSON](eva_gs1_9n5_AAAAAA.json) |

</details>

<details><summary><code>evj_3wb_3l3</code> 姚信（6 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 姚信 | [《陳書・列傳第二十一: 江總 姚察》][41]、[《三國志・虞陸張駱陸吾朱傳》][790]、[《三國志・陸遜傳》][800]、[《三國志・吳主五子傳》][805]、[《周書・藝術》][1193] | [JSON](evj_3wb_3l3.json) |
| `****A` | 姚郢（姚僧垣曾祖） | [《周書・藝術》][1193] | [JSON](evj_3wb_3l3_%2A%2A%2A%2AA.json) |
| `****A*A` | 姚菩提（梁高平令） | [《周書・藝術》][1193] | [JSON](evj_3wb_3l3_%2A%2A%2A%2AA%2AA.json) |
| `****A*AA` | 姚僧垣（字法衞） | [《周書・藝術》][1193] | [JSON](evj_3wb_3l3_%2A%2A%2A%2AA%2AAA.json) |
| `****A*AAA` | 姚察（字伯審） | [《陳書・列傳第二十一: 江總 姚察》][41] | [JSON](evj_3wb_3l3_%2A%2A%2A%2AA%2AAAA.json) |
| `****A*AAAA` | 姚思廉（姚察子，奉詔續成梁陳史） | [《陳書・列傳第二十一: 江總 姚察》][41] | [JSON](evj_3wb_3l3_%2A%2A%2A%2AA%2AAAAA.json) |

</details>

<details><summary><code>ex7_8jy_o48</code> 郭洪之（郭祚父）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 郭洪之（郭祚父） | [《魏書・郭祚 張彝》][1177] | [JSON](ex7_8jy_o48.json) |
| `A` | 郭祚（字季祐） | [《魏書・郭祚 張彝》][1177] | [JSON](ex7_8jy_o48_A.json) |

</details>

<details><summary><code>eya_qj3_tev</code> 酈食其（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 酈食其 | [《史記・酈生陸賈列傳》][888] | [JSON](eya_qj3_tev.json) |
| `A` | 疥（酈食其子） | [《史記・酈生陸賈列傳》][888] | [JSON](eya_qj3_tev_A.json) |

</details>

<details><summary><code>f04_rc9_xqn</code> 太史敫（田世家候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 太史敫 | [《史記・田敬仲完世家》][837] | [JSON](f04_rc9_xqn.json) |
| `A` | 君王后 | [《史記・田敬仲完世家》][837] | [JSON](f04_rc9_xqn_A.json) |

</details>

<details><summary><code>f2z_47w_81j</code> 商玄石（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 商玄石 | [《宋書・謝晦》][1023]、[《宋書・謝晦》][1024] | [JSON](f2z_47w_81j.json) |
| `A` | 商懷福 | [《宋書・謝晦》][1023]、[《宋書・謝晦》][1024] | [JSON](f2z_47w_81j_A.json) |

</details>

<details><summary><code>f41_ulg_3u1</code> 衛滿（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 衛滿 | [《史記・朝鮮列傳》][906] | [JSON](f41_ulg_3u1.json) |
| `*A` | 右渠 | [《史記・朝鮮列傳》][906] | [JSON](f41_ulg_3u1_%2AA.json) |
| `*AA` | 長（右渠子） | [《史記・朝鮮列傳》][906] | [JSON](f41_ulg_3u1_%2AAA.json) |

</details>

<details><summary><code>f84_da6_42a</code> 孔愉（5 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 孔愉 | [《晉書・孔愉 丁潭 陶回》][249] | [JSON](f84_da6_42a.json) |
| `A` | 孔誾（孔愉子、孔靖父） | [《南史・孔靖　孔琳之　殷景仁》][686] | [JSON](f84_da6_42a_A.json) |
| `AA` | 孔靖（字季恭，晉書作靜） | [《南史・孔靖　孔琳之　殷景仁》][686] | [JSON](f84_da6_42a_AA.json) |
| `AAA` | 孔靈運（孔琇之父） | [《南齊書・良政》][516] | [JSON](f84_da6_42a_AAA.json) |
| `AAAA` | 孔琇之（會稽山陰人，孔靈運子） | [《南齊書・王奐 從弟繢 張沖》][497]、[《南齊書・良政》][516] | [JSON](f84_da6_42a_AAAA.json) |

</details>

<details><summary><code>f89_ad1_61d</code> 王凌（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 王凌 | [《三國志・王毌丘諸葛鄧鍾傳》][756] | [JSON](f89_ad1_61d.json) |
| `A` | 王廣 | [《三國志・王毌丘諸葛鄧鍾傳》][756] | [JSON](f89_ad1_61d_A.json) |

</details>

<details><summary><code>f8d_j5p_nop</code> 孔防叔（孔子世家候選）（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 孔防叔 | [《史記・孔子世家》][838] | [JSON](f8d_j5p_nop.json) |
| `A` | 伯夏 | [《史記・孔子世家》][838] | [JSON](f8d_j5p_nop_A.json) |
| `AA` | 叔梁紇 | [《史記・孔子世家》][838] | [JSON](f8d_j5p_nop_AA.json) |

</details>

<details><summary><code>f90_933_c35</code> 猗盧（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 猗盧 | [《晉書・王沈 荀顗 荀勖 馮紞》][158]、[《晉書・鄭袤 李胤 盧欽 華表 石鑒 溫羨》][178] | [JSON](f90_933_c35.json) |
| `A` | 日律孫 | [《晉書・王沈 荀顗 荀勖 馮紞》][158] | [JSON](f90_933_c35_A.json) |

</details>

<details><summary><code>faf_5al_ikw</code> 鄭武公（老韓列傳候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 鄭武公 | [《史記・老子韓非列傳》][854] | [JSON](faf_5al_ikw.json) |
| `A` | 鄭武公之子 | [《史記・老子韓非列傳》][854] | [JSON](faf_5al_ikw_A.json) |

</details>

<details><summary><code>fcu_pw8_tkw</code> 蔡興宗（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 蔡興宗 | [《南齊書・王融 謝朓》][493]、[《南史・謝晦　謝裕　謝方明　謝靈運》][590]、[《南史・王曇首》][614]、[《南史・王曇首》][621]、[《南史・王曇首》][620]、[《宋書・徐湛之 江湛 王僧綽》][1081]、[《宋書・徐湛之 江湛 王僧綽》][1079]、[《宋書・徐湛之 江湛 王僧綽》][1080] | [JSON](fcu_pw8_tkw.json) |
| `A` | 蔡約 | [《南史・王曇首》][614] | [JSON](fcu_pw8_tkw_A.json) |

</details>

<details><summary><code>fd3_tly_1lo</code> 沸（魯魏公）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 沸（魯魏公） | [《史記・魯周公世家》][824] | [JSON](fd3_tly_1lo.json) |
| `A` | 擢（魯厲公） | [《史記・魯周公世家》][824]、[《史記・三代世表》][1222] | [JSON](fd3_tly_1lo_A.json) |

</details>

<details><summary><code>fdb_6pb_gux</code> 蒯聵（太史公自序候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 蒯聵 | [《史記・太史公自序》][921] | [JSON](fdb_6pb_gux.json) |
| `***A` | 司馬卬 | [《史記・高祖本紀》][816]、[《史記・太史公自序》][921] | [JSON](fdb_6pb_gux_%2A%2A%2AA.json) |

</details>

<details><summary><code>ffc_ea1_a8f</code> 范寧（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 范寧 | [《晉書・王湛 荀崧 范汪 劉惔 張憑 韓伯》][233] | [JSON](ffc_ea1_a8f.json) |
| `A` | 范泰 | [《宋書・趙倫之 王懿 張邵》][1040]、[《宋書・范泰 王准之 王韶之 荀伯子》][1064] | [JSON](ffc_ea1_a8f_A.json) |

</details>

<details><summary><code>fh0_oxc_05e</code> 韋旭（韋世康祖）（4 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 韋旭（韋世康祖） | [《隋書・列傳第12 韋世康 柳機》][1143] | [JSON](fh0_oxc_05e.json) |
| `A` | 韋夐（韋世康父） | [《隋書・列傳第12 韋世康 柳機》][1143] | [JSON](fh0_oxc_05e_A.json) |
| `AA` | 韋世康（京兆杜陵） | [《隋書・列傳第12 韋世康 柳機》][1143]、[《隋書・列傳第12 韋世康 柳機》][1144] | [JSON](fh0_oxc_05e_AA.json) |
| `AB` | 韋洸（字世穆） | [《隋書・列傳第12 韋世康 柳機》][1143] | [JSON](fh0_oxc_05e_AB.json) |

</details>

<details><summary><code>fjm_eo3_0zz</code> 始興王憺（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 始興王憺 | [《南史・王裕之　王鎮之　王韶之　王悅之　王准之》][677]、[《南史・王裕之　王鎮之　王韶之　王悅之　王准之》][662] | [JSON](fjm_eo3_0zz.json) |
| `A` | 繁昌主 | [《梁書・王瞻 王志 王峻 王暕 子訓 王泰 王份 孫鍚 僉 張充 柳惲 蔡撙 江蒨》][337]、[《南史・王裕之　王鎮之　王韶之　王悅之　王准之》][677]、[《南史・王裕之　王鎮之　王韶之　王悅之　王准之》][662] | [JSON](fjm_eo3_0zz_A.json) |

</details>

<details><summary><code>fmh_dmt_cql</code> 汲黯（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 汲黯 | [《史記・汲鄭列傳》][911] | [JSON](fmh_dmt_cql.json) |
| `A` | 汲偃 | [《漢書・張馮汲鄭傳》][67]、[《史記・汲鄭列傳》][911] | [JSON](fmh_dmt_cql_A.json) |

</details>

<details><summary><code>fo7_f8v_rmf</code> 梁武帝衍（10 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 梁武帝衍 | [《梁書・謝朏 弟子覽》][323] | [JSON](fo7_f8v_rmf.json) |
| `A` | 蕭玉姚 | [《梁書・皇后》][314]、[《梁書・皇后》][315]、[《南史・后妃下》][559] | [JSON](fo7_f8v_rmf_A.json) |
| `B` | 蕭玉婉 | [《梁書・皇后》][314]、[《梁書・皇后》][315]、[《南史・后妃下》][559] | [JSON](fo7_f8v_rmf_B.json) |
| `C` | 蕭績（字世謹） | [《梁書・高祖三王》][357] | [JSON](fo7_f8v_rmf_C.json) |
| `CA` | 蕭會理（字長才，南康王績子） | [《梁書・高祖三王》][355] | [JSON](fo7_f8v_rmf_CA.json) |
| `D` | 蕭紀（武陵王） | [《梁書・豫章王綜 武陵王紀 臨賀王正德 河東王譽》][393] | [JSON](fo7_f8v_rmf_D.json) |
| `E` | 蕭玉志（梁安吉公主，王實妻） | [《南史・王誕　王華　王惠　王彧》][653] | [JSON](fo7_f8v_rmf_E.json) |
| `F` | 梁永嘉公主（王銓妻） | [《南史・王誕　王華　王惠　王彧》][635]、[《文獻通考・卷二百五十八》][1182] | [JSON](fo7_f8v_rmf_F.json) |
| `G` | 蕭續（梁廬陵威王） | [《南史・梁武帝諸子》][717] | [JSON](fo7_f8v_rmf_G.json) |
| `H` | 蕭玉嬛（梁永康公主） | [《梁書・皇后》][315]、[《南史・后妃下》][559] | [JSON](fo7_f8v_rmf_H.json) |

</details>

<details><summary><code>fom_gr9_c8v</code> 孫叔敖（循吏列傳候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 孫叔敖 | [《史記・循吏列傳》][910]、[《史記・滑稽列傳》][917] | [JSON](fom_gr9_c8v.json) |
| `A` | 孫叔敖子（未名） | [《史記・滑稽列傳》][917] | [JSON](fom_gr9_c8v_A.json) |

</details>

<details><summary><code>fp6_ia6_7yw</code> 孔子（11 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 孔子 | [《史記・孔子世家》][838] | [JSON](fp6_ia6_7yw.json) |
| `A` | 鯉 | [《史記・孔子世家》][838] | [JSON](fp6_ia6_7yw_A.json) |
| `AA` | 伋 | [《史記・孔子世家》][838] | [JSON](fp6_ia6_7yw_AA.json) |
| `AAA` | 白 | [《史記・孔子世家》][838] | [JSON](fp6_ia6_7yw_AAA.json) |
| `AAAA` | 求 | [《史記・孔子世家》][838] | [JSON](fp6_ia6_7yw_AAAA.json) |
| `AAAAA` | 箕 | [《史記・孔子世家》][838] | [JSON](fp6_ia6_7yw_AAAAA.json) |
| `AAAAAA` | 穿 | [《史記・孔子世家》][838] | [JSON](fp6_ia6_7yw_AAAAAA.json) |
| `AAAAAAA` | 子慎 | [《史記・孔子世家》][838] | [JSON](fp6_ia6_7yw_AAAAAAA.json) |
| `AAAAAAAA` | 鮒 | [《史記・孔子世家》][838] | [JSON](fp6_ia6_7yw_AAAAAAAA.json) |
| `B` | 孔鯉 | [《史記・仲尼弟子列傳》][858] | [JSON](fp6_ia6_7yw_B.json) |
| `C` | 孔子之女 | [《史記・仲尼弟子列傳》][858] | [JSON](fp6_ia6_7yw_C.json) |

</details>

<details><summary><code>fs1_z3i_d4r</code> 趙遐（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 趙遐 | [《崔混墓誌・節錄》][44] | [JSON](fs1_z3i_d4r.json) |
| `A` | 趙氏（崔混妻） | [《崔混墓誌・節錄》][44] | [JSON](fs1_z3i_d4r_A.json) |

</details>

<details><summary><code>fum_370_iq6</code> 結〔楊播高祖〕（28 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 結〔楊播高祖〕 | [《魏書・楊播》][1171] | [JSON](fum_370_iq6.json) |
| `A` | 珍〔楊播曾祖〕 | [《魏書・楊播》][1171]、[《魏書・楊播》][1172] | [JSON](fum_370_iq6_A.json) |
| `AA` | 真〔楊播祖〕 | [《楊舒墓誌・全文》][55]、[《魏書・楊播》][1171]、[《魏書・楊播》][1172] | [JSON](fum_370_iq6_AA.json) |
| `AAA` | 懿〔楊播父〕 | [《魏書・楊播》][1171] | [JSON](fum_370_iq6_AAA.json) |
| `AAAA` | 楊播 | [《魏書・楊播》][1171] | [JSON](fum_370_iq6_AAAA.json) |
| `AAAAA` | 侃〔楊播子，字士業〕 | [《魏書・楊播》][1171] | [JSON](fum_370_iq6_AAAAA.json) |
| `AAAAAA` | 師沖〔楊侃長子，北史作師仲〕 | [《魏書・楊播》][1171] | [JSON](fum_370_iq6_AAAAAA.json) |
| `AAAAAB` | 純陀〔楊侃嗣子〕 | [《魏書・楊播》][1171] | [JSON](fum_370_iq6_AAAAAB.json) |
| `AAAB` | 楊椿 | [《魏書・楊播》][1172] | [JSON](fum_370_iq6_AAAB.json) |
| `AAABA` | 楊昱 | [《魏書・楊播》][1172] | [JSON](fum_370_iq6_AAABA.json) |
| `AAABAA` | 孝邕〔楊昱子〕 | [《魏書・楊播》][1172] | [JSON](fum_370_iq6_AAABAA.json) |
| `AAAC` | 穎〔楊椿弟，字惠哲〕 | [《魏書・楊播》][1172] | [JSON](fum_370_iq6_AAAC.json) |
| `AAACA` | 叔良〔楊穎子〕 | [《魏書・楊播》][1172] | [JSON](fum_370_iq6_AAACA.json) |
| `AAAD` | 順〔楊穎弟，字延和〕 | [《魏書・楊播》][1172] | [JSON](fum_370_iq6_AAAD.json) |
| `AAADA` | 辯〔楊順子，字僧達〕 | [《魏書・楊播》][1172] | [JSON](fum_370_iq6_AAADA.json) |
| `AAADB` | 仲宣〔楊順子〕 | [《魏書・楊播》][1172] | [JSON](fum_370_iq6_AAADB.json) |
| `AAADBA` | 玄就〔楊仲宣子〕 | [《魏書・楊播》][1172] | [JSON](fum_370_iq6_AAADBA.json) |
| `AAADC` | 測〔楊仲宣弟〕 | [《魏書・楊播》][1172] | [JSON](fum_370_iq6_AAADC.json) |
| `AAADD` | 稚卿〔楊測弟〕 | [《魏書・楊播》][1172] | [JSON](fum_370_iq6_AAADD.json) |
| `AAAE` | 楊津〔字羅漢，本名延祚〕 | [《魏書・楊播》][1173] | [JSON](fum_370_iq6_AAAE.json) |
| `AAAEA` | 楊遁〔字山才，津長子〕 | [《魏書・楊播》][1173] | [JSON](fum_370_iq6_AAAEA.json) |
| `AAAEB` | 楊逸〔字遵道，津第二子〕 | [《魏書・楊播》][1173] | [JSON](fum_370_iq6_AAAEB.json) |
| `AAAEC` | 楊謐〔字遵智，逸弟〕 | [《魏書・楊播》][1173] | [JSON](fum_370_iq6_AAAEC.json) |
| `AAAED` | 楊遵彥〔謐弟〕 | [《南史・王弘》][608]、[《魏書・楊播》][1173] | [JSON](fum_370_iq6_AAAED.json) |
| `AAAF` | 楊暐〔字延季，津弟〕 | [《魏書・楊播》][1173] | [JSON](fum_370_iq6_AAAF.json) |
| `AAAFA` | 楊元讓〔暐子〕 | [《魏書・楊播》][1173] | [JSON](fum_370_iq6_AAAFA.json) |
| `AAB` | 洛州恒農簡公〔楊舒墓誌父〕 | [《楊舒墓誌・全文》][55] | [JSON](fum_370_iq6_AAB.json) |
| `AABA` | 舒〔楊昱第六叔〕 | [《楊舒墓誌・全文》][55] | [JSON](fum_370_iq6_AABA.json) |

</details>

<details><summary><code>fv1_k6x_jeu</code> 虛閭權渠單于（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 虛閭權渠單于 | [《漢書・匈奴傳》][72] | [JSON](fv1_k6x_jeu.json) |
| `A` | 呼韓邪單于（稽侯狦） | [《漢書・匈奴傳》][72] | [JSON](fv1_k6x_jeu_A.json) |

</details>

<details><summary><code>fvm_66f_0k3</code> 周緤（4 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 周緤 | [《史記・傅靳蒯成列傳》][889] | [JSON](fvm_66f_0k3.json) |
| `A` | 周昌（蒯成侯之子） | [《漢書・樊酈滕灌傅靳周傳》][66]、[《史記・傅靳蒯成列傳》][889]、[《史記・高祖功臣侯者年表》][1227] | [JSON](fvm_66f_0k3_A.json) |
| `C` | 周應 | [《漢書・樊酈滕灌傅靳周傳》][66] | [JSON](fvm_66f_0k3_C.json) |
| `CA` | 周仲居 | [《史記・高祖功臣侯者年表》][1227] | [JSON](fvm_66f_0k3_CA.json) |

</details>

<details><summary><code>g7w_9tv_iqb</code> 王僧辯（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 王僧辯 | [《南史・王誕　王華　王惠　王彧》][641]、[《南史・王裕之　王鎮之　王韶之　王悅之　王准之》][664]、[《南史・江子一　胡僧祐　徐文盛　陰子春　杜崱　王琳　張彪》][724] | [JSON](g7w_9tv_iqb.json) |
| `A` | 王僧辯女（杜龕妻） | [《南史・江子一　胡僧祐　徐文盛　陰子春　杜崱　王琳　張彪》][724] | [JSON](g7w_9tv_iqb_A.json) |

</details>

<details><summary><code>g83_41s_o52</code> 焦文珪（南安氐人，焦度祖）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 焦文珪（南安氐人，焦度祖） | [《南齊書・薛淵 戴僧靜 桓康 焦度 曹虎》][436] | [JSON](g83_41s_o52.json) |
| `*A` | 焦度（字文續） | [《南齊書・薛淵 戴僧靜 桓康 焦度 曹虎》][436] | [JSON](g83_41s_o52_%2AA.json) |

</details>

<details><summary><code>g9h_5ih_ug1</code> 伍奢（伍胥列傳候選）（4 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 伍奢 | [《史記・伍子胥列傳》][857] | [JSON](g9h_5ih_ug1.json) |
| `A` | 伍子胥 | [《史記・伍子胥列傳》][857] | [JSON](g9h_5ih_ug1_A.json) |
| `AA` | 伍子胥之子 | [《史記・伍子胥列傳》][857] | [JSON](g9h_5ih_ug1_AA.json) |
| `B` | 伍尚 | [《史記・伍子胥列傳》][857] | [JSON](g9h_5ih_ug1_B.json) |

</details>

<details><summary><code>ga6_jt5_6g1</code> 圉（衛孔文子）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 圉（衛孔文子） | [《史記・衛康叔世家》][828] | [JSON](ga6_jt5_6g1.json) |
| `A` | 悝（衛孔氏） | [《史記・衛康叔世家》][828] | [JSON](ga6_jt5_6g1_A.json) |

</details>

<details><summary><code>gcb_rf3_coi</code> 費王（晉穆侯）（4 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 費王（晉穆侯） | [《史記・晉世家》][830] | [JSON](gcb_rf3_coi.json) |
| `A` | 仇（晉文侯） | [《史記・晉世家》][830] | [JSON](gcb_rf3_coi_A.json) |
| `AA` | 伯（晉昭侯） | [《史記・晉世家》][830] | [JSON](gcb_rf3_coi_AA.json) |
| `B` | 成師（曲沃桓叔） | [《史記・晉世家》][830] | [JSON](gcb_rf3_coi_B.json) |

</details>

<details><summary><code>gcu_93j_y97</code> 鄭遵（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 鄭遵 | [《南史・范泰　荀伯子　徐廣　鄭鮮之　裴松之　何承天》][697] | [JSON](gcu_93j_y97.json) |
| `A` | 鄭鮮之 | [《南史・范泰　荀伯子　徐廣　鄭鮮之　裴松之　何承天》][697] | [JSON](gcu_93j_y97_A.json) |

</details>

<details><summary><code>gdj_k53_v1x</code> 王翦（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 王翦 | [《史記・白起王翦列傳》][864] | [JSON](gdj_k53_v1x.json) |
| `*A` | 王離 | [《史記・白起王翦列傳》][864] | [JSON](gdj_k53_v1x_%2AA.json) |
| `A` | 王賁 | [《史記・白起王翦列傳》][864] | [JSON](gdj_k53_v1x_A.json) |

</details>

<details><summary><code>ghg_5p7_q21</code> 遂（杞釐公）（4 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 遂（杞釐公） | [《史記・陳杞世家》][827] | [JSON](ghg_5p7_q21.json) |
| `A` | 維（杞湣公） | [《史記・陳杞世家》][827] | [JSON](ghg_5p7_q21_A.json) |
| `AA` | 敕（杞出公） | [《史記・陳杞世家》][827] | [JSON](ghg_5p7_q21_AA.json) |
| `AAA` | 春（杞簡公） | [《史記・陳杞世家》][827] | [JSON](ghg_5p7_q21_AAA.json) |

</details>

<details><summary><code>gjl_f5h_2a6</code> 劉景猷（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 劉景猷 | [《南齊書・皇后》][420]、[《南齊書・皇后》][421]、[《南史・后妃上》][530]、[《南史・后妃上》][531] | [JSON](gjl_f5h_2a6.json) |
| `A` | 劉惠端 | [《南齊書・皇后》][420]、[《南齊書・皇后》][421]、[《南史・后妃上》][530]、[《南史・后妃上》][531]、[《昭明文選・卷五十八》][1185]、[《昭明文選・卷五十八》][1186]、[《昭明文選・卷五十八》][1187] | [JSON](gjl_f5h_2a6_A.json) |
| `B` | 劉暄 | [《南史・謝晦　謝裕　謝方明　謝靈運》][590] | [JSON](gjl_f5h_2a6_B.json) |

</details>

<details><summary><code>gke_14h_1xk</code> 宇（燕王）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 宇（燕王） | [《三國志・三少帝紀》][732]、[《三國志・諸夏侯曹傳》][733] | [JSON](gke_14h_1xk.json) |
| `A` | 曹奐〔字景明〕 | [《三國志・三少帝紀》][732] | [JSON](gke_14h_1xk_A.json) |

</details>

<details><summary><code>gm4_alk_hn7</code> 劉玄之（7 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 劉玄之 | [《南齊書・皇后》][412]、[《南齊書・皇后》][411]、[《南史・后妃上》][532]、[《南史・后妃上》][533] | [JSON](gm4_alk_hn7.json) |
| `A` | 劉壽之 | [《南齊書・皇后》][412]、[《南齊書・皇后》][411]、[《南史・后妃上》][532]、[《南史・后妃上》][533] | [JSON](gm4_alk_hn7_A.json) |
| `AA` | 劉智容 | [《南史・后妃上》][532]、[《南史・后妃上》][533] | [JSON](gm4_alk_hn7_AA.json) |
| `AB` | 劉興道 | [《南齊書・皇后》][412]、[《南齊書・皇后》][411] | [JSON](gm4_alk_hn7_AB.json) |
| `AC` | 劉文蔚 | [《南齊書・皇后》][412]、[《南齊書・皇后》][411] | [JSON](gm4_alk_hn7_AC.json) |
| `AD` | 劉義徽 | [《南齊書・皇后》][412]、[《南齊書・皇后》][411] | [JSON](gm4_alk_hn7_AD.json) |
| `AE` | 劉義倫 | [《南齊書・皇后》][412]、[《南齊書・皇后》][411] | [JSON](gm4_alk_hn7_AE.json) |

</details>

<details><summary><code>gn7_br7_32m</code> 伯州犁（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 伯州犁 | [《史記・吳太伯世家》][822] | [JSON](gn7_br7_32m.json) |
| `*A` | 伯嚭 | [《史記・吳太伯世家》][822] | [JSON](gn7_br7_32m_%2AA.json) |

</details>

<details><summary><code>gqj_xdu_8rf</code> 張騫（李將軍列傳候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 張騫 | [《史記・大宛列傳》][914] | [JSON](gqj_xdu_8rf.json) |
| `A` | 張騫子（未名） | [《史記・大宛列傳》][914] | [JSON](gqj_xdu_8rf_A.json) |

</details>

<details><summary><code>gtj_19g_u2l</code> 殷道矜（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 殷道矜 | [《南齊書・王奐 從弟繢 張沖》][504] | [JSON](gtj_19g_u2l.json) |
| `A` | 殷恒（字昭度，殷道矜子） | [《南齊書・王奐 從弟繢 張沖》][504] | [JSON](gtj_19g_u2l_A.json) |

</details>

<details><summary><code>gts_42q_flu</code> 睔（鄭世家成公候選）（7 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 睔 | [《史記・鄭世家》][833] | [JSON](gts_42q_flu.json) |
| `A` | 惲 | [《史記・鄭世家》][833] | [JSON](gts_42q_flu_A.json) |
| `AA` | 嘉 | [《史記・鄭世家》][833] | [JSON](gts_42q_flu_AA.json) |
| `AAA` | 寧 | [《史記・鄭世家》][833] | [JSON](gts_42q_flu_AAA.json) |
| `AAAA` | 蠆 | [《史記・鄭世家》][833] | [JSON](gts_42q_flu_AAAA.json) |
| `AAAAA` | 勝 | [《史記・鄭世家》][833] | [JSON](gts_42q_flu_AAAAA.json) |
| `AAAAAA` | 易 | [《史記・鄭世家》][833] | [JSON](gts_42q_flu_AAAAAA.json) |

</details>

<details><summary><code>gyg_hql_qdj</code> 慕容永（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 慕容永 | [《晉書・溫嶠 郗鑒》][219] | [JSON](gyg_hql_qdj.json) |
| `A` | 慕容弘〔常山公、慕容永子〕 | [《晉書・溫嶠 郗鑒》][219]、[《資治通鑑・晉紀三十》][1209] | [JSON](gyg_hql_qdj_A.json) |

</details>

<details><summary><code>gzc_9vs_o43</code> 孟嘉〔字萬年〕（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 孟嘉〔字萬年〕 | [《晉書・叛臣一》][283] | [JSON](gzc_9vs_o43.json) |
| `A` | 孟氏〔孟嘉第四女、陶淵明母〕 | — | [JSON](gzc_9vs_o43_A.json) |

</details>

<details><summary><code>h15_bxq_n5u</code> 周優〔周翼父〕（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 周優〔周翼父〕 | [《世說新語・德行》][926] | [JSON](h15_bxq_n5u.json) |
| `A` | 周翼〔字子卿，郗鑒外甥〕 | [《世說新語・德行》][926] | [JSON](h15_bxq_n5u_A.json) |

</details>

<details><summary><code>h1w_44g_vef</code> 張孟（魏其武安侯列傳候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 張孟 | [《史記・魏其武安列傳》][898] | [JSON](h1w_44g_vef.json) |
| `A` | 灌夫 | [《史記・魏其武安列傳》][898] | [JSON](h1w_44g_vef_A.json) |

</details>

<details><summary><code>h4f_d5f_vdl</code> 蟬封（大宛列傳候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 蟬封 | [《史記・大宛列傳》][914] | [JSON](h4f_d5f_vdl.json) |
| `A` | 蟬封子（入質，未名） | [《史記・大宛列傳》][914] | [JSON](h4f_d5f_vdl_A.json) |

</details>

<details><summary><code>h6m_t08_wbd</code> 顧向（5 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 顧向 | [《三國志・張顧諸葛步傳》][777] | [JSON](h6m_t08_wbd.json) |
| `A` | 顧悌 | [《三國志・張顧諸葛步傳》][777] | [JSON](h6m_t08_wbd_A.json) |
| `AA` | 顧彥〔顧悌子〕 | [《三國志・張顧諸葛步傳》][777] | [JSON](h6m_t08_wbd_AA.json) |
| `AB` | 顧禮 | [《三國志・張顧諸葛步傳》][777] | [JSON](h6m_t08_wbd_AB.json) |
| `AC` | 顧謙 | [《三國志・張顧諸葛步傳》][777] | [JSON](h6m_t08_wbd_AC.json) |

</details>

<details><summary><code>h7n_w5t_i1c</code> 曹休未名祖父（7 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 曹休未名祖父 | [《三國志・諸夏侯曹傳》][733] | [JSON](h7n_w5t_i1c.json) |
| `A` | 曹休未名父 | [《三國志・諸夏侯曹傳》][733] | [JSON](h7n_w5t_i1c_A.json) |
| `AA` | 曹休 | [《三國志・諸夏侯曹傳》][733] | [JSON](h7n_w5t_i1c_AA.json) |
| `AAA` | 肇（曹攄祖、曹休子） | [《三國志・諸夏侯曹傳》][733] | [JSON](h7n_w5t_i1c_AAA.json) |
| `AAA*A` | 曹顏遠 | [《晉書・良吏》][258] | [JSON](h7n_w5t_i1c_AAA%2AA.json) |
| `AAAA` | 興（肇子） | [《三國志・諸夏侯曹傳》][733] | [JSON](h7n_w5t_i1c_AAAA.json) |
| `AAB` | 纂（肇弟） | [《三國志・諸夏侯曹傳》][733] | [JSON](h7n_w5t_i1c_AAB.json) |

</details>

<details><summary><code>h9n_acw_xpo</code> 戴碩子（法興父）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 戴碩子（法興父） | [《宋書・恩倖》][1139] | [JSON](h9n_acw_xpo.json) |
| `A` | 戴法興（會稽山陰人） | [《宋書・恩倖》][1139] | [JSON](h9n_acw_xpo_A.json) |

</details>

<details><summary><code>hb9_2gq_205</code> 袁昂〔吳郡不降梁〕（5 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 袁昂〔吳郡不降梁〕 | [《南史・王曇首》][626] | [JSON](hb9_2gq_205.json) |
| `A` | 袁君正（梁吳郡太守，字世忠） | [《南史・袁湛》][684] | [JSON](hb9_2gq_205_A.json) |
| `AA` | 袁樞（陳尚書左僕射，字踐言） | [《陳書・列傳第十一: 王沖 王通 袁敬》][34] | [JSON](hb9_2gq_205_AA.json) |
| `B` | 袁敬（陳左光祿大夫，字子恭） | [《陳書・列傳第十一: 王沖 王通 袁敬》][33] | [JSON](hb9_2gq_205_B.json) |
| `BA` | 袁元友（袁敬子） | [《陳書・列傳第十一: 王沖 王通 袁敬》][33] | [JSON](hb9_2gq_205_BA.json) |

</details>

<details><summary><code>hgm_jvn_hle</code> 晉武帝（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 晉武帝 | [《晉書・王沈 荀顗 荀勖 馮紞》][158] | [JSON](hgm_jvn_hle.json) |
| `A` | 襄城公主〔晉武帝女、王敦妻〕 | [《晉書・叛臣一》][282] | [JSON](hgm_jvn_hle_A.json) |
| `B` | 滎陽公主〔晉武帝女〕 | [《晉書・鄭袤 李胤 盧欽 華表 石鑒 溫羨》][178] | [JSON](hgm_jvn_hle_B.json) |

</details>

<details><summary><code>hx8_st4_jdd</code> 宋孝武帝駿（15 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 宋孝武帝駿 | [《宋書・殷淳 張暢 何偃 江智淵》][1063] | [JSON](hx8_st4_jdd.json) |
| `A` | 安固公主（宋孝武女） | [《梁書・王瞻 王志 王峻 王暕 子訓 王泰 王份 孫鍚 僉 張充 柳惲 蔡撙 江蒨》][343]、[《梁書・王瞻 王志 王峻 王暕 子訓 王泰 王份 孫鍚 僉 張充 柳惲 蔡撙 江蒨》][342]、[《南史・王曇首》][631]、[《南史・王曇首》][630] | [JSON](hx8_st4_jdd_A.json) |
| `B` | 永嘉王子仁 | [《宋書・孝武十四王》][1098] | [JSON](hx8_st4_jdd_B.json) |
| `C` | 劉楚玉（山陰公主） | [《南齊書・王琨 張岱 褚炫 何戢 王延之 阮韜》][441]、[《南史・后妃上》][545]、[《南史・后妃上》][546]、[《宋書・后妃》][1017] | [JSON](hx8_st4_jdd_C.json) |
| `D` | 劉楚佩（臨淮康哀公主） | [《南史・后妃上》][545]、[《南史・后妃上》][546]、[《宋書・后妃》][1017] | [JSON](hx8_st4_jdd_D.json) |
| `E` | 劉楚琇（宋孝武皇女） | [《南史・后妃上》][545]、[《南史・后妃上》][546]、[《宋書・后妃》][1017] | [JSON](hx8_st4_jdd_E.json) |
| `F` | 劉脩明（康樂公主） | [《南史・后妃上》][545]、[《南史・后妃上》][546]、[《宋書・后妃》][1017] | [JSON](hx8_st4_jdd_F.json) |
| `G` | 臨汝公主（宋孝武帝女，江斆妻） | [《南齊書・江斆 何昌㝢 謝𤅢 王思遠》][480]、[《南史・王誕　王華　王惠　王彧》][656] | [JSON](hx8_st4_jdd_G.json) |
| `H` | 劉子真（始安王，字孝貞） | [《宋書・孝武十四王》][1093] | [JSON](hx8_st4_jdd_H.json) |
| `I` | 劉子產（宋臨賀王，字孝仁） | [《宋書・文九王》][1083] | [JSON](hx8_st4_jdd_I.json) |
| `J` | 劉子羽（齊敬王，字孝英） | [《宋書・孝武十四王》][1096] | [JSON](hx8_st4_jdd_J.json) |
| `K` | 劉子雲（晉陵孝王，字孝舉） | [《宋書・孝武十四王》][1096] | [JSON](hx8_st4_jdd_K.json) |
| `L` | 劉子文（宋孝武皇子） | [《宋書・孝武十四王》][1094] | [JSON](hx8_st4_jdd_L.json) |
| `M` | 劉子師（南海哀王，字孝友） | [《宋書・孝武十四王》][1095] | [JSON](hx8_st4_jdd_M.json) |
| `N` | 宋孝武帝第十二皇女（子鸞同生妹） | — | [JSON](hx8_st4_jdd_N.json) |

</details>

<details><summary><code>hxn_tox_kna</code> 宗叔獻（宗靈秀父）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 宗叔獻（宗靈秀父） | [《宋書・朱脩之 宗愨 王玄謨》][1089] | [JSON](hxn_tox_kna.json) |
| `A` | 宗靈秀（宋黃門侍郎） | [《宋書・朱脩之 宗愨 王玄謨》][1089] | [JSON](hxn_tox_kna_A.json) |

</details>

<details><summary><code>i08_s4b_5bb</code> 王晏〔齊尚書令〕（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 王晏〔齊尚書令〕 | [《南史・王裕之　王鎮之　王韶之　王悅之　王准之》][673] | [JSON](i08_s4b_5bb.json) |
| `A` | 王德元（王晏子，初名湛） | [《南齊書・王晏 蕭諶 蕭坦之 江祏》][473]、[《南史・王裕之　王鎮之　王韶之　王悅之　王准之》][660] | [JSON](i08_s4b_5bb_A.json) |
| `B` | 王德和（王德元弟） | [《南齊書・王晏 蕭諶 蕭坦之 江祏》][473] | [JSON](i08_s4b_5bb_B.json) |

</details>

<details><summary><code>i30_mjq_6q8</code> 呂公（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 呂公 | [《史記・高祖本紀》][816] | [JSON](i30_mjq_6q8.json) |
| `A` | 呂后 | [《史記・呂后本紀》][817] | [JSON](i30_mjq_6q8_A.json) |

</details>

<details><summary><code>i3f_9l9_g53</code> 陳平（5 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 陳平 | [《史記・陳丞相世家》][847] | [JSON](i3f_9l9_g53.json) |
| `**A` | 陳掌 | [《史記・陳丞相世家》][847] | [JSON](i3f_9l9_g53_%2A%2AA.json) |
| `A` | 買 | [《史記・陳丞相世家》][847] | [JSON](i3f_9l9_g53_A.json) |
| `AA` | 恢 | [《史記・陳丞相世家》][847] | [JSON](i3f_9l9_g53_AA.json) |
| `AAA` | 何 | [《史記・陳丞相世家》][847] | [JSON](i3f_9l9_g53_AAA.json) |

</details>

<details><summary><code>i5r_vby_q00</code> 殷禮（4 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 殷禮 | [《三國志・張顧諸葛步傳》][775] | [JSON](i5r_vby_q00.json) |
| `A` | 殷基 | [《三國志・張顧諸葛步傳》][775] | [JSON](i5r_vby_q00_A.json) |
| `AA` | 殷巨 | [《三國志・張顧諸葛步傳》][775] | [JSON](i5r_vby_q00_AA.json) |
| `AB` | 殷祐 | [《三國志・張顧諸葛步傳》][775] | [JSON](i5r_vby_q00_AB.json) |

</details>

<details><summary><code>i7a_22p_qda</code> 句踐（7 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 句踐 | [《史記・越王勾踐世家》][832] | [JSON](i7a_22p_qda.json) |
| `A` | 鼫與 | [《史記・越王勾踐世家》][832] | [JSON](i7a_22p_qda_A.json) |
| `AA` | 不壽 | [《史記・越王勾踐世家》][832] | [JSON](i7a_22p_qda_AA.json) |
| `AAA` | 翁 | [《史記・越王勾踐世家》][832] | [JSON](i7a_22p_qda_AAA.json) |
| `AAAA` | 翳 | [《史記・越王勾踐世家》][832] | [JSON](i7a_22p_qda_AAAA.json) |
| `AAAAA` | 之侯 | [《史記・越王勾踐世家》][832] | [JSON](i7a_22p_qda_AAAAA.json) |
| `AAAAAA` | 無彊 | [《史記・越王勾踐世家》][832] | [JSON](i7a_22p_qda_AAAAAA.json) |

</details>

<details><summary><code>i8i_rvh_4lp</code> 燬（衛文公）（8 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 燬（衛文公） | [《史記・衛康叔世家》][828] | [JSON](i8i_rvh_4lp.json) |
| `A` | 鄭（衛成公） | [《史記・衛康叔世家》][828] | [JSON](i8i_rvh_4lp_A.json) |
| `AA` | 遫（衛穆公） | [《史記・衛康叔世家》][828] | [JSON](i8i_rvh_4lp_AA.json) |
| `AAA` | 臧（衛定公） | [《史記・衛康叔世家》][828] | [JSON](i8i_rvh_4lp_AAA.json) |
| `AAAA` | 衎（衛獻公） | [《史記・衛康叔世家》][828] | [JSON](i8i_rvh_4lp_AAAA.json) |
| `AAAAA` | 惡（衛襄公） | [《史記・衛康叔世家》][828] | [JSON](i8i_rvh_4lp_AAAAA.json) |
| `AAAAAA` | 元（衛靈公） | [《史記・衛康叔世家》][828] | [JSON](i8i_rvh_4lp_AAAAAA.json) |
| `AAAAAAA` | 郢（衛子南） | [《史記・衛康叔世家》][828] | [JSON](i8i_rvh_4lp_AAAAAAA.json) |

</details>

<details><summary><code>i9w_mm6_m7t</code> 顧謙（字公讓，顧覬之高祖）（4 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 顧謙（字公讓，顧覬之高祖） | [《宋書・劉秀之 顧琛 顧覬之》][1100] | [JSON](i9w_mm6_m7t.json) |
| `*A` | 顧崇（大司農，顧覬之祖） | [《宋書・劉秀之 顧琛 顧覬之》][1100] | [JSON](i9w_mm6_m7t_%2AA.json) |
| `*AA` | 顧黃老（司徒左西掾） | [《宋書・劉秀之 顧琛 顧覬之》][1100] | [JSON](i9w_mm6_m7t_%2AAA.json) |
| `*AAA` | 顧覬之（字偉仁，山陰令） | [《宋書・劉秀之 顧琛 顧覬之》][1100] | [JSON](i9w_mm6_m7t_%2AAAA.json) |

</details>

<details><summary><code>icd_mkz_d9n</code> 陳宣帝頊（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 陳宣帝頊 | [《陳書・列傳第十一: 王沖 王通 袁敬》][33] | [JSON](icd_mkz_d9n.json) |
| `A` | 陳叔寶（陳後主） | [《陳書・本紀第六: 後主》][15] | [JSON](icd_mkz_d9n_A.json) |

</details>

<details><summary><code>ier_lqj_x4q</code> 郗愔（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 郗愔 | [《晉書・溫嶠 郗鑒》][215] | [JSON](ier_lqj_x4q.json) |
| `A` | 郗融 | [《晉書・溫嶠 郗鑒》][221]、[《晉書・溫嶠 郗鑒》][220] | [JSON](ier_lqj_x4q_A.json) |
| `B` | 郗沖 | [《晉書・溫嶠 郗鑒》][221]、[《晉書・溫嶠 郗鑒》][220] | [JSON](ier_lqj_x4q_B.json) |

</details>

<details><summary><code>iij_zqi_k5l</code> 齊平公（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 齊平公 | [《史記・齊太公世家》][823] | [JSON](iij_zqi_k5l.json) |
| `A` | 積（齊宣公） | [《史記・齊太公世家》][823] | [JSON](iij_zqi_k5l_A.json) |
| `AA` | 貸（齊康公） | [《史記・齊太公世家》][823] | [JSON](iij_zqi_k5l_AA.json) |

</details>

[1]: https://zh.wikisource.org/w/index.php?title=北史/卷016&oldid=1518816
[6]: https://zh.wikisource.org/w/index.php?title=北史/卷044&oldid=2183262
[7]: https://zh.wikisource.org/w/index.php?title=冊府元龜_(四庫全書本)/全覽10&oldid=650326
[12]: https://zh.wikisource.org/w/index.php?oldid=8231316
[15]: https://zh.wikisource.org/w/index.php?oldid=2312453
[17]: https://zh.wikisource.org/w/index.php?oldid=2015446
[19]: https://zh.wikisource.org/w/index.php?oldid=1488469
[21]: https://zh.wikisource.org/w/index.php?oldid=1488469
[23]: https://zh.wikisource.org/w/index.php?oldid=2262003
[24]: https://zh.wikisource.org/w/index.php?oldid=2262003
[25]: https://zh.wikisource.org/w/index.php?oldid=2262003
[27]: https://zh.wikisource.org/w/index.php?oldid=1544244
[30]: https://zh.wikisource.org/w/index.php?oldid=1544244
[33]: https://zh.wikisource.org/w/index.php?oldid=1544244
[34]: https://zh.wikisource.org/w/index.php?oldid=1544244
[37]: https://zh.wikisource.org/w/index.php?oldid=1514499
[41]: https://zh.wikisource.org/w/index.php?oldid=1463644
[42]: https://zh.wikisource.org/w/index.php?oldid=2581394
[43]: https://www.sohu.com/a/259439652_258370
[44]: https://guji.10huan.com/Article/7147_7165.html
[45]: https://imgsoflfg-1302780771.cos.ap-shanghai.myqcloud.com/lfgimgs/94b58f207eda4759b6d188b00fc826c6p5.jpg
[46]: https://lfglib.cn/wp-content/uploads/lfgimgs/gujicover/94b58f207eda4759b6d188b00fc826c6p1.jpg
[47]: https://www.dpm.org.cn/collection/impres/230177.html
[48]: https://www.dpm.org.cn/collection/impres/230096.html
[49]: https://img0-cdn.51sdj.cn/data/attachment/uploads/20200615/1592186750291282.jpg
[51]: https://homepage.ntu.edu.tw/~history/public_html/newsletter/public_html/09newsletter/03/newsletter3_09.pdf#page=3
[53]: https://homepage.ntu.edu.tw/~history/public_html/newsletter/public_html/09newsletter/04/newsletter4_23.pdf
[55]: http://csid.zju.edu.cn/tomb/stone/detail?id=40288b955bd07752015bfb74a80002de
[56]: https://www.i-repository.net/il/cont/01/G0000721f/000/756/000756311.jpg
[61]: https://zh.wikisource.org/w/index.php?oldid=636080
[64]: https://github.com/kanripo/KR2a0007/blob/683113d4baf6febecaf2ccb7913df87c4d68d454/KR2a0007_007.txt
[66]: https://zh.wikisource.org/w/index.php?title=漢書/卷041&oldid=2342290
[67]: https://github.com/kanripo/KR2a0007/blob/683113d4baf6febecaf2ccb7913df87c4d68d454/KR2a0007_050.txt
[68]: https://github.com/kanripo/KR2a0007/blob/683113d4baf6febecaf2ccb7913df87c4d68d454/KR2a0007_059.txt
[72]: https://zh.wikisource.org/w/index.php?oldid=2605445
[73]: https://github.com/kanripo/KR2a0007/blob/683113d4baf6febecaf2ccb7913df87c4d68d454/KR2a0007_098.txt
[74]: https://github.com/kanripo/KR2a0009/blob/6db36b6dcbe843b825354c22e9be9193d0137c04/KR2a0009_009.txt
[76]: https://github.com/kanripo/KR2a0009/blob/6db36b6dcbe843b825354c22e9be9193d0137c04/KR2a0009_092.txt
[81]: https://zh.wikisource.org/w/index.php?oldid=1458097
[85]: https://zh.wikisource.org/w/index.php?oldid=2603565
[96]: https://zh.wikisource.org/w/index.php?oldid=7904721
[142]: https://zh.wikisource.org/w/index.php?oldid=2479706
[146]: https://zh.wikisource.org/w/index.php?title=%E6%99%89%E6%9B%B8%2F%E5%8D%B7032&oldid=1543614
[150]: https://zh.wikisource.org/w/index.php?title=%E6%99%89%E6%9B%B8%2F%E5%8D%B7032&oldid=1543614
[151]: https://zh.wikisource.org/w/index.php?title=%E6%99%89%E6%9B%B8%2F%E5%8D%B7033&oldid=2650519
[153]: https://zh.wikisource.org/w/index.php?oldid=2108231
[155]: https://zh.wikisource.org/w/index.php?oldid=2108231
[156]: https://zh.wikisource.org/w/index.php?title=%E6%99%89%E6%9B%B8%2F%E5%8D%B7037&oldid=2630018
[157]: https://zh.wikisource.org/w/index.php?oldid=2444513
[158]: https://zh.wikisource.org/w/index.php?title=晉書/卷039&oldid=2108782
[160]: https://zh.wikisource.org/w/index.php?title=晉書/卷042&oldid=2180524
[162]: https://zh.wikisource.org/w/index.php?oldid=2618531
[163]: https://zh.wikisource.org/w/index.php?oldid=2618531
[164]: https://zh.wikisource.org/w/index.php?oldid=2618531
[165]: https://zh.wikisource.org/w/index.php?oldid=2618531
[166]: https://zh.wikisource.org/w/index.php?oldid=2618531
[169]: https://zh.wikisource.org/w/index.php?title=晉書/卷043&oldid=2618531
[171]: https://zh.wikisource.org/w/index.php?oldid=1775345
[172]: https://zh.wikisource.org/w/index.php?oldid=1775345
[173]: https://zh.wikisource.org/w/index.php?oldid=1775345
[174]: https://zh.wikisource.org/w/index.php?oldid=1775345
[175]: https://zh.wikisource.org/w/index.php?oldid=1775345
[176]: https://zh.wikisource.org/w/index.php?oldid=1775345
[177]: https://zh.wikisource.org/w/index.php?oldid=1775345
[178]: https://zh.wikisource.org/w/index.php?oldid=1775345
[183]: https://zh.wikisource.org/w/index.php?oldid=1775345
[185]: https://zh.wikisource.org/w/index.php?oldid=1775345
[186]: https://zh.wikisource.org/w/index.php?oldid=1775345
[190]: https://zh.wikisource.org/w/index.php?oldid=2199702
[200]: https://zh.wikisource.org/w/index.php?title=晉書/卷059&oldid=2650517
[201]: https://zh.wikisource.org/w/index.php?title=晉書/卷059&oldid=2650517
[202]: https://zh.wikisource.org/w/index.php?title=晉書/卷059&oldid=2650517
[203]: https://zh.wikisource.org/w/index.php?oldid=7903772
[204]: https://zh.wikisource.org/w/index.php?title=%E6%99%89%E6%9B%B8%2F%E5%8D%B7061&oldid=7903772
[205]: https://zh.wikisource.org/w/index.php?oldid=2629226
[209]: https://zh.wikisource.org/w/index.php?title=%E6%99%89%E6%9B%B8%2F%E5%8D%B7064&oldid=2622004
[212]: https://zh.wikisource.org/w/index.php?title=%E6%99%89%E6%9B%B8%2F%E5%8D%B7065&oldid=1756144
[213]: https://zh.wikisource.org/w/index.php?oldid=1527632
[214]: https://zh.wikisource.org/w/index.php?oldid=2592755
[215]: https://zh.wikisource.org/w/index.php?oldid=2592755
[216]: https://zh.wikisource.org/w/index.php?oldid=2592755
[218]: https://commons.wikimedia.org/w/index.php?oldid=1047611719
[219]: https://zh.wikisource.org/w/index.php?oldid=2592755
[220]: https://commons.wikimedia.org/w/index.php?oldid=1047611719
[221]: https://zh.wikisource.org/w/index.php?oldid=2592755
[224]: https://zh.wikisource.org/w/index.php?title=%E6%99%89%E6%9B%B8%2F%E5%8D%B7069&oldid=2012453
[229]: https://zh.wikisource.org/w/index.php?oldid=2296501
[230]: https://zh.wikisource.org/w/index.php?oldid=2296501
[231]: https://zh.wikisource.org/w/index.php?title=晉書/卷074&oldid=1536331
[233]: https://zh.wikisource.org/w/index.php?title=晉書/卷075&oldid=2645530
[235]: https://zh.wikisource.org/w/index.php?title=晉書/卷075&oldid=2645530
[239]: https://zh.wikisource.org/w/index.php?title=%E6%99%89%E6%9B%B8%2F%E5%8D%B7076&oldid=2180533
[240]: https://zh.wikisource.org/w/index.php?title=%E6%99%89%E6%9B%B8%2F%E5%8D%B7076&oldid=2180533
[241]: https://zh.wikisource.org/w/index.php?title=%E6%99%89%E6%9B%B8%2F%E5%8D%B7076&oldid=2180533
[242]: https://zh.wikisource.org/w/index.php?oldid=2180533
[244]: https://zh.wikisource.org/w/index.php?oldid=2180533
[246]: https://zh.wikisource.org/w/index.php?oldid=2180533
[247]: https://zh.wikisource.org/w/index.php?title=%E6%99%89%E6%9B%B8%2F%E5%8D%B7076&oldid=2180533
[248]: https://zh.wikisource.org/w/index.php?title=%E6%99%89%E6%9B%B8%2F%E5%8D%B7077&oldid=8750392
[249]: https://zh.wikisource.org/w/index.php?oldid=1506266
[250]: https://zh.wikisource.org/w/index.php?title=%E6%99%89%E6%9B%B8%2F%E5%8D%B7079&oldid=2645985
[251]: https://zh.wikisource.org/w/index.php?oldid=2603570
[252]: https://upload.wikimedia.org/wikipedia/commons/3/30/NLC016-HWRB201817005-3307_%E6%99%89%E6%9B%B8_%E4%B8%80%E7%99%BE%E4%B8%89%E5%8D%81%E5%8D%B7_%E9%9F%B3%E7%BE%A9%E4%B8%89%E5%8D%B7_%E7%AC%AC20%E5%86%8A.pdf#page=27
[256]: https://zh.wikisource.org/w/index.php?oldid=2835777
[257]: https://zh.wikisource.org/w/index.php?title=%E6%99%89%E6%9B%B8%2F%E5%8D%B7089&oldid=2835777
[258]: https://zh.wikisource.org/w/index.php?title=晉書/卷090&oldid=2835599
[264]: https://zh.wikisource.org/w/index.php?oldid=1548000
[265]: https://zh.wikisource.org/w/index.php?oldid=1548000
[268]: https://zh.wikisource.org/w/index.php?oldid=2625341
[270]: https://commons.wikimedia.org/w/index.php?oldid=979438884
[271]: https://zh.wikisource.org/w/index.php?oldid=2625341
[274]: https://commons.wikimedia.org/w/index.php?oldid=979438884
[275]: https://zh.wikisource.org/w/index.php?oldid=2625341
[281]: https://zh.wikisource.org/w/index.php?title=晉書/卷098&oldid=2614273
[282]: https://zh.wikisource.org/w/index.php?oldid=2614273
[283]: https://zh.wikisource.org/w/index.php?oldid=2614273
[284]: https://zh.wikisource.org/w/index.php?oldid=2614273
[285]: https://zh.wikisource.org/w/index.php?title=晉書/卷099&oldid=2644703
[290]: https://zh.wikisource.org/w/index.php?oldid=2614290
[293]: https://zh.wikisource.org/w/index.php?oldid=2180614
[297]: https://zh.wikisource.org/w/index.php?title=舊唐書/卷89&oldid=2589393
[308]: https://zh.wikisource.org/w/index.php?oldid=2312810
[311]: https://zh.wikisource.org/w/index.php?oldid=1566494
[312]: https://zh.wikisource.org/w/index.php?oldid=1566494
[313]: https://zh.wikisource.org/w/index.php?oldid=1566494
[314]: https://zh.wikisource.org/w/index.php?title=梁書/卷07&oldid=1566494
[315]: https://zh.wikisource.org/w/index.php?oldid=1566494
[317]: https://zh.wikisource.org/w/index.php?oldid=1566494
[320]: https://zh.wikisource.org/w/index.php?title=梁書/卷08&oldid=1538023
[321]: https://zh.wikisource.org/w/index.php?oldid=1508511
[322]: https://zh.wikisource.org/w/index.php?oldid=1514504
[323]: https://zh.wikisource.org/w/index.php?title=梁書/卷15&oldid=1506954
[327]: https://zh.wikisource.org/w/index.php?oldid=1508503
[328]: https://zh.wikisource.org/w/index.php?oldid=1508503
[329]: https://zh.wikisource.org/w/index.php?oldid=1508503
[332]: https://zh.wikisource.org/w/index.php?oldid=2063232
[333]: https://zh.wikisource.org/w/index.php?oldid=1506948
[336]: https://zh.wikisource.org/w/index.php?oldid=1544250
[337]: https://zh.wikisource.org/w/index.php?oldid=1544250
[338]: https://zh.wikisource.org/w/index.php?title=梁書/卷21&oldid=1544250
[340]: https://commons.wikimedia.org/w/index.php?oldid=902340163
[341]: https://zh.wikisource.org/w/index.php?oldid=1544250
[342]: https://commons.wikimedia.org/w/index.php?oldid=902340163
[343]: https://zh.wikisource.org/w/index.php?oldid=1544250
[344]: https://zh.wikisource.org/w/index.php?oldid=1544250
[350]: https://zh.wikisource.org/w/index.php?oldid=1511478
[353]: https://zh.wikisource.org/w/index.php?oldid=1511902
[355]: https://zh.wikisource.org/w/index.php?oldid=1538079
[357]: https://zh.wikisource.org/w/index.php?oldid=1538079
[360]: https://zh.wikisource.org/w/index.php?oldid=1514481
[361]: https://zh.wikisource.org/w/index.php?oldid=1514481
[362]: https://commons.wikimedia.org/wiki/File:NLC892-411999017142-12700_二十四史_第167冊.pdf
[363]: https://zh.wikisource.org/w/index.php?oldid=1514481
[364]: https://zh.wikisource.org/w/index.php?oldid=1514481
[365]: https://zh.wikisource.org/w/index.php?oldid=1511900
[367]: https://zh.wikisource.org/w/index.php?title=梁書/卷41&oldid=1512987
[375]: https://zh.wikisource.org/w/index.php?oldid=2087360
[376]: https://zh.wikisource.org/w/index.php?oldid=2087360
[377]: https://zh.wikisource.org/w/index.php?oldid=2087360
[378]: https://zh.wikisource.org/w/index.php?oldid=2087360
[379]: https://zh.wikisource.org/w/index.php?oldid=2087360
[380]: https://zh.wikisource.org/w/index.php?oldid=2087360
[387]: https://commons.wikimedia.org/w/index.php?oldid=703777627
[388]: https://zh.wikisource.org/w/index.php?title=梁書/卷50&oldid=1514482
[389]: https://zh.wikisource.org/w/index.php?title=梁書/卷50&oldid=1514482
[390]: https://commons.wikimedia.org/w/index.php?oldid=703777627
[391]: https://zh.wikisource.org/w/index.php?title=梁書/卷50&oldid=1514482
[393]: https://zh.wikisource.org/w/index.php?oldid=1530936
[394]: https://zh.wikisource.org/w/index.php?oldid=2312009
[395]: https://zh.wikisource.org/w/index.php?title=南齊書/卷2&oldid=2312009
[404]: https://commons.wikimedia.org/w/index.php?oldid=703777584
[405]: https://zh.wikisource.org/w/index.php?oldid=2074177
[406]: https://commons.wikimedia.org/w/index.php?oldid=703777584
[407]: https://zh.wikisource.org/w/index.php?oldid=2074177
[411]: https://commons.wikimedia.org/w/index.php?oldid=703777584
[412]: https://zh.wikisource.org/w/index.php?title=南齊書/卷20&oldid=2074177
[413]: https://zh.wikisource.org/w/index.php?title=南齊書/卷20&oldid=2074177
[414]: https://commons.wikimedia.org/w/index.php?oldid=703777584
[415]: https://zh.wikisource.org/w/index.php?oldid=2074177
[416]: https://commons.wikimedia.org/w/index.php?oldid=703777584
[417]: https://zh.wikisource.org/w/index.php?oldid=2074177
[418]: https://commons.wikimedia.org/w/index.php?oldid=703777584
[419]: https://zh.wikisource.org/w/index.php?oldid=2074177
[420]: https://commons.wikimedia.org/w/index.php?oldid=703777584
[421]: https://zh.wikisource.org/w/index.php?title=南齊書/卷20&oldid=2074177
[423]: https://zh.wikisource.org/w/index.php?title=南齊書/卷23&oldid=1545488
[424]: https://zh.wikisource.org/w/index.php?title=南齊書/卷24&oldid=1507882
[432]: https://zh.wikisource.org/w/index.php?oldid=1508012
[433]: https://zh.wikisource.org/w/index.php?oldid=1508012
[436]: https://zh.wikisource.org/w/index.php?oldid=1513917
[438]: https://zh.wikisource.org/w/index.php?oldid=2062531
[441]: https://zh.wikisource.org/w/index.php?oldid=1513918
[444]: https://zh.wikisource.org/w/index.php?oldid=1513918
[446]: https://zh.wikisource.org/w/index.php?oldid=1513918
[448]: https://zh.wikisource.org/w/index.php?oldid=1513918
[449]: https://zh.wikisource.org/w/index.php?oldid=1513918
[450]: https://zh.wikisource.org/w/index.php?oldid=1513918
[452]: https://zh.wikisource.org/w/index.php?title=%E5%8D%97%E9%BD%8A%E6%9B%B8%2F%E5%8D%B732&oldid=1513918
[453]: https://github.com/kanripo/KR2a0017/blob/787dd9a7da495542e8f17c26c96900ce37b2c211/KR2a0017_033.txt
[454]: https://zh.wikisource.org/w/index.php?title=南齊書/卷33&oldid=1492444
[455]: https://zh.wikisource.org/w/index.php?oldid=1514487
[456]: https://zh.wikisource.org/w/index.php?oldid=2401782
[457]: https://zh.wikisource.org/w/index.php?oldid=2401782
[458]: https://zh.wikisource.org/w/index.php?oldid=2401782
[459]: https://zh.wikisource.org/w/index.php?oldid=2401782
[460]: https://zh.wikisource.org/w/index.php?title=南齊書/卷36&oldid=1492438
[461]: https://commons.wikimedia.org/w/index.php?oldid=1154634011
[462]: https://zh.wikisource.org/w/index.php?title=南齊書/卷36&oldid=1492438
[464]: https://zh.wikisource.org/w/index.php?title=南齊書/卷39&oldid=1545485
[472]: https://zh.wikisource.org/w/index.php?oldid=2044621
[473]: https://zh.wikisource.org/w/index.php?oldid=1507997
[474]: https://zh.wikisource.org/w/index.php?oldid=1507997
[479]: https://zh.wikisource.org/w/index.php?oldid=2400356
[480]: https://zh.wikisource.org/w/index.php?oldid=2400356
[481]: https://zh.wikisource.org/w/index.php?oldid=2400356
[482]: https://zh.wikisource.org/w/index.php?oldid=2400356
[483]: https://zh.wikisource.org/w/index.php?oldid=2400356
[484]: https://zh.wikisource.org/w/index.php?title=南齊書/卷43&oldid=2400356
[485]: https://zh.wikisource.org/w/index.php?title=南齊書/卷44&oldid=1507959
[486]: https://zh.wikisource.org/w/index.php?title=南齊書/卷45&oldid=2273185
[487]: https://zh.wikisource.org/w/index.php?title=南齊書/卷45&oldid=2273185
[488]: https://zh.wikisource.org/w/index.php?oldid=2273185
[490]: https://zh.wikisource.org/w/index.php?title=%E5%8D%97%E9%BD%8A%E6%9B%B8%2F%E5%8D%B746&oldid=1511897
[491]: https://commons.wikimedia.org/wiki/File:NLC892-411999017142-12542_二十四史_第161冊.pdf
[492]: https://zh.wikisource.org/w/index.php?oldid=1492435
[493]: https://zh.wikisource.org/w/index.php?title=南齊書/卷47&oldid=1492435
[495]: https://zh.wikisource.org/w/index.php?oldid=2261984
[497]: https://zh.wikisource.org/w/index.php?oldid=2261984
[501]: https://zh.wikisource.org/w/index.php?oldid=2261984
[503]: https://zh.wikisource.org/w/index.php?oldid=2261984
[504]: https://zh.wikisource.org/w/index.php?oldid=2261984
[505]: https://zh.wikisource.org/w/index.php?oldid=2261984
[508]: https://zh.wikisource.org/w/index.php?oldid=2261984
[516]: https://zh.wikisource.org/w/index.php?oldid=1501803
[517]: https://zh.wikisource.org/w/index.php?oldid=1501803
[522]: https://commons.wikimedia.org/w/index.php?oldid=1298729844
[523]: https://zh.wikisource.org/w/index.php?oldid=2288359
[524]: https://commons.wikimedia.org/w/index.php?oldid=1298729844
[525]: https://zh.wikisource.org/w/index.php?oldid=2288359
[529]: https://zh.wikisource.org/w/index.php?oldid=2288359
[530]: https://commons.wikimedia.org/w/index.php?oldid=1298729844
[531]: https://zh.wikisource.org/w/index.php?oldid=2288359
[532]: https://commons.wikimedia.org/w/index.php?oldid=1298729844
[533]: https://zh.wikisource.org/w/index.php?oldid=2288359
[534]: https://zh.wikisource.org/w/index.php?oldid=2288359
[536]: https://zh.wikisource.org/w/index.php?title=南史/卷11&oldid=2288359
[541]: https://commons.wikimedia.org/w/index.php?oldid=1298729844
[542]: https://zh.wikisource.org/w/index.php?oldid=2288359
[543]: https://commons.wikimedia.org/w/index.php?oldid=1298729844
[544]: https://zh.wikisource.org/w/index.php?oldid=2288359
[545]: https://commons.wikimedia.org/w/index.php?oldid=1298729844
[546]: https://zh.wikisource.org/w/index.php?oldid=2288359
[547]: https://commons.wikimedia.org/w/index.php?oldid=1298729844
[548]: https://zh.wikisource.org/w/index.php?oldid=2288359
[549]: https://zh.wikisource.org/w/index.php?oldid=2288359
[550]: https://zh.wikisource.org/w/index.php?oldid=2288359
[551]: https://zh.wikisource.org/w/index.php?oldid=2288359
[552]: https://zh.wikisource.org/w/index.php?title=南史/卷11&oldid=2288359
[553]: https://zh.wikisource.org/w/index.php?title=南史/卷11&oldid=2288359
[554]: https://zh.wikisource.org/w/index.php?oldid=2060595
[555]: https://zh.wikisource.org/w/index.php?oldid=2060595
[557]: https://zh.wikisource.org/w/index.php?oldid=2060595
[558]: https://zh.wikisource.org/w/index.php?oldid=2060595
[559]: https://zh.wikisource.org/w/index.php?oldid=2060595
[561]: https://zh.wikisource.org/w/index.php?oldid=2060595
[562]: https://zh.wikisource.org/w/index.php?oldid=2060595
[564]: https://zh.wikisource.org/w/index.php?oldid=2268660
[566]: https://zh.wikisource.org/w/index.php?oldid=1963381
[567]: https://zh.wikisource.org/w/index.php?oldid=1963381
[568]: https://zh.wikisource.org/w/index.php?oldid=1963381
[570]: https://zh.wikisource.org/w/index.php?oldid=1963381
[573]: https://zh.wikisource.org/w/index.php?oldid=1963381
[576]: https://zh.wikisource.org/w/index.php?oldid=1531762
[578]: https://zh.wikisource.org/w/index.php?oldid=1531762
[584]: https://zh.wikisource.org/w/index.php?title=南史/卷19&oldid=1531762
[587]: https://zh.wikisource.org/w/index.php?title=南史/卷19&oldid=1531762
[588]: https://zh.wikisource.org/w/index.php?title=南史/卷19&oldid=1531762
[589]: https://zh.wikisource.org/w/index.php?title=南史/卷19&oldid=1531762
[590]: https://zh.wikisource.org/w/index.php?title=南史/卷19&oldid=1531762
[591]: https://zh.wikisource.org/w/index.php?title=南史/卷19&oldid=1531762
[592]: https://zh.wikisource.org/w/index.php?title=南史/卷19&oldid=1531762
[594]: https://github.com/kanripo/KR2a0024/blob/3c7bdbb072bf8e1eb70d134a94570c4b8de058ea/KR2a0024_020.txt
[595]: https://zh.wikisource.org/w/index.php?oldid=513423
[597]: https://zh.wikisource.org/w/index.php?oldid=1752646
[598]: https://zh.wikisource.org/w/index.php?oldid=1752646
[599]: https://zh.wikisource.org/w/index.php?oldid=1752646
[603]: https://zh.wikisource.org/w/index.php?oldid=1752646
[606]: https://zh.wikisource.org/w/index.php?oldid=1752646
[607]: https://zh.wikisource.org/w/index.php?oldid=1752646
[608]: https://zh.wikisource.org/w/index.php?oldid=1752646
[610]: https://zh.wikisource.org/w/index.php?oldid=1752646
[612]: https://zh.wikisource.org/w/index.php?oldid=1477957
[613]: https://zh.wikisource.org/w/index.php?oldid=1477957
[614]: https://zh.wikisource.org/w/index.php?oldid=1477957
[615]: https://zh.wikisource.org/w/index.php?oldid=1477957
[617]: https://zh.wikisource.org/w/index.php?oldid=1477957
[618]: https://zh.wikisource.org/w/index.php?title=南史/卷22&oldid=1477957
[619]: https://zh.wikisource.org/w/index.php?oldid=1477957
[620]: https://commons.wikimedia.org/wiki/File:NLC892-411999017142-12360_二十四史_第246冊.pdf
[621]: https://zh.wikisource.org/w/index.php?title=南史/卷22&oldid=1477957
[623]: https://zh.wikisource.org/w/index.php?oldid=1477957
[626]: https://zh.wikisource.org/w/index.php?oldid=1477957
[628]: https://commons.wikimedia.org/wiki/File:NLC892-411999017142-12360_二十四史_第246冊.pdf
[629]: https://zh.wikisource.org/w/index.php?oldid=1477957
[630]: https://zh.wikisource.org/w/index.php?oldid=1477957
[631]: https://github.com/kanripo/KR2a0024/blob/3c7bdbb072bf8e1eb70d134a94570c4b8de058ea/KR2a0024_022.txt
[633]: https://commons.wikimedia.org/wiki/File:NLC892-411999017142-12361_二十四史_第247冊.pdf
[634]: https://zh.wikisource.org/w/index.php?oldid=2478204
[635]: https://zh.wikisource.org/w/index.php?oldid=2478204
[639]: https://zh.wikisource.org/w/index.php?oldid=2478204
[640]: https://zh.wikisource.org/w/index.php?oldid=2478204
[641]: https://zh.wikisource.org/w/index.php?oldid=2478204
[642]: https://zh.wikisource.org/w/index.php?oldid=2478204
[643]: https://zh.wikisource.org/w/index.php?oldid=2478204
[644]: https://zh.wikisource.org/w/index.php?oldid=2478204
[648]: https://zh.wikisource.org/w/index.php?oldid=2478204
[650]: https://zh.wikisource.org/w/index.php?oldid=2478204
[652]: https://zh.wikisource.org/w/index.php?oldid=2478204
[653]: https://zh.wikisource.org/w/index.php?oldid=2478204
[654]: https://zh.wikisource.org/w/index.php?oldid=2478204
[655]: https://zh.wikisource.org/w/index.php?oldid=2478204
[656]: https://zh.wikisource.org/w/index.php?oldid=2478204
[659]: https://zh.wikisource.org/w/index.php?oldid=1765279
[660]: https://zh.wikisource.org/w/index.php?oldid=1765279
[661]: https://zh.wikisource.org/w/index.php?oldid=1765279
[662]: https://commons.wikimedia.org/w/index.php?oldid=1158108475
[663]: https://zh.wikisource.org/w/index.php?oldid=1765279
[664]: https://zh.wikisource.org/w/index.php?oldid=1765279
[666]: https://zh.wikisource.org/w/index.php?oldid=1765279
[667]: https://commons.wikimedia.org/wiki/File:NLC892-411999017142-12361_%E4%BA%8C%E5%8D%81%E5%9B%9B%E5%8F%B2_%E7%AC%AC247%E5%86%8A.pdf
[668]: https://zh.wikisource.org/w/index.php?oldid=1765279
[669]: https://zh.wikisource.org/w/index.php?oldid=1765279
[673]: https://zh.wikisource.org/w/index.php?oldid=1765279
[674]: https://zh.wikisource.org/w/index.php?oldid=1765279
[675]: https://zh.wikisource.org/w/index.php?oldid=1765279
[676]: https://commons.wikimedia.org/w/index.php?oldid=1158108475
[677]: https://zh.wikisource.org/w/index.php?title=%E5%8D%97%E5%8F%B2%2F%E5%8D%B724&oldid=1765279
[684]: https://zh.wikisource.org/w/index.php?oldid=1477359
[686]: https://zh.wikisource.org/w/index.php?oldid=1611067
[687]: https://zh.wikisource.org/w/index.php?oldid=1511857
[688]: https://zh.wikisource.org/w/index.php?oldid=1511857
[690]: https://zh.wikisource.org/w/index.php?oldid=1752309
[691]: https://zh.wikisource.org/w/index.php?oldid=8730255
[693]: https://zh.wikisource.org/w/index.php?title=南史/卷31&oldid=8730255
[694]: https://zh.wikisource.org/w/index.php?oldid=8730255
[696]: https://zh.wikisource.org/w/index.php?title=%E5%8D%97%E5%8F%B2%2F%E5%8D%B733&oldid=1554233
[697]: https://zh.wikisource.org/w/index.php?title=南史/卷33&oldid=1554233
[701]: https://zh.wikisource.org/w/index.php?oldid=1956596
[702]: https://zh.wikisource.org/w/index.php?oldid=1569807
[703]: https://zh.wikisource.org/w/index.php?oldid=1552313
[710]: https://zh.wikisource.org/w/index.php?oldid=2598501
[712]: https://zh.wikisource.org/w/index.php?title=南史/卷48&oldid=2493997
[717]: https://zh.wikisource.org/w/index.php?oldid=1518868
[721]: https://zh.wikisource.org/w/index.php?oldid=1553912
[722]: https://zh.wikisource.org/w/index.php?oldid=1553912
[723]: https://zh.wikisource.org/w/index.php?oldid=1495505
[724]: https://zh.wikisource.org/w/index.php?oldid=1748895
[727]: https://zh.wikisource.org/w/index.php?oldid=1748901
[732]: https://zh.wikisource.org/w/index.php?oldid=8746774
[733]: https://raw.githubusercontent.com/kanripo/KR2a0012/214fcafa79894355909c9d8c2c1533089e7791c6/KR2a0012_009.txt
[734]: https://raw.githubusercontent.com/kanripo/KR2a0012/214fcafa79894355909c9d8c2c1533089e7791c6/KR2a0012_009.txt
[735]: https://da.library.pref.osaka.jp/api/items/01-0015983/manifest.json
[736]: https://github.com/kanripo/KR2a0012/blob/214fcafa79894355909c9d8c2c1533089e7791c6/KR2a0012_010.txt
[738]: https://zh.wikisource.org/w/index.php?title=三國志/卷11&oldid=2373044
[740]: https://zh.wikisource.org/w/index.php?oldid=2331498
[744]: https://raw.githubusercontent.com/kanripo/KR2a0012/214fcafa79894355909c9d8c2c1533089e7791c6/KR2a0012_015.txt
[748]: https://github.com/kanripo/KR2a0012/blob/214fcafa79894355909c9d8c2c1533089e7791c6/KR2a0012_019.txt
[750]: https://raw.githubusercontent.com/kanripo/KR2a0012/214fcafa79894355909c9d8c2c1533089e7791c6/KR2a0012_022.txt
[754]: https://github.com/kanripo/KR2a0012/blob/214fcafa79894355909c9d8c2c1533089e7791c6/KR2a0012_027.txt
[756]: https://github.com/kanripo/KR2a0012/blob/214fcafa79894355909c9d8c2c1533089e7791c6/KR2a0012_028.txt
[762]: https://zh.wikisource.org/w/index.php?oldid=2085144
[765]: https://zh.wikisource.org/w/index.php?oldid=2085144
[767]: https://zh.wikisource.org/w/index.php?oldid=2085144
[768]: https://zh.wikisource.org/w/index.php?oldid=2085144
[770]: https://zh.wikisource.org/w/index.php?oldid=2085144
[771]: https://zh.wikisource.org/w/index.php?oldid=2085144
[775]: https://zh.wikisource.org/w/index.php?oldid=2085149
[776]: https://zh.wikisource.org/w/index.php?oldid=2085149
[777]: https://zh.wikisource.org/w/index.php?oldid=2085149
[782]: https://zh.wikisource.org/w/index.php?oldid=2085149
[790]: https://zh.wikisource.org/w/index.php?oldid=2638131
[791]: https://zh.wikisource.org/w/index.php?oldid=2638131
[792]: https://zh.wikisource.org/w/index.php?oldid=2638131
[795]: https://zh.wikisource.org/w/index.php?oldid=2638131
[797]: https://zh.wikisource.org/w/index.php?oldid=2638131
[799]: https://zh.wikisource.org/w/index.php?oldid=2131313
[800]: https://zh.wikisource.org/w/index.php?oldid=2131313
[802]: https://zh.wikisource.org/w/index.php?oldid=2085159
[803]: https://zh.wikisource.org/w/index.php?oldid=2085159
[804]: https://zh.wikisource.org/w/index.php?oldid=2085159
[805]: https://zh.wikisource.org/w/index.php?oldid=2085159
[806]: https://zh.wikisource.org/w/index.php?oldid=2085159
[811]: https://zh.wikisource.org/w/index.php?title=史記/卷003&oldid=7909145
[812]: https://zh.wikisource.org/w/index.php?title=史記/卷004&oldid=7909147
[813]: https://zh.wikisource.org/w/index.php?title=史記/卷005&oldid=8744286
[814]: https://zh.wikisource.org/w/index.php?title=史記/卷006&oldid=7907969
[815]: https://zh.wikisource.org/w/index.php?title=史記/卷007&oldid=5978360
[816]: https://zh.wikisource.org/w/index.php?title=史記/卷008&oldid=2440965
[817]: https://zh.wikisource.org/w/index.php?title=史記/卷009&oldid=2087062
[819]: https://zh.wikisource.org/w/index.php?title=史記/卷011&oldid=2520527
[822]: https://zh.wikisource.org/w/index.php?title=史記/卷031&oldid=7909287
[823]: https://zh.wikisource.org/w/index.php?title=史記/卷032&oldid=445042
[824]: https://zh.wikisource.org/w/index.php?title=史記/魯周公世家&oldid=7909289
[825]: https://zh.wikisource.org/w/index.php?title=史記/卷034&oldid=2559287
[826]: https://zh.wikisource.org/w/index.php?title=史記/卷035&oldid=8737302
[827]: https://zh.wikisource.org/w/index.php?title=史記/卷036&oldid=2588525
[828]: https://zh.wikisource.org/w/index.php?title=史記/卷037&oldid=5977124
[829]: https://zh.wikisource.org/w/index.php?title=史記/卷038&oldid=8737306
[830]: https://zh.wikisource.org/w/index.php?title=史記/卷039&oldid=2588534
[831]: https://zh.wikisource.org/w/index.php?title=史記/卷040&oldid=8736796
[832]: https://zh.wikisource.org/w/index.php?title=史記/卷041&oldid=2018395
[833]: https://zh.wikisource.org/w/index.php?title=史記/卷042&oldid=2016409
[834]: https://zh.wikisource.org/w/index.php?title=史記/卷043&oldid=7903603
[835]: https://zh.wikisource.org/w/index.php?title=史記/卷044&oldid=7903606
[836]: https://zh.wikisource.org/w/index.php?title=史記/卷045&oldid=7903607
[837]: https://zh.wikisource.org/w/index.php?title=史記/卷046&oldid=2560838
[838]: https://zh.wikisource.org/w/index.php?title=史記/卷047&oldid=7903609
[840]: https://zh.wikisource.org/w/index.php?title=史記/卷049&oldid=7903610
[842]: https://zh.wikisource.org/w/index.php?title=史記/卷051&oldid=2380315
[845]: https://zh.wikisource.org/w/index.php?title=史記/卷054&oldid=1490182
[846]: https://zh.wikisource.org/w/index.php?title=史記/卷055&oldid=2666612
[847]: https://zh.wikisource.org/w/index.php?title=史記/卷056&oldid=1961615
[848]: https://zh.wikisource.org/w/index.php?title=史記/卷057&oldid=1569360
[854]: https://zh.wikisource.org/w/index.php?title=史記/卷063&oldid=7903601
[857]: https://zh.wikisource.org/w/index.php?title=史記/卷066&oldid=2621138
[858]: https://zh.wikisource.org/w/index.php?title=史記/卷067&oldid=7869003
[860]: https://zh.wikisource.org/w/index.php?title=史記/卷069&oldid=2621145
[862]: https://zh.wikisource.org/w/index.php?title=史記/卷071&oldid=2621152
[864]: https://zh.wikisource.org/w/index.php?title=史記/卷073&oldid=7909285
[868]: https://zh.wikisource.org/w/index.php?title=史記/卷077&oldid=367917
[870]: https://zh.wikisource.org/w/index.php?title=史記/卷079&oldid=2549307
[871]: https://zh.wikisource.org/w/index.php?title=史記/卷080&oldid=2089316
[875]: https://zh.wikisource.org/w/index.php?title=史記/卷084&oldid=1568305
[876]: https://zh.wikisource.org/w/index.php?title=史記/卷085&oldid=2027911
[877]: https://zh.wikisource.org/w/index.php?title=史記/卷086&oldid=2388562
[878]: https://zh.wikisource.org/w/index.php?title=史記/卷087&oldid=2364605
[880]: https://zh.wikisource.org/w/index.php?title=史記/卷089&oldid=8744143
[884]: https://zh.wikisource.org/w/index.php?title=史記/卷093&oldid=368019
[885]: https://zh.wikisource.org/w/index.php?title=史記/卷094&oldid=2171897
[886]: https://zh.wikisource.org/w/index.php?title=史記/卷095&oldid=2298709
[887]: https://zh.wikisource.org/w/index.php?title=史記/卷096&oldid=8770206
[888]: https://zh.wikisource.org/w/index.php?title=史記/卷097&oldid=1383195
[889]: https://zh.wikisource.org/w/index.php?title=史記/卷098&oldid=1490318
[891]: https://zh.wikisource.org/w/index.php?title=史記/卷100&oldid=1965696
[892]: https://zh.wikisource.org/w/index.php?title=史記/卷101&oldid=368092
[893]: https://zh.wikisource.org/w/index.php?title=史記/卷102&oldid=1753957
[894]: https://zh.wikisource.org/w/index.php?title=史記/卷103&oldid=2096814
[895]: https://zh.wikisource.org/w/index.php?title=史記/卷104&oldid=8739534
[896]: https://zh.wikisource.org/w/index.php?title=史記/卷105&oldid=8842726
[898]: https://zh.wikisource.org/w/index.php?title=史記/卷107&oldid=2540571
[900]: https://zh.wikisource.org/w/index.php?title=史記/卷109&oldid=1765440
[901]: https://zh.wikisource.org/w/index.php?title=史記/卷110&oldid=8735645
[902]: https://zh.wikisource.org/w/index.php?title=史記/卷111&oldid=8730225
[904]: https://zh.wikisource.org/w/index.php?title=史記/卷113&oldid=8735632
[905]: https://zh.wikisource.org/w/index.php?title=史記/卷114&oldid=8735633
[906]: https://zh.wikisource.org/w/index.php?title=史記/卷115&oldid=439220
[907]: https://zh.wikisource.org/w/index.php?title=史記/卷116&oldid=7903636
[909]: https://zh.wikisource.org/w/index.php?title=史記/卷118&oldid=7904122
[910]: https://zh.wikisource.org/w/index.php?title=史記/卷119&oldid=7904123
[911]: https://zh.wikisource.org/w/index.php?title=史記/卷120&oldid=9166127
[913]: https://zh.wikisource.org/w/index.php?title=史記/卷122&oldid=7904124
[914]: https://zh.wikisource.org/w/index.php?title=史記/卷123&oldid=8736799
[915]: https://zh.wikisource.org/w/index.php?title=史記/卷124&oldid=367994
[917]: https://zh.wikisource.org/w/index.php?title=史記/卷126&oldid=2609358
[921]: https://zh.wikisource.org/w/index.php?title=史記/卷130&oldid=2609362
[922]: https://zh.wikisource.org/w/index.php?oldid=2567459
[926]: https://zh.wikisource.org/w/index.php?oldid=2567459
[927]: https://zh.wikisource.org/w/index.php?oldid=2567459
[929]: https://zh.wikisource.org/w/index.php?oldid=2567463
[943]: https://zh.wikisource.org/w/index.php?oldid=2567462
[947]: https://zh.wikisource.org/w/index.php?oldid=2567465
[962]: https://zh.wikisource.org/w/index.php?oldid=1532652
[968]: https://zh.wikisource.org/w/index.php?oldid=1532655
[984]: https://zh.wikisource.org/w/index.php?oldid=1503586
[986]: https://zh.wikisource.org/w/index.php?oldid=1503586
[987]: https://zh.wikisource.org/w/index.php?oldid=2004422
[988]: https://zh.wikisource.org/w/index.php?oldid=2004422
[999]: https://raw.githubusercontent.com/kanripo/KR2a0016/e80c057667e3c8684f11d5088251e10244d5a264/KR2a0016_001.txt
[1005]: https://zh.wikisource.org/w/index.php?oldid=2368147
[1011]: https://zh.wikisource.org/w/index.php?oldid=1748380
[1012]: https://zh.wikisource.org/w/index.php?oldid=2634831
[1013]: https://zh.wikisource.org/w/index.php?oldid=2634831
[1014]: https://zh.wikisource.org/w/index.php?oldid=2634831
[1015]: https://zh.wikisource.org/w/index.php?oldid=2634831
[1016]: https://raw.githubusercontent.com/kanripo/KR2a0016/e80c057667e3c8684f11d5088251e10244d5a264/KR2a0016_041.txt
[1017]: https://zh.wikisource.org/w/index.php?oldid=2634831
[1018]: https://zh.wikisource.org/w/index.php?oldid=2634831
[1019]: https://commons.wikimedia.org/w/index.php?oldid=979637190
[1020]: https://zh.wikisource.org/w/index.php?oldid=2634831
[1021]: https://zh.wikisource.org/w/index.php?title=宋書/卷41&oldid=2634831
[1022]: https://zh.wikisource.org/w/index.php?title=宋書/卷42&oldid=1478172
[1023]: https://commons.wikimedia.org/w/index.php?title=File:NLC892-411999017142-12779_%E4%BA%8C%E5%8D%81%E5%9B%9B%E5%8F%B2_%E7%AC%AC144%E5%86%8A.pdf&oldid=979637198
[1024]: https://zh.wikisource.org/w/index.php?title=%E5%AE%8B%E6%9B%B8/%E5%8D%B744&oldid=1746033
[1028]: https://zh.wikisource.org/w/index.php?oldid=2118581
[1031]: https://zh.wikisource.org/w/index.php?oldid=2118581
[1033]: https://raw.githubusercontent.com/kanripo/KR2a0016/e80c057667e3c8684f11d5088251e10244d5a264/KR2a0016_046.txt
[1034]: https://zh.wikisource.org/w/index.php?oldid=2118581
[1037]: https://zh.wikisource.org/w/index.php?oldid=2118581
[1040]: https://zh.wikisource.org/w/index.php?oldid=2118581
[1044]: https://zh.wikisource.org/w/index.php?oldid=1791560
[1045]: https://zh.wikisource.org/w/index.php?oldid=2371899
[1046]: https://zh.wikisource.org/w/index.php?oldid=1959959
[1047]: https://zh.wikisource.org/w/index.php?oldid=1959959
[1048]: https://zh.wikisource.org/w/index.php?oldid=2190655
[1049]: https://zh.wikisource.org/w/index.php?oldid=2190655
[1052]: https://zh.wikisource.org/w/index.php?oldid=2190655
[1053]: https://zh.wikisource.org/w/index.php?oldid=2190655
[1054]: https://zh.wikisource.org/w/index.php?oldid=2190655
[1056]: https://raw.githubusercontent.com/kanripo/KR2a0016/e80c057667e3c8684f11d5088251e10244d5a264/KR2a0016_053.txt
[1057]: https://zh.wikisource.org/w/index.php?oldid=1996685
[1058]: https://raw.githubusercontent.com/kanripo/KR2a0016/e80c057667e3c8684f11d5088251e10244d5a264/KR2a0016_053.txt
[1059]: https://raw.githubusercontent.com/kanripo/KR2a0016/e80c057667e3c8684f11d5088251e10244d5a264/KR2a0016_056.txt
[1062]: https://github.com/kanripo/KR2a0016/blob/e80c057667e3c8684f11d5088251e10244d5a264/KR2a0016_058.txt
[1063]: https://raw.githubusercontent.com/kanripo/KR2a0016/e80c057667e3c8684f11d5088251e10244d5a264/KR2a0016_059.txt
[1064]: https://zh.wikisource.org/w/index.php?title=宋書/卷60&oldid=1996694
[1065]: https://zh.wikisource.org/w/index.php?oldid=1996694
[1066]: https://zh.wikisource.org/w/index.php?oldid=1996694
[1067]: https://zh.wikisource.org/w/index.php?title=%E5%AE%8B%E6%9B%B8/%E5%8D%B760&oldid=1996694
[1069]: https://github.com/kanripo/KR2a0016/blob/e80c057667e3c8684f11d5088251e10244d5a264/KR2a0016_062.txt
[1071]: https://zh.wikisource.org/w/index.php?title=宋書/卷63&oldid=2118589
[1072]: https://commons.wikimedia.org/wiki/File:NLC892-411999017142-12245_二十四史_第147冊.pdf
[1074]: https://zh.wikisource.org/w/index.php?title=%E5%AE%8B%E6%9B%B8%2F%E5%8D%B764&oldid=1748217
[1075]: https://zh.wikisource.org/w/index.php?oldid=2069104
[1076]: https://upload.wikimedia.org/wikipedia/commons/c/cb/NLC892-411999017142-12245_%E4%BA%8C%E5%8D%81%E5%9B%9B%E5%8F%B2_%E7%AC%AC147%E5%86%8A.pdf#page=64
[1077]: https://zh.wikisource.org/w/index.php?title=%E5%AE%8B%E6%9B%B8%2F%E5%8D%B766&oldid=2069104
[1078]: https://raw.githubusercontent.com/kanripo/KR2a0016/e80c057667e3c8684f11d5088251e10244d5a264/KR2a0016_067.txt
[1079]: https://zh.wikisource.org/w/index.php?title=宋書/卷71&oldid=2485515
[1080]: https://commons.wikimedia.org/wiki/File:NLC892-411999017142-12246_二十四史_第148冊.pdf
[1081]: https://github.com/kanripo/KR2a0016/blob/e80c057667e3c8684f11d5088251e10244d5a264/KR2a0016_071.txt
[1082]: https://zh.wikisource.org/w/index.php?oldid=1997159
[1083]: https://zh.wikisource.org/w/index.php?oldid=1997159
[1084]: https://zh.wikisource.org/w/index.php?oldid=2118597
[1085]: https://zh.wikisource.org/w/index.php?oldid=2118597
[1086]: https://zh.wikisource.org/w/index.php?oldid=2118597
[1087]: https://zh.wikisource.org/w/index.php?title=宋書/卷75&oldid=1997722
[1089]: https://zh.wikisource.org/w/index.php?oldid=1997726
[1091]: https://zh.wikisource.org/w/index.php?title=宋書/卷77&oldid=1997730
[1093]: https://zh.wikisource.org/w/index.php?oldid=2261200
[1094]: https://zh.wikisource.org/w/index.php?oldid=2261200
[1095]: https://commons.wikimedia.org/w/index.php?oldid=1229668893
[1096]: https://zh.wikisource.org/w/index.php?oldid=2261200
[1097]: https://zh.wikisource.org/w/index.php?oldid=2261200
[1098]: https://zh.wikisource.org/w/index.php?title=宋書/卷80&oldid=2261200
[1099]: https://zh.wikisource.org/w/index.php?oldid=2261200
[1100]: https://zh.wikisource.org/w/index.php?oldid=2069213
[1105]: https://zh.wikisource.org/w/index.php?oldid=2069101
[1107]: https://github.com/kanripo/KR2a0016/blob/e80c057667e3c8684f11d5088251e10244d5a264/KR2a0016_085.txt
[1108]: https://zh.wikisource.org/w/index.php?title=宋書/卷86&oldid=2069103
[1110]: https://zh.wikisource.org/w/index.php?title=宋書/卷88&oldid=2069210
[1112]: https://zh.wikisource.org/w/index.php?title=宋書/卷88&oldid=2069210
[1113]: https://zh.wikisource.org/w/index.php?title=宋書/卷88&oldid=2069210
[1114]: https://zh.wikisource.org/w/index.php?oldid=2195614
[1115]: https://zh.wikisource.org/w/index.php?oldid=2195614
[1116]: https://zh.wikisource.org/w/index.php?oldid=2195614
[1122]: https://zh.wikisource.org/w/index.php?oldid=2195614
[1126]: https://zh.wikisource.org/w/index.php?oldid=2195614
[1127]: https://commons.wikimedia.org/w/index.php?oldid=979439170
[1128]: https://zh.wikisource.org/w/index.php?oldid=2195614
[1129]: https://zh.wikisource.org/w/index.php?oldid=2195614
[1131]: https://zh.wikisource.org/w/index.php?title=%E5%AE%8B%E6%9B%B8%2F%E5%8D%B792&oldid=2195614
[1132]: https://commons.wikimedia.org/wiki/File:NLC016-HWRB201817006-2849_%E5%AE%8B%E6%9B%B8_%E4%B8%80%E7%99%BE%E5%8D%B7_%E7%AC%AC23%E5%86%8A.pdf
[1133]: https://zh.wikisource.org/w/index.php?oldid=1962755
[1135]: https://zh.wikisource.org/w/index.php?oldid=1962755
[1137]: https://zh.wikisource.org/w/index.php?oldid=1962755
[1138]: https://zh.wikisource.org/w/index.php?title=%E5%AE%8B%E6%9B%B8%2F%E5%8D%B793&oldid=1962755
[1139]: https://zh.wikisource.org/w/index.php?oldid=2195835
[1140]: https://zh.wikisource.org/w/index.php?oldid=8230488
[1143]: https://zh.wikisource.org/w/index.php?oldid=2180354
[1144]: https://zh.wikisource.org/w/index.php?oldid=582080
[1145]: https://zh.wikisource.org/w/index.php?oldid=11122997
[1150]: https://zh.wikisource.org/w/index.php?oldid=2607174
[1158]: https://zh.wikisource.org/w/index.php?oldid=2587825
[1163]: https://zh.wikisource.org/w/index.php?title=魏書/卷18&oldid=1550395
[1164]: https://zh.wikisource.org/w/index.php?title=魏書/卷24&oldid=2021236
[1167]: https://raw.githubusercontent.com/kanripo/KR2a0020/17b6525eb5aaa878b9640f5a61e90da934ce5fc4/KR2a0020_035.txt
[1168]: https://github.com/kanripo/KR2a0020/blob/17b6525eb5aaa878b9640f5a61e90da934ce5fc4/KR2a0020_038.txt
[1170]: https://zh.wikisource.org/w/index.php?oldid=1501651
[1171]: https://zh.wikisource.org/w/index.php?title=%E9%AD%8F%E6%9B%B8%2F%E5%8D%B758&oldid=2087998
[1172]: https://zh.wikisource.org/w/index.php?title=%E9%AD%8F%E6%9B%B8%2F%E5%8D%B758&oldid=2087998
[1173]: https://zh.wikisource.org/w/index.php?title=%E9%AD%8F%E6%9B%B8%2F%E5%8D%B758&oldid=2087998
[1177]: https://zh.wikisource.org/w/index.php?oldid=1513419
[1178]: https://zh.wikisource.org/w/index.php?title=魏書/卷67&oldid=468068
[1179]: https://zh.wikisource.org/w/index.php?oldid=2294110
[1180]: https://zh.wikisource.org/w/index.php?oldid=760052
[1182]: https://zh.wikisource.org/w/index.php?oldid=760052
[1185]: https://commons.wikimedia.org/w/index.php?oldid=1130546999
[1186]: https://zh.wikisource.org/w/index.php?oldid=2004220
[1187]: https://commons.wikimedia.org/w/index.php?oldid=1130546999
[1188]: https://zh.wikisource.org/w/index.php?title=%E6%96%B0%E5%94%90%E6%9B%B8%2F%E5%8D%B7071%E4%B8%8B&oldid=2405769
[1189]: https://zh.wikisource.org/w/index.php?oldid=1519175
[1190]: https://zh.wikisource.org/w/index.php?title=新唐書/卷116&oldid=3528844
[1191]: https://zh.wikisource.org/w/index.php?oldid=2610515
[1192]: https://zh.wikisource.org/w/index.php?title=周書/卷41&oldid=2432538
[1193]: https://zh.wikisource.org/w/index.php?oldid=2432541
[1199]: https://zh.wikisource.org/w/index.php?oldid=2454083
[1200]: https://zh.wikisource.org/w/index.php?title=%E8%B3%87%E6%B2%BB%E9%80%9A%E9%91%91/%E5%8D%B7094&oldid=2312212
[1201]: https://zh.wikisource.org/w/index.php?oldid=2617598
[1209]: https://zh.wikisource.org/w/index.php?oldid=1497680
[1213]: https://zh.wikisource.org/w/index.php?oldid=1552077
[1222]: https://zh.wikisource.org/w/index.php?title=史記/卷013&oldid=2606991
[1223]: https://zh.wikisource.org/w/index.php?title=史記/卷014&oldid=2607001
[1224]: https://zh.wikisource.org/w/index.php?title=史記/卷015&oldid=2607002
[1225]: https://zh.wikisource.org/w/index.php?title=史記/卷016&oldid=2607007
[1227]: https://zh.wikisource.org/w/index.php?title=史記/卷018&oldid=9484995
[1229]: https://zh.wikisource.org/w/index.php?title=史記/卷020&oldid=2607036
