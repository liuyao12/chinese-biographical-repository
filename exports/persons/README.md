# 人物 JSON 索引

可重建匯出，涵蓋目前已標註資料，包含明示選用的暫定跨篇同指；原 ID、證據與判讀均保留。並非全部史料或完整覆核。

程式可讀取 [index.json](index.json)，再依各筆 `path` 取得人物資料。重新產生：`python3 scripts/export_person_bundles.py`。

出生排行與籍貫結構化欄位仍在逐篇回填；缺欄位不代表來源沒有此資訊。

漢劉氏的組裝見 [家族組裝資料](../../registry/family-assemblies.json)。`assembled_identity.person_id` 是共用家族根的組裝 ID，`source_person_ids` 保留各篇候選；父子及同指證據可由記錄 ID 回查。

點選家族標題可展開或收起後代。`*` 表示缺名世代，不建立人物，也不表示不同缺名位置是同一人。表內只列家族根後的 ID 尾碼；根人物以「根」表示，完整 ID 保留於家族標題及 JSON。最多提及來源另列一欄，同數並列；提及次數不代表史料優先權。舊 ID 與 JSON 入口保留為別名；索引只計現行人物。

尚未連入同族的人物見 [獨立人物索引](unconnected.md)。

## 可展開家族

<details><summary><code>04f_hzf_n06</code> 陳平（陳丞相世家候選）（5 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 陳平 | [《史記・陳丞相世家》][38] | [JSON](04f_hzf_n06.json) |
| `**A` | 陳掌 | [《史記・陳丞相世家》][38] | [JSON](04f_hzf_n06_%2A%2AA.json) |
| `A` | 買 | [《史記・陳丞相世家》][38] | [JSON](04f_hzf_n06_A.json) |
| `AA` | 恢 | [《史記・陳丞相世家》][38] | [JSON](04f_hzf_n06_AA.json) |
| `AAA` | 何 | [《史記・陳丞相世家》][38] | [JSON](04f_hzf_n06_AAA.json) |

</details>

<details><summary><code>04u_gq0_nke</code> 鼂錯父未名（袁盎鼂錯列傳候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 鼂錯父未名 | [《史記・袁盎鼂錯列傳》][83] | [JSON](04u_gq0_nke.json) |
| `A` | 鼂錯 | [《史記・袁盎鼂錯列傳》][83] | [JSON](04u_gq0_nke_A.json) |

</details>

<details><summary><code>06i_k5v_922</code> 申侯（鄭世家武姜父候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 申侯 | [《史記・鄭世家》][24] | [JSON](06i_k5v_922.json) |
| `A` | 武姜 | [《史記・鄭世家》][24] | [JSON](06i_k5v_922_A.json) |

</details>

<details><summary><code>0ad_dbw_97q</code> 晉昭公（4 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 晉昭公 | [《史記・晉世家》][21] | [JSON](0ad_dbw_97q.json) |
| `A` | 雍（戴子晉昭公子） | [《史記・晉世家》][21] | [JSON](0ad_dbw_97q_A.json) |
| `AA` | 忌（戴子子） | [《史記・晉世家》][21] | [JSON](0ad_dbw_97q_AA.json) |
| `AAA` | 驕（晉哀公） | [《史記・晉世家》][21] | [JSON](0ad_dbw_97q_AAA.json) |

</details>

<details><summary><code>0bu_skv_qsr</code> 呂青（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 呂青 | [《史記・項羽本紀》][7]、[《史記・高祖本紀》][8] | [JSON](0bu_skv_qsr.json) |
| `A` | 呂臣 | [《史記・項羽本紀》][7]、[《史記・高祖本紀》][8] | [JSON](0bu_skv_qsr_A.json) |

</details>

<details><summary><code>0hs_fg6_1qj</code> 田榮（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 田榮 | [《史記・田儋列傳》][76] | [JSON](0hs_fg6_1qj.json) |
| `A` | 廣（田榮子） | [《史記・高祖本紀》][8] | [JSON](0hs_fg6_1qj_A.json) |

</details>

<details><summary><code>0lu_mmj_s8t</code> 允常（越世家候選）（8 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 允常 | [《史記・越王勾踐世家》][23] | [JSON](0lu_mmj_s8t.json) |
| `A` | 句踐 | [《史記・越王勾踐世家》][23] | [JSON](0lu_mmj_s8t_A.json) |
| `AA` | 鼫與 | [《史記・越王勾踐世家》][23] | [JSON](0lu_mmj_s8t_AA.json) |
| `AAA` | 不壽 | [《史記・越王勾踐世家》][23] | [JSON](0lu_mmj_s8t_AAA.json) |
| `AAAA` | 翁 | [《史記・越王勾踐世家》][23] | [JSON](0lu_mmj_s8t_AAAA.json) |
| `AAAAA` | 翳 | [《史記・越王勾踐世家》][23] | [JSON](0lu_mmj_s8t_AAAAA.json) |
| `AAAAAA` | 之侯 | [《史記・越王勾踐世家》][23] | [JSON](0lu_mmj_s8t_AAAAAA.json) |
| `AAAAAAA` | 無彊 | [《史記・越王勾踐世家》][23] | [JSON](0lu_mmj_s8t_AAAAAAA.json) |

</details>

<details><summary><code>0s7_r72_j8q</code> 魯武公（4 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 魯武公 | [《史記・魯周公世家》][15] | [JSON](0s7_r72_j8q.json) |
| `A` | 括（魯武公長子） | [《史記・魯周公世家》][15] | [JSON](0s7_r72_j8q_A.json) |
| `AA` | 伯御（魯君） | [《史記・魯周公世家》][15] | [JSON](0s7_r72_j8q_AA.json) |
| `B` | 戲（魯懿公） | [《史記・魯周公世家》][15] | [JSON](0s7_r72_j8q_B.json) |

</details>

<details><summary><code>0us_j8h_to7</code> 假（老韓列傳候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 假 | [《史記・老子韓非列傳》][45] | [JSON](0us_j8h_to7.json) |
| `A` | 解 | [《史記・老子韓非列傳》][45] | [JSON](0us_j8h_to7_A.json) |

</details>

<details><summary><code>0va_zus_2zt</code> 商臣（楚穆王）（12 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 商臣（楚穆王） | [《史記・楚世家》][22] | [JSON](0va_zus_2zt.json) |
| `A` | 侶（楚莊王） | [《史記・楚世家》][22] | [JSON](0va_zus_2zt_A.json) |
| `AA` | 審（楚共王） | [《史記・楚世家》][22] | [JSON](0va_zus_2zt_AA.json) |
| `AAA` | 招（楚康王） | [《史記・楚世家》][22] | [JSON](0va_zus_2zt_AAA.json) |
| `AAAA` | 員（郟敖） | [《史記・楚世家》][22] | [JSON](0va_zus_2zt_AAAA.json) |
| `AAAAA` | 莫（郟敖子） | [《史記・楚世家》][22] | [JSON](0va_zus_2zt_AAAAA.json) |
| `AAAAB` | 平夏（郟敖子） | [《史記・楚世家》][22] | [JSON](0va_zus_2zt_AAAAB.json) |
| `AAB` | 圍 | [《史記・楚世家》][22] | [JSON](0va_zus_2zt_AAB.json) |
| `AAC` | 子比（楚初王） | [《史記・楚世家》][22] | [JSON](0va_zus_2zt_AAC.json) |
| `AAD` | 子皙（楚令尹） | [《史記・楚世家》][22] | [JSON](0va_zus_2zt_AAD.json) |
| `AAE` | 棄疾 | [《史記・楚世家》][22] | [JSON](0va_zus_2zt_AAE.json) |
| `AAEA` | 珍（熊珍楚昭王） | [《史記・楚世家》][22] | [JSON](0va_zus_2zt_AAEA.json) |

</details>

<details><summary><code>0xl_7ir_tmn</code> 孔子（弟子列傳候選）（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 孔子 | [《史記・孔子世家》][29] | [JSON](0xl_7ir_tmn.json) |
| `A` | 孔鯉 | [《史記・仲尼弟子列傳》][49] | [JSON](0xl_7ir_tmn_A.json) |
| `B` | 孔子之女 | [《史記・仲尼弟子列傳》][49] | [JSON](0xl_7ir_tmn_B.json) |

</details>

<details><summary><code>0xt_iyn_d3t</code> 趙夙（趙世家候選）（12 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 趙夙 | [《史記・趙世家》][25] | [JSON](0xt_iyn_d3t.json) |
| `A` | 共孟 | [《史記・趙世家》][25] | [JSON](0xt_iyn_d3t_A.json) |
| `AA` | 趙衰 | [《史記・晉世家》][21] | [JSON](0xt_iyn_d3t_AA.json) |
| `AAA` | 趙盾 | [《史記・晉世家》][21] | [JSON](0xt_iyn_d3t_AAA.json) |
| `AAAA` | 趙朔 | [《史記・趙世家》][25] | [JSON](0xt_iyn_d3t_AAAA.json) |
| `AAAAA` | 趙武 | [《史記・趙世家》][25] | [JSON](0xt_iyn_d3t_AAAAA.json) |
| `AAAAAA` | 趙景叔 | [《史記・趙世家》][25] | [JSON](0xt_iyn_d3t_AAAAAA.json) |
| `AAAAAAA` | 趙鞅 | [《史記・趙世家》][25] | [JSON](0xt_iyn_d3t_AAAAAAA.json) |
| `AAAAAAAA` | 毋卹 | [《史記・趙世家》][25] | [JSON](0xt_iyn_d3t_AAAAAAAA.json) |
| `AAB` | 趙同 | [《史記・趙世家》][25] | [JSON](0xt_iyn_d3t_AAB.json) |
| `AAC` | 趙括 | [《史記・趙世家》][25] | [JSON](0xt_iyn_d3t_AAC.json) |
| `AAD` | 趙嬰齊 | [《史記・趙世家》][25] | [JSON](0xt_iyn_d3t_AAD.json) |

</details>

<details><summary><code>113_odk_emq</code> 衞綰（萬石張叔列傳候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 衞綰 | [《史記・萬石張叔列傳》][85] | [JSON](113_odk_emq.json) |
| `A` | 信（衞綰子） | [《史記・萬石張叔列傳》][85] | [JSON](113_odk_emq_A.json) |

</details>

<details><summary><code>128_4ab_z34</code> 熊延（楚君）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 熊延（楚君） | [《史記・楚世家》][22] | [JSON](128_4ab_z34.json) |
| `A` | 熊勇（楚君） | [《史記・楚世家》][22] | [JSON](128_4ab_z34_A.json) |

</details>

<details><summary><code>1f5_azb_lmy</code> 專諸（刺客列傳候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 專諸 | [《史記・刺客列傳》][68] | [JSON](1f5_azb_lmy.json) |
| `A` | 專諸子未名 | [《史記・刺客列傳》][68] | [JSON](1f5_azb_lmy_A.json) |

</details>

<details><summary><code>1g3_02y_oor</code> 太公望（5 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 太公望 | [《史記・齊太公世家》][14] | [JSON](1g3_02y_oor.json) |
| `A` | 丁公呂伋 | [《史記・齊太公世家》][14] | [JSON](1g3_02y_oor_A.json) |
| `AA` | 得（齊乙公） | [《史記・齊太公世家》][14] | [JSON](1g3_02y_oor_AA.json) |
| `AAA` | 慈母（齊癸公） | [《史記・齊太公世家》][14] | [JSON](1g3_02y_oor_AAA.json) |
| `AAAA` | 不辰（齊哀公） | [《史記・齊太公世家》][14] | [JSON](1g3_02y_oor_AAAA.json) |

</details>

<details><summary><code>1h3_vs7_t8h</code> 齊湣王（燕篇）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 齊湣王（燕篇） | [《史記・燕召公世家》][16] | [JSON](1h3_vs7_t8h.json) |
| `A` | 襄王（齊湣王子） | [《史記・田敬仲完世家》][28] | [JSON](1h3_vs7_t8h_A.json) |

</details>

<details><summary><code>1hf_1k0_bnj</code> 夷仲年（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 夷仲年 | [《史記・齊太公世家》][14] | [JSON](1hf_1k0_bnj.json) |
| `A` | 公孫無知 | [《史記・齊太公世家》][14] | [JSON](1hf_1k0_bnj_A.json) |

</details>

<details><summary><code>1l4_2pq_e7w</code> 熊通（楚武王候選）（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 熊通 | [《史記・楚世家》][22] | [JSON](1l4_2pq_e7w.json) |
| `A` | 熊貲（楚文王） | [《史記・楚世家》][22] | [JSON](1l4_2pq_e7w_A.json) |
| `AA` | 熊艱（莊敖） | [《史記・楚世家》][22] | [JSON](1l4_2pq_e7w_AA.json) |

</details>

<details><summary><code>1oe_02j_wh7</code> 晉襄公（趙世家候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 晉襄公 | [《史記・趙世家》][25] | [JSON](1oe_02j_wh7.json) |
| `**A` | 周 | [《史記・趙世家》][25] | [JSON](1oe_02j_wh7_%2A%2AA.json) |

</details>

<details><summary><code>1pc_mnq_z0c</code> 懿公（燕文公後）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 懿公（燕文公後） | [《史記・燕召公世家》][16] | [JSON](1pc_mnq_z0c.json) |
| `A` | 惠公（燕懿公子） | [《史記・燕召公世家》][16] | [JSON](1pc_mnq_z0c_A.json) |

</details>

<details><summary><code>1y5_eke_4gl</code> 陽慶（扁鵲倉公列傳候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 陽慶 | [《史記・扁鵲倉公列傳》][87] | [JSON](1y5_eke_4gl.json) |
| `A` | 殷（慶子） | [《史記・扁鵲倉公列傳》][87] | [JSON](1y5_eke_4gl_A.json) |

</details>

<details><summary><code>1za_blw_7lb</code> 伯魯（趙世家候選）（6 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 伯魯 | [《史記・趙世家》][25] | [JSON](1za_blw_7lb.json) |
| `A` | 周 | [《史記・趙世家》][25] | [JSON](1za_blw_7lb_A.json) |
| `AA` | 浣 | [《史記・趙世家》][25] | [JSON](1za_blw_7lb_AA.json) |
| `AAA` | 籍 | [《史記・趙世家》][25] | [JSON](1za_blw_7lb_AAA.json) |
| `AAAA` | 章 | [《史記・趙世家》][25] | [JSON](1za_blw_7lb_AAAA.json) |
| `AAAAA` | 種 | [《史記・趙世家》][25] | [JSON](1za_blw_7lb_AAAAA.json) |

</details>

<details><summary><code>2d3_fsd_1dh</code> 楚成王（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 楚成王 | [《史記・晉世家》][21] | [JSON](2d3_fsd_1dh.json) |
| `A` | 楚商臣 | [《史記・陳杞世家》][18] | [JSON](2d3_fsd_1dh_A.json) |

</details>

<details><summary><code>2v6_0g1_ve2</code> 衍（宋微仲）（13 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 衍（宋微仲） | [《史記・宋微子世家》][20] | [JSON](2v6_0g1_ve2.json) |
| `A` | 稽（宋公） | [《史記・宋微子世家》][20] | [JSON](2v6_0g1_ve2_A.json) |
| `AA` | 申（宋丁公） | [《史記・宋微子世家》][20] | [JSON](2v6_0g1_ve2_AA.json) |
| `AAA` | 共（宋湣公） | [《史記・宋微子世家》][20] | [JSON](2v6_0g1_ve2_AAA.json) |
| `AAAA` | 鮒祀（宋厲公） | [《史記・宋微子世家》][20] | [JSON](2v6_0g1_ve2_AAAA.json) |
| `AAAAA` | 舉（宋釐公） | [《史記・宋微子世家》][20] | [JSON](2v6_0g1_ve2_AAAAA.json) |
| `AAAAAA` | 覵（宋惠公） | [《史記・宋微子世家》][20] | [JSON](2v6_0g1_ve2_AAAAAA.json) |
| `AAAAAAA` | 哀公（宋惠公子） | [《史記・宋微子世家》][20] | [JSON](2v6_0g1_ve2_AAAAAAA.json) |
| `AAAAAAAA` | 戴公（宋哀公子） | [《史記・宋微子世家》][20] | [JSON](2v6_0g1_ve2_AAAAAAAA.json) |
| `AAAAAAAAA` | 司空（宋武公） | [《史記・宋微子世家》][20] | [JSON](2v6_0g1_ve2_AAAAAAAAA.json) |
| `AAAAAAAAAA` | 宋女（魯惠公夫人） | [《史記・宋微子世家》][20] | [JSON](2v6_0g1_ve2_AAAAAAAAAA.json) |
| `AAAAAAAAAB` | 力（宋宣公） | [《史記・宋微子世家》][20] | [JSON](2v6_0g1_ve2_AAAAAAAAAB.json) |
| `AAAAAAAAABA` | 與夷 | [《史記・宋微子世家》][20] | [JSON](2v6_0g1_ve2_AAAAAAAAABA.json) |

</details>

<details><summary><code>30v_zf2_l7l</code> 齊王建（田儋列傳候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 齊王建 | [《史記・秦始皇本紀》][6]、[《史記・田儋列傳》][76] | [JSON](30v_zf2_l7l.json) |
| `*A` | 田安 | [《史記・項羽本紀》][7]、[《史記・田儋列傳》][76] | [JSON](30v_zf2_l7l_%2AA.json) |

</details>

<details><summary><code>31t_28w_hda</code> 平（留侯世家候選）（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 平 | [《史記・留侯世家》][37] | [JSON](31t_28w_hda.json) |
| `A` | 張良 | [《史記・留侯世家》][37] | [JSON](31t_28w_hda_A.json) |
| `AA` | 不疑 | [《史記・留侯世家》][37] | [JSON](31t_28w_hda_AA.json) |

</details>

<details><summary><code>3oc_7gw_pl5</code> 番君（黥布列傳候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 番君 | [《史記・高祖本紀》][8] | [JSON](3oc_7gw_pl5.json) |
| `A` | 英布妻未名 | [《史記・黥布列傳》][73] | [JSON](3oc_7gw_pl5_A.json) |

</details>

<details><summary><code>3te_z66_d5a</code> 張敖（外戚世家候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 張敖 | [《史記・外戚世家》][31] | [JSON](3te_z66_d5a.json) |
| `A` | 孝惠皇后 | [《史記・外戚世家》][31] | [JSON](3te_z66_d5a_A.json) |

</details>

<details><summary><code>42z_cse_1ka</code> 熊良夫（楚宣王）（4 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 熊良夫（楚宣王） | [《史記・楚世家》][22] | [JSON](42z_cse_1ka.json) |
| `A` | 熊商（楚威王） | [《史記・楚世家》][22] | [JSON](42z_cse_1ka_A.json) |
| `AA` | 熊槐 | [《史記・楚世家》][22] | [JSON](42z_cse_1ka_AA.json) |
| `AAA` | 子蘭（楚懷王子） | [《史記・屈原賈生列傳》][66] | [JSON](42z_cse_1ka_AAA.json) |

</details>

<details><summary><code>46a_tvp_dq9</code> 秦獻公（魏世家候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 秦獻公 | [《史記・魏世家》][26] | [JSON](46a_tvp_dq9.json) |
| `A` | 秦孝公 | [《史記・魏世家》][26] | [JSON](46a_tvp_dq9_A.json) |

</details>

<details><summary><code>46l_ir2_1cr</code> 敖（趙王）（4 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 敖（趙王） | [《史記・呂太后本紀》][9] | [JSON](46l_ir2_1cr.json) |
| `A` | 偃（魯王） | [《史記・呂太后本紀》][9] | [JSON](46l_ir2_1cr_A.json) |
| `B` | 侈（張敖前姬子） | [《史記・呂太后本紀》][9] | [JSON](46l_ir2_1cr_B.json) |
| `C` | 壽（張敖前姬子） | [《史記・呂太后本紀》][9] | [JSON](46l_ir2_1cr_C.json) |

</details>

<details><summary><code>4wv_6og_mwb</code> 申無宇（芋尹）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 申無宇（芋尹） | [《史記・楚世家》][22] | [JSON](4wv_6og_mwb.json) |
| `A` | 申亥（收葬楚靈王者） | [《史記・楚世家》][22] | [JSON](4wv_6og_mwb_A.json) |

</details>

<details><summary><code>4xe_ms4_pr9</code> 夢者（曹亡敘事未名）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 夢者（曹亡敘事未名） | [《史記・管蔡世家》][17] | [JSON](4xe_ms4_pr9.json) |
| `A` | 夢者子（未名） | [《史記・管蔡世家》][17] | [JSON](4xe_ms4_pr9_A.json) |

</details>

<details><summary><code>50h_gqe_1p1</code> 具（魯獻公）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 具（魯獻公） | [《史記・魯周公世家》][15] | [JSON](50h_gqe_1p1.json) |
| `A` | 濞（魯真公） | [《史記・魯周公世家》][15] | [JSON](50h_gqe_1p1_A.json) |

</details>

<details><summary><code>524_au1_97b</code> 張耳（陳涉世家候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 張耳 | [《史記・張耳陳餘列傳》][71] | [JSON](524_au1_97b.json) |
| `A` | 張敖 | [《史記・張耳陳餘列傳》][71] | [JSON](524_au1_97b_A.json) |

</details>

<details><summary><code>5bo_dxd_69k</code> 冉雍父（弟子列傳候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 冉雍父 | [《史記・仲尼弟子列傳》][49] | [JSON](5bo_dxd_69k.json) |
| `A` | 冉雍 | [《史記・仲尼弟子列傳》][49] | [JSON](5bo_dxd_69k_A.json) |

</details>

<details><summary><code>5dd_l1c_6g8</code> 衛青（外戚世家候選）（5 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 衛青 | [《史記・外戚世家》][31] | [JSON](5dd_l1c_6g8.json) |
| `A` | 衛青子陰安侯 | [《史記・外戚世家》][31] | [JSON](5dd_l1c_6g8_A.json) |
| `B` | 衛青子發干侯 | [《史記・外戚世家》][31] | [JSON](5dd_l1c_6g8_B.json) |
| `C` | 衛青子宜春侯 | [《史記・外戚世家》][31] | [JSON](5dd_l1c_6g8_C.json) |
| `D` | 伉 | [《史記・外戚世家》][31] | [JSON](5dd_l1c_6g8_D.json) |

