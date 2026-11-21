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
| `根` | 阮裕（韜玄祖） | [《晉書・王羲之》][99] | [JSON](03n_n2r_8rt.json) |
| `***A` | 阮韜 | [《南史・王裕之　王鎮之　王韶之　王悅之　王准之》][241] | [JSON](03n_n2r_8rt_%2A%2A%2AA.json) |

</details>

<details><summary><code>04u_gq0_nke</code> 鼂錯父未名（袁盎鼂錯列傳候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 鼂錯父未名 | [《史記・袁盎鼂錯列傳》][347] | [JSON](04u_gq0_nke.json) |
| `A` | 鼂錯 | [《史記・袁盎鼂錯列傳》][347] | [JSON](04u_gq0_nke_A.json) |

</details>

<details><summary><code>06i_k5v_922</code> 申侯（鄭世家武姜父候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 申侯 | [《史記・鄭世家》][288] | [JSON](06i_k5v_922.json) |
| `A` | 武姜 | [《史記・鄭世家》][288] | [JSON](06i_k5v_922_A.json) |

</details>

<details><summary><code>0ad_dbw_97q</code> 晉昭公（4 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 晉昭公 | [《史記・晉世家》][285] | [JSON](0ad_dbw_97q.json) |
| `A` | 雍（戴子晉昭公子） | [《史記・晉世家》][285] | [JSON](0ad_dbw_97q_A.json) |
| `AA` | 忌（戴子子） | [《史記・晉世家》][285] | [JSON](0ad_dbw_97q_AA.json) |
| `AAA` | 驕（晉哀公） | [《史記・晉世家》][285] | [JSON](0ad_dbw_97q_AAA.json) |

</details>

<details><summary><code>0bu_skv_qsr</code> 呂青（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 呂青 | [《史記・項羽本紀》][271]、[《史記・高祖本紀》][272] | [JSON](0bu_skv_qsr.json) |
| `A` | 呂臣 | [《史記・項羽本紀》][271]、[《史記・高祖本紀》][272] | [JSON](0bu_skv_qsr_A.json) |

</details>

<details><summary><code>0c1_b9d_9c2</code> 楊彪（7 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 楊彪 | [《後漢書・孝獻帝紀》][31] | [JSON](0c1_b9d_9c2.json) |
| `A` | 楊脩 | [《三國志・任城陳蕭王傳》][258] | [JSON](0c1_b9d_9c2_A.json) |
| `AA` | 楊囂 | [《三國志・任城陳蕭王傳》][258] | [JSON](0c1_b9d_9c2_AA.json) |
| `AAA` | 楊準 | [《三國志・任城陳蕭王傳》][258] | [JSON](0c1_b9d_9c2_AAA.json) |
| `AAAA` | 楊嶠 | [《三國志・任城陳蕭王傳》][258] | [JSON](0c1_b9d_9c2_AAAA.json) |
| `AAAB` | 楊髦 | [《三國志・任城陳蕭王傳》][258] | [JSON](0c1_b9d_9c2_AAAB.json) |
| `AAAC` | 楊俊 | [《三國志・任城陳蕭王傳》][258] | [JSON](0c1_b9d_9c2_AAAC.json) |

</details>

<details><summary><code>0db_22c_332</code> 何進（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 何進 | [《後漢書・荀韓鍾陳列傳》][33] | [JSON](0db_22c_332.json) |
| `*A` | 何晏 | [《三國志・諸夏侯曹傳》][252] | [JSON](0db_22c_332_%2AA.json) |
| `*AA` | 晏未名男 | [《三國志・諸夏侯曹傳》][252] | [JSON](0db_22c_332_%2AAA.json) |

</details>

<details><summary><code>0hs_fg6_1qj</code> 田榮（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 田榮 | [《史記・田儋列傳》][340] | [JSON](0hs_fg6_1qj.json) |
| `A` | 廣（田榮子） | [《史記・酈生陸賈列傳》][343] | [JSON](0hs_fg6_1qj_A.json) |
| `B` | 田廣 | [《史記・田儋列傳》][340] | [JSON](0hs_fg6_1qj_B.json) |

</details>

<details><summary><code>0lf_ggf_5xo</code> 張弘策（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 張弘策 | [《南史・謝晦　謝裕　謝方明　謝靈運》][194] | [JSON](0lf_ggf_5xo.json) |
| `A` | 張緬（字元長） | [《梁書・張緬 弟纘 綰》][134] | [JSON](0lf_ggf_5xo_A.json) |

</details>

<details><summary><code>0s7_r72_j8q</code> 魯武公（4 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 魯武公 | [《史記・魯周公世家》][279] | [JSON](0s7_r72_j8q.json) |
| `A` | 括（魯武公長子） | [《史記・魯周公世家》][279] | [JSON](0s7_r72_j8q_A.json) |
| `AA` | 伯御（魯君） | [《史記・魯周公世家》][279] | [JSON](0s7_r72_j8q_AA.json) |
| `B` | 戲（魯懿公） | [《史記・魯周公世家》][279] | [JSON](0s7_r72_j8q_B.json) |

</details>

<details><summary><code>0us_j8h_to7</code> 假（老韓列傳候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 假 | [《史記・老子韓非列傳》][309] | [JSON](0us_j8h_to7.json) |
| `A` | 解 | [《史記・老子韓非列傳》][309] | [JSON](0us_j8h_to7_A.json) |

</details>

<details><summary><code>0xt_iyn_d3t</code> 趙夙（趙世家候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 趙夙 | [《史記・趙世家》][289] | [JSON](0xt_iyn_d3t.json) |
| `A` | 共孟 | [《史記・趙世家》][289] | [JSON](0xt_iyn_d3t_A.json) |

</details>

<details><summary><code>0zd_9uz_t7m</code> 臧汪（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 臧汪 | [《南史・后妃上》][179] | [JSON](0zd_9uz_t7m.json) |
| `A` | 臧儁 | [《南史・后妃上》][178]、[《南史・后妃上》][179]、[《宋書・后妃》][423] | [JSON](0zd_9uz_t7m_A.json) |
| `AA` | 臧愛親 | [《南史・后妃上》][179]、[《南史・范泰　荀伯子　徐廣　鄭鮮之　裴松之　何承天》][244]、[《宋書・鄭鮮之 裴松之 何承天》][446] | [JSON](0zd_9uz_t7m_AA.json) |

</details>

<details><summary><code>113_odk_emq</code> 衞綰（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 衞綰 | [《史記・萬石張叔列傳》][349] | [JSON](113_odk_emq.json) |
| `A` | 信（衞綰子） | [《史記・萬石張叔列傳》][349] | [JSON](113_odk_emq_A.json) |

</details>

<details><summary><code>128_4ab_z34</code> 熊延（楚君）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 熊延（楚君） | [《史記・楚世家》][286] | [JSON](128_4ab_z34.json) |
| `A` | 熊勇（楚君） | [《史記・楚世家》][286] | [JSON](128_4ab_z34_A.json) |

</details>

<details><summary><code>175_99c_b41</code> 柔（王沈祖）（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 柔（王沈祖） | [《三國志・徐胡二王傳》][262] | [JSON](175_99c_b41.json) |
| `A` | 機（王沈父） | [《晉書・王沈 荀顗 荀勖 馮紞》][68] | [JSON](175_99c_b41_A.json) |
| `AA` | 王沈 | [《晉書・王沈 荀顗 荀勖 馮紞》][68] | [JSON](175_99c_b41_AA.json) |

</details>

<details><summary><code>1a3_b0c_e6d</code> 謝沖（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 謝沖 | [《南史・謝晦　謝裕　謝方明　謝靈運》][182] | [JSON](1a3_b0c_e6d.json) |
| `A` | 謝明慧 | [《晉書・謝尚 謝安》][98] | [JSON](1a3_b0c_e6d_A.json) |

</details>

<details><summary><code>1ay_9qe_u4h</code> 荀馗（5 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 荀馗 | [《晉書・王湛 荀崧 范汪 劉惔 張憑 韓伯》][90] | [JSON](1ay_9qe_u4h.json) |
| `A` | 荀序 | [《晉書・王沈 荀顗 荀勖 馮紞》][68]、[《晉書・王湛 荀崧 范汪 劉惔 張憑 韓伯》][90] | [JSON](1ay_9qe_u4h_A.json) |
| `AA` | 恆（荀序子） | [《晉書・王沈 荀顗 荀勖 馮紞》][68] | [JSON](1ay_9qe_u4h_AA.json) |
| `AAA` | 龍符（恆子） | [《晉書・王沈 荀顗 荀勖 馮紞》][68] | [JSON](1ay_9qe_u4h_AAA.json) |
| `B` | 荀廞 | [《晉書・王湛 荀崧 范汪 劉惔 張憑 韓伯》][90] | [JSON](1ay_9qe_u4h_B.json) |

</details>

<details><summary><code>1b1_d4d_bb8</code> 謝鐵（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 謝鐵 | [《南史・謝晦　謝裕　謝方明　謝靈運》][182] | [JSON](1b1_d4d_bb8.json) |
| `A` | 謝邈 | [《晉書・謝尚 謝安》][98] | [JSON](1b1_d4d_bb8_A.json) |

</details>

<details><summary><code>1ex_se1_yef</code> 張湯父（未名）（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 張湯父（未名） | [《漢書・張湯傳》][26]、[《史記・酷吏列傳》][368] | [JSON](1ex_se1_yef.json) |
| `A` | 張湯 | [《史記・酷吏列傳》][368] | [JSON](1ex_se1_yef_A.json) |
| `AA` | 張安世 | [《漢書・張湯傳》][26] | [JSON](1ex_se1_yef_AA.json) |

</details>

<details><summary><code>1g3_02y_oor</code> 太公望（5 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 太公望 | [《史記・齊太公世家》][278] | [JSON](1g3_02y_oor.json) |
| `A` | 丁公呂伋 | [《史記・齊太公世家》][278] | [JSON](1g3_02y_oor_A.json) |
| `AA` | 得（齊乙公） | [《史記・齊太公世家》][278] | [JSON](1g3_02y_oor_AA.json) |
| `AAA` | 慈母（齊癸公） | [《史記・齊太公世家》][278] | [JSON](1g3_02y_oor_AAA.json) |
| `AAAA` | 不辰（齊哀公） | [《史記・齊太公世家》][278] | [JSON](1g3_02y_oor_AAAA.json) |

</details>

<details><summary><code>1h3_vs7_t8h</code> 齊湣王（燕篇）（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 齊湣王（燕篇） | [《史記・燕召公世家》][280] | [JSON](1h3_vs7_t8h.json) |
| `A` | 襄王（齊湣王子） | [《史記・田敬仲完世家》][292] | [JSON](1h3_vs7_t8h_A.json) |
| `AA` | 齊王建 | [《史記・田敬仲完世家》][292] | [JSON](1h3_vs7_t8h_AA.json) |

</details>

<details><summary><code>1hf_1k0_bnj</code> 夷仲年（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 夷仲年 | [《史記・齊太公世家》][278]、[《史記・十二諸侯年表》][495] | [JSON](1hf_1k0_bnj.json) |
| `A` | 公孫無知 | [《史記・齊太公世家》][278] | [JSON](1hf_1k0_bnj_A.json) |

</details>

<details><summary><code>1kj_vhc_cx9</code> 上官桀（三王世家候選）（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 上官桀 | [《漢書・昭帝紀》][22] | [JSON](1kj_vhc_cx9.json) |
| `A` | 上官安 | [《漢書・昭帝紀》][22] | [JSON](1kj_vhc_cx9_A.json) |
| `AA` | 上官氏（孝昭皇后） | [《漢書・昭帝紀》][22] | [JSON](1kj_vhc_cx9_AA.json) |

</details>

<details><summary><code>1l4_2pq_e7w</code> 熊通（楚武王候選）（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 熊通 | [《史記・楚世家》][286] | [JSON](1l4_2pq_e7w.json) |
| `A` | 熊貲（楚文王） | [《史記・楚世家》][286] | [JSON](1l4_2pq_e7w_A.json) |
| `AA` | 熊艱（莊敖） | [《史記・楚世家》][286] | [JSON](1l4_2pq_e7w_AA.json) |

</details>

<details><summary><code>1pc_mnq_z0c</code> 懿公（燕文公後）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 懿公（燕文公後） | [《史記・燕召公世家》][280] | [JSON](1pc_mnq_z0c.json) |
| `A` | 惠公（燕懿公子） | [《史記・燕召公世家》][280] | [JSON](1pc_mnq_z0c_A.json) |

</details>

<details><summary><code>1y5_eke_4gl</code> 陽慶（扁鵲倉公列傳候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 陽慶 | [《史記・扁鵲倉公列傳》][351] | [JSON](1y5_eke_4gl.json) |
| `A` | 殷（慶子） | [《史記・扁鵲倉公列傳》][351] | [JSON](1y5_eke_4gl_A.json) |

</details>

<details><summary><code>1za_blw_7lb</code> 伯魯（趙世家候選）（6 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 伯魯 | [《史記・趙世家》][289] | [JSON](1za_blw_7lb.json) |
| `A` | 周 | [《史記・趙世家》][289] | [JSON](1za_blw_7lb_A.json) |
| `AA` | 浣 | [《史記・趙世家》][289] | [JSON](1za_blw_7lb_AA.json) |
| `AAA` | 籍 | [《史記・趙世家》][289] | [JSON](1za_blw_7lb_AAA.json) |
| `AAAA` | 章 | [《史記・趙世家》][289] | [JSON](1za_blw_7lb_AAAA.json) |
| `AAAAA` | 種 | [《史記・趙世家》][289] | [JSON](1za_blw_7lb_AAAAA.json) |

</details>

<details><summary><code>23q_wcp_hny</code> 崔道固（7 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 崔道固 | [《魏書・燕鳳 許謙 張衮 崔玄伯 鄧淵》][472] | [JSON](23q_wcp_hny.json) |
| `A` | 崔景微 | [《宋書・薛安都 沈文秀 崔道固》][461]、[《宋書・薛安都 沈文秀 崔道固》][462] | [JSON](23q_wcp_hny_A.json) |
| `B` | 崔景徽 | [《魏書・燕鳳 許謙 張衮 崔玄伯 鄧淵》][472] | [JSON](23q_wcp_hny_B.json) |
| `BA` | 崔休纂 | [《北史・崔光 崔亮》][6]、[《魏書・燕鳳 許謙 張衮 崔玄伯 鄧淵》][472] | [JSON](23q_wcp_hny_BA.json) |
| `C` | 崔景業 | [《魏書・燕鳳 許謙 張衮 崔玄伯 鄧淵》][472] | [JSON](23q_wcp_hny_C.json) |
| `CA` | 崔休緒 | [《魏書・燕鳳 許謙 張衮 崔玄伯 鄧淵》][472] | [JSON](23q_wcp_hny_CA.json) |
| `D` | 崔景淵 | [《魏書・燕鳳 許謙 張衮 崔玄伯 鄧淵》][472] | [JSON](23q_wcp_hny_D.json) |

</details>

<details><summary><code>262_b8f_4ie</code> 裴朴之（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 裴朴之 | [《南齊書・皇后》][144]、[《南史・后妃上》][176] | [JSON](262_b8f_4ie.json) |
| `A` | 裴璣之 | [《南齊書・皇后》][144]、[《南史・后妃上》][176] | [JSON](262_b8f_4ie_A.json) |
| `AA` | 裴惠昭 | [《南齊書・高帝下》][139]、[《南齊書・皇后》][144]、[《南史・后妃上》][176] | [JSON](262_b8f_4ie_AA.json) |

</details>

<details><summary><code>27j_f4p_jwp</code> 李廣（7 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 李廣 | [《史記・李將軍列傳》][355] | [JSON](27j_f4p_jwp.json) |
| `A` | 李敢 | [《史記・李將軍列傳》][355] | [JSON](27j_f4p_jwp_A.json) |
| `AA` | 李敢女（未名） | [《史記・李將軍列傳》][355] | [JSON](27j_f4p_jwp_AA.json) |
| `AB` | 禹（李敢男） | [《史記・李將軍列傳》][355] | [JSON](27j_f4p_jwp_AB.json) |
| `B` | 當戸 | [《史記・李將軍列傳》][355] | [JSON](27j_f4p_jwp_B.json) |
| `BA` | 李陵 | [《史記・李將軍列傳》][355] | [JSON](27j_f4p_jwp_BA.json) |
| `C` | 椒 | [《史記・李將軍列傳》][355] | [JSON](27j_f4p_jwp_C.json) |

</details>

<details><summary><code>2a3_ci1_y4y</code> 元湛（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 元湛 | [《北史・道武七王 明元六王 太武五王》][1]、[《冊府元龜・宗室部·承襲第三》][7]、[《元湛墓誌・節錄》][17]、[《魏書・太武五王》][471] | [JSON](2a3_ci1_y4y.json) |
| `A` | 元法輪 | [《北史・道武七王 明元六王 太武五王》][1]、[《冊府元龜・宗室部·承襲第三》][7]、[《魏書・太武五王》][471] | [JSON](2a3_ci1_y4y_A.json) |

</details>

<details><summary><code>2bc_992_946</code> 謝靜（4 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 謝靜 | [《晉書・謝尚 謝安》][98] | [JSON](2bc_992_946.json) |
| `A` | 謝肅 | [《晉書・謝尚 謝安》][98] | [JSON](2bc_992_946_A.json) |
| `B` | 謝虔 | [《晉書・謝尚 謝安》][98] | [JSON](2bc_992_946_B.json) |
| `BA` | 謝靈佑 | [《晉書・謝尚 謝安》][98] | [JSON](2bc_992_946_BA.json) |

</details>

<details><summary><code>2c3_7e0_16b</code> 卞範之（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 卞範之 | [《晉書・叛臣二》][110] | [JSON](2c3_7e0_16b.json) |
| `A` | 卞範之女（拒婚對象，未名） | [《宋書・張茂度 庾登之 謝方明 江夷》][432] | [JSON](2c3_7e0_16b_A.json) |

</details>

<details><summary><code>2d3_fsd_1dh</code> 楚成王（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 楚成王 | [《史記・晉世家》][285] | [JSON](2d3_fsd_1dh.json) |
| `A` | 楚商臣 | [《史記・陳杞世家》][282] | [JSON](2d3_fsd_1dh_A.json) |

</details>

<details><summary><code>2n6_7xk_5ov</code> 江夏王義恭（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 江夏王義恭 | [《宋書・殷淳 張暢 何偃 江智淵》][438] | [JSON](2n6_7xk_5ov.json) |
| `A` | 王僧虔妻（江夏王女，未名） | [《南齊書・王僧虔 張緒》][151] | [JSON](2n6_7xk_5ov_A.json) |

</details>

<details><summary><code>2pg_br4_mcl</code> 王濛（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 王濛 | [《晉書・謝尚 謝安》][98] | [JSON](2pg_br4_mcl.json) |
| `A` | 王修 | [《晉書・謝尚 謝安》][98] | [JSON](2pg_br4_mcl_A.json) |

</details>

<details><summary><code>2v5_rhh_fd6</code> 檀韶（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 檀韶 | [《南齊書・王僧虔 張緒》][151] | [JSON](2v5_rhh_fd6.json) |
| `*A` | 檀珪 | [《南齊書・王僧虔 張緒》][151] | [JSON](2v5_rhh_fd6_%2AA.json) |

</details>

<details><summary><code>2v6_0g1_ve2</code> 衍（宋微仲）（12 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 衍（宋微仲） | [《史記・宋微子世家》][284] | [JSON](2v6_0g1_ve2.json) |
| `A` | 稽（宋公） | [《史記・宋微子世家》][284] | [JSON](2v6_0g1_ve2_A.json) |
| `AA` | 申（宋丁公） | [《史記・宋微子世家》][284] | [JSON](2v6_0g1_ve2_AA.json) |
| `AAA` | 共（宋湣公） | [《史記・宋微子世家》][284] | [JSON](2v6_0g1_ve2_AAA.json) |
| `AAAA` | 鮒祀（宋厲公） | [《史記・宋微子世家》][284] | [JSON](2v6_0g1_ve2_AAAA.json) |
| `AAAAA` | 舉（宋釐公） | [《史記・宋微子世家》][284] | [JSON](2v6_0g1_ve2_AAAAA.json) |
| `AAAAAA` | 覵（宋惠公） | [《史記・宋微子世家》][284] | [JSON](2v6_0g1_ve2_AAAAAA.json) |
| `AAAAAAA` | 哀公（宋惠公子） | [《史記・宋微子世家》][284] | [JSON](2v6_0g1_ve2_AAAAAAA.json) |
| `AAAAAAAA` | 戴公（宋哀公子） | [《史記・宋微子世家》][284] | [JSON](2v6_0g1_ve2_AAAAAAAA.json) |
| `AAAAAAAAA` | 司空（宋武公） | [《史記・宋微子世家》][284] | [JSON](2v6_0g1_ve2_AAAAAAAAA.json) |
| `AAAAAAAAAA` | 宋女（魯惠公夫人） | [《史記・宋微子世家》][284] | [JSON](2v6_0g1_ve2_AAAAAAAAAA.json) |
| `AAAAAAAAAB` | 力（宋宣公） | [《史記・宋微子世家》][284] | [JSON](2v6_0g1_ve2_AAAAAAAAAB.json) |

</details>

<details><summary><code>2ya_f42_kcq</code> 荀昶（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 荀昶 | [《宋書・范泰 王准之 王韶之 荀伯子》][440] | [JSON](2ya_f42_kcq.json) |
| `A` | 荀萬秋 | [《宋書・范泰 王准之 王韶之 荀伯子》][440] | [JSON](2ya_f42_kcq_A.json) |

</details>

<details><summary><code>30f_353_0e8</code> 崔鴻（7 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 崔鴻 | [《魏書・崔光》][481] | [JSON](30f_353_0e8.json) |
| `A` | 崔子文 | [《崔鴻墓誌・節錄》][11] | [JSON](30f_353_0e8_A.json) |
| `B` | 崔子真 | [《崔鴻墓誌・節錄》][11] | [JSON](30f_353_0e8_B.json) |
| `C` | 崔子長 | [《崔鴻墓誌・節錄》][11] | [JSON](30f_353_0e8_C.json) |
| `D` | 崔子發 | [《崔鴻墓誌・節錄》][11] | [JSON](30f_353_0e8_D.json) |
| `E` | 崔子房 | [《崔鴻墓誌・節錄》][11] | [JSON](30f_353_0e8_E.json) |
| `F` | 崔元華 | [《崔鴻墓誌・節錄》][11] | [JSON](30f_353_0e8_F.json) |

</details>

<details><summary><code>30k_jzz_tpd</code> 邵（9 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 邵 | [《三國志・諸夏侯曹傳》][252] | [JSON](30k_jzz_tpd.json) |
| `A` | 曹真 | [《三國志・諸夏侯曹傳》][252] | [JSON](30k_jzz_tpd_A.json) |
| `AA` | 曹爽 | [《三國志・諸夏侯曹傳》][252] | [JSON](30k_jzz_tpd_AA.json) |
| `AB` | 曹羲 | [《三國志・諸夏侯曹傳》][252] | [JSON](30k_jzz_tpd_AB.json) |
| `AC` | 曹訓 | [《三國志・諸夏侯曹傳》][252] | [JSON](30k_jzz_tpd_AC.json) |
| `AD` | 曹則 | [《三國志・諸夏侯曹傳》][252] | [JSON](30k_jzz_tpd_AD.json) |
| `AE` | 曹彦 | [《三國志・諸夏侯曹傳》][252] | [JSON](30k_jzz_tpd_AE.json) |
| `AF` | 曹皚 | [《三國志・諸夏侯曹傳》][252] | [JSON](30k_jzz_tpd_AF.json) |
| `B` | 曹彬 | [《三國志・諸夏侯曹傳》][252] | [JSON](30k_jzz_tpd_B.json) |

</details>

<details><summary><code>315_3d4_416</code> 任旐（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 任旐 | [《三國志・徐胡二王傳》][262] | [JSON](315_3d4_416.json) |
| `A` | 任嘏 | [《三國志・徐胡二王傳》][262] | [JSON](315_3d4_416_A.json) |

</details>

<details><summary><code>318_d06_496</code> 黃祖（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 黃祖 | [《三國志・二荀賈傳》][253] | [JSON](318_d06_496.json) |
| `A` | 黃射 | [《三國志・二荀賈傳》][253] | [JSON](318_d06_496_A.json) |

</details>

<details><summary><code>326_faf_cd3</code> 王羲之（7 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 王羲之 | [《晉書・王羲之》][99] | [JSON](326_faf_cd3.json) |
| `*A` | 王靜之 | [《晉書・王羲之》][99] | [JSON](326_faf_cd3_%2AA.json) |
| `A` | 王玄之 | [《晉書・王羲之》][99]、[《晉書・王羲之》][100] | [JSON](326_faf_cd3_A.json) |
| `B` | 王徽之 | [《晉書・王羲之》][99] | [JSON](326_faf_cd3_B.json) |
| `BA` | 王楨之 | [《晉書・王羲之》][99] | [JSON](326_faf_cd3_BA.json) |
| `C` | 王操之 | [《晉書・王羲之》][99] | [JSON](326_faf_cd3_C.json) |
| `D` | 王肅之 | [《世說新語・排調》][410] | [JSON](326_faf_cd3_D.json) |

</details>

<details><summary><code>344_68f_98e</code> 郭嘉（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 郭嘉 | [《三國志・二荀賈傳》][254] | [JSON](344_68f_98e.json) |
| `A` | 郭奕（字伯益，郭嘉子） | [《三國志・徐胡二王傳》][262] | [JSON](344_68f_98e_A.json) |

</details>

<details><summary><code>37j_16p_7n8</code> 曹參（6 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 曹參 | [《史記・曹相國世家》][300] | [JSON](37j_16p_7n8.json) |
| `A` | 窋 | [《史記・曹相國世家》][300] | [JSON](37j_16p_7n8_A.json) |
| `AA` | 奇 | [《史記・曹相國世家》][300] | [JSON](37j_16p_7n8_AA.json) |
| `AAA` | 時 | [《史記・曹相國世家》][300] | [JSON](37j_16p_7n8_AAA.json) |
| `AAAA` | 襄 | [《史記・衛將軍驃騎列傳》][357] | [JSON](37j_16p_7n8_AAAA.json) |
| `AAAAA` | 宗 | [《史記・曹相國世家》][300] | [JSON](37j_16p_7n8_AAAAA.json) |

</details>

<details><summary><code>3b9_b07_bdb</code> 馮紞（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 馮紞 | [《晉書・王沈 荀顗 荀勖 馮紞》][68] | [JSON](3b9_b07_bdb.json) |
| `A` | 播（馮紞子） | [《晉書・王沈 荀顗 荀勖 馮紞》][68] | [JSON](3b9_b07_bdb_A.json) |
| `B` | 熊（馮紞子） | [《晉書・王沈 荀顗 荀勖 馮紞》][68] | [JSON](3b9_b07_bdb_B.json) |

</details>

<details><summary><code>3bh_k4m_fg4</code> 宋太祖義隆（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 宋太祖義隆 | [《宋書・王華 王曇首 殷景仁 沈演之》][443] | [JSON](3bh_k4m_fg4.json) |
| `A` | 東陽獻公主 | [《南史・后妃上》][178]、[《宋書・后妃》][423]、[《宋書・徐湛之 江湛 王僧綽》][451] | [JSON](3bh_k4m_fg4_A.json) |

</details>

<details><summary><code>3c9_d1d_870</code> 王謐（4 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 王謐 | [《晉書・王導》][82] | [JSON](3c9_d1d_870.json) |
| `A` | 王瓘 | [《晉書・王導》][82] | [JSON](3c9_d1d_870_A.json) |
| `B` | 王球 | [《南史・謝弘微》][198] | [JSON](3c9_d1d_870_B.json) |
| `C` | 王琇 | [《晉書・王導》][82] | [JSON](3c9_d1d_870_C.json) |

</details>

<details><summary><code>3ea_uzt_2n2</code> 何准（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 何准 | [《晉書・后妃下》][60] | [JSON](3ea_uzt_2n2.json) |
| `A` | 何法倪 | [《晉書・后妃下》][60] | [JSON](3ea_uzt_2n2_A.json) |

</details>

<details><summary><code>3jf_ce1_jy2</code> 昆莫父（未名）（大宛列傳候選）（5 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 昆莫父（未名） | [《史記・大宛列傳》][369] | [JSON](3jf_ce1_jy2.json) |
| `A` | 昆莫 | [《史記・大宛列傳》][369] | [JSON](3jf_ce1_jy2_A.json) |
| `AA` | 大祿 | [《史記・大宛列傳》][369] | [JSON](3jf_ce1_jy2_AA.json) |
| `AB` | 大祿兄（未名太子） | [《史記・大宛列傳》][369] | [JSON](3jf_ce1_jy2_AB.json) |
| `ABA` | 岑娶 | [《史記・大宛列傳》][369] | [JSON](3jf_ce1_jy2_ABA.json) |

</details>

<details><summary><code>3qs_nqa_ioa</code> 混〔靖父；武原令〕（6 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 混〔靖父；武原令〕 | [《宋書・武帝上》][418] | [JSON](3qs_nqa_ioa.json) |
| `A` | 靖〔翹父；東安太守〕 | [《宋書・武帝上》][418] | [JSON](3qs_nqa_ioa_A.json) |
| `AA` | 翹〔孝皇帝；高祖之父〕 | [《宋書・后妃》][422] | [JSON](3qs_nqa_ioa_AA.json) |
| `AAA` | 宋高祖裕 | [《魏書・崔浩》][474] | [JSON](3qs_nqa_ioa_AAA.json) |
| `AAB` | 道憐 | [《宋書・張茂度 庾登之 謝方明 江夷》][434] | [JSON](3qs_nqa_ioa_AAB.json) |
| `AAC` | 臨川王道規 | [《晉書・叛臣二》][110] | [JSON](3qs_nqa_ioa_AAC.json) |

</details>

<details><summary><code>3te_z66_d5a</code> 張敖（外戚世家候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 張敖 | [《史記・外戚世家》][295] | [JSON](3te_z66_d5a.json) |
| `A` | 孝惠皇后 | [《史記・外戚世家》][295] | [JSON](3te_z66_d5a_A.json) |

</details>

<details><summary><code>3tg_h3n_iou</code> 樂玄（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 樂玄 | [《南齊書・王琨 張岱 褚炫 何戢 王延之 阮韜》][149]、[《南史・王誕　王華　王惠　王彧》][240] | [JSON](3tg_h3n_iou.json) |
| `A` | 樂玄女〔王懌妻〕 | — | [JSON](3tg_h3n_iou_A.json) |

</details>

<details><summary><code>3tt_4ey_uti</code> 袁湛（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 袁湛 | [《晉書・謝尚 謝安》][98] | [JSON](3tt_4ey_uti.json) |
| `A` | 袁齊媯 | [《南史・后妃上》][178]、[《宋書・后妃》][423] | [JSON](3tt_4ey_uti_A.json) |

</details>

<details><summary><code>3tw_nq2_gyn</code> 霍去病（外戚世家候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 霍去病 | [《史記・衛將軍驃騎列傳》][357] | [JSON](3tw_nq2_gyn.json) |
| `A` | 嬗 | [《史記・衛將軍驃騎列傳》][357] | [JSON](3tw_nq2_gyn_A.json) |

</details>

<details><summary><code>3xx_gdy_or6</code> 裴〔周浚父〕等兩支（共同父未名；編輯接合）（15 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `A` | 裴〔周浚父〕 | [《晉書・周浚 成公簡 苟晞 華軼 劉喬》][79] | [JSON](3xx_gdy_or6_A.json) |
| `AA` | 周浚 | [《晉書・周浚 成公簡 苟晞 華軼 劉喬》][79] | [JSON](3xx_gdy_or6_AA.json) |
| `AAA` | 周顗 | [《晉書・劉隗 刁協 戴若思 周顗》][84] | [JSON](3xx_gdy_or6_AAA.json) |
| `AAAA` | 周閔 | [《晉書・劉隗 刁協 戴若思 周顗》][84] | [JSON](3xx_gdy_or6_AAAA.json) |
| `AAAB` | 周恬 | [《晉書・劉隗 刁協 戴若思 周顗》][84] | [JSON](3xx_gdy_or6_AAAB.json) |
| `AAAC` | 周頤 | [《晉書・劉隗 刁協 戴若思 周顗》][84] | [JSON](3xx_gdy_or6_AAAC.json) |
| `AAACA` | 周琳 | [《晉書・劉隗 刁協 戴若思 周顗》][84] | [JSON](3xx_gdy_or6_AAACA.json) |
| `AAACAA` | 周文 | [《晉書・劉隗 刁協 戴若思 周顗》][84] | [JSON](3xx_gdy_or6_AAACAA.json) |
| `AAB` | 周嵩 | [《晉書・周浚 成公簡 苟晞 華軼 劉喬》][79] | [JSON](3xx_gdy_or6_AAB.json) |
| `AABA` | 王應之嫂〔嵩之女，未名〕 | [《晉書・周浚 成公簡 苟晞 華軼 劉喬》][79] | [JSON](3xx_gdy_or6_AABA.json) |
| `AAC` | 周謨 | [《晉書・周浚 成公簡 苟晞 華軼 劉喬》][79] | [JSON](3xx_gdy_or6_AAC.json) |
| `B` | 蕤〔周馥父〕 | [《晉書・周浚 成公簡 苟晞 華軼 劉喬》][79] | [JSON](3xx_gdy_or6_B.json) |
| `BA` | 周馥 | [《晉書・周浚 成公簡 苟晞 華軼 劉喬》][79] | [JSON](3xx_gdy_or6_BA.json) |
| `BAA` | 密〔周馥子〕 | [《晉書・周浚 成公簡 苟晞 華軼 劉喬》][79] | [JSON](3xx_gdy_or6_BAA.json) |
| `BAB` | 周矯 | [《晉書・周浚 成公簡 苟晞 華軼 劉喬》][79] | [JSON](3xx_gdy_or6_BAB.json) |

</details>

<details><summary><code>408_ce3_5d8</code> 沈慶之（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 沈慶之 | [《南史・王弘》][207]、[《宋書・王僧達 顏竣》][452] | [JSON](408_ce3_5d8.json) |
| `A` | 沈文季 | [《南齊書・徐孝嗣 沈文季》][164]、[《南史・王曇首》][222] | [JSON](408_ce3_5d8_A.json) |

</details>

<details><summary><code>42z_cse_1ka</code> 熊良夫（楚宣王）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 熊良夫（楚宣王） | [《史記・楚世家》][286] | [JSON](42z_cse_1ka.json) |
| `A` | 熊商（楚威王） | [《史記・楚世家》][286] | [JSON](42z_cse_1ka_A.json) |

</details>

<details><summary><code>46a_tvp_dq9</code> 秦獻公（魏世家候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 秦獻公 | [《史記・魏世家》][290] | [JSON](46a_tvp_dq9.json) |
| `A` | 秦孝公 | [《史記・魏世家》][290] | [JSON](46a_tvp_dq9_A.json) |

</details>

<details><summary><code>47p_kjh_ez7</code> 齊太祖道成（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 齊太祖道成 | [《梁書・謝朏 弟子覽》][120] | [JSON](47p_kjh_ez7.json) |
| `A` | 臨海長公主（齊高帝女） | [《南史・王曇首》][216] | [JSON](47p_kjh_ez7_A.json) |
| `B` | 江夏王鋒 | [《南齊書・高祖十二王》][154] | [JSON](47p_kjh_ez7_B.json) |

</details>

<details><summary><code>49g_7az_e4i</code> 李斯（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 李斯 | [《史記・李斯列傳》][333] | [JSON](49g_7az_e4i.json) |
| `A` | 李由 | [《史記・李斯列傳》][333] | [JSON](49g_7az_e4i_A.json) |
| `B` | 李斯中子未名 | [《史記・李斯列傳》][333] | [JSON](49g_7az_e4i_B.json) |

</details>

<details><summary><code>4ag_yml_73x</code> 休（平原劉氏父）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 休（平原劉氏父） | [《崔混墓誌・節錄》][12] | [JSON](4ag_yml_73x.json) |
| `A` | 劉氏（崔敬友妻） | [《崔混墓誌・節錄》][12] | [JSON](4ag_yml_73x_A.json) |

</details>

<details><summary><code>4c2_763_efd</code> 謝喻（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 謝喻 | [《晉書・謝尚 謝安》][98] | [JSON](4c2_763_efd.json) |
| `A` | 謝暠 | [《晉書・謝尚 謝安》][98] | [JSON](4c2_763_efd_A.json) |

</details>

<details><summary><code>4ij_7ik_fgy</code> 謝鯤（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 謝鯤 | [《晉書・謝尚 謝安》][98] | [JSON](4ij_7ik_fgy.json) |
| `A` | 謝尚 | [《晉書・謝尚 謝安》][98] | [JSON](4ij_7ik_fgy_A.json) |

</details>

<details><summary><code>4qr_wrk_3vd</code> 庾琛（32 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 庾琛 | [《晉書・庾亮》][86] | [JSON](4qr_wrk_3vd.json) |
| `A` | 庾文君 | [《晉書・后妃下》][63]、[《晉書・庾亮》][86] | [JSON](4qr_wrk_3vd_A.json) |
| `B` | 庾亮 | [《晉書・庾亮》][86] | [JSON](4qr_wrk_3vd_B.json) |
| `BA` | 庾彬 | [《晉書・庾亮》][86] | [JSON](4qr_wrk_3vd_BA.json) |
| `BB` | 庾羲 | [《晉書・庾亮》][86] | [JSON](4qr_wrk_3vd_BB.json) |
| `BBA` | 庾准 | [《晉書・庾亮》][86] | [JSON](4qr_wrk_3vd_BBA.json) |
| `BBAA` | 庾悅 | [《晉書・庾亮》][86] | [JSON](4qr_wrk_3vd_BBAA.json) |
| `BBB` | 庾楷 | [《晉書・叛臣二》][110] | [JSON](4qr_wrk_3vd_BBB.json) |
| `BC` | 庾龢 | [《晉書・庾亮》][86] | [JSON](4qr_wrk_3vd_BC.json) |
| `BCA` | 庾恆 | [《晉書・庾亮》][86] | [JSON](4qr_wrk_3vd_BCA.json) |
| `C` | 庾懌 | [《晉書・庾亮》][85] | [JSON](4qr_wrk_3vd_C.json) |
| `CA` | 庾統 | [《晉書・庾亮》][85] | [JSON](4qr_wrk_3vd_CA.json) |
| `CAA` | 庾玄之 | [《晉書・庾亮》][85] | [JSON](4qr_wrk_3vd_CAA.json) |
| `D` | 庾冰 | [《晉書・庾亮》][85] | [JSON](4qr_wrk_3vd_D.json) |
| `DA` | 庾希 | [《晉書・庾亮》][85] | [JSON](4qr_wrk_3vd_DA.json) |
| `DAA` | 庾攸之 | [《晉書・庾亮》][85] | [JSON](4qr_wrk_3vd_DAA.json) |
| `DB` | 庾襲 | [《晉書・庾亮》][85] | [JSON](4qr_wrk_3vd_DB.json) |
| `DC` | 庾友 | [《晉書・庾亮》][85] | [JSON](4qr_wrk_3vd_DC.json) |
| `DCA` | 庾叔宣 | [《晉書・庾亮》][85] | [JSON](4qr_wrk_3vd_DCA.json) |
| `DD` | 庾蘊 | [《晉書・庾亮》][85] | [JSON](4qr_wrk_3vd_DD.json) |
| `DDA` | 庾廓之 | [《晉書・庾亮》][85] | [JSON](4qr_wrk_3vd_DDA.json) |
| `DDB` | 庾廓（宋書原稱） | [《宋書・張茂度 庾登之 謝方明 江夷》][433] | [JSON](4qr_wrk_3vd_DDB.json) |
| `DDBA` | 庾登之 | [《宋書・張茂度 庾登之 謝方明 江夷》][433] | [JSON](4qr_wrk_3vd_DDBA.json) |
| `DDBAA` | 庾沖遠 | [《宋書・張茂度 庾登之 謝方明 江夷》][433] | [JSON](4qr_wrk_3vd_DDBAA.json) |
| `DDBB` | 庾炳之 | [《宋書・張茂度 庾登之 謝方明 江夷》][433] | [JSON](4qr_wrk_3vd_DDBB.json) |
| `DDBBA` | 庾季遠 | [《宋書・張茂度 庾登之 謝方明 江夷》][433] | [JSON](4qr_wrk_3vd_DDBBA.json) |
| `DDBBB` | 庾弘遠 | [《宋書・張茂度 庾登之 謝方明 江夷》][433] | [JSON](4qr_wrk_3vd_DDBBB.json) |
| `DE` | 庾倩 | [《晉書・庾亮》][85] | [JSON](4qr_wrk_3vd_DE.json) |
| `DF` | 庾邈 | [《晉書・庾亮》][85] | [JSON](4qr_wrk_3vd_DF.json) |
| `DG` | 庾柔 | [《晉書・庾亮》][85] | [JSON](4qr_wrk_3vd_DG.json) |
| `E` | 庾條 | [《晉書・庾亮》][85] | [JSON](4qr_wrk_3vd_E.json) |
| `F` | 庾翼 | [《晉書・謝尚 謝安》][98] | [JSON](4qr_wrk_3vd_F.json) |

</details>

<details><summary><code>4w5_b4e_vf5</code> 王翁孺（14 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 王翁孺 | [《漢書・元后傳》][30] | [JSON](4w5_b4e_vf5.json) |
| `A` | 王禁 | [《漢書・元后傳》][30] | [JSON](4w5_b4e_vf5_A.json) |
| `AA` | 君俠 | [《漢書・元后傳》][30] | [JSON](4w5_b4e_vf5_AA.json) |
| `AB` | 政君 | [《漢書・元后傳》][30] | [JSON](4w5_b4e_vf5_AB.json) |
| `AC` | 君力 | [《漢書・元后傳》][30] | [JSON](4w5_b4e_vf5_AC.json) |
| `AD` | 君弟 | [《漢書・元后傳》][30] | [JSON](4w5_b4e_vf5_AD.json) |
| `AE` | 鳳 | [《漢書・元后傳》][30] | [JSON](4w5_b4e_vf5_AE.json) |
| `AF` | 曼 | [《漢書・元后傳》][30] | [JSON](4w5_b4e_vf5_AF.json) |
| `AG` | 譚 | [《漢書・元后傳》][30] | [JSON](4w5_b4e_vf5_AG.json) |
| `AH` | 崇 | [《漢書・元后傳》][30] | [JSON](4w5_b4e_vf5_AH.json) |
| `AI` | 商 | [《漢書・元后傳》][30] | [JSON](4w5_b4e_vf5_AI.json) |
| `AJ` | 立 | [《漢書・元后傳》][30] | [JSON](4w5_b4e_vf5_AJ.json) |
| `AK` | 根 | [《漢書・元后傳》][30] | [JSON](4w5_b4e_vf5_AK.json) |
| `AL` | 逢時 | [《漢書・元后傳》][30] | [JSON](4w5_b4e_vf5_AL.json) |

</details>

<details><summary><code>4wv_6og_mwb</code> 申無宇（芋尹）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 申無宇（芋尹） | [《史記・楚世家》][286] | [JSON](4wv_6og_mwb.json) |
| `A` | 申亥（收葬楚靈王者） | [《史記・楚世家》][286] | [JSON](4wv_6og_mwb_A.json) |

</details>

<details><summary><code>4xe_ms4_pr9</code> 夢者（曹亡敘事未名）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 夢者（曹亡敘事未名） | [《史記・管蔡世家》][281] | [JSON](4xe_ms4_pr9.json) |
| `A` | 夢者子（未名） | [《史記・管蔡世家》][281] | [JSON](4xe_ms4_pr9_A.json) |

</details>

<details><summary><code>4xl_1hw_6cg</code> 孫宏（許邁妻父）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 孫宏（許邁妻父） | [《真誥・卷二十》][485] | [JSON](4xl_1hw_6cg.json) |
| `A` | 孫氏（許邁妻） | [《晉書・王羲之》][99] | [JSON](4xl_1hw_6cg_A.json) |

</details>

<details><summary><code>4yg_ete_09a</code> 柴武（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 柴武 | [《史記・韓信盧綰列傳》][339] | [JSON](4yg_ete_09a.json) |
| `A` | 奇（柴武子） | [《史記・淮南衡山列傳》][364] | [JSON](4yg_ete_09a_A.json) |

</details>

<details><summary><code>505_n4y_p39</code> 秦開（匈奴列傳候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 秦開 | [《史記・匈奴列傳》][356] | [JSON](505_n4y_p39.json) |
| `*A` | 秦舞陽 | [《史記・刺客列傳》][332] | [JSON](505_n4y_p39_%2AA.json) |

</details>

<details><summary><code>50h_gqe_1p1</code> 具（魯獻公）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 具（魯獻公） | [《史記・魯周公世家》][279] | [JSON](50h_gqe_1p1.json) |
| `A` | 濞（魯真公） | [《史記・魯周公世家》][279]、[《史記・三代世表》][494] | [JSON](50h_gqe_1p1_A.json) |

</details>

<details><summary><code>573_104_0c1</code> 李崇（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 李崇 | [《魏書・刁雍 王慧龍 韓延之 袁式》][475] | [JSON](573_104_0c1.json) |
| `A` | 李世哲 | [《魏書・刁雍 王慧龍 韓延之 袁式》][475] | [JSON](573_104_0c1_A.json) |
| `B` | 青肫〔李崇子〕 | [《魏書・刁雍 王慧龍 韓延之 袁式》][475] | [JSON](573_104_0c1_B.json) |

</details>

<details><summary><code>59d_72d_924</code> 王雅（4 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 王雅 | [《晉書・王湛 荀崧 范汪 劉惔 張憑 韓伯》][88] | [JSON](59d_72d_924.json) |
| `A` | 王准之（東海，王雅子） | [《南史・江淹　任昉　王僧孺》][250] | [JSON](59d_72d_924_A.json) |
| `AA` | 王延年（王僧孺父） | [《南史・江淹　任昉　王僧孺》][250] | [JSON](59d_72d_924_AA.json) |
| `AAA` | 王僧孺 | [《南史・王曇首》][221]、[《南史・江淹　任昉　王僧孺》][250] | [JSON](59d_72d_924_AAA.json) |

</details>

<details><summary><code>5bo_dxd_69k</code> 冉雍父（弟子列傳候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 冉雍父 | [《史記・仲尼弟子列傳》][313] | [JSON](5bo_dxd_69k.json) |
| `A` | 冉雍 | [《史記・仲尼弟子列傳》][313] | [JSON](5bo_dxd_69k_A.json) |

</details>

<details><summary><code>5dd_l1c_6g8</code> 衛青（5 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 衛青 | [《史記・衛將軍驃騎列傳》][357] | [JSON](5dd_l1c_6g8.json) |
| `A` | 衛青子陰安侯 | [《史記・衛將軍驃騎列傳》][357] | [JSON](5dd_l1c_6g8_A.json) |
| `B` | 衛青子發干侯 | [《史記・衛將軍驃騎列傳》][357] | [JSON](5dd_l1c_6g8_B.json) |
| `C` | 衛青子宜春侯（來源候選；預設不接父系） | [《史記・外戚世家》][295] | [JSON](5dd_l1c_6g8_C.json) |
| `D` | 衛伉 | [《史記・衛將軍驃騎列傳》][357] | [JSON](5dd_l1c_6g8_D.json) |

</details>

<details><summary><code>5dm_e40_rqh</code> 古公亶父（28 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 古公亶父 | [《史記・周本紀》][268] | [JSON](5dm_e40_rqh.json) |
| `A` | 仲雍 | [《史記・吳太伯世家》][277] | [JSON](5dm_e40_rqh_A.json) |
| `AA` | 季簡 | [《史記・吳太伯世家》][277] | [JSON](5dm_e40_rqh_AA.json) |
| `AAA` | 叔達 | [《史記・吳太伯世家》][277] | [JSON](5dm_e40_rqh_AAA.json) |
| `AAAA` | 周章（吳君） | [《史記・吳太伯世家》][277] | [JSON](5dm_e40_rqh_AAAA.json) |
| `AAAAA` | 熊遂 | [《史記・吳太伯世家》][277] | [JSON](5dm_e40_rqh_AAAAA.json) |
| `AAAAAA` | 柯相 | [《史記・吳太伯世家》][277] | [JSON](5dm_e40_rqh_AAAAAA.json) |
| `AAAAAAA` | 彊鳩夷 | [《史記・吳太伯世家》][277] | [JSON](5dm_e40_rqh_AAAAAAA.json) |
| `AAAAAAAA` | 餘橋疑吾 | [《史記・吳太伯世家》][277] | [JSON](5dm_e40_rqh_AAAAAAAA.json) |
| `AAAAAAAAA` | 柯盧 | [《史記・吳太伯世家》][277] | [JSON](5dm_e40_rqh_AAAAAAAAA.json) |
| `AAAAAAAAAA` | 周繇 | [《史記・吳太伯世家》][277] | [JSON](5dm_e40_rqh_AAAAAAAAAA.json) |
| `AAAAAAAAAAA` | 屈羽 | [《史記・吳太伯世家》][277] | [JSON](5dm_e40_rqh_AAAAAAAAAAA.json) |
| `AAAAAAAAAAAA` | 夷吾（吳君） | [《史記・吳太伯世家》][277] | [JSON](5dm_e40_rqh_AAAAAAAAAAAA.json) |
| `AAAAAAAAAAAAA` | 禽處 | [《史記・吳太伯世家》][277] | [JSON](5dm_e40_rqh_AAAAAAAAAAAAA.json) |
| `AAAAAAAAAAAAAA` | 轉（吳君） | [《史記・吳太伯世家》][277] | [JSON](5dm_e40_rqh_AAAAAAAAAAAAAA.json) |
| `AAAAAAAAAAAAAAA` | 頗髙 | [《史記・吳太伯世家》][277] | [JSON](5dm_e40_rqh_AAAAAAAAAAAAAAA.json) |
| `AAAAAAAAAAAAAAAA` | 句卑 | [《史記・吳太伯世家》][277] | [JSON](5dm_e40_rqh_AAAAAAAAAAAAAAAA.json) |
| `AAAAAAAAAAAAAAAAA` | 去齊 | [《史記・吳太伯世家》][277] | [JSON](5dm_e40_rqh_AAAAAAAAAAAAAAAAA.json) |
| `AAAAAAAAAAAAAAAAAA` | 壽夢 | [《史記・吳太伯世家》][277] | [JSON](5dm_e40_rqh_AAAAAAAAAAAAAAAAAA.json) |
| `AAAAAAAAAAAAAAAAAAA` | 諸樊 | [《史記・吳太伯世家》][277] | [JSON](5dm_e40_rqh_AAAAAAAAAAAAAAAAAAA.json) |
| `AAAAAAAAAAAAAAAAAAAA` | 闔閭 | [《史記・吳太伯世家》][277] | [JSON](5dm_e40_rqh_AAAAAAAAAAAAAAAAAAAA.json) |
| `AAAAAAAAAAAAAAAAAAAAA` | 夫差 | [《史記・越王勾踐世家》][287] | [JSON](5dm_e40_rqh_AAAAAAAAAAAAAAAAAAAAA.json) |
| `AAAAAAAAAAAAAAAAAAB` | 餘祭 | [《史記・吳太伯世家》][277] | [JSON](5dm_e40_rqh_AAAAAAAAAAAAAAAAAAB.json) |
| `AAAAAAAAAAAAAAAAAAC` | 餘眛 | [《史記・吳太伯世家》][277] | [JSON](5dm_e40_rqh_AAAAAAAAAAAAAAAAAAC.json) |
| `AAAAAAAAAAAAAAAAAACA` | 僚（吳王） | [《史記・吳太伯世家》][277] | [JSON](5dm_e40_rqh_AAAAAAAAAAAAAAAAAACA.json) |
| `AAAAAAAAAAAAAAAAAAD` | 季札 | [《史記・吳太伯世家》][277] | [JSON](5dm_e40_rqh_AAAAAAAAAAAAAAAAAAD.json) |
| `B` | 太伯 | [《史記・吳太伯世家》][277] | [JSON](5dm_e40_rqh_B.json) |
| `C` | 虞仲 | [《史記・周本紀》][268] | [JSON](5dm_e40_rqh_C.json) |

</details>

<details><summary><code>5if_pf6_zos</code> 郭解父（未名）（游俠列傳候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 郭解父（未名） | [《史記・游俠列傳》][370] | [JSON](5if_pf6_zos.json) |
| `A` | 郭解 | [《史記・游俠列傳》][370] | [JSON](5if_pf6_zos_A.json) |

</details>

<details><summary><code>5is_zik_jbp</code> 劉弘〔荊州刺史〕（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 劉弘〔荊州刺史〕 | [《晉書・劉弘 陶侃》][83] | [JSON](5is_zik_jbp.json) |
| `A` | 劉璠〔劉弘子〕 | [《晉書・山濤 王戎 郭舒 樂廣》][70]、[《晉書・劉弘 陶侃》][83] | [JSON](5is_zik_jbp_A.json) |

</details>

<details><summary><code>5jc_z9b_i2n</code> 柳卓（6 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 柳卓 | [《宋書・柳元景 顏師伯 沈慶之》][453] | [JSON](5jc_z9b_i2n.json) |
| `A` | 柳恬 | [《宋書・柳元景 顏師伯 沈慶之》][453] | [JSON](5jc_z9b_i2n_A.json) |
| `AA` | 柳憑 | [《南齊書・柳世隆 張瑰》][147]、[《宋書・柳元景 顏師伯 沈慶之》][453] | [JSON](5jc_z9b_i2n_AA.json) |
| `AAA` | 柳叔宗 | [《南齊書・柳世隆 張瑰》][147] | [JSON](5jc_z9b_i2n_AAA.json) |
| `AAAA` | 柳世隆 | [《南齊書・柳世隆 張瑰》][147] | [JSON](5jc_z9b_i2n_AAAA.json) |
| `AAB` | 柳元景 | [《宋書・柳元景 顏師伯 沈慶之》][453] | [JSON](5jc_z9b_i2n_AAB.json) |

</details>

<details><summary><code>5km_89r_9jr</code> 元君（衛嗣君弟）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 元君（衛嗣君弟） | [《史記・衛康叔世家》][283] | [JSON](5km_89r_9jr.json) |
| `A` | 衛君角 | [《史記・衛康叔世家》][283] | [JSON](5km_89r_9jr_A.json) |

</details>

<details><summary><code>5pw_05i_uhv</code> 平（本文燕昭王）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 平（本文燕昭王） | [《史記・樂毅列傳》][326] | [JSON](5pw_05i_uhv.json) |
| `A` | 惠王（燕昭王子） | [《史記・樂毅列傳》][326] | [JSON](5pw_05i_uhv_A.json) |

</details>

<details><summary><code>5xt_rg8_7zs</code> 項燕（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 項燕 | [《史記・秦始皇本紀》][270]、[《史記・六國年表》][496] | [JSON](5xt_rg8_7zs.json) |
| `A` | 項梁 | [《史記・項羽本紀》][271] | [JSON](5xt_rg8_7zs_A.json) |

</details>

<details><summary><code>684_eaa_511</code> 謝景仁（5 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 謝景仁 | [《南史・謝晦　謝裕　謝方明　謝靈運》][195] | [JSON](684_eaa_511.json) |
| `A` | 謝恂 | [《南史・謝晦　謝裕　謝方明　謝靈運》][195] | [JSON](684_eaa_511_A.json) |
| `AA` | 謝孺子 | [《南史・謝晦　謝裕　謝方明　謝靈運》][195] | [JSON](684_eaa_511_AA.json) |
| `AAA` | 謝璟 | [《南史・謝晦　謝裕　謝方明　謝靈運》][195] | [JSON](684_eaa_511_AAA.json) |
| `AAAA` | 謝微 | [《南史・謝晦　謝裕　謝方明　謝靈運》][195] | [JSON](684_eaa_511_AAAA.json) |

</details>

<details><summary><code>696_456_df6</code> 荀曇（6 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 荀曇 | [《三國志・二荀賈傳》][254] | [JSON](696_456_df6.json) |
| `A` | 荀彞 | [《三國志・二荀賈傳》][254] | [JSON](696_456_df6_A.json) |
| `AA` | 荀攸 | [《三國志・二荀賈傳》][254] | [JSON](696_456_df6_AA.json) |
| `AA*A` | 荀彪 | [《三國志・二荀賈傳》][254] | [JSON](696_456_df6_AA%2AA.json) |
| `AAA` | 荀緝 | [《三國志・二荀賈傳》][254] | [JSON](696_456_df6_AAA.json) |
| `AAB` | 荀適 | [《三國志・二荀賈傳》][254] | [JSON](696_456_df6_AAB.json) |

</details>

<details><summary><code>69x_se2_859</code> 邴吉（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 邴吉 | [《史記・張丞相列傳》][342] | [JSON](69x_se2_859.json) |
| `A` | 邴顯 | [《史記・張丞相列傳》][342] | [JSON](69x_se2_859_A.json) |

</details>

<details><summary><code>6bn_yfc_lzi</code> 田叔（梁孝王世家候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 田叔 | [《史記・田叔列傳》][350] | [JSON](6bn_yfc_lzi.json) |
| `A` | 田仁 | [《史記・田叔列傳》][350] | [JSON](6bn_yfc_lzi_A.json) |

</details>

<details><summary><code>6d6_eg1_o3a</code> 王仲（外戚世家候選）（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 王仲 | [《史記・外戚世家》][295] | [JSON](6d6_eg1_o3a.json) |
| `A` | 王太后 | [《史記・外戚世家》][295] | [JSON](6d6_eg1_o3a_A.json) |
| `B` | 王信 | [《史記・絳侯周勃世家》][303] | [JSON](6d6_eg1_o3a_B.json) |

</details>

<details><summary><code>6di_ywz_ju4</code> 莊伯（晉曲沃弒君記事）（13 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 莊伯（晉曲沃弒君記事） | [《史記・晉世家》][285] | [JSON](6di_ywz_ju4.json) |
| `A` | 稱（曲沃／晉武公） | [《史記・晉世家》][285] | [JSON](6di_ywz_ju4_A.json) |
| `AA` | 晉獻公 | [《史記・晉世家》][285] | [JSON](6di_ywz_ju4_AA.json) |
| `AAA` | 晉文公 | [《史記・晉世家》][285] | [JSON](6di_ywz_ju4_AAA.json) |
| `AAAA` | 伯鯈（重耳子） | [《史記・晉世家》][285] | [JSON](6di_ywz_ju4_AAAA.json) |
| `AAAB` | 叔劉（重耳子） | [《史記・晉世家》][285] | [JSON](6di_ywz_ju4_AAAB.json) |
| `AAAC` | 黑臀（晉成公） | [《史記・晉世家》][285] | [JSON](6di_ywz_ju4_AAAC.json) |
| `AAAD` | 晉襄公 | [《史記・晉世家》][285] | [JSON](6di_ywz_ju4_AAAD.json) |
| `AAADA` | 捷（晉襄公少子桓叔） | [《史記・晉世家》][285] | [JSON](6di_ywz_ju4_AAADA.json) |
| `AAADAA` | 談（惠伯） | [《史記・晉世家》][285] | [JSON](6di_ywz_ju4_AAADAA.json) |
| `AAADAAA` | 晉悼公 | [《史記・晉世家》][285] | [JSON](6di_ywz_ju4_AAADAAA.json) |
| `AAB` | 申生 | [《史記・晉世家》][285] | [JSON](6di_ywz_ju4_AAB.json) |
| `AAC` | 奚齊 | [《史記・晉世家》][285] | [JSON](6di_ywz_ju4_AAC.json) |

</details>

<details><summary><code>6f6_d1e_11a</code> 道素（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 道素 | [《晉書・王沈 荀顗 荀勖 馮紞》][68] | [JSON](6f6_d1e_11a.json) |
| `A` | 崇之 | [《晉書・王沈 荀顗 荀勖 馮紞》][68] | [JSON](6f6_d1e_11a_A.json) |

</details>

<details><summary><code>6fg_r6l_5a5</code> 嵇康（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 嵇康 | [《晉書・忠義》][101] | [JSON](6fg_r6l_5a5.json) |
| `A` | 嵇紹 | [《晉書・忠義》][101] | [JSON](6fg_r6l_5a5_A.json) |
| `AA` | 嵇軫 | [《晉書・忠義》][101] | [JSON](6fg_r6l_5a5_AA.json) |

</details>

<details><summary><code>6ks_x4x_dbf</code> 臧荼（外戚世家候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 臧荼 | [《史記・外戚世家》][295] | [JSON](6ks_x4x_dbf.json) |
| `*A` | 臧兒 | [《史記・外戚世家》][295] | [JSON](6ks_x4x_dbf_%2AA.json) |

</details>

<details><summary><code>6lr_zci_i0j</code> 郗鑒（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 郗鑒 | [《晉書・庾亮》][86] | [JSON](6lr_zci_i0j.json) |
| `A` | 郗璿 | [《世說新語・雅量》][389] | [JSON](6lr_zci_i0j_A.json) |

</details>

<details><summary><code>6oy_t19_ywe</code> 秦惠王（蘇秦列傳候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 秦惠王 | [《史記・蘇秦列傳》][315] | [JSON](6oy_t19_ywe.json) |
| `A` | 秦惠王女 | [《史記・蘇秦列傳》][315] | [JSON](6oy_t19_ywe_A.json) |

</details>

<details><summary><code>6wx_fr3_b2e</code> 滿（陳胡公）（8 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 滿（陳胡公） | [《史記・陳杞世家》][282] | [JSON](6wx_fr3_b2e.json) |
| `A` | 犀侯（陳申公） | [《史記・陳杞世家》][282] | [JSON](6wx_fr3_b2e_A.json) |
| `AA` | 突（陳孝公） | [《史記・陳杞世家》][282] | [JSON](6wx_fr3_b2e_AA.json) |
| `AAA` | 圉戎（陳慎公） | [《史記・陳杞世家》][282] | [JSON](6wx_fr3_b2e_AAA.json) |
| `AAAA` | 寧（陳幽公） | [《史記・陳杞世家》][282] | [JSON](6wx_fr3_b2e_AAAA.json) |
| `AAAAA` | 孝（陳釐公） | [《史記・陳杞世家》][282] | [JSON](6wx_fr3_b2e_AAAAA.json) |
| `AAAAAA` | 靈（陳武公） | [《史記・陳杞世家》][282] | [JSON](6wx_fr3_b2e_AAAAAA.json) |
| `AAAAAAA` | 說（陳夷公） | [《史記・陳杞世家》][282] | [JSON](6wx_fr3_b2e_AAAAAAA.json) |

</details>

<details><summary><code>719_b25_cc3</code> 庾深之（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 庾深之 | [《南齊書・虞玩之 劉休 沈沖 庾杲之 王諶》][153] | [JSON](719_b25_cc3.json) |
| `A` | 庾粲 | [《南齊書・虞玩之 劉休 沈沖 庾杲之 王諶》][153] | [JSON](719_b25_cc3_A.json) |
| `AA` | 庾杲之 | [《南齊書・虞玩之 劉休 沈沖 庾杲之 王諶》][153] | [JSON](719_b25_cc3_AA.json) |

</details>

<details><summary><code>766_5dq_zws</code> 朱家（季布欒布列傳候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 朱家 | [《史記・季布欒布列傳》][346] | [JSON](766_5dq_zws.json) |
| `A` | 朱家子未名 | [《史記・季布欒布列傳》][346] | [JSON](766_5dq_zws_A.json) |

</details>

<details><summary><code>77h_id3_a0i</code> 陸邵（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 陸邵 | [《南齊書・劉瓛 弟璡 陸澄》][157]、[《南史・陸澄　陸慧曉　陸杲》][249] | [JSON](77h_id3_a0i.json) |
| `A` | 陸瑗 | [《南齊書・劉瓛 弟璡 陸澄》][157]、[《南史・陸澄　陸慧曉　陸杲》][249] | [JSON](77h_id3_a0i_A.json) |
| `AA` | 陸澄 | [《南齊書・褚淵 淵弟澄 徐嗣 王儉》][146]、[《南史・王曇首》][222] | [JSON](77h_id3_a0i_AA.json) |

</details>

<details><summary><code>78u_8ii_bnr</code> 專諸（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 專諸 | [《史記・刺客列傳》][332] | [JSON](78u_8ii_bnr.json) |
| `A` | 專諸子（本卷未名） | [《史記・吳太伯世家》][277]、[《史記・刺客列傳》][332] | [JSON](78u_8ii_bnr_A.json) |

</details>

<details><summary><code>796_nkw_0jz</code> 張蒼父未名（張丞相列傳候選）（4 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 張蒼父未名 | [《史記・張丞相列傳》][342] | [JSON](796_nkw_0jz.json) |
| `A` | 張蒼 | [《史記・張丞相列傳》][342] | [JSON](796_nkw_0jz_A.json) |
| `AA` | 張蒼子未名（康侯） | [《史記・張丞相列傳》][342] | [JSON](796_nkw_0jz_AA.json) |
| `AAA` | 張類 | [《史記・張丞相列傳》][342] | [JSON](796_nkw_0jz_AAA.json) |

</details>

<details><summary><code>7ad_718_47c</code> 王慧龍（8 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 王慧龍 | [《魏書・刁雍 王慧龍 韓延之 袁式》][475] | [JSON](7ad_718_47c.json) |
| `A` | 王寶興 | [《魏書・刁雍 王慧龍 韓延之 袁式》][475] | [JSON](7ad_718_47c_A.json) |
| `AA` | 王瓊 | [《魏書・刁雍 王慧龍 韓延之 袁式》][475] | [JSON](7ad_718_47c_AA.json) |
| `AAA` | 王遵業 | [《魏書・刁雍 王慧龍 韓延之 袁式》][475] | [JSON](7ad_718_47c_AAA.json) |
| `AAAA` | 王松年 | [《魏書・刁雍 王慧龍 韓延之 袁式》][475] | [JSON](7ad_718_47c_AAAA.json) |
| `AAB` | 王瓊長女〔入嬪，未名〕 | [《魏書・刁雍 王慧龍 韓延之 袁式》][475] | [JSON](7ad_718_47c_AAB.json) |
| `AAC` | 王瓊女〔盧道亮妻，未名〕 | [《魏書・刁雍 王慧龍 韓延之 袁式》][475] | [JSON](7ad_718_47c_AAC.json) |
| `B` | 王慧龍女〔未名〕 | [《魏書・刁雍 王慧龍 韓延之 袁式》][475] | [JSON](7ad_718_47c_B.json) |

</details>

<details><summary><code>7b9_110_008</code> 韋端（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 韋端 | [《三國志・二荀賈傳》][254] | [JSON](7b9_110_008.json) |
| `A` | 韋康 | [《三國志・二荀賈傳》][254] | [JSON](7b9_110_008_A.json) |

</details>

<details><summary><code>7du_pfa_2s5</code> 蹇叔（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 蹇叔 | [《史記・秦本紀》][269] | [JSON](7du_pfa_2s5.json) |
| `A` | 西乞術 | [《史記・秦本紀》][269]、[《史記・晉世家》][285] | [JSON](7du_pfa_2s5_A.json) |
| `B` | 白乙丙 | [《史記・秦本紀》][269]、[《史記・晉世家》][285] | [JSON](7du_pfa_2s5_B.json) |

</details>

<details><summary><code>7dv_lqp_y4z</code> 靳歙（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 靳歙 | [《漢書・樊酈滕灌傅靳周傳》][24] | [JSON](7dv_lqp_y4z.json) |
| `A` | 靳亭 | [《史記・高祖功臣侯者年表》][499] | [JSON](7dv_lqp_y4z_A.json) |

</details>

<details><summary><code>7hw_8jq_c1e</code> 楊暉〔鈞祖，弘農簡公原記〕（7 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 楊暉〔鈞祖，弘農簡公原記〕 | [《魏書・楊播》][478] | [JSON](7hw_8jq_c1e.json) |
| `A` | 楊恩〔鈞父〕 | [《魏書・楊播》][478] | [JSON](7hw_8jq_c1e_A.json) |
| `AA` | 楊鈞〔恒州刺史〕 | [《魏書・楊播》][478] | [JSON](7hw_8jq_c1e_AA.json) |
| `AAA` | 楊暄〔鈞長子〕 | [《魏書・楊播》][478] | [JSON](7hw_8jq_c1e_AAA.json) |
| `AAB` | 楊穆〔暄弟〕 | [《魏書・楊播》][478] | [JSON](7hw_8jq_c1e_AAB.json) |
| `AAC` | 楊儉〔穆弟〕 | [《魏書・楊播》][478] | [JSON](7hw_8jq_c1e_AAC.json) |
| `AAD` | 楊寬〔儉弟〕 | [《魏書・楊播》][478] | [JSON](7hw_8jq_c1e_AAD.json) |

</details>

<details><summary><code>7mz_d13_9ka</code> 田氏（外戚世家候選）（4 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 田氏 | [《史記・外戚世家》][295] | [JSON](7mz_d13_9ka.json) |
| `A` | 田蚡 | [《史記・魏其武安列傳》][353] | [JSON](7mz_d13_9ka_A.json) |
| `AA` | 恬（田蚡子） | [《史記・魏其武安列傳》][353] | [JSON](7mz_d13_9ka_AA.json) |
| `B` | 勝 | [《史記・外戚世家》][295]、[《史記・魏其武安列傳》][353] | [JSON](7mz_d13_9ka_B.json) |

</details>

<details><summary><code>7r6_k52_qji</code> 王仁（132 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 王仁 | [《晉書・王祥 鄭沖 何曾 石苞》][64] | [JSON](7r6_k52_qji.json) |
| `A` | 王融 | [《晉書・王祥 鄭沖 何曾 石苞》][64] | [JSON](7r6_k52_qji_A.json) |
| `AA` | 王祥 | [《晉書・王祥 鄭沖 何曾 石苞》][64] | [JSON](7r6_k52_qji_AA.json) |
| `AAA` | 王肇 | [《晉書・王祥 鄭沖 何曾 石苞》][64] | [JSON](7r6_k52_qji_AAA.json) |
| `AAAA` | 王俊 | [《晉書・王祥 鄭沖 何曾 石苞》][64] | [JSON](7r6_k52_qji_AAAA.json) |
| `AAAAA` | 王遐 | [《晉書・王祥 鄭沖 何曾 石苞》][64] | [JSON](7r6_k52_qji_AAAAA.json) |
| `AAB` | 王夏 | [《晉書・王祥 鄭沖 何曾 石苞》][64] | [JSON](7r6_k52_qji_AAB.json) |
| `AAC` | 王馥 | [《晉書・王祥 鄭沖 何曾 石苞》][64] | [JSON](7r6_k52_qji_AAC.json) |
| `AACA` | 王根 | [《晉書・王祥 鄭沖 何曾 石苞》][64] | [JSON](7r6_k52_qji_AACA.json) |
| `AAD` | 王烈 | [《晉書・王祥 鄭沖 何曾 石苞》][64] | [JSON](7r6_k52_qji_AAD.json) |
| `AAE` | 王芬 | [《晉書・王祥 鄭沖 何曾 石苞》][64] | [JSON](7r6_k52_qji_AAE.json) |
| `AB` | 王覽 | [《晉書・王祥 鄭沖 何曾 石苞》][64] | [JSON](7r6_k52_qji_AB.json) |
| `ABA` | 王裁 | [《晉書・王祥 鄭沖 何曾 石苞》][64] | [JSON](7r6_k52_qji_ABA.json) |
| `ABAA` | 王導 | [《晉書・王導》][82] | [JSON](7r6_k52_qji_ABAA.json) |
| `ABAAA` | 王洽 | [《晉書・王導》][82] | [JSON](7r6_k52_qji_ABAAA.json) |
| `ABAAAA` | 王珣 | [《晉書・王導》][82] | [JSON](7r6_k52_qji_ABAAAA.json) |
| `ABAAAAA` | 王弘 | [《宋書・劉穆之 王弘》][424] | [JSON](7r6_k52_qji_ABAAAAA.json) |
| `ABAAAAAA` | 王錫 | [《宋書・王僧達 顏竣》][452] | [JSON](7r6_k52_qji_ABAAAAAA.json) |
| `ABAAAAAAA` | 王僧亮 | [《南史・王弘》][210] | [JSON](7r6_k52_qji_ABAAAAAAA.json) |
| `ABAAAAAAB` | 王僧衍 | [《南史・王弘》][201]、[《南史・王弘》][210] | [JSON](7r6_k52_qji_ABAAAAAAB.json) |
| `ABAAAAAABA` | 王茂璋 | [《南史・王弘》][201] | [JSON](7r6_k52_qji_ABAAAAAABA.json) |
| `ABAAAAAABAA` | 王沖〔字長深〕 | [《南史・王弘》][201] | [JSON](7r6_k52_qji_ABAAAAAABAA.json) |
| `ABAAAAAABAAA` | 王瑒 | [《南史・王弘》][211] | [JSON](7r6_k52_qji_ABAAAAAABAAA.json) |
| `ABAAAAAABAAB` | 王瑜〔陳使齊者〕 | [《南史・王弘》][212] | [JSON](7r6_k52_qji_ABAAAAAABAAB.json) |
| `ABAAAAAB` | 王僧達 | [《宋書・王僧達 顏竣》][452] | [JSON](7r6_k52_qji_ABAAAAAB.json) |
| `ABAAAAABA` | 王道琰 | [《南史・王弘》][202]、[《宋書・王僧達 顏竣》][452] | [JSON](7r6_k52_qji_ABAAAAABA.json) |
| `ABAAAAB` | 王虞 | [《南史・王弘》][203] | [JSON](7r6_k52_qji_ABAAAAB.json) |
| `ABAAAABA` | 王深 | [《南史・王弘》][203] | [JSON](7r6_k52_qji_ABAAAABA.json) |
| `ABAAAAC` | 王柳 | [《南史・王弘》][203]、[《南史・王弘》][214]、[《宋書・劉穆之 王弘》][424] | [JSON](7r6_k52_qji_ABAAAAC.json) |
| `ABAAAACA` | 王猷（字世倫） | [《南史・王弘》][214] | [JSON](7r6_k52_qji_ABAAAACA.json) |
| `ABAAAACAA` | 王瞻 | [《梁書・王瞻 王志 王峻 王暕 子訓 王泰 王份 孫鍚 僉 張充 柳惲 蔡撙 江蒨》][126]、[《梁書・王瞻 王志 王峻 王暕 子訓 王泰 王份 孫鍚 僉 張充 柳惲 蔡撙 江蒨》][125] | [JSON](7r6_k52_qji_ABAAAACAA.json) |
| `ABAAAACAAA` | 王長玄 | [《梁書・王瞻 王志 王峻 王暕 子訓 王泰 王份 孫鍚 僉 張充 柳惲 蔡撙 江蒨》][126]、[《梁書・王瞻 王志 王峻 王暕 子訓 王泰 王份 孫鍚 僉 張充 柳惲 蔡撙 江蒨》][125]、[《南史・王弘》][214] | [JSON](7r6_k52_qji_ABAAAACAAA.json) |
| `ABAAAAD` | 王孺 | [《南史・王弘》][203]、[《宋書・劉穆之 王弘》][424] | [JSON](7r6_k52_qji_ABAAAAD.json) |
| `ABAAAADA` | 王微 | [《宋書・羊欣 張敷 王微》][442] | [JSON](7r6_k52_qji_ABAAAADA.json) |
| `ABAAAAE` | 王曇首 | [《宋書・王華 王曇首 殷景仁 沈演之》][443] | [JSON](7r6_k52_qji_ABAAAAE.json) |
| `ABAAAAEA` | 王僧綽 | [《宋書・徐湛之 江湛 王僧綽》][451] | [JSON](7r6_k52_qji_ABAAAAEA.json) |
| `ABAAAAEAA` | 王儉 | [《南史・王曇首》][222] | [JSON](7r6_k52_qji_ABAAAAEAA.json) |
| `ABAAAAEAAA` | 王騫 | [《南史・王曇首》][223] | [JSON](7r6_k52_qji_ABAAAAEAAA.json) |
| `ABAAAAEAAAA` | 王規 | [《南史・王曇首》][219] | [JSON](7r6_k52_qji_ABAAAAEAAAA.json) |
| `ABAAAAEAAAAA` | 王褒 | [《舊唐書・列傳第三十九: 狄仁傑 王方慶 姚璹》][113]、[《梁書・王規 劉瑴 宗懍 王承 褚翔 蕭介 從父兄洽 褚球 劉孺 弟覽 遵 劉潛 弟孝勝 孝威 孝先 殷芸 蕭幾》][135]、[《周書・列傳第33 王襃 庾信》][486] | [JSON](7r6_k52_qji_ABAAAAEAAAAA.json) |
| `ABAAAAEAAAAAA` | 王鼒 | [《舊唐書・列傳第三十九: 狄仁傑 王方慶 姚璹》][113]、[《周書・列傳第33 王襃 庾信》][486] | [JSON](7r6_k52_qji_ABAAAAEAAAAAA.json) |
| `ABAAAAEAAAAAAA` | 王弘直 | [《舊唐書・列傳第三十九: 狄仁傑 王方慶 姚璹》][113]、[《新唐書・王綝　韋思謙　陸元方　王及善　李日知　杜景佺　李懷遠》][484] | [JSON](7r6_k52_qji_ABAAAAEAAAAAAA.json) |
| `ABAAAAEAAAAAAAA` | 王方慶 | [《舊唐書・列傳第三十九: 狄仁傑 王方慶 姚璹》][113]、[《新唐書・王綝　韋思謙　陸元方　王及善　李日知　杜景佺　李懷遠》][484] | [JSON](7r6_k52_qji_ABAAAAEAAAAAAAA.json) |
| `ABAAAAEAAAAAAAAA` | 王光輔 | [《舊唐書・列傳第三十九: 狄仁傑 王方慶 姚璹》][113] | [JSON](7r6_k52_qji_ABAAAAEAAAAAAAAA.json) |
| `ABAAAAEAAAAAAAAB` | 王晙 | [《舊唐書・列傳第三十九: 狄仁傑 王方慶 姚璹》][113] | [JSON](7r6_k52_qji_ABAAAAEAAAAAAAAB.json) |
| `ABAAAAEAAB` | 王暕（字思晦） | [《南史・王曇首》][221] | [JSON](7r6_k52_qji_ABAAAAEAAB.json) |
| `ABAAAAEAABA` | 王承（字安期，王暕子） | [《南史・王曇首》][217] | [JSON](7r6_k52_qji_ABAAAAEAABA.json) |
| `ABAAAAEAABB` | 王幼（王承弟） | [《梁書・王瞻 王志 王峻 王暕 子訓 王泰 王份 孫鍚 僉 張充 柳惲 蔡撙 江蒨》][123]、[《南史・王曇首》][217]、[《南史・王曇首》][221] | [JSON](7r6_k52_qji_ABAAAAEAABB.json) |
| `ABAAAAEAABC` | 王訓（字懷範） | [《南史・王曇首》][229] | [JSON](7r6_k52_qji_ABAAAAEAABC.json) |
| `ABAAAAEAABD` | 王訏（王暕子） | [《梁書・王瞻 王志 王峻 王暕 子訓 王泰 王份 孫鍚 僉 張充 柳惲 蔡撙 江蒨》][123] | [JSON](7r6_k52_qji_ABAAAAEAABD.json) |
| `ABAAAAEAB` | 王遜 | [《南齊書・褚淵 淵弟澄 徐嗣 王儉》][146]、[《南史・王曇首》][222] | [JSON](7r6_k52_qji_ABAAAAEAB.json) |
| `ABAAAAEB` | 王僧虔 | [《南齊書・王僧虔 張緒》][151] | [JSON](7r6_k52_qji_ABAAAAEB.json) |
| `ABAAAAEBA` | 王慈 | [《南史・王曇首》][218] | [JSON](7r6_k52_qji_ABAAAAEBA.json) |
| `ABAAAAEBAA` | 王泰（字仲通） | [《南史・王曇首》][226] | [JSON](7r6_k52_qji_ABAAAAEBAA.json) |
| `ABAAAAEBAAA` | 王廓（王泰子） | [《南史・王曇首》][226] | [JSON](7r6_k52_qji_ABAAAAEBAAA.json) |
| `ABAAAAEBAB` | 王觀（王慈子） | [《南史・王曇首》][218] | [JSON](7r6_k52_qji_ABAAAAEBAB.json) |
| `ABAAAAEBAC` | 王慈女（江夏王鋒妃） | — | [JSON](7r6_k52_qji_ABAAAAEBAC.json) |
| `ABAAAAEBB` | 王寂 | [《南齊書・王僧虔 張緒》][151] | [JSON](7r6_k52_qji_ABAAAAEBB.json) |
| `ABAAAAEBC` | 王志 | [《南史・王曇首》][234] | [JSON](7r6_k52_qji_ABAAAAEBC.json) |
| `ABAAAAEBCA` | 王緝 | [《梁書・王瞻 王志 王峻 王暕 子訓 王泰 王份 孫鍚 僉 張充 柳惲 蔡撙 江蒨》][128]、[《梁書・王瞻 王志 王峻 王暕 子訓 王泰 王份 孫鍚 僉 張充 柳惲 蔡撙 江蒨》][127]、[《南史・王曇首》][234]、[《南史・王曇首》][233] | [JSON](7r6_k52_qji_ABAAAAEBCA.json) |
| `ABAAAAEBCB` | 王休 | [《梁書・王瞻 王志 王峻 王暕 子訓 王泰 王份 孫鍚 僉 張充 柳惲 蔡撙 江蒨》][128]、[《梁書・王瞻 王志 王峻 王暕 子訓 王泰 王份 孫鍚 僉 張充 柳惲 蔡撙 江蒨》][127]、[《南史・王曇首》][234]、[《南史・王曇首》][233] | [JSON](7r6_k52_qji_ABAAAAEBCB.json) |
| `ABAAAAEBCC` | 王諲 | [《梁書・王瞻 王志 王峻 王暕 子訓 王泰 王份 孫鍚 僉 張充 柳惲 蔡撙 江蒨》][128]、[《梁書・王瞻 王志 王峻 王暕 子訓 王泰 王份 孫鍚 僉 張充 柳惲 蔡撙 江蒨》][127]、[《南史・謝晦　謝裕　謝方明　謝靈運》][194]、[《南史・王曇首》][234]、[《南史・王曇首》][233] | [JSON](7r6_k52_qji_ABAAAAEBCC.json) |
| `ABAAAAEBCD` | 王操 | [《梁書・王瞻 王志 王峻 王暕 子訓 王泰 王份 孫鍚 僉 張充 柳惲 蔡撙 江蒨》][128]、[《梁書・王瞻 王志 王峻 王暕 子訓 王泰 王份 孫鍚 僉 張充 柳惲 蔡撙 江蒨》][127]、[《南史・王曇首》][234]、[《南史・王曇首》][233] | [JSON](7r6_k52_qji_ABAAAAEBCD.json) |
| `ABAAAAEBCE` | 王素 | [《梁書・王瞻 王志 王峻 王暕 子訓 王泰 王份 孫鍚 僉 張充 柳惲 蔡撙 江蒨》][128]、[《梁書・王瞻 王志 王峻 王暕 子訓 王泰 王份 孫鍚 僉 張充 柳惲 蔡撙 江蒨》][127]、[《南史・王曇首》][234]、[《南史・王曇首》][233] | [JSON](7r6_k52_qji_ABAAAAEBCE.json) |
| `ABAAAAEBD` | 王彬（字思文） | [《南史・王曇首》][216] | [JSON](7r6_k52_qji_ABAAAAEBD.json) |
| `ABAAAB` | 王瑉 | [《晉書・王導》][82] | [JSON](7r6_k52_qji_ABAAAB.json) |
| `ABAAABA` | 王朗（王瑉子） | [《晉書・王導》][82] | [JSON](7r6_k52_qji_ABAAABA.json) |
| `ABAAABB` | 王練 | [《宋書・劉穆之 王弘》][424] | [JSON](7r6_k52_qji_ABAAABB.json) |
| `ABAAABBA` | 王釗 | [《宋書・劉穆之 王弘》][424] | [JSON](7r6_k52_qji_ABAAABBA.json) |
| `ABAAB` | 王悅 | [《晉書・王導》][82] | [JSON](7r6_k52_qji_ABAAB.json) |
| `ABAAC` | 王恬 | [《晉書・王導》][82] | [JSON](7r6_k52_qji_ABAAC.json) |
| `ABAACA` | 王琨 | [《世說新語・排調》][411] | [JSON](7r6_k52_qji_ABAACA.json) |
| `ABAACAA` | 王嘏 | [《晉書・王導》][82]、[《晉書・叛臣二》][110] | [JSON](7r6_k52_qji_ABAACAA.json) |
| `ABAACAAA` | 王恢（王嘏子） | [《晉書・王導》][82] | [JSON](7r6_k52_qji_ABAACAAA.json) |
| `ABAAD` | 王協 | [《晉書・王導》][82] | [JSON](7r6_k52_qji_ABAAD.json) |
| `ABAAE` | 王邵 | [《晉書・王導》][82] | [JSON](7r6_k52_qji_ABAAE.json) |
| `ABAAED` | 王穆（王劭子） | [《晉書・王導》][82] | [JSON](7r6_k52_qji_ABAAED.json) |
| `ABAAEDA` | 王簡 | [《晉書・王導》][82] | [JSON](7r6_k52_qji_ABAAEDA.json) |
| `ABAAEDB` | 王智 | [《晉書・王導》][82] | [JSON](7r6_k52_qji_ABAAEDB.json) |
| `ABAAEDC` | 王超 | [《晉書・王導》][82] | [JSON](7r6_k52_qji_ABAAEDC.json) |
| `ABAAEE` | 王默（王劭子） | [《晉書・王導》][82] | [JSON](7r6_k52_qji_ABAAEE.json) |
| `ABAAEEA` | 王鑒（王默子） | [《晉書・王導》][82] | [JSON](7r6_k52_qji_ABAAEEA.json) |
| `ABAAEEB` | 王惠 | [《南史・謝弘微》][198] | [JSON](7r6_k52_qji_ABAAEEB.json) |
| `ABAAEF` | 王恢（王劭子） | [《晉書・王導》][82] | [JSON](7r6_k52_qji_ABAAEF.json) |
| `ABAAF` | 王薈 | [《晉書・王導》][82] | [JSON](7r6_k52_qji_ABAAF.json) |
| `ABAAFA` | 王廞 | [《宋書・王華 王曇首 殷景仁 沈演之》][443] | [JSON](7r6_k52_qji_ABAAFA.json) |
| `ABAAFAA` | 王泰 | [《晉書・王導》][82]、[《南史・王誕　王華　王惠　王彧》][238]、[《宋書・王華 王曇首 殷景仁 沈演之》][443]、[《宋書・王華 王曇首 殷景仁 沈演之》][444] | [JSON](7r6_k52_qji_ABAAFAA.json) |
| `ABAAFAB` | 王華 | [《宋書・王華 王曇首 殷景仁 沈演之》][443] | [JSON](7r6_k52_qji_ABAAFAB.json) |
| `ABAAFABA` | 王嗣 | [《宋書・徐湛之 江湛 王僧綽》][451] | [JSON](7r6_k52_qji_ABAAFABA.json) |
| `ABAAFABAA` | 王長 | [《南史・王誕　王華　王惠　王彧》][240]、[《宋書・王華 王曇首 殷景仁 沈演之》][443]、[《宋書・王華 王曇首 殷景仁 沈演之》][444] | [JSON](7r6_k52_qji_ABAAFABAA.json) |
| `ABAAFAC` | 王廞女 | [《宋書・王華 王曇首 殷景仁 沈演之》][443]、[《宋書・王華 王曇首 殷景仁 沈演之》][444] | [JSON](7r6_k52_qji_ABAAFAC.json) |
| `ABAAFB` | 王懌 | [《南史・王誕　王華　王惠　王彧》][240] | [JSON](7r6_k52_qji_ABAAFB.json) |
| `ABAAFBA` | 王琨〔王懌子〕 | [《南史・王誕　王華　王惠　王彧》][240] | [JSON](7r6_k52_qji_ABAAFBA.json) |
| `ABAB` | 王穎 | [《世說新語・品藻》][402] | [JSON](7r6_k52_qji_ABAB.json) |
| `ABAC` | 王敞 | [《世說新語・品藻》][402] | [JSON](7r6_k52_qji_ABAC.json) |
| `ABB` | 王基 | [《晉書・王祥 鄭沖 何曾 石苞》][64] | [JSON](7r6_k52_qji_ABB.json) |
| `ABC` | 王會 | [《晉書・王祥 鄭沖 何曾 石苞》][64] | [JSON](7r6_k52_qji_ABC.json) |
| `ABD` | 王正 | [《晉書・王祥 鄭沖 何曾 石苞》][64] | [JSON](7r6_k52_qji_ABD.json) |
| `ABDA` | 王廙 | [《晉書・王舒 王廙 虞潭 顧眾 張闓》][96] | [JSON](7r6_k52_qji_ABDA.json) |
| `ABDAA` | 王頤之 | [《晉書・王舒 王廙 虞潭 顧眾 張闓》][96] | [JSON](7r6_k52_qji_ABDAA.json) |
| `ABDAB` | 王胡之 | [《晉書・王舒 王廙 虞潭 顧眾 張闓》][96] | [JSON](7r6_k52_qji_ABDAB.json) |
| `ABDABA` | 王茂之 | [《晉書・王舒 王廙 虞潭 顧眾 張闓》][96]、[《南史・范泰　荀伯子　徐廣　鄭鮮之　裴松之　何承天》][244]、[《宋書・鄭鮮之 裴松之 何承天》][446]、[《宋書・王敬弘 何尚之》][447] | [JSON](7r6_k52_qji_ABDABA.json) |
| `ABDABAA` | 王敬弘 | [《宋書・王敬弘 何尚之》][447] | [JSON](7r6_k52_qji_ABDABAA.json) |
| `ABDABAAA` | 王恢之 | [《宋書・王敬弘 何尚之》][447] | [JSON](7r6_k52_qji_ABDABAAA.json) |
| `ABDABAAB` | 王瓚之 | [《南史・王裕之　王鎮之　王韶之　王悅之　王准之》][241] | [JSON](7r6_k52_qji_ABDABAAB.json) |
| `ABDABAABA` | 王秀之 | [《南齊書・王秀之 王慈 蔡約 陸慧曉 顧憲之 蕭惠基》][167] | [JSON](7r6_k52_qji_ABDABAABA.json) |
| `ABDABAABAA` | 王峻 | [《南史・王裕之　王鎮之　王韶之　王悅之　王准之》][241] | [JSON](7r6_k52_qji_ABDABAABAA.json) |
| `ABDABAABAAA` | 王琮 | [《南史・王裕之　王鎮之　王韶之　王悅之　王准之》][241] | [JSON](7r6_k52_qji_ABDABAABAAA.json) |
| `ABDABAAC` | 王昇之 | [《南史・王裕之　王鎮之　王韶之　王悅之　王准之》][241]、[《宋書・王敬弘 何尚之》][447] | [JSON](7r6_k52_qji_ABDABAAC.json) |
| `ABDABAACA` | 王延之 | [《南齊書・王琨 張岱 褚炫 何戢 王延之 阮韜》][150] | [JSON](7r6_k52_qji_ABDABAACA.json) |
| `ABDABAACAA` | 王倫之 | [《南史・王裕之　王鎮之　王韶之　王悅之　王准之》][241] | [JSON](7r6_k52_qji_ABDABAACAA.json) |
| `ABDABAACAAA` | 王昕（綸之子） | [《南史・王裕之　王鎮之　王韶之　王悅之　王准之》][241] | [JSON](7r6_k52_qji_ABDABAACAAA.json) |
| `ABDABAAD` | 王敬弘女（何述之妻，未名） | [《宋書・王敬弘 何尚之》][447] | [JSON](7r6_k52_qji_ABDABAAD.json) |
| `ABDABAAE` | 王敬弘女（孔尚妻） | [《宋書・隱逸》][464] | [JSON](7r6_k52_qji_ABDABAAE.json) |
| `ABDABB` | 王和之（字興道） | [《世說新語・輕詆》][412] | [JSON](7r6_k52_qji_ABDABB.json) |
| `ABDAC` | 王耆之 | [《世說新語・賞譽》][399] | [JSON](7r6_k52_qji_ABDAC.json) |
| `ABDACA` | 王隨之 | [《南史・王裕之　王鎮之　王韶之　王悅之　王准之》][241]、[《宋書・良吏》][463] | [JSON](7r6_k52_qji_ABDACA.json) |
| `ABDACAA` | 王鎮之 | [《宋書・良吏》][463] | [JSON](7r6_k52_qji_ABDACAA.json) |
| `ABDACAAA` | 王標之 | [《南史・王裕之　王鎮之　王韶之　王悅之　王准之》][241]、[《宋書・良吏》][463] | [JSON](7r6_k52_qji_ABDACAAA.json) |
| `ABDACAB` | 王弘之 | [《宋書・隱逸》][464] | [JSON](7r6_k52_qji_ABDACAB.json) |
| `ABDACABA` | 王曇生 | [《宋書・隱逸》][464] | [JSON](7r6_k52_qji_ABDACABA.json) |
| `ABDB` | 王彬 | [《晉書・王舒 王廙 虞潭 顧眾 張闓》][93] | [JSON](7r6_k52_qji_ABDB.json) |
| `ABDBA` | 王彭之 | [《世說新語・輕詆》][413] | [JSON](7r6_k52_qji_ABDBA.json) |
| `ABDBB` | 王彪之 | [《晉書・王舒 王廙 虞潭 顧眾 張闓》][92] | [JSON](7r6_k52_qji_ABDBB.json) |
| `ABDBBA` | 王越之 | [《晉書・王舒 王廙 虞潭 顧眾 張闓》][92] | [JSON](7r6_k52_qji_ABDBBA.json) |
| `ABDBBB` | 王臨之 | [《晉書・王舒 王廙 虞潭 顧眾 張闓》][92] | [JSON](7r6_k52_qji_ABDBBB.json) |
| `ABDBC` | 興之〔本誌贛令〕 | [《王閩之墓誌・全文》][14] | [JSON](7r6_k52_qji_ABDBC.json) |
| `ABDBCA` | 王閩之 | [《王閩之墓誌・全文》][14] | [JSON](7r6_k52_qji_ABDBCA.json) |
| `ABE` | 王彥 | [《晉書・王祥 鄭沖 何曾 石苞》][64] | [JSON](7r6_k52_qji_ABE.json) |
| `ABF` | 王琛 | [《晉書・王祥 鄭沖 何曾 石苞》][64] | [JSON](7r6_k52_qji_ABF.json) |
| `ABFA` | 王棱 | [《晉書・王舒 王廙 虞潭 顧眾 張闓》][94] | [JSON](7r6_k52_qji_ABFA.json) |
| `ABFB` | 王侃 | [《晉書・王舒 王廙 虞潭 顧眾 張闓》][94] | [JSON](7r6_k52_qji_ABFB.json) |

</details>

<details><summary><code>7s2_h0m_msl</code> 蘇（曹戴伯）（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 蘇（曹戴伯） | [《史記・管蔡世家》][281] | [JSON](7s2_h0m_msl.json) |
| `A` | 兕（曹惠伯） | [《史記・管蔡世家》][281] | [JSON](7s2_h0m_msl_A.json) |
| `AA` | 石甫（曹惠伯子） | [《史記・管蔡世家》][281] | [JSON](7s2_h0m_msl_AA.json) |

</details>

<details><summary><code>7tm_3ss_4on</code> 周苛（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 周苛 | [《史記・張丞相列傳》][342] | [JSON](7tm_3ss_4on.json) |
| `*A` | 平（周苛孫） | [《史記・孝景本紀》][275] | [JSON](7tm_3ss_4on_%2AA.json) |
| `A` | 周成 | [《史記・張丞相列傳》][342] | [JSON](7tm_3ss_4on_A.json) |

</details>

<details><summary><code>7uk_oqn_ymk</code> 陳宣公杵臼（田世家候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 陳宣公杵臼 | [《史記・田敬仲完世家》][292] | [JSON](7uk_oqn_ymk.json) |
| `A` | 御寇 | [《史記・田敬仲完世家》][292] | [JSON](7uk_oqn_ymk_A.json) |

</details>

<details><summary><code>866_0fd_205</code> 劉表（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 劉表 | [《三國志・二荀賈傳》][254] | [JSON](866_0fd_205.json) |
| `A` | 劉脩 | [《三國志・任城陳蕭王傳》][258] | [JSON](866_0fd_205_A.json) |
| `B` | 劉琮 | [《三國志・二荀賈傳》][254] | [JSON](866_0fd_205_B.json) |

</details>

<details><summary><code>89c_afa_3eb</code> 單固父伯龍（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 單固父伯龍 | [《三國志・王毌丘諸葛鄧鍾傳》][263] | [JSON](89c_afa_3eb.json) |
| `A` | 單固 | [《三國志・王毌丘諸葛鄧鍾傳》][263] | [JSON](89c_afa_3eb_A.json) |

</details>

<details><summary><code>8e8_ca8_29d</code> 王佑（4 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 王佑 | [《晉書・王湛 荀崧 范汪 劉惔 張憑 韓伯》][88] | [JSON](8e8_ca8_29d.json) |
| `A` | 王嶠 | [《晉書・王湛 荀崧 范汪 劉惔 張憑 韓伯》][88] | [JSON](8e8_ca8_29d_A.json) |
| `AA` | 王淡 | [《晉書・王湛 荀崧 范汪 劉惔 張憑 韓伯》][88] | [JSON](8e8_ca8_29d_AA.json) |
| `AAA` | 王度世 | [《晉書・王湛 荀崧 范汪 劉惔 張憑 韓伯》][88] | [JSON](8e8_ca8_29d_AAA.json) |

</details>

<details><summary><code>8im_m5e_cpy</code> 甘茂（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 甘茂 | [《史記・樗里子甘茂列傳》][317] | [JSON](8im_m5e_cpy.json) |
| `*A` | 甘羅 | [《史記・樗里子甘茂列傳》][317] | [JSON](8im_m5e_cpy_%2AA.json) |

</details>

<details><summary><code>8rw_c97_jpz</code> 梁伯（晉惠公外家）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 梁伯（晉惠公外家） | [《史記・晉世家》][285] | [JSON](8rw_c97_jpz.json) |
| `A` | 梁伯女（圉母） | [《史記・晉世家》][285] | [JSON](8rw_c97_jpz_A.json) |

</details>

<details><summary><code>8uz_r1g_a0f</code> 溫恕（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 溫恕 | [《三國志・劉司馬梁張溫賈傳》][257] | [JSON](8uz_r1g_a0f.json) |
| `A` | 溫恢 | [《三國志・劉司馬梁張溫賈傳》][257] | [JSON](8uz_r1g_a0f_A.json) |
| `AA` | 溫生 | [《三國志・劉司馬梁張溫賈傳》][257] | [JSON](8uz_r1g_a0f_AA.json) |

</details>

<details><summary><code>8xz_mlj_r3c</code> 韓千秋（南越列傳候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 韓千秋 | [《史記・南越列傳》][359] | [JSON](8xz_mlj_r3c.json) |
| `A` | 延年 | [《史記・建元以來侯者年表》][501] | [JSON](8xz_mlj_r3c_A.json) |

</details>

<details><summary><code>932_46f_026</code> 明帝（魏，荀勖引古）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 明帝（魏，荀勖引古） | [《三國志・諸夏侯曹傳》][252] | [JSON](932_46f_026.json) |
| `A` | 淑（平原懿公主） | [《三國志・桓二陳徐衞盧傳》][259] | [JSON](932_46f_026_A.json) |

</details>

<details><summary><code>98i_dd4_aof</code> 多同（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 多同 | [《史記・西南夷列傳》][362] | [JSON](98i_dd4_aof.json) |
| `A` | 多同子 | [《史記・西南夷列傳》][362] | [JSON](98i_dd4_aof_A.json) |

</details>

<details><summary><code>98q_mll_d6v</code> 蕭道生（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 蕭道生 | [《南齊書・明帝》][140]、[《南齊書・宗室》][165]、[《南齊書・宗室》][166] | [JSON](98q_mll_d6v.json) |
| `A` | 蕭鳳 | [《南齊書・宗室》][165]、[《南齊書・宗室》][166] | [JSON](98q_mll_d6v_A.json) |
| `AA` | 蕭遙光 | [《南齊書・王融 謝朓》][168] | [JSON](98q_mll_d6v_AA.json) |

</details>

<details><summary><code>995_xas_r98</code> 申（蔡昭侯）（6 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 申（蔡昭侯） | [《史記・管蔡世家》][281] | [JSON](995_xas_r98.json) |
| `A` | 朔（蔡成侯） | [《史記・管蔡世家》][281] | [JSON](995_xas_r98_A.json) |
| `AA` | 產（蔡聲侯） | [《史記・管蔡世家》][281]、[《史記・六國年表》][496] | [JSON](995_xas_r98_AA.json) |
| `AAA` | 元侯（蔡君） | [《史記・管蔡世家》][281] | [JSON](995_xas_r98_AAA.json) |
| `AAAA` | 齊（蔡末侯） | [《史記・管蔡世家》][281] | [JSON](995_xas_r98_AAAA.json) |
| `B` | 蔡昭侯質吳子（未名） | [《史記・管蔡世家》][281] | [JSON](995_xas_r98_B.json) |

</details>

<details><summary><code>9c5_a31_807</code> 武沈（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 武沈 | [《晉書・庾亮》][85] | [JSON](9c5_a31_807.json) |
| `A` | 武遵 | [《晉書・庾亮》][85] | [JSON](9c5_a31_807_A.json) |

</details>

<details><summary><code>9fa_127_a71</code> 務勿塵（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 務勿塵 | [《晉書・王沈 荀顗 荀勖 馮紞》][68] | [JSON](9fa_127_a71.json) |
| `A` | 疾陸眷 | [《晉書・王沈 荀顗 荀勖 馮紞》][68] | [JSON](9fa_127_a71_A.json) |

</details>

<details><summary><code>9nr_qwg_vuf</code> 叔孫宣伯（魯）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 叔孫宣伯（魯） | [《史記・齊太公世家》][278] | [JSON](9nr_qwg_vuf.json) |
| `A` | 景公母（叔孫宣伯女） | [《史記・齊太公世家》][278] | [JSON](9nr_qwg_vuf_A.json) |

</details>

<details><summary><code>9oa_4bh_lmd</code> 鄭伯（楚莊王圍鄭時）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 鄭伯（楚莊王圍鄭時） | [《史記・鄭世家》][288] | [JSON](9oa_4bh_lmd.json) |
| `A` | 沸 | [《史記・鄭世家》][288] | [JSON](9oa_4bh_lmd_A.json) |

</details>

<details><summary><code>9w2_c77_53m</code> 齊桓公（12 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 齊桓公 | [《史記・齊太公世家》][278] | [JSON](9w2_c77_53m.json) |
| `A` | 元（齊惠公） | [《史記・齊太公世家》][278] | [JSON](9w2_c77_53m_A.json) |
| `AA` | 無野（齊頃公） | [《史記・齊太公世家》][278] | [JSON](9w2_c77_53m_AA.json) |
| `AAA` | 環（齊靈公） | [《史記・齊太公世家》][278] | [JSON](9w2_c77_53m_AAA.json) |
| `AAAA` | 齊莊公（崔杼時） | [《史記・齊太公世家》][278] | [JSON](9w2_c77_53m_AAAA.json) |
| `B` | 無詭（齊桓公子） | [《史記・齊太公世家》][278] | [JSON](9w2_c77_53m_B.json) |
| `C` | 昭（齊孝公） | [《史記・齊太公世家》][278] | [JSON](9w2_c77_53m_C.json) |
| `D` | 潘（齊昭公） | [《史記・齊太公世家》][278] | [JSON](9w2_c77_53m_D.json) |
| `DA` | 舍（齊昭公子） | [《史記・齊太公世家》][278] | [JSON](9w2_c77_53m_DA.json) |
| `E` | 商人（齊懿公） | [《史記・齊太公世家》][278] | [JSON](9w2_c77_53m_E.json) |
| `F` | 雍（齊桓公子） | [《史記・齊太公世家》][278]、[《史記・楚世家》][286] | [JSON](9w2_c77_53m_F.json) |
| `G` | 齊姜（申生母） | [《史記・晉世家》][285] | [JSON](9w2_c77_53m_G.json) |

</details>

<details><summary><code>9w8_tqh_ysn</code> 陳寔（17 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 陳寔 | [《後漢書・荀韓鍾陳列傳》][33] | [JSON](9w8_tqh_ysn.json) |
| `A` | 紀（陳羣父） | [《後漢書・荀韓鍾陳列傳》][33]、[《三國志・桓二陳徐衞盧傳》][259] | [JSON](9w8_tqh_ysn_A.json) |
| `AA` | 陳群 | [《三國志・桓二陳徐衞盧傳》][259] | [JSON](9w8_tqh_ysn_AA.json) |
| `AAA` | 陳泰 | [《三國志・桓二陳徐衞盧傳》][259] | [JSON](9w8_tqh_ysn_AAA.json) |
| `AAAA` | 恂（陳泰子） | [《三國志・桓二陳徐衞盧傳》][259] | [JSON](9w8_tqh_ysn_AAAA.json) |
| `AAB` | 陳羣未名另封子 | [《三國志・桓二陳徐衞盧傳》][259] | [JSON](9w8_tqh_ysn_AAB.json) |
| `B` | 諶（陳羣叔父） | [《三國志・桓二陳徐衞盧傳》][259] | [JSON](9w8_tqh_ysn_B.json) |
| `B*A` | 佐（陳諶孫）（來源候選；預設不接父系） | [《三國志・桓二陳徐衞盧傳》][259] | [JSON](9w8_tqh_ysn_B%2AA.json) |
| `B*AA` | 凖（陳佐子） | [《新唐書・宰相世系一下》][483] | [JSON](9w8_tqh_ysn_B%2AAA.json) |
| `B*AA*A` | 逵（字林道） | [《三國志・桓二陳徐衞盧傳》][259] | [JSON](9w8_tqh_ysn_B%2AAA%2AA.json) |
| `B*AB` | 戴（凖弟） | [《三國志・桓二陳徐衞盧傳》][259] | [JSON](9w8_tqh_ysn_B%2AAB.json) |
| `B*AC` | 徵（凖弟） | [《三國志・桓二陳徐衞盧傳》][259] | [JSON](9w8_tqh_ysn_B%2AAC.json) |
| `B*B` | 坦（陳佐弟） | [《三國志・桓二陳徐衞盧傳》][259] | [JSON](9w8_tqh_ysn_B%2AB.json) |
| `C` | 夔〔新唐陳氏序〕 | [《新唐書・宰相世系一下》][483] | [JSON](9w8_tqh_ysn_C.json) |
| `D` | 洽〔新唐陳氏序〕 | [《新唐書・宰相世系一下》][483] | [JSON](9w8_tqh_ysn_D.json) |
| `E` | 休〔新唐陳氏序〕 | [《新唐書・宰相世系一下》][483] | [JSON](9w8_tqh_ysn_E.json) |
| `F` | 光〔新唐陳氏序〕 | [《新唐書・宰相世系一下》][483] | [JSON](9w8_tqh_ysn_F.json) |

</details>

<details><summary><code>9yf_c3t_x2w</code> 衛君父引古未名（李斯列傳候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 衛君父引古未名 | [《史記・李斯列傳》][333] | [JSON](9yf_c3t_x2w.json) |
| `A` | 衛君引古未名 | [《史記・李斯列傳》][333] | [JSON](9yf_c3t_x2w_A.json) |

</details>

<details><summary><code>9zj_vf7_86a</code> 薄氏〔薄太后之父；靈文侯〕（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 薄氏〔薄太后之父；靈文侯〕 | [《史記・外戚世家》][295] | [JSON](9zj_vf7_86a.json) |
| `A` | 薄太后（孝文帝母） | [《史記・外戚世家》][295] | [JSON](9zj_vf7_86a_A.json) |

</details>

<details><summary><code>a04_d8f_416</code> 王允之（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 王允之 | [《晉書・王舒 王廙 虞潭 顧眾 張闓》][95] | [JSON](a04_d8f_416.json) |
| `A` | 王晞之 | [《晉書・王舒 王廙 虞潭 顧眾 張闓》][95] | [JSON](a04_d8f_416_A.json) |
| `AA` | 王肇之 | [《晉書・王舒 王廙 虞潭 顧眾 張闓》][95] | [JSON](a04_d8f_416_AA.json) |

</details>

<details><summary><code>a13_5fp_pek</code> 梁襄王（趙世家候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 梁襄王 | [《史記・趙世家》][289] | [JSON](a13_5fp_pek.json) |
| `A` | 嗣 | [《史記・趙世家》][289] | [JSON](a13_5fp_pek_A.json) |

</details>

<details><summary><code>a1f_f17_ccb</code> 荀衢（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 荀衢 | [《三國志・二荀賈傳》][254] | [JSON](a1f_f17_ccb.json) |
| `A` | 荀祈 | [《三國志・二荀賈傳》][254] | [JSON](a1f_f17_ccb_A.json) |

</details>

<details><summary><code>a28_f5c_105</code> 曹洪（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 曹洪 | [《三國志・二荀賈傳》][254] | [JSON](a28_f5c_105.json) |
| `A` | 曹氏（荀粲妻，曹洪女） | [《三國志・二荀賈傳》][254] | [JSON](a28_f5c_105_A.json) |

</details>

<details><summary><code>a7k_sl0_d7u</code> 金王孫（外戚世家候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 金王孫 | [《史記・外戚世家》][295] | [JSON](a7k_sl0_d7u.json) |
| `A` | 修成君 | [《史記・外戚世家》][295]、[《史記・淮南衡山列傳》][364] | [JSON](a7k_sl0_d7u_A.json) |

</details>

<details><summary><code>a8f_ec8_e74</code> 王澤（18 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 王澤 | [《三國志・徐胡二王傳》][262] | [JSON](a8f_ec8_e74.json) |
| `A` | 王昶 | [《三國志・徐胡二王傳》][262] | [JSON](a8f_ec8_e74_A.json) |
| `AA` | 王湛 | [《晉書・王湛 荀崧 范汪 劉惔 張憑 韓伯》][88] | [JSON](a8f_ec8_e74_AA.json) |
| `AAA` | 王承 | [《晉書・王湛 荀崧 范汪 劉惔 張憑 韓伯》][88] | [JSON](a8f_ec8_e74_AAA.json) |
| `AAAA` | 王述 | [《晉書・王湛 荀崧 范汪 劉惔 張憑 韓伯》][88] | [JSON](a8f_ec8_e74_AAAA.json) |
| `AAAAA` | 王坦之 | [《晉書・王湛 荀崧 范汪 劉惔 張憑 韓伯》][88] | [JSON](a8f_ec8_e74_AAAAA.json) |
| `AAAAAA` | 王愷 | [《晉書・王湛 荀崧 范汪 劉惔 張憑 韓伯》][88] | [JSON](a8f_ec8_e74_AAAAAA.json) |
| `AAAAAB` | 王愉 | [《晉書・王湛 荀崧 范汪 劉惔 張憑 韓伯》][88] | [JSON](a8f_ec8_e74_AAAAAB.json) |
| `AAAAABA` | 王綏 | [《晉書・王湛 荀崧 范汪 劉惔 張憑 韓伯》][88] | [JSON](a8f_ec8_e74_AAAAABA.json) |
| `AAAAAC` | 王國寶 | [《晉書・王湛 荀崧 范汪 劉惔 張憑 韓伯》][88] | [JSON](a8f_ec8_e74_AAAAAC.json) |
| `AAAAAD` | 王忱 | [《晉書・王湛 荀崧 范汪 劉惔 張憑 韓伯》][88] | [JSON](a8f_ec8_e74_AAAAAD.json) |
| `AB` | 王渾 | [《晉書・王渾 王濬 唐彬》][69] | [JSON](a8f_ec8_e74_AB.json) |
| `ABA` | 王尚 | [《晉書・王渾 王濬 唐彬》][69] | [JSON](a8f_ec8_e74_ABA.json) |
| `ABB` | 王濟 | [《晉書・王渾 王濬 唐彬》][69] | [JSON](a8f_ec8_e74_ABB.json) |
| `ABBA` | 王卓 | [《晉書・王渾 王濬 唐彬》][69] | [JSON](a8f_ec8_e74_ABBA.json) |
| `ABBB` | 王聿 | [《晉書・王渾 王濬 唐彬》][69] | [JSON](a8f_ec8_e74_ABBB.json) |
| `ABC` | 王澄〔王濟弟〕 | [《晉書・王渾 王濬 唐彬》][69] | [JSON](a8f_ec8_e74_ABC.json) |
| `AC` | 王深（字道冲，王昶子） | [《三國志・徐胡二王傳》][262] | [JSON](a8f_ec8_e74_AC.json) |

</details>

<details><summary><code>a9m_987_rss</code> 叔牙（莊公弟）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 叔牙（莊公弟） | [《史記・魯周公世家》][279] | [JSON](a9m_987_rss.json) |
| `A` | 叔牙子（未名） | [《史記・魯周公世家》][279] | [JSON](a9m_987_rss_A.json) |

</details>

<details><summary><code>a9v_t0d_3va</code> 晉惠公（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 晉惠公 | [《史記・晉世家》][285] | [JSON](a9v_t0d_3va.json) |
| `A` | 晉懷公 | [《史記・晉世家》][285] | [JSON](a9v_t0d_3va_A.json) |
| `B` | 妾（梁伯女所生女） | [《史記・晉世家》][285] | [JSON](a9v_t0d_3va_B.json) |

</details>

<details><summary><code>aa6_83c_juy</code> 謝裒（64 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 謝裒 | [《南史・謝晦　謝裕　謝方明　謝靈運》][191] | [JSON](aa6_83c_juy.json) |
| `A` | 謝據 | [《南史・謝晦　謝裕　謝方明　謝靈運》][191] | [JSON](aa6_83c_juy_A.json) |
| `AA` | 謝朗 | [《晉書・謝尚 謝安》][98] | [JSON](aa6_83c_juy_AA.json) |
| `AAA` | 謝重 | [《晉書・謝尚 謝安》][98] | [JSON](aa6_83c_juy_AAA.json) |
| `AAA*A` | 謝紹 | [《南史・謝晦　謝裕　謝方明　謝靈運》][191]、[《宋書・謝晦》][425]、[《宋書・謝晦》][426] | [JSON](aa6_83c_juy_AAA%2AA.json) |
| `AAA*B` | 謝世猷 | [《宋書・謝晦》][425]、[《宋書・謝晦》][426] | [JSON](aa6_83c_juy_AAA%2AB.json) |
| `AAAA` | 謝晦 | [《宋書・謝晦》][425] | [JSON](aa6_83c_juy_AAAA.json) |
| `AAAAA` | 謝世休 | [《宋書・謝晦》][425]、[《宋書・謝晦》][426] | [JSON](aa6_83c_juy_AAAAA.json) |
| `AAAAB` | 謝晦女（彭城王義康妃） | [《南史・謝晦　謝裕　謝方明　謝靈運》][191] | [JSON](aa6_83c_juy_AAAAB.json) |
| `AAAB` | 謝絢 | [《晉書・謝尚 謝安》][98]、[《南史・謝晦　謝裕　謝方明　謝靈運》][191] | [JSON](aa6_83c_juy_AAAB.json) |
| `AAABA` | 謝世基 | [《宋書・謝晦》][425]、[《宋書・謝晦》][426] | [JSON](aa6_83c_juy_AAABA.json) |
| `AAAC` | 謝氏（荀伯子妻） | [《宋書・范泰 王准之 王韶之 荀伯子》][440] | [JSON](aa6_83c_juy_AAAC.json) |
| `AAAD` | 謝瞻 | [《宋書・謝瞻 孔琳之》][435] | [JSON](aa6_83c_juy_AAAD.json) |
| `AAAE` | 㬭 | [《宋書・謝瞻 孔琳之》][435] | [JSON](aa6_83c_juy_AAAE.json) |
| `AAAEA` | 世平 | [《南史・謝晦　謝裕　謝方明　謝靈運》][191]、[《宋書・謝晦》][425]、[《宋書・謝晦》][426]、[《宋書・謝瞻 孔琳之》][435] | [JSON](aa6_83c_juy_AAAEA.json) |
| `AAAF` | 謝遯 | [《宋書・謝晦》][425]、[《宋書・謝晦》][426] | [JSON](aa6_83c_juy_AAAF.json) |
| `AB` | 謝允 | [《南史・謝晦　謝裕　謝方明　謝靈運》][195] | [JSON](aa6_83c_juy_AB.json) |
| `ABA` | 謝純 | [《南史・謝晦　謝裕　謝方明　謝靈運》][193] | [JSON](aa6_83c_juy_ABA.json) |
| `ABB` | 謝甝 | [《南史・謝晦　謝裕　謝方明　謝靈運》][193] | [JSON](aa6_83c_juy_ABB.json) |
| `ABC` | 謝述 | [《南史・謝晦　謝裕　謝方明　謝靈運》][193] | [JSON](aa6_83c_juy_ABC.json) |
| `ABCA` | 謝約 | [《南史・謝晦　謝裕　謝方明　謝靈運》][197] | [JSON](aa6_83c_juy_ABCA.json) |
| `ABCB` | 謝緯 | [《南齊書・王融 謝朓》][168]、[《南史・謝晦　謝裕　謝方明　謝靈運》][193]、[《南史・謝晦　謝裕　謝方明　謝靈運》][197] | [JSON](aa6_83c_juy_ABCB.json) |
| `ABCBA` | 謝朓 | [《南史・謝晦　謝裕　謝方明　謝靈運》][194] | [JSON](aa6_83c_juy_ABCBA.json) |
| `ABCBAA` | 謝謨 | [《南史・謝晦　謝裕　謝方明　謝靈運》][194] | [JSON](aa6_83c_juy_ABCBAA.json) |
| `B` | 謝安 | [《晉書・謝尚 謝安》][98] | [JSON](aa6_83c_juy_B.json) |
| `B*A` | 謝璞 | [《南史・謝晦　謝裕　謝方明　謝靈運》][192] | [JSON](aa6_83c_juy_B%2AA.json) |
| `BA` | 謝琰 | [《晉書・謝尚 謝安》][98] | [JSON](aa6_83c_juy_BA.json) |
| `BAA` | 謝肇 | [《晉書・謝尚 謝安》][98] | [JSON](aa6_83c_juy_BAA.json) |
| `BAB` | 謝峻 | [《晉書・謝尚 謝安》][98] | [JSON](aa6_83c_juy_BAB.json) |
| `BAC` | 謝混 | [《南史・謝弘微》][198] | [JSON](aa6_83c_juy_BAC.json) |
| `BACA` | 謝氏（殷叡妻） | [《宋書・王惠 謝弘微 王球》][437] | [JSON](aa6_83c_juy_BACA.json) |
| `BB` | 謝氏（王瑉妻） | [《晉書・謝尚 謝安》][98] | [JSON](aa6_83c_juy_BB.json) |
| `C` | 謝奕 | [《晉書・謝尚 謝安》][98] | [JSON](aa6_83c_juy_C.json) |
| `CA` | 謝康 | [《晉書・謝尚 謝安》][98] | [JSON](aa6_83c_juy_CA.json) |
| `CB` | 謝泉 | [《晉書・謝尚 謝安》][98] | [JSON](aa6_83c_juy_CB.json) |
| `CC` | 謝靖 | [《晉書・謝尚 謝安》][98] | [JSON](aa6_83c_juy_CC.json) |
| `CD` | 謝玄 | [《晉書・謝尚 謝安》][98] | [JSON](aa6_83c_juy_CD.json) |
| `CDA` | 謝瑍 | [《晉書・謝尚 謝安》][98] | [JSON](aa6_83c_juy_CDA.json) |
| `CDAA` | 謝靈運 | [《宋書・謝靈運》][448] | [JSON](aa6_83c_juy_CDAA.json) |
| `CDAAA` | 鳯（謝靈運子） | [《宋書・謝靈運》][448] | [JSON](aa6_83c_juy_CDAAA.json) |
| `CDAAB` | 謝鳳 | [《南史・謝晦　謝裕　謝方明　謝靈運》][180] | [JSON](aa6_83c_juy_CDAAB.json) |
| `CDAABA` | 謝超宗 | [《南史・謝晦　謝裕　謝方明　謝靈運》][180] | [JSON](aa6_83c_juy_CDAABA.json) |
| `CDAABAA` | 謝才卿 | [《南齊書・謝超宗 劉祥》][155]、[《南史・謝晦　謝裕　謝方明　謝靈運》][188] | [JSON](aa6_83c_juy_CDAABAA.json) |
| `CDAABAAA` | 謝藻 | [《梁書・文學下》][138]、[《南史・謝晦　謝裕　謝方明　謝靈運》][196] | [JSON](aa6_83c_juy_CDAABAAA.json) |
| `CDAABAB` | 謝幾卿 | [《南史・謝晦　謝裕　謝方明　謝靈運》][184] | [JSON](aa6_83c_juy_CDAABAB.json) |
| `CE` | 謝道韞 | [《晉書・列女》][107] | [JSON](aa6_83c_juy_CE.json) |
| `D` | 謝萬 | [《晉書・謝尚 謝安》][98] | [JSON](aa6_83c_juy_D.json) |
| `DA` | 謝氏（王珣妻） | [《晉書・謝尚 謝安》][98] | [JSON](aa6_83c_juy_DA.json) |
| `DB` | 謝韶 | [《晉書・謝尚 謝安》][98] | [JSON](aa6_83c_juy_DB.json) |
| `DBA` | 謝思 | [《南史・謝弘微》][198]、[《宋書・王惠 謝弘微 王球》][437] | [JSON](aa6_83c_juy_DBA.json) |
| `DBAA` | 謝曜 | [《南史・謝弘微》][198] | [JSON](aa6_83c_juy_DBAA.json) |
| `DBAB` | 謝弘微 | [《宋書・王惠 謝弘微 王球》][437] | [JSON](aa6_83c_juy_DBAB.json) |
| `DBABA` | 謝莊 | [《宋書・謝莊 王景文》][456] | [JSON](aa6_83c_juy_DBABA.json) |
| `DBABAA` | 謝颺 | [《南齊書・江斆 何昌㝢 謝𤅢 王思遠》][163]、[《宋書・謝莊 王景文》][456] | [JSON](aa6_83c_juy_DBABAA.json) |
| `DBABAAA` | 順帝皇后（颺女，未名） | [《宋書・謝莊 王景文》][456] | [JSON](aa6_83c_juy_DBABAAA.json) |
| `DBABAB` | 謝朏 | [《梁書・謝朏 弟子覽》][120] | [JSON](aa6_83c_juy_DBABAB.json) |
| `DBABABA` | 諼〔謝朏子〕 | [《梁書・謝朏 弟子覽》][120] | [JSON](aa6_83c_juy_DBABABA.json) |
| `DBABABB` | 篹〔謝朏次子〕 | [《梁書・謝朏 弟子覽》][120] | [JSON](aa6_83c_juy_DBABABB.json) |
| `DBABAC` | 謝𤅢〔字義潔〕 | [《南齊書・江斆 何昌㝢 謝𤅢 王思遠》][163] | [JSON](aa6_83c_juy_DBABAC.json) |
| `DBABACA` | 謝舉（字言揚） | [《梁書・王僧孺 張率 劉孝綽 王筠》][133]、[《梁書・王僧孺 張率 劉孝綽 王筠》][132]、[《南史・謝弘微》][199] | [JSON](aa6_83c_juy_DBABACA.json) |
| `DBABAD` | 顥〔謝𤅢兄，字仁悠〕 | [《南齊書・江斆 何昌㝢 謝𤅢 王思遠》][163] | [JSON](aa6_83c_juy_DBABAD.json) |
| `DBABAE` | 嵷〔謝𤅢兄〕 | [《南齊書・江斆 何昌㝢 謝𤅢 王思遠》][163] | [JSON](aa6_83c_juy_DBABAE.json) |
| `E` | 謝石 | [《晉書・謝尚 謝安》][98] | [JSON](aa6_83c_juy_E.json) |
| `EA` | 謝汪 | [《晉書・謝尚 謝安》][98] | [JSON](aa6_83c_juy_EA.json) |

</details>

<details><summary><code>aa9_7e9_5b9</code> 魯宗之（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 魯宗之 | [《晉書・桓彝》][87] | [JSON](aa9_7e9_5b9.json) |
| `A` | 魯軌 | [《魏書・刁雍 王慧龍 韓延之 袁式》][475] | [JSON](aa9_7e9_5b9_A.json) |

</details>

<details><summary><code>acg_se3_w5x</code> 周呂侯（呂后兄）（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 周呂侯（呂后兄） | [《史記・呂后本紀》][273] | [JSON](acg_se3_w5x.json) |
| `A` | 呂台 | [《史記・呂后本紀》][273] | [JSON](acg_se3_w5x_A.json) |
| `B` | 呂產 | [《史記・呂后本紀》][273] | [JSON](acg_se3_w5x_B.json) |

</details>

<details><summary><code>ae2_620_2bc</code> 袁渙（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 袁渙 | [《三國志・袁張涼國田王邴管傳》][255] | [JSON](ae2_620_2bc.json) |
| `A` | 袁㝢 | [《三國志・袁張涼國田王邴管傳》][255] | [JSON](ae2_620_2bc_A.json) |
| `B` | 袁準 | [《三國志・袁張涼國田王邴管傳》][255] | [JSON](ae2_620_2bc_B.json) |

</details>

<details><summary><code>afj_vl8_7fu</code> 安丘侯説（萬石張叔列傳候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 安丘侯説 | [《史記・萬石張叔列傳》][349] | [JSON](afj_vl8_7fu.json) |
| `A` | 張歐 | [《史記・萬石張叔列傳》][349] | [JSON](afj_vl8_7fu_A.json) |

</details>

<details><summary><code>agx_sqm_4ou</code> 張耳（5 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 張耳 | [《史記・張耳陳餘列傳》][335] | [JSON](agx_sqm_4ou.json) |
| `A` | 張敖 | [《史記・張耳陳餘列傳》][335] | [JSON](agx_sqm_4ou_A.json) |
| `AA` | 張偃 | [《史記・呂后本紀》][273]、[《史記・張耳陳餘列傳》][335] | [JSON](agx_sqm_4ou_AA.json) |
| `AB` | 張壽 | [《史記・張耳陳餘列傳》][335] | [JSON](agx_sqm_4ou_AB.json) |
| `AC` | 張侈 | [《史記・張耳陳餘列傳》][335] | [JSON](agx_sqm_4ou_AC.json) |

</details>

<details><summary><code>ao3_0fy_d45</code> 秦昭王（6 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 秦昭王 | [《史記・范睢蔡澤列傳》][325] | [JSON](ao3_0fy_d45.json) |
| `A` | 秦孝文王 | [《史記・呂不韋列傳》][331] | [JSON](ao3_0fy_d45_A.json) |
| `AA` | 秦莊襄王 | [《史記・呂不韋列傳》][331] | [JSON](ao3_0fy_d45_AA.json) |
| `AAA` | 秦始皇帝 | [《史記・秦始皇本紀》][270] | [JSON](ao3_0fy_d45_AAA.json) |
| `AAAA` | 胡亥 | [《史記・秦始皇本紀》][270] | [JSON](ao3_0fy_d45_AAAA.json) |
| `AAAB` | 扶蘇 | [《史記・李斯列傳》][333] | [JSON](ao3_0fy_d45_AAAB.json) |

</details>

<details><summary><code>apr_7dg_tdd</code> 謝方明（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 謝方明 | [《宋書・張茂度 庾登之 謝方明 江夷》][432] | [JSON](apr_7dg_tdd.json) |
| `A` | 惠連 | [《宋書・謝靈運》][448] | [JSON](apr_7dg_tdd_A.json) |

</details>

<details><summary><code>ath_xsq_n4i</code> 魯定公（11 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 魯定公 | [《史記・魯周公世家》][279] | [JSON](ath_xsq_n4i.json) |
| `A` | 魯哀公 | [《史記・魯周公世家》][279] | [JSON](ath_xsq_n4i_A.json) |
| `AA` | 寧（魯悼公） | [《史記・魯周公世家》][279] | [JSON](ath_xsq_n4i_AA.json) |
| `AAA` | 嘉（魯元公） | [《史記・魯周公世家》][279] | [JSON](ath_xsq_n4i_AAA.json) |
| `AAAA` | 顯（魯穆公） | [《史記・魯周公世家》][279] | [JSON](ath_xsq_n4i_AAAA.json) |
| `AAAAA` | 奮（魯共公） | [《史記・魯周公世家》][279] | [JSON](ath_xsq_n4i_AAAAA.json) |
| `AAAAAA` | 屯（魯康公） | [《史記・魯周公世家》][279] | [JSON](ath_xsq_n4i_AAAAAA.json) |
| `AAAAAAA` | 匽（魯景公） | [《史記・魯周公世家》][279] | [JSON](ath_xsq_n4i_AAAAAAA.json) |
| `AAAAAAAA` | 叔（魯平公） | [《史記・魯周公世家》][279] | [JSON](ath_xsq_n4i_AAAAAAAA.json) |
| `AAAAAAAAA` | 賈（魯文公） | [《史記・魯周公世家》][279] | [JSON](ath_xsq_n4i_AAAAAAAAA.json) |
| `AAAAAAAAAA` | 讎（魯頃公） | [《史記・魯周公世家》][279] | [JSON](ath_xsq_n4i_AAAAAAAAAA.json) |

</details>

<details><summary><code>b1r_inb_fts</code> 樊噲（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 樊噲 | [《史記・樊酈滕灌列傳》][341] | [JSON](b1r_inb_fts.json) |
| `A` | 樊市人 | [《史記・樊酈滕灌列傳》][341] | [JSON](b1r_inb_fts_A.json) |
| `B` | 樊伉 | [《史記・樊酈滕灌列傳》][341] | [JSON](b1r_inb_fts_B.json) |

</details>

<details><summary><code>bm8_bzq_1ee</code> 觀起（蔡大夫）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 觀起（蔡大夫） | [《史記・楚世家》][286] | [JSON](bm8_bzq_1ee.json) |
| `A` | 觀從（楚變亂謀者） | [《史記・楚世家》][286] | [JSON](bm8_bzq_1ee_A.json) |

</details>

<details><summary><code>bn4_lhp_9h1</code> 姑容（杞桓公）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 姑容（杞桓公） | [《史記・陳杞世家》][282] | [JSON](bn4_lhp_9h1.json) |
| `A` | 丐（杞孝公） | [《史記・陳杞世家》][282] | [JSON](bn4_lhp_9h1_A.json) |

</details>

<details><summary><code>buv_igi_gpn</code> 帝乙（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 帝乙 | [《史記・殷本紀》][267] | [JSON](buv_igi_gpn.json) |
| `A` | 微子啓 | [《史記・宋微子世家》][284] | [JSON](buv_igi_gpn_A.json) |

</details>

<details><summary><code>bvb_d1z_fd0</code> 尉佗（6 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 尉佗 | [《史記・南越列傳》][359] | [JSON](bvb_d1z_fd0.json) |
| `*A` | 胡 | [《史記・南越列傳》][359] | [JSON](bvb_d1z_fd0_%2AA.json) |
| `*AA` | 嬰齊 | [《史記・南越列傳》][359] | [JSON](bvb_d1z_fd0_%2AAA.json) |
| `*AAA` | 興 | [《史記・南越列傳》][359] | [JSON](bvb_d1z_fd0_%2AAAA.json) |
| `*AAB` | 次公 | [《史記・南越列傳》][359] | [JSON](bvb_d1z_fd0_%2AAAB.json) |
| `*AAC` | 建德 | [《史記・南越列傳》][359] | [JSON](bvb_d1z_fd0_%2AAAC.json) |

</details>

<details><summary><code>bwv_ob8_6xi</code> 共敖（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 共敖 | [《史記・項羽本紀》][271]、[《史記・秦楚之際月表》][497] | [JSON](bwv_ob8_6xi.json) |
| `A` | 共尉 | [《史記・荊燕世家》][297]、[《史記・秦楚之際月表》][497] | [JSON](bwv_ob8_6xi_A.json) |

</details>

<details><summary><code>c0i_eah_y59</code> 咎（韓世家釐王候選）（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 咎 | [《史記・韓世家》][291] | [JSON](c0i_eah_y59.json) |
| `A` | 桓惠王 | [《史記・韓世家》][291] | [JSON](c0i_eah_y59_A.json) |
| `AA` | 韓王安 | [《史記・韓世家》][291]、[《史記・六國年表》][496] | [JSON](c0i_eah_y59_AA.json) |

</details>

<details><summary><code>c19_xxo_r8f</code> 直不疑（萬石張叔列傳候選）（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 直不疑 | [《史記・萬石張叔列傳》][349] | [JSON](c19_xxo_r8f.json) |
| `*A` | 望（直不疑孫） | [《史記・萬石張叔列傳》][349] | [JSON](c19_xxo_r8f_%2AA.json) |
| `A` | 相如（直不疑子） | [《史記・萬石張叔列傳》][349] | [JSON](c19_xxo_r8f_A.json) |

</details>

<details><summary><code>c1t_5mz_5ia</code> 晉昭公（趙世家候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 晉昭公 | [《史記・趙世家》][289] | [JSON](c1t_5mz_5ia.json) |
| `**A` | 驕 | [《史記・趙世家》][289] | [JSON](c1t_5mz_5ia_%2A%2AA.json) |

</details>

<details><summary><code>c27_590_7e3</code> 賈充（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 賈充 | [《晉書・王沈 荀顗 荀勖 馮紞》][68] | [JSON](c27_590_7e3.json) |
| `A` | 賈充女（荀顗薦選太子妃者） | [《晉書・王沈 荀顗 荀勖 馮紞》][68] | [JSON](c27_590_7e3_A.json) |

</details>

<details><summary><code>c2w_s7g_en0</code> 楚懷王（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 楚懷王 | [《史記・楚世家》][286] | [JSON](c2w_s7g_en0.json) |
| `*A` | 楚懷王心 | [《史記・高祖本紀》][272] | [JSON](c2w_s7g_en0_%2AA.json) |
| `A` | 子蘭（楚懷王子） | [《史記・屈原賈生列傳》][330] | [JSON](c2w_s7g_en0_A.json) |

</details>

<details><summary><code>c46_2c9_597</code> 唐衡（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 唐衡 | [《三國志・二荀賈傳》][254] | [JSON](c46_2c9_597.json) |
| `A` | 唐氏（荀彧妻，唐衡女） | [《三國志・二荀賈傳》][254] | [JSON](c46_2c9_597_A.json) |

</details>

<details><summary><code>cek_1yy_pne</code> 奄父（趙世家候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 奄父 | [《史記・趙世家》][289] | [JSON](cek_1yy_pne.json) |
| `A` | 叔帶 | [《史記・趙世家》][289] | [JSON](cek_1yy_pne_A.json) |

</details>

<details><summary><code>ceq_pnr_q0e</code> 殷叡〔齊，殷鈞父〕（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 殷叡〔齊，殷鈞父〕 | [《梁書・陸倕 到洽 明山賓 殷鈞 陸襄》][130]、[《南史・謝晦　謝裕　謝方明　謝靈運》][194] | [JSON](ceq_pnr_q0e.json) |
| `A` | 殷鈞 | [《南史・王曇首》][232]、[《南史・王曇首》][231] | [JSON](ceq_pnr_q0e_A.json) |

</details>

<details><summary><code>cjd_ybv_2wu</code> 蜚廉（趙世家祖系候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 蜚廉 | [《史記・趙世家》][289] | [JSON](cjd_ybv_2wu.json) |
| `A` | 惡來 | [《史記・趙世家》][289] | [JSON](cjd_ybv_2wu_A.json) |

</details>

<details><summary><code>cti_o52_4nz</code> 宋明帝彧（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 宋明帝彧 | [《魏書・燕鳳 許謙 張衮 崔玄伯 鄧淵》][472] | [JSON](cti_o52_4nz.json) |
| `A` | 陽羨公主 | — | [JSON](cti_o52_4nz_A.json) |

</details>

<details><summary><code>d50_8f5_wul</code> 嘉〔張茂度高祖〕（19 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 嘉〔張茂度高祖〕 | [《宋書・張茂度 庾登之 謝方明 江夷》][434] | [JSON](d50_8f5_wul.json) |
| `A` | 澄〔張茂度曾祖〕 | [《宋書・張茂度 庾登之 謝方明 江夷》][434] | [JSON](d50_8f5_wul_A.json) |
| `AA` | 彭祖〔張茂度祖〕 | [《宋書・張茂度 庾登之 謝方明 江夷》][434] | [JSON](d50_8f5_wul_AA.json) |
| `AAA` | 張敞〔邵父〕 | [《宋書・趙倫之 王懿 張邵》][429] | [JSON](d50_8f5_wul_AAA.json) |
| `AAAA` | 張裕〔字茂度〕 | [《宋書・張茂度 庾登之 謝方明 江夷》][434] | [JSON](d50_8f5_wul_AAAA.json) |
| `AAAAA` | 張演〔046／053父系歧異〕 | [《宋書・張茂度 庾登之 謝方明 江夷》][434] | [JSON](d50_8f5_wul_AAAAA.json) |
| `AAAAB` | 張鏡〔046／053父系歧異〕 | [《宋書・趙倫之 王懿 張邵》][429]、[《宋書・張茂度 庾登之 謝方明 江夷》][434]、[《宋書・殷淳 張暢 何偃 江智淵》][438] | [JSON](d50_8f5_wul_AAAAB.json) |
| `AAAAC` | 張寅 | [《南齊書・王僧虔 張緒》][152]、[《南史・張裕》][243] | [JSON](d50_8f5_wul_AAAAC.json) |
| `AAAACA` | 張緒 | [《南齊書・王僧虔 張緒》][152]、[《南史・張裕》][243] | [JSON](d50_8f5_wul_AAAACA.json) |
| `AAAB` | 張褘〔059亦禕，046偉；張暢父〕 | [《宋書・殷淳 張暢 何偃 江智淵》][438] | [JSON](d50_8f5_wul_AAAB.json) |
| `AAABA` | 張暢 | [《宋書・殷淳 張暢 何偃 江智淵》][438] | [JSON](d50_8f5_wul_AAABA.json) |
| `AAABAA` | 張浩〔張暢子〕 | [《宋書・殷淳 張暢 何偃 江智淵》][438] | [JSON](d50_8f5_wul_AAABAA.json) |
| `AAABAB` | 張淹〔張暢子〕 | [《宋書・殷淳 張暢 何偃 江智淵》][438] | [JSON](d50_8f5_wul_AAABAB.json) |
| `AAABB` | 張牧〔張暢弟〕 | [《宋書・殷淳 張暢 何偃 江智淵》][438] | [JSON](d50_8f5_wul_AAABB.json) |
| `AAABC` | 張說〔046作悦〕 | [《宋書・殷淳 張暢 何偃 江智淵》][438] | [JSON](d50_8f5_wul_AAABC.json) |
| `AAAC` | 張邵 | [《宋書・趙倫之 王懿 張邵》][429] | [JSON](d50_8f5_wul_AAAC.json) |
| `AAACA` | 張敷 | [《宋書・趙倫之 王懿 張邵》][429] | [JSON](d50_8f5_wul_AAACA.json) |
| `AAACB` | 張柬〔敷弟〕 | [《宋書・趙倫之 王懿 張邵》][429] | [JSON](d50_8f5_wul_AAACB.json) |
| `AAACBA` | 張式〔柬子〕 | [《宋書・趙倫之 王懿 張邵》][429] | [JSON](d50_8f5_wul_AAACBA.json) |

</details>

<details><summary><code>d7u_bgr_wdi</code> 蟲達（史表作蠱逢）（4 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 蟲達（史表作蠱逢） | [《漢書・髙惠髙后文功臣表》曲成列][504] | [JSON](d7u_bgr_wdi.json) |
| `***A` | 宣（蟲達玄孫） | [《漢書・髙惠髙后文功臣表》曲成列][504] | [JSON](d7u_bgr_wdi_%2A%2A%2AA.json) |
| `*A` | 皇柔（史表作皋柔） | [《史記・高祖功臣侯者年表》][499] | [JSON](d7u_bgr_wdi_%2AA.json) |
| `A` | 捷（曲城侯） | [《漢書・髙惠髙后文功臣表》曲成列][504]、[《史記・高祖功臣侯者年表》][499] | [JSON](d7u_bgr_wdi_A.json) |

</details>

<details><summary><code>dad_b77_b38</code> 魏武（引古）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 魏武（引古） | [《三國志・二荀賈傳》][254] | [JSON](dad_b77_b38.json) |
| `A` | 安陽公主 | [《三國志・二荀賈傳》][254] | [JSON](dad_b77_b38_A.json) |

</details>

<details><summary><code>djo_u3b_i9w</code> 殷羨（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 殷羨 | [《晉書・陸曄 何充 褚翜 蔡謨 諸葛恢 殷浩》][97] | [JSON](djo_u3b_i9w.json) |
| `A` | 殷浩 | [《晉書・陸曄 何充 褚翜 蔡謨 諸葛恢 殷浩》][97] | [JSON](djo_u3b_i9w_A.json) |
| `AA` | 殷涓 | [《晉書・叛臣一》][109] | [JSON](djo_u3b_i9w_AA.json) |

</details>

<details><summary><code>dkn_ge4_286</code> 司馬鈞（52 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 司馬鈞 | [《晉書・高祖宣帝》][37] | [JSON](dkn_ge4_286.json) |
| `A` | 司馬量 | [《晉書・高祖宣帝》][37] | [JSON](dkn_ge4_286_A.json) |
| `AA` | 司馬儁 | [《晉書・高祖宣帝》][37] | [JSON](dkn_ge4_286_AA.json) |
| `AAA` | 司馬防 | [《晉書・高祖宣帝》][37] | [JSON](dkn_ge4_286_AAA.json) |
| `AAAA` | 司馬懿 | [《三國志・諸夏侯曹傳》][252] | [JSON](dkn_ge4_286_AAAA.json) |
| `AAAAA` | 司馬伷 | [《晉書・宣五王 文六王》][67] | [JSON](dkn_ge4_286_AAAAA.json) |
| `AAAAAA` | 司馬覲 | [《晉書・宣五王 文六王》][67] | [JSON](dkn_ge4_286_AAAAAA.json) |
| `AAAAAAA` | 晉元帝 | [《晉書・王導》][82] | [JSON](dkn_ge4_286_AAAAAAA.json) |
| `AAAAAAAA` | 晉明帝 | [《晉書・庾亮》][86] | [JSON](dkn_ge4_286_AAAAAAAA.json) |
| `AAAAAAAAA` | 晉成帝 | [《晉書・庾亮》][86] | [JSON](dkn_ge4_286_AAAAAAAAA.json) |
| `AAAAAAAB` | 琅邪孝王裒 | [《晉書・武十三王 元四王 簡文三子》][80] | [JSON](dkn_ge4_286_AAAAAAAB.json) |
| `AAAAAAABA` | 司馬安國 | [《晉書・武十三王 元四王 簡文三子》][80] | [JSON](dkn_ge4_286_AAAAAAABA.json) |
| `AAAAAAAC` | 東海哀王沖 | [《晉書・庾亮》][85] | [JSON](dkn_ge4_286_AAAAAAAC.json) |
| `AAAAAAAD` | 武陵威王晞 | [《晉書・王舒 王廙 虞潭 顧眾 張闓》][92] | [JSON](dkn_ge4_286_AAAAAAAD.json) |
| `AAAAAAAE` | 琅邪悼王煥 | [《晉書・后妃下》][63]、[《晉書・武十三王 元四王 簡文三子》][80] | [JSON](dkn_ge4_286_AAAAAAAE.json) |
| `AAAAAAAF` | 晉簡文帝 | [《晉書・叛臣一》][109] | [JSON](dkn_ge4_286_AAAAAAAF.json) |
| `AAAAAAAFA` | 司馬道子 | [《晉書・王湛 荀崧 范汪 劉惔 張憑 韓伯》][88] | [JSON](dkn_ge4_286_AAAAAAAFA.json) |
| `AAAAAAAFB` | 司馬道福 | [《太平御覽・皇親部十五》][466] | [JSON](dkn_ge4_286_AAAAAAAFB.json) |
| `AAAAAAAG` | 尋陽公主 | [《晉書・后妃下》][63] | [JSON](dkn_ge4_286_AAAAAAAG.json) |
| `AAAAAAB` | 司馬渾 | [《晉書・宣五王 文六王》][67]、[《晉書・武十三王 元四王 簡文三子》][80] | [JSON](dkn_ge4_286_AAAAAAB.json) |
| `AAAAAB` | 司馬澹 | [《晉書・孝懷帝 孝愍帝》][41]、[《晉書・宣五王 文六王》][67] | [JSON](dkn_ge4_286_AAAAAB.json) |
| `AAAAAC` | 司馬繇 | [《晉書・山濤 王戎 郭舒 樂廣》][73] | [JSON](dkn_ge4_286_AAAAAC.json) |
| `AAAAAD` | 司馬漼 | [《晉書・宣五王 文六王》][67] | [JSON](dkn_ge4_286_AAAAAD.json) |
| `AAAAB` | 司馬幹 | [《晉書・王沈 荀顗 荀勖 馮紞》][68] | [JSON](dkn_ge4_286_AAAAB.json) |
| `AAAAC` | 司馬亮 | [《晉書・汝南王亮 楚王瑋 趙王倫 齊王冏 長沙王乂 成都王潁 河間王顒 東海王越》][78] | [JSON](dkn_ge4_286_AAAAC.json) |
| `AAAACA` | 司馬粹 | [《晉書・汝南王亮 楚王瑋 趙王倫 齊王冏 長沙王乂 成都王潁 河間王顒 東海王越》][78] | [JSON](dkn_ge4_286_AAAACA.json) |
| `AAAACB` | 司馬矩 | [《晉書・汝南王亮 楚王瑋 趙王倫 齊王冏 長沙王乂 成都王潁 河間王顒 東海王越》][78] | [JSON](dkn_ge4_286_AAAACB.json) |
| `AAAACC` | 司馬羕 | [《晉書・汝南王亮 楚王瑋 趙王倫 齊王冏 長沙王乂 成都王潁 河間王顒 東海王越》][78] | [JSON](dkn_ge4_286_AAAACC.json) |
| `AAAACC*A` | 瑉（羕孫） | [《晉書・汝南王亮 楚王瑋 趙王倫 齊王冏 長沙王乂 成都王潁 河間王顒 東海王越》][78] | [JSON](dkn_ge4_286_AAAACC%2AA.json) |
| `AAAACC*B` | 崧（羕孫、生父未名） | [《晉書・汝南王亮 楚王瑋 趙王倫 齊王冏 長沙王乂 成都王潁 河間王顒 東海王越》][78]、[《資治通鑑・晉紀十六》][489] | [JSON](dkn_ge4_286_AAAACC%2AB.json) |
| `AAAACCA` | 播（羕世子） | [《晉書・汝南王亮 楚王瑋 趙王倫 齊王冏 長沙王乂 成都王潁 河間王顒 東海王越》][78] | [JSON](dkn_ge4_286_AAAACCA.json) |
| `AAAACCB` | 充（羕子、播弟） | [《晉書・汝南王亮 楚王瑋 趙王倫 齊王冏 長沙王乂 成都王潁 河間王顒 東海王越》][78]、[《資治通鑑・晉紀十六》][489] | [JSON](dkn_ge4_286_AAAACCB.json) |
| `AAAACD` | 司馬宗 | [《晉書・庾亮》][86] | [JSON](dkn_ge4_286_AAAACD.json) |
| `AAAACE` | 司馬熙 | [《晉書・汝南王亮 楚王瑋 趙王倫 齊王冏 長沙王乂 成都王潁 河間王顒 東海王越》][78] | [JSON](dkn_ge4_286_AAAACE.json) |
| `AAAAD` | 司馬京 | [《晉書・宣五王 文六王》][67] | [JSON](dkn_ge4_286_AAAAD.json) |
| `AAAAE` | 司馬駿 | [《晉書・宣五王 文六王》][67]、[《晉書・王沈 荀顗 荀勖 馮紞》][68]、[《晉書・王渾 王濬 唐彬》][69] | [JSON](dkn_ge4_286_AAAAE.json) |
| `AAAAF` | 司馬肜 | [《晉書・山濤 王戎 郭舒 樂廣》][73] | [JSON](dkn_ge4_286_AAAAF.json) |
| `AAAAG` | 司馬倫 | [《晉書・汝南王亮 楚王瑋 趙王倫 齊王冏 長沙王乂 成都王潁 河間王顒 東海王越》][76] | [JSON](dkn_ge4_286_AAAAG.json) |
| `AAAAH` | 司馬景王 | [《三國志・諸夏侯曹傳》][252] | [JSON](dkn_ge4_286_AAAAH.json) |
| `AAAAI` | 司馬文王 | [《晉書・王沈 荀顗 荀勖 馮紞》][68] | [JSON](dkn_ge4_286_AAAAI.json) |
| `AAAB` | 司馬朗 | [《晉書・高祖宣帝》][37] | [JSON](dkn_ge4_286_AAAB.json) |
| `AAAC` | 孚（安平獻王） | [《晉書・宗室》][66] | [JSON](dkn_ge4_286_AAAC.json) |
| `AAAD` | 馗（宣帝弟、權父） | [《晉書・宗室》][66] | [JSON](dkn_ge4_286_AAAD.json) |
| `AAADA` | 彭城穆王權 | [《晉書・宗室》][66] | [JSON](dkn_ge4_286_AAADA.json) |
| `AAADAA` | 彭城元王植 | [《晉書・宗室》][66] | [JSON](dkn_ge4_286_AAADAA.json) |
| `AAADAAA` | 彭城康王釋 | [《晉書・宗室》][66] | [JSON](dkn_ge4_286_AAADAAA.json) |
| `AAADAAAA` | 彭城王雄 | [《晉書・宗室》][66]、[《資治通鑑・晉紀十六》][489] | [JSON](dkn_ge4_286_AAADAAAA.json) |
| `AAADAAAB` | 紘（釋子） | [《晉書・宗室》][66] | [JSON](dkn_ge4_286_AAADAAAB.json) |
| `AAAE` | 恂（八達之一） | [《晉書・宗室》][66] | [JSON](dkn_ge4_286_AAAE.json) |
| `AAAF` | 進（八達之一） | [《晉書・宗室》][66] | [JSON](dkn_ge4_286_AAAF.json) |
| `AAAG` | 通（八達之一） | [《晉書・宗室》][66] | [JSON](dkn_ge4_286_AAAG.json) |
| `AAAH` | 敏（八達之一） | [《晉書・宗室》][66] | [JSON](dkn_ge4_286_AAAH.json) |

</details>

<details><summary><code>dm0_58v_50i</code> 趙衰（5 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 趙衰 | [《史記・晉世家》][285] | [JSON](dm0_58v_50i.json) |
| `A` | 趙盾 | [《史記・晉世家》][285] | [JSON](dm0_58v_50i_A.json) |
| `B` | 趙同 | [《史記・趙世家》][289] | [JSON](dm0_58v_50i_B.json) |
| `C` | 趙括 | [《史記・趙世家》][289] | [JSON](dm0_58v_50i_C.json) |
| `D` | 趙嬰齊 | [《史記・趙世家》][289] | [JSON](dm0_58v_50i_D.json) |

</details>

<details><summary><code>dq6_ovk_58c</code> 張釋之（張釋之馮唐列傳候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 張釋之 | [《史記・張釋之馮唐列傳》][348] | [JSON](dq6_ovk_58c.json) |
| `A` | 張摯 | [《史記・張釋之馮唐列傳》][348] | [JSON](dq6_ovk_58c_A.json) |

</details>

<details><summary><code>e00_pe1_zri</code> 無諸（東越列傳候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 無諸 | [《史記・東越列傳》][360] | [JSON](e00_pe1_zri.json) |
| `*A` | 丑 | [《史記・東越列傳》][360] | [JSON](e00_pe1_zri_%2AA.json) |

</details>

<details><summary><code>e2r_5iw_ui0</code> 劉穎之（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 劉穎之 | [《宋書・殷孝祖 劉勔》][457] | [JSON](e2r_5iw_ui0.json) |
| `A` | 劉勔 | [《宋書・薛安都 沈文秀 崔道固》][459] | [JSON](e2r_5iw_ui0_A.json) |

</details>

<details><summary><code>e5k_f2i_cog</code> 郗曇（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 郗曇 | [《晉書・謝尚 謝安》][98]、[《晉書・王羲之》][99]、[《世說新語・德行》][378] | [JSON](e5k_f2i_cog.json) |
| `A` | 郗道茂 | [《世說新語・德行》][378] | [JSON](e5k_f2i_cog_A.json) |

</details>

<details><summary><code>ea5_zvr_hlp</code> 張良（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 張良 | [《史記・留侯世家》][301] | [JSON](ea5_zvr_hlp.json) |
| `A` | 張辟彊 | [《史記・呂后本紀》][273] | [JSON](ea5_zvr_hlp_A.json) |
| `B` | 不疑 | [《史記・留侯世家》][301] | [JSON](ea5_zvr_hlp_B.json) |

</details>

<details><summary><code>ei2_qej_czn</code> 公乘氏（張耳陳餘列傳候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 公乘氏 | [《史記・張耳陳餘列傳》][335] | [JSON](ei2_qej_czn.json) |
| `A` | 陳餘妻未名 | [《史記・張耳陳餘列傳》][335] | [JSON](ei2_qej_czn_A.json) |

</details>

<details><summary><code>ei7_fai_lvy</code> 丑（鄭世家共公候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 丑 | [《史記・鄭世家》][288] | [JSON](ei7_fai_lvy.json) |
| `A` | 已 | [《史記・鄭世家》][288] | [JSON](ei7_fai_lvy_A.json) |

</details>

<details><summary><code>esh_e0a_jrw</code> 石奮父未名（萬石張叔列傳候選）（7 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 石奮父未名 | [《史記・萬石張叔列傳》][349] | [JSON](esh_e0a_jrw.json) |
| `A` | 石奮 | [《史記・萬石張叔列傳》][349] | [JSON](esh_e0a_jrw_A.json) |
| `AA` | 建（石奮長子） | [《史記・萬石張叔列傳》][349] | [JSON](esh_e0a_jrw_AA.json) |
| `AB` | 甲（石奮次子失名佔位） | [《史記・萬石張叔列傳》][349] | [JSON](esh_e0a_jrw_AB.json) |
| `AC` | 乙（石奮次子失名佔位） | [《史記・萬石張叔列傳》][349] | [JSON](esh_e0a_jrw_AC.json) |
| `AD` | 慶（石奮子） | [《史記・萬石張叔列傳》][349] | [JSON](esh_e0a_jrw_AD.json) |
| `ADA` | 德（石慶中子） | [《史記・萬石張叔列傳》][349] | [JSON](esh_e0a_jrw_ADA.json) |

</details>

<details><summary><code>eva_gs1_9n5</code> 魏文侯（趙世家候選）（7 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 魏文侯 | [《史記・趙世家》][289] | [JSON](eva_gs1_9n5.json) |
| `A` | 撃 | [《史記・魏世家》][290] | [JSON](eva_gs1_9n5_A.json) |
| `AA` | 罃 | [《史記・魏世家》][290] | [JSON](eva_gs1_9n5_AA.json) |
| `AAA` | 襄王 | [《史記・魏世家》][290] | [JSON](eva_gs1_9n5_AAA.json) |
| `AAAA` | 哀王 | [《史記・魏世家》][290] | [JSON](eva_gs1_9n5_AAAA.json) |
| `AAAAA` | 昭王 | [《史記・魏世家》][290] | [JSON](eva_gs1_9n5_AAAAA.json) |
| `AAAAAA` | 安釐王 | [《史記・魏公子列傳》][323] | [JSON](eva_gs1_9n5_AAAAAA.json) |

</details>

<details><summary><code>eya_qj3_tev</code> 酈食其（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 酈食其 | [《史記・酈生陸賈列傳》][343] | [JSON](eya_qj3_tev.json) |
| `A` | 疥（酈食其子） | [《史記・酈生陸賈列傳》][343] | [JSON](eya_qj3_tev_A.json) |

</details>

<details><summary><code>f04_rc9_xqn</code> 太史敫（田世家候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 太史敫 | [《史記・田敬仲完世家》][292] | [JSON](f04_rc9_xqn.json) |
| `A` | 君王后 | [《史記・田敬仲完世家》][292] | [JSON](f04_rc9_xqn_A.json) |

</details>

<details><summary><code>f2z_47w_81j</code> 商玄石（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 商玄石 | [《宋書・謝晦》][425]、[《宋書・謝晦》][426] | [JSON](f2z_47w_81j.json) |
| `A` | 商懷福 | [《宋書・謝晦》][425]、[《宋書・謝晦》][426] | [JSON](f2z_47w_81j_A.json) |

</details>

<details><summary><code>f41_ulg_3u1</code> 衛滿（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 衛滿 | [《史記・朝鮮列傳》][361] | [JSON](f41_ulg_3u1.json) |
| `*A` | 右渠 | [《史記・朝鮮列傳》][361] | [JSON](f41_ulg_3u1_%2AA.json) |
| `*AA` | 長（右渠子） | [《史記・朝鮮列傳》][361] | [JSON](f41_ulg_3u1_%2AAA.json) |

</details>

<details><summary><code>f89_ad1_61d</code> 王凌（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 王凌 | [《三國志・王毌丘諸葛鄧鍾傳》][263] | [JSON](f89_ad1_61d.json) |
| `A` | 王廣 | [《三國志・王毌丘諸葛鄧鍾傳》][263] | [JSON](f89_ad1_61d_A.json) |

</details>

<details><summary><code>f8d_j5p_nop</code> 孔防叔（孔子世家候選）（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 孔防叔 | [《史記・孔子世家》][293] | [JSON](f8d_j5p_nop.json) |
| `A` | 伯夏 | [《史記・孔子世家》][293] | [JSON](f8d_j5p_nop_A.json) |
| `AA` | 叔梁紇 | [《史記・孔子世家》][293] | [JSON](f8d_j5p_nop_AA.json) |

</details>

<details><summary><code>f90_933_c35</code> 猗盧（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 猗盧 | [《晉書・王沈 荀顗 荀勖 馮紞》][68] | [JSON](f90_933_c35.json) |
| `A` | 日律孫 | [《晉書・王沈 荀顗 荀勖 馮紞》][68] | [JSON](f90_933_c35_A.json) |

</details>

<details><summary><code>faf_5al_ikw</code> 鄭武公（老韓列傳候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 鄭武公 | [《史記・老子韓非列傳》][309] | [JSON](faf_5al_ikw.json) |
| `A` | 鄭武公之子 | [《史記・老子韓非列傳》][309] | [JSON](faf_5al_ikw_A.json) |

</details>

<details><summary><code>fcu_pw8_tkw</code> 蔡興宗（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 蔡興宗 | [《南齊書・王融 謝朓》][168]、[《南史・謝晦　謝裕　謝方明　謝靈運》][194]、[《南史・王曇首》][218]、[《南史・王曇首》][225]、[《南史・王曇首》][224]、[《宋書・徐湛之 江湛 王僧綽》][451]、[《宋書・徐湛之 江湛 王僧綽》][449]、[《宋書・徐湛之 江湛 王僧綽》][450] | [JSON](fcu_pw8_tkw.json) |
| `A` | 蔡約 | [《南史・王曇首》][218] | [JSON](fcu_pw8_tkw_A.json) |

</details>

<details><summary><code>fd3_tly_1lo</code> 沸（魯魏公）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 沸（魯魏公） | [《史記・魯周公世家》][279] | [JSON](fd3_tly_1lo.json) |
| `A` | 擢（魯厲公） | [《史記・魯周公世家》][279]、[《史記・三代世表》][494] | [JSON](fd3_tly_1lo_A.json) |

</details>

<details><summary><code>fdb_6pb_gux</code> 蒯聵（太史公自序候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 蒯聵 | [《史記・太史公自序》][376] | [JSON](fdb_6pb_gux.json) |
| `***A` | 司馬卬 | [《史記・高祖本紀》][272]、[《史記・太史公自序》][376] | [JSON](fdb_6pb_gux_%2A%2A%2AA.json) |

</details>

<details><summary><code>ffc_ea1_a8f</code> 范寧（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 范寧 | [《晉書・王湛 荀崧 范汪 劉惔 張憑 韓伯》][88] | [JSON](ffc_ea1_a8f.json) |
| `A` | 范泰 | [《宋書・范泰 王准之 王韶之 荀伯子》][439] | [JSON](ffc_ea1_a8f_A.json) |

</details>

<details><summary><code>fjm_eo3_0zz</code> 始興王憺（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 始興王憺 | [《南史・王裕之　王鎮之　王韶之　王悅之　王准之》][241] | [JSON](fjm_eo3_0zz.json) |
| `A` | 繁昌主 | [《南史・王裕之　王鎮之　王韶之　王悅之　王准之》][241] | [JSON](fjm_eo3_0zz_A.json) |

</details>

<details><summary><code>fmh_dmt_cql</code> 汲黯（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 汲黯 | [《史記・汲鄭列傳》][366] | [JSON](fmh_dmt_cql.json) |
| `A` | 汲偃 | [《漢書・張馮汲鄭傳》][25]、[《史記・汲鄭列傳》][366] | [JSON](fmh_dmt_cql_A.json) |

</details>

<details><summary><code>fo7_f8v_rmf</code> 梁武帝衍（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 梁武帝衍 | [《梁書・謝朏 弟子覽》][120] | [JSON](fo7_f8v_rmf.json) |
| `A` | 蕭玉姚 | [《梁書・皇后》][118] | [JSON](fo7_f8v_rmf_A.json) |
| `B` | 蕭玉婉 | [《梁書・皇后》][118] | [JSON](fo7_f8v_rmf_B.json) |

</details>

<details><summary><code>fom_gr9_c8v</code> 孫叔敖（循吏列傳候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 孫叔敖 | [《史記・循吏列傳》][365]、[《史記・滑稽列傳》][372] | [JSON](fom_gr9_c8v.json) |
| `A` | 孫叔敖子（未名） | [《史記・滑稽列傳》][372] | [JSON](fom_gr9_c8v_A.json) |

</details>

<details><summary><code>fp6_ia6_7yw</code> 孔子（11 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 孔子 | [《史記・孔子世家》][293] | [JSON](fp6_ia6_7yw.json) |
| `A` | 鯉 | [《史記・孔子世家》][293] | [JSON](fp6_ia6_7yw_A.json) |
| `AA` | 伋 | [《史記・孔子世家》][293] | [JSON](fp6_ia6_7yw_AA.json) |
| `AAA` | 白 | [《史記・孔子世家》][293] | [JSON](fp6_ia6_7yw_AAA.json) |
| `AAAA` | 求 | [《史記・孔子世家》][293] | [JSON](fp6_ia6_7yw_AAAA.json) |
| `AAAAA` | 箕 | [《史記・孔子世家》][293] | [JSON](fp6_ia6_7yw_AAAAA.json) |
| `AAAAAA` | 穿 | [《史記・孔子世家》][293] | [JSON](fp6_ia6_7yw_AAAAAA.json) |
| `AAAAAAA` | 子慎 | [《史記・孔子世家》][293] | [JSON](fp6_ia6_7yw_AAAAAAA.json) |
| `AAAAAAAA` | 鮒 | [《史記・孔子世家》][293] | [JSON](fp6_ia6_7yw_AAAAAAAA.json) |
| `B` | 孔鯉 | [《史記・仲尼弟子列傳》][313] | [JSON](fp6_ia6_7yw_B.json) |
| `C` | 孔子之女 | [《史記・仲尼弟子列傳》][313] | [JSON](fp6_ia6_7yw_C.json) |

</details>

<details><summary><code>fs1_z3i_d4r</code> 趙遐（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 趙遐 | [《崔混墓誌・節錄》][12] | [JSON](fs1_z3i_d4r.json) |
| `A` | 趙氏（崔混妻） | [《崔混墓誌・節錄》][12] | [JSON](fs1_z3i_d4r_A.json) |

</details>

<details><summary><code>fum_370_iq6</code> 結〔楊播高祖〕（28 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 結〔楊播高祖〕 | [《魏書・楊播》][476] | [JSON](fum_370_iq6.json) |
| `A` | 珍〔楊播曾祖〕 | [《魏書・楊播》][476]、[《魏書・楊播》][477] | [JSON](fum_370_iq6_A.json) |
| `AA` | 真〔楊播祖〕 | [《楊舒墓誌・全文》][16]、[《魏書・楊播》][476]、[《魏書・楊播》][477] | [JSON](fum_370_iq6_AA.json) |
| `AAA` | 懿〔楊播父〕 | [《魏書・楊播》][476] | [JSON](fum_370_iq6_AAA.json) |
| `AAAA` | 楊播 | [《魏書・楊播》][476] | [JSON](fum_370_iq6_AAAA.json) |
| `AAAAA` | 侃〔楊播子，字士業〕 | [《魏書・楊播》][476] | [JSON](fum_370_iq6_AAAAA.json) |
| `AAAAAA` | 師沖〔楊侃長子，北史作師仲〕 | [《魏書・楊播》][476] | [JSON](fum_370_iq6_AAAAAA.json) |
| `AAAAAB` | 純陀〔楊侃嗣子〕 | [《魏書・楊播》][476] | [JSON](fum_370_iq6_AAAAAB.json) |
| `AAAB` | 楊椿 | [《魏書・楊播》][477] | [JSON](fum_370_iq6_AAAB.json) |
| `AAABA` | 楊昱 | [《魏書・楊播》][477] | [JSON](fum_370_iq6_AAABA.json) |
| `AAABAA` | 孝邕〔楊昱子〕 | [《魏書・楊播》][477] | [JSON](fum_370_iq6_AAABAA.json) |
| `AAAC` | 穎〔楊椿弟，字惠哲〕 | [《魏書・楊播》][477] | [JSON](fum_370_iq6_AAAC.json) |
| `AAACA` | 叔良〔楊穎子〕 | [《魏書・楊播》][477] | [JSON](fum_370_iq6_AAACA.json) |
| `AAAD` | 順〔楊穎弟，字延和〕 | [《魏書・楊播》][477] | [JSON](fum_370_iq6_AAAD.json) |
| `AAADA` | 辯〔楊順子，字僧達〕 | [《魏書・楊播》][477] | [JSON](fum_370_iq6_AAADA.json) |
| `AAADB` | 仲宣〔楊順子〕 | [《魏書・楊播》][477] | [JSON](fum_370_iq6_AAADB.json) |
| `AAADBA` | 玄就〔楊仲宣子〕 | [《魏書・楊播》][477] | [JSON](fum_370_iq6_AAADBA.json) |
| `AAADC` | 測〔楊仲宣弟〕 | [《魏書・楊播》][477] | [JSON](fum_370_iq6_AAADC.json) |
| `AAADD` | 稚卿〔楊測弟〕 | [《魏書・楊播》][477] | [JSON](fum_370_iq6_AAADD.json) |
| `AAAE` | 楊津〔字羅漢，本名延祚〕 | [《魏書・楊播》][478] | [JSON](fum_370_iq6_AAAE.json) |
| `AAAEA` | 楊遁〔字山才，津長子〕 | [《魏書・楊播》][478] | [JSON](fum_370_iq6_AAAEA.json) |
| `AAAEB` | 楊逸〔字遵道，津第二子〕 | [《魏書・楊播》][478] | [JSON](fum_370_iq6_AAAEB.json) |
| `AAAEC` | 楊謐〔字遵智，逸弟〕 | [《魏書・楊播》][478] | [JSON](fum_370_iq6_AAAEC.json) |
| `AAAED` | 楊遵彥〔謐弟〕 | [《南史・王弘》][212]、[《魏書・楊播》][478] | [JSON](fum_370_iq6_AAAED.json) |
| `AAAF` | 楊暐〔字延季，津弟〕 | [《魏書・楊播》][478] | [JSON](fum_370_iq6_AAAF.json) |
| `AAAFA` | 楊元讓〔暐子〕 | [《魏書・楊播》][478] | [JSON](fum_370_iq6_AAAFA.json) |
| `AAB` | 洛州恒農簡公〔楊舒墓誌父〕 | [《楊舒墓誌・全文》][16] | [JSON](fum_370_iq6_AAB.json) |
| `AABA` | 舒〔楊昱第六叔〕 | [《楊舒墓誌・全文》][16] | [JSON](fum_370_iq6_AABA.json) |

</details>

<details><summary><code>fvm_66f_0k3</code> 周緤（4 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 周緤 | [《史記・傅靳蒯成列傳》][344] | [JSON](fvm_66f_0k3.json) |
| `A` | 周昌（蒯成侯之子） | [《漢書・樊酈滕灌傅靳周傳》][24]、[《史記・傅靳蒯成列傳》][344]、[《史記・高祖功臣侯者年表》][499] | [JSON](fvm_66f_0k3_A.json) |
| `C` | 周應 | [《漢書・樊酈滕灌傅靳周傳》][24] | [JSON](fvm_66f_0k3_C.json) |
| `CA` | 周仲居 | [《史記・高祖功臣侯者年表》][499] | [JSON](fvm_66f_0k3_CA.json) |

</details>

<details><summary><code>g9h_5ih_ug1</code> 伍奢（伍胥列傳候選）（4 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 伍奢 | [《史記・伍子胥列傳》][312] | [JSON](g9h_5ih_ug1.json) |
| `A` | 伍子胥 | [《史記・伍子胥列傳》][312] | [JSON](g9h_5ih_ug1_A.json) |
| `AA` | 伍子胥之子 | [《史記・伍子胥列傳》][312] | [JSON](g9h_5ih_ug1_AA.json) |
| `B` | 伍尚 | [《史記・伍子胥列傳》][312] | [JSON](g9h_5ih_ug1_B.json) |

</details>

<details><summary><code>ga6_jt5_6g1</code> 圉（衛孔文子）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 圉（衛孔文子） | [《史記・衛康叔世家》][283] | [JSON](ga6_jt5_6g1.json) |
| `A` | 悝（衛孔氏） | [《史記・衛康叔世家》][283] | [JSON](ga6_jt5_6g1_A.json) |

</details>

<details><summary><code>gcb_rf3_coi</code> 費王（晉穆侯）（4 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 費王（晉穆侯） | [《史記・晉世家》][285] | [JSON](gcb_rf3_coi.json) |
| `A` | 仇（晉文侯） | [《史記・晉世家》][285] | [JSON](gcb_rf3_coi_A.json) |
| `AA` | 伯（晉昭侯） | [《史記・晉世家》][285] | [JSON](gcb_rf3_coi_AA.json) |
| `B` | 成師（曲沃桓叔） | [《史記・晉世家》][285] | [JSON](gcb_rf3_coi_B.json) |

</details>

<details><summary><code>gcu_93j_y97</code> 鄭遵（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 鄭遵 | [《南史・范泰　荀伯子　徐廣　鄭鮮之　裴松之　何承天》][245] | [JSON](gcu_93j_y97.json) |
| `A` | 鄭鮮之 | [《南史・范泰　荀伯子　徐廣　鄭鮮之　裴松之　何承天》][245] | [JSON](gcu_93j_y97_A.json) |

</details>

<details><summary><code>gdj_k53_v1x</code> 王翦（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 王翦 | [《史記・白起王翦列傳》][319] | [JSON](gdj_k53_v1x.json) |
| `*A` | 王離 | [《史記・白起王翦列傳》][319] | [JSON](gdj_k53_v1x_%2AA.json) |
| `A` | 王賁 | [《史記・白起王翦列傳》][319] | [JSON](gdj_k53_v1x_A.json) |

</details>

<details><summary><code>ghg_5p7_q21</code> 遂（杞釐公）（4 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 遂（杞釐公） | [《史記・陳杞世家》][282] | [JSON](ghg_5p7_q21.json) |
| `A` | 維（杞湣公） | [《史記・陳杞世家》][282] | [JSON](ghg_5p7_q21_A.json) |
| `AA` | 敕（杞出公） | [《史記・陳杞世家》][282] | [JSON](ghg_5p7_q21_AA.json) |
| `AAA` | 春（杞簡公） | [《史記・陳杞世家》][282] | [JSON](ghg_5p7_q21_AAA.json) |

</details>

<details><summary><code>gjl_f5h_2a6</code> 劉景猷（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 劉景猷 | [《南齊書・皇后》][145] | [JSON](gjl_f5h_2a6.json) |
| `A` | 劉惠端 | [《南齊書・皇后》][145] | [JSON](gjl_f5h_2a6_A.json) |
| `B` | 劉暄 | [《南史・謝晦　謝裕　謝方明　謝靈運》][194] | [JSON](gjl_f5h_2a6_B.json) |

</details>

<details><summary><code>gm4_alk_hn7</code> 劉玄之（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 劉玄之 | [《南齊書・皇后》][143] | [JSON](gm4_alk_hn7.json) |
| `A` | 劉壽之 | [《南齊書・皇后》][143] | [JSON](gm4_alk_hn7_A.json) |
| `AA` | 劉智容 | [《南齊書・皇后》][143] | [JSON](gm4_alk_hn7_AA.json) |

</details>

<details><summary><code>gn7_br7_32m</code> 伯州犁（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 伯州犁 | [《史記・吳太伯世家》][277] | [JSON](gn7_br7_32m.json) |
| `*A` | 伯嚭 | [《史記・吳太伯世家》][277] | [JSON](gn7_br7_32m_%2AA.json) |

</details>

<details><summary><code>gqj_xdu_8rf</code> 張騫（李將軍列傳候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 張騫 | [《史記・大宛列傳》][369] | [JSON](gqj_xdu_8rf.json) |
| `A` | 張騫子（未名） | [《史記・大宛列傳》][369] | [JSON](gqj_xdu_8rf_A.json) |

</details>

<details><summary><code>gts_42q_flu</code> 睔（鄭世家成公候選）（7 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 睔 | [《史記・鄭世家》][288] | [JSON](gts_42q_flu.json) |
| `A` | 惲 | [《史記・鄭世家》][288] | [JSON](gts_42q_flu_A.json) |
| `AA` | 嘉 | [《史記・鄭世家》][288] | [JSON](gts_42q_flu_AA.json) |
| `AAA` | 寧 | [《史記・鄭世家》][288] | [JSON](gts_42q_flu_AAA.json) |
| `AAAA` | 蠆 | [《史記・鄭世家》][288] | [JSON](gts_42q_flu_AAAA.json) |
| `AAAAA` | 勝 | [《史記・鄭世家》][288] | [JSON](gts_42q_flu_AAAAA.json) |
| `AAAAAA` | 易 | [《史記・鄭世家》][288] | [JSON](gts_42q_flu_AAAAAA.json) |

</details>

<details><summary><code>h1w_44g_vef</code> 張孟（魏其武安侯列傳候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 張孟 | [《史記・魏其武安列傳》][353] | [JSON](h1w_44g_vef.json) |
| `A` | 灌夫 | [《史記・魏其武安列傳》][353] | [JSON](h1w_44g_vef_A.json) |

</details>

<details><summary><code>h4f_d5f_vdl</code> 蟬封（大宛列傳候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 蟬封 | [《史記・大宛列傳》][369] | [JSON](h4f_d5f_vdl.json) |
| `A` | 蟬封子（入質，未名） | [《史記・大宛列傳》][369] | [JSON](h4f_d5f_vdl_A.json) |

</details>

<details><summary><code>h7n_w5t_i1c</code> 曹休未名祖父（7 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 曹休未名祖父 | [《三國志・諸夏侯曹傳》][251] | [JSON](h7n_w5t_i1c.json) |
| `A` | 曹休未名父 | [《三國志・諸夏侯曹傳》][251] | [JSON](h7n_w5t_i1c_A.json) |
| `AA` | 曹休 | [《三國志・諸夏侯曹傳》][251] | [JSON](h7n_w5t_i1c_AA.json) |
| `AAA` | 肇（曹攄祖、曹休子） | [《三國志・諸夏侯曹傳》][251] | [JSON](h7n_w5t_i1c_AAA.json) |
| `AAA*A` | 曹顏遠 | [《晉書・良吏》][102] | [JSON](h7n_w5t_i1c_AAA%2AA.json) |
| `AAAA` | 興（肇子） | [《三國志・諸夏侯曹傳》][251] | [JSON](h7n_w5t_i1c_AAAA.json) |
| `AAB` | 纂（肇弟） | [《三國志・諸夏侯曹傳》][251] | [JSON](h7n_w5t_i1c_AAB.json) |

</details>

<details><summary><code>hx8_st4_jdd</code> 宋孝武帝駿（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 宋孝武帝駿 | [《宋書・殷淳 張暢 何偃 江智淵》][438] | [JSON](hx8_st4_jdd.json) |
| `A` | 安固公主（宋孝武女） | [《梁書・王瞻 王志 王峻 王暕 子訓 王泰 王份 孫鍚 僉 張充 柳惲 蔡撙 江蒨》][128]、[《梁書・王瞻 王志 王峻 王暕 子訓 王泰 王份 孫鍚 僉 張充 柳惲 蔡撙 江蒨》][127]、[《南史・王曇首》][234]、[《南史・王曇首》][233] | [JSON](hx8_st4_jdd_A.json) |
| `B` | 永嘉王子仁 | [《宋書・孝武十四王》][454] | [JSON](hx8_st4_jdd_B.json) |

</details>

<details><summary><code>i30_mjq_6q8</code> 呂公（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 呂公 | [《史記・高祖本紀》][272] | [JSON](i30_mjq_6q8.json) |
| `A` | 呂后 | [《史記・呂后本紀》][273] | [JSON](i30_mjq_6q8_A.json) |

</details>

<details><summary><code>i3f_9l9_g53</code> 陳平（5 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 陳平 | [《史記・陳丞相世家》][302] | [JSON](i3f_9l9_g53.json) |
| `**A` | 陳掌 | [《史記・陳丞相世家》][302] | [JSON](i3f_9l9_g53_%2A%2AA.json) |
| `A` | 買 | [《史記・陳丞相世家》][302] | [JSON](i3f_9l9_g53_A.json) |
| `AA` | 恢 | [《史記・陳丞相世家》][302] | [JSON](i3f_9l9_g53_AA.json) |
| `AAA` | 何 | [《史記・陳丞相世家》][302] | [JSON](i3f_9l9_g53_AAA.json) |

</details>

<details><summary><code>i7a_22p_qda</code> 句踐（7 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 句踐 | [《史記・越王勾踐世家》][287] | [JSON](i7a_22p_qda.json) |
| `A` | 鼫與 | [《史記・越王勾踐世家》][287] | [JSON](i7a_22p_qda_A.json) |
| `AA` | 不壽 | [《史記・越王勾踐世家》][287] | [JSON](i7a_22p_qda_AA.json) |
| `AAA` | 翁 | [《史記・越王勾踐世家》][287] | [JSON](i7a_22p_qda_AAA.json) |
| `AAAA` | 翳 | [《史記・越王勾踐世家》][287] | [JSON](i7a_22p_qda_AAAA.json) |
| `AAAAA` | 之侯 | [《史記・越王勾踐世家》][287] | [JSON](i7a_22p_qda_AAAAA.json) |
| `AAAAAA` | 無彊 | [《史記・越王勾踐世家》][287] | [JSON](i7a_22p_qda_AAAAAA.json) |

</details>

<details><summary><code>i8i_rvh_4lp</code> 燬（衛文公）（8 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 燬（衛文公） | [《史記・衛康叔世家》][283] | [JSON](i8i_rvh_4lp.json) |
| `A` | 鄭（衛成公） | [《史記・衛康叔世家》][283] | [JSON](i8i_rvh_4lp_A.json) |
| `AA` | 遫（衛穆公） | [《史記・衛康叔世家》][283] | [JSON](i8i_rvh_4lp_AA.json) |
| `AAA` | 臧（衛定公） | [《史記・衛康叔世家》][283] | [JSON](i8i_rvh_4lp_AAA.json) |
| `AAAA` | 衎（衛獻公） | [《史記・衛康叔世家》][283] | [JSON](i8i_rvh_4lp_AAAA.json) |
| `AAAAA` | 惡（衛襄公） | [《史記・衛康叔世家》][283] | [JSON](i8i_rvh_4lp_AAAAA.json) |
| `AAAAAA` | 元（衛靈公） | [《史記・衛康叔世家》][283] | [JSON](i8i_rvh_4lp_AAAAAA.json) |
| `AAAAAAA` | 郢（衛子南） | [《史記・衛康叔世家》][283] | [JSON](i8i_rvh_4lp_AAAAAAA.json) |

</details>

<details><summary><code>iij_zqi_k5l</code> 齊平公（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 齊平公 | [《史記・齊太公世家》][278] | [JSON](iij_zqi_k5l.json) |
| `A` | 積（齊宣公） | [《史記・齊太公世家》][278] | [JSON](iij_zqi_k5l_A.json) |
| `AA` | 貸（齊康公） | [《史記・齊太公世家》][278] | [JSON](iij_zqi_k5l_AA.json) |

</details>

<details><summary><code>inr_w1g_bu5</code> 子襄（孔子世家候選）（7 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 子襄 | [《史記・孔子世家》][293] | [JSON](inr_w1g_bu5.json) |
| `A` | 忠 | [《史記・孔子世家》][293] | [JSON](inr_w1g_bu5_A.json) |
| `AA` | 武 | [《史記・孔子世家》][293] | [JSON](inr_w1g_bu5_AA.json) |
| `AAA` | 延年 | [《史記・孔子世家》][293] | [JSON](inr_w1g_bu5_AAA.json) |
| `AAB` | 安國 | [《史記・孔子世家》][293] | [JSON](inr_w1g_bu5_AAB.json) |
| `AABA` | 卬 | [《史記・孔子世家》][293] | [JSON](inr_w1g_bu5_AABA.json) |
| `AABAA` | 驩 | [《史記・孔子世家》][293] | [JSON](inr_w1g_bu5_AABAA.json) |

</details>

<details><summary><code>ixk_6fg_v6f</code> 竇后父（外戚世家候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 竇后父 | [《史記・外戚世家》][295] | [JSON](ixk_6fg_v6f.json) |
| `A` | 竇太后（孝文帝皇后） | [《史記・梁孝王世家》][304] | [JSON](ixk_6fg_v6f_A.json) |

</details>

<details><summary><code>j32_wtj_khz</code> 袁盎父未名（袁盎鼂錯列傳候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 袁盎父未名 | [《史記・袁盎鼂錯列傳》][347] | [JSON](j32_wtj_khz.json) |
| `A` | 袁盎 | [《史記・袁盎鼂錯列傳》][347] | [JSON](j32_wtj_khz_A.json) |

</details>

<details><summary><code>jfc_0dt_42a</code> 顧秘（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 顧秘 | [《晉書・王舒 王廙 虞潭 顧眾 張闓》][91] | [JSON](jfc_0dt_42a.json) |
| `A` | 顧衆 | [《晉書・王舒 王廙 虞潭 顧眾 張闓》][95] | [JSON](jfc_0dt_42a_A.json) |

</details>

<details><summary><code>jg1_ag9_033</code> 老子（孔子世家候選）（4 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 老子 | [《史記・老子韓非列傳》][309] | [JSON](jg1_ag9_033.json) |
| `A` | 宗 | [《史記・老子韓非列傳》][309] | [JSON](jg1_ag9_033_A.json) |
| `AA` | 注 | [《史記・老子韓非列傳》][309] | [JSON](jg1_ag9_033_AA.json) |
| `AAA` | 宮 | [《史記・老子韓非列傳》][309] | [JSON](jg1_ag9_033_AAA.json) |

</details>

<details><summary><code>jgo_o5m_l1f</code> 劉秉（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 劉秉 | [《南齊書・褚淵 淵弟澄 徐嗣 王儉》][146]、[《南史・謝晦　謝裕　謝方明　謝靈運》][180]、[《南史・王曇首》][218]、[《南史・王曇首》][222] | [JSON](jgo_o5m_l1f.json) |
| `A` | 劉秉女（王慈妻） | — | [JSON](jgo_o5m_l1f_A.json) |

</details>

<details><summary><code>jjl_irg_zke</code> 盧綰父未名（韓信盧綰列傳候選）（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 盧綰父未名 | [《史記・韓信盧綰列傳》][339] | [JSON](jjl_irg_zke.json) |
| `A` | 盧綰 | [《史記・韓信盧綰列傳》][339] | [JSON](jjl_irg_zke_A.json) |
| `A*A` | 盧他之 | [《史記・韓信盧綰列傳》][339] | [JSON](jjl_irg_zke_A%2AA.json) |

</details>

<details><summary><code>jo4_4bf_0ra</code> 劉澤（5 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 劉澤 | [《史記・荊燕世家》][297] | [JSON](jo4_4bf_0ra.json) |
| `A` | 嘉（燕康王） | [《史記・荊燕世家》][297] | [JSON](jo4_4bf_0ra_A.json) |
| `AA` | 定國 | [《史記・荊燕世家》][297] | [JSON](jo4_4bf_0ra_AA.json) |
| `AAA` | 定國所生男（荊燕世家未名者） | [《史記・荊燕世家》][297] | [JSON](jo4_4bf_0ra_AAA.json) |
| `AB` | 田蚡夫人（燕康王女，未名） | [《史記・魏其武安列傳》][353] | [JSON](jo4_4bf_0ra_AB.json) |

</details>

<details><summary><code>jqx_jns_jae</code> 虞豫（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 虞豫 | [《晉書・后妃下》][63] | [JSON](jqx_jns_jae.json) |
| `A` | 虞孟母 | [《晉書・后妃下》][63] | [JSON](jqx_jns_jae_A.json) |

</details>

<details><summary><code>jru_oiq_x0q</code> 楚成王（鄭世家候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 楚成王 | [《史記・鄭世家》][288] | [JSON](jru_oiq_x0q.json) |
| `A` | 商臣 | [《史記・鄭世家》][288] | [JSON](jru_oiq_x0q_A.json) |

</details>

<details><summary><code>jx9_cov_qe0</code> 欒布（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 欒布 | [《史記・季布欒布列傳》][346] | [JSON](jx9_cov_qe0.json) |
| `A` | 賁（欒布子） | [《史記・季布欒布列傳》][346]、[《史記・惠景間侯者年表》][500] | [JSON](jx9_cov_qe0_A.json) |

</details>

<details><summary><code>jyf_yg2_dqk</code> 沈劭之（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 沈劭之 | [《宋書・薛安都 沈文秀 崔道固》][460] | [JSON](jyf_yg2_dqk.json) |
| `A` | 沈文秀 | [《宋書・薛安都 沈文秀 崔道固》][460] | [JSON](jyf_yg2_dqk_A.json) |

</details>

<details><summary><code>jyx_72x_8t2</code> 褚淵（4 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 褚淵 | [《南史・王曇首》][222] | [JSON](jyx_72x_8t2.json) |
| `A` | 褚蓁 | [《梁書・王規 劉瑴 宗懍 王承 褚翔 蕭介 從父兄洽 褚球 劉孺 弟覽 遵 劉潛 弟孝勝 孝威 孝先 殷芸 蕭幾》][136] | [JSON](jyx_72x_8t2_A.json) |
| `AA` | 褚向（字景政） | [《梁書・王規 劉瑴 宗懍 王承 褚翔 蕭介 從父兄洽 褚球 劉孺 弟覽 遵 劉潛 弟孝勝 孝威 孝先 殷芸 蕭幾》][136] | [JSON](jyx_72x_8t2_AA.json) |
| `AAA` | 褚翔 | [《梁書・王規 劉瑴 宗懍 王承 褚翔 蕭介 從父兄洽 褚球 劉孺 弟覽 遵 劉潛 弟孝勝 孝威 孝先 殷芸 蕭幾》][136] | [JSON](jyx_72x_8t2_AAA.json) |

</details>

<details><summary><code>k2p_5ol_dwh</code> 蒙驁（4 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 蒙驁 | [《史記・蒙恬列傳》][334] | [JSON](k2p_5ol_dwh.json) |
| `A` | 蒙武 | [《史記・蒙恬列傳》][334] | [JSON](k2p_5ol_dwh_A.json) |
| `AA` | 蒙恬 | [《史記・蒙恬列傳》][334] | [JSON](k2p_5ol_dwh_AA.json) |
| `AB` | 蒙毅 | [《史記・蒙恬列傳》][334] | [JSON](k2p_5ol_dwh_AB.json) |

</details>

<details><summary><code>k5z_d58_n7p</code> 熊元（楚考烈王）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 熊元（楚考烈王） | [《史記・春申君列傳》][324] | [JSON](k5z_d58_n7p.json) |
| `A` | 悍（楚幽王） | [《史記・春申君列傳》][324] | [JSON](k5z_d58_n7p_A.json) |

</details>

<details><summary><code>kix_r92_2ed</code> 齊世祖賾（6 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 齊世祖賾 | [《南齊書・虞玩之 劉休 沈沖 庾杲之 王諶》][153] | [JSON](kix_r92_2ed.json) |
| `A` | 蕭子敬（安陸王） | [《南齊書・武十七王》][160] | [JSON](kix_r92_2ed_A.json) |
| `B` | 蕭子琳 | [《南史・齊武帝諸子　文惠諸子　明帝諸子》][248] | [JSON](kix_r92_2ed_B.json) |
| `C` | 蕭子罕（南海王） | [《梁書・王瞻 王志 王峻 王暕 子訓 王泰 王份 孫鍚 僉 張充 柳惲 蔡撙 江蒨》][126]、[《梁書・王瞻 王志 王峻 王暕 子訓 王泰 王份 孫鍚 僉 張充 柳惲 蔡撙 江蒨》][125]、[《南齊書・武十七王》][159] | [JSON](kix_r92_2ed_C.json) |
| `D` | 吳縣公主（齊武帝長女） | — | [JSON](kix_r92_2ed_D.json) |
| `E` | 廬陵王子卿 | [《南齊書・武十七王》][158] | [JSON](kix_r92_2ed_E.json) |

</details>

<details><summary><code>koy_6jg_gcc</code> 周勃（6 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 周勃 | [《史記・絳侯周勃世家》][303] | [JSON](koy_6jg_gcc.json) |
| `A` | 勝之 | [《史記・絳侯周勃世家》][303] | [JSON](koy_6jg_gcc_A.json) |
| `B` | 堅 | [《史記・絳侯周勃世家》][303] | [JSON](koy_6jg_gcc_B.json) |
| `BA` | 建德 | [《史記・絳侯周勃世家》][303] | [JSON](koy_6jg_gcc_BA.json) |
| `C` | 周亞夫 | [《史記・絳侯周勃世家》][303] | [JSON](koy_6jg_gcc_C.json) |
| `CA` | 亞夫子 | [《史記・絳侯周勃世家》][303] | [JSON](koy_6jg_gcc_CA.json) |

</details>

<details><summary><code>kt8_3kv_44r</code> 頑（衛昭伯）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 頑（衛昭伯） | [《史記・衛康叔世家》][283] | [JSON](kt8_3kv_44r.json) |
| `A` | 申（衛戴公） | [《史記・衛康叔世家》][283] | [JSON](kt8_3kv_44r_A.json) |

</details>

<details><summary><code>ktk_wbg_wnm</code> 鄧公（袁盎鼂錯列傳候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 鄧公 | [《史記・袁盎鼂錯列傳》][347] | [JSON](ktk_wbg_wnm.json) |
| `A` | 章（鄧公子） | [《史記・袁盎鼂錯列傳》][347] | [JSON](ktk_wbg_wnm_A.json) |

</details>

<details><summary><code>l3c_zg4_f7z</code> 宋襄公（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 宋襄公 | [《史記・宋微子世家》][284] | [JSON](l3c_zg4_f7z.json) |
| `A` | 王臣（宋成公） | [《史記・宋微子世家》][284] | [JSON](l3c_zg4_f7z_A.json) |
| `AA` | 杵臼（宋昭公） | [《史記・宋微子世家》][284] | [JSON](l3c_zg4_f7z_AA.json) |

</details>

<details><summary><code>l8e_pxu_xre</code> 武公（趙世家趙君候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 武公 | [《史記・趙世家》][289] | [JSON](l8e_pxu_xre.json) |
| `A` | 朝 | [《史記・趙世家》][289] | [JSON](l8e_pxu_xre_A.json) |

</details>

<details><summary><code>l9e_fbr_36a</code> 倉（韓世家襄王候選）（9 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 倉 | [《史記・韓世家》][291] | [JSON](l9e_fbr_36a.json) |
| `*A` | 韓王信（韓太尉） | [《史記・韓信盧綰列傳》][339] | [JSON](l9e_fbr_36a_%2AA.json) |
| `*AA` | 韓王信太子未名 | [《史記・韓信盧綰列傳》][339] | [JSON](l9e_fbr_36a_%2AAA.json) |
| `*AAA` | 韓嬰 | [《史記・韓信盧綰列傳》][339] | [JSON](l9e_fbr_36a_%2AAAA.json) |
| `*AB` | 韓穨當 | [《史記・韓信盧綰列傳》][339] | [JSON](l9e_fbr_36a_%2AAB.json) |
| `*AB*A` | 韓嫣 | [《史記・佞幸列傳》][371] | [JSON](l9e_fbr_36a_%2AAB%2AA.json) |
| `*AB*B` | 韓說 | [《史記・東越列傳》][360] | [JSON](l9e_fbr_36a_%2AAB%2AB.json) |
| `*AB*B*A` | 韓曾 | [《史記・韓信盧綰列傳》][339] | [JSON](l9e_fbr_36a_%2AAB%2AB%2AA.json) |
| `*AB*BA` | 韓說子未名 | [《史記・韓信盧綰列傳》][339] | [JSON](l9e_fbr_36a_%2AAB%2ABA.json) |

</details>

<details><summary><code>lc5_nwz_ikf</code> 襲之〔宣之繼者〕（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 襲之〔宣之繼者〕 | [《宋書・后妃》][422] | [JSON](lc5_nwz_ikf.json) |
| `A` | 祖憐〔襲之子〕 | [《宋書・后妃》][422] | [JSON](lc5_nwz_ikf_A.json) |

</details>

<details><summary><code>lc6_cup_v9c</code> 稱（魯孝公）（5 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 稱（魯孝公） | [《史記・魯周公世家》][279] | [JSON](lc6_cup_v9c.json) |
| `A` | 弗湟（魯惠公） | [《史記・魯周公世家》][279] | [JSON](lc6_cup_v9c_A.json) |
| `AA` | 魯隱公 | [《史記・魯周公世家》][279] | [JSON](lc6_cup_v9c_AA.json) |
| `AB` | 魯桓公 | [《史記・魯周公世家》][279] | [JSON](lc6_cup_v9c_AB.json) |
| `ABA` | 季友（成季） | [《史記・魯周公世家》][279] | [JSON](lc6_cup_v9c_ABA.json) |

</details>

<details><summary><code>lcc_msq_vdt</code> 露（曹靖公）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 露（曹靖公） | [《史記・管蔡世家》][281] | [JSON](lcc_msq_vdt.json) |
| `A` | 伯陽（曹君） | [《史記・管蔡世家》][281] | [JSON](lcc_msq_vdt_A.json) |

</details>

<details><summary><code>li9_cmb_8ci</code> 滕公（本卷稱呼）（4 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 滕公（本卷稱呼） | [《史記・樊酈滕灌列傳》][341] | [JSON](li9_cmb_8ci.json) |
| `A` | 夏侯灶 | [《史記・樊酈滕灌列傳》][341] | [JSON](li9_cmb_8ci_A.json) |
| `AA` | 夏侯賜 | [《史記・樊酈滕灌列傳》][341] | [JSON](li9_cmb_8ci_AA.json) |
| `AAA` | 夏侯頗 | [《史記・樊酈滕灌列傳》][341] | [JSON](li9_cmb_8ci_AAA.json) |

</details>

<details><summary><code>ll1_7jh_vr0</code> 鄭合（6 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 鄭合 | [《晉書・后妃下》][63] | [JSON](ll1_7jh_vr0.json) |
| `A` | 鄭愷 | [《晉書・后妃下》][63] | [JSON](ll1_7jh_vr0_A.json) |
| `AA` | 鄭阿春 | [《晉書・后妃下》][63] | [JSON](ll1_7jh_vr0_AA.json) |
| `AB` | 鄭氏（阿春妹，王褒妻） | [《晉書・后妃下》][63] | [JSON](ll1_7jh_vr0_AB.json) |
| `AC` | 鄭氏（阿春三妹，劉傭妻） | [《晉書・后妃下》][63] | [JSON](ll1_7jh_vr0_AC.json) |
| `AD` | 鄭氏（阿春幼妹，李氏妻） | [《晉書・后妃下》][63] | [JSON](ll1_7jh_vr0_AD.json) |

</details>

<details><summary><code>lmu_nbm_rzo</code> 燮（陳平公）（21 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 燮（陳平公） | [《史記・陳杞世家》][282] | [JSON](lmu_nbm_rzo.json) |
| `A` | 圉（陳文公） | [《史記・陳杞世家》][282] | [JSON](lmu_nbm_rzo_A.json) |
| `AA` | 佗（陳厲公） | [《史記・陳杞世家》][282] | [JSON](lmu_nbm_rzo_AA.json) |
| `AAA` | 完（敬仲） | [《史記・田敬仲完世家》][292] | [JSON](lmu_nbm_rzo_AAA.json) |
| `AAAA` | 稚孟夷 | [《史記・田敬仲完世家》][292] | [JSON](lmu_nbm_rzo_AAAA.json) |
| `AAAAA` | 湣孟莊 | [《史記・田敬仲完世家》][292] | [JSON](lmu_nbm_rzo_AAAAA.json) |
| `AAAAAA` | 田文子須無 | [《史記・田敬仲完世家》][292] | [JSON](lmu_nbm_rzo_AAAAAA.json) |
| `AAAAAAA` | 田桓子無宇 | [《史記・田敬仲完世家》][292] | [JSON](lmu_nbm_rzo_AAAAAAA.json) |
| `AAAAAAAA` | 武子開 | [《史記・田敬仲完世家》][292] | [JSON](lmu_nbm_rzo_AAAAAAAA.json) |
| `AAAAAAAB` | 田釐子乞 | [《史記・田敬仲完世家》][292] | [JSON](lmu_nbm_rzo_AAAAAAAB.json) |
| `AAAAAAABA` | 田常 | [《史記・田敬仲完世家》][292] | [JSON](lmu_nbm_rzo_AAAAAAABA.json) |
| `AAAAAAABAA` | 田襄子盤 | [《史記・田敬仲完世家》][292] | [JSON](lmu_nbm_rzo_AAAAAAABAA.json) |
| `AAAAAAABAAA` | 田莊子白 | [《史記・田敬仲完世家》][292] | [JSON](lmu_nbm_rzo_AAAAAAABAAA.json) |
| `AAAAAAABAAAA` | 太公和 | [《史記・田敬仲完世家》][292] | [JSON](lmu_nbm_rzo_AAAAAAABAAAA.json) |
| `AAAAAAABAAAAA` | 桓公午 | [《史記・扁鵲倉公列傳》][351] | [JSON](lmu_nbm_rzo_AAAAAAABAAAAA.json) |
| `AAAAAAABAAAAAA` | 因齊 | [《史記・田敬仲完世家》][292] | [JSON](lmu_nbm_rzo_AAAAAAABAAAAAA.json) |
| `AAAAAAABAAAAAAA` | 辟彊 | [《史記・田敬仲完世家》][292]、[《史記・孟嘗君列傳》][321] | [JSON](lmu_nbm_rzo_AAAAAAABAAAAAAA.json) |
| `AAAAAAABAAAAAAAA` | 齊湣王 | [《史記・孟嘗君列傳》][321] | [JSON](lmu_nbm_rzo_AAAAAAABAAAAAAAA.json) |
| `AB` | 鮑（陳桓公） | [《史記・陳杞世家》][282] | [JSON](lmu_nbm_rzo_AB.json) |
| `ABA` | 免（陳桓公太子） | [《史記・陳杞世家》][282] | [JSON](lmu_nbm_rzo_ABA.json) |
| `ABB` | 躍（陳利公） | [《史記・陳杞世家》][282] | [JSON](lmu_nbm_rzo_ABB.json) |

</details>

<details><summary><code>lrg_cze_g1l</code> 蘇峻（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 蘇峻 | [《晉書・庾亮》][86]、[《晉書・叛臣三》][112] | [JSON](lrg_cze_g1l.json) |
| `A` | 蘇碩 | [《晉書・叛臣三》][112] | [JSON](lrg_cze_g1l_A.json) |

</details>

<details><summary><code>lt4_hpv_4ku</code> 武成王（燕君）（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 武成王（燕君） | [《史記・燕召公世家》][280] | [JSON](lt4_hpv_4ku.json) |
| `A` | 孝王（燕君） | [《史記・燕召公世家》][280] | [JSON](lt4_hpv_4ku_A.json) |
| `AA` | 燕王喜 | [《史記・燕召公世家》][280] | [JSON](lt4_hpv_4ku_AA.json) |

</details>

<details><summary><code>lwx_9yq_ad7</code> 紂（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 紂 | [《史記・殷本紀》][267] | [JSON](lwx_9yq_ad7.json) |
| `A` | 武庚 | [《史記・衛康叔世家》][283] | [JSON](lwx_9yq_ad7_A.json) |

</details>

<details><summary><code>m0b_b5e_153</code> 田常（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 田常 | [《史記・齊太公世家》][278] | [JSON](m0b_b5e_153.json) |
| `**A` | 田和 | [《史記・六國年表》][496] | [JSON](m0b_b5e_153_%2A%2AA.json) |

</details>

<details><summary><code>m8d_pnd_ias</code> 惠侯（燕君）（10 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 惠侯（燕君） | [《史記・燕召公世家》][280] | [JSON](m8d_pnd_ias.json) |
| `A` | 釐侯（燕君） | [《史記・燕召公世家》][280] | [JSON](m8d_pnd_ias_A.json) |
| `AA` | 頃侯（燕君） | [《史記・燕召公世家》][280] | [JSON](m8d_pnd_ias_AA.json) |
| `AAA` | 哀侯（燕君） | [《史記・燕召公世家》][280] | [JSON](m8d_pnd_ias_AAA.json) |
| `AAAA` | 鄭侯（燕君） | [《史記・燕召公世家》][280] | [JSON](m8d_pnd_ias_AAAA.json) |
| `AAAAA` | 繆侯（燕君） | [《史記・燕召公世家》][280] | [JSON](m8d_pnd_ias_AAAAA.json) |
| `AAAAAA` | 宣侯（燕君） | [《史記・燕召公世家》][280] | [JSON](m8d_pnd_ias_AAAAAA.json) |
| `AAAAAAA` | 桓侯（燕君） | [《史記・燕召公世家》][280] | [JSON](m8d_pnd_ias_AAAAAAA.json) |
| `AAAAAAAA` | 燕莊公 | [《史記・齊太公世家》][278]、[《史記・燕召公世家》][280] | [JSON](m8d_pnd_ias_AAAAAAAA.json) |
| `AAAAAAAAA` | 襄公（燕君） | [《史記・燕召公世家》][280] | [JSON](m8d_pnd_ias_AAAAAAAAA.json) |

</details>

<details><summary><code>m8n_ntm_79h</code> 盧植（12 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 盧植 | [《後漢書・吳延史盧趙列傳》][34] | [JSON](m8n_ntm_79h.json) |
| `A` | 盧毓 | [《三國志・桓二陳徐衞盧傳》][260] | [JSON](m8n_ntm_79h_A.json) |
| `A*A` | 藩〔盧毓孫〕 | [《三國志・桓二陳徐衞盧傳》][260] | [JSON](m8n_ntm_79h_A%2AA.json) |
| `AA` | 盧欽〔舉王衍者〕 | [《三國志・桓二陳徐衞盧傳》][260] | [JSON](m8n_ntm_79h_AA.json) |
| `AAA` | 盧浮 | [《三國志・桓二陳徐衞盧傳》][260] | [JSON](m8n_ntm_79h_AAA.json) |
| `AB` | 盧珽 | [《三國志・桓二陳徐衞盧傳》][260] | [JSON](m8n_ntm_79h_AB.json) |
| `ABA` | 皓〔盧珽子〕 | [《三國志・桓二陳徐衞盧傳》][260] | [JSON](m8n_ntm_79h_ABA.json) |
| `ABB` | 盧志 | [《三國志・桓二陳徐衞盧傳》][260] | [JSON](m8n_ntm_79h_ABB.json) |
| `ABBA` | 盧諶 | [《三國志・桓二陳徐衞盧傳》][260] | [JSON](m8n_ntm_79h_ABBA.json) |
| `ABBA**A` | 盧循 | [《宋書・張茂度 庾登之 謝方明 江夷》][434] | [JSON](m8n_ntm_79h_ABBA%2A%2AA.json) |
| `ABBAA` | 偃〔盧諶子〕 | [《魏書・燕鳳 許謙 張衮 崔玄伯 鄧淵》][473] | [JSON](m8n_ntm_79h_ABBAA.json) |
| `ABBAAA` | 邈〔偃子〕 | [《魏書・燕鳳 許謙 張衮 崔玄伯 鄧淵》][473] | [JSON](m8n_ntm_79h_ABBAAA.json) |

</details>

<details><summary><code>m9n_b6v_wo0</code> 梁孝王（本卷未名）（5 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 梁孝王（本卷未名） | [《史記・孝景本紀》][275] | [JSON](m9n_b6v_wo0.json) |
| `A` | 明（梁孝王子） | [《史記・孝景本紀》][275] | [JSON](m9n_b6v_wo0_A.json) |
| `B` | 彭離（梁孝王子） | [《史記・孝景本紀》][275] | [JSON](m9n_b6v_wo0_B.json) |
| `C` | 定（梁孝王子） | [《史記・孝景本紀》][275] | [JSON](m9n_b6v_wo0_C.json) |
| `D` | 不識（梁孝王子） | [《史記・孝景本紀》][275] | [JSON](m9n_b6v_wo0_D.json) |

</details>

<details><summary><code>maz_aq2_t5g</code> 季勝（趙世家祖系候選）（4 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 季勝 | [《史記・趙世家》][289] | [JSON](maz_aq2_t5g.json) |
| `A` | 孟增 | [《史記・趙世家》][289] | [JSON](maz_aq2_t5g_A.json) |
| `AA` | 衡父 | [《史記・趙世家》][289] | [JSON](maz_aq2_t5g_AA.json) |
| `AAA` | 造父 | [《史記・趙世家》][289] | [JSON](maz_aq2_t5g_AAA.json) |

</details>

<details><summary><code>mgh_3bh_rit</code> 周厲王（鄭世家候選）（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 周厲王 | [《史記・鄭世家》][288] | [JSON](mgh_3bh_rit.json) |
| `A` | 友 | [《史記・鄭世家》][288] | [JSON](mgh_3bh_rit_A.json) |
| `AA` | 掘突 | [《史記・鄭世家》][288] | [JSON](mgh_3bh_rit_AA.json) |

</details>

<details><summary><code>mj8_5ic_4kk</code> 殷道鸞（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 殷道鸞 | [《宋書・謝晦》][425]、[《宋書・謝晦》][426] | [JSON](mj8_5ic_4kk.json) |
| `A` | 殷琰 | [《宋書・蕭惠開 殷琰》][458]、[《宋書・薛安都 沈文秀 崔道固》][459] | [JSON](mj8_5ic_4kk_A.json) |

</details>

<details><summary><code>ms3_fa1_ps9</code> 田生（荊燕世家候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 田生 | [《史記・荊燕世家》][297] | [JSON](ms3_fa1_ps9.json) |
| `A` | 田生子 | [《史記・荊燕世家》][297] | [JSON](ms3_fa1_ps9_A.json) |

</details>

<details><summary><code>muq_yy8_8er</code> 寤生（鄭世家莊公候選）（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 寤生 | [《史記・鄭世家》][288] | [JSON](muq_yy8_8er.json) |
| `A` | 忽 | [《史記・鄭世家》][288] | [JSON](muq_yy8_8er_A.json) |
| `B` | 突 | [《史記・鄭世家》][288] | [JSON](muq_yy8_8er_B.json) |

</details>

<details><summary><code>mwc_md4_l0g</code> 王含（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 王含 | [《晉書・王舒 王廙 虞潭 顧眾 張闓》][93] | [JSON](mwc_md4_l0g.json) |
| `A` | 王應 | [《晉書・王舒 王廙 虞潭 顧眾 張闓》][93] | [JSON](mwc_md4_l0g_A.json) |

</details>

<details><summary><code>mxz_qw8_acd</code> 王揖（4 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 王揖 | [《南史・王曇首》][230]、[《南史・王曇首》][234] | [JSON](mxz_qw8_acd.json) |
| `A` | 王筠 | [《梁書・王僧孺 張率 劉孝綽 王筠》][133]、[《梁書・王僧孺 張率 劉孝綽 王筠》][132] | [JSON](mxz_qw8_acd_A.json) |
| `AA` | 王祥（王筠子） | [《南史・王曇首》][232]、[《南史・王曇首》][231]、[《隋書・文學》][465] | [JSON](mxz_qw8_acd_AA.json) |
| `AAA` | 王胄（字承基） | [《隋書・文學》][465] | [JSON](mxz_qw8_acd_AAA.json) |

</details>

<details><summary><code>n0i_g82_0n2</code> 蒯聵（衛莊公）（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 蒯聵（衛莊公） | [《史記・衛康叔世家》][283] | [JSON](n0i_g82_0n2.json) |
| `A` | 輒（衛出公） | [《史記・衛康叔世家》][283] | [JSON](n0i_g82_0n2_A.json) |
| `AA` | 出公子（衛黔所攻者未名） | [《史記・衛康叔世家》][283] | [JSON](n0i_g82_0n2_AA.json) |

</details>

<details><summary><code>n2x_d8l_n0d</code> 嵇翰（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 嵇翰 | [《晉書・忠義》][101] | [JSON](n2x_d8l_n0d.json) |
| `*A` | 嵇曠 | [《晉書・忠義》][101] | [JSON](n2x_d8l_n0d_%2AA.json) |

</details>

<details><summary><code>n3u_6wg_kay</code> 隆（張次公父）（衛將軍驃騎列傳候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 隆（張次公父） | [《史記・衛將軍驃騎列傳》][357] | [JSON](n3u_6wg_kay.json) |
| `A` | 張次公 | [《史記・衛將軍驃騎列傳》][357] | [JSON](n3u_6wg_kay_A.json) |

</details>

<details><summary><code>n4f_fqh_04q</code> 易王（燕君）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 易王（燕君） | [《史記・蘇秦列傳》][315] | [JSON](n4f_fqh_04q.json) |
| `A` | 燕噲（本篇燕君） | [《史記・燕召公世家》][280] | [JSON](n4f_fqh_04q_A.json) |

</details>

<details><summary><code>nbl_2bu_99w</code> 王舒（4 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 王舒 | [《晉書・王舒 王廙 虞潭 顧眾 張闓》][95] | [JSON](nbl_2bu_99w.json) |
| `A` | 王晏之 | [《晉書・王舒 王廙 虞潭 顧眾 張闓》][95] | [JSON](nbl_2bu_99w_A.json) |
| `AA` | 王崐之 | [《晉書・王舒 王廙 虞潭 顧眾 張闓》][95] | [JSON](nbl_2bu_99w_AA.json) |
| `AAA` | 王陋之 | [《晉書・王舒 王廙 虞潭 顧眾 張闓》][95] | [JSON](nbl_2bu_99w_AAA.json) |

</details>

<details><summary><code>nf1_c66_863</code> 楊季主（游俠列傳候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 楊季主 | [《史記・游俠列傳》][370] | [JSON](nf1_c66_863.json) |
| `A` | 楊季主子（未名縣掾） | [《史記・游俠列傳》][370] | [JSON](nf1_c66_863_A.json) |

</details>

<details><summary><code>nfj_6w2_8mn</code> 增（魏世家景湣王候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 增 | [《史記・魏世家》][290] | [JSON](nfj_6w2_8mn.json) |
| `A` | 假 | [《史記・魏世家》][290] | [JSON](nfj_6w2_8mn_A.json) |

</details>

<details><summary><code>nuf_tb9_fjs</code> 竇嬰父（未名）（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 竇嬰父（未名） | [《史記・魏其武安列傳》][353] | [JSON](nuf_tb9_fjs.json) |
| `A` | 竇嬰 | [《史記・魏其武安列傳》][353] | [JSON](nuf_tb9_fjs_A.json) |
| `AA` | 竇嬰子未名 | [《史記・魏其武安列傳》][353] | [JSON](nuf_tb9_fjs_AA.json) |

</details>

<details><summary><code>nxl_qt6_cpl</code> 畢萬（魏世家候選）（9 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 畢萬 | [《史記・魏世家》][290] | [JSON](nxl_qt6_cpl.json) |
| `A` | 魏武子 | [《史記・魏世家》][290] | [JSON](nxl_qt6_cpl_A.json) |
| `AA` | 魏悼子 | [《史記・魏世家》][290] | [JSON](nxl_qt6_cpl_AA.json) |
| `AAA` | 魏絳 | [《史記・魏世家》][290] | [JSON](nxl_qt6_cpl_AAA.json) |
| `AAAA` | 魏嬴 | [《史記・魏世家》][290] | [JSON](nxl_qt6_cpl_AAAA.json) |
| `AAAAA` | 魏獻子 | [《史記・魏世家》][290] | [JSON](nxl_qt6_cpl_AAAAA.json) |
| `AAAAAA` | 魏侈 | [《史記・魏世家》][290] | [JSON](nxl_qt6_cpl_AAAAAA.json) |
| `AAAAAA*A` | 魏桓子 | [《史記・魏世家》][290] | [JSON](nxl_qt6_cpl_AAAAAA%2AA.json) |
| `AAAAAA*A*A` | 都 | [《史記・魏世家》][290] | [JSON](nxl_qt6_cpl_AAAAAA%2AA%2AA.json) |

</details>

<details><summary><code>nye_x8g_zwl</code> 陳桓公鮑（田世家候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 陳桓公鮑 | [《史記・田敬仲完世家》][292] | [JSON](nye_x8g_zwl.json) |
| `A` | 陳莊公林 | [《史記・田敬仲完世家》][292] | [JSON](nye_x8g_zwl_A.json) |

</details>

<details><summary><code>o0l_em5_5v9</code> 吳芮（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 吳芮 | [《史記・高祖本紀》][272] | [JSON](o0l_em5_5v9.json) |
| `A` | 臣（吳芮子） | [《史記・呂后本紀》][273]、[《史記・黥布列傳》][337]、[《史記・漢興以來諸侯王年表》][498] | [JSON](o0l_em5_5v9_A.json) |
| `B` | 英布妻未名 | [《史記・黥布列傳》][337] | [JSON](o0l_em5_5v9_B.json) |

</details>

<details><summary><code>opr_t0a_l8g</code> 淳于公（齊太倉令）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 淳于公（齊太倉令） | [《史記・扁鵲倉公列傳》][351] | [JSON](opr_t0a_l8g.json) |
| `A` | 緹縈 | [《史記・扁鵲倉公列傳》][351] | [JSON](opr_t0a_l8g_A.json) |

</details>

<details><summary><code>osu_yvw_bwr</code> 熊惲（楚成王候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 熊惲 | [《史記・楚世家》][286] | [JSON](osu_yvw_bwr.json) |
| `A` | 職（楚成王欲立之子） | [《史記・楚世家》][286] | [JSON](osu_yvw_bwr_A.json) |

</details>

<details><summary><code>p4b_qf7_603</code> 趙武（趙庶子）（4 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 趙武（趙庶子） | [《史記・趙世家》][289] | [JSON](p4b_qf7_603.json) |
| `A` | 趙景叔 | [《史記・趙世家》][289] | [JSON](p4b_qf7_603_A.json) |
| `AA` | 趙鞅 | [《史記・趙世家》][289] | [JSON](p4b_qf7_603_AA.json) |
| `AAA` | 趙襄子毋卹 | [《史記・趙世家》][289] | [JSON](p4b_qf7_603_AAA.json) |

</details>

<details><summary><code>p93_tgr_t8r</code> 王遠（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 王遠 | [《南史・王弘》][213] | [JSON](p93_tgr_t8r.json) |
| `A` | 王僧祐 | [《南齊書・王秀之 王慈 蔡約 陸慧曉 顧憲之 蕭惠基》][167]、[《南史・王弘》][208] | [JSON](p93_tgr_t8r_A.json) |
| `AA` | 王籍〔字文海〕 | [《南史・王弘》][205] | [JSON](p93_tgr_t8r_AA.json) |

</details>

<details><summary><code>p9l_wy7_y7m</code> 魏文侯（孫吳列傳候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 魏文侯 | [《史記・孫子吳起列傳》][311] | [JSON](p9l_wy7_y7m.json) |
| `A` | 魏武侯 | [《史記・孫子吳起列傳》][311] | [JSON](p9l_wy7_y7m_A.json) |

</details>

<details><summary><code>pev_wez_mab</code> 宋富人（老韓列傳候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 宋富人 | [《史記・老子韓非列傳》][309] | [JSON](pev_wez_mab.json) |
| `A` | 富人之子 | [《史記・老子韓非列傳》][309] | [JSON](pev_wez_mab_A.json) |

</details>

<details><summary><code>pg6_rqk_vuk</code> 如姬父未名（魏公子列傳候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 如姬父未名 | [《史記・魏公子列傳》][323] | [JSON](pg6_rqk_vuk.json) |
| `A` | 如姬 | [《史記・魏公子列傳》][323] | [JSON](pg6_rqk_vuk_A.json) |

</details>

<details><summary><code>ph1_ms8_hyq</code> 亮〔孝懿蕭后祖；字保祚〕（5 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 亮〔孝懿蕭后祖；字保祚〕 | [《宋書・后妃》][422] | [JSON](ph1_ms8_hyq.json) |
| `A` | 蕭卓 | [《宋書・后妃》][422] | [JSON](ph1_ms8_hyq_A.json) |
| `AA` | 蕭文夀〔孝懿皇后〕 | [《宋書・后妃》][422] | [JSON](ph1_ms8_hyq_AA.json) |
| `AB` | 源之〔蕭卓子〕 | [《宋書・后妃》][422] | [JSON](ph1_ms8_hyq_AB.json) |
| `ABA` | 蕭思話 | [《南齊書・王僧虔 張緒》][151] | [JSON](ph1_ms8_hyq_ABA.json) |

</details>

<details><summary><code>pj3_k53_wtj</code> 觸龍（趙世家左師候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 觸龍 | [《史記・趙世家》][289] | [JSON](pj3_k53_wtj.json) |
| `A` | 舒祺 | [《史記・趙世家》][289] | [JSON](pj3_k53_wtj_A.json) |

</details>

<details><summary><code>pme_eis_xqi</code> 司馬錯（7 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 司馬錯 | [《史記・秦本紀》][269] | [JSON](pme_eis_xqi.json) |
| `*A` | 司馬靳 | [《史記・太史公自序》][376] | [JSON](pme_eis_xqi_%2AA.json) |
| `*A*A` | 司馬昌 | [《史記・太史公自序》][376] | [JSON](pme_eis_xqi_%2AA%2AA.json) |
| `*A*AA` | 司馬無澤 | [《史記・太史公自序》][376] | [JSON](pme_eis_xqi_%2AA%2AAA.json) |
| `*A*AAA` | 司馬喜 | [《史記・太史公自序》][376] | [JSON](pme_eis_xqi_%2AA%2AAAA.json) |
| `*A*AAAA` | 司馬談 | [《史記・太史公自序》][376] | [JSON](pme_eis_xqi_%2AA%2AAAAA.json) |
| `*A*AAAAA` | 司馬遷 | [《史記・太史公自序》][376] | [JSON](pme_eis_xqi_%2AA%2AAAAAA.json) |

</details>

<details><summary><code>ptn_sz3_vro</code> 劉義慶（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 劉義慶 | [《宋書・謝靈運》][448] | [JSON](ptn_sz3_vro.json) |
| `A` | 臨川王義慶女（王僧達妻，未名） | [《宋書・王僧達 顏竣》][452] | [JSON](ptn_sz3_vro_A.json) |

</details>

<details><summary><code>pyb_nda_bwz</code> 鄖公與懷之父（伍胥列傳候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 鄖公與懷之父 | [《史記・伍子胥列傳》][312] | [JSON](pyb_nda_bwz.json) |
| `A` | 懷 | [《史記・伍子胥列傳》][312] | [JSON](pyb_nda_bwz_A.json) |

</details>

<details><summary><code>q1y_uet_htw</code> 伯州犁（伍胥列傳候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 伯州犁 | [《史記・伍子胥列傳》][312] | [JSON](q1y_uet_htw.json) |
| `*A` | 伯嚭 | [《史記・伍子胥列傳》][312] | [JSON](q1y_uet_htw_%2AA.json) |

</details>

<details><summary><code>q60_34y_1zh</code> 章（楚惠王）（5 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 章（楚惠王） | [《史記・楚世家》][286] | [JSON](q60_34y_1zh.json) |
| `A` | 中（楚簡王） | [《史記・楚世家》][286] | [JSON](q60_34y_1zh_A.json) |
| `AA` | 當（楚聲王） | [《史記・楚世家》][286] | [JSON](q60_34y_1zh_AA.json) |
| `AAA` | 熊疑（楚悼王） | [《史記・范睢蔡澤列傳》][325] | [JSON](q60_34y_1zh_AAA.json) |
| `AAAA` | 臧（楚肅王） | [《史記・楚世家》][286] | [JSON](q60_34y_1zh_AAAA.json) |

</details>

<details><summary><code>q63_4br_3of</code> 江德隣（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 江德隣 | [《南齊書・王晏 蕭諶 蕭坦之 江祏》][162] | [JSON](q63_4br_3of.json) |
| `A` | 江祏 | [《南史・謝晦　謝裕　謝方明　謝靈運》][194] | [JSON](q63_4br_3of_A.json) |
| `B` | 江祀 | [《南史・謝晦　謝裕　謝方明　謝靈運》][194] | [JSON](q63_4br_3of_B.json) |

</details>

<details><summary><code>q69_35n_f3h</code> 公孫弘（平津侯主父列傳候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 公孫弘 | [《史記・平津侯主父列傳》][358] | [JSON](q69_35n_f3h.json) |
| `A` | 公孫度 | [《史記・平津侯主父列傳》][358] | [JSON](q69_35n_f3h_A.json) |

</details>

<details><summary><code>q6w_qm5_w2b</code> 丹（趙世家孝成王候選）（4 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 丹 | [《史記・平原君虞卿列傳》][322] | [JSON](q6w_qm5_w2b.json) |
| `A` | 偃 | [《史記・趙世家》][289] | [JSON](q6w_qm5_w2b_A.json) |
| `AA` | 趙王遷 | [《史記・趙世家》][289] | [JSON](q6w_qm5_w2b_AA.json) |
| `AB` | 代王嘉 | [《史記・秦始皇本紀》][270]、[《史記・六國年表》][496] | [JSON](q6w_qm5_w2b_AB.json) |

</details>

<details><summary><code>q71_dto_v57</code> 秦宜禄（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 秦宜禄 | [《三國志・諸夏侯曹傳》][252] | [JSON](q71_dto_v57.json) |
| `A` | 秦朗 | [《三國志・諸夏侯曹傳》][252] | [JSON](q71_dto_v57_A.json) |

</details>

<details><summary><code>q7c_rp0_s04</code> 趙主父（楚篇懷王奔趙時）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 趙主父（楚篇懷王奔趙時） | [《史記・楚世家》][286] | [JSON](q7c_rp0_s04.json) |
| `A` | 趙惠王（楚篇初立者） | [《史記・楚世家》][286] | [JSON](q7c_rp0_s04_A.json) |

</details>

<details><summary><code>q7m_r8k_2vn</code> 王僧朗（18 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 王僧朗 | [《梁書・王瞻 王志 王峻 王暕 子訓 王泰 王份 孫鍚 僉 張充 柳惲 蔡撙 江蒨》][122]、[《南齊書・王奐 從弟繢 張沖》][170] | [JSON](q7m_r8k_2vn.json) |
| `A` | 王粹 | [《梁書・王瞻 王志 王峻 王暕 子訓 王泰 王份 孫鍚 僉 張充 柳惲 蔡撙 江蒨》][122]、[《南齊書・王奐 從弟繢 張沖》][170]、[《南史・王誕　王華　王惠　王彧》][239] | [JSON](q7m_r8k_2vn_A.json) |
| `AA` | 王奐 | [《南齊書・王奐 從弟繢 張沖》][170] | [JSON](q7m_r8k_2vn_AA.json) |
| `AAA` | 王琛 | [《北史・王肅 劉芳 常爽》][4]、[《王令媛墓誌・節錄》][13]、[《王翊墓誌・節錄》][15]、[《南齊書・王奐 從弟繢 張沖》][170]、[《魏書・王肅 宋弁》][480] | [JSON](q7m_r8k_2vn_AAA.json) |
| `AAAA` | 王翊 | [《王翊墓誌・節錄》][15] | [JSON](q7m_r8k_2vn_AAAA.json) |
| `AAAAA` | 王令媛 | [《王令媛墓誌・節錄》][13] | [JSON](q7m_r8k_2vn_AAAAA.json) |
| `AB` | 王份 | [《梁書・王瞻 王志 王峻 王暕 子訓 王泰 王份 孫鍚 僉 張充 柳惲 蔡撙 江蒨》][122] | [JSON](q7m_r8k_2vn_AB.json) |
| `ABA` | 王琳 | [《梁書・王瞻 王志 王峻 王暕 子訓 王泰 王份 孫鍚 僉 張充 柳惲 蔡撙 江蒨》][122]、[《南史・王誕　王華　王惠　王彧》][236] | [JSON](q7m_r8k_2vn_ABA.json) |
| `ABAA` | 王銓 | [《南史・王誕　王華　王惠　王彧》][236] | [JSON](q7m_r8k_2vn_ABAA.json) |
| `ABAB` | 王錫 | [《梁書・王瞻 王志 王峻 王暕 子訓 王泰 王份 孫鍚 僉 張充 柳惲 蔡撙 江蒨》][122]、[《南史・王誕　王華　王惠　王彧》][236] | [JSON](q7m_r8k_2vn_ABAB.json) |
| `ABABA` | 王㳬 | [《周書・列傳第40 蕭詧》][487] | [JSON](q7m_r8k_2vn_ABABA.json) |
| `ABABAA` | 王瓘 | [《周書・列傳第40 蕭詧》][487] | [JSON](q7m_r8k_2vn_ABABAA.json) |
| `ABABB` | 王湜 | [《梁書・王瞻 王志 王峻 王暕 子訓 王泰 王份 孫鍚 僉 張充 柳惲 蔡撙 江蒨》][121]、[《南史・王誕　王華　王惠　王彧》][235]、[《周書・列傳第40 蕭詧》][487] | [JSON](q7m_r8k_2vn_ABABB.json) |
| `ABABBA` | 王懷 | [《周書・列傳第40 蕭詧》][487] | [JSON](q7m_r8k_2vn_ABABBA.json) |
| `ABAC` | 王通 | [《陳書・列傳第十一: 王沖 王通 袁敬》][8] | [JSON](q7m_r8k_2vn_ABAC.json) |
| `ABAD` | 王質 | [《陳書・列傳第十二: 沈眾 袁泌 劉仲威 陸山才 王質 韋載》][9] | [JSON](q7m_r8k_2vn_ABAD.json) |
| `ABAE` | 王固 | [《陳書・列傳第十五: 謝哲 蕭乾 謝嘏 張種 王固 孔奐 蕭允》][10] | [JSON](q7m_r8k_2vn_ABAE.json) |
| `ABAEA` | 王寬 | [《陳書・列傳第十五: 謝哲 蕭乾 謝嘏 張種 王固 孔奐 蕭允》][10] | [JSON](q7m_r8k_2vn_ABAEA.json) |

</details>

<details><summary><code>q8m_d0c_kq3</code> 楚莊王（13 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 楚莊王 | [《史記・楚世家》][286] | [JSON](q8m_d0c_kq3.json) |
| `A` | 審（楚共王） | [《史記・楚世家》][286] | [JSON](q8m_d0c_kq3_A.json) |
| `AA` | 招（楚康王） | [《史記・楚世家》][286] | [JSON](q8m_d0c_kq3_AA.json) |
| `AAA` | 員（郟敖） | [《史記・楚世家》][286] | [JSON](q8m_d0c_kq3_AAA.json) |
| `AAAA` | 莫（郟敖子） | [《史記・楚世家》][286] | [JSON](q8m_d0c_kq3_AAAA.json) |
| `AAAB` | 平夏（郟敖子） | [《史記・楚世家》][286] | [JSON](q8m_d0c_kq3_AAAB.json) |
| `AB` | 圍 | [《史記・楚世家》][286] | [JSON](q8m_d0c_kq3_AB.json) |
| `AC` | 子比（楚初王） | [《史記・楚世家》][286] | [JSON](q8m_d0c_kq3_AC.json) |
| `AD` | 子皙（楚令尹） | [《史記・楚世家》][286] | [JSON](q8m_d0c_kq3_AD.json) |
| `AE` | 楚平王 | [《史記・楚世家》][286] | [JSON](q8m_d0c_kq3_AE.json) |
| `AEA` | 楚昭王 | [《史記・楚世家》][286] | [JSON](q8m_d0c_kq3_AEA.json) |
| `AEB` | 楚太子建 | [《史記・伍子胥列傳》][312] | [JSON](q8m_d0c_kq3_AEB.json) |
| `AEBA` | 白公勝 | [《史記・伍子胥列傳》][312] | [JSON](q8m_d0c_kq3_AEBA.json) |

</details>

<details><summary><code>qdt_1oy_jci</code> 杵臼（陳宣公）（7 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 杵臼（陳宣公） | [《史記・陳杞世家》][282] | [JSON](qdt_1oy_jci.json) |
| `A` | 款（陳穆公） | [《史記・陳杞世家》][282] | [JSON](qdt_1oy_jci_A.json) |
| `AA` | 朔（陳共公） | [《史記・陳杞世家》][282] | [JSON](qdt_1oy_jci_AA.json) |
| `AAA` | 平國（陳靈公） | [《史記・陳杞世家》][282] | [JSON](qdt_1oy_jci_AAA.json) |
| `AAAA` | 午（陳成公） | [《史記・陳杞世家》][282] | [JSON](qdt_1oy_jci_AAAA.json) |
| `AAAAA` | 哀公（陳君） | [《史記・陳杞世家》][282] | [JSON](qdt_1oy_jci_AAAAA.json) |
| `B` | 御寇（陳宣公太子） | [《史記・陳杞世家》][282] | [JSON](qdt_1oy_jci_B.json) |

</details>

<details><summary><code>qg7_n12_fne</code> 審食其（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 審食其 | [《史記・酈生陸賈列傳》][343] | [JSON](qg7_n12_fne.json) |
| `*A` | 審卿 | [《史記・淮南衡山列傳》][364] | [JSON](qg7_n12_fne_%2AA.json) |

</details>

<details><summary><code>qh8_95j_eh2</code> 獻舞（蔡哀侯）（10 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 獻舞（蔡哀侯） | [《史記・管蔡世家》][281] | [JSON](qh8_95j_eh2.json) |
| `A` | 肸（蔡繆侯） | [《史記・管蔡世家》][281] | [JSON](qh8_95j_eh2_A.json) |
| `AA` | 果（蔡莊侯） | [《史記・管蔡世家》][281] | [JSON](qh8_95j_eh2_AA.json) |
| `AAA` | 申（蔡文侯） | [《史記・管蔡世家》][281] | [JSON](qh8_95j_eh2_AAA.json) |
| `AAAA` | 固（蔡景侯） | [《史記・管蔡世家》][281] | [JSON](qh8_95j_eh2_AAAA.json) |
| `AAAAA` | 般（蔡靈侯） | [《史記・管蔡世家》][281] | [JSON](qh8_95j_eh2_AAAAA.json) |
| `AAAAAA` | 友（蔡隱太子） | [《史記・管蔡世家》][281] | [JSON](qh8_95j_eh2_AAAAAA.json) |
| `AAAAAAA` | 東國（蔡悼侯） | [《史記・管蔡世家》][281] | [JSON](qh8_95j_eh2_AAAAAAA.json) |
| `AAAAB` | 廬（蔡平侯） | [《史記・管蔡世家》][281] | [JSON](qh8_95j_eh2_AAAAB.json) |
| `AAAABA` | 平侯子（被東國攻者未名） | [《史記・管蔡世家》][281] | [JSON](qh8_95j_eh2_AAAABA.json) |

</details>

<details><summary><code>qhp_lk5_t1e</code> 李延年父（未名）（佞幸列傳候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 李延年父（未名） | [《史記・佞幸列傳》][371] | [JSON](qhp_lk5_t1e.json) |
| `A` | 李延年 | [《史記・佞幸列傳》][371] | [JSON](qhp_lk5_t1e_A.json) |

</details>

<details><summary><code>qjs_3hl_6ck</code> 公子發（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 公子發 | [《春秋左傳注疏・卷三十》][493] | [JSON](qjs_3hl_6ck.json) |
| `A` | 子産 | [《史記・鄭世家》][288] | [JSON](qjs_3hl_6ck_A.json) |

</details>

<details><summary><code>qok_ik2_99j</code> 壽（齊悼惠王世家候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 壽 | [《史記・齊悼惠王世家》][298] | [JSON](qok_ik2_99j.json) |
| `A` | 次景 | [《史記・齊悼惠王世家》][298] | [JSON](qok_ik2_99j_A.json) |

</details>

<details><summary><code>qsd_v11_ya1</code> 宏（王懿祖）（4 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 宏（王懿祖） | [《宋書・趙倫之 王懿 張邵》][428] | [JSON](qsd_v11_ya1.json) |
| `A` | 苖（王懿父） | [《宋書・趙倫之 王懿 張邵》][428] | [JSON](qsd_v11_ya1_A.json) |
| `AA` | 王仲徳〔劉義隆鎮北將軍〕 | [《宋書・趙倫之 王懿 張邵》][428] | [JSON](qsd_v11_ya1_AA.json) |
| `AAA` | 正脩（王懿子） | [《宋書・趙倫之 王懿 張邵》][428] | [JSON](qsd_v11_ya1_AAA.json) |

</details>

<details><summary><code>qvt_eq1_lcf</code> 蕭道賜（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 蕭道賜 | [《梁書・武帝上》][115] | [JSON](qvt_eq1_lcf.json) |
| `A` | 蕭順之 | [《梁書・武帝中》][116] | [JSON](qvt_eq1_lcf_A.json) |
| `AA` | 蕭恢 | [《梁書・太祖五王》][129] | [JSON](qvt_eq1_lcf_AA.json) |

</details>

<details><summary><code>qxa_jm7_zmy</code> 黔（衛悼公）（10 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 黔（衛悼公） | [《史記・衛康叔世家》][283] | [JSON](qxa_jm7_zmy.json) |
| `A` | 弗（衛敬公） | [《史記・衛康叔世家》][283] | [JSON](qxa_jm7_zmy_A.json) |
| `AA` | 糾（衛昭公） | [《史記・衛康叔世家》][283] | [JSON](qxa_jm7_zmy_AA.json) |
| `AB` | 適（衛公子） | [《史記・衛康叔世家》][283] | [JSON](qxa_jm7_zmy_AB.json) |
| `ABA` | 穨（衛愼公） | [《史記・衛康叔世家》][283] | [JSON](qxa_jm7_zmy_ABA.json) |
| `ABAA` | 訓（衛聲公） | [《史記・衛康叔世家》][283] | [JSON](qxa_jm7_zmy_ABAA.json) |
| `ABAAA` | 遫（衛成侯） | [《史記・衛康叔世家》][283] | [JSON](qxa_jm7_zmy_ABAAA.json) |
| `ABAAAA` | 平侯（衛成侯子） | [《史記・衛康叔世家》][283] | [JSON](qxa_jm7_zmy_ABAAAA.json) |
| `ABAAAAA` | 嗣君（衛平侯子） | [《史記・衛康叔世家》][283] | [JSON](qxa_jm7_zmy_ABAAAAA.json) |
| `ABAAAAAA` | 懷君（衛嗣君子） | [《史記・衛康叔世家》][283] | [JSON](qxa_jm7_zmy_ABAAAAAA.json) |

</details>

<details><summary><code>qy1_adc_gam</code> 晉（衛宣公）（6 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 晉（衛宣公） | [《史記・衛康叔世家》][283] | [JSON](qy1_adc_gam.json) |
| `A` | 伋（衛宣公太子） | [《史記・衛康叔世家》][283] | [JSON](qy1_adc_gam_A.json) |
| `AA` | 太子伋之子（未名） | [《史記・衛康叔世家》][283] | [JSON](qy1_adc_gam_AA.json) |
| `B` | 壽（衛宣公子） | [《史記・衛康叔世家》][283] | [JSON](qy1_adc_gam_B.json) |
| `C` | 朔（衛惠公） | [《史記・衛康叔世家》][283] | [JSON](qy1_adc_gam_C.json) |
| `CA` | 赤（衛懿公） | [《史記・衛康叔世家》][283] | [JSON](qy1_adc_gam_CA.json) |

</details>

<details><summary><code>r5n_x7v_cwf</code> 彪〔孝穆趙后祖；字世範〕（5 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 彪〔孝穆趙后祖；字世範〕 | [《宋書・后妃》][422] | [JSON](r5n_x7v_cwf.json) |
| `A` | 趙裔 | [《宋書・后妃》][422] | [JSON](r5n_x7v_cwf_A.json) |
| `AA` | 宣之〔趙裔長子〕 | [《宋書・后妃》][422] | [JSON](r5n_x7v_cwf_AA.json) |
| `AB` | 趙安〔孝穆皇后；本見證，高祖之母〕 | [《宋書・后妃》][422] | [JSON](r5n_x7v_cwf_AB.json) |
| `AC` | 倫之〔宣之弟〕 | [《宋書・后妃》][422] | [JSON](r5n_x7v_cwf_AC.json) |

</details>

<details><summary><code>r6c_fhk_jo9</code> 韓太傅（儒林列傳候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 韓太傅 | [《史記・儒林列傳》][367] | [JSON](r6c_fhk_jo9.json) |
| `*A` | 韓生孫商 | [《史記・儒林列傳》][367] | [JSON](r6c_fhk_jo9_%2AA.json) |

</details>

<details><summary><code>r9u_j0z_xtb</code> 秦侯（5 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 秦侯 | [《史記・秦本紀》][269] | [JSON](r9u_j0z_xtb.json) |
| `A` | 公伯 | [《史記・秦本紀》][269] | [JSON](r9u_j0z_xtb_A.json) |
| `AA` | 秦仲 | [《史記・秦本紀》][269] | [JSON](r9u_j0z_xtb_AA.json) |
| `AAA` | 秦莊公 | [《史記・秦本紀》][269] | [JSON](r9u_j0z_xtb_AAA.json) |
| `AAAA` | 世父 | [《史記・秦本紀》][269] | [JSON](r9u_j0z_xtb_AAAA.json) |

</details>

<details><summary><code>ra9_o4d_rli</code> 竇長君（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 竇長君 | [《史記・外戚世家》][295]、[《史記・季布欒布列傳》][346] | [JSON](ra9_o4d_rli.json) |
| `A` | 彭祖 | [《史記・外戚世家》][295] | [JSON](ra9_o4d_rli_A.json) |

</details>

<details><summary><code>rdo_wsn_30x</code> 東樓公（杞君）（8 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 東樓公（杞君） | [《史記・陳杞世家》][282] | [JSON](rdo_wsn_30x.json) |
| `A` | 西樓公（杞君） | [《史記・陳杞世家》][282] | [JSON](rdo_wsn_30x_A.json) |
| `AA` | 題公（杞君） | [《史記・陳杞世家》][282] | [JSON](rdo_wsn_30x_AA.json) |
| `AAA` | 謀娶公（杞君） | [《史記・陳杞世家》][282] | [JSON](rdo_wsn_30x_AAA.json) |
| `AAAA` | 武公（杞君） | [《史記・陳杞世家》][282] | [JSON](rdo_wsn_30x_AAAA.json) |
| `AAAAA` | 靖公（杞君） | [《史記・陳杞世家》][282] | [JSON](rdo_wsn_30x_AAAAA.json) |
| `AAAAAA` | 共公（杞君） | [《史記・陳杞世家》][282] | [JSON](rdo_wsn_30x_AAAAAA.json) |
| `AAAAAAA` | 德公（杞君） | [《史記・陳杞世家》][282] | [JSON](rdo_wsn_30x_AAAAAAA.json) |

</details>

<details><summary><code>rex_cs0_mfo</code> 鮑革（宋文公）（12 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 鮑革（宋文公） | [《史記・宋微子世家》][284] | [JSON](rex_cs0_mfo.json) |
| `A` | 瑕（宋共公） | [《史記・宋微子世家》][284] | [JSON](rex_cs0_mfo_A.json) |
| `AA` | 戌（本版宋平公） | [《史記・宋微子世家》][284] | [JSON](rex_cs0_mfo_AA.json) |
| `AAA` | 佐（宋元公） | [《史記・宋微子世家》][284] | [JSON](rex_cs0_mfo_AAA.json) |
| `AAAA` | 頭曼（宋景公） | [《史記・宋微子世家》][284] | [JSON](rex_cs0_mfo_AAAA.json) |
| `AAAB` | 褍秦（宋元公少子） | [《史記・宋微子世家》][284] | [JSON](rex_cs0_mfo_AAAB.json) |
| `AAABA` | 糾（宋公孫） | [《史記・宋微子世家》][284] | [JSON](rex_cs0_mfo_AAABA.json) |
| `AAABAA` | 特（後宋昭公） | [《史記・宋微子世家》][284] | [JSON](rex_cs0_mfo_AAABAA.json) |
| `AAABAAA` | 購由（宋悼公） | [《史記・宋微子世家》][284] | [JSON](rex_cs0_mfo_AAABAAA.json) |
| `AAABAAAA` | 田（宋休公） | [《史記・宋微子世家》][284] | [JSON](rex_cs0_mfo_AAABAAAA.json) |
| `AAABAAAAA` | 辟兵（宋辟公） | [《史記・宋微子世家》][284] | [JSON](rex_cs0_mfo_AAABAAAAA.json) |
| `AAABAAAAAA` | 剔成（宋君） | [《史記・宋微子世家》][284] | [JSON](rex_cs0_mfo_AAABAAAAAA.json) |

</details>

<details><summary><code>rl6_a40_3hj</code> 馮唐祖父未名（張釋之馮唐列傳候選）（4 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 馮唐祖父未名 | [《史記・張釋之馮唐列傳》][348] | [JSON](rl6_a40_3hj.json) |
| `A` | 馮唐父未名 | [《史記・張釋之馮唐列傳》][348] | [JSON](rl6_a40_3hj_A.json) |
| `AA` | 馮唐 | [《史記・張釋之馮唐列傳》][348] | [JSON](rl6_a40_3hj_AA.json) |
| `AAA` | 馮遂 | [《史記・張釋之馮唐列傳》][348] | [JSON](rl6_a40_3hj_AAA.json) |

</details>

<details><summary><code>rlk_lzd_86c</code> 澄〔王衍弟，荊州刺史〕（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 澄〔王衍弟，荊州刺史〕 | [《晉書・山濤 王戎 郭舒 樂廣》][71] | [JSON](rlk_lzd_86c.json) |
| `A` | 王詹〔王澄長子〕 | [《晉書・山濤 王戎 郭舒 樂廣》][71] | [JSON](rlk_lzd_86c_A.json) |
| `B` | 王徽〔王澄子，右軍司馬〕 | [《世說新語・言語》][380] | [JSON](rlk_lzd_86c_B.json) |

</details>

<details><summary><code>rlv_clg_euu</code> 丕鄭（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 丕鄭 | [《史記・晉世家》][285] | [JSON](rlv_clg_euu.json) |
| `A` | 丕豹 | [《史記・秦本紀》][269] | [JSON](rlv_clg_euu_A.json) |

</details>

<details><summary><code>rr8_o9c_jc1</code> 負芻（曹成公）（4 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 負芻（曹成公） | [《史記・管蔡世家》][281] | [JSON](rr8_o9c_jc1.json) |
| `A` | 勝（曹武公） | [《史記・管蔡世家》][281] | [JSON](rr8_o9c_jc1_A.json) |
| `AA` | 平公（曹武公子） | [《史記・管蔡世家》][281] | [JSON](rr8_o9c_jc1_AA.json) |
| `AAA` | 午（曹悼公） | [《史記・管蔡世家》][281] | [JSON](rr8_o9c_jc1_AAA.json) |

</details>

<details><summary><code>s11_z5r_y2z</code> 東方朔（滑稽列傳候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 東方朔 | [《史記・滑稽列傳》][372] | [JSON](s11_z5r_y2z.json) |
| `A` | 東方朔子（未名） | [《史記・滑稽列傳》][372] | [JSON](s11_z5r_y2z_A.json) |

</details>

<details><summary><code>sj9_pfu_fwh</code> 灌嬰（4 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 灌嬰 | [《史記・樊酈滕灌列傳》][341] | [JSON](sj9_pfu_fwh.json) |
| `*A` | 灌賢 | [《史記・魏其武安列傳》][353] | [JSON](sj9_pfu_fwh_%2AA.json) |
| `A` | 灌阿 | [《史記・樊酈滕灌列傳》][341] | [JSON](sj9_pfu_fwh_A.json) |
| `AA` | 灌彊 | [《史記・樊酈滕灌列傳》][341] | [JSON](sj9_pfu_fwh_AA.json) |

</details>

<details><summary><code>sjw_4mo_dlf</code> 徐生（儒林列傳候選）（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 徐生 | [《史記・儒林列傳》][367] | [JSON](sjw_4mo_dlf.json) |
| `*A` | 徐延 | [《史記・儒林列傳》][367] | [JSON](sjw_4mo_dlf_%2AA.json) |
| `*B` | 徐襄 | [《史記・儒林列傳》][367] | [JSON](sjw_4mo_dlf_%2AB.json) |

</details>

<details><summary><code>sm1_jfi_7k2</code> 王獻之（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 王獻之 | [《晉書・王羲之》][99] | [JSON](sm1_jfi_7k2.json) |
| `A` | 王神愛 | [《晉書・安帝 恭帝》][54]、[《晉書・后妃下》][62]、[《太平御覽・皇親部十五》][466] | [JSON](sm1_jfi_7k2_A.json) |

</details>

<details><summary><code>spx_gk1_rrr</code> 徐湛之（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 徐湛之 | [《南史・王曇首》][225]、[《宋書・徐湛之 江湛 王僧綽》][451]、[《宋書・徐湛之 江湛 王僧綽》][449]、[《宋書・徐湛之 江湛 王僧綽》][450] | [JSON](spx_gk1_rrr.json) |
| `A` | 徐湛之女（隨王誕妃，未名） | [《宋書・徐湛之 江湛 王僧綽》][451] | [JSON](spx_gk1_rrr_A.json) |

</details>

<details><summary><code>sy5_s6h_9ex</code> 鄭文公（重耳過國者）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 鄭文公（重耳過國者） | [《史記・鄭世家》][288] | [JSON](sy5_s6h_9ex.json) |
| `A` | 蘭 | [《史記・鄭世家》][288] | [JSON](sy5_s6h_9ex_A.json) |

</details>

<details><summary><code>t6q_oe6_hom</code> 伏生（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 伏生 | [《史記・儒林列傳》][367] | [JSON](t6q_oe6_hom.json) |
| `*A` | 伏生孫（未名） | [《史記・儒林列傳》][367] | [JSON](t6q_oe6_hom_%2AA.json) |

</details>

<details><summary><code>t7q_vt4_ktj</code> 山（齊獻公）（7 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 山（齊獻公） | [《史記・齊太公世家》][278] | [JSON](t7q_vt4_ktj.json) |
| `A` | 壽（齊武公） | [《史記・齊太公世家》][278] | [JSON](t7q_vt4_ktj_A.json) |
| `AA` | 無忌（齊厲公） | [《史記・齊太公世家》][278] | [JSON](t7q_vt4_ktj_AA.json) |
| `AAA` | 赤（齊文公） | [《史記・齊太公世家》][278] | [JSON](t7q_vt4_ktj_AAA.json) |
| `AAAA` | 脫（齊成公） | [《史記・齊太公世家》][278] | [JSON](t7q_vt4_ktj_AAAA.json) |
| `AAAAA` | 購（齊莊公） | [《史記・齊太公世家》][278] | [JSON](t7q_vt4_ktj_AAAAA.json) |
| `AAAAAA` | 祿甫（齊釐公） | [《史記・齊太公世家》][278] | [JSON](t7q_vt4_ktj_AAAAAA.json) |

</details>

<details><summary><code>tkc_9z3_91l</code> 朱建（酈生陸賈列傳候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 朱建 | [《史記・酈生陸賈列傳》][343] | [JSON](tkc_9z3_91l.json) |
| `A` | 朱建子未名 | [《史記・酈生陸賈列傳》][343] | [JSON](tkc_9z3_91l_A.json) |

</details>

<details><summary><code>txj_z8z_5me</code> 肅侯（趙世家候選）（4 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 肅侯 | [《史記・趙世家》][289] | [JSON](txj_z8z_5me.json) |
| `A` | 趙武靈王 | [《史記・趙世家》][289] | [JSON](txj_z8z_5me_A.json) |
| `AA` | 公子章 | [《史記・趙世家》][289] | [JSON](txj_z8z_5me_AA.json) |
| `AB` | 何 | [《史記・趙世家》][289] | [JSON](txj_z8z_5me_AB.json) |

</details>

<details><summary><code>tz9_dhl_ifo</code> 樛樂（南越列傳候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 樛樂 | [《史記・南越列傳》][359] | [JSON](tz9_dhl_ifo.json) |
| `A` | 廣德 | [《史記・建元以來侯者年表》][501] | [JSON](tz9_dhl_ifo_A.json) |

</details>

<details><summary><code>u3k_51j_4ul</code> 薛廣（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 薛廣 | [《宋書・薛安都 沈文秀 崔道固》][462] | [JSON](u3k_51j_4ul.json) |
| `A` | 薛安都 | [《北史・崔光 崔亮》][6]、[《魏書・燕鳳 許謙 張衮 崔玄伯 鄧淵》][472] | [JSON](u3k_51j_4ul_A.json) |

</details>

<details><summary><code>u3z_kcn_2cf</code> 崔敬友（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 崔敬友 | [《崔混墓誌・節錄》][12] | [JSON](u3z_kcn_2cf.json) |
| `A` | 崔鵾 | [《北史・崔光 崔亮》][5]、[《崔鴻墓誌・節錄》][11]、[《魏書・崔光》][481] | [JSON](u3z_kcn_2cf_A.json) |
| `B` | 崔鷫 | [《崔鴻墓誌・節錄》][11] | [JSON](u3z_kcn_2cf_B.json) |

</details>

<details><summary><code>u61_ylg_6av</code> 石季龍（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 石季龍 | [《晉書・陳騫 裴秀》][65] | [JSON](u61_ylg_6av.json) |
| `A` | 石世 | [《晉書・孝宗穆帝 哀帝 廢帝海西公》][49] | [JSON](u61_ylg_6av_A.json) |

</details>

<details><summary><code>u87_cc1_7vm</code> 田儋（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 田儋 | [《史記・田儋列傳》][340] | [JSON](u87_cc1_7vm.json) |
| `A` | 田市 | [《史記・田儋列傳》][340] | [JSON](u87_cc1_7vm_A.json) |

</details>

<details><summary><code>u9s_w6j_8mc</code> 桓顥（41 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 桓顥 | [《晉書・桓彝》][87] | [JSON](u9s_w6j_8mc.json) |
| `A` | 桓彝 | [《晉書・桓彝》][87] | [JSON](u9s_w6j_8mc_A.json) |
| `AA` | 桓溫 | [《晉書・叛臣一》][109] | [JSON](u9s_w6j_8mc_AA.json) |
| `AAA` | 桓熙 | [《晉書・叛臣一》][109] | [JSON](u9s_w6j_8mc_AAA.json) |
| `AAB` | 桓濟 | [《晉書・叛臣一》][109] | [JSON](u9s_w6j_8mc_AAB.json) |
| `AABA` | 桓亮 | [《晉書・叛臣二》][110] | [JSON](u9s_w6j_8mc_AABA.json) |
| `AAC` | 桓歆 | [《晉書・叛臣二》][110] | [JSON](u9s_w6j_8mc_AAC.json) |
| `AAD` | 桓禕 | [《晉書・叛臣一》][109] | [JSON](u9s_w6j_8mc_AAD.json) |
| `AAE` | 桓偉 | [《晉書・叛臣二》][110] | [JSON](u9s_w6j_8mc_AAE.json) |
| `AAEA` | 桓浚 | [《晉書・叛臣二》][110] | [JSON](u9s_w6j_8mc_AAEA.json) |
| `AAEB` | 桓邈 | [《晉書・叛臣二》][110] | [JSON](u9s_w6j_8mc_AAEB.json) |
| `AAF` | 桓玄 | [《晉書・叛臣二》][110] | [JSON](u9s_w6j_8mc_AAF.json) |
| `AAFA` | 桓升 | [《晉書・叛臣二》][110] | [JSON](u9s_w6j_8mc_AAFA.json) |
| `AB` | 桓雲 | [《晉書・桓彝》][87] | [JSON](u9s_w6j_8mc_AB.json) |
| `AB*A` | 桓放之 | [《晉書・叛臣二》][110] | [JSON](u9s_w6j_8mc_AB%2AA.json) |
| `ABA` | 桓序 | [《晉書・桓彝》][87] | [JSON](u9s_w6j_8mc_ABA.json) |
| `AC` | 桓豁 | [《晉書・桓彝》][87] | [JSON](u9s_w6j_8mc_AC.json) |
| `ACA` | 桓石虔 | [《晉書・桓彝》][87] | [JSON](u9s_w6j_8mc_ACA.json) |
| `ACAA` | 桓誕 | [《晉書・桓彝》][87] | [JSON](u9s_w6j_8mc_ACAA.json) |
| `ACAB` | 桓洪 | [《晉書・桓彝》][87] | [JSON](u9s_w6j_8mc_ACAB.json) |
| `ACAC` | 桓振 | [《晉書・桓彝》][87] | [JSON](u9s_w6j_8mc_ACAC.json) |
| `ACB` | 桓石秀 | [《晉書・桓彝》][87] | [JSON](u9s_w6j_8mc_ACB.json) |
| `ACBA` | 桓稚玉 | [《晉書・桓彝》][87] | [JSON](u9s_w6j_8mc_ACBA.json) |
| `ACC` | 桓石民 | [《晉書・桓彝》][87] | [JSON](u9s_w6j_8mc_ACC.json) |
| `ACD` | 桓石生 | [《晉書・桓彝》][87] | [JSON](u9s_w6j_8mc_ACD.json) |
| `ACE` | 桓石綏 | [《晉書・桓彝》][87] | [JSON](u9s_w6j_8mc_ACE.json) |
| `ACF` | 桓石康 | [《晉書・叛臣二》][110] | [JSON](u9s_w6j_8mc_ACF.json) |
| `ACG` | 桓權 | [《晉書・叛臣二》][110] | [JSON](u9s_w6j_8mc_ACG.json) |
| `AD` | 桓秘 | [《晉書・桓彝》][87] | [JSON](u9s_w6j_8mc_AD.json) |
| `ADA` | 桓蔚 | [《晉書・叛臣二》][110] | [JSON](u9s_w6j_8mc_ADA.json) |
| `AE` | 桓沖 | [《晉書・桓彝》][87] | [JSON](u9s_w6j_8mc_AE.json) |
| `AEA` | 桓嗣 | [《晉書・桓彝》][87] | [JSON](u9s_w6j_8mc_AEA.json) |
| `AEAA` | 桓胤 | [《晉書・叛臣二》][110] | [JSON](u9s_w6j_8mc_AEAA.json) |
| `AEB` | 桓謙 | [《晉書・桓彝》][87] | [JSON](u9s_w6j_8mc_AEB.json) |
| `AEC` | 桓修 | [《晉書・桓彝》][87] | [JSON](u9s_w6j_8mc_AEC.json) |
| `AECA` | 桓修長女〔王琨妻〕 | — | [JSON](u9s_w6j_8mc_AECA.json) |
| `AECB` | 桓修小女〔庾敬度妻〕 | — | [JSON](u9s_w6j_8mc_AECB.json) |
| `AED` | 桓崇 | [《晉書・桓彝》][87] | [JSON](u9s_w6j_8mc_AED.json) |
| `AEE` | 桓弘 | [《晉書・桓彝》][87]、[《晉書・叛臣二》][110] | [JSON](u9s_w6j_8mc_AEE.json) |
| `AEF` | 桓羨 | [《晉書・桓彝》][87] | [JSON](u9s_w6j_8mc_AEF.json) |
| `AEG` | 桓怡 | [《晉書・桓彝》][87] | [JSON](u9s_w6j_8mc_AEG.json) |

</details>

<details><summary><code>uay_2h8_ps8</code> 師（陳悼太子）（4 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 師（陳悼太子） | [《史記・陳杞世家》][282] | [JSON](uay_2h8_ps8.json) |
| `A` | 吳（陳惠公） | [《史記・陳杞世家》][282] | [JSON](uay_2h8_ps8_A.json) |
| `AA` | 柳（陳懷公） | [《史記・陳杞世家》][282] | [JSON](uay_2h8_ps8_AA.json) |
| `AAA` | 越（陳湣公） | [《史記・陳杞世家》][282] | [JSON](uay_2h8_ps8_AAA.json) |

</details>

<details><summary><code>uei_vr9_n3j</code> 竇長君（絳侯周勃世家候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 竇長君 | [《史記・絳侯周勃世家》][303] | [JSON](uei_vr9_n3j.json) |
| `A` | 彭祖 | [《史記・絳侯周勃世家》][303] | [JSON](uei_vr9_n3j_A.json) |

</details>

<details><summary><code>ufr_eoj_xit</code> 石奢父（未名）（循吏列傳候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 石奢父（未名） | [《史記・循吏列傳》][365] | [JSON](ufr_eoj_xit.json) |
| `A` | 石奢 | [《史記・循吏列傳》][365] | [JSON](ufr_eoj_xit_A.json) |

</details>

<details><summary><code>uj9_x5q_yir</code> 宋義（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 宋義 | [《史記・項羽本紀》][271] | [JSON](uj9_x5q_yir.json) |
| `A` | 宋襄 | [《史記・項羽本紀》][271] | [JSON](uj9_x5q_yir_A.json) |

</details>

<details><summary><code>us5_6hk_3qm</code> 屠者（留侯世家候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 屠者 | [《史記・留侯世家》][301] | [JSON](us5_6hk_3qm.json) |
| `A` | 秦嶢下軍將 | [《史記・留侯世家》][301] | [JSON](us5_6hk_3qm_A.json) |

</details>

<details><summary><code>uud_qa6_4u1</code> 郁（杞平公）（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 郁（杞平公） | [《史記・陳杞世家》][282] | [JSON](uud_qa6_4u1.json) |
| `A` | 成（杞悼公） | [《史記・陳杞世家》][282] | [JSON](uud_qa6_4u1_A.json) |
| `AA` | 乞（杞隱公） | [《史記・陳杞世家》][282] | [JSON](uud_qa6_4u1_AA.json) |

</details>

<details><summary><code>vcm_d77_tsz</code> 昌〔祖沖之祖〕（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 昌〔祖沖之祖〕 | [《南齊書・文學》][173] | [JSON](vcm_d77_tsz.json) |
| `A` | 朔之〔祖沖之父〕 | [《南齊書・文學》][173] | [JSON](vcm_d77_tsz_A.json) |
| `AA` | 祖沖之 | [《南齊書・文學》][173] | [JSON](vcm_d77_tsz_AA.json) |

</details>

<details><summary><code>vfh_ufx_cdv</code> 張慶之（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 張慶之 | [《崔鴻墓誌・節錄》][11]、[《崔混墓誌・節錄》][12] | [JSON](vfh_ufx_cdv.json) |
| `A` | 張氏（崔鴻妻） | [《崔混墓誌・節錄》][12] | [JSON](vfh_ufx_cdv_A.json) |

</details>

<details><summary><code>vgg_tso_418</code> 月氏王（被殺）（大宛列傳候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 月氏王（被殺） | [《史記・大宛列傳》][369] | [JSON](vgg_tso_418.json) |
| `A` | 月氏太子（繼王） | [《史記・大宛列傳》][369] | [JSON](vgg_tso_418_A.json) |

</details>

<details><summary><code>vhw_07a_wzm</code> 孔惔（淳之祖）（6 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 孔惔（淳之祖） | [《宋書・隱逸》][464] | [JSON](vhw_07a_wzm.json) |
| `A` | 孔粲（淳之父） | [《宋書・隱逸》][464] | [JSON](vhw_07a_wzm_A.json) |
| `AA` | 孔淳之 | [《宋書・隱逸》][464] | [JSON](vhw_07a_wzm_AA.json) |
| `AAA` | 孔尚 | [《宋書・隱逸》][464] | [JSON](vhw_07a_wzm_AAA.json) |
| `AB` | 孔默之 | [《宋書・隱逸》][464] | [JSON](vhw_07a_wzm_AB.json) |
| `ABA` | 孔熙先 | [《宋書・隱逸》][464] | [JSON](vhw_07a_wzm_ABA.json) |

</details>

<details><summary><code>vna_am7_jn5</code> 韋賢（張丞相列傳候選）（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 韋賢 | [《史記・張丞相列傳》][342] | [JSON](vna_am7_jn5.json) |
| `A` | 韋玄成 | [《史記・張丞相列傳》][342] | [JSON](vna_am7_jn5_A.json) |
| `B` | 韋賢長子未名 | [《史記・張丞相列傳》][342] | [JSON](vna_am7_jn5_B.json) |

</details>

<details><summary><code>vpy_180_2oi</code> 昧〔裴松之祖〕（7 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 昧〔裴松之祖〕 | [《南史・范泰　荀伯子　徐廣　鄭鮮之　裴松之　何承天》][244]、[《宋書・鄭鮮之 裴松之 何承天》][446] | [JSON](vpy_180_2oi.json) |
| `A` | 珪〔裴松之父〕 | [《南史・范泰　荀伯子　徐廣　鄭鮮之　裴松之　何承天》][244]、[《宋書・鄭鮮之 裴松之 何承天》][446] | [JSON](vpy_180_2oi_A.json) |
| `AA` | 裴松之 | [《南史・范泰　荀伯子　徐廣　鄭鮮之　裴松之　何承天》][244]、[《宋書・鄭鮮之 裴松之 何承天》][446] | [JSON](vpy_180_2oi_AA.json) |
| `AAA` | 駰〔裴松之子〕 | [《南史・范泰　荀伯子　徐廣　鄭鮮之　裴松之　何承天》][244] | [JSON](vpy_180_2oi_AAA.json) |
| `AAAA` | 昭明〔裴子野父〕 | [《南史・范泰　荀伯子　徐廣　鄭鮮之　裴松之　何承天》][244] | [JSON](vpy_180_2oi_AAAA.json) |
| `AAAAA` | 裴子野 | [《南史・范泰　荀伯子　徐廣　鄭鮮之　裴松之　何承天》][244] | [JSON](vpy_180_2oi_AAAAA.json) |
| `AAAAAA` | 謇〔子野子；南史作騫〕 | [《梁書・裴子野 顧協 徐摛 鮑泉》][131]、[《南史・范泰　荀伯子　徐廣　鄭鮮之　裴松之　何承天》][244] | [JSON](vpy_180_2oi_AAAAAA.json) |

</details>

<details><summary><code>vs4_n7e_1qh</code> 武（曹繆公）（8 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 武（曹繆公） | [《史記・管蔡世家》][281] | [JSON](vs4_n7e_1qh.json) |
| `A` | 終生（曹桓公） | [《史記・管蔡世家》][281] | [JSON](vs4_n7e_1qh_A.json) |
| `AA` | 夕姑（曹莊公） | [《史記・管蔡世家》][281] | [JSON](vs4_n7e_1qh_AA.json) |
| `AAA` | 夷（曹釐公） | [《史記・管蔡世家》][281] | [JSON](vs4_n7e_1qh_AAA.json) |
| `AAAA` | 班（曹昭公） | [《史記・管蔡世家》][281] | [JSON](vs4_n7e_1qh_AAAA.json) |
| `AAAAA` | 襄（曹共公） | [《史記・管蔡世家》][281] | [JSON](vs4_n7e_1qh_AAAAA.json) |
| `AAAAAA` | 壽（曹文公） | [《史記・管蔡世家》][281] | [JSON](vs4_n7e_1qh_AAAAAA.json) |
| `AAAAAAA` | 彊（曹宣公） | [《史記・管蔡世家》][281] | [JSON](vs4_n7e_1qh_AAAAAAA.json) |

</details>

<details><summary><code>vs9_1es_k35</code> 田氏（鄭阿春前夫）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 田氏（鄭阿春前夫） | [《晉書・后妃下》][63] | [JSON](vs9_1es_k35.json) |
| `A` | 鄭阿春前婚所生子（未名） | [《晉書・后妃下》][63] | [JSON](vs9_1es_k35_A.json) |

</details>

<details><summary><code>vtu_yuj_kdz</code> 齊王建（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 齊王建 | [《史記・秦始皇本紀》][270]、[《史記・田儋列傳》][340] | [JSON](vtu_yuj_kdz.json) |
| `*A` | 田安 | [《史記・項羽本紀》][271]、[《史記・田儋列傳》][340] | [JSON](vtu_yuj_kdz_%2AA.json) |

</details>

<details><summary><code>vty_3n0_0ed</code> 病疽卒父（孫吳列傳候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 病疽卒父 | [《史記・孫子吳起列傳》][311] | [JSON](vty_3n0_0ed.json) |
| `A` | 病疽卒 | [《史記・孫子吳起列傳》][311] | [JSON](vty_3n0_0ed_A.json) |

</details>

<details><summary><code>vwy_7cv_69j</code> 桓子（趙世家候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 桓子 | [《史記・趙世家》][289] | [JSON](vwy_7cv_69j.json) |
| `A` | 桓子之子（趙世家未名者） | [《史記・趙世家》][289] | [JSON](vwy_7cv_69j_A.json) |

</details>

<details><summary><code>w44_37v_bcb</code> 和（宋穆公）（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 和（宋穆公） | [《史記・宋微子世家》][284] | [JSON](w44_37v_bcb.json) |
| `A` | 馮（宋莊公） | [《史記・宋微子世家》][284] | [JSON](w44_37v_bcb_A.json) |
| `AA` | 捷（宋湣公） | [《史記・宋微子世家》][284] | [JSON](w44_37v_bcb_AA.json) |

</details>

<details><summary><code>w4m_9tw_147</code> 齊明帝鸞（5 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 齊明帝鸞 | [《南齊書・江斆 何昌㝢 謝𤅢 王思遠》][163] | [JSON](w4m_9tw_147.json) |
| `A` | 蕭寶卷 | [《北史・司馬休之 司馬楚之 劉昶 蕭寶夤 蕭正表 蕭祗 蕭退 蕭泰 蕭撝 蕭圓肅 蕭大圜》][3]、[《梁書・王瞻 王志 王峻 王暕 子訓 王泰 王份 孫鍚 僉 張充 柳惲 蔡撙 江蒨》][128]、[《梁書・王瞻 王志 王峻 王暕 子訓 王泰 王份 孫鍚 僉 張充 柳惲 蔡撙 江蒨》][127]、[《梁書・謝朏 弟子覽》][120]、[《南齊書・東昏侯》][141]、[《南史・王曇首》][234]、[《南史・王曇首》][233]、[《魏書・劉昶 蕭寶夤 蕭正表》][479] | [JSON](w4m_9tw_147_A.json) |
| `B` | 蕭寶玄 | [《南齊書・明帝》][140]、[《南齊書・王融 謝朓》][168]、[《南齊書・文二王 明七王》][172]、[《南史・謝晦　謝裕　謝方明　謝靈運》][194] | [JSON](w4m_9tw_147_B.json) |
| `C` | 蕭寶義 | [《南齊書・文二王 明七王》][172] | [JSON](w4m_9tw_147_C.json) |
| `D` | 蕭寶夤（字智亮） | [《魏書・楊播》][477] | [JSON](w4m_9tw_147_D.json) |

</details>

<details><summary><code>w8j_vnd_rs4</code> 傅寬（4 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 傅寬 | [《漢書・樊酈滕灌傅靳周傳》][24] | [JSON](w8j_vnd_rs4.json) |
| `A` | 傅精 | [《史記・傅靳蒯成列傳》][344]、[《史記・高祖功臣侯者年表》][499] | [JSON](w8j_vnd_rs4_A.json) |
| `AA` | 傅則 | [《史記・傅靳蒯成列傳》][344]、[《史記・高祖功臣侯者年表》][499] | [JSON](w8j_vnd_rs4_AA.json) |
| `AAA` | 傅偃 | [《史記・高祖功臣侯者年表》][499] | [JSON](w8j_vnd_rs4_AAA.json) |

</details>

<details><summary><code>wjt_htu_081</code> 頭曼（匈奴列傳）（13 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 頭曼（匈奴列傳） | [《史記・匈奴列傳》][356] | [JSON](wjt_htu_081.json) |
| `A` | 冒頓（匈奴列傳第6段） | [《史記・匈奴列傳》][356] | [JSON](wjt_htu_081_A.json) |
| `AA` | 稽粥（匈奴列傳第18至20段） | [《史記・匈奴列傳》][356] | [JSON](wjt_htu_081_AA.json) |
| `AAA` | 軍臣（匈奴列傳第27段） | [《史記・匈奴列傳》][356] | [JSON](wjt_htu_081_AAA.json) |
| `AAAA` | 於單（匈奴列傳第31至32段） | [《史記・匈奴列傳》][356] | [JSON](wjt_htu_081_AAAA.json) |
| `AAB` | 伊稚斜（匈奴列傳第31至32段） | [《史記・衛將軍驃騎列傳》][357] | [JSON](wjt_htu_081_AAB.json) |
| `AABA` | 烏維（匈奴列傳第42至43段） | [《史記・匈奴列傳》][356] | [JSON](wjt_htu_081_AABA.json) |
| `AABAA` | 烏師廬（匈奴列傳第49段） | [《史記・匈奴列傳》][356] | [JSON](wjt_htu_081_AABAA.json) |
| `AABAAA` | 兒單于之子（未名） | [《史記・匈奴列傳》][356] | [JSON](wjt_htu_081_AABAAA.json) |
| `AABB` | 呴犁湖（匈奴列傳第53段） | [《史記・匈奴列傳》][356] | [JSON](wjt_htu_081_AABB.json) |
| `AABC` | 且鞮侯（匈奴列傳第56段） | [《史記・匈奴列傳》][356] | [JSON](wjt_htu_081_AABC.json) |
| `AABCA` | 且鞮侯之女（未名，妻李陵者） | [《史記・李將軍列傳》][355]、[《史記・匈奴列傳》][356] | [JSON](wjt_htu_081_AABCA.json) |
| `B` | 少子（匈奴列傳第6段） | [《史記・匈奴列傳》][356] | [JSON](wjt_htu_081_B.json) |

</details>

<details><summary><code>wtu_qvi_0rz</code> 李矩（李充父）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 李矩（李充父） | [《晉書・文苑》][103] | [JSON](wtu_qvi_0rz.json) |
| `A` | 李充 | [《晉書・文苑》][103] | [JSON](wtu_qvi_0rz_A.json) |

</details>

<details><summary><code>wuz_yxe_b9k</code> 齊景公（4 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 齊景公 | [《史記・齊太公世家》][278] | [JSON](wuz_yxe_b9k.json) |
| `A` | 齊悼公 | [《史記・齊太公世家》][278] | [JSON](wuz_yxe_b9k_A.json) |
| `AA` | 齊簡公 | [《史記・齊太公世家》][278] | [JSON](wuz_yxe_b9k_AA.json) |
| `B` | 孺子（齊） | [《史記・齊太公世家》][278] | [JSON](wuz_yxe_b9k_B.json) |

</details>

<details><summary><code>x3q_cqm_dup</code> 竟陵王子良（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 竟陵王子良 | [《南史・王弘》][206] | [JSON](x3q_cqm_dup.json) |
| `A` | 蕭昭胄 | [《南史・袁湛》][242] | [JSON](x3q_cqm_dup_A.json) |

</details>

<details><summary><code>x50_1p7_qkk</code> 魯莊公（10 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 魯莊公 | [《史記・魯周公世家》][279] | [JSON](x50_1p7_qkk.json) |
| `A` | 魯湣公 | [《史記・魯周公世家》][279] | [JSON](x50_1p7_qkk_A.json) |
| `B` | 魯釐公 | [《史記・魯周公世家》][279] | [JSON](x50_1p7_qkk_B.json) |
| `BA` | 興（魯文公） | [《史記・魯周公世家》][279] | [JSON](x50_1p7_qkk_BA.json) |
| `BAA` | 惡（文公子） | [《史記・魯周公世家》][279] | [JSON](x50_1p7_qkk_BAA.json) |
| `BAB` | 視（文公子） | [《史記・魯周公世家》][279] | [JSON](x50_1p7_qkk_BAB.json) |
| `BAC` | 俀（魯宣公） | [《史記・魯周公世家》][279] | [JSON](x50_1p7_qkk_BAC.json) |
| `BACA` | 黑肱（魯成公） | [《史記・魯周公世家》][279] | [JSON](x50_1p7_qkk_BACA.json) |
| `BACAA` | 午（魯襄公） | [《史記・魯周公世家》][279] | [JSON](x50_1p7_qkk_BACAA.json) |
| `C` | 斑（莊公子） | [《史記・魯周公世家》][279] | [JSON](x50_1p7_qkk_C.json) |

</details>

<details><summary><code>xaa_ewn_4ro</code> 臧荼（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 臧荼 | [《史記・樊酈滕灌列傳》][341] | [JSON](xaa_ewn_4ro.json) |
| `A` | 衍（臧荼子） | [《史記・韓信盧綰列傳》][339] | [JSON](xaa_ewn_4ro_A.json) |

</details>

<details><summary><code>xd8_uww_5ok</code> 蕭何（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 蕭何 | [《史記・蕭相國世家》][299] | [JSON](xd8_uww_5ok.json) |
| `*A` | 系（蕭何孫） | [《史記・孝景本紀》][275] | [JSON](xd8_uww_5ok_%2AA.json) |

</details>

<details><summary><code>xgd_r31_cmr</code> 崔杼（4 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 崔杼 | [《史記・齊太公世家》][278] | [JSON](xgd_r31_cmr.json) |
| `A` | 成（崔杼子） | [《史記・齊太公世家》][278] | [JSON](xgd_r31_cmr_A.json) |
| `B` | 彊（崔杼子） | [《史記・齊太公世家》][278] | [JSON](xgd_r31_cmr_B.json) |
| `C` | 明（崔杼子） | [《史記・齊太公世家》][278] | [JSON](xgd_r31_cmr_C.json) |

</details>

<details><summary><code>xgx_g4a_c28</code> 趙兼（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 趙兼 | [《史記・孝文本紀》][274]、[《史記・淮南衡山列傳》][364]、[《史記・酷吏列傳》][368]、[《史記・惠景間侯者年表》][500] | [JSON](xgx_g4a_c28.json) |
| `A` | 周陽由 | [《史記・酷吏列傳》][368] | [JSON](xgx_g4a_c28_A.json) |

</details>

<details><summary><code>xke_dj3_6ba</code> 褚䂮（10 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 褚䂮 | [《晉書・王沈 荀顗 荀勖 馮紞》][68]、[《晉書・外戚》][104] | [JSON](xke_dj3_6ba.json) |
| `A` | 褚洽 | [《晉書・外戚》][104] | [JSON](xke_dj3_6ba_A.json) |
| `AA` | 褚裒 | [《晉書・外戚》][104] | [JSON](xke_dj3_6ba_AA.json) |
| `AAA` | 褚歆 | [《晉書・外戚》][104] | [JSON](xke_dj3_6ba_AAA.json) |
| `AAAA` | 褚爽 | [《晉書・外戚》][105] | [JSON](xke_dj3_6ba_AAAA.json) |
| `AAAAA` | 褚秀之 | [《晉書・外戚》][105] | [JSON](xke_dj3_6ba_AAAAA.json) |
| `AAAAB` | 褚炎之 | [《晉書・外戚》][105] | [JSON](xke_dj3_6ba_AAAAB.json) |
| `AAAAC` | 褚喻之 | [《晉書・外戚》][105] | [JSON](xke_dj3_6ba_AAAAC.json) |
| `AAAAD` | 褚靈媛 | [《晉書・后妃下》][58] | [JSON](xke_dj3_6ba_AAAAD.json) |
| `AAB` | 褚蒜子 | [《晉書・后妃下》][59] | [JSON](xke_dj3_6ba_AAB.json) |

</details>

<details><summary><code>xny_prn_zyi</code> 酈商（6 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 酈商 | [《史記・樊酈滕灌列傳》][341] | [JSON](xny_prn_zyi.json) |
| `A` | 酈寄 | [《史記・樊酈滕灌列傳》][341] | [JSON](xny_prn_zyi_A.json) |
| `B` | 酈堅 | [《史記・樊酈滕灌列傳》][341] | [JSON](xny_prn_zyi_B.json) |
| `BA` | 酈遂成 | [《史記・樊酈滕灌列傳》][341] | [JSON](xny_prn_zyi_BA.json) |
| `BAA` | 酈世宗 | [《史記・樊酈滕灌列傳》][341] | [JSON](xny_prn_zyi_BAA.json) |
| `BAAA` | 酈終根 | [《史記・樊酈滕灌列傳》][341] | [JSON](xny_prn_zyi_BAAA.json) |

</details>

<details><summary><code>xrt_zof_cbt</code> 和（衛武公）（4 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 和（衛武公） | [《史記・衛康叔世家》][283] | [JSON](xrt_zof_cbt.json) |
| `A` | 揚（衛莊公） | [《史記・衛康叔世家》][283] | [JSON](xrt_zof_cbt_A.json) |
| `AA` | 州吁（衛君） | [《史記・衛康叔世家》][283] | [JSON](xrt_zof_cbt_AA.json) |
| `AB` | 完（衛桓公） | [《史記・衛康叔世家》][283] | [JSON](xrt_zof_cbt_AB.json) |

</details>

<details><summary><code>xxh_xtr_3f9</code> 袁豹（5 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 袁豹 | [《宋書・庾悅 王誕 謝景仁 袁湛 褚叔度》][431] | [JSON](xxh_xtr_3f9.json) |
| `A` | 袁洵 | [《南齊書・袁彖 孔稚珪 劉繪》][169]、[《宋書・庾悅 王誕 謝景仁 袁湛 褚叔度》][431] | [JSON](xxh_xtr_3f9_A.json) |
| `AA` | 袁顗 | [《南史・袁湛》][242]、[《宋書・庾悅 王誕 謝景仁 袁湛 褚叔度》][431] | [JSON](xxh_xtr_3f9_AA.json) |
| `AB` | 袁覬 | [《南齊書・袁彖 孔稚珪 劉繪》][169]、[《南史・袁湛》][242]、[《宋書・庾悅 王誕 謝景仁 袁湛 褚叔度》][431] | [JSON](xxh_xtr_3f9_AB.json) |
| `ABA` | 袁氏（竟陵王子良妃） | [《南齊書・皇后》][144]、[《南齊書・武十七王》][161]、[《南史・后妃上》][176] | [JSON](xxh_xtr_3f9_ABA.json) |

</details>

<details><summary><code>y0c_hok_598</code> 李同父未名（平原君虞卿列傳候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 李同父未名 | [《史記・平原君虞卿列傳》][322] | [JSON](y0c_hok_598.json) |
| `A` | 李同 | [《史記・平原君虞卿列傳》][322] | [JSON](y0c_hok_598_A.json) |

</details>

<details><summary><code>y3i_rsz_brn</code> 韓厥（14 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 韓厥 | [《史記・韓世家》][291] | [JSON](y3i_rsz_brn.json) |
| `A` | 韓宣子 | [《史記・韓世家》][291] | [JSON](y3i_rsz_brn_A.json) |
| `AA` | 韓貞子 | [《史記・韓世家》][291] | [JSON](y3i_rsz_brn_AA.json) |
| `AAA` | 韓簡子 | [《史記・韓世家》][291] | [JSON](y3i_rsz_brn_AAA.json) |
| `AAAA` | 韓莊子 | [《史記・韓世家》][291] | [JSON](y3i_rsz_brn_AAAA.json) |
| `AAAAA` | 韓康子 | [《史記・韓世家》][291] | [JSON](y3i_rsz_brn_AAAAA.json) |
| `AAAAAA` | 武子 | [《史記・韓世家》][291] | [JSON](y3i_rsz_brn_AAAAAA.json) |
| `AAAAAAA` | 虔 | [《史記・韓世家》][291] | [JSON](y3i_rsz_brn_AAAAAAA.json) |
| `AAAAAAAA` | 取 | [《史記・韓世家》][291] | [JSON](y3i_rsz_brn_AAAAAAAA.json) |
| `AAAAAAAAA` | 韓文侯 | [《史記・韓世家》][291] | [JSON](y3i_rsz_brn_AAAAAAAAA.json) |
| `AAAAAAAAAA` | 韓哀侯 | [《史記・韓世家》][291] | [JSON](y3i_rsz_brn_AAAAAAAAAA.json) |
| `AAAAAAAAAAA` | 韓懿侯 | [《史記・韓世家》][291] | [JSON](y3i_rsz_brn_AAAAAAAAAAA.json) |
| `AAAAAAAAAAAA` | 韓昭侯 | [《史記・韓世家》][291] | [JSON](y3i_rsz_brn_AAAAAAAAAAAA.json) |
| `AAAAAAAAAAAAA` | 宣惠王 | [《史記・韓世家》][291] | [JSON](y3i_rsz_brn_AAAAAAAAAAAAA.json) |

</details>

<details><summary><code>y3u_i0l_ztj</code> 韓宣王（趙世家候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 韓宣王 | [《史記・趙世家》][289] | [JSON](y3u_i0l_ztj.json) |
| `A` | 倉 | [《史記・趙世家》][289] | [JSON](y3u_i0l_ztj_A.json) |

</details>

[1]: https://zh.wikisource.org/w/index.php?title=北史/卷016&oldid=1518816
[3]: https://zh.wikisource.org/w/index.php?oldid=11071379
[4]: https://zh.wikisource.org/w/index.php?title=北史/卷042&oldid=2626092
[5]: https://zh.wikisource.org/w/index.php?title=北史/卷044&oldid=2183262
[6]: https://zh.wikisource.org/w/index.php?title=北史/卷044&oldid=2183262
[7]: https://zh.wikisource.org/w/index.php?title=冊府元龜_(四庫全書本)/全覽10&oldid=650326
[8]: https://zh.wikisource.org/w/index.php?title=陳書/卷17&oldid=1544244
[9]: https://zh.wikisource.org/w/index.php?title=陳書/卷18&oldid=2132778
[10]: https://zh.wikisource.org/w/index.php?title=陳書/卷21&oldid=1511909
[11]: https://www.sohu.com/a/260163234_770283
[12]: https://guji.10huan.com/Article/7147_7165.html
[13]: https://www.i-repository.net/il/cont/01/G0000721f/000/756/000756292.jpg
[14]: https://homepage.ntu.edu.tw/~history/public_html/newsletter/public_html/09newsletter/03/newsletter3_09.pdf#page=3
[15]: https://www.sohu.com/a/279761580_738227
[16]: http://csid.zju.edu.cn/tomb/stone/detail?id=40288b955bd07752015bfb74a80002de
[17]: https://www.i-repository.net/il/cont/01/G0000721f/000/756/000756311.jpg
[22]: https://github.com/kanripo/KR2a0007/blob/683113d4baf6febecaf2ccb7913df87c4d68d454/KR2a0007_007.txt
[24]: https://zh.wikisource.org/w/index.php?title=漢書/卷041&oldid=2342290
[25]: https://github.com/kanripo/KR2a0007/blob/683113d4baf6febecaf2ccb7913df87c4d68d454/KR2a0007_050.txt
[26]: https://github.com/kanripo/KR2a0007/blob/683113d4baf6febecaf2ccb7913df87c4d68d454/KR2a0007_059.txt
[30]: https://github.com/kanripo/KR2a0007/blob/683113d4baf6febecaf2ccb7913df87c4d68d454/KR2a0007_098.txt
[31]: https://github.com/kanripo/KR2a0009/blob/6db36b6dcbe843b825354c22e9be9193d0137c04/KR2a0009_009.txt
[33]: https://github.com/kanripo/KR2a0009/blob/6db36b6dcbe843b825354c22e9be9193d0137c04/KR2a0009_092.txt
[34]: https://github.com/kanripo/KR2a0009/blob/6db36b6dcbe843b825354c22e9be9193d0137c04/KR2a0009_094.txt
[37]: https://zh.wikisource.org/w/index.php?oldid=2603565
[41]: https://zh.wikisource.org/w/index.php?oldid=7904721
[49]: https://raw.githubusercontent.com/kanripo/KR2a0015/82291520954e5af1fdade894971a2f5810fd4e31/KR2a0015_008.txt
[54]: https://zh.wikisource.org/w/index.php?oldid=2567072
[58]: https://zh.wikisource.org/w/index.php?oldid=1543614
[59]: https://zh.wikisource.org/w/index.php?oldid=1543614
[60]: https://zh.wikisource.org/w/index.php?title=%E6%99%89%E6%9B%B8%2F%E5%8D%B7032&oldid=1543614
[62]: https://zh.wikisource.org/w/index.php?oldid=1543614
[63]: https://zh.wikisource.org/w/index.php?title=%E6%99%89%E6%9B%B8%2F%E5%8D%B7032&oldid=1543614
[64]: https://zh.wikisource.org/w/index.php?title=%E6%99%89%E6%9B%B8%2F%E5%8D%B7033&oldid=2650519
[65]: https://zh.wikisource.org/w/index.php?title=%E6%99%89%E6%9B%B8%2F%E5%8D%B7035&oldid=2506399
[66]: https://zh.wikisource.org/w/index.php?title=%E6%99%89%E6%9B%B8%2F%E5%8D%B7037&oldid=2630018
[67]: https://zh.wikisource.org/w/index.php?oldid=2444513
[68]: https://zh.wikisource.org/w/index.php?title=晉書/卷039&oldid=2108782
[69]: https://zh.wikisource.org/w/index.php?title=晉書/卷042&oldid=2180524
[70]: https://zh.wikisource.org/w/index.php?oldid=2618531
[71]: https://zh.wikisource.org/w/index.php?oldid=2618531
[73]: https://zh.wikisource.org/w/index.php?title=晉書/卷043&oldid=2618531
[76]: https://zh.wikisource.org/w/index.php?title=晉書/卷059&oldid=2650517
[78]: https://zh.wikisource.org/w/index.php?title=晉書/卷059&oldid=2650517
[79]: https://zh.wikisource.org/w/index.php?title=%E6%99%89%E6%9B%B8%2F%E5%8D%B7061&oldid=7903772
[80]: https://zh.wikisource.org/w/index.php?title=%E6%99%89%E6%9B%B8%2F%E5%8D%B7064&oldid=2622004
[82]: https://zh.wikisource.org/w/index.php?title=%E6%99%89%E6%9B%B8%2F%E5%8D%B7065&oldid=1756144
[83]: https://zh.wikisource.org/w/index.php?oldid=1527632
[84]: https://zh.wikisource.org/w/index.php?title=%E6%99%89%E6%9B%B8%2F%E5%8D%B7069&oldid=2012453
[85]: https://zh.wikisource.org/w/index.php?oldid=2296501
[86]: https://zh.wikisource.org/w/index.php?oldid=2296501
[87]: https://zh.wikisource.org/w/index.php?title=晉書/卷074&oldid=1536331
[88]: https://zh.wikisource.org/w/index.php?title=晉書/卷075&oldid=2645530
[90]: https://zh.wikisource.org/w/index.php?title=晉書/卷075&oldid=2645530
[91]: https://zh.wikisource.org/w/index.php?oldid=2180533
[92]: https://zh.wikisource.org/w/index.php?title=%E6%99%89%E6%9B%B8%2F%E5%8D%B7076&oldid=2180533
[93]: https://zh.wikisource.org/w/index.php?title=%E6%99%89%E6%9B%B8%2F%E5%8D%B7076&oldid=2180533
[94]: https://zh.wikisource.org/w/index.php?title=%E6%99%89%E6%9B%B8%2F%E5%8D%B7076&oldid=2180533
[95]: https://zh.wikisource.org/w/index.php?oldid=2180533
[96]: https://zh.wikisource.org/w/index.php?title=%E6%99%89%E6%9B%B8%2F%E5%8D%B7076&oldid=2180533
[97]: https://zh.wikisource.org/w/index.php?title=%E6%99%89%E6%9B%B8%2F%E5%8D%B7077&oldid=8750392
[98]: https://zh.wikisource.org/w/index.php?title=%E6%99%89%E6%9B%B8%2F%E5%8D%B7079&oldid=2645985
[99]: https://zh.wikisource.org/w/index.php?oldid=2603570
[100]: https://upload.wikimedia.org/wikipedia/commons/3/30/NLC016-HWRB201817005-3307_%E6%99%89%E6%9B%B8_%E4%B8%80%E7%99%BE%E4%B8%89%E5%8D%81%E5%8D%B7_%E9%9F%B3%E7%BE%A9%E4%B8%89%E5%8D%B7_%E7%AC%AC20%E5%86%8A.pdf#page=27
[101]: https://zh.wikisource.org/w/index.php?title=%E6%99%89%E6%9B%B8%2F%E5%8D%B7089&oldid=2835777
[102]: https://zh.wikisource.org/w/index.php?title=晉書/卷090&oldid=2835599
[103]: https://zh.wikisource.org/w/index.php?oldid=2835641
[104]: https://zh.wikisource.org/w/index.php?oldid=1548000
[105]: https://zh.wikisource.org/w/index.php?oldid=1548000
[107]: https://zh.wikisource.org/w/index.php?oldid=2625341
[109]: https://zh.wikisource.org/w/index.php?title=晉書/卷098&oldid=2614273
[110]: https://zh.wikisource.org/w/index.php?title=晉書/卷099&oldid=2644703
[112]: https://zh.wikisource.org/w/index.php?title=%E6%99%89%E6%9B%B8%2F%E5%8D%B7100&oldid=2614279
[113]: https://zh.wikisource.org/w/index.php?title=舊唐書/卷89&oldid=2589393
[115]: https://zh.wikisource.org/w/index.php?oldid=1729539
[116]: https://zh.wikisource.org/w/index.php?oldid=2401748
[118]: https://zh.wikisource.org/w/index.php?title=梁書/卷07&oldid=1566494
[120]: https://zh.wikisource.org/w/index.php?title=梁書/卷15&oldid=1506954
[121]: https://zh.wikisource.org/w/index.php?title=梁書/卷21&oldid=1544250
[122]: https://zh.wikisource.org/w/index.php?title=梁書/卷21&oldid=1544250
[123]: https://zh.wikisource.org/w/index.php?oldid=1544250
[125]: https://commons.wikimedia.org/w/index.php?oldid=902340163
[126]: https://zh.wikisource.org/w/index.php?oldid=1544250
[127]: https://commons.wikimedia.org/w/index.php?oldid=902340163
[128]: https://zh.wikisource.org/w/index.php?oldid=1544250
[129]: https://zh.wikisource.org/w/index.php?oldid=1513347
[130]: https://zh.wikisource.org/w/index.php?title=梁書/卷27&oldid=1511478
[131]: https://zh.wikisource.org/w/index.php?title=%E6%A2%81%E6%9B%B8%2F%E5%8D%B730&oldid=1508510
[132]: https://commons.wikimedia.org/wiki/File:NLC892-411999017142-12700_二十四史_第167冊.pdf
[133]: https://zh.wikisource.org/w/index.php?oldid=1514481
[134]: https://zh.wikisource.org/w/index.php?oldid=1511900
[135]: https://zh.wikisource.org/w/index.php?title=梁書/卷41&oldid=1512987
[136]: https://zh.wikisource.org/w/index.php?oldid=1512987
[138]: https://zh.wikisource.org/w/index.php?title=梁書/卷50&oldid=1514482
[139]: https://zh.wikisource.org/w/index.php?title=南齊書/卷2&oldid=2312009
[140]: https://zh.wikisource.org/w/index.php?title=南齊書/卷6&oldid=2311630
[141]: https://zh.wikisource.org/w/index.php?title=南齊書/卷7&oldid=2438183
[143]: https://zh.wikisource.org/w/index.php?title=南齊書/卷20&oldid=2074177
[144]: https://zh.wikisource.org/w/index.php?title=南齊書/卷20&oldid=2074177
[145]: https://zh.wikisource.org/w/index.php?title=南齊書/卷20&oldid=2074177
[146]: https://zh.wikisource.org/w/index.php?title=南齊書/卷23&oldid=1545488
[147]: https://zh.wikisource.org/w/index.php?title=南齊書/卷24&oldid=1507882
[149]: https://zh.wikisource.org/w/index.php?oldid=1513918
[150]: https://zh.wikisource.org/w/index.php?title=%E5%8D%97%E9%BD%8A%E6%9B%B8%2F%E5%8D%B732&oldid=1513918
[151]: https://github.com/kanripo/KR2a0017/blob/787dd9a7da495542e8f17c26c96900ce37b2c211/KR2a0017_033.txt
[152]: https://zh.wikisource.org/w/index.php?title=南齊書/卷33&oldid=1492444
[153]: https://zh.wikisource.org/w/index.php?oldid=1514487
[154]: https://zh.wikisource.org/w/index.php?oldid=2401782
[155]: https://zh.wikisource.org/w/index.php?title=南齊書/卷36&oldid=1492438
[157]: https://zh.wikisource.org/w/index.php?title=南齊書/卷39&oldid=1545485
[158]: https://zh.wikisource.org/w/index.php?oldid=2272748
[159]: https://zh.wikisource.org/w/index.php?oldid=2272748
[160]: https://zh.wikisource.org/w/index.php?oldid=2272748
[161]: https://zh.wikisource.org/w/index.php?title=南齊書/卷40&oldid=2272748
[162]: https://zh.wikisource.org/w/index.php?title=南齊書/卷42&oldid=1507997
[163]: https://zh.wikisource.org/w/index.php?title=南齊書/卷43&oldid=2400356
[164]: https://zh.wikisource.org/w/index.php?title=南齊書/卷44&oldid=1507959
[165]: https://zh.wikisource.org/w/index.php?title=南齊書/卷45&oldid=2273185
[166]: https://zh.wikisource.org/w/index.php?title=南齊書/卷45&oldid=2273185
[167]: https://zh.wikisource.org/w/index.php?title=%E5%8D%97%E9%BD%8A%E6%9B%B8%2F%E5%8D%B746&oldid=1511897
[168]: https://zh.wikisource.org/w/index.php?title=南齊書/卷47&oldid=1492435
[169]: https://zh.wikisource.org/w/index.php?title=南齊書/卷48&oldid=1511898
[170]: https://zh.wikisource.org/w/index.php?title=南齊書/卷49&oldid=2261984
[172]: https://zh.wikisource.org/w/index.php?title=南齊書/卷50&oldid=2272731
[173]: https://github.com/kanripo/KR2a0017/blob/787dd9a7da495542e8f17c26c96900ce37b2c211/KR2a0017_052.txt
[176]: https://zh.wikisource.org/w/index.php?title=南史/卷11&oldid=2288359
[178]: https://zh.wikisource.org/w/index.php?title=南史/卷11&oldid=2288359
[179]: https://zh.wikisource.org/w/index.php?title=南史/卷11&oldid=2288359
[180]: https://zh.wikisource.org/w/index.php?oldid=1531762
[182]: https://zh.wikisource.org/w/index.php?oldid=1531762
[184]: https://zh.wikisource.org/w/index.php?oldid=1531762
[188]: https://zh.wikisource.org/w/index.php?title=南史/卷19&oldid=1531762
[191]: https://zh.wikisource.org/w/index.php?title=南史/卷19&oldid=1531762
[192]: https://zh.wikisource.org/w/index.php?title=南史/卷19&oldid=1531762
[193]: https://zh.wikisource.org/w/index.php?title=南史/卷19&oldid=1531762
[194]: https://zh.wikisource.org/w/index.php?title=南史/卷19&oldid=1531762
[195]: https://zh.wikisource.org/w/index.php?title=南史/卷19&oldid=1531762
[196]: https://zh.wikisource.org/w/index.php?title=南史/卷19&oldid=1531762
[197]: https://zh.wikisource.org/w/index.php?title=南史/卷19&oldid=1531762
[198]: https://github.com/kanripo/KR2a0024/blob/3c7bdbb072bf8e1eb70d134a94570c4b8de058ea/KR2a0024_020.txt
[199]: https://zh.wikisource.org/w/index.php?oldid=513423
[201]: https://zh.wikisource.org/w/index.php?oldid=1752646
[202]: https://zh.wikisource.org/w/index.php?oldid=1752646
[203]: https://zh.wikisource.org/w/index.php?oldid=1752646
[205]: https://zh.wikisource.org/w/index.php?oldid=1752646
[206]: https://zh.wikisource.org/w/index.php?oldid=1752646
[207]: https://zh.wikisource.org/w/index.php?oldid=1752646
[208]: https://zh.wikisource.org/w/index.php?oldid=1752646
[210]: https://zh.wikisource.org/w/index.php?oldid=1752646
[211]: https://zh.wikisource.org/w/index.php?oldid=1752646
[212]: https://zh.wikisource.org/w/index.php?oldid=1752646
[213]: https://zh.wikisource.org/w/index.php?oldid=1752646
[214]: https://zh.wikisource.org/w/index.php?oldid=1752646
[216]: https://zh.wikisource.org/w/index.php?oldid=1477957
[217]: https://zh.wikisource.org/w/index.php?oldid=1477957
[218]: https://zh.wikisource.org/w/index.php?oldid=1477957
[219]: https://zh.wikisource.org/w/index.php?oldid=1477957
[221]: https://zh.wikisource.org/w/index.php?oldid=1477957
[222]: https://zh.wikisource.org/w/index.php?title=南史/卷22&oldid=1477957
[223]: https://zh.wikisource.org/w/index.php?oldid=1477957
[224]: https://commons.wikimedia.org/wiki/File:NLC892-411999017142-12360_二十四史_第246冊.pdf
[225]: https://zh.wikisource.org/w/index.php?title=南史/卷22&oldid=1477957
[226]: https://zh.wikisource.org/w/index.php?oldid=1477957
[229]: https://zh.wikisource.org/w/index.php?oldid=1477957
[230]: https://zh.wikisource.org/w/index.php?oldid=1477957
[231]: https://commons.wikimedia.org/wiki/File:NLC892-411999017142-12360_二十四史_第246冊.pdf
[232]: https://zh.wikisource.org/w/index.php?oldid=1477957
[233]: https://zh.wikisource.org/w/index.php?oldid=1477957
[234]: https://github.com/kanripo/KR2a0024/blob/3c7bdbb072bf8e1eb70d134a94570c4b8de058ea/KR2a0024_022.txt
[235]: https://zh.wikisource.org/w/index.php?title=南史/卷23&oldid=2478204
[236]: https://zh.wikisource.org/w/index.php?title=南史/卷23&oldid=2478204
[238]: https://zh.wikisource.org/w/index.php?oldid=2478204
[239]: https://zh.wikisource.org/w/index.php?title=南史/卷23&oldid=2478204
[240]: https://zh.wikisource.org/w/index.php?oldid=2478204
[241]: https://zh.wikisource.org/w/index.php?title=%E5%8D%97%E5%8F%B2%2F%E5%8D%B724&oldid=1765279
[242]: https://zh.wikisource.org/w/index.php?title=南史/卷26&oldid=1477359
[243]: https://zh.wikisource.org/w/index.php?title=南史/卷31&oldid=8730255
[244]: https://zh.wikisource.org/w/index.php?title=%E5%8D%97%E5%8F%B2%2F%E5%8D%B733&oldid=1554233
[245]: https://zh.wikisource.org/w/index.php?title=南史/卷33&oldid=1554233
[248]: https://zh.wikisource.org/w/index.php?title=南史/卷44&oldid=2027785
[249]: https://zh.wikisource.org/w/index.php?title=南史/卷48&oldid=2493997
[250]: https://zh.wikisource.org/w/index.php?oldid=1553912
[251]: https://raw.githubusercontent.com/kanripo/KR2a0012/214fcafa79894355909c9d8c2c1533089e7791c6/KR2a0012_009.txt
[252]: https://raw.githubusercontent.com/kanripo/KR2a0012/214fcafa79894355909c9d8c2c1533089e7791c6/KR2a0012_009.txt
[253]: https://da.library.pref.osaka.jp/api/items/01-0015983/manifest.json
[254]: https://github.com/kanripo/KR2a0012/blob/214fcafa79894355909c9d8c2c1533089e7791c6/KR2a0012_010.txt
[255]: https://zh.wikisource.org/w/index.php?title=三國志/卷11&oldid=2373044
[257]: https://raw.githubusercontent.com/kanripo/KR2a0012/214fcafa79894355909c9d8c2c1533089e7791c6/KR2a0012_015.txt
[258]: https://github.com/kanripo/KR2a0012/blob/214fcafa79894355909c9d8c2c1533089e7791c6/KR2a0012_019.txt
[259]: https://raw.githubusercontent.com/kanripo/KR2a0012/214fcafa79894355909c9d8c2c1533089e7791c6/KR2a0012_022.txt
[260]: https://raw.githubusercontent.com/kanripo/KR2a0012/214fcafa79894355909c9d8c2c1533089e7791c6/KR2a0012_022.txt
[262]: https://github.com/kanripo/KR2a0012/blob/214fcafa79894355909c9d8c2c1533089e7791c6/KR2a0012_027.txt
[263]: https://github.com/kanripo/KR2a0012/blob/214fcafa79894355909c9d8c2c1533089e7791c6/KR2a0012_028.txt
[267]: https://zh.wikisource.org/w/index.php?title=史記/卷003&oldid=7909145
[268]: https://zh.wikisource.org/w/index.php?title=史記/卷004&oldid=7909147
[269]: https://zh.wikisource.org/w/index.php?title=史記/卷005&oldid=8744286
[270]: https://zh.wikisource.org/w/index.php?title=史記/卷006&oldid=7907969
[271]: https://zh.wikisource.org/w/index.php?title=史記/卷007&oldid=5978360
[272]: https://zh.wikisource.org/w/index.php?title=史記/卷008&oldid=2440965
[273]: https://zh.wikisource.org/w/index.php?title=史記/卷009&oldid=2087062
[274]: https://zh.wikisource.org/w/index.php?title=史記/卷010&oldid=2599229
[275]: https://zh.wikisource.org/w/index.php?title=史記/卷011&oldid=2520527
[277]: https://zh.wikisource.org/w/index.php?title=史記/卷031&oldid=7909287
[278]: https://zh.wikisource.org/w/index.php?title=史記/卷032&oldid=445042
[279]: https://zh.wikisource.org/w/index.php?title=史記/魯周公世家&oldid=7909289
[280]: https://zh.wikisource.org/w/index.php?title=史記/卷034&oldid=2559287
[281]: https://zh.wikisource.org/w/index.php?title=史記/卷035&oldid=8737302
[282]: https://zh.wikisource.org/w/index.php?title=史記/卷036&oldid=2588525
[283]: https://zh.wikisource.org/w/index.php?title=史記/卷037&oldid=5977124
[284]: https://zh.wikisource.org/w/index.php?title=史記/卷038&oldid=8737306
[285]: https://zh.wikisource.org/w/index.php?title=史記/卷039&oldid=2588534
[286]: https://zh.wikisource.org/w/index.php?title=史記/卷040&oldid=8736796
[287]: https://zh.wikisource.org/w/index.php?title=史記/卷041&oldid=2018395
[288]: https://zh.wikisource.org/w/index.php?title=史記/卷042&oldid=2016409
[289]: https://zh.wikisource.org/w/index.php?title=史記/卷043&oldid=7903603
[290]: https://zh.wikisource.org/w/index.php?title=史記/卷044&oldid=7903606
[291]: https://zh.wikisource.org/w/index.php?title=史記/卷045&oldid=7903607
[292]: https://zh.wikisource.org/w/index.php?title=史記/卷046&oldid=2560838
[293]: https://zh.wikisource.org/w/index.php?title=史記/卷047&oldid=7903609
[295]: https://zh.wikisource.org/w/index.php?title=史記/卷049&oldid=7903610
[297]: https://zh.wikisource.org/w/index.php?title=史記/卷051&oldid=2380315
[298]: https://zh.wikisource.org/w/index.php?title=史記/卷052&oldid=5977113
[299]: https://zh.wikisource.org/w/index.php?title=史記/卷053&oldid=2087971
[300]: https://zh.wikisource.org/w/index.php?title=史記/卷054&oldid=1490182
[301]: https://zh.wikisource.org/w/index.php?title=史記/卷055&oldid=2666612
[302]: https://zh.wikisource.org/w/index.php?title=史記/卷056&oldid=1961615
[303]: https://zh.wikisource.org/w/index.php?title=史記/卷057&oldid=1569360
[304]: https://zh.wikisource.org/w/index.php?title=史記/卷058&oldid=8735555
[309]: https://zh.wikisource.org/w/index.php?title=史記/卷063&oldid=7903601
[311]: https://zh.wikisource.org/w/index.php?title=史記/卷065&oldid=2567048
[312]: https://zh.wikisource.org/w/index.php?title=史記/卷066&oldid=2621138
[313]: https://zh.wikisource.org/w/index.php?title=史記/卷067&oldid=7869003
[315]: https://zh.wikisource.org/w/index.php?title=史記/卷069&oldid=2621145
[317]: https://zh.wikisource.org/w/index.php?title=史記/卷071&oldid=2621152
[319]: https://zh.wikisource.org/w/index.php?title=史記/卷073&oldid=7909285
[321]: https://zh.wikisource.org/w/index.php?title=史記/卷075&oldid=1965692
[322]: https://zh.wikisource.org/w/index.php?title=史記/卷076&oldid=7909284
[323]: https://zh.wikisource.org/w/index.php?title=史記/卷077&oldid=367917
[324]: https://zh.wikisource.org/w/index.php?title=史記/卷078&oldid=2089016
[325]: https://zh.wikisource.org/w/index.php?title=史記/卷079&oldid=2549307
[326]: https://zh.wikisource.org/w/index.php?title=史記/卷080&oldid=2089316
[330]: https://zh.wikisource.org/w/index.php?title=史記/卷084&oldid=1568305
[331]: https://zh.wikisource.org/w/index.php?title=史記/卷085&oldid=2027911
[332]: https://zh.wikisource.org/w/index.php?title=史記/卷086&oldid=2388562
[333]: https://zh.wikisource.org/w/index.php?title=史記/卷087&oldid=2364605
[334]: https://zh.wikisource.org/w/index.php?title=史記/卷088&oldid=1965690
[335]: https://zh.wikisource.org/w/index.php?title=史記/卷089&oldid=8744143
[337]: https://zh.wikisource.org/w/index.php?title=史記/卷091&oldid=2509940
[339]: https://zh.wikisource.org/w/index.php?title=史記/卷093&oldid=368019
[340]: https://zh.wikisource.org/w/index.php?title=史記/卷094&oldid=2171897
[341]: https://zh.wikisource.org/w/index.php?title=史記/卷095&oldid=2298709
[342]: https://zh.wikisource.org/w/index.php?title=史記/卷096&oldid=8770206
[343]: https://zh.wikisource.org/w/index.php?title=史記/卷097&oldid=1383195
[344]: https://zh.wikisource.org/w/index.php?title=史記/卷098&oldid=1490318
[346]: https://zh.wikisource.org/w/index.php?title=史記/卷100&oldid=1965696
[347]: https://zh.wikisource.org/w/index.php?title=史記/卷101&oldid=368092
[348]: https://zh.wikisource.org/w/index.php?title=史記/卷102&oldid=1753957
[349]: https://zh.wikisource.org/w/index.php?title=史記/卷103&oldid=2096814
[350]: https://zh.wikisource.org/w/index.php?title=史記/卷104&oldid=8739534
[351]: https://zh.wikisource.org/w/index.php?title=史記/卷105&oldid=8842726
[353]: https://zh.wikisource.org/w/index.php?title=史記/卷107&oldid=2540571
[355]: https://zh.wikisource.org/w/index.php?title=史記/卷109&oldid=1765440
[356]: https://zh.wikisource.org/w/index.php?title=史記/卷110&oldid=8735645
[357]: https://zh.wikisource.org/w/index.php?title=史記/卷111&oldid=8730225
[358]: https://zh.wikisource.org/w/index.php?title=史記/卷112&oldid=2089420
[359]: https://zh.wikisource.org/w/index.php?title=史記/卷113&oldid=8735632
[360]: https://zh.wikisource.org/w/index.php?title=史記/卷114&oldid=8735633
[361]: https://zh.wikisource.org/w/index.php?title=史記/卷115&oldid=439220
[362]: https://zh.wikisource.org/w/index.php?title=史記/卷116&oldid=7903636
[364]: https://zh.wikisource.org/w/index.php?title=史記/卷118&oldid=7904122
[365]: https://zh.wikisource.org/w/index.php?title=史記/卷119&oldid=7904123
[366]: https://zh.wikisource.org/w/index.php?title=史記/卷120&oldid=9166127
[367]: https://zh.wikisource.org/w/index.php?title=史記/卷121&oldid=8735621
[368]: https://zh.wikisource.org/w/index.php?title=史記/卷122&oldid=7904124
[369]: https://zh.wikisource.org/w/index.php?title=史記/卷123&oldid=8736799
[370]: https://zh.wikisource.org/w/index.php?title=史記/卷124&oldid=367994
[371]: https://zh.wikisource.org/w/index.php?title=史記/卷125&oldid=2273599
[372]: https://zh.wikisource.org/w/index.php?title=史記/卷126&oldid=2609358
[376]: https://zh.wikisource.org/w/index.php?title=史記/卷130&oldid=2609362
[378]: https://zh.wikisource.org/w/index.php?oldid=2567459
[380]: https://zh.wikisource.org/w/index.php?oldid=2567463
[389]: https://zh.wikisource.org/w/index.php?oldid=2567465
[399]: https://zh.wikisource.org/w/index.php?oldid=1532652
[402]: https://zh.wikisource.org/w/index.php?oldid=1532655
[410]: https://zh.wikisource.org/w/index.php?oldid=1503586
[411]: https://zh.wikisource.org/w/index.php?oldid=1503586
[412]: https://zh.wikisource.org/w/index.php?oldid=2004422
[413]: https://zh.wikisource.org/w/index.php?oldid=2004422
[418]: https://raw.githubusercontent.com/kanripo/KR2a0016/e80c057667e3c8684f11d5088251e10244d5a264/KR2a0016_001.txt
[422]: https://raw.githubusercontent.com/kanripo/KR2a0016/e80c057667e3c8684f11d5088251e10244d5a264/KR2a0016_041.txt
[423]: https://zh.wikisource.org/w/index.php?title=宋書/卷41&oldid=2634831
[424]: https://zh.wikisource.org/w/index.php?title=宋書/卷42&oldid=1478172
[425]: https://commons.wikimedia.org/w/index.php?title=File:NLC892-411999017142-12779_%E4%BA%8C%E5%8D%81%E5%9B%9B%E5%8F%B2_%E7%AC%AC144%E5%86%8A.pdf&oldid=979637198
[426]: https://zh.wikisource.org/w/index.php?title=%E5%AE%8B%E6%9B%B8/%E5%8D%B744&oldid=1746033
[428]: https://raw.githubusercontent.com/kanripo/KR2a0016/e80c057667e3c8684f11d5088251e10244d5a264/KR2a0016_046.txt
[429]: https://raw.githubusercontent.com/kanripo/KR2a0016/e80c057667e3c8684f11d5088251e10244d5a264/KR2a0016_046.txt
[431]: https://zh.wikisource.org/w/index.php?title=宋書/卷52&oldid=2190655
[432]: https://raw.githubusercontent.com/kanripo/KR2a0016/e80c057667e3c8684f11d5088251e10244d5a264/KR2a0016_053.txt
[433]: https://zh.wikisource.org/w/index.php?oldid=1996685
[434]: https://raw.githubusercontent.com/kanripo/KR2a0016/e80c057667e3c8684f11d5088251e10244d5a264/KR2a0016_053.txt
[435]: https://raw.githubusercontent.com/kanripo/KR2a0016/e80c057667e3c8684f11d5088251e10244d5a264/KR2a0016_056.txt
[437]: https://github.com/kanripo/KR2a0016/blob/e80c057667e3c8684f11d5088251e10244d5a264/KR2a0016_058.txt
[438]: https://raw.githubusercontent.com/kanripo/KR2a0016/e80c057667e3c8684f11d5088251e10244d5a264/KR2a0016_059.txt
[439]: https://zh.wikisource.org/w/index.php?title=宋書/卷60&oldid=1996694
[440]: https://zh.wikisource.org/w/index.php?title=%E5%AE%8B%E6%9B%B8/%E5%8D%B760&oldid=1996694
[442]: https://github.com/kanripo/KR2a0016/blob/e80c057667e3c8684f11d5088251e10244d5a264/KR2a0016_062.txt
[443]: https://zh.wikisource.org/w/index.php?title=宋書/卷63&oldid=2118589
[444]: https://commons.wikimedia.org/wiki/File:NLC892-411999017142-12245_二十四史_第147冊.pdf
[446]: https://zh.wikisource.org/w/index.php?title=%E5%AE%8B%E6%9B%B8%2F%E5%8D%B764&oldid=1748217
[447]: https://zh.wikisource.org/w/index.php?title=%E5%AE%8B%E6%9B%B8%2F%E5%8D%B766&oldid=2069104
[448]: https://raw.githubusercontent.com/kanripo/KR2a0016/e80c057667e3c8684f11d5088251e10244d5a264/KR2a0016_067.txt
[449]: https://zh.wikisource.org/w/index.php?title=宋書/卷71&oldid=2485515
[450]: https://commons.wikimedia.org/wiki/File:NLC892-411999017142-12246_二十四史_第148冊.pdf
[451]: https://github.com/kanripo/KR2a0016/blob/e80c057667e3c8684f11d5088251e10244d5a264/KR2a0016_071.txt
[452]: https://zh.wikisource.org/w/index.php?title=宋書/卷75&oldid=1997722
[453]: https://zh.wikisource.org/w/index.php?title=宋書/卷77&oldid=1997730
[454]: https://zh.wikisource.org/w/index.php?title=宋書/卷80&oldid=2261200
[456]: https://github.com/kanripo/KR2a0016/blob/e80c057667e3c8684f11d5088251e10244d5a264/KR2a0016_085.txt
[457]: https://zh.wikisource.org/w/index.php?title=宋書/卷86&oldid=2069103
[458]: https://zh.wikisource.org/w/index.php?title=宋書/卷87&oldid=2069105
[459]: https://zh.wikisource.org/w/index.php?title=宋書/卷88&oldid=2069210
[460]: https://zh.wikisource.org/w/index.php?title=宋書/卷88&oldid=2069210
[461]: https://zh.wikisource.org/w/index.php?title=宋書/卷88&oldid=2069210
[462]: https://zh.wikisource.org/w/index.php?title=宋書/卷88&oldid=2069210
[463]: https://zh.wikisource.org/w/index.php?title=%E5%AE%8B%E6%9B%B8%2F%E5%8D%B792&oldid=2195614
[464]: https://zh.wikisource.org/w/index.php?title=%E5%AE%8B%E6%9B%B8%2F%E5%8D%B793&oldid=1962755
[465]: https://zh.wikisource.org/w/index.php?title=隋書/卷76&oldid=2616529
[466]: https://zh.wikisource.org/w/index.php?oldid=2607174
[471]: https://zh.wikisource.org/w/index.php?title=魏書/卷18&oldid=1550395
[472]: https://zh.wikisource.org/w/index.php?title=魏書/卷24&oldid=2021236
[473]: https://raw.githubusercontent.com/kanripo/KR2a0020/17b6525eb5aaa878b9640f5a61e90da934ce5fc4/KR2a0020_024.txt
[474]: https://raw.githubusercontent.com/kanripo/KR2a0020/17b6525eb5aaa878b9640f5a61e90da934ce5fc4/KR2a0020_035.txt
[475]: https://github.com/kanripo/KR2a0020/blob/17b6525eb5aaa878b9640f5a61e90da934ce5fc4/KR2a0020_038.txt
[476]: https://zh.wikisource.org/w/index.php?title=%E9%AD%8F%E6%9B%B8%2F%E5%8D%B758&oldid=2087998
[477]: https://zh.wikisource.org/w/index.php?title=%E9%AD%8F%E6%9B%B8%2F%E5%8D%B758&oldid=2087998
[478]: https://zh.wikisource.org/w/index.php?title=%E9%AD%8F%E6%9B%B8%2F%E5%8D%B758&oldid=2087998
[479]: https://zh.wikisource.org/w/index.php?oldid=1504720
[480]: https://zh.wikisource.org/w/index.php?title=魏書/卷63&oldid=1513418
[481]: https://zh.wikisource.org/w/index.php?title=魏書/卷67&oldid=468068
[483]: https://zh.wikisource.org/w/index.php?title=%E6%96%B0%E5%94%90%E6%9B%B8%2F%E5%8D%B7071%E4%B8%8B&oldid=2405769
[484]: https://zh.wikisource.org/w/index.php?title=新唐書/卷116&oldid=3528844
[485]: https://zh.wikisource.org/w/index.php?oldid=2610515
[486]: https://zh.wikisource.org/w/index.php?title=周書/卷41&oldid=2432538
[487]: https://zh.wikisource.org/w/index.php?title=周書/卷48&oldid=2432546
[489]: https://zh.wikisource.org/w/index.php?title=%E8%B3%87%E6%B2%BB%E9%80%9A%E9%91%91/%E5%8D%B7094&oldid=2312212
[493]: https://github.com/kanripo/KR1e0004/blob/685a6ddca22d98535cac38038afdff7308273d23/KR1e0004_030.txt#L776-L776
[494]: https://zh.wikisource.org/w/index.php?title=史記/卷013&oldid=2606991
[495]: https://zh.wikisource.org/w/index.php?title=史記/卷014&oldid=2607001
[496]: https://zh.wikisource.org/w/index.php?title=史記/卷015&oldid=2607002
[497]: https://zh.wikisource.org/w/index.php?title=史記/卷016&oldid=2607007
[498]: https://zh.wikisource.org/w/index.php?title=史記/卷017&oldid=2607010
[499]: https://zh.wikisource.org/w/index.php?title=史記/卷018&oldid=9484995
[500]: https://zh.wikisource.org/w/index.php?title=史記/卷019&oldid=6359260
[501]: https://zh.wikisource.org/w/index.php?title=史記/卷020&oldid=2607036
