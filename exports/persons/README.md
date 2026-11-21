# 人物 JSON 索引

可重建匯出，涵蓋目前已標註資料，包含明示選用的暫定跨篇同指；原 ID、證據與判讀均保留。並非全部史料或完整覆核。

程式可讀取 [index.json](index.json)，再依各筆 `path` 取得人物資料。重新產生：`python3 scripts/export_person_bundles.py`。

出生排行與籍貫結構化欄位仍在逐篇回填；缺欄位不代表來源沒有此資訊。提及頻次依固定見證的獨立位置計算；原始錨點完整保留，同位置節引重出另列raw／duplicate與對應群組，不代表來源權威度。

已接合父系見 [家族組裝資料](../../registry/family-assemblies.json)。`assembled_identity.person_id` 是共用家族根的組裝 ID，`source_person_ids` 保留各篇候選；父子及同指證據可由記錄 ID 回查。缺代節點另有 `ancestor_person_id`、`generation_distance` 與空值中間世代；父親空值不表示它另成一族。

點選家族標題可展開或收起後代。`*` 表示缺名世代，不建立人物，也不表示不同缺名位置是同一人。表內只列家族根後的 ID 尾碼；根人物以「根」表示，完整 ID 保留於家族標題及 JSON。最多提及來源另列一欄，同數並列；提及次數不代表史料優先權。已完成格式遷移的舊 ID 與 JSON 入口已撤除；待身份覆核的來源候選仍分存。

尚未連入同族的人物見 [獨立人物索引](unconnected.md)。

## 可展開家族


[第1頁](README.md) · [第2頁](families-002.md)

<details><summary><code>03n_n2r_8rt</code> 阮裕（韜玄祖）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 阮裕（韜玄祖） | [《晉書・王羲之》][196] | [JSON](03n_n2r_8rt.json) |
| `***A` | 阮韜 | [《南史・王裕之　王鎮之　王韶之　王悅之　王准之》][506] | [JSON](03n_n2r_8rt_%2A%2A%2AA.json) |

</details>

<details><summary><code>04u_gq0_nke</code> 鼂錯父未名（袁盎鼂錯列傳候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 鼂錯父未名 | [《史記・袁盎鼂錯列傳》][649] | [JSON](04u_gq0_nke.json) |
| `A` | 鼂錯 | [《史記・袁盎鼂錯列傳》][649] | [JSON](04u_gq0_nke_A.json) |

</details>

<details><summary><code>069_dn8_o4r</code> 江遵（江祏祖）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 江遵（江祏祖） | [《南史・荀伯玉　崔祖思　蘇侃　虞悰　胡諧之　虞玩之　劉休　江祏》][529] | [JSON](069_dn8_o4r.json) |
| `A` | 江氏（齊景皇后，蕭鸞母） | [《南史・荀伯玉　崔祖思　蘇侃　虞悰　胡諧之　虞玩之　劉休　江祏》][529] | [JSON](069_dn8_o4r_A.json) |

</details>

<details><summary><code>06i_k5v_922</code> 申侯（鄭世家武姜父候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 申侯 | [《史記・鄭世家》][590] | [JSON](06i_k5v_922.json) |
| `A` | 武姜 | [《史記・鄭世家》][590] | [JSON](06i_k5v_922_A.json) |

</details>

<details><summary><code>0ad_dbw_97q</code> 晉昭公（4 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 晉昭公 | [《史記・晉世家》][587] | [JSON](0ad_dbw_97q.json) |
| `A` | 雍（戴子晉昭公子） | [《史記・晉世家》][587] | [JSON](0ad_dbw_97q_A.json) |
| `AA` | 忌（戴子子） | [《史記・晉世家》][587] | [JSON](0ad_dbw_97q_AA.json) |
| `AAA` | 驕（晉哀公） | [《史記・晉世家》][587] | [JSON](0ad_dbw_97q_AAA.json) |

</details>

<details><summary><code>0bu_skv_qsr</code> 呂青（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 呂青 | [《史記・項羽本紀》][573]、[《史記・高祖本紀》][574] | [JSON](0bu_skv_qsr.json) |
| `A` | 呂臣 | [《史記・項羽本紀》][573]、[《史記・高祖本紀》][574] | [JSON](0bu_skv_qsr_A.json) |

</details>

<details><summary><code>0c1_b9d_9c2</code> 楊彪（7 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 楊彪 | [《後漢書・孝獻帝紀》][51] | [JSON](0c1_b9d_9c2.json) |
| `A` | 楊脩 | [《三國志・任城陳蕭王傳》][554] | [JSON](0c1_b9d_9c2_A.json) |
| `AA` | 楊囂 | [《三國志・任城陳蕭王傳》][554] | [JSON](0c1_b9d_9c2_AA.json) |
| `AAA` | 楊準 | [《三國志・任城陳蕭王傳》][554] | [JSON](0c1_b9d_9c2_AAA.json) |
| `AAAA` | 楊嶠 | [《三國志・任城陳蕭王傳》][554] | [JSON](0c1_b9d_9c2_AAAA.json) |
| `AAAB` | 楊髦 | [《三國志・任城陳蕭王傳》][554] | [JSON](0c1_b9d_9c2_AAAB.json) |
| `AAAC` | 楊俊 | [《三國志・任城陳蕭王傳》][554] | [JSON](0c1_b9d_9c2_AAAC.json) |

</details>

<details><summary><code>0db_22c_332</code> 何進（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 何進 | [《後漢書・荀韓鍾陳列傳》][53] | [JSON](0db_22c_332.json) |
| `*A` | 何晏 | [《三國志・諸夏侯曹傳》][541] | [JSON](0db_22c_332_%2AA.json) |
| `*AA` | 晏未名男 | [《三國志・諸夏侯曹傳》][541] | [JSON](0db_22c_332_%2AAA.json) |

</details>

<details><summary><code>0hs_fg6_1qj</code> 田榮（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 田榮 | [《史記・田儋列傳》][642] | [JSON](0hs_fg6_1qj.json) |
| `A` | 廣（田榮子） | [《史記・酈生陸賈列傳》][645] | [JSON](0hs_fg6_1qj_A.json) |
| `B` | 田廣 | [《史記・田儋列傳》][642] | [JSON](0hs_fg6_1qj_B.json) |

</details>

<details><summary><code>0lf_ggf_5xo</code> 張弘策（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 張弘策 | [《南史・謝晦　謝裕　謝方明　謝靈運》][432] | [JSON](0lf_ggf_5xo.json) |
| `A` | 張緬（字元長） | [《梁書・張緬 弟纘 綰》][268] | [JSON](0lf_ggf_5xo_A.json) |

</details>

<details><summary><code>0s7_r72_j8q</code> 魯武公（4 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 魯武公 | [《史記・魯周公世家》][581] | [JSON](0s7_r72_j8q.json) |
| `A` | 括（魯武公長子） | [《史記・魯周公世家》][581] | [JSON](0s7_r72_j8q_A.json) |
| `AA` | 伯御（魯君） | [《史記・魯周公世家》][581] | [JSON](0s7_r72_j8q_AA.json) |
| `B` | 戲（魯懿公） | [《史記・魯周公世家》][581] | [JSON](0s7_r72_j8q_B.json) |

</details>

<details><summary><code>0us_j8h_to7</code> 假（老韓列傳候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 假 | [《史記・老子韓非列傳》][611] | [JSON](0us_j8h_to7.json) |
| `A` | 解 | [《史記・老子韓非列傳》][611] | [JSON](0us_j8h_to7_A.json) |

</details>

<details><summary><code>0va_s3x_wb4</code> 蕭統（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 蕭統 | [《梁書・昭明太子 哀太子 愍懷太子》][242]、[《南史・王曇首》][471]、[《南史・王曇首》][470] | [JSON](0va_s3x_wb4.json) |
| `A` | 蕭譽（梁河東王） | [《梁書・豫章王綜 武陵王紀 臨賀王正德 河東王譽》][278] | [JSON](0va_s3x_wb4_A.json) |

</details>

<details><summary><code>0xt_iyn_d3t</code> 趙夙（趙世家候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 趙夙 | [《史記・趙世家》][591] | [JSON](0xt_iyn_d3t.json) |
| `A` | 共孟 | [《史記・趙世家》][591] | [JSON](0xt_iyn_d3t_A.json) |

</details>

<details><summary><code>0zd_9uz_t7m</code> 臧汪（5 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 臧汪 | [《南史・后妃上》][403] | [JSON](0zd_9uz_t7m.json) |
| `A` | 臧儁 | [《南史・后妃上》][401]、[《南史・后妃上》][402]、[《南史・后妃上》][403]、[《宋書・后妃》][759] | [JSON](0zd_9uz_t7m_A.json) |
| `AA` | 臧愛親 | [《南史・后妃上》][403]、[《南史・范泰　荀伯子　徐廣　鄭鮮之　裴松之　何承天》][518]、[《宋書・鄭鮮之 裴松之 何承天》][795] | [JSON](0zd_9uz_t7m_AA.json) |
| `AB` | 臧熹（字義和） | [《宋書・臧質 魯爽 沈攸之》][805] | [JSON](0zd_9uz_t7m_AB.json) |
| `ABA` | 臧質（字含文） | [《宋書・臧質 魯爽 沈攸之》][805]、[《宋書・朱脩之 宗愨 王玄謨》][808] | [JSON](0zd_9uz_t7m_ABA.json) |

</details>

<details><summary><code>113_odk_emq</code> 衞綰（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 衞綰 | [《史記・萬石張叔列傳》][651] | [JSON](113_odk_emq.json) |
| `A` | 信（衞綰子） | [《史記・萬石張叔列傳》][651] | [JSON](113_odk_emq_A.json) |

</details>

<details><summary><code>128_4ab_z34</code> 熊延（楚君）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 熊延（楚君） | [《史記・楚世家》][588] | [JSON](128_4ab_z34.json) |
| `A` | 熊勇（楚君） | [《史記・楚世家》][588] | [JSON](128_4ab_z34_A.json) |

</details>

<details><summary><code>16c_0og_lvl</code> 沈叔仁（沈攸之父）（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 沈叔仁（沈攸之父） | [《宋書・臧質 魯爽 沈攸之》][803]、[《宋書・臧質 魯爽 沈攸之》][804] | [JSON](16c_0og_lvl.json) |
| `A` | 沈攸之（字仲達） | [《南齊書・王奐 從弟繢 張沖》][360]、[《南史・王誕　王華　王惠　王彧》][482]、[《宋書・臧質 魯爽 沈攸之》][803]、[《宋書・臧質 魯爽 沈攸之》][804] | [JSON](16c_0og_lvl_A.json) |
| `AA` | 沈文和（攸之第三子） | [《南史・沈慶之　宗愨》][521] | [JSON](16c_0og_lvl_AA.json) |

</details>

<details><summary><code>175_99c_b41</code> 柔（王沈祖）（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 柔（王沈祖） | [《三國志・徐胡二王傳》][560] | [JSON](175_99c_b41.json) |
| `A` | 機（王沈父） | [《晉書・王沈 荀顗 荀勖 馮紞》][119] | [JSON](175_99c_b41_A.json) |
| `AA` | 王沈 | [《晉書・王沈 荀顗 荀勖 馮紞》][119] | [JSON](175_99c_b41_AA.json) |

</details>

<details><summary><code>1a3_b0c_e6d</code> 謝沖（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 謝沖 | [《南史・謝晦　謝裕　謝方明　謝靈運》][420] | [JSON](1a3_b0c_e6d.json) |
| `A` | 謝明慧 | [《晉書・謝尚 謝安》][195] | [JSON](1a3_b0c_e6d_A.json) |

</details>

<details><summary><code>1ay_9qe_u4h</code> 荀馗（5 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 荀馗 | [《晉書・王湛 荀崧 范汪 劉惔 張憑 韓伯》][187] | [JSON](1ay_9qe_u4h.json) |
| `A` | 荀序 | [《晉書・王沈 荀顗 荀勖 馮紞》][119]、[《晉書・王湛 荀崧 范汪 劉惔 張憑 韓伯》][187] | [JSON](1ay_9qe_u4h_A.json) |
| `AA` | 恆（荀序子） | [《晉書・王沈 荀顗 荀勖 馮紞》][119] | [JSON](1ay_9qe_u4h_AA.json) |
| `AAA` | 龍符（恆子） | [《晉書・王沈 荀顗 荀勖 馮紞》][119] | [JSON](1ay_9qe_u4h_AAA.json) |
| `B` | 荀廞 | [《晉書・王湛 荀崧 范汪 劉惔 張憑 韓伯》][187] | [JSON](1ay_9qe_u4h_B.json) |

</details>

<details><summary><code>1b1_d4d_bb8</code> 謝鐵（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 謝鐵 | [《南史・謝晦　謝裕　謝方明　謝靈運》][420] | [JSON](1b1_d4d_bb8.json) |
| `A` | 謝邈 | [《晉書・謝尚 謝安》][195] | [JSON](1b1_d4d_bb8_A.json) |

</details>

<details><summary><code>1dq_vh2_eru</code> 張華（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 張華 | [《晉書・忠義》][200] | [JSON](1dq_vh2_eru.json) |
| `*****A` | 張穆之（字思靜） | [《南史・后妃下》][405] | [JSON](1dq_vh2_eru_%2A%2A%2A%2A%2AA.json) |
| `*****AA` | 張尚柔（梁太祖獻皇后） | [《南史・后妃下》][405] | [JSON](1dq_vh2_eru_%2A%2A%2A%2A%2AAA.json) |

</details>

<details><summary><code>1ec_i30_u8n</code> 溫恭〔濟南太守〕（6 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 溫恭〔濟南太守〕 | [《新唐書・宰相世系二中》][872] | [JSON](1ec_i30_u8n.json) |
| `A` | 溫羨 | [《晉書・鄭袤 李胤 盧欽 華表 石鑒 溫羨》][146] | [JSON](1ec_i30_u8n_A.json) |
| `AA` | 溫允〔溫羨子〕 | [《晉書・鄭袤 李胤 盧欽 華表 石鑒 溫羨》][137]、[《晉書・鄭袤 李胤 盧欽 華表 石鑒 溫羨》][146] | [JSON](1ec_i30_u8n_AA.json) |
| `AB` | 溫祗 | [《晉書・鄭袤 李胤 盧欽 華表 石鑒 溫羨》][146] | [JSON](1ec_i30_u8n_AB.json) |
| `AC` | 溫裕〔字敬嗣〕 | [《晉書・鄭袤 李胤 盧欽 華表 石鑒 溫羨》][146] | [JSON](1ec_i30_u8n_AC.json) |
| `B` | 溫襜〔本傳憺〕 | [《新唐書・宰相世系二中》][872] | [JSON](1ec_i30_u8n_B.json) |

</details>

<details><summary><code>1ex_se1_yef</code> 張湯父（未名）（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 張湯父（未名） | [《漢書・張湯傳》][45]、[《史記・酷吏列傳》][670] | [JSON](1ex_se1_yef.json) |
| `A` | 張湯 | [《史記・酷吏列傳》][670] | [JSON](1ex_se1_yef_A.json) |
| `AA` | 張安世 | [《漢書・張湯傳》][45] | [JSON](1ex_se1_yef_AA.json) |

</details>

<details><summary><code>1g3_02y_oor</code> 太公望（5 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 太公望 | [《史記・齊太公世家》][580] | [JSON](1g3_02y_oor.json) |
| `A` | 丁公呂伋 | [《史記・齊太公世家》][580] | [JSON](1g3_02y_oor_A.json) |
| `AA` | 得（齊乙公） | [《史記・齊太公世家》][580] | [JSON](1g3_02y_oor_AA.json) |
| `AAA` | 慈母（齊癸公） | [《史記・齊太公世家》][580] | [JSON](1g3_02y_oor_AAA.json) |
| `AAAA` | 不辰（齊哀公） | [《史記・齊太公世家》][580] | [JSON](1g3_02y_oor_AAAA.json) |

</details>

<details><summary><code>1h3_vs7_t8h</code> 齊湣王（燕篇）（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 齊湣王（燕篇） | [《史記・燕召公世家》][582] | [JSON](1h3_vs7_t8h.json) |
| `A` | 襄王（齊湣王子） | [《史記・田敬仲完世家》][594] | [JSON](1h3_vs7_t8h_A.json) |
| `AA` | 齊王建 | [《史記・田敬仲完世家》][594] | [JSON](1h3_vs7_t8h_AA.json) |

</details>

<details><summary><code>1hf_1k0_bnj</code> 夷仲年（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 夷仲年 | [《史記・齊太公世家》][580]、[《史記・十二諸侯年表》][896] | [JSON](1hf_1k0_bnj.json) |
| `A` | 公孫無知 | [《史記・齊太公世家》][580] | [JSON](1hf_1k0_bnj_A.json) |

</details>

<details><summary><code>1kj_vhc_cx9</code> 上官桀（三王世家候選）（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 上官桀 | [《漢書・昭帝紀》][41] | [JSON](1kj_vhc_cx9.json) |
| `A` | 上官安 | [《漢書・昭帝紀》][41] | [JSON](1kj_vhc_cx9_A.json) |
| `AA` | 上官氏（孝昭皇后） | [《漢書・昭帝紀》][41] | [JSON](1kj_vhc_cx9_AA.json) |

</details>

<details><summary><code>1l4_2pq_e7w</code> 熊通（楚武王候選）（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 熊通 | [《史記・楚世家》][588] | [JSON](1l4_2pq_e7w.json) |
| `A` | 熊貲（楚文王） | [《史記・楚世家》][588] | [JSON](1l4_2pq_e7w_A.json) |
| `AA` | 熊艱（莊敖） | [《史記・楚世家》][588] | [JSON](1l4_2pq_e7w_AA.json) |

</details>

<details><summary><code>1pc_mnq_z0c</code> 懿公（燕文公後）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 懿公（燕文公後） | [《史記・燕召公世家》][582] | [JSON](1pc_mnq_z0c.json) |
| `A` | 惠公（燕懿公子） | [《史記・燕召公世家》][582] | [JSON](1pc_mnq_z0c_A.json) |

</details>

<details><summary><code>1tc_q18_x7v</code> 王彧（8 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 王彧 | [《南史・王誕　王華　王惠　王彧》][496] | [JSON](1tc_q18_x7v.json) |
| `A` | 王絢（字長素，王彧長子） | [《南史・王誕　王華　王惠　王彧》][494] | [JSON](1tc_q18_x7v_A.json) |
| `AA` | 王婼（王絢子） | [《宋書・謝莊 王景文》][817] | [JSON](1tc_q18_x7v_AA.json) |
| `B` | 王繢（字叔素，王彧子） | [《南史・王誕　王華　王惠　王彧》][483] | [JSON](1tc_q18_x7v_B.json) |
| `BA` | 王雋（王繢長子） | [《南史・王誕　王華　王惠　王彧》][483] | [JSON](1tc_q18_x7v_BA.json) |
| `BAA` | 王克（王雋子） | [《南史・王誕　王華　王惠　王彧》][483] | [JSON](1tc_q18_x7v_BAA.json) |
| `BB` | 王繢女（齊安陸王子敬妃） | [《南齊書・王奐 從弟繢 張沖》][364]、[《南史・王誕　王華　王惠　王彧》][483] | [JSON](1tc_q18_x7v_BB.json) |
| `C` | 王約（王繢弟） | [《南史・王誕　王華　王惠　王彧》][483] | [JSON](1tc_q18_x7v_C.json) |

</details>

<details><summary><code>1up_vyo_s9g</code> 徐榮祖（徐夤父）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 徐榮祖（徐夤父） | [《南史・江淹　任昉　王僧孺》][535] | [JSON](1up_vyo_s9g.json) |
| `A` | 徐夤（高平，徐榮祖子） | [《南史・江淹　任昉　王僧孺》][535] | [JSON](1up_vyo_s9g_A.json) |

</details>

<details><summary><code>1y5_eke_4gl</code> 陽慶（扁鵲倉公列傳候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 陽慶 | [《史記・扁鵲倉公列傳》][653] | [JSON](1y5_eke_4gl.json) |
| `A` | 殷（慶子） | [《史記・扁鵲倉公列傳》][653] | [JSON](1y5_eke_4gl_A.json) |

</details>

<details><summary><code>1za_blw_7lb</code> 伯魯（趙世家候選）（6 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 伯魯 | [《史記・趙世家》][591] | [JSON](1za_blw_7lb.json) |
| `A` | 周 | [《史記・趙世家》][591] | [JSON](1za_blw_7lb_A.json) |
| `AA` | 浣 | [《史記・趙世家》][591] | [JSON](1za_blw_7lb_AA.json) |
| `AAA` | 籍 | [《史記・趙世家》][591] | [JSON](1za_blw_7lb_AAA.json) |
| `AAAA` | 章 | [《史記・趙世家》][591] | [JSON](1za_blw_7lb_AAAA.json) |
| `AAAAA` | 種 | [《史記・趙世家》][591] | [JSON](1za_blw_7lb_AAAAA.json) |

</details>

<details><summary><code>23q_wcp_hny</code> 崔道固（7 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 崔道固 | [《魏書・燕鳳 許謙 張衮 崔玄伯 鄧淵》][848] | [JSON](23q_wcp_hny.json) |
| `A` | 崔景微 | [《宋書・薛安都 沈文秀 崔道固》][824]、[《宋書・薛安都 沈文秀 崔道固》][825] | [JSON](23q_wcp_hny_A.json) |
| `B` | 崔景徽 | [《魏書・燕鳳 許謙 張衮 崔玄伯 鄧淵》][848] | [JSON](23q_wcp_hny_B.json) |
| `BA` | 崔休纂 | [《北史・崔光 崔亮》][6]、[《魏書・燕鳳 許謙 張衮 崔玄伯 鄧淵》][848] | [JSON](23q_wcp_hny_BA.json) |
| `C` | 崔景業 | [《魏書・燕鳳 許謙 張衮 崔玄伯 鄧淵》][848] | [JSON](23q_wcp_hny_C.json) |
| `CA` | 崔休緒 | [《魏書・燕鳳 許謙 張衮 崔玄伯 鄧淵》][848] | [JSON](23q_wcp_hny_CA.json) |
| `D` | 崔景淵 | [《魏書・燕鳳 許謙 張衮 崔玄伯 鄧淵》][848] | [JSON](23q_wcp_hny_D.json) |

</details>

<details><summary><code>262_b8f_4ie</code> 裴朴之（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 裴朴之 | [《南齊書・皇后》][298]、[《南史・后妃上》][391] | [JSON](262_b8f_4ie.json) |
| `A` | 裴璣之 | [《南齊書・皇后》][298]、[《南史・后妃上》][391] | [JSON](262_b8f_4ie_A.json) |
| `AA` | 裴惠昭 | [《南齊書・高帝下》][281]、[《南齊書・皇后》][298]、[《南齊書・皇后》][300]、[《南齊書・皇后》][299]、[《南史・后妃上》][391] | [JSON](262_b8f_4ie_AA.json) |

</details>

<details><summary><code>27j_f4p_jwp</code> 李廣（7 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 李廣 | [《史記・李將軍列傳》][657] | [JSON](27j_f4p_jwp.json) |
| `A` | 李敢 | [《史記・李將軍列傳》][657] | [JSON](27j_f4p_jwp_A.json) |
| `AA` | 李敢女（未名） | [《史記・李將軍列傳》][657] | [JSON](27j_f4p_jwp_AA.json) |
| `AB` | 禹（李敢男） | [《史記・李將軍列傳》][657] | [JSON](27j_f4p_jwp_AB.json) |
| `B` | 當戸 | [《史記・李將軍列傳》][657] | [JSON](27j_f4p_jwp_B.json) |
| `BA` | 李陵 | [《史記・李將軍列傳》][657] | [JSON](27j_f4p_jwp_BA.json) |
| `C` | 椒 | [《史記・李將軍列傳》][657] | [JSON](27j_f4p_jwp_C.json) |

</details>

<details><summary><code>2a3_ci1_y4y</code> 元湛（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 元湛 | [《北史・道武七王 明元六王 太武五王》][1]、[《冊府元龜・宗室部·承襲第三》][7]、[《元湛墓誌・節錄》][34]、[《魏書・太武五王》][847] | [JSON](2a3_ci1_y4y.json) |
| `A` | 元法輪 | [《北史・道武七王 明元六王 太武五王》][1]、[《冊府元龜・宗室部·承襲第三》][7]、[《魏書・太武五王》][847] | [JSON](2a3_ci1_y4y_A.json) |

</details>

<details><summary><code>2bc_992_946</code> 謝靜（4 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 謝靜 | [《晉書・謝尚 謝安》][195] | [JSON](2bc_992_946.json) |
| `A` | 謝肅 | [《晉書・謝尚 謝安》][195] | [JSON](2bc_992_946_A.json) |
| `B` | 謝虔 | [《晉書・謝尚 謝安》][195] | [JSON](2bc_992_946_B.json) |
| `BA` | 謝靈佑 | [《晉書・謝尚 謝安》][195] | [JSON](2bc_992_946_BA.json) |

</details>

<details><summary><code>2c3_7e0_16b</code> 卞範之（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 卞範之 | [《晉書・叛臣二》][224] | [JSON](2c3_7e0_16b.json) |
| `A` | 卞範之女（拒婚對象，未名） | [《宋書・張茂度 庾登之 謝方明 江夷》][778] | [JSON](2c3_7e0_16b_A.json) |

</details>

<details><summary><code>2d3_fsd_1dh</code> 楚成王（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 楚成王 | [《史記・晉世家》][587] | [JSON](2d3_fsd_1dh.json) |
| `A` | 楚商臣 | [《史記・陳杞世家》][584] | [JSON](2d3_fsd_1dh_A.json) |

</details>

<details><summary><code>2d4_2ed_646</code> 席恭穆（安定焉氏人，鎮西司馬）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 席恭穆（安定焉氏人，鎮西司馬） | [《南齊書・王奐 從弟繢 張沖》][366] | [JSON](2d4_2ed_646.json) |
| `A` | 席謙（新蔡太守，席恭穆子） | [《南齊書・王奐 從弟繢 張沖》][366] | [JSON](2d4_2ed_646_A.json) |

</details>

<details><summary><code>2mj_6rl_6xs</code> 陳廢帝伯宗（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 陳廢帝伯宗 | [《陳書・本紀第四: 廢帝》][11] | [JSON](2mj_6rl_6xs.json) |
| `A` | 陳至澤（臨海嗣王） | [《陳書・皇后》][14]、[《南史・后妃下》][404] | [JSON](2mj_6rl_6xs_A.json) |

</details>

<details><summary><code>2n6_7xk_5ov</code> 江夏王義恭（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 江夏王義恭 | [《宋書・殷淳 張暢 何偃 江智淵》][785] | [JSON](2n6_7xk_5ov.json) |
| `A` | 王僧虔妻（江夏王女，未名） | [《南齊書・王僧虔 張緒》][330] | [JSON](2n6_7xk_5ov_A.json) |

</details>

<details><summary><code>2pg_br4_mcl</code> 王濛（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 王濛 | [《晉書・謝尚 謝安》][195] | [JSON](2pg_br4_mcl.json) |
| `A` | 王修 | [《晉書・謝尚 謝安》][195] | [JSON](2pg_br4_mcl_A.json) |

</details>

<details><summary><code>2v5_rhh_fd6</code> 檀韶（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 檀韶 | [《南齊書・王僧虔 張緒》][330] | [JSON](2v5_rhh_fd6.json) |
| `*A` | 檀珪 | [《南齊書・王僧虔 張緒》][330] | [JSON](2v5_rhh_fd6_%2AA.json) |

</details>

<details><summary><code>2v6_0g1_ve2</code> 衍（宋微仲）（12 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 衍（宋微仲） | [《史記・宋微子世家》][586] | [JSON](2v6_0g1_ve2.json) |
| `A` | 稽（宋公） | [《史記・宋微子世家》][586] | [JSON](2v6_0g1_ve2_A.json) |
| `AA` | 申（宋丁公） | [《史記・宋微子世家》][586] | [JSON](2v6_0g1_ve2_AA.json) |
| `AAA` | 共（宋湣公） | [《史記・宋微子世家》][586] | [JSON](2v6_0g1_ve2_AAA.json) |
| `AAAA` | 鮒祀（宋厲公） | [《史記・宋微子世家》][586] | [JSON](2v6_0g1_ve2_AAAA.json) |
| `AAAAA` | 舉（宋釐公） | [《史記・宋微子世家》][586] | [JSON](2v6_0g1_ve2_AAAAA.json) |
| `AAAAAA` | 覵（宋惠公） | [《史記・宋微子世家》][586] | [JSON](2v6_0g1_ve2_AAAAAA.json) |
| `AAAAAAA` | 哀公（宋惠公子） | [《史記・宋微子世家》][586] | [JSON](2v6_0g1_ve2_AAAAAAA.json) |
| `AAAAAAAA` | 戴公（宋哀公子） | [《史記・宋微子世家》][586] | [JSON](2v6_0g1_ve2_AAAAAAAA.json) |
| `AAAAAAAAA` | 司空（宋武公） | [《史記・宋微子世家》][586] | [JSON](2v6_0g1_ve2_AAAAAAAAA.json) |
| `AAAAAAAAAA` | 宋女（魯惠公夫人） | [《史記・宋微子世家》][586] | [JSON](2v6_0g1_ve2_AAAAAAAAAA.json) |
| `AAAAAAAAAB` | 力（宋宣公） | [《史記・宋微子世家》][586] | [JSON](2v6_0g1_ve2_AAAAAAAAAB.json) |

</details>

<details><summary><code>2we_3ll_c5i</code> 裴順宗（裴叔業父）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 裴順宗（裴叔業父） | [《魏書・裴叔業 夏侯道遷 李元護 席法友 王世弼 江悦之 淳于誕 李苗》][863] | [JSON](2we_3ll_c5i.json) |
| `A` | 裴叔業（河東聞喜人） | [《南齊書・王奐 從弟繢 張沖》][360]、[《南史・王誕　王華　王惠　王彧》][482]、[《魏書・裴叔業 夏侯道遷 李元護 席法友 王世弼 江悦之 淳于誕 李苗》][863] | [JSON](2we_3ll_c5i_A.json) |

</details>

<details><summary><code>2ya_f42_kcq</code> 荀昶（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 荀昶 | [《宋書・范泰 王准之 王韶之 荀伯子》][789] | [JSON](2ya_f42_kcq.json) |
| `A` | 荀萬秋 | [《宋書・范泰 王准之 王韶之 荀伯子》][789] | [JSON](2ya_f42_kcq_A.json) |

</details>

<details><summary><code>30f_353_0e8</code> 崔鴻（7 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 崔鴻 | [《魏書・崔光》][862] | [JSON](30f_353_0e8.json) |
| `A` | 崔子文 | [《崔鴻墓誌・節錄》][24] | [JSON](30f_353_0e8_A.json) |
| `B` | 崔子真 | [《崔鴻墓誌・節錄》][24] | [JSON](30f_353_0e8_B.json) |
| `C` | 崔子長 | [《崔鴻墓誌・節錄》][24] | [JSON](30f_353_0e8_C.json) |
| `D` | 崔子發 | [《崔鴻墓誌・節錄》][24] | [JSON](30f_353_0e8_D.json) |
| `E` | 崔子房 | [《崔鴻墓誌・節錄》][24] | [JSON](30f_353_0e8_E.json) |
| `F` | 崔元華 | [《崔鴻墓誌・節錄》][24] | [JSON](30f_353_0e8_F.json) |

</details>

<details><summary><code>30k_jzz_tpd</code> 邵（9 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 邵 | [《三國志・諸夏侯曹傳》][541] | [JSON](30k_jzz_tpd.json) |
| `A` | 曹真 | [《三國志・諸夏侯曹傳》][541] | [JSON](30k_jzz_tpd_A.json) |
| `AA` | 曹爽 | [《三國志・諸夏侯曹傳》][541] | [JSON](30k_jzz_tpd_AA.json) |
| `AB` | 曹羲 | [《三國志・諸夏侯曹傳》][541] | [JSON](30k_jzz_tpd_AB.json) |
| `AC` | 曹訓 | [《三國志・諸夏侯曹傳》][541] | [JSON](30k_jzz_tpd_AC.json) |
| `AD` | 曹則 | [《三國志・諸夏侯曹傳》][541] | [JSON](30k_jzz_tpd_AD.json) |
| `AE` | 曹彦 | [《三國志・諸夏侯曹傳》][541] | [JSON](30k_jzz_tpd_AE.json) |
| `AF` | 曹皚 | [《三國志・諸夏侯曹傳》][541] | [JSON](30k_jzz_tpd_AF.json) |
| `B` | 曹彬 | [《三國志・諸夏侯曹傳》][541] | [JSON](30k_jzz_tpd_B.json) |

</details>

<details><summary><code>315_3d4_416</code> 任旐（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 任旐 | [《三國志・徐胡二王傳》][560] | [JSON](315_3d4_416.json) |
| `A` | 任嘏 | [《三國志・徐胡二王傳》][560] | [JSON](315_3d4_416_A.json) |

</details>

<details><summary><code>318_d06_496</code> 黃祖（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 黃祖 | [《三國志・二荀賈傳》][542] | [JSON](318_d06_496.json) |
| `A` | 黃射 | [《三國志・二荀賈傳》][542] | [JSON](318_d06_496_A.json) |

</details>

<details><summary><code>326_faf_cd3</code> 王羲之（8 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 王羲之 | [《晉書・王羲之》][196] | [JSON](326_faf_cd3.json) |
| `*A` | 王靜之 | [《宋書・良吏》][826] | [JSON](326_faf_cd3_%2AA.json) |
| `*AA` | 王悅之（字少明，宋書作悅） | [《南史・王裕之　王鎮之　王韶之　王悅之　王准之》][504]、[《宋書・良吏》][826] | [JSON](326_faf_cd3_%2AAA.json) |
| `A` | 王玄之 | [《晉書・王羲之》][196]、[《晉書・王羲之》][197] | [JSON](326_faf_cd3_A.json) |
| `B` | 王徽之 | [《晉書・王羲之》][196] | [JSON](326_faf_cd3_B.json) |
| `BA` | 王楨之 | [《晉書・王羲之》][196] | [JSON](326_faf_cd3_BA.json) |
| `C` | 王操之 | [《晉書・王羲之》][196] | [JSON](326_faf_cd3_C.json) |
| `D` | 王肅之 | [《世說新語・排調》][734] | [JSON](326_faf_cd3_D.json) |

</details>

<details><summary><code>344_68f_98e</code> 郭嘉（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 郭嘉 | [《三國志・二荀賈傳》][543] | [JSON](344_68f_98e.json) |
| `A` | 郭奕（字伯益，郭嘉子） | [《三國志・徐胡二王傳》][560] | [JSON](344_68f_98e_A.json) |

</details>

<details><summary><code>37j_16p_7n8</code> 曹參（6 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 曹參 | [《史記・曹相國世家》][602] | [JSON](37j_16p_7n8.json) |
| `A` | 窋 | [《史記・曹相國世家》][602] | [JSON](37j_16p_7n8_A.json) |
| `AA` | 奇 | [《史記・曹相國世家》][602] | [JSON](37j_16p_7n8_AA.json) |
| `AAA` | 時 | [《史記・曹相國世家》][602] | [JSON](37j_16p_7n8_AAA.json) |
| `AAAA` | 襄 | [《史記・衛將軍驃騎列傳》][659] | [JSON](37j_16p_7n8_AAAA.json) |
| `AAAAA` | 宗 | [《史記・曹相國世家》][602] | [JSON](37j_16p_7n8_AAAAA.json) |

</details>

<details><summary><code>3b9_b07_bdb</code> 馮紞（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 馮紞 | [《晉書・王沈 荀顗 荀勖 馮紞》][119] | [JSON](3b9_b07_bdb.json) |
| `A` | 播（馮紞子） | [《晉書・王沈 荀顗 荀勖 馮紞》][119] | [JSON](3b9_b07_bdb_A.json) |
| `B` | 熊（馮紞子） | [《晉書・王沈 荀顗 荀勖 馮紞》][119] | [JSON](3b9_b07_bdb_B.json) |

</details>

<details><summary><code>3bh_k4m_fg4</code> 宋太祖義隆（6 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 宋太祖義隆 | [《宋書・王華 王曇首 殷景仁 沈演之》][792] | [JSON](3bh_k4m_fg4.json) |
| `A` | 東陽獻公主 | [《南史・后妃上》][402]、[《宋書・后妃》][759]、[《宋書・徐湛之 江湛 王僧綽》][801] | [JSON](3bh_k4m_fg4_A.json) |
| `B` | 劉英媛（臨川長公主） | [《南史・王誕　王華　王惠　王彧》][498]、[《宋書・后妃》][755] | [JSON](3bh_k4m_fg4_B.json) |
| `C` | 長城公主（宋文帝第五女，謝緯妻） | [《宋書・庾悅 王誕 謝景仁 袁湛 褚叔度》][776] | [JSON](3bh_k4m_fg4_C.json) |
| `D` | 琅邪貞長公主（宋文帝女，褚曖妻） | [《南史・褚裕之》][514]、[《宋書・庾悅 王誕 謝景仁 袁湛 褚叔度》][770] | [JSON](3bh_k4m_fg4_D.json) |
| `E` | 劉休祐（晉平剌王） | [《宋書・文九王》][802] | [JSON](3bh_k4m_fg4_E.json) |

</details>

<details><summary><code>3c9_d1d_870</code> 王謐（5 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 王謐 | [《晉書・王導》][169] | [JSON](3c9_d1d_870.json) |
| `*A` | 王履（王謐孫，王球兄子） | [《南史・王誕　王華　王惠　王彧》][490] | [JSON](3c9_d1d_870_%2AA.json) |
| `A` | 王瓘 | [《晉書・王導》][169] | [JSON](3c9_d1d_870_A.json) |
| `B` | 王球 | [《南史・王誕　王華　王惠　王彧》][490] | [JSON](3c9_d1d_870_B.json) |
| `C` | 王琇 | [《晉書・王導》][169] | [JSON](3c9_d1d_870_C.json) |

</details>

<details><summary><code>3ea_uzt_2n2</code> 何准（8 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 何准 | [《晉書・外戚》][207] | [JSON](3ea_uzt_2n2.json) |
| `A` | 何法倪 | [《晉書・后妃下》][109] | [JSON](3ea_uzt_2n2_A.json) |
| `B` | 何澄（字季玄，何准子） | [《晉書・外戚》][207] | [JSON](3ea_uzt_2n2_B.json) |
| `BA` | 何融（晉元熙大司農，何澄次子） | [《晉書・外戚》][207]、[《宋書・后妃》][753] | [JSON](3ea_uzt_2n2_BA.json) |
| `BA*A` | 何瑀（字稚玉，何融孫） | [《宋書・后妃》][753] | [JSON](3ea_uzt_2n2_BA%2AA.json) |
| `BB` | 何籍（何澄長子） | [《晉書・外戚》][207] | [JSON](3ea_uzt_2n2_BB.json) |
| `C` | 何放（何准子，繼何充） | [《晉書・外戚》][207] | [JSON](3ea_uzt_2n2_C.json) |
| `D` | 何惔（何准子） | [《晉書・外戚》][207] | [JSON](3ea_uzt_2n2_D.json) |

</details>

<details><summary><code>3jf_ce1_jy2</code> 昆莫父（未名）（大宛列傳候選）（5 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 昆莫父（未名） | [《史記・大宛列傳》][671] | [JSON](3jf_ce1_jy2.json) |
| `A` | 昆莫 | [《史記・大宛列傳》][671] | [JSON](3jf_ce1_jy2_A.json) |
| `AA` | 大祿 | [《史記・大宛列傳》][671] | [JSON](3jf_ce1_jy2_AA.json) |
| `AB` | 大祿兄（未名太子） | [《史記・大宛列傳》][671] | [JSON](3jf_ce1_jy2_AB.json) |
| `ABA` | 岑娶 | [《史記・大宛列傳》][671] | [JSON](3jf_ce1_jy2_ABA.json) |

</details>

<details><summary><code>3qs_nqa_ioa</code> 混〔靖父；武原令〕（12 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 混〔靖父；武原令〕 | [《宋書・武帝上》][745] | [JSON](3qs_nqa_ioa.json) |
| `A` | 靖〔翹父；東安太守〕 | [《宋書・武帝上》][745] | [JSON](3qs_nqa_ioa_A.json) |
| `AA` | 翹〔孝皇帝；高祖之父〕 | [《宋書・后妃》][754] | [JSON](3qs_nqa_ioa_AA.json) |
| `AAA` | 宋高祖裕 | [《魏書・崔浩》][851] | [JSON](3qs_nqa_ioa_AAA.json) |
| `AAAA` | 劉榮男（吳興長公主） | [《南史・王誕　王華　王惠　王彧》][476]、[《南史・王誕　王華　王惠　王彧》][475]、[《宋書・后妃》][755] | [JSON](3qs_nqa_ioa_AAAA.json) |
| `AAAB` | 宋新安公主（劉裕第五女） | [《南史・王誕　王華　王惠　王彧》][496] | [JSON](3qs_nqa_ioa_AAAB.json) |
| `AAB` | 道憐 | [《宋書・張茂度 庾登之 謝方明 江夷》][780] | [JSON](3qs_nqa_ioa_AAB.json) |
| `AABA` | 劉義融（桂陽恭侯） | [《南史・宋宗室及諸王上》][407]、[《宋書・宗室》][769] | [JSON](3qs_nqa_ioa_AABA.json) |
| `AABAA` | 劉覬（桂陽孝侯） | [《南史・宋宗室及諸王上》][407] | [JSON](3qs_nqa_ioa_AABAA.json) |
| `AABAB` | 劉襲（字茂德，臨澧忠侯） | [《南史・宋宗室及諸王上》][407] | [JSON](3qs_nqa_ioa_AABAB.json) |
| `AABABA` | 劉晃（宋宗室） | [《南史・宋宗室及諸王上》][407]、[《宋書・后妃》][756] | [JSON](3qs_nqa_ioa_AABABA.json) |
| `AAC` | 臨川王道規 | [《晉書・叛臣二》][224] | [JSON](3qs_nqa_ioa_AAC.json) |

</details>

<details><summary><code>3te_z66_d5a</code> 張敖（外戚世家候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 張敖 | [《史記・外戚世家》][597] | [JSON](3te_z66_d5a.json) |
| `A` | 孝惠皇后 | [《史記・外戚世家》][597] | [JSON](3te_z66_d5a_A.json) |

</details>

<details><summary><code>3tg_h3n_iou</code> 樂玄（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 樂玄 | [《南齊書・王琨 張岱 褚炫 何戢 王延之 阮韜》][326]、[《南史・王誕　王華　王惠　王彧》][485] | [JSON](3tg_h3n_iou.json) |
| `A` | 樂玄女〔王懌妻〕 | — | [JSON](3tg_h3n_iou_A.json) |

</details>

<details><summary><code>3tt_4ey_uti</code> 袁湛（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 袁湛 | [《晉書・謝尚 謝安》][195] | [JSON](3tt_4ey_uti.json) |
| `A` | 袁齊媯 | [《南史・后妃上》][402]、[《宋書・后妃》][759] | [JSON](3tt_4ey_uti_A.json) |

</details>

<details><summary><code>3tw_nq2_gyn</code> 霍去病（外戚世家候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 霍去病 | [《史記・衛將軍驃騎列傳》][659] | [JSON](3tw_nq2_gyn.json) |
| `A` | 嬗 | [《史記・衛將軍驃騎列傳》][659] | [JSON](3tw_nq2_gyn_A.json) |

</details>

<details><summary><code>3xx_gdy_or6</code> 裴〔周浚父〕等兩支（共同父未名；編輯接合）（15 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `A` | 裴〔周浚父〕 | [《晉書・周浚 成公簡 苟晞 華軼 劉喬》][162] | [JSON](3xx_gdy_or6_A.json) |
| `AA` | 周浚 | [《晉書・周浚 成公簡 苟晞 華軼 劉喬》][162] | [JSON](3xx_gdy_or6_AA.json) |
| `AAA` | 周顗 | [《晉書・劉隗 刁協 戴若思 周顗》][179] | [JSON](3xx_gdy_or6_AAA.json) |
| `AAAA` | 周閔 | [《晉書・劉隗 刁協 戴若思 周顗》][179] | [JSON](3xx_gdy_or6_AAAA.json) |
| `AAAB` | 周恬 | [《晉書・劉隗 刁協 戴若思 周顗》][179] | [JSON](3xx_gdy_or6_AAAB.json) |
| `AAAC` | 周頤 | [《晉書・劉隗 刁協 戴若思 周顗》][179] | [JSON](3xx_gdy_or6_AAAC.json) |
| `AAACA` | 周琳 | [《晉書・劉隗 刁協 戴若思 周顗》][179] | [JSON](3xx_gdy_or6_AAACA.json) |
| `AAACAA` | 周文 | [《晉書・劉隗 刁協 戴若思 周顗》][179] | [JSON](3xx_gdy_or6_AAACAA.json) |
| `AAB` | 周嵩 | [《晉書・周浚 成公簡 苟晞 華軼 劉喬》][162] | [JSON](3xx_gdy_or6_AAB.json) |
| `AABA` | 王應之嫂〔嵩之女，未名〕 | [《晉書・周浚 成公簡 苟晞 華軼 劉喬》][162] | [JSON](3xx_gdy_or6_AABA.json) |
| `AAC` | 周謨 | [《晉書・周浚 成公簡 苟晞 華軼 劉喬》][162] | [JSON](3xx_gdy_or6_AAC.json) |
| `B` | 蕤〔周馥父〕 | [《晉書・周浚 成公簡 苟晞 華軼 劉喬》][162] | [JSON](3xx_gdy_or6_B.json) |
| `BA` | 周馥 | [《晉書・周浚 成公簡 苟晞 華軼 劉喬》][162] | [JSON](3xx_gdy_or6_BA.json) |
| `BAA` | 密〔周馥子〕 | [《晉書・周浚 成公簡 苟晞 華軼 劉喬》][162] | [JSON](3xx_gdy_or6_BAA.json) |
| `BAB` | 周矯 | [《晉書・周浚 成公簡 苟晞 華軼 劉喬》][162] | [JSON](3xx_gdy_or6_BAB.json) |

</details>

<details><summary><code>408_ce3_5d8</code> 沈慶之（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 沈慶之 | [《南史・王弘》][445]、[《宋書・王僧達 顏竣》][806] | [JSON](408_ce3_5d8.json) |
| `A` | 沈文季 | [《南齊書・徐孝嗣 沈文季》][351]、[《南史・王曇首》][460] | [JSON](408_ce3_5d8_A.json) |

</details>

<details><summary><code>418_c91_b6b</code> 華廙（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 華廙 | [《晉書・鄭袤 李胤 盧欽 華表 石鑒 溫羨》][136] | [JSON](418_c91_b6b.json) |
| `A` | 華混〔字敬倫，裴注作昆〕 | [《晉書・鄭袤 李胤 盧欽 華表 石鑒 溫羨》][136] | [JSON](418_c91_b6b_A.json) |
| `AA` | 華陶〔鞏令〕 | [《晉書・鄭袤 李胤 盧欽 華表 石鑒 溫羨》][136] | [JSON](418_c91_b6b_AA.json) |

</details>

<details><summary><code>42z_cse_1ka</code> 熊良夫（楚宣王）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 熊良夫（楚宣王） | [《史記・楚世家》][588] | [JSON](42z_cse_1ka.json) |
| `A` | 熊商（楚威王） | [《史記・楚世家》][588] | [JSON](42z_cse_1ka_A.json) |

</details>

<details><summary><code>46a_tvp_dq9</code> 秦獻公（魏世家候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 秦獻公 | [《史記・魏世家》][592] | [JSON](46a_tvp_dq9.json) |
| `A` | 秦孝公 | [《史記・魏世家》][592] | [JSON](46a_tvp_dq9_A.json) |

</details>

<details><summary><code>47p_kjh_ez7</code> 齊太祖道成（4 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 齊太祖道成 | [《梁書・謝朏 弟子覽》][243] | [JSON](47p_kjh_ez7.json) |
| `A` | 臨海長公主（齊高帝女） | [《南史・王曇首》][454] | [JSON](47p_kjh_ez7_A.json) |
| `B` | 江夏王鋒 | [《南齊書・高祖十二王》][334] | [JSON](47p_kjh_ez7_B.json) |
| `C` | 蕭映（臨川獻王，字宣光） | [《南齊書・高祖十二王》][333] | [JSON](47p_kjh_ez7_C.json) |

</details>

<details><summary><code>49g_7az_e4i</code> 李斯（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 李斯 | [《史記・李斯列傳》][635] | [JSON](49g_7az_e4i.json) |
| `A` | 李由 | [《史記・李斯列傳》][635] | [JSON](49g_7az_e4i_A.json) |
| `B` | 李斯中子未名 | [《史記・李斯列傳》][635] | [JSON](49g_7az_e4i_B.json) |

</details>

<details><summary><code>4ag_yml_73x</code> 休（平原劉氏父）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 休（平原劉氏父） | [《崔混墓誌・節錄》][25] | [JSON](4ag_yml_73x.json) |
| `A` | 劉氏（崔敬友妻） | [《崔混墓誌・節錄》][25] | [JSON](4ag_yml_73x_A.json) |

</details>

<details><summary><code>4c2_19b_bf4</code> 沈充（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 沈充 | [《晉書・叛臣一》][223] | [JSON](4c2_19b_bf4.json) |
| `A` | 沈勁〔字世堅、沈充子〕 | [《晉書・忠義》][199]、[《晉書・叛臣一》][223] | [JSON](4c2_19b_bf4_A.json) |

</details>

<details><summary><code>4c2_763_efd</code> 謝喻（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 謝喻 | [《晉書・謝尚 謝安》][195] | [JSON](4c2_763_efd.json) |
| `A` | 謝暠 | [《晉書・謝尚 謝安》][195] | [JSON](4c2_763_efd_A.json) |

</details>

<details><summary><code>4ij_7ik_fgy</code> 謝鯤（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 謝鯤 | [《晉書・謝尚 謝安》][195] | [JSON](4ij_7ik_fgy.json) |
| `A` | 謝尚 | [《晉書・謝尚 謝安》][195] | [JSON](4ij_7ik_fgy_A.json) |

</details>

<details><summary><code>4qr_wrk_3vd</code> 庾琛（32 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 庾琛 | [《晉書・庾亮》][182] | [JSON](4qr_wrk_3vd.json) |
| `A` | 庾文君 | [《晉書・后妃下》][112]、[《晉書・庾亮》][182] | [JSON](4qr_wrk_3vd_A.json) |
| `B` | 庾亮 | [《晉書・庾亮》][182] | [JSON](4qr_wrk_3vd_B.json) |
| `BA` | 庾彬 | [《晉書・庾亮》][182] | [JSON](4qr_wrk_3vd_BA.json) |
| `BB` | 庾羲 | [《晉書・庾亮》][182] | [JSON](4qr_wrk_3vd_BB.json) |
| `BBA` | 庾准 | [《晉書・庾亮》][182] | [JSON](4qr_wrk_3vd_BBA.json) |
| `BBAA` | 庾悅 | [《晉書・庾亮》][182] | [JSON](4qr_wrk_3vd_BBAA.json) |
| `BBB` | 庾楷 | [《晉書・叛臣二》][224] | [JSON](4qr_wrk_3vd_BBB.json) |
| `BC` | 庾龢 | [《晉書・庾亮》][182] | [JSON](4qr_wrk_3vd_BC.json) |
| `BCA` | 庾恆 | [《晉書・庾亮》][182] | [JSON](4qr_wrk_3vd_BCA.json) |
| `C` | 庾懌 | [《晉書・庾亮》][181] | [JSON](4qr_wrk_3vd_C.json) |
| `CA` | 庾統 | [《晉書・庾亮》][181] | [JSON](4qr_wrk_3vd_CA.json) |
| `CAA` | 庾玄之 | [《晉書・庾亮》][181] | [JSON](4qr_wrk_3vd_CAA.json) |
| `D` | 庾冰 | [《晉書・庾亮》][181] | [JSON](4qr_wrk_3vd_D.json) |
| `DA` | 庾希 | [《晉書・庾亮》][181] | [JSON](4qr_wrk_3vd_DA.json) |
| `DAA` | 庾攸之 | [《晉書・庾亮》][181] | [JSON](4qr_wrk_3vd_DAA.json) |
| `DB` | 庾襲 | [《晉書・庾亮》][181] | [JSON](4qr_wrk_3vd_DB.json) |
| `DC` | 庾友 | [《晉書・庾亮》][181] | [JSON](4qr_wrk_3vd_DC.json) |
| `DCA` | 庾叔宣 | [《晉書・庾亮》][181] | [JSON](4qr_wrk_3vd_DCA.json) |
| `DD` | 庾蘊 | [《晉書・庾亮》][181] | [JSON](4qr_wrk_3vd_DD.json) |
| `DDA` | 庾廓之 | [《晉書・庾亮》][181] | [JSON](4qr_wrk_3vd_DDA.json) |
| `DDB` | 庾廓（宋書原稱） | [《宋書・張茂度 庾登之 謝方明 江夷》][779] | [JSON](4qr_wrk_3vd_DDB.json) |
| `DDBA` | 庾登之 | [《宋書・張茂度 庾登之 謝方明 江夷》][779] | [JSON](4qr_wrk_3vd_DDBA.json) |
| `DDBAA` | 庾沖遠 | [《宋書・后妃》][755]、[《宋書・張茂度 庾登之 謝方明 江夷》][779] | [JSON](4qr_wrk_3vd_DDBAA.json) |
| `DDBB` | 庾炳之 | [《宋書・張茂度 庾登之 謝方明 江夷》][779] | [JSON](4qr_wrk_3vd_DDBB.json) |
| `DDBBA` | 庾季遠 | [《宋書・張茂度 庾登之 謝方明 江夷》][779] | [JSON](4qr_wrk_3vd_DDBBA.json) |
| `DDBBB` | 庾弘遠 | [《宋書・張茂度 庾登之 謝方明 江夷》][779] | [JSON](4qr_wrk_3vd_DDBBB.json) |
| `DE` | 庾倩 | [《晉書・庾亮》][181] | [JSON](4qr_wrk_3vd_DE.json) |
| `DF` | 庾邈 | [《晉書・庾亮》][181] | [JSON](4qr_wrk_3vd_DF.json) |
| `DG` | 庾柔 | [《晉書・庾亮》][181] | [JSON](4qr_wrk_3vd_DG.json) |
| `E` | 庾條 | [《晉書・庾亮》][181] | [JSON](4qr_wrk_3vd_E.json) |
| `F` | 庾翼 | [《晉書・謝尚 謝安》][195] | [JSON](4qr_wrk_3vd_F.json) |

</details>

<details><summary><code>4w5_b4e_vf5</code> 王翁孺（14 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 王翁孺 | [《漢書・元后傳》][50] | [JSON](4w5_b4e_vf5.json) |
| `A` | 王禁 | [《漢書・元后傳》][50] | [JSON](4w5_b4e_vf5_A.json) |
| `AA` | 君俠 | [《漢書・元后傳》][50] | [JSON](4w5_b4e_vf5_AA.json) |
| `AB` | 政君 | [《漢書・元后傳》][50] | [JSON](4w5_b4e_vf5_AB.json) |
| `AC` | 君力 | [《漢書・元后傳》][50] | [JSON](4w5_b4e_vf5_AC.json) |
| `AD` | 君弟 | [《漢書・元后傳》][50] | [JSON](4w5_b4e_vf5_AD.json) |
| `AE` | 鳳 | [《漢書・元后傳》][50] | [JSON](4w5_b4e_vf5_AE.json) |
| `AF` | 曼 | [《漢書・元后傳》][50] | [JSON](4w5_b4e_vf5_AF.json) |
| `AG` | 譚 | [《漢書・元后傳》][50] | [JSON](4w5_b4e_vf5_AG.json) |
| `AH` | 崇 | [《漢書・元后傳》][50] | [JSON](4w5_b4e_vf5_AH.json) |
| `AI` | 商 | [《漢書・元后傳》][50] | [JSON](4w5_b4e_vf5_AI.json) |
| `AJ` | 立 | [《漢書・元后傳》][50] | [JSON](4w5_b4e_vf5_AJ.json) |
| `AK` | 根 | [《漢書・元后傳》][50] | [JSON](4w5_b4e_vf5_AK.json) |
| `AL` | 逢時 | [《漢書・元后傳》][50] | [JSON](4w5_b4e_vf5_AL.json) |

</details>

<details><summary><code>4wv_6og_mwb</code> 申無宇（芋尹）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 申無宇（芋尹） | [《史記・楚世家》][588] | [JSON](4wv_6og_mwb.json) |
| `A` | 申亥（收葬楚靈王者） | [《史記・楚世家》][588] | [JSON](4wv_6og_mwb_A.json) |

</details>

<details><summary><code>4xe_ms4_pr9</code> 夢者（曹亡敘事未名）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 夢者（曹亡敘事未名） | [《史記・管蔡世家》][583] | [JSON](4xe_ms4_pr9.json) |
| `A` | 夢者子（未名） | [《史記・管蔡世家》][583] | [JSON](4xe_ms4_pr9_A.json) |

</details>

<details><summary><code>4xl_1hw_6cg</code> 孫宏（許邁妻父）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 孫宏（許邁妻父） | [《真誥・卷二十》][874] | [JSON](4xl_1hw_6cg.json) |
| `A` | 孫氏（許邁妻） | [《晉書・王羲之》][196] | [JSON](4xl_1hw_6cg_A.json) |

</details>

<details><summary><code>4yg_ete_09a</code> 柴武（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 柴武 | [《史記・韓信盧綰列傳》][641] | [JSON](4yg_ete_09a.json) |
| `A` | 奇（柴武子） | [《史記・淮南衡山列傳》][666] | [JSON](4yg_ete_09a_A.json) |

</details>

<details><summary><code>505_n4y_p39</code> 秦開（匈奴列傳候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 秦開 | [《史記・匈奴列傳》][658] | [JSON](505_n4y_p39.json) |
| `*A` | 秦舞陽 | [《史記・刺客列傳》][634] | [JSON](505_n4y_p39_%2AA.json) |

</details>

<details><summary><code>50h_gqe_1p1</code> 具（魯獻公）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 具（魯獻公） | [《史記・魯周公世家》][581] | [JSON](50h_gqe_1p1.json) |
| `A` | 濞（魯真公） | [《史記・魯周公世家》][581]、[《史記・三代世表》][895] | [JSON](50h_gqe_1p1_A.json) |

</details>

<details><summary><code>573_104_0c1</code> 李崇（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 李崇 | [《魏書・刁雍 王慧龍 韓延之 袁式》][852] | [JSON](573_104_0c1.json) |
| `A` | 李世哲 | [《魏書・刁雍 王慧龍 韓延之 袁式》][852] | [JSON](573_104_0c1_A.json) |
| `B` | 青肫〔李崇子〕 | [《魏書・刁雍 王慧龍 韓延之 袁式》][852] | [JSON](573_104_0c1_B.json) |

</details>

<details><summary><code>591_360_8ca</code> 樂廣（7 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 樂廣 | [《晉書・山濤 王戎 郭舒 樂廣》][124] | [JSON](591_360_8ca.json) |
| `*****A` | 樂藹（字蔚遠） | [《梁書・宗夬 劉坦 樂藹》][245] | [JSON](591_360_8ca_%2A%2A%2A%2A%2AA.json) |
| `A` | 樂凱〔字弘緒〕 | [《晉書・山濤 王戎 郭舒 樂廣》][124] | [JSON](591_360_8ca_A.json) |
| `B` | 樂肇〔字弘茂〕 | [《晉書・山濤 王戎 郭舒 樂廣》][124] | [JSON](591_360_8ca_B.json) |
| `C` | 樂謨〔字弘範〕 | [《晉書・山濤 王戎 郭舒 樂廣》][124] | [JSON](591_360_8ca_C.json) |
| `D` | 樂廣女〔成都王妃〕 | [《晉書・山濤 王戎 郭舒 樂廣》][124]、[《世說新語・言語》][686]、[《資治通鑑・晉紀七》][880] | [JSON](591_360_8ca_D.json) |
| `E` | 樂廣女〔衛玠妻〕 | [《晉書・衞瓘 張華》][115]、[《世說新語・言語》][686] | [JSON](591_360_8ca_E.json) |

</details>

<details><summary><code>59d_72d_924</code> 王雅（4 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 王雅 | [《晉書・王湛 荀崧 范汪 劉惔 張憑 韓伯》][185] | [JSON](59d_72d_924.json) |
| `A` | 王准之（東海，王雅子） | [《梁書・王僧孺 張率 劉孝綽 王筠》][264]、[《南史・江淹　任昉　王僧孺》][534]、[《南史・江淹　任昉　王僧孺》][535] | [JSON](59d_72d_924_A.json) |
| `AA` | 王延年（王僧孺父） | [《南史・江淹　任昉　王僧孺》][534]、[《南史・江淹　任昉　王僧孺》][535] | [JSON](59d_72d_924_AA.json) |
| `AAA` | 王僧孺 | [《南史・江淹　任昉　王僧孺》][535] | [JSON](59d_72d_924_AAA.json) |

</details>

<details><summary><code>5bo_dxd_69k</code> 冉雍父（弟子列傳候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 冉雍父 | [《史記・仲尼弟子列傳》][615] | [JSON](5bo_dxd_69k.json) |
| `A` | 冉雍 | [《史記・仲尼弟子列傳》][615] | [JSON](5bo_dxd_69k_A.json) |

</details>

<details><summary><code>5dd_l1c_6g8</code> 衛青（5 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 衛青 | [《史記・衛將軍驃騎列傳》][659] | [JSON](5dd_l1c_6g8.json) |
| `A` | 衛青子陰安侯 | [《史記・衛將軍驃騎列傳》][659] | [JSON](5dd_l1c_6g8_A.json) |
| `B` | 衛青子發干侯 | [《史記・衛將軍驃騎列傳》][659] | [JSON](5dd_l1c_6g8_B.json) |
| `C` | 衛青子宜春侯（來源候選；預設不接父系） | [《史記・外戚世家》][597] | [JSON](5dd_l1c_6g8_C.json) |
| `D` | 衛伉 | [《史記・衛將軍驃騎列傳》][659] | [JSON](5dd_l1c_6g8_D.json) |

</details>

<details><summary><code>5dm_e40_rqh</code> 古公亶父（28 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 古公亶父 | [《史記・周本紀》][570] | [JSON](5dm_e40_rqh.json) |
| `A` | 仲雍 | [《史記・吳太伯世家》][579] | [JSON](5dm_e40_rqh_A.json) |
| `AA` | 季簡 | [《史記・吳太伯世家》][579] | [JSON](5dm_e40_rqh_AA.json) |
| `AAA` | 叔達 | [《史記・吳太伯世家》][579] | [JSON](5dm_e40_rqh_AAA.json) |
| `AAAA` | 周章（吳君） | [《史記・吳太伯世家》][579] | [JSON](5dm_e40_rqh_AAAA.json) |
| `AAAAA` | 熊遂 | [《史記・吳太伯世家》][579] | [JSON](5dm_e40_rqh_AAAAA.json) |
| `AAAAAA` | 柯相 | [《史記・吳太伯世家》][579] | [JSON](5dm_e40_rqh_AAAAAA.json) |
| `AAAAAAA` | 彊鳩夷 | [《史記・吳太伯世家》][579] | [JSON](5dm_e40_rqh_AAAAAAA.json) |
| `AAAAAAAA` | 餘橋疑吾 | [《史記・吳太伯世家》][579] | [JSON](5dm_e40_rqh_AAAAAAAA.json) |
| `AAAAAAAAA` | 柯盧 | [《史記・吳太伯世家》][579] | [JSON](5dm_e40_rqh_AAAAAAAAA.json) |
| `AAAAAAAAAA` | 周繇 | [《史記・吳太伯世家》][579] | [JSON](5dm_e40_rqh_AAAAAAAAAA.json) |
| `AAAAAAAAAAA` | 屈羽 | [《史記・吳太伯世家》][579] | [JSON](5dm_e40_rqh_AAAAAAAAAAA.json) |
| `AAAAAAAAAAAA` | 夷吾（吳君） | [《史記・吳太伯世家》][579] | [JSON](5dm_e40_rqh_AAAAAAAAAAAA.json) |
| `AAAAAAAAAAAAA` | 禽處 | [《史記・吳太伯世家》][579] | [JSON](5dm_e40_rqh_AAAAAAAAAAAAA.json) |
| `AAAAAAAAAAAAAA` | 轉（吳君） | [《史記・吳太伯世家》][579] | [JSON](5dm_e40_rqh_AAAAAAAAAAAAAA.json) |
| `AAAAAAAAAAAAAAA` | 頗髙 | [《史記・吳太伯世家》][579] | [JSON](5dm_e40_rqh_AAAAAAAAAAAAAAA.json) |
| `AAAAAAAAAAAAAAAA` | 句卑 | [《史記・吳太伯世家》][579] | [JSON](5dm_e40_rqh_AAAAAAAAAAAAAAAA.json) |
| `AAAAAAAAAAAAAAAAA` | 去齊 | [《史記・吳太伯世家》][579] | [JSON](5dm_e40_rqh_AAAAAAAAAAAAAAAAA.json) |
| `AAAAAAAAAAAAAAAAAA` | 壽夢 | [《史記・吳太伯世家》][579] | [JSON](5dm_e40_rqh_AAAAAAAAAAAAAAAAAA.json) |
| `AAAAAAAAAAAAAAAAAAA` | 諸樊 | [《史記・吳太伯世家》][579] | [JSON](5dm_e40_rqh_AAAAAAAAAAAAAAAAAAA.json) |
| `AAAAAAAAAAAAAAAAAAAA` | 闔閭 | [《史記・吳太伯世家》][579] | [JSON](5dm_e40_rqh_AAAAAAAAAAAAAAAAAAAA.json) |
| `AAAAAAAAAAAAAAAAAAAAA` | 夫差 | [《史記・越王勾踐世家》][589] | [JSON](5dm_e40_rqh_AAAAAAAAAAAAAAAAAAAAA.json) |
| `AAAAAAAAAAAAAAAAAAB` | 餘祭 | [《史記・吳太伯世家》][579] | [JSON](5dm_e40_rqh_AAAAAAAAAAAAAAAAAAB.json) |
| `AAAAAAAAAAAAAAAAAAC` | 餘眛 | [《史記・吳太伯世家》][579] | [JSON](5dm_e40_rqh_AAAAAAAAAAAAAAAAAAC.json) |
| `AAAAAAAAAAAAAAAAAACA` | 僚（吳王） | [《史記・吳太伯世家》][579] | [JSON](5dm_e40_rqh_AAAAAAAAAAAAAAAAAACA.json) |
| `AAAAAAAAAAAAAAAAAAD` | 季札 | [《史記・吳太伯世家》][579] | [JSON](5dm_e40_rqh_AAAAAAAAAAAAAAAAAAD.json) |
| `B` | 太伯 | [《史記・吳太伯世家》][579] | [JSON](5dm_e40_rqh_B.json) |
| `C` | 虞仲 | [《史記・周本紀》][570] | [JSON](5dm_e40_rqh_C.json) |

</details>

<details><summary><code>5if_pf6_zos</code> 郭解父（未名）（游俠列傳候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 郭解父（未名） | [《史記・游俠列傳》][672] | [JSON](5if_pf6_zos.json) |
| `A` | 郭解 | [《史記・游俠列傳》][672] | [JSON](5if_pf6_zos_A.json) |

</details>

<details><summary><code>5is_zik_jbp</code> 劉弘〔荊州刺史〕（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 劉弘〔荊州刺史〕 | [《晉書・劉弘 陶侃》][170] | [JSON](5is_zik_jbp.json) |
| `A` | 劉璠〔劉弘子〕 | [《晉書・山濤 王戎 郭舒 樂廣》][123]、[《晉書・劉弘 陶侃》][170] | [JSON](5is_zik_jbp_A.json) |

</details>

<details><summary><code>5jc_z9b_i2n</code> 柳卓（7 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 柳卓 | [《宋書・柳元景 顏師伯 沈慶之》][810] | [JSON](5jc_z9b_i2n.json) |
| `A` | 柳恬 | [《宋書・柳元景 顏師伯 沈慶之》][810] | [JSON](5jc_z9b_i2n_A.json) |
| `AA` | 柳憑 | [《南齊書・柳世隆 張瑰》][309]、[《宋書・柳元景 顏師伯 沈慶之》][810] | [JSON](5jc_z9b_i2n_AA.json) |
| `AAA` | 柳叔宗 | [《南齊書・柳世隆 張瑰》][309] | [JSON](5jc_z9b_i2n_AAA.json) |
| `AAAA` | 柳世隆 | [《南齊書・柳世隆 張瑰》][309] | [JSON](5jc_z9b_i2n_AAAA.json) |
| `AAB` | 柳元景 | [《宋書・朱脩之 宗愨 王玄謨》][808] | [JSON](5jc_z9b_i2n_AAB.json) |
| `AAC` | 柳僧景（柳元景弟） | [《宋書・朱脩之 宗愨 王玄謨》][808] | [JSON](5jc_z9b_i2n_AAC.json) |

</details>

<details><summary><code>5km_89r_9jr</code> 元君（衛嗣君弟）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 元君（衛嗣君弟） | [《史記・衛康叔世家》][585] | [JSON](5km_89r_9jr.json) |
| `A` | 衛君角 | [《史記・衛康叔世家》][585] | [JSON](5km_89r_9jr_A.json) |

</details>

<details><summary><code>5pw_05i_uhv</code> 平（本文燕昭王）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 平（本文燕昭王） | [《史記・樂毅列傳》][628] | [JSON](5pw_05i_uhv.json) |
| `A` | 惠王（燕昭王子） | [《史記・樂毅列傳》][628] | [JSON](5pw_05i_uhv_A.json) |

</details>

<details><summary><code>5ql_hfz_086</code> 房叔安（字子仁）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 房叔安（字子仁） | [《南史・王鎮惡　朱齡石　毛脩之　傅弘之　朱脩之　王玄謨》][410]、[《南史・王鎮惡　朱齡石　毛脩之　傅弘之　朱脩之　王玄謨》][412] | [JSON](5ql_hfz_086.json) |
| `A` | 房長瑜（房叔安子） | [《南史・王鎮惡　朱齡石　毛脩之　傅弘之　朱脩之　王玄謨》][408]、[《南史・王鎮惡　朱齡石　毛脩之　傅弘之　朱脩之　王玄謨》][409] | [JSON](5ql_hfz_086_A.json) |

</details>

<details><summary><code>5we_446_pbb</code> 荀永（荀伯玉祖）（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 荀永（荀伯玉祖） | [《南齊書・江謐 荀伯玉》][322] | [JSON](5we_446_pbb.json) |
| `A` | 荀闡之（荀伯玉父） | [《南齊書・江謐 荀伯玉》][322] | [JSON](5we_446_pbb_A.json) |
| `AA` | 荀伯玉（字弄璋） | [《南齊書・江謐 荀伯玉》][322] | [JSON](5we_446_pbb_AA.json) |

</details>

<details><summary><code>5xt_rg8_7zs</code> 項燕（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 項燕 | [《史記・秦始皇本紀》][572]、[《史記・六國年表》][897] | [JSON](5xt_rg8_7zs.json) |
| `A` | 項梁 | [《史記・項羽本紀》][573] | [JSON](5xt_rg8_7zs_A.json) |

</details>

<details><summary><code>603_131_11e</code> 楊駿（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 楊駿 | [《晉書・汝南王亮 楚王瑋 趙王倫 齊王冏 長沙王乂 成都王潁 河間王顒 東海王越》][160] | [JSON](603_131_11e.json) |
| `A` | 楊芷〔武悼楊皇后〕 | [《晉書・后妃上》][105] | [JSON](603_131_11e_A.json) |

</details>

<details><summary><code>62o_3do_q72</code> 游幼（游明根父）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 游幼（游明根父） | [《魏書・游明根 劉芳》][854] | [JSON](62o_3do_q72.json) |
| `A` | 游明根（字志遠） | [《魏書・游明根 劉芳》][854] | [JSON](62o_3do_q72_A.json) |

</details>

<details><summary><code>684_eaa_511</code> 謝景仁（5 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 謝景仁 | [《宋書・庾悅 王誕 謝景仁 袁湛 褚叔度》][775] | [JSON](684_eaa_511.json) |
| `A` | 謝恂 | [《南史・謝晦　謝裕　謝方明　謝靈運》][433] | [JSON](684_eaa_511_A.json) |
| `AA` | 謝孺子 | [《南史・謝晦　謝裕　謝方明　謝靈運》][433] | [JSON](684_eaa_511_AA.json) |
| `AAA` | 謝璟 | [《梁書・文學下》][277]、[《梁書・文學下》][276] | [JSON](684_eaa_511_AAA.json) |
| `AAAA` | 謝微 | [《梁書・文學下》][277]、[《梁書・文學下》][276] | [JSON](684_eaa_511_AAAA.json) |

</details>

<details><summary><code>696_456_df6</code> 荀曇（6 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 荀曇 | [《三國志・二荀賈傳》][543] | [JSON](696_456_df6.json) |
| `A` | 荀彞 | [《三國志・二荀賈傳》][543] | [JSON](696_456_df6_A.json) |
| `AA` | 荀攸 | [《三國志・二荀賈傳》][543] | [JSON](696_456_df6_AA.json) |
| `AA*A` | 荀彪 | [《三國志・二荀賈傳》][543] | [JSON](696_456_df6_AA%2AA.json) |
| `AAA` | 荀緝 | [《三國志・二荀賈傳》][543] | [JSON](696_456_df6_AAA.json) |
| `AAB` | 荀適 | [《三國志・二荀賈傳》][543] | [JSON](696_456_df6_AAB.json) |

</details>

<details><summary><code>69x_se2_859</code> 邴吉（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 邴吉 | [《史記・張丞相列傳》][644] | [JSON](69x_se2_859.json) |
| `A` | 邴顯 | [《史記・張丞相列傳》][644] | [JSON](69x_se2_859_A.json) |

</details>

<details><summary><code>6bn_yfc_lzi</code> 田叔（梁孝王世家候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 田叔 | [《史記・田叔列傳》][652] | [JSON](6bn_yfc_lzi.json) |
| `A` | 田仁 | [《史記・田叔列傳》][652] | [JSON](6bn_yfc_lzi_A.json) |

</details>

<details><summary><code>6d6_eg1_o3a</code> 王仲（外戚世家候選）（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 王仲 | [《史記・外戚世家》][597] | [JSON](6d6_eg1_o3a.json) |
| `A` | 王太后 | [《史記・外戚世家》][597] | [JSON](6d6_eg1_o3a_A.json) |
| `B` | 王信 | [《史記・絳侯周勃世家》][605] | [JSON](6d6_eg1_o3a_B.json) |

</details>

<details><summary><code>6di_ywz_ju4</code> 莊伯（晉曲沃弒君記事）（13 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 莊伯（晉曲沃弒君記事） | [《史記・晉世家》][587] | [JSON](6di_ywz_ju4.json) |
| `A` | 稱（曲沃／晉武公） | [《史記・晉世家》][587] | [JSON](6di_ywz_ju4_A.json) |
| `AA` | 晉獻公 | [《史記・晉世家》][587] | [JSON](6di_ywz_ju4_AA.json) |
| `AAA` | 晉文公 | [《史記・晉世家》][587] | [JSON](6di_ywz_ju4_AAA.json) |
| `AAAA` | 伯鯈（重耳子） | [《史記・晉世家》][587] | [JSON](6di_ywz_ju4_AAAA.json) |
| `AAAB` | 叔劉（重耳子） | [《史記・晉世家》][587] | [JSON](6di_ywz_ju4_AAAB.json) |
| `AAAC` | 黑臀（晉成公） | [《史記・晉世家》][587] | [JSON](6di_ywz_ju4_AAAC.json) |
| `AAAD` | 晉襄公 | [《史記・晉世家》][587] | [JSON](6di_ywz_ju4_AAAD.json) |
| `AAADA` | 捷（晉襄公少子桓叔） | [《史記・晉世家》][587] | [JSON](6di_ywz_ju4_AAADA.json) |
| `AAADAA` | 談（惠伯） | [《史記・晉世家》][587] | [JSON](6di_ywz_ju4_AAADAA.json) |
| `AAADAAA` | 晉悼公 | [《史記・晉世家》][587] | [JSON](6di_ywz_ju4_AAADAAA.json) |
| `AAB` | 申生 | [《史記・晉世家》][587] | [JSON](6di_ywz_ju4_AAB.json) |
| `AAC` | 奚齊 | [《史記・晉世家》][587] | [JSON](6di_ywz_ju4_AAC.json) |

</details>

<details><summary><code>6f6_d1e_11a</code> 道素（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 道素 | [《晉書・王沈 荀顗 荀勖 馮紞》][119] | [JSON](6f6_d1e_11a.json) |
| `A` | 崇之 | [《晉書・王沈 荀顗 荀勖 馮紞》][119] | [JSON](6f6_d1e_11a_A.json) |

</details>

<details><summary><code>6fg_r6l_5a5</code> 嵇康（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 嵇康 | [《晉書・忠義》][200] | [JSON](6fg_r6l_5a5.json) |
| `A` | 嵇紹 | [《晉書・忠義》][200] | [JSON](6fg_r6l_5a5_A.json) |
| `AA` | 嵇軫 | [《晉書・忠義》][200] | [JSON](6fg_r6l_5a5_AA.json) |

</details>

<details><summary><code>6fs_tis_zoa</code> 褚湛之（字休玄，褚淵、褚澄父）（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 褚湛之（字休玄，褚淵、褚澄父） | [《南史・褚裕之》][515]、[《宋書・庾悅 王誕 謝景仁 袁湛 褚叔度》][771] | [JSON](6fs_tis_zoa.json) |
| `A` | 褚澄（褚湛之子，吳郡太守） | [《南史・后妃上》][381]、[《南史・后妃上》][382]、[《南史・王誕　王華　王惠　王彧》][497] | [JSON](6fs_tis_zoa_A.json) |
| `AA` | 褚令璩（齊東昏侯皇后） | [《南齊書・皇后》][292]、[《南齊書・皇后》][291]、[《南史・后妃上》][381]、[《南史・后妃上》][382] | [JSON](6fs_tis_zoa_AA.json) |

</details>

<details><summary><code>6ks_x4x_dbf</code> 臧荼（外戚世家候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 臧荼 | [《史記・外戚世家》][597] | [JSON](6ks_x4x_dbf.json) |
| `*A` | 臧兒 | [《史記・外戚世家》][597] | [JSON](6ks_x4x_dbf_%2AA.json) |

</details>

<details><summary><code>6lr_zci_i0j</code> 郗鑒（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 郗鑒 | [《晉書・溫嶠 郗鑒》][173] | [JSON](6lr_zci_i0j.json) |
| `A` | 郗璿 | [《世說新語・雅量》][702] | [JSON](6lr_zci_i0j_A.json) |

</details>

<details><summary><code>6oy_t19_ywe</code> 秦惠王（蘇秦列傳候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 秦惠王 | [《史記・蘇秦列傳》][617] | [JSON](6oy_t19_ywe.json) |
| `A` | 秦惠王女 | [《史記・蘇秦列傳》][617] | [JSON](6oy_t19_ywe_A.json) |

</details>

<details><summary><code>6v8_pk9_7k5</code> 溫嶠（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 溫嶠 | [《晉書・溫嶠 郗鑒》][171] | [JSON](6v8_pk9_7k5.json) |
| `A` | 溫放之 | [《晉書・溫嶠 郗鑒》][171] | [JSON](6v8_pk9_7k5_A.json) |
| `B` | 溫式之 | [《溫嶠墓誌・節錄》][31] | [JSON](6v8_pk9_7k5_B.json) |

</details>

<details><summary><code>6wx_fr3_b2e</code> 滿（陳胡公）（8 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 滿（陳胡公） | [《史記・陳杞世家》][584] | [JSON](6wx_fr3_b2e.json) |
| `A` | 犀侯（陳申公） | [《史記・陳杞世家》][584] | [JSON](6wx_fr3_b2e_A.json) |
| `AA` | 突（陳孝公） | [《史記・陳杞世家》][584] | [JSON](6wx_fr3_b2e_AA.json) |
| `AAA` | 圉戎（陳慎公） | [《史記・陳杞世家》][584] | [JSON](6wx_fr3_b2e_AAA.json) |
| `AAAA` | 寧（陳幽公） | [《史記・陳杞世家》][584] | [JSON](6wx_fr3_b2e_AAAA.json) |
| `AAAAA` | 孝（陳釐公） | [《史記・陳杞世家》][584] | [JSON](6wx_fr3_b2e_AAAAA.json) |
| `AAAAAA` | 靈（陳武公） | [《史記・陳杞世家》][584] | [JSON](6wx_fr3_b2e_AAAAAA.json) |
| `AAAAAAA` | 說（陳夷公） | [《史記・陳杞世家》][584] | [JSON](6wx_fr3_b2e_AAAAAAA.json) |

</details>

<details><summary><code>719_b25_cc3</code> 庾深之（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 庾深之 | [《南齊書・虞玩之 劉休 沈沖 庾杲之 王諶》][332] | [JSON](719_b25_cc3.json) |
| `A` | 庾粲 | [《南齊書・虞玩之 劉休 沈沖 庾杲之 王諶》][332] | [JSON](719_b25_cc3_A.json) |
| `AA` | 庾杲之 | [《南齊書・虞玩之 劉休 沈沖 庾杲之 王諶》][332] | [JSON](719_b25_cc3_AA.json) |

</details>

<details><summary><code>72e_1a7_3ac</code> 王准之（5 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 王准之 | [《宋書・范泰 王准之 王韶之 荀伯子》][788] | [JSON](72e_1a7_3ac.json) |
| `A` | 王興之（王准之子） | [《南史・王裕之　王鎮之　王韶之　王悅之　王准之》][500]、[《南史・王裕之　王鎮之　王韶之　王悅之　王准之》][505]、[《宋書・范泰 王准之 王韶之 荀伯子》][788] | [JSON](72e_1a7_3ac_A.json) |
| `AA` | 王進之（王輿之子） | [《南史・王裕之　王鎮之　王韶之　王悅之　王准之》][500] | [JSON](72e_1a7_3ac_AA.json) |
| `AAA` | 王清（王進之子，中廬公） | [《南史・王裕之　王鎮之　王韶之　王悅之　王准之》][501] | [JSON](72e_1a7_3ac_AAA.json) |
| `AAAA` | 王猛（字世雄，本名勇） | [《南史・王裕之　王鎮之　王韶之　王悅之　王准之》][501] | [JSON](72e_1a7_3ac_AAAA.json) |

</details>

<details><summary><code>766_5dq_zws</code> 朱家（季布欒布列傳候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 朱家 | [《史記・季布欒布列傳》][648] | [JSON](766_5dq_zws.json) |
| `A` | 朱家子未名 | [《史記・季布欒布列傳》][648] | [JSON](766_5dq_zws_A.json) |

</details>

<details><summary><code>77h_id3_a0i</code> 陸邵（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 陸邵 | [《南齊書・劉瓛 弟璡 陸澄》][338]、[《南史・陸澄　陸慧曉　陸杲》][530] | [JSON](77h_id3_a0i.json) |
| `A` | 陸瑗 | [《南齊書・劉瓛 弟璡 陸澄》][338]、[《南史・陸澄　陸慧曉　陸杲》][530] | [JSON](77h_id3_a0i_A.json) |
| `AA` | 陸澄 | [《南齊書・褚淵 淵弟澄 徐嗣 王儉》][308]、[《南史・王曇首》][460] | [JSON](77h_id3_a0i_AA.json) |

</details>

<details><summary><code>77n_qzq_xi3</code> 石鑒〔西晉太尉，字林伯〕（6 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 石鑒〔西晉太尉，字林伯〕 | [《晉書・鄭袤 李胤 盧欽 華表 石鑒 溫羨》][144] | [JSON](77n_qzq_xi3.json) |
| `A` | 石尠〔城陽簡侯，字處約〕 | [《晉城陽簡侯石尠墓誌・節錄》][27] | [JSON](77n_qzq_xi3_A.json) |
| `AA` | 石定〔字庶公〕 | [《處士石定墓誌・節錄》][26] | [JSON](77n_qzq_xi3_AA.json) |
| `AB` | 石邁〔字庶昆〕 | [《晉城陽簡侯石尠墓誌・節錄》][27] | [JSON](77n_qzq_xi3_AB.json) |
| `AC` | 石恭〔石尠庶子〕 | [《晉城陽簡侯石尠墓誌・節錄》][27] | [JSON](77n_qzq_xi3_AC.json) |
| `AD` | 石氏〔字令脩〕 | [《晉城陽簡侯石尠墓誌・節錄》][27] | [JSON](77n_qzq_xi3_AD.json) |

</details>

<details><summary><code>78u_8ii_bnr</code> 專諸（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 專諸 | [《史記・刺客列傳》][634] | [JSON](78u_8ii_bnr.json) |
| `A` | 專諸子（本卷未名） | [《史記・吳太伯世家》][579]、[《史記・刺客列傳》][634] | [JSON](78u_8ii_bnr_A.json) |

</details>

<details><summary><code>796_nkw_0jz</code> 張蒼父未名（張丞相列傳候選）（4 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 張蒼父未名 | [《史記・張丞相列傳》][644] | [JSON](796_nkw_0jz.json) |
| `A` | 張蒼 | [《史記・張丞相列傳》][644] | [JSON](796_nkw_0jz_A.json) |
| `AA` | 張蒼子未名（康侯） | [《史記・張丞相列傳》][644] | [JSON](796_nkw_0jz_AA.json) |
| `AAA` | 張類 | [《史記・張丞相列傳》][644] | [JSON](796_nkw_0jz_AAA.json) |

</details>

<details><summary><code>7a0_95e_c4a</code> 王敬則（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 王敬則 | [《南齊書・王融 謝朓》][358] | [JSON](7a0_95e_c4a.json) |
| `A` | 王敬則女（謝朓妻，未名） | — | [JSON](7a0_95e_c4a_A.json) |

</details>

<details><summary><code>7ad_718_47c</code> 王慧龍（8 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 王慧龍 | [《魏書・刁雍 王慧龍 韓延之 袁式》][852] | [JSON](7ad_718_47c.json) |
| `A` | 王寶興 | [《魏書・刁雍 王慧龍 韓延之 袁式》][852] | [JSON](7ad_718_47c_A.json) |
| `AA` | 王瓊 | [《魏書・刁雍 王慧龍 韓延之 袁式》][852] | [JSON](7ad_718_47c_AA.json) |
| `AAA` | 王遵業 | [《魏書・刁雍 王慧龍 韓延之 袁式》][852] | [JSON](7ad_718_47c_AAA.json) |
| `AAAA` | 王松年 | [《魏書・刁雍 王慧龍 韓延之 袁式》][852] | [JSON](7ad_718_47c_AAAA.json) |
| `AAB` | 王瓊長女〔入嬪，未名〕 | [《魏書・刁雍 王慧龍 韓延之 袁式》][852] | [JSON](7ad_718_47c_AAB.json) |
| `AAC` | 王瓊女〔盧道亮妻，未名〕 | [《魏書・刁雍 王慧龍 韓延之 袁式》][852] | [JSON](7ad_718_47c_AAC.json) |
| `B` | 王慧龍女〔未名〕 | [《魏書・刁雍 王慧龍 韓延之 袁式》][852] | [JSON](7ad_718_47c_B.json) |

</details>

<details><summary><code>7b9_110_008</code> 韋端（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 韋端 | [《三國志・二荀賈傳》][543] | [JSON](7b9_110_008.json) |
| `A` | 韋康 | [《三國志・二荀賈傳》][543] | [JSON](7b9_110_008_A.json) |

</details>

<details><summary><code>7du_pfa_2s5</code> 蹇叔（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 蹇叔 | [《史記・秦本紀》][571] | [JSON](7du_pfa_2s5.json) |
| `A` | 西乞術 | [《史記・秦本紀》][571]、[《史記・晉世家》][587] | [JSON](7du_pfa_2s5_A.json) |
| `B` | 白乙丙 | [《史記・秦本紀》][571]、[《史記・晉世家》][587] | [JSON](7du_pfa_2s5_B.json) |

</details>

<details><summary><code>7dv_lqp_y4z</code> 靳歙（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 靳歙 | [《漢書・樊酈滕灌傅靳周傳》][43] | [JSON](7dv_lqp_y4z.json) |
| `A` | 靳亭 | [《史記・高祖功臣侯者年表》][900] | [JSON](7dv_lqp_y4z_A.json) |

</details>

<details><summary><code>7hw_8jq_c1e</code> 楊暉〔鈞祖，弘農簡公原記〕（7 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 楊暉〔鈞祖，弘農簡公原記〕 | [《魏書・楊播》][857] | [JSON](7hw_8jq_c1e.json) |
| `A` | 楊恩〔鈞父〕 | [《魏書・楊播》][857] | [JSON](7hw_8jq_c1e_A.json) |
| `AA` | 楊鈞〔恒州刺史〕 | [《魏書・楊播》][857] | [JSON](7hw_8jq_c1e_AA.json) |
| `AAA` | 楊暄〔鈞長子〕 | [《魏書・楊播》][857] | [JSON](7hw_8jq_c1e_AAA.json) |
| `AAB` | 楊穆〔暄弟〕 | [《魏書・楊播》][857] | [JSON](7hw_8jq_c1e_AAB.json) |
| `AAC` | 楊儉〔穆弟〕 | [《魏書・楊播》][857] | [JSON](7hw_8jq_c1e_AAC.json) |
| `AAD` | 楊寬〔儉弟〕 | [《魏書・楊播》][857] | [JSON](7hw_8jq_c1e_AAD.json) |

</details>

<details><summary><code>7mz_d13_9ka</code> 田氏（外戚世家候選）（4 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 田氏 | [《史記・外戚世家》][597] | [JSON](7mz_d13_9ka.json) |
| `A` | 田蚡 | [《史記・魏其武安列傳》][655] | [JSON](7mz_d13_9ka_A.json) |
| `AA` | 恬（田蚡子） | [《史記・魏其武安列傳》][655] | [JSON](7mz_d13_9ka_AA.json) |
| `B` | 勝 | [《史記・外戚世家》][597]、[《史記・魏其武安列傳》][655] | [JSON](7mz_d13_9ka_B.json) |

</details>

<details><summary><code>7r6_k52_qji</code> 王仁（150 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 王仁 | [《晉書・王祥 鄭沖 何曾 石苞》][113] | [JSON](7r6_k52_qji.json) |
| `A` | 王融 | [《晉書・王祥 鄭沖 何曾 石苞》][113]、[《世說新語・德行》][679] | [JSON](7r6_k52_qji_A.json) |
| `AA` | 王祥 | [《晉書・王祥 鄭沖 何曾 石苞》][113] | [JSON](7r6_k52_qji_AA.json) |
| `AAA` | 王肇 | [《晉書・王祥 鄭沖 何曾 石苞》][113] | [JSON](7r6_k52_qji_AAA.json) |
| `AAAA` | 王俊 | [《晉書・王祥 鄭沖 何曾 石苞》][113] | [JSON](7r6_k52_qji_AAAA.json) |
| `AAAAA` | 王遐 | [《晉書・王祥 鄭沖 何曾 石苞》][113] | [JSON](7r6_k52_qji_AAAAA.json) |
| `AAB` | 王夏 | [《晉書・王祥 鄭沖 何曾 石苞》][113] | [JSON](7r6_k52_qji_AAB.json) |
| `AAC` | 王馥 | [《晉書・王祥 鄭沖 何曾 石苞》][113] | [JSON](7r6_k52_qji_AAC.json) |
| `AACA` | 王根 | [《晉書・王祥 鄭沖 何曾 石苞》][113] | [JSON](7r6_k52_qji_AACA.json) |
| `AAD` | 王烈 | [《晉書・王祥 鄭沖 何曾 石苞》][113] | [JSON](7r6_k52_qji_AAD.json) |
| `AAE` | 王芬 | [《晉書・王祥 鄭沖 何曾 石苞》][113] | [JSON](7r6_k52_qji_AAE.json) |
| `AB` | 王覽 | [《晉書・王祥 鄭沖 何曾 石苞》][113] | [JSON](7r6_k52_qji_AB.json) |
| `ABA` | 王裁 | [《晉書・王祥 鄭沖 何曾 石苞》][113] | [JSON](7r6_k52_qji_ABA.json) |
| `ABAA` | 王導 | [《晉書・王導》][169] | [JSON](7r6_k52_qji_ABAA.json) |
| `ABAAA` | 王洽 | [《晉書・王導》][169] | [JSON](7r6_k52_qji_ABAAA.json) |
| `ABAAAA` | 王珣 | [《晉書・王導》][169] | [JSON](7r6_k52_qji_ABAAAA.json) |
| `ABAAAAA` | 王弘 | [《宋書・劉穆之 王弘》][760] | [JSON](7r6_k52_qji_ABAAAAA.json) |
| `ABAAAAAA` | 王錫 | [《宋書・王僧達 顏竣》][806] | [JSON](7r6_k52_qji_ABAAAAAA.json) |
| `ABAAAAAAA` | 王僧亮 | [《南史・王弘》][448] | [JSON](7r6_k52_qji_ABAAAAAAA.json) |
| `ABAAAAAAB` | 王僧衍 | [《南史・王弘》][439]、[《南史・王弘》][448] | [JSON](7r6_k52_qji_ABAAAAAAB.json) |
| `ABAAAAAABA` | 王茂璋 | [《南史・王弘》][439] | [JSON](7r6_k52_qji_ABAAAAAABA.json) |
| `ABAAAAAABAA` | 王沖〔字長深〕 | [《南史・王弘》][439] | [JSON](7r6_k52_qji_ABAAAAAABAA.json) |
| `ABAAAAAABAAA` | 王瑒 | [《南史・王弘》][449] | [JSON](7r6_k52_qji_ABAAAAAABAAA.json) |
| `ABAAAAAABAAB` | 王瑜〔陳使齊者〕 | [《南史・王弘》][450] | [JSON](7r6_k52_qji_ABAAAAAABAAB.json) |
| `ABAAAAAB` | 王僧達 | [《宋書・王僧達 顏竣》][806] | [JSON](7r6_k52_qji_ABAAAAAB.json) |
| `ABAAAAABA` | 王道琰 | [《南齊書・王融 謝朓》][357]、[《南齊書・王融 謝朓》][356]、[《南史・王弘》][440]、[《宋書・王僧達 顏竣》][806] | [JSON](7r6_k52_qji_ABAAAAABA.json) |
| `ABAAAAB` | 王虞 | [《南史・王弘》][441] | [JSON](7r6_k52_qji_ABAAAAB.json) |
| `ABAAAABA` | 王深 | [《南史・王弘》][441] | [JSON](7r6_k52_qji_ABAAAABA.json) |
| `ABAAAAC` | 王柳 | [《南史・王弘》][441]、[《南史・王弘》][452]、[《宋書・劉穆之 王弘》][760] | [JSON](7r6_k52_qji_ABAAAAC.json) |
| `ABAAAACA` | 王猷（字世倫） | [《南史・王弘》][452] | [JSON](7r6_k52_qji_ABAAAACA.json) |
| `ABAAAACAA` | 王瞻 | [《梁書・王瞻 王志 王峻 王暕 子訓 王泰 王份 孫鍚 僉 張充 柳惲 蔡撙 江蒨》][253]、[《梁書・王瞻 王志 王峻 王暕 子訓 王泰 王份 孫鍚 僉 張充 柳惲 蔡撙 江蒨》][252] | [JSON](7r6_k52_qji_ABAAAACAA.json) |
| `ABAAAACAAA` | 王長玄 | [《梁書・王瞻 王志 王峻 王暕 子訓 王泰 王份 孫鍚 僉 張充 柳惲 蔡撙 江蒨》][253]、[《梁書・王瞻 王志 王峻 王暕 子訓 王泰 王份 孫鍚 僉 張充 柳惲 蔡撙 江蒨》][252]、[《南史・王弘》][452] | [JSON](7r6_k52_qji_ABAAAACAAA.json) |
| `ABAAAAD` | 王孺 | [《南史・王弘》][441]、[《宋書・劉穆之 王弘》][760] | [JSON](7r6_k52_qji_ABAAAAD.json) |
| `ABAAAADA` | 王微 | [《宋書・羊欣 張敷 王微》][791] | [JSON](7r6_k52_qji_ABAAAADA.json) |
| `ABAAAAE` | 王曇首 | [《宋書・王華 王曇首 殷景仁 沈演之》][792] | [JSON](7r6_k52_qji_ABAAAAE.json) |
| `ABAAAAEA` | 王僧綽 | [《宋書・徐湛之 江湛 王僧綽》][801] | [JSON](7r6_k52_qji_ABAAAAEA.json) |
| `ABAAAAEAA` | 王儉 | [《南史・王曇首》][460] | [JSON](7r6_k52_qji_ABAAAAEAA.json) |
| `ABAAAAEAA*A` | 王蕣華〔齊和帝皇后〕 | [《南齊書・皇后》][304]、[《南齊書・皇后》][303]、[《南史・后妃上》][398]、[《南史・后妃上》][399] | [JSON](7r6_k52_qji_ABAAAAEAA%2AA.json) |
| `ABAAAAEAAA` | 王騫 | [《南史・王曇首》][461] | [JSON](7r6_k52_qji_ABAAAAEAAA.json) |
| `ABAAAAEAAAA` | 王規 | [《南史・王曇首》][457] | [JSON](7r6_k52_qji_ABAAAAEAAAA.json) |
| `ABAAAAEAAAAA` | 王褒 | [《舊唐書・列傳第三十九: 狄仁傑 王方慶 姚璹》][232]、[《梁書・王規 劉瑴 宗懍 王承 褚翔 蕭介 從父兄洽 褚球 劉孺 弟覽 遵 劉潛 弟孝勝 孝威 孝先 殷芸 蕭幾》][269]、[《周書・列傳第33 王襃 庾信》][875] | [JSON](7r6_k52_qji_ABAAAAEAAAAA.json) |
| `ABAAAAEAAAAAA` | 王鼒 | [《舊唐書・列傳第三十九: 狄仁傑 王方慶 姚璹》][232]、[《周書・列傳第33 王襃 庾信》][875] | [JSON](7r6_k52_qji_ABAAAAEAAAAAA.json) |
| `ABAAAAEAAAAAAA` | 王弘直 | [《舊唐書・列傳第三十九: 狄仁傑 王方慶 姚璹》][232]、[《新唐書・王綝　韋思謙　陸元方　王及善　李日知　杜景佺　李懷遠》][873] | [JSON](7r6_k52_qji_ABAAAAEAAAAAAA.json) |
| `ABAAAAEAAAAAAAA` | 王方慶 | [《舊唐書・列傳第三十九: 狄仁傑 王方慶 姚璹》][232]、[《新唐書・王綝　韋思謙　陸元方　王及善　李日知　杜景佺　李懷遠》][873] | [JSON](7r6_k52_qji_ABAAAAEAAAAAAAA.json) |
| `ABAAAAEAAAAAAAAA` | 王光輔 | [《舊唐書・列傳第三十九: 狄仁傑 王方慶 姚璹》][232] | [JSON](7r6_k52_qji_ABAAAAEAAAAAAAAA.json) |
| `ABAAAAEAAAAAAAAB` | 王晙 | [《舊唐書・列傳第三十九: 狄仁傑 王方慶 姚璹》][232] | [JSON](7r6_k52_qji_ABAAAAEAAAAAAAAB.json) |
| `ABAAAAEAAB` | 王暕（字思晦） | [《梁書・王瞻 王志 王峻 王暕 子訓 王泰 王份 孫鍚 僉 張充 柳惲 蔡撙 江蒨》][248] | [JSON](7r6_k52_qji_ABAAAAEAAB.json) |
| `ABAAAAEAABA` | 王承（字安期，王暕子） | [《南史・王曇首》][455] | [JSON](7r6_k52_qji_ABAAAAEAABA.json) |
| `ABAAAAEAABB` | 王幼（王承弟） | [《梁書・王瞻 王志 王峻 王暕 子訓 王泰 王份 孫鍚 僉 張充 柳惲 蔡撙 江蒨》][248]、[《南史・王曇首》][455]、[《南史・王曇首》][459] | [JSON](7r6_k52_qji_ABAAAAEAABB.json) |
| `ABAAAAEAABC` | 王訓（字懷範） | [《南史・王曇首》][468] | [JSON](7r6_k52_qji_ABAAAAEAABC.json) |
| `ABAAAAEAABD` | 王訏（王暕子） | [《梁書・王瞻 王志 王峻 王暕 子訓 王泰 王份 孫鍚 僉 張充 柳惲 蔡撙 江蒨》][248] | [JSON](7r6_k52_qji_ABAAAAEAABD.json) |
| `ABAAAAEAB` | 王遜 | [《南齊書・褚淵 淵弟澄 徐嗣 王儉》][308]、[《南史・王曇首》][460] | [JSON](7r6_k52_qji_ABAAAAEAB.json) |
| `ABAAAAEB` | 王僧虔 | [《南齊書・王僧虔 張緒》][330] | [JSON](7r6_k52_qji_ABAAAAEB.json) |
| `ABAAAAEBA` | 王慈 | [《南史・王曇首》][456] | [JSON](7r6_k52_qji_ABAAAAEBA.json) |
| `ABAAAAEBAA` | 王泰（字仲通） | [《南史・王曇首》][465] | [JSON](7r6_k52_qji_ABAAAAEBAA.json) |
| `ABAAAAEBAAA` | 王廓（王泰子） | [《梁書・王瞻 王志 王峻 王暕 子訓 王泰 王份 孫鍚 僉 張充 柳惲 蔡撙 江蒨》][250]、[《南史・王曇首》][465] | [JSON](7r6_k52_qji_ABAAAAEBAAA.json) |
| `ABAAAAEBAB` | 王觀（王慈子） | [《南史・王曇首》][456] | [JSON](7r6_k52_qji_ABAAAAEBAB.json) |
| `ABAAAAEBAC` | 王慈女（江夏王鋒妃） | — | [JSON](7r6_k52_qji_ABAAAAEBAC.json) |
| `ABAAAAEBAD` | 王韶明〔齊海陵王妃〕 | [《南齊書・皇后》][302]、[《南齊書・皇后》][301]、[《南史・后妃上》][396]、[《南史・后妃上》][397] | [JSON](7r6_k52_qji_ABAAAAEBAD.json) |
| `ABAAAAEBB` | 王寂 | [《南齊書・王僧虔 張緒》][330] | [JSON](7r6_k52_qji_ABAAAAEBB.json) |
| `ABAAAAEBC` | 王志 | [《南史・王曇首》][473] | [JSON](7r6_k52_qji_ABAAAAEBC.json) |
| `ABAAAAEBCA` | 王緝 | [《梁書・王瞻 王志 王峻 王暕 子訓 王泰 王份 孫鍚 僉 張充 柳惲 蔡撙 江蒨》][255]、[《梁書・王瞻 王志 王峻 王暕 子訓 王泰 王份 孫鍚 僉 張充 柳惲 蔡撙 江蒨》][254]、[《南史・王曇首》][473]、[《南史・王曇首》][472] | [JSON](7r6_k52_qji_ABAAAAEBCA.json) |
| `ABAAAAEBCB` | 王休 | [《梁書・王瞻 王志 王峻 王暕 子訓 王泰 王份 孫鍚 僉 張充 柳惲 蔡撙 江蒨》][255]、[《梁書・王瞻 王志 王峻 王暕 子訓 王泰 王份 孫鍚 僉 張充 柳惲 蔡撙 江蒨》][254]、[《南史・王曇首》][473]、[《南史・王曇首》][472] | [JSON](7r6_k52_qji_ABAAAAEBCB.json) |
| `ABAAAAEBCC` | 王諲 | [《梁書・王瞻 王志 王峻 王暕 子訓 王泰 王份 孫鍚 僉 張充 柳惲 蔡撙 江蒨》][255]、[《梁書・王瞻 王志 王峻 王暕 子訓 王泰 王份 孫鍚 僉 張充 柳惲 蔡撙 江蒨》][254]、[《南史・謝晦　謝裕　謝方明　謝靈運》][432]、[《南史・王曇首》][473]、[《南史・王曇首》][472] | [JSON](7r6_k52_qji_ABAAAAEBCC.json) |
| `ABAAAAEBCD` | 王操 | [《梁書・王瞻 王志 王峻 王暕 子訓 王泰 王份 孫鍚 僉 張充 柳惲 蔡撙 江蒨》][255]、[《梁書・王瞻 王志 王峻 王暕 子訓 王泰 王份 孫鍚 僉 張充 柳惲 蔡撙 江蒨》][254]、[《南史・王曇首》][473]、[《南史・王曇首》][472] | [JSON](7r6_k52_qji_ABAAAAEBCD.json) |
| `ABAAAAEBCE` | 王素 | [《梁書・王瞻 王志 王峻 王暕 子訓 王泰 王份 孫鍚 僉 張充 柳惲 蔡撙 江蒨》][255]、[《梁書・王瞻 王志 王峻 王暕 子訓 王泰 王份 孫鍚 僉 張充 柳惲 蔡撙 江蒨》][254]、[《南史・王曇首》][473]、[《南史・王曇首》][472] | [JSON](7r6_k52_qji_ABAAAAEBCE.json) |
| `ABAAAAEBD` | 王彬（字思文） | [《南史・王曇首》][454] | [JSON](7r6_k52_qji_ABAAAAEBD.json) |
| `ABAAAB` | 王瑉 | [《晉書・王導》][169] | [JSON](7r6_k52_qji_ABAAAB.json) |
| `ABAAABA` | 王朗（王瑉子） | [《晉書・王導》][169] | [JSON](7r6_k52_qji_ABAAABA.json) |
| `ABAAABB` | 王練 | [《宋書・劉穆之 王弘》][760] | [JSON](7r6_k52_qji_ABAAABB.json) |
| `ABAAABBA` | 王釗 | [《宋書・劉穆之 王弘》][760] | [JSON](7r6_k52_qji_ABAAABBA.json) |
| `ABAAB` | 王悅 | [《晉書・王導》][169] | [JSON](7r6_k52_qji_ABAAB.json) |
| `ABAAC` | 王恬 | [《晉書・王導》][169] | [JSON](7r6_k52_qji_ABAAC.json) |
| `ABAACA` | 王琨 | [《世說新語・排調》][735] | [JSON](7r6_k52_qji_ABAACA.json) |
| `ABAACAA` | 王嘏 | [《南史・王誕　王華　王惠　王彧》][476]、[《南史・王誕　王華　王惠　王彧》][475] | [JSON](7r6_k52_qji_ABAACAA.json) |
| `ABAACAAA` | 王恢（王嘏子） | [《晉書・王導》][169]、[《南史・王誕　王華　王惠　王彧》][476]、[《南史・王誕　王華　王惠　王彧》][475] | [JSON](7r6_k52_qji_ABAACAAA.json) |
| `ABAACAAB` | 王偃（字子游，王嘏子） | [《南史・王誕　王華　王惠　王彧》][476]、[《南史・王誕　王華　王惠　王彧》][475] | [JSON](7r6_k52_qji_ABAACAAB.json) |
| `ABAACAABA` | 王憲嫄（孝武文穆王皇后） | [《宋書・后妃》][755] | [JSON](7r6_k52_qji_ABAACAABA.json) |
| `ABAACAABB` | 王藻（王偃長子） | [《南史・王誕　王華　王惠　王彧》][498]、[《宋書・后妃》][755] | [JSON](7r6_k52_qji_ABAACAABB.json) |
| `ABAACAABC` | 王懋（字昌業，王藻弟） | [《南史・王誕　王華　王惠　王彧》][495] | [JSON](7r6_k52_qji_ABAACAABC.json) |
| `ABAACAABCA` | 王瑩（字奉光，王懋子） | [《南史・王誕　王華　王惠　王彧》][495] | [JSON](7r6_k52_qji_ABAACAABCA.json) |
| `ABAACAABCAA` | 王實（王瑩少子） | [《南史・王誕　王華　王惠　王彧》][495] | [JSON](7r6_k52_qji_ABAACAABCAA.json) |
| `ABAACAABD` | 王攸（王懋弟） | [《南史・王誕　王華　王惠　王彧》][486] | [JSON](7r6_k52_qji_ABAACAABD.json) |
| `ABAACAABDA` | 王亮（字奉叔，王攸子） | [《南史・王誕　王華　王惠　王彧》][486] | [JSON](7r6_k52_qji_ABAACAABDA.json) |
| `ABAACAABE` | 王臻（王攸弟） | [《宋書・后妃》][755] | [JSON](7r6_k52_qji_ABAACAABE.json) |
| `ABAAD` | 王協 | [《晉書・王導》][169] | [JSON](7r6_k52_qji_ABAAD.json) |
| `ABAAE` | 王邵 | [《晉書・王導》][169] | [JSON](7r6_k52_qji_ABAAE.json) |
| `ABAAED` | 王穆（王劭子） | [《晉書・王導》][169] | [JSON](7r6_k52_qji_ABAAED.json) |
| `ABAAEDA` | 王簡 | [《晉書・王導》][169] | [JSON](7r6_k52_qji_ABAAEDA.json) |
| `ABAAEDB` | 王智 | [《南史・王誕　王華　王惠　王彧》][496] | [JSON](7r6_k52_qji_ABAAEDB.json) |
| `ABAAEDC` | 王超 | [《晉書・王導》][169] | [JSON](7r6_k52_qji_ABAAEDC.json) |
| `ABAAEE` | 王默（王劭子） | [《晉書・王導》][169] | [JSON](7r6_k52_qji_ABAAEE.json) |
| `ABAAEEA` | 王鑒（王默子） | [《南史・王誕　王華　王惠　王彧》][484] | [JSON](7r6_k52_qji_ABAAEEA.json) |
| `ABAAEEB` | 王惠 | [《南史・王誕　王華　王惠　王彧》][484] | [JSON](7r6_k52_qji_ABAAEEB.json) |
| `ABAAEF` | 王恢（王劭子） | [《晉書・王導》][169] | [JSON](7r6_k52_qji_ABAAEF.json) |
| `ABAAF` | 王薈 | [《晉書・王導》][169] | [JSON](7r6_k52_qji_ABAAF.json) |
| `ABAAFA` | 王廞 | [《宋書・王華 王曇首 殷景仁 沈演之》][792] | [JSON](7r6_k52_qji_ABAAFA.json) |
| `ABAAFAA` | 王泰 | [《晉書・王導》][169]、[《南史・王誕　王華　王惠　王彧》][481]、[《宋書・王華 王曇首 殷景仁 沈演之》][792]、[《宋書・王華 王曇首 殷景仁 沈演之》][793] | [JSON](7r6_k52_qji_ABAAFAA.json) |
| `ABAAFAB` | 王華 | [《宋書・王華 王曇首 殷景仁 沈演之》][792] | [JSON](7r6_k52_qji_ABAAFAB.json) |
| `ABAAFABA` | 王嗣 | [《宋書・徐湛之 江湛 王僧綽》][801] | [JSON](7r6_k52_qji_ABAAFABA.json) |
| `ABAAFABAA` | 王長 | [《南史・王誕　王華　王惠　王彧》][485]、[《宋書・王華 王曇首 殷景仁 沈演之》][792]、[《宋書・王華 王曇首 殷景仁 沈演之》][793] | [JSON](7r6_k52_qji_ABAAFABAA.json) |
| `ABAAFAC` | 王廞女 | [《宋書・王華 王曇首 殷景仁 沈演之》][792]、[《宋書・王華 王曇首 殷景仁 沈演之》][793] | [JSON](7r6_k52_qji_ABAAFAC.json) |
| `ABAAFB` | 王懌 | [《南史・王誕　王華　王惠　王彧》][485] | [JSON](7r6_k52_qji_ABAAFB.json) |
| `ABAAFBA` | 王琨〔王懌子〕 | [《南史・王誕　王華　王惠　王彧》][485] | [JSON](7r6_k52_qji_ABAAFBA.json) |
| `ABAB` | 王穎 | [《世說新語・品藻》][721] | [JSON](7r6_k52_qji_ABAB.json) |
| `ABAC` | 王敞 | [《世說新語・品藻》][721] | [JSON](7r6_k52_qji_ABAC.json) |
| `ABB` | 王基 | [《晉書・王祥 鄭沖 何曾 石苞》][113] | [JSON](7r6_k52_qji_ABB.json) |
| `ABC` | 王會 | [《晉書・王祥 鄭沖 何曾 石苞》][113] | [JSON](7r6_k52_qji_ABC.json) |
| `ABD` | 王正 | [《晉書・王祥 鄭沖 何曾 石苞》][113] | [JSON](7r6_k52_qji_ABD.json) |
| `ABDA` | 王廙 | [《晉書・王舒 王廙 虞潭 顧眾 張闓》][193] | [JSON](7r6_k52_qji_ABDA.json) |
| `ABDAA` | 王頤之 | [《晉書・王舒 王廙 虞潭 顧眾 張闓》][193] | [JSON](7r6_k52_qji_ABDAA.json) |
| `ABDAB` | 王胡之 | [《晉書・王舒 王廙 虞潭 顧眾 張闓》][193] | [JSON](7r6_k52_qji_ABDAB.json) |
| `ABDABA` | 王茂之 | [《晉書・王舒 王廙 虞潭 顧眾 張闓》][193]、[《南史・范泰　荀伯子　徐廣　鄭鮮之　裴松之　何承天》][518]、[《宋書・鄭鮮之 裴松之 何承天》][795]、[《宋書・王敬弘 何尚之》][797]、[《宋書・王敬弘 何尚之》][796] | [JSON](7r6_k52_qji_ABDABA.json) |
| `ABDABAA` | 王敬弘 | [《南史・王裕之　王鎮之　王韶之　王悅之　王准之》][506] | [JSON](7r6_k52_qji_ABDABAA.json) |
| `ABDABAAA` | 王恢之 | [《宋書・王敬弘 何尚之》][797] | [JSON](7r6_k52_qji_ABDABAAA.json) |
| `ABDABAAB` | 王瓚之 | [《南史・王裕之　王鎮之　王韶之　王悅之　王准之》][506] | [JSON](7r6_k52_qji_ABDABAAB.json) |
| `ABDABAABA` | 王秀之 | [《南齊書・王秀之 王慈 蔡約 陸慧曉 顧憲之 蕭惠基》][355] | [JSON](7r6_k52_qji_ABDABAABA.json) |
| `ABDABAABAA` | 王峻 | [《梁書・王瞻 王志 王峻 王暕 子訓 王泰 王份 孫鍚 僉 張充 柳惲 蔡撙 江蒨》][249] | [JSON](7r6_k52_qji_ABDABAABAA.json) |
| `ABDABAABAAA` | 王琮 | [《梁書・王瞻 王志 王峻 王暕 子訓 王泰 王份 孫鍚 僉 張充 柳惲 蔡撙 江蒨》][249]、[《南史・王裕之　王鎮之　王韶之　王悅之　王准之》][506] | [JSON](7r6_k52_qji_ABDABAABAAA.json) |
| `ABDABAABAAB` | 王玩（王峻子） | [《梁書・王瞻 王志 王峻 王暕 子訓 王泰 王份 孫鍚 僉 張充 柳惲 蔡撙 江蒨》][249] | [JSON](7r6_k52_qji_ABDABAABAAB.json) |
| `ABDABAAC` | 王昇之 | [《南史・王裕之　王鎮之　王韶之　王悅之　王准之》][506]、[《宋書・王敬弘 何尚之》][797] | [JSON](7r6_k52_qji_ABDABAAC.json) |
| `ABDABAACA` | 王延之 | [《南齊書・王琨 張岱 褚炫 何戢 王延之 阮韜》][329] | [JSON](7r6_k52_qji_ABDABAACA.json) |
| `ABDABAACAA` | 王倫之 | [《南史・王裕之　王鎮之　王韶之　王悅之　王准之》][506] | [JSON](7r6_k52_qji_ABDABAACAA.json) |
| `ABDABAACAAA` | 王昕（綸之子） | [《南史・王裕之　王鎮之　王韶之　王悅之　王准之》][506] | [JSON](7r6_k52_qji_ABDABAACAAA.json) |
| `ABDABAAD` | 王敬弘女（何述之妻，未名） | — | [JSON](7r6_k52_qji_ABDABAAD.json) |
| `ABDABAAE` | 王敬弘女（孔尚妻） | [《宋書・隱逸》][828] | [JSON](7r6_k52_qji_ABDABAAE.json) |
| `ABDABB` | 王和之（字興道） | [《世說新語・輕詆》][736] | [JSON](7r6_k52_qji_ABDABB.json) |
| `ABDAC` | 王耆之 | [《世說新語・賞譽》][716] | [JSON](7r6_k52_qji_ABDAC.json) |
| `ABDACA` | 王隨之 | [《南史・王裕之　王鎮之　王韶之　王悅之　王准之》][506]、[《宋書・良吏》][827] | [JSON](7r6_k52_qji_ABDACA.json) |
| `ABDACAA` | 王鎮之 | [《宋書・良吏》][827] | [JSON](7r6_k52_qji_ABDACAA.json) |
| `ABDACAAA` | 王標之 | [《南史・王裕之　王鎮之　王韶之　王悅之　王准之》][506]、[《宋書・良吏》][827] | [JSON](7r6_k52_qji_ABDACAAA.json) |
| `ABDACAB` | 王弘之 | [《宋書・隱逸》][828] | [JSON](7r6_k52_qji_ABDACAB.json) |
| `ABDACABA` | 王曇生 | [《宋書・隱逸》][828] | [JSON](7r6_k52_qji_ABDACABA.json) |
| `ABDACABB` | 王普曜（王晏父） | [《古今姓氏書辯證・卷十四》][39]、[《南齊書・王奐 從弟繢 張沖》][360]、[《南史・王誕　王華　王惠　王彧》][482] | [JSON](7r6_k52_qji_ABDACABB.json) |
| `ABDACABBA` | 王詡（王晏弟） | [《古今姓氏書辯證・卷十四》][39] | [JSON](7r6_k52_qji_ABDACABBA.json) |
| `ABDACABC` | 王羅雲（王思遠父） | [《古今姓氏書辯證・卷十四》][39]、[《南齊書・江斆 何昌㝢 謝𤅢 王思遠》][349] | [JSON](7r6_k52_qji_ABDACABC.json) |
| `ABDAD` | 王羨之（鎮軍掾） | [《南史・王裕之　王鎮之　王韶之　王悅之　王准之》][503]、[《南史・王裕之　王鎮之　王韶之　王悅之　王准之》][502]、[《宋書・范泰 王准之 王韶之 荀伯子》][787] | [JSON](7r6_k52_qji_ABDAD.json) |
| `ABDADA` | 王偉之（王韶之父） | [《南史・王裕之　王鎮之　王韶之　王悅之　王准之》][503]、[《南史・王裕之　王鎮之　王韶之　王悅之　王准之》][502]、[《宋書・范泰 王准之 王韶之 荀伯子》][787] | [JSON](7r6_k52_qji_ABDADA.json) |
| `ABDB` | 王彬 | [《晉書・王舒 王廙 虞潭 顧眾 張闓》][190] | [JSON](7r6_k52_qji_ABDB.json) |
| `ABDBA` | 王彭之 | [《世說新語・輕詆》][737] | [JSON](7r6_k52_qji_ABDBA.json) |
| `ABDBB` | 王彪之 | [《晉書・王舒 王廙 虞潭 顧眾 張闓》][189] | [JSON](7r6_k52_qji_ABDBB.json) |
| `ABDBBA` | 王越之 | [《晉書・王舒 王廙 虞潭 顧眾 張闓》][189] | [JSON](7r6_k52_qji_ABDBBA.json) |
| `ABDBBB` | 王臨之 | [《宋書・范泰 王准之 王韶之 荀伯子》][788] | [JSON](7r6_k52_qji_ABDBBB.json) |
| `ABDBBBA` | 王訥之（字永言） | [《宋書・范泰 王准之 王韶之 荀伯子》][788] | [JSON](7r6_k52_qji_ABDBBBA.json) |
| `ABDBC` | 興之〔本誌贛令〕 | [《王閩之墓誌・全文》][29] | [JSON](7r6_k52_qji_ABDBC.json) |
| `ABDBCA` | 王閩之 | [《王閩之墓誌・全文》][29] | [JSON](7r6_k52_qji_ABDBCA.json) |
| `ABE` | 王彥 | [《晉書・叛臣一》][221] | [JSON](7r6_k52_qji_ABE.json) |
| `ABF` | 王琛 | [《晉書・王祥 鄭沖 何曾 石苞》][113] | [JSON](7r6_k52_qji_ABF.json) |
| `ABFA` | 王棱 | [《晉書・王舒 王廙 虞潭 顧眾 張闓》][191] | [JSON](7r6_k52_qji_ABFA.json) |
| `ABFB` | 王侃 | [《晉書・王舒 王廙 虞潭 顧眾 張闓》][191] | [JSON](7r6_k52_qji_ABFB.json) |

</details>

<details><summary><code>7s2_h0m_msl</code> 蘇（曹戴伯）（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 蘇（曹戴伯） | [《史記・管蔡世家》][583] | [JSON](7s2_h0m_msl.json) |
| `A` | 兕（曹惠伯） | [《史記・管蔡世家》][583] | [JSON](7s2_h0m_msl_A.json) |
| `AA` | 石甫（曹惠伯子） | [《史記・管蔡世家》][583] | [JSON](7s2_h0m_msl_AA.json) |

</details>

<details><summary><code>7tm_3ss_4on</code> 周苛（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 周苛 | [《史記・張丞相列傳》][644] | [JSON](7tm_3ss_4on.json) |
| `*A` | 平（周苛孫） | [《史記・孝景本紀》][577] | [JSON](7tm_3ss_4on_%2AA.json) |
| `A` | 周成 | [《史記・張丞相列傳》][644] | [JSON](7tm_3ss_4on_A.json) |

</details>

<details><summary><code>7uk_oqn_ymk</code> 陳宣公杵臼（田世家候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 陳宣公杵臼 | [《史記・田敬仲完世家》][594] | [JSON](7uk_oqn_ymk.json) |
| `A` | 御寇 | [《史記・田敬仲完世家》][594] | [JSON](7uk_oqn_ymk_A.json) |

</details>

<details><summary><code>7zi_5gs_mq2</code> 華歆（12 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 華歆 | [《晉書・鄭袤 李胤 盧欽 華表 石鑒 溫羨》][147] | [JSON](7zi_5gs_mq2.json) |
| `A` | 華表〔字偉容〕 | [《晉書・鄭袤 李胤 盧欽 華表 石鑒 溫羨》][133] | [JSON](7zi_5gs_mq2_A.json) |
| `AA` | 華岑〔華表子〕 | [《晉書・鄭袤 李胤 盧欽 華表 石鑒 溫羨》][133] | [JSON](7zi_5gs_mq2_AA.json) |
| `AB` | 華嶠〔字叔駿〕 | [《晉書・鄭袤 李胤 盧欽 華表 石鑒 溫羨》][135] | [JSON](7zi_5gs_mq2_AB.json) |
| `ABA` | 華頤〔長樂內史〕 | [《晉書・鄭袤 李胤 盧欽 華表 石鑒 溫羨》][135] | [JSON](7zi_5gs_mq2_ABA.json) |
| `ABB` | 華徹〔華嶠中子〕 | [《晉書・鄭袤 李胤 盧欽 華表 石鑒 溫羨》][135] | [JSON](7zi_5gs_mq2_ABB.json) |
| `ABC` | 華暢〔華嶠少子〕 | [《晉書・鄭袤 李胤 盧欽 華表 石鑒 溫羨》][135] | [JSON](7zi_5gs_mq2_ABC.json) |
| `AC` | 華鑒〔華表子〕 | [《晉書・鄭袤 李胤 盧欽 華表 石鑒 溫羨》][133] | [JSON](7zi_5gs_mq2_AC.json) |
| `AD` | 華澹〔字玄駿〕 | [《晉書・鄭袤 李胤 盧欽 華表 石鑒 溫羨》][133]、[《晉書・周浚 成公簡 苟晞 華軼 劉喬》][161] | [JSON](7zi_5gs_mq2_AD.json) |
| `AE` | 華簡〔華表子〕 | [《晉書・鄭袤 李胤 盧欽 華表 石鑒 溫羨》][133] | [JSON](7zi_5gs_mq2_AE.json) |
| `B` | 華博〔華歆中子〕 | [《三國志・鍾繇華歆王朗傳》][546] | [JSON](7zi_5gs_mq2_B.json) |
| `C` | 華周〔華歆少子〕 | [《三國志・鍾繇華歆王朗傳》][546] | [JSON](7zi_5gs_mq2_C.json) |

</details>

<details><summary><code>82k_3oi_qf8</code> 山簡〔吊王衍幼子者〕（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 山簡〔吊王衍幼子者〕 | [《晉書・山濤 王戎 郭舒 樂廣》][125] | [JSON](82k_3oi_qf8.json) |
| `A` | 山遐〔字彥林〕 | [《晉書・山濤 王戎 郭舒 樂廣》][127] | [JSON](82k_3oi_qf8_A.json) |

</details>

<details><summary><code>85g_yq3_0w6</code> 王宰（王玄載祖）（4 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 王宰（王玄載祖） | [《南齊書・劉懷珍 李安民 王玄載》][318] | [JSON](85g_yq3_0w6.json) |
| `A` | 王蕤（王玄載父，東莞太守） | [《南齊書・劉懷珍 李安民 王玄載》][318]、[《南史・王鎮惡　朱齡石　毛脩之　傅弘之　朱脩之　王玄謨》][415] | [JSON](85g_yq3_0w6_A.json) |
| `AA` | 王玄載（字彥休） | [《南齊書・劉懷珍 李安民 王玄載》][318] | [JSON](85g_yq3_0w6_AA.json) |
| `AB` | 王玄邈〔齊安北將軍〕 | [《南齊書・劉懷珍 李安民 王玄載》][317] | [JSON](85g_yq3_0w6_AB.json) |

</details>

<details><summary><code>866_0fd_205</code> 劉表（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 劉表 | [《三國志・二荀賈傳》][543] | [JSON](866_0fd_205.json) |
| `A` | 劉脩 | [《三國志・任城陳蕭王傳》][554] | [JSON](866_0fd_205_A.json) |
| `B` | 劉琮 | [《三國志・二荀賈傳》][543] | [JSON](866_0fd_205_B.json) |

</details>

<details><summary><code>882_bd1_ca9</code> 李胤（5 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 李胤 | [《晉書・鄭袤 李胤 盧欽 華表 石鑒 溫羨》][138] | [JSON](882_bd1_ca9.json) |
| `A` | 李固〔字萬基〕 | [《晉書・鄭袤 李胤 盧欽 華表 石鑒 溫羨》][138] | [JSON](882_bd1_ca9_A.json) |
| `AA` | 李志〔字彥道〕 | [《晉書・鄭袤 李胤 盧欽 華表 石鑒 溫羨》][138] | [JSON](882_bd1_ca9_AA.json) |
| `B` | 李真長〔太僕卿〕 | [《晉書・鄭袤 李胤 盧欽 華表 石鑒 溫羨》][138] | [JSON](882_bd1_ca9_B.json) |
| `C` | 李修〔太弟中庶子〕 | [《晉書・鄭袤 李胤 盧欽 華表 石鑒 溫羨》][138] | [JSON](882_bd1_ca9_C.json) |

</details>

<details><summary><code>89c_afa_3eb</code> 單固父伯龍（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 單固父伯龍 | [《三國志・王毌丘諸葛鄧鍾傳》][562] | [JSON](89c_afa_3eb.json) |
| `A` | 單固 | [《三國志・王毌丘諸葛鄧鍾傳》][562] | [JSON](89c_afa_3eb_A.json) |

</details>

<details><summary><code>8e8_ca8_29d</code> 王佑（4 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 王佑 | [《晉書・王湛 荀崧 范汪 劉惔 張憑 韓伯》][185] | [JSON](8e8_ca8_29d.json) |
| `A` | 王嶠 | [《晉書・王湛 荀崧 范汪 劉惔 張憑 韓伯》][185] | [JSON](8e8_ca8_29d_A.json) |
| `AA` | 王淡 | [《晉書・王湛 荀崧 范汪 劉惔 張憑 韓伯》][185] | [JSON](8e8_ca8_29d_AA.json) |
| `AAA` | 王度世 | [《晉書・王湛 荀崧 范汪 劉惔 張憑 韓伯》][185] | [JSON](8e8_ca8_29d_AAA.json) |

</details>

<details><summary><code>8fx_ugl_pnj</code> 侯弘遠（侯瑱父）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 侯弘遠（侯瑱父） | [《陳書・列傳第三: 侯瑱 歐陽頠 吳明徹 裴子烈》][16] | [JSON](8fx_ugl_pnj.json) |
| `A` | 侯瑱（字伯玉） | [《陳書・列傳第三: 侯瑱 歐陽頠 吳明徹 裴子烈》][16] | [JSON](8fx_ugl_pnj_A.json) |

</details>

<details><summary><code>8im_m5e_cpy</code> 甘茂（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 甘茂 | [《史記・樗里子甘茂列傳》][619] | [JSON](8im_m5e_cpy.json) |
| `*A` | 甘羅 | [《史記・樗里子甘茂列傳》][619] | [JSON](8im_m5e_cpy_%2AA.json) |

</details>

<details><summary><code>8rw_c97_jpz</code> 梁伯（晉惠公外家）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 梁伯（晉惠公外家） | [《史記・晉世家》][587] | [JSON](8rw_c97_jpz.json) |
| `A` | 梁伯女（圉母） | [《史記・晉世家》][587] | [JSON](8rw_c97_jpz_A.json) |

</details>

<details><summary><code>8uz_r1g_a0f</code> 溫恕（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 溫恕 | [《三國志・劉司馬梁張溫賈傳》][550] | [JSON](8uz_r1g_a0f.json) |
| `A` | 溫恢 | [《三國志・劉司馬梁張溫賈傳》][550] | [JSON](8uz_r1g_a0f_A.json) |
| `AA` | 溫生 | [《三國志・劉司馬梁張溫賈傳》][550] | [JSON](8uz_r1g_a0f_AA.json) |

</details>

<details><summary><code>8xz_mlj_r3c</code> 韓千秋（南越列傳候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 韓千秋 | [《史記・南越列傳》][661] | [JSON](8xz_mlj_r3c.json) |
| `A` | 延年 | [《史記・建元以來侯者年表》][902] | [JSON](8xz_mlj_r3c_A.json) |

</details>

<details><summary><code>932_46f_026</code> 明帝（魏，荀勖引古）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 明帝（魏，荀勖引古） | [《三國志・諸夏侯曹傳》][541] | [JSON](932_46f_026.json) |
| `A` | 淑（平原懿公主） | [《三國志・桓二陳徐衞盧傳》][556] | [JSON](932_46f_026_A.json) |

</details>

<details><summary><code>96a_987_925</code> 山濤（7 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 山濤 | [《晉書・山濤 王戎 郭舒 樂廣》][126] | [JSON](96a_987_925.json) |
| `A` | 山該〔字伯倫〕 | [《晉書・山濤 王戎 郭舒 樂廣》][126] | [JSON](96a_987_925_A.json) |
| `AA` | 山瑋〔字彥祖〕 | [《晉書・山濤 王戎 郭舒 樂廣》][126] | [JSON](96a_987_925_AA.json) |
| `AB` | 山世回 | [《晉書・山濤 王戎 郭舒 樂廣》][126] | [JSON](96a_987_925_AB.json) |
| `B` | 山淳〔字子玄〕 | [《晉書・山濤 王戎 郭舒 樂廣》][126] | [JSON](96a_987_925_B.json) |
| `C` | 山允〔字叔真〕 | [《晉書・山濤 王戎 郭舒 樂廣》][126] | [JSON](96a_987_925_C.json) |
| `D` | 山謨〔字季長〕 | [《晉書・山濤 王戎 郭舒 樂廣》][126] | [JSON](96a_987_925_D.json) |

</details>

<details><summary><code>98i_dd4_aof</code> 多同（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 多同 | [《史記・西南夷列傳》][664] | [JSON](98i_dd4_aof.json) |
| `A` | 多同子 | [《史記・西南夷列傳》][664] | [JSON](98i_dd4_aof_A.json) |

</details>

<details><summary><code>98q_mll_d6v</code> 蕭道生（5 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 蕭道生 | [《南史・齊宗室》][522] | [JSON](98q_mll_d6v.json) |
| `A` | 蕭鳳 | [《南齊書・宗室》][352]、[《南齊書・宗室》][353]、[《南史・齊宗室》][522] | [JSON](98q_mll_d6v_A.json) |
| `AA` | 蕭遙光 | [《南齊書・王融 謝朓》][358] | [JSON](98q_mll_d6v_AA.json) |
| `B` | 蕭緬（字景業，安陸昭王） | [《南史・齊宗室》][522] | [JSON](98q_mll_d6v_B.json) |
| `BA` | 蕭寶晊（安陸王緬子，湘東王） | [《南史・王誕　王華　王惠　王彧》][486]、[《南史・齊宗室》][522] | [JSON](98q_mll_d6v_BA.json) |

</details>

<details><summary><code>995_xas_r98</code> 申（蔡昭侯）（6 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 申（蔡昭侯） | [《史記・管蔡世家》][583] | [JSON](995_xas_r98.json) |
| `A` | 朔（蔡成侯） | [《史記・管蔡世家》][583] | [JSON](995_xas_r98_A.json) |
| `AA` | 產（蔡聲侯） | [《史記・管蔡世家》][583]、[《史記・六國年表》][897] | [JSON](995_xas_r98_AA.json) |
| `AAA` | 元侯（蔡君） | [《史記・管蔡世家》][583] | [JSON](995_xas_r98_AAA.json) |
| `AAAA` | 齊（蔡末侯） | [《史記・管蔡世家》][583] | [JSON](995_xas_r98_AAAA.json) |
| `B` | 蔡昭侯質吳子（未名） | [《史記・管蔡世家》][583] | [JSON](995_xas_r98_B.json) |

</details>

<details><summary><code>9ac_ddl_9iz</code> 殷元素（殷寧父，宋南康相）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 殷元素（殷寧父，宋南康相） | [《南齊書・王奐 從弟繢 張沖》][368]、[《南史・范岫　傅昭　孔休源　江革　徐勉　許懋　殷鈞》][536] | [JSON](9ac_ddl_9iz.json) |
| `A` | 殷寧（殷元素子、殷叡父） | [《南史・范岫　傅昭　孔休源　江革　徐勉　許懋　殷鈞》][536] | [JSON](9ac_ddl_9iz_A.json) |

</details>

<details><summary><code>9c5_a31_807</code> 武沈（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 武沈 | [《晉書・庾亮》][181] | [JSON](9c5_a31_807.json) |
| `A` | 武遵 | [《晉書・庾亮》][181] | [JSON](9c5_a31_807_A.json) |

</details>

<details><summary><code>9fa_127_a71</code> 務勿塵（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 務勿塵 | [《晉書・王沈 荀顗 荀勖 馮紞》][119] | [JSON](9fa_127_a71.json) |
| `A` | 疾陸眷 | [《晉書・王沈 荀顗 荀勖 馮紞》][119] | [JSON](9fa_127_a71_A.json) |

</details>

<details><summary><code>9nr_qwg_vuf</code> 叔孫宣伯（魯）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 叔孫宣伯（魯） | [《史記・齊太公世家》][580] | [JSON](9nr_qwg_vuf.json) |
| `A` | 景公母（叔孫宣伯女） | [《史記・齊太公世家》][580] | [JSON](9nr_qwg_vuf_A.json) |

</details>

<details><summary><code>9oa_4bh_lmd</code> 鄭伯（楚莊王圍鄭時）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 鄭伯（楚莊王圍鄭時） | [《史記・鄭世家》][590] | [JSON](9oa_4bh_lmd.json) |
| `A` | 沸 | [《史記・鄭世家》][590] | [JSON](9oa_4bh_lmd_A.json) |

</details>

<details><summary><code>9w2_c77_53m</code> 齊桓公（12 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 齊桓公 | [《史記・齊太公世家》][580] | [JSON](9w2_c77_53m.json) |
| `A` | 元（齊惠公） | [《史記・齊太公世家》][580] | [JSON](9w2_c77_53m_A.json) |
| `AA` | 無野（齊頃公） | [《史記・齊太公世家》][580] | [JSON](9w2_c77_53m_AA.json) |
| `AAA` | 環（齊靈公） | [《史記・齊太公世家》][580] | [JSON](9w2_c77_53m_AAA.json) |
| `AAAA` | 齊莊公（崔杼時） | [《史記・齊太公世家》][580] | [JSON](9w2_c77_53m_AAAA.json) |
| `B` | 無詭（齊桓公子） | [《史記・齊太公世家》][580] | [JSON](9w2_c77_53m_B.json) |
| `C` | 昭（齊孝公） | [《史記・齊太公世家》][580] | [JSON](9w2_c77_53m_C.json) |
| `D` | 潘（齊昭公） | [《史記・齊太公世家》][580] | [JSON](9w2_c77_53m_D.json) |
| `DA` | 舍（齊昭公子） | [《史記・齊太公世家》][580] | [JSON](9w2_c77_53m_DA.json) |
| `E` | 商人（齊懿公） | [《史記・齊太公世家》][580] | [JSON](9w2_c77_53m_E.json) |
| `F` | 雍（齊桓公子） | [《史記・齊太公世家》][580]、[《史記・楚世家》][588] | [JSON](9w2_c77_53m_F.json) |
| `G` | 齊姜（申生母） | [《史記・晉世家》][587] | [JSON](9w2_c77_53m_G.json) |

</details>

<details><summary><code>9w8_tqh_ysn</code> 陳寔（17 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 陳寔 | [《後漢書・荀韓鍾陳列傳》][53] | [JSON](9w8_tqh_ysn.json) |
| `A` | 紀（陳羣父） | [《後漢書・荀韓鍾陳列傳》][53]、[《三國志・桓二陳徐衞盧傳》][556] | [JSON](9w8_tqh_ysn_A.json) |
| `AA` | 陳群 | [《三國志・桓二陳徐衞盧傳》][556] | [JSON](9w8_tqh_ysn_AA.json) |
| `AAA` | 陳泰 | [《三國志・桓二陳徐衞盧傳》][556] | [JSON](9w8_tqh_ysn_AAA.json) |
| `AAAA` | 恂（陳泰子） | [《三國志・桓二陳徐衞盧傳》][556] | [JSON](9w8_tqh_ysn_AAAA.json) |
| `AAB` | 陳羣未名另封子 | [《三國志・桓二陳徐衞盧傳》][556] | [JSON](9w8_tqh_ysn_AAB.json) |
| `B` | 諶（陳羣叔父） | [《三國志・桓二陳徐衞盧傳》][556] | [JSON](9w8_tqh_ysn_B.json) |
| `B*A` | 佐（陳諶孫）（來源候選；預設不接父系） | [《三國志・桓二陳徐衞盧傳》][556] | [JSON](9w8_tqh_ysn_B%2AA.json) |
| `B*AA` | 凖（陳佐子） | [《新唐書・宰相世系一下》][871] | [JSON](9w8_tqh_ysn_B%2AAA.json) |
| `B*AA*A` | 逵（字林道） | [《三國志・桓二陳徐衞盧傳》][556] | [JSON](9w8_tqh_ysn_B%2AAA%2AA.json) |
| `B*AB` | 戴（凖弟） | [《三國志・桓二陳徐衞盧傳》][556] | [JSON](9w8_tqh_ysn_B%2AAB.json) |
| `B*AC` | 徵（凖弟） | [《三國志・桓二陳徐衞盧傳》][556] | [JSON](9w8_tqh_ysn_B%2AAC.json) |
| `B*B` | 坦（陳佐弟） | [《三國志・桓二陳徐衞盧傳》][556] | [JSON](9w8_tqh_ysn_B%2AB.json) |
| `C` | 夔〔新唐陳氏序〕 | [《新唐書・宰相世系一下》][871] | [JSON](9w8_tqh_ysn_C.json) |
| `D` | 洽〔新唐陳氏序〕 | [《新唐書・宰相世系一下》][871] | [JSON](9w8_tqh_ysn_D.json) |
| `E` | 休〔新唐陳氏序〕 | [《新唐書・宰相世系一下》][871] | [JSON](9w8_tqh_ysn_E.json) |
| `F` | 光〔新唐陳氏序〕 | [《新唐書・宰相世系一下》][871] | [JSON](9w8_tqh_ysn_F.json) |

</details>

<details><summary><code>9yf_c3t_x2w</code> 衛君父引古未名（李斯列傳候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 衛君父引古未名 | [《史記・李斯列傳》][635] | [JSON](9yf_c3t_x2w.json) |
| `A` | 衛君引古未名 | [《史記・李斯列傳》][635] | [JSON](9yf_c3t_x2w_A.json) |

</details>

<details><summary><code>9zj_vf7_86a</code> 薄氏〔薄太后之父；靈文侯〕（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 薄氏〔薄太后之父；靈文侯〕 | [《史記・外戚世家》][597] | [JSON](9zj_vf7_86a.json) |
| `A` | 薄太后（孝文帝母） | [《史記・外戚世家》][597] | [JSON](9zj_vf7_86a_A.json) |

</details>

<details><summary><code>a04_d8f_416</code> 王允之（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 王允之 | [《晉書・王舒 王廙 虞潭 顧眾 張闓》][192] | [JSON](a04_d8f_416.json) |
| `A` | 王晞之 | [《晉書・王舒 王廙 虞潭 顧眾 張闓》][192] | [JSON](a04_d8f_416_A.json) |
| `AA` | 王肇之 | [《晉書・王舒 王廙 虞潭 顧眾 張闓》][192] | [JSON](a04_d8f_416_AA.json) |

</details>

<details><summary><code>a13_5fp_pek</code> 梁襄王（趙世家候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 梁襄王 | [《史記・趙世家》][591] | [JSON](a13_5fp_pek.json) |
| `A` | 嗣 | [《史記・趙世家》][591] | [JSON](a13_5fp_pek_A.json) |

</details>

<details><summary><code>a1f_f17_ccb</code> 荀衢（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 荀衢 | [《三國志・二荀賈傳》][543] | [JSON](a1f_f17_ccb.json) |
| `A` | 荀祈 | [《三國志・二荀賈傳》][543] | [JSON](a1f_f17_ccb_A.json) |

</details>

<details><summary><code>a28_f5c_105</code> 曹洪（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 曹洪 | [《三國志・二荀賈傳》][543] | [JSON](a28_f5c_105.json) |
| `A` | 曹氏（荀粲妻，曹洪女） | [《三國志・二荀賈傳》][543] | [JSON](a28_f5c_105_A.json) |

</details>

<details><summary><code>a7k_sl0_d7u</code> 金王孫（外戚世家候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 金王孫 | [《史記・外戚世家》][597] | [JSON](a7k_sl0_d7u.json) |
| `A` | 修成君 | [《史記・外戚世家》][597]、[《史記・淮南衡山列傳》][666] | [JSON](a7k_sl0_d7u_A.json) |

</details>

<details><summary><code>a8f_ec8_e74</code> 王澤（18 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 王澤 | [《三國志・徐胡二王傳》][560] | [JSON](a8f_ec8_e74.json) |
| `A` | 王昶 | [《三國志・徐胡二王傳》][560] | [JSON](a8f_ec8_e74_A.json) |
| `AA` | 王湛 | [《晉書・王湛 荀崧 范汪 劉惔 張憑 韓伯》][185] | [JSON](a8f_ec8_e74_AA.json) |
| `AAA` | 王承 | [《晉書・王湛 荀崧 范汪 劉惔 張憑 韓伯》][185] | [JSON](a8f_ec8_e74_AAA.json) |
| `AAAA` | 王述 | [《晉書・王湛 荀崧 范汪 劉惔 張憑 韓伯》][185] | [JSON](a8f_ec8_e74_AAAA.json) |
| `AAAAA` | 王坦之 | [《晉書・王湛 荀崧 范汪 劉惔 張憑 韓伯》][185] | [JSON](a8f_ec8_e74_AAAAA.json) |
| `AAAAAA` | 王愷 | [《晉書・王湛 荀崧 范汪 劉惔 張憑 韓伯》][185] | [JSON](a8f_ec8_e74_AAAAAA.json) |
| `AAAAAB` | 王愉 | [《晉書・王湛 荀崧 范汪 劉惔 張憑 韓伯》][185] | [JSON](a8f_ec8_e74_AAAAAB.json) |
| `AAAAABA` | 王綏 | [《晉書・王湛 荀崧 范汪 劉惔 張憑 韓伯》][185] | [JSON](a8f_ec8_e74_AAAAABA.json) |
| `AAAAAC` | 王國寶 | [《晉書・王湛 荀崧 范汪 劉惔 張憑 韓伯》][185] | [JSON](a8f_ec8_e74_AAAAAC.json) |
| `AAAAAD` | 王忱 | [《晉書・王湛 荀崧 范汪 劉惔 張憑 韓伯》][185] | [JSON](a8f_ec8_e74_AAAAAD.json) |
| `AB` | 王渾 | [《晉書・王渾 王濬 唐彬》][121] | [JSON](a8f_ec8_e74_AB.json) |
| `ABA` | 王尚 | [《晉書・王渾 王濬 唐彬》][121] | [JSON](a8f_ec8_e74_ABA.json) |
| `ABB` | 王濟 | [《晉書・王渾 王濬 唐彬》][121] | [JSON](a8f_ec8_e74_ABB.json) |
| `ABBA` | 王卓 | [《晉書・王渾 王濬 唐彬》][121] | [JSON](a8f_ec8_e74_ABBA.json) |
| `ABBB` | 王聿 | [《晉書・王渾 王濬 唐彬》][121] | [JSON](a8f_ec8_e74_ABBB.json) |
| `ABC` | 王澄〔王濟弟〕 | [《晉書・王渾 王濬 唐彬》][121] | [JSON](a8f_ec8_e74_ABC.json) |
| `AC` | 王深（字道冲，王昶子） | [《三國志・徐胡二王傳》][560] | [JSON](a8f_ec8_e74_AC.json) |

</details>

<details><summary><code>a9m_987_rss</code> 叔牙（莊公弟）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 叔牙（莊公弟） | [《史記・魯周公世家》][581] | [JSON](a9m_987_rss.json) |
| `A` | 叔牙子（未名） | [《史記・魯周公世家》][581] | [JSON](a9m_987_rss_A.json) |

</details>

<details><summary><code>a9v_t0d_3va</code> 晉惠公（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 晉惠公 | [《史記・晉世家》][587] | [JSON](a9v_t0d_3va.json) |
| `A` | 晉懷公 | [《史記・晉世家》][587] | [JSON](a9v_t0d_3va_A.json) |
| `B` | 妾（梁伯女所生女） | [《史記・晉世家》][587] | [JSON](a9v_t0d_3va_B.json) |

</details>

<details><summary><code>aa6_83c_juy</code> 謝裒（65 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 謝裒 | [《南史・謝晦　謝裕　謝方明　謝靈運》][429] | [JSON](aa6_83c_juy.json) |
| `A` | 謝據 | [《南史・謝晦　謝裕　謝方明　謝靈運》][429] | [JSON](aa6_83c_juy_A.json) |
| `AA` | 謝朗 | [《晉書・謝尚 謝安》][195] | [JSON](aa6_83c_juy_AA.json) |
| `AAA` | 謝重 | [《晉書・謝尚 謝安》][195] | [JSON](aa6_83c_juy_AAA.json) |
| `AAA*A` | 謝紹 | [《南史・謝晦　謝裕　謝方明　謝靈運》][429]、[《宋書・謝晦》][761]、[《宋書・謝晦》][762] | [JSON](aa6_83c_juy_AAA%2AA.json) |
| `AAA*B` | 謝世猷 | [《宋書・謝晦》][761]、[《宋書・謝晦》][762] | [JSON](aa6_83c_juy_AAA%2AB.json) |
| `AAAA` | 謝晦 | [《宋書・謝晦》][761] | [JSON](aa6_83c_juy_AAAA.json) |
| `AAAAA` | 謝世休 | [《宋書・謝晦》][761]、[《宋書・謝晦》][762] | [JSON](aa6_83c_juy_AAAAA.json) |
| `AAAAB` | 謝晦女（彭城王義康妃） | [《南史・謝晦　謝裕　謝方明　謝靈運》][429] | [JSON](aa6_83c_juy_AAAAB.json) |
| `AAAB` | 謝絢 | [《晉書・謝尚 謝安》][195]、[《南史・謝晦　謝裕　謝方明　謝靈運》][429] | [JSON](aa6_83c_juy_AAAB.json) |
| `AAABA` | 謝世基 | [《宋書・謝晦》][761]、[《宋書・謝晦》][762] | [JSON](aa6_83c_juy_AAABA.json) |
| `AAAC` | 謝氏（荀伯子妻） | [《宋書・范泰 王准之 王韶之 荀伯子》][789] | [JSON](aa6_83c_juy_AAAC.json) |
| `AAAD` | 謝瞻 | [《宋書・謝瞻 孔琳之》][781] | [JSON](aa6_83c_juy_AAAD.json) |
| `AAAE` | 㬭 | [《宋書・謝瞻 孔琳之》][781] | [JSON](aa6_83c_juy_AAAE.json) |
| `AAAEA` | 世平 | [《南史・謝晦　謝裕　謝方明　謝靈運》][429]、[《宋書・謝晦》][761]、[《宋書・謝晦》][762]、[《宋書・謝瞻 孔琳之》][781] | [JSON](aa6_83c_juy_AAAEA.json) |
| `AAAF` | 謝遯 | [《宋書・謝晦》][761]、[《宋書・謝晦》][762] | [JSON](aa6_83c_juy_AAAF.json) |
| `AB` | 謝允 | [《南史・謝晦　謝裕　謝方明　謝靈運》][433] | [JSON](aa6_83c_juy_AB.json) |
| `ABA` | 謝純 | [《宋書・庾悅 王誕 謝景仁 袁湛 褚叔度》][774] | [JSON](aa6_83c_juy_ABA.json) |
| `ABA*A` | 謝沈（謝純孫） | [《宋書・庾悅 王誕 謝景仁 袁湛 褚叔度》][774] | [JSON](aa6_83c_juy_ABA%2AA.json) |
| `ABB` | 謝甝 | [《南史・謝晦　謝裕　謝方明　謝靈運》][431] | [JSON](aa6_83c_juy_ABB.json) |
| `ABC` | 謝述 | [《宋書・庾悅 王誕 謝景仁 袁湛 褚叔度》][776] | [JSON](aa6_83c_juy_ABC.json) |
| `ABCA` | 謝約 | [《宋書・庾悅 王誕 謝景仁 袁湛 褚叔度》][776] | [JSON](aa6_83c_juy_ABCA.json) |
| `ABCB` | 謝緯 | [《宋書・庾悅 王誕 謝景仁 袁湛 褚叔度》][776] | [JSON](aa6_83c_juy_ABCB.json) |
| `ABCBA` | 謝朓 | [《南史・謝晦　謝裕　謝方明　謝靈運》][432] | [JSON](aa6_83c_juy_ABCBA.json) |
| `ABCBAA` | 謝謨 | [《南史・謝晦　謝裕　謝方明　謝靈運》][432] | [JSON](aa6_83c_juy_ABCBAA.json) |
| `B` | 謝安 | [《晉書・謝尚 謝安》][195] | [JSON](aa6_83c_juy_B.json) |
| `B*A` | 謝璞 | [《南史・謝晦　謝裕　謝方明　謝靈運》][430] | [JSON](aa6_83c_juy_B%2AA.json) |
| `BA` | 謝琰 | [《晉書・謝尚 謝安》][195] | [JSON](aa6_83c_juy_BA.json) |
| `BAA` | 謝肇 | [《晉書・謝尚 謝安》][195] | [JSON](aa6_83c_juy_BAA.json) |
| `BAB` | 謝峻 | [《晉書・謝尚 謝安》][195] | [JSON](aa6_83c_juy_BAB.json) |
| `BAC` | 謝混 | [《南史・謝弘微》][436] | [JSON](aa6_83c_juy_BAC.json) |
| `BACA` | 謝氏（殷叡妻） | [《宋書・王惠 謝弘微 王球》][784] | [JSON](aa6_83c_juy_BACA.json) |
| `BB` | 謝氏（王瑉妻） | [《晉書・謝尚 謝安》][195] | [JSON](aa6_83c_juy_BB.json) |
| `C` | 謝奕 | [《晉書・謝尚 謝安》][195] | [JSON](aa6_83c_juy_C.json) |
| `CA` | 謝康 | [《晉書・謝尚 謝安》][195] | [JSON](aa6_83c_juy_CA.json) |
| `CB` | 謝泉 | [《晉書・謝尚 謝安》][195] | [JSON](aa6_83c_juy_CB.json) |
| `CC` | 謝靖 | [《晉書・謝尚 謝安》][195] | [JSON](aa6_83c_juy_CC.json) |
| `CD` | 謝玄 | [《晉書・謝尚 謝安》][195] | [JSON](aa6_83c_juy_CD.json) |
| `CDA` | 謝瑍 | [《晉書・謝尚 謝安》][195] | [JSON](aa6_83c_juy_CDA.json) |
| `CDAA` | 謝靈運 | [《宋書・謝靈運》][798] | [JSON](aa6_83c_juy_CDAA.json) |
| `CDAAA` | 鳯（謝靈運子） | [《宋書・謝靈運》][798] | [JSON](aa6_83c_juy_CDAAA.json) |
| `CDAAB` | 謝鳳 | [《南史・謝晦　謝裕　謝方明　謝靈運》][418] | [JSON](aa6_83c_juy_CDAAB.json) |
| `CDAABA` | 謝超宗 | [《南齊書・謝超宗 劉祥》][337]、[《南齊書・謝超宗 劉祥》][336] | [JSON](aa6_83c_juy_CDAABA.json) |
| `CDAABAA` | 謝才卿 | [《南齊書・謝超宗 劉祥》][335]、[《南齊書・謝超宗 劉祥》][337]、[《南齊書・謝超宗 劉祥》][336]、[《南史・謝晦　謝裕　謝方明　謝靈運》][426] | [JSON](aa6_83c_juy_CDAABAA.json) |
| `CDAABAAA` | 謝藻 | [《梁書・文學下》][273]、[《梁書・文學下》][274]、[《梁書・文學下》][275]、[《南史・謝晦　謝裕　謝方明　謝靈運》][434] | [JSON](aa6_83c_juy_CDAABAAA.json) |
| `CDAABAB` | 謝幾卿 | [《梁書・文學下》][273]、[《梁書・文學下》][274] | [JSON](aa6_83c_juy_CDAABAB.json) |
| `CE` | 謝道韞 | [《晉書・列女》][215]、[《晉書・列女》][216] | [JSON](aa6_83c_juy_CE.json) |
| `D` | 謝萬 | [《晉書・謝尚 謝安》][195] | [JSON](aa6_83c_juy_D.json) |
| `DA` | 謝氏（王珣妻） | [《晉書・謝尚 謝安》][195] | [JSON](aa6_83c_juy_DA.json) |
| `DB` | 謝韶 | [《晉書・謝尚 謝安》][195] | [JSON](aa6_83c_juy_DB.json) |
| `DBA` | 謝思 | [《南史・謝弘微》][436]、[《宋書・王惠 謝弘微 王球》][784] | [JSON](aa6_83c_juy_DBA.json) |
| `DBAA` | 謝曜 | [《南史・謝弘微》][436] | [JSON](aa6_83c_juy_DBAA.json) |
| `DBAB` | 謝弘微 | [《宋書・王惠 謝弘微 王球》][784] | [JSON](aa6_83c_juy_DBAB.json) |
| `DBABA` | 謝莊 | [《宋書・謝莊 王景文》][819] | [JSON](aa6_83c_juy_DBABA.json) |
| `DBABAA` | 謝颺 | [《南齊書・江斆 何昌㝢 謝𤅢 王思遠》][350]、[《南史・后妃上》][400]、[《宋書・謝莊 王景文》][819] | [JSON](aa6_83c_juy_DBABAA.json) |
| `DBABAAA` | 謝梵境〔宋順帝皇后〕 | [《南史・后妃上》][400]、[《宋書・后妃》][758]、[《宋書・后妃》][757]、[《宋書・謝莊 王景文》][819] | [JSON](aa6_83c_juy_DBABAAA.json) |
| `DBABAB` | 謝朏 | [《梁書・謝朏 弟子覽》][243] | [JSON](aa6_83c_juy_DBABAB.json) |
| `DBABABA` | 諼〔謝朏子〕 | [《梁書・謝朏 弟子覽》][243] | [JSON](aa6_83c_juy_DBABABA.json) |
| `DBABABB` | 篹〔謝朏次子〕 | [《梁書・謝朏 弟子覽》][243] | [JSON](aa6_83c_juy_DBABABB.json) |
| `DBABAC` | 謝𤅢〔字義潔〕 | [《南齊書・江斆 何昌㝢 謝𤅢 王思遠》][350] | [JSON](aa6_83c_juy_DBABAC.json) |
| `DBABACA` | 謝舉（字言揚） | [《梁書・王僧孺 張率 劉孝綽 王筠》][266]、[《梁書・王僧孺 張率 劉孝綽 王筠》][265]、[《南史・謝弘微》][437] | [JSON](aa6_83c_juy_DBABACA.json) |
| `DBABAD` | 顥〔謝𤅢兄，字仁悠〕 | [《南齊書・江斆 何昌㝢 謝𤅢 王思遠》][350] | [JSON](aa6_83c_juy_DBABAD.json) |
| `DBABAE` | 嵷〔謝𤅢兄〕 | [《南齊書・江斆 何昌㝢 謝𤅢 王思遠》][350] | [JSON](aa6_83c_juy_DBABAE.json) |
| `E` | 謝石 | [《晉書・謝尚 謝安》][195] | [JSON](aa6_83c_juy_E.json) |
| `EA` | 謝汪 | [《晉書・謝尚 謝安》][195] | [JSON](aa6_83c_juy_EA.json) |

</details>

<details><summary><code>aa9_7e9_5b9</code> 魯宗之（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 魯宗之 | [《晉書・桓彝》][183] | [JSON](aa9_7e9_5b9.json) |
| `A` | 魯軌 | [《魏書・刁雍 王慧龍 韓延之 袁式》][852] | [JSON](aa9_7e9_5b9_A.json) |

</details>

<details><summary><code>acg_se3_w5x</code> 周呂侯（呂后兄）（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 周呂侯（呂后兄） | [《史記・呂后本紀》][575] | [JSON](acg_se3_w5x.json) |
| `A` | 呂台 | [《史記・呂后本紀》][575] | [JSON](acg_se3_w5x_A.json) |
| `B` | 呂產 | [《史記・呂后本紀》][575] | [JSON](acg_se3_w5x_B.json) |

</details>

<details><summary><code>acp_3ec_zvn</code> 李頡（李郃父）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 李頡（李郃父） | [《後漢書・方術列傳》][58] | [JSON](acp_3ec_zvn.json) |
| `A` | 李郃（字孟節） | [《後漢書・方術列傳》][58] | [JSON](acp_3ec_zvn_A.json) |

</details>

<details><summary><code>ae2_620_2bc</code> 袁渙（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 袁渙 | [《三國志・袁張涼國田王邴管傳》][545] | [JSON](ae2_620_2bc.json) |
| `A` | 袁㝢 | [《三國志・袁張涼國田王邴管傳》][545] | [JSON](ae2_620_2bc_A.json) |
| `B` | 袁準 | [《三國志・袁張涼國田王邴管傳》][545] | [JSON](ae2_620_2bc_B.json) |

</details>

<details><summary><code>ae4_588_bdb</code> 鄭泰（7 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 鄭泰 | [《晉書・鄭袤 李胤 盧欽 華表 石鑒 溫羨》][147] | [JSON](ae4_588_bdb.json) |
| `A` | 鄭袤〔字林叔〕 | [《晉書・鄭袤 李胤 盧欽 華表 石鑒 溫羨》][147] | [JSON](ae4_588_bdb_A.json) |
| `AA` | 鄭質〔鄭袤子〕 | [《晉書・鄭袤 李胤 盧欽 華表 石鑒 溫羨》][147] | [JSON](ae4_588_bdb_AA.json) |
| `AB` | 鄭舒〔鄭袤子〕 | [《晉書・鄭袤 李胤 盧欽 華表 石鑒 溫羨》][147] | [JSON](ae4_588_bdb_AB.json) |
| `AC` | 鄭詡〔鄭袤子〕 | [《晉書・鄭袤 李胤 盧欽 華表 石鑒 溫羨》][147] | [JSON](ae4_588_bdb_AC.json) |
| `AD` | 鄭稱〔鄭袤子〕 | [《晉書・鄭袤 李胤 盧欽 華表 石鑒 溫羨》][147] | [JSON](ae4_588_bdb_AD.json) |
| `AE` | 鄭予〔鄭袤子〕 | [《晉書・鄭袤 李胤 盧欽 華表 石鑒 溫羨》][147] | [JSON](ae4_588_bdb_AE.json) |

</details>

<details><summary><code>ae7_dcf_084</code> 范汪（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 范汪 | [《晉書・庾亮》][181]、[《晉書・謝尚 謝安》][195]、[《世說新語・方正》][698]、[《宋書・范泰 王准之 王韶之 荀伯子》][786] | [JSON](ae7_dcf_084.json) |
| `A` | 范蓋（范汪女，王坦之妻） | [《世說新語・方正》][698] | [JSON](ae7_dcf_084_A.json) |

</details>

<details><summary><code>afj_vl8_7fu</code> 安丘侯説（萬石張叔列傳候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 安丘侯説 | [《史記・萬石張叔列傳》][651] | [JSON](afj_vl8_7fu.json) |
| `A` | 張歐 | [《史記・萬石張叔列傳》][651] | [JSON](afj_vl8_7fu_A.json) |

</details>

<details><summary><code>agx_sqm_4ou</code> 張耳（5 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 張耳 | [《史記・張耳陳餘列傳》][637] | [JSON](agx_sqm_4ou.json) |
| `A` | 張敖 | [《史記・張耳陳餘列傳》][637] | [JSON](agx_sqm_4ou_A.json) |
| `AA` | 張偃 | [《史記・呂后本紀》][575]、[《史記・張耳陳餘列傳》][637] | [JSON](agx_sqm_4ou_AA.json) |
| `AB` | 張壽 | [《史記・張耳陳餘列傳》][637] | [JSON](agx_sqm_4ou_AB.json) |
| `AC` | 張侈 | [《史記・張耳陳餘列傳》][637] | [JSON](agx_sqm_4ou_AC.json) |

</details>

<details><summary><code>ao3_0fy_d45</code> 秦昭王（6 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 秦昭王 | [《史記・范睢蔡澤列傳》][627] | [JSON](ao3_0fy_d45.json) |
| `A` | 秦孝文王 | [《史記・呂不韋列傳》][633] | [JSON](ao3_0fy_d45_A.json) |
| `AA` | 秦莊襄王 | [《史記・呂不韋列傳》][633] | [JSON](ao3_0fy_d45_AA.json) |
| `AAA` | 秦始皇帝 | [《史記・秦始皇本紀》][572] | [JSON](ao3_0fy_d45_AAA.json) |
| `AAAA` | 胡亥 | [《史記・秦始皇本紀》][572] | [JSON](ao3_0fy_d45_AAAA.json) |
| `AAAB` | 扶蘇 | [《史記・李斯列傳》][635] | [JSON](ao3_0fy_d45_AAAB.json) |

</details>

<details><summary><code>apr_7dg_tdd</code> 謝方明（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 謝方明 | [《宋書・張茂度 庾登之 謝方明 江夷》][778] | [JSON](apr_7dg_tdd.json) |
| `A` | 惠連 | [《宋書・謝靈運》][798] | [JSON](apr_7dg_tdd_A.json) |

</details>

<details><summary><code>ath_xsq_n4i</code> 魯定公（11 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 魯定公 | [《史記・魯周公世家》][581] | [JSON](ath_xsq_n4i.json) |
| `A` | 魯哀公 | [《史記・魯周公世家》][581] | [JSON](ath_xsq_n4i_A.json) |
| `AA` | 寧（魯悼公） | [《史記・魯周公世家》][581] | [JSON](ath_xsq_n4i_AA.json) |
| `AAA` | 嘉（魯元公） | [《史記・魯周公世家》][581] | [JSON](ath_xsq_n4i_AAA.json) |
| `AAAA` | 顯（魯穆公） | [《史記・魯周公世家》][581] | [JSON](ath_xsq_n4i_AAAA.json) |
| `AAAAA` | 奮（魯共公） | [《史記・魯周公世家》][581] | [JSON](ath_xsq_n4i_AAAAA.json) |
| `AAAAAA` | 屯（魯康公） | [《史記・魯周公世家》][581] | [JSON](ath_xsq_n4i_AAAAAA.json) |
| `AAAAAAA` | 匽（魯景公） | [《史記・魯周公世家》][581] | [JSON](ath_xsq_n4i_AAAAAAA.json) |
| `AAAAAAAA` | 叔（魯平公） | [《史記・魯周公世家》][581] | [JSON](ath_xsq_n4i_AAAAAAAA.json) |
| `AAAAAAAAA` | 賈（魯文公） | [《史記・魯周公世家》][581] | [JSON](ath_xsq_n4i_AAAAAAAAA.json) |
| `AAAAAAAAAA` | 讎（魯頃公） | [《史記・魯周公世家》][581] | [JSON](ath_xsq_n4i_AAAAAAAAAA.json) |

</details>

<details><summary><code>b0c_13f_c3a</code> 王衍（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 王衍 | [《晉書・山濤 王戎 郭舒 樂廣》][130] | [JSON](b0c_13f_c3a.json) |
| `A` | 王衍長女〔賈后為謐聘之〕 | — | [JSON](b0c_13f_c3a_A.json) |

</details>

<details><summary><code>b1r_inb_fts</code> 樊噲（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 樊噲 | [《史記・樊酈滕灌列傳》][643] | [JSON](b1r_inb_fts.json) |
| `A` | 樊市人 | [《史記・樊酈滕灌列傳》][643] | [JSON](b1r_inb_fts_A.json) |
| `B` | 樊伉 | [《史記・樊酈滕灌列傳》][643] | [JSON](b1r_inb_fts_B.json) |

</details>

<details><summary><code>b21_e55_8bd</code> 劉琨（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 劉琨 | [《晉書・溫嶠 郗鑒》][171] | [JSON](b21_e55_8bd.json) |
| `A` | 劉群〔劉琨子〕 | [《晉書・劉琨 祖逖》][163] | [JSON](b21_e55_8bd_A.json) |

</details>

<details><summary><code>bdx_txf_e62</code> 垣敞（垣護之祖）（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 垣敞（垣護之祖） | [《宋書・胡藩 劉康祖 垣護之 張興世》][768] | [JSON](bdx_txf_e62.json) |
| `A` | 垣苗（垣護之父） | [《宋書・胡藩 劉康祖 垣護之 張興世》][768] | [JSON](bdx_txf_e62_A.json) |
| `AA` | 垣護之（字彥宗） | [《宋書・朱脩之 宗愨 王玄謨》][808] | [JSON](bdx_txf_e62_AA.json) |

</details>

<details><summary><code>bm8_bzq_1ee</code> 觀起（蔡大夫）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 觀起（蔡大夫） | [《史記・楚世家》][588] | [JSON](bm8_bzq_1ee.json) |
| `A` | 觀從（楚變亂謀者） | [《史記・楚世家》][588] | [JSON](bm8_bzq_1ee_A.json) |

</details>

<details><summary><code>bn4_lhp_9h1</code> 姑容（杞桓公）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 姑容（杞桓公） | [《史記・陳杞世家》][584] | [JSON](bn4_lhp_9h1.json) |
| `A` | 丐（杞孝公） | [《史記・陳杞世家》][584] | [JSON](bn4_lhp_9h1_A.json) |

</details>

<details><summary><code>buv_igi_gpn</code> 帝乙（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 帝乙 | [《史記・殷本紀》][569] | [JSON](buv_igi_gpn.json) |
| `A` | 微子啓 | [《史記・宋微子世家》][586] | [JSON](buv_igi_gpn_A.json) |

</details>

<details><summary><code>bvb_d1z_fd0</code> 尉佗（6 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 尉佗 | [《史記・南越列傳》][661] | [JSON](bvb_d1z_fd0.json) |
| `*A` | 胡 | [《史記・南越列傳》][661] | [JSON](bvb_d1z_fd0_%2AA.json) |
| `*AA` | 嬰齊 | [《史記・南越列傳》][661] | [JSON](bvb_d1z_fd0_%2AAA.json) |
| `*AAA` | 興 | [《史記・南越列傳》][661] | [JSON](bvb_d1z_fd0_%2AAAA.json) |
| `*AAB` | 次公 | [《史記・南越列傳》][661] | [JSON](bvb_d1z_fd0_%2AAAB.json) |
| `*AAC` | 建德 | [《史記・南越列傳》][661] | [JSON](bvb_d1z_fd0_%2AAAC.json) |

</details>

<details><summary><code>bwv_ob8_6xi</code> 共敖（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 共敖 | [《史記・項羽本紀》][573]、[《史記・秦楚之際月表》][898] | [JSON](bwv_ob8_6xi.json) |
| `A` | 共尉 | [《史記・荊燕世家》][599]、[《史記・秦楚之際月表》][898] | [JSON](bwv_ob8_6xi_A.json) |

</details>

<details><summary><code>c0i_eah_y59</code> 咎（韓世家釐王候選）（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 咎 | [《史記・韓世家》][593] | [JSON](c0i_eah_y59.json) |
| `A` | 桓惠王 | [《史記・韓世家》][593] | [JSON](c0i_eah_y59_A.json) |
| `AA` | 韓王安 | [《史記・韓世家》][593]、[《史記・六國年表》][897] | [JSON](c0i_eah_y59_AA.json) |

</details>

<details><summary><code>c19_xxo_r8f</code> 直不疑（萬石張叔列傳候選）（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 直不疑 | [《史記・萬石張叔列傳》][651] | [JSON](c19_xxo_r8f.json) |
| `*A` | 望（直不疑孫） | [《史記・萬石張叔列傳》][651] | [JSON](c19_xxo_r8f_%2AA.json) |
| `A` | 相如（直不疑子） | [《史記・萬石張叔列傳》][651] | [JSON](c19_xxo_r8f_A.json) |

</details>

<details><summary><code>c1t_5mz_5ia</code> 晉昭公（趙世家候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 晉昭公 | [《史記・趙世家》][591] | [JSON](c1t_5mz_5ia.json) |
| `**A` | 驕 | [《史記・趙世家》][591] | [JSON](c1t_5mz_5ia_%2A%2AA.json) |

</details>

<details><summary><code>c27_590_7e3</code> 賈充（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 賈充 | [《晉書・王沈 荀顗 荀勖 馮紞》][119] | [JSON](c27_590_7e3.json) |
| `A` | 賈充女（荀顗薦選太子妃者） | [《晉書・王沈 荀顗 荀勖 馮紞》][119] | [JSON](c27_590_7e3_A.json) |

</details>

<details><summary><code>c2w_s7g_en0</code> 楚懷王（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 楚懷王 | [《史記・楚世家》][588] | [JSON](c2w_s7g_en0.json) |
| `*A` | 楚懷王心 | [《史記・高祖本紀》][574] | [JSON](c2w_s7g_en0_%2AA.json) |
| `A` | 子蘭（楚懷王子） | [《史記・屈原賈生列傳》][632] | [JSON](c2w_s7g_en0_A.json) |

</details>

<details><summary><code>c46_2c9_597</code> 唐衡（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 唐衡 | [《三國志・二荀賈傳》][543] | [JSON](c46_2c9_597.json) |
| `A` | 唐氏（荀彧妻，唐衡女） | [《三國志・二荀賈傳》][543] | [JSON](c46_2c9_597_A.json) |

</details>

<details><summary><code>ccd_af3_98e</code> 建平王宏（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 建平王宏 | [《南齊書・王琨 張岱 褚炫 何戢 王延之 阮韜》][329]、[《南史・王曇首》][463]、[《南史・王曇首》][462]、[《宋書・徐湛之 江湛 王僧綽》][801]、[《宋書・徐湛之 江湛 王僧綽》][799]、[《宋書・徐湛之 江湛 王僧綽》][800]、[《資治通鑑・宋紀十五》][887] | [JSON](ccd_af3_98e.json) |
| `A` | 劉景素（宋建平王，劉宏子） | [《資治通鑑・宋紀十五》][887] | [JSON](ccd_af3_98e_A.json) |

</details>

<details><summary><code>cek_1yy_pne</code> 奄父（趙世家候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 奄父 | [《史記・趙世家》][591] | [JSON](cek_1yy_pne.json) |
| `A` | 叔帶 | [《史記・趙世家》][591] | [JSON](cek_1yy_pne_A.json) |

</details>

<details><summary><code>ceq_pnr_q0e</code> 殷叡〔齊，殷鈞父〕（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 殷叡〔齊，殷鈞父〕 | [《南齊書・王奐 從弟繢 張沖》][368]、[《南史・王誕　王華　王惠　王彧》][482] | [JSON](ceq_pnr_q0e.json) |
| `A` | 殷鈞 | [《南史・王曇首》][471]、[《南史・王曇首》][470] | [JSON](ceq_pnr_q0e_A.json) |

</details>

<details><summary><code>cjd_ybv_2wu</code> 蜚廉（趙世家祖系候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 蜚廉 | [《史記・趙世家》][591] | [JSON](cjd_ybv_2wu.json) |
| `A` | 惡來 | [《史記・趙世家》][591] | [JSON](cjd_ybv_2wu_A.json) |

</details>

<details><summary><code>cti_o52_4nz</code> 宋明帝彧（5 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 宋明帝彧 | [《魏書・燕鳳 許謙 張衮 崔玄伯 鄧淵》][848] | [JSON](cti_o52_4nz.json) |
| `A` | 陽羨公主 | [《文獻通考・卷二百五十八》][864] | [JSON](cti_o52_4nz_A.json) |
| `B` | 劉伯姒（晉陵長公主） | [《宋書・后妃》][756] | [JSON](cti_o52_4nz_B.json) |
| `C` | 劉伯媛（建安長公主） | [《宋書・后妃》][756] | [JSON](cti_o52_4nz_C.json) |
| `D` | 臨淮公主（南朝宋，王瑩妻） | [《南史・王誕　王華　王惠　王彧》][495]、[《文獻通考・卷二百五十八》][864] | [JSON](cti_o52_4nz_D.json) |

</details>

<details><summary><code>d50_8f5_wul</code> 嘉〔張茂度高祖〕（23 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 嘉〔張茂度高祖〕 | [《宋書・張茂度 庾登之 謝方明 江夷》][780] | [JSON](d50_8f5_wul.json) |
| `A` | 澄〔張茂度曾祖〕 | [《宋書・張茂度 庾登之 謝方明 江夷》][780] | [JSON](d50_8f5_wul_A.json) |
| `AA` | 彭祖〔張茂度祖〕 | [《宋書・張茂度 庾登之 謝方明 江夷》][780] | [JSON](d50_8f5_wul_AA.json) |
| `AAA` | 張敞〔邵父〕 | [《宋書・趙倫之 王懿 張邵》][766] | [JSON](d50_8f5_wul_AAA.json) |
| `AAAA` | 張裕〔字茂度〕 | [《宋書・張茂度 庾登之 謝方明 江夷》][780] | [JSON](d50_8f5_wul_AAAA.json) |
| `AAAAA` | 張演〔046／053父系歧異〕 | [《宋書・張茂度 庾登之 謝方明 江夷》][780] | [JSON](d50_8f5_wul_AAAAA.json) |
| `AAAAB` | 張鏡〔046／053父系歧異〕 | [《南齊書・王琨 張岱 褚炫 何戢 王延之 阮韜》][325]、[《南齊書・王琨 張岱 褚炫 何戢 王延之 阮韜》][328]、[《宋書・趙倫之 王懿 張邵》][766]、[《宋書・張茂度 庾登之 謝方明 江夷》][780]、[《宋書・殷淳 張暢 何偃 江智淵》][785] | [JSON](d50_8f5_wul_AAAAB.json) |
| `AAAAC` | 張寅 | [《南齊書・王琨 張岱 褚炫 何戢 王延之 阮韜》][325]、[《南齊書・王琨 張岱 褚炫 何戢 王延之 阮韜》][328]、[《南齊書・王僧虔 張緒》][331]、[《南史・張裕》][517] | [JSON](d50_8f5_wul_AAAAC.json) |
| `AAAACA` | 張緒 | [《南齊書・王僧虔 張緒》][331]、[《南史・張裕》][517] | [JSON](d50_8f5_wul_AAAACA.json) |
| `AAAAD` | 張岱（字景山，張茂度子） | [《南齊書・王琨 張岱 褚炫 何戢 王延之 阮韜》][327]、[《南齊書・王奐 從弟繢 張沖》][363] | [JSON](d50_8f5_wul_AAAAD.json) |
| `AAAAE` | 張永（字景雲） | [《南史・王誕　王華　王惠　王彧》][496] | [JSON](d50_8f5_wul_AAAAE.json) |
| `AAAAEA` | 張瑰（字祖逸） | [《南史・張裕》][516] | [JSON](d50_8f5_wul_AAAAEA.json) |
| `AAAAEAA` | 張率（字士簡） | [《梁書・王僧孺 張率 劉孝綽 王筠》][267] | [JSON](d50_8f5_wul_AAAAEAA.json) |
| `AAAB` | 張褘〔059亦禕，046偉；張暢父〕 | [《宋書・殷淳 張暢 何偃 江智淵》][785] | [JSON](d50_8f5_wul_AAAB.json) |
| `AAABA` | 張暢 | [《宋書・殷淳 張暢 何偃 江智淵》][785] | [JSON](d50_8f5_wul_AAABA.json) |
| `AAABAA` | 張浩〔張暢子〕 | [《宋書・殷淳 張暢 何偃 江智淵》][785] | [JSON](d50_8f5_wul_AAABAA.json) |
| `AAABAB` | 張淹〔張暢子〕 | [《宋書・殷淳 張暢 何偃 江智淵》][785] | [JSON](d50_8f5_wul_AAABAB.json) |
| `AAABB` | 張牧〔張暢弟〕 | [《宋書・殷淳 張暢 何偃 江智淵》][785] | [JSON](d50_8f5_wul_AAABB.json) |
| `AAABC` | 張說〔046作悦〕 | [《宋書・殷淳 張暢 何偃 江智淵》][785] | [JSON](d50_8f5_wul_AAABC.json) |
| `AAAC` | 張邵 | [《宋書・趙倫之 王懿 張邵》][766] | [JSON](d50_8f5_wul_AAAC.json) |
| `AAACA` | 張敷 | [《宋書・趙倫之 王懿 張邵》][766] | [JSON](d50_8f5_wul_AAACA.json) |
| `AAACB` | 張柬〔敷弟〕 | [《宋書・趙倫之 王懿 張邵》][766] | [JSON](d50_8f5_wul_AAACB.json) |
| `AAACBA` | 張式〔柬子〕 | [《宋書・趙倫之 王懿 張邵》][766] | [JSON](d50_8f5_wul_AAACBA.json) |

</details>

<details><summary><code>d5x_77n_qxq</code> 陸閑（字遐業）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 陸閑（字遐業） | [《梁書・陸倕 到洽 明山賓 殷鈞 陸襄》][258] | [JSON](d5x_77n_qxq.json) |
| `A` | 陸襄（字師卿） | [《梁書・陸倕 到洽 明山賓 殷鈞 陸襄》][258] | [JSON](d5x_77n_qxq_A.json) |

</details>

<details><summary><code>d7u_bgr_wdi</code> 蟲達（史表作蠱逢）（4 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 蟲達（史表作蠱逢） | [《漢書・髙惠髙后文功臣表》曲成列][905] | [JSON](d7u_bgr_wdi.json) |
| `***A` | 宣（蟲達玄孫） | [《漢書・髙惠髙后文功臣表》曲成列][905] | [JSON](d7u_bgr_wdi_%2A%2A%2AA.json) |
| `*A` | 皇柔（史表作皋柔） | [《史記・高祖功臣侯者年表》][900] | [JSON](d7u_bgr_wdi_%2AA.json) |
| `A` | 捷（曲城侯） | [《漢書・髙惠髙后文功臣表》曲成列][905]、[《史記・高祖功臣侯者年表》][900] | [JSON](d7u_bgr_wdi_A.json) |

</details>

<details><summary><code>d96_1fa_e9a</code> 劉聰（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 劉聰 | [《晉書・王沈 荀顗 荀勖 馮紞》][119]、[《晉書・山濤 王戎 郭舒 樂廣》][125]、[《晉書・鄭袤 李胤 盧欽 華表 石鑒 溫羨》][134]、[《晉書・鄭袤 李胤 盧欽 華表 石鑒 溫羨》][139]、[《晉書・汝南王亮 楚王瑋 趙王倫 齊王冏 長沙王乂 成都王潁 河間王顒 東海王越》][158]、[《晉書・汝南王亮 楚王瑋 趙王倫 齊王冏 長沙王乂 成都王潁 河間王顒 東海王越》][159]、[《晉書・溫嶠 郗鑒》][171]、[《晉書・列女》][212]、[《晉書・列女》][211]、[《晉書・劉聰》][228]、[《太平御覽・宗親部九》][842] | [JSON](d96_1fa_e9a.json) |
| `A` | 劉粲〔字士光〕 | [《晉書・鄭袤 李胤 盧欽 華表 石鑒 溫羨》][139] | [JSON](d96_1fa_e9a_A.json) |

</details>

<details><summary><code>dad_b77_b38</code> 魏武（引古）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 魏武（引古） | [《三國志・二荀賈傳》][543] | [JSON](dad_b77_b38.json) |
| `A` | 安陽公主 | [《三國志・二荀賈傳》][543] | [JSON](dad_b77_b38_A.json) |

</details>

<details><summary><code>djo_u3b_i9w</code> 殷羨（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 殷羨 | [《晉書・陸曄 何充 褚翜 蔡謨 諸葛恢 殷浩》][194] | [JSON](djo_u3b_i9w.json) |
| `A` | 殷浩 | [《晉書・陸曄 何充 褚翜 蔡謨 諸葛恢 殷浩》][194] | [JSON](djo_u3b_i9w_A.json) |
| `AA` | 殷涓 | [《晉書・叛臣一》][220] | [JSON](djo_u3b_i9w_AA.json) |

</details>

<details><summary><code>dkn_ge4_286</code> 司馬鈞（52 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 司馬鈞 | [《晉書・高祖宣帝》][62] | [JSON](dkn_ge4_286.json) |
| `A` | 司馬量 | [《晉書・高祖宣帝》][62] | [JSON](dkn_ge4_286_A.json) |
| `AA` | 司馬儁 | [《晉書・高祖宣帝》][62] | [JSON](dkn_ge4_286_AA.json) |
| `AAA` | 司馬防 | [《晉書・高祖宣帝》][62] | [JSON](dkn_ge4_286_AAA.json) |
| `AAAA` | 司馬懿 | [《三國志・諸夏侯曹傳》][541] | [JSON](dkn_ge4_286_AAAA.json) |
| `AAAAA` | 司馬伷 | [《晉書・宣五王 文六王》][118] | [JSON](dkn_ge4_286_AAAAA.json) |
| `AAAAAA` | 司馬覲 | [《晉書・宣五王 文六王》][118] | [JSON](dkn_ge4_286_AAAAAA.json) |
| `AAAAAAA` | 晉元帝 | [《晉書・王導》][169] | [JSON](dkn_ge4_286_AAAAAAA.json) |
| `AAAAAAAA` | 晉明帝 | [《晉書・庾亮》][182] | [JSON](dkn_ge4_286_AAAAAAAA.json) |
| `AAAAAAAAA` | 晉成帝 | [《晉書・庾亮》][182] | [JSON](dkn_ge4_286_AAAAAAAAA.json) |
| `AAAAAAAB` | 琅邪孝王裒 | [《晉書・武十三王 元四王 簡文三子》][167] | [JSON](dkn_ge4_286_AAAAAAAB.json) |
| `AAAAAAABA` | 司馬安國 | [《晉書・武十三王 元四王 簡文三子》][167] | [JSON](dkn_ge4_286_AAAAAAABA.json) |
| `AAAAAAAC` | 東海哀王沖 | [《晉書・庾亮》][181] | [JSON](dkn_ge4_286_AAAAAAAC.json) |
| `AAAAAAAD` | 武陵威王晞 | [《晉書・王舒 王廙 虞潭 顧眾 張闓》][189] | [JSON](dkn_ge4_286_AAAAAAAD.json) |
| `AAAAAAAE` | 琅邪悼王煥 | [《晉書・后妃下》][112]、[《晉書・武十三王 元四王 簡文三子》][167] | [JSON](dkn_ge4_286_AAAAAAAE.json) |
| `AAAAAAAF` | 晉簡文帝 | [《晉書・叛臣一》][220] | [JSON](dkn_ge4_286_AAAAAAAF.json) |
| `AAAAAAAFA` | 司馬道子 | [《晉書・王湛 荀崧 范汪 劉惔 張憑 韓伯》][185] | [JSON](dkn_ge4_286_AAAAAAAFA.json) |
| `AAAAAAAFB` | 司馬道福 | [《太平御覽・皇親部十五》][836] | [JSON](dkn_ge4_286_AAAAAAAFB.json) |
| `AAAAAAAG` | 尋陽公主 | [《晉書・后妃下》][112] | [JSON](dkn_ge4_286_AAAAAAAG.json) |
| `AAAAAAB` | 司馬渾 | [《晉書・宣五王 文六王》][118]、[《晉書・武十三王 元四王 簡文三子》][167] | [JSON](dkn_ge4_286_AAAAAAB.json) |
| `AAAAAB` | 司馬澹 | [《晉書・孝懷帝 孝愍帝》][73]、[《晉書・宣五王 文六王》][118] | [JSON](dkn_ge4_286_AAAAAB.json) |
| `AAAAAC` | 司馬繇 | [《晉書・山濤 王戎 郭舒 樂廣》][130] | [JSON](dkn_ge4_286_AAAAAC.json) |
| `AAAAAD` | 司馬漼 | [《晉書・宣五王 文六王》][118] | [JSON](dkn_ge4_286_AAAAAD.json) |
| `AAAAB` | 司馬幹 | [《晉書・王沈 荀顗 荀勖 馮紞》][119] | [JSON](dkn_ge4_286_AAAAB.json) |
| `AAAAC` | 司馬亮 | [《晉書・汝南王亮 楚王瑋 趙王倫 齊王冏 長沙王乂 成都王潁 河間王顒 東海王越》][160] | [JSON](dkn_ge4_286_AAAAC.json) |
| `AAAACA` | 司馬粹 | [《晉書・汝南王亮 楚王瑋 趙王倫 齊王冏 長沙王乂 成都王潁 河間王顒 東海王越》][160] | [JSON](dkn_ge4_286_AAAACA.json) |
| `AAAACB` | 司馬矩 | [《晉書・汝南王亮 楚王瑋 趙王倫 齊王冏 長沙王乂 成都王潁 河間王顒 東海王越》][160] | [JSON](dkn_ge4_286_AAAACB.json) |
| `AAAACC` | 司馬羕 | [《晉書・汝南王亮 楚王瑋 趙王倫 齊王冏 長沙王乂 成都王潁 河間王顒 東海王越》][160] | [JSON](dkn_ge4_286_AAAACC.json) |
| `AAAACC*A` | 瑉（羕孫） | [《晉書・汝南王亮 楚王瑋 趙王倫 齊王冏 長沙王乂 成都王潁 河間王顒 東海王越》][160] | [JSON](dkn_ge4_286_AAAACC%2AA.json) |
| `AAAACC*B` | 崧（羕孫、生父未名） | [《晉書・汝南王亮 楚王瑋 趙王倫 齊王冏 長沙王乂 成都王潁 河間王顒 東海王越》][160]、[《資治通鑑・晉紀十六》][881] | [JSON](dkn_ge4_286_AAAACC%2AB.json) |
| `AAAACCA` | 播（羕世子） | [《晉書・汝南王亮 楚王瑋 趙王倫 齊王冏 長沙王乂 成都王潁 河間王顒 東海王越》][160] | [JSON](dkn_ge4_286_AAAACCA.json) |
| `AAAACCB` | 充（羕子、播弟） | [《晉書・汝南王亮 楚王瑋 趙王倫 齊王冏 長沙王乂 成都王潁 河間王顒 東海王越》][160]、[《資治通鑑・晉紀十六》][881] | [JSON](dkn_ge4_286_AAAACCB.json) |
| `AAAACD` | 司馬宗 | [《晉書・庾亮》][182] | [JSON](dkn_ge4_286_AAAACD.json) |
| `AAAACE` | 司馬熙 | [《晉書・汝南王亮 楚王瑋 趙王倫 齊王冏 長沙王乂 成都王潁 河間王顒 東海王越》][160] | [JSON](dkn_ge4_286_AAAACE.json) |
| `AAAAD` | 司馬京 | [《晉書・宣五王 文六王》][118] | [JSON](dkn_ge4_286_AAAAD.json) |
| `AAAAE` | 司馬駿 | [《晉書・宣五王 文六王》][118]、[《晉書・王沈 荀顗 荀勖 馮紞》][119]、[《晉書・王渾 王濬 唐彬》][121] | [JSON](dkn_ge4_286_AAAAE.json) |
| `AAAAF` | 司馬肜 | [《晉書・山濤 王戎 郭舒 樂廣》][130] | [JSON](dkn_ge4_286_AAAAF.json) |
| `AAAAG` | 司馬倫 | [《晉書・汝南王亮 楚王瑋 趙王倫 齊王冏 長沙王乂 成都王潁 河間王顒 東海王越》][158] | [JSON](dkn_ge4_286_AAAAG.json) |
| `AAAAH` | 司馬景王 | [《晉書・山濤 王戎 郭舒 樂廣》][126]、[《三國志・諸夏侯曹傳》][541] | [JSON](dkn_ge4_286_AAAAH.json) |
| `AAAAI` | 司馬文王 | [《晉書・王沈 荀顗 荀勖 馮紞》][119] | [JSON](dkn_ge4_286_AAAAI.json) |
| `AAAB` | 司馬朗 | [《晉書・高祖宣帝》][62] | [JSON](dkn_ge4_286_AAAB.json) |
| `AAAC` | 孚（安平獻王） | [《晉書・宗室》][117] | [JSON](dkn_ge4_286_AAAC.json) |
| `AAAD` | 馗（宣帝弟、權父） | [《晉書・宗室》][117] | [JSON](dkn_ge4_286_AAAD.json) |
| `AAADA` | 彭城穆王權 | [《晉書・宗室》][117] | [JSON](dkn_ge4_286_AAADA.json) |
| `AAADAA` | 彭城元王植 | [《晉書・宗室》][117] | [JSON](dkn_ge4_286_AAADAA.json) |
| `AAADAAA` | 彭城康王釋 | [《晉書・宗室》][117] | [JSON](dkn_ge4_286_AAADAAA.json) |
| `AAADAAAA` | 彭城王雄 | [《晉書・宗室》][117]、[《資治通鑑・晉紀十六》][881] | [JSON](dkn_ge4_286_AAADAAAA.json) |
| `AAADAAAB` | 紘（釋子） | [《晉書・宗室》][117] | [JSON](dkn_ge4_286_AAADAAAB.json) |
| `AAAE` | 恂（八達之一） | [《晉書・宗室》][117] | [JSON](dkn_ge4_286_AAAE.json) |
| `AAAF` | 進（八達之一） | [《晉書・宗室》][117] | [JSON](dkn_ge4_286_AAAF.json) |
| `AAAG` | 通（八達之一） | [《晉書・宗室》][117] | [JSON](dkn_ge4_286_AAAG.json) |
| `AAAH` | 敏（八達之一） | [《晉書・宗室》][117] | [JSON](dkn_ge4_286_AAAH.json) |

</details>

<details><summary><code>dm0_58v_50i</code> 趙衰（5 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 趙衰 | [《史記・晉世家》][587] | [JSON](dm0_58v_50i.json) |
| `A` | 趙盾 | [《史記・晉世家》][587] | [JSON](dm0_58v_50i_A.json) |
| `B` | 趙同 | [《史記・趙世家》][591] | [JSON](dm0_58v_50i_B.json) |
| `C` | 趙括 | [《史記・趙世家》][591] | [JSON](dm0_58v_50i_C.json) |
| `D` | 趙嬰齊 | [《史記・趙世家》][591] | [JSON](dm0_58v_50i_D.json) |

</details>

<details><summary><code>dq6_ovk_58c</code> 張釋之（張釋之馮唐列傳候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 張釋之 | [《史記・張釋之馮唐列傳》][650] | [JSON](dq6_ovk_58c.json) |
| `A` | 張摯 | [《史記・張釋之馮唐列傳》][650] | [JSON](dq6_ovk_58c_A.json) |

</details>

<details><summary><code>e00_pe1_zri</code> 無諸（東越列傳候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 無諸 | [《史記・東越列傳》][662] | [JSON](e00_pe1_zri.json) |
| `*A` | 丑 | [《史記・東越列傳》][662] | [JSON](e00_pe1_zri_%2AA.json) |

</details>

<details><summary><code>e2r_5iw_ui0</code> 劉穎之（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 劉穎之 | [《宋書・殷孝祖 劉勔》][820] | [JSON](e2r_5iw_ui0.json) |
| `A` | 劉勔 | [《宋書・薛安都 沈文秀 崔道固》][822] | [JSON](e2r_5iw_ui0_A.json) |

</details>

<details><summary><code>e5k_f2i_cog</code> 郗曇（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 郗曇 | [《晉書・溫嶠 郗鑒》][176]、[《晉書・溫嶠 郗鑒》][175] | [JSON](e5k_f2i_cog.json) |
| `A` | 郗道茂 | [《世說新語・德行》][684] | [JSON](e5k_f2i_cog_A.json) |

</details>

<details><summary><code>ea5_zvr_hlp</code> 張良（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 張良 | [《史記・留侯世家》][603] | [JSON](ea5_zvr_hlp.json) |
| `A` | 張辟彊 | [《史記・呂后本紀》][575] | [JSON](ea5_zvr_hlp_A.json) |
| `B` | 不疑 | [《史記・留侯世家》][603] | [JSON](ea5_zvr_hlp_B.json) |

</details>

<details><summary><code>ebb_5a7_96e</code> 郗恢（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 郗恢 | [《晉書・溫嶠 郗鑒》][176] | [JSON](ebb_5a7_96e.json) |
| `A` | 郗循 | [《晉書・溫嶠 郗鑒》][176] | [JSON](ebb_5a7_96e_A.json) |

</details>

<details><summary><code>egx_xax_4ic</code> 蕭承之（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 蕭承之 | [《南史・后妃上》][379]、[《南史・后妃上》][380] | [JSON](egx_xax_4ic.json) |
| `A` | 蕭道度 | [《南齊書・高帝下》][280]、[《南齊書・皇后》][290]、[《南齊書・皇后》][289]、[《南史・后妃上》][379]、[《南史・后妃上》][380] | [JSON](egx_xax_4ic_A.json) |

</details>

<details><summary><code>ei2_qej_czn</code> 公乘氏（張耳陳餘列傳候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 公乘氏 | [《史記・張耳陳餘列傳》][637] | [JSON](ei2_qej_czn.json) |
| `A` | 陳餘妻未名 | [《史記・張耳陳餘列傳》][637] | [JSON](ei2_qej_czn_A.json) |

</details>

<details><summary><code>ei7_fai_lvy</code> 丑（鄭世家共公候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 丑 | [《史記・鄭世家》][590] | [JSON](ei7_fai_lvy.json) |
| `A` | 已 | [《史記・鄭世家》][590] | [JSON](ei7_fai_lvy_A.json) |

</details>

<details><summary><code>eom_42c_5zd</code> 華恆〔廷尉〕（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 華恆〔廷尉〕 | [《晉書・鄭袤 李胤 盧欽 華表 石鑒 溫羨》][134] | [JSON](eom_42c_5zd.json) |
| `A` | 華俊〔華恆子〕 | [《晉書・鄭袤 李胤 盧欽 華表 石鑒 溫羨》][134] | [JSON](eom_42c_5zd_A.json) |
| `AA` | 華仰之〔大長秋〕 | [《晉書・鄭袤 李胤 盧欽 華表 石鑒 溫羨》][134] | [JSON](eom_42c_5zd_AA.json) |

</details>

<details><summary><code>esh_e0a_jrw</code> 石奮父未名（萬石張叔列傳候選）（7 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 石奮父未名 | [《史記・萬石張叔列傳》][651] | [JSON](esh_e0a_jrw.json) |
| `A` | 石奮 | [《史記・萬石張叔列傳》][651] | [JSON](esh_e0a_jrw_A.json) |
| `AA` | 建（石奮長子） | [《史記・萬石張叔列傳》][651] | [JSON](esh_e0a_jrw_AA.json) |
| `AB` | 甲（石奮次子失名佔位） | [《史記・萬石張叔列傳》][651] | [JSON](esh_e0a_jrw_AB.json) |
| `AC` | 乙（石奮次子失名佔位） | [《史記・萬石張叔列傳》][651] | [JSON](esh_e0a_jrw_AC.json) |
| `AD` | 慶（石奮子） | [《史記・萬石張叔列傳》][651] | [JSON](esh_e0a_jrw_AD.json) |
| `ADA` | 德（石慶中子） | [《史記・萬石張叔列傳》][651] | [JSON](esh_e0a_jrw_ADA.json) |

</details>

<details><summary><code>eva_gs1_9n5</code> 魏文侯（趙世家候選）（7 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 魏文侯 | [《史記・趙世家》][591] | [JSON](eva_gs1_9n5.json) |
| `A` | 撃 | [《史記・魏世家》][592] | [JSON](eva_gs1_9n5_A.json) |
| `AA` | 罃 | [《史記・魏世家》][592] | [JSON](eva_gs1_9n5_AA.json) |
| `AAA` | 襄王 | [《史記・魏世家》][592] | [JSON](eva_gs1_9n5_AAA.json) |
| `AAAA` | 哀王 | [《史記・魏世家》][592] | [JSON](eva_gs1_9n5_AAAA.json) |
| `AAAAA` | 昭王 | [《史記・魏世家》][592] | [JSON](eva_gs1_9n5_AAAAA.json) |
| `AAAAAA` | 安釐王 | [《史記・魏公子列傳》][625] | [JSON](eva_gs1_9n5_AAAAAA.json) |

</details>

<details><summary><code>ex7_8jy_o48</code> 郭洪之（郭祚父）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 郭洪之（郭祚父） | [《魏書・郭祚 張彝》][861] | [JSON](ex7_8jy_o48.json) |
| `A` | 郭祚（字季祐） | [《魏書・郭祚 張彝》][861] | [JSON](ex7_8jy_o48_A.json) |

</details>

<details><summary><code>eya_qj3_tev</code> 酈食其（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 酈食其 | [《史記・酈生陸賈列傳》][645] | [JSON](eya_qj3_tev.json) |
| `A` | 疥（酈食其子） | [《史記・酈生陸賈列傳》][645] | [JSON](eya_qj3_tev_A.json) |

</details>

<details><summary><code>f04_rc9_xqn</code> 太史敫（田世家候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 太史敫 | [《史記・田敬仲完世家》][594] | [JSON](f04_rc9_xqn.json) |
| `A` | 君王后 | [《史記・田敬仲完世家》][594] | [JSON](f04_rc9_xqn_A.json) |

</details>

<details><summary><code>f2z_47w_81j</code> 商玄石（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 商玄石 | [《宋書・謝晦》][761]、[《宋書・謝晦》][762] | [JSON](f2z_47w_81j.json) |
| `A` | 商懷福 | [《宋書・謝晦》][761]、[《宋書・謝晦》][762] | [JSON](f2z_47w_81j_A.json) |

</details>

<details><summary><code>f41_ulg_3u1</code> 衛滿（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 衛滿 | [《史記・朝鮮列傳》][663] | [JSON](f41_ulg_3u1.json) |
| `*A` | 右渠 | [《史記・朝鮮列傳》][663] | [JSON](f41_ulg_3u1_%2AA.json) |
| `*AA` | 長（右渠子） | [《史記・朝鮮列傳》][663] | [JSON](f41_ulg_3u1_%2AAA.json) |

</details>

<details><summary><code>f84_da6_42a</code> 孔愉（5 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 孔愉 | [《晉書・顯宗成帝 康帝》][80]、[《晉書・王沈 荀顗 荀勖 馮紞》][119]、[《南史・孔靖　孔琳之　殷景仁》][513] | [JSON](f84_da6_42a.json) |
| `A` | 孔誾（孔愉子、孔靖父） | [《南史・孔靖　孔琳之　殷景仁》][513] | [JSON](f84_da6_42a_A.json) |
| `AA` | 孔靖（字季恭，晉書作靜） | [《南史・孔靖　孔琳之　殷景仁》][513] | [JSON](f84_da6_42a_AA.json) |
| `AAA` | 孔靈運（孔琇之父） | [《南齊書・良政》][374] | [JSON](f84_da6_42a_AAA.json) |
| `AAAA` | 孔琇之（會稽山陰人，孔靈運子） | [《南齊書・王奐 從弟繢 張沖》][360]、[《南齊書・良政》][374] | [JSON](f84_da6_42a_AAAA.json) |

</details>

<details><summary><code>f89_ad1_61d</code> 王凌（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 王凌 | [《三國志・王毌丘諸葛鄧鍾傳》][562] | [JSON](f89_ad1_61d.json) |
| `A` | 王廣 | [《三國志・王毌丘諸葛鄧鍾傳》][562] | [JSON](f89_ad1_61d_A.json) |

</details>

<details><summary><code>f8d_j5p_nop</code> 孔防叔（孔子世家候選）（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 孔防叔 | [《史記・孔子世家》][595] | [JSON](f8d_j5p_nop.json) |
| `A` | 伯夏 | [《史記・孔子世家》][595] | [JSON](f8d_j5p_nop_A.json) |
| `AA` | 叔梁紇 | [《史記・孔子世家》][595] | [JSON](f8d_j5p_nop_AA.json) |

</details>

<details><summary><code>f90_933_c35</code> 猗盧（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 猗盧 | [《晉書・王沈 荀顗 荀勖 馮紞》][119]、[《晉書・鄭袤 李胤 盧欽 華表 石鑒 溫羨》][139] | [JSON](f90_933_c35.json) |
| `A` | 日律孫 | [《晉書・王沈 荀顗 荀勖 馮紞》][119] | [JSON](f90_933_c35_A.json) |

</details>

<details><summary><code>faf_5al_ikw</code> 鄭武公（老韓列傳候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 鄭武公 | [《史記・老子韓非列傳》][611] | [JSON](faf_5al_ikw.json) |
| `A` | 鄭武公之子 | [《史記・老子韓非列傳》][611] | [JSON](faf_5al_ikw_A.json) |

</details>

<details><summary><code>fcu_pw8_tkw</code> 蔡興宗（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 蔡興宗 | [《南齊書・王融 謝朓》][358]、[《南史・謝晦　謝裕　謝方明　謝靈運》][432]、[《南史・王曇首》][456]、[《南史・王曇首》][463]、[《南史・王曇首》][462]、[《宋書・徐湛之 江湛 王僧綽》][801]、[《宋書・徐湛之 江湛 王僧綽》][799]、[《宋書・徐湛之 江湛 王僧綽》][800] | [JSON](fcu_pw8_tkw.json) |
| `A` | 蔡約 | [《南史・王曇首》][456] | [JSON](fcu_pw8_tkw_A.json) |

</details>

<details><summary><code>fd3_tly_1lo</code> 沸（魯魏公）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 沸（魯魏公） | [《史記・魯周公世家》][581] | [JSON](fd3_tly_1lo.json) |
| `A` | 擢（魯厲公） | [《史記・魯周公世家》][581]、[《史記・三代世表》][895] | [JSON](fd3_tly_1lo_A.json) |

</details>

<details><summary><code>fdb_6pb_gux</code> 蒯聵（太史公自序候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 蒯聵 | [《史記・太史公自序》][678] | [JSON](fdb_6pb_gux.json) |
| `***A` | 司馬卬 | [《史記・高祖本紀》][574]、[《史記・太史公自序》][678] | [JSON](fdb_6pb_gux_%2A%2A%2AA.json) |

</details>

<details><summary><code>ffc_ea1_a8f</code> 范寧（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 范寧 | [《晉書・王湛 荀崧 范汪 劉惔 張憑 韓伯》][185] | [JSON](ffc_ea1_a8f.json) |
| `A` | 范泰 | [《宋書・范泰 王准之 王韶之 荀伯子》][786] | [JSON](ffc_ea1_a8f_A.json) |

</details>

<details><summary><code>fjm_eo3_0zz</code> 始興王憺（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 始興王憺 | [《南史・王裕之　王鎮之　王韶之　王悅之　王准之》][506] | [JSON](fjm_eo3_0zz.json) |
| `A` | 繁昌主 | [《梁書・王瞻 王志 王峻 王暕 子訓 王泰 王份 孫鍚 僉 張充 柳惲 蔡撙 江蒨》][249]、[《南史・王裕之　王鎮之　王韶之　王悅之　王准之》][506] | [JSON](fjm_eo3_0zz_A.json) |

</details>

<details><summary><code>fmh_dmt_cql</code> 汲黯（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 汲黯 | [《史記・汲鄭列傳》][668] | [JSON](fmh_dmt_cql.json) |
| `A` | 汲偃 | [《漢書・張馮汲鄭傳》][44]、[《史記・汲鄭列傳》][668] | [JSON](fmh_dmt_cql_A.json) |

</details>

<details><summary><code>fo7_f8v_rmf</code> 梁武帝衍（8 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 梁武帝衍 | [《梁書・謝朏 弟子覽》][243] | [JSON](fo7_f8v_rmf.json) |
| `A` | 蕭玉姚 | [《梁書・皇后》][240] | [JSON](fo7_f8v_rmf_A.json) |
| `B` | 蕭玉婉 | [《梁書・皇后》][240] | [JSON](fo7_f8v_rmf_B.json) |
| `C` | 蕭績（字世謹） | [《梁書・高祖三王》][262] | [JSON](fo7_f8v_rmf_C.json) |
| `CA` | 蕭會理（字長才，南康王績子） | [《梁書・高祖三王》][261] | [JSON](fo7_f8v_rmf_CA.json) |
| `D` | 蕭紀（武陵王） | [《梁書・豫章王綜 武陵王紀 臨賀王正德 河東王譽》][279] | [JSON](fo7_f8v_rmf_D.json) |
| `E` | 蕭玉志（梁安吉公主，王實妻） | [《南史・王誕　王華　王惠　王彧》][495] | [JSON](fo7_f8v_rmf_E.json) |
| `F` | 梁永嘉公主（王銓妻） | [《南史・王誕　王華　王惠　王彧》][477]、[《文獻通考・卷二百五十八》][866] | [JSON](fo7_f8v_rmf_F.json) |

</details>

<details><summary><code>fom_gr9_c8v</code> 孫叔敖（循吏列傳候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 孫叔敖 | [《史記・循吏列傳》][667]、[《史記・滑稽列傳》][674] | [JSON](fom_gr9_c8v.json) |
| `A` | 孫叔敖子（未名） | [《史記・滑稽列傳》][674] | [JSON](fom_gr9_c8v_A.json) |

</details>

<details><summary><code>fp6_ia6_7yw</code> 孔子（11 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 孔子 | [《史記・孔子世家》][595] | [JSON](fp6_ia6_7yw.json) |
| `A` | 鯉 | [《史記・孔子世家》][595] | [JSON](fp6_ia6_7yw_A.json) |
| `AA` | 伋 | [《史記・孔子世家》][595] | [JSON](fp6_ia6_7yw_AA.json) |
| `AAA` | 白 | [《史記・孔子世家》][595] | [JSON](fp6_ia6_7yw_AAA.json) |
| `AAAA` | 求 | [《史記・孔子世家》][595] | [JSON](fp6_ia6_7yw_AAAA.json) |
| `AAAAA` | 箕 | [《史記・孔子世家》][595] | [JSON](fp6_ia6_7yw_AAAAA.json) |
| `AAAAAA` | 穿 | [《史記・孔子世家》][595] | [JSON](fp6_ia6_7yw_AAAAAA.json) |
| `AAAAAAA` | 子慎 | [《史記・孔子世家》][595] | [JSON](fp6_ia6_7yw_AAAAAAA.json) |
| `AAAAAAAA` | 鮒 | [《史記・孔子世家》][595] | [JSON](fp6_ia6_7yw_AAAAAAAA.json) |
| `B` | 孔鯉 | [《史記・仲尼弟子列傳》][615] | [JSON](fp6_ia6_7yw_B.json) |
| `C` | 孔子之女 | [《史記・仲尼弟子列傳》][615] | [JSON](fp6_ia6_7yw_C.json) |

</details>

<details><summary><code>fs1_z3i_d4r</code> 趙遐（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 趙遐 | [《崔混墓誌・節錄》][25] | [JSON](fs1_z3i_d4r.json) |
| `A` | 趙氏（崔混妻） | [《崔混墓誌・節錄》][25] | [JSON](fs1_z3i_d4r_A.json) |

</details>

<details><summary><code>fum_370_iq6</code> 結〔楊播高祖〕（28 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 結〔楊播高祖〕 | [《魏書・楊播》][855] | [JSON](fum_370_iq6.json) |
| `A` | 珍〔楊播曾祖〕 | [《魏書・楊播》][855]、[《魏書・楊播》][856] | [JSON](fum_370_iq6_A.json) |
| `AA` | 真〔楊播祖〕 | [《楊舒墓誌・全文》][33]、[《魏書・楊播》][855]、[《魏書・楊播》][856] | [JSON](fum_370_iq6_AA.json) |
| `AAA` | 懿〔楊播父〕 | [《魏書・楊播》][855] | [JSON](fum_370_iq6_AAA.json) |
| `AAAA` | 楊播 | [《魏書・楊播》][855] | [JSON](fum_370_iq6_AAAA.json) |
| `AAAAA` | 侃〔楊播子，字士業〕 | [《魏書・楊播》][855] | [JSON](fum_370_iq6_AAAAA.json) |
| `AAAAAA` | 師沖〔楊侃長子，北史作師仲〕 | [《魏書・楊播》][855] | [JSON](fum_370_iq6_AAAAAA.json) |
| `AAAAAB` | 純陀〔楊侃嗣子〕 | [《魏書・楊播》][855] | [JSON](fum_370_iq6_AAAAAB.json) |
| `AAAB` | 楊椿 | [《魏書・楊播》][856] | [JSON](fum_370_iq6_AAAB.json) |
| `AAABA` | 楊昱 | [《魏書・楊播》][856] | [JSON](fum_370_iq6_AAABA.json) |
| `AAABAA` | 孝邕〔楊昱子〕 | [《魏書・楊播》][856] | [JSON](fum_370_iq6_AAABAA.json) |
| `AAAC` | 穎〔楊椿弟，字惠哲〕 | [《魏書・楊播》][856] | [JSON](fum_370_iq6_AAAC.json) |
| `AAACA` | 叔良〔楊穎子〕 | [《魏書・楊播》][856] | [JSON](fum_370_iq6_AAACA.json) |
| `AAAD` | 順〔楊穎弟，字延和〕 | [《魏書・楊播》][856] | [JSON](fum_370_iq6_AAAD.json) |
| `AAADA` | 辯〔楊順子，字僧達〕 | [《魏書・楊播》][856] | [JSON](fum_370_iq6_AAADA.json) |
| `AAADB` | 仲宣〔楊順子〕 | [《魏書・楊播》][856] | [JSON](fum_370_iq6_AAADB.json) |
| `AAADBA` | 玄就〔楊仲宣子〕 | [《魏書・楊播》][856] | [JSON](fum_370_iq6_AAADBA.json) |
| `AAADC` | 測〔楊仲宣弟〕 | [《魏書・楊播》][856] | [JSON](fum_370_iq6_AAADC.json) |
| `AAADD` | 稚卿〔楊測弟〕 | [《魏書・楊播》][856] | [JSON](fum_370_iq6_AAADD.json) |
| `AAAE` | 楊津〔字羅漢，本名延祚〕 | [《魏書・楊播》][857] | [JSON](fum_370_iq6_AAAE.json) |
| `AAAEA` | 楊遁〔字山才，津長子〕 | [《魏書・楊播》][857] | [JSON](fum_370_iq6_AAAEA.json) |
| `AAAEB` | 楊逸〔字遵道，津第二子〕 | [《魏書・楊播》][857] | [JSON](fum_370_iq6_AAAEB.json) |
| `AAAEC` | 楊謐〔字遵智，逸弟〕 | [《魏書・楊播》][857] | [JSON](fum_370_iq6_AAAEC.json) |
| `AAAED` | 楊遵彥〔謐弟〕 | [《南史・王弘》][450]、[《魏書・楊播》][857] | [JSON](fum_370_iq6_AAAED.json) |
| `AAAF` | 楊暐〔字延季，津弟〕 | [《魏書・楊播》][857] | [JSON](fum_370_iq6_AAAF.json) |
| `AAAFA` | 楊元讓〔暐子〕 | [《魏書・楊播》][857] | [JSON](fum_370_iq6_AAAFA.json) |
| `AAB` | 洛州恒農簡公〔楊舒墓誌父〕 | [《楊舒墓誌・全文》][33] | [JSON](fum_370_iq6_AAB.json) |
| `AABA` | 舒〔楊昱第六叔〕 | [《楊舒墓誌・全文》][33] | [JSON](fum_370_iq6_AABA.json) |

</details>

<details><summary><code>fv1_k6x_jeu</code> 虛閭權渠單于（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 虛閭權渠單于 | [《漢書・匈奴傳》][49] | [JSON](fv1_k6x_jeu.json) |
| `A` | 呼韓邪單于（稽侯狦） | [《漢書・匈奴傳》][49] | [JSON](fv1_k6x_jeu_A.json) |

</details>

<details><summary><code>fvm_66f_0k3</code> 周緤（4 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 周緤 | [《史記・傅靳蒯成列傳》][646] | [JSON](fvm_66f_0k3.json) |
| `A` | 周昌（蒯成侯之子） | [《漢書・樊酈滕灌傅靳周傳》][43]、[《史記・傅靳蒯成列傳》][646]、[《史記・高祖功臣侯者年表》][900] | [JSON](fvm_66f_0k3_A.json) |
| `C` | 周應 | [《漢書・樊酈滕灌傅靳周傳》][43] | [JSON](fvm_66f_0k3_C.json) |
| `CA` | 周仲居 | [《史記・高祖功臣侯者年表》][900] | [JSON](fvm_66f_0k3_CA.json) |

</details>

<details><summary><code>g7w_9tv_iqb</code> 王僧辯（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 王僧辯 | [《南史・王誕　王華　王惠　王彧》][483]、[《南史・王裕之　王鎮之　王韶之　王悅之　王准之》][501]、[《南史・江子一　胡僧祐　徐文盛　陰子春　杜崱　王琳　張彪》][537] | [JSON](g7w_9tv_iqb.json) |
| `A` | 王僧辯女（杜龕妻） | [《南史・江子一　胡僧祐　徐文盛　陰子春　杜崱　王琳　張彪》][537] | [JSON](g7w_9tv_iqb_A.json) |

</details>

<details><summary><code>g83_41s_o52</code> 焦文珪（南安氐人，焦度祖）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 焦文珪（南安氐人，焦度祖） | [《南齊書・薛淵 戴僧靜 桓康 焦度 曹虎》][321] | [JSON](g83_41s_o52.json) |
| `*A` | 焦度（字文續） | [《南齊書・薛淵 戴僧靜 桓康 焦度 曹虎》][321] | [JSON](g83_41s_o52_%2AA.json) |

</details>

<details><summary><code>g9h_5ih_ug1</code> 伍奢（伍胥列傳候選）（4 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 伍奢 | [《史記・伍子胥列傳》][614] | [JSON](g9h_5ih_ug1.json) |
| `A` | 伍子胥 | [《史記・伍子胥列傳》][614] | [JSON](g9h_5ih_ug1_A.json) |
| `AA` | 伍子胥之子 | [《史記・伍子胥列傳》][614] | [JSON](g9h_5ih_ug1_AA.json) |
| `B` | 伍尚 | [《史記・伍子胥列傳》][614] | [JSON](g9h_5ih_ug1_B.json) |

</details>

<details><summary><code>ga6_jt5_6g1</code> 圉（衛孔文子）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 圉（衛孔文子） | [《史記・衛康叔世家》][585] | [JSON](ga6_jt5_6g1.json) |
| `A` | 悝（衛孔氏） | [《史記・衛康叔世家》][585] | [JSON](ga6_jt5_6g1_A.json) |

</details>

<details><summary><code>gcb_rf3_coi</code> 費王（晉穆侯）（4 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 費王（晉穆侯） | [《史記・晉世家》][587] | [JSON](gcb_rf3_coi.json) |
| `A` | 仇（晉文侯） | [《史記・晉世家》][587] | [JSON](gcb_rf3_coi_A.json) |
| `AA` | 伯（晉昭侯） | [《史記・晉世家》][587] | [JSON](gcb_rf3_coi_AA.json) |
| `B` | 成師（曲沃桓叔） | [《史記・晉世家》][587] | [JSON](gcb_rf3_coi_B.json) |

</details>

<details><summary><code>gcu_93j_y97</code> 鄭遵（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 鄭遵 | [《南史・范泰　荀伯子　徐廣　鄭鮮之　裴松之　何承天》][519] | [JSON](gcu_93j_y97.json) |
| `A` | 鄭鮮之 | [《南史・范泰　荀伯子　徐廣　鄭鮮之　裴松之　何承天》][519] | [JSON](gcu_93j_y97_A.json) |

</details>

<details><summary><code>gdj_k53_v1x</code> 王翦（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 王翦 | [《史記・白起王翦列傳》][621] | [JSON](gdj_k53_v1x.json) |
| `*A` | 王離 | [《史記・白起王翦列傳》][621] | [JSON](gdj_k53_v1x_%2AA.json) |
| `A` | 王賁 | [《史記・白起王翦列傳》][621] | [JSON](gdj_k53_v1x_A.json) |

</details>

<details><summary><code>ghg_5p7_q21</code> 遂（杞釐公）（4 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 遂（杞釐公） | [《史記・陳杞世家》][584] | [JSON](ghg_5p7_q21.json) |
| `A` | 維（杞湣公） | [《史記・陳杞世家》][584] | [JSON](ghg_5p7_q21_A.json) |
| `AA` | 敕（杞出公） | [《史記・陳杞世家》][584] | [JSON](ghg_5p7_q21_AA.json) |
| `AAA` | 春（杞簡公） | [《史記・陳杞世家》][584] | [JSON](ghg_5p7_q21_AAA.json) |

</details>

<details><summary><code>gjl_f5h_2a6</code> 劉景猷（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 劉景猷 | [《南齊書・皇后》][305]、[《南齊書・皇后》][306]、[《南史・后妃上》][386]、[《南史・后妃上》][387] | [JSON](gjl_f5h_2a6.json) |
| `A` | 劉惠端 | [《南齊書・皇后》][305]、[《南齊書・皇后》][306]、[《南史・后妃上》][386]、[《南史・后妃上》][387]、[《昭明文選・卷五十八》][868]、[《昭明文選・卷五十八》][869]、[《昭明文選・卷五十八》][870] | [JSON](gjl_f5h_2a6_A.json) |
| `B` | 劉暄 | [《南史・謝晦　謝裕　謝方明　謝靈運》][432] | [JSON](gjl_f5h_2a6_B.json) |

</details>

<details><summary><code>gke_14h_1xk</code> 宇（燕王）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 宇（燕王） | [《三國志・三少帝紀》][539]、[《三國志・諸夏侯曹傳》][540] | [JSON](gke_14h_1xk.json) |
| `A` | 曹奐〔字景明〕 | [《三國志・三少帝紀》][539] | [JSON](gke_14h_1xk_A.json) |

</details>

<details><summary><code>gm4_alk_hn7</code> 劉玄之（7 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 劉玄之 | [《南齊書・皇后》][297]、[《南齊書・皇后》][296]、[《南史・后妃上》][388]、[《南史・后妃上》][389] | [JSON](gm4_alk_hn7.json) |
| `A` | 劉壽之 | [《南齊書・皇后》][297]、[《南齊書・皇后》][296]、[《南史・后妃上》][388]、[《南史・后妃上》][389] | [JSON](gm4_alk_hn7_A.json) |
| `AA` | 劉智容 | [《南史・后妃上》][388]、[《南史・后妃上》][389] | [JSON](gm4_alk_hn7_AA.json) |
| `AB` | 劉興道 | [《南齊書・皇后》][297]、[《南齊書・皇后》][296] | [JSON](gm4_alk_hn7_AB.json) |
| `AC` | 劉文蔚 | [《南齊書・皇后》][297]、[《南齊書・皇后》][296] | [JSON](gm4_alk_hn7_AC.json) |
| `AD` | 劉義徽 | [《南齊書・皇后》][297]、[《南齊書・皇后》][296] | [JSON](gm4_alk_hn7_AD.json) |
| `AE` | 劉義倫 | [《南齊書・皇后》][297]、[《南齊書・皇后》][296] | [JSON](gm4_alk_hn7_AE.json) |

</details>

<details><summary><code>gn7_br7_32m</code> 伯州犁（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 伯州犁 | [《史記・吳太伯世家》][579] | [JSON](gn7_br7_32m.json) |
| `*A` | 伯嚭 | [《史記・吳太伯世家》][579] | [JSON](gn7_br7_32m_%2AA.json) |

</details>

<details><summary><code>gqj_xdu_8rf</code> 張騫（李將軍列傳候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 張騫 | [《史記・大宛列傳》][671] | [JSON](gqj_xdu_8rf.json) |
| `A` | 張騫子（未名） | [《史記・大宛列傳》][671] | [JSON](gqj_xdu_8rf_A.json) |

</details>

<details><summary><code>gtj_19g_u2l</code> 殷道矜（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 殷道矜 | [《南齊書・王奐 從弟繢 張沖》][367] | [JSON](gtj_19g_u2l.json) |
| `A` | 殷恒（字昭度，殷道矜子） | [《南齊書・王奐 從弟繢 張沖》][367] | [JSON](gtj_19g_u2l_A.json) |

</details>

<details><summary><code>gts_42q_flu</code> 睔（鄭世家成公候選）（7 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 睔 | [《史記・鄭世家》][590] | [JSON](gts_42q_flu.json) |
| `A` | 惲 | [《史記・鄭世家》][590] | [JSON](gts_42q_flu_A.json) |
| `AA` | 嘉 | [《史記・鄭世家》][590] | [JSON](gts_42q_flu_AA.json) |
| `AAA` | 寧 | [《史記・鄭世家》][590] | [JSON](gts_42q_flu_AAA.json) |
| `AAAA` | 蠆 | [《史記・鄭世家》][590] | [JSON](gts_42q_flu_AAAA.json) |
| `AAAAA` | 勝 | [《史記・鄭世家》][590] | [JSON](gts_42q_flu_AAAAA.json) |
| `AAAAAA` | 易 | [《史記・鄭世家》][590] | [JSON](gts_42q_flu_AAAAAA.json) |

</details>

<details><summary><code>gyg_hql_qdj</code> 慕容永（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 慕容永 | [《晉書・溫嶠 郗鑒》][176] | [JSON](gyg_hql_qdj.json) |
| `A` | 慕容弘〔常山公、慕容永子〕 | [《晉書・溫嶠 郗鑒》][176]、[《資治通鑑・晉紀三十》][884] | [JSON](gyg_hql_qdj_A.json) |

</details>

<details><summary><code>gzc_9vs_o43</code> 孟嘉〔字萬年〕（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 孟嘉〔字萬年〕 | [《晉書・叛臣一》][222] | [JSON](gzc_9vs_o43.json) |
| `A` | 孟氏〔孟嘉第四女、陶淵明母〕 | — | [JSON](gzc_9vs_o43_A.json) |

</details>

<details><summary><code>h15_bxq_n5u</code> 周優〔周翼父〕（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 周優〔周翼父〕 | [《世說新語・德行》][683] | [JSON](h15_bxq_n5u.json) |
| `A` | 周翼〔字子卿，郗鑒外甥〕 | [《世說新語・德行》][683] | [JSON](h15_bxq_n5u_A.json) |

</details>

<details><summary><code>h1w_44g_vef</code> 張孟（魏其武安侯列傳候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 張孟 | [《史記・魏其武安列傳》][655] | [JSON](h1w_44g_vef.json) |
| `A` | 灌夫 | [《史記・魏其武安列傳》][655] | [JSON](h1w_44g_vef_A.json) |

</details>

<details><summary><code>h4f_d5f_vdl</code> 蟬封（大宛列傳候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 蟬封 | [《史記・大宛列傳》][671] | [JSON](h4f_d5f_vdl.json) |
| `A` | 蟬封子（入質，未名） | [《史記・大宛列傳》][671] | [JSON](h4f_d5f_vdl_A.json) |

</details>

<details><summary><code>h7n_w5t_i1c</code> 曹休未名祖父（7 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 曹休未名祖父 | [《三國志・諸夏侯曹傳》][540] | [JSON](h7n_w5t_i1c.json) |
| `A` | 曹休未名父 | [《三國志・諸夏侯曹傳》][540] | [JSON](h7n_w5t_i1c_A.json) |
| `AA` | 曹休 | [《三國志・諸夏侯曹傳》][540] | [JSON](h7n_w5t_i1c_AA.json) |
| `AAA` | 肇（曹攄祖、曹休子） | [《三國志・諸夏侯曹傳》][540] | [JSON](h7n_w5t_i1c_AAA.json) |
| `AAA*A` | 曹顏遠 | [《晉書・良吏》][201] | [JSON](h7n_w5t_i1c_AAA%2AA.json) |
| `AAAA` | 興（肇子） | [《三國志・諸夏侯曹傳》][540] | [JSON](h7n_w5t_i1c_AAAA.json) |
| `AAB` | 纂（肇弟） | [《三國志・諸夏侯曹傳》][540] | [JSON](h7n_w5t_i1c_AAB.json) |

</details>

<details><summary><code>h9n_acw_xpo</code> 戴碩子（法興父）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 戴碩子（法興父） | [《宋書・恩倖》][829] | [JSON](h9n_acw_xpo.json) |
| `A` | 戴法興（會稽山陰人） | [《宋書・恩倖》][829] | [JSON](h9n_acw_xpo_A.json) |

</details>

<details><summary><code>hgm_jvn_hle</code> 晉武帝（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 晉武帝 | [《晉書・王沈 荀顗 荀勖 馮紞》][119] | [JSON](hgm_jvn_hle.json) |
| `A` | 襄城公主〔晉武帝女、王敦妻〕 | [《晉書・叛臣一》][221] | [JSON](hgm_jvn_hle_A.json) |
| `B` | 滎陽公主〔晉武帝女〕 | [《晉書・鄭袤 李胤 盧欽 華表 石鑒 溫羨》][139] | [JSON](hgm_jvn_hle_B.json) |

</details>

<details><summary><code>hx8_st4_jdd</code> 宋孝武帝駿（8 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 宋孝武帝駿 | [《宋書・殷淳 張暢 何偃 江智淵》][785] | [JSON](hx8_st4_jdd.json) |
| `A` | 安固公主（宋孝武女） | [《梁書・王瞻 王志 王峻 王暕 子訓 王泰 王份 孫鍚 僉 張充 柳惲 蔡撙 江蒨》][255]、[《梁書・王瞻 王志 王峻 王暕 子訓 王泰 王份 孫鍚 僉 張充 柳惲 蔡撙 江蒨》][254]、[《南史・王曇首》][473]、[《南史・王曇首》][472] | [JSON](hx8_st4_jdd_A.json) |
| `B` | 永嘉王子仁 | [《宋書・孝武十四王》][812] | [JSON](hx8_st4_jdd_B.json) |
| `C` | 劉楚玉（山陰公主） | [《南齊書・王琨 張岱 褚炫 何戢 王延之 阮韜》][323]、[《宋書・后妃》][755] | [JSON](hx8_st4_jdd_C.json) |
| `D` | 劉楚佩（臨淮康哀公主） | [《宋書・后妃》][755] | [JSON](hx8_st4_jdd_D.json) |
| `E` | 劉楚琇（宋孝武皇女） | [《宋書・后妃》][755] | [JSON](hx8_st4_jdd_E.json) |
| `F` | 劉脩明（康樂公主） | [《宋書・后妃》][755] | [JSON](hx8_st4_jdd_F.json) |
| `G` | 臨汝公主（宋孝武帝女，江斆妻） | [《南齊書・江斆 何昌㝢 謝𤅢 王思遠》][348]、[《南史・王誕　王華　王惠　王彧》][498] | [JSON](hx8_st4_jdd_G.json) |

</details>

<details><summary><code>hxn_tox_kna</code> 宗叔獻（宗靈秀父）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 宗叔獻（宗靈秀父） | [《宋書・朱脩之 宗愨 王玄謨》][808] | [JSON](hxn_tox_kna.json) |
| `A` | 宗靈秀（宋黃門侍郎） | [《宋書・朱脩之 宗愨 王玄謨》][808] | [JSON](hxn_tox_kna_A.json) |

</details>

<details><summary><code>i08_s4b_5bb</code> 王晏〔齊尚書令〕（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 王晏〔齊尚書令〕 | [《南齊書・王奐 從弟繢 張沖》][360] | [JSON](i08_s4b_5bb.json) |
| `A` | 王德元（王晏子，初名湛） | [《南齊書・王晏 蕭諶 蕭坦之 江祏》][345] | [JSON](i08_s4b_5bb_A.json) |
| `B` | 王德和（王德元弟） | [《南齊書・王晏 蕭諶 蕭坦之 江祏》][345] | [JSON](i08_s4b_5bb_B.json) |

</details>

<details><summary><code>i30_mjq_6q8</code> 呂公（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 呂公 | [《史記・高祖本紀》][574] | [JSON](i30_mjq_6q8.json) |
| `A` | 呂后 | [《史記・呂后本紀》][575] | [JSON](i30_mjq_6q8_A.json) |

</details>

<details><summary><code>i3f_9l9_g53</code> 陳平（5 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 陳平 | [《史記・陳丞相世家》][604] | [JSON](i3f_9l9_g53.json) |
| `**A` | 陳掌 | [《史記・陳丞相世家》][604] | [JSON](i3f_9l9_g53_%2A%2AA.json) |
| `A` | 買 | [《史記・陳丞相世家》][604] | [JSON](i3f_9l9_g53_A.json) |
| `AA` | 恢 | [《史記・陳丞相世家》][604] | [JSON](i3f_9l9_g53_AA.json) |
| `AAA` | 何 | [《史記・陳丞相世家》][604] | [JSON](i3f_9l9_g53_AAA.json) |

</details>

<details><summary><code>i7a_22p_qda</code> 句踐（7 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 句踐 | [《史記・越王勾踐世家》][589] | [JSON](i7a_22p_qda.json) |
| `A` | 鼫與 | [《史記・越王勾踐世家》][589] | [JSON](i7a_22p_qda_A.json) |
| `AA` | 不壽 | [《史記・越王勾踐世家》][589] | [JSON](i7a_22p_qda_AA.json) |
| `AAA` | 翁 | [《史記・越王勾踐世家》][589] | [JSON](i7a_22p_qda_AAA.json) |
| `AAAA` | 翳 | [《史記・越王勾踐世家》][589] | [JSON](i7a_22p_qda_AAAA.json) |
| `AAAAA` | 之侯 | [《史記・越王勾踐世家》][589] | [JSON](i7a_22p_qda_AAAAA.json) |
| `AAAAAA` | 無彊 | [《史記・越王勾踐世家》][589] | [JSON](i7a_22p_qda_AAAAAA.json) |

</details>

<details><summary><code>i8i_rvh_4lp</code> 燬（衛文公）（8 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 燬（衛文公） | [《史記・衛康叔世家》][585] | [JSON](i8i_rvh_4lp.json) |
| `A` | 鄭（衛成公） | [《史記・衛康叔世家》][585] | [JSON](i8i_rvh_4lp_A.json) |
| `AA` | 遫（衛穆公） | [《史記・衛康叔世家》][585] | [JSON](i8i_rvh_4lp_AA.json) |
| `AAA` | 臧（衛定公） | [《史記・衛康叔世家》][585] | [JSON](i8i_rvh_4lp_AAA.json) |
| `AAAA` | 衎（衛獻公） | [《史記・衛康叔世家》][585] | [JSON](i8i_rvh_4lp_AAAA.json) |
| `AAAAA` | 惡（衛襄公） | [《史記・衛康叔世家》][585] | [JSON](i8i_rvh_4lp_AAAAA.json) |
| `AAAAAA` | 元（衛靈公） | [《史記・衛康叔世家》][585] | [JSON](i8i_rvh_4lp_AAAAAA.json) |
| `AAAAAAA` | 郢（衛子南） | [《史記・衛康叔世家》][585] | [JSON](i8i_rvh_4lp_AAAAAAA.json) |

</details>

<details><summary><code>ier_lqj_x4q</code> 郗愔（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 郗愔 | [《晉書・溫嶠 郗鑒》][172] | [JSON](ier_lqj_x4q.json) |
| `A` | 郗融 | [《晉書・溫嶠 郗鑒》][178]、[《晉書・溫嶠 郗鑒》][177] | [JSON](ier_lqj_x4q_A.json) |
| `B` | 郗沖 | [《晉書・溫嶠 郗鑒》][178]、[《晉書・溫嶠 郗鑒》][177] | [JSON](ier_lqj_x4q_B.json) |

</details>

<details><summary><code>iij_zqi_k5l</code> 齊平公（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 齊平公 | [《史記・齊太公世家》][580] | [JSON](iij_zqi_k5l.json) |
| `A` | 積（齊宣公） | [《史記・齊太公世家》][580] | [JSON](iij_zqi_k5l_A.json) |
| `AA` | 貸（齊康公） | [《史記・齊太公世家》][580] | [JSON](iij_zqi_k5l_AA.json) |

</details>

<details><summary><code>inr_w1g_bu5</code> 子襄（孔子世家候選）（7 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 子襄 | [《史記・孔子世家》][595] | [JSON](inr_w1g_bu5.json) |
| `A` | 忠 | [《史記・孔子世家》][595] | [JSON](inr_w1g_bu5_A.json) |
| `AA` | 武 | [《史記・孔子世家》][595] | [JSON](inr_w1g_bu5_AA.json) |
| `AAA` | 延年 | [《史記・孔子世家》][595] | [JSON](inr_w1g_bu5_AAA.json) |
| `AAB` | 安國 | [《史記・孔子世家》][595] | [JSON](inr_w1g_bu5_AAB.json) |
| `AABA` | 卬 | [《史記・孔子世家》][595] | [JSON](inr_w1g_bu5_AABA.json) |
| `AABAA` | 驩 | [《史記・孔子世家》][595] | [JSON](inr_w1g_bu5_AABAA.json) |

</details>

<details><summary><code>ixk_6fg_v6f</code> 竇后父（外戚世家候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 竇后父 | [《史記・外戚世家》][597] | [JSON](ixk_6fg_v6f.json) |
| `A` | 竇太后（孝文帝皇后） | [《史記・梁孝王世家》][606] | [JSON](ixk_6fg_v6f_A.json) |

</details>

<details><summary><code>j32_wtj_khz</code> 袁盎父未名（袁盎鼂錯列傳候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 袁盎父未名 | [《史記・袁盎鼂錯列傳》][649] | [JSON](j32_wtj_khz.json) |
| `A` | 袁盎 | [《史記・袁盎鼂錯列傳》][649] | [JSON](j32_wtj_khz_A.json) |

</details>

<details><summary><code>jfc_0dt_42a</code> 顧秘（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 顧秘 | [《晉書・王舒 王廙 虞潭 顧眾 張闓》][188] | [JSON](jfc_0dt_42a.json) |
| `A` | 顧衆 | [《晉書・王舒 王廙 虞潭 顧眾 張闓》][192] | [JSON](jfc_0dt_42a_A.json) |

</details>

<details><summary><code>jg1_ag9_033</code> 老子（孔子世家候選）（4 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 老子 | [《史記・老子韓非列傳》][611] | [JSON](jg1_ag9_033.json) |
| `A` | 宗 | [《史記・老子韓非列傳》][611] | [JSON](jg1_ag9_033_A.json) |
| `AA` | 注 | [《史記・老子韓非列傳》][611] | [JSON](jg1_ag9_033_AA.json) |
| `AAA` | 宮 | [《史記・老子韓非列傳》][611] | [JSON](jg1_ag9_033_AAA.json) |

</details>

<details><summary><code>jgo_o5m_l1f</code> 劉秉（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 劉秉 | [《南史・王鎮惡　朱齡石　毛脩之　傅弘之　朱脩之　王玄謨》][417] | [JSON](jgo_o5m_l1f.json) |
| `A` | 劉秉女（王慈妻） | — | [JSON](jgo_o5m_l1f_A.json) |

</details>

<details><summary><code>jjl_irg_zke</code> 盧綰父未名（韓信盧綰列傳候選）（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 盧綰父未名 | [《史記・韓信盧綰列傳》][641] | [JSON](jjl_irg_zke.json) |
| `A` | 盧綰 | [《史記・韓信盧綰列傳》][641] | [JSON](jjl_irg_zke_A.json) |
| `A*A` | 盧他之 | [《史記・韓信盧綰列傳》][641] | [JSON](jjl_irg_zke_A%2AA.json) |

</details>

<details><summary><code>jo4_4bf_0ra</code> 劉澤（5 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 劉澤 | [《史記・荊燕世家》][599] | [JSON](jo4_4bf_0ra.json) |
| `A` | 嘉（燕康王） | [《史記・荊燕世家》][599] | [JSON](jo4_4bf_0ra_A.json) |
| `AA` | 定國 | [《史記・荊燕世家》][599] | [JSON](jo4_4bf_0ra_AA.json) |
| `AAA` | 定國所生男（荊燕世家未名者） | [《史記・荊燕世家》][599] | [JSON](jo4_4bf_0ra_AAA.json) |
| `AB` | 田蚡夫人（燕康王女，未名） | [《史記・魏其武安列傳》][655] | [JSON](jo4_4bf_0ra_AB.json) |

</details>

<details><summary><code>jqx_jns_jae</code> 虞豫（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 虞豫 | [《晉書・后妃下》][112] | [JSON](jqx_jns_jae.json) |
| `A` | 虞孟母 | [《晉書・后妃下》][112] | [JSON](jqx_jns_jae_A.json) |

</details>

<details><summary><code>jru_oiq_x0q</code> 楚成王（鄭世家候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 楚成王 | [《史記・鄭世家》][590] | [JSON](jru_oiq_x0q.json) |
| `A` | 商臣 | [《史記・鄭世家》][590] | [JSON](jru_oiq_x0q_A.json) |

</details>

<details><summary><code>jx9_cov_qe0</code> 欒布（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 欒布 | [《史記・季布欒布列傳》][648] | [JSON](jx9_cov_qe0.json) |
| `A` | 賁（欒布子） | [《史記・季布欒布列傳》][648]、[《史記・惠景間侯者年表》][901] | [JSON](jx9_cov_qe0_A.json) |

</details>

<details><summary><code>jyf_yg2_dqk</code> 沈劭之（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 沈劭之 | [《宋書・薛安都 沈文秀 崔道固》][823] | [JSON](jyf_yg2_dqk.json) |
| `A` | 沈文秀 | [《南齊書・劉懷珍 李安民 王玄載》][317] | [JSON](jyf_yg2_dqk_A.json) |

</details>

<details><summary><code>jyx_72x_8t2</code> 褚淵（4 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 褚淵 | [《南史・王曇首》][460] | [JSON](jyx_72x_8t2.json) |
| `A` | 褚蓁 | [《梁書・王規 劉瑴 宗懍 王承 褚翔 蕭介 從父兄洽 褚球 劉孺 弟覽 遵 劉潛 弟孝勝 孝威 孝先 殷芸 蕭幾》][270] | [JSON](jyx_72x_8t2_A.json) |
| `AA` | 褚向（字景政） | [《梁書・王規 劉瑴 宗懍 王承 褚翔 蕭介 從父兄洽 褚球 劉孺 弟覽 遵 劉潛 弟孝勝 孝威 孝先 殷芸 蕭幾》][270] | [JSON](jyx_72x_8t2_AA.json) |
| `AAA` | 褚翔 | [《梁書・王規 劉瑴 宗懍 王承 褚翔 蕭介 從父兄洽 褚球 劉孺 弟覽 遵 劉潛 弟孝勝 孝威 孝先 殷芸 蕭幾》][270] | [JSON](jyx_72x_8t2_AAA.json) |

</details>

<details><summary><code>k2p_5ol_dwh</code> 蒙驁（4 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 蒙驁 | [《史記・蒙恬列傳》][636] | [JSON](k2p_5ol_dwh.json) |
| `A` | 蒙武 | [《史記・蒙恬列傳》][636] | [JSON](k2p_5ol_dwh_A.json) |
| `AA` | 蒙恬 | [《史記・蒙恬列傳》][636] | [JSON](k2p_5ol_dwh_AA.json) |
| `AB` | 蒙毅 | [《史記・蒙恬列傳》][636] | [JSON](k2p_5ol_dwh_AB.json) |

</details>

<details><summary><code>k5z_d58_n7p</code> 熊元（楚考烈王）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 熊元（楚考烈王） | [《史記・春申君列傳》][626] | [JSON](k5z_d58_n7p.json) |
| `A` | 悍（楚幽王） | [《史記・春申君列傳》][626] | [JSON](k5z_d58_n7p_A.json) |

</details>

<details><summary><code>kix_r92_2ed</code> 齊世祖賾（8 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 齊世祖賾 | [《南齊書・虞玩之 劉休 沈沖 庾杲之 王諶》][332] | [JSON](kix_r92_2ed.json) |
| `A` | 蕭子敬（安陸王） | [《南齊書・武十七王》][341] | [JSON](kix_r92_2ed_A.json) |
| `B` | 蕭子琳 | [《南史・齊武帝諸子　文惠諸子　明帝諸子》][525] | [JSON](kix_r92_2ed_B.json) |
| `C` | 蕭子罕（南海王） | [《梁書・王瞻 王志 王峻 王暕 子訓 王泰 王份 孫鍚 僉 張充 柳惲 蔡撙 江蒨》][253]、[《梁書・王瞻 王志 王峻 王暕 子訓 王泰 王份 孫鍚 僉 張充 柳惲 蔡撙 江蒨》][252]、[《南齊書・武十七王》][340] | [JSON](kix_r92_2ed_C.json) |
| `D` | 吳縣公主（齊武帝長女） | — | [JSON](kix_r92_2ed_D.json) |
| `E` | 廬陵王子卿 | [《南齊書・武十七王》][339] | [JSON](kix_r92_2ed_E.json) |
| `F` | 蕭子貞（字雲松） | [《南齊書・武十七王》][342] | [JSON](kix_r92_2ed_F.json) |
| `G` | 蕭子響（字雲音，魚復侯） | [《南齊書・武十七王》][344] | [JSON](kix_r92_2ed_G.json) |

</details>

<details><summary><code>koy_6jg_gcc</code> 周勃（6 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 周勃 | [《史記・絳侯周勃世家》][605] | [JSON](koy_6jg_gcc.json) |
| `A` | 勝之 | [《史記・絳侯周勃世家》][605] | [JSON](koy_6jg_gcc_A.json) |
| `B` | 堅 | [《史記・絳侯周勃世家》][605] | [JSON](koy_6jg_gcc_B.json) |
| `BA` | 建德 | [《史記・絳侯周勃世家》][605] | [JSON](koy_6jg_gcc_BA.json) |
| `C` | 周亞夫 | [《史記・絳侯周勃世家》][605] | [JSON](koy_6jg_gcc_C.json) |
| `CA` | 亞夫子 | [《史記・絳侯周勃世家》][605] | [JSON](koy_6jg_gcc_CA.json) |

</details>

<details><summary><code>kt8_3kv_44r</code> 頑（衛昭伯）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 頑（衛昭伯） | [《史記・衛康叔世家》][585] | [JSON](kt8_3kv_44r.json) |
| `A` | 申（衛戴公） | [《史記・衛康叔世家》][585] | [JSON](kt8_3kv_44r_A.json) |

</details>

<details><summary><code>ktk_wbg_wnm</code> 鄧公（袁盎鼂錯列傳候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 鄧公 | [《史記・袁盎鼂錯列傳》][649] | [JSON](ktk_wbg_wnm.json) |
| `A` | 章（鄧公子） | [《史記・袁盎鼂錯列傳》][649] | [JSON](ktk_wbg_wnm_A.json) |

</details>

<details><summary><code>l3c_zg4_f7z</code> 宋襄公（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 宋襄公 | [《史記・宋微子世家》][586] | [JSON](l3c_zg4_f7z.json) |
| `A` | 王臣（宋成公） | [《史記・宋微子世家》][586] | [JSON](l3c_zg4_f7z_A.json) |
| `AA` | 杵臼（宋昭公） | [《史記・宋微子世家》][586] | [JSON](l3c_zg4_f7z_AA.json) |

</details>

<details><summary><code>l8e_pxu_xre</code> 武公（趙世家趙君候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 武公 | [《史記・趙世家》][591] | [JSON](l8e_pxu_xre.json) |
| `A` | 朝 | [《史記・趙世家》][591] | [JSON](l8e_pxu_xre_A.json) |

</details>

<details><summary><code>l9e_fbr_36a</code> 倉（韓世家襄王候選）（9 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 倉 | [《史記・韓世家》][593] | [JSON](l9e_fbr_36a.json) |
| `*A` | 韓王信（韓太尉） | [《史記・韓信盧綰列傳》][641] | [JSON](l9e_fbr_36a_%2AA.json) |
| `*AA` | 韓王信太子未名 | [《史記・韓信盧綰列傳》][641] | [JSON](l9e_fbr_36a_%2AAA.json) |
| `*AAA` | 韓嬰 | [《史記・韓信盧綰列傳》][641] | [JSON](l9e_fbr_36a_%2AAAA.json) |
| `*AB` | 韓穨當 | [《史記・韓信盧綰列傳》][641] | [JSON](l9e_fbr_36a_%2AAB.json) |
| `*AB*A` | 韓嫣 | [《史記・佞幸列傳》][673] | [JSON](l9e_fbr_36a_%2AAB%2AA.json) |
| `*AB*B` | 韓說 | [《史記・東越列傳》][662] | [JSON](l9e_fbr_36a_%2AAB%2AB.json) |
| `*AB*B*A` | 韓曾 | [《史記・韓信盧綰列傳》][641] | [JSON](l9e_fbr_36a_%2AAB%2AB%2AA.json) |
| `*AB*BA` | 韓說子未名 | [《史記・韓信盧綰列傳》][641] | [JSON](l9e_fbr_36a_%2AAB%2ABA.json) |

</details>

<details><summary><code>lc5_nwz_ikf</code> 襲之〔宣之繼者〕（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 襲之〔宣之繼者〕 | [《宋書・后妃》][754] | [JSON](lc5_nwz_ikf.json) |
| `A` | 祖憐〔襲之子〕 | [《宋書・后妃》][754] | [JSON](lc5_nwz_ikf_A.json) |

</details>

<details><summary><code>lc6_cup_v9c</code> 稱（魯孝公）（5 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 稱（魯孝公） | [《史記・魯周公世家》][581] | [JSON](lc6_cup_v9c.json) |
| `A` | 弗湟（魯惠公） | [《史記・魯周公世家》][581] | [JSON](lc6_cup_v9c_A.json) |
| `AA` | 魯隱公 | [《史記・魯周公世家》][581] | [JSON](lc6_cup_v9c_AA.json) |
| `AB` | 魯桓公 | [《史記・魯周公世家》][581] | [JSON](lc6_cup_v9c_AB.json) |
| `ABA` | 季友（成季） | [《史記・魯周公世家》][581] | [JSON](lc6_cup_v9c_ABA.json) |

</details>

<details><summary><code>lcc_msq_vdt</code> 露（曹靖公）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 露（曹靖公） | [《史記・管蔡世家》][583] | [JSON](lcc_msq_vdt.json) |
| `A` | 伯陽（曹君） | [《史記・管蔡世家》][583] | [JSON](lcc_msq_vdt_A.json) |

</details>

<details><summary><code>li9_cmb_8ci</code> 滕公（本卷稱呼）（4 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 滕公（本卷稱呼） | [《史記・樊酈滕灌列傳》][643] | [JSON](li9_cmb_8ci.json) |
| `A` | 夏侯灶 | [《史記・樊酈滕灌列傳》][643] | [JSON](li9_cmb_8ci_A.json) |
| `AA` | 夏侯賜 | [《史記・樊酈滕灌列傳》][643] | [JSON](li9_cmb_8ci_AA.json) |
| `AAA` | 夏侯頗 | [《史記・樊酈滕灌列傳》][643] | [JSON](li9_cmb_8ci_AAA.json) |

</details>

<details><summary><code>ll1_7jh_vr0</code> 鄭合（6 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 鄭合 | [《晉書・后妃下》][112] | [JSON](ll1_7jh_vr0.json) |
| `A` | 鄭愷 | [《晉書・后妃下》][112] | [JSON](ll1_7jh_vr0_A.json) |
| `AA` | 鄭阿春 | [《晉書・后妃下》][112] | [JSON](ll1_7jh_vr0_AA.json) |
| `AB` | 鄭氏（阿春妹，王褒妻） | [《晉書・后妃下》][112] | [JSON](ll1_7jh_vr0_AB.json) |
| `AC` | 鄭氏（阿春三妹，劉傭妻） | [《晉書・后妃下》][112] | [JSON](ll1_7jh_vr0_AC.json) |
| `AD` | 鄭氏（阿春幼妹，李氏妻） | [《晉書・后妃下》][112] | [JSON](ll1_7jh_vr0_AD.json) |

</details>

<details><summary><code>lmu_nbm_rzo</code> 燮（陳平公）（21 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 燮（陳平公） | [《史記・陳杞世家》][584] | [JSON](lmu_nbm_rzo.json) |
| `A` | 圉（陳文公） | [《史記・陳杞世家》][584] | [JSON](lmu_nbm_rzo_A.json) |
| `AA` | 佗（陳厲公） | [《史記・陳杞世家》][584] | [JSON](lmu_nbm_rzo_AA.json) |
| `AAA` | 完（敬仲） | [《史記・田敬仲完世家》][594] | [JSON](lmu_nbm_rzo_AAA.json) |
| `AAAA` | 稚孟夷 | [《史記・田敬仲完世家》][594] | [JSON](lmu_nbm_rzo_AAAA.json) |
| `AAAAA` | 湣孟莊 | [《史記・田敬仲完世家》][594] | [JSON](lmu_nbm_rzo_AAAAA.json) |
| `AAAAAA` | 田文子須無 | [《史記・田敬仲完世家》][594] | [JSON](lmu_nbm_rzo_AAAAAA.json) |
| `AAAAAAA` | 田桓子無宇 | [《史記・田敬仲完世家》][594] | [JSON](lmu_nbm_rzo_AAAAAAA.json) |
| `AAAAAAAA` | 武子開 | [《史記・田敬仲完世家》][594] | [JSON](lmu_nbm_rzo_AAAAAAAA.json) |
| `AAAAAAAB` | 田釐子乞 | [《史記・田敬仲完世家》][594] | [JSON](lmu_nbm_rzo_AAAAAAAB.json) |
| `AAAAAAABA` | 田常 | [《史記・田敬仲完世家》][594] | [JSON](lmu_nbm_rzo_AAAAAAABA.json) |
| `AAAAAAABAA` | 田襄子盤 | [《史記・田敬仲完世家》][594] | [JSON](lmu_nbm_rzo_AAAAAAABAA.json) |
| `AAAAAAABAAA` | 田莊子白 | [《史記・田敬仲完世家》][594] | [JSON](lmu_nbm_rzo_AAAAAAABAAA.json) |
| `AAAAAAABAAAA` | 太公和 | [《史記・田敬仲完世家》][594] | [JSON](lmu_nbm_rzo_AAAAAAABAAAA.json) |
| `AAAAAAABAAAAA` | 桓公午 | [《史記・扁鵲倉公列傳》][653] | [JSON](lmu_nbm_rzo_AAAAAAABAAAAA.json) |
| `AAAAAAABAAAAAA` | 因齊 | [《史記・田敬仲完世家》][594] | [JSON](lmu_nbm_rzo_AAAAAAABAAAAAA.json) |
| `AAAAAAABAAAAAAA` | 辟彊 | [《史記・田敬仲完世家》][594]、[《史記・孟嘗君列傳》][623] | [JSON](lmu_nbm_rzo_AAAAAAABAAAAAAA.json) |
| `AAAAAAABAAAAAAAA` | 齊湣王 | [《史記・孟嘗君列傳》][623] | [JSON](lmu_nbm_rzo_AAAAAAABAAAAAAAA.json) |
| `AB` | 鮑（陳桓公） | [《史記・陳杞世家》][584] | [JSON](lmu_nbm_rzo_AB.json) |
| `ABA` | 免（陳桓公太子） | [《史記・陳杞世家》][584] | [JSON](lmu_nbm_rzo_ABA.json) |
| `ABB` | 躍（陳利公） | [《史記・陳杞世家》][584] | [JSON](lmu_nbm_rzo_ABB.json) |

</details>

<details><summary><code>lrg_cze_g1l</code> 蘇峻（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 蘇峻 | [《晉書・溫嶠 郗鑒》][171]、[《晉書・庾亮》][182]、[《晉書・叛臣三》][227] | [JSON](lrg_cze_g1l.json) |
| `A` | 蘇碩 | [《晉書・叛臣三》][227] | [JSON](lrg_cze_g1l_A.json) |

</details>

<details><summary><code>lt4_hpv_4ku</code> 武成王（燕君）（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 武成王（燕君） | [《史記・燕召公世家》][582] | [JSON](lt4_hpv_4ku.json) |
| `A` | 孝王（燕君） | [《史記・燕召公世家》][582] | [JSON](lt4_hpv_4ku_A.json) |
| `AA` | 燕王喜 | [《史記・燕召公世家》][582] | [JSON](lt4_hpv_4ku_AA.json) |

</details>

<details><summary><code>lwx_9yq_ad7</code> 紂（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 紂 | [《史記・殷本紀》][569] | [JSON](lwx_9yq_ad7.json) |
| `A` | 武庚 | [《史記・衛康叔世家》][585] | [JSON](lwx_9yq_ad7_A.json) |

</details>

<details><summary><code>lxy_zsx_o2z</code> 崔參〔清河、溫嶠外祖〕（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 崔參〔清河、溫嶠外祖〕 | [《世說新語・尤悔》][741] | [JSON](lxy_zsx_o2z.json) |
| `A` | 清河崔氏〔溫嶠母〕 | [《晉書・溫嶠 郗鑒》][171]、[《世說新語・尤悔》][741] | [JSON](lxy_zsx_o2z_A.json) |

</details>

<details><summary><code>m0b_b5e_153</code> 田常（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 田常 | [《史記・齊太公世家》][580] | [JSON](m0b_b5e_153.json) |
| `**A` | 田和 | [《史記・六國年表》][897] | [JSON](m0b_b5e_153_%2A%2AA.json) |

</details>

<details><summary><code>m8d_pnd_ias</code> 惠侯（燕君）（10 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 惠侯（燕君） | [《史記・燕召公世家》][582] | [JSON](m8d_pnd_ias.json) |
| `A` | 釐侯（燕君） | [《史記・燕召公世家》][582] | [JSON](m8d_pnd_ias_A.json) |
| `AA` | 頃侯（燕君） | [《史記・燕召公世家》][582] | [JSON](m8d_pnd_ias_AA.json) |
| `AAA` | 哀侯（燕君） | [《史記・燕召公世家》][582] | [JSON](m8d_pnd_ias_AAA.json) |
| `AAAA` | 鄭侯（燕君） | [《史記・燕召公世家》][582] | [JSON](m8d_pnd_ias_AAAA.json) |
| `AAAAA` | 繆侯（燕君） | [《史記・燕召公世家》][582] | [JSON](m8d_pnd_ias_AAAAA.json) |
| `AAAAAA` | 宣侯（燕君） | [《史記・燕召公世家》][582] | [JSON](m8d_pnd_ias_AAAAAA.json) |
| `AAAAAAA` | 桓侯（燕君） | [《史記・燕召公世家》][582] | [JSON](m8d_pnd_ias_AAAAAAA.json) |
| `AAAAAAAA` | 燕莊公 | [《史記・齊太公世家》][580]、[《史記・燕召公世家》][582] | [JSON](m8d_pnd_ias_AAAAAAAA.json) |
| `AAAAAAAAA` | 襄公（燕君） | [《史記・燕召公世家》][582] | [JSON](m8d_pnd_ias_AAAAAAAAA.json) |

</details>

<details><summary><code>m8n_ntm_79h</code> 盧植（15 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 盧植 | [《後漢書・吳延史盧趙列傳》][55] | [JSON](m8n_ntm_79h.json) |
| `A` | 盧毓 | [《三國志・桓二陳徐衞盧傳》][557] | [JSON](m8n_ntm_79h_A.json) |
| `A*A` | 藩〔盧毓孫〕 | [《三國志・桓二陳徐衞盧傳》][557] | [JSON](m8n_ntm_79h_A%2AA.json) |
| `AA` | 盧欽〔舉王衍者〕 | [《晉書・鄭袤 李胤 盧欽 華表 石鑒 溫羨》][141] | [JSON](m8n_ntm_79h_AA.json) |
| `AAA` | 盧浮 | [《三國志・桓二陳徐衞盧傳》][557] | [JSON](m8n_ntm_79h_AAA.json) |
| `AB` | 盧珽 | [《三國志・桓二陳徐衞盧傳》][557] | [JSON](m8n_ntm_79h_AB.json) |
| `ABA` | 皓〔盧珽子〕 | [《三國志・桓二陳徐衞盧傳》][557] | [JSON](m8n_ntm_79h_ABA.json) |
| `ABB` | 盧志 | [《晉書・鄭袤 李胤 盧欽 華表 石鑒 溫羨》][143] | [JSON](m8n_ntm_79h_ABB.json) |
| `ABBA` | 盧諶 | [《晉書・鄭袤 李胤 盧欽 華表 石鑒 溫羨》][139] | [JSON](m8n_ntm_79h_ABBA.json) |
| `ABBA**A` | 盧循 | [《宋書・庾悅 王誕 謝景仁 袁湛 褚叔度》][773] | [JSON](m8n_ntm_79h_ABBA%2A%2AA.json) |
| `ABBAA` | 偃〔盧諶子〕 | [《魏書・燕鳳 許謙 張衮 崔玄伯 鄧淵》][849]、[《魏書・燕鳳 許謙 張衮 崔玄伯 鄧淵》][850] | [JSON](m8n_ntm_79h_ABBAA.json) |
| `ABBAAA` | 邈〔偃子〕 | [《魏書・燕鳳 許謙 張衮 崔玄伯 鄧淵》][849]、[《魏書・燕鳳 許謙 張衮 崔玄伯 鄧淵》][850]、[《魏書・盧玄》][853] | [JSON](m8n_ntm_79h_ABBAAA.json) |
| `ABBAAAA` | 盧玄〔字子真〕 | [《魏書・盧玄》][853] | [JSON](m8n_ntm_79h_ABBAAAA.json) |
| `ABBB` | 盧謐〔盧志子〕 | [《晉書・鄭袤 李胤 盧欽 華表 石鑒 溫羨》][143] | [JSON](m8n_ntm_79h_ABBB.json) |
| `ABBC` | 盧詵〔盧志子〕 | [《晉書・鄭袤 李胤 盧欽 華表 石鑒 溫羨》][143] | [JSON](m8n_ntm_79h_ABBC.json) |

</details>

<details><summary><code>m9n_b6v_wo0</code> 梁孝王（本卷未名）（5 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 梁孝王（本卷未名） | [《史記・孝景本紀》][577] | [JSON](m9n_b6v_wo0.json) |
| `A` | 明（梁孝王子） | [《史記・孝景本紀》][577] | [JSON](m9n_b6v_wo0_A.json) |
| `B` | 彭離（梁孝王子） | [《史記・孝景本紀》][577] | [JSON](m9n_b6v_wo0_B.json) |
| `C` | 定（梁孝王子） | [《史記・孝景本紀》][577] | [JSON](m9n_b6v_wo0_C.json) |
| `D` | 不識（梁孝王子） | [《史記・孝景本紀》][577] | [JSON](m9n_b6v_wo0_D.json) |

</details>

<details><summary><code>maz_aq2_t5g</code> 季勝（趙世家祖系候選）（4 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 季勝 | [《史記・趙世家》][591] | [JSON](maz_aq2_t5g.json) |
| `A` | 孟增 | [《史記・趙世家》][591] | [JSON](maz_aq2_t5g_A.json) |
| `AA` | 衡父 | [《史記・趙世家》][591] | [JSON](maz_aq2_t5g_AA.json) |
| `AAA` | 造父 | [《史記・趙世家》][591] | [JSON](maz_aq2_t5g_AAA.json) |

</details>

<details><summary><code>mgh_3bh_rit</code> 周厲王（鄭世家候選）（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 周厲王 | [《史記・鄭世家》][590] | [JSON](mgh_3bh_rit.json) |
| `A` | 友 | [《史記・鄭世家》][590] | [JSON](mgh_3bh_rit_A.json) |
| `AA` | 掘突 | [《史記・鄭世家》][590] | [JSON](mgh_3bh_rit_AA.json) |

</details>

<details><summary><code>mj8_5ic_4kk</code> 殷道鸞（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 殷道鸞 | [《宋書・謝晦》][761]、[《宋書・謝晦》][762] | [JSON](mj8_5ic_4kk.json) |
| `A` | 殷琰 | [《南齊書・劉懷珍 李安民 王玄載》][314]、[《宋書・蕭惠開 殷琰》][821]、[《宋書・薛安都 沈文秀 崔道固》][822] | [JSON](mj8_5ic_4kk_A.json) |

</details>

<details><summary><code>mnv_izb_7w3</code> 蕭景〔吳平侯〕（4 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 蕭景〔吳平侯〕 | [《梁書・裴子野 顧協 徐摛 鮑泉》][263]、[《南史・梁宗室上》][532] | [JSON](mnv_izb_7w3.json) |
| `A` | 蕭勸（字文肅） | [《南史・梁宗室上》][532] | [JSON](mnv_izb_7w3_A.json) |
| `B` | 蕭勉（字文祗） | [《南史・梁宗室上》][532] | [JSON](mnv_izb_7w3_B.json) |
| `C` | 蕭勃（曲江鄕侯） | [《南史・王誕　王華　王惠　王彧》][487]、[《南史・梁宗室上》][532] | [JSON](mnv_izb_7w3_C.json) |

</details>

<details><summary><code>ms3_fa1_ps9</code> 田生（荊燕世家候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 田生 | [《史記・荊燕世家》][599] | [JSON](ms3_fa1_ps9.json) |
| `A` | 田生子 | [《史記・荊燕世家》][599] | [JSON](ms3_fa1_ps9_A.json) |

</details>

<details><summary><code>muq_yy8_8er</code> 寤生（鄭世家莊公候選）（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 寤生 | [《史記・鄭世家》][590] | [JSON](muq_yy8_8er.json) |
| `A` | 忽 | [《史記・鄭世家》][590] | [JSON](muq_yy8_8er_A.json) |
| `B` | 突 | [《史記・鄭世家》][590] | [JSON](muq_yy8_8er_B.json) |

</details>

<details><summary><code>mwc_md4_l0g</code> 王含（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 王含 | [《晉書・叛臣一》][221] | [JSON](mwc_md4_l0g.json) |
| `A` | 王應 | [《晉書・叛臣一》][221] | [JSON](mwc_md4_l0g_A.json) |
| `B` | 王瑜〔王含子、散騎常侍〕 | [《晉書・叛臣一》][221] | [JSON](mwc_md4_l0g_B.json) |

</details>

<details><summary><code>mxz_qw8_acd</code> 王揖（4 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 王揖 | [《南史・王曇首》][469]、[《南史・王曇首》][473] | [JSON](mxz_qw8_acd.json) |
| `A` | 王筠 | [《梁書・王僧孺 張率 劉孝綽 王筠》][266]、[《梁書・王僧孺 張率 劉孝綽 王筠》][265] | [JSON](mxz_qw8_acd_A.json) |
| `AA` | 王祥（王筠子） | [《南史・王曇首》][471]、[《南史・王曇首》][470]、[《隋書・文學》][832] | [JSON](mxz_qw8_acd_AA.json) |
| `AAA` | 王胄（字承基） | [《隋書・文學》][832] | [JSON](mxz_qw8_acd_AAA.json) |

</details>

<details><summary><code>n0i_g82_0n2</code> 蒯聵（衛莊公）（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 蒯聵（衛莊公） | [《史記・衛康叔世家》][585] | [JSON](n0i_g82_0n2.json) |
| `A` | 輒（衛出公） | [《史記・衛康叔世家》][585] | [JSON](n0i_g82_0n2_A.json) |
| `AA` | 出公子（衛黔所攻者未名） | [《史記・衛康叔世家》][585] | [JSON](n0i_g82_0n2_AA.json) |

</details>

<details><summary><code>n2x_d8l_n0d</code> 嵇翰（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 嵇翰 | [《晉書・忠義》][200] | [JSON](n2x_d8l_n0d.json) |
| `*A` | 嵇曠 | [《晉書・忠義》][200] | [JSON](n2x_d8l_n0d_%2AA.json) |

</details>

<details><summary><code>n3u_6wg_kay</code> 隆（張次公父）（衛將軍驃騎列傳候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 隆（張次公父） | [《史記・衛將軍驃騎列傳》][659] | [JSON](n3u_6wg_kay.json) |
| `A` | 張次公 | [《史記・衛將軍驃騎列傳》][659] | [JSON](n3u_6wg_kay_A.json) |

</details>

<details><summary><code>n4f_fqh_04q</code> 易王（燕君）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 易王（燕君） | [《史記・蘇秦列傳》][617] | [JSON](n4f_fqh_04q.json) |
| `A` | 燕噲（本篇燕君） | [《史記・燕召公世家》][582] | [JSON](n4f_fqh_04q_A.json) |

</details>

<details><summary><code>nbl_2bu_99w</code> 王舒（4 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 王舒 | [《晉書・王舒 王廙 虞潭 顧眾 張闓》][192] | [JSON](nbl_2bu_99w.json) |
| `A` | 王晏之 | [《晉書・王舒 王廙 虞潭 顧眾 張闓》][192] | [JSON](nbl_2bu_99w_A.json) |
| `AA` | 王崐之 | [《晉書・王舒 王廙 虞潭 顧眾 張闓》][192] | [JSON](nbl_2bu_99w_AA.json) |
| `AAA` | 王陋之 | [《晉書・王舒 王廙 虞潭 顧眾 張闓》][192] | [JSON](nbl_2bu_99w_AAA.json) |

</details>

<details><summary><code>nf1_c66_863</code> 楊季主（游俠列傳候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 楊季主 | [《史記・游俠列傳》][672] | [JSON](nf1_c66_863.json) |
| `A` | 楊季主子（未名縣掾） | [《史記・游俠列傳》][672] | [JSON](nf1_c66_863_A.json) |

</details>

<details><summary><code>nfj_6w2_8mn</code> 增（魏世家景湣王候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 增 | [《史記・魏世家》][592] | [JSON](nfj_6w2_8mn.json) |
| `A` | 假 | [《史記・魏世家》][592] | [JSON](nfj_6w2_8mn_A.json) |

</details>

<details><summary><code>nuf_tb9_fjs</code> 竇嬰父（未名）（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 竇嬰父（未名） | [《史記・魏其武安列傳》][655] | [JSON](nuf_tb9_fjs.json) |
| `A` | 竇嬰 | [《史記・魏其武安列傳》][655] | [JSON](nuf_tb9_fjs_A.json) |
| `AA` | 竇嬰子未名 | [《史記・魏其武安列傳》][655] | [JSON](nuf_tb9_fjs_AA.json) |

</details>

<details><summary><code>nxl_qt6_cpl</code> 畢萬（魏世家候選）（9 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 畢萬 | [《史記・魏世家》][592] | [JSON](nxl_qt6_cpl.json) |
| `A` | 魏武子 | [《史記・魏世家》][592] | [JSON](nxl_qt6_cpl_A.json) |
| `AA` | 魏悼子 | [《史記・魏世家》][592] | [JSON](nxl_qt6_cpl_AA.json) |
| `AAA` | 魏絳 | [《史記・魏世家》][592] | [JSON](nxl_qt6_cpl_AAA.json) |
| `AAAA` | 魏嬴 | [《史記・魏世家》][592] | [JSON](nxl_qt6_cpl_AAAA.json) |
| `AAAAA` | 魏獻子 | [《史記・魏世家》][592] | [JSON](nxl_qt6_cpl_AAAAA.json) |
| `AAAAAA` | 魏侈 | [《史記・魏世家》][592] | [JSON](nxl_qt6_cpl_AAAAAA.json) |
| `AAAAAA*A` | 魏桓子 | [《史記・魏世家》][592] | [JSON](nxl_qt6_cpl_AAAAAA%2AA.json) |
| `AAAAAA*A*A` | 都 | [《史記・魏世家》][592] | [JSON](nxl_qt6_cpl_AAAAAA%2AA%2AA.json) |

</details>

<details><summary><code>nye_x8g_zwl</code> 陳桓公鮑（田世家候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 陳桓公鮑 | [《史記・田敬仲完世家》][594] | [JSON](nye_x8g_zwl.json) |
| `A` | 陳莊公林 | [《史記・田敬仲完世家》][594] | [JSON](nye_x8g_zwl_A.json) |

</details>

<details><summary><code>o0l_em5_5v9</code> 吳芮（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 吳芮 | [《史記・高祖本紀》][574] | [JSON](o0l_em5_5v9.json) |
| `A` | 臣（吳芮子） | [《史記・呂后本紀》][575]、[《史記・黥布列傳》][639]、[《史記・漢興以來諸侯王年表》][899] | [JSON](o0l_em5_5v9_A.json) |
| `B` | 英布妻未名 | [《史記・黥布列傳》][639] | [JSON](o0l_em5_5v9_B.json) |

</details>

<details><summary><code>opr_t0a_l8g</code> 淳于公（齊太倉令）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 淳于公（齊太倉令） | [《史記・扁鵲倉公列傳》][653] | [JSON](opr_t0a_l8g.json) |
| `A` | 緹縈 | [《史記・扁鵲倉公列傳》][653] | [JSON](opr_t0a_l8g_A.json) |

</details>

<details><summary><code>osu_yvw_bwr</code> 熊惲（楚成王候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 熊惲 | [《史記・楚世家》][588] | [JSON](osu_yvw_bwr.json) |
| `A` | 職（楚成王欲立之子） | [《史記・楚世家》][588] | [JSON](osu_yvw_bwr_A.json) |

</details>

<details><summary><code>p4b_qf7_603</code> 趙武（趙庶子）（4 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 趙武（趙庶子） | [《史記・趙世家》][591] | [JSON](p4b_qf7_603.json) |
| `A` | 趙景叔 | [《史記・趙世家》][591] | [JSON](p4b_qf7_603_A.json) |
| `AA` | 趙鞅 | [《史記・趙世家》][591] | [JSON](p4b_qf7_603_AA.json) |
| `AAA` | 趙襄子毋卹 | [《史記・趙世家》][591] | [JSON](p4b_qf7_603_AAA.json) |

</details>

<details><summary><code>p6s_2qn_p8n</code> 平原侯植（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 平原侯植 | [《三國志・任城陳蕭王傳》][554] | [JSON](p6s_2qn_p8n.json) |
| `A` | 曹志〔字允恭〕 | [《晉書・曹志 庾峻 郭象 庾純 秦秀》][151] | [JSON](p6s_2qn_p8n_A.json) |

</details>

<details><summary><code>p93_tgr_t8r</code> 王遠（4 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 王遠 | [《南史・王弘》][451] | [JSON](p93_tgr_t8r.json) |
| `A` | 王僧祐 | [《南齊書・王秀之 王慈 蔡約 陸慧曉 顧憲之 蕭惠基》][355]、[《南史・王弘》][446] | [JSON](p93_tgr_t8r_A.json) |
| `AA` | 王籍〔字文海〕 | [《梁書・文學下》][272]、[《南史・王弘》][443] | [JSON](p93_tgr_t8r_AA.json) |
| `AAA` | 王碧（王籍子） | [《梁書・文學下》][272] | [JSON](p93_tgr_t8r_AAA.json) |

</details>

<details><summary><code>p9l_wy7_y7m</code> 魏文侯（孫吳列傳候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 魏文侯 | [《史記・孫子吳起列傳》][613] | [JSON](p9l_wy7_y7m.json) |
| `A` | 魏武侯 | [《史記・孫子吳起列傳》][613] | [JSON](p9l_wy7_y7m_A.json) |

</details>

<details><summary><code>pbz_pni_tco</code> 何偃（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 何偃 | [《宋書・羊欣 張敷 王微》][791] | [JSON](pbz_pni_tco.json) |
| `A` | 何戢 | [《南史・后妃上》][384]、[《南史・后妃上》][385] | [JSON](pbz_pni_tco_A.json) |
| `AA` | 何婧英 | [《南史・后妃上》][384]、[《南史・后妃上》][385] | [JSON](pbz_pni_tco_AA.json) |

</details>

<details><summary><code>pev_wez_mab</code> 宋富人（老韓列傳候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 宋富人 | [《史記・老子韓非列傳》][611] | [JSON](pev_wez_mab.json) |
| `A` | 富人之子 | [《史記・老子韓非列傳》][611] | [JSON](pev_wez_mab_A.json) |

</details>

<details><summary><code>pg6_rqk_vuk</code> 如姬父未名（魏公子列傳候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 如姬父未名 | [《史記・魏公子列傳》][625] | [JSON](pg6_rqk_vuk.json) |
| `A` | 如姬 | [《史記・魏公子列傳》][625] | [JSON](pg6_rqk_vuk_A.json) |

</details>

<details><summary><code>ph1_ms8_hyq</code> 亮〔孝懿蕭后祖；字保祚〕（7 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 亮〔孝懿蕭后祖；字保祚〕 | [《宋書・后妃》][754] | [JSON](ph1_ms8_hyq.json) |
| `A` | 蕭卓 | [《宋書・后妃》][754] | [JSON](ph1_ms8_hyq_A.json) |
| `AA` | 蕭文夀〔孝懿皇后〕 | [《宋書・后妃》][754] | [JSON](ph1_ms8_hyq_AA.json) |
| `AB` | 源之〔蕭卓子〕 | [《宋書・后妃》][754] | [JSON](ph1_ms8_hyq_AB.json) |
| `ABA` | 蕭思話 | [《南齊書・王僧虔 張緒》][330]、[《南史・王曇首》][464] | [JSON](ph1_ms8_hyq_ABA.json) |
| `ABAA` | 蕭惠基 | [《南齊書・王秀之 王慈 蔡約 陸慧曉 顧憲之 蕭惠基》][354]、[《南史・王曇首》][464] | [JSON](ph1_ms8_hyq_ABAA.json) |
| `ABAB` | 蕭惠明（蕭思話次子） | [《南史・王誕　王華　王惠　王彧》][497]、[《宋書・蕭思話 劉延孫》][811] | [JSON](ph1_ms8_hyq_ABAB.json) |

</details>

<details><summary><code>pib_5me_1wm</code> 陳肇之（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 陳肇之 | [《南齊書・皇后》][290]、[《南齊書・皇后》][289] | [JSON](pib_5me_1wm.json) |
| `A` | 陳道止 | [《南史・后妃上》][379]、[《南史・后妃上》][380] | [JSON](pib_5me_1wm_A.json) |

</details>

<details><summary><code>pj3_k53_wtj</code> 觸龍（趙世家左師候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 觸龍 | [《史記・趙世家》][591] | [JSON](pj3_k53_wtj.json) |
| `A` | 舒祺 | [《史記・趙世家》][591] | [JSON](pj3_k53_wtj_A.json) |

</details>

<details><summary><code>pme_eis_xqi</code> 司馬錯（7 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 司馬錯 | [《史記・秦本紀》][571] | [JSON](pme_eis_xqi.json) |
| `*A` | 司馬靳 | [《史記・太史公自序》][678] | [JSON](pme_eis_xqi_%2AA.json) |
| `*A*A` | 司馬昌 | [《史記・太史公自序》][678] | [JSON](pme_eis_xqi_%2AA%2AA.json) |
| `*A*AA` | 司馬無澤 | [《史記・太史公自序》][678] | [JSON](pme_eis_xqi_%2AA%2AAA.json) |
| `*A*AAA` | 司馬喜 | [《史記・太史公自序》][678] | [JSON](pme_eis_xqi_%2AA%2AAAA.json) |
| `*A*AAAA` | 司馬談 | [《史記・太史公自序》][678] | [JSON](pme_eis_xqi_%2AA%2AAAAA.json) |
| `*A*AAAAA` | 司馬遷 | [《史記・太史公自序》][678] | [JSON](pme_eis_xqi_%2AA%2AAAAAA.json) |

</details>

<details><summary><code>pne_ii9_42q</code> 王廣〔西揚州刺史〕（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 王廣〔西揚州刺史〕 | [《太平御覽・人事部八十一》][841] | [JSON](pne_ii9_42q.json) |
| `A` | 王氏〔西揚州刺史王廣女〕 | [《晉書・列女》][212]、[《晉書・列女》][211]、[《太平御覽・人事部八十一》][841]、[《太平御覽・宗親部九》][842] | [JSON](pne_ii9_42q_A.json) |

</details>

<details><summary><code>ptn_sz3_vro</code> 劉義慶（4 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 劉義慶 | [《宋書・謝靈運》][798] | [JSON](ptn_sz3_vro.json) |
| `A` | 臨川王義慶女（王僧達妻，未名） | [《宋書・王僧達 顏竣》][806] | [JSON](ptn_sz3_vro_A.json) |
| `B` | 劉燁（字景舒，臨川哀王） | [《南史・宋宗室及諸王上》][406] | [JSON](ptn_sz3_vro_B.json) |
| `BA` | 劉綽（宋宗室） | [《南史・宋宗室及諸王上》][406]、[《宋書・后妃》][756] | [JSON](ptn_sz3_vro_BA.json) |

</details>

<details><summary><code>pyb_nda_bwz</code> 鄖公與懷之父（伍胥列傳候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 鄖公與懷之父 | [《史記・伍子胥列傳》][614] | [JSON](pyb_nda_bwz.json) |
| `A` | 懷 | [《史記・伍子胥列傳》][614] | [JSON](pyb_nda_bwz_A.json) |

</details>

<details><summary><code>q1y_uet_htw</code> 伯州犁（伍胥列傳候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 伯州犁 | [《史記・伍子胥列傳》][614] | [JSON](q1y_uet_htw.json) |
| `*A` | 伯嚭 | [《史記・伍子胥列傳》][614] | [JSON](q1y_uet_htw_%2AA.json) |

</details>

<details><summary><code>q60_34y_1zh</code> 章（楚惠王）（5 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 章（楚惠王） | [《史記・楚世家》][588] | [JSON](q60_34y_1zh.json) |
| `A` | 中（楚簡王） | [《史記・楚世家》][588] | [JSON](q60_34y_1zh_A.json) |
| `AA` | 當（楚聲王） | [《史記・楚世家》][588] | [JSON](q60_34y_1zh_AA.json) |
| `AAA` | 熊疑（楚悼王） | [《史記・范睢蔡澤列傳》][627] | [JSON](q60_34y_1zh_AAA.json) |
| `AAAA` | 臧（楚肅王） | [《史記・楚世家》][588] | [JSON](q60_34y_1zh_AAAA.json) |

</details>

<details><summary><code>q63_4br_3of</code> 江德隣（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 江德隣 | [《南史・荀伯玉　崔祖思　蘇侃　虞悰　胡諧之　虞玩之　劉休　江祏》][529] | [JSON](q63_4br_3of.json) |
| `A` | 江祏 | [《南史・謝晦　謝裕　謝方明　謝靈運》][432] | [JSON](q63_4br_3of_A.json) |
| `B` | 江祀 | [《南史・謝晦　謝裕　謝方明　謝靈運》][432] | [JSON](q63_4br_3of_B.json) |

</details>

<details><summary><code>q69_35n_f3h</code> 公孫弘（平津侯主父列傳候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 公孫弘 | [《史記・平津侯主父列傳》][660] | [JSON](q69_35n_f3h.json) |
| `A` | 公孫度 | [《史記・平津侯主父列傳》][660] | [JSON](q69_35n_f3h_A.json) |

</details>

<details><summary><code>q6w_qm5_w2b</code> 丹（趙世家孝成王候選）（4 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 丹 | [《史記・平原君虞卿列傳》][624] | [JSON](q6w_qm5_w2b.json) |
| `A` | 偃 | [《史記・趙世家》][591] | [JSON](q6w_qm5_w2b_A.json) |
| `AA` | 趙王遷 | [《史記・趙世家》][591] | [JSON](q6w_qm5_w2b_AA.json) |
| `AB` | 代王嘉 | [《史記・秦始皇本紀》][572]、[《史記・六國年表》][897] | [JSON](q6w_qm5_w2b_AB.json) |

</details>

<details><summary><code>q71_dto_v57</code> 秦宜禄（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 秦宜禄 | [《三國志・諸夏侯曹傳》][541] | [JSON](q71_dto_v57.json) |
| `A` | 秦朗 | [《三國志・諸夏侯曹傳》][541] | [JSON](q71_dto_v57_A.json) |

</details>

<details><summary><code>q7c_rp0_s04</code> 趙主父（楚篇懷王奔趙時）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 趙主父（楚篇懷王奔趙時） | [《史記・楚世家》][588] | [JSON](q7c_rp0_s04.json) |
| `A` | 趙惠王（楚篇初立者） | [《史記・楚世家》][588] | [JSON](q7c_rp0_s04_A.json) |

</details>

[1]: https://zh.wikisource.org/w/index.php?title=北史/卷016&oldid=1518816
[6]: https://zh.wikisource.org/w/index.php?title=北史/卷044&oldid=2183262
[7]: https://zh.wikisource.org/w/index.php?title=冊府元龜_(四庫全書本)/全覽10&oldid=650326
[11]: https://zh.wikisource.org/w/index.php?oldid=8231316
[14]: https://zh.wikisource.org/w/index.php?oldid=2015446
[16]: https://zh.wikisource.org/w/index.php?oldid=1488469
[24]: https://www.sohu.com/a/259439652_258370
[25]: https://guji.10huan.com/Article/7147_7165.html
[26]: https://www.dpm.org.cn/collection/impres/230177.html
[27]: https://www.dpm.org.cn/collection/impres/230096.html
[29]: https://homepage.ntu.edu.tw/~history/public_html/newsletter/public_html/09newsletter/03/newsletter3_09.pdf#page=3
[31]: https://homepage.ntu.edu.tw/~history/public_html/newsletter/public_html/09newsletter/04/newsletter4_23.pdf
[33]: http://csid.zju.edu.cn/tomb/stone/detail?id=40288b955bd07752015bfb74a80002de
[34]: https://www.i-repository.net/il/cont/01/G0000721f/000/756/000756311.jpg
[39]: https://zh.wikisource.org/w/index.php?oldid=636080
[41]: https://github.com/kanripo/KR2a0007/blob/683113d4baf6febecaf2ccb7913df87c4d68d454/KR2a0007_007.txt
[43]: https://zh.wikisource.org/w/index.php?title=漢書/卷041&oldid=2342290
[44]: https://github.com/kanripo/KR2a0007/blob/683113d4baf6febecaf2ccb7913df87c4d68d454/KR2a0007_050.txt
[45]: https://github.com/kanripo/KR2a0007/blob/683113d4baf6febecaf2ccb7913df87c4d68d454/KR2a0007_059.txt
[49]: https://zh.wikisource.org/w/index.php?oldid=2605445
[50]: https://github.com/kanripo/KR2a0007/blob/683113d4baf6febecaf2ccb7913df87c4d68d454/KR2a0007_098.txt
[51]: https://github.com/kanripo/KR2a0009/blob/6db36b6dcbe843b825354c22e9be9193d0137c04/KR2a0009_009.txt
[53]: https://github.com/kanripo/KR2a0009/blob/6db36b6dcbe843b825354c22e9be9193d0137c04/KR2a0009_092.txt
[55]: https://github.com/kanripo/KR2a0009/blob/6db36b6dcbe843b825354c22e9be9193d0137c04/KR2a0009_094.txt
[58]: https://zh.wikisource.org/w/index.php?oldid=1458097
[62]: https://zh.wikisource.org/w/index.php?oldid=2603565
[73]: https://zh.wikisource.org/w/index.php?oldid=7904721
[80]: https://raw.githubusercontent.com/kanripo/KR2a0015/82291520954e5af1fdade894971a2f5810fd4e31/KR2a0015_006.txt
[105]: https://zh.wikisource.org/w/index.php?oldid=2479706
[109]: https://zh.wikisource.org/w/index.php?title=%E6%99%89%E6%9B%B8%2F%E5%8D%B7032&oldid=1543614
[112]: https://zh.wikisource.org/w/index.php?title=%E6%99%89%E6%9B%B8%2F%E5%8D%B7032&oldid=1543614
[113]: https://zh.wikisource.org/w/index.php?title=%E6%99%89%E6%9B%B8%2F%E5%8D%B7033&oldid=2650519
[115]: https://zh.wikisource.org/w/index.php?oldid=2108231
[117]: https://zh.wikisource.org/w/index.php?title=%E6%99%89%E6%9B%B8%2F%E5%8D%B7037&oldid=2630018
[118]: https://zh.wikisource.org/w/index.php?oldid=2444513
[119]: https://zh.wikisource.org/w/index.php?title=晉書/卷039&oldid=2108782
[121]: https://zh.wikisource.org/w/index.php?title=晉書/卷042&oldid=2180524
[123]: https://zh.wikisource.org/w/index.php?oldid=2618531
[124]: https://zh.wikisource.org/w/index.php?oldid=2618531
[125]: https://zh.wikisource.org/w/index.php?oldid=2618531
[126]: https://zh.wikisource.org/w/index.php?oldid=2618531
[127]: https://zh.wikisource.org/w/index.php?oldid=2618531
[130]: https://zh.wikisource.org/w/index.php?title=晉書/卷043&oldid=2618531
[133]: https://zh.wikisource.org/w/index.php?oldid=1775345
[134]: https://zh.wikisource.org/w/index.php?oldid=1775345
[135]: https://zh.wikisource.org/w/index.php?oldid=1775345
[136]: https://zh.wikisource.org/w/index.php?oldid=1775345
[137]: https://zh.wikisource.org/w/index.php?oldid=1775345
[138]: https://zh.wikisource.org/w/index.php?oldid=1775345
[139]: https://zh.wikisource.org/w/index.php?oldid=1775345
[141]: https://zh.wikisource.org/w/index.php?oldid=1775345
[143]: https://zh.wikisource.org/w/index.php?oldid=1775345
[144]: https://zh.wikisource.org/w/index.php?oldid=1775345
[146]: https://zh.wikisource.org/w/index.php?oldid=1775345
[147]: https://zh.wikisource.org/w/index.php?oldid=1775345
[151]: https://zh.wikisource.org/w/index.php?oldid=2305862
[158]: https://zh.wikisource.org/w/index.php?title=晉書/卷059&oldid=2650517
[159]: https://zh.wikisource.org/w/index.php?title=晉書/卷059&oldid=2650517
[160]: https://zh.wikisource.org/w/index.php?title=晉書/卷059&oldid=2650517
[161]: https://zh.wikisource.org/w/index.php?oldid=7903772
[162]: https://zh.wikisource.org/w/index.php?title=%E6%99%89%E6%9B%B8%2F%E5%8D%B7061&oldid=7903772
[163]: https://zh.wikisource.org/w/index.php?oldid=2629226
[167]: https://zh.wikisource.org/w/index.php?title=%E6%99%89%E6%9B%B8%2F%E5%8D%B7064&oldid=2622004
[169]: https://zh.wikisource.org/w/index.php?title=%E6%99%89%E6%9B%B8%2F%E5%8D%B7065&oldid=1756144
[170]: https://zh.wikisource.org/w/index.php?oldid=1527632
[171]: https://zh.wikisource.org/w/index.php?oldid=2592755
[172]: https://zh.wikisource.org/w/index.php?oldid=2592755
[173]: https://zh.wikisource.org/w/index.php?oldid=2592755
[175]: https://commons.wikimedia.org/w/index.php?oldid=1047611719
[176]: https://zh.wikisource.org/w/index.php?oldid=2592755
[177]: https://commons.wikimedia.org/w/index.php?oldid=1047611719
[178]: https://zh.wikisource.org/w/index.php?oldid=2592755
[179]: https://zh.wikisource.org/w/index.php?title=%E6%99%89%E6%9B%B8%2F%E5%8D%B7069&oldid=2012453
[181]: https://zh.wikisource.org/w/index.php?oldid=2296501
[182]: https://zh.wikisource.org/w/index.php?oldid=2296501
[183]: https://zh.wikisource.org/w/index.php?title=晉書/卷074&oldid=1536331
[185]: https://zh.wikisource.org/w/index.php?title=晉書/卷075&oldid=2645530
[187]: https://zh.wikisource.org/w/index.php?title=晉書/卷075&oldid=2645530
[188]: https://zh.wikisource.org/w/index.php?oldid=2180533
[189]: https://zh.wikisource.org/w/index.php?title=%E6%99%89%E6%9B%B8%2F%E5%8D%B7076&oldid=2180533
[190]: https://zh.wikisource.org/w/index.php?title=%E6%99%89%E6%9B%B8%2F%E5%8D%B7076&oldid=2180533
[191]: https://zh.wikisource.org/w/index.php?title=%E6%99%89%E6%9B%B8%2F%E5%8D%B7076&oldid=2180533
[192]: https://zh.wikisource.org/w/index.php?oldid=2180533
[193]: https://zh.wikisource.org/w/index.php?title=%E6%99%89%E6%9B%B8%2F%E5%8D%B7076&oldid=2180533
[194]: https://zh.wikisource.org/w/index.php?title=%E6%99%89%E6%9B%B8%2F%E5%8D%B7077&oldid=8750392
[195]: https://zh.wikisource.org/w/index.php?title=%E6%99%89%E6%9B%B8%2F%E5%8D%B7079&oldid=2645985
[196]: https://zh.wikisource.org/w/index.php?oldid=2603570
[197]: https://upload.wikimedia.org/wikipedia/commons/3/30/NLC016-HWRB201817005-3307_%E6%99%89%E6%9B%B8_%E4%B8%80%E7%99%BE%E4%B8%89%E5%8D%81%E5%8D%B7_%E9%9F%B3%E7%BE%A9%E4%B8%89%E5%8D%B7_%E7%AC%AC20%E5%86%8A.pdf#page=27
[199]: https://zh.wikisource.org/w/index.php?oldid=2835777
[200]: https://zh.wikisource.org/w/index.php?title=%E6%99%89%E6%9B%B8%2F%E5%8D%B7089&oldid=2835777
[201]: https://zh.wikisource.org/w/index.php?title=晉書/卷090&oldid=2835599
[207]: https://zh.wikisource.org/w/index.php?oldid=1548000
[211]: https://commons.wikimedia.org/w/index.php?oldid=979438884
[212]: https://zh.wikisource.org/w/index.php?oldid=2625341
[215]: https://commons.wikimedia.org/w/index.php?oldid=979438884
[216]: https://zh.wikisource.org/w/index.php?oldid=2625341
[220]: https://zh.wikisource.org/w/index.php?title=晉書/卷098&oldid=2614273
[221]: https://zh.wikisource.org/w/index.php?oldid=2614273
[222]: https://zh.wikisource.org/w/index.php?oldid=2614273
[223]: https://zh.wikisource.org/w/index.php?oldid=2614273
[224]: https://zh.wikisource.org/w/index.php?title=晉書/卷099&oldid=2644703
[227]: https://zh.wikisource.org/w/index.php?title=%E6%99%89%E6%9B%B8%2F%E5%8D%B7100&oldid=2614279
[228]: https://zh.wikisource.org/w/index.php?oldid=2614290
[232]: https://zh.wikisource.org/w/index.php?title=舊唐書/卷89&oldid=2589393
[240]: https://zh.wikisource.org/w/index.php?title=梁書/卷07&oldid=1566494
[242]: https://zh.wikisource.org/w/index.php?title=梁書/卷08&oldid=1538023
[243]: https://zh.wikisource.org/w/index.php?title=梁書/卷15&oldid=1506954
[245]: https://zh.wikisource.org/w/index.php?oldid=2063232
[248]: https://zh.wikisource.org/w/index.php?oldid=1544250
[249]: https://zh.wikisource.org/w/index.php?oldid=1544250
[250]: https://zh.wikisource.org/w/index.php?title=梁書/卷21&oldid=1544250
[252]: https://commons.wikimedia.org/w/index.php?oldid=902340163
[253]: https://zh.wikisource.org/w/index.php?oldid=1544250
[254]: https://commons.wikimedia.org/w/index.php?oldid=902340163
[255]: https://zh.wikisource.org/w/index.php?oldid=1544250
[258]: https://zh.wikisource.org/w/index.php?oldid=1511478
[261]: https://zh.wikisource.org/w/index.php?oldid=1538079
[262]: https://zh.wikisource.org/w/index.php?oldid=1538079
[263]: https://zh.wikisource.org/w/index.php?title=%E6%A2%81%E6%9B%B8%2F%E5%8D%B730&oldid=1508510
[264]: https://zh.wikisource.org/w/index.php?oldid=1514481
[265]: https://commons.wikimedia.org/wiki/File:NLC892-411999017142-12700_二十四史_第167冊.pdf
[266]: https://zh.wikisource.org/w/index.php?oldid=1514481
[267]: https://zh.wikisource.org/w/index.php?oldid=1514481
[268]: https://zh.wikisource.org/w/index.php?oldid=1511900
[269]: https://zh.wikisource.org/w/index.php?title=梁書/卷41&oldid=1512987
[270]: https://zh.wikisource.org/w/index.php?oldid=1512987
[272]: https://zh.wikisource.org/w/index.php?oldid=1514482
[273]: https://commons.wikimedia.org/w/index.php?oldid=703777627
[274]: https://zh.wikisource.org/w/index.php?title=梁書/卷50&oldid=1514482
[275]: https://zh.wikisource.org/w/index.php?title=梁書/卷50&oldid=1514482
[276]: https://commons.wikimedia.org/w/index.php?oldid=703777627
[277]: https://zh.wikisource.org/w/index.php?title=梁書/卷50&oldid=1514482
[278]: https://zh.wikisource.org/w/index.php?oldid=1530936
[279]: https://zh.wikisource.org/w/index.php?oldid=1530936
[280]: https://zh.wikisource.org/w/index.php?oldid=2312009
[281]: https://zh.wikisource.org/w/index.php?title=南齊書/卷2&oldid=2312009
[289]: https://commons.wikimedia.org/w/index.php?oldid=703777584
[290]: https://zh.wikisource.org/w/index.php?oldid=2074177
[291]: https://commons.wikimedia.org/w/index.php?oldid=703777584
[292]: https://zh.wikisource.org/w/index.php?oldid=2074177
[296]: https://commons.wikimedia.org/w/index.php?oldid=703777584
[297]: https://zh.wikisource.org/w/index.php?title=南齊書/卷20&oldid=2074177
[298]: https://zh.wikisource.org/w/index.php?title=南齊書/卷20&oldid=2074177
[299]: https://commons.wikimedia.org/w/index.php?oldid=703777584
[300]: https://zh.wikisource.org/w/index.php?oldid=2074177
[301]: https://commons.wikimedia.org/w/index.php?oldid=703777584
[302]: https://zh.wikisource.org/w/index.php?oldid=2074177
[303]: https://commons.wikimedia.org/w/index.php?oldid=703777584
[304]: https://zh.wikisource.org/w/index.php?oldid=2074177
[305]: https://commons.wikimedia.org/w/index.php?oldid=703777584
[306]: https://zh.wikisource.org/w/index.php?title=南齊書/卷20&oldid=2074177
[308]: https://zh.wikisource.org/w/index.php?title=南齊書/卷23&oldid=1545488
[309]: https://zh.wikisource.org/w/index.php?title=南齊書/卷24&oldid=1507882
[314]: https://zh.wikisource.org/w/index.php?oldid=1508012
[317]: https://zh.wikisource.org/w/index.php?oldid=1508012
[318]: https://zh.wikisource.org/w/index.php?oldid=1508012
[321]: https://zh.wikisource.org/w/index.php?oldid=1513917
[322]: https://zh.wikisource.org/w/index.php?oldid=2062531
[323]: https://zh.wikisource.org/w/index.php?oldid=1513918
[325]: https://zh.wikisource.org/w/index.php?oldid=1513918
[326]: https://zh.wikisource.org/w/index.php?oldid=1513918
[327]: https://zh.wikisource.org/w/index.php?oldid=1513918
[328]: https://zh.wikisource.org/w/index.php?oldid=1513918
[329]: https://zh.wikisource.org/w/index.php?title=%E5%8D%97%E9%BD%8A%E6%9B%B8%2F%E5%8D%B732&oldid=1513918
[330]: https://github.com/kanripo/KR2a0017/blob/787dd9a7da495542e8f17c26c96900ce37b2c211/KR2a0017_033.txt
[331]: https://zh.wikisource.org/w/index.php?title=南齊書/卷33&oldid=1492444
[332]: https://zh.wikisource.org/w/index.php?oldid=1514487
[333]: https://zh.wikisource.org/w/index.php?oldid=2401782
[334]: https://zh.wikisource.org/w/index.php?oldid=2401782
[335]: https://zh.wikisource.org/w/index.php?title=南齊書/卷36&oldid=1492438
[336]: https://commons.wikimedia.org/w/index.php?oldid=1154634011
[337]: https://zh.wikisource.org/w/index.php?title=南齊書/卷36&oldid=1492438
[338]: https://zh.wikisource.org/w/index.php?title=南齊書/卷39&oldid=1545485
[339]: https://zh.wikisource.org/w/index.php?oldid=2272748
[340]: https://zh.wikisource.org/w/index.php?oldid=2272748
[341]: https://zh.wikisource.org/w/index.php?oldid=2272748
[342]: https://zh.wikisource.org/w/index.php?oldid=2272748
[344]: https://zh.wikisource.org/w/index.php?oldid=2272748
[345]: https://zh.wikisource.org/w/index.php?oldid=1507997
[348]: https://zh.wikisource.org/w/index.php?oldid=2400356
[349]: https://zh.wikisource.org/w/index.php?oldid=2400356
[350]: https://zh.wikisource.org/w/index.php?title=南齊書/卷43&oldid=2400356
[351]: https://zh.wikisource.org/w/index.php?title=南齊書/卷44&oldid=1507959
[352]: https://zh.wikisource.org/w/index.php?title=南齊書/卷45&oldid=2273185
[353]: https://zh.wikisource.org/w/index.php?title=南齊書/卷45&oldid=2273185
[354]: https://zh.wikisource.org/w/index.php?oldid=1511897
[355]: https://zh.wikisource.org/w/index.php?title=%E5%8D%97%E9%BD%8A%E6%9B%B8%2F%E5%8D%B746&oldid=1511897
[356]: https://commons.wikimedia.org/wiki/File:NLC892-411999017142-12542_二十四史_第161冊.pdf
[357]: https://zh.wikisource.org/w/index.php?oldid=1492435
[358]: https://zh.wikisource.org/w/index.php?title=南齊書/卷47&oldid=1492435
[360]: https://zh.wikisource.org/w/index.php?oldid=2261984
[363]: https://zh.wikisource.org/w/index.php?oldid=2261984
[364]: https://zh.wikisource.org/w/index.php?oldid=2261984
[366]: https://zh.wikisource.org/w/index.php?oldid=2261984
[367]: https://zh.wikisource.org/w/index.php?oldid=2261984
[368]: https://zh.wikisource.org/w/index.php?oldid=2261984
[374]: https://zh.wikisource.org/w/index.php?oldid=1501803
[379]: https://commons.wikimedia.org/w/index.php?oldid=1298729844
[380]: https://zh.wikisource.org/w/index.php?oldid=2288359
[381]: https://commons.wikimedia.org/w/index.php?oldid=1298729844
[382]: https://zh.wikisource.org/w/index.php?oldid=2288359
[384]: https://commons.wikimedia.org/w/index.php?oldid=1298729844
[385]: https://zh.wikisource.org/w/index.php?oldid=2288359
[386]: https://commons.wikimedia.org/w/index.php?oldid=1298729844
[387]: https://zh.wikisource.org/w/index.php?oldid=2288359
[388]: https://commons.wikimedia.org/w/index.php?oldid=1298729844
[389]: https://zh.wikisource.org/w/index.php?oldid=2288359
[391]: https://zh.wikisource.org/w/index.php?title=南史/卷11&oldid=2288359
[396]: https://commons.wikimedia.org/w/index.php?oldid=1298729844
[397]: https://zh.wikisource.org/w/index.php?oldid=2288359
[398]: https://commons.wikimedia.org/w/index.php?oldid=1298729844
[399]: https://zh.wikisource.org/w/index.php?oldid=2288359
[400]: https://zh.wikisource.org/w/index.php?oldid=2288359
[401]: https://zh.wikisource.org/w/index.php?oldid=2288359
[402]: https://zh.wikisource.org/w/index.php?title=南史/卷11&oldid=2288359
[403]: https://zh.wikisource.org/w/index.php?title=南史/卷11&oldid=2288359
[404]: https://zh.wikisource.org/w/index.php?oldid=2060595
[405]: https://zh.wikisource.org/w/index.php?oldid=2060595
[406]: https://zh.wikisource.org/w/index.php?oldid=2268660
[407]: https://zh.wikisource.org/w/index.php?oldid=2268660
[408]: https://zh.wikisource.org/w/index.php?oldid=1963381
[409]: https://zh.wikisource.org/w/index.php?oldid=1963381
[410]: https://zh.wikisource.org/w/index.php?oldid=1963381
[412]: https://zh.wikisource.org/w/index.php?oldid=1963381
[415]: https://zh.wikisource.org/w/index.php?oldid=1963381
[417]: https://zh.wikisource.org/w/index.php?oldid=1963381
[418]: https://zh.wikisource.org/w/index.php?oldid=1531762
[420]: https://zh.wikisource.org/w/index.php?oldid=1531762
[426]: https://zh.wikisource.org/w/index.php?title=南史/卷19&oldid=1531762
[429]: https://zh.wikisource.org/w/index.php?title=南史/卷19&oldid=1531762
[430]: https://zh.wikisource.org/w/index.php?title=南史/卷19&oldid=1531762
[431]: https://zh.wikisource.org/w/index.php?title=南史/卷19&oldid=1531762
[432]: https://zh.wikisource.org/w/index.php?title=南史/卷19&oldid=1531762
[433]: https://zh.wikisource.org/w/index.php?title=南史/卷19&oldid=1531762
[434]: https://zh.wikisource.org/w/index.php?title=南史/卷19&oldid=1531762
[436]: https://github.com/kanripo/KR2a0024/blob/3c7bdbb072bf8e1eb70d134a94570c4b8de058ea/KR2a0024_020.txt
[437]: https://zh.wikisource.org/w/index.php?oldid=513423
[439]: https://zh.wikisource.org/w/index.php?oldid=1752646
[440]: https://zh.wikisource.org/w/index.php?oldid=1752646
[441]: https://zh.wikisource.org/w/index.php?oldid=1752646
[443]: https://zh.wikisource.org/w/index.php?oldid=1752646
[445]: https://zh.wikisource.org/w/index.php?oldid=1752646
[446]: https://zh.wikisource.org/w/index.php?oldid=1752646
[448]: https://zh.wikisource.org/w/index.php?oldid=1752646
[449]: https://zh.wikisource.org/w/index.php?oldid=1752646
[450]: https://zh.wikisource.org/w/index.php?oldid=1752646
[451]: https://zh.wikisource.org/w/index.php?oldid=1752646
[452]: https://zh.wikisource.org/w/index.php?oldid=1752646
[454]: https://zh.wikisource.org/w/index.php?oldid=1477957
[455]: https://zh.wikisource.org/w/index.php?oldid=1477957
[456]: https://zh.wikisource.org/w/index.php?oldid=1477957
[457]: https://zh.wikisource.org/w/index.php?oldid=1477957
[459]: https://zh.wikisource.org/w/index.php?oldid=1477957
[460]: https://zh.wikisource.org/w/index.php?title=南史/卷22&oldid=1477957
[461]: https://zh.wikisource.org/w/index.php?oldid=1477957
[462]: https://commons.wikimedia.org/wiki/File:NLC892-411999017142-12360_二十四史_第246冊.pdf
[463]: https://zh.wikisource.org/w/index.php?title=南史/卷22&oldid=1477957
[464]: https://zh.wikisource.org/w/index.php?oldid=1477957
[465]: https://zh.wikisource.org/w/index.php?oldid=1477957
[468]: https://zh.wikisource.org/w/index.php?oldid=1477957
[469]: https://zh.wikisource.org/w/index.php?oldid=1477957
[470]: https://commons.wikimedia.org/wiki/File:NLC892-411999017142-12360_二十四史_第246冊.pdf
[471]: https://zh.wikisource.org/w/index.php?oldid=1477957
[472]: https://zh.wikisource.org/w/index.php?oldid=1477957
[473]: https://github.com/kanripo/KR2a0024/blob/3c7bdbb072bf8e1eb70d134a94570c4b8de058ea/KR2a0024_022.txt
[475]: https://commons.wikimedia.org/wiki/File:NLC892-411999017142-12361_二十四史_第247冊.pdf
[476]: https://zh.wikisource.org/w/index.php?oldid=2478204
[477]: https://zh.wikisource.org/w/index.php?oldid=2478204
[481]: https://zh.wikisource.org/w/index.php?oldid=2478204
[482]: https://zh.wikisource.org/w/index.php?oldid=2478204
[483]: https://zh.wikisource.org/w/index.php?oldid=2478204
[484]: https://zh.wikisource.org/w/index.php?oldid=2478204
[485]: https://zh.wikisource.org/w/index.php?oldid=2478204
[486]: https://zh.wikisource.org/w/index.php?oldid=2478204
[487]: https://zh.wikisource.org/w/index.php?oldid=2478204
[490]: https://zh.wikisource.org/w/index.php?oldid=2478204
[494]: https://zh.wikisource.org/w/index.php?oldid=2478204
[495]: https://zh.wikisource.org/w/index.php?oldid=2478204
[496]: https://zh.wikisource.org/w/index.php?oldid=2478204
[497]: https://zh.wikisource.org/w/index.php?oldid=2478204
[498]: https://zh.wikisource.org/w/index.php?oldid=2478204
[500]: https://zh.wikisource.org/w/index.php?oldid=1765279
[501]: https://zh.wikisource.org/w/index.php?oldid=1765279
[502]: https://commons.wikimedia.org/wiki/File:NLC892-411999017142-12361_%E4%BA%8C%E5%8D%81%E5%9B%9B%E5%8F%B2_%E7%AC%AC247%E5%86%8A.pdf
[503]: https://zh.wikisource.org/w/index.php?oldid=1765279
[504]: https://zh.wikisource.org/w/index.php?oldid=1765279
[505]: https://zh.wikisource.org/w/index.php?oldid=1765279
[506]: https://zh.wikisource.org/w/index.php?title=%E5%8D%97%E5%8F%B2%2F%E5%8D%B724&oldid=1765279
[513]: https://zh.wikisource.org/w/index.php?oldid=1611067
[514]: https://zh.wikisource.org/w/index.php?oldid=1511857
[515]: https://zh.wikisource.org/w/index.php?oldid=1511857
[516]: https://zh.wikisource.org/w/index.php?oldid=8730255
[517]: https://zh.wikisource.org/w/index.php?title=南史/卷31&oldid=8730255
[518]: https://zh.wikisource.org/w/index.php?title=%E5%8D%97%E5%8F%B2%2F%E5%8D%B733&oldid=1554233
[519]: https://zh.wikisource.org/w/index.php?title=南史/卷33&oldid=1554233
[521]: https://zh.wikisource.org/w/index.php?oldid=1956596
[522]: https://zh.wikisource.org/w/index.php?oldid=1552313
[525]: https://zh.wikisource.org/w/index.php?title=南史/卷44&oldid=2027785
[529]: https://zh.wikisource.org/w/index.php?oldid=2598501
[530]: https://zh.wikisource.org/w/index.php?title=南史/卷48&oldid=2493997
[532]: https://zh.wikisource.org/w/index.php?oldid=2027179
[534]: https://zh.wikisource.org/w/index.php?oldid=1553912
[535]: https://zh.wikisource.org/w/index.php?oldid=1553912
[536]: https://zh.wikisource.org/w/index.php?oldid=1495505
[537]: https://zh.wikisource.org/w/index.php?oldid=1748895
[539]: https://zh.wikisource.org/w/index.php?oldid=8746774
[540]: https://raw.githubusercontent.com/kanripo/KR2a0012/214fcafa79894355909c9d8c2c1533089e7791c6/KR2a0012_009.txt
[541]: https://raw.githubusercontent.com/kanripo/KR2a0012/214fcafa79894355909c9d8c2c1533089e7791c6/KR2a0012_009.txt
[542]: https://da.library.pref.osaka.jp/api/items/01-0015983/manifest.json
[543]: https://github.com/kanripo/KR2a0012/blob/214fcafa79894355909c9d8c2c1533089e7791c6/KR2a0012_010.txt
[545]: https://zh.wikisource.org/w/index.php?title=三國志/卷11&oldid=2373044
[546]: https://zh.wikisource.org/w/index.php?oldid=2331498
[550]: https://raw.githubusercontent.com/kanripo/KR2a0012/214fcafa79894355909c9d8c2c1533089e7791c6/KR2a0012_015.txt
[554]: https://github.com/kanripo/KR2a0012/blob/214fcafa79894355909c9d8c2c1533089e7791c6/KR2a0012_019.txt
[556]: https://raw.githubusercontent.com/kanripo/KR2a0012/214fcafa79894355909c9d8c2c1533089e7791c6/KR2a0012_022.txt
[557]: https://raw.githubusercontent.com/kanripo/KR2a0012/214fcafa79894355909c9d8c2c1533089e7791c6/KR2a0012_022.txt
[560]: https://github.com/kanripo/KR2a0012/blob/214fcafa79894355909c9d8c2c1533089e7791c6/KR2a0012_027.txt
[562]: https://github.com/kanripo/KR2a0012/blob/214fcafa79894355909c9d8c2c1533089e7791c6/KR2a0012_028.txt
[569]: https://zh.wikisource.org/w/index.php?title=史記/卷003&oldid=7909145
[570]: https://zh.wikisource.org/w/index.php?title=史記/卷004&oldid=7909147
[571]: https://zh.wikisource.org/w/index.php?title=史記/卷005&oldid=8744286
[572]: https://zh.wikisource.org/w/index.php?title=史記/卷006&oldid=7907969
[573]: https://zh.wikisource.org/w/index.php?title=史記/卷007&oldid=5978360
[574]: https://zh.wikisource.org/w/index.php?title=史記/卷008&oldid=2440965
[575]: https://zh.wikisource.org/w/index.php?title=史記/卷009&oldid=2087062
[577]: https://zh.wikisource.org/w/index.php?title=史記/卷011&oldid=2520527
[579]: https://zh.wikisource.org/w/index.php?title=史記/卷031&oldid=7909287
[580]: https://zh.wikisource.org/w/index.php?title=史記/卷032&oldid=445042
[581]: https://zh.wikisource.org/w/index.php?title=史記/魯周公世家&oldid=7909289
[582]: https://zh.wikisource.org/w/index.php?title=史記/卷034&oldid=2559287
[583]: https://zh.wikisource.org/w/index.php?title=史記/卷035&oldid=8737302
[584]: https://zh.wikisource.org/w/index.php?title=史記/卷036&oldid=2588525
[585]: https://zh.wikisource.org/w/index.php?title=史記/卷037&oldid=5977124
[586]: https://zh.wikisource.org/w/index.php?title=史記/卷038&oldid=8737306
[587]: https://zh.wikisource.org/w/index.php?title=史記/卷039&oldid=2588534
[588]: https://zh.wikisource.org/w/index.php?title=史記/卷040&oldid=8736796
[589]: https://zh.wikisource.org/w/index.php?title=史記/卷041&oldid=2018395
[590]: https://zh.wikisource.org/w/index.php?title=史記/卷042&oldid=2016409
[591]: https://zh.wikisource.org/w/index.php?title=史記/卷043&oldid=7903603
[592]: https://zh.wikisource.org/w/index.php?title=史記/卷044&oldid=7903606
[593]: https://zh.wikisource.org/w/index.php?title=史記/卷045&oldid=7903607
[594]: https://zh.wikisource.org/w/index.php?title=史記/卷046&oldid=2560838
[595]: https://zh.wikisource.org/w/index.php?title=史記/卷047&oldid=7903609
[597]: https://zh.wikisource.org/w/index.php?title=史記/卷049&oldid=7903610
[599]: https://zh.wikisource.org/w/index.php?title=史記/卷051&oldid=2380315
[602]: https://zh.wikisource.org/w/index.php?title=史記/卷054&oldid=1490182
[603]: https://zh.wikisource.org/w/index.php?title=史記/卷055&oldid=2666612
[604]: https://zh.wikisource.org/w/index.php?title=史記/卷056&oldid=1961615
[605]: https://zh.wikisource.org/w/index.php?title=史記/卷057&oldid=1569360
[606]: https://zh.wikisource.org/w/index.php?title=史記/卷058&oldid=8735555
[611]: https://zh.wikisource.org/w/index.php?title=史記/卷063&oldid=7903601
[613]: https://zh.wikisource.org/w/index.php?title=史記/卷065&oldid=2567048
[614]: https://zh.wikisource.org/w/index.php?title=史記/卷066&oldid=2621138
[615]: https://zh.wikisource.org/w/index.php?title=史記/卷067&oldid=7869003
[617]: https://zh.wikisource.org/w/index.php?title=史記/卷069&oldid=2621145
[619]: https://zh.wikisource.org/w/index.php?title=史記/卷071&oldid=2621152
[621]: https://zh.wikisource.org/w/index.php?title=史記/卷073&oldid=7909285
[623]: https://zh.wikisource.org/w/index.php?title=史記/卷075&oldid=1965692
[624]: https://zh.wikisource.org/w/index.php?title=史記/卷076&oldid=7909284
[625]: https://zh.wikisource.org/w/index.php?title=史記/卷077&oldid=367917
[626]: https://zh.wikisource.org/w/index.php?title=史記/卷078&oldid=2089016
[627]: https://zh.wikisource.org/w/index.php?title=史記/卷079&oldid=2549307
[628]: https://zh.wikisource.org/w/index.php?title=史記/卷080&oldid=2089316
[632]: https://zh.wikisource.org/w/index.php?title=史記/卷084&oldid=1568305
[633]: https://zh.wikisource.org/w/index.php?title=史記/卷085&oldid=2027911
[634]: https://zh.wikisource.org/w/index.php?title=史記/卷086&oldid=2388562
[635]: https://zh.wikisource.org/w/index.php?title=史記/卷087&oldid=2364605
[636]: https://zh.wikisource.org/w/index.php?title=史記/卷088&oldid=1965690
[637]: https://zh.wikisource.org/w/index.php?title=史記/卷089&oldid=8744143
[639]: https://zh.wikisource.org/w/index.php?title=史記/卷091&oldid=2509940
[641]: https://zh.wikisource.org/w/index.php?title=史記/卷093&oldid=368019
[642]: https://zh.wikisource.org/w/index.php?title=史記/卷094&oldid=2171897
[643]: https://zh.wikisource.org/w/index.php?title=史記/卷095&oldid=2298709
[644]: https://zh.wikisource.org/w/index.php?title=史記/卷096&oldid=8770206
[645]: https://zh.wikisource.org/w/index.php?title=史記/卷097&oldid=1383195
[646]: https://zh.wikisource.org/w/index.php?title=史記/卷098&oldid=1490318
[648]: https://zh.wikisource.org/w/index.php?title=史記/卷100&oldid=1965696
[649]: https://zh.wikisource.org/w/index.php?title=史記/卷101&oldid=368092
[650]: https://zh.wikisource.org/w/index.php?title=史記/卷102&oldid=1753957
[651]: https://zh.wikisource.org/w/index.php?title=史記/卷103&oldid=2096814
[652]: https://zh.wikisource.org/w/index.php?title=史記/卷104&oldid=8739534
[653]: https://zh.wikisource.org/w/index.php?title=史記/卷105&oldid=8842726
[655]: https://zh.wikisource.org/w/index.php?title=史記/卷107&oldid=2540571
[657]: https://zh.wikisource.org/w/index.php?title=史記/卷109&oldid=1765440
[658]: https://zh.wikisource.org/w/index.php?title=史記/卷110&oldid=8735645
[659]: https://zh.wikisource.org/w/index.php?title=史記/卷111&oldid=8730225
[660]: https://zh.wikisource.org/w/index.php?title=史記/卷112&oldid=2089420
[661]: https://zh.wikisource.org/w/index.php?title=史記/卷113&oldid=8735632
[662]: https://zh.wikisource.org/w/index.php?title=史記/卷114&oldid=8735633
[663]: https://zh.wikisource.org/w/index.php?title=史記/卷115&oldid=439220
[664]: https://zh.wikisource.org/w/index.php?title=史記/卷116&oldid=7903636
[666]: https://zh.wikisource.org/w/index.php?title=史記/卷118&oldid=7904122
[667]: https://zh.wikisource.org/w/index.php?title=史記/卷119&oldid=7904123
[668]: https://zh.wikisource.org/w/index.php?title=史記/卷120&oldid=9166127
[670]: https://zh.wikisource.org/w/index.php?title=史記/卷122&oldid=7904124
[671]: https://zh.wikisource.org/w/index.php?title=史記/卷123&oldid=8736799
[672]: https://zh.wikisource.org/w/index.php?title=史記/卷124&oldid=367994
[673]: https://zh.wikisource.org/w/index.php?title=史記/卷125&oldid=2273599
[674]: https://zh.wikisource.org/w/index.php?title=史記/卷126&oldid=2609358
[678]: https://zh.wikisource.org/w/index.php?title=史記/卷130&oldid=2609362
[679]: https://zh.wikisource.org/w/index.php?oldid=2567459
[683]: https://zh.wikisource.org/w/index.php?oldid=2567459
[684]: https://zh.wikisource.org/w/index.php?oldid=2567459
[686]: https://zh.wikisource.org/w/index.php?oldid=2567463
[698]: https://zh.wikisource.org/w/index.php?oldid=2567462
[702]: https://zh.wikisource.org/w/index.php?oldid=2567465
[716]: https://zh.wikisource.org/w/index.php?oldid=1532652
[721]: https://zh.wikisource.org/w/index.php?oldid=1532655
[734]: https://zh.wikisource.org/w/index.php?oldid=1503586
[735]: https://zh.wikisource.org/w/index.php?oldid=1503586
[736]: https://zh.wikisource.org/w/index.php?oldid=2004422
[737]: https://zh.wikisource.org/w/index.php?oldid=2004422
[741]: https://zh.wikisource.org/w/index.php?oldid=1500491
[745]: https://raw.githubusercontent.com/kanripo/KR2a0016/e80c057667e3c8684f11d5088251e10244d5a264/KR2a0016_001.txt
[753]: https://zh.wikisource.org/w/index.php?oldid=2634831
[754]: https://raw.githubusercontent.com/kanripo/KR2a0016/e80c057667e3c8684f11d5088251e10244d5a264/KR2a0016_041.txt
[755]: https://zh.wikisource.org/w/index.php?oldid=2634831
[756]: https://zh.wikisource.org/w/index.php?oldid=2634831
[757]: https://commons.wikimedia.org/w/index.php?oldid=979637190
[758]: https://zh.wikisource.org/w/index.php?oldid=2634831
[759]: https://zh.wikisource.org/w/index.php?title=宋書/卷41&oldid=2634831
[760]: https://zh.wikisource.org/w/index.php?title=宋書/卷42&oldid=1478172
[761]: https://commons.wikimedia.org/w/index.php?title=File:NLC892-411999017142-12779_%E4%BA%8C%E5%8D%81%E5%9B%9B%E5%8F%B2_%E7%AC%AC144%E5%86%8A.pdf&oldid=979637198
[762]: https://zh.wikisource.org/w/index.php?title=%E5%AE%8B%E6%9B%B8/%E5%8D%B744&oldid=1746033
[766]: https://raw.githubusercontent.com/kanripo/KR2a0016/e80c057667e3c8684f11d5088251e10244d5a264/KR2a0016_046.txt
[768]: https://zh.wikisource.org/w/index.php?oldid=2371899
[769]: https://zh.wikisource.org/w/index.php?oldid=1959959
[770]: https://zh.wikisource.org/w/index.php?oldid=2190655
[771]: https://zh.wikisource.org/w/index.php?oldid=2190655
[773]: https://zh.wikisource.org/w/index.php?oldid=2190655
[774]: https://zh.wikisource.org/w/index.php?oldid=2190655
[775]: https://zh.wikisource.org/w/index.php?oldid=2190655
[776]: https://zh.wikisource.org/w/index.php?oldid=2190655
[778]: https://raw.githubusercontent.com/kanripo/KR2a0016/e80c057667e3c8684f11d5088251e10244d5a264/KR2a0016_053.txt
[779]: https://zh.wikisource.org/w/index.php?oldid=1996685
[780]: https://raw.githubusercontent.com/kanripo/KR2a0016/e80c057667e3c8684f11d5088251e10244d5a264/KR2a0016_053.txt
[781]: https://raw.githubusercontent.com/kanripo/KR2a0016/e80c057667e3c8684f11d5088251e10244d5a264/KR2a0016_056.txt
[784]: https://github.com/kanripo/KR2a0016/blob/e80c057667e3c8684f11d5088251e10244d5a264/KR2a0016_058.txt
[785]: https://raw.githubusercontent.com/kanripo/KR2a0016/e80c057667e3c8684f11d5088251e10244d5a264/KR2a0016_059.txt
[786]: https://zh.wikisource.org/w/index.php?title=宋書/卷60&oldid=1996694
[787]: https://zh.wikisource.org/w/index.php?oldid=1996694
[788]: https://zh.wikisource.org/w/index.php?oldid=1996694
[789]: https://zh.wikisource.org/w/index.php?title=%E5%AE%8B%E6%9B%B8/%E5%8D%B760&oldid=1996694
[791]: https://github.com/kanripo/KR2a0016/blob/e80c057667e3c8684f11d5088251e10244d5a264/KR2a0016_062.txt
[792]: https://zh.wikisource.org/w/index.php?title=宋書/卷63&oldid=2118589
[793]: https://commons.wikimedia.org/wiki/File:NLC892-411999017142-12245_二十四史_第147冊.pdf
[795]: https://zh.wikisource.org/w/index.php?title=%E5%AE%8B%E6%9B%B8%2F%E5%8D%B764&oldid=1748217
[796]: https://upload.wikimedia.org/wikipedia/commons/c/cb/NLC892-411999017142-12245_%E4%BA%8C%E5%8D%81%E5%9B%9B%E5%8F%B2_%E7%AC%AC147%E5%86%8A.pdf#page=64
[797]: https://zh.wikisource.org/w/index.php?title=%E5%AE%8B%E6%9B%B8%2F%E5%8D%B766&oldid=2069104
[798]: https://raw.githubusercontent.com/kanripo/KR2a0016/e80c057667e3c8684f11d5088251e10244d5a264/KR2a0016_067.txt
[799]: https://zh.wikisource.org/w/index.php?title=宋書/卷71&oldid=2485515
[800]: https://commons.wikimedia.org/wiki/File:NLC892-411999017142-12246_二十四史_第148冊.pdf
[801]: https://github.com/kanripo/KR2a0016/blob/e80c057667e3c8684f11d5088251e10244d5a264/KR2a0016_071.txt
[802]: https://zh.wikisource.org/w/index.php?oldid=1997159
[803]: https://zh.wikisource.org/w/index.php?oldid=2118597
[804]: https://zh.wikisource.org/w/index.php?oldid=2118597
[805]: https://zh.wikisource.org/w/index.php?oldid=2118597
[806]: https://zh.wikisource.org/w/index.php?title=宋書/卷75&oldid=1997722
[808]: https://zh.wikisource.org/w/index.php?oldid=1997726
[810]: https://zh.wikisource.org/w/index.php?title=宋書/卷77&oldid=1997730
[811]: https://zh.wikisource.org/w/index.php?oldid=2069112
[812]: https://zh.wikisource.org/w/index.php?title=宋書/卷80&oldid=2261200
[817]: https://zh.wikisource.org/w/index.php?oldid=2069101
[819]: https://github.com/kanripo/KR2a0016/blob/e80c057667e3c8684f11d5088251e10244d5a264/KR2a0016_085.txt
[820]: https://zh.wikisource.org/w/index.php?title=宋書/卷86&oldid=2069103
[821]: https://zh.wikisource.org/w/index.php?title=宋書/卷87&oldid=2069105
[822]: https://zh.wikisource.org/w/index.php?title=宋書/卷88&oldid=2069210
[823]: https://zh.wikisource.org/w/index.php?title=宋書/卷88&oldid=2069210
[824]: https://zh.wikisource.org/w/index.php?title=宋書/卷88&oldid=2069210
[825]: https://zh.wikisource.org/w/index.php?title=宋書/卷88&oldid=2069210
[826]: https://zh.wikisource.org/w/index.php?oldid=2195614
[827]: https://zh.wikisource.org/w/index.php?title=%E5%AE%8B%E6%9B%B8%2F%E5%8D%B792&oldid=2195614
[828]: https://zh.wikisource.org/w/index.php?title=%E5%AE%8B%E6%9B%B8%2F%E5%8D%B793&oldid=1962755
[829]: https://zh.wikisource.org/w/index.php?oldid=2195835
[832]: https://zh.wikisource.org/w/index.php?title=隋書/卷76&oldid=2616529
[836]: https://zh.wikisource.org/w/index.php?oldid=2607174
[841]: https://zh.wikisource.org/w/index.php?oldid=2587734
[842]: https://zh.wikisource.org/w/index.php?oldid=2587825
[847]: https://zh.wikisource.org/w/index.php?title=魏書/卷18&oldid=1550395
[848]: https://zh.wikisource.org/w/index.php?title=魏書/卷24&oldid=2021236
[849]: https://raw.githubusercontent.com/kanripo/KR2a0020/17b6525eb5aaa878b9640f5a61e90da934ce5fc4/KR2a0020_024.txt
[850]: https://zh.wikisource.org/w/index.php?oldid=2021236
[851]: https://raw.githubusercontent.com/kanripo/KR2a0020/17b6525eb5aaa878b9640f5a61e90da934ce5fc4/KR2a0020_035.txt
[852]: https://github.com/kanripo/KR2a0020/blob/17b6525eb5aaa878b9640f5a61e90da934ce5fc4/KR2a0020_038.txt
[853]: https://zh.wikisource.org/w/index.php?oldid=2120299
[854]: https://zh.wikisource.org/w/index.php?oldid=1501651
[855]: https://zh.wikisource.org/w/index.php?title=%E9%AD%8F%E6%9B%B8%2F%E5%8D%B758&oldid=2087998
[856]: https://zh.wikisource.org/w/index.php?title=%E9%AD%8F%E6%9B%B8%2F%E5%8D%B758&oldid=2087998
[857]: https://zh.wikisource.org/w/index.php?title=%E9%AD%8F%E6%9B%B8%2F%E5%8D%B758&oldid=2087998
[861]: https://zh.wikisource.org/w/index.php?oldid=1513419
[862]: https://zh.wikisource.org/w/index.php?title=魏書/卷67&oldid=468068
[863]: https://zh.wikisource.org/w/index.php?oldid=2294110
[864]: https://zh.wikisource.org/w/index.php?oldid=760052
[866]: https://zh.wikisource.org/w/index.php?oldid=760052
[868]: https://commons.wikimedia.org/w/index.php?oldid=1130546999
[869]: https://zh.wikisource.org/w/index.php?oldid=2004220
[870]: https://commons.wikimedia.org/w/index.php?oldid=1130546999
[871]: https://zh.wikisource.org/w/index.php?title=%E6%96%B0%E5%94%90%E6%9B%B8%2F%E5%8D%B7071%E4%B8%8B&oldid=2405769
[872]: https://zh.wikisource.org/w/index.php?oldid=1519175
[873]: https://zh.wikisource.org/w/index.php?title=新唐書/卷116&oldid=3528844
[874]: https://zh.wikisource.org/w/index.php?oldid=2610515
[875]: https://zh.wikisource.org/w/index.php?title=周書/卷41&oldid=2432538
[880]: https://zh.wikisource.org/w/index.php?oldid=2454083
[881]: https://zh.wikisource.org/w/index.php?title=%E8%B3%87%E6%B2%BB%E9%80%9A%E9%91%91/%E5%8D%B7094&oldid=2312212
[884]: https://zh.wikisource.org/w/index.php?oldid=1497680
[887]: https://zh.wikisource.org/w/index.php?oldid=1552077
[895]: https://zh.wikisource.org/w/index.php?title=史記/卷013&oldid=2606991
[896]: https://zh.wikisource.org/w/index.php?title=史記/卷014&oldid=2607001
[897]: https://zh.wikisource.org/w/index.php?title=史記/卷015&oldid=2607002
[898]: https://zh.wikisource.org/w/index.php?title=史記/卷016&oldid=2607007
[899]: https://zh.wikisource.org/w/index.php?title=史記/卷017&oldid=2607010
[900]: https://zh.wikisource.org/w/index.php?title=史記/卷018&oldid=9484995
[901]: https://zh.wikisource.org/w/index.php?title=史記/卷019&oldid=6359260
[902]: https://zh.wikisource.org/w/index.php?title=史記/卷020&oldid=2607036