</details>

<details><summary><code>5dm_e40_rqh</code> 古公亶父（27 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 古公亶父 | [《史記・周本紀》][4] | [JSON](5dm_e40_rqh.json) |
| `A` | 仲雍 | [《史記・吳太伯世家》][13] | [JSON](5dm_e40_rqh_A.json) |
| `AA` | 季簡 | [《史記・吳太伯世家》][13] | [JSON](5dm_e40_rqh_AA.json) |
| `AAA` | 叔達 | [《史記・吳太伯世家》][13] | [JSON](5dm_e40_rqh_AAA.json) |
| `AAAA` | 周章（吳君） | [《史記・吳太伯世家》][13] | [JSON](5dm_e40_rqh_AAAA.json) |
| `AAAAA` | 熊遂 | [《史記・吳太伯世家》][13] | [JSON](5dm_e40_rqh_AAAAA.json) |
| `AAAAAA` | 柯相 | [《史記・吳太伯世家》][13] | [JSON](5dm_e40_rqh_AAAAAA.json) |
| `AAAAAAA` | 彊鳩夷 | [《史記・吳太伯世家》][13] | [JSON](5dm_e40_rqh_AAAAAAA.json) |
| `AAAAAAAA` | 餘橋疑吾 | [《史記・吳太伯世家》][13] | [JSON](5dm_e40_rqh_AAAAAAAA.json) |
| `AAAAAAAAA` | 柯盧 | [《史記・吳太伯世家》][13] | [JSON](5dm_e40_rqh_AAAAAAAAA.json) |
| `AAAAAAAAAA` | 周繇 | [《史記・吳太伯世家》][13] | [JSON](5dm_e40_rqh_AAAAAAAAAA.json) |
| `AAAAAAAAAAA` | 屈羽 | [《史記・吳太伯世家》][13] | [JSON](5dm_e40_rqh_AAAAAAAAAAA.json) |
| `AAAAAAAAAAAA` | 夷吾（吳君） | [《史記・吳太伯世家》][13] | [JSON](5dm_e40_rqh_AAAAAAAAAAAA.json) |
| `AAAAAAAAAAAAA` | 禽處 | [《史記・吳太伯世家》][13] | [JSON](5dm_e40_rqh_AAAAAAAAAAAAA.json) |
| `AAAAAAAAAAAAAA` | 轉（吳君） | [《史記・吳太伯世家》][13] | [JSON](5dm_e40_rqh_AAAAAAAAAAAAAA.json) |
| `AAAAAAAAAAAAAAA` | 頗髙 | [《史記・吳太伯世家》][13] | [JSON](5dm_e40_rqh_AAAAAAAAAAAAAAA.json) |
| `AAAAAAAAAAAAAAAA` | 句卑 | [《史記・吳太伯世家》][13] | [JSON](5dm_e40_rqh_AAAAAAAAAAAAAAAA.json) |
| `AAAAAAAAAAAAAAAAA` | 去齊 | [《史記・吳太伯世家》][13] | [JSON](5dm_e40_rqh_AAAAAAAAAAAAAAAAA.json) |
| `AAAAAAAAAAAAAAAAAA` | 壽夢 | [《史記・吳太伯世家》][13] | [JSON](5dm_e40_rqh_AAAAAAAAAAAAAAAAAA.json) |
| `AAAAAAAAAAAAAAAAAAA` | 諸樊 | [《史記・吳太伯世家》][13] | [JSON](5dm_e40_rqh_AAAAAAAAAAAAAAAAAAA.json) |
| `AAAAAAAAAAAAAAAAAAAA` | 闔閭 | [《史記・吳太伯世家》][13] | [JSON](5dm_e40_rqh_AAAAAAAAAAAAAAAAAAAA.json) |
| `AAAAAAAAAAAAAAAAAAAAA` | 夫差 | [《史記・越王勾踐世家》][23] | [JSON](5dm_e40_rqh_AAAAAAAAAAAAAAAAAAAAA.json) |
| `AAAAAAAAAAAAAAAAAAB` | 餘祭 | [《史記・吳太伯世家》][13] | [JSON](5dm_e40_rqh_AAAAAAAAAAAAAAAAAAB.json) |
| `AAAAAAAAAAAAAAAAAAC` | 餘眛 | [《史記・吳太伯世家》][13] | [JSON](5dm_e40_rqh_AAAAAAAAAAAAAAAAAAC.json) |
| `AAAAAAAAAAAAAAAAAACA` | 僚（吳王） | [《史記・吳太伯世家》][13] | [JSON](5dm_e40_rqh_AAAAAAAAAAAAAAAAAACA.json) |
| `AAAAAAAAAAAAAAAAAAD` | 季札 | [《史記・吳太伯世家》][13] | [JSON](5dm_e40_rqh_AAAAAAAAAAAAAAAAAAD.json) |
| `B` | 太伯 | [《史記・吳太伯世家》][13] | [JSON](5dm_e40_rqh_B.json) |

</details>

<details><summary><code>5km_89r_9jr</code> 元君（衛嗣君弟）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 元君（衛嗣君弟） | [《史記・衛康叔世家》][19] | [JSON](5km_89r_9jr.json) |
| `A` | 衛君角 | [《史記・衛康叔世家》][19] | [JSON](5km_89r_9jr_A.json) |

</details>

<details><summary><code>5ok_joj_etv</code> 李斯（李斯列傳候選）（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 李斯 | [《史記・李斯列傳》][69] | [JSON](5ok_joj_etv.json) |
| `A` | 李由 | [《史記・李斯列傳》][69] | [JSON](5ok_joj_etv_A.json) |
| `B` | 李斯中子未名 | [《史記・李斯列傳》][69] | [JSON](5ok_joj_etv_B.json) |

</details>

<details><summary><code>5pw_05i_uhv</code> 平（本文燕昭王）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 平（本文燕昭王） | [《史記・樂毅列傳》][62] | [JSON](5pw_05i_uhv.json) |
| `A` | 惠王（燕昭王子） | [《史記・樂毅列傳》][62] | [JSON](5pw_05i_uhv_A.json) |

</details>

<details><summary><code>5xt_rg8_7zs</code> 項燕（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 項燕 | [《史記・秦始皇本紀》][6] | [JSON](5xt_rg8_7zs.json) |
| `A` | 項梁 | [《史記・項羽本紀》][7] | [JSON](5xt_rg8_7zs_A.json) |

</details>

<details><summary><code>69x_se2_859</code> 邴吉（張丞相列傳候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 邴吉 | [《史記・張丞相列傳》][78] | [JSON](69x_se2_859.json) |
| `A` | 邴顯 | [《史記・張丞相列傳》][78] | [JSON](69x_se2_859_A.json) |

</details>

<details><summary><code>6d6_eg1_o3a</code> 王仲（外戚世家候選）（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 王仲 | [《史記・外戚世家》][31] | [JSON](6d6_eg1_o3a.json) |
| `A` | 王太后 | [《史記・外戚世家》][31] | [JSON](6d6_eg1_o3a_A.json) |
| `B` | 信 | [《史記・外戚世家》][31] | [JSON](6d6_eg1_o3a_B.json) |

</details>

<details><summary><code>6di_ywz_ju4</code> 莊伯（晉曲沃弒君記事）（9 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 莊伯（晉曲沃弒君記事） | [《史記・晉世家》][21] | [JSON](6di_ywz_ju4.json) |
| `A` | 稱（曲沃／晉武公） | [《史記・晉世家》][21] | [JSON](6di_ywz_ju4_A.json) |
| `AA` | 晉獻公 | [《史記・晉世家》][21] | [JSON](6di_ywz_ju4_AA.json) |
| `AAA` | 晉文公 | [《史記・晉世家》][21] | [JSON](6di_ywz_ju4_AAA.json) |
| `AAAA` | 伯鯈（重耳子） | [《史記・晉世家》][21] | [JSON](6di_ywz_ju4_AAAA.json) |
| `AAAB` | 叔劉（重耳子） | [《史記・晉世家》][21] | [JSON](6di_ywz_ju4_AAAB.json) |
| `AAAC` | 黑臀（晉成公） | [《史記・晉世家》][21] | [JSON](6di_ywz_ju4_AAAC.json) |
| `AAB` | 申生 | [《史記・晉世家》][21] | [JSON](6di_ywz_ju4_AAB.json) |
| `AAC` | 奚齊 | [《史記・晉世家》][21] | [JSON](6di_ywz_ju4_AAC.json) |

</details>

<details><summary><code>6dq_od2_cg1</code> 魏昭王（魏公子列傳候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 魏昭王 | [《史記・魏世家》][26] | [JSON](6dq_od2_cg1.json) |
| `A` | 魏公子無忌 | [《史記・魏公子列傳》][59] | [JSON](6dq_od2_cg1_A.json) |

</details>

<details><summary><code>6ks_x4x_dbf</code> 臧荼（外戚世家候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 臧荼 | [《史記・外戚世家》][31] | [JSON](6ks_x4x_dbf.json) |
| `*A` | 臧兒 | [《史記・外戚世家》][31] | [JSON](6ks_x4x_dbf_%2AA.json) |

</details>

<details><summary><code>6oy_t19_ywe</code> 秦惠王（蘇秦列傳候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 秦惠王 | [《史記・蘇秦列傳》][51] | [JSON](6oy_t19_ywe.json) |
| `A` | 秦惠王女 | [《史記・蘇秦列傳》][51] | [JSON](6oy_t19_ywe_A.json) |

</details>

<details><summary><code>6wx_fr3_b2e</code> 滿（陳胡公）（8 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 滿（陳胡公） | [《史記・陳杞世家》][18] | [JSON](6wx_fr3_b2e.json) |
| `A` | 犀侯（陳申公） | [《史記・陳杞世家》][18] | [JSON](6wx_fr3_b2e_A.json) |
| `AA` | 突（陳孝公） | [《史記・陳杞世家》][18] | [JSON](6wx_fr3_b2e_AA.json) |
| `AAA` | 圉戎（陳慎公） | [《史記・陳杞世家》][18] | [JSON](6wx_fr3_b2e_AAA.json) |
| `AAAA` | 寧（陳幽公） | [《史記・陳杞世家》][18] | [JSON](6wx_fr3_b2e_AAAA.json) |
| `AAAAA` | 孝（陳釐公） | [《史記・陳杞世家》][18] | [JSON](6wx_fr3_b2e_AAAAA.json) |
| `AAAAAA` | 靈（陳武公） | [《史記・陳杞世家》][18] | [JSON](6wx_fr3_b2e_AAAAAA.json) |
| `AAAAAAA` | 說（陳夷公） | [《史記・陳杞世家》][18] | [JSON](6wx_fr3_b2e_AAAAAAA.json) |

</details>

<details><summary><code>6zh_3z5_gsm</code> 闔廬（越世家候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 闔廬 | [《史記・越王勾踐世家》][23] | [JSON](6zh_3z5_gsm.json) |
| `A` | 夫差 | [《史記・越王勾踐世家》][23] | [JSON](6zh_3z5_gsm_A.json) |

</details>

<details><summary><code>6zt_fca_se8</code> 趙奢（廉頗藺相如列傳候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 趙奢 | [《史記・廉頗藺相如列傳》][63] | [JSON](6zt_fca_se8.json) |
| `A` | 趙括 | [《史記・廉頗藺相如列傳》][63] | [JSON](6zt_fca_se8_A.json) |

</details>

<details><summary><code>761_6ot_9wz</code> 管仲父（管晏列傳候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 管仲父 | [《史記・管晏列傳》][44] | [JSON](761_6ot_9wz.json) |
| `A` | 管仲 | [《史記・齊太公世家》][14] | [JSON](761_6ot_9wz_A.json) |

</details>

<details><summary><code>766_5dq_zws</code> 朱家（季布欒布列傳候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 朱家 | [《史記・季布欒布列傳》][82] | [JSON](766_5dq_zws.json) |
| `A` | 朱家子未名 | [《史記・季布欒布列傳》][82] | [JSON](766_5dq_zws_A.json) |

</details>

<details><summary><code>78u_8ii_bnr</code> 專諸（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 專諸 | [《史記・吳太伯世家》][13] | [JSON](78u_8ii_bnr.json) |
| `A` | 專諸子（本卷未名） | [《史記・吳太伯世家》][13] | [JSON](78u_8ii_bnr_A.json) |

</details>

<details><summary><code>796_nkw_0jz</code> 張蒼父未名（張丞相列傳候選）（4 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 張蒼父未名 | [《史記・張丞相列傳》][78] | [JSON](796_nkw_0jz.json) |
| `A` | 張蒼 | [《史記・張丞相列傳》][78] | [JSON](796_nkw_0jz_A.json) |
| `AA` | 張蒼子未名（康侯） | [《史記・張丞相列傳》][78] | [JSON](796_nkw_0jz_AA.json) |
| `AAA` | 張類 | [《史記・張丞相列傳》][78] | [JSON](796_nkw_0jz_AAA.json) |

</details>

<details><summary><code>7du_pfa_2s5</code> 蹇叔（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 蹇叔 | [《史記・秦本紀》][5] | [JSON](7du_pfa_2s5.json) |
| `A` | 西乞術 | [《史記・秦本紀》][5]、[《史記・晉世家》][21] | [JSON](7du_pfa_2s5_A.json) |
| `B` | 白乙丙 | [《史記・秦本紀》][5]、[《史記・晉世家》][21] | [JSON](7du_pfa_2s5_B.json) |

</details>

<details><summary><code>7dv_lqp_y4z</code> 靳歙（傅靳蒯成列傳候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 靳歙 | [《史記・傅靳蒯成列傳》][80] | [JSON](7dv_lqp_y4z.json) |
| `A` | 靳亭 | [《史記・傅靳蒯成列傳》][80] | [JSON](7dv_lqp_y4z_A.json) |

</details>

<details><summary><code>7mz_d13_9ka</code> 田氏（外戚世家候選）（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 田氏 | [《史記・外戚世家》][31] | [JSON](7mz_d13_9ka.json) |
| `A` | 田蚡 | [《史記・外戚世家》][31] | [JSON](7mz_d13_9ka_A.json) |
| `B` | 勝 | [《史記・外戚世家》][31] | [JSON](7mz_d13_9ka_B.json) |

</details>

<details><summary><code>7s2_h0m_msl</code> 蘇（曹戴伯）（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 蘇（曹戴伯） | [《史記・管蔡世家》][17] | [JSON](7s2_h0m_msl.json) |
| `A` | 兕（曹惠伯） | [《史記・管蔡世家》][17] | [JSON](7s2_h0m_msl_A.json) |
| `AA` | 石甫（曹惠伯子） | [《史記・管蔡世家》][17] | [JSON](7s2_h0m_msl_AA.json) |

</details>

<details><summary><code>7s4_7ac_lhn</code> 齊威王（孟嘗君列傳候選）（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 齊威王 | [《史記・孟嘗君列傳》][57] | [JSON](7s4_7ac_lhn.json) |
| `A` | 田嬰 | [《史記・孟嘗君列傳》][57] | [JSON](7s4_7ac_lhn_A.json) |
| `AA` | 孟嘗君田文 | [《史記・孟嘗君列傳》][57] | [JSON](7s4_7ac_lhn_AA.json) |

</details>

<details><summary><code>7tm_3ss_4on</code> 周苛（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 周苛 | [《史記・張丞相列傳》][78] | [JSON](7tm_3ss_4on.json) |
| `*A` | 平（周苛孫） | [《史記・孝景本紀》][11] | [JSON](7tm_3ss_4on_%2AA.json) |

</details>

<details><summary><code>7uk_oqn_ymk</code> 陳宣公杵臼（田世家候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 陳宣公杵臼 | [《史記・田敬仲完世家》][28] | [JSON](7uk_oqn_ymk.json) |
| `A` | 御寇 | [《史記・田敬仲完世家》][28] | [JSON](7uk_oqn_ymk_A.json) |

</details>

<details><summary><code>8rw_c97_jpz</code> 梁伯（晉惠公外家）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 梁伯（晉惠公外家） | [《史記・晉世家》][21] | [JSON](8rw_c97_jpz.json) |
| `A` | 梁伯女（圉母） | [《史記・晉世家》][21] | [JSON](8rw_c97_jpz_A.json) |

</details>

<details><summary><code>913_1wz_ofu</code> 曹參（曹相國世家候選）（6 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 曹參 | [《史記・曹相國世家》][36] | [JSON](913_1wz_ofu.json) |
| `A` | 窋 | [《史記・曹相國世家》][36] | [JSON](913_1wz_ofu_A.json) |
| `AA` | 奇 | [《史記・曹相國世家》][36] | [JSON](913_1wz_ofu_AA.json) |
| `AAA` | 時 | [《史記・曹相國世家》][36] | [JSON](913_1wz_ofu_AAA.json) |
| `AAAA` | 襄 | [《史記・曹相國世家》][36] | [JSON](913_1wz_ofu_AAAA.json) |
| `AAAAA` | 宗 | [《史記・曹相國世家》][36] | [JSON](913_1wz_ofu_AAAAA.json) |

</details>

<details><summary><code>98v_uic_i4i</code> 孤竹君（伯夷列傳候選）（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 孤竹君 | [《史記・伯夷列傳》][43] | [JSON](98v_uic_i4i.json) |
| `A` | 伯夷 | [《史記・伯夷列傳》][43] | [JSON](98v_uic_i4i_A.json) |
| `B` | 叔齊 | [《史記・伯夷列傳》][43] | [JSON](98v_uic_i4i_B.json) |

</details>

<details><summary><code>995_xas_r98</code> 申（蔡昭侯）（6 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 申（蔡昭侯） | [《史記・管蔡世家》][17] | [JSON](995_xas_r98.json) |
| `A` | 朔（蔡成侯） | [《史記・管蔡世家》][17] | [JSON](995_xas_r98_A.json) |
| `AA` | 產（蔡聲侯） | [《史記・管蔡世家》][17] | [JSON](995_xas_r98_AA.json) |
| `AAA` | 元侯（蔡君） | [《史記・管蔡世家》][17] | [JSON](995_xas_r98_AAA.json) |
| `AAAA` | 齊（蔡末侯） | [《史記・管蔡世家》][17] | [JSON](995_xas_r98_AAAA.json) |
| `B` | 蔡昭侯質吳子（未名） | [《史記・管蔡世家》][17] | [JSON](995_xas_r98_B.json) |

</details>

<details><summary><code>9nr_qwg_vuf</code> 叔孫宣伯（魯）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 叔孫宣伯（魯） | [《史記・齊太公世家》][14] | [JSON](9nr_qwg_vuf.json) |
| `A` | 景公母（叔孫宣伯女） | [《史記・齊太公世家》][14] | [JSON](9nr_qwg_vuf_A.json) |

</details>

<details><summary><code>9w2_c77_53m</code> 齊桓公（12 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 齊桓公 | [《史記・齊太公世家》][14] | [JSON](9w2_c77_53m.json) |
| `A` | 元（齊惠公） | [《史記・齊太公世家》][14] | [JSON](9w2_c77_53m_A.json) |
| `AA` | 無野（齊頃公） | [《史記・齊太公世家》][14] | [JSON](9w2_c77_53m_AA.json) |
| `AAA` | 環（齊靈公） | [《史記・齊太公世家》][14] | [JSON](9w2_c77_53m_AAA.json) |
| `AAAA` | 齊莊公（崔杼時） | [《史記・齊太公世家》][14] | [JSON](9w2_c77_53m_AAAA.json) |
| `B` | 無詭（齊桓公子） | [《史記・齊太公世家》][14] | [JSON](9w2_c77_53m_B.json) |
| `C` | 昭（齊孝公） | [《史記・齊太公世家》][14] | [JSON](9w2_c77_53m_C.json) |
| `D` | 潘（齊昭公） | [《史記・齊太公世家》][14] | [JSON](9w2_c77_53m_D.json) |
| `DA` | 舍（齊昭公子） | [《史記・齊太公世家》][14] | [JSON](9w2_c77_53m_DA.json) |
| `E` | 商人（齊懿公） | [《史記・齊太公世家》][14] | [JSON](9w2_c77_53m_E.json) |
| `F` | 雍（齊桓公子） | [《史記・齊太公世家》][14]、[《史記・楚世家》][22] | [JSON](9w2_c77_53m_F.json) |
| `G` | 齊姜（申生母） | [《史記・晉世家》][21] | [JSON](9w2_c77_53m_G.json) |

</details>

<details><summary><code>9yf_c3t_x2w</code> 衛君父引古未名（李斯列傳候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 衛君父引古未名 | [《史記・李斯列傳》][69] | [JSON](9yf_c3t_x2w.json) |
| `A` | 衛君引古未名 | [《史記・李斯列傳》][69] | [JSON](9yf_c3t_x2w_A.json) |

</details>

<details><summary><code>9zj_vf7_86a</code> 薄氏父（外戚世家候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 薄氏父 | [《史記・外戚世家》][31] | [JSON](9zj_vf7_86a.json) |
| `A` | 薄太后 | [《史記・外戚世家》][31] | [JSON](9zj_vf7_86a_A.json) |

</details>

<details><summary><code>a13_5fp_pek</code> 梁襄王（趙世家候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 梁襄王 | [《史記・趙世家》][25] | [JSON](a13_5fp_pek.json) |
| `A` | 嗣 | [《史記・趙世家》][25] | [JSON](a13_5fp_pek_A.json) |

</details>

<details><summary><code>a7k_sl0_d7u</code> 金王孫（外戚世家候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 金王孫 | [《史記・外戚世家》][31] | [JSON](a7k_sl0_d7u.json) |
| `A` | 修成君 | [《史記・外戚世家》][31] | [JSON](a7k_sl0_d7u_A.json) |

</details>

<details><summary><code>a9m_987_rss</code> 叔牙（莊公弟）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 叔牙（莊公弟） | [《史記・魯周公世家》][15] | [JSON](a9m_987_rss.json) |
| `A` | 叔牙子（未名） | [《史記・魯周公世家》][15] | [JSON](a9m_987_rss_A.json) |

</details>

<details><summary><code>a9v_t0d_3va</code> 晉惠公（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 晉惠公 | [《史記・晉世家》][21] | [JSON](a9v_t0d_3va.json) |
| `A` | 晉懷公 | [《史記・晉世家》][21] | [JSON](a9v_t0d_3va_A.json) |
| `B` | 妾（梁伯女所生女） | [《史記・晉世家》][21] | [JSON](a9v_t0d_3va_B.json) |

</details>

<details><summary><code>acg_se3_w5x</code> 周呂侯（呂后兄）（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 周呂侯（呂后兄） | [《史記・呂太后本紀》][9] | [JSON](acg_se3_w5x.json) |
| `A` | 呂台 | [《史記・呂太后本紀》][9] | [JSON](acg_se3_w5x_A.json) |
| `B` | 呂產 | [《史記・呂太后本紀》][9] | [JSON](acg_se3_w5x_B.json) |

</details>

<details><summary><code>acp_p3n_gli</code> 懷王（陳涉世家心祖未名者）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 懷王（陳涉世家心祖未名者） | [《史記・陳涉世家》][30] | [JSON](acp_p3n_gli.json) |
| `*A` | 心 | [《史記・高祖本紀》][8] | [JSON](acp_p3n_gli_%2AA.json) |

</details>

<details><summary><code>afj_vl8_7fu</code> 安丘侯説（萬石張叔列傳候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 安丘侯説 | [《史記・萬石張叔列傳》][85] | [JSON](afj_vl8_7fu.json) |
| `A` | 張歐 | [《史記・萬石張叔列傳》][85] | [JSON](afj_vl8_7fu_A.json) |

</details>

<details><summary><code>anb_2wd_5ci</code> 周苛（張丞相列傳候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 周苛 | [《史記・張丞相列傳》][78] | [JSON](anb_2wd_5ci.json) |
| `A` | 周成 | [《史記・張丞相列傳》][78] | [JSON](anb_2wd_5ci_A.json) |

</details>

<details><summary><code>ant_017_buy</code> 九侯引古（魯仲連鄒陽列傳候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 九侯引古 | [《史記・魯仲連鄒陽列傳》][65] | [JSON](ant_017_buy.json) |
| `A` | 九侯子引古未名 | [《史記・魯仲連鄒陽列傳》][65] | [JSON](ant_017_buy_A.json) |

</details>

<details><summary><code>ao3_0fy_d45</code> 秦昭王（6 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 秦昭王 | [《史記・范睢蔡澤列傳》][61] | [JSON](ao3_0fy_d45.json) |
| `A` | 秦孝文王 | [《史記・呂不韋列傳》][67] | [JSON](ao3_0fy_d45_A.json) |
| `AA` | 秦莊襄王 | [《史記・呂不韋列傳》][67] | [JSON](ao3_0fy_d45_AA.json) |
| `AAA` | 秦始皇帝 | [《史記・秦始皇本紀》][6] | [JSON](ao3_0fy_d45_AAA.json) |
| `AAAA` | 胡亥 | [《史記・秦始皇本紀》][6] | [JSON](ao3_0fy_d45_AAAA.json) |
| `AAAB` | 扶蘇 | [《史記・李斯列傳》][69] | [JSON](ao3_0fy_d45_AAAB.json) |

</details>

<details><summary><code>ath_xsq_n4i</code> 魯定公（11 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 魯定公 | [《史記・魯周公世家》][15] | [JSON](ath_xsq_n4i.json) |
| `A` | 魯哀公 | [《史記・魯周公世家》][15] | [JSON](ath_xsq_n4i_A.json) |
| `AA` | 寧（魯悼公） | [《史記・魯周公世家》][15] | [JSON](ath_xsq_n4i_AA.json) |
| `AAA` | 嘉（魯元公） | [《史記・魯周公世家》][15] | [JSON](ath_xsq_n4i_AAA.json) |
| `AAAA` | 顯（魯穆公） | [《史記・魯周公世家》][15] | [JSON](ath_xsq_n4i_AAAA.json) |
| `AAAAA` | 奮（魯共公） | [《史記・魯周公世家》][15] | [JSON](ath_xsq_n4i_AAAAA.json) |
| `AAAAAA` | 屯（魯康公） | [《史記・魯周公世家》][15] | [JSON](ath_xsq_n4i_AAAAAA.json) |
| `AAAAAAA` | 匽（魯景公） | [《史記・魯周公世家》][15] | [JSON](ath_xsq_n4i_AAAAAAA.json) |
| `AAAAAAAA` | 叔（魯平公） | [《史記・魯周公世家》][15] | [JSON](ath_xsq_n4i_AAAAAAAA.json) |
| `AAAAAAAAA` | 賈（魯文公） | [《史記・魯周公世家》][15] | [JSON](ath_xsq_n4i_AAAAAAAAA.json) |
| `AAAAAAAAAA` | 讎（魯頃公） | [《史記・魯周公世家》][15] | [JSON](ath_xsq_n4i_AAAAAAAAAA.json) |

</details>

<details><summary><code>awy_adj_c0u</code> 臧茶（韓信盧綰列傳候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 臧茶 | [《史記・韓信盧綰列傳》][75] | [JSON](awy_adj_c0u.json) |
| `A` | 衍（臧茶子） | [《史記・韓信盧綰列傳》][75] | [JSON](awy_adj_c0u_A.json) |

</details>

<details><summary><code>bc3_hmj_aps</code> 劉澤（荊燕世家候選）（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 劉澤 | [《史記・荊燕世家》][33] | [JSON](bc3_hmj_aps.json) |
| `A` | 嘉 | [《史記・荊燕世家》][33] | [JSON](bc3_hmj_aps_A.json) |
| `AA` | 定國 | [《史記・荊燕世家》][33] | [JSON](bc3_hmj_aps_AA.json) |

</details>

<details><summary><code>bm8_bzq_1ee</code> 觀起（蔡大夫）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 觀起（蔡大夫） | [《史記・楚世家》][22] | [JSON](bm8_bzq_1ee.json) |
| `A` | 觀從（楚變亂謀者） | [《史記・楚世家》][22] | [JSON](bm8_bzq_1ee_A.json) |

</details>

<details><summary><code>bn4_lhp_9h1</code> 姑容（杞桓公）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 姑容（杞桓公） | [《史記・陳杞世家》][18] | [JSON](bn4_lhp_9h1.json) |
| `A` | 丐（杞孝公） | [《史記・陳杞世家》][18] | [JSON](bn4_lhp_9h1_A.json) |

</details>

<details><summary><code>bni_7nd_jnt</code> 酈商（樊酈滕灌列傳候選）（6 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 酈商 | [《史記・樊酈滕灌列傳》][77] | [JSON](bni_7nd_jnt.json) |
| `A` | 酈堅 | [《史記・樊酈滕灌列傳》][77] | [JSON](bni_7nd_jnt_A.json) |
| `AA` | 酈遂成 | [《史記・樊酈滕灌列傳》][77] | [JSON](bni_7nd_jnt_AA.json) |
| `AAA` | 酈世宗 | [《史記・樊酈滕灌列傳》][77] | [JSON](bni_7nd_jnt_AAA.json) |
| `AAAA` | 酈終根 | [《史記・樊酈滕灌列傳》][77] | [JSON](bni_7nd_jnt_AAAA.json) |
| `B` | 酈寄 | [《史記・樊酈滕灌列傳》][77] | [JSON](bni_7nd_jnt_B.json) |

</details>

<details><summary><code>buv_igi_gpn</code> 帝乙（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 帝乙 | [《史記・殷本紀》][3] | [JSON](buv_igi_gpn.json) |
| `A` | 微子啓 | [《史記・宋微子世家》][20] | [JSON](buv_igi_gpn_A.json) |

</details>

<details><summary><code>c0i_eah_y59</code> 咎（韓世家釐王候選）（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 咎 | [《史記・韓世家》][27] | [JSON](c0i_eah_y59.json) |
| `A` | 桓惠王 | [《史記・韓世家》][27] | [JSON](c0i_eah_y59_A.json) |
| `AA` | 安 | [《史記・韓世家》][27] | [JSON](c0i_eah_y59_AA.json) |

</details>

<details><summary><code>c19_xxo_r8f</code> 直不疑（萬石張叔列傳候選）（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 直不疑 | [《史記・萬石張叔列傳》][85] | [JSON](c19_xxo_r8f.json) |
| `*A` | 望（直不疑孫） | [《史記・萬石張叔列傳》][85] | [JSON](c19_xxo_r8f_%2AA.json) |
| `A` | 相如（直不疑子） | [《史記・萬石張叔列傳》][85] | [JSON](c19_xxo_r8f_A.json) |

</details>

<details><summary><code>c1t_5mz_5ia</code> 晉昭公（趙世家候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 晉昭公 | [《史記・趙世家》][25] | [JSON](c1t_5mz_5ia.json) |
| `**A` | 驕 | [《史記・趙世家》][25] | [JSON](c1t_5mz_5ia_%2A%2AA.json) |

</details>

<details><summary><code>c2w_s7g_en0</code> 楚懷王（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 楚懷王 | [《史記・楚世家》][22] | [JSON](c2w_s7g_en0.json) |
| `*A` | 楚懷王心 | [《史記・高祖本紀》][8] | [JSON](c2w_s7g_en0_%2AA.json) |

</details>

<details><summary><code>cek_1yy_pne</code> 奄父（趙世家候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 奄父 | [《史記・趙世家》][25] | [JSON](cek_1yy_pne.json) |
| `A` | 叔帶 | [《史記・趙世家》][25] | [JSON](cek_1yy_pne_A.json) |

</details>

<details><summary><code>cjd_ybv_2wu</code> 蜚廉（趙世家祖系候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 蜚廉 | [《史記・趙世家》][25] | [JSON](cjd_ybv_2wu.json) |
| `A` | 惡來 | [《史記・趙世家》][25] | [JSON](cjd_ybv_2wu_A.json) |

</details>

<details><summary><code>d9b_5t4_9eb</code> 趙惠文王（廉頗藺相如列傳候選）（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 趙惠文王 | [《史記・廉頗藺相如列傳》][63] | [JSON](d9b_5t4_9eb.json) |
| `A` | 趙孝成王 | [《史記・平原君虞卿列傳》][58] | [JSON](d9b_5t4_9eb_A.json) |
| `AA` | 趙悼襄王 | [《史記・趙世家》][25] | [JSON](d9b_5t4_9eb_AA.json) |

</details>

<details><summary><code>d9y_q1n_fte</code> 樊噲（樊酈滕灌列傳候選）（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 樊噲 | [《史記・樊酈滕灌列傳》][77] | [JSON](d9y_q1n_fte.json) |
| `A` | 樊市人 | [《史記・樊酈滕灌列傳》][77] | [JSON](d9y_q1n_fte_A.json) |
| `B` | 樊伉 | [《史記・樊酈滕灌列傳》][77] | [JSON](d9y_q1n_fte_B.json) |

</details>

<details><summary><code>dm0_58v_50i</code> 趙衰（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 趙衰 | [《史記・晉世家》][21] | [JSON](dm0_58v_50i.json) |
| `A` | 趙盾 | [《史記・晉世家》][21] | [JSON](dm0_58v_50i_A.json) |

</details>

<details><summary><code>dng_dw6_2qy</code> 顏無繇（弟子列傳候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 顏無繇 | [《史記・仲尼弟子列傳》][49] | [JSON](dng_dw6_2qy.json) |
| `A` | 顏回 | [《史記・仲尼弟子列傳》][49] | [JSON](dng_dw6_2qy_A.json) |

</details>

<details><summary><code>dq6_ovk_58c</code> 張釋之（張釋之馮唐列傳候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 張釋之 | [《史記・張釋之馮唐列傳》][84] | [JSON](dq6_ovk_58c.json) |
| `A` | 張摯 | [《史記・張釋之馮唐列傳》][84] | [JSON](dq6_ovk_58c_A.json) |

</details>

<details><summary><code>e5t_5l9_wg0</code> 建（鄭世家楚太子候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 建 | [《史記・楚世家》][22] | [JSON](e5t_5l9_wg0.json) |
| `A` | 勝 | [《史記・楚世家》][22] | [JSON](e5t_5l9_wg0_A.json) |

</details>

<details><summary><code>e9l_7dr_a7o</code> 夏侯嬰（樊酈滕灌列傳候選）（4 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 夏侯嬰 | [《史記・樊酈滕灌列傳》][77] | [JSON](e9l_7dr_a7o.json) |
| `A` | 夏侯灶 | [《史記・樊酈滕灌列傳》][77] | [JSON](e9l_7dr_a7o_A.json) |
| `AA` | 夏侯賜 | [《史記・樊酈滕灌列傳》][77] | [JSON](e9l_7dr_a7o_AA.json) |
| `AAA` | 夏侯頗 | [《史記・樊酈滕灌列傳》][77] | [JSON](e9l_7dr_a7o_AAA.json) |

</details>

<details><summary><code>ea5_zvr_hlp</code> 張良（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 張良 | [《史記・留侯世家》][37] | [JSON](ea5_zvr_hlp.json) |
| `A` | 張辟彊 | [《史記・呂太后本紀》][9] | [JSON](ea5_zvr_hlp_A.json) |

</details>

<details><summary><code>ei2_qej_czn</code> 公乘氏（張耳陳餘列傳候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 公乘氏 | [《史記・張耳陳餘列傳》][71] | [JSON](ei2_qej_czn.json) |
| `A` | 陳餘妻未名 | [《史記・張耳陳餘列傳》][71] | [JSON](ei2_qej_czn_A.json) |

</details>

<details><summary><code>ei7_fai_lvy</code> 丑（鄭世家共公候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 丑 | [《史記・鄭世家》][24] | [JSON](ei7_fai_lvy.json) |
| `A` | 已 | [《史記・鄭世家》][24] | [JSON](ei7_fai_lvy_A.json) |

</details>

<details><summary><code>esh_e0a_jrw</code> 石奮父未名（萬石張叔列傳候選）（7 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 石奮父未名 | [《史記・萬石張叔列傳》][85] | [JSON](esh_e0a_jrw.json) |
| `A` | 石奮 | [《史記・萬石張叔列傳》][85] | [JSON](esh_e0a_jrw_A.json) |
| `AA` | 建（石奮長子） | [《史記・萬石張叔列傳》][85] | [JSON](esh_e0a_jrw_AA.json) |
| `AB` | 甲（石奮次子失名佔位） | [《史記・萬石張叔列傳》][85] | [JSON](esh_e0a_jrw_AB.json) |
| `AC` | 乙（石奮次子失名佔位） | [《史記・萬石張叔列傳》][85] | [JSON](esh_e0a_jrw_AC.json) |
| `AD` | 慶（石奮子） | [《史記・萬石張叔列傳》][85] | [JSON](esh_e0a_jrw_AD.json) |
| `ADA` | 德（石慶中子） | [《史記・萬石張叔列傳》][85] | [JSON](esh_e0a_jrw_ADA.json) |

</details>

<details><summary><code>ety_hqv_lhh</code> 輒父（孔子世家在外未名者）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 輒父（孔子世家在外未名者） | [《史記・衛康叔世家》][19] | [JSON](ety_hqv_lhh.json) |
| `A` | 輒 | [《史記・衛康叔世家》][19] | [JSON](ety_hqv_lhh_A.json) |

</details>

<details><summary><code>eva_gs1_9n5</code> 魏文侯（趙世家候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 魏文侯 | [《史記・趙世家》][25] | [JSON](eva_gs1_9n5.json) |
| `A` | 撃 | [《史記・魏世家》][26] | [JSON](eva_gs1_9n5_A.json) |

</details>

<details><summary><code>exh_47e_0gw</code> 酈食其（酈生陸賈列傳候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 酈食其 | [《史記・酈生陸賈列傳》][79] | [JSON](exh_47e_0gw.json) |
| `A` | 疥（酈食其子） | [《史記・酈生陸賈列傳》][79] | [JSON](exh_47e_0gw_A.json) |

</details>

<details><summary><code>f04_rc9_xqn</code> 太史敫（田世家候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 太史敫 | [《史記・田敬仲完世家》][28] | [JSON](f04_rc9_xqn.json) |
| `A` | 君王后 | [《史記・田敬仲完世家》][28] | [JSON](f04_rc9_xqn_A.json) |

</details>

<details><summary><code>f7y_qvp_mch</code> 楚懷王（屈原賈生列傳候選）（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 楚懷王 | [《史記・屈原賈生列傳》][66] | [JSON](f7y_qvp_mch.json) |
| `A` | 子蘭 | [《史記・屈原賈生列傳》][66] | [JSON](f7y_qvp_mch_A.json) |
| `B` | 頃襄王 | [《史記・屈原賈生列傳》][66] | [JSON](f7y_qvp_mch_B.json) |

</details>

<details><summary><code>f8d_j5p_nop</code> 孔防叔（孔子世家候選）（12 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 孔防叔 | [《史記・孔子世家》][29] | [JSON](f8d_j5p_nop.json) |
| `A` | 伯夏 | [《史記・孔子世家》][29] | [JSON](f8d_j5p_nop_A.json) |
| `AA` | 叔梁紇 | [《史記・孔子世家》][29] | [JSON](f8d_j5p_nop_AA.json) |
| `AAA` | 孔子 | [《史記・孔子世家》][29] | [JSON](f8d_j5p_nop_AAA.json) |
| `AAAA` | 鯉 | [《史記・孔子世家》][29] | [JSON](f8d_j5p_nop_AAAA.json) |
| `AAAAA` | 伋 | [《史記・孔子世家》][29] | [JSON](f8d_j5p_nop_AAAAA.json) |
| `AAAAAA` | 白 | [《史記・孔子世家》][29] | [JSON](f8d_j5p_nop_AAAAAA.json) |
| `AAAAAAA` | 求 | [《史記・孔子世家》][29] | [JSON](f8d_j5p_nop_AAAAAAA.json) |
| `AAAAAAAA` | 箕 | [《史記・孔子世家》][29] | [JSON](f8d_j5p_nop_AAAAAAAA.json) |
| `AAAAAAAAA` | 穿 | [《史記・孔子世家》][29] | [JSON](f8d_j5p_nop_AAAAAAAAA.json) |
| `AAAAAAAAAA` | 子慎 | [《史記・孔子世家》][29] | [JSON](f8d_j5p_nop_AAAAAAAAAA.json) |
| `AAAAAAAAAAA` | 鮒 | [《史記・孔子世家》][29] | [JSON](f8d_j5p_nop_AAAAAAAAAAA.json) |

</details>

<details><summary><code>faf_5al_ikw</code> 鄭武公（老韓列傳候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 鄭武公 | [《史記・老子韓非列傳》][45] | [JSON](faf_5al_ikw.json) |
| `A` | 鄭武公之子 | [《史記・老子韓非列傳》][45] | [JSON](faf_5al_ikw_A.json) |

</details>

<details><summary><code>fd2_w60_h42</code> 蒙驁（蒙恬列傳候選）（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 蒙驁 | [《史記・蒙恬列傳》][70] | [JSON](fd2_w60_h42.json) |
| `A` | 蒙武 | [《史記・蒙恬列傳》][70] | [JSON](fd2_w60_h42_A.json) |
| `AA` | 蒙恬 | [《史記・蒙恬列傳》][70] | [JSON](fd2_w60_h42_AA.json) |

</details>

<details><summary><code>fd3_tly_1lo</code> 沸（魯魏公）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 沸（魯魏公） | [《史記・魯周公世家》][15] | [JSON](fd3_tly_1lo.json) |
| `A` | 擢（魯厲公） | [《史記・魯周公世家》][15] | [JSON](fd3_tly_1lo_A.json) |

</details>

<details><summary><code>fea_it8_9n7</code> 韓厥（韓世家獻子候選）（14 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 韓厥 | [《史記・韓世家》][27] | [JSON](fea_it8_9n7.json) |
| `A` | 韓宣子 | [《史記・韓世家》][27] | [JSON](fea_it8_9n7_A.json) |
| `AA` | 韓貞子 | [《史記・韓世家》][27] | [JSON](fea_it8_9n7_AA.json) |
| `AAA` | 韓簡子 | [《史記・韓世家》][27] | [JSON](fea_it8_9n7_AAA.json) |
| `AAAA` | 韓莊子 | [《史記・韓世家》][27] | [JSON](fea_it8_9n7_AAAA.json) |
| `AAAAA` | 韓康子 | [《史記・韓世家》][27] | [JSON](fea_it8_9n7_AAAAA.json) |
| `AAAAAA` | 武子 | [《史記・韓世家》][27] | [JSON](fea_it8_9n7_AAAAAA.json) |
| `AAAAAAA` | 虔 | [《史記・韓世家》][27] | [JSON](fea_it8_9n7_AAAAAAA.json) |
| `AAAAAAAA` | 取 | [《史記・韓世家》][27] | [JSON](fea_it8_9n7_AAAAAAAA.json) |
| `AAAAAAAAA` | 韓文侯 | [《史記・韓世家》][27] | [JSON](fea_it8_9n7_AAAAAAAAA.json) |
| `AAAAAAAAAA` | 韓哀侯 | [《史記・韓世家》][27] | [JSON](fea_it8_9n7_AAAAAAAAAA.json) |
| `AAAAAAAAAAA` | 韓懿侯 | [《史記・韓世家》][27] | [JSON](fea_it8_9n7_AAAAAAAAAAA.json) |
| `AAAAAAAAAAAA` | 韓昭侯 | [《史記・韓世家》][27] | [JSON](fea_it8_9n7_AAAAAAAAAAAA.json) |
| `AAAAAAAAAAAAA` | 宣惠王 | [《史記・韓世家》][27] | [JSON](fea_it8_9n7_AAAAAAAAAAAAA.json) |

</details>

<details><summary><code>fvm_66f_0k3</code> 周緤（傅靳蒯成列傳候選）（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 周緤 | [《史記・傅靳蒯成列傳》][80] | [JSON](fvm_66f_0k3.json) |
| `A` | 周昌 | [《史記・傅靳蒯成列傳》][80] | [JSON](fvm_66f_0k3_A.json) |
| `B` | 周居 | [《史記・傅靳蒯成列傳》][80] | [JSON](fvm_66f_0k3_B.json) |

</details>

<details><summary><code>g9h_5ih_ug1</code> 伍奢（伍胥列傳候選）（4 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 伍奢 | [《史記・伍子胥列傳》][48] | [JSON](g9h_5ih_ug1.json) |
| `A` | 伍子胥 | [《史記・伍子胥列傳》][48] | [JSON](g9h_5ih_ug1_A.json) |
| `AA` | 伍子胥之子 | [《史記・伍子胥列傳》][48] | [JSON](g9h_5ih_ug1_AA.json) |
| `B` | 伍尚 | [《史記・伍子胥列傳》][48] | [JSON](g9h_5ih_ug1_B.json) |

</details>

<details><summary><code>ga6_jt5_6g1</code> 圉（衛孔文子）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 圉（衛孔文子） | [《史記・衛康叔世家》][19] | [JSON](ga6_jt5_6g1.json) |
| `A` | 悝（衛孔氏） | [《史記・衛康叔世家》][19] | [JSON](ga6_jt5_6g1_A.json) |

</details>

<details><summary><code>gau_cq7_7g1</code> 建（楚平王太子候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 建 | [《史記・楚世家》][22] | [JSON](gau_cq7_7g1.json) |
| `A` | 白公勝 | [《史記・楚世家》][22] | [JSON](gau_cq7_7g1_A.json) |

</details>

<details><summary><code>gcb_rf3_coi</code> 費王（晉穆侯）（4 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 費王（晉穆侯） | [《史記・晉世家》][21] | [JSON](gcb_rf3_coi.json) |
| `A` | 仇（晉文侯） | [《史記・晉世家》][21] | [JSON](gcb_rf3_coi_A.json) |
| `AA` | 伯（晉昭侯） | [《史記・晉世家》][21] | [JSON](gcb_rf3_coi_AA.json) |
| `B` | 成師（曲沃桓叔） | [《史記・晉世家》][21] | [JSON](gcb_rf3_coi_B.json) |

</details>

<details><summary><code>gh3_d07_hkt</code> 韓說（韓信盧綰列傳候選）（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 韓說 | [《史記・韓信盧綰列傳》][75] | [JSON](gh3_d07_hkt.json) |
| `*A` | 韓曾 | [《史記・韓信盧綰列傳》][75] | [JSON](gh3_d07_hkt_%2AA.json) |
| `A` | 韓代 | [《史記・韓信盧綰列傳》][75] | [JSON](gh3_d07_hkt_A.json) |

</details>

<details><summary><code>ghg_5p7_q21</code> 遂（杞釐公）（4 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 遂（杞釐公） | [《史記・陳杞世家》][18] | [JSON](ghg_5p7_q21.json) |
| `A` | 維（杞湣公） | [《史記・陳杞世家》][18] | [JSON](ghg_5p7_q21_A.json) |
| `AA` | 敕（杞出公） | [《史記・陳杞世家》][18] | [JSON](ghg_5p7_q21_AA.json) |
| `AAA` | 春（杞簡公） | [《史記・陳杞世家》][18] | [JSON](ghg_5p7_q21_AAA.json) |

</details>

<details><summary><code>gn7_br7_32m</code> 伯州犁（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 伯州犁 | [《史記・吳太伯世家》][13] | [JSON](gn7_br7_32m.json) |
| `*A` | 伯嚭 | [《史記・吳太伯世家》][13] | [JSON](gn7_br7_32m_%2AA.json) |

</details>

<details><summary><code>gts_42q_flu</code> 睔（鄭世家成公候選）（8 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 睔 | [《史記・鄭世家》][24] | [JSON](gts_42q_flu.json) |
| `A` | 惲 | [《史記・鄭世家》][24] | [JSON](gts_42q_flu_A.json) |
| `AA` | 嘉 | [《史記・鄭世家》][24] | [JSON](gts_42q_flu_AA.json) |
| `AAA` | 寧 | [《史記・鄭世家》][24] | [JSON](gts_42q_flu_AAA.json) |
| `AAAA` | 蠆 | [《史記・鄭世家》][24] | [JSON](gts_42q_flu_AAAA.json) |
| `AAAAA` | 勝 | [《史記・鄭世家》][24] | [JSON](gts_42q_flu_AAAAA.json) |
| `AAAAAA` | 易 | [《史記・鄭世家》][24] | [JSON](gts_42q_flu_AAAAAA.json) |
| `B` | 子産 | [《史記・鄭世家》][24] | [JSON](gts_42q_flu_B.json) |

</details>

<details><summary><code>gyt_axg_s7t</code> 田叔（田叔列傳候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 田叔 | [《史記・田叔列傳》][86] | [JSON](gyt_axg_s7t.json) |
| `A` | 田仁 | [《史記・田叔列傳》][86] | [JSON](gyt_axg_s7t_A.json) |

</details>

<details><summary><code>h69_ln7_f94</code> 太子建（伍胥列傳候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 太子建 | [《史記・伍子胥列傳》][48] | [JSON](h69_ln7_f94.json) |
| `A` | 勝 | [《史記・伍子胥列傳》][48] | [JSON](h69_ln7_f94_A.json) |

</details>

<details><summary><code>i30_mjq_6q8</code> 呂公（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 呂公 | [《史記・高祖本紀》][8] | [JSON](i30_mjq_6q8.json) |
| `A` | 呂后 | [《史記・呂太后本紀》][9] | [JSON](i30_mjq_6q8_A.json) |

</details>

<details><summary><code>i8i_rvh_4lp</code> 燬（衛文公）（8 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 燬（衛文公） | [《史記・衛康叔世家》][19] | [JSON](i8i_rvh_4lp.json) |
| `A` | 鄭（衛成公） | [《史記・衛康叔世家》][19] | [JSON](i8i_rvh_4lp_A.json) |
| `AA` | 遫（衛穆公） | [《史記・衛康叔世家》][19] | [JSON](i8i_rvh_4lp_AA.json) |
| `AAA` | 臧（衛定公） | [《史記・衛康叔世家》][19] | [JSON](i8i_rvh_4lp_AAA.json) |
| `AAAA` | 衎（衛獻公） | [《史記・衛康叔世家》][19] | [JSON](i8i_rvh_4lp_AAAA.json) |
| `AAAAA` | 惡（衛襄公） | [《史記・衛康叔世家》][19] | [JSON](i8i_rvh_4lp_AAAAA.json) |
| `AAAAAA` | 元（衛靈公） | [《史記・衛康叔世家》][19] | [JSON](i8i_rvh_4lp_AAAAAA.json) |
| `AAAAAAA` | 郢（衛子南） | [《史記・衛康叔世家》][19] | [JSON](i8i_rvh_4lp_AAAAAAA.json) |

</details>

<details><summary><code>idh_bo6_4kq</code> 樂毅（樂毅列傳候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 樂毅 | [《史記・樂毅列傳》][62] | [JSON](idh_bo6_4kq.json) |
| `A` | 樂閒 | [《史記・樂毅列傳》][62] | [JSON](idh_bo6_4kq_A.json) |

</details>

<details><summary><code>iij_zqi_k5l</code> 齊平公（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 齊平公 | [《史記・齊太公世家》][14] | [JSON](iij_zqi_k5l.json) |
| `A` | 積（齊宣公） | [《史記・齊太公世家》][14] | [JSON](iij_zqi_k5l_A.json) |
| `AA` | 貸（齊康公） | [《史記・齊太公世家》][14] | [JSON](iij_zqi_k5l_AA.json) |

</details>

<details><summary><code>inr_w1g_bu5</code> 子襄（孔子世家候選）（7 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 子襄 | [《史記・孔子世家》][29] | [JSON](inr_w1g_bu5.json) |
| `A` | 忠 | [《史記・孔子世家》][29] | [JSON](inr_w1g_bu5_A.json) |
| `AA` | 武 | [《史記・孔子世家》][29] | [JSON](inr_w1g_bu5_AA.json) |
| `AAA` | 延年 | [《史記・孔子世家》][29] | [JSON](inr_w1g_bu5_AAA.json) |
| `AAB` | 安國 | [《史記・孔子世家》][29] | [JSON](inr_w1g_bu5_AAB.json) |
| `AABA` | 卬 | [《史記・孔子世家》][29] | [JSON](inr_w1g_bu5_AABA.json) |
| `AABAA` | 驩 | [《史記・孔子世家》][29] | [JSON](inr_w1g_bu5_AABAA.json) |

</details>

<details><summary><code>ixk_6fg_v6f</code> 竇后父（外戚世家候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 竇后父 | [《史記・外戚世家》][31] | [JSON](ixk_6fg_v6f.json) |
| `A` | 竇太后 | [《史記・外戚世家》][31] | [JSON](ixk_6fg_v6f_A.json) |

</details>

<details><summary><code>j32_wtj_khz</code> 袁盎父未名（袁盎鼂錯列傳候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 袁盎父未名 | [《史記・袁盎鼂錯列傳》][83] | [JSON](j32_wtj_khz.json) |
| `A` | 袁盎 | [《史記・袁盎鼂錯列傳》][83] | [JSON](j32_wtj_khz_A.json) |

</details>

<details><summary><code>j80_2bm_4af</code> 田儋（田儋列傳候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 田儋 | [《史記・田儋列傳》][76] | [JSON](j80_2bm_4af.json) |
| `A` | 田市 | [《史記・田儋列傳》][76] | [JSON](j80_2bm_4af_A.json) |

</details>

<details><summary><code>jjl_irg_zke</code> 盧綰父未名（韓信盧綰列傳候選）（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 盧綰父未名 | [《史記・韓信盧綰列傳》][75] | [JSON](jjl_irg_zke.json) |
| `A` | 盧綰 | [《史記・韓信盧綰列傳》][75] | [JSON](jjl_irg_zke_A.json) |
| `A*A` | 盧他之 | [《史記・韓信盧綰列傳》][75] | [JSON](jjl_irg_zke_A%2AA.json) |

</details>

<details><summary><code>jru_oiq_x0q</code> 楚成王（鄭世家候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 楚成王 | [《史記・鄭世家》][24] | [JSON](jru_oiq_x0q.json) |
| `A` | 商臣 | [《史記・鄭世家》][24] | [JSON](jru_oiq_x0q_A.json) |

</details>

<details><summary><code>jx9_cov_qe0</code> 欒布（季布欒布列傳候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 欒布 | [《史記・季布欒布列傳》][82] | [JSON](jx9_cov_qe0.json) |
| `A` | 賁（欒布子） | [《史記・季布欒布列傳》][82] | [JSON](jx9_cov_qe0_A.json) |

</details>

<details><summary><code>k5z_d58_n7p</code> 熊元（楚考烈王）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 熊元（楚考烈王） | [《史記・春申君列傳》][60] | [JSON](k5z_d58_n7p.json) |
| `A` | 悍（楚幽王） | [《史記・春申君列傳》][60] | [JSON](k5z_d58_n7p_A.json) |

</details>

<details><summary><code>kat_48c_thr</code> 晉襄公（4 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 晉襄公 | [《史記・晉世家》][21] | [JSON](kat_48c_thr.json) |
| `A` | 捷（晉襄公少子桓叔） | [《史記・晉世家》][21] | [JSON](kat_48c_thr_A.json) |
| `AA` | 談（惠伯） | [《史記・晉世家》][21] | [JSON](kat_48c_thr_AA.json) |
| `AAA` | 晉悼公 | [《史記・晉世家》][21] | [JSON](kat_48c_thr_AAA.json) |

</details>

<details><summary><code>kbc_11y_cku</code> 堅（鄭世家襄公候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 堅 | [《史記・鄭世家》][24] | [JSON](kbc_11y_cku.json) |
| `A` | 沸 | [《史記・鄭世家》][24] | [JSON](kbc_11y_cku_A.json) |

</details>

<details><summary><code>krx_d9v_3wv</code> 冒頓父未名（劉敬叔孫通列傳候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 冒頓父未名 | [《史記・劉敬叔孫通列傳》][81] | [JSON](krx_d9v_3wv.json) |
| `A` | 冒頓 | [《史記・韓信盧綰列傳》][75] | [JSON](krx_d9v_3wv_A.json) |

</details>

<details><summary><code>kt8_3kv_44r</code> 頑（衛昭伯）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 頑（衛昭伯） | [《史記・衛康叔世家》][19] | [JSON](kt8_3kv_44r.json) |
| `A` | 申（衛戴公） | [《史記・衛康叔世家》][19] | [JSON](kt8_3kv_44r_A.json) |

</details>

<details><summary><code>ktk_wbg_wnm</code> 鄧公（袁盎鼂錯列傳候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 鄧公 | [《史記・袁盎鼂錯列傳》][83] | [JSON](ktk_wbg_wnm.json) |
| `A` | 章（鄧公子） | [《史記・袁盎鼂錯列傳》][83] | [JSON](ktk_wbg_wnm_A.json) |

</details>

<details><summary><code>l3c_zg4_f7z</code> 宋襄公（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 宋襄公 | [《史記・宋微子世家》][20] | [JSON](l3c_zg4_f7z.json) |
| `A` | 王臣（宋成公） | [《史記・宋微子世家》][20] | [JSON](l3c_zg4_f7z_A.json) |
| `AA` | 杵臼（宋昭公） | [《史記・宋微子世家》][20] | [JSON](l3c_zg4_f7z_AA.json) |

</details>

<details><summary><code>l8e_pxu_xre</code> 武公（趙世家趙君候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 武公 | [《史記・趙世家》][25] | [JSON](l8e_pxu_xre.json) |
| `A` | 朝 | [《史記・趙世家》][25] | [JSON](l8e_pxu_xre_A.json) |

</details>

<details><summary><code>lc6_cup_v9c</code> 稱（魯孝公）（5 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 稱（魯孝公） | [《史記・魯周公世家》][15] | [JSON](lc6_cup_v9c.json) |
| `A` | 弗湟（魯惠公） | [《史記・魯周公世家》][15] | [JSON](lc6_cup_v9c_A.json) |
| `AA` | 魯隱公 | [《史記・魯周公世家》][15] | [JSON](lc6_cup_v9c_AA.json) |
| `AB` | 魯桓公 | [《史記・魯周公世家》][15] | [JSON](lc6_cup_v9c_AB.json) |
| `ABA` | 季友（成季） | [《史記・魯周公世家》][15] | [JSON](lc6_cup_v9c_ABA.json) |

</details>

<details><summary><code>lcc_msq_vdt</code> 露（曹靖公）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 露（曹靖公） | [《史記・管蔡世家》][17] | [JSON](lcc_msq_vdt.json) |
| `A` | 伯陽（曹君） | [《史記・管蔡世家》][17] | [JSON](lcc_msq_vdt_A.json) |

</details>

<details><summary><code>lmu_nbm_rzo</code> 燮（陳平公）（7 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 燮（陳平公） | [《史記・陳杞世家》][18] | [JSON](lmu_nbm_rzo.json) |
| `A` | 圉（陳文公） | [《史記・陳杞世家》][18] | [JSON](lmu_nbm_rzo_A.json) |
| `AA` | 佗（陳厲公） | [《史記・陳杞世家》][18] | [JSON](lmu_nbm_rzo_AA.json) |
| `AAA` | 完（敬仲） | [《史記・田敬仲完世家》][28] | [JSON](lmu_nbm_rzo_AAA.json) |
| `AB` | 鮑（陳桓公） | [《史記・陳杞世家》][18] | [JSON](lmu_nbm_rzo_AB.json) |
| `ABA` | 免（陳桓公太子） | [《史記・陳杞世家》][18] | [JSON](lmu_nbm_rzo_ABA.json) |
| `ABB` | 躍（陳利公） | [《史記・陳杞世家》][18] | [JSON](lmu_nbm_rzo_ABB.json) |

</details>

<details><summary><code>lt4_hpv_4ku</code> 武成王（燕君）（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 武成王（燕君） | [《史記・燕召公世家》][16] | [JSON](lt4_hpv_4ku.json) |
| `A` | 孝王（燕君） | [《史記・燕召公世家》][16] | [JSON](lt4_hpv_4ku_A.json) |
| `AA` | 燕王喜 | [《史記・燕召公世家》][16] | [JSON](lt4_hpv_4ku_AA.json) |

</details>

<details><summary><code>lwx_9yq_ad7</code> 紂（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 紂 | [《史記・殷本紀》][3] | [JSON](lwx_9yq_ad7.json) |
| `A` | 武庚 | [《史記・衛康叔世家》][19] | [JSON](lwx_9yq_ad7_A.json) |

</details>

<details><summary><code>ly0_vry_w1c</code> 燕昭王（樂毅列傳候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 燕昭王 | [《史記・樂毅列傳》][62] | [JSON](ly0_vry_w1c.json) |
| `A` | 燕惠王 | [《史記・樂毅列傳》][62] | [JSON](ly0_vry_w1c_A.json) |

</details>

<details><summary><code>m0b_b5e_153</code> 田常（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 田常 | [《史記・齊太公世家》][14] | [JSON](m0b_b5e_153.json) |
| `**A` | 田和 | [《史記・齊太公世家》][14]、[《史記・陳杞世家》][18] | [JSON](m0b_b5e_153_%2A%2AA.json) |

</details>

<details><summary><code>m0z_vep_k8y</code> 諸樊（刺客列傳候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 諸樊 | [《史記・刺客列傳》][68] | [JSON](m0z_vep_k8y.json) |
| `A` | 公子光 | [《史記・刺客列傳》][68] | [JSON](m0z_vep_k8y_A.json) |

</details>

<details><summary><code>m8d_pnd_ias</code> 惠侯（燕君）（10 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 惠侯（燕君） | [《史記・燕召公世家》][16] | [JSON](m8d_pnd_ias.json) |
| `A` | 釐侯（燕君） | [《史記・燕召公世家》][16] | [JSON](m8d_pnd_ias_A.json) |
| `AA` | 頃侯（燕君） | [《史記・燕召公世家》][16] | [JSON](m8d_pnd_ias_AA.json) |
| `AAA` | 哀侯（燕君） | [《史記・燕召公世家》][16] | [JSON](m8d_pnd_ias_AAA.json) |
| `AAAA` | 鄭侯（燕君） | [《史記・燕召公世家》][16] | [JSON](m8d_pnd_ias_AAAA.json) |
| `AAAAA` | 繆侯（燕君） | [《史記・燕召公世家》][16] | [JSON](m8d_pnd_ias_AAAAA.json) |
| `AAAAAA` | 宣侯（燕君） | [《史記・燕召公世家》][16] | [JSON](m8d_pnd_ias_AAAAAA.json) |
| `AAAAAAA` | 桓侯（燕君） | [《史記・燕召公世家》][16] | [JSON](m8d_pnd_ias_AAAAAAA.json) |
| `AAAAAAAA` | 燕莊公 | [《史記・齊太公世家》][14]、[《史記・燕召公世家》][16] | [JSON](m8d_pnd_ias_AAAAAAAA.json) |
| `AAAAAAAAA` | 襄公（燕君） | [《史記・燕召公世家》][16] | [JSON](m8d_pnd_ias_AAAAAAAAA.json) |

</details>

<details><summary><code>m9n_b6v_wo0</code> 梁孝王（本卷未名）（5 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 梁孝王（本卷未名） | [《史記・孝景本紀》][11] | [JSON](m9n_b6v_wo0.json) |
| `A` | 明（梁孝王子） | [《史記・孝景本紀》][11] | [JSON](m9n_b6v_wo0_A.json) |
| `B` | 彭離（梁孝王子） | [《史記・孝景本紀》][11] | [JSON](m9n_b6v_wo0_B.json) |
| `C` | 定（梁孝王子） | [《史記・孝景本紀》][11] | [JSON](m9n_b6v_wo0_C.json) |
| `D` | 不識（梁孝王子） | [《史記・孝景本紀》][11] | [JSON](m9n_b6v_wo0_D.json) |

</details>

<details><summary><code>maz_aq2_t5g</code> 季勝（趙世家祖系候選）（4 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 季勝 | [《史記・趙世家》][25] | [JSON](maz_aq2_t5g.json) |
| `A` | 孟增 | [《史記・趙世家》][25] | [JSON](maz_aq2_t5g_A.json) |
| `AA` | 衡父 | [《史記・趙世家》][25] | [JSON](maz_aq2_t5g_AA.json) |
| `AAA` | 造父 | [《史記・趙世家》][25] | [JSON](maz_aq2_t5g_AAA.json) |

</details>

<details><summary><code>mby_4zh_oni</code> 安國君（呂不韋列傳候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 安國君 | [《史記・呂不韋列傳》][67] | [JSON](mby_4zh_oni.json) |
| `A` | 子楚 | [《史記・呂不韋列傳》][67] | [JSON](mby_4zh_oni_A.json) |

</details>

<details><summary><code>mdl_l60_pwy</code> 灌嬰（樊酈滕灌列傳候選）（4 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 灌嬰 | [《史記・樊酈滕灌列傳》][77] | [JSON](mdl_l60_pwy.json) |
| `*A` | 灌賢 | [《史記・樊酈滕灌列傳》][77] | [JSON](mdl_l60_pwy_%2AA.json) |
| `A` | 灌阿 | [《史記・樊酈滕灌列傳》][77] | [JSON](mdl_l60_pwy_A.json) |
| `AA` | 灌彊 | [《史記・樊酈滕灌列傳》][77] | [JSON](mdl_l60_pwy_AA.json) |

</details>

<details><summary><code>mgh_3bh_rit</code> 周厲王（鄭世家候選）（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 周厲王 | [《史記・鄭世家》][24] | [JSON](mgh_3bh_rit.json) |
| `A` | 友 | [《史記・鄭世家》][24] | [JSON](mgh_3bh_rit_A.json) |
| `AA` | 掘突 | [《史記・鄭世家》][24] | [JSON](mgh_3bh_rit_AA.json) |

</details>

<details><summary><code>mpi_zkg_f48</code> 楚懷王（春申君列傳候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 楚懷王 | [《史記・楚世家》][22] | [JSON](mpi_zkg_f48.json) |
| `A` | 楚頃襄王 | [《史記・楚世家》][22] | [JSON](mpi_zkg_f48_A.json) |

</details>

<details><summary><code>ms3_fa1_ps9</code> 田生（荊燕世家候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 田生 | [《史記・荊燕世家》][33] | [JSON](ms3_fa1_ps9.json) |
| `A` | 田生子 | [《史記・荊燕世家》][33] | [JSON](ms3_fa1_ps9_A.json) |

</details>

<details><summary><code>muq_yy8_8er</code> 寤生（鄭世家莊公候選）（5 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 寤生 | [《史記・鄭世家》][24] | [JSON](muq_yy8_8er.json) |
| `A` | 忽 | [《史記・鄭世家》][24] | [JSON](muq_yy8_8er_A.json) |
| `B` | 突 | [《史記・鄭世家》][24] | [JSON](muq_yy8_8er_B.json) |
| `BA` | 踕 | [《史記・鄭世家》][24] | [JSON](muq_yy8_8er_BA.json) |
| `BAA` | 蘭 | [《史記・鄭世家》][24] | [JSON](muq_yy8_8er_BAA.json) |

</details>

<details><summary><code>n0i_g82_0n2</code> 蒯聵（衛莊公）（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 蒯聵（衛莊公） | [《史記・衛康叔世家》][19] | [JSON](n0i_g82_0n2.json) |
| `A` | 輒（衛出公） | [《史記・衛康叔世家》][19] | [JSON](n0i_g82_0n2_A.json) |
| `AA` | 出公子（衛黔所攻者未名） | [《史記・衛康叔世家》][19] | [JSON](n0i_g82_0n2_AA.json) |

</details>

<details><summary><code>n4f_fqh_04q</code> 易王（燕君）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 易王（燕君） | [《史記・蘇秦列傳》][51] | [JSON](n4f_fqh_04q.json) |
| `A` | 燕噲（本篇燕君） | [《史記・燕召公世家》][16] | [JSON](n4f_fqh_04q_A.json) |

</details>

<details><summary><code>net_rj0_wi8</code> 張耳（張耳陳餘列傳候選）（5 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 張耳 | [《史記・張耳陳餘列傳》][71] | [JSON](net_rj0_wi8.json) |
| `A` | 張敖 | [《史記・張耳陳餘列傳》][71] | [JSON](net_rj0_wi8_A.json) |
| `AA` | 張偃 | [《史記・張耳陳餘列傳》][71] | [JSON](net_rj0_wi8_AA.json) |
| `AB` | 張壽 | [《史記・張耳陳餘列傳》][71] | [JSON](net_rj0_wi8_AB.json) |
| `AC` | 張侈 | [《史記・張耳陳餘列傳》][71] | [JSON](net_rj0_wi8_AC.json) |

</details>

<details><summary><code>nfj_6w2_8mn</code> 增（魏世家景湣王候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 增 | [《史記・魏世家》][26] | [JSON](nfj_6w2_8mn.json) |
| `A` | 假 | [《史記・魏世家》][26] | [JSON](nfj_6w2_8mn_A.json) |

</details>

<details><summary><code>nxl_qt6_cpl</code> 畢萬（魏世家候選）（15 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 畢萬 | [《史記・魏世家》][26] | [JSON](nxl_qt6_cpl.json) |
| `A` | 魏武子 | [《史記・魏世家》][26] | [JSON](nxl_qt6_cpl_A.json) |
| `AA` | 魏悼子 | [《史記・魏世家》][26] | [JSON](nxl_qt6_cpl_AA.json) |
| `AAA` | 魏絳 | [《史記・魏世家》][26] | [JSON](nxl_qt6_cpl_AAA.json) |
| `AAAA` | 魏嬴 | [《史記・魏世家》][26] | [JSON](nxl_qt6_cpl_AAAA.json) |
| `AAAAA` | 魏獻子 | [《史記・魏世家》][26] | [JSON](nxl_qt6_cpl_AAAAA.json) |
| `AAAAAA` | 魏侈 | [《史記・魏世家》][26] | [JSON](nxl_qt6_cpl_AAAAAA.json) |
| `AAAAAA*A` | 魏桓子 | [《史記・魏世家》][26] | [JSON](nxl_qt6_cpl_AAAAAA%2AA.json) |
| `AAAAAA*A*A` | 都 | [《史記・魏世家》][26] | [JSON](nxl_qt6_cpl_AAAAAA%2AA%2AA.json) |
| `AAAAAA*A*AA` | 撃 | [《史記・魏世家》][26] | [JSON](nxl_qt6_cpl_AAAAAA%2AA%2AAA.json) |
| `AAAAAA*A*AAA` | 罃 | [《史記・魏世家》][26] | [JSON](nxl_qt6_cpl_AAAAAA%2AA%2AAAA.json) |
| `AAAAAA*A*AAAA` | 襄王 | [《史記・魏世家》][26] | [JSON](nxl_qt6_cpl_AAAAAA%2AA%2AAAAA.json) |
| `AAAAAA*A*AAAAA` | 哀王 | [《史記・魏世家》][26] | [JSON](nxl_qt6_cpl_AAAAAA%2AA%2AAAAAA.json) |
| `AAAAAA*A*AAAAAA` | 昭王 | [《史記・魏世家》][26] | [JSON](nxl_qt6_cpl_AAAAAA%2AA%2AAAAAAA.json) |
| `AAAAAA*A*AAAAAAA` | 安釐王 | [《史記・魏公子列傳》][59] | [JSON](nxl_qt6_cpl_AAAAAA%2AA%2AAAAAAAA.json) |

</details>

<details><summary><code>nye_x8g_zwl</code> 陳桓公鮑（田世家候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 陳桓公鮑 | [《史記・田敬仲完世家》][28] | [JSON](nye_x8g_zwl.json) |
| `A` | 陳莊公林 | [《史記・田敬仲完世家》][28] | [JSON](nye_x8g_zwl_A.json) |

</details>

<details><summary><code>o0l_em5_5v9</code> 吳芮（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 吳芮 | [《史記・高祖本紀》][8] | [JSON](o0l_em5_5v9.json) |
| `A` | 臣（吳芮子） | [《史記・呂太后本紀》][9] | [JSON](o0l_em5_5v9_A.json) |

</details>

<details><summary><code>opr_t0a_l8g</code> 淳于公（齊太倉令）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 淳于公（齊太倉令） | [《史記・扁鵲倉公列傳》][87] | [JSON](opr_t0a_l8g.json) |
| `A` | 緹縈 | [《史記・扁鵲倉公列傳》][87] | [JSON](opr_t0a_l8g_A.json) |

</details>

<details><summary><code>osu_yvw_bwr</code> 熊惲（楚成王候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 熊惲 | [《史記・楚世家》][22] | [JSON](osu_yvw_bwr.json) |
| `A` | 職（楚成王欲立之子） | [《史記・楚世家》][22] | [JSON](osu_yvw_bwr_A.json) |

</details>

<details><summary><code>p9l_wy7_y7m</code> 魏文侯（孫吳列傳候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 魏文侯 | [《史記・孫子吳起列傳》][47] | [JSON](p9l_wy7_y7m.json) |
| `A` | 魏武侯 | [《史記・孫子吳起列傳》][47] | [JSON](p9l_wy7_y7m_A.json) |

</details>

<details><summary><code>pev_wez_mab</code> 宋富人（老韓列傳候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 宋富人 | [《史記・老子韓非列傳》][45] | [JSON](pev_wez_mab.json) |
| `A` | 富人之子 | [《史記・老子韓非列傳》][45] | [JSON](pev_wez_mab_A.json) |

</details>

<details><summary><code>pg6_rqk_vuk</code> 如姬父未名（魏公子列傳候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 如姬父未名 | [《史記・魏公子列傳》][59] | [JSON](pg6_rqk_vuk.json) |
| `A` | 如姬 | [《史記・魏公子列傳》][59] | [JSON](pg6_rqk_vuk_A.json) |

</details>

<details><summary><code>pj3_k53_wtj</code> 觸龍（趙世家左師候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 觸龍 | [《史記・趙世家》][25] | [JSON](pj3_k53_wtj.json) |
| `A` | 舒祺 | [《史記・趙世家》][25] | [JSON](pj3_k53_wtj_A.json) |

</details>

<details><summary><code>pyb_nda_bwz</code> 鄖公與懷之父（伍胥列傳候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 鄖公與懷之父 | [《史記・伍子胥列傳》][48] | [JSON](pyb_nda_bwz.json) |
| `A` | 懷 | [《史記・伍子胥列傳》][48] | [JSON](pyb_nda_bwz_A.json) |

</details>

<details><summary><code>pyc_fs9_nif</code> 齊湣王（田單列傳候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 齊湣王 | [《史記・田單列傳》][64] | [JSON](pyc_fs9_nif.json) |
| `A` | 法章齊襄王 | [《史記・田敬仲完世家》][28] | [JSON](pyc_fs9_nif_A.json) |

</details>

<details><summary><code>q1y_uet_htw</code> 伯州犁（伍胥列傳候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 伯州犁 | [《史記・伍子胥列傳》][48] | [JSON](q1y_uet_htw.json) |
| `*A` | 伯嚭 | [《史記・伍子胥列傳》][48] | [JSON](q1y_uet_htw_%2AA.json) |

</details>

<details><summary><code>q4v_vmz_dvi</code> 老子（老韓列傳候選）（4 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 老子 | [《史記・老子韓非列傳》][45] | [JSON](q4v_vmz_dvi.json) |
| `A` | 宗 | [《史記・老子韓非列傳》][45] | [JSON](q4v_vmz_dvi_A.json) |
| `AA` | 注 | [《史記・老子韓非列傳》][45] | [JSON](q4v_vmz_dvi_AA.json) |
| `AAA` | 宮 | [《史記・老子韓非列傳》][45] | [JSON](q4v_vmz_dvi_AAA.json) |

</details>

<details><summary><code>q60_34y_1zh</code> 章（楚惠王）（5 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 章（楚惠王） | [《史記・楚世家》][22] | [JSON](q60_34y_1zh.json) |
| `A` | 中（楚簡王） | [《史記・楚世家》][22] | [JSON](q60_34y_1zh_A.json) |
| `AA` | 當（楚聲王） | [《史記・楚世家》][22] | [JSON](q60_34y_1zh_AA.json) |
| `AAA` | 熊疑（楚悼王） | [《史記・楚世家》][22] | [JSON](q60_34y_1zh_AAA.json) |
| `AAAA` | 臧（楚肅王） | [《史記・楚世家》][22] | [JSON](q60_34y_1zh_AAAA.json) |

</details>

<details><summary><code>q6w_qm5_w2b</code> 丹（趙世家孝成王候選）（4 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 丹 | [《史記・平原君虞卿列傳》][58] | [JSON](q6w_qm5_w2b.json) |
| `A` | 偃 | [《史記・趙世家》][25] | [JSON](q6w_qm5_w2b_A.json) |
| `AA` | 遷 | [《史記・趙世家》][25] | [JSON](q6w_qm5_w2b_AA.json) |
| `AB` | 嘉 | [《史記・趙世家》][25] | [JSON](q6w_qm5_w2b_AB.json) |

</details>

<details><summary><code>q7c_rp0_s04</code> 趙主父（楚篇懷王奔趙時）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 趙主父（楚篇懷王奔趙時） | [《史記・楚世家》][22] | [JSON](q7c_rp0_s04.json) |
| `A` | 趙惠王（楚篇初立者） | [《史記・楚世家》][22] | [JSON](q7c_rp0_s04_A.json) |

</details>

<details><summary><code>qdt_1oy_jci</code> 杵臼（陳宣公）（7 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 杵臼（陳宣公） | [《史記・陳杞世家》][18] | [JSON](qdt_1oy_jci.json) |
| `A` | 款（陳穆公） | [《史記・陳杞世家》][18] | [JSON](qdt_1oy_jci_A.json) |
| `AA` | 朔（陳共公） | [《史記・陳杞世家》][18] | [JSON](qdt_1oy_jci_AA.json) |
| `AAA` | 平國（陳靈公） | [《史記・陳杞世家》][18] | [JSON](qdt_1oy_jci_AAA.json) |
| `AAAA` | 午（陳成公） | [《史記・陳杞世家》][18] | [JSON](qdt_1oy_jci_AAAA.json) |
| `AAAAA` | 哀公（陳君） | [《史記・陳杞世家》][18] | [JSON](qdt_1oy_jci_AAAAA.json) |
| `B` | 御寇（陳宣公太子） | [《史記・陳杞世家》][18] | [JSON](qdt_1oy_jci_B.json) |

</details>

<details><summary><code>qh8_95j_eh2</code> 獻舞（蔡哀侯）（10 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 獻舞（蔡哀侯） | [《史記・管蔡世家》][17] | [JSON](qh8_95j_eh2.json) |
| `A` | 肸（蔡繆侯） | [《史記・管蔡世家》][17] | [JSON](qh8_95j_eh2_A.json) |
| `AA` | 果（蔡莊侯） | [《史記・管蔡世家》][17] | [JSON](qh8_95j_eh2_AA.json) |
| `AAA` | 申（蔡文侯） | [《史記・管蔡世家》][17] | [JSON](qh8_95j_eh2_AAA.json) |
| `AAAA` | 固（蔡景侯） | [《史記・管蔡世家》][17] | [JSON](qh8_95j_eh2_AAAA.json) |
| `AAAAA` | 般（蔡靈侯） | [《史記・管蔡世家》][17] | [JSON](qh8_95j_eh2_AAAAA.json) |
| `AAAAAA` | 友（蔡隱太子） | [《史記・管蔡世家》][17] | [JSON](qh8_95j_eh2_AAAAAA.json) |
| `AAAAAAA` | 東國（蔡悼侯） | [《史記・管蔡世家》][17] | [JSON](qh8_95j_eh2_AAAAAAA.json) |
| `AAAAB` | 廬（蔡平侯） | [《史記・管蔡世家》][17] | [JSON](qh8_95j_eh2_AAAAB.json) |
| `AAAABA` | 平侯子（被東國攻者未名） | [《史記・管蔡世家》][17] | [JSON](qh8_95j_eh2_AAAABA.json) |

</details>

<details><summary><code>qlm_m3s_f3b</code> 楚平王（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 楚平王 | [《史記・伍子胥列傳》][48] | [JSON](qlm_m3s_f3b.json) |
| `A` | 太子建（楚） | [《史記・秦本紀》][5] | [JSON](qlm_m3s_f3b_A.json) |

</details>

<details><summary><code>qok_ik2_99j</code> 壽（齊悼惠王世家候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 壽 | [《史記・齊悼惠王世家》][34] | [JSON](qok_ik2_99j.json) |
| `A` | 次景 | [《史記・齊悼惠王世家》][34] | [JSON](qok_ik2_99j_A.json) |

</details>

<details><summary><code>qxa_jm7_zmy</code> 黔（衛悼公）（10 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 黔（衛悼公） | [《史記・衛康叔世家》][19] | [JSON](qxa_jm7_zmy.json) |
| `A` | 弗（衛敬公） | [《史記・衛康叔世家》][19] | [JSON](qxa_jm7_zmy_A.json) |
| `AA` | 糾（衛昭公） | [《史記・衛康叔世家》][19] | [JSON](qxa_jm7_zmy_AA.json) |
| `AB` | 適（衛公子） | [《史記・衛康叔世家》][19] | [JSON](qxa_jm7_zmy_AB.json) |
| `ABA` | 穨（衛愼公） | [《史記・衛康叔世家》][19] | [JSON](qxa_jm7_zmy_ABA.json) |
| `ABAA` | 訓（衛聲公） | [《史記・衛康叔世家》][19] | [JSON](qxa_jm7_zmy_ABAA.json) |
| `ABAAA` | 遫（衛成侯） | [《史記・衛康叔世家》][19] | [JSON](qxa_jm7_zmy_ABAAA.json) |
| `ABAAAA` | 平侯（衛成侯子） | [《史記・衛康叔世家》][19] | [JSON](qxa_jm7_zmy_ABAAAA.json) |
| `ABAAAAA` | 嗣君（衛平侯子） | [《史記・衛康叔世家》][19] | [JSON](qxa_jm7_zmy_ABAAAAA.json) |
| `ABAAAAAA` | 懷君（衛嗣君子） | [《史記・衛康叔世家》][19] | [JSON](qxa_jm7_zmy_ABAAAAAA.json) |

</details>

<details><summary><code>qy1_adc_gam</code> 晉（衛宣公）（5 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 晉（衛宣公） | [《史記・衛康叔世家》][19] | [JSON](qy1_adc_gam.json) |
| `A` | 伋（衛宣公太子） | [《史記・衛康叔世家》][19] | [JSON](qy1_adc_gam_A.json) |
| `B` | 壽（衛宣公子） | [《史記・衛康叔世家》][19] | [JSON](qy1_adc_gam_B.json) |
| `C` | 朔（衛惠公） | [《史記・衛康叔世家》][19] | [JSON](qy1_adc_gam_C.json) |
| `CA` | 赤（衛懿公） | [《史記・衛康叔世家》][19] | [JSON](qy1_adc_gam_CA.json) |

</details>

<details><summary><code>r9u_j0z_xtb</code> 秦侯（5 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 秦侯 | [《史記・秦本紀》][5] | [JSON](r9u_j0z_xtb.json) |
| `A` | 公伯 | [《史記・秦本紀》][5] | [JSON](r9u_j0z_xtb_A.json) |
| `AA` | 秦仲 | [《史記・秦本紀》][5] | [JSON](r9u_j0z_xtb_AA.json) |
| `AAA` | 秦莊公 | [《史記・秦本紀》][5] | [JSON](r9u_j0z_xtb_AAA.json) |
| `AAAA` | 世父 | [《史記・秦本紀》][5] | [JSON](r9u_j0z_xtb_AAAA.json) |

</details>

<details><summary><code>ra9_o4d_rli</code> 竇長君（外戚世家候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 竇長君 | [《史記・外戚世家》][31] | [JSON](ra9_o4d_rli.json) |
| `A` | 彭祖 | [《史記・外戚世家》][31] | [JSON](ra9_o4d_rli_A.json) |

</details>

<details><summary><code>rdo_wsn_30x</code> 東樓公（杞君）（8 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 東樓公（杞君） | [《史記・陳杞世家》][18] | [JSON](rdo_wsn_30x.json) |
| `A` | 西樓公（杞君） | [《史記・陳杞世家》][18] | [JSON](rdo_wsn_30x_A.json) |
| `AA` | 題公（杞君） | [《史記・陳杞世家》][18] | [JSON](rdo_wsn_30x_AA.json) |
| `AAA` | 謀娶公（杞君） | [《史記・陳杞世家》][18] | [JSON](rdo_wsn_30x_AAA.json) |
| `AAAA` | 武公（杞君） | [《史記・陳杞世家》][18] | [JSON](rdo_wsn_30x_AAAA.json) |
| `AAAAA` | 靖公（杞君） | [《史記・陳杞世家》][18] | [JSON](rdo_wsn_30x_AAAAA.json) |
| `AAAAAA` | 共公（杞君） | [《史記・陳杞世家》][18] | [JSON](rdo_wsn_30x_AAAAAA.json) |
| `AAAAAAA` | 德公（杞君） | [《史記・陳杞世家》][18] | [JSON](rdo_wsn_30x_AAAAAAA.json) |

</details>

<details><summary><code>rex_cs0_mfo</code> 鮑革（宋文公）（12 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 鮑革（宋文公） | [《史記・宋微子世家》][20] | [JSON](rex_cs0_mfo.json) |
| `A` | 瑕（宋共公） | [《史記・宋微子世家》][20] | [JSON](rex_cs0_mfo_A.json) |
| `AA` | 戌（本版宋平公） | [《史記・宋微子世家》][20] | [JSON](rex_cs0_mfo_AA.json) |
| `AAA` | 佐（宋元公） | [《史記・宋微子世家》][20] | [JSON](rex_cs0_mfo_AAA.json) |
| `AAAA` | 頭曼（宋景公） | [《史記・宋微子世家》][20] | [JSON](rex_cs0_mfo_AAAA.json) |
| `AAAB` | 褍秦（宋元公少子） | [《史記・宋微子世家》][20] | [JSON](rex_cs0_mfo_AAAB.json) |
| `AAABA` | 糾（宋公孫） | [《史記・宋微子世家》][20] | [JSON](rex_cs0_mfo_AAABA.json) |
| `AAABAA` | 特（後宋昭公） | [《史記・宋微子世家》][20] | [JSON](rex_cs0_mfo_AAABAA.json) |
| `AAABAAA` | 購由（宋悼公） | [《史記・宋微子世家》][20] | [JSON](rex_cs0_mfo_AAABAAA.json) |
| `AAABAAAA` | 田（宋休公） | [《史記・宋微子世家》][20] | [JSON](rex_cs0_mfo_AAABAAAA.json) |
| `AAABAAAAA` | 辟兵（宋辟公） | [《史記・宋微子世家》][20] | [JSON](rex_cs0_mfo_AAABAAAAA.json) |
| `AAABAAAAAA` | 剔成（宋君） | [《史記・宋微子世家》][20] | [JSON](rex_cs0_mfo_AAABAAAAAA.json) |

</details>

<details><summary><code>rjl_5bl_0dm</code> 楚平王（伍胥列傳候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 楚平王 | [《史記・伍子胥列傳》][48] | [JSON](rjl_5bl_0dm.json) |
| `A` | 軫 | [《史記・伍子胥列傳》][48] | [JSON](rjl_5bl_0dm_A.json) |

</details>

<details><summary><code>rl6_a40_3hj</code> 馮唐祖父未名（張釋之馮唐列傳候選）（4 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 馮唐祖父未名 | [《史記・張釋之馮唐列傳》][84] | [JSON](rl6_a40_3hj.json) |
| `A` | 馮唐父未名 | [《史記・張釋之馮唐列傳》][84] | [JSON](rl6_a40_3hj_A.json) |
| `AA` | 馮唐 | [《史記・張釋之馮唐列傳》][84] | [JSON](rl6_a40_3hj_AA.json) |
| `AAA` | 馮遂 | [《史記・張釋之馮唐列傳》][84] | [JSON](rl6_a40_3hj_AAA.json) |

</details>

<details><summary><code>rlv_clg_euu</code> 丕鄭（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 丕鄭 | [《史記・晉世家》][21] | [JSON](rlv_clg_euu.json) |
| `A` | 丕豹 | [《史記・秦本紀》][5] | [JSON](rlv_clg_euu_A.json) |

</details>

<details><summary><code>rr8_o9c_jc1</code> 負芻（曹成公）（4 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 負芻（曹成公） | [《史記・管蔡世家》][17] | [JSON](rr8_o9c_jc1.json) |
| `A` | 勝（曹武公） | [《史記・管蔡世家》][17] | [JSON](rr8_o9c_jc1_A.json) |
| `AA` | 平公（曹武公子） | [《史記・管蔡世家》][17] | [JSON](rr8_o9c_jc1_AA.json) |
| `AAA` | 午（曹悼公） | [《史記・管蔡世家》][17] | [JSON](rr8_o9c_jc1_AAA.json) |

</details>

<details><summary><code>t3i_l5f_u0p</code> 絳侯父稱候選（吳王濞列傳候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 絳侯父稱候選 | [《史記・吳王濞列傳》][88] | [JSON](t3i_l5f_u0p.json) |
| `A` | 周亞夫 | [《史記・絳侯周勃世家》][39] | [JSON](t3i_l5f_u0p_A.json) |

</details>

<details><summary><code>t7q_vt4_ktj</code> 山（齊獻公）（7 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 山（齊獻公） | [《史記・齊太公世家》][14] | [JSON](t7q_vt4_ktj.json) |
| `A` | 壽（齊武公） | [《史記・齊太公世家》][14] | [JSON](t7q_vt4_ktj_A.json) |
| `AA` | 無忌（齊厲公） | [《史記・齊太公世家》][14] | [JSON](t7q_vt4_ktj_AA.json) |
| `AAA` | 赤（齊文公） | [《史記・齊太公世家》][14] | [JSON](t7q_vt4_ktj_AAA.json) |
| `AAAA` | 脫（齊成公） | [《史記・齊太公世家》][14] | [JSON](t7q_vt4_ktj_AAAA.json) |
| `AAAAA` | 購（齊莊公） | [《史記・齊太公世家》][14] | [JSON](t7q_vt4_ktj_AAAAA.json) |
| `AAAAAA` | 祿甫（齊釐公） | [《史記・齊太公世家》][14] | [JSON](t7q_vt4_ktj_AAAAAA.json) |

</details>

<details><summary><code>t9b_1eg_mqs</code> 田榮（田儋列傳候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 田榮 | [《史記・田儋列傳》][76] | [JSON](t9b_1eg_mqs.json) |
| `A` | 田廣 | [《史記・田儋列傳》][76] | [JSON](t9b_1eg_mqs_A.json) |

</details>

<details><summary><code>tkc_9z3_91l</code> 朱建（酈生陸賈列傳候選）（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 朱建 | [《史記・酈生陸賈列傳》][79] | [JSON](tkc_9z3_91l.json) |
| `A` | 朱建子未名（太史公友） | [《史記・酈生陸賈列傳》][79] | [JSON](tkc_9z3_91l_A.json) |
| `B` | 朱建子未名（使匈奴） | [《史記・酈生陸賈列傳》][79] | [JSON](tkc_9z3_91l_B.json) |

</details>

<details><summary><code>tqe_7o9_t4k</code> 柴武（袁盎鼂錯列傳候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 柴武 | [《史記・袁盎鼂錯列傳》][83] | [JSON](tqe_7o9_t4k.json) |
| `A` | 柴武太子未名 | [《史記・孝文本紀》][10]、[《史記・袁盎鼂錯列傳》][83] | [JSON](tqe_7o9_t4k_A.json) |

</details>

<details><summary><code>twz_p17_9b4</code> 王翦（白起王翦列傳候選）（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 王翦 | [《史記・白起王翦列傳》][55] | [JSON](twz_p17_9b4.json) |
| `*A` | 王離 | [《史記・白起王翦列傳》][55] | [JSON](twz_p17_9b4_%2AA.json) |
| `A` | 王賁 | [《史記・白起王翦列傳》][55] | [JSON](twz_p17_9b4_A.json) |

</details>

<details><summary><code>txj_z8z_5me</code> 肅侯（趙世家候選）（4 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 肅侯 | [《史記・趙世家》][25] | [JSON](txj_z8z_5me.json) |
| `A` | 武靈王 | [《史記・趙世家》][25] | [JSON](txj_z8z_5me_A.json) |
| `AA` | 公子章 | [《史記・趙世家》][25] | [JSON](txj_z8z_5me_AA.json) |
| `AB` | 何 | [《史記・趙世家》][25] | [JSON](txj_z8z_5me_AB.json) |

</details>

<details><summary><code>u3q_fto_w1f</code> 太王（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 太王 | [《史記・周本紀》][4] | [JSON](u3q_fto_w1f.json) |
| `A` | 虞仲 | [《史記・周本紀》][4] | [JSON](u3q_fto_w1f_A.json) |

</details>

<details><summary><code>u87_cc1_7vm</code> 田儋（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 田儋 | [《史記・田儋列傳》][76] | [JSON](u87_cc1_7vm.json) |
| `A` | 田市 | [《史記・田儋列傳》][76] | [JSON](u87_cc1_7vm_A.json) |

</details>

<details><summary><code>uay_2h8_ps8</code> 師（陳悼太子）（4 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 師（陳悼太子） | [《史記・陳杞世家》][18] | [JSON](uay_2h8_ps8.json) |
| `A` | 吳（陳惠公） | [《史記・陳杞世家》][18] | [JSON](uay_2h8_ps8_A.json) |
| `AA` | 柳（陳懷公） | [《史記・陳杞世家》][18] | [JSON](uay_2h8_ps8_AA.json) |
| `AAA` | 越（陳湣公） | [《史記・陳杞世家》][18] | [JSON](uay_2h8_ps8_AAA.json) |

</details>

<details><summary><code>uei_vr9_n3j</code> 竇長君（絳侯周勃世家候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 竇長君 | [《史記・絳侯周勃世家》][39] | [JSON](uei_vr9_n3j.json) |
| `A` | 彭祖 | [《史記・絳侯周勃世家》][39] | [JSON](uei_vr9_n3j_A.json) |

</details>

<details><summary><code>uj9_x5q_yir</code> 宋義（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 宋義 | [《史記・項羽本紀》][7] | [JSON](uj9_x5q_yir.json) |
| `A` | 宋襄 | [《史記・項羽本紀》][7] | [JSON](uj9_x5q_yir_A.json) |

</details>

<details><summary><code>us5_6hk_3qm</code> 屠者（留侯世家候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 屠者 | [《史記・留侯世家》][37] | [JSON](us5_6hk_3qm.json) |
| `A` | 秦嶢下軍將 | [《史記・留侯世家》][37] | [JSON](us5_6hk_3qm_A.json) |

</details>

<details><summary><code>uud_qa6_4u1</code> 郁（杞平公）（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 郁（杞平公） | [《史記・陳杞世家》][18] | [JSON](uud_qa6_4u1.json) |
| `A` | 成（杞悼公） | [《史記・陳杞世家》][18] | [JSON](uud_qa6_4u1_A.json) |
| `AA` | 乞（杞隱公） | [《史記・陳杞世家》][18] | [JSON](uud_qa6_4u1_AA.json) |

</details>

<details><summary><code>vna_am7_jn5</code> 韋賢（張丞相列傳候選）（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 韋賢 | [《史記・張丞相列傳》][78] | [JSON](vna_am7_jn5.json) |
| `A` | 韋玄成 | [《史記・張丞相列傳》][78] | [JSON](vna_am7_jn5_A.json) |
| `B` | 韋賢長子未名 | [《史記・張丞相列傳》][78] | [JSON](vna_am7_jn5_B.json) |

</details>

<details><summary><code>vs4_n7e_1qh</code> 武（曹繆公）（8 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 武（曹繆公） | [《史記・管蔡世家》][17] | [JSON](vs4_n7e_1qh.json) |
| `A` | 終生（曹桓公） | [《史記・管蔡世家》][17] | [JSON](vs4_n7e_1qh_A.json) |
| `AA` | 夕姑（曹莊公） | [《史記・管蔡世家》][17] | [JSON](vs4_n7e_1qh_AA.json) |
| `AAA` | 夷（曹釐公） | [《史記・管蔡世家》][17] | [JSON](vs4_n7e_1qh_AAA.json) |
| `AAAA` | 班（曹昭公） | [《史記・管蔡世家》][17] | [JSON](vs4_n7e_1qh_AAAA.json) |
| `AAAAA` | 襄（曹共公） | [《史記・管蔡世家》][17] | [JSON](vs4_n7e_1qh_AAAAA.json) |
| `AAAAAA` | 壽（曹文公） | [《史記・管蔡世家》][17] | [JSON](vs4_n7e_1qh_AAAAAA.json) |
| `AAAAAAA` | 彊（曹宣公） | [《史記・管蔡世家》][17] | [JSON](vs4_n7e_1qh_AAAAAAA.json) |

</details>

<details><summary><code>vtu_yuj_kdz</code> 齊王建（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 齊王建 | [《史記・秦始皇本紀》][6]、[《史記・田儋列傳》][76] | [JSON](vtu_yuj_kdz.json) |
| `*A` | 田安 | [《史記・項羽本紀》][7]、[《史記・田儋列傳》][76] | [JSON](vtu_yuj_kdz_%2AA.json) |

</details>

<details><summary><code>vty_3n0_0ed</code> 病疽卒父（孫吳列傳候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 病疽卒父 | [《史記・孫子吳起列傳》][47] | [JSON](vty_3n0_0ed.json) |
| `A` | 病疽卒 | [《史記・孫子吳起列傳》][47] | [JSON](vty_3n0_0ed_A.json) |

</details>

<details><summary><code>vwy_7cv_69j</code> 桓子（趙世家候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 桓子 | [《史記・趙世家》][25] | [JSON](vwy_7cv_69j.json) |
| `A` | 桓子之子（趙世家未名者） | [《史記・趙世家》][25] | [JSON](vwy_7cv_69j_A.json) |

</details>

<details><summary><code>w44_37v_bcb</code> 和（宋穆公）（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 和（宋穆公） | [《史記・宋微子世家》][20] | [JSON](w44_37v_bcb.json) |
| `A` | 馮（宋莊公） | [《史記・宋微子世家》][20] | [JSON](w44_37v_bcb_A.json) |
| `AA` | 捷（宋湣公） | [《史記・宋微子世家》][20] | [JSON](w44_37v_bcb_AA.json) |

</details>

<details><summary><code>w8j_vnd_rs4</code> 傅寬（傅靳蒯成列傳候選）（4 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 傅寬 | [《史記・傅靳蒯成列傳》][80] | [JSON](w8j_vnd_rs4.json) |
| `A` | 傅精 | [《史記・傅靳蒯成列傳》][80] | [JSON](w8j_vnd_rs4_A.json) |
| `AA` | 傅則 | [《史記・傅靳蒯成列傳》][80] | [JSON](w8j_vnd_rs4_AA.json) |
| `AAA` | 傅偃 | [《史記・傅靳蒯成列傳》][80] | [JSON](w8j_vnd_rs4_AAA.json) |

</details>

<details><summary><code>wuz_yxe_b9k</code> 齊景公（4 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 齊景公 | [《史記・齊太公世家》][14] | [JSON](wuz_yxe_b9k.json) |
| `A` | 齊悼公 | [《史記・齊太公世家》][14] | [JSON](wuz_yxe_b9k_A.json) |
| `AA` | 齊簡公 | [《史記・齊太公世家》][14] | [JSON](wuz_yxe_b9k_AA.json) |
| `B` | 孺子（齊） | [《史記・齊太公世家》][14] | [JSON](wuz_yxe_b9k_B.json) |

</details>

<details><summary><code>x50_1p7_qkk</code> 魯莊公（10 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 魯莊公 | [《史記・魯周公世家》][15] | [JSON](x50_1p7_qkk.json) |
| `A` | 魯湣公 | [《史記・魯周公世家》][15] | [JSON](x50_1p7_qkk_A.json) |
| `B` | 魯釐公 | [《史記・魯周公世家》][15] | [JSON](x50_1p7_qkk_B.json) |
| `BA` | 興（魯文公） | [《史記・魯周公世家》][15] | [JSON](x50_1p7_qkk_BA.json) |
| `BAA` | 惡（文公子） | [《史記・魯周公世家》][15] | [JSON](x50_1p7_qkk_BAA.json) |
| `BAB` | 視（文公子） | [《史記・魯周公世家》][15] | [JSON](x50_1p7_qkk_BAB.json) |
| `BAC` | 俀（魯宣公） | [《史記・魯周公世家》][15] | [JSON](x50_1p7_qkk_BAC.json) |
| `BACA` | 黑肱（魯成公） | [《史記・魯周公世家》][15] | [JSON](x50_1p7_qkk_BACA.json) |
| `BACAA` | 午（魯襄公） | [《史記・魯周公世家》][15] | [JSON](x50_1p7_qkk_BACAA.json) |
| `C` | 斑（莊公子） | [《史記・魯周公世家》][15] | [JSON](x50_1p7_qkk_C.json) |

</details>

<details><summary><code>xcr_p13_j7x</code> 甘茂（樗里子甘茂列傳候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 甘茂 | [《史記・樗里子甘茂列傳》][53] | [JSON](xcr_p13_j7x.json) |
| `*A` | 甘羅 | [《史記・樗里子甘茂列傳》][53] | [JSON](xcr_p13_j7x_%2AA.json) |

</details>

<details><summary><code>xd8_uww_5ok</code> 蕭何（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 蕭何 | [《史記・蕭相國世家》][35] | [JSON](xd8_uww_5ok.json) |
| `*A` | 系（蕭何孫） | [《史記・孝景本紀》][11] | [JSON](xd8_uww_5ok_%2AA.json) |

</details>

<details><summary><code>xgd_r31_cmr</code> 崔杼（4 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 崔杼 | [《史記・齊太公世家》][14] | [JSON](xgd_r31_cmr.json) |
| `A` | 成（崔杼子） | [《史記・齊太公世家》][14] | [JSON](xgd_r31_cmr_A.json) |
| `B` | 彊（崔杼子） | [《史記・齊太公世家》][14] | [JSON](xgd_r31_cmr_B.json) |
| `C` | 明（崔杼子） | [《史記・齊太公世家》][14] | [JSON](xgd_r31_cmr_C.json) |

</details>

<details><summary><code>xnj_cjk_pcj</code> 韓襄王（韓信盧綰列傳候選）（6 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 韓襄王 | [《史記・韓信盧綰列傳》][75] | [JSON](xnj_cjk_pcj.json) |
| `*A` | 韓王信 | [《史記・韓信盧綰列傳》][75] | [JSON](xnj_cjk_pcj_%2AA.json) |
| `*AA` | 韓王信太子未名 | [《史記・韓信盧綰列傳》][75] | [JSON](xnj_cjk_pcj_%2AAA.json) |
| `*AAA` | 韓嬰 | [《史記・韓信盧綰列傳》][75] | [JSON](xnj_cjk_pcj_%2AAAA.json) |
| `*AB` | 韓穨當 | [《史記・韓信盧綰列傳》][75] | [JSON](xnj_cjk_pcj_%2AAB.json) |
| `*AB*A` | 韓嫣 | [《史記・韓信盧綰列傳》][75] | [JSON](xnj_cjk_pcj_%2AAB%2AA.json) |

</details>

<details><summary><code>xny_prn_zyi</code> 酈商（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 酈商 | [《史記・樊酈滕灌列傳》][77] | [JSON](xny_prn_zyi.json) |
| `A` | 酈寄 | [《史記・樊酈滕灌列傳》][77] | [JSON](xny_prn_zyi_A.json) |

</details>

<details><summary><code>xrt_zof_cbt</code> 和（衛武公）（4 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 和（衛武公） | [《史記・衛康叔世家》][19] | [JSON](xrt_zof_cbt.json) |
| `A` | 揚（衛莊公） | [《史記・衛康叔世家》][19] | [JSON](xrt_zof_cbt_A.json) |
| `AA` | 州吁（衛君） | [《史記・衛康叔世家》][19] | [JSON](xrt_zof_cbt_AA.json) |
| `AB` | 完（衛桓公） | [《史記・衛康叔世家》][19] | [JSON](xrt_zof_cbt_AB.json) |

</details>

<details><summary><code>xyg_gxo_6tt</code> 夷眛（刺客列傳候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 夷眛 | [《史記・刺客列傳》][68] | [JSON](xyg_gxo_6tt.json) |
| `A` | 吳王僚 | [《史記・刺客列傳》][68] | [JSON](xyg_gxo_6tt_A.json) |

</details>

<details><summary><code>y0c_hok_598</code> 李同父未名（平原君虞卿列傳候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 李同父未名 | [《史記・平原君虞卿列傳》][58] | [JSON](y0c_hok_598.json) |
| `A` | 李同 | [《史記・平原君虞卿列傳》][58] | [JSON](y0c_hok_598_A.json) |

</details>

<details><summary><code>y3u_i0l_ztj</code> 韓宣王（趙世家候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 韓宣王 | [《史記・趙世家》][25] | [JSON](y3u_i0l_ztj.json) |
| `A` | 倉 | [《史記・趙世家》][25] | [JSON](y3u_i0l_ztj_A.json) |

</details>

<details><summary><code>y4i_pjk_4gn</code> 季歷（47 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 季歷 | [《史記・周本紀》][4] | [JSON](y4i_pjk_4gn.json) |
| `A` | 西伯昌 | [《史記・周本紀》][4] | [JSON](y4i_pjk_4gn_A.json) |
| `AA` | 周武王 | [《史記・周本紀》][4] | [JSON](y4i_pjk_4gn_AA.json) |
| `AAA` | 晉唐叔 | [《史記・晉世家》][21] | [JSON](y4i_pjk_4gn_AAA.json) |
| `AAAA` | 燮（晉侯） | [《史記・晉世家》][21] | [JSON](y4i_pjk_4gn_AAAA.json) |
| `AAAAA` | 寧族（晉武侯） | [《史記・晉世家》][21] | [JSON](y4i_pjk_4gn_AAAAA.json) |
| `AAAAAA` | 服人（晉成侯） | [《史記・晉世家》][21] | [JSON](y4i_pjk_4gn_AAAAAA.json) |
| `AAAAAAA` | 福（晉厲侯） | [《史記・晉世家》][21] | [JSON](y4i_pjk_4gn_AAAAAAA.json) |
| `AAAAAAAA` | 宜臼（晉靖侯） | [《史記・晉世家》][21] | [JSON](y4i_pjk_4gn_AAAAAAAA.json) |
| `AAAAAAAA*A` | 欒賓（靖侯庶孫） | [《史記・晉世家》][21] | [JSON](y4i_pjk_4gn_AAAAAAAA%2AA.json) |
| `AB` | 管叔 | [《史記・管蔡世家》][17] | [JSON](y4i_pjk_4gn_AB.json) |
| `AC` | 蔡叔 | [《史記・管蔡世家》][17] | [JSON](y4i_pjk_4gn_AC.json) |
| `ACA` | 胡（蔡仲） | [《史記・管蔡世家》][17] | [JSON](y4i_pjk_4gn_ACA.json) |
| `ACAA` | 荒（蔡伯） | [《史記・管蔡世家》][17] | [JSON](y4i_pjk_4gn_ACAA.json) |
| `ACAAA` | 宮侯（蔡君） | [《史記・管蔡世家》][17] | [JSON](y4i_pjk_4gn_ACAAA.json) |
| `ACAAAA` | 厲侯（蔡君） | [《史記・管蔡世家》][17] | [JSON](y4i_pjk_4gn_ACAAAA.json) |
| `ACAAAAA` | 武侯（蔡君） | [《史記・管蔡世家》][17] | [JSON](y4i_pjk_4gn_ACAAAAA.json) |
| `ACAAAAAA` | 夷侯（蔡君） | [《史記・管蔡世家》][17] | [JSON](y4i_pjk_4gn_ACAAAAAA.json) |
| `ACAAAAAAA` | 所事（蔡釐侯） | [《史記・管蔡世家》][17] | [JSON](y4i_pjk_4gn_ACAAAAAAA.json) |
| `ACAAAAAAAA` | 興（蔡共侯） | [《史記・管蔡世家》][17] | [JSON](y4i_pjk_4gn_ACAAAAAAAA.json) |
| `ACAAAAAAAAA` | 戴侯（蔡君） | [《史記・管蔡世家》][17] | [JSON](y4i_pjk_4gn_ACAAAAAAAAA.json) |
| `ACAAAAAAAAAA` | 措父（蔡宣侯） | [《史記・管蔡世家》][17] | [JSON](y4i_pjk_4gn_ACAAAAAAAAAA.json) |
| `ACAAAAAAAAAAA` | 封人（蔡桓侯） | [《史記・管蔡世家》][17] | [JSON](y4i_pjk_4gn_ACAAAAAAAAAAA.json) |
| `AD` | 周公 | [《史記・魯周公世家》][15] | [JSON](y4i_pjk_4gn_AD.json) |
| `ADA` | 伯禽 | [《史記・魯周公世家》][15] | [JSON](y4i_pjk_4gn_ADA.json) |
| `ADAA` | 酋（魯考公） | [《史記・魯周公世家》][15] | [JSON](y4i_pjk_4gn_ADAA.json) |
| `AE` | 衛康叔封 | [《史記・衛康叔世家》][19] | [JSON](y4i_pjk_4gn_AE.json) |
| `AEA` | 康伯（衛康叔子） | [《史記・衛康叔世家》][19] | [JSON](y4i_pjk_4gn_AEA.json) |
| `AEAA` | 考伯（衛君） | [《史記・衛康叔世家》][19] | [JSON](y4i_pjk_4gn_AEAA.json) |
| `AEAAA` | 嗣伯（衛君） | [《史記・衛康叔世家》][19] | [JSON](y4i_pjk_4gn_AEAAA.json) |
| `AEAAAA` | 偼伯（衛君） | [《史記・衛康叔世家》][19] | [JSON](y4i_pjk_4gn_AEAAAA.json) |
| `AEAAAAA` | 靖伯（衛君） | [《史記・衛康叔世家》][19] | [JSON](y4i_pjk_4gn_AEAAAAA.json) |
| `AEAAAAAA` | 貞伯（衛君） | [《史記・衛康叔世家》][19] | [JSON](y4i_pjk_4gn_AEAAAAAA.json) |
| `AEAAAAAAA` | 頃侯（衛君） | [《史記・衛康叔世家》][19] | [JSON](y4i_pjk_4gn_AEAAAAAAA.json) |
| `AEAAAAAAAA` | 釐侯（衛君） | [《史記・衛康叔世家》][19] | [JSON](y4i_pjk_4gn_AEAAAAAAAA.json) |
| `AF` | 伯邑考（文王長子） | [《史記・管蔡世家》][17] | [JSON](y4i_pjk_4gn_AF.json) |
| `AG` | 曹叔振鐸 | [《史記・管蔡世家》][17] | [JSON](y4i_pjk_4gn_AG.json) |
| `AGA` | 脾（曹太伯） | [《史記・管蔡世家》][17] | [JSON](y4i_pjk_4gn_AGA.json) |
| `AGAA` | 平（曹仲君） | [《史記・管蔡世家》][17] | [JSON](y4i_pjk_4gn_AGAA.json) |
| `AGAAA` | 侯（曹宮伯） | [《史記・管蔡世家》][17] | [JSON](y4i_pjk_4gn_AGAAA.json) |
| `AGAAAA` | 云（曹孝伯） | [《史記・管蔡世家》][17] | [JSON](y4i_pjk_4gn_AGAAAA.json) |
| `AGAAAAA` | 喜（曹夷伯） | [《史記・管蔡世家》][17] | [JSON](y4i_pjk_4gn_AGAAAAA.json) |
| `AH` | 成叔武（文王子） | [《史記・管蔡世家》][17] | [JSON](y4i_pjk_4gn_AH.json) |
| `AI` | 霍叔處（文王子） | [《史記・管蔡世家》][17] | [JSON](y4i_pjk_4gn_AI.json) |
| `AJ` | 冉季載（文王少子） | [《史記・管蔡世家》][17] | [JSON](y4i_pjk_4gn_AJ.json) |
| `B` | 虢叔 | [《史記・秦本紀》][5]、[《史記・晉世家》][21] | [JSON](y4i_pjk_4gn_B.json) |
| `C` | 虢仲（王季子） | [《史記・晉世家》][21] | [JSON](y4i_pjk_4gn_C.json) |

</details>

<details><summary><code>y5g_spw_43b</code> 太史嬓（田單列傳候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 太史嬓 | [《史記・田敬仲完世家》][28] | [JSON](y5g_spw_43b.json) |
| `A` | 嬓女君王后 | [《史記・田敬仲完世家》][28] | [JSON](y5g_spw_43b_A.json) |

</details>

<details><summary><code>y97_huh_vuz</code> 秦襄公（34 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 秦襄公 | [《史記・秦本紀》][5] | [JSON](y97_huh_vuz.json) |
| `A` | 秦文公 | [《史記・秦本紀》][5] | [JSON](y97_huh_vuz_A.json) |
| `AA` | 靜公（卷末世系） | [《史記・秦始皇本紀》][6] | [JSON](y97_huh_vuz_AA.json) |
| `AAA` | 憲公（卷末世系） | [《史記・秦始皇本紀》][6] | [JSON](y97_huh_vuz_AAA.json) |
| `AAAA` | 秦德公 | [《史記・秦本紀》][5] | [JSON](y97_huh_vuz_AAAA.json) |
| `AAAAA` | 秦穆公 | [《史記・秦本紀》][5] | [JSON](y97_huh_vuz_AAAAA.json) |
| `AAAAAA` | 秦康公 | [《史記・秦本紀》][5] | [JSON](y97_huh_vuz_AAAAAA.json) |
| `AAAAAAA` | 秦共公 | [《史記・秦本紀》][5] | [JSON](y97_huh_vuz_AAAAAAA.json) |
| `AAAAAAAA` | 秦桓公 | [《史記・秦本紀》][5] | [JSON](y97_huh_vuz_AAAAAAAA.json) |
| `AAAAAAAAA` | 秦景公 | [《史記・秦本紀》][5] | [JSON](y97_huh_vuz_AAAAAAAAA.json) |
| `AAAAAAAAAA` | 秦哀公 | [《史記・秦本紀》][5] | [JSON](y97_huh_vuz_AAAAAAAAAA.json) |
| `AAAAAAAAAAA` | 秦夷公 | [《史記・秦本紀》][5] | [JSON](y97_huh_vuz_AAAAAAAAAAA.json) |
| `AAAAAAAAAAAA` | 秦惠公（夷公子） | [《史記・秦本紀》][5] | [JSON](y97_huh_vuz_AAAAAAAAAAAA.json) |
| `AAAAAAAAAAAAA` | 秦悼公 | [《史記・秦本紀》][5]、[《史記・秦始皇本紀》][6] | [JSON](y97_huh_vuz_AAAAAAAAAAAAA.json) |
| `AAAAAAAAAAAAAA` | 秦厲共公 | [《史記・秦本紀》][5] | [JSON](y97_huh_vuz_AAAAAAAAAAAAAA.json) |
| `AAAAAAAAAAAAAAA` | 秦躁公 | [《史記・秦本紀》][5] | [JSON](y97_huh_vuz_AAAAAAAAAAAAAAA.json) |
| `AAAAAAAAAAAAAB` | 剌龔公（本文字形） | [《史記・秦始皇本紀》][6] | [JSON](y97_huh_vuz_AAAAAAAAAAAAAB.json) |
| `AAAAAAAAAAAAABA` | 秦懷公 | [《史記・秦本紀》][5] | [JSON](y97_huh_vuz_AAAAAAAAAAAAABA.json) |
| `AAAAAAAAAAAAABAA` | 昭子（秦懷公太子） | [《史記・秦本紀》][5] | [JSON](y97_huh_vuz_AAAAAAAAAAAAABAA.json) |
| `AAAAAAAAAAAAABAAA` | 秦靈公 | [《史記・秦本紀》][5] | [JSON](y97_huh_vuz_AAAAAAAAAAAAABAAA.json) |
| `AAAAAAAAAAAAABAAAA` | 秦獻公 | [《史記・秦本紀》][5] | [JSON](y97_huh_vuz_AAAAAAAAAAAAABAAAA.json) |
| `AAAAAAAAAAAAABAAAAA` | 秦孝公 | [《史記・商君列傳》][50] | [JSON](y97_huh_vuz_AAAAAAAAAAAAABAAAAA.json) |
| `AAAAAAAAAAAAABAAAAAA` | 秦惠王 | [《史記・楚世家》][22] | [JSON](y97_huh_vuz_AAAAAAAAAAAAABAAAAAA.json) |
| `AAAAAAAAAAAAABAAAAAAA` | 秦武王 | [《史記・樗里子甘茂列傳》][53] | [JSON](y97_huh_vuz_AAAAAAAAAAAAABAAAAAAA.json) |
| `AAAAAAAAAAAAABAAAAAAB` | 秦惠王女（燕太子婦） | [《史記・燕召公世家》][16] | [JSON](y97_huh_vuz_AAAAAAAAAAAAABAAAAAAB.json) |
| `AAAAAAAAAAAAABAB` | 秦簡公 | [《史記・秦本紀》][5] | [JSON](y97_huh_vuz_AAAAAAAAAAAAABAB.json) |
| `AAAAAAAAAAAAABABA` | 秦惠公（簡公子） | [《史記・秦本紀》][5] | [JSON](y97_huh_vuz_AAAAAAAAAAAAABABA.json) |
| `AAAAAAAAAAAAABABAA` | 出子（秦惠公子） | [《史記・秦本紀》][5] | [JSON](y97_huh_vuz_AAAAAAAAAAAAABABAA.json) |
| `AAAAAAAAAB` | 畢公（秦卷末世系） | [《史記・秦始皇本紀》][6] | [JSON](y97_huh_vuz_AAAAAAAAAB.json) |
| `AAAAB` | 秦宣公 | [《史記・秦本紀》][5] | [JSON](y97_huh_vuz_AAAAB.json) |
| `AAAAC` | 秦成公 | [《史記・秦本紀》][5] | [JSON](y97_huh_vuz_AAAAC.json) |
| `AAAB` | 秦武公 | [《史記・秦本紀》][5] | [JSON](y97_huh_vuz_AAAB.json) |
| `AAABA` | 白（秦武公子） | [《史記・秦本紀》][5] | [JSON](y97_huh_vuz_AAABA.json) |
| `AAAC` | 出子 | [《史記・秦本紀》][5] | [JSON](y97_huh_vuz_AAAC.json) |

</details>

<details><summary><code>yaj_2vc_98w</code> 吳廣（趙世家娃嬴父候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 吳廣 | [《史記・趙世家》][25] | [JSON](yaj_2vc_98w.json) |
| `A` | 娃嬴 | [《史記・趙世家》][25] | [JSON](yaj_2vc_98w_A.json) |

</details>

<details><summary><code>yb7_umd_09d</code> 公子光（伍胥列傳候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 公子光 | [《史記・吳太伯世家》][13] | [JSON](yb7_umd_09d.json) |
| `A` | 夫差 | [《史記・伍子胥列傳》][48] | [JSON](yb7_umd_09d_A.json) |

</details>

<details><summary><code>ycd_ixa_ovp</code> 周勃（絳侯周勃世家候選）（6 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 周勃 | [《史記・絳侯周勃世家》][39] | [JSON](ycd_ixa_ovp.json) |
| `A` | 勝之 | [《史記・絳侯周勃世家》][39] | [JSON](ycd_ixa_ovp_A.json) |
| `B` | 周亞夫 | [《史記・絳侯周勃世家》][39] | [JSON](ycd_ixa_ovp_B.json) |
| `BA` | 亞夫子 | [《史記・絳侯周勃世家》][39] | [JSON](ycd_ixa_ovp_BA.json) |
| `C` | 堅 | [《史記・絳侯周勃世家》][39] | [JSON](ycd_ixa_ovp_C.json) |
| `CA` | 建德 | [《史記・絳侯周勃世家》][39] | [JSON](ycd_ixa_ovp_CA.json) |

</details>

<details><summary><code>yg7_rda_vb8</code> 淳于意（扁鵲倉公列傳候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 淳于意 | [《史記・扁鵲倉公列傳》][87] | [JSON](yg7_rda_vb8.json) |
| `A` | 緹縈 | [《史記・扁鵲倉公列傳》][87] | [JSON](yg7_rda_vb8_A.json) |

</details>

<details><summary><code>yhm_h9f_8p0</code> 范蠡（越世家候選）（4 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 范蠡 | [《史記・越王勾踐世家》][23] | [JSON](yhm_h9f_8p0.json) |
| `A` | 朱公長男（越世家未名者） | [《史記・越王勾踐世家》][23] | [JSON](yhm_h9f_8p0_A.json) |
| `B` | 朱公中男（越世家未名者） | [《史記・越王勾踐世家》][23] | [JSON](yhm_h9f_8p0_B.json) |
| `C` | 朱公少子（越世家未名者） | [《史記・越王勾踐世家》][23] | [JSON](yhm_h9f_8p0_C.json) |

</details>

<details><summary><code>yht_8tu_hv4</code> 齊景公（田世家候選）（4 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 齊景公 | [《史記・田敬仲完世家》][28] | [JSON](yht_8tu_hv4.json) |
| `A` | 荼 | [《史記・田敬仲完世家》][28] | [JSON](yht_8tu_hv4_A.json) |
| `B` | 陽生 | [《史記・田敬仲完世家》][28] | [JSON](yht_8tu_hv4_B.json) |
| `BA` | 壬 | [《史記・田敬仲完世家》][28] | [JSON](yht_8tu_hv4_BA.json) |

</details>

<details><summary><code>ylb_ttg_8dr</code> 百里傒（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 百里傒 | [《史記・秦本紀》][5] | [JSON](ylb_ttg_8dr.json) |
| `A` | 孟明視 | [《史記・秦本紀》][5] | [JSON](ylb_ttg_8dr_A.json) |

</details>

<details><summary><code>ymr_gcs_kii</code> 熊嚴（楚君）（10 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 熊嚴（楚君） | [《史記・楚世家》][22] | [JSON](ymr_gcs_kii.json) |
| `A` | 伯霜（熊霜） | [《史記・楚世家》][22] | [JSON](ymr_gcs_kii_A.json) |
| `B` | 仲雪（熊嚴子） | [《史記・楚世家》][22] | [JSON](ymr_gcs_kii_B.json) |
| `C` | 叔堪（熊嚴子） | [《史記・楚世家》][22] | [JSON](ymr_gcs_kii_C.json) |
| `D` | 季徇（熊徇） | [《史記・楚世家》][22] | [JSON](ymr_gcs_kii_D.json) |
| `DA` | 熊咢（楚君） | [《史記・楚世家》][22] | [JSON](ymr_gcs_kii_DA.json) |
| `DAA` | 熊儀（若敖） | [《史記・楚世家》][22] | [JSON](ymr_gcs_kii_DAA.json) |
| `DAAA` | 熊坎（霄敖） | [《史記・楚世家》][22] | [JSON](ymr_gcs_kii_DAAA.json) |
| `DAAAA` | 熊眴（蚡冒） | [《史記・楚世家》][22] | [JSON](ymr_gcs_kii_DAAAA.json) |
| `DAAAAA` | 蚡冒子（熊通所弒未名者） | [《史記・楚世家》][22] | [JSON](ymr_gcs_kii_DAAAAA.json) |

</details>

<details><summary><code>yph_dkb_w4w</code> 申屠嘉（張丞相列傳候選）（4 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 申屠嘉 | [《史記・張丞相列傳》][78] | [JSON](yph_dkb_w4w.json) |
| `A` | 申屠蔑 | [《史記・張丞相列傳》][78] | [JSON](yph_dkb_w4w_A.json) |
| `AA` | 申屠去病 | [《史記・張丞相列傳》][78] | [JSON](yph_dkb_w4w_AA.json) |
| `AAA` | 申屠臾 | [《史記・張丞相列傳》][78] | [JSON](yph_dkb_w4w_AAA.json) |

</details>

<details><summary><code>yqp_nlb_p1p</code> 太公（漢王父稱）（110 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 太公（漢王父稱） | [《史記・高祖本紀》][8] | [JSON](yqp_nlb_p1p.json) |
| `A` | 沛公（本卷稱呼） | [《史記・高祖本紀》][8] | [JSON](yqp_nlb_p1p_A.json) |
| `AA` | 孝惠（本卷稱呼） | [《史記・呂太后本紀》][9] | [JSON](yqp_nlb_p1p_AA.json) |
| `AB` | 劉肥 | [《史記・齊悼惠王世家》][34] | [JSON](yqp_nlb_p1p_AB.json) |
| `ABA` | 齊哀王（本卷未名） | [《史記・齊悼惠王世家》][34] | [JSON](yqp_nlb_p1p_ABA.json) |
| `ABB` | 卬（膠西王） | [《史記・吳王濞列傳》][88] | [JSON](yqp_nlb_p1p_ABB.json) |
| `ABBA` | 膠西王太子德 | [《史記・吳王濞列傳》][88] | [JSON](yqp_nlb_p1p_ABBA.json) |
| `ABC` | 興居（齊悼惠王子） | [《史記・齊悼惠王世家》][34] | [JSON](yqp_nlb_p1p_ABC.json) |
| `ABD` | 辟光（濟南王） | [《史記・齊悼惠王世家》][34] | [JSON](yqp_nlb_p1p_ABD.json) |
| `ABE` | 雄渠（膠東王） | [《史記・齊悼惠王世家》][34] | [JSON](yqp_nlb_p1p_ABE.json) |
| `ABF` | 劉章 | [《史記・齊悼惠王世家》][34] | [JSON](yqp_nlb_p1p_ABF.json) |
| `ABFA` | 喜 | [《史記・齊悼惠王世家》][34] | [JSON](yqp_nlb_p1p_ABFA.json) |
| `ABFAA` | 延校勘建未定 | [《史記・齊悼惠王世家》][34] | [JSON](yqp_nlb_p1p_ABFAA.json) |
| `ABFAAA` | 義 | [《史記・齊悼惠王世家》][34] | [JSON](yqp_nlb_p1p_ABFAAA.json) |
| `ABFAAAA` | 武城陽惠王 | [《史記・齊悼惠王世家》][34] | [JSON](yqp_nlb_p1p_ABFAAAA.json) |
| `ABFAAAAA` | 順 | [《史記・齊悼惠王世家》][34] | [JSON](yqp_nlb_p1p_ABFAAAAA.json) |
| `ABFAAAAAA` | 恢城陽戴王 | [《史記・齊悼惠王世家》][34] | [JSON](yqp_nlb_p1p_ABFAAAAAA.json) |
| `ABFAAAAAAA` | 景城陽末王 | [《史記・齊悼惠王世家》][34] | [JSON](yqp_nlb_p1p_ABFAAAAAAA.json) |
| `ABG` | 賢（菑川王） | [《史記・齊悼惠王世家》][34] | [JSON](yqp_nlb_p1p_ABG.json) |
| `ABH` | 志（濟北王） | [《史記・齊悼惠王世家》][34] | [JSON](yqp_nlb_p1p_ABH.json) |
| `ABHA` | 建菑川靖王 | [《史記・齊悼惠王世家》][34] | [JSON](yqp_nlb_p1p_ABHA.json) |
| `ABHAA` | 遺 | [《史記・齊悼惠王世家》][34] | [JSON](yqp_nlb_p1p_ABHAA.json) |
| `ABHAAA` | 終古 | [《史記・齊悼惠王世家》][34] | [JSON](yqp_nlb_p1p_ABHAAA.json) |
| `ABHAAAA` | 尚菑川孝王 | [《史記・齊悼惠王世家》][34] | [JSON](yqp_nlb_p1p_ABHAAAA.json) |
| `ABHAAAAA` | 橫 | [《史記・齊悼惠王世家》][34] | [JSON](yqp_nlb_p1p_ABHAAAAA.json) |
| `AC` | 恒（高祖子） | [《史記・孝文本紀》][10] | [JSON](yqp_nlb_p1p_AC.json) |
| `ACA` | 文帝太子（本卷未名） | [《史記・梁孝王世家》][40] | [JSON](yqp_nlb_p1p_ACA.json) |
| `ACAA` | 徹（景帝子） | [《史記・孝武本紀》][12] | [JSON](yqp_nlb_p1p_ACAA.json) |
| `ACAAA` | 閎 | [《史記・三王世家》][42] | [JSON](yqp_nlb_p1p_ACAAA.json) |
| `ACAAB` | 旦 | [《史記・三王世家》][42] | [JSON](yqp_nlb_p1p_ACAAB.json) |
| `ACAABA` | 安定侯子 | [《史記・三王世家》][42] | [JSON](yqp_nlb_p1p_ACAABA.json) |
| `ACAABB` | 建 | [《史記・三王世家》][42] | [JSON](yqp_nlb_p1p_ACAABB.json) |
| `ACAAC` | 胥 | [《史記・三王世家》][42] | [JSON](yqp_nlb_p1p_ACAAC.json) |
| `ACAACA` | 朝陽侯子 | [《史記・三王世家》][42] | [JSON](yqp_nlb_p1p_ACAACA.json) |
| `ACAACB` | 平曲侯子 | [《史記・三王世家》][42] | [JSON](yqp_nlb_p1p_ACAACB.json) |
| `ACAACC` | 南利侯子 | [《史記・三王世家》][42] | [JSON](yqp_nlb_p1p_ACAACC.json) |
| `ACAACD` | 弘 | [《史記・三王世家》][42] | [JSON](yqp_nlb_p1p_ACAACD.json) |
| `ACAAD` | 據 | [《史記・外戚世家》][31] | [JSON](yqp_nlb_p1p_ACAAD.json) |
| `ACAAE` | 昭帝 | [《史記・三王世家》][42] | [JSON](yqp_nlb_p1p_ACAAE.json) |
| `ACAB` | 德 | [《史記・五宗世家》][41] | [JSON](yqp_nlb_p1p_ACAB.json) |
| `ACABA` | 不害 | [《史記・五宗世家》][41] | [JSON](yqp_nlb_p1p_ACABA.json) |
| `ACABAA` | 基 | [《史記・五宗世家》][41] | [JSON](yqp_nlb_p1p_ACABAA.json) |
| `ACABAAA` | 授 | [《史記・五宗世家》][41] | [JSON](yqp_nlb_p1p_ACABAAA.json) |
| `ACAC` | 閼于 | [《史記・五宗世家》][41] | [JSON](yqp_nlb_p1p_ACAC.json) |
| `ACAD` | 發 | [《史記・五宗世家》][41] | [JSON](yqp_nlb_p1p_ACAD.json) |
| `ACADA` | 庸 | [《史記・五宗世家》][41] | [JSON](yqp_nlb_p1p_ACADA.json) |
| `ACADAA` | 鮒鮈 | [《史記・五宗世家》][41] | [JSON](yqp_nlb_p1p_ACADAA.json) |
| `ACAE` | 乘 | [《史記・五宗世家》][41] | [JSON](yqp_nlb_p1p_ACAE.json) |
| `ACAF` | 廣川王（徙趙王未名） | [《史記・五宗世家》][41] | [JSON](yqp_nlb_p1p_ACAF.json) |
| `ACAG` | 舜（景帝子） | [《史記・五宗世家》][41] | [JSON](yqp_nlb_p1p_ACAG.json) |
| `ACAGA` | 棁 | [《史記・五宗世家》][41] | [JSON](yqp_nlb_p1p_ACAGA.json) |
| `ACAGB` | 平 | [《史記・五宗世家》][41] | [JSON](yqp_nlb_p1p_ACAGB.json) |
| `ACAGC` | 商 | [《史記・五宗世家》][41] | [JSON](yqp_nlb_p1p_ACAGC.json) |
| `ACAGCA` | 安世 | [《史記・五宗世家》][41] | [JSON](yqp_nlb_p1p_ACAGCA.json) |
| `ACAH` | 栗太子（本卷未名） | [《史記・五宗世家》][41] | [JSON](yqp_nlb_p1p_ACAH.json) |
| `ACAI` | 勝（景帝子） | [《史記・五宗世家》][41] | [JSON](yqp_nlb_p1p_ACAI.json) |
| `ACAIA` | 昌 | [《史記・五宗世家》][41] | [JSON](yqp_nlb_p1p_ACAIA.json) |
| `ACAIAA` | 昆侈 | [《史記・五宗世家》][41] | [JSON](yqp_nlb_p1p_ACAIAA.json) |
| `ACAJ` | 越（景帝子） | [《史記・五宗世家》][41] | [JSON](yqp_nlb_p1p_ACAJ.json) |
| `ACAJA` | 齊 | [《史記・五宗世家》][41] | [JSON](yqp_nlb_p1p_ACAJA.json) |
| `ACAK` | 非（汝南王） | [《史記・五宗世家》][41] | [JSON](yqp_nlb_p1p_ACAK.json) |
| `ACAKA` | 建 | [《史記・五宗世家》][41] | [JSON](yqp_nlb_p1p_ACAKA.json) |
| `ACAL` | 餘（淮陽王） | [《史記・五宗世家》][41] | [JSON](yqp_nlb_p1p_ACAL.json) |
| `ACALA` | 光 | [《史記・五宗世家》][41] | [JSON](yqp_nlb_p1p_ACALA.json) |
| `ACAM` | 寄（景帝子） | [《史記・五宗世家》][41] | [JSON](yqp_nlb_p1p_ACAM.json) |
| `ACAMA` | 賢 | [《史記・五宗世家》][41] | [JSON](yqp_nlb_p1p_ACAMA.json) |
| `ACAMAA` | 膠東慶 | [《史記・五宗世家》][41] | [JSON](yqp_nlb_p1p_ACAMAA.json) |
| `ACAMB` | 六安慶 | [《史記・五宗世家》][41] | [JSON](yqp_nlb_p1p_ACAMB.json) |
| `ACAN` | 端（景帝子） | [《史記・五宗世家》][41] | [JSON](yqp_nlb_p1p_ACAN.json) |
| `ACB` | 梁懷王 | [《史記・屈原賈生列傳》][66] | [JSON](yqp_nlb_p1p_ACB.json) |
| `ACC` | 參 | [《史記・梁孝王世家》][40] | [JSON](yqp_nlb_p1p_ACC.json) |
| `ACCA` | 登 | [《史記・梁孝王世家》][40] | [JSON](yqp_nlb_p1p_ACCA.json) |
| `ACCAA` | 義 | [《史記・梁孝王世家》][40] | [JSON](yqp_nlb_p1p_ACCAA.json) |
| `ACD` | 勝 | [《史記・梁孝王世家》][40] | [JSON](yqp_nlb_p1p_ACD.json) |
| `ACE` | 孝文帝女公主 | [《史記・絳侯周勃世家》][39] | [JSON](yqp_nlb_p1p_ACE.json) |
| `ACF` | 嫖 | [《史記・外戚世家》][31] | [JSON](yqp_nlb_p1p_ACF.json) |
| `ACG` | 武（文帝子） | [《史記・梁孝王世家》][40] | [JSON](yqp_nlb_p1p_ACG.json) |
| `ACGA` | 買 | [《史記・梁孝王世家》][40] | [JSON](yqp_nlb_p1p_ACGA.json) |
| `ACGAA` | 襄 | [《史記・梁孝王世家》][40] | [JSON](yqp_nlb_p1p_ACGAA.json) |
| `ACGAAA` | 無傷 | [《史記・梁孝王世家》][40] | [JSON](yqp_nlb_p1p_ACGAAA.json) |
| `ACGB` | 明 | [《史記・梁孝王世家》][40] | [JSON](yqp_nlb_p1p_ACGB.json) |
| `ACGC` | 彭離 | [《史記・梁孝王世家》][40] | [JSON](yqp_nlb_p1p_ACGC.json) |
| `ACGD` | 定 | [《史記・梁孝王世家》][40] | [JSON](yqp_nlb_p1p_ACGD.json) |
| `ACGE` | 不識 | [《史記・梁孝王世家》][40] | [JSON](yqp_nlb_p1p_ACGE.json) |
| `AD` | 恢（高祖子） | [《史記・呂太后本紀》][9] | [JSON](yqp_nlb_p1p_AD.json) |
| `AE` | 友（高祖子） | [《史記・呂太后本紀》][9] | [JSON](yqp_nlb_p1p_AE.json) |
| `AEA` | 遂（趙幽王子） | [《史記・楚元王世家》][32] | [JSON](yqp_nlb_p1p_AEA.json) |
| `AEB` | 辟彊（趙幽王子） | [《史記・孝文本紀》][10]、[《史記・楚元王世家》][32] | [JSON](yqp_nlb_p1p_AEB.json) |
| `AEBA` | 福 | [《史記・楚元王世家》][32] | [JSON](yqp_nlb_p1p_AEBA.json) |
| `AF` | 長（高祖子） | [《史記・袁盎鼂錯列傳》][83] | [JSON](yqp_nlb_p1p_AF.json) |
| `AG` | 建（高祖子） | [《史記・高祖本紀》][8]、[《史記・呂太后本紀》][9] | [JSON](yqp_nlb_p1p_AG.json) |
| `AH` | 如意（高祖子） | [《史記・呂太后本紀》][9] | [JSON](yqp_nlb_p1p_AH.json) |
| `AI` | 魯元（本卷稱呼） | [《史記・呂太后本紀》][9] | [JSON](yqp_nlb_p1p_AI.json) |
| `B` | 伯 | [《史記・楚元王世家》][32] | [JSON](yqp_nlb_p1p_B.json) |
| `BA` | 信羹頡侯 | [《史記・楚元王世家》][32] | [JSON](yqp_nlb_p1p_BA.json) |
| `C` | 仲 | [《史記・高祖本紀》][8]、[《史記・吳王濞列傳》][88] | [JSON](yqp_nlb_p1p_C.json) |
| `CA` | 劉濞 | [《史記・吳王濞列傳》][88] | [JSON](yqp_nlb_p1p_CA.json) |
| `CAA` | 吳太子被殺未名 | [《史記・吳王濞列傳》][88] | [JSON](yqp_nlb_p1p_CAA.json) |
| `CAB` | 吳王少子未名 | [《史記・吳王濞列傳》][88] | [JSON](yqp_nlb_p1p_CAB.json) |
| `CAC` | 吳王戰時太子未名 | [《史記・吳王濞列傳》][88] | [JSON](yqp_nlb_p1p_CAC.json) |
| `CAD` | 子華 | [《史記・吳王濞列傳》][88] | [JSON](yqp_nlb_p1p_CAD.json) |
| `CAE` | 子駒 | [《史記・吳王濞列傳》][88] | [JSON](yqp_nlb_p1p_CAE.json) |
| `D` | 劉交 | [《史記・楚元王世家》][32] | [JSON](yqp_nlb_p1p_D.json) |
| `DA` | 藝（楚元王子） | [《史記・孝景本紀》][11] | [JSON](yqp_nlb_p1p_DA.json) |
| `DB` | 禮（楚元王子） | [《史記・楚元王世家》][32] | [JSON](yqp_nlb_p1p_DB.json) |
| `DBA` | 道 | [《史記・楚元王世家》][32] | [JSON](yqp_nlb_p1p_DBA.json) |
| `DBAA` | 注 | [《史記・楚元王世家》][32] | [JSON](yqp_nlb_p1p_DBAA.json) |
| `DBAAA` | 純 | [《史記・楚元王世家》][32] | [JSON](yqp_nlb_p1p_DBAAA.json) |
| `DC` | 郢 | [《史記・楚元王世家》][32] | [JSON](yqp_nlb_p1p_DC.json) |
| `DCA` | 戊（楚王） | [《史記・楚元王世家》][32] | [JSON](yqp_nlb_p1p_DCA.json) |

</details>

<details><summary><code>z0a_bdl_gn5</code> 秦王政（李斯列傳候選）（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 秦王政 | [《史記・李斯列傳》][69] | [JSON](z0a_bdl_gn5.json) |
| `A` | 扶蘇 | [《史記・李斯列傳》][69] | [JSON](z0a_bdl_gn5_A.json) |
| `B` | 胡亥 | [《史記・秦始皇本紀》][6] | [JSON](z0a_bdl_gn5_B.json) |

</details>

<details><summary><code>z8l_wje_08d</code> 卜商（弟子列傳候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 卜商 | [《史記・仲尼弟子列傳》][49] | [JSON](z8l_wje_08d.json) |
| `A` | 卜商之子 | [《史記・仲尼弟子列傳》][49] | [JSON](z8l_wje_08d_A.json) |

</details>

<details><summary><code>zan_qcc_jy5</code> 陳文公（田世家候選）（19 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 陳文公 | [《史記・田敬仲完世家》][28] | [JSON](zan_qcc_jy5.json) |
| `A` | 陳厲公他 | [《史記・田敬仲完世家》][28] | [JSON](zan_qcc_jy5_A.json) |
| `AA` | 陳完 | [《史記・田敬仲完世家》][28] | [JSON](zan_qcc_jy5_AA.json) |
| `AAA` | 稚孟夷 | [《史記・田敬仲完世家》][28] | [JSON](zan_qcc_jy5_AAA.json) |
| `AAAA` | 湣孟莊 | [《史記・田敬仲完世家》][28] | [JSON](zan_qcc_jy5_AAAA.json) |
| `AAAAA` | 田文子須無 | [《史記・田敬仲完世家》][28] | [JSON](zan_qcc_jy5_AAAAA.json) |
| `AAAAAA` | 田桓子無宇 | [《史記・田敬仲完世家》][28] | [JSON](zan_qcc_jy5_AAAAAA.json) |
| `AAAAAAA` | 武子開 | [《史記・田敬仲完世家》][28] | [JSON](zan_qcc_jy5_AAAAAAA.json) |
| `AAAAAAB` | 田釐子乞 | [《史記・田敬仲完世家》][28] | [JSON](zan_qcc_jy5_AAAAAAB.json) |
| `AAAAAABA` | 田常 | [《史記・田敬仲完世家》][28] | [JSON](zan_qcc_jy5_AAAAAABA.json) |
| `AAAAAABAA` | 田襄子盤 | [《史記・田敬仲完世家》][28] | [JSON](zan_qcc_jy5_AAAAAABAA.json) |
| `AAAAAABAAA` | 田莊子白 | [《史記・田敬仲完世家》][28] | [JSON](zan_qcc_jy5_AAAAAABAAA.json) |
| `AAAAAABAAAA` | 太公和 | [《史記・田敬仲完世家》][28] | [JSON](zan_qcc_jy5_AAAAAABAAAA.json) |
| `AAAAAABAAAAA` | 桓公午 | [《史記・田敬仲完世家》][28] | [JSON](zan_qcc_jy5_AAAAAABAAAAA.json) |
| `AAAAAABAAAAAA` | 因齊 | [《史記・田敬仲完世家》][28] | [JSON](zan_qcc_jy5_AAAAAABAAAAAA.json) |
| `AAAAAABAAAAAAA` | 辟彊 | [《史記・田敬仲完世家》][28]、[《史記・孟嘗君列傳》][57] | [JSON](zan_qcc_jy5_AAAAAABAAAAAAA.json) |
| `AAAAAABAAAAAAAA` | 地 | [《史記・孟嘗君列傳》][57] | [JSON](zan_qcc_jy5_AAAAAABAAAAAAAA.json) |
| `AAAAAABAAAAAAAAA` | 法章 | [《史記・田敬仲完世家》][28] | [JSON](zan_qcc_jy5_AAAAAABAAAAAAAAA.json) |
| `AAAAAABAAAAAAAAAA` | 建 | [《史記・田敬仲完世家》][28] | [JSON](zan_qcc_jy5_AAAAAABAAAAAAAAAA.json) |

</details>

<details><summary><code>zk0_g6b_nbq</code> 伍奢（楚篇候選）（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 伍奢 | [《史記・楚世家》][22] | [JSON](zk0_g6b_nbq.json) |
| `A` | 伍尚 | [《史記・楚世家》][22] | [JSON](zk0_g6b_nbq_A.json) |
| `B` | 伍胥 | [《史記・楚世家》][22] | [JSON](zk0_g6b_nbq_B.json) |

</details>

<details><summary><code>zql_k3t_8ro</code> 先軫（重耳五士）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 先軫（重耳五士） | [《史記・晉世家》][21] | [JSON](zql_k3t_8ro.json) |
| `A` | 先縠（右行將） | [《史記・晉世家》][21] | [JSON](zql_k3t_8ro_A.json) |

</details>

<details><summary><code>zrx_2ip_d1p</code> 張負（陳丞相世家候選）（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 張負 | [《史記・陳丞相世家》][38] | [JSON](zrx_2ip_d1p.json) |
| `*A` | 張氏女 | [《史記・陳丞相世家》][38] | [JSON](zrx_2ip_d1p_%2AA.json) |
| `A` | 張仲 | [《史記・陳丞相世家》][38] | [JSON](zrx_2ip_d1p_A.json) |

</details>

<details><summary><code>zwr_jel_e3l</code> 齊宣公（田世家候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 齊宣公 | [《史記・田敬仲完世家》][28] | [JSON](zwr_jel_e3l.json) |
| `A` | 康公貸 | [《史記・田敬仲完世家》][28] | [JSON](zwr_jel_e3l_A.json) |

</details>

<details><summary><code>zxf_443_omv</code> 趙盾（韓世家候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 趙盾 | [《史記・韓世家》][27] | [JSON](zxf_443_omv.json) |
| `A` | 趙朔 | [《史記・趙世家》][25] | [JSON](zxf_443_omv_A.json) |

</details>


[1]: https://zh.wikisource.org/w/index.php?title=史記/卷001&oldid=7903634
[2]: https://zh.wikisource.org/w/index.php?title=史記/卷002&oldid=7903612
[3]: https://zh.wikisource.org/w/index.php?title=史記/卷003&oldid=7909145
[4]: https://zh.wikisource.org/w/index.php?title=史記/卷004&oldid=7909147
[5]: https://zh.wikisource.org/w/index.php?title=史記/卷005&oldid=8744286
[6]: https://zh.wikisource.org/w/index.php?title=史記/卷006&oldid=7907969
[7]: https://zh.wikisource.org/w/index.php?title=史記/卷007&oldid=5978360
[8]: https://zh.wikisource.org/w/index.php?title=史記/卷008&oldid=2440965
[9]: https://zh.wikisource.org/w/index.php?title=史記/卷009&oldid=2087062
[10]: https://zh.wikisource.org/w/index.php?title=史記/卷010&oldid=2599229
[11]: https://zh.wikisource.org/w/index.php?title=史記/卷011&oldid=2520527
[12]: https://zh.wikisource.org/w/index.php?title=史記/卷012&oldid=8733061
[13]: https://zh.wikisource.org/w/index.php?title=史記/卷031&oldid=7909287
[14]: https://zh.wikisource.org/w/index.php?title=史記/卷032&oldid=445042
[15]: https://zh.wikisource.org/w/index.php?title=史記/魯周公世家&oldid=7909289
[16]: https://zh.wikisource.org/w/index.php?title=史記/卷034&oldid=2559287
[17]: https://zh.wikisource.org/w/index.php?title=史記/卷035&oldid=8737302
[18]: https://zh.wikisource.org/w/index.php?title=史記/卷036&oldid=2588525
[19]: https://zh.wikisource.org/w/index.php?title=史記/卷037&oldid=5977124
[20]: https://zh.wikisource.org/w/index.php?title=史記/卷038&oldid=8737306
[21]: https://zh.wikisource.org/w/index.php?title=史記/卷039&oldid=2588534
[22]: https://zh.wikisource.org/w/index.php?title=史記/卷040&oldid=8736796
[23]: https://zh.wikisource.org/w/index.php?title=史記/卷041&oldid=2018395
[24]: https://zh.wikisource.org/w/index.php?title=史記/卷042&oldid=2016409
[25]: https://zh.wikisource.org/w/index.php?title=史記/卷043&oldid=7903603
[26]: https://zh.wikisource.org/w/index.php?title=史記/卷044&oldid=7903606
[27]: https://zh.wikisource.org/w/index.php?title=史記/卷045&oldid=7903607
[28]: https://zh.wikisource.org/w/index.php?title=史記/卷046&oldid=2560838
[29]: https://zh.wikisource.org/w/index.php?title=史記/卷047&oldid=7903609
[30]: https://zh.wikisource.org/w/index.php?title=史記/卷048&oldid=2531218
[31]: https://zh.wikisource.org/w/index.php?title=史記/卷049&oldid=7903610
[32]: https://zh.wikisource.org/w/index.php?title=史記/卷050&oldid=8737728
[33]: https://zh.wikisource.org/w/index.php?title=史記/卷051&oldid=2380315
[34]: https://zh.wikisource.org/w/index.php?title=史記/卷052&oldid=5977113
[35]: https://zh.wikisource.org/w/index.php?title=史記/卷053&oldid=2087971
[36]: https://zh.wikisource.org/w/index.php?title=史記/卷054&oldid=1490182
[37]: https://zh.wikisource.org/w/index.php?title=史記/卷055&oldid=2666612
[38]: https://zh.wikisource.org/w/index.php?title=史記/卷056&oldid=1961615
[39]: https://zh.wikisource.org/w/index.php?title=史記/卷057&oldid=1569360
[40]: https://zh.wikisource.org/w/index.php?title=史記/卷058&oldid=8735555
[41]: https://zh.wikisource.org/w/index.php?title=史記/卷059&oldid=2621125
[42]: https://zh.wikisource.org/w/index.php?title=史記/卷060&oldid=7909290
[43]: https://zh.wikisource.org/w/index.php?title=史記/卷061&oldid=2621133
[44]: https://zh.wikisource.org/w/index.php?title=史記/卷062&oldid=7903600
[45]: https://zh.wikisource.org/w/index.php?title=史記/卷063&oldid=7903601
[46]: https://zh.wikisource.org/w/index.php?title=史記/卷064&oldid=7895410
[47]: https://zh.wikisource.org/w/index.php?title=史記/卷065&oldid=2567048
[48]: https://zh.wikisource.org/w/index.php?title=史記/卷066&oldid=2621138
[49]: https://zh.wikisource.org/w/index.php?title=史記/卷067&oldid=7869003
[50]: https://zh.wikisource.org/w/index.php?title=史記/卷068&oldid=8764712
[51]: https://zh.wikisource.org/w/index.php?title=史記/卷069&oldid=2621145
[52]: https://zh.wikisource.org/w/index.php?title=史記/卷070&oldid=2621148
[53]: https://zh.wikisource.org/w/index.php?title=史記/卷071&oldid=2621152
[54]: https://zh.wikisource.org/w/index.php?title=史記/卷072&oldid=367921
[55]: https://zh.wikisource.org/w/index.php?title=史記/卷073&oldid=7909285
[56]: https://zh.wikisource.org/w/index.php?title=史記/卷074&oldid=7908177
[57]: https://zh.wikisource.org/w/index.php?title=史記/卷075&oldid=1965692
[58]: https://zh.wikisource.org/w/index.php?title=史記/卷076&oldid=7909284
[59]: https://zh.wikisource.org/w/index.php?title=史記/卷077&oldid=367917
[60]: https://zh.wikisource.org/w/index.php?title=史記/卷078&oldid=2089016
[61]: https://zh.wikisource.org/w/index.php?title=史記/卷079&oldid=2549307
[62]: https://zh.wikisource.org/w/index.php?title=史記/卷080&oldid=2089316
[63]: https://zh.wikisource.org/w/index.php?title=史記/卷081&oldid=8735558
[64]: https://zh.wikisource.org/w/index.php?title=史記/卷082&oldid=2529471
[65]: https://zh.wikisource.org/w/index.php?title=史記/卷083&oldid=2089252
[66]: https://zh.wikisource.org/w/index.php?title=史記/卷084&oldid=1568305
[67]: https://zh.wikisource.org/w/index.php?title=史記/卷085&oldid=2027911
[68]: https://zh.wikisource.org/w/index.php?title=史記/卷086&oldid=2388562
[69]: https://zh.wikisource.org/w/index.php?title=史記/卷087&oldid=2364605
[70]: https://zh.wikisource.org/w/index.php?title=史記/卷088&oldid=1965690
[71]: https://zh.wikisource.org/w/index.php?title=史記/卷089&oldid=8744143
[72]: https://zh.wikisource.org/w/index.php?title=史記/卷090&oldid=376055
[73]: https://zh.wikisource.org/w/index.php?title=史記/卷091&oldid=2509940
[74]: https://zh.wikisource.org/w/index.php?title=史記/卷092&oldid=2256147
[75]: https://zh.wikisource.org/w/index.php?title=史記/卷093&oldid=368019
[76]: https://zh.wikisource.org/w/index.php?title=史記/卷094&oldid=2171897
[77]: https://zh.wikisource.org/w/index.php?title=史記/卷095&oldid=2298709
[78]: https://zh.wikisource.org/w/index.php?title=史記/卷096&oldid=8770206
[79]: https://zh.wikisource.org/w/index.php?title=史記/卷097&oldid=1383195
[80]: https://zh.wikisource.org/w/index.php?title=史記/卷098&oldid=1490318
[81]: https://zh.wikisource.org/w/index.php?title=史記/卷099&oldid=368013
[82]: https://zh.wikisource.org/w/index.php?title=史記/卷100&oldid=1965696
[83]: https://zh.wikisource.org/w/index.php?title=史記/卷101&oldid=368092
[84]: https://zh.wikisource.org/w/index.php?title=史記/卷102&oldid=1753957
[85]: https://zh.wikisource.org/w/index.php?title=史記/卷103&oldid=2096814
[86]: https://zh.wikisource.org/w/index.php?title=史記/卷104&oldid=8739534
[87]: https://zh.wikisource.org/w/index.php?title=史記/卷105&oldid=8842726
[88]: https://zh.wikisource.org/w/index.php?title=史記/卷106&oldid=405869
