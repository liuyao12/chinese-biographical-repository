# 人物 JSON 索引

可重建匯出，涵蓋目前已標註資料，包含明示選用的暫定跨篇同指；原 ID、證據與判讀均保留。並非全部史料或完整覆核。

程式可讀取 [index.json](index.json)，再依各筆 `path` 取得人物資料。重新產生：`python3 scripts/export_person_bundles.py`。

出生排行與籍貫結構化欄位仍在逐篇回填；缺欄位不代表來源沒有此資訊。

漢劉氏的組裝見 [家族組裝資料](../../registry/family-assemblies.json)。`assembled_identity.person_id` 是共用家族根的組裝 ID，`source_person_ids` 保留各篇候選；父子及同指證據可由記錄 ID 回查。

點選家族標題可展開或收起後代。`*` 表示缺名世代，不建立人物，也不表示不同缺名位置是同一人。表內只列家族根後的 ID 尾碼；根人物以「根」表示，完整 ID 保留於家族標題及 JSON。最多提及來源另列一欄，同數並列；提及次數不代表史料優先權。舊 ID 與 JSON 入口保留為別名；索引只計現行人物。

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

## 尚未連入同族的人物

| 人物 ID | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `00c_o71_46y` | 太史公 | [《史記・傅靳蒯成列傳》][80] | [JSON](00c_o71_46y.json) |
| `00c_uyw_qpw` | 平陽君 | [《史記・白起王翦列傳》][55] | [JSON](00c_uyw_qpw.json) |
| `00m_y5g_qwy` | 孝景 | [《史記・韓信盧綰列傳》][75] | [JSON](00m_y5g_qwy.json) |
| `00z_jmb_pug` | 孔子 | [《史記・田叔列傳》][86] | [JSON](00z_jmb_pug.json) |
| `01e_vdz_o3s` | 少傅安 | [《史記・三王世家》][42] | [JSON](01e_vdz_o3s.json) |
| `01l_433_l69` | 申叔時（楚使者） | [《史記・陳杞世家》][18]、[《史記・楚世家》][22] | [JSON](01l_433_l69.json) |
| `01m_8vn_zqy` | 陳勝 | [《史記・劉敬叔孫通列傳》][81] | [JSON](01m_8vn_zqy.json) |
| `023_j4f_3vn` | 孟嘗 | [《史記・魏世家》][26] | [JSON](023_j4f_3vn.json) |
| `02f_ql9_7if` | 毀孟嘗於齊湣者未名 | [《史記・孟嘗君列傳》][57] | [JSON](02f_ql9_7if.json) |
| `02g_rlg_6nk` | 河閒王未名 | [《史記・萬石張叔列傳》][85] | [JSON](02g_rlg_6nk.json) |
| `02k_166_l3b` | 闔閭引古 | [《史記・樂毅列傳》][62] | [JSON](02k_166_l3b.json) |
| `02m_tgr_6k2` | 韓廣母（陳涉世家未名者） | [《史記・陳涉世家》][30] | [JSON](02m_tgr_6k2.json) |
| `02p_okn_rhi` | 秦太子（魏世家質魏死未名者） | [《史記・魏世家》][26] | [JSON](02p_okn_rhi.json) |
| `02z_7va_g33` | 荊軻 | [《史記・刺客列傳》][68] | [JSON](02z_7va_g33.json) |
| `03j_syw_e4g` | 湣王（尉繚引述） | [《史記・秦始皇本紀》][6] | [JSON](03j_syw_e4g.json) |
| `03v_bhv_img` | 趙勝 | [《史記・平原君虞卿列傳》][58] | [JSON](03v_bhv_img.json) |
| `03x_n5w_br7` | 閼與秦將未名 | [《史記・廉頗藺相如列傳》][63] | [JSON](03x_n5w_br7.json) |
| `04g_x9a_lho` | 勃（太尉用稱） | [《史記・韓信盧綰列傳》][75] | [JSON](04g_x9a_lho.json) |
| `04s_md1_e2f` | 薄太后 | [《史記・張釋之馮唐列傳》][84] | [JSON](04s_md1_e2f.json) |
| `04z_mgy_h00` | 客人 | [《史記・商君列傳》][50] | [JSON](04z_mgy_h00.json) |
| `052_eu1_tdb` | 建元中上未具名 | [《史記・袁盎鼂錯列傳》][83] | [JSON](052_eu1_tdb.json) |
| `057_xe9_rab` | 祝融 | [《史記・鄭世家》][24] | [JSON](057_xe9_rab.json) |
| `05u_ssx_nu1` | 箕子引古 | [《史記・范睢蔡澤列傳》][61] | [JSON](05u_ssx_nu1.json) |
| `063_z1q_xjl` | 傅抵 | [《史記・趙世家》][25] | [JSON](063_z1q_xjl.json) |
| `06j_tk0_9q6` | 越王句踐 | [《史記・伍子胥列傳》][48] | [JSON](06j_tk0_9q6.json) |
| `06n_ttw_xgt` | 鄒陽 | [《史記・梁孝王世家》][40] | [JSON](06n_ttw_xgt.json) |
| `06s_zyx_maw` | 墨翟引古 | [《史記・魯仲連鄒陽列傳》][65] | [JSON](06s_zyx_maw.json) |
| `070_l9o_nc8` | 梁惠王 | [《史記・老子韓非列傳》][45] | [JSON](070_l9o_nc8.json) |
| `078_odx_6hv` | 賀 | [《史記・五宗世家》][41] | [JSON](078_odx_6hv.json) |
| `07v_jz5_mnd` | 成差（秦將） | [《史記・晉世家》][21] | [JSON](07v_jz5_mnd.json) |
| `07x_xmm_xfa` | 无忌 | [《史記・魏公子列傳》][59] | [JSON](07x_xmm_xfa.json) |
| `08a_qz8_tyb` | 太史公 | [《史記・荊燕世家》][33] | [JSON](08a_qz8_tyb.json) |
| `08d_ist_dhd` | 比干 | [《史記・孔子世家》][29] | [JSON](08d_ist_dhd.json) |
| `08j_zgn_g6d` | 東陽侯未名 | [《史記・屈原賈生列傳》][66] | [JSON](08j_zgn_g6d.json) |
| `08l_wt5_kry` | 伍子胥 | [《史記・仲尼弟子列傳》][49] | [JSON](08l_wt5_kry.json) |
| `09a_teq_6v4` | 吳王夫差（引古） | [《史記・蒙恬列傳》][70] | [JSON](09a_teq_6v4.json) |
| `09s_wy8_uyj` | 甫假 | [《史記・鄭世家》][24] | [JSON](09s_wy8_uyj.json) |
| `09x_42a_awj` | 高陵君 | [《史記・范睢蔡澤列傳》][61] | [JSON](09x_42a_awj.json) |
| `09z_62n_amz` | 楚威王 | [《史記・老子韓非列傳》][45] | [JSON](09z_62n_amz.json) |
| `0ak_s2u_6hd` | 趙稷 | [《史記・趙世家》][25] | [JSON](0ak_s2u_6hd.json) |
| `0am_5u1_2in` | 陽文君 | [《史記・春申君列傳》][60] | [JSON](0am_5u1_2in.json) |
| `0as_za5_mdt` | 呂媭女（劉澤妻） | [《史記・呂太后本紀》][9] | [JSON](0as_za5_mdt.json) |
| `0bh_flo_trm` | 季桓子（魯卿） | [《史記・魯周公世家》][15] | [JSON](0bh_flo_trm.json) |
| `0bm_5gr_a7x` | 少主未詳名 | [《史記・酈生陸賈列傳》][79] | [JSON](0bm_5gr_a7x.json) |
| `0bm_dju_96r` | 丁公（齊人封禪議者） | [《史記・孝武本紀》][12] | [JSON](0bm_dju_96r.json) |
| `0bw_wln_zu9` | 公孫弘 | [《史記・孝武本紀》][12] | [JSON](0bw_wln_zu9.json) |
| `0c1_mro_k7x` | 梁王未具名 | [《史記・張釋之馮唐列傳》][84] | [JSON](0c1_mro_k7x.json) |
| `0cl_p1u_mri` | 渾邪（隴西太守） | [《史記・孝景本紀》][11] | [JSON](0cl_p1u_mri.json) |
| `0ct_rge_697` | 韓舉 | [《史記・韓世家》][27] | [JSON](0ct_rge_697.json) |
| `0cu_hq2_9t8` | 莊襄王 | [《史記・李斯列傳》][69] | [JSON](0cu_hq2_9t8.json) |
| `0d8_fpd_jlq` | 高誓 | [《史記・秦始皇本紀》][6] | [JSON](0d8_fpd_jlq.json) |
| `0dj_gcr_vj7` | 趙良 | [《史記・商君列傳》][50] | [JSON](0dj_gcr_vj7.json) |
| `0e2_f7l_x0w` | 賈嘉 | [《史記・屈原賈生列傳》][66] | [JSON](0e2_f7l_x0w.json) |
| `0e4_dav_p5t` | 聶政母未名 | [《史記・刺客列傳》][68] | [JSON](0e4_dav_p5t.json) |
| `0f5_o4n_ur1` | 秦孝公引古 | [《史記・范睢蔡澤列傳》][61] | [JSON](0f5_o4n_ur1.json) |
| `0ff_m7l_g3x` | 女鳩 | [《史記・殷本紀》][3] | [JSON](0ff_m7l_g3x.json) |
| `0fj_88o_fyj` | 惠文后（趙世家未名者） | [《史記・趙世家》][25] | [JSON](0fj_88o_fyj.json) |
| `0fm_cc8_dzu` | 亞圉 | [《史記・周本紀》][4] | [JSON](0fm_cc8_dzu.json) |
| `0fv_vgd_85y` | 延陵季子 | [《史記・趙世家》][25] | [JSON](0fv_vgd_85y.json) |
| `0g3_cdx_6yo` | 賈佗（重耳五士） | [《史記・晉世家》][21]、[《史記・楚世家》][22] | [JSON](0g3_cdx_6yo.json) |
| `0gg_iqz_iey` | 景駒 | [《史記・黥布列傳》][73] | [JSON](0gg_iqz_iey.json) |
| `0gr_kq8_371` | 魯桓公 | [《史記・魯周公世家》][15] | [JSON](0gr_kq8_371.json) |
| `0gy_vl6_l9g` | 林慮公主 | [《史記・外戚世家》][31] | [JSON](0gy_vl6_l9g.json) |
| `0h0_68r_si5` | 咎單 | [《史記・殷本紀》][3] | [JSON](0h0_68r_si5.json) |
| `0h7_yvr_qgh` | 左公子（衛壽朔傅） | [《史記・衛康叔世家》][19] | [JSON](0h7_yvr_qgh.json) |
| `0hi_bbh_glh` | 桓公（燕釐公後） | [《史記・燕召公世家》][16] | [JSON](0hi_bbh_glh.json) |
| `0hj_4kj_cen` | 太史儋 | [《史記・老子韓非列傳》][45] | [JSON](0hj_4kj_cen.json) |
| `0i1_nlq_3m4` | 項羽 | [《史記・項羽本紀》][7] | [JSON](0i1_nlq_3m4.json) |
| `0ij_f01_5wr` | 魏齊 | [《史記・范睢蔡澤列傳》][61] | [JSON](0ij_f01_5wr.json) |
| `0ix_wr1_nuo` | 單于 | [《史記・陳丞相世家》][38] | [JSON](0ix_wr1_nuo.json) |
| `0j3_2uz_7wo` | 秦嘉 | [《史記・項羽本紀》][7] | [JSON](0j3_2uz_7wo.json) |
| `0j5_w25_k4p` | 甘龍 | [《史記・商君列傳》][50] | [JSON](0j5_w25_k4p.json) |
| `0jb_r4l_gxr` | 桀引古 | [《史記・田單列傳》][64] | [JSON](0jb_r4l_gxr.json) |
| `0jj_3xt_ip6` | 太子未名 | [《史記・淮陰侯列傳》][74] | [JSON](0jj_3xt_ip6.json) |
| `0jl_b1p_z9y` | 由余引古 | [《史記・魯仲連鄒陽列傳》][65] | [JSON](0jl_b1p_z9y.json) |
| `0jy_rdt_zu1` | 石奮姊未名 | [《史記・萬石張叔列傳》][85] | [JSON](0jy_rdt_zu1.json) |
| `0k3_rt8_aa5` | 狗盜客未名 | [《史記・孟嘗君列傳》][57] | [JSON](0k3_rt8_aa5.json) |
| `0k4_eok_19j` | 靈公夫人（命郢太子者） | [《史記・衛康叔世家》][19] | [JSON](0k4_eok_19j.json) |
| `0k8_5z8_6e7` | 相者老父（高祖田間敘事） | [《史記・高祖本紀》][8] | [JSON](0k8_5z8_6e7.json) |
| `0kd_j19_qdq` | 綺里季 | [《史記・留侯世家》][37] | [JSON](0kd_j19_qdq.json) |
| `0kw_mlk_u3z` | 去疾（秦右丞相） | [《史記・秦始皇本紀》][6] | [JSON](0kw_mlk_u3z.json) |
| `0l7_ynh_g9v` | 薄昭 | [《史記・孝文本紀》][10] | [JSON](0l7_ynh_g9v.json) |
| `0lb_ygj_t93` | 臧荼 | [《史記・季布欒布列傳》][82] | [JSON](0lb_ygj_t93.json) |
| `0lb_z6g_41m` | 荀卿 | [《史記・孟子荀卿列傳》][56] | [JSON](0lb_z6g_41m.json) |
| `0lu_9v0_ck5` | 武王引古 | [《史記・穰侯列傳》][54] | [JSON](0lu_9v0_ck5.json) |
| `0m1_h6w_rs2` | 由引古短稱未定 | [《史記・魯仲連鄒陽列傳》][65] | [JSON](0m1_h6w_rs2.json) |
| `0ml_cvy_pxe` | 韓徐 | [《史記・趙世家》][25] | [JSON](0ml_cvy_pxe.json) |
| `0n7_8en_8ji` | 趙孝成王 | [《史記・白起王翦列傳》][55] | [JSON](0n7_8en_8ji.json) |
| `0ng_one_sdy` | 宋玉 | [《史記・屈原賈生列傳》][66] | [JSON](0ng_one_sdy.json) |
| `0o0_6rh_6u5` | 韓公叔 | [《史記・張儀列傳》][52] | [JSON](0o0_6rh_6u5.json) |
| `0of_7ly_ddz` | 竇太后 | [《史記・楚元王世家》][32] | [JSON](0of_7ly_ddz.json) |
| `0oi_5wz_q0n` | 項伯 | [《史記・黥布列傳》][73] | [JSON](0oi_5wz_q0n.json) |
| `0p4_7a4_vvh` | 龐涓 | [《史記・孫子吳起列傳》][47] | [JSON](0p4_7a4_vvh.json) |
| `0p4_ef2_1xa` | 龐暖 | [《史記・廉頗藺相如列傳》][63] | [JSON](0p4_ef2_1xa.json) |
| `0p8_ug5_eja` | 晉平公 | [《史記・魯周公世家》][15]、[《史記・晉世家》][21] | [JSON](0p8_ug5_eja.json) |
| `0pp_ng8_juf` | 江羋（楚成王寵姬） | [《史記・楚世家》][22] | [JSON](0pp_ng8_juf.json) |
| `0ps_77i_xfv` | 造父 | [《史記・秦本紀》][5] | [JSON](0ps_77i_xfv.json) |
| `0q2_ioh_psy` | 周袑 | [《史記・趙世家》][25] | [JSON](0q2_ioh_psy.json) |
| `0q5_5mc_kx6` | 樂瑕公 | [《史記・樂毅列傳》][62] | [JSON](0q5_5mc_kx6.json) |
| `0q9_h79_ob0` | 陽處父（賈季所殺者） | [《史記・晉世家》][21] | [JSON](0q9_h79_ob0.json) |
| `0qj_puw_myv` | 慎到 | [《史記・孟子荀卿列傳》][56] | [JSON](0qj_puw_myv.json) |
| `0qr_fjs_wjx` | 馯臂子弘 | [《史記・仲尼弟子列傳》][49] | [JSON](0qr_fjs_wjx.json) |
| `0qu_bd0_57x` | 秦王（田世家煮棗議論未名者） | [《史記・田敬仲完世家》][28] | [JSON](0qu_bd0_57x.json) |
| `0r9_eg1_k8e` | 桑弘羊 | [《史記・萬石張叔列傳》][85] | [JSON](0r9_eg1_k8e.json) |
| `0rc_0ya_wg8` | 申包胥 | [《史記・秦本紀》][5] | [JSON](0rc_0ya_wg8.json) |
| `0rg_7of_rgi` | 魏襄王 | [《史記・蘇秦列傳》][51] | [JSON](0rg_7of_rgi.json) |
| `0ri_3st_fjq` | 桓楚 | [《史記・項羽本紀》][7] | [JSON](0ri_3st_fjq.json) |
| `0rm_hvx_4a6` | 神農 | [《史記・趙世家》][25] | [JSON](0rm_hvx_4a6.json) |
| `0rr_kmr_57j` | 杜赫 | [《史記・陳涉世家》][30] | [JSON](0rr_kmr_57j.json) |
| `0ru_rmr_cxs` | 逢丑父 | [《史記・韓世家》][27] | [JSON](0ru_rmr_cxs.json) |
| `0sl_eh8_yhw` | 呂后 | [《史記・季布欒布列傳》][82] | [JSON](0sl_eh8_yhw.json) |
| `0sl_xzo_kcf` | 共公（燕悼公後） | [《史記・燕召公世家》][16] | [JSON](0sl_xzo_kcf.json) |
| `0st_zou_rja` | 太史公 | [《史記・穰侯列傳》][54] | [JSON](0st_zou_rja.json) |
| `0th_8iq_2q0` | 王龁 | [《史記・白起王翦列傳》][55] | [JSON](0th_8iq_2q0.json) |
| `0tj_vst_yao` | 張儀 | [《史記・樗里子甘茂列傳》][53] | [JSON](0tj_vst_yao.json) |
| `0tp_9hs_kjs` | 孔子 | [《史記・孔子世家》][29] | [JSON](0tp_9hs_kjs.json) |
| `0tz_6h5_zmv` | 秦武王 | [《史記・魏世家》][26] | [JSON](0tz_6h5_zmv.json) |
| `0w8_6xd_lpn` | 魏讎餘 | [《史記・秦本紀》][5] | [JSON](0w8_6xd_lpn.json) |
| `0wd_9iu_71i` | 陳渉 | [《史記・張耳陳餘列傳》][71] | [JSON](0wd_9iu_71i.json) |
| `0wf_2jc_8dh` | 夫概 | [《史記・吳太伯世家》][13] | [JSON](0wf_2jc_8dh.json) |
| `0wg_3ra_wdt` | 田忌 | [《史記・田敬仲完世家》][28] | [JSON](0wg_3ra_wdt.json) |
| `0wg_9tr_v8o` | 周子家豎 | [《史記・仲尼弟子列傳》][49] | [JSON](0wg_9tr_v8o.json) |
| `0wt_iyc_10n` | 識 | [《史記・魏世家》][26] | [JSON](0wt_iyc_10n.json) |
| `0wy_0ou_190` | 晉昭公 | [《史記・魏世家》][26] | [JSON](0wy_0ou_190.json) |
| `0wy_1jp_os3` | 大行騫 | [《史記・五宗世家》][41] | [JSON](0wy_1jp_os3.json) |
| `0xe_mxp_vls` | 顏何 | [《史記・仲尼弟子列傳》][49] | [JSON](0xe_mxp_vls.json) |
| `0xk_jpf_0xw` | 白起 | [《史記・白起王翦列傳》][55] | [JSON](0xk_jpf_0xw.json) |
| `0xm_s1t_gt4` | 齊湣王 | [《史記・魏世家》][26] | [JSON](0xm_s1t_gt4.json) |
| `0xx_ozc_454` | 趙高 | [《史記・李斯列傳》][69] | [JSON](0xx_ozc_454.json) |
| `0y8_25d_hrm` | 任鄙 | [《史記・秦本紀》][5] | [JSON](0y8_25d_hrm.json) |
| `0yh_g69_8b8` | 堯引古傳說 | [《史記・李斯列傳》][69] | [JSON](0yh_g69_8b8.json) |
| `0yo_s0o_8oq` | 幽王 | [《史記・外戚世家》][31] | [JSON](0yo_s0o_8oq.json) |
| `0yz_dji_ezy` | 辟陽侯（高祖本紀） | [《史記・高祖本紀》][8] | [JSON](0yz_dji_ezy.json) |
| `0z4_onh_r27` | 鄒陽 | [《史記・魯仲連鄒陽列傳》][65] | [JSON](0z4_onh_r27.json) |
| `0zd_hnj_i5u` | 莊賈 | [《史記・司馬穰苴列傳》][46] | [JSON](0zd_hnj_i5u.json) |
| `0zt_vze_ehx` | 丹 | [《史記・魏世家》][26] | [JSON](0zt_vze_ehx.json) |
| `100_d2u_5lk` | 魏襄 | [《史記・趙世家》][25] | [JSON](100_d2u_5lk.json) |
| `106_acx_xuq` | 范吉射 | [《史記・趙世家》][25] | [JSON](106_acx_xuq.json) |
| `11c_2n2_xqq` | 子綦（楚亂記事） | [《史記・陳杞世家》][18] | [JSON](11c_2n2_xqq.json) |
| `11t_oop_uck` | 翟景 | [《史記・秦始皇本紀》][6] | [JSON](11t_oop_uck.json) |
| `126_sy4_j11` | 新垣平 | [《史記・孝文本紀》][10] | [JSON](126_sy4_j11.json) |
| `12c_x1u_m8d` | 楚王東徙陳 | [《史記・白起王翦列傳》][55] | [JSON](12c_x1u_m8d.json) |
| `12e_g55_fat` | 晏圉 | [《史記・齊太公世家》][14] | [JSON](12e_g55_fat.json) |
| `12q_du8_nrm` | 昭滑 | [《史記・秦始皇本紀》][6] | [JSON](12q_du8_nrm.json) |
| `134_cb7_kph` | 公中緩 | [《史記・魏世家》][26] | [JSON](134_cb7_kph.json) |
| `13u_gnj_7au` | 南宮萬（宋臣） | [《史記・宋微子世家》][20] | [JSON](13u_gnj_7au.json) |
| `14d_o9y_nd0` | 田廣 | [《史記・曹相國世家》][36] | [JSON](14d_o9y_nd0.json) |
| `14z_ay0_40z` | 車千秋 | [《史記・田叔列傳》][86] | [JSON](14z_ay0_40z.json) |
| `15d_u8k_luo` | 蕭何 | [《史記・張丞相列傳》][78] | [JSON](15d_u8k_luo.json) |
| `15h_34z_4to` | 太嶽（姜姓祖先引語） | [《史記・陳杞世家》][18] | [JSON](15h_34z_4to.json) |
| `16c_ysj_x0r` | 子家 | [《史記・鄭世家》][24] | [JSON](16c_ysj_x0r.json) |
| `16n_czk_thg` | 田忌 | [《史記・田敬仲完世家》][28] | [JSON](16n_czk_thg.json) |
| `16v_9b1_4bn` | 桀溺 | [《史記・孔子世家》][29] | [JSON](16v_9b1_4bn.json) |
| `172_ij7_8yf` | 公子高 | [《史記・李斯列傳》][69] | [JSON](172_ij7_8yf.json) |
| `17c_7g8_b8g` | 盧生 | [《史記・秦始皇本紀》][6] | [JSON](17c_7g8_b8g.json) |
| `17g_8m0_z0r` | 秦王 | [《史記・老子韓非列傳》][45] | [JSON](17g_8m0_z0r.json) |
| `17m_f1z_yem` | 鴈門守圂 | [《史記・絳侯周勃世家》][39] | [JSON](17m_f1z_yem.json) |
| `18b_jpl_omt` | 夫差 | [《史記・孔子世家》][29] | [JSON](18b_jpl_omt.json) |
| `18h_w34_uzz` | 須（宋文公母弟） | [《史記・宋微子世家》][20] | [JSON](18h_w34_uzz.json) |
| `18m_gsh_vrt` | 智罃（楚所虜晉將） | [《史記・晉世家》][21] | [JSON](18m_gsh_vrt.json) |
| `18r_wn6_nhh` | 穆叔（昭公立時） | [《史記・魯周公世家》][15] | [JSON](18r_wn6_nhh.json) |
| `18x_9in_irn` | 涇陽君 | [《史記・蘇秦列傳》][51] | [JSON](18x_9in_irn.json) |
| `18z_pak_jrh` | 秦冉 | [《史記・仲尼弟子列傳》][49] | [JSON](18z_pak_jrh.json) |
| `19n_dlz_s8g` | 項籍 | [《史記・項羽本紀》][7] | [JSON](19n_dlz_s8g.json) |
| `19n_vi1_hfz` | 彭越 | [《史記・黥布列傳》][73] | [JSON](19n_vi1_hfz.json) |
| `19x_18p_3zj` | 御叔（夏姬夫） | [《史記・陳杞世家》][18] | [JSON](19x_18p_3zj.json) |
| `1a1_znz_wjz` | 魯閔公 | [《史記・趙世家》][25] | [JSON](1a1_znz_wjz.json) |
| `1a2_arl_bzv` | 武王 | [《史記・陳涉世家》][30] | [JSON](1a2_arl_bzv.json) |
| `1a2_o78_c2n` | 晉鄙 | [《史記・魏公子列傳》][59] | [JSON](1a2_o78_c2n.json) |
| `1aa_yn3_kv1` | 平陽公主 | [《史記・曹相國世家》][36] | [JSON](1aa_yn3_kv1.json) |
| `1ag_0z1_mlq` | 申侯 | [《史記・周本紀》][4] | [JSON](1ag_0z1_mlq.json) |
| `1as_2bm_qu5` | 李牧 | [《史記・廉頗藺相如列傳》][63] | [JSON](1as_2bm_qu5.json) |
| `1by_i1o_3pu` | 禹（引古） | [《史記・淮陰侯列傳》][74] | [JSON](1by_i1o_3pu.json) |
| `1bz_2re_b8l` | 毋卹之母（趙世家翟婢未名者） | [《史記・趙世家》][25] | [JSON](1bz_2re_b8l.json) |
| `1c0_cid_jlo` | 棠公妻（本卷未名） | [《史記・齊太公世家》][14] | [JSON](1c0_cid_jlo.json) |
| `1cd_mzr_sj4` | 當陽君（本卷稱呼） | [《史記・黥布列傳》][73] | [JSON](1cd_mzr_sj4.json) |
| `1cl_1rg_gk9` | 桓齮 | [《史記・廉頗藺相如列傳》][63] | [JSON](1cl_1rg_gk9.json) |
| `1cr_7o7_q01` | 宋莊公 | [《史記・鄭世家》][24] | [JSON](1cr_7o7_q01.json) |
| `1d2_lvj_esk` | 齊威王 | [《史記・孫子吳起列傳》][47] | [JSON](1d2_lvj_esk.json) |
| `1dh_qy1_ptc` | 晉獻公 | [《史記・趙世家》][25] | [JSON](1dh_qy1_ptc.json) |
| `1dm_ebc_uzk` | 散宜生 | [《史記・周本紀》][4] | [JSON](1dm_ebc_uzk.json) |
| `1dz_0ef_p4o` | 趙史援 | [《史記・趙世家》][25] | [JSON](1dz_0ef_p4o.json) |
| `1ec_jmi_32g` | 繻 | [《史記・鄭世家》][24] | [JSON](1ec_jmi_32g.json) |
| `1g7_uhi_22s` | 稷 | [《史記・趙世家》][25] | [JSON](1g7_uhi_22s.json) |
| `1gj_dvk_m38` | 尚席 | [《史記・絳侯周勃世家》][39] | [JSON](1gj_dvk_m38.json) |
| `1gk_6c4_iou` | 泰帝（素女敘事） | [《史記・孝武本紀》][12] | [JSON](1gk_6c4_iou.json) |
| `1h5_8jc_qp7` | 孟軻 | [《史記・孟子荀卿列傳》][56] | [JSON](1h5_8jc_qp7.json) |
| `1hb_k44_h0v` | 利（殺蔡昭侯者） | [《史記・管蔡世家》][17] | [JSON](1hb_k44_h0v.json) |
| `1hk_5o1_t7e` | 周殷 | [《史記・黥布列傳》][73] | [JSON](1hk_5o1_t7e.json) |
| `1hl_8ey_4br` | 祁侯賀 | [《史記・孝文本紀》][10] | [JSON](1hl_8ey_4br.json) |
| `1hn_skd_uu8` | 如耳 | [《史記・魏世家》][26] | [JSON](1hn_skd_uu8.json) |
| `1hq_b3w_91p` | 連稱 | [《史記・齊太公世家》][14] | [JSON](1hq_b3w_91p.json) |
| `1hy_i0l_xfz` | 棼如（喬如弟） | [《史記・魯周公世家》][15] | [JSON](1hy_i0l_xfz.json) |
| `1i8_vsx_dbq` | 章平 | [《史記・傅靳蒯成列傳》][80] | [JSON](1i8_vsx_dbq.json) |
| `1ia_b4v_w14` | 單于未詳名（嫚書） | [《史記・季布欒布列傳》][82] | [JSON](1ia_b4v_w14.json) |
| `1ia_pai_f8d` | 白起 | [《史記・魯仲連鄒陽列傳》][65] | [JSON](1ia_pai_f8d.json) |
| `1is_5g0_ufp` | 張春 | [《史記・曹相國世家》][36] | [JSON](1is_5g0_ufp.json) |
| `1is_max_s0c` | 蘇秦引古 | [《史記・范睢蔡澤列傳》][61] | [JSON](1is_max_s0c.json) |
| `1iv_bo2_ode` | 齊王畔約未名 | [《史記・吳王濞列傳》][88] | [JSON](1iv_bo2_ode.json) |
| `1jv_ziq_uxq` | 魏咎 | [《史記・陳丞相世家》][38] | [JSON](1jv_ziq_uxq.json) |
| `1jz_1em_9vm` | 陳豨 | [《史記・陳丞相世家》][38] | [JSON](1jz_1em_9vm.json) |
| `1kd_7ht_slq` | 虞（項王美人） | [《史記・項羽本紀》][7] | [JSON](1kd_7ht_slq.json) |
| `1kf_2ya_m0o` | 徹母（膠東王太后） | [《史記・外戚世家》][31] | [JSON](1kf_2ya_m0o.json) |
| `1kj_vhc_cx9` | 上官桀 | [《史記・三王世家》][42] | [JSON](1kj_vhc_cx9.json) |
| `1kl_hvr_p01` | 丹 | [《史記・五宗世家》][41] | [JSON](1kl_hvr_p01.json) |
| `1ku_2ry_mri` | 公孫支 | [《史記・秦本紀》][5] | [JSON](1ku_2ry_mri.json) |
| `1kw_6ot_aly` | 開地 | [《史記・留侯世家》][37] | [JSON](1kw_6ot_aly.json) |
| `1kz_3nc_s0n` | 鮑子 | [《史記・齊太公世家》][14] | [JSON](1kz_3nc_s0n.json) |
| `1l7_kaw_8j8` | 盂黶（蒯聵使者） | [《史記・衛康叔世家》][19] | [JSON](1l7_kaw_8j8.json) |
| `1le_lgg_yjv` | 成（昌武侯） | [《史記・秦始皇本紀》][6] | [JSON](1le_lgg_yjv.json) |
| `1lm_pm5_tpv` | 中衍 | [《史記・趙世家》][25] | [JSON](1lm_pm5_tpv.json) |
| `1lo_5gt_g3x` | 友（吳太子） | [《史記・吳太伯世家》][13] | [JSON](1lo_5gt_g3x.json) |
| `1lp_mgy_t05` | 申侯之女（大駱妻） | [《史記・秦本紀》][5] | [JSON](1lp_mgy_t05.json) |
| `1mi_jrf_gto` | 子魚（教宋湣公者） | [《史記・宋微子世家》][20] | [JSON](1mi_jrf_gto.json) |
| `1ml_gpo_pr5` | 管仲 | [《史記・刺客列傳》][68] | [JSON](1ml_gpo_pr5.json) |
| `1ml_lhf_3h1` | 尉斯離 | [《史記・秦本紀》][5] | [JSON](1ml_lhf_3h1.json) |
| `1mq_n0d_l6s` | 鄂侯引古 | [《史記・魯仲連鄒陽列傳》][65] | [JSON](1mq_n0d_l6s.json) |
| `1n9_5tg_1zs` | 夷王 | [《史記・周本紀》][4] | [JSON](1n9_5tg_1zs.json) |
| `1nk_3if_xps` | 荷蕢者（孔子世家未名者） | [《史記・孔子世家》][29] | [JSON](1nk_3if_xps.json) |
| `1nq_8wd_78r` | 女防 | [《史記・秦本紀》][5] | [JSON](1nq_8wd_78r.json) |
| `1nt_8g8_bif` | 子路 | [《史記・仲尼弟子列傳》][49] | [JSON](1nt_8g8_bif.json) |
| `1ot_coy_e83` | 老萊子 | [《史記・仲尼弟子列傳》][49] | [JSON](1ot_coy_e83.json) |
| `1ox_twh_3rs` | 伯陽（幽王時） | [《史記・周本紀》][4] | [JSON](1ox_twh_3rs.json) |
| `1p0_3w7_7vc` | 巫賢 | [《史記・殷本紀》][3]、[《史記・燕召公世家》][16] | [JSON](1p0_3w7_7vc.json) |
| `1p5_pqh_qdg` | 方與公未詳名 | [《史記・張丞相列傳》][78] | [JSON](1p5_pqh_qdg.json) |
| `1pc_iyw_umt` | 廧咎如長女（趙世家未名者） | [《史記・趙世家》][25] | [JSON](1pc_iyw_umt.json) |
| `1pz_hzu_z44` | 楚將軍（受商於地未名） | [《史記・楚世家》][22] | [JSON](1pz_hzu_z44.json) |
| `1qc_43r_k5l` | 張儀引古 | [《史記・李斯列傳》][69] | [JSON](1qc_43r_k5l.json) |
| `1r4_52u_h4m` | 子犯（楚篇晉文公腹心） | [《史記・晉世家》][21] | [JSON](1r4_52u_h4m.json) |
| `1re_sks_vyx` | 曹咎 | [《史記・高祖本紀》][8] | [JSON](1re_sks_vyx.json) |
| `1s5_789_bxk` | 太史公 | [《史記・孟嘗君列傳》][57] | [JSON](1s5_789_bxk.json) |
| `1s9_9xl_xoz` | 魏文侯引古 | [《史記・魯仲連鄒陽列傳》][65] | [JSON](1s9_9xl_xoz.json) |
| `1s9_u8o_ryn` | 巫咸 | [《史記・殷本紀》][3] | [JSON](1s9_u8o_ryn.json) |
| `1sd_oek_swt` | 餘樊君 | [《史記・項羽本紀》][7] | [JSON](1sd_oek_swt.json) |
| `1sp_iuz_5xh` | 周殷 | [《史記・黥布列傳》][73] | [JSON](1sp_iuz_5xh.json) |
| `1t2_224_c5d` | 蓋公 | [《史記・樂毅列傳》][62] | [JSON](1t2_224_c5d.json) |
| `1tl_xlo_url` | 楚宣（列國君主） | [《史記・秦本紀》][5] | [JSON](1tl_xlo_url.json) |
| `1tp_unw_nod` | 鉅鹿趙王 | [《史記・白起王翦列傳》][55] | [JSON](1tp_unw_nod.json) |
| `1tz_1iv_r3r` | 太尉勃未詳姓 | [《史記・傅靳蒯成列傳》][80] | [JSON](1tz_1iv_r3r.json) |
| `1u0_up8_swa` | 茀（主屨者） | [《史記・齊太公世家》][14] | [JSON](1u0_up8_swa.json) |
| `1u5_bgn_fp2` | 司馬尚 | [《史記・廉頗藺相如列傳》][63] | [JSON](1u5_bgn_fp2.json) |
| `1u7_dot_pe3` | 惠文后 | [《史記・穰侯列傳》][54] | [JSON](1u7_dot_pe3.json) |
| `1ub_pb8_7fr` | 太史公 | [《史記・仲尼弟子列傳》][49] | [JSON](1ub_pb8_7fr.json) |
| `1ul_a2h_xbc` | 晉獻公 | [《史記・魏世家》][26] | [JSON](1ul_a2h_xbc.json) |
| `1uq_93c_cmo` | 柳（晉幽公） | [《史記・晉世家》][21] | [JSON](1uq_93c_cmo.json) |
| `1uq_j2z_9xd` | 東郭女（崔杼所取） | [《史記・齊太公世家》][14] | [JSON](1uq_j2z_9xd.json) |
| `1vh_24w_d7w` | 鞠武 | [《史記・刺客列傳》][68] | [JSON](1vh_24w_d7w.json) |
| `1vr_rmi_ay7` | 蓋餘 | [《史記・刺客列傳》][68] | [JSON](1vr_rmi_ay7.json) |
| `1wa_qpl_7iq` | 安國君 | [《史記・秦本紀》][5] | [JSON](1wa_qpl_7iq.json) |
| `1wk_2dd_421` | 灌嬰 | [《史記・田儋列傳》][76] | [JSON](1wk_2dd_421.json) |
| `1wp_coh_osw` | 去疾（晉頃公） | [《史記・晉世家》][21] | [JSON](1wp_coh_osw.json) |
| `1wq_ksz_p4p` | 莊襄王 | [《史記・陳涉世家》][30] | [JSON](1wq_ksz_p4p.json) |
| `1wy_ygt_gre` | 薛公未詳名 | [《史記・樊酈滕灌列傳》][77] | [JSON](1wy_ygt_gre.json) |
| `1x1_4h8_ibu` | 虎圈嗇夫未名 | [《史記・張釋之馮唐列傳》][84] | [JSON](1x1_4h8_ibu.json) |
| `1xd_b3z_bfz` | 伯臩 | [《史記・周本紀》][4] | [JSON](1xd_b3z_bfz.json) |
| `1xg_tyg_l9z` | 劉禮 | [《史記・孝文本紀》][10] | [JSON](1xg_tyg_l9z.json) |
| `1xp_n08_qzo` | 振（商先祖） | [《史記・殷本紀》][3] | [JSON](1xp_n08_qzo.json) |
| `1xx_s1v_svn` | 陳豨 | [《史記・韓信盧綰列傳》][75] | [JSON](1xx_s1v_svn.json) |
| `1ym_x9f_a12` | 思王 | [《史記・周本紀》][4] | [JSON](1ym_x9f_a12.json) |
| `1z3_l69_xi9` | 子罕引古 | [《史記・李斯列傳》][69] | [JSON](1z3_l69_xi9.json) |
| `1zm_8zk_4hh` | 非子 | [《史記・秦本紀》][5] | [JSON](1zm_8zk_4hh.json) |
| `1zr_pe3_6jo` | 親弗 | [《史記・孟嘗君列傳》][57] | [JSON](1zr_pe3_6jo.json) |
| `20a_y6s_j9g` | 章邯 | [《史記・絳侯周勃世家》][39] | [JSON](20a_y6s_j9g.json) |
| `20h_8e9_zop` | 宣太后 | [《史記・范睢蔡澤列傳》][61] | [JSON](20h_8e9_zop.json) |
| `21a_kok_ndw` | 虢君未名 | [《史記・扁鵲倉公列傳》][87] | [JSON](21a_kok_ndw.json) |
| `21i_ev7_c9u` | 武臣 | [《史記・張耳陳餘列傳》][71] | [JSON](21i_ev7_c9u.json) |
| `220_2hx_s8j` | 蔡侯（楚靈王醉殺者未名） | [《史記・楚世家》][22] | [JSON](220_2hx_s8j.json) |
| `22o_cth_7hm` | 淳于髡 | [《史記・孟子荀卿列傳》][56] | [JSON](22o_cth_7hm.json) |
| `237_cbp_w2w` | 趙公子嘉 | [《史記・秦始皇本紀》][6] | [JSON](237_cbp_w2w.json) |
| `23k_ck2_otm` | 公子郢 | [《史記・仲尼弟子列傳》][49] | [JSON](23k_ck2_otm.json) |
| `23r_tex_w2g` | 林父（衛孫文子） | [《史記・衛康叔世家》][19] | [JSON](23r_tex_w2g.json) |
| `23s_dd0_gbc` | 百里奚引古 | [《史記・魯仲連鄒陽列傳》][65] | [JSON](23s_dd0_gbc.json) |
| `23z_9xy_hzo` | 鐘離眛 | [《史記・淮陰侯列傳》][74] | [JSON](23z_9xy_hzo.json) |
| `242_htg_awo` | 太子（宋御所殺者未名） | [《史記・宋微子世家》][20] | [JSON](242_htg_awo.json) |
| `243_u8f_u71` | 潁川守尊 | [《史記・孝文本紀》][10] | [JSON](243_u8f_u71.json) |
| `24e_as3_xfw` | 子罕引古 | [《史記・魯仲連鄒陽列傳》][65] | [JSON](24e_as3_xfw.json) |
| `250_q6f_brq` | 伯禽 | [《史記・魯周公世家》][15] | [JSON](250_q6f_brq.json) |
| `253_2n7_qs7` | 皇后未名（文帝） | [《史記・袁盎鼂錯列傳》][83] | [JSON](253_2n7_qs7.json) |
| `25f_g5k_wae` | 高肆 | [《史記・絳侯周勃世家》][39] | [JSON](25f_g5k_wae.json) |
| `25o_mn8_27w` | 衛少兒 | [《史記・外戚世家》][31] | [JSON](25o_mn8_27w.json) |
| `261_d2j_rm9` | 任王后 | [《史記・梁孝王世家》][40] | [JSON](261_d2j_rm9.json) |
| `26f_e5j_68s` | 堯（孔子世家形貌比擬傳說） | [《史記・孔子世家》][29] | [JSON](26f_e5j_68s.json) |
| `26q_bpg_wb6` | 田常母（田世家祭辭未名者） | [《史記・田敬仲完世家》][28] | [JSON](26q_bpg_wb6.json) |
| `26r_t32_9rn` | 卜子夏 | [《史記・魏世家》][26] | [JSON](26r_t32_9rn.json) |
| `26s_7sw_89e` | 臧文仲（魯弔宋水者） | [《史記・宋微子世家》][20] | [JSON](26s_7sw_89e.json) |
| `275_ump_um1` | 趙怱 | [《史記・趙世家》][25]、[《史記・廉頗藺相如列傳》][63] | [JSON](275_ump_um1.json) |
| `279_znq_bwx` | 荊軻 | [《史記・魏世家》][26] | [JSON](279_znq_bwx.json) |
| `27q_nw7_jv8` | 田閒 | [《史記・田儋列傳》][76] | [JSON](27q_nw7_jv8.json) |
| `27r_a47_f8b` | 陳勝 | [《史記・魏豹彭越列傳》][72] | [JSON](27r_a47_f8b.json) |
| `27v_an7_gp2` | 庶長章 | [《史記・秦本紀》][5] | [JSON](27v_an7_gp2.json) |
| `27w_87k_66k` | 彭越 | [《史記・田儋列傳》][76] | [JSON](27w_87k_66k.json) |
| `282_wxp_l9r` | 周公 | [《史記・劉敬叔孫通列傳》][81] | [JSON](282_wxp_l9r.json) |
| `28d_4fi_xdp` | 代王孝文帝 | [《史記・齊悼惠王世家》][34] | [JSON](28d_4fi_xdp.json) |
| `28h_ams_w0k` | 呂望 | [《史記・白起王翦列傳》][55] | [JSON](28h_ams_w0k.json) |
| `28u_l10_cos` | 甯越 | [《史記・陳涉世家》][30] | [JSON](28u_l10_cos.json) |
| `29i_iqg_x15` | 段干朋 | [《史記・田敬仲完世家》][28] | [JSON](29i_iqg_x15.json) |
| `29j_y7o_2cf` | 張敖 | [《史記・張耳陳餘列傳》][71] | [JSON](29j_y7o_2cf.json) |
| `29l_qoo_n4x` | 彭越 | [《史記・荊燕世家》][33] | [JSON](29l_qoo_n4x.json) |
| `29w_q1t_l0v` | 姬姚 | [《史記・周本紀》][4] | [JSON](29w_q1t_l0v.json) |
| `2ae_mb5_3t2` | 楊熊 | [《史記・留侯世家》][37] | [JSON](2ae_mb5_3t2.json) |
| `2ah_uo6_lge` | 侯公（漢使） | [《史記・項羽本紀》][7] | [JSON](2ah_uo6_lge.json) |
| `2ai_498_crf` | 秦二世 | [《史記・白起王翦列傳》][55] | [JSON](2ai_498_crf.json) |
| `2aw_0yj_oei` | 衛伯（宋攻昭公者） | [《史記・宋微子世家》][20] | [JSON](2aw_0yj_oei.json) |
| `2b1_faa_7h8` | 尹喜 | [《史記・老子韓非列傳》][45] | [JSON](2b1_faa_7h8.json) |
| `2b9_5sw_foy` | 稱（顓頊子楚篇祖系） | [《史記・楚世家》][22] | [JSON](2b9_5sw_foy.json) |
| `2bk_fz6_icl` | 白起 | [《史記・白起王翦列傳》][55] | [JSON](2bk_fz6_icl.json) |
| `2bl_b4d_kfg` | 公孫詭 | [《史記・梁孝王世家》][40] | [JSON](2bl_b4d_kfg.json) |
| `2bq_vfh_tem` | 鮑牧 | [《史記・齊太公世家》][14] | [JSON](2bq_vfh_tem.json) |
| `2bw_ckk_9u2` | 冉有（季氏用者） | [《史記・魯周公世家》][15] | [JSON](2bw_ckk_9u2.json) |
| `2c8_uuj_bc8` | 巫馬施 | [《史記・仲尼弟子列傳》][49] | [JSON](2c8_uuj_bc8.json) |
| `2c9_tl4_1sc` | 太尉勃 | [《史記・齊悼惠王世家》][34] | [JSON](2c9_tl4_1sc.json) |
| `2cg_r5b_krs` | 太子未名（元狩元年立） | [《史記・萬石張叔列傳》][85] | [JSON](2cg_r5b_krs.json) |
| `2cx_p6z_4uc` | 周繆王 | [《史記・趙世家》][25] | [JSON](2cx_p6z_4uc.json) |
| `2d1_ymx_i2x` | 武公（燕昭公後） | [《史記・燕召公世家》][16] | [JSON](2d1_ymx_i2x.json) |
| `2dw_3cl_e1j` | 解揚（紿救宋者） | [《史記・晉世家》][21] | [JSON](2dw_3cl_e1j.json) |
| `2ed_ew8_szv` | 太史公 | [《史記・張丞相列傳》][78] | [JSON](2ed_ew8_szv.json) |
| `2ek_pbu_zht` | 魏昭王 | [《史記・孟嘗君列傳》][57] | [JSON](2ek_pbu_zht.json) |
| `2em_jud_jao` | 趙王張儀說趙 | [《史記・張儀列傳》][52] | [JSON](2em_jud_jao.json) |
| `2en_16a_r4i` | 虞君（獻公時） | [《史記・秦本紀》][5] | [JSON](2en_16a_r4i.json) |
| `2eo_3mk_s7c` | 長沮 | [《史記・仲尼弟子列傳》][49] | [JSON](2eo_3mk_s7c.json) |
| `2ev_182_3gg` | 冒頓 | [《史記・韓信盧綰列傳》][75] | [JSON](2ev_182_3gg.json) |
| `2fo_m4u_tux` | 芒卯 | [《史記・穰侯列傳》][54] | [JSON](2fo_m4u_tux.json) |
| `2gj_2vz_ekz` | 子餘（楚篇晉文公腹心） | [《史記・楚世家》][22] | [JSON](2gj_2vz_ekz.json) |
| `2ih_dpv_yf7` | 蘇代 | [《史記・孟嘗君列傳》][57] | [JSON](2ih_dpv_yf7.json) |
| `2ii_p53_1ov` | 檀子 | [《史記・田敬仲完世家》][28] | [JSON](2ii_p53_1ov.json) |
| `2ip_ioo_pf7` | 鄒衍 | [《史記・孟子荀卿列傳》][56] | [JSON](2ip_ioo_pf7.json) |
| `2j3_uzv_a2x` | 呂忿 | [《史記・呂太后本紀》][9] | [JSON](2j3_uzv_a2x.json) |
| `2j4_zl6_6ms` | 鐘離生 | [《史記・外戚世家》][31] | [JSON](2j4_zl6_6ms.json) |
| `2j9_c6k_fjs` | 章邯 | [《史記・項羽本紀》][7] | [JSON](2j9_c6k_fjs.json) |
| `2jb_t1c_fpa` | 申 | [《史記・魏世家》][26] | [JSON](2jb_t1c_fpa.json) |
| `2jn_tjp_75n` | 周仁 | [《史記・萬石張叔列傳》][85] | [JSON](2jn_tjp_75n.json) |
| `2jv_fri_ifh` | 萇弘（周臣） | [《史記・管蔡世家》][17] | [JSON](2jv_fri_ifh.json) |
| `2k3_1v0_aqi` | 程縱 | [《史記・樊酈滕灌列傳》][77] | [JSON](2k3_1v0_aqi.json) |
| `2kq_bij_vxi` | 邢夫人 | [《史記・外戚世家》][31] | [JSON](2kq_bij_vxi.json) |
| `2kq_omm_diy` | 冒頓 | [《史記・樊酈滕灌列傳》][77] | [JSON](2kq_omm_diy.json) |
| `2lu_xqb_9gv` | 范皋繹 | [《史記・趙世家》][25] | [JSON](2lu_xqb_9gv.json) |
| `2m1_6jd_hdo` | 專諸 | [《史記・吳太伯世家》][13] | [JSON](2m1_6jd_hdo.json) |
| `2m6_2n1_s07` | 湯引古 | [《史記・孟子荀卿列傳》][56] | [JSON](2m6_2n1_s07.json) |
| `2mo_u4v_gii` | 周公（季札論樂稱） | [《史記・吳太伯世家》][13] | [JSON](2mo_u4v_gii.json) |
| `2mw_zet_vw9` | 將廬（齊王） | [《史記・孝景本紀》][11] | [JSON](2mw_zet_vw9.json) |
| `2ne_w1o_8cu` | 威累（卷末世系） | [《史記・秦始皇本紀》][6] | [JSON](2ne_w1o_8cu.json) |
| `2nk_7we_scq` | 馮亭 | [《史記・趙世家》][25] | [JSON](2nk_7we_scq.json) |
| `2nr_puu_sui` | 申叔時（楚莊王使者） | [《史記・陳杞世家》][18]、[《史記・楚世家》][22] | [JSON](2nr_puu_sui.json) |
| `2nw_f4l_qld` | 般妻（楚婦未名） | [《史記・管蔡世家》][17] | [JSON](2nw_f4l_qld.json) |
| `2oj_wrn_skl` | 褒姒 | [《史記・外戚世家》][31] | [JSON](2oj_wrn_skl.json) |
| `2ps_i8p_n0m` | 孟嘗 | [《史記・陳涉世家》][30] | [JSON](2ps_i8p_n0m.json) |
| `2ps_uom_6ah` | 華督（楚篇宋太宰） | [《史記・楚世家》][22] | [JSON](2ps_uom_6ah.json) |
| `2pv_dtb_lrw` | 魏章 | [《史記・樗里子甘茂列傳》][53] | [JSON](2pv_dtb_lrw.json) |
| `2qe_ml9_mta` | 田需 | [《史記・魏世家》][26] | [JSON](2qe_ml9_mta.json) |
| `2qj_hw4_si9` | 太甲 | [《史記・殷本紀》][3] | [JSON](2qj_hw4_si9.json) |
| `2qq_5wq_wzo` | 灌將軍 | [《史記・荊燕世家》][33] | [JSON](2qq_5wq_wzo.json) |
| `2qv_1rq_zp0` | 樂乘 | [《史記・樂毅列傳》][62] | [JSON](2qv_1rq_zp0.json) |
| `2r3_3yo_3sa` | 樊於期引古 | [《史記・刺客列傳》][68] | [JSON](2r3_3yo_3sa.json) |
| `2rc_bl1_v99` | 齊丞相舍人未名 | [《史記・扁鵲倉公列傳》][87] | [JSON](2rc_bl1_v99.json) |
| `2rj_hat_gfq` | 顏幸 | [《史記・仲尼弟子列傳》][49] | [JSON](2rj_hat_gfq.json) |
| `2rk_my8_sbg` | 栗腹 | [《史記・魯仲連鄒陽列傳》][65] | [JSON](2rk_my8_sbg.json) |
| `2rm_drg_ym7` | 柴將軍 | [《史記・齊悼惠王世家》][34] | [JSON](2rm_drg_ym7.json) |
| `2rz_j0z_ij3` | 澠池趙禦史未名 | [《史記・廉頗藺相如列傳》][63] | [JSON](2rz_j0z_ij3.json) |
| `2sg_8ra_hq5` | 田廣 | [《史記・酈生陸賈列傳》][79] | [JSON](2sg_8ra_hq5.json) |
| `2sz_e8r_hih` | 韓襄哀王 | [《史記・留侯世家》][37] | [JSON](2sz_e8r_hih.json) |
| `2t1_1bj_ewv` | 貫高 | [《史記・張耳陳餘列傳》][71] | [JSON](2t1_1bj_ewv.json) |
| `2t5_tp3_6ti` | 燕王 | [《史記・齊悼惠王世家》][34] | [JSON](2t5_tp3_6ti.json) |
| `2to_ofg_fuz` | 顓頊 | [《史記・五帝本紀》][1] | [JSON](2to_ofg_fuz.json) |
| `2u6_7bk_902` | 漢惠帝 | [《史記・樊酈滕灌列傳》][77] | [JSON](2u6_7bk_902.json) |
| `2ui_e50_uz6` | 燕昭王 | [《史記・樂毅列傳》][62] | [JSON](2ui_e50_uz6.json) |
| `2uk_ay7_hjf` | 竇嬰 | [《史記・袁盎鼂錯列傳》][83] | [JSON](2uk_ay7_hjf.json) |
| `2uk_lgn_scq` | 審食其 | [《史記・陳丞相世家》][38] | [JSON](2uk_lgn_scq.json) |
| `2ul_m9b_m11` | 周夷王 | [《史記・楚世家》][22] | [JSON](2ul_m9b_m11.json) |
| `2vc_12q_w0e` | 叔姜（哀姜娣） | [《史記・魯周公世家》][15] | [JSON](2vc_12q_w0e.json) |
| `2vi_3p8_mar` | 太史公 | [《史記・袁盎鼂錯列傳》][83] | [JSON](2vi_3p8_mar.json) |
| `2vz_w08_06z` | 子家（魯昭公隨臣） | [《史記・魯周公世家》][15] | [JSON](2vz_w08_06z.json) |
| `2wb_n1j_m5a` | 趙朔妻（趙世家晉成公姊未名者） | [《史記・趙世家》][25] | [JSON](2wb_n1j_m5a.json) |
| `2wl_dla_w69` | 王齮 | [《史記・秦始皇本紀》][6] | [JSON](2wl_dla_w69.json) |
| `2wp_usr_ncd` | 衛鞅 | [《史記・商君列傳》][50] | [JSON](2wp_usr_ncd.json) |
| `2wt_drt_ii8` | 王夫人子齊王 | [《史記・外戚世家》][31] | [JSON](2wt_drt_ii8.json) |
| `2ww_4rg_iv9` | 應高 | [《史記・吳王濞列傳》][88] | [JSON](2ww_4rg_iv9.json) |
| `2xk_syj_egr` | 陳勝 | [《史記・黥布列傳》][73] | [JSON](2xk_syj_egr.json) |
| `2z1_3uv_8xx` | 春申君 | [《史記・春申君列傳》][60] | [JSON](2z1_3uv_8xx.json) |
| `307_auq_l0i` | 太史公 | [《史記・楚元王世家》][32] | [JSON](307_auq_l0i.json) |
| `30y_9u3_v0b` | 陳豨 | [《史記・曹相國世家》][36] | [JSON](30y_9u3_v0b.json) |
| `31b_36a_313` | 辟陽侯未具名 | [《史記・袁盎鼂錯列傳》][83] | [JSON](31b_36a_313.json) |
| `31r_axc_fmj` | 公孫衍（楚篇合秦議者） | [《史記・楚世家》][22] | [JSON](31r_axc_fmj.json) |
| `31y_gr6_mkf` | 薛公（楚將） | [《史記・項羽本紀》][7]、[《史記・高祖本紀》][8] | [JSON](31y_gr6_mkf.json) |
| `325_xsc_kdn` | 予（夏王） | [《史記・夏本紀》][2] | [JSON](325_xsc_kdn.json) |
| `32l_gy6_4fi` | 趙奢 | [《史記・秦始皇本紀》][6] | [JSON](32l_gy6_4fi.json) |
| `32m_9wz_1y5` | 會稽守通 | [《史記・項羽本紀》][7] | [JSON](32m_9wz_1y5.json) |
| `32w_2ob_y8q` | 句井疆 | [《史記・仲尼弟子列傳》][49] | [JSON](32w_2ob_y8q.json) |
| `335_2xl_tn8` | 秦皇帝引古 | [《史記・魯仲連鄒陽列傳》][65] | [JSON](335_2xl_tn8.json) |
| `335_flt_fs5` | 傳舍長未名 | [《史記・孟嘗君列傳》][57] | [JSON](335_flt_fs5.json) |
| `339_a7b_n8d` | 周天子（孔子世家踐土未名者） | [《史記・孔子世家》][29] | [JSON](339_a7b_n8d.json) |
| `33c_qfa_gcj` | 壺黶 | [《史記・仲尼弟子列傳》][49] | [JSON](33c_qfa_gcj.json) |
| `33g_ue6_pz0` | 蕭何 | [《史記・淮陰侯列傳》][74] | [JSON](33g_ue6_pz0.json) |
| `33j_itf_q0q` | 蔡昭公 | [《史記・孔子世家》][29] | [JSON](33j_itf_q0q.json) |
| `33k_p1u_8v9` | 趙王遷 | [《史記・趙世家》][25] | [JSON](33k_p1u_8v9.json) |
| `33t_2vr_k9o` | 牟辛 | [《史記・田敬仲完世家》][28] | [JSON](33t_2vr_k9o.json) |
| `33z_av8_anq` | 鄭弘 | [《史記・張丞相列傳》][78] | [JSON](33z_av8_anq.json) |
| `349_zmu_2u4` | 曹參 | [《史記・田儋列傳》][76] | [JSON](349_zmu_2u4.json) |
| `34q_hne_erk` | 田甲 | [《史記・孟嘗君列傳》][57] | [JSON](34q_hne_erk.json) |
| `34u_t1e_mvb` | 子産（鄭執政） | [《史記・吳太伯世家》][13] | [JSON](34u_t1e_mvb.json) |
| `356_1uv_7i4` | 越女（楚莊王所抱者） | [《史記・楚世家》][22] | [JSON](356_1uv_7i4.json) |
| `35b_1t3_p8s` | 犁鉏 | [《史記・齊太公世家》][14] | [JSON](35b_1t3_p8s.json) |
| `35t_t2n_iyq` | 敬嬴（文公次妃） | [《史記・魯周公世家》][15] | [JSON](35t_t2n_iyq.json) |
| `362_ss6_ac0` | 陳餘 | [《史記・張耳陳餘列傳》][71] | [JSON](362_ss6_ac0.json) |
| `363_21i_84z` | 畔 | [《史記・陳涉世家》][30] | [JSON](363_21i_84z.json) |
| `364_wrf_g4o` | 牛翦 | [《史記・趙世家》][25] | [JSON](364_wrf_g4o.json) |
| `36s_ym3_fp3` | 魯公子翚 | [《史記・秦本紀》][5] | [JSON](36s_ym3_fp3.json) |
| `36t_qh2_t5n` | 吳起引古 | [《史記・范睢蔡澤列傳》][61] | [JSON](36t_qh2_t5n.json) |
| `370_sgw_aye` | 魏惠王 | [《史記・商君列傳》][50] | [JSON](370_sgw_aye.json) |
| `377_emg_150` | 曾參 | [《史記・張儀列傳》][52] | [JSON](377_emg_150.json) |
| `37f_nn3_ssi` | 田常 | [《史記・齊太公世家》][14] | [JSON](37f_nn3_ssi.json) |
| `37j_16p_7n8` | 曹參 | [《史記・曹相國世家》][36] | [JSON](37j_16p_7n8.json) |
| `37m_d72_3mo` | 駘 | [《史記・鄭世家》][24] | [JSON](37m_d72_3mo.json) |
| `37x_h50_3ls` | 如意（趙王） | [《史記・樊酈滕灌列傳》][77] | [JSON](37x_h50_3ls.json) |
| `388_k2s_lyw` | 仲伯 | [《史記・殷本紀》][3] | [JSON](388_k2s_lyw.json) |
| `38a_7fk_ezx` | 公仲侈 | [《史記・樗里子甘茂列傳》][53] | [JSON](38a_7fk_ezx.json) |
| `38g_ysr_j1n` | 乙 | [《史記・鄭世家》][24] | [JSON](38g_ysr_j1n.json) |
| `396_7d9_rpc` | 晉景公 | [《史記・趙世家》][25] | [JSON](396_7d9_rpc.json) |
| `396_zge_56w` | 申句須 | [《史記・孔子世家》][29] | [JSON](396_zge_56w.json) |
| `398_14a_ml2` | 周蘭 | [《史記・傅靳蒯成列傳》][80] | [JSON](398_14a_ml2.json) |
| `39e_wj9_6m0` | 韓王信 | [《史記・樊酈滕灌列傳》][77] | [JSON](39e_wj9_6m0.json) |
| `3a7_boe_phl` | 主壬 | [《史記・殷本紀》][3] | [JSON](3a7_boe_phl.json) |
| `3a9_w7x_73x` | 楚莊王 | [《史記・楚世家》][22] | [JSON](3a9_w7x_73x.json) |
| `3av_pp6_8bu` | 他姬子燕王 | [《史記・外戚世家》][31] | [JSON](3av_pp6_8bu.json) |
| `3bl_wnq_da6` | 魏王圍蒲陽 | [《史記・張儀列傳》][52] | [JSON](3bl_wnq_da6.json) |
| `3ca_ch7_nw1` | 趙成 | [《史記・秦始皇本紀》][6] | [JSON](3ca_ch7_nw1.json) |
| `3co_cqa_4uq` | 微子啓之母 | [《史記・殷本紀》][3] | [JSON](3co_cqa_4uq.json) |
| `3ct_ifg_ey2` | 韓信舍人弟未名 | [《史記・淮陰侯列傳》][74] | [JSON](3ct_ifg_ey2.json) |
| `3d1_2fa_7bd` | 蘇秦謀齊燕王 | [《史記・張儀列傳》][52] | [JSON](3d1_2fa_7bd.json) |
| `3d1_wjo_6ov` | 狐季姬（楚篇晉文公母） | [《史記・楚世家》][22] | [JSON](3d1_wjo_6ov.json) |
| `3do_pdw_2wm` | 韓舉 | [《史記・趙世家》][25] | [JSON](3do_pdw_2wm.json) |
| `3ef_1ha_zmh` | 吳王夫差 | [《史記・仲尼弟子列傳》][49] | [JSON](3ef_1ha_zmh.json) |
| `3eg_t7p_ay0` | 主腐者吏未名 | [《史記・呂不韋列傳》][67] | [JSON](3eg_t7p_ay0.json) |
| `3eo_u7e_pxx` | 王夫人 | [《史記・三王世家》][42] | [JSON](3eo_u7e_pxx.json) |
| `3f0_m1h_7ah` | 鄭厲公 | [《史記・周本紀》][4] | [JSON](3f0_m1h_7ah.json) |
| `3f9_kxm_8rv` | 呂不韋 | [《史記・呂不韋列傳》][67] | [JSON](3f9_kxm_8rv.json) |
| `3fo_o8y_1nx` | 王離 | [《史記・張耳陳餘列傳》][71] | [JSON](3fo_o8y_1nx.json) |
| `3gd_6f0_cnf` | 秦信 | [《史記・扁鵲倉公列傳》][87] | [JSON](3gd_6f0_cnf.json) |
| `3gd_w8i_skr` | 申侯（孝王時） | [《史記・秦本紀》][5] | [JSON](3gd_w8i_skr.json) |
| `3gm_vdd_51h` | 呂祿女 | [《史記・外戚世家》][31] | [JSON](3gm_vdd_51h.json) |
| `3go_52y_0mp` | 伯樂引古 | [《史記・屈原賈生列傳》][66] | [JSON](3go_52y_0mp.json) |
| `3hy_4xq_wqu` | 定王（瑜） | [《史記・周本紀》][4] | [JSON](3hy_4xq_wqu.json) |
| `3i8_q7r_0px` | 趙王遷（燕王喜記事） | [《史記・燕召公世家》][16] | [JSON](3i8_q7r_0px.json) |
| `3i9_kae_h9x` | 樂池 | [《史記・趙世家》][25] | [JSON](3i9_kae_h9x.json) |
| `3id_eoz_71f` | 夏姬（御叔妻） | [《史記・陳杞世家》][18] | [JSON](3id_eoz_71f.json) |
| `3ig_qln_usl` | 伍子胥引古 | [《史記・李斯列傳》][69] | [JSON](3ig_qln_usl.json) |
| `3il_71l_avp` | 田嬰 | [《史記・楚世家》][22] | [JSON](3il_71l_avp.json) |
| `3il_m0o_93j` | 邑姜 | [《史記・鄭世家》][24] | [JSON](3il_m0o_93j.json) |
| `3ix_k6j_eea` | 灌將軍 | [《史記・外戚世家》][31] | [JSON](3ix_k6j_eea.json) |
| `3j2_4x7_nzr` | 董翳 | [《史記・項羽本紀》][7] | [JSON](3j2_4x7_nzr.json) |
| `3ja_mh8_wrw` | 楊熊 | [《史記・曹相國世家》][36] | [JSON](3ja_mh8_wrw.json) |
| `3jf_ru8_mz9` | 孫臏 | [《史記・孫子吳起列傳》][47] | [JSON](3jf_ru8_mz9.json) |
| `3jf_y3v_rq2` | 楚王合從未名 | [《史記・平原君虞卿列傳》][58] | [JSON](3jf_y3v_rq2.json) |
| `3jk_04c_cyw` | 侯敞 | [《史記・韓信盧綰列傳》][75] | [JSON](3jk_04c_cyw.json) |
| `3jt_de3_wuf` | 懿王 | [《史記・周本紀》][4] | [JSON](3jt_de3_wuf.json) |
| `3jv_9t6_3tk` | 譚伯 | [《史記・周本紀》][4] | [JSON](3jv_9t6_3tk.json) |
| `3ki_pir_nb6` | 師襄子 | [《史記・孔子世家》][29] | [JSON](3ki_pir_nb6.json) |
| `3l2_mmn_rps` | 孔成子（解康叔夢者） | [《史記・衛康叔世家》][19] | [JSON](3l2_mmn_rps.json) |
| `3la_fcr_q0l` | 武涉 | [《史記・項羽本紀》][7]、[《史記・高祖本紀》][8] | [JSON](3la_fcr_q0l.json) |
| `3lq_bkx_u08` | 易牙 | [《史記・齊太公世家》][14] | [JSON](3lq_bkx_u08.json) |
| `3lq_wm9_1ov` | 田子方 | [《史記・魏世家》][26] | [JSON](3lq_wm9_1ov.json) |
| `3lw_vex_s0b` | 長沙哀王 | [《史記・黥布列傳》][73] | [JSON](3lw_vex_s0b.json) |
| `3lx_052_bv0` | 秦王反間未名 | [《史記・魏公子列傳》][59] | [JSON](3lx_052_bv0.json) |
| `3m0_o0z_l0l` | 盧綰 | [《史記・荊燕世家》][33] | [JSON](3m0_o0z_l0l.json) |
| `3mb_c4b_fqg` | 季康子 | [《史記・仲尼弟子列傳》][49] | [JSON](3mb_c4b_fqg.json) |
| `3ml_cbm_uoq` | 晉頃公 | [《史記・魏世家》][26] | [JSON](3ml_cbm_uoq.json) |
| `3mo_tz2_5vi` | 宛春（楚子玉使者） | [《史記・晉世家》][21] | [JSON](3mo_tz2_5vi.json) |
| `3n3_u3h_uie` | 宋宣公 | [《史記・梁孝王世家》][40] | [JSON](3n3_u3h_uie.json) |
| `3nq_r49_oo5` | 吁子 | [《史記・孟子荀卿列傳》][56] | [JSON](3nq_r49_oo5.json) |
| `3nz_bcz_xq7` | 項梁 | [《史記・留侯世家》][37] | [JSON](3nz_bcz_xq7.json) |
| `3o1_9dz_em1` | 仲（張釋之兄） | [《史記・張釋之馮唐列傳》][84] | [JSON](3o1_9dz_em1.json) |
| `3oj_19k_zvz` | 魯僖公（楚篇請兵者） | [《史記・楚世家》][22] | [JSON](3oj_19k_zvz.json) |
| `3p2_0dm_6ra` | 劉舍 | [《史記・孝景本紀》][11] | [JSON](3p2_0dm_6ra.json) |
| `3p4_wjn_b2w` | 杜摯 | [《史記・秦本紀》][5]、[《史記・商君列傳》][50] | [JSON](3p4_wjn_b2w.json) |
| `3p9_gxf_c4f` | 王喜 | [《史記・韓信盧綰列傳》][75] | [JSON](3p9_gxf_c4f.json) |
| `3pd_gkb_bof` | 嘉（景帝初丞相稱） | [《史記・孝文本紀》][10] | [JSON](3pd_gkb_bof.json) |
| `3po_rdb_3hc` | 盜蹠 | [《史記・伯夷列傳》][43] | [JSON](3po_rdb_3hc.json) |
| `3q1_bhh_ppr` | 奚斯（魯大夫） | [《史記・魯周公世家》][15] | [JSON](3q1_bhh_ppr.json) |
| `3qd_6c7_i1s` | 呂后舍人未名 | [《史記・魏豹彭越列傳》][72] | [JSON](3qd_6c7_i1s.json) |
| `3qe_csy_8ad` | 邢說 | [《史記・傅靳蒯成列傳》][80] | [JSON](3qe_csy_8ad.json) |
| `3ql_hwu_hx5` | 齊使者（越世家攻楚勸說未名者） | [《史記・越王勾踐世家》][23] | [JSON](3ql_hwu_hx5.json) |
| `3ra_r7y_zcd` | 酈商 | [《史記・樊酈滕灌列傳》][77] | [JSON](3ra_r7y_zcd.json) |
| `3rf_eo0_kf0` | 圯上老父 | [《史記・留侯世家》][37] | [JSON](3rf_eo0_kf0.json) |
| `3rj_an2_t19` | 伯宗（晉諫臣） | [《史記・晉世家》][21] | [JSON](3rj_an2_t19.json) |
| `3rk_5as_4o8` | 灌嬰 | [《史記・樊酈滕灌列傳》][77] | [JSON](3rk_5as_4o8.json) |
| `3rp_q9b_xr8` | 魏王（田世家煮棗議論未名者） | [《史記・田敬仲完世家》][28] | [JSON](3rp_q9b_xr8.json) |
| `3ru_k83_cb9` | 小白母（衛女未名） | [《史記・齊太公世家》][14]、[《史記・楚世家》][22] | [JSON](3ru_k83_cb9.json) |
| `3s4_d8d_8v7` | 孝王 | [《史記・秦本紀》][5] | [JSON](3s4_d8d_8v7.json) |
| `3sc_20t_48d` | 史墨 | [《史記・魯周公世家》][15] | [JSON](3sc_20t_48d.json) |
| `3sg_3tv_dpq` | 黃帝引古 | [《史記・樂毅列傳》][62] | [JSON](3sg_3tv_dpq.json) |
| `3sg_fes_hit` | 項籍 | [《史記・荊燕世家》][33] | [JSON](3sg_fes_hit.json) |
| `3si_5fm_wfy` | 呂產 | [《史記・呂太后本紀》][9] | [JSON](3si_5fm_wfy.json) |
| `3sp_xmg_o87` | 張武 | [《史記・孝文本紀》][10] | [JSON](3sp_xmg_o87.json) |
| `3sy_jfh_khw` | 躄者未名 | [《史記・平原君虞卿列傳》][58] | [JSON](3sy_jfh_khw.json) |
| `3sz_fvq_k6r` | 邊伯 | [《史記・周本紀》][4] | [JSON](3sz_fvq_k6r.json) |
| `3t5_k5f_n2u` | 申生引古 | [《史記・范睢蔡澤列傳》][61] | [JSON](3t5_k5f_n2u.json) |
| `3th_8ky_c6y` | 昌僕 | [《史記・五帝本紀》][1] | [JSON](3th_8ky_c6y.json) |
| `3ti_3ui_sdb` | 杜赫 | [《史記・秦始皇本紀》][6] | [JSON](3ti_3ui_sdb.json) |
| `3tp_ab0_hlx` | 竇廣國 | [《史記・外戚世家》][31] | [JSON](3tp_ab0_hlx.json) |
| `3ts_h1q_wbo` | 顏聚 | [《史記・趙世家》][25]、[《史記・廉頗藺相如列傳》][63] | [JSON](3ts_h1q_wbo.json) |
| `3tw_nq2_gyn` | 霍去病 | [《史記・外戚世家》][31] | [JSON](3tw_nq2_gyn.json) |
| `3ty_cnm_mh5` | 上林行人未名 | [《史記・李斯列傳》][69] | [JSON](3ty_cnm_mh5.json) |
| `3u1_ov8_6ry` | 公子范 | [《史記・趙世家》][25] | [JSON](3u1_ov8_6ry.json) |
| `3u2_btf_ob4` | 周舍 | [《史記・孝文本紀》][10] | [JSON](3u2_btf_ob4.json) |
| `3u4_2bl_u1l` | 公祖句茲 | [《史記・仲尼弟子列傳》][49] | [JSON](3u4_2bl_u1l.json) |
| `3un_4f9_e3v` | 菑川王美人未名 | [《史記・扁鵲倉公列傳》][87] | [JSON](3un_4f9_e3v.json) |
| `3ut_yhd_f9d` | 公孫慶 | [《史記・陳涉世家》][30] | [JSON](3ut_yhd_f9d.json) |
| `3v2_uap_0g0` | 三父 | [《史記・秦本紀》][5] | [JSON](3v2_uap_0g0.json) |
| `3vk_jr4_vnd` | 齮（南陽守） | [《史記・樊酈滕灌列傳》][77] | [JSON](3vk_jr4_vnd.json) |
| `3vz_xp9_jrh` | 襄公夫人（衛未名） | [《史記・衛康叔世家》][19] | [JSON](3vz_xp9_jrh.json) |
| `3w5_mbd_87m` | 鄭昌 | [《史記・韓信盧綰列傳》][75] | [JSON](3w5_mbd_87m.json) |
| `3w5_zp1_0g6` | 高武侯鰓 | [《史記・高祖本紀》][8] | [JSON](3w5_zp1_0g6.json) |
| `3wu_5e9_3sk` | 蔡女（田世家厲公母未名者） | [《史記・田敬仲完世家》][28] | [JSON](3wu_5e9_3sk.json) |
| `3x2_x5v_51q` | 公賓 | [《史記・孔子世家》][29] | [JSON](3x2_x5v_51q.json) |
| `3xa_jvi_o6n` | 趙禹 | [《史記・田叔列傳》][86] | [JSON](3xa_jvi_o6n.json) |
| `3xj_ut0_ope` | 田豹 | [《史記・田敬仲完世家》][28] | [JSON](3xj_ut0_ope.json) |
| `3yj_8tp_4mp` | 伊尹 | [《史記・老子韓非列傳》][45] | [JSON](3yj_8tp_4mp.json) |
| `3yz_ws9_5dw` | 匡王 | [《史記・周本紀》][4] | [JSON](3yz_ws9_5dw.json) |
| `3z8_zue_k0k` | 句望 | [《史記・五帝本紀》][1] | [JSON](3z8_zue_k0k.json) |
| `3zw_02o_knb` | 章平 | [《史記・絳侯周勃世家》][39] | [JSON](3zw_02o_knb.json) |
| `40h_sbg_kpj` | 慶鄭（惠公諫臣） | [《史記・晉世家》][21] | [JSON](40h_sbg_kpj.json) |
| `40p_hkv_oqy` | 莊青翟 | [《史記・張丞相列傳》][78] | [JSON](40p_hkv_oqy.json) |
| `418_6k8_181` | 春申君 | [《史記・陳涉世家》][30] | [JSON](418_6k8_181.json) |
| `41b_aj9_500` | 重耳 | [《史記・魏世家》][26] | [JSON](41b_aj9_500.json) |
| `41m_4yl_j39` | 張敖 | [《史記・張丞相列傳》][78] | [JSON](41m_4yl_j39.json) |
| `422_9v5_g9x` | 蘇秦 | [《史記・蘇秦列傳》][51] | [JSON](422_9v5_g9x.json) |
| `423_9wn_ew3` | 李由 | [《史記・項羽本紀》][7] | [JSON](423_9wn_ew3.json) |
| `42a_nv5_urq` | 妲己 | [《史記・殷本紀》][3] | [JSON](42a_nv5_urq.json) |
| `42c_0ck_iry` | 桓齮 | [《史記・秦始皇本紀》][6] | [JSON](42c_0ck_iry.json) |
| `42k_42i_2kj` | 無咎 | [《史記・齊太公世家》][14] | [JSON](42k_42i_2kj.json) |
| `431_23t_wkr` | 冒頓 | [《史記・田叔列傳》][86] | [JSON](431_23t_wkr.json) |
| `431_o36_6w9` | 蜀守若 | [《史記・秦本紀》][5] | [JSON](431_o36_6w9.json) |
| `436_eoz_u4n` | 紂 | [《史記・張丞相列傳》][78] | [JSON](436_eoz_u4n.json) |
| `43a_ywd_jl7` | 成王 | [《史記・外戚世家》][31] | [JSON](43a_ywd_jl7.json) |
| `43x_4at_fj2` | 賈壽 | [《史記・呂太后本紀》][9] | [JSON](43x_4at_fj2.json) |
| `447_8ix_j7j` | 宋王書信 | [《史記・蘇秦列傳》][51] | [JSON](447_8ix_j7j.json) |
| `44k_ouz_zd0` | 朱公長男之母（越世家未名者） | [《史記・越王勾踐世家》][23] | [JSON](44k_ouz_zd0.json) |
| `44s_fyq_t0d` | 羨門 | [《史記・秦始皇本紀》][6]、[《史記・孝武本紀》][12] | [JSON](44s_fyq_t0d.json) |
| `44u_z5w_09n` | 荊軻 | [《史記・田敬仲完世家》][28] | [JSON](44u_z5w_09n.json) |
| `44y_h3t_0pc` | 伯服（幽王子） | [《史記・周本紀》][4] | [JSON](44y_h3t_0pc.json) |
| `452_xfy_50i` | 趙賁 | [《史記・樊酈滕灌列傳》][77] | [JSON](452_xfy_50i.json) |
| `45y_6ae_x2a` | 竇嬰 | [《史記・外戚世家》][31] | [JSON](45y_6ae_x2a.json) |
| `466_skv_k2t` | 陳勝 | [《史記・白起王翦列傳》][55] | [JSON](466_skv_k2t.json) |
| `46e_c85_fft` | 趙文子 | [《史記・吳太伯世家》][13] | [JSON](46e_c85_fft.json) |
| `46o_tfb_rlc` | 公劉 | [《史記・劉敬叔孫通列傳》][81] | [JSON](46o_tfb_rlc.json) |
| `47r_xxi_en8` | 燭庸（吳公子） | [《史記・吳太伯世家》][13] | [JSON](47r_xxi_en8.json) |
| `47s_3n9_u3c` | 項羽 | [《史記・淮陰侯列傳》][74] | [JSON](47s_3n9_u3c.json) |
| `47s_jy6_iam` | 子申（楚昭王弟） | [《史記・楚世家》][22] | [JSON](47s_jy6_iam.json) |
| `47w_1p3_yyi` | 守陘 | [《史記・絳侯周勃世家》][39] | [JSON](47w_1p3_yyi.json) |
| `47y_fpt_ae1` | 孫子 | [《史記・孟子荀卿列傳》][56] | [JSON](47y_fpt_ae1.json) |
| `482_ly0_otk` | 顓孫師 | [《史記・仲尼弟子列傳》][49] | [JSON](482_ly0_otk.json) |
| `484_day_gmv` | 匡衡 | [《史記・張丞相列傳》][78] | [JSON](484_day_gmv.json) |
| `48a_5al_4n8` | 芮姬（孺子母） | [《史記・齊太公世家》][14] | [JSON](48a_5al_4n8.json) |
| `48a_gwp_kht` | 曾子 | [《史記・孫子吳起列傳》][47] | [JSON](48a_gwp_kht.json) |
| `48p_k57_rfk` | 羽嬰 | [《史記・曹相國世家》][36] | [JSON](48p_k57_rfk.json) |
| `496_l4q_fsy` | 今皇帝（孔子世家博士所事未名者） | [《史記・孔子世家》][29] | [JSON](496_l4q_fsy.json) |
| `49c_ey3_m75` | 如意 | [《史記・外戚世家》][31] | [JSON](49c_ey3_m75.json) |
| `49c_qn7_421` | 燕王喜 | [《史記・白起王翦列傳》][55] | [JSON](49c_qn7_421.json) |
| `49g_7az_e4i` | 李斯 | [《史記・李斯列傳》][69] | [JSON](49g_7az_e4i.json) |
| `49t_1cr_hfa` | 武涉 | [《史記・淮陰侯列傳》][74] | [JSON](49t_1cr_hfa.json) |
| `49u_1m4_z7p` | 周威王 | [《史記・魏世家》][26] | [JSON](49u_1m4_z7p.json) |
| `49x_hsj_tmo` | 燕易王 | [《史記・蘇秦列傳》][51] | [JSON](49x_hsj_tmo.json) |
| `4aa_9tj_jvn` | 鄭姬（昭母） | [《史記・齊太公世家》][14] | [JSON](4aa_9tj_jvn.json) |
| `4ai_d4s_gde` | 趙高 | [《史記・李斯列傳》][69] | [JSON](4ai_d4s_gde.json) |
| `4b8_j4t_8tj` | 趙王（田世家平陸未名者） | [《史記・田敬仲完世家》][28] | [JSON](4b8_j4t_8tj.json) |
| `4bb_se5_6zs` | 季孫引古未定 | [《史記・魯仲連鄒陽列傳》][65] | [JSON](4bb_se5_6zs.json) |
| `4bt_npm_axo` | 比干引古 | [《史記・魯仲連鄒陽列傳》][65] | [JSON](4bt_npm_axo.json) |
| `4bx_elr_66i` | 子反（宋圍城記事） | [《史記・宋微子世家》][20] | [JSON](4bx_elr_66i.json) |
| `4bx_x9i_210` | 叔瞻（鄭臣） | [《史記・鄭世家》][24] | [JSON](4bx_x9i_210.json) |
| `4ck_c0z_a0t` | 五羖 | [《史記・孔子世家》][29] | [JSON](4ck_c0z_a0t.json) |
| `4cv_f12_d1p` | 韓昭侯 | [《史記・趙世家》][25] | [JSON](4cv_f12_d1p.json) |
| `4cy_oy6_nua` | 田儋 | [《史記・陳涉世家》][30] | [JSON](4cy_oy6_nua.json) |
| `4d0_phq_cjk` | 申公巫臣 | [《史記・晉世家》][21] | [JSON](4d0_phq_cjk.json) |
| `4dk_afl_vwx` | 屈侯鮒 | [《史記・魏世家》][26] | [JSON](4dk_afl_vwx.json) |
| `4dm_2h1_9je` | 屈原（楚篇使齊者） | [《史記・楚世家》][22] | [JSON](4dm_2h1_9je.json) |
| `4dr_y2e_ta8` | 段干木 | [《史記・魏世家》][26] | [JSON](4dr_y2e_ta8.json) |
| `4e7_nix_4rh` | 韓宣子 | [《史記・吳太伯世家》][13]、[《史記・晉世家》][21] | [JSON](4e7_nix_4rh.json) |
| `4ef_u9d_swf` | 董緶 | [《史記・陳涉世家》][30] | [JSON](4ef_u9d_swf.json) |
| `4eg_94p_uen` | 欒貞子（襄公六年卒者） | [《史記・晉世家》][21] | [JSON](4eg_94p_uen.json) |
| `4ej_bfp_hod` | 康子 | [《史記・孔子世家》][29] | [JSON](4ej_bfp_hod.json) |
| `4eq_1xe_1xg` | 侯家舍人未名 | [《史記・樊酈滕灌列傳》][77] | [JSON](4eq_1xe_1xg.json) |
| `4es_tvz_kjv` | 翳（翟王） | [《史記・淮陰侯列傳》][74] | [JSON](4es_tvz_kjv.json) |
| `4fa_1v4_jmc` | 南子 | [《史記・仲尼弟子列傳》][49] | [JSON](4fa_1v4_jmc.json) |
| `4fa_nn3_4zq` | 紂引古 | [《史記・魯仲連鄒陽列傳》][65] | [JSON](4fa_nn3_4zq.json) |
| `4gn_hir_vrl` | 秦王（魏世家增質秦未名者） | [《史記・魏世家》][26] | [JSON](4gn_hir_vrl.json) |
| `4gs_evl_a1u` | 秦司馬夷 | [《史記・曹相國世家》][36] | [JSON](4gs_evl_a1u.json) |
| `4hf_tdv_ju8` | 夏說 | [《史記・淮陰侯列傳》][74] | [JSON](4hf_tdv_ju8.json) |
| `4hs_s8h_blc` | 韓信 | [《史記・黥布列傳》][73] | [JSON](4hs_s8h_blc.json) |
| `4hw_5vr_bqf` | 秦穆公 | [《史記・秦本紀》][5] | [JSON](4hw_5vr_bqf.json) |
| `4i4_lmr_aap` | 秦王義渠事件 | [《史記・張儀列傳》][52] | [JSON](4i4_lmr_aap.json) |
| `4i4_ywy_p53` | 梁繇靡（韓原御者） | [《史記・晉世家》][21] | [JSON](4i4_ywy_p53.json) |
| `4ic_qbn_lc9` | 韓昭侯 | [《史記・老子韓非列傳》][45] | [JSON](4ic_qbn_lc9.json) |
| `4iy_sew_r5r` | 李斯 | [《史記・蕭相國世家》][35] | [JSON](4iy_sew_r5r.json) |
| `4jp_1f7_xgx` | 樓季引古 | [《史記・李斯列傳》][69] | [JSON](4jp_1f7_xgx.json) |
| `4jv_qte_5p4` | 章邯 | [《史記・項羽本紀》][7] | [JSON](4jv_qte_5p4.json) |
| `4k0_mri_buk` | 盧綰 | [《史記・樊酈滕灌列傳》][77] | [JSON](4k0_mri_buk.json) |
| `4ki_y9a_zjy` | 陳澤 | [《史記・淮陰侯列傳》][74] | [JSON](4ki_y9a_zjy.json) |
| `4kq_wgk_0k4` | 衛姬（楚篇齊桓公母） | [《史記・齊太公世家》][14]、[《史記・楚世家》][22] | [JSON](4kq_wgk_0k4.json) |
| `4ky_3rl_efu` | 侯生 | [《史記・秦始皇本紀》][6] | [JSON](4ky_3rl_efu.json) |
| `4lj_xrf_bsl` | 晉景公 | [《史記・晉世家》][21] | [JSON](4lj_xrf_bsl.json) |
| `4m0_6oi_xjv` | 楚隆 | [《史記・趙世家》][25] | [JSON](4m0_6oi_xjv.json) |
| `4mm_rhu_h4k` | 黥布 | [《史記・留侯世家》][37] | [JSON](4mm_rhu_h4k.json) |
| `4n3_9bj_cuq` | 穨 | [《史記・鄭世家》][24] | [JSON](4n3_9bj_cuq.json) |
| `4nb_0tn_256` | 陶青 | [《史記・孝景本紀》][11] | [JSON](4nb_0tn_256.json) |
| `4nq_12w_41d` | 如姬父仇人未名 | [《史記・魏公子列傳》][59] | [JSON](4nq_12w_41d.json) |
| `4oj_l54_3pa` | 公孫臣 | [《史記・張丞相列傳》][78] | [JSON](4oj_l54_3pa.json) |
| `4oo_ax5_tpl` | 午（邯鄲大夫） | [《史記・晉世家》][21] | [JSON](4oo_ax5_tpl.json) |
| `4oq_2zh_bd2` | 南陽守齮 | [《史記・高祖本紀》][8] | [JSON](4oq_2zh_bd2.json) |
| `4p6_tvl_gnh` | 綦毋卹 | [《史記・樊酈滕灌列傳》][77] | [JSON](4p6_tvl_gnh.json) |
| `4q3_8yy_0ys` | 王黃 | [《史記・韓信盧綰列傳》][75] | [JSON](4q3_8yy_0ys.json) |
| `4qa_pqm_6hr` | 繁君（丞相司直） | [《史記・張丞相列傳》][78] | [JSON](4qa_pqm_6hr.json) |
| `4qc_auj_w5k` | 韓嫣 | [《史記・外戚世家》][31] | [JSON](4qc_auj_w5k.json) |
| `4qd_4bt_jf6` | 考叔 | [《史記・鄭世家》][24] | [JSON](4qd_4bt_jf6.json) |
| `4qi_6lx_4be` | 孟孫（孔子世家保成未名者） | [《史記・孔子世家》][29] | [JSON](4qi_6lx_4be.json) |
| `4qp_m76_23j` | 商鞅 | [《史記・田敬仲完世家》][28] | [JSON](4qp_m76_23j.json) |
| `4qt_ofp_ysv` | 梁孝王 | [《史記・魯仲連鄒陽列傳》][65] | [JSON](4qt_ofp_ysv.json) |
| `4qu_7zi_cdd` | 趙孝成王（燕王喜記事） | [《史記・燕召公世家》][16] | [JSON](4qu_7zi_cdd.json) |
| `4r7_u1t_cn0` | 楚靈王 | [《史記・孔子世家》][29] | [JSON](4r7_u1t_cn0.json) |
| `4r9_n1i_pu5` | 酈食其 | [《史記・酈生陸賈列傳》][79] | [JSON](4r9_n1i_pu5.json) |
| `4rk_808_kn9` | 韓宣子（楚篇議子比者） | [《史記・楚世家》][22] | [JSON](4rk_808_kn9.json) |
| `4rt_vz6_obh` | 項悍 | [《史記・傅靳蒯成列傳》][80] | [JSON](4rt_vz6_obh.json) |
| `4rw_nce_8oq` | 史狗 | [《史記・吳太伯世家》][13] | [JSON](4rw_nce_8oq.json) |
| `4t4_ojw_dn7` | 西王母 | [《史記・趙世家》][25] | [JSON](4t4_ojw_dn7.json) |
| `4t6_6il_chg` | 樂毅 | [《史記・樂毅列傳》][62] | [JSON](4t6_6il_chg.json) |
| `4t6_6ur_8lb` | 孔子引古 | [《史記・魯仲連鄒陽列傳》][65] | [JSON](4t6_6ur_8lb.json) |
| `4tb_tcb_9tq` | 朝（孝惠後宮子稱） | [《史記・呂太后本紀》][9] | [JSON](4tb_tcb_9tq.json) |
| `4tf_n3p_1xu` | 正考父（宋大夫作頌記事） | [《史記・宋微子世家》][20] | [JSON](4tf_n3p_1xu.json) |
| `4tj_hha_8k9` | 楚王（田世家煮棗議論未名者） | [《史記・田敬仲完世家》][28] | [JSON](4tj_hha_8k9.json) |
| `4tn_boq_btx` | 顏髙 | [《史記・仲尼弟子列傳》][49] | [JSON](4tn_boq_btx.json) |
| `4tq_wkd_83s` | 趙王降秦 | [《史記・白起王翦列傳》][55] | [JSON](4tq_wkd_83s.json) |
| `4tr_mlx_ju2` | 姜原 | [《史記・外戚世家》][31] | [JSON](4tr_mlx_ju2.json) |
| `4tv_nhj_oxt` | 羋戎 | [《史記・范睢蔡澤列傳》][61] | [JSON](4tv_nhj_oxt.json) |
| `4u0_rni_a7s` | 項梁 | [《史記・李斯列傳》][69] | [JSON](4u0_rni_a7s.json) |
| `4ua_tkd_2kk` | 郅都 | [《史記・五宗世家》][41] | [JSON](4ua_tkd_2kk.json) |
| `4ud_0tq_d3r` | 宣伯 | [《史記・魯周公世家》][15] | [JSON](4ud_0tq_d3r.json) |
| `4uh_n5r_0id` | 宰予 | [《史記・仲尼弟子列傳》][49] | [JSON](4uh_n5r_0id.json) |
| `4v3_fka_aca` | 公子成 | [《史記・趙世家》][25] | [JSON](4v3_fka_aca.json) |
| `4vk_6jr_jtl` | 秦昭王引古 | [《史記・李斯列傳》][69] | [JSON](4vk_6jr_jtl.json) |
| `4vo_tst_9dm` | 少帝 | [《史記・齊悼惠王世家》][34] | [JSON](4vo_tst_9dm.json) |
| `4w2_573_fnh` | 王夫人（武帝所幸） | [《史記・孝武本紀》][12] | [JSON](4w2_573_fnh.json) |
| `4w2_vs3_n1r` | 趙鞅 | [《史記・魏世家》][26] | [JSON](4w2_vs3_n1r.json) |
| `4w3_yw4_lcm` | 淖齒 | [《史記・田單列傳》][64] | [JSON](4w3_yw4_lcm.json) |
| `4wc_97x_2gd` | 孝惠 | [《史記・陳丞相世家》][38] | [JSON](4wc_97x_2gd.json) |
| `4we_dkh_dzr` | 賈華（伐屈者） | [《史記・晉世家》][21] | [JSON](4we_dkh_dzr.json) |
| `4wh_yve_8ul` | 景快 | [《史記・秦本紀》][5]、[《史記・楚世家》][22] | [JSON](4wh_yve_8ul.json) |
| `4xh_zzy_gyn` | 太史公 | [《史記・屈原賈生列傳》][66] | [JSON](4xh_zzy_gyn.json) |
| `4xv_96s_2qj` | 周市 | [《史記・魏豹彭越列傳》][72] | [JSON](4xv_96s_2qj.json) |
| `4xv_p1u_vn2` | 高后 | [《史記・韓信盧綰列傳》][75] | [JSON](4xv_p1u_vn2.json) |
| `4y3_xk6_8vs` | 富辰 | [《史記・周本紀》][4] | [JSON](4y3_xk6_8vs.json) |
| `4ym_j77_5al` | 胥童（晉姬兄） | [《史記・晉世家》][21] | [JSON](4ym_j77_5al.json) |
| `4yr_em4_wid` | 慎靚王 | [《史記・周本紀》][4] | [JSON](4yr_em4_wid.json) |
| `4ys_gkz_j29` | 孟嘗君引述 | [《史記・呂不韋列傳》][67] | [JSON](4ys_gkz_j29.json) |
| `4yy_xd0_rft` | 梁王（魏世家蘇代游説所指未名者） | [《史記・魏世家》][26] | [JSON](4yy_xd0_rft.json) |
| `4z2_eut_yeu` | 范陽令未名 | [《史記・張耳陳餘列傳》][71] | [JSON](4z2_eut_yeu.json) |
| `504_piy_j5v` | 章邯 | [《史記・項羽本紀》][7] | [JSON](504_piy_j5v.json) |
| `50g_j9s_2le` | 項羽 | [《史記・酈生陸賈列傳》][79] | [JSON](50g_j9s_2le.json) |
| `50q_se5_gmw` | 湯 | [《史記・商君列傳》][50] | [JSON](50q_se5_gmw.json) |
| `50s_src_65d` | 齊湣王（楚篇約從者） | [《史記・楚世家》][22] | [JSON](50s_src_65d.json) |
| `50y_1nz_2rt` | 袁盎 | [《史記・袁盎鼂錯列傳》][83] | [JSON](50y_1nz_2rt.json) |
| `51c_0t8_4nj` | 公子延 | [《史記・蘇秦列傳》][51] | [JSON](51c_0t8_4nj.json) |
| `51q_vfp_w6t` | 狄黑 | [《史記・仲尼弟子列傳》][49] | [JSON](51q_vfp_w6t.json) |
| `51s_div_vuy` | 繆公 | [《史記・孟子荀卿列傳》][56] | [JSON](51s_div_vuy.json) |
| `523_zlc_qfv` | 齊湣王引古 | [《史記・魯仲連鄒陽列傳》][65] | [JSON](523_zlc_qfv.json) |
| `52f_fie_3vj` | 昆吾（陸終長子） | [《史記・楚世家》][22] | [JSON](52f_fie_3vj.json) |
| `52o_i25_ekg` | 李夫人 | [《史記・外戚世家》][31] | [JSON](52o_i25_ekg.json) |
| `52v_lww_ywo` | 周章 | [《史記・張耳陳餘列傳》][71] | [JSON](52v_lww_ywo.json) |
| `531_xn1_ynu` | 灶 | [《史記・穰侯列傳》][54] | [JSON](531_xn1_ynu.json) |
| `53c_7dg_tfn` | 孔將軍（垓下敘事） | [《史記・高祖本紀》][8] | [JSON](53c_7dg_tfn.json) |
| `53e_xmi_9zk` | 蘇代 | [《史記・周本紀》][4] | [JSON](53e_xmi_9zk.json) |
| `53n_g5n_wci` | 帶佗 | [《史記・秦始皇本紀》][6] | [JSON](53n_g5n_wci.json) |
| `53z_6rk_goh` | 子產 | [《史記・孔子世家》][29] | [JSON](53z_6rk_goh.json) |
| `542_vdp_y8p` | 蒯聵 | [《史記・孔子世家》][29] | [JSON](542_vdp_y8p.json) |
| `548_u01_jnh` | 公子囊瓦 | [《史記・伍子胥列傳》][48] | [JSON](548_u01_jnh.json) |
| `54k_feb_3iw` | 薛文 | [《史記・田敬仲完世家》][28] | [JSON](54k_feb_3iw.json) |
| `55g_mc2_xo2` | 周勃 | [《史記・絳侯周勃世家》][39] | [JSON](55g_mc2_xo2.json) |
| `561_608_i0z` | 呂祿 | [《史記・呂太后本紀》][9] | [JSON](561_608_i0z.json) |
| `56r_ewo_1hp` | 毀隃 | [《史記・周本紀》][4] | [JSON](56r_ewo_1hp.json) |
| `56x_3iq_m0y` | 項羽 | [《史記・項羽本紀》][7] | [JSON](56x_3iq_m0y.json) |
| `584_79c_2t1` | 蜀王 | [《史記・張儀列傳》][52] | [JSON](584_79c_2t1.json) |
| `59b_c0s_5il` | 濟北王劫守未名 | [《史記・吳王濞列傳》][88] | [JSON](59b_c0s_5il.json) |
| `59m_lub_ftn` | 燕伋 | [《史記・仲尼弟子列傳》][49] | [JSON](59m_lub_ftn.json) |
| `59o_pnz_um0` | 呂釋之嗣子（未名） | [《史記・呂太后本紀》][9] | [JSON](59o_pnz_um0.json) |
| `5ad_lr6_exk` | 李牧北邊代將者未名 | [《史記・廉頗藺相如列傳》][63] | [JSON](5ad_lr6_exk.json) |
| `5aj_khx_izm` | 已死太子（趙世家孝成王十年未名者） | [《史記・趙世家》][25] | [JSON](5aj_khx_izm.json) |
| `5aj_ozr_k8y` | 公孫支 | [《史記・扁鵲倉公列傳》][87] | [JSON](5aj_ozr_k8y.json) |
| `5an_r55_hee` | 張儀 | [《史記・張儀列傳》][52] | [JSON](5an_r55_hee.json) |
| `5av_w6l_zea` | 應侯 | [《史記・范睢蔡澤列傳》][61] | [JSON](5av_w6l_zea.json) |
| `5b0_v43_0o7` | 靳尚 | [《史記・張儀列傳》][52] | [JSON](5b0_v43_0o7.json) |
| `5b9_na5_dn4` | 齊頃公 | [《史記・韓世家》][27] | [JSON](5b9_na5_dn4.json) |
| `5bm_cbv_s8c` | 田文（長安相工） | [《史記・張丞相列傳》][78] | [JSON](5bm_cbv_s8c.json) |
| `5bx_zam_t0r` | 晉昭公 | [《史記・鄭世家》][24] | [JSON](5bx_zam_t0r.json) |
| `5c1_xyw_n3t` | 肥義 | [《史記・趙世家》][25] | [JSON](5c1_xyw_n3t.json) |
| `5c9_asn_jp0` | 韓聶 | [《史記・田敬仲完世家》][28] | [JSON](5c9_asn_jp0.json) |
| `5cz_60u_g28` | 比干 | [《史記・留侯世家》][37] | [JSON](5cz_60u_g28.json) |
| `5da_d1r_s7j` | 太子（宋特所殺者未名） | [《史記・宋微子世家》][20] | [JSON](5da_d1r_s7j.json) |
| `5dc_2fb_2bu` | 楚使者 | [《史記・老子韓非列傳》][45] | [JSON](5dc_2fb_2bu.json) |
| `5dg_lbc_hdn` | 太史公 | [《史記・張釋之馮唐列傳》][84] | [JSON](5dg_lbc_hdn.json) |
| `5dh_xqg_em0` | 姜氏（晉穆侯夫人） | [《史記・晉世家》][21] | [JSON](5dh_xqg_em0.json) |
| `5dl_6xj_187` | 魏王咎 | [《史記・田儋列傳》][76] | [JSON](5dl_6xj_187.json) |
| `5do_703_rfz` | 王陵 | [《史記・陳丞相世家》][38] | [JSON](5do_703_rfz.json) |
| `5do_gvs_t80` | 叔孫（迎昭公記事未名） | [《史記・魯周公世家》][15] | [JSON](5do_gvs_t80.json) |
| `5dq_f5i_bkh` | 平陽侯 | [《史記・齊悼惠王世家》][34] | [JSON](5dq_f5i_bkh.json) |
| `5dy_81j_55y` | 蓋餘（吳公子） | [《史記・吳太伯世家》][13] | [JSON](5dy_81j_55y.json) |
| `5e0_jgn_wj9` | 畢公髙 | [《史記・魏世家》][26] | [JSON](5e0_jgn_wj9.json) |
| `5e8_vhx_rs4` | 公孫杵臼 | [《史記・趙世家》][25] | [JSON](5e8_vhx_rs4.json) |
| `5f6_5r4_eni` | 孝惠帝 | [《史記・曹相國世家》][36] | [JSON](5f6_5r4_eni.json) |
| `5fk_w9g_t8y` | 弗父何 | [《史記・孔子世家》][29] | [JSON](5fk_w9g_t8y.json) |
| `5g0_8ty_89n` | 屠岸賈 | [《史記・趙世家》][25] | [JSON](5g0_8ty_89n.json) |
| `5gf_evg_l0y` | 樂羊 | [《史記・樗里子甘茂列傳》][53] | [JSON](5gf_evg_l0y.json) |
| `5gu_ab2_kmn` | 公子朔 | [《史記・魏世家》][26] | [JSON](5gu_ab2_kmn.json) |
| `5gw_05t_sxy` | 楚聲王 | [《史記・周本紀》][4] | [JSON](5gw_05t_sxy.json) |
| `5h1_m8f_043` | 太史公 | [《史記・梁孝王世家》][40] | [JSON](5h1_m8f_043.json) |
| `5he_z7b_nzv` | 樓緩 | [《史記・穰侯列傳》][54] | [JSON](5he_z7b_nzv.json) |
| `5i3_d8c_1u7` | 大夫種 | [《史記・仲尼弟子列傳》][49] | [JSON](5i3_d8c_1u7.json) |
| `5ii_dzh_6bo` | 高后 | [《史記・曹相國世家》][36] | [JSON](5ii_dzh_6bo.json) |
| `5ij_409_sfj` | 楊熊 | [《史記・樊酈滕灌列傳》][77] | [JSON](5ij_409_sfj.json) |
| `5iu_ut5_0yv` | 蜀侯煇 | [《史記・樗里子甘茂列傳》][53] | [JSON](5iu_ut5_0yv.json) |
| `5j9_f5f_48v` | 公叔妻公主 | [《史記・孫子吳起列傳》][47] | [JSON](5j9_f5f_48v.json) |
| `5jy_q5w_acp` | 趙奢 | [《史記・陳涉世家》][30] | [JSON](5jy_q5w_acp.json) |
| `5k2_i3p_h9m` | 桀比擬 | [《史記・蕭相國世家》][35] | [JSON](5k2_i3p_h9m.json) |
| `5k7_otk_r9v` | 盤庚 | [《史記・殷本紀》][3] | [JSON](5k7_otk_r9v.json) |
| `5k8_ms4_y3k` | 淮陰侯未詳名 | [《史記・傅靳蒯成列傳》][80] | [JSON](5k8_ms4_y3k.json) |
| `5kc_wmn_zbj` | 孫臏 | [《史記・陳涉世家》][30] | [JSON](5kc_wmn_zbj.json) |
| `5kt_ucd_fbz` | 韓信 | [《史記・張耳陳餘列傳》][71] | [JSON](5kt_ucd_fbz.json) |
| `5kw_jr9_kzn` | 周天子伐梁 | [《史記・張儀列傳》][52] | [JSON](5kw_jr9_kzn.json) |
| `5ky_x6i_539` | 晏嬰 | [《史記・田敬仲完世家》][28] | [JSON](5ky_x6i_539.json) |
| `5l3_mwc_fj2` | 衛尉定 | [《史記・孝文本紀》][10] | [JSON](5l3_mwc_fj2.json) |
| `5l5_0v4_gqg` | 公孫龍 | [《史記・平原君虞卿列傳》][58] | [JSON](5l5_0v4_gqg.json) |
| `5lh_q1k_9qg` | 子重（楚將宋盟記事） | [《史記・宋微子世家》][20] | [JSON](5lh_q1k_9qg.json) |
| `5mb_gmu_c2n` | 黃姬 | [《史記・扁鵲倉公列傳》][87] | [JSON](5mb_gmu_c2n.json) |
| `5md_xfr_2k3` | 魏王索魏齊未名 | [《史記・范睢蔡澤列傳》][61] | [JSON](5md_xfr_2k3.json) |
| `5mj_zds_atm` | 韓王張儀說韓 | [《史記・張儀列傳》][52] | [JSON](5mj_zds_atm.json) |
| `5mm_yit_hs8` | 長姬（陳哀公師母） | [《史記・陳杞世家》][18] | [JSON](5mm_yit_hs8.json) |
| `5na_uad_5vl` | 彭越 | [《史記・留侯世家》][37] | [JSON](5na_uad_5vl.json) |
| `5nc_cwr_2tg` | 黃帝 | [《史記・陳丞相世家》][38] | [JSON](5nc_cwr_2tg.json) |
| `5ni_ydv_892` | 公子通 | [《史記・秦本紀》][5] | [JSON](5ni_ydv_892.json) |
| `5nt_1fk_g2o` | 衛長君 | [《史記・外戚世家》][31] | [JSON](5nt_1fk_g2o.json) |
| `5o2_8lk_osv` | 中謝莊舄故事 | [《史記・張儀列傳》][52] | [JSON](5o2_8lk_osv.json) |
| `5oa_q8c_ncf` | 伍子胥引古 | [《史記・范睢蔡澤列傳》][61] | [JSON](5oa_q8c_ncf.json) |
| `5oj_ytk_tgo` | 若木 | [《史記・秦本紀》][5] | [JSON](5oj_ytk_tgo.json) |
| `5on_fmd_qzc` | 徒父祺 | [《史記・趙世家》][25] | [JSON](5on_fmd_qzc.json) |
| `5oq_4kn_ytm` | 祝聸 | [《史記・鄭世家》][24] | [JSON](5oq_4kn_ytm.json) |
| `5os_ov1_i72` | 魏太子申 | [《史記・魏世家》][26] | [JSON](5os_ov1_i72.json) |
| `5pe_wi8_omy` | 田子行 | [《史記・田敬仲完世家》][28] | [JSON](5pe_wi8_omy.json) |
| `5pr_wl7_dk1` | 太顛 | [《史記・周本紀》][4] | [JSON](5pr_wl7_dk1.json) |
| `5q1_0om_9ly` | 屈丐 | [《史記・韓世家》][27] | [JSON](5q1_0om_9ly.json) |
| `5q3_f2w_w1e` | 田儋奴未名 | [《史記・田儋列傳》][76] | [JSON](5q3_f2w_w1e.json) |
| `5r6_g5i_kd4` | 遠吏故事夫 | [《史記・蘇秦列傳》][51] | [JSON](5r6_g5i_kd4.json) |
| `5rl_b1r_2tk` | 華陽君 | [《史記・范睢蔡澤列傳》][61] | [JSON](5rl_b1r_2tk.json) |
| `5ry_fls_4ob` | 太史公 | [《史記・老子韓非列傳》][45] | [JSON](5ry_fls_4ob.json) |
| `5s5_hwm_0gx` | 燕文公夫人（未名） | [《史記・蘇秦列傳》][51] | [JSON](5s5_hwm_0gx.json) |
| `5so_wyq_db0` | 張賀 | [《史記・陳涉世家》][30] | [JSON](5so_wyq_db0.json) |
| `5sp_ts1_az0` | 冀芮（晉奔梁記事） | [《史記・晉世家》][21] | [JSON](5sp_ts1_az0.json) |
| `5sx_o5n_zj6` | 紂引古 | [《史記・孟子荀卿列傳》][56] | [JSON](5sx_o5n_zj6.json) |
| `5t3_6uk_ndj` | 公子紲 | [《史記・趙世家》][25] | [JSON](5t3_6uk_ndj.json) |
| `5tm_4da_km9` | 子羔（衛亂出城者） | [《史記・衛康叔世家》][19] | [JSON](5tm_4da_km9.json) |
| `5ty_zo4_nz8` | 太史公 | [《史記・五宗世家》][41] | [JSON](5ty_zo4_nz8.json) |
| `5v8_amk_emn` | 龐涓 | [《史記・孫子吳起列傳》][47] | [JSON](5v8_amk_emn.json) |
| `5va_k17_tk7` | 周文王 | [《史記・劉敬叔孫通列傳》][81] | [JSON](5va_k17_tk7.json) |
| `5vz_50g_h50` | 汲黯 | [《史記・梁孝王世家》][40] | [JSON](5vz_50g_h50.json) |
| `5w4_qju_qbd` | 客卿錯 | [《史記・白起王翦列傳》][55] | [JSON](5w4_qju_qbd.json) |
| `5wb_odp_wx1` | 任不齊 | [《史記・仲尼弟子列傳》][49] | [JSON](5wb_odp_wx1.json) |
| `5wp_sih_p2e` | 韓武子 | [《史記・韓世家》][27] | [JSON](5wp_sih_p2e.json) |
| `5x1_l5n_39c` | 趙桓子 | [《史記・魏世家》][26] | [JSON](5x1_l5n_39c.json) |
| `5x6_bvq_088` | 郭開 | [《史記・廉頗藺相如列傳》][63] | [JSON](5x6_bvq_088.json) |
| `5xc_h44_k0y` | 申徒嘉 | [《史記・孝文本紀》][10]、[《史記・孝景本紀》][11] | [JSON](5xc_h44_k0y.json) |
| `5yg_1bz_wto` | 秦獻公 | [《史記・秦本紀》][5] | [JSON](5yg_1bz_wto.json) |
| `5yi_qwl_awr` | 趙王被虜未名 | [《史記・刺客列傳》][68] | [JSON](5yi_qwl_awr.json) |
| `5yr_u9t_c8n` | 蹠（引古） | [《史記・淮陰侯列傳》][74] | [JSON](5yr_u9t_c8n.json) |
| `5z2_ick_ts9` | 虢中庶子未名 | [《史記・扁鵲倉公列傳》][87] | [JSON](5z2_ick_ts9.json) |
| `5za_kx5_duo` | 康（熊渠長子句亶王） | [《史記・楚世家》][22] | [JSON](5za_kx5_duo.json) |
| `5zd_tsn_2xr` | 子亹 | [《史記・鄭世家》][24] | [JSON](5zd_tsn_2xr.json) |
| `5zv_8nc_ifz` | 伯夷引古 | [《史記・屈原賈生列傳》][66] | [JSON](5zv_8nc_ifz.json) |
| `600_7ih_3xk` | 李延年 | [《史記・外戚世家》][31] | [JSON](600_7ih_3xk.json) |
| `602_qwv_jz8` | 楚武王（陳篇紀年） | [《史記・陳杞世家》][18] | [JSON](602_qwv_jz8.json) |
| `608_d7l_epu` | 伋他女（衛宣公另取者） | [《史記・衛康叔世家》][19] | [JSON](608_d7l_epu.json) |
| `60e_l3p_h3j` | 盛橋 | [《史記・春申君列傳》][60] | [JSON](60e_l3p_h3j.json) |
| `60u_e89_x8d` | 王翦 | [《史記・廉頗藺相如列傳》][63] | [JSON](60u_e89_x8d.json) |
| `611_no8_35r` | 呂禮 | [《史記・穰侯列傳》][54] | [JSON](611_no8_35r.json) |
| `61b_fc5_6h4` | 祖伊 | [《史記・殷本紀》][3] | [JSON](61b_fc5_6h4.json) |
| `61g_cr5_n52` | 建母蔡女 | [《史記・伍子胥列傳》][48] | [JSON](61g_cr5_n52.json) |
| `61h_0sk_4pb` | 吳起 | [《史記・孫子吳起列傳》][47] | [JSON](61h_0sk_4pb.json) |
| `629_vqz_3ln` | 祖丁 | [《史記・殷本紀》][3] | [JSON](629_vqz_3ln.json) |
| `62z_e94_uw5` | 孫遬 | [《史記・曹相國世家》][36] | [JSON](62z_e94_uw5.json) |
| `631_4pw_giq` | 示瞇明（救趙盾者） | [《史記・晉世家》][21] | [JSON](631_4pw_giq.json) |
| `631_ags_hxe` | 鯁 | [《史記・韓世家》][27] | [JSON](631_ags_hxe.json) |
| `631_j7q_04t` | 天子 | [《史記・商君列傳》][50] | [JSON](631_j7q_04t.json) |
| `632_664_al2` | 夏說 | [《史記・曹相國世家》][36] | [JSON](632_664_al2.json) |
| `639_jt7_ns0` | 周蘭 | [《史記・高祖本紀》][8] | [JSON](639_jt7_ns0.json) |
| `63o_61u_6tf` | 項冠 | [《史記・傅靳蒯成列傳》][80] | [JSON](63o_61u_6tf.json) |
| `63o_tsj_qtc` | 泄鈞 | [《史記・趙世家》][25] | [JSON](63o_tsj_qtc.json) |
| `63v_kp5_pfj` | 樂（晉公子） | [《史記・晉世家》][21] | [JSON](63v_kp5_pfj.json) |
| `63x_7fc_69z` | 祭仲 | [《史記・鄭世家》][24] | [JSON](63x_7fc_69z.json) |
| `640_i2y_3qc` | 太卜未名 | [《史記・李斯列傳》][69] | [JSON](640_i2y_3qc.json) |
| `645_hym_djj` | 李夫人子昌邑王 | [《史記・外戚世家》][31] | [JSON](645_hym_djj.json) |
| `64c_hdt_bl8` | 惠文王 | [《史記・陳涉世家》][30] | [JSON](64c_hdt_bl8.json) |
| `64q_wka_hx1` | 齊桓引古未定 | [《史記・李斯列傳》][69] | [JSON](64q_wka_hx1.json) |
| `64t_pmo_3d4` | 太子未具名（兵事） | [《史記・田叔列傳》][86] | [JSON](64t_pmo_3d4.json) |
| `658_fyo_lfi` | 游孫 | [《史記・周本紀》][4] | [JSON](658_fyo_lfi.json) |
| `65f_dvi_ljt` | 桀 | [《史記・夏本紀》][2] | [JSON](65f_dvi_ljt.json) |
| `65g_u1c_0st` | 黥布 | [《史記・荊燕世家》][33] | [JSON](65g_u1c_0st.json) |
| `65q_ft7_2u1` | 燕狗屠未名 | [《史記・刺客列傳》][68] | [JSON](65q_ft7_2u1.json) |
| `65r_40m_v04` | 陳餘 | [《史記・張丞相列傳》][78] | [JSON](65r_40m_v04.json) |
| `65u_rbx_hst` | 游騰 | [《史記・樗里子甘茂列傳》][53] | [JSON](65u_rbx_hst.json) |
| `664_wah_z4z` | 黥布 | [《史記・樊酈滕灌列傳》][77] | [JSON](664_wah_z4z.json) |
| `667_fm8_khs` | 微（商先祖） | [《史記・殷本紀》][3] | [JSON](667_fm8_khs.json) |
| `66i_9gx_pc4` | 商瞿 | [《史記・仲尼弟子列傳》][49] | [JSON](66i_9gx_pc4.json) |
| `66l_m67_5ie` | 夏育 | [《史記・范睢蔡澤列傳》][61] | [JSON](66l_m67_5ie.json) |
| `66o_td0_2ox` | 孝文 | [《史記・韓信盧綰列傳》][75] | [JSON](66o_td0_2ox.json) |
| `66z_79l_gv6` | 桓公（燕襄公後） | [《史記・燕召公世家》][16] | [JSON](66z_79l_gv6.json) |
| `673_a1m_bhc` | 胡亥 | [《史記・張耳陳餘列傳》][71] | [JSON](673_a1m_bhc.json) |
| `67d_hkx_fvu` | 越女（楚惠王章母） | [《史記・楚世家》][22] | [JSON](67d_hkx_fvu.json) |
| `67k_3wh_j8c` | 魏絳（和戎臣） | [《史記・晉世家》][21] | [JSON](67k_3wh_j8c.json) |
| `67y_7vs_x2g` | 叔詹 | [《史記・鄭世家》][24] | [JSON](67y_7vs_x2g.json) |
| `68g_980_mer` | 劇孟 | [《史記・吳王濞列傳》][88] | [JSON](68g_980_mer.json) |
| `68u_x4k_2k4` | 張蒼 | [《史記・張丞相列傳》][78] | [JSON](68u_x4k_2k4.json) |
| `68y_cvr_pg1` | 呂媭 | [《史記・呂太后本紀》][9] | [JSON](68y_cvr_pg1.json) |
| `691_4u8_7bw` | 巴姬（楚共王埋璧者） | [《史記・楚世家》][22] | [JSON](691_4u8_7bw.json) |
| `694_r93_h9m` | 宋王（魏世家温死未名者） | [《史記・魏世家》][26] | [JSON](694_r93_h9m.json) |
| `697_9f9_d41` | 辟陽侯未詳名 | [《史記・酈生陸賈列傳》][79] | [JSON](697_9f9_d41.json) |
| `699_2t4_dcd` | 楊樛 | [《史記・秦始皇本紀》][6] | [JSON](699_2t4_dcd.json) |
| `699_ven_lj5` | 呂祿 | [《史記・樊酈滕灌列傳》][77] | [JSON](699_ven_lj5.json) |
| `69f_iaq_kzb` | 昭陽（楚柱國） | [《史記・楚世家》][22] | [JSON](69f_iaq_kzb.json) |
| `69q_8gz_nxe` | 田單 | [《史記・田單列傳》][64] | [JSON](69q_8gz_nxe.json) |
| `69v_q1z_72c` | 禹引古 | [《史記・屈原賈生列傳》][66] | [JSON](69v_q1z_72c.json) |
| `6a5_ca8_2a8` | 如意 | [《史記・張丞相列傳》][78] | [JSON](6a5_ca8_2a8.json) |
| `6a7_li3_zwm` | 靈王 | [《史記・周本紀》][4] | [JSON](6a7_li3_zwm.json) |
| `6a8_or0_gdl` | 莊王引古未定 | [《史記・春申君列傳》][60] | [JSON](6a8_or0_gdl.json) |
| `6af_362_yyq` | 皇后未詳名 | [《史記・外戚世家》][31] | [JSON](6af_362_yyq.json) |
| `6af_e19_epo` | 御史光 | [《史記・三王世家》][42] | [JSON](6af_e19_epo.json) |
| `6aj_h39_deu` | 秦太子 | [《史記・楚世家》][22] | [JSON](6aj_h39_deu.json) |
| `6au_wbx_fu3` | 韓昭侯 | [《史記・留侯世家》][37] | [JSON](6au_wbx_fu3.json) |
| `6aw_ppq_4x9` | 曹卹 | [《史記・仲尼弟子列傳》][49] | [JSON](6aw_ppq_4x9.json) |
| `6ax_bt5_t0u` | 李由 | [《史記・陳涉世家》][30] | [JSON](6ax_bt5_t0u.json) |
| `6bn_yfc_lzi` | 田叔 | [《史記・田叔列傳》][86] | [JSON](6bn_yfc_lzi.json) |
| `6bp_mr9_l3w` | 平陽主 | [《史記・田叔列傳》][86] | [JSON](6bp_mr9_l3w.json) |
| `6bt_r2x_97d` | 楚王（魏世家徙陳未名者） | [《史記・魏世家》][26] | [JSON](6bt_r2x_97d.json) |
| `6c5_di7_e68` | 孝惠帝 | [《史記・絳侯周勃世家》][39] | [JSON](6c5_di7_e68.json) |
| `6c6_lvq_rd4` | 大任 | [《史記・外戚世家》][31] | [JSON](6c6_lvq_rd4.json) |
| `6c7_5zy_3zt` | 丁疾 | [《史記・陳涉世家》][30] | [JSON](6c7_5zy_3zt.json) |
| `6cd_fed_sfz` | 唐眛 | [《史記・楚世家》][22]、[《史記・屈原賈生列傳》][66] | [JSON](6cd_fed_sfz.json) |
| `6cy_2mz_me0` | 郤至（鄢陵晉臣） | [《史記・晉世家》][21] | [JSON](6cy_2mz_me0.json) |
| `6d2_kut_dhh` | 武王 | [《史記・周本紀》][4] | [JSON](6d2_kut_dhh.json) |
| `6d7_k17_86x` | 楚相唐眛 | [《史記・樂毅列傳》][62] | [JSON](6d7_k17_86x.json) |
| `6da_ad5_2s8` | 平陽君 | [《史記・平原君虞卿列傳》][58] | [JSON](6da_ad5_2s8.json) |
| `6db_083_t88` | 侍者未名（袁盎） | [《史記・袁盎鼂錯列傳》][83] | [JSON](6db_083_t88.json) |
| `6ds_5ek_8sw` | 劉禮 | [《史記・袁盎鼂錯列傳》][83] | [JSON](6ds_5ek_8sw.json) |
| `6ek_pen_a4x` | 楊熊 | [《史記・傅靳蒯成列傳》][80] | [JSON](6ek_pen_a4x.json) |
| `6f4_vqj_dgu` | 痤 | [《史記・趙世家》][25] | [JSON](6f4_vqj_dgu.json) |
| `6f9_sts_981` | 公孫閲 | [《史記・田敬仲完世家》][28] | [JSON](6f9_sts_981.json) |
| `6fo_fh6_ckq` | 楚王（韓世家修魚議論未名者） | [《史記・韓世家》][27] | [JSON](6fo_fh6_ckq.json) |
| `6gi_f63_kiu` | 季魴侯 | [《史記・齊太公世家》][14] | [JSON](6gi_f63_kiu.json) |
| `6gt_7z8_hup` | 召平 | [《史記・呂太后本紀》][9] | [JSON](6gt_7z8_hup.json) |
| `6h5_lou_110` | 通（救楚秦客卿） | [《史記・楚世家》][22] | [JSON](6h5_lou_110.json) |
| `6hd_nol_p5r` | 狐毛（重耳從者） | [《史記・晉世家》][21] | [JSON](6hd_nol_p5r.json) |
| `6hn_lac_kwl` | 尉繚 | [《史記・秦始皇本紀》][6] | [JSON](6hn_lac_kwl.json) |
| `6hq_bb2_3rb` | 扁鵲 | [《史記・扁鵲倉公列傳》][87] | [JSON](6hq_bb2_3rb.json) |
| `6hu_5eu_5t3` | 馮梁 | [《史記・樊酈滕灌列傳》][77] | [JSON](6hu_5eu_5t3.json) |
| `6i8_efe_yzr` | 燕將保聊城未名 | [《史記・魯仲連鄒陽列傳》][65] | [JSON](6i8_efe_yzr.json) |
| `6in_5g6_f6d` | 趙高 | [《史記・劉敬叔孫通列傳》][81] | [JSON](6in_5g6_f6d.json) |
| `6ip_dr3_fbl` | 禹 | [《史記・夏本紀》][2] | [JSON](6ip_dr3_fbl.json) |
| `6j7_udm_uq6` | 齊湣王 | [《史記・蘇秦列傳》][51] | [JSON](6j7_udm_uq6.json) |
| `6jz_eg8_plz` | 申功 | [《史記・孝武本紀》][12] | [JSON](6jz_eg8_plz.json) |
| `6k3_ylu_5tf` | 差弗 | [《史記・周本紀》][4] | [JSON](6k3_ylu_5tf.json) |
| `6kj_g6a_tau` | 馮驩 | [《史記・孟嘗君列傳》][57] | [JSON](6kj_g6a_tau.json) |
| `6l4_h2o_qll` | 后稷 | [《史記・劉敬叔孫通列傳》][81] | [JSON](6l4_h2o_qll.json) |
| `6l6_hg3_38c` | 龍且 | [《史記・高祖本紀》][8] | [JSON](6l6_hg3_38c.json) |
| `6lf_vzz_61d` | 不降 | [《史記・夏本紀》][2] | [JSON](6lf_vzz_61d.json) |
| `6lg_orw_k7o` | 趙惠文王 | [《史記・趙世家》][25] | [JSON](6lg_orw_k7o.json) |
| `6lu_kih_t5b` | 齊襄王 | [《史記・孟子荀卿列傳》][56] | [JSON](6lu_kih_t5b.json) |
| `6mm_1pn_fhf` | 秦武王 | [《史記・張儀列傳》][52] | [JSON](6mm_1pn_fhf.json) |
| `6mm_oky_qqa` | 仲孫（齊使） | [《史記・齊太公世家》][14] | [JSON](6mm_oky_qqa.json) |
| `6mp_ckp_omx` | 侍者（楚靈王問愛子者） | [《史記・楚世家》][22] | [JSON](6mp_ckp_omx.json) |
| `6mp_d5b_nax` | 華毋傷 | [《史記・樊酈滕灌列傳》][77] | [JSON](6mp_d5b_nax.json) |
| `6mv_qs6_u86` | 宋子主人家丈人未名 | [《史記・刺客列傳》][68] | [JSON](6mv_qs6_u86.json) |
| `6mx_6a9_sa9` | 王吸 | [《史記・高祖本紀》][8] | [JSON](6mx_6a9_sa9.json) |
| `6n5_bpu_v5a` | 王綰 | [《史記・秦始皇本紀》][6] | [JSON](6n5_bpu_v5a.json) |
| `6nb_nln_q3c` | 竇后母 | [《史記・外戚世家》][31] | [JSON](6nb_nln_q3c.json) |
| `6nc_iwu_8b0` | 楚莊王 | [《史記・楚世家》][22] | [JSON](6nc_iwu_8b0.json) |
| `6o1_fcy_vcy` | 虢石父 | [《史記・周本紀》][4] | [JSON](6o1_fcy_vcy.json) |
| `6o2_xmb_367` | 視廉頗趙使者未名 | [《史記・廉頗藺相如列傳》][63] | [JSON](6o2_xmb_367.json) |
| `6ok_4l3_7h8` | 成 | [《史記・蘇秦列傳》][51] | [JSON](6ok_4l3_7h8.json) |
| `6p4_9oc_1a9` | 周公忌父（禮惠公使者） | [《史記・晉世家》][21] | [JSON](6p4_9oc_1a9.json) |
| `6p8_djv_2oj` | 公戶滿意 | [《史記・三王世家》][42] | [JSON](6p8_djv_2oj.json) |
| `6pb_ld3_dg2` | 宣公（燕桓公後） | [《史記・燕召公世家》][16] | [JSON](6pb_ld3_dg2.json) |
| `6pj_g2n_v7a` | 外壬 | [《史記・殷本紀》][3] | [JSON](6pj_g2n_v7a.json) |
| `6pr_ztz_o62` | 鄖公（昭王出奔時） | [《史記・吳太伯世家》][13] | [JSON](6pr_ztz_o62.json) |
| `6pz_7ge_y2n` | 黥布 | [《史記・陳涉世家》][30] | [JSON](6pz_7ge_y2n.json) |
| `6q3_5d1_jsc` | 友 | [《史記・齊悼惠王世家》][34] | [JSON](6q3_5d1_jsc.json) |
| `6qu_ijl_anf` | 季姬（季康子妹） | [《史記・齊太公世家》][14] | [JSON](6qu_ijl_anf.json) |
| `6qw_s6t_pib` | 王臧 | [《史記・萬石張叔列傳》][85] | [JSON](6qw_s6t_pib.json) |
| `6r7_9o6_c1i` | 田橫 | [《史記・田儋列傳》][76] | [JSON](6r7_9o6_c1i.json) |
| `6rk_dgb_df6` | 韓萬（曲沃殺哀侯者） | [《史記・晉世家》][21] | [JSON](6rk_dgb_df6.json) |
| `6ry_qb7_2ur` | 韋孟 | [《史記・楚元王世家》][32] | [JSON](6ry_qb7_2ur.json) |
| `6s6_l25_zty` | 秦王政 | [《史記・魏世家》][26] | [JSON](6s6_l25_zty.json) |
| `6se_oxf_lfu` | 蘇從（楚莊王諫臣） | [《史記・楚世家》][22] | [JSON](6se_oxf_lfu.json) |
| `6sl_m8t_cxz` | 王武 | [《史記・樊酈滕灌列傳》][77] | [JSON](6sl_m8t_cxz.json) |
| `6tr_abu_yi3` | 蘇秦從者 | [《史記・蘇秦列傳》][51] | [JSON](6tr_abu_yi3.json) |
| `6u1_ku8_gw2` | 雍廩 | [《史記・秦本紀》][5] | [JSON](6u1_ku8_gw2.json) |
| `6u2_boa_dbm` | 子之 | [《史記・趙世家》][25] | [JSON](6u2_boa_dbm.json) |
| `6u6_x1f_xgg` | 季桓子 | [《史記・孔子世家》][29] | [JSON](6u6_x1f_xgg.json) |
| `6ub_tha_gkr` | 髙 | [《史記・越王勾踐世家》][23] | [JSON](6ub_tha_gkr.json) |
| `6us_ibm_u05` | 陳嬰 | [《史記・項羽本紀》][7] | [JSON](6us_ibm_u05.json) |
| `6v4_57w_76j` | 石奮母未名 | [《史記・萬石張叔列傳》][85] | [JSON](6v4_57w_76j.json) |
| `6ve_ik8_jv8` | 魏豹 | [《史記・魏豹彭越列傳》][72] | [JSON](6ve_ik8_jv8.json) |
| `6w8_1nb_1wo` | 夷皋之母（趙世家未名者） | [《史記・趙世家》][25] | [JSON](6w8_1nb_1wo.json) |
| `6wr_5vs_sge` | 虢公丑（亡周者） | [《史記・晉世家》][21] | [JSON](6wr_5vs_sge.json) |
| `6x9_ucz_nl2` | 文公（燕桓公後） | [《史記・燕召公世家》][16] | [JSON](6x9_ucz_nl2.json) |
| `6xf_5sb_pd8` | 石乞 | [《史記・伍子胥列傳》][48] | [JSON](6xf_5sb_pd8.json) |
| `6xn_8k7_kse` | 主癸 | [《史記・殷本紀》][3] | [JSON](6xn_8k7_kse.json) |
| `6yh_04q_wda` | 召平 | [《史記・項羽本紀》][7] | [JSON](6yh_04q_wda.json) |
| `6yt_2tn_8zg` | 衞元君 | [《史記・刺客列傳》][68] | [JSON](6yt_2tn_8zg.json) |
| `6yy_w3j_hb2` | 徐越 | [《史記・趙世家》][25] | [JSON](6yy_w3j_hb2.json) |
| `6za_ai0_6dp` | 太公（季札論樂稱） | [《史記・吳太伯世家》][13] | [JSON](6za_ai0_6dp.json) |
| `6zc_puw_3ua` | 鑿（晉出公） | [《史記・晉世家》][21] | [JSON](6zc_puw_3ua.json) |
| `6zf_2fu_9xy` | 王賁 | [《史記・趙世家》][25] | [JSON](6zf_2fu_9xy.json) |
| `6zj_q8y_4ic` | 燕昭王 | [《史記・蘇秦列傳》][51] | [JSON](6zj_q8y_4ic.json) |
| `6zw_vkw_sxz` | 高后 | [《史記・吳王濞列傳》][88] | [JSON](6zw_vkw_sxz.json) |
| `6zy_q58_1rh` | 栗姬 | [《史記・外戚世家》][31] | [JSON](6zy_q58_1rh.json) |
| `70v_82v_y7m` | 韓武子 | [《史記・鄭世家》][24] | [JSON](70v_82v_y7m.json) |
| `716_g9k_cg4` | 穆生 | [《史記・楚元王世家》][32] | [JSON](716_g9k_cg4.json) |
| `718_52s_bo3` | 齊湣王 | [《史記・張儀列傳》][52] | [JSON](718_52s_bo3.json) |
| `71k_260_g1p` | 呂望 | [《史記・劉敬叔孫通列傳》][81] | [JSON](71k_260_g1p.json) |
| `71l_l4m_9m5` | 周青臣 | [《史記・秦始皇本紀》][6]、[《史記・李斯列傳》][69] | [JSON](71l_l4m_9m5.json) |
| `71m_zie_vnr` | 袁濤涂 | [《史記・齊太公世家》][14] | [JSON](71m_zie_vnr.json) |
| `71u_x7f_gpq` | 荀息 | [《史記・鄭世家》][24] | [JSON](71u_x7f_gpq.json) |
| `72m_dhb_tf7` | 漢元帝 | [《史記・張丞相列傳》][78] | [JSON](72m_dhb_tf7.json) |
| `72v_2mg_72h` | 衛靈公（蔡會邵陵記事） | [《史記・管蔡世家》][17] | [JSON](72v_2mg_72h.json) |
| `737_irc_rz7` | 張敖前姬（未名） | [《史記・呂太后本紀》][9] | [JSON](737_irc_rz7.json) |
| `73a_qx5_k2c` | 豐王 | [《史記・秦本紀》][5] | [JSON](73a_qx5_k2c.json) |
| `73j_rq4_ugv` | 閼氏 | [《史記・陳丞相世家》][38] | [JSON](73j_rq4_ugv.json) |
| `741_7st_iab` | 漢孝惠帝 | [《史記・張耳陳餘列傳》][71] | [JSON](741_7st_iab.json) |
| `743_4lh_p0l` | 蹇叔引古 | [《史記・李斯列傳》][69] | [JSON](743_4lh_p0l.json) |
| `746_tyc_8dd` | 黃帝脈書引稱 | [《史記・扁鵲倉公列傳》][87] | [JSON](746_tyc_8dd.json) |
| `74z_fwh_7yq` | 樊穆仲 | [《史記・魯周公世家》][15] | [JSON](74z_fwh_7yq.json) |
| `75i_qx7_fod` | 荷蓧丈人 | [《史記・仲尼弟子列傳》][49] | [JSON](75i_qx7_fod.json) |
| `75z_auw_aaj` | 趙豹 | [《史記・趙世家》][25] | [JSON](75z_auw_aaj.json) |
| `772_pdn_60l` | 絳侯 | [《史記・外戚世家》][31] | [JSON](772_pdn_60l.json) |
| `77g_feh_ev3` | 蘇角 | [《史記・項羽本紀》][7] | [JSON](77g_feh_ev3.json) |
| `77k_lwd_yfy` | 襄彊 | [《史記・陳涉世家》][30] | [JSON](77k_lwd_yfy.json) |
| `77o_my6_sxt` | 王夫人趙人 | [《史記・外戚世家》][31] | [JSON](77o_my6_sxt.json) |
| `78c_udb_chz` | 周元王 | [《史記・越王勾踐世家》][23] | [JSON](78c_udb_chz.json) |
| `78j_6yv_eaf` | 黔牟（衛君） | [《史記・衛康叔世家》][19] | [JSON](78j_6yv_eaf.json) |
| `78k_der_mz8` | 王陵 | [《史記・陳丞相世家》][38] | [JSON](78k_der_mz8.json) |
| `79h_j8x_96s` | 燕后（趙世家未名者） | [《史記・趙世家》][25] | [JSON](79h_j8x_96s.json) |
| `79o_p9o_a9a` | 韓公叔 | [《史記・周本紀》][4] | [JSON](79o_p9o_a9a.json) |
| `79p_ubr_lij` | 范獻子 | [《史記・魏世家》][26] | [JSON](79p_ubr_lij.json) |
| `7a3_95s_58p` | 聶政 | [《史記・韓世家》][27] | [JSON](7a3_95s_58p.json) |
| `7a4_dik_1f3` | 趙肅侯（蘇秦記事） | [《史記・燕召公世家》][16] | [JSON](7a4_dik_1f3.json) |
| `7a9_wo3_vlp` | 達巷童子（孔子世家未名者） | [《史記・孔子世家》][29] | [JSON](7a9_wo3_vlp.json) |
| `7ak_v0v_9b7` | 楚太子傅未名 | [《史記・春申君列傳》][60] | [JSON](7ak_v0v_9b7.json) |
| `7as_qo0_b5u` | 齊景公 | [《史記・齊太公世家》][14] | [JSON](7as_qo0_b5u.json) |
| `7bk_jpm_vgm` | 荀櫟（范中行之仇） | [《史記・晉世家》][21] | [JSON](7bk_jpm_vgm.json) |
| `7bs_2iz_9rk` | 公歛處父 | [《史記・孔子世家》][29] | [JSON](7bs_2iz_9rk.json) |
| `7bu_r9j_p1d` | 孟嘗齊君 | [《史記・平原君虞卿列傳》][58] | [JSON](7bu_r9j_p1d.json) |
| `7c4_6v2_yvm` | 子貢 | [《史記・仲尼弟子列傳》][49] | [JSON](7c4_6v2_yvm.json) |
| `7c7_u2o_px7` | 蘇代 | [《史記・白起王翦列傳》][55] | [JSON](7c7_u2o_px7.json) |
| `7cf_b22_wao` | 范痤 | [《史記・魏世家》][26] | [JSON](7cf_b22_wao.json) |
| `7ck_5iz_er1` | 張春 | [《史記・高祖本紀》][8] | [JSON](7ck_5iz_er1.json) |
| `7d0_1pe_vkv` | 燕昭王 | [《史記・趙世家》][25] | [JSON](7d0_1pe_vkv.json) |
| `7d6_5it_vnr` | 夏黃公 | [《史記・留侯世家》][37] | [JSON](7d6_5it_vnr.json) |
| `7da_a9c_neu` | 宋留 | [《史記・陳涉世家》][30] | [JSON](7da_a9c_neu.json) |
| `7dn_nar_2m5` | 王陵母 | [《史記・陳丞相世家》][38] | [JSON](7dn_nar_2m5.json) |
| `7eu_sd1_8qe` | 韓宣王 | [《史記・蘇秦列傳》][51] | [JSON](7eu_sd1_8qe.json) |
| `7f0_iw2_xq3` | 信期 | [《史記・趙世家》][25] | [JSON](7f0_iw2_xq3.json) |
| `7ff_u3q_0hy` | 樊須 | [《史記・仲尼弟子列傳》][49] | [JSON](7ff_u3q_0hy.json) |
| `7fj_v15_1ej` | 馬服子 | [《史記・韓世家》][27] | [JSON](7fj_v15_1ej.json) |
| `7ge_psz_ic9` | 茅蘭 | [《史記・梁孝王世家》][40] | [JSON](7ge_psz_ic9.json) |
| `7gg_m5f_ub1` | 孝武皇帝 | [《史記・屈原賈生列傳》][66] | [JSON](7gg_m5f_ub1.json) |
| `7gs_9lq_cdp` | 萬章 | [《史記・孟子荀卿列傳》][56] | [JSON](7gs_9lq_cdp.json) |
| `7gw_5nr_iqq` | 荀卿 | [《史記・老子韓非列傳》][45] | [JSON](7gw_5nr_iqq.json) |
| `7gz_q9f_d37` | 鄭莊公 | [《史記・周本紀》][4] | [JSON](7gz_q9f_d37.json) |
| `7hd_xs5_eks` | 蚩尤 | [《史記・酈生陸賈列傳》][79] | [JSON](7hd_xs5_eks.json) |
| `7he_05e_e75` | 叔向（楚篇議子比者） | [《史記・楚世家》][22] | [JSON](7he_05e_e75.json) |
| `7hi_gqd_koj` | 彭祖 | [《史記・五帝本紀》][1] | [JSON](7hi_gqd_koj.json) |
| `7hl_jbv_m5y` | 子駟 | [《史記・鄭世家》][24] | [JSON](7hl_jbv_m5y.json) |
| `7i7_yuy_aif` | 韓釐王 | [《史記・留侯世家》][37] | [JSON](7i7_yuy_aif.json) |
| `7ih_43x_9sa` | 楚頃王（魯頃公記事） | [《史記・魯周公世家》][15] | [JSON](7ih_43x_9sa.json) |
| `7ii_vxr_vet` | 叔虞母（武王夢子敘事） | [《史記・晉世家》][21] | [JSON](7ii_vxr_vet.json) |
| `7il_k45_hze` | 五父（蔡人所殺者） | [《史記・陳杞世家》][18] | [JSON](7il_k45_hze.json) |
| `7iw_e5e_9e5` | 罷軍 | [《史記・齊悼惠王世家》][34] | [JSON](7iw_e5e_9e5.json) |
| `7iw_jix_h9n` | 曹咎 | [《史記・魏豹彭越列傳》][72] | [JSON](7iw_jix_h9n.json) |
| `7j8_d3i_ond` | 公子卬 | [《史記・趙世家》][25]、[《史記・魏世家》][26] | [JSON](7j8_d3i_ond.json) |
| `7jn_lg6_yg9` | 賈生（陳涉世家褚氏引文署稱未名者） | [《史記・陳涉世家》][30] | [JSON](7jn_lg6_yg9.json) |
| `7js_9iu_itl` | 南宮敬叔 | [《史記・孔子世家》][29] | [JSON](7js_9iu_itl.json) |
| `7jv_pwp_se2` | 少康 | [《史記・吳太伯世家》][13] | [JSON](7jv_pwp_se2.json) |
| `7ki_x83_hpc` | 杜摯 | [《史記・秦本紀》][5]、[《史記・商君列傳》][50] | [JSON](7ki_x83_hpc.json) |
| `7kl_if8_wye` | 公孫臣 | [《史記・張丞相列傳》][78] | [JSON](7kl_if8_wye.json) |
| `7kx_pw4_7mz` | 公甫家相室未名 | [《史記・平原君虞卿列傳》][58] | [JSON](7kx_pw4_7mz.json) |
| `7l6_9t8_q1p` | 莊王 | [《史記・周本紀》][4] | [JSON](7l6_9t8_q1p.json) |
| `7l9_yz7_nwv` | 吳王未具名 | [《史記・袁盎鼂錯列傳》][83] | [JSON](7l9_yz7_nwv.json) |
| `7lc_ham_b1m` | 太子完考烈王 | [《史記・春申君列傳》][60] | [JSON](7lc_ham_b1m.json) |
| `7m7_ebn_vli` | 司馬穰苴 | [《史記・司馬穰苴列傳》][46] | [JSON](7m7_ebn_vli.json) |
| `7m7_qvm_4oj` | 召公奭 | [《史記・燕召公世家》][16] | [JSON](7m7_qvm_4oj.json) |
| `7md_vp9_mh6` | 晁錯 | [《史記・袁盎鼂錯列傳》][83] | [JSON](7md_vp9_mh6.json) |
| `7mh_byk_zx4` | 矯子庸疵 | [《史記・仲尼弟子列傳》][49] | [JSON](7mh_byk_zx4.json) |
| `7mh_pz3_7ja` | 籍秦 | [《史記・趙世家》][25] | [JSON](7mh_pz3_7ja.json) |
| `7mw_nab_5z6` | 淮陰（用稱） | [《史記・韓信盧綰列傳》][75] | [JSON](7mw_nab_5z6.json) |
| `7n2_guq_6ri` | 魏子 | [《史記・孟嘗君列傳》][57] | [JSON](7n2_guq_6ri.json) |
| `7nr_u9c_hkv` | 濟北王（武帝封禪時未名） | [《史記・孝武本紀》][12] | [JSON](7nr_u9c_hkv.json) |
| `7o6_to6_t8j` | 皋陶（引古疑問） | [《史記・黥布列傳》][73] | [JSON](7o6_to6_t8j.json) |
| `7of_rv0_ayn` | 李克 | [《史記・孫子吳起列傳》][47] | [JSON](7of_rv0_ayn.json) |
| `7ok_zhn_ztl` | 劇辛 | [《史記・趙世家》][25] | [JSON](7ok_zhn_ztl.json) |
| `7oo_7ou_iqf` | 廉頗 | [《史記・范睢蔡澤列傳》][61] | [JSON](7oo_7ou_iqf.json) |
| `7ou_w2x_zxh` | 宋公 | [《史記・穰侯列傳》][54] | [JSON](7ou_w2x_zxh.json) |
| `7oz_44p_91g` | 孟賁（引古） | [《史記・淮陰侯列傳》][74] | [JSON](7oz_44p_91g.json) |
| `7p1_uko_gaz` | 呂后 | [《史記・張丞相列傳》][78] | [JSON](7p1_uko_gaz.json) |
| `7pl_s0g_rkh` | 孟嘗君薛文 | [《史記・孟嘗君列傳》][57] | [JSON](7pl_s0g_rkh.json) |
| `7pz_aqk_pf6` | 須賈 | [《史記・穰侯列傳》][54] | [JSON](7pz_aqk_pf6.json) |
| `7q0_00l_ra0` | 比干引古 | [《史記・李斯列傳》][69] | [JSON](7q0_00l_ra0.json) |
| `7q5_0n4_mjt` | 趙王 | [《史記・齊悼惠王世家》][34] | [JSON](7q5_0n4_mjt.json) |
| `7q8_n5b_w58` | 石曼尃（衛逐君者） | [《史記・衛康叔世家》][19] | [JSON](7q8_n5b_w58.json) |
| `7qj_amj_139` | 薛公（魏世家未名者） | [《史記・魏世家》][26] | [JSON](7qj_amj_139.json) |
| `7r3_6s9_pcv` | 漢髙帝 | [《史記・越王勾踐世家》][23] | [JSON](7r3_6s9_pcv.json) |
| `7r3_beh_4ty` | 秦昭王 | [《史記・韓世家》][27] | [JSON](7r3_beh_4ty.json) |
| `7rl_p9k_ood` | 褚先生（陳涉世家附載署稱未名者） | [《史記・陳涉世家》][30] | [JSON](7rl_p9k_ood.json) |
| `7ry_vg8_a0d` | 王廖 | [《史記・陳涉世家》][30] | [JSON](7ry_vg8_a0d.json) |
| `7s0_f3b_8hp` | 公子政 | [《史記・魏世家》][26] | [JSON](7s0_f3b_8hp.json) |
| `7s0_vhn_yay` | 項梁 | [《史記・酈生陸賈列傳》][79] | [JSON](7s0_vhn_yay.json) |
| `7s1_ctn_j9k` | 鄭袖 | [《史記・張儀列傳》][52] | [JSON](7s1_ctn_j9k.json) |
| `7s1_uqc_cgq` | 墨翟 | [《史記・陳涉世家》][30] | [JSON](7s1_uqc_cgq.json) |
| `7se_ujg_epu` | 太史公 | [《史記・絳侯周勃世家》][39] | [JSON](7se_ujg_epu.json) |
| `7sn_e31_tv8` | 種首 | [《史記・田敬仲完世家》][28] | [JSON](7sn_e31_tv8.json) |
| `7sp_0wy_o3j` | 韓悼惠王 | [《史記・留侯世家》][37] | [JSON](7sp_0wy_o3j.json) |
| `7st_a3s_dis` | 司馬夷 | [《史記・樊酈滕灌列傳》][77] | [JSON](7st_a3s_dis.json) |
| `7st_hlk_scq` | 渾良夫（孔氏豎） | [《史記・衛康叔世家》][19] | [JSON](7st_hlk_scq.json) |
| `7st_ix6_uvb` | 王生 | [《史記・張釋之馮唐列傳》][84] | [JSON](7st_ix6_uvb.json) |
| `7te_st3_3xk` | 項羽 | [《史記・外戚世家》][31] | [JSON](7te_st3_3xk.json) |
| `7tn_7ia_95n` | 亭長妻未名 | [《史記・淮陰侯列傳》][74] | [JSON](7tn_7ia_95n.json) |
| `7ul_aeb_w4e` | 丁公 | [《史記・季布欒布列傳》][82] | [JSON](7ul_aeb_w4e.json) |
| `7v2_mrf_ojp` | 小白 | [《史記・越王勾踐世家》][23] | [JSON](7v2_mrf_ojp.json) |
| `7v9_n58_3l5` | 田橫 | [《史記・樊酈滕灌列傳》][77] | [JSON](7v9_n58_3l5.json) |
| `7vi_sab_7i7` | 呉太子（越世家黃池留守未名者） | [《史記・越王勾踐世家》][23] | [JSON](7vi_sab_7i7.json) |
| `7vk_c99_qcj` | 呂勝 | [《史記・項羽本紀》][7] | [JSON](7vk_c99_qcj.json) |
| `7vn_izu_nhv` | 韓武子（楚篇三晉記事） | [《史記・楚世家》][22] | [JSON](7vn_izu_nhv.json) |
| `7wj_a59_ofd` | 趙君（京兆尹） | [《史記・張丞相列傳》][78] | [JSON](7wj_a59_ofd.json) |
| `7wk_awi_f4x` | 單于未詳名 | [《史記・酈生陸賈列傳》][79] | [JSON](7wk_awi_f4x.json) |
| `7x0_k51_hpv` | 文王醫案候選 | [《史記・扁鵲倉公列傳》][87] | [JSON](7x0_k51_hpv.json) |
| `7x2_x55_1b6` | 蚩尤 | [《史記・五帝本紀》][1] | [JSON](7x2_x55_1b6.json) |
| `7xa_un5_pdp` | 昧 | [《史記・鄭世家》][24] | [JSON](7xa_un5_pdp.json) |
| `7xt_xw9_q0r` | 項羽 | [《史記・項羽本紀》][7] | [JSON](7xt_xw9_q0r.json) |
| `7xy_9gg_opk` | 李斯 | [《史記・李斯列傳》][69] | [JSON](7xy_9gg_opk.json) |
| `7y1_9ih_ndo` | 公叔祖類 | [《史記・周本紀》][4] | [JSON](7y1_9ih_ndo.json) |
| `7yv_ale_8x8` | 風后 | [《史記・五帝本紀》][1]、[《史記・孝武本紀》][12] | [JSON](7yv_ale_8x8.json) |
| `7yw_3hb_kj0` | 龐煖（趙將） | [《史記・燕召公世家》][16] | [JSON](7yw_3hb_kj0.json) |
| `7z0_oil_c91` | 禹 | [《史記・越王勾踐世家》][23] | [JSON](7z0_oil_c91.json) |
| `7ze_tjk_sc8` | 程嬰 | [《史記・趙世家》][25] | [JSON](7ze_tjk_sc8.json) |
| `7zk_y8t_6l9` | 張儀 | [《史記・蘇秦列傳》][51] | [JSON](7zk_y8t_6l9.json) |
| `7zq_926_dnw` | 劉澤 | [《史記・三王世家》][42] | [JSON](7zq_926_dnw.json) |
| `7zv_9sd_gug` | 趙朔（下軍將） | [《史記・趙世家》][25] | [JSON](7zv_9sd_gug.json) |
| `80h_7uw_251` | 祖己 | [《史記・殷本紀》][3] | [JSON](80h_7uw_251.json) |
| `813_xhq_hmb` | 齊桓公引古 | [《史記・范睢蔡澤列傳》][61] | [JSON](813_xhq_hmb.json) |
| `816_kfm_jer` | 周太史（田世家卜完未名者） | [《史記・田敬仲完世家》][28] | [JSON](816_kfm_jer.json) |
| `81b_bpq_qcv` | 周武王 | [《史記・劉敬叔孫通列傳》][81] | [JSON](81b_bpq_qcv.json) |
| `81n_sfg_u64` | 齊釐公 | [《史記・鄭世家》][24] | [JSON](81n_sfg_u64.json) |
| `822_l2b_8aq` | 鄧說 | [《史記・陳涉世家》][30] | [JSON](822_l2b_8aq.json) |
| `82f_v64_vcn` | 楊端和 | [《史記・秦始皇本紀》][6] | [JSON](82f_v64_vcn.json) |
| `82r_i62_9f9` | 成安君未詳名 | [《史記・酈生陸賈列傳》][79] | [JSON](82r_i62_9f9.json) |
| `830_x2v_h3v` | 慶封 | [《史記・齊太公世家》][14] | [JSON](830_x2v_h3v.json) |
| `831_9kk_gnr` | 齊太史弟（復書被殺未名） | [《史記・齊太公世家》][14] | [JSON](831_9kk_gnr.json) |
| `83h_9bz_3je` | 隗林 | [《史記・秦始皇本紀》][6] | [JSON](83h_9bz_3je.json) |
| `83k_5bc_a7g` | 項聲 | [《史記・黥布列傳》][73] | [JSON](83k_5bc_a7g.json) |
| `840_l2v_yep` | 華元（宋右師） | [《史記・宋微子世家》][20] | [JSON](840_l2v_yep.json) |
| `841_xi4_je8` | 荀寅 | [《史記・趙世家》][25] | [JSON](841_xi4_je8.json) |
| `846_l8f_x6q` | 蘇秦引古 | [《史記・魯仲連鄒陽列傳》][65] | [JSON](846_l8f_x6q.json) |
| `84r_unt_2kk` | 曼丘臣 | [《史記・韓信盧綰列傳》][75] | [JSON](84r_unt_2kk.json) |
| `84v_f1t_rm0` | 公子糾 | [《史記・齊太公世家》][14] | [JSON](84v_f1t_rm0.json) |
| `84w_57j_1n6` | 德侯宗正未具名 | [《史記・吳王濞列傳》][88] | [JSON](84w_57j_1n6.json) |
| `84x_1ix_p37` | 令勉（中大夫） | [《史記・孝文本紀》][10] | [JSON](84x_1ix_p37.json) |
| `84x_bfx_b8h` | 孔子 | [《史記・樗里子甘茂列傳》][53] | [JSON](84x_bfx_b8h.json) |
| `85i_mqq_7az` | 燕王書信未名 | [《史記・吳王濞列傳》][88] | [JSON](85i_mqq_7az.json) |
| `863_cee_u4m` | 盧綰 | [《史記・韓信盧綰列傳》][75] | [JSON](863_cee_u4m.json) |
| `865_tu4_a4b` | 平陽侯窋 | [《史記・呂太后本紀》][9] | [JSON](865_tu4_a4b.json) |
| `86n_f7d_f7h` | 淖姬 | [《史記・五宗世家》][41] | [JSON](86n_f7d_f7h.json) |
| `86t_kt8_pzq` | 要離引古 | [《史記・魯仲連鄒陽列傳》][65] | [JSON](86t_kt8_pzq.json) |
| `86x_xyw_vsx` | 雍巫 | [《史記・齊太公世家》][14] | [JSON](86x_xyw_vsx.json) |
| `87m_0rf_gep` | 屈匄（楚大將軍） | [《史記・楚世家》][22] | [JSON](87m_0rf_gep.json) |
| `87m_fib_7uw` | 項羽 | [《史記・項羽本紀》][7] | [JSON](87m_fib_7uw.json) |
| `87n_vk2_1ig` | 李少君 | [《史記・孝武本紀》][12] | [JSON](87n_vk2_1ig.json) |
| `87x_kxf_d86` | 所忠 | [《史記・五宗世家》][41] | [JSON](87x_kxf_d86.json) |
| `883_auv_cl0` | 姬宋（燕惠公所寵） | [《史記・燕召公世家》][16] | [JSON](883_auv_cl0.json) |
| `883_mfp_qi1` | 曹姓（陸終子稱） | [《史記・楚世家》][22] | [JSON](883_mfp_qi1.json) |
| `88a_evh_42n` | 少康 | [《史記・越王勾踐世家》][23] | [JSON](88a_evh_42n.json) |
| `88j_vat_t9z` | 閼氏未名 | [《史記・韓信盧綰列傳》][75] | [JSON](88j_vat_t9z.json) |
| `88o_bkx_z5h` | 燕王喜（引古） | [《史記・蒙恬列傳》][70] | [JSON](88o_bkx_z5h.json) |
| `88t_ocd_fva` | 太史趙（晉平公問者） | [《史記・陳杞世家》][18] | [JSON](88t_ocd_fva.json) |
| `88w_qqj_hs8` | 朱亥 | [《史記・魏公子列傳》][59] | [JSON](88w_qqj_hs8.json) |
| `89e_iub_u5e` | 齊王 | [《史記・荊燕世家》][33] | [JSON](89e_iub_u5e.json) |
| `89q_9ev_4g6` | 左車（周昌後裔） | [《史記・孝景本紀》][11] | [JSON](89q_9ev_4g6.json) |
| `89y_y9f_yw0` | 太史公 | [《史記・齊悼惠王世家》][34] | [JSON](89y_y9f_yw0.json) |
| `8a9_3wc_bf6` | 許君（楚成王伐許時未名） | [《史記・楚世家》][22] | [JSON](8a9_3wc_bf6.json) |
| `8a9_tj8_6i7` | 箕子 | [《史記・宋微子世家》][20] | [JSON](8a9_tj8_6i7.json) |
| `8ai_yuw_oyp` | 魏文侯 | [《史記・樂毅列傳》][62] | [JSON](8ai_yuw_oyp.json) |
| `8an_gej_gnk` | 高昭子 | [《史記・齊太公世家》][14] | [JSON](8an_gej_gnk.json) |
| `8b2_83x_21q` | 鍼季 | [《史記・魯周公世家》][15] | [JSON](8b2_83x_21q.json) |
| `8bo_1e6_bs3` | 呂臺 | [《史記・齊悼惠王世家》][34] | [JSON](8bo_1e6_bs3.json) |
| `8bp_7m7_8zj` | 成開方 | [《史記・扁鵲倉公列傳》][87] | [JSON](8bp_7m7_8zj.json) |
| `8bq_3qv_7hb` | 魏惠王 | [《史記・韓世家》][27] | [JSON](8bq_3qv_7hb.json) |
| `8dd_6r9_hz4` | 汝南王 | [《史記・孝景本紀》][11] | [JSON](8dd_6r9_hz4.json) |
| `8dt_xw6_0pu` | 井伯（虞大夫） | [《史記・晉世家》][21] | [JSON](8dt_xw6_0pu.json) |
| `8e4_llb_ya6` | 龍且 | [《史記・陳丞相世家》][38] | [JSON](8e4_llb_ya6.json) |
| `8eh_dw1_jzp` | 孔子引述 | [《史記・呂不韋列傳》][67] | [JSON](8eh_dw1_jzp.json) |
| `8f2_m4v_3el` | 魏獻子 | [《史記・吳太伯世家》][13]、[《史記・晉世家》][21] | [JSON](8f2_m4v_3el.json) |
| `8f4_l5y_hda` | 下邳令未名 | [《史記・吳王濞列傳》][88] | [JSON](8f4_l5y_hda.json) |
| `8f4_qc5_g5e` | 接輿引古 | [《史記・魯仲連鄒陽列傳》][65] | [JSON](8f4_qc5_g5e.json) |
| `8f9_9wq_24y` | 高后 | [《史記・扁鵲倉公列傳》][87] | [JSON](8f9_9wq_24y.json) |
| `8fc_208_nfv` | 魏桓子 | [《史記・韓世家》][27] | [JSON](8fc_208_nfv.json) |
| `8fl_fbf_5p5` | 秦獻公 | [《史記・趙世家》][25] | [JSON](8fl_fbf_5p5.json) |
| `8fs_6cy_lw8` | 禹 | [《史記・孫子吳起列傳》][47] | [JSON](8fs_6cy_lw8.json) |
| `8ft_8ic_nez` | 太姒（文王正妃） | [《史記・管蔡世家》][17] | [JSON](8ft_8ic_nez.json) |
| `8g7_sug_2dg` | 元咺（衛大夫） | [《史記・衛康叔世家》][19] | [JSON](8g7_sug_2dg.json) |
| `8ga_fba_dw9` | 趙孝成王 | [《史記・平原君虞卿列傳》][58] | [JSON](8ga_fba_dw9.json) |
| `8gc_e5b_r4v` | 王子克 | [《史記・周本紀》][4] | [JSON](8gc_e5b_r4v.json) |
| `8gd_zz1_8a3` | 蜚廉 | [《史記・秦本紀》][5] | [JSON](8gd_zz1_8a3.json) |
| `8ge_1zr_lz9` | 冉孺 | [《史記・仲尼弟子列傳》][49] | [JSON](8ge_1zr_lz9.json) |
| `8gp_odm_2fn` | 薄昭 | [《史記・孝文本紀》][10] | [JSON](8gp_odm_2fn.json) |
| `8gq_slb_ulu` | 瞽叟 | [《史記・五帝本紀》][1] | [JSON](8gq_slb_ulu.json) |
| `8gy_kn0_9rf` | 長沮 | [《史記・孔子世家》][29] | [JSON](8gy_kn0_9rf.json) |
| `8h0_xff_vya` | 齊襄王 | [《史記・范睢蔡澤列傳》][61] | [JSON](8h0_xff_vya.json) |
| `8h7_82d_vjr` | 項梁 | [《史記・田儋列傳》][76] | [JSON](8h7_82d_vjr.json) |
| `8ht_nw8_3lv` | 周市 | [《史記・田儋列傳》][76] | [JSON](8ht_nw8_3lv.json) |
| `8i3_5vf_iu9` | 韓王成 | [《史記・留侯世家》][37] | [JSON](8i3_5vf_iu9.json) |
| `8i7_3dy_neb` | 斑師（衛君） | [《史記・衛康叔世家》][19] | [JSON](8i7_3dy_neb.json) |
| `8im_m5e_cpy` | 甘茂 | [《史記・樗里子甘茂列傳》][53] | [JSON](8im_m5e_cpy.json) |
| `8ji_f2j_ga7` | 宋邑 | [《史記・扁鵲倉公列傳》][87] | [JSON](8ji_f2j_ga7.json) |
| `8jr_zbk_lao` | 獵會未到者未名 | [《史記・田叔列傳》][86] | [JSON](8jr_zbk_lao.json) |
| `8jz_gel_lxj` | 鋗人（楚靈王求食者未名） | [《史記・楚世家》][22] | [JSON](8jz_gel_lxj.json) |
| `8jz_o3s_obt` | 黃帝 | [《史記・孝武本紀》][12] | [JSON](8jz_o3s_obt.json) |
| `8k1_7os_zkf` | 葉公 | [《史記・伍子胥列傳》][48] | [JSON](8k1_7os_zkf.json) |
| `8k3_wi8_pth` | 趙歇 | [《史記・張耳陳餘列傳》][71] | [JSON](8k3_wi8_pth.json) |
| `8kb_lbx_kcf` | 曹子引古未定 | [《史記・刺客列傳》][68] | [JSON](8kb_lbx_kcf.json) |
| `8kd_lv1_5lu` | 姑布子卿 | [《史記・趙世家》][25] | [JSON](8kd_lv1_5lu.json) |
| `8l5_257_bj3` | 子韋（宋司星） | [《史記・宋微子世家》][20] | [JSON](8l5_257_bj3.json) |
| `8nv_485_mex` | 趙成侯 | [《史記・秦本紀》][5] | [JSON](8nv_485_mex.json) |
| `8o8_8nk_ldw` | 趙爵 | [《史記・趙世家》][25] | [JSON](8o8_8nk_ldw.json) |
| `8oa_uge_0p6` | 趙高母未名 | [《史記・蒙恬列傳》][70] | [JSON](8oa_uge_0p6.json) |
| `8ov_spc_ch8` | 重耳母女弟（夷吾母） | [《史記・晉世家》][21] | [JSON](8ov_spc_ch8.json) |
| `8pb_yn0_e78` | 項燕 | [《史記・白起王翦列傳》][55] | [JSON](8pb_yn0_e78.json) |
| `8pi_259_b4u` | 南子 | [《史記・孔子世家》][29] | [JSON](8pi_259_b4u.json) |
| `8py_u6m_e6a` | 百里奚（引古） | [《史記・蒙恬列傳》][70] | [JSON](8py_u6m_e6a.json) |
| `8q9_6wj_aid` | 巫臣子（吳行人未名） | [《史記・晉世家》][21] | [JSON](8q9_6wj_aid.json) |
| `8qn_pes_ndt` | 孔父妻（華督所取者未名） | [《史記・宋微子世家》][20] | [JSON](8qn_pes_ndt.json) |
| `8qw_wy4_91g` | 鄧侯（楚文王過鄧時未名） | [《史記・楚世家》][22] | [JSON](8qw_wy4_91g.json) |
| `8r1_6zb_ghp` | 高陵君 | [《史記・范睢蔡澤列傳》][61] | [JSON](8r1_6zb_ghp.json) |
| `8r1_wnc_n5o` | 西周武公 | [《史記・周本紀》][4] | [JSON](8r1_wnc_n5o.json) |
| `8r5_zyc_5dx` | 柴將軍未詳名 | [《史記・韓信盧綰列傳》][75] | [JSON](8r5_zyc_5dx.json) |
| `8r8_law_3lz` | 周赧王 | [《史記・周本紀》][4] | [JSON](8r8_law_3lz.json) |
| `8rc_l89_zwn` | 斯短稱引古未定 | [《史記・屈原賈生列傳》][66] | [JSON](8rc_l89_zwn.json) |
| `8rg_idp_izr` | 芒卯 | [《史記・穰侯列傳》][54] | [JSON](8rg_idp_izr.json) |
| `8rl_z9b_qjh` | 公孫余假 | [《史記・孔子世家》][29] | [JSON](8rl_z9b_qjh.json) |
| `8sb_tti_0yc` | 始皇 | [《史記・陳涉世家》][30] | [JSON](8sb_tti_0yc.json) |
| `8sq_zq4_x84` | 公孫痤 | [《史記・秦本紀》][5] | [JSON](8sq_zq4_x84.json) |
| `8st_c0j_4fk` | 劉澤 | [《史記・齊悼惠王世家》][34] | [JSON](8st_c0j_4fk.json) |
| `8td_4s1_hgs` | 棠公 | [《史記・齊太公世家》][14] | [JSON](8td_4s1_hgs.json) |
| `8tn_cxl_8ru` | 燕噲 | [《史記・燕召公世家》][16] | [JSON](8tn_cxl_8ru.json) |
| `8u0_i5d_aql` | 楊武 | [《史記・項羽本紀》][7] | [JSON](8u0_i5d_aql.json) |
| `8u9_s13_86r` | 郤縠（中軍將） | [《史記・晉世家》][21] | [JSON](8u9_s13_86r.json) |
| `8u9_ugq_ise` | 暴鳶 | [《史記・秦本紀》][5] | [JSON](8u9_ugq_ise.json) |
| `8uy_02i_ne6` | 王翦 | [《史記・刺客列傳》][68] | [JSON](8uy_02i_ne6.json) |
| `8uy_mfn_msk` | 咎如少女（趙衰妻） | [《史記・晉世家》][21] | [JSON](8uy_mfn_msk.json) |
| `8uz_lzx_abe` | 彌子之母 | [《史記・老子韓非列傳》][45] | [JSON](8uz_lzx_abe.json) |
| `8v2_utn_r1e` | 利幾 | [《史記・高祖本紀》][8] | [JSON](8v2_utn_r1e.json) |
| `8ve_7km_25p` | 呂后 | [《史記・黥布列傳》][73] | [JSON](8ve_7km_25p.json) |
| `8ve_l7c_yz3` | 晁錯 | [《史記・張丞相列傳》][78] | [JSON](8ve_l7c_yz3.json) |
| `8vp_hqi_6mq` | 召忽 | [《史記・齊太公世家》][14] | [JSON](8vp_hqi_6mq.json) |
| `8vt_geo_sqb` | 趙王未詳名 | [《史記・樊酈滕灌列傳》][77] | [JSON](8vt_geo_sqb.json) |
| `8w3_sd6_lr3` | 鹿毛壽（讓國進言者） | [《史記・燕召公世家》][16] | [JSON](8w3_sd6_lr3.json) |
| `8w8_yyv_mrh` | 出於 | [《史記・扁鵲倉公列傳》][87] | [JSON](8w8_yyv_mrh.json) |
| `8w9_7hx_mgb` | 騎劫 | [《史記・樂毅列傳》][62] | [JSON](8w9_7hx_mgb.json) |
| `8w9_x0s_cyf` | 子之 | [《史記・燕召公世家》][16] | [JSON](8w9_x0s_cyf.json) |
| `8wv_thm_2zy` | 晏嬰 | [《史記・孟子荀卿列傳》][56] | [JSON](8wv_thm_2zy.json) |
| `8ww_xz0_o82` | 鄭姬（楚莊王所抱者） | [《史記・楚世家》][22] | [JSON](8ww_xz0_o82.json) |
| `8xv_ax8_bpe` | 陳平嫂 | [《史記・陳丞相世家》][38] | [JSON](8xv_ax8_bpe.json) |
| `8yw_17t_rrj` | 成王弟 | [《史記・梁孝王世家》][40] | [JSON](8yw_17t_rrj.json) |
| `8yw_fij_nt2` | 趙括（晉卿） | [《史記・晉世家》][21] | [JSON](8yw_fij_nt2.json) |
| `8yw_ksh_n5l` | 周幽王 | [《史記・趙世家》][25] | [JSON](8yw_ksh_n5l.json) |
| `8yx_xsn_k1g` | 太子建從者 | [《史記・伍子胥列傳》][48] | [JSON](8yx_xsn_k1g.json) |
| `8zj_5p3_i5y` | 夏桀 | [《史記・孫子吳起列傳》][47] | [JSON](8zj_5p3_i5y.json) |
| `8zs_p2x_twj` | 臧文仲 | [《史記・仲尼弟子列傳》][49] | [JSON](8zs_p2x_twj.json) |
| `903_9bw_83a` | 少妾（陳哀公勝母） | [《史記・陳杞世家》][18] | [JSON](903_9bw_83a.json) |
| `90i_ym7_hnz` | 建德 | [《史記・楚元王世家》][32] | [JSON](90i_ym7_hnz.json) |
| `90m_2uj_bu6` | 附沮（楚篇祖系） | [《史記・楚世家》][22] | [JSON](90m_2uj_bu6.json) |
| `90s_rhf_ff3` | 林（陳莊公） | [《史記・陳杞世家》][18] | [JSON](90s_rhf_ff3.json) |
| `910_4xt_rwk` | 秦穆公 | [《史記・孔子世家》][29] | [JSON](910_4xt_rwk.json) |
| `91b_436_pst` | 魯女（光母未名） | [《史記・齊太公世家》][14] | [JSON](91b_436_pst.json) |
| `91e_89k_8p8` | 項莊 | [《史記・樊酈滕灌列傳》][77] | [JSON](91e_89k_8p8.json) |
| `91s_bsz_pe8` | 安期生 | [《史記・孝武本紀》][12] | [JSON](91s_bsz_pe8.json) |
| `921_w24_4mr` | 平陽公主 | [《史記・樊酈滕灌列傳》][77] | [JSON](921_w24_4mr.json) |
| `929_zmz_x6k` | 孝文太子 | [《史記・絳侯周勃世家》][39] | [JSON](929_zmz_x6k.json) |
| `92t_lra_3r9` | 程處 | [《史記・樊酈滕灌列傳》][77] | [JSON](92t_lra_3r9.json) |
| `92w_9ey_nuv` | 息夫人（陳女未名） | [《史記・管蔡世家》][17] | [JSON](92w_9ey_nuv.json) |
| `92x_vc4_9h0` | 武負 | [《史記・高祖本紀》][8] | [JSON](92x_vc4_9h0.json) |
| `932_ice_oix` | 樗里子 | [《史記・魏世家》][26] | [JSON](932_ice_oix.json) |
| `934_0gu_keg` | 魏襄王 | [《史記・魏世家》][26] | [JSON](934_0gu_keg.json) |
| `935_1k9_x7t` | 秦昭王 | [《史記・范睢蔡澤列傳》][61] | [JSON](935_1k9_x7t.json) |
| `94a_9mp_mel` | 伯夷引古 | [《史記・范睢蔡澤列傳》][61] | [JSON](94a_9mp_mel.json) |
| `94b_b75_ipy` | 漆彫開 | [《史記・仲尼弟子列傳》][49] | [JSON](94b_b75_ipy.json) |
| `94s_w92_nqh` | 楡次主人未名 | [《史記・刺客列傳》][68] | [JSON](94s_w92_nqh.json) |
| `94w_aq9_d5c` | 楚懷王 | [《史記・高祖本紀》][8] | [JSON](94w_aq9_d5c.json) |
| `95o_n0j_io3` | 唐山（宋司馬） | [《史記・宋微子世家》][20] | [JSON](95o_n0j_io3.json) |
| `95o_t1b_ren` | 吳起 | [《史記・陳涉世家》][30] | [JSON](95o_t1b_ren.json) |
| `971_iwp_102` | 延陵季子引古 | [《史記・范睢蔡澤列傳》][61] | [JSON](971_iwp_102.json) |
| `975_ptr_1sv` | 呂后 | [《史記・淮陰侯列傳》][74] | [JSON](975_ptr_1sv.json) |
| `977_am7_t53` | 周成王 | [《史記・趙世家》][25] | [JSON](977_am7_t53.json) |
| `97g_m2u_raa` | 孔父 | [《史記・鄭世家》][24] | [JSON](97g_m2u_raa.json) |
| `97i_ulh_8fv` | 駟鈞 | [《史記・呂太后本紀》][9] | [JSON](97i_ulh_8fv.json) |
| `97s_gzq_ow9` | 卬（北地都尉） | [《史記・張釋之馮唐列傳》][84] | [JSON](97s_gzq_ow9.json) |
| `97x_bw8_rqz` | 項聲 | [《史記・樊酈滕灌列傳》][77] | [JSON](97x_bw8_rqz.json) |
| `97y_40q_pnl` | 唐眛（楚將） | [《史記・楚世家》][22]、[《史記・屈原賈生列傳》][66] | [JSON](97y_40q_pnl.json) |
| `97z_1s7_oq1` | 秦監公 | [《史記・曹相國世家》][36] | [JSON](97z_1s7_oq1.json) |
| `98b_07q_k2m` | 重耳 | [《史記・晉世家》][21] | [JSON](98b_07q_k2m.json) |
| `98b_qae_m9k` | 李良從官進言者未名 | [《史記・張耳陳餘列傳》][71] | [JSON](98b_qae_m9k.json) |
| `98e_ijv_9wt` | 費將軍（垓下敘事） | [《史記・高祖本紀》][8] | [JSON](98e_ijv_9wt.json) |
| `98o_tak_pi0` | 趙周 | [《史記・張丞相列傳》][78] | [JSON](98o_tak_pi0.json) |
| `98p_51k_nct` | 南庚 | [《史記・殷本紀》][3] | [JSON](98p_51k_nct.json) |
| `98y_02x_z6o` | 蘇秦 | [《史記・蘇秦列傳》][51] | [JSON](98y_02x_z6o.json) |
| `996_uzv_2bc` | 子公 | [《史記・鄭世家》][24] | [JSON](996_uzv_2bc.json) |
| `999_8x2_oj9` | 韓王安 | [《史記・秦始皇本紀》][6]、[《史記・燕召公世家》][16] | [JSON](999_8x2_oj9.json) |
| `99a_9ca_6fi` | 孫臏 | [《史記・秦始皇本紀》][6] | [JSON](99a_9ca_6fi.json) |
| `99c_825_chj` | 紂 | [《史記・魏世家》][26] | [JSON](99c_825_chj.json) |
| `9a4_nbk_pp5` | 晉君（內昭公議事未名） | [《史記・魯周公世家》][15] | [JSON](9a4_nbk_pp5.json) |
| `9aa_fhj_xvu` | 徐盧校勘名 | [《史記・絳侯周勃世家》][39] | [JSON](9aa_fhj_xvu.json) |
| `9ae_9vp_6fz` | 相壯 | [《史記・樗里子甘茂列傳》][53] | [JSON](9ae_9vp_6fz.json) |
| `9aw_sc6_dx3` | 周天子（田世家立田和未名者） | [《史記・田敬仲完世家》][28] | [JSON](9aw_sc6_dx3.json) |
| `9bk_i60_uy7` | 辛勝 | [《史記・秦始皇本紀》][6] | [JSON](9bk_i60_uy7.json) |
| `9bq_w53_csf` | 周烈王引古 | [《史記・魯仲連鄒陽列傳》][65] | [JSON](9bq_w53_csf.json) |
| `9cq_h7j_stw` | 滕公 | [《史記・樊酈滕灌列傳》][77] | [JSON](9cq_h7j_stw.json) |
| `9d5_n20_car` | 太中大夫明 | [《史記・三王世家》][42] | [JSON](9d5_n20_car.json) |
| `9dn_jfi_fc0` | 湯引古 | [《史記・平原君虞卿列傳》][58] | [JSON](9dn_jfi_fc0.json) |
| `9do_2ro_4b8` | 朱雞石 | [《史記・項羽本紀》][7] | [JSON](9do_2ro_4b8.json) |
| `9dx_y3b_try` | 蕭氏未詳名 | [《史記・張丞相列傳》][78] | [JSON](9dx_y3b_try.json) |
| `9ec_mww_wxr` | 慶舍 | [《史記・齊太公世家》][14] | [JSON](9ec_mww_wxr.json) |
| `9ef_e9z_h1f` | 慶 | [《史記・陳涉世家》][30] | [JSON](9ef_e9z_h1f.json) |
| `9fg_73i_8fk` | 相 | [《史記・夏本紀》][2]、[《史記・吳太伯世家》][13] | [JSON](9fg_73i_8fk.json) |
| `9g0_ueo_x4u` | 延陵季子 | [《史記・鄭世家》][24] | [JSON](9g0_ueo_x4u.json) |
| `9gq_tfb_414` | 楚昭王 | [《史記・吳太伯世家》][13]、[《史記・管蔡世家》][17] | [JSON](9gq_tfb_414.json) |
| `9gy_e16_ue3` | 宋義 | [《史記・黥布列傳》][73] | [JSON](9gy_e16_ue3.json) |
| `9h5_akj_wys` | 彭越 | [《史記・魏豹彭越列傳》][72] | [JSON](9h5_akj_wys.json) |
| `9h9_tgw_47c` | 燕姬（景公夫人） | [《史記・齊太公世家》][14] | [JSON](9h9_tgw_47c.json) |
| `9hr_p35_zdj` | 閎籍孺 | [《史記・酈生陸賈列傳》][79] | [JSON](9hr_p35_zdj.json) |
| `9hw_mvo_jk8` | 俠累 | [《史記・刺客列傳》][68] | [JSON](9hw_mvo_jk8.json) |
| `9i1_0jo_8sa` | 淮南厲王 | [《史記・屈原賈生列傳》][66] | [JSON](9i1_0jo_8sa.json) |
| `9ia_6lk_9sa` | 魏昭王 | [《史記・范睢蔡澤列傳》][61] | [JSON](9ia_6lk_9sa.json) |
| `9il_6ew_aq3` | 籍（晉獻侯） | [《史記・晉世家》][21] | [JSON](9il_6ew_aq3.json) |
| `9il_q12_qhj` | 考王 | [《史記・周本紀》][4] | [JSON](9il_q12_qhj.json) |
| `9iv_9yu_skl` | 趙亥（建成侯） | [《史記・秦始皇本紀》][6] | [JSON](9iv_9yu_skl.json) |
| `9j0_saz_b8g` | 卞和引古 | [《史記・魯仲連鄒陽列傳》][65] | [JSON](9j0_saz_b8g.json) |
| `9j0_xt0_2hq` | 泄冶（陳諫臣） | [《史記・陳杞世家》][18] | [JSON](9j0_xt0_2hq.json) |
| `9j5_0wx_64h` | 夫概 | [《史記・伍子胥列傳》][48] | [JSON](9j5_0wx_64h.json) |
| `9j9_xgc_3x3` | 韓襄王 | [《史記・樗里子甘茂列傳》][53] | [JSON](9j9_xgc_3x3.json) |
| `9jw_91d_emz` | 田逆 | [《史記・齊太公世家》][14] | [JSON](9jw_91d_emz.json) |
| `9kf_g2j_i2h` | 孟軻（伐燕進言者） | [《史記・燕召公世家》][16] | [JSON](9kf_g2j_i2h.json) |
| `9li_j1i_hm5` | 田單（齊將） | [《史記・田單列傳》][64] | [JSON](9li_j1i_hm5.json) |
| `9lk_49t_e6e` | 陳武（漢初大將軍） | [《史記・孝文本紀》][10] | [JSON](9lk_49t_e6e.json) |
| `9lp_b6m_laq` | 李斯引古 | [《史記・魯仲連鄒陽列傳》][65] | [JSON](9lp_b6m_laq.json) |
| `9lv_6cv_fpp` | 柴將軍（垓下敘事） | [《史記・高祖本紀》][8] | [JSON](9lv_6cv_fpp.json) |
| `9mg_wxe_cao` | 呂產 | [《史記・荊燕世家》][33] | [JSON](9mg_wxe_cao.json) |
| `9mh_7cb_704` | 成（大駱子） | [《史記・秦本紀》][5] | [JSON](9mh_7cb_704.json) |
| `9mw_pdn_ati` | 范睢 | [《史記・范睢蔡澤列傳》][61] | [JSON](9mw_pdn_ati.json) |
| `9n1_t73_kdy` | 秦昭王 | [《史記・樂毅列傳》][62] | [JSON](9n1_t73_kdy.json) |
| `9n6_i20_6n9` | 涉閒 | [《史記・項羽本紀》][7] | [JSON](9n6_i20_6n9.json) |
| `9nc_i02_15v` | 徐巿（本文字形） | [《史記・秦始皇本紀》][6] | [JSON](9nc_i02_15v.json) |
| `9np_rzc_2gg` | 伯夷 | [《史記・鄭世家》][24] | [JSON](9np_rzc_2gg.json) |
| `9o2_2ov_exd` | 帶他 | [《史記・陳涉世家》][30] | [JSON](9o2_2ov_exd.json) |
| `9o3_tsd_zsk` | 申侯（楚成王伐齊將） | [《史記・楚世家》][22] | [JSON](9o3_tsd_zsk.json) |
| `9o5_pap_blt` | 趙疵 | [《史記・趙世家》][25] | [JSON](9o5_pap_blt.json) |
| `9oa_4bh_lmd` | 鄭伯（楚莊王圍鄭時） | [《史記・鄭世家》][24] | [JSON](9oa_4bh_lmd.json) |
| `9oc_37g_jlc` | 后勝 | [《史記・田敬仲完世家》][28] | [JSON](9oc_37g_jlc.json) |
| `9oe_ish_fuj` | 王子朝 | [《史記・周本紀》][4] | [JSON](9oe_ish_fuj.json) |
| `9pq_9wn_9y1` | 項佗 | [《史記・樊酈滕灌列傳》][77] | [JSON](9pq_9wn_9y1.json) |
| `9pr_eer_wtk` | 新垣衍 | [《史記・魯仲連鄒陽列傳》][65] | [JSON](9pr_eer_wtk.json) |
| `9pr_pid_8tj` | 黃帝 | [《史記・孟子荀卿列傳》][56] | [JSON](9pr_pid_8tj.json) |
| `9pv_or9_2r6` | 虢太子未名 | [《史記・扁鵲倉公列傳》][87] | [JSON](9pv_or9_2r6.json) |
| `9px_mn4_w7x` | 修成君 | [《史記・齊悼惠王世家》][34] | [JSON](9px_mn4_w7x.json) |
| `9pz_z2d_tqx` | 茅焦 | [《史記・秦始皇本紀》][6]、[《史記・呂不韋列傳》][67] | [JSON](9pz_z2d_tqx.json) |
| `9q0_896_584` | 禹 | [《史記・伯夷列傳》][43] | [JSON](9q0_896_584.json) |
| `9qj_prl_ehx` | 犀首 | [《史記・張儀列傳》][52] | [JSON](9qj_prl_ehx.json) |
| `9qr_quf_02m` | 帝嚳 | [《史記・五帝本紀》][1] | [JSON](9qr_quf_02m.json) |
| `9qt_orl_5f2` | 彭越 | [《史記・魏豹彭越列傳》][72] | [JSON](9qt_orl_5f2.json) |
| `9qv_dcf_92g` | 廑 | [《史記・夏本紀》][2] | [JSON](9qv_dcf_92g.json) |
| `9rl_u52_5fz` | 惡來 | [《史記・秦本紀》][5] | [JSON](9rl_u52_5fz.json) |
| `9rn_poi_ayp` | 襄仲（文公時） | [《史記・魯周公世家》][15] | [JSON](9rn_poi_ayp.json) |
| `9rs_a73_ub4` | 虞仲（周章弟） | [《史記・吳太伯世家》][13] | [JSON](9rs_a73_ub4.json) |
| `9s2_52x_617` | 范曾 | [《史記・黥布列傳》][73] | [JSON](9s2_52x_617.json) |
| `9s8_yra_ciz` | 齊王命列大夫 | [《史記・孟子荀卿列傳》][56] | [JSON](9s8_yra_ciz.json) |
| `9sb_chn_ytt` | 中山武公 | [《史記・趙世家》][25] | [JSON](9sb_chn_ytt.json) |
| `9t0_psw_zf3` | 戚姬 | [《史記・張丞相列傳》][78] | [JSON](9t0_psw_zf3.json) |
| `9t6_8nc_nuo` | 樂乘 | [《史記・樂毅列傳》][62] | [JSON](9t6_8nc_nuo.json) |
| `9ta_gen_pky` | 項它 | [《史記・魏豹彭越列傳》][72] | [JSON](9ta_gen_pky.json) |
| `9tl_l1k_ize` | 衛靈公 | [《史記・孟子荀卿列傳》][56] | [JSON](9tl_l1k_ize.json) |
| `9tl_u6l_vyp` | 臧荼 | [《史記・絳侯周勃世家》][39] | [JSON](9tl_u6l_vyp.json) |
| `9uc_3ge_wyg` | 衡山王未詳名 | [《史記・酈生陸賈列傳》][79] | [JSON](9uc_3ge_wyg.json) |
| `9ud_33t_j5m` | 齊王書信 | [《史記・蘇秦列傳》][51] | [JSON](9ud_33t_j5m.json) |
| `9ui_6ki_31p` | 留侯未詳名 | [《史記・留侯世家》][37] | [JSON](9ui_6ki_31p.json) |
| `9ul_wlf_q1k` | 呂祿 | [《史記・張丞相列傳》][78] | [JSON](9ul_wlf_q1k.json) |
| `9uw_tzo_yj8` | 悼公 | [《史記・伍子胥列傳》][48] | [JSON](9uw_tzo_yj8.json) |
| `9v3_xea_50v` | 長公主 | [《史記・孝景本紀》][11] | [JSON](9v3_xea_50v.json) |
| `9v8_tr9_ikg` | 郤芮 | [《史記・晉世家》][21] | [JSON](9v8_tr9_ikg.json) |
| `9w2_rfm_964` | 羊斟 | [《史記・鄭世家》][24] | [JSON](9w2_rfm_964.json) |
| `9wg_gdm_8pd` | 亭長未名 | [《史記・淮陰侯列傳》][74] | [JSON](9wg_gdm_8pd.json) |
| `9wm_v9j_esn` | 孔子 | [《史記・孔子世家》][29] | [JSON](9wm_v9j_esn.json) |
| `9wx_3fi_zk2` | 項羽 | [《史記・劉敬叔孫通列傳》][81] | [JSON](9wx_3fi_zk2.json) |
| `9x9_12x_dhb` | 李延年 | [《史記・孝武本紀》][12] | [JSON](9x9_12x_dhb.json) |
| `9xr_uju_djo` | 陶青 | [《史記・張丞相列傳》][78] | [JSON](9xr_uju_djo.json) |
| `9y3_c3o_5zb` | 秦將卻軍未名 | [《史記・魯仲連鄒陽列傳》][65] | [JSON](9y3_c3o_5zb.json) |
| `9yu_h0u_07p` | 李斯引古 | [《史記・屈原賈生列傳》][66] | [JSON](9yu_h0u_07p.json) |
| `9yz_2do_3dm` | 蘇代 | [《史記・魏世家》][26] | [JSON](9yz_2do_3dm.json) |
| `9zv_c2c_v3b` | 仇液 | [《史記・穰侯列傳》][54] | [JSON](9zv_c2c_v3b.json) |
| `a00_ney_bf4` | 象 | [《史記・五帝本紀》][1] | [JSON](a00_ney_bf4.json) |
| `a0a_4q4_biw` | 韓襄王 | [《史記・秦本紀》][5] | [JSON](a0a_4q4_biw.json) |
| `a0l_8nr_2to` | 齊湣王相（議歸楚太子未名者） | [《史記・楚世家》][22] | [JSON](a0l_8nr_2to.json) |
| `a0l_wan_b7q` | 棄疾 | [《史記・楚世家》][22] | [JSON](a0l_wan_b7q.json) |
| `a0z_bx1_tnh` | 曹參 | [《史記・曹相國世家》][36] | [JSON](a0z_bx1_tnh.json) |
| `a16_zm9_diw` | 石生 | [《史記・秦始皇本紀》][6] | [JSON](a16_zm9_diw.json) |
| `a19_9ni_9mq` | 陳嬰母 | [《史記・項羽本紀》][7] | [JSON](a19_9ni_9mq.json) |
| `a1u_jzk_000` | 吳季札 | [《史記・韓世家》][27] | [JSON](a1u_jzk_000.json) |
| `a2c_d6k_c4o` | 季武子 | [《史記・孔子世家》][29] | [JSON](a2c_d6k_c4o.json) |
| `a2n_tv1_o25` | 管仲母 | [《史記・管晏列傳》][44] | [JSON](a2n_tv1_o25.json) |
| `a2v_ea5_yii` | 齊歸（裯母） | [《史記・魯周公世家》][15] | [JSON](a2v_ea5_yii.json) |
| `a2w_jo1_uxj` | 外黃令舍人兒 | [《史記・項羽本紀》][7] | [JSON](a2w_jo1_uxj.json) |
| `a2x_dkn_fj9` | 郭開 | [《史記・廉頗藺相如列傳》][63] | [JSON](a2x_dkn_fj9.json) |
| `a3j_iyj_exa` | 文王引古未定 | [《史記・春申君列傳》][60] | [JSON](a3j_iyj_exa.json) |
| `a3u_jao_m4o` | 城陽君 | [《史記・秦本紀》][5] | [JSON](a3u_jao_m4o.json) |
| `a3w_z9o_hsu` | 田忌 | [《史記・孟子荀卿列傳》][56] | [JSON](a3w_z9o_hsu.json) |
| `a43_p6o_o49` | 陳勝 | [《史記・季布欒布列傳》][82] | [JSON](a43_p6o_o49.json) |
| `a48_r53_plq` | 孝惠皇帝（孔子世家博士所事未名者） | [《史記・孔子世家》][29] | [JSON](a48_r53_plq.json) |
| `a4c_92r_l2i` | 微子引古 | [《史記・范睢蔡澤列傳》][61] | [JSON](a4c_92r_l2i.json) |
| `a51_heh_znt` | 牛畜 | [《史記・趙世家》][25] | [JSON](a51_heh_znt.json) |
| `a54_d6h_wd1` | 王温舒 | [《史記・萬石張叔列傳》][85] | [JSON](a54_d6h_wd1.json) |
| `a5n_z4j_1uf` | 堯 | [《史記・伯夷列傳》][43] | [JSON](a5n_z4j_1uf.json) |
| `a70_h0o_diu` | 富父終甥 | [《史記・魯周公世家》][15] | [JSON](a70_h0o_diu.json) |
| `a72_80l_b8r` | 穰侯（韓世家未名者） | [《史記・韓世家》][27] | [JSON](a72_80l_b8r.json) |
| `a7c_94k_tf9` | 曹（蕭曹用稱） | [《史記・韓信盧綰列傳》][75] | [JSON](a7c_94k_tf9.json) |
| `a7m_05v_rds` | 綰 | [《史記・孝景本紀》][11] | [JSON](a7m_05v_rds.json) |
| `a82_krd_hlg` | 薄太后 | [《史記・孝文本紀》][10]、[《史記・絳侯周勃世家》][39] | [JSON](a82_krd_hlg.json) |
| `a8j_xnu_ibi` | 通（曹隱公） | [《史記・管蔡世家》][17] | [JSON](a8j_xnu_ibi.json) |
| `a9f_5ms_y31` | 陳恢 | [《史記・高祖本紀》][8] | [JSON](a9f_5ms_y31.json) |
| `a9s_6ix_kzx` | 趙袑 | [《史記・趙世家》][25] | [JSON](a9s_6ix_kzx.json) |
| `a9s_bmk_9h5` | 彭祖（陸終子） | [《史記・楚世家》][22] | [JSON](a9s_bmk_9h5.json) |
| `aa9_8gx_l6j` | 御說（宋桓公） | [《史記・宋微子世家》][20] | [JSON](aa9_8gx_l6j.json) |
| `aal_nze_fai` | 舜引古 | [《史記・魯仲連鄒陽列傳》][65] | [JSON](aal_nze_fai.json) |
| `aav_n19_j6o` | 趙固 | [《史記・趙世家》][25] | [JSON](aav_n19_j6o.json) |
| `abc_8g5_0zf` | 高后 | [《史記・楚元王世家》][32] | [JSON](abc_8g5_0zf.json) |
| `ac8_u5v_dxj` | 宋殤公（楚篇弒君記事） | [《史記・楚世家》][22] | [JSON](ac8_u5v_dxj.json) |
| `acr_zxn_ca3` | 嚴仲子 | [《史記・刺客列傳》][68] | [JSON](acr_zxn_ca3.json) |
| `ad1_fs3_e4j` | 子上（楚成王令尹） | [《史記・楚世家》][22] | [JSON](ad1_fs3_e4j.json) |
| `adj_kqv_jh0` | 田祿伯 | [《史記・吳王濞列傳》][88] | [JSON](adj_kqv_jh0.json) |
| `aec_cp5_x6d` | 主父偃 | [《史記・齊悼惠王世家》][34] | [JSON](aec_cp5_x6d.json) |
| `aek_yfr_e0h` | 項梁 | [《史記・黥布列傳》][73] | [JSON](aek_yfr_e0h.json) |
| `aey_tui_wzm` | 齊太師（孔子世家未名者） | [《史記・孔子世家》][29] | [JSON](aey_tui_wzm.json) |
| `aez_p66_9uj` | 藺相如持璧歸趙從者未名 | [《史記・廉頗藺相如列傳》][63] | [JSON](aez_p66_9uj.json) |
| `af6_mhg_pyn` | 呂種 | [《史記・呂太后本紀》][9] | [JSON](af6_mhg_pyn.json) |
| `afb_ahe_sqp` | 趙堯 | [《史記・張丞相列傳》][78] | [JSON](afb_ahe_sqp.json) |
| `afc_k9r_hjr` | 衡父 | [《史記・秦本紀》][5] | [JSON](afc_k9r_hjr.json) |
| `afe_vxj_iuk` | 中御府長信 | [《史記・扁鵲倉公列傳》][87] | [JSON](afe_vxj_iuk.json) |
| `afy_rj9_84r` | 秦皇帝 | [《史記・齊悼惠王世家》][34] | [JSON](afy_rj9_84r.json) |
| `agc_zmx_tap` | 鄦公 | [《史記・鄭世家》][24] | [JSON](agc_zmx_tap.json) |
| `agr_7ae_9ur` | 路中大夫 | [《史記・齊悼惠王世家》][34] | [JSON](agr_7ae_9ur.json) |
| `agx_sqm_4ou` | 張耳 | [《史記・張耳陳餘列傳》][71] | [JSON](agx_sqm_4ou.json) |
| `ah7_qcl_dpg` | 周青臣 | [《史記・秦始皇本紀》][6]、[《史記・李斯列傳》][69] | [JSON](ah7_qcl_dpg.json) |
| `ahe_e3g_ua6` | 右尹（勸楚靈王逃亡者未名） | [《史記・楚世家》][22] | [JSON](ahe_e3g_ua6.json) |
| `ai6_yoy_d51` | 鄭文公（楚篇朝楚者） | [《史記・楚世家》][22] | [JSON](ai6_yoy_d51.json) |
| `aig_hbr_uc9` | 騶衍 | [《史記・孟子荀卿列傳》][56] | [JSON](aig_hbr_uc9.json) |
| `ajo_g09_qqk` | 將軍摎 | [《史記・秦本紀》][5] | [JSON](ajo_g09_qqk.json) |
| `ajv_agq_es1` | 秦昭王 | [《史記・范睢蔡澤列傳》][61] | [JSON](ajv_agq_es1.json) |
| `ajw_5lx_1mf` | 齊鮑牧 | [《史記・伍子胥列傳》][48] | [JSON](ajw_5lx_1mf.json) |
| `al3_w9j_0ng` | 宋昌 | [《史記・孝文本紀》][10] | [JSON](al3_w9j_0ng.json) |
| `alv_ted_3rj` | 司馬喜引古 | [《史記・魯仲連鄒陽列傳》][65] | [JSON](alv_ted_3rj.json) |
| `aml_541_6lh` | 子綦（楚昭王從臣） | [《史記・楚世家》][22] | [JSON](aml_541_6lh.json) |
| `aml_745_t4f` | 祭公謀父 | [《史記・周本紀》][4] | [JSON](aml_745_t4f.json) |
| `amq_yua_viu` | 庶長封 | [《史記・秦本紀》][5] | [JSON](amq_yua_viu.json) |
| `an9_1k7_get` | 秦惠王 | [《史記・田敬仲完世家》][28] | [JSON](an9_1k7_get.json) |
| `anb_y7b_x61` | 仲尼 | [《史記・陳涉世家》][30] | [JSON](anb_y7b_x61.json) |
| `anh_fih_n7i` | 孝惠帝 | [《史記・季布欒布列傳》][82] | [JSON](anh_fih_n7i.json) |
| `ant_2so_obo` | 宣平侯女（孝惠皇后） | [《史記・呂太后本紀》][9] | [JSON](ant_2so_obo.json) |
| `any_r0t_f7c` | 郭開 | [《史記・廉頗藺相如列傳》][63] | [JSON](any_r0t_f7c.json) |
| `ao1_jlu_689` | 太叔（孔子世家被攻未名者） | [《史記・孔子世家》][29] | [JSON](ao1_jlu_689.json) |
| `ao8_ud8_zti` | 趙希 | [《史記・趙世家》][25] | [JSON](ao8_ud8_zti.json) |
| `aoj_li6_wuk` | 防與先生 | [《史記・楚元王世家》][32] | [JSON](aoj_li6_wuk.json) |
| `aon_o1a_cxi` | 陳軫 | [《史記・韓世家》][27] | [JSON](aon_o1a_cxi.json) |
| `apo_85x_sj0` | 魏王欲事未定 | [《史記・范睢蔡澤列傳》][61] | [JSON](apo_85x_sj0.json) |
| `apu_6fw_asx` | 馮琴對者（魏世家中旗讀法未定） | [《史記・魏世家》][26] | [JSON](apu_6fw_asx.json) |
| `apz_fp8_twe` | 魏公子卬 | [《史記・商君列傳》][50] | [JSON](apz_fp8_twe.json) |
| `aq4_814_hq2` | 安期生 | [《史記・田儋列傳》][76] | [JSON](aq4_814_hq2.json) |
| `aru_qbv_1vo` | 李必 | [《史記・樊酈滕灌列傳》][77] | [JSON](aru_qbv_1vo.json) |
| `ary_z8m_f18` | 景王 | [《史記・周本紀》][4] | [JSON](ary_z8m_f18.json) |
| `as3_a3z_9jx` | 公甫文伯母未名 | [《史記・平原君虞卿列傳》][58] | [JSON](as3_a3z_9jx.json) |
| `asz_r1c_0yz` | 楚南公 | [《史記・項羽本紀》][7] | [JSON](asz_r1c_0yz.json) |
| `atg_2va_c3g` | 公孫翩 | [《史記・孔子世家》][29] | [JSON](atg_2va_c3g.json) |
| `atj_f3h_1y6` | 郤缺（河曲晉將） | [《史記・晉世家》][21] | [JSON](atj_f3h_1y6.json) |
| `atl_qkh_lx9` | 子政 | [《史記・秦始皇本紀》][6] | [JSON](atl_qkh_lx9.json) |
| `aty_1xv_rg0` | 宋武公（鄋瞞記事） | [《史記・魯周公世家》][15] | [JSON](aty_1xv_rg0.json) |
| `au5_uur_6pa` | 商澤 | [《史記・仲尼弟子列傳》][49] | [JSON](au5_uur_6pa.json) |
| `aua_4v4_axs` | 晉靈公 | [《史記・韓世家》][27] | [JSON](aua_4v4_axs.json) |
| `auy_ue1_w17` | 齊宣王 | [《史記・孟子荀卿列傳》][56] | [JSON](auy_ue1_w17.json) |
| `avz_fhq_79h` | 齊王馮驩復孟未定 | [《史記・孟嘗君列傳》][57] | [JSON](avz_fhq_79h.json) |
| `awg_p4y_84n` | 紀侯（譖齊哀公者） | [《史記・齊太公世家》][14] | [JSON](awg_p4y_84n.json) |
| `awq_cww_3iz` | 嚭 | [《史記・孔子世家》][29] | [JSON](awq_cww_3iz.json) |
| `ax6_77g_gsd` | 石丞相 | [《史記・田叔列傳》][86] | [JSON](ax6_77g_gsd.json) |
| `axb_rzj_r68` | 臺駘 | [《史記・鄭世家》][24] | [JSON](axb_rzj_r68.json) |
| `axg_i3i_ioc` | 晏嬰 | [《史記・齊太公世家》][14] | [JSON](axg_i3i_ioc.json) |
| `axo_it5_tk0` | 貫髙 | [《史記・張耳陳餘列傳》][71] | [JSON](axo_it5_tk0.json) |
| `axt_oe2_4fw` | 吳廣 | [《史記・李斯列傳》][69] | [JSON](axt_oe2_4fw.json) |
| `axz_rge_e2h` | 子將（齊臣） | [《史記・魯周公世家》][15] | [JSON](axz_rge_e2h.json) |
| `ay6_6gn_kvo` | 汝陰侯滕公未詳名 | [《史記・季布欒布列傳》][82] | [JSON](ay6_6gn_kvo.json) |
| `aya_jle_hkr` | 公仲連 | [《史記・趙世家》][25] | [JSON](aya_jle_hkr.json) |
| `ayq_esq_ghv` | 尹婕妤 | [《史記・外戚世家》][31] | [JSON](ayq_esq_ghv.json) |
| `azb_h5v_rtu` | 郤臻（中軍佐） | [《史記・晉世家》][21] | [JSON](azb_h5v_rtu.json) |
| `b08_8h4_pmi` | 荷蓧丈人（孔子世家未名者） | [《史記・孔子世家》][29] | [JSON](b08_8h4_pmi.json) |
| `b10_tgz_55a` | 子陽 | [《史記・鄭世家》][24] | [JSON](b10_tgz_55a.json) |
| `b1k_e7u_kej` | 禹引古 | [《史記・范睢蔡澤列傳》][61] | [JSON](b1k_e7u_kej.json) |
| `b1o_1ft_704` | 吳客（孔子世家骨節未名者） | [《史記・孔子世家》][29] | [JSON](b1o_1ft_704.json) |
| `b1r_inb_fts` | 樊噲 | [《史記・樊酈滕灌列傳》][77] | [JSON](b1r_inb_fts.json) |
| `b23_5g5_byb` | 周公（共和時） | [《史記・周本紀》][4] | [JSON](b23_5g5_byb.json) |
| `b25_37c_r2x` | 蒲將軍 | [《史記・項羽本紀》][7] | [JSON](b25_37c_r2x.json) |
| `b26_2bj_z9b` | 原憲 | [《史記・仲尼弟子列傳》][49] | [JSON](b26_2bj_z9b.json) |
| `b2d_qc8_y7m` | 蒯聵 | [《史記・趙世家》][25] | [JSON](b2d_qc8_y7m.json) |
| `b2q_ckr_hyx` | 遠吏故事妻 | [《史記・蘇秦列傳》][51] | [JSON](b2q_ckr_hyx.json) |
| `b2s_jfq_0ra` | 衛文公女弟（宋桓公夫人） | [《史記・宋微子世家》][20] | [JSON](b2s_jfq_0ra.json) |
| `b41_mli_il4` | 魏太子申 | [《史記・商君列傳》][50] | [JSON](b41_mli_il4.json) |
| `b4e_iku_zxl` | 太史公（趙世家論贊敘述者） | [《史記・趙世家》][25] | [JSON](b4e_iku_zxl.json) |
| `b4g_yp9_37o` | 客卿灶 | [《史記・秦本紀》][5] | [JSON](b4g_yp9_37o.json) |
| `b4l_2ug_qy3` | 欒大 | [《史記・孝武本紀》][12] | [JSON](b4l_2ug_qy3.json) |
| `b4t_oro_krn` | 樓昌 | [《史記・平原君虞卿列傳》][58] | [JSON](b4t_oro_krn.json) |
| `b4v_jbu_4sr` | 尸子 | [《史記・孟子荀卿列傳》][56] | [JSON](b4v_jbu_4sr.json) |
| `b5p_ukb_hcb` | 泄 | [《史記・夏本紀》][2] | [JSON](b5p_ukb_hcb.json) |
| `b5q_cso_92n` | 子孔 | [《史記・鄭世家》][24] | [JSON](b5q_cso_92n.json) |
| `b5v_sfz_r1u` | 石乞（白公死士） | [《史記・楚世家》][22] | [JSON](b5v_sfz_r1u.json) |
| `b63_kmr_qa6` | 盧蒲嫳 | [《史記・齊太公世家》][14] | [JSON](b63_kmr_qa6.json) |
| `b63_rxr_c4f` | 蒯通 | [《史記・高祖本紀》][8] | [JSON](b63_rxr_c4f.json) |
| `b6b_x4q_wih` | 皇仆 | [《史記・周本紀》][4] | [JSON](b6b_x4q_wih.json) |
| `b6e_72d_vqf` | 楚王莊舄故事 | [《史記・張儀列傳》][52] | [JSON](b6e_72d_vqf.json) |
| `b6f_0d0_nbx` | 韓王（田世家煮棗議論未名者） | [《史記・田敬仲完世家》][28] | [JSON](b6f_0d0_nbx.json) |
| `b6q_m0p_k99` | 伊尹 | [《史記・孟子荀卿列傳》][56] | [JSON](b6q_m0p_k99.json) |
| `b6v_43j_xx8` | 高昭子 | [《史記・孔子世家》][29] | [JSON](b6v_43j_xx8.json) |
| `b6y_c2c_kp6` | 齊女侍者（桑上聽謀者） | [《史記・晉世家》][21] | [JSON](b6y_c2c_kp6.json) |
| `b7k_7g1_8yf` | 太史公 | [《史記・孟子荀卿列傳》][56] | [JSON](b7k_7g1_8yf.json) |
| `b7l_3h4_2hu` | 樊噲 | [《史記・淮陰侯列傳》][74] | [JSON](b7l_3h4_2hu.json) |
| `b7o_fu7_sjf` | 髙柴 | [《史記・仲尼弟子列傳》][49] | [JSON](b7o_fu7_sjf.json) |
| `b7w_mdw_awu` | 袁絲 | [《史記・袁盎鼂錯列傳》][83] | [JSON](b7w_mdw_awu.json) |
| `b83_37f_n0v` | 荊軻 | [《史記・刺客列傳》][68] | [JSON](b83_37f_n0v.json) |
| `b8c_ev6_7ax` | 膠東康王（本卷未名） | [《史記・孝武本紀》][12] | [JSON](b8c_ev6_7ax.json) |
| `bad_bqg_ijn` | 知伯 | [《史記・鄭世家》][24] | [JSON](bad_bqg_ijn.json) |
| `baj_rkd_i0t` | 陳莊 | [《史記・張儀列傳》][52] | [JSON](baj_rkd_i0t.json) |
| `ban_njw_2yn` | 燕丹引古 | [《史記・魯仲連鄒陽列傳》][65] | [JSON](ban_njw_2yn.json) |
| `bas_qk7_iyc` | 后緡 | [《史記・吳太伯世家》][13] | [JSON](bas_qk7_iyc.json) |
| `bb8_fpc_b3e` | 龍賈 | [《史記・秦本紀》][5] | [JSON](bb8_fpc_b3e.json) |
| `bb9_ay5_fta` | 晉厲公 | [《史記・趙世家》][25] | [JSON](bb9_ay5_fta.json) |
| `bbk_ttr_lc5` | 王奢引古 | [《史記・魯仲連鄒陽列傳》][65] | [JSON](bbk_ttr_lc5.json) |
| `bbt_vs5_5ka` | 華無傷 | [《史記・田儋列傳》][76] | [JSON](bbt_vs5_5ka.json) |
| `bc6_jy5_6ia` | 咸陽進言者 | [《史記・項羽本紀》][7] | [JSON](bc6_jy5_6ia.json) |
| `bci_d32_jrt` | 春申 | [《史記・陳涉世家》][30] | [JSON](bci_d32_jrt.json) |
| `bcq_8mf_d5t` | 旋（留公） | [《史記・樊酈滕灌列傳》][77] | [JSON](bcq_8mf_d5t.json) |
| `bcz_ap5_p19` | 主父（田世家趙未名者） | [《史記・田敬仲完世家》][28] | [JSON](bcz_ap5_p19.json) |
| `bd5_w1z_btw` | 毛公 | [《史記・魏公子列傳》][59] | [JSON](bd5_w1z_btw.json) |
| `bdb_k4z_a2p` | 楚威王 | [《史記・孟嘗君列傳》][57] | [JSON](bdb_k4z_a2p.json) |
| `bdo_vu7_rhg` | 朱虎 | [《史記・五帝本紀》][1] | [JSON](bdo_vu7_rhg.json) |
| `bdp_w3v_6nc` | 錦（汾陰巫） | [《史記・孝武本紀》][12] | [JSON](bdp_w3v_6nc.json) |
| `be7_122_810` | 會（臧昭伯弟） | [《史記・魯周公世家》][15] | [JSON](be7_122_810.json) |
| `be9_40v_4al` | 伯鯈 | [《史記・鄭世家》][24] | [JSON](be9_40v_4al.json) |
| `bec_cmv_yf6` | 產 | [《史記・外戚世家》][31] | [JSON](bec_cmv_yf6.json) |
| `beh_dee_mk2` | 晉厲公 | [《史記・鄭世家》][24] | [JSON](beh_dee_mk2.json) |
| `bez_s9y_575` | 梁惠王 | [《史記・魏世家》][26] | [JSON](bez_s9y_575.json) |
| `bf5_80m_ih1` | 管引古 | [《史記・孟子荀卿列傳》][56] | [JSON](bf5_80m_ih1.json) |
| `bfc_uke_v0c` | 鄭國 | [《史記・李斯列傳》][69] | [JSON](bfc_uke_v0c.json) |
| `bff_e4b_8yv` | 楚惠王（滅蔡記事） | [《史記・陳杞世家》][18] | [JSON](bff_e4b_8yv.json) |
| `bfv_clh_n6y` | 趙造 | [《史記・趙世家》][25] | [JSON](bfv_clh_n6y.json) |
| `bfv_gd8_7ty` | 劉賈 | [《史記・荊燕世家》][33] | [JSON](bfv_gd8_7ty.json) |
| `bgb_g5s_np0` | 百里奚引古 | [《史記・李斯列傳》][69] | [JSON](bgb_g5s_np0.json) |
| `bge_04q_zxe` | 范睢引古 | [《史記・李斯列傳》][69] | [JSON](bge_04q_zxe.json) |
| `bgn_wm2_amb` | 熊狂（楚先祖） | [《史記・楚世家》][22] | [JSON](bgn_wm2_amb.json) |
| `bgw_oxa_kg9` | 共太子（西周） | [《史記・周本紀》][4] | [JSON](bgw_oxa_kg9.json) |
| `bhc_ti8_lk7` | 頃王 | [《史記・周本紀》][4] | [JSON](bhc_ti8_lk7.json) |
| `bhp_5xd_88r` | 魏惠王 | [《史記・秦本紀》][5] | [JSON](bhp_5xd_88r.json) |
| `bhx_zqp_1m0` | 勝（河東太守） | [《史記・孝武本紀》][12] | [JSON](bhx_zqp_1m0.json) |
| `bhy_6ln_wvi` | 郯公未詳名 | [《史記・樊酈滕灌列傳》][77] | [JSON](bhy_6ln_wvi.json) |
| `bi7_ukk_d76` | 孔子引古 | [《史記・李斯列傳》][69] | [JSON](bi7_ukk_d76.json) |
| `bic_9dz_hu6` | 韓嚴 | [《史記・韓世家》][27] | [JSON](bic_9dz_hu6.json) |
| `bii_kfo_q7m` | 介山子然 | [《史記・仲尼弟子列傳》][49] | [JSON](bii_kfo_q7m.json) |
| `bit_d2r_h4o` | 孔甲 | [《史記・夏本紀》][2] | [JSON](bit_d2r_h4o.json) |
| `bj4_3sq_ua6` | 箕子引古 | [《史記・樂毅列傳》][62] | [JSON](bj4_3sq_ua6.json) |
| `bj5_9k5_t5c` | 蘇秦母 | [《史記・蘇秦列傳》][51] | [JSON](bj5_9k5_t5c.json) |
| `bjd_so0_6y9` | 公子卬（秦將） | [《史記・秦本紀》][5] | [JSON](bjd_so0_6y9.json) |
| `bji_l4u_wvs` | 太史公 | [《史記・管晏列傳》][44] | [JSON](bji_l4u_wvs.json) |
| `bk0_cz6_i48` | 赤松子 | [《史記・留侯世家》][37] | [JSON](bk0_cz6_i48.json) |
| `bk0_xlz_uod` | 貧人女故事 | [《史記・樗里子甘茂列傳》][53] | [JSON](bk0_xlz_uod.json) |
| `bkf_68m_hxl` | 劇辛 | [《史記・廉頗藺相如列傳》][63] | [JSON](bkf_68m_hxl.json) |
| `bkf_kyo_vhe` | 張儀 | [《史記・田敬仲完世家》][28] | [JSON](bkf_kyo_vhe.json) |
| `bkg_oa7_g5d` | 管夫人 | [《史記・外戚世家》][31] | [JSON](bkg_oa7_g5d.json) |
| `bkr_vp5_w7r` | 太史公 | [《史記・刺客列傳》][68] | [JSON](bkr_vp5_w7r.json) |
| `bkz_jr0_4ey` | 韓厥 | [《史記・韓世家》][27] | [JSON](bkz_jr0_4ey.json) |
| `bl6_mow_siu` | 公孫喜 | [《史記・秦本紀》][5] | [JSON](bl6_mow_siu.json) |
| `ble_6gl_3l8` | 空同氏（趙世家襄子妻未名者） | [《史記・趙世家》][25] | [JSON](ble_6gl_3l8.json) |
| `blo_hqh_iqg` | 小乙 | [《史記・殷本紀》][3] | [JSON](blo_hqh_iqg.json) |
| `blw_xsu_w9q` | 兒寬 | [《史記・萬石張叔列傳》][85] | [JSON](blw_xsu_w9q.json) |
| `blx_v56_6o2` | 廩辛 | [《史記・殷本紀》][3] | [JSON](blx_v56_6o2.json) |
| `bnh_asf_e35` | 舜 | [《史記・伯夷列傳》][43] | [JSON](bnh_asf_e35.json) |
| `bnk_8kb_0y4` | 太史公 | [《史記・白起王翦列傳》][55] | [JSON](bnk_8kb_0y4.json) |
| `bnl_xoy_8z2` | 龍逢引古 | [《史記・魯仲連鄒陽列傳》][65] | [JSON](bnl_xoy_8z2.json) |
| `bnu_h9l_z1o` | 太丁（武乙子） | [《史記・殷本紀》][3] | [JSON](bnu_h9l_z1o.json) |
| `bnv_tw5_0yz` | 公玊帶 | [《史記・孝武本紀》][12] | [JSON](bnv_tw5_0yz.json) |
| `bnz_tdi_29i` | 酈生 | [《史記・酈生陸賈列傳》][79] | [JSON](bnz_tdi_29i.json) |
| `bo5_otw_yvj` | 宋武公（孔子世家正考父所佐） | [《史記・孔子世家》][29] | [JSON](bo5_otw_yvj.json) |
| `bo6_x83_hfu` | 魏咎 | [《史記・魏豹彭越列傳》][72] | [JSON](bo6_x83_hfu.json) |
| `bof_yfp_ill` | 竫公 | [《史記・秦本紀》][5] | [JSON](bof_yfp_ill.json) |
| `bop_rln_19h` | 公孫雄 | [《史記・越王勾踐世家》][23] | [JSON](bop_rln_19h.json) |
| `bpi_u2n_1py` | 女修 | [《史記・秦本紀》][5] | [JSON](bpi_u2n_1py.json) |
| `bpl_8yn_rrf` | 淳于髡 | [《史記・孟子荀卿列傳》][56] | [JSON](bpl_8yn_rrf.json) |
| `bq7_19x_aoe` | 中大夫令齊 | [《史記・秦始皇本紀》][6] | [JSON](bq7_19x_aoe.json) |
| `bqi_nsb_iq4` | 秦惠王 | [《史記・穰侯列傳》][54] | [JSON](bqi_nsb_iq4.json) |
| `bql_o3k_2vn` | 文王 | [《史記・孔子世家》][29] | [JSON](bql_o3k_2vn.json) |
| `bqz_ijs_4pp` | 渉閒 | [《史記・項羽本紀》][7] | [JSON](bqz_ijs_4pp.json) |
| `br3_x48_86w` | 秦繆 | [《史記・孔子世家》][29] | [JSON](br3_x48_86w.json) |
| `bro_0ln_j9p` | 春平君（趙世家未名者） | [《史記・趙世家》][25] | [JSON](bro_0ln_j9p.json) |
| `brx_0of_9p8` | 韓懿侯 | [《史記・魏世家》][26] | [JSON](brx_0of_9p8.json) |
| `bs4_1ga_74d` | 太任 | [《史記・周本紀》][4] | [JSON](bs4_1ga_74d.json) |
| `bsf_8kr_gjr` | 鄭桓公 | [《史記・楚世家》][22] | [JSON](bsf_8kr_gjr.json) |
| `bsx_usd_ats` | 伊尹引古 | [《史記・春申君列傳》][60] | [JSON](bsx_usd_ats.json) |
| `bt3_1wn_4hf` | 綰 | [《史記・孝景本紀》][11] | [JSON](bt3_1wn_4hf.json) |
| `bt8_llh_ecr` | 呂尚引古 | [《史記・范睢蔡澤列傳》][61] | [JSON](bt8_llh_ecr.json) |
| `btf_wl1_z5n` | 黥布 | [《史記・黥布列傳》][73] | [JSON](btf_wl1_z5n.json) |
| `btm_i0w_9n1` | 秦昭王 | [《史記・呂不韋列傳》][67] | [JSON](btm_i0w_9n1.json) |
| `bty_4r4_dtw` | 向壽 | [《史記・穰侯列傳》][54] | [JSON](bty_4r4_dtw.json) |
| `bu8_4ec_il7` | 陽虎 | [《史記・趙世家》][25] | [JSON](bu8_4ec_il7.json) |
| `bua_ysr_cq0` | 公孫詭 | [《史記・魯仲連鄒陽列傳》][65] | [JSON](bua_ysr_cq0.json) |
| `buc_xho_3di` | 武王 | [《史記・孫子吳起列傳》][47] | [JSON](buc_xho_3di.json) |
| `bum_gr7_dzi` | 簡如（鄋瞞記事） | [《史記・魯周公世家》][15] | [JSON](bum_gr7_dzi.json) |
| `buq_0q6_91x` | 雍齒 | [《史記・高祖本紀》][8] | [JSON](buq_0q6_91x.json) |
| `bvb_d1z_fd0` | 尉佗 | [《史記・孝文本紀》][10] | [JSON](bvb_d1z_fd0.json) |
| `bvi_h86_vk1` | 陳軫 | [《史記・張儀列傳》][52] | [JSON](bvi_h86_vk1.json) |
| `bvk_gpk_f1b` | 鄭子產 | [《史記・仲尼弟子列傳》][49] | [JSON](bvk_gpk_f1b.json) |
| `bvo_240_ek3` | 周幽王 | [《史記・周本紀》][4] | [JSON](bvo_240_ek3.json) |
| `bwl_rr1_upp` | 景差 | [《史記・屈原賈生列傳》][66] | [JSON](bwl_rr1_upp.json) |
| `bwv_ob8_6xi` | 共敖 | [《史記・項羽本紀》][7] | [JSON](bwv_ob8_6xi.json) |
| `bwv_p3h_q1j` | 趙賁 | [《史記・曹相國世家》][36] | [JSON](bwv_p3h_q1j.json) |
| `bwx_d97_fb5` | 太康 | [《史記・夏本紀》][2] | [JSON](bwx_d97_fb5.json) |
| `bx9_am2_k4h` | 欒書 | [《史記・趙世家》][25] | [JSON](bx9_am2_k4h.json) |
| `bxk_5iq_ogx` | 絳（列侯用稱） | [《史記・淮陰侯列傳》][74] | [JSON](bxk_5iq_ogx.json) |
| `bxr_8km_7zg` | 襄平侯通 | [《史記・孝文本紀》][10] | [JSON](bxr_8km_7zg.json) |
| `bxt_j9p_lj9` | 伯姬（蒯聵姊、孔悝母） | [《史記・衛康叔世家》][19] | [JSON](bxt_j9p_lj9.json) |
| `bxu_47d_1lv` | 子陽 | [《史記・扁鵲倉公列傳》][87] | [JSON](bxu_47d_1lv.json) |
| `bye_bxt_gks` | 季平子 | [《史記・孔子世家》][29] | [JSON](bye_bxt_gks.json) |
| `byn_obj_9yj` | 夫差 | [《史記・酈生陸賈列傳》][79] | [JSON](byn_obj_9yj.json) |
| `byo_1xs_pax` | 燕王喜 | [《史記・樗里子甘茂列傳》][53] | [JSON](byo_1xs_pax.json) |
| `bz0_g4p_1o5` | 晏嬰 | [《史記・齊太公世家》][14] | [JSON](bz0_g4p_1o5.json) |
| `bz6_7ka_tht` | 范齊 | [《史記・韓信盧綰列傳》][75] | [JSON](bz6_7ka_tht.json) |
| `bz9_nkh_ebk` | 張儀妻 | [《史記・張儀列傳》][52] | [JSON](bz9_nkh_ebk.json) |
| `bzo_2h9_2wd` | 齊景公 | [《史記・孔子世家》][29] | [JSON](bzo_2h9_2wd.json) |
| `bzw_kmw_yhu` | 武（古王引語） | [《史記・酈生陸賈列傳》][79] | [JSON](bzw_kmw_yhu.json) |
| `c02_5lv_kt3` | 春申楚君 | [《史記・春申君列傳》][60] | [JSON](c02_5lv_kt3.json) |
| `c0u_sd1_13u` | 劉敬 | [《史記・劉敬叔孫通列傳》][81] | [JSON](c0u_sd1_13u.json) |
| `c18_pif_asp` | 犖（圉人） | [《史記・魯周公世家》][15] | [JSON](c18_pif_asp.json) |
| `c1o_5sb_6my` | 韓王成 | [《史記・韓信盧綰列傳》][75] | [JSON](c1o_5sb_6my.json) |
| `c1q_qcc_hwm` | 子嬰 | [《史記・秦始皇本紀》][6] | [JSON](c1q_qcc_hwm.json) |
| `c23_24c_gpm` | 膠西王卬 | [《史記・老子韓非列傳》][45] | [JSON](c23_24c_gpm.json) |
| `c29_dz7_9t4` | 囊瓦（子常） | [《史記・管蔡世家》][17] | [JSON](c29_dz7_9t4.json) |
| `c2a_8kr_ki8` | 扈輒 | [《史記・秦始皇本紀》][6] | [JSON](c2a_8kr_ki8.json) |
| `c2i_ybj_ryx` | 孝昭 | [《史記・屈原賈生列傳》][66] | [JSON](c2i_ybj_ryx.json) |
| `c2t_tz0_ic9` | 解狐（祁傒所薦者） | [《史記・晉世家》][21] | [JSON](c2t_tz0_ic9.json) |
| `c30_pt8_774` | 顏聚（引古） | [《史記・蒙恬列傳》][70] | [JSON](c30_pt8_774.json) |
| `c31_ept_hu4` | 周敬王 | [《史記・鄭世家》][24] | [JSON](c31_ept_hu4.json) |
| `c38_dzq_0o4` | 屈丐 | [《史記・張儀列傳》][52] | [JSON](c38_dzq_0o4.json) |
| `c3r_z15_12i` | 韓相國（韓世家華陽未名者） | [《史記・韓世家》][27] | [JSON](c3r_z15_12i.json) |
| `c47_gko_qgr` | 魏王須賈引語 | [《史記・穰侯列傳》][54] | [JSON](c47_gko_qgr.json) |
| `c4o_fny_0vd` | 堯 | [《史記・劉敬叔孫通列傳》][81] | [JSON](c4o_fny_0vd.json) |
| `c4w_uo5_66h` | 孟釐子 | [《史記・孔子世家》][29] | [JSON](c4w_uo5_66h.json) |
| `c56_xgh_owp` | 胡亥 | [《史記・劉敬叔孫通列傳》][81] | [JSON](c56_xgh_owp.json) |
| `c59_t5o_6dk` | 楚平王（引古） | [《史記・蒙恬列傳》][70] | [JSON](c59_t5o_6dk.json) |
| `c5j_5bu_v0o` | 魏尚 | [《史記・張釋之馮唐列傳》][84] | [JSON](c5j_5bu_v0o.json) |
| `c5t_8kk_hd5` | 夏說 | [《史記・張耳陳餘列傳》][71] | [JSON](c5t_8kk_hd5.json) |
| `c68_rcg_qsu` | 皇太后未名（建元語境） | [《史記・萬石張叔列傳》][85] | [JSON](c68_rcg_qsu.json) |
| `c6v_07v_vxz` | 種（袁盎兄子） | [《史記・袁盎鼂錯列傳》][83] | [JSON](c6v_07v_vxz.json) |
| `c78_536_k7y` | 楊何 | [《史記・仲尼弟子列傳》][49] | [JSON](c78_536_k7y.json) |
| `c7c_u1x_vni` | 晉文侯 | [《史記・趙世家》][25] | [JSON](c7c_u1x_vni.json) |
| `c7w_nyj_95u` | 曾參 | [《史記・仲尼弟子列傳》][49] | [JSON](c7w_nyj_95u.json) |
| `c8b_f8t_ylf` | 欒書 | [《史記・晉世家》][21] | [JSON](c8b_f8t_ylf.json) |
| `c8v_5v6_309` | 甯昌 | [《史記・高祖本紀》][8] | [JSON](c8v_5v6_309.json) |
| `c90_m9w_lqu` | 呂釋之 | [《史記・呂太后本紀》][9] | [JSON](c90_m9w_lqu.json) |
| `c92_v5d_med` | 陸終（楚篇祖系） | [《史記・楚世家》][22] | [JSON](c92_v5d_med.json) |
| `c93_3hq_rqm` | 應侯 | [《史記・平原君虞卿列傳》][58] | [JSON](c93_3hq_rqm.json) |
| `c9b_upc_ym4` | 嫪毐 | [《史記・呂不韋列傳》][67] | [JSON](c9b_upc_ym4.json) |
| `c9d_eyb_lp5` | 悼公（韓世家被弒未名者） | [《史記・韓世家》][27] | [JSON](c9d_eyb_lp5.json) |
| `c9n_rjf_cwd` | 陽周使者未名 | [《史記・蒙恬列傳》][70] | [JSON](c9n_rjf_cwd.json) |
| `c9y_o6o_wvn` | 齊簡公 | [《史記・齊太公世家》][14] | [JSON](c9y_o6o_wvn.json) |
| `ca1_8ty_axt` | 周後（封周子南君未名） | [《史記・孝武本紀》][12] | [JSON](ca1_8ty_axt.json) |
| `ca5_zxe_kxk` | 陳女（衛莊公夫人） | [《史記・衛康叔世家》][19] | [JSON](ca5_zxe_kxk.json) |
| `can_0qj_fka` | 龍且 | [《史記・傅靳蒯成列傳》][80] | [JSON](can_0qj_fka.json) |
| `cat_72w_jpo` | 搖 | [《史記・越王勾踐世家》][23] | [JSON](cat_72w_jpo.json) |
| `caz_735_cfr` | 燕王蘇秦引古未名 | [《史記・魯仲連鄒陽列傳》][65] | [JSON](caz_735_cfr.json) |
| `cbe_j1r_ru1` | 後子鍼 | [《史記・秦本紀》][5] | [JSON](cbe_j1r_ru1.json) |
| `cbw_dwt_6vf` | 信陵魏君 | [《史記・魏公子列傳》][59] | [JSON](cbw_dwt_6vf.json) |
| `cby_w5h_loi` | 公子揮（隱公時） | [《史記・魯周公世家》][15] | [JSON](cby_w5h_loi.json) |
| `cbz_512_ef1` | 趙成季 | [《史記・韓世家》][27] | [JSON](cbz_512_ef1.json) |
| `cc1_svd_sxi` | 幕（陳篇世系引語） | [《史記・陳杞世家》][18] | [JSON](cc1_svd_sxi.json) |
| `cc2_r4q_j5y` | 盧綰 | [《史記・韓信盧綰列傳》][75] | [JSON](cc2_r4q_j5y.json) |
| `cc6_hl9_128` | 奮 | [《史記・陳丞相世家》][38] | [JSON](cc6_hl9_128.json) |
| `ccg_ycv_y85` | 慎夫人 | [《史記・張釋之馮唐列傳》][84] | [JSON](ccg_ycv_y85.json) |
| `ccv_1jr_0jn` | 晁錯 | [《史記・齊悼惠王世家》][34] | [JSON](ccv_1jr_0jn.json) |
| `ccx_50c_ssi` | 寧越 | [《史記・秦始皇本紀》][6] | [JSON](ccx_50c_ssi.json) |
| `cdg_kvt_y0p` | 虞卿 | [《史記・平原君虞卿列傳》][58] | [JSON](cdg_kvt_y0p.json) |
| `cdl_qsi_xdj` | 張儀 | [《史記・趙世家》][25] | [JSON](cdl_qsi_xdj.json) |
| `ce2_d95_01s` | 信陵魏君 | [《史記・魏公子列傳》][59] | [JSON](ce2_d95_01s.json) |
| `cez_do1_byp` | 趙平原君 | [《史記・孟嘗君列傳》][57] | [JSON](cez_do1_byp.json) |
| `cez_le6_frl` | 太史公 | [《史記・酈生陸賈列傳》][79] | [JSON](cez_le6_frl.json) |
| `cf1_j34_un3` | 子貢 | [《史記・伍子胥列傳》][48] | [JSON](cf1_j34_un3.json) |
| `cfe_5pa_uvn` | 子閭（楚昭王弟） | [《史記・楚世家》][22] | [JSON](cfe_5pa_uvn.json) |
| `cfk_4it_4yn` | 郭蒙 | [《史記・高祖本紀》][8] | [JSON](cfk_4it_4yn.json) |
| `cfp_6vv_wdr` | 夷皋 | [《史記・趙世家》][25] | [JSON](cfp_6vv_wdr.json) |
| `cg8_qo1_c39` | 紅（熊渠中子鄂王） | [《史記・楚世家》][22] | [JSON](cg8_qo1_c39.json) |
| `cg9_yco_y2z` | 張買 | [《史記・呂太后本紀》][9] | [JSON](cg9_yco_y2z.json) |
| `cg9_z9s_tw8` | 孟蘭皋 | [《史記・商君列傳》][50] | [JSON](cg9_z9s_tw8.json) |
| `cgc_imx_hn5` | 仲由 | [《史記・仲尼弟子列傳》][49] | [JSON](cgc_imx_hn5.json) |
| `cgn_4cw_i0o` | 公孫支 | [《史記・趙世家》][25] | [JSON](cgn_4cw_i0o.json) |
| `ch1_cu1_wfj` | 晉文公引古 | [《史記・魯仲連鄒陽列傳》][65] | [JSON](ch1_cu1_wfj.json) |
| `che_kst_jnn` | 公子朝（衞） | [《史記・吳太伯世家》][13] | [JSON](che_kst_jnn.json) |
| `chh_mde_x8x` | 馮 | [《史記・鄭世家》][24] | [JSON](chh_mde_x8x.json) |
| `chj_jwd_e4f` | 秦莊襄王 | [《史記・范睢蔡澤列傳》][61] | [JSON](chj_jwd_e4f.json) |
| `chm_jfj_3y8` | 管引古短稱未定 | [《史記・魯仲連鄒陽列傳》][65] | [JSON](chm_jfj_3y8.json) |
| `chn_cq4_nzo` | 秦皇帝 | [《史記・蕭相國世家》][35] | [JSON](chn_cq4_nzo.json) |
| `chp_5kd_7fb` | 魏冉 | [《史記・田敬仲完世家》][28] | [JSON](chp_5kd_7fb.json) |
| `ci2_vzk_6ry` | 彭越 | [《史記・酈生陸賈列傳》][79] | [JSON](ci2_vzk_6ry.json) |
| `cib_z4c_cbq` | 灌（列侯用稱） | [《史記・淮陰侯列傳》][74] | [JSON](cib_z4c_cbq.json) |
| `cid_65s_8up` | 郢人 | [《史記・荊燕世家》][33] | [JSON](cid_65s_8up.json) |
| `cij_zvk_7rn` | 秦武王后 | [《史記・秦本紀》][5] | [JSON](cij_zvk_7rn.json) |
| `cir_0db_bfw` | 齊丞相壽 | [《史記・呂太后本紀》][9] | [JSON](cir_0db_bfw.json) |
| `cjo_gf9_e2j` | 周類 | [《史記・樊酈滕灌列傳》][77] | [JSON](cjo_gf9_e2j.json) |
| `cjp_mjw_yng` | 呂通 | [《史記・呂太后本紀》][9] | [JSON](cjp_mjw_yng.json) |
| `ck6_yav_z22` | 張子卿 | [《史記・荊燕世家》][33] | [JSON](ck6_yav_z22.json) |
| `ck7_0oc_r4j` | 曼成然（告初王者） | [《史記・楚世家》][22] | [JSON](ck7_0oc_r4j.json) |
| `ck9_676_tlm` | 關其思 | [《史記・老子韓非列傳》][45] | [JSON](ck9_676_tlm.json) |
| `ckv_ev3_1vi` | 司馬梗 | [《史記・秦本紀》][5]、[《史記・白起王翦列傳》][55] | [JSON](ckv_ev3_1vi.json) |
| `cl3_0w4_ya1` | 田盻子（楚篇齊臣） | [《史記・楚世家》][22] | [JSON](cl3_0w4_ya1.json) |
| `cl4_p3h_bpz` | 蒙驁 | [《史記・魏公子列傳》][59] | [JSON](cl4_p3h_bpz.json) |
| `cl5_pg2_s79` | 田都 | [《史記・項羽本紀》][7] | [JSON](cl5_pg2_s79.json) |
| `cl7_1pf_m9j` | 韓公叔 | [《史記・樗里子甘茂列傳》][53] | [JSON](cl7_1pf_m9j.json) |
| `cld_aan_e20` | 武丁 | [《史記・殷本紀》][3] | [JSON](cld_aan_e20.json) |
| `clj_4gu_9bw` | 韓哀（列國君主） | [《史記・秦本紀》][5]、[《史記・晉世家》][21] | [JSON](clj_4gu_9bw.json) |
| `clw_2zf_477` | 朱建母未名 | [《史記・酈生陸賈列傳》][79] | [JSON](clw_2zf_477.json) |
| `cm7_og0_w7q` | 皋（夏王） | [《史記・夏本紀》][2] | [JSON](cm7_og0_w7q.json) |
| `cma_1u0_x5e` | 叔向 | [《史記・鄭世家》][24] | [JSON](cma_1u0_x5e.json) |
| `cme_bmz_6qx` | 英布所幸姬未名 | [《史記・黥布列傳》][73] | [JSON](cme_bmz_6qx.json) |
| `cmh_x83_hjk` | 蜀侯煇 | [《史記・秦本紀》][5] | [JSON](cmh_x83_hjk.json) |
| `cml_pmg_4g7` | 王武 | [《史記・傅靳蒯成列傳》][80] | [JSON](cml_pmg_4g7.json) |
| `cmu_mm9_y05` | 內史騰 | [《史記・秦始皇本紀》][6] | [JSON](cmu_mm9_y05.json) |
| `cn8_id5_95v` | 秦昭王 | [《史記・范睢蔡澤列傳》][61] | [JSON](cn8_id5_95v.json) |
| `cno_x3i_mx4` | 士燮 | [《史記・齊太公世家》][14] | [JSON](cno_x3i_mx4.json) |
| `co1_fld_bmx` | 太史伯 | [《史記・鄭世家》][24] | [JSON](co1_fld_bmx.json) |
| `cof_m2m_hgi` | 熊麗（楚先祖） | [《史記・楚世家》][22] | [JSON](cof_m2m_hgi.json) |
| `cok_fra_foo` | 周昌 | [《史記・韓信盧綰列傳》][75] | [JSON](cok_fra_foo.json) |
| `coy_kpb_pfl` | 紂引古 | [《史記・樂毅列傳》][62] | [JSON](coy_kpb_pfl.json) |
| `coz_ul3_g8w` | 宰予 | [《史記・孔子世家》][29] | [JSON](coz_ul3_g8w.json) |
| `cp2_vf3_igr` | 魯昭公 | [《史記・魯周公世家》][15] | [JSON](cp2_vf3_igr.json) |
| `cpa_nf6_chj` | 田都 | [《史記・項羽本紀》][7] | [JSON](cpa_nf6_chj.json) |
| `cpz_emh_3e9` | 右公子（衛伋傅） | [《史記・衛康叔世家》][19] | [JSON](cpz_emh_3e9.json) |
| `cq4_gz4_67r` | 楚共王 | [《史記・鄭世家》][24] | [JSON](cq4_gz4_67r.json) |
| `cqb_a3u_l7y` | 賁赫 | [《史記・黥布列傳》][73] | [JSON](cqb_a3u_l7y.json) |
| `cqw_m1b_mk5` | 勝（陳哀公子） | [《史記・陳杞世家》][18] | [JSON](cqw_m1b_mk5.json) |
| `cr3_n7l_ek6` | 庶長改 | [《史記・秦本紀》][5] | [JSON](cr3_n7l_ek6.json) |
| `crw_0bp_tv7` | 晉定公 | [《史記・韓世家》][27] | [JSON](crw_0bp_tv7.json) |
| `crw_kww_5qn` | 老子 | [《史記・仲尼弟子列傳》][49] | [JSON](crw_kww_5qn.json) |
| `css_bys_twl` | 韓長孺 | [《史記・梁孝王世家》][40] | [JSON](css_bys_twl.json) |
| `ct9_9gi_txz` | 秦王長平未名 | [《史記・平原君虞卿列傳》][58] | [JSON](ct9_9gi_txz.json) |
| `ct9_yjs_xjr` | 李歸 | [《史記・陳涉世家》][30] | [JSON](ct9_yjs_xjr.json) |
| `ctd_4t7_tmc` | 禹 | [《史記・蘇秦列傳》][51] | [JSON](ctd_4t7_tmc.json) |
| `cte_yao_v47` | 季心 | [《史記・季布欒布列傳》][82] | [JSON](cte_yao_v47.json) |
| `ctl_rtd_6df` | 魏豹 | [《史記・魏豹彭越列傳》][72] | [JSON](ctl_rtd_6df.json) |
| `cuz_4hf_i52` | 子夏 | [《史記・孔子世家》][29] | [JSON](cuz_4hf_i52.json) |
| `cvy_rt4_kwy` | 景駒 | [《史記・項羽本紀》][7] | [JSON](cvy_rt4_kwy.json) |
| `cwo_p3o_pnj` | 鄖公 | [《史記・伍子胥列傳》][48] | [JSON](cwo_p3o_pnj.json) |
| `cwr_47k_5ds` | 陳軫 | [《史記・陳涉世家》][30] | [JSON](cwr_47k_5ds.json) |
| `cxt_wg1_9qm` | 項羽 | [《史記・季布欒布列傳》][82] | [JSON](cxt_wg1_9qm.json) |
| `cxz_e3l_l70` | 趙武 | [《史記・趙世家》][25] | [JSON](cxz_e3l_l70.json) |
| `cy4_4y3_3er` | 季心 | [《史記・季布欒布列傳》][82] | [JSON](cy4_4y3_3er.json) |
| `cya_zvr_rpv` | 徐偃王 | [《史記・趙世家》][25] | [JSON](cya_zvr_rpv.json) |
| `cyi_wjz_uxt` | 項伯 | [《史記・項羽本紀》][7] | [JSON](cyi_wjz_uxt.json) |
| `cyl_qxa_g8o` | 成王 | [《史記・魯周公世家》][15] | [JSON](cyl_qxa_g8o.json) |
| `cyo_vyj_6o2` | 接輿 | [《史記・孔子世家》][29] | [JSON](cyo_vyj_6o2.json) |
| `czz_xfb_r7x` | 書信太后 | [《史記・蘇秦列傳》][51] | [JSON](czz_xfb_r7x.json) |
| `d0b_8uf_u5w` | 郤宛 | [《史記・伍子胥列傳》][48] | [JSON](d0b_8uf_u5w.json) |
| `d0c_mzc_xon` | 魏無忌 | [《史記・秦本紀》][5]、[《史記・高祖本紀》][8] | [JSON](d0c_mzc_xon.json) |
| `d0s_8m9_sci` | 太姜 | [《史記・周本紀》][4] | [JSON](d0s_8m9_sci.json) |
| `d0z_er0_gco` | 王離 | [《史記・曹相國世家》][36] | [JSON](d0z_er0_gco.json) |
| `d1q_nn7_fvn` | 趙夷吾 | [《史記・楚元王世家》][32] | [JSON](d1q_nn7_fvn.json) |
| `d1r_5dd_9tm` | 燕質子 | [《史記・蘇秦列傳》][51] | [JSON](d1r_5dd_9tm.json) |
| `d28_lyw_tjf` | 顏聚 | [《史記・趙世家》][25]、[《史記・廉頗藺相如列傳》][63] | [JSON](d28_lyw_tjf.json) |
| `d31_kms_f7h` | 李牧 | [《史記・秦始皇本紀》][6]、[《史記・燕召公世家》][16] | [JSON](d31_kms_f7h.json) |
| `d31_nve_gr6` | 被廢太子未名 | [《史記・萬石張叔列傳》][85] | [JSON](d31_nve_gr6.json) |
| `d31_spk_c5m` | 燕周 | [《史記・趙世家》][25] | [JSON](d31_spk_c5m.json) |
| `d3p_px2_tmf` | 衞靈公 | [《史記・孔子世家》][29] | [JSON](d3p_px2_tmf.json) |
| `d4o_xs0_n1j` | 趙蔥 | [《史記・趙世家》][25]、[《史記・廉頗藺相如列傳》][63] | [JSON](d4o_xs0_n1j.json) |
| `d54_3hk_joc` | 李醯 | [《史記・扁鵲倉公列傳》][87] | [JSON](d54_3hk_joc.json) |
| `d5a_qyv_5a6` | 子服景伯 | [《史記・魯周公世家》][15] | [JSON](d5a_qyv_5a6.json) |
| `d5i_2yx_pft` | 殷王未詳名 | [《史記・樊酈滕灌列傳》][77] | [JSON](d5i_2yx_pft.json) |
| `d6k_t0w_99b` | 穰侯引古 | [《史記・李斯列傳》][69] | [JSON](d6k_t0w_99b.json) |
| `d70_b62_mly` | 知伯 | [《史記・樗里子甘茂列傳》][53] | [JSON](d70_b62_mly.json) |
| `d75_oh8_6xl` | 霍伯（襄公六年卒者） | [《史記・晉世家》][21] | [JSON](d75_oh8_6xl.json) |
| `d77_fah_85y` | 燕悼（列國君主） | [《史記・秦本紀》][5] | [JSON](d77_fah_85y.json) |
| `d7e_wsc_ujq` | 呂祿 | [《史記・楚元王世家》][32] | [JSON](d7e_wsc_ujq.json) |
| `d7k_yfy_48i` | 高圉 | [《史記・周本紀》][4] | [JSON](d7k_yfy_48i.json) |
| `d7l_uch_op6` | 布（故將軍） | [《史記・孝景本紀》][11] | [JSON](d7l_uch_op6.json) |
| `d7n_zpt_kt4` | 楚惠王 | [《史記・楚世家》][22] | [JSON](d7n_zpt_kt4.json) |
| `d85_rbs_9sv` | 劉賈 | [《史記・荊燕世家》][33] | [JSON](d85_rbs_9sv.json) |
| `d8c_dea_li8` | 田乞 | [《史記・田敬仲完世家》][28] | [JSON](d8c_dea_li8.json) |
| `d8k_3w1_ta8` | 鍾離眛 | [《史記・陳丞相世家》][38] | [JSON](d8k_3w1_ta8.json) |
| `d8s_9jm_qyc` | 周王 | [《史記・張儀列傳》][52] | [JSON](d8s_9jm_qyc.json) |
| `d8y_r3m_ivr` | 陳侯（石碏共謀記事） | [《史記・衛康叔世家》][19] | [JSON](d8y_r3m_ivr.json) |
| `d9l_4lw_kc2` | 項梁 | [《史記・樊酈滕灌列傳》][77] | [JSON](d9l_4lw_kc2.json) |
| `d9l_gw6_hc0` | 黃帝 | [《史記・外戚世家》][31] | [JSON](d9l_gw6_hc0.json) |
| `d9r_fyd_lvn` | 夷姜（衛宣公夫人） | [《史記・衛康叔世家》][19] | [JSON](d9r_fyd_lvn.json) |
| `d9t_tnl_qbw` | 堯 | [《史記・蘇秦列傳》][51] | [JSON](d9t_tnl_qbw.json) |
| `d9u_3uy_sms` | 魏豹 | [《史記・魏豹彭越列傳》][72] | [JSON](d9u_3uy_sms.json) |
| `d9w_fkp_wp3` | 魏公子無忌 | [《史記・魏公子列傳》][59] | [JSON](d9w_fkp_wp3.json) |
| `da9_8rf_0us` | 涉 | [《史記・孔子世家》][29] | [JSON](da9_8rf_0us.json) |
| `db0_yyf_4td` | 許暦 | [《史記・廉頗藺相如列傳》][63] | [JSON](db0_yyf_4td.json) |
| `db9_3sk_h2i` | 秦昭王幸姬未名 | [《史記・孟嘗君列傳》][57] | [JSON](db9_3sk_h2i.json) |
| `dbp_8hk_z35` | 樓煩王（趙世家未名者） | [《史記・趙世家》][25] | [JSON](dbp_8hk_z35.json) |
| `dbu_31o_zf6` | 秦太后（魏世家无忌議論未名者） | [《史記・魏世家》][26] | [JSON](dbu_31o_zf6.json) |
| `dc4_qnx_hp2` | 晉鄙 | [《史記・魏公子列傳》][59] | [JSON](dc4_qnx_hp2.json) |
| `dco_hwr_j82` | 昌文君 | [《史記・秦始皇本紀》][6] | [JSON](dco_hwr_j82.json) |
| `dcp_1gr_65s` | 羲仲 | [《史記・五帝本紀》][1] | [JSON](dcp_1gr_65s.json) |
| `dd0_uda_xje` | 晉平公 | [《史記・趙世家》][25] | [JSON](dd0_uda_xje.json) |
| `dda_1pf_g3o` | 駱甲 | [《史記・樊酈滕灌列傳》][77] | [JSON](dda_1pf_g3o.json) |
| `ddb_bi5_eco` | 韓信 | [《史記・淮陰侯列傳》][74] | [JSON](ddb_bi5_eco.json) |
| `ddb_l4j_4j2` | 舜 | [《史記・五帝本紀》][1] | [JSON](ddb_l4j_4j2.json) |
| `ddd_32x_k8h` | 膠東王書信未名 | [《史記・吳王濞列傳》][88] | [JSON](ddd_32x_k8h.json) |
| `ddf_jql_z0y` | 宣太后 | [《史記・樗里子甘茂列傳》][53] | [JSON](ddf_jql_z0y.json) |
| `ddp_ol8_1w5` | 司馬遷 | [《史記・秦始皇本紀》][6] | [JSON](ddp_ol8_1w5.json) |
| `de9_bqj_6wy` | 屠中少年未名 | [《史記・淮陰侯列傳》][74] | [JSON](de9_bqj_6wy.json) |
| `dep_bjj_vwe` | 蟜（長公主子） | [《史記・孝景本紀》][11] | [JSON](dep_bjj_vwe.json) |
| `dfq_kor_hpu` | 祁傒（薦人者） | [《史記・晉世家》][21] | [JSON](dfq_kor_hpu.json) |
| `dfy_5r0_ek4` | 田文子 | [《史記・齊太公世家》][14] | [JSON](dfy_5r0_ek4.json) |
| `dfy_jd8_999` | 張同 | [《史記・項羽本紀》][7] | [JSON](dfy_jd8_999.json) |
| `dfz_u6h_g3y` | 衛使（齊頃宴使未名） | [《史記・晉世家》][21] | [JSON](dfz_u6h_g3y.json) |
| `dg7_r3z_0tk` | 孔子 | [《史記・外戚世家》][31] | [JSON](dg7_r3z_0tk.json) |
| `dgh_7wa_4c5` | 田間 | [《史記・田儋列傳》][76] | [JSON](dgh_7wa_4c5.json) |
| `dgt_1d3_vg8` | 秦惠王引古 | [《史記・李斯列傳》][69] | [JSON](dgt_1d3_vg8.json) |
| `dgz_tme_821` | 魯定公 | [《史記・孔子世家》][29] | [JSON](dgz_tme_821.json) |
| `dgz_z4a_to4` | 被虜魏太子（趙世家未名者） | [《史記・趙世家》][25] | [JSON](dgz_z4a_to4.json) |
| `dh1_24y_t56` | 犀首 | [《史記・蘇秦列傳》][51] | [JSON](dh1_24y_t56.json) |
| `dhg_342_gdf` | 段（鄭伯弟） | [《史記・衛康叔世家》][19] | [JSON](dhg_342_gdf.json) |
| `dhq_jrq_2tw` | 鬻熊（楚先祖） | [《史記・楚世家》][22] | [JSON](dhq_jrq_2tw.json) |
| `dhs_j6g_06s` | 呂不韋（楚篇秦相） | [《史記・呂不韋列傳》][67] | [JSON](dhs_j6g_06s.json) |
| `dhu_m3k_yii` | 當道者（趙世家神異敘事未名者） | [《史記・趙世家》][25] | [JSON](dhu_m3k_yii.json) |
| `dhv_na8_x3q` | 渉賓 | [《史記・趙世家》][25] | [JSON](dhv_na8_x3q.json) |
| `di1_tea_bkj` | 曲沃莊伯 | [《史記・楚世家》][22] | [JSON](di1_tea_bkj.json) |
| `dic_j3m_5rx` | 淮南王未具名 | [《史記・張釋之馮唐列傳》][84] | [JSON](dic_j3m_5rx.json) |
| `dik_hub_0os` | 老子引稱 | [《史記・扁鵲倉公列傳》][87] | [JSON](dik_hub_0os.json) |
| `dip_c4z_kc6` | 韓安國 | [《史記・萬石張叔列傳》][85] | [JSON](dip_c4z_kc6.json) |
| `dj2_abb_e9l` | 成公（燕孝公後） | [《史記・燕召公世家》][16] | [JSON](dj2_abb_e9l.json) |
| `djb_njc_1kd` | 秦昭王 | [《史記・廉頗藺相如列傳》][63] | [JSON](djb_njc_1kd.json) |
| `djc_n3a_hms` | 建的美人子（未名） | [《史記・呂太后本紀》][9] | [JSON](djc_n3a_hms.json) |
| `djd_opf_kwf` | 韓信 | [《史記・淮陰侯列傳》][74] | [JSON](djd_opf_kwf.json) |
| `djd_pvu_i6v` | 夷逸 | [《史記・孔子世家》][29] | [JSON](djd_pvu_i6v.json) |
| `djm_aky_j4f` | 唐舉 | [《史記・范睢蔡澤列傳》][61] | [JSON](djm_aky_j4f.json) |
| `djp_k1v_gxx` | 小甲 | [《史記・殷本紀》][3] | [JSON](djp_k1v_gxx.json) |
| `djv_oak_6lj` | 諸呂女（友后） | [《史記・呂太后本紀》][9] | [JSON](djv_oak_6lj.json) |
| `dk6_96b_fol` | 孟嘗齊君 | [《史記・孟嘗君列傳》][57] | [JSON](dk6_96b_fol.json) |
| `dkc_j4z_klk` | 卓子 | [《史記・晉世家》][21] | [JSON](dkc_j4z_klk.json) |
| `dko_o9v_cf7` | 陶朱（引文稱呼） | [《史記・秦始皇本紀》][6] | [JSON](dko_o9v_cf7.json) |
| `dlj_z70_agw` | 郎中令循 | [《史記・扁鵲倉公列傳》][87] | [JSON](dlj_z70_agw.json) |
| `dlo_vgs_o6c` | 叔段 | [《史記・鄭世家》][24] | [JSON](dlo_vgs_o6c.json) |
| `dlr_lwl_clv` | 燕昭王 | [《史記・張儀列傳》][52] | [JSON](dlr_lwl_clv.json) |
| `dlu_57f_6uq` | 程姬 | [《史記・五宗世家》][41] | [JSON](dlu_57f_6uq.json) |
| `dmj_kii_tgq` | 熊繹（楚先祖） | [《史記・楚世家》][22] | [JSON](dmj_kii_tgq.json) |
| `dmn_8r0_7nc` | 胡君 | [《史記・老子韓非列傳》][45] | [JSON](dmn_8r0_7nc.json) |
| `dmy_cng_1ol` | 張耳 | [《史記・曹相國世家》][36] | [JSON](dmy_cng_1ol.json) |
| `dn5_bzg_3uf` | 劉累 | [《史記・夏本紀》][2] | [JSON](dn5_bzg_3uf.json) |
| `dn5_zej_pi4` | 遠吏故事私者 | [《史記・蘇秦列傳》][51] | [JSON](dn5_zej_pi4.json) |
| `dn9_0bf_0rg` | 燕王（趙世家攻趙未名者） | [《史記・趙世家》][25] | [JSON](dn9_0bf_0rg.json) |
| `dna_233_hvk` | 吳王闔廬 | [《史記・吳太伯世家》][13] | [JSON](dna_233_hvk.json) |
| `dnb_rcf_15u` | 田光 | [《史記・樊酈滕灌列傳》][77] | [JSON](dnb_rcf_15u.json) |
| `dnk_4l4_x8s` | 里吏未名 | [《史記・張耳陳餘列傳》][71] | [JSON](dnk_4l4_x8s.json) |
| `dnm_d15_o58` | 韓眾 | [《史記・秦始皇本紀》][6] | [JSON](dnm_d15_o58.json) |
| `dnw_uzl_q9q` | 鄭定公 | [《史記・伍子胥列傳》][48] | [JSON](dnw_uzl_q9q.json) |
| `dnz_dal_a9s` | 伯氏子（郤宛宗姓奔吳者） | [《史記・楚世家》][22] | [JSON](dnz_dal_a9s.json) |
| `doa_gbf_ent` | 康（成康合稱） | [《史記・劉敬叔孫通列傳》][81] | [JSON](doa_gbf_ent.json) |
| `doj_zhx_nm1` | 韓安國 | [《史記・梁孝王世家》][40] | [JSON](doj_zhx_nm1.json) |
| `dok_si1_ksk` | 周子 | [《史記・田敬仲完世家》][28] | [JSON](dok_si1_ksk.json) |
| `dp6_alh_k8g` | 文公（燕武公後） | [《史記・燕召公世家》][16] | [JSON](dp6_alh_k8g.json) |
| `dpe_gcv_w1b` | 羋戎 | [《史記・韓世家》][27] | [JSON](dpe_gcv_w1b.json) |
| `dpm_ilj_9bs` | 齊王（商於失約未名者） | [《史記・楚世家》][22] | [JSON](dpm_ilj_9bs.json) |
| `dpn_mmt_rm9` | 端木賜 | [《史記・仲尼弟子列傳》][49] | [JSON](dpn_mmt_rm9.json) |
| `dpq_m7y_b7q` | 潁校勘侯 | [《史記・絳侯周勃世家》][39] | [JSON](dpq_m7y_b7q.json) |
| `dpt_ry7_e1z` | 叔孫通 | [《史記・劉敬叔孫通列傳》][81] | [JSON](dpt_ry7_e1z.json) |
| `dpx_453_4rt` | 丹朱 | [《史記・五帝本紀》][1] | [JSON](dpx_453_4rt.json) |
| `dpx_ood_o3d` | 楚懷王 | [《史記・高祖本紀》][8] | [JSON](dpx_ood_o3d.json) |
| `dq0_1ox_9ny` | 涇陽君 | [《史記・范睢蔡澤列傳》][61] | [JSON](dq0_1ox_9ny.json) |
| `dq5_xjc_0q4` | 燕惠王 | [《史記・樂毅列傳》][62] | [JSON](dq5_xjc_0q4.json) |
| `dqd_6ym_hvy` | 扁鵲 | [《史記・趙世家》][25] | [JSON](dqd_6ym_hvy.json) |
| `dqp_8qa_bbz` | 趙將泥 | [《史記・秦本紀》][5] | [JSON](dqp_8qa_bbz.json) |
| `dqt_ei7_x33` | 趙使珠履故事未名 | [《史記・春申君列傳》][60] | [JSON](dqt_ei7_x33.json) |
| `dqw_zsr_wlf` | 鄖公（楚昭王出奔接應者） | [《史記・楚世家》][22] | [JSON](dqw_zsr_wlf.json) |
| `dqz_ka3_on8` | 田閒 | [《史記・酈生陸賈列傳》][79] | [JSON](dqz_ka3_on8.json) |
| `drb_gcn_28e` | 騶忌 | [《史記・田敬仲完世家》][28] | [JSON](drb_gcn_28e.json) |
| `drd_2tl_s7k` | 句踐引古 | [《史記・屈原賈生列傳》][66] | [JSON](drd_2tl_s7k.json) |
| `drk_9j9_izn` | 樓昌 | [《史記・趙世家》][25] | [JSON](drk_9j9_izn.json) |
| `drl_351_czw` | 忽（鄭太子） | [《史記・齊太公世家》][14] | [JSON](drl_351_czw.json) |
| `drl_v87_rou` | 玄囂 | [《史記・五帝本紀》][1] | [JSON](drl_v87_rou.json) |
| `drr_d46_t8n` | 樊仲山父 | [《史記・魯周公世家》][15] | [JSON](drr_d46_t8n.json) |
| `drr_o13_0jb` | 小辛 | [《史記・殷本紀》][3] | [JSON](drr_o13_0jb.json) |
| `drx_32r_pdh` | 羲叔 | [《史記・五帝本紀》][1] | [JSON](drx_32r_pdh.json) |
| `dsc_tie_q5s` | 昌意 | [《史記・五帝本紀》][1] | [JSON](dsc_tie_q5s.json) |
| `dsg_875_jr4` | 太史公 | [《史記・李斯列傳》][69] | [JSON](dsg_875_jr4.json) |
| `dsv_qg0_ete` | 英布 | [《史記・黥布列傳》][73] | [JSON](dsv_qg0_ete.json) |
| `dsw_072_bp0` | 趙王未具名 | [《史記・扁鵲倉公列傳》][87] | [JSON](dsw_072_bp0.json) |
| `dts_kvn_lq6` | 景監 | [《史記・商君列傳》][50] | [JSON](dts_kvn_lq6.json) |
| `dtx_aht_hnz` | 勝（皇太后弟） | [《史記・孝景本紀》][11] | [JSON](dtx_aht_hnz.json) |
| `du0_60z_b4p` | 禹 | [《史記・仲尼弟子列傳》][49] | [JSON](du0_60z_b4p.json) |
| `dur_ktk_918` | 平原君 | [《史記・廉頗藺相如列傳》][63] | [JSON](dur_ktk_918.json) |
| `duy_acg_01x` | 素女 | [《史記・孝武本紀》][12] | [JSON](duy_acg_01x.json) |
| `dw0_uvv_mjl` | 魏王宜陽盟 | [《史記・樗里子甘茂列傳》][53] | [JSON](dw0_uvv_mjl.json) |
| `dwe_x5u_t0q` | 衞康叔（季札論樂稱） | [《史記・吳太伯世家》][13] | [JSON](dwe_x5u_t0q.json) |
| `dwf_eik_t2x` | 南陽守齮 | [《史記・曹相國世家》][36] | [JSON](dwf_eik_t2x.json) |
| `dwm_kwy_53u` | 宣太后 | [《史記・秦本紀》][5] | [JSON](dwm_kwy_53u.json) |
| `dwv_5hn_680` | 孟賁 | [《史記・張儀列傳》][52] | [JSON](dwv_5hn_680.json) |
| `dxi_0q9_9vq` | 公孫喜 | [《史記・秦本紀》][5] | [JSON](dxi_0q9_9vq.json) |
| `dxn_drv_maj` | 趙穿 | [《史記・晉世家》][21] | [JSON](dxn_drv_maj.json) |
| `dxo_6ig_5eg` | 蒙毅 | [《史記・蒙恬列傳》][70] | [JSON](dxo_6ig_5eg.json) |
| `dxw_mqx_r82` | 中𤳹 | [《史記・殷本紀》][3] | [JSON](dxw_mqx_r82.json) |
| `dxz_9j5_10h` | 秦王政 | [《史記・田敬仲完世家》][28] | [JSON](dxz_9j5_10h.json) |
| `dy8_rby_5q2` | 伍舉 | [《史記・楚世家》][22] | [JSON](dy8_rby_5q2.json) |
| `dyh_neb_15u` | 田忌 | [《史記・孫子吳起列傳》][47] | [JSON](dyh_neb_15u.json) |
| `dym_ay3_38w` | 虢公（伐曲沃者未名） | [《史記・晉世家》][21] | [JSON](dym_ay3_38w.json) |
| `dzf_ach_247` | 箕子 | [《史記・留侯世家》][37] | [JSON](dzf_ach_247.json) |
| `dzg_1wj_d9x` | 叔齊 | [《史記・周本紀》][4] | [JSON](dzg_1wj_d9x.json) |
| `dzh_7q4_5aj` | 始成（本卷稱呼） | [《史記・項羽本紀》][7] | [JSON](dzh_7q4_5aj.json) |
| `dzo_7i3_hdh` | 兒良 | [《史記・秦始皇本紀》][6] | [JSON](dzo_7i3_hdh.json) |
| `e0c_am8_axw` | 澠池秦禦史未名 | [《史記・廉頗藺相如列傳》][63] | [JSON](e0c_am8_axw.json) |
| `e0h_ki4_flp` | 孫臏 | [《史記・田敬仲完世家》][28] | [JSON](e0h_ki4_flp.json) |
| `e0l_w0i_2e1` | 李牧北邊所事趙王未名 | [《史記・廉頗藺相如列傳》][63] | [JSON](e0l_w0i_2e1.json) |
| `e1d_wc6_1lj` | 太史公（魏世家論贊敘述者） | [《史記・魏世家》][26] | [JSON](e1d_wc6_1lj.json) |
| `e1p_6au_ihu` | 太史公 | [《史記・曹相國世家》][36] | [JSON](e1p_6au_ihu.json) |
| `e1s_57b_7qv` | 尹霸 | [《史記・梁孝王世家》][40] | [JSON](e1s_57b_7qv.json) |
| `e1v_3is_1tq` | 豎刀 | [《史記・齊太公世家》][14] | [JSON](e1v_3is_1tq.json) |
| `e21_uii_5lx` | 趙利 | [《史記・高祖本紀》][8] | [JSON](e21_uii_5lx.json) |
| `e2a_a4e_6s8` | 公子少官 | [《史記・秦本紀》][5] | [JSON](e2a_a4e_6s8.json) |
| `e2j_anv_pmt` | 吳廣所因夫人（趙世家未名者） | [《史記・趙世家》][25] | [JSON](e2j_anv_pmt.json) |
| `e2m_g41_b73` | 屈完 | [《史記・齊太公世家》][14] | [JSON](e2m_g41_b73.json) |
| `e2p_9wz_fh1` | 季君 | [《史記・穰侯列傳》][54] | [JSON](e2p_9wz_fh1.json) |
| `e2t_fmt_70p` | 孤竹中子 | [《史記・伯夷列傳》][43] | [JSON](e2t_fmt_70p.json) |
| `e3o_2bk_lhm` | 燕太子丹 | [《史記・刺客列傳》][68] | [JSON](e3o_2bk_lhm.json) |
| `e45_75h_f5q` | 仇液 | [《史記・趙世家》][25] | [JSON](e45_75h_f5q.json) |
| `e4c_pkg_cq7` | 黥布 | [《史記・張丞相列傳》][78] | [JSON](e4c_pkg_cq7.json) |
| `e4t_vcw_lrt` | 曹氏未詳名 | [《史記・樊酈滕灌列傳》][77] | [JSON](e4t_vcw_lrt.json) |
| `e55_tuo_wbc` | 章子（齊將） | [《史記・秦本紀》][5]、[《史記・燕召公世家》][16] | [JSON](e55_tuo_wbc.json) |
| `e5f_wil_2zp` | 周亞夫 | [《史記・絳侯周勃世家》][39] | [JSON](e5f_wil_2zp.json) |
| `e5s_bwt_y45` | 劉敬 | [《史記・劉敬叔孫通列傳》][81] | [JSON](e5s_bwt_y45.json) |
| `e69_9n6_wvq` | 曹沫 | [《史記・刺客列傳》][68] | [JSON](e69_9n6_wvq.json) |
| `e6h_mzk_hli` | 宋宣公（孔子世家正考父所佐） | [《史記・孔子世家》][29] | [JSON](e6h_mzk_hli.json) |
| `e6q_5h6_4k7` | 馬犯 | [《史記・周本紀》][4] | [JSON](e6q_5h6_4k7.json) |
| `e74_jhr_fqm` | 入（深澤侯） | [《史記・孝武本紀》][12] | [JSON](e74_jhr_fqm.json) |
| `e79_ty0_mkx` | 春申君 | [《史記・春申君列傳》][60] | [JSON](e79_ty0_mkx.json) |
| `e7m_t5x_d4z` | 秦昭王 | [《史記・魯仲連鄒陽列傳》][65] | [JSON](e7m_t5x_d4z.json) |
| `e7u_po2_uqa` | 趙嚪 | [《史記・樂毅列傳》][62] | [JSON](e7u_po2_uqa.json) |
| `e8s_gf1_o9r` | 公子繇 | [《史記・張儀列傳》][52] | [JSON](e8s_gf1_o9r.json) |
| `e8y_ush_o9u` | 劉揭 | [《史記・呂太后本紀》][9]、[《史記・孝文本紀》][10] | [JSON](e8y_ush_o9u.json) |
| `e92_dyr_eqf` | 太史公 | [《史記・田單列傳》][64] | [JSON](e92_dyr_eqf.json) |
| `e95_m0u_b1x` | 蔡澤 | [《史記・樗里子甘茂列傳》][53] | [JSON](e95_m0u_b1x.json) |
| `e97_4fl_7ej` | 曾參同名殺人者 | [《史記・樗里子甘茂列傳》][53] | [JSON](e97_4fl_7ej.json) |
| `e9j_riv_dom` | 漂母未名 | [《史記・淮陰侯列傳》][74] | [JSON](e9j_riv_dom.json) |
| `e9o_aty_rnt` | 桀 | [《史記・張儀列傳》][52] | [JSON](e9o_aty_rnt.json) |
| `e9r_6rz_g0z` | 太史公 | [《史記・魏公子列傳》][59] | [JSON](e9r_6rz_g0z.json) |
| `e9v_wow_vpm` | 太史公 | [《史記・外戚世家》][31] | [JSON](e9v_wow_vpm.json) |
| `e9w_izn_j6r` | 樊他廣 | [《史記・樊酈滕灌列傳》][77] | [JSON](e9w_izn_j6r.json) |
| `ea7_lok_3qv` | 慶節 | [《史記・周本紀》][4] | [JSON](ea7_lok_3qv.json) |
| `ea8_yum_lvj` | 契 | [《史記・殷本紀》][3] | [JSON](ea8_yum_lvj.json) |
| `eal_ozl_urh` | 蒙恬 | [《史記・白起王翦列傳》][55] | [JSON](eal_ozl_urh.json) |
| `eaq_bx2_o37` | 芮伯（德成時） | [《史記・秦本紀》][5] | [JSON](eaq_bx2_o37.json) |
| `eav_dh2_8o8` | 盧綰妻未名 | [《史記・韓信盧綰列傳》][75] | [JSON](eav_dh2_8o8.json) |
| `eb9_g6y_4q6` | 彌子瑕 | [《史記・老子韓非列傳》][45] | [JSON](eb9_g6y_4q6.json) |
| `ebi_jr2_aky` | 魯王未名 | [《史記・田叔列傳》][86] | [JSON](ebi_jr2_aky.json) |
| `ebz_s7c_pds` | 相國參未詳姓 | [《史記・傅靳蒯成列傳》][80] | [JSON](ebz_s7c_pds.json) |
| `ec1_59q_70f` | 少姬（陳哀公偃母） | [《史記・陳杞世家》][18] | [JSON](ec1_59q_70f.json) |
| `ecc_wdp_4h3` | 亹（衛懷公） | [《史記・衛康叔世家》][19] | [JSON](ecc_wdp_4h3.json) |
| `ecl_t01_cwr` | 酈商 | [《史記・田儋列傳》][76] | [JSON](ecl_t01_cwr.json) |
| `ecn_gan_nzt` | 梁惠王引古 | [《史記・穰侯列傳》][54] | [JSON](ecn_gan_nzt.json) |
| `ect_ro2_yyf` | 慶封 | [《史記・齊太公世家》][14] | [JSON](ect_ro2_yyf.json) |
| `edg_w12_1tw` | 楚懷王 | [《史記・范睢蔡澤列傳》][61] | [JSON](edg_w12_1tw.json) |
| `edi_tx6_0zm` | 召引功 | [《史記・白起王翦列傳》][55] | [JSON](edi_tx6_0zm.json) |
| `edm_4zm_yh1` | 叔向 | [《史記・晉世家》][21] | [JSON](edm_4zm_yh1.json) |
| `ee9_kk5_7tj` | 師曠 | [《史記・晉世家》][21] | [JSON](ee9_kk5_7tj.json) |
| `eee_3o6_5s7` | 從史未名（救袁盎） | [《史記・袁盎鼂錯列傳》][83] | [JSON](eee_3o6_5s7.json) |
| `een_gmx_37i` | 孔子 | [《史記・孔子世家》][29] | [JSON](een_gmx_37i.json) |
| `eep_7t4_31w` | 慎夫人 | [《史記・袁盎鼂錯列傳》][83] | [JSON](eep_7t4_31w.json) |
| `eet_iph_y41` | 魏王犀首事件 | [《史記・張儀列傳》][52] | [JSON](eet_iph_y41.json) |
| `eey_qdy_jzn` | 宋遺（辱齊勇士） | [《史記・楚世家》][22] | [JSON](eey_qdy_jzn.json) |
| `efc_pnt_wy1` | 趙惠文王 | [《史記・趙世家》][25] | [JSON](efc_pnt_wy1.json) |
| `efo_3ww_ein` | 賤妾（衛襄公元母） | [《史記・衛康叔世家》][19] | [JSON](efo_3ww_ein.json) |
| `eg3_vej_g33` | 虢文公 | [《史記・周本紀》][4] | [JSON](eg3_vej_g33.json) |
| `ego_1he_n42` | 少帝 | [《史記・外戚世家》][31] | [JSON](ego_1he_n42.json) |
| `egy_txn_xs1` | 申 | [《史記・魏世家》][26] | [JSON](egy_txn_xs1.json) |
| `egz_t7c_4jf` | 甘般（君奭引述） | [《史記・燕召公世家》][16] | [JSON](egz_t7c_4jf.json) |
| `eh7_raa_ap6` | 伯夷 | [《史記・伯夷列傳》][43] | [JSON](eh7_raa_ap6.json) |
| `ehf_uuv_att` | 子西 | [《史記・伍子胥列傳》][48] | [JSON](ehf_uuv_att.json) |
| `ehh_a65_95j` | 黥布 | [《史記・韓信盧綰列傳》][75] | [JSON](ehh_a65_95j.json) |
| `ehi_e39_173` | 荊軻所待客未名 | [《史記・刺客列傳》][68] | [JSON](ehi_e39_173.json) |
| `ehx_l0f_ti8` | 秦孝公引古 | [《史記・李斯列傳》][69] | [JSON](ehx_l0f_ti8.json) |
| `ei3_w5i_7ai` | 韓公子長 | [《史記・秦本紀》][5] | [JSON](ei3_w5i_7ai.json) |
| `ei8_u9a_hcx` | 虞初 | [《史記・孝武本紀》][12] | [JSON](ei8_u9a_hcx.json) |
| `eid_g2a_uis` | 屈固（楚惠王從者） | [《史記・楚世家》][22] | [JSON](eid_g2a_uis.json) |
| `eij_dot_bjg` | 紂 | [《史記・殷本紀》][3] | [JSON](eij_dot_bjg.json) |
| `eim_new_gh3` | 項他 | [《史記・曹相國世家》][36] | [JSON](eim_new_gh3.json) |
| `ej1_app_vbi` | 太史公 | [《史記・陳丞相世家》][38] | [JSON](ej1_app_vbi.json) |
| `ej1_px0_oja` | 沃甲 | [《史記・殷本紀》][3] | [JSON](ej1_px0_oja.json) |
| `ej5_fv0_qii` | 晉平公 | [《史記・鄭世家》][24] | [JSON](ej5_fv0_qii.json) |
| `ejl_xm5_780` | 公叔氏（孔子世家蒲畔未名者） | [《史記・孔子世家》][29] | [JSON](ejl_xm5_780.json) |
| `ejp_e4r_st7` | 石乞 | [《史記・仲尼弟子列傳》][49] | [JSON](ejp_e4r_st7.json) |
| `ejx_n17_vnl` | 齊中大夫未名 | [《史記・扁鵲倉公列傳》][87] | [JSON](ejx_n17_vnl.json) |
| `ek7_93z_gap` | 趙簡子 | [《史記・扁鵲倉公列傳》][87] | [JSON](ek7_93z_gap.json) |
| `ek7_zwf_lkt` | 武王后（魏世家未名者） | [《史記・魏世家》][26] | [JSON](ek7_zwf_lkt.json) |
| `ekn_61g_qaz` | 章邯 | [《史記・樊酈滕灌列傳》][77] | [JSON](ekn_61g_qaz.json) |
| `ekr_gcm_hox` | 魯昭公 | [《史記・仲尼弟子列傳》][49] | [JSON](ekr_gcm_hox.json) |
| `eku_vg7_a7e` | 樂毅 | [《史記・陳涉世家》][30] | [JSON](eku_vg7_a7e.json) |
| `emm_08p_2n8` | 魏文侯（楚篇三晉記事） | [《史記・楚世家》][22] | [JSON](emm_08p_2n8.json) |
| `ens_bv2_oaj` | 齊太醫未名 | [《史記・扁鵲倉公列傳》][87] | [JSON](ens_bv2_oaj.json) |
| `enz_lny_xoh` | 白起 | [《史記・白起王翦列傳》][55] | [JSON](enz_lny_xoh.json) |
| `eof_wj7_9ih` | 商容 | [《史記・留侯世家》][37] | [JSON](eof_wj7_9ih.json) |
| `eok_92w_kgq` | 子我 | [《史記・齊太公世家》][14] | [JSON](eok_92w_kgq.json) |
| `eoq_ojx_q0n` | 田榮 | [《史記・田儋列傳》][76] | [JSON](eoq_ojx_q0n.json) |
| `eot_1qk_6ee` | 越王句踐引古 | [《史記・范睢蔡澤列傳》][61] | [JSON](eot_1qk_6ee.json) |
| `epd_7nt_bg9` | 黥布 | [《史記・蕭相國世家》][35] | [JSON](epd_7nt_bg9.json) |
| `epd_st0_lry` | 公良孺 | [《史記・孔子世家》][29] | [JSON](epd_st0_lry.json) |
| `epj_utq_pyg` | 春申（四君稱呼） | [《史記・秦始皇本紀》][6] | [JSON](epj_utq_pyg.json) |
| `epn_7nx_g1b` | 張恢 | [《史記・袁盎鼂錯列傳》][83] | [JSON](epn_7nx_g1b.json) |
| `epq_pym_fky` | 句踐（引古） | [《史記・淮陰侯列傳》][74] | [JSON](epq_pym_fky.json) |
| `eqc_fta_phm` | 王錯 | [《史記・魏世家》][26] | [JSON](eqc_fta_phm.json) |
| `eqd_9b3_f2r` | 虢射 | [《史記・晉世家》][21] | [JSON](eqd_9b3_f2r.json) |
| `eqd_qrh_r6x` | 義帝未詳名 | [《史記・酈生陸賈列傳》][79] | [JSON](eqd_qrh_r6x.json) |
| `eqh_hzf_78x` | 江充 | [《史記・五宗世家》][41] | [JSON](eqh_hzf_78x.json) |
| `eqp_oer_tei` | 晉孝侯（楚篇曲沃記事） | [《史記・楚世家》][22] | [JSON](eqp_oer_tei.json) |
| `eqw_b2i_pp0` | 莊生 | [《史記・越王勾踐世家》][23] | [JSON](eqw_b2i_pp0.json) |
| `eqw_jou_32v` | 逢侯丑（楚裨將軍） | [《史記・楚世家》][22] | [JSON](eqw_jou_32v.json) |
| `eqx_c6q_58a` | 李兌 | [《史記・范睢蔡澤列傳》][61] | [JSON](eqx_c6q_58a.json) |
| `er5_u4u_i79` | 紀翁主 | [《史記・齊悼惠王世家》][34] | [JSON](er5_u4u_i79.json) |
| `es4_a59_527` | 熊亶（楚先祖） | [《史記・楚世家》][22] | [JSON](es4_a59_527.json) |
| `es5_b3z_9kk` | 太后未名（梁案） | [《史記・田叔列傳》][86] | [JSON](es5_b3z_9kk.json) |
| `es9_3y0_6pn` | 晉景公 | [《史記・韓世家》][27] | [JSON](es9_3y0_6pn.json) |
| `ese_u3z_tem` | 田豹 | [《史記・司馬穰苴列傳》][46] | [JSON](ese_u3z_tem.json) |
| `esh_8wg_qx0` | 魏王豹 | [《史記・曹相國世家》][36] | [JSON](esh_8wg_qx0.json) |
| `esk_795_o9g` | 田豹 | [《史記・齊太公世家》][14] | [JSON](esk_795_o9g.json) |
| `esm_oea_nvb` | 馬服子未名 | [《史記・范睢蔡澤列傳》][61] | [JSON](esm_oea_nvb.json) |
| `esn_e4u_x5x` | 孫良夫（衛救魯記事） | [《史記・衛康叔世家》][19] | [JSON](esn_e4u_x5x.json) |
| `esn_fxf_cpj` | 孔忠 | [《史記・仲尼弟子列傳》][49] | [JSON](esn_fxf_cpj.json) |
| `esz_z17_u3u` | 子之 | [《史記・樂毅列傳》][62] | [JSON](esz_z17_u3u.json) |
| `et8_4b0_91i` | 逢同 | [《史記・越王勾踐世家》][23] | [JSON](et8_4b0_91i.json) |
| `etb_k6i_en4` | 魏公子卬引古 | [《史記・范睢蔡澤列傳》][61] | [JSON](etb_k6i_en4.json) |
| `euc_oun_w4b` | 悼公（燕惠公後） | [《史記・燕召公世家》][16] | [JSON](euc_oun_w4b.json) |
| `euw_a6w_5kn` | 熊摯紅（熊渠後繼） | [《史記・楚世家》][22] | [JSON](euw_a6w_5kn.json) |
| `eux_olw_pzm` | 韓信 | [《史記・淮陰侯列傳》][74] | [JSON](eux_olw_pzm.json) |
| `ev5_tf4_yrs` | 偃（崔氏相者） | [《史記・齊太公世家》][14] | [JSON](ev5_tf4_yrs.json) |
| `ev7_bgb_mtr` | 魏相田文 | [《史記・孫子吳起列傳》][47] | [JSON](ev7_bgb_mtr.json) |
| `evh_7zu_u3x` | 慎夫人 | [《史記・外戚世家》][31] | [JSON](evh_7zu_u3x.json) |
| `evn_9i5_s69` | 萊侯（太公就國時未名） | [《史記・齊太公世家》][14] | [JSON](evn_9i5_s69.json) |
| `ewb_7x8_5z2` | 中行文子 | [《史記・魏世家》][26] | [JSON](ewb_7x8_5z2.json) |
| `ewk_5mw_a5n` | 晉襄父（本文用字） | [《史記・魯周公世家》][15] | [JSON](ewk_5mw_a5n.json) |
| `ex1_pps_iby` | 江陵王未詳名 | [《史記・傅靳蒯成列傳》][80] | [JSON](ex1_pps_iby.json) |
| `exl_e7q_rma` | 車丞相未詳名 | [《史記・張丞相列傳》][78] | [JSON](exl_e7q_rma.json) |
| `ey4_td6_sc4` | 嫘祖 | [《史記・五帝本紀》][1] | [JSON](ey4_td6_sc4.json) |
| `eya_qj3_tev` | 酈食其 | [《史記・酈生陸賈列傳》][79] | [JSON](eya_qj3_tev.json) |
| `eyc_0n9_y2x` | 士蒍（晉臣） | [《史記・晉世家》][21] | [JSON](eyc_0n9_y2x.json) |
| `eyc_8y6_02q` | 郭隗（燕招賢者） | [《史記・燕召公世家》][16] | [JSON](eyc_8y6_02q.json) |
| `eyp_jnx_te1` | 秦莊襄王 | [《史記・呂不韋列傳》][67] | [JSON](eyp_jnx_te1.json) |
| `ez4_g40_5ja` | 宋君（韓世家被執未名者） | [《史記・韓世家》][27] | [JSON](ez4_g40_5ja.json) |
| `ez6_e2l_0ml` | 騎劫（燕將） | [《史記・樂毅列傳》][62] | [JSON](ez6_e2l_0ml.json) |
| `ezo_kwy_dw4` | 饕餮 | [《史記・五帝本紀》][1] | [JSON](ezo_kwy_dw4.json) |
| `ezp_adc_v7h` | 檮杌 | [《史記・五帝本紀》][1] | [JSON](ezp_adc_v7h.json) |
| `ezu_to5_b2p` | 孟增 | [《史記・秦本紀》][5] | [JSON](ezu_to5_b2p.json) |
| `f08_kt7_a71` | 公子虔 | [《史記・商君列傳》][50] | [JSON](f08_kt7_a71.json) |
| `f0b_vw6_d85` | 熊勝（楚先祖） | [《史記・楚世家》][22] | [JSON](f0b_vw6_d85.json) |
| `f0l_i51_7ek` | 張丑（楚威王說客） | [《史記・楚世家》][22] | [JSON](f0l_i51_7ek.json) |
| `f0u_lxn_ztw` | 晁錯 | [《史記・袁盎鼂錯列傳》][83] | [JSON](f0u_lxn_ztw.json) |
| `f0w_zvb_6ui` | 魏犫（楚篇文公股肱） | [《史記・晉世家》][21]、[《史記・楚世家》][22] | [JSON](f0w_zvb_6ui.json) |
| `f1d_zbt_d2u` | 大業 | [《史記・秦本紀》][5] | [JSON](f1d_zbt_d2u.json) |
| `f1f_c8i_jm9` | 惠公（西周） | [《史記・周本紀》][4] | [JSON](f1f_c8i_jm9.json) |
| `f1l_p1w_796` | 叔振鐸 | [《史記・周本紀》][4] | [JSON](f1l_p1w_796.json) |
| `f23_b0p_hqg` | 髙渠彌 | [《史記・鄭世家》][24] | [JSON](f23_b0p_hqg.json) |
| `f2n_1g8_h3m` | 趙倉唐 | [《史記・魏世家》][26] | [JSON](f2n_1g8_h3m.json) |
| `f2w_0vq_9ld` | 秦孝文王 | [《史記・范睢蔡澤列傳》][61] | [JSON](f2w_0vq_9ld.json) |
| `f30_vxh_z7o` | 隨何 | [《史記・留侯世家》][37] | [JSON](f30_vxh_z7o.json) |
| `f32_hqy_au7` | 偃（陳哀公子） | [《史記・陳杞世家》][18] | [JSON](f32_hqy_au7.json) |
| `f3g_9nj_1ae` | 田常引古 | [《史記・魯仲連鄒陽列傳》][65] | [JSON](f3g_9nj_1ae.json) |
| `f3g_x6y_1iy` | 平王 | [《史記・周本紀》][4] | [JSON](f3g_x6y_1iy.json) |
| `f3j_nl2_i2g` | 蚡（皇太后弟） | [《史記・孝景本紀》][11]、[《史記・孝武本紀》][12] | [JSON](f3j_nl2_i2g.json) |
| `f3s_h05_04d` | 惠公適夫人（未名） | [《史記・魯周公世家》][15] | [JSON](f3s_h05_04d.json) |
| `f41_iwq_mkl` | 祖庚 | [《史記・殷本紀》][3] | [JSON](f41_iwq_mkl.json) |
| `f42_zl0_lkq` | 晉厲公 | [《史記・晉世家》][21] | [JSON](f42_zl0_lkq.json) |
| `f45_owg_dw1` | 周（引古） | [《史記・淮陰侯列傳》][74] | [JSON](f45_owg_dw1.json) |
| `f47_ssw_aov` | 文子齊謀伐楚未定 | [《史記・范睢蔡澤列傳》][61] | [JSON](f47_ssw_aov.json) |
| `f4j_73i_aup` | 秦昭王 | [《史記・樗里子甘茂列傳》][53] | [JSON](f4j_73i_aup.json) |
| `f53_xev_s2o` | 紂之母 | [《史記・殷本紀》][3] | [JSON](f53_xev_s2o.json) |
| `f6e_ib9_ktb` | 顏噲 | [《史記・仲尼弟子列傳》][49] | [JSON](f6e_ib9_ktb.json) |
| `f6g_596_kog` | 章武侯 | [《史記・絳侯周勃世家》][39] | [JSON](f6g_596_kog.json) |
| `f79_cpn_758` | 公子悝 | [《史記・秦本紀》][5] | [JSON](f79_cpn_758.json) |
| `f82_dk6_87k` | 晉頃公 | [《史記・伍子胥列傳》][48] | [JSON](f82_dk6_87k.json) |
| `f83_k7g_go4` | 范昭子 | [《史記・趙世家》][25] | [JSON](f83_k7g_go4.json) |
| `f8h_ahy_gjk` | 秦大夫（楚太子所殺未名） | [《史記・楚世家》][22] | [JSON](f8h_ahy_gjk.json) |
| `f8j_w3m_2ep` | 曹參 | [《史記・酈生陸賈列傳》][79] | [JSON](f8j_w3m_2ep.json) |
| `f8p_npb_om0` | 齊女（衛宣公正夫人） | [《史記・衛康叔世家》][19] | [JSON](f8p_npb_om0.json) |
| `f99_rwc_qgo` | 公叔僕 | [《史記・孫子吳起列傳》][47] | [JSON](f99_rwc_qgo.json) |
| `f9c_9te_ebx` | 延陵鈞 | [《史記・趙世家》][25] | [JSON](f9c_9te_ebx.json) |
| `f9d_icg_tck` | 哀王 | [《史記・周本紀》][4] | [JSON](f9d_icg_tck.json) |
| `f9x_bo2_whn` | 孔子 | [《史記・趙世家》][25] | [JSON](f9x_bo2_whn.json) |
| `fa2_16v_bwx` | 紂 | [《史記・蘇秦列傳》][51] | [JSON](fa2_16v_bwx.json) |
| `fae_ax5_a6k` | 樗里子 | [《史記・樗里子甘茂列傳》][53] | [JSON](fae_ax5_a6k.json) |
| `fas_3ef_vnq` | 王陵 | [《史記・白起王翦列傳》][55] | [JSON](fas_3ef_vnq.json) |
| `fbb_ef2_6rv` | 子豹 | [《史記・扁鵲倉公列傳》][87] | [JSON](fbb_ef2_6rv.json) |
| `fbi_2jp_um3` | 師服（晉人命名評論） | [《史記・晉世家》][21] | [JSON](fbi_2jp_um3.json) |
| `fbj_yol_ei3` | 彊（齊頃公太子） | [《史記・晉世家》][21] | [JSON](fbj_yol_ei3.json) |
| `fbp_g9d_1zu` | 晉悼公 | [《史記・魏世家》][26] | [JSON](fbp_g9d_1zu.json) |
| `fbs_rkc_yim` | 王悍 | [《史記・楚元王世家》][32] | [JSON](fbs_rkc_yim.json) |
| `fbw_boe_fyu` | 蔡女（楚太子建母） | [《史記・楚世家》][22] | [JSON](fbw_boe_fyu.json) |
| `fcd_zxy_ct1` | 韓王信 | [《史記・韓信盧綰列傳》][75] | [JSON](fcd_zxy_ct1.json) |
| `fd5_uxa_0c9` | 幽王 | [《史記・周本紀》][4] | [JSON](fd5_uxa_0c9.json) |
| `fd9_3qc_637` | 大費（秦本紀） | [《史記・秦本紀》][5] | [JSON](fd9_3qc_637.json) |
| `fdc_ofl_z5f` | 秦王政 | [《史記・秦始皇本紀》][6] | [JSON](fdc_ofl_z5f.json) |
| `fdi_2l0_u1g` | 薄案 | [《史記・外戚世家》][31] | [JSON](fdi_2l0_u1g.json) |
| `fdp_ctj_2jn` | 韓廣 | [《史記・陳涉世家》][30] | [JSON](fdp_ctj_2jn.json) |
| `fe0_6ra_d9a` | 榮伯 | [《史記・周本紀》][4] | [JSON](fe0_6ra_d9a.json) |
| `fem_3iz_8yb` | 南宮括 | [《史記・仲尼弟子列傳》][49] | [JSON](fem_3iz_8yb.json) |
| `feo_rlp_5n7` | 盜高廟玉環者未名 | [《史記・張釋之馮唐列傳》][84] | [JSON](feo_rlp_5n7.json) |
| `fep_gp5_yz2` | 老子 | [《史記・陳丞相世家》][38] | [JSON](fep_gp5_yz2.json) |
| `ffe_4pb_te4` | 孔寧（陳大夫） | [《史記・陳杞世家》][18] | [JSON](ffe_4pb_te4.json) |
| `fgh_29v_mtm` | 榮旂 | [《史記・仲尼弟子列傳》][49] | [JSON](fgh_29v_mtm.json) |
| `fgm_y8o_tv2` | 蟜極 | [《史記・五帝本紀》][1] | [JSON](fgm_y8o_tv2.json) |
| `fgp_e4n_xnh` | 陳豨 | [《史記・淮陰侯列傳》][74] | [JSON](fgp_e4n_xnh.json) |
| `fgr_573_f18` | 祝午 | [《史記・齊悼惠王世家》][34] | [JSON](fgr_573_f18.json) |
| `fie_vij_hw2` | 王孫滿 | [《史記・楚世家》][22] | [JSON](fie_vij_hw2.json) |
| `fip_5au_13p` | 小白 | [《史記・齊太公世家》][14] | [JSON](fip_5au_13p.json) |
| `fit_pze_t69` | 知伯 | [《史記・魏世家》][26] | [JSON](fit_pze_t69.json) |
| `fiw_di7_wro` | 伯服（襄王使者） | [《史記・周本紀》][4] | [JSON](fiw_di7_wro.json) |
| `fje_cj8_po0` | 夏説 | [《史記・張耳陳餘列傳》][71] | [JSON](fje_cj8_po0.json) |
| `fji_le1_7p1` | 韓君俠累季父未名 | [《史記・刺客列傳》][68] | [JSON](fji_le1_7p1.json) |
| `fjo_zh4_b7q` | 陸賈 | [《史記・酈生陸賈列傳》][79] | [JSON](fjo_zh4_b7q.json) |
| `fks_8ov_okp` | 智伯 | [《史記・晉世家》][21] | [JSON](fks_8ov_okp.json) |
| `fkx_pbx_7kt` | 費昌 | [《史記・秦本紀》][5] | [JSON](fkx_pbx_7kt.json) |
| `fl4_t18_ifh` | 孤竹君 | [《史記・蘇秦列傳》][51] | [JSON](fl4_t18_ifh.json) |
| `flg_pi3_zdp` | 侍醫遂 | [《史記・扁鵲倉公列傳》][87] | [JSON](flg_pi3_zdp.json) |
| `flr_6dp_xgn` | 華陽引古 | [《史記・李斯列傳》][69] | [JSON](flr_6dp_xgn.json) |
| `fm3_f8m_0vr` | 欒逞（欒書孫） | [《史記・晉世家》][21] | [JSON](fm3_f8m_0vr.json) |
| `fmb_kx3_vmm` | 鉏麑（刺盾者） | [《史記・晉世家》][21] | [JSON](fmb_kx3_vmm.json) |
| `fmd_j09_ef0` | 比干（引古） | [《史記・蒙恬列傳》][70] | [JSON](fmd_j09_ef0.json) |
| `fmk_3kl_4cb` | 宛若 | [《史記・孝武本紀》][12] | [JSON](fmk_3kl_4cb.json) |
| `fmo_6wd_9wn` | 壽（荼異母兄） | [《史記・齊太公世家》][14] | [JSON](fmo_6wd_9wn.json) |
| `fn4_068_lvo` | 項王 | [《史記・李斯列傳》][69] | [JSON](fn4_068_lvo.json) |
| `fn4_s0b_4jd` | 趙王書信未名 | [《史記・吳王濞列傳》][88] | [JSON](fn4_s0b_4jd.json) |
| `fnb_86c_jy4` | 成安君 | [《史記・曹相國世家》][36] | [JSON](fnb_86c_jy4.json) |
| `fnf_65y_ed5` | 烏獲 | [《史記・范睢蔡澤列傳》][61] | [JSON](fnf_65y_ed5.json) |
| `fng_mjp_tdn` | 糾（齊公子） | [《史記・齊太公世家》][14] | [JSON](fng_mjp_tdn.json) |
| `fo2_the_x22` | 栗腹（燕相） | [《史記・燕召公世家》][16]、[《史記・樂毅列傳》][62] | [JSON](fo2_the_x22.json) |
| `fo6_plq_cng` | 賈偃 | [《史記・白起王翦列傳》][55] | [JSON](fo6_plq_cng.json) |
| `fo7_9ev_cht` | 羊勝 | [《史記・梁孝王世家》][40] | [JSON](fo7_9ev_cht.json) |
| `fo8_gdc_pg8` | 欒盈 | [《史記・齊太公世家》][14] | [JSON](fo8_gdc_pg8.json) |
| `foh_3hu_yh7` | 廷尉未名 | [《史記・張耳陳餘列傳》][71] | [JSON](foh_3hu_yh7.json) |
| `foo_tch_2bb` | 燕王喜 | [《史記・田敬仲完世家》][28] | [JSON](foo_tch_2bb.json) |
| `foy_wud_r8i` | 齊王中子未定 | [《史記・扁鵲倉公列傳》][87] | [JSON](foy_wud_r8i.json) |
| `fp6_ia6_7yw` | 孔子 | [《史記・孔子世家》][29] | [JSON](fp6_ia6_7yw.json) |
| `fpb_qvf_bl8` | 阿大夫（田世家未名者） | [《史記・田敬仲完世家》][28] | [JSON](fpb_qvf_bl8.json) |
| `fpp_ue3_su5` | 周主鴆（未名） | [《史記・衛康叔世家》][19] | [JSON](fpp_ue3_su5.json) |
| `fpv_2sb_uay` | 陸賈 | [《史記・酈生陸賈列傳》][79] | [JSON](fpv_2sb_uay.json) |
| `fq3_1ko_7tz` | 周惠王 | [《史記・鄭世家》][24] | [JSON](fq3_1ko_7tz.json) |
| `fqj_az4_0ep` | 臣扈（君奭引述） | [《史記・燕召公世家》][16] | [JSON](fqj_az4_0ep.json) |
| `fqm_332_ccr` | 勸公子忘功客未名 | [《史記・魏公子列傳》][59] | [JSON](fqm_332_ccr.json) |
| `fqt_y7z_vdn` | 魯哀公 | [《史記・仲尼弟子列傳》][49] | [JSON](fqt_y7z_vdn.json) |
| `fqw_nka_rjt` | 甘茂 | [《史記・韓世家》][27] | [JSON](fqw_nka_rjt.json) |
| `fqy_h9x_4nx` | 申包胥引古 | [《史記・范睢蔡澤列傳》][61] | [JSON](fqy_h9x_4nx.json) |
| `fr3_x62_cai` | 河亶甲 | [《史記・殷本紀》][3] | [JSON](fr3_x62_cai.json) |
| `frl_sio_pwm` | 太公（引古） | [《史記・淮陰侯列傳》][74] | [JSON](frl_sio_pwm.json) |
| `frp_bsu_g43` | 王黃 | [《史記・樊酈滕灌列傳》][77] | [JSON](frp_bsu_g43.json) |
| `frs_icw_4ma` | 荊軻 | [《史記・刺客列傳》][68] | [JSON](frs_icw_4ma.json) |
| `fs1_3m9_rj3` | 章平 | [《史記・高祖本紀》][8] | [JSON](fs1_3m9_rj3.json) |
| `fs3_38r_obw` | 須賈 | [《史記・范睢蔡澤列傳》][61] | [JSON](fs3_38r_obw.json) |
| `fs9_9td_byt` | 騶忌 | [《史記・田敬仲完世家》][28] | [JSON](fs9_9td_byt.json) |
| `fsx_vbt_ii4` | 周公引古 | [《史記・范睢蔡澤列傳》][61] | [JSON](fsx_vbt_ii4.json) |
| `fto_fi5_11x` | 大駱 | [《史記・秦本紀》][5] | [JSON](fto_fi5_11x.json) |
| `fu8_kck_4vb` | 屈丐 | [《史記・張儀列傳》][52] | [JSON](fu8_kck_4vb.json) |
| `fuj_mp6_k5d` | 商君公孫鞅引古 | [《史記・范睢蔡澤列傳》][61] | [JSON](fuj_mp6_k5d.json) |
| `fv2_9nj_8b4` | 韓王被虜未名 | [《史記・刺客列傳》][68] | [JSON](fv2_9nj_8b4.json) |
| `fva_alg_40j` | 句踐 | [《史記・孔子世家》][29] | [JSON](fva_alg_40j.json) |
| `fvc_9z0_643` | 淖齒 | [《史記・田敬仲完世家》][28] | [JSON](fvc_9z0_643.json) |
| `fvc_qlq_6o2` | 韓王 | [《史記・老子韓非列傳》][45] | [JSON](fvc_qlq_6o2.json) |
| `fvd_oal_6gi` | 越王句踐 | [《史記・蘇秦列傳》][51] | [JSON](fvd_oal_6gi.json) |
| `fvj_ir6_7zh` | 公孫龍 | [《史記・平原君虞卿列傳》][58] | [JSON](fvj_ir6_7zh.json) |
| `fw5_xvm_aza` | 接輿引古 | [《史記・范睢蔡澤列傳》][61] | [JSON](fw5_xvm_aza.json) |
| `fw7_8k1_43d` | 周最 | [《史記・孟嘗君列傳》][57] | [JSON](fw7_8k1_43d.json) |
| `fw9_g5w_om8` | 堯 | [《史記・趙世家》][25] | [JSON](fw9_g5w_om8.json) |
| `fwf_1wp_wzg` | 呂太后 | [《史記・齊悼惠王世家》][34] | [JSON](fwf_1wp_wzg.json) |
| `fwu_nkh_9qr` | 張羽 | [《史記・吳王濞列傳》][88] | [JSON](fwu_nkh_9qr.json) |
| `fx4_w1m_tu6` | 平原君趙勝 | [《史記・平原君虞卿列傳》][58] | [JSON](fx4_w1m_tu6.json) |
| `fx4_ybu_7b9` | 長盧 | [《史記・孟子荀卿列傳》][56] | [JSON](fx4_ybu_7b9.json) |
| `fxa_91g_1cz` | 召滑 | [《史記・樗里子甘茂列傳》][53] | [JSON](fxa_91g_1cz.json) |
| `fxc_ppb_ofs` | 丞相敞未詳姓 | [《史記・傅靳蒯成列傳》][80] | [JSON](fxc_ppb_ofs.json) |
| `fxh_d0f_a1l` | 趙夙 | [《史記・魏世家》][26] | [JSON](fxh_d0f_a1l.json) |
| `fxy_b0h_ssn` | 公子光（楚篇吳伐楚者） | [《史記・楚世家》][22] | [JSON](fxy_b0h_ssn.json) |
| `fy2_9h4_gdt` | 太史公 | [《史記・孫子吳起列傳》][47] | [JSON](fy2_9h4_gdt.json) |
| `fy7_290_36y` | 呂后 | [《史記・呂太后本紀》][9] | [JSON](fy7_290_36y.json) |
| `fyf_enn_4w8` | 陳軫 | [《史記・秦始皇本紀》][6] | [JSON](fyf_enn_4w8.json) |
| `fyt_uh2_b2k` | 舜引古 | [《史記・范睢蔡澤列傳》][61] | [JSON](fyt_uh2_b2k.json) |
| `fyu_tcg_kev` | 翟后 | [《史記・周本紀》][4] | [JSON](fyu_tcg_kev.json) |
| `fzk_mr8_bej` | 秦獻公（楚篇周賀者） | [《史記・楚世家》][22] | [JSON](fzk_mr8_bej.json) |
| `g0f_lnq_gkm` | 褒后 | [《史記・鄭世家》][24] | [JSON](g0f_lnq_gkm.json) |
| `g0o_7tz_csx` | 戎胥軒 | [《史記・秦本紀》][5] | [JSON](g0o_7tz_csx.json) |
| `g0p_ahe_0bb` | 閼氏未詳名 | [《史記・樊酈滕灌列傳》][77] | [JSON](g0p_ahe_0bb.json) |
| `g0r_9hy_37h` | 趙利 | [《史記・高祖本紀》][8] | [JSON](g0r_9hy_37h.json) |
| `g0t_7m5_3bk` | 鄧都尉 | [《史記・吳王濞列傳》][88] | [JSON](g0t_7m5_3bk.json) |
| `g14_wpb_odv` | 荀息 | [《史記・晉世家》][21] | [JSON](g14_wpb_odv.json) |
| `g1r_0em_2tf` | 莊周 | [《史記・老子韓非列傳》][45] | [JSON](g1r_0em_2tf.json) |
| `g22_f2k_eav` | 趙豹 | [《史記・趙世家》][25] | [JSON](g22_f2k_eav.json) |
| `g2b_tzq_wxz` | 韓非 | [《史記・秦始皇本紀》][6] | [JSON](g2b_tzq_wxz.json) |
| `g2e_ui5_mts` | 伍徐 | [《史記・陳涉世家》][30] | [JSON](g2e_ui5_mts.json) |
| `g2j_v25_c9b` | 蟣蝨 | [《史記・韓世家》][27] | [JSON](g2j_v25_c9b.json) |
| `g2k_ddk_pxs` | 晉悼公 | [《史記・鄭世家》][24] | [JSON](g2k_ddk_pxs.json) |
| `g2o_10m_zsp` | 淳于髡 | [《史記・孟子荀卿列傳》][56] | [JSON](g2o_10m_zsp.json) |
| `g2v_d8d_els` | 李兌 | [《史記・趙世家》][25] | [JSON](g2v_d8d_els.json) |
| `g4n_b86_xmr` | 昭魚 | [《史記・魏世家》][26] | [JSON](g4n_b86_xmr.json) |
| `g50_yu6_9yk` | 沛公 | [《史記・李斯列傳》][69] | [JSON](g50_yu6_9yk.json) |
| `g5b_oty_6le` | 呂更始 | [《史記・呂太后本紀》][9] | [JSON](g5b_oty_6le.json) |
| `g61_dv0_745` | 狐氏女（重耳母） | [《史記・晉世家》][21] | [JSON](g61_dv0_745.json) |
| `g65_rlp_udt` | 楚莊王 | [《史記・伍子胥列傳》][48] | [JSON](g65_rlp_udt.json) |
| `g68_3hl_fiw` | 王衛尉 | [《史記・蕭相國世家》][35] | [JSON](g68_3hl_fiw.json) |
| `g6c_exa_3pg` | 李園女弟子楚幽王 | [《史記・春申君列傳》][60] | [JSON](g6c_exa_3pg.json) |
| `g6e_oyg_ok4` | 司馬子綦 | [《史記・伍子胥列傳》][48] | [JSON](g6e_oyg_ok4.json) |
| `g6i_kby_l4h` | 環淵 | [《史記・孟子荀卿列傳》][56] | [JSON](g6i_kby_l4h.json) |
| `g6k_27w_gan` | 周文 | [《史記・陳涉世家》][30] | [JSON](g6k_27w_gan.json) |
| `g6l_rp7_156` | 桀 | [《史記・張丞相列傳》][78] | [JSON](g6l_rp7_156.json) |
| `g6n_ybc_0r2` | 義伯 | [《史記・殷本紀》][3] | [JSON](g6n_ybc_0r2.json) |
| `g70_oq8_1fb` | 項羽 | [《史記・項羽本紀》][7] | [JSON](g70_oq8_1fb.json) |
| `g7a_dv4_au1` | 樊噲 | [《史記・樊酈滕灌列傳》][77] | [JSON](g7a_dv4_au1.json) |
| `g7e_e8s_vnu` | 董安于 | [《史記・扁鵲倉公列傳》][87] | [JSON](g7e_e8s_vnu.json) |
| `g7g_fpv_oq5` | 實遣家人子未名 | [《史記・劉敬叔孫通列傳》][81] | [JSON](g7g_fpv_oq5.json) |
| `g8d_9kf_uqg` | 莊忌夫子 | [《史記・魯仲連鄒陽列傳》][65] | [JSON](g8d_9kf_uqg.json) |
| `g8i_wsz_vkj` | 辛廖（占畢萬者） | [《史記・晉世家》][21] | [JSON](g8i_wsz_vkj.json) |
| `g9g_mv1_6zj` | 蓋公 | [《史記・曹相國世家》][36] | [JSON](g9g_mv1_6zj.json) |
| `g9x_uoh_p49` | 孟戲 | [《史記・秦本紀》][5] | [JSON](g9x_uoh_p49.json) |
| `g9x_wll_ruk` | 成王引古 | [《史記・范睢蔡澤列傳》][61] | [JSON](g9x_wll_ruk.json) |
| `ga0_0p4_5xy` | 雍（晉襄公弟） | [《史記・晉世家》][21] | [JSON](ga0_0p4_5xy.json) |
| `gaj_q2w_f4h` | 顏之僕 | [《史記・仲尼弟子列傳》][49] | [JSON](gaj_q2w_f4h.json) |
| `gar_g8m_0lo` | 伍奢（引古） | [《史記・蒙恬列傳》][70] | [JSON](gar_g8m_0lo.json) |
| `gas_wud_t4m` | 鄭忠 | [《史記・項羽本紀》][7]、[《史記・高祖本紀》][8] | [JSON](gas_wud_t4m.json) |
| `gb5_f9t_hd2` | 趙孝成王 | [《史記・魯仲連鄒陽列傳》][65] | [JSON](gb5_f9t_hd2.json) |
| `gbf_h5a_e3f` | 呂后 | [《史記・蕭相國世家》][35] | [JSON](gbf_h5a_e3f.json) |
| `gbi_qsy_i7l` | 魏冉 | [《史記・穰侯列傳》][54] | [JSON](gbi_qsy_i7l.json) |
| `gcd_ek1_6jn` | 田橫 | [《史記・田儋列傳》][76] | [JSON](gcd_ek1_6jn.json) |
| `gd9_jxj_uqe` | 鉤弋夫人 | [《史記・外戚世家》][31] | [JSON](gd9_jxj_uqe.json) |
| `gde_5zz_7rg` | 熊楊（楚先祖） | [《史記・楚世家》][22] | [JSON](gde_5zz_7rg.json) |
| `gdj_k53_v1x` | 王翦 | [《史記・白起王翦列傳》][55] | [JSON](gdj_k53_v1x.json) |
| `gdl_uc7_0y0` | 延陵季子（引古） | [《史記・張耳陳餘列傳》][71] | [JSON](gdl_uc7_0y0.json) |
| `gdy_039_7n5` | 子穨 | [《史記・周本紀》][4] | [JSON](gdy_039_7n5.json) |
| `gec_tof_7li` | 益 | [《史記・夏本紀》][2] | [JSON](gec_tof_7li.json) |
| `gem_sji_xo8` | 栗姬 | [《史記・五宗世家》][41] | [JSON](gem_sji_xo8.json) |
| `gew_3f0_q9o` | 趙歇 | [《史記・張耳陳餘列傳》][71] | [JSON](gew_3f0_q9o.json) |
| `gf2_bab_2ln` | 田乞 | [《史記・齊太公世家》][14] | [JSON](gf2_bab_2ln.json) |
| `gfh_xl8_j6e` | 呂后 | [《史記・呂太后本紀》][9] | [JSON](gfh_xl8_j6e.json) |
| `gfr_55l_72s` | 周昌 | [《史記・張丞相列傳》][78] | [JSON](gfr_55l_72s.json) |
| `gfr_toc_lua` | 衞君（田世家接湣王未名者） | [《史記・田敬仲完世家》][28] | [JSON](gfr_toc_lua.json) |
| `gft_rfa_1uq` | 申繻 | [《史記・魯周公世家》][15] | [JSON](gft_rfa_1uq.json) |
| `gfy_kw8_8tm` | 城陽共王（本卷未名） | [《史記・孝景本紀》][11] | [JSON](gfy_kw8_8tm.json) |
| `gg7_gm5_159` | 管夷吾引古 | [《史記・魯仲連鄒陽列傳》][65] | [JSON](gg7_gm5_159.json) |
| `gg7_zrf_25b` | 梁父侯未詳名 | [《史記・酈生陸賈列傳》][79] | [JSON](gg7_zrf_25b.json) |
| `ggi_5lp_87e` | 伯夷 | [《史記・劉敬叔孫通列傳》][81] | [JSON](ggi_5lp_87e.json) |
| `ggn_i2q_6d5` | 魏錯 | [《史記・秦本紀》][5] | [JSON](ggn_i2q_6d5.json) |
| `ggw_ogf_emc` | 桀 | [《史記・留侯世家》][37] | [JSON](ggw_ogf_emc.json) |
| `ghj_5dg_gu1` | 會人（陸終子） | [《史記・楚世家》][22] | [JSON](ghj_5dg_gu1.json) |
| `ghk_av2_9f8` | 公之魚 | [《史記・孔子世家》][29] | [JSON](ghk_av2_9f8.json) |
| `ghq_hdt_7iz` | 子結（楚昭王弟） | [《史記・楚世家》][22] | [JSON](ghq_hdt_7iz.json) |
| `gi7_lw7_z9m` | 韓馮 | [《史記・田敬仲完世家》][28] | [JSON](gi7_lw7_z9m.json) |
| `gir_5c2_ilu` | 楊中倩待核異稱 | [《史記・扁鵲倉公列傳》][87] | [JSON](gir_5c2_ilu.json) |
| `gj7_qds_jsk` | 卿秦 | [《史記・趙世家》][25] | [JSON](gj7_qds_jsk.json) |
| `gk2_t8l_zhj` | 緣斯（長翟） | [《史記・魯周公世家》][15]、[《史記・宋微子世家》][20] | [JSON](gk2_t8l_zhj.json) |
| `gkk_c0y_s45` | 楚王（越世家朱公救子未名者） | [《史記・越王勾踐世家》][23] | [JSON](gkk_c0y_s45.json) |
| `gkp_6th_pl9` | 禹 | [《史記・趙世家》][25] | [JSON](gkp_6th_pl9.json) |
| `gku_l2n_o0a` | 使者僕 | [《史記・司馬穰苴列傳》][46] | [JSON](gku_l2n_o0a.json) |
| `gli_u6t_bjm` | 屬庸 | [《史記・刺客列傳》][68] | [JSON](gli_u6t_bjm.json) |
| `glj_fdq_9ca` | 趙高 | [《史記・李斯列傳》][69] | [JSON](glj_fdq_9ca.json) |
| `glp_7jv_6nn` | 殤叔（晉穆侯弟） | [《史記・晉世家》][21] | [JSON](glp_7jv_6nn.json) |
| `glu_u6e_lf4` | 楚靈王 | [《史記・管蔡世家》][17]、[《史記・陳杞世家》][18] | [JSON](glu_u6e_lf4.json) |
| `gm9_yt2_fcc` | 蕭桐叔子 | [《史記・齊太公世家》][14] | [JSON](gm9_yt2_fcc.json) |
| `gmc_nsr_p62` | 甯惠子（衛臣） | [《史記・衛康叔世家》][19] | [JSON](gmc_nsr_p62.json) |
| `gmx_6ao_hg2` | 榮夫未名 | [《史記・刺客列傳》][68] | [JSON](gmx_6ao_hg2.json) |
| `gnf_v23_0ks` | 枚生未定 | [《史記・魯仲連鄒陽列傳》][65] | [JSON](gnf_v23_0ks.json) |
| `gnq_vre_5v8` | 舜（引古） | [《史記・淮陰侯列傳》][74] | [JSON](gnq_vre_5v8.json) |
| `gns_w0b_kfj` | 所忠 | [《史記・孝武本紀》][12] | [JSON](gns_w0b_kfj.json) |
| `gnt_6z9_vud` | 武王引古 | [《史記・孟子荀卿列傳》][56] | [JSON](gnt_6z9_vud.json) |
| `go2_1n3_2gu` | 荀欣 | [《史記・趙世家》][25] | [JSON](go2_1n3_2gu.json) |
| `go2_q1p_21g` | 高陵君 | [《史記・蘇秦列傳》][51] | [JSON](go2_q1p_21g.json) |
| `gob_5tz_8nl` | 老子引古 | [《史記・樂毅列傳》][62] | [JSON](gob_5tz_8nl.json) |
| `gog_539_j1v` | 接子 | [《史記・孟子荀卿列傳》][56] | [JSON](gog_539_j1v.json) |
| `goj_kf0_ild` | 文信侯（趙世家未名者） | [《史記・趙世家》][25] | [JSON](goj_kf0_ild.json) |
| `gom_t9h_dzr` | 勳 | [《史記・絳侯周勃世家》][39] | [JSON](gom_t9h_dzr.json) |
| `gp0_e9b_qin` | 皇后 | [《史記・絳侯周勃世家》][39] | [JSON](gp0_e9b_qin.json) |
| `gp2_zpp_ejb` | 欒布 | [《史記・齊悼惠王世家》][34] | [JSON](gp2_zpp_ejb.json) |
| `gp4_92s_txh` | 公子華 | [《史記・張儀列傳》][52] | [JSON](gp4_92s_txh.json) |
| `gpc_3lv_azn` | 蒙恬 | [《史記・陳涉世家》][30] | [JSON](gpc_3lv_azn.json) |
| `gpd_9u1_j6l` | 秦始皇帝 | [《史記・秦始皇本紀》][6] | [JSON](gpd_9u1_j6l.json) |
| `gpi_dmt_1vv` | 陳嬰 | [《史記・黥布列傳》][73] | [JSON](gpi_dmt_1vv.json) |
| `gqa_y4i_81t` | 夏啟 | [《史記・夏本紀》][2] | [JSON](gqa_y4i_81t.json) |
| `gqj_hc0_q5p` | 太史公 | [《史記・淮陰侯列傳》][74] | [JSON](gqj_hc0_q5p.json) |
| `gqz_ag8_bj5` | 句踐 | [《史記・趙世家》][25] | [JSON](gqz_ag8_bj5.json) |
| `gr5_u66_wkh` | 嬰 | [《史記・鄭世家》][24] | [JSON](gr5_u66_wkh.json) |
| `grd_2u0_1ep` | 陽甲 | [《史記・殷本紀》][3] | [JSON](grd_2u0_1ep.json) |
| `grj_xg2_ghx` | 奮揚（楚司馬） | [《史記・楚世家》][22] | [JSON](grj_xg2_ghx.json) |
| `grn_vtp_db9` | 商鞅引古 | [《史記・魯仲連鄒陽列傳》][65] | [JSON](grn_vtp_db9.json) |
| `grr_fo8_y9b` | 太師疵 | [《史記・周本紀》][4] | [JSON](grr_fo8_y9b.json) |
| `gsq_vgq_esv` | 顏淵 | [《史記・仲尼弟子列傳》][49] | [JSON](gsq_vgq_esv.json) |
| `gsy_2ez_vyj` | 鮑焦引古 | [《史記・魯仲連鄒陽列傳》][65] | [JSON](gsy_2ez_vyj.json) |
| `gsy_66d_6si` | 暴子 | [《史記・穰侯列傳》][54] | [JSON](gsy_66d_6si.json) |
| `gt1_z7d_s3u` | 襄王 | [《史記・周本紀》][4] | [JSON](gt1_z7d_s3u.json) |
| `gt3_uk9_ziy` | 孔子 | [《史記・鄭世家》][24] | [JSON](gt3_uk9_ziy.json) |
| `gt6_lcc_g2n` | 齊王太后未名 | [《史記・扁鵲倉公列傳》][87] | [JSON](gt6_lcc_g2n.json) |
| `gt7_y57_atj` | 廉頗 | [《史記・廉頗藺相如列傳》][63] | [JSON](gt7_y57_atj.json) |
| `gtf_oo3_boo` | 管至父 | [《史記・秦本紀》][5]、[《史記・齊太公世家》][14] | [JSON](gtf_oo3_boo.json) |
| `gts_qwq_ofq` | 夫差（楚篇吳王） | [《史記・楚世家》][22] | [JSON](gts_qwq_ofq.json) |
| `gu2_fde_5bw` | 種（越大夫） | [《史記・越王勾踐世家》][23] | [JSON](gu2_fde_5bw.json) |
| `gu5_ugq_r65` | 黃帝引古傳說 | [《史記・李斯列傳》][69] | [JSON](gu5_ugq_r65.json) |
| `gub_mns_uyh` | 燕將未名 | [《史記・張耳陳餘列傳》][71] | [JSON](gub_mns_uyh.json) |
| `guh_2ns_rmq` | 髙漸離 | [《史記・刺客列傳》][68] | [JSON](guh_2ns_rmq.json) |
| `gum_nos_5cz` | 晉鄙 | [《史記・魏公子列傳》][59] | [JSON](gum_nos_5cz.json) |
| `gv0_6h6_ek6` | 龐涓 | [《史記・孫子吳起列傳》][47] | [JSON](gv0_6h6_ek6.json) |
| `gv5_znn_7hk` | 屠岸賈 | [《史記・趙世家》][25] | [JSON](gv5_znn_7hk.json) |
| `gv8_tj5_hcy` | 公孫歸父（宣公時） | [《史記・魯周公世家》][15] | [JSON](gv8_tj5_hcy.json) |
| `gvf_h1q_fdl` | 魏壽餘（詳反晉者） | [《史記・晉世家》][21] | [JSON](gvf_h1q_fdl.json) |
| `gvp_kl8_u6o` | 莊周 | [《史記・孟子荀卿列傳》][56] | [JSON](gvp_kl8_u6o.json) |
| `gw0_pdi_7ji` | 孔子 | [《史記・留侯世家》][37] | [JSON](gw0_pdi_7ji.json) |
| `gwd_nwe_4s7` | 少連 | [《史記・孔子世家》][29] | [JSON](gwd_nwe_4s7.json) |
| `gwl_0sh_hcp` | 楚昭王引古 | [《史記・范睢蔡澤列傳》][61] | [JSON](gwl_0sh_hcp.json) |
| `gwo_lf6_tr7` | 蠡（引古） | [《史記・韓信盧綰列傳》][75] | [JSON](gwo_lf6_tr7.json) |
| `gx0_1xv_0gm` | 呂產 | [《史記・齊悼惠王世家》][34] | [JSON](gx0_1xv_0gm.json) |
| `gxs_1ia_tsp` | 太仆未名 | [《史記・魏豹彭越列傳》][72] | [JSON](gxs_1ia_tsp.json) |
| `gy0_w6c_v4l` | 商君 | [《史記・商君列傳》][50] | [JSON](gy0_w6c_v4l.json) |
| `gy6_lx6_eb2` | 趙公子渴 | [《史記・秦本紀》][5] | [JSON](gy6_lx6_eb2.json) |
| `gy7_87j_x9e` | 郅都 | [《史記・萬石張叔列傳》][85] | [JSON](gy7_87j_x9e.json) |
| `gyr_88s_bq0` | 韓信 | [《史記・淮陰侯列傳》][74] | [JSON](gyr_88s_bq0.json) |
| `gyz_mj7_l1f` | 鯫生 | [《史記・留侯世家》][37] | [JSON](gyz_mj7_l1f.json) |
| `gz0_xuu_ont` | 樂毅 | [《史記・樂毅列傳》][62] | [JSON](gz0_xuu_ont.json) |
| `gz1_n2k_xs6` | 太史公（韓世家論贊敘述者） | [《史記・韓世家》][27] | [JSON](gz1_n2k_xs6.json) |
| `gz3_7on_7yc` | 丕豹引古 | [《史記・李斯列傳》][69] | [JSON](gz3_7on_7yc.json) |
| `gze_eo7_lon` | 孟公綽 | [《史記・仲尼弟子列傳》][49] | [JSON](gze_eo7_lon.json) |
| `gzw_egi_c4r` | 齊王求女弟未名 | [《史記・春申君列傳》][60] | [JSON](gzw_egi_c4r.json) |
| `h08_rhq_ogn` | 韓王信 | [《史記・韓信盧綰列傳》][75] | [JSON](h08_rhq_ogn.json) |
| `h0m_56l_zq0` | 魯隱公（楚篇弒君記事） | [《史記・楚世家》][22] | [JSON](h0m_56l_zq0.json) |
| `h15_bnp_8ii` | 張勝 | [《史記・韓信盧綰列傳》][75] | [JSON](h15_bnp_8ii.json) |
| `h1i_f19_pf4` | 齊丞相舍人奴未名 | [《史記・扁鵲倉公列傳》][87] | [JSON](h1i_f19_pf4.json) |
| `h1l_7wr_80t` | 褚先生 | [《史記・田叔列傳》][86] | [JSON](h1l_7wr_80t.json) |
| `h1s_x8q_27p` | 內史廖 | [《史記・秦本紀》][5] | [JSON](h1s_x8q_27p.json) |
| `h1v_8ap_b9y` | 管仲 | [《史記・齊太公世家》][14] | [JSON](h1v_8ap_b9y.json) |
| `h1w_580_5oa` | 張黡 | [《史記・張耳陳餘列傳》][71] | [JSON](h1w_580_5oa.json) |
| `h29_d0o_1td` | 呂祿 | [《史記・齊悼惠王世家》][34] | [JSON](h29_d0o_1td.json) |
| `h2h_z86_a3d` | 吳廣 | [《史記・陳涉世家》][30] | [JSON](h2h_z86_a3d.json) |
| `h2m_fay_h7r` | 季子札 | [《史記・刺客列傳》][68] | [JSON](h2m_fay_h7r.json) |
| `h2o_6n8_bid` | 趙襄子姊 | [《史記・張儀列傳》][52] | [JSON](h2o_6n8_bid.json) |
| `h3l_xit_ohp` | 佐弋竭 | [《史記・秦始皇本紀》][6] | [JSON](h3l_xit_ohp.json) |
| `h3x_nrw_uay` | 徐偃王 | [《史記・秦本紀》][5] | [JSON](h3x_nrw_uay.json) |
| `h40_rtd_6ut` | 樂池 | [《史記・秦本紀》][5] | [JSON](h40_rtd_6ut.json) |
| `h4c_ia5_qoe` | 五大夫禮 | [《史記・秦本紀》][5] | [JSON](h4c_ia5_qoe.json) |
| `h4s_bj9_3tm` | 旁皋 | [《史記・秦本紀》][5] | [JSON](h4s_bj9_3tm.json) |
| `h55_n0n_dfm` | 張澤 | [《史記・呂太后本紀》][9] | [JSON](h55_n0n_dfm.json) |
| `h55_rzc_q0s` | 欒甯（孔氏老） | [《史記・衛康叔世家》][19] | [JSON](h55_rzc_q0s.json) |
| `h5t_yvi_cqr` | 李斯舍人未名 | [《史記・蒙恬列傳》][70] | [JSON](h5t_yvi_cqr.json) |
| `h68_fxp_gwo` | 許由 | [《史記・袁盎鼂錯列傳》][83] | [JSON](h68_fxp_gwo.json) |
| `h68_ts0_5vs` | 齊女（衛莊公夫人） | [《史記・衛康叔世家》][19] | [JSON](h68_ts0_5vs.json) |
| `h6b_bxc_9d4` | 侯敞 | [《史記・高祖本紀》][8] | [JSON](h6b_bxc_9d4.json) |
| `h6m_d9k_vzq` | 蘇代 | [《史記・樗里子甘茂列傳》][53] | [JSON](h6m_d9k_vzq.json) |
| `h6x_6lh_xwj` | 景陽（救趙楚將軍） | [《史記・楚世家》][22] | [JSON](h6x_6lh_xwj.json) |
| `h72_e8m_q6q` | 防風氏（孔子世家會稽傳說） | [《史記・孔子世家》][29] | [JSON](h72_e8m_q6q.json) |
| `h72_sie_kj3` | 齊莊公 | [《史記・田敬仲完世家》][28] | [JSON](h72_sie_kj3.json) |
| `h7h_mul_94y` | 孟懿子（魯卿） | [《史記・魯周公世家》][15] | [JSON](h7h_mul_94y.json) |
| `h7h_ofc_cha` | 壽成 | [《史記・三王世家》][42] | [JSON](h7h_ofc_cha.json) |
| `h7t_e5e_m79` | 恢所愛姬（未名） | [《史記・呂太后本紀》][9] | [JSON](h7t_e5e_m79.json) |
| `h88_q0o_cte` | 齊桓侯 | [《史記・扁鵲倉公列傳》][87] | [JSON](h88_q0o_cte.json) |
| `h8u_hld_5su` | 無忌 | [《史記・魏公子列傳》][59] | [JSON](h8u_hld_5su.json) |
| `h9c_g6l_yzs` | 王恬開 | [《史記・魏豹彭越列傳》][72] | [JSON](h9c_g6l_yzs.json) |
| `h9h_k94_pst` | 慎夫人 | [《史記・孝文本紀》][10] | [JSON](h9h_k94_pst.json) |
| `h9o_8gw_05e` | 褚先生 | [《史記・梁孝王世家》][40] | [JSON](h9o_8gw_05e.json) |
| `ha5_pra_1p1` | 趙賁 | [《史記・絳侯周勃世家》][39] | [JSON](ha5_pra_1p1.json) |
| `ha6_keq_bag` | 白起（引古） | [《史記・蒙恬列傳》][70] | [JSON](ha6_keq_bag.json) |
| `hae_ws1_2ad` | 秦舞陽 | [《史記・刺客列傳》][68] | [JSON](hae_ws1_2ad.json) |
| `hap_m8c_czz` | 西門豹 | [《史記・魏世家》][26] | [JSON](hap_m8c_czz.json) |
| `hb5_4zq_x4c` | 田角 | [《史記・田儋列傳》][76] | [JSON](hb5_4zq_x4c.json) |
| `hcd_x63_gy5` | 秦祖 | [《史記・仲尼弟子列傳》][49] | [JSON](hcd_x63_gy5.json) |
| `hci_lxd_jyi` | 孝己 | [《史記・陳丞相世家》][38] | [JSON](hci_lxd_jyi.json) |
| `hck_akv_oeh` | 國 | [《史記・越王勾踐世家》][23] | [JSON](hck_akv_oeh.json) |
| `hcx_p3r_9bu` | 鄧女 | [《史記・鄭世家》][24] | [JSON](hcx_p3r_9bu.json) |
| `hdc_c4s_8ox` | 信陵 | [《史記・陳涉世家》][30] | [JSON](hdc_c4s_8ox.json) |
| `hdo_orr_p35` | 蔽火光者未名 | [《史記・孟嘗君列傳》][57] | [JSON](hdo_orr_p35.json) |
| `hds_rdm_z1p` | 申徒（魏公） | [《史記・樊酈滕灌列傳》][77] | [JSON](hds_rdm_z1p.json) |
| `hem_2v5_vo9` | 報乙 | [《史記・殷本紀》][3] | [JSON](hem_2v5_vo9.json) |
| `her_yz1_pgf` | 蒙武 | [《史記・秦本紀》][5]、[《史記・秦始皇本紀》][6]、[《史記・楚世家》][22] | [JSON](her_yz1_pgf.json) |
| `hfi_bl9_w2c` | 公子將閭 | [《史記・秦始皇本紀》][6] | [JSON](hfi_bl9_w2c.json) |
| `hfn_aif_jww` | 韓安國 | [《史記・吳王濞列傳》][88] | [JSON](hfn_aif_jww.json) |
| `hfw_50q_zd2` | 呂媼 | [《史記・高祖本紀》][8] | [JSON](hfw_50q_zd2.json) |
| `hg5_iv6_53r` | 柘稽 | [《史記・越王勾踐世家》][23] | [JSON](hg5_iv6_53r.json) |
| `hg5_p1m_pny` | 悼太子（昭襄時） | [《史記・秦本紀》][5] | [JSON](hg5_p1m_pny.json) |
| `hgi_77w_xaa` | 起（衛君） | [《史記・衛康叔世家》][19] | [JSON](hgi_77w_xaa.json) |
| `hgu_sqs_8l9` | 少衛姬（元母） | [《史記・齊太公世家》][14] | [JSON](hgu_sqs_8l9.json) |
| `hh3_ak4_jge` | 太史公 | [《史記・魯仲連鄒陽列傳》][65] | [JSON](hh3_ak4_jge.json) |
| `hhe_qbu_ohy` | 朱雞石 | [《史記・陳涉世家》][30] | [JSON](hhe_qbu_ohy.json) |
| `hi5_2q4_qme` | 陳太后 | [《史記・梁孝王世家》][40] | [JSON](hi5_2q4_qme.json) |
| `hil_73x_nk5` | 女華 | [《史記・秦本紀》][5] | [JSON](hil_73x_nk5.json) |
| `hil_pvv_3c6` | 秦女（楚平王妻珍母） | [《史記・楚世家》][22] | [JSON](hil_pvv_3c6.json) |
| `hio_jt3_l3z` | 鐘離眛 | [《史記・樊酈滕灌列傳》][77] | [JSON](hio_jt3_l3z.json) |
| `hiz_hez_6wg` | 平原君 | [《史記・魯仲連鄒陽列傳》][65] | [JSON](hiz_hez_6wg.json) |
| `hjk_nm8_og1` | 曹山跗 | [《史記・扁鵲倉公列傳》][87] | [JSON](hjk_nm8_og1.json) |
| `hjx_5rx_wzu` | 韓信平城下 | [《史記・傅靳蒯成列傳》][80] | [JSON](hjx_5rx_wzu.json) |
| `hk6_cwu_bmf` | 蕭何 | [《史記・蕭相國世家》][35] | [JSON](hk6_cwu_bmf.json) |
| `hka_te6_9q1` | 崇侯虎 | [《史記・周本紀》][4] | [JSON](hka_te6_9q1.json) |
| `hkc_5tg_d73` | 鮑叔牙 | [《史記・管晏列傳》][44] | [JSON](hkc_5tg_d73.json) |
| `hl3_lu0_nrx` | 虞將軍未詳名 | [《史記・劉敬叔孫通列傳》][81] | [JSON](hl3_lu0_nrx.json) |
| `hl7_zsf_3lx` | 胡衍 | [《史記・樗里子甘茂列傳》][53] | [JSON](hl7_zsf_3lx.json) |
| `hlr_wnv_o0x` | 太史公 | [《史記・張儀列傳》][52] | [JSON](hlr_wnv_o0x.json) |
| `hm1_rqr_l9u` | 韓王信（韓太尉） | [《史記・韓信盧綰列傳》][75] | [JSON](hm1_rqr_l9u.json) |
| `hm9_d4o_xna` | 犯蹕者未名 | [《史記・張釋之馮唐列傳》][84] | [JSON](hm9_d4o_xna.json) |
| `hmc_rv2_qxm` | 齊宣王（燕篇） | [《史記・蘇秦列傳》][51] | [JSON](hmc_rv2_qxm.json) |
| `hmf_0gk_k9w` | 衛將軍未具名 | [《史記・田叔列傳》][86] | [JSON](hmf_0gk_k9w.json) |
| `hmr_3oo_5m5` | 漢宣帝 | [《史記・張丞相列傳》][78] | [JSON](hmr_3oo_5m5.json) |
| `hmx_ohe_wso` | 楚考烈王（滅魯記事） | [《史記・魯周公世家》][15] | [JSON](hmx_ohe_wso.json) |
| `hn4_62t_avw` | 衛君 | [《史記・老子韓非列傳》][45] | [JSON](hn4_62t_avw.json) |
| `hn4_jh3_9yu` | 郈昭伯 | [《史記・孔子世家》][29] | [JSON](hn4_jh3_9yu.json) |
| `hnq_jmv_kxf` | 樂羊 | [《史記・魏世家》][26] | [JSON](hnq_jmv_kxf.json) |
| `hnq_xtn_hjk` | 魏齊 | [《史記・魏世家》][26] | [JSON](hnq_xtn_hjk.json) |
| `hnx_2zc_ixj` | 陳澤 | [《史記・張耳陳餘列傳》][71] | [JSON](hnx_2zc_ixj.json) |
| `ho4_me8_not` | 趙肅侯 | [《史記・蘇秦列傳》][51] | [JSON](ho4_me8_not.json) |
| `ho5_sbj_e9x` | 宰孔 | [《史記・齊太公世家》][14] | [JSON](ho5_sbj_e9x.json) |
| `ho7_tz6_77t` | 蘇秦貸資者 | [《史記・蘇秦列傳》][51] | [JSON](ho7_tz6_77t.json) |
| `hob_fsb_jia` | 魏惠王 | [《史記・趙世家》][25] | [JSON](hob_fsb_jia.json) |
| `hot_99a_5vc` | 程縱 | [《史記・絳侯周勃世家》][39] | [JSON](hot_99a_5vc.json) |
| `hp0_wll_0jp` | 太史公 | [《史記・呂不韋列傳》][67] | [JSON](hp0_wll_0jp.json) |
| `hp3_t87_5a3` | 趙養卒未名 | [《史記・張耳陳餘列傳》][71] | [JSON](hp3_t87_5a3.json) |
| `hph_y6n_3zb` | 李牧 | [《史記・廉頗藺相如列傳》][63] | [JSON](hph_y6n_3zb.json) |
| `hpy_6lu_tc5` | 趙賁 | [《史記・傅靳蒯成列傳》][80] | [JSON](hpy_6lu_tc5.json) |
| `hqa_44f_22t` | 趙文子（季子所語者） | [《史記・晉世家》][21] | [JSON](hqa_44f_22t.json) |
| `hqe_r6c_hmf` | 芒 | [《史記・夏本紀》][2] | [JSON](hqe_r6c_hmf.json) |
| `hqm_y3n_8bq` | 魏惠王（楚篇強國記事） | [《史記・楚世家》][22] | [JSON](hqm_y3n_8bq.json) |
| `hqs_i1n_n5h` | 陽虎 | [《史記・魯周公世家》][15] | [JSON](hqs_i1n_n5h.json) |
| `hr1_cou_3hm` | 田解 | [《史記・傅靳蒯成列傳》][80] | [JSON](hr1_cou_3hm.json) |
| `hrg_u13_8h3` | 公子卬 | [《史記・趙世家》][25]、[《史記・魏世家》][26] | [JSON](hrg_u13_8h3.json) |
| `hri_c2p_nht` | 周殷 | [《史記・陳丞相世家》][38] | [JSON](hri_c2p_nht.json) |
| `hrm_lw1_f9d` | 楚懷王 | [《史記・曹相國世家》][36] | [JSON](hrm_lw1_f9d.json) |
| `hrw_lli_22s` | 季康子 | [《史記・魯周公世家》][15] | [JSON](hrw_lli_22s.json) |
| `hsg_oao_yjg` | 孫奮 | [《史記・樊酈滕灌列傳》][77] | [JSON](hsg_oao_yjg.json) |
| `ht1_kdz_izj` | 陳豨 | [《史記・樊酈滕灌列傳》][77] | [JSON](ht1_kdz_izj.json) |
| `ht8_t4d_vbc` | 陳豨 | [《史記・張丞相列傳》][78] | [JSON](ht8_t4d_vbc.json) |
| `htd_fv4_x64` | 羿 | [《史記・仲尼弟子列傳》][49] | [JSON](htd_fv4_x64.json) |
| `hts_3sp_0x7` | 韓信 | [《史記・淮陰侯列傳》][74] | [JSON](hts_3sp_0x7.json) |
| `hu1_vru_vho` | 叔孫昭子（內昭公議事） | [《史記・魯周公世家》][15] | [JSON](hu1_vru_vho.json) |
| `huf_d39_8pf` | 周太史儋 | [《史記・老子韓非列傳》][45] | [JSON](huf_d39_8pf.json) |
| `huq_dao_urx` | 東陽甯君 | [《史記・高祖本紀》][8] | [JSON](huq_dao_urx.json) |
| `hv8_0ce_lw9` | 閎夭 | [《史記・周本紀》][4] | [JSON](hv8_0ce_lw9.json) |
| `hvf_el4_hqj` | 田假 | [《史記・田儋列傳》][76] | [JSON](hvf_el4_hqj.json) |
| `hvn_rqs_4hz` | 紀信 | [《史記・項羽本紀》][7] | [JSON](hvn_rqs_4hz.json) |
| `hvx_dq8_la2` | 燕王喜 | [《史記・刺客列傳》][68] | [JSON](hvx_dq8_la2.json) |
| `hw7_g75_oiz` | 化爲丈夫女子（魏世家敘事未名者） | [《史記・魏世家》][26] | [JSON](hw7_g75_oiz.json) |
| `hwx_vox_7ml` | 董狐（晉太史） | [《史記・晉世家》][21] | [JSON](hwx_vox_7ml.json) |
| `hwx_ze7_xjq` | 巨嫂 | [《史記・楚元王世家》][32] | [JSON](hwx_ze7_xjq.json) |
| `hx3_xne_efc` | 南宮牛（萬弟） | [《史記・宋微子世家》][20] | [JSON](hx3_xne_efc.json) |
| `hxh_k0o_r87` | 召騷 | [《史記・陳涉世家》][30] | [JSON](hxh_k0o_r87.json) |
| `hxh_m9p_3io` | 晉君 | [《史記・仲尼弟子列傳》][49] | [JSON](hxh_m9p_3io.json) |
| `hxk_jd2_eqg` | 樂成侯（欒大引見者） | [《史記・孝武本紀》][12] | [JSON](hxk_jd2_eqg.json) |
| `hxt_doh_daz` | 毛翕公 | [《史記・樂毅列傳》][62] | [JSON](hxt_doh_daz.json) |
| `hy4_7ra_i67` | 樅公 | [《史記・項羽本紀》][7]、[《史記・高祖本紀》][8] | [JSON](hy4_7ra_i67.json) |
| `hya_7qu_m25` | 穰侯 | [《史記・白起王翦列傳》][55] | [JSON](hya_7qu_m25.json) |
| `hza_lsx_umi` | 韓子引古未定 | [《史記・范睢蔡澤列傳》][61] | [JSON](hza_lsx_umi.json) |
| `hzc_zln_xl1` | 涇陽君（田世家未名者） | [《史記・田敬仲完世家》][28] | [JSON](hzc_zln_xl1.json) |
| `hzd_39r_m9e` | 吳太伯 | [《史記・吳太伯世家》][13] | [JSON](hzd_39r_m9e.json) |
| `hzs_qet_58s` | 豎陽穀（楚篇進酒者） | [《史記・晉世家》][21]、[《史記・楚世家》][22] | [JSON](hzs_qet_58s.json) |
| `hzt_j3d_1r3` | 嫪毐 | [《史記・呂不韋列傳》][67] | [JSON](hzt_j3d_1r3.json) |
| `hzx_kl2_8vp` | 少師彊 | [《史記・周本紀》][4] | [JSON](hzx_kl2_8vp.json) |
| `i02_muu_r2s` | 平原君 | [《史記・平原君虞卿列傳》][58] | [JSON](i02_muu_r2s.json) |
| `i0f_weg_moh` | 夏無且 | [《史記・刺客列傳》][68] | [JSON](i0f_weg_moh.json) |
| `i0l_qkb_6wb` | 紂 | [《史記・張儀列傳》][52] | [JSON](i0l_qkb_6wb.json) |
| `i0s_qll_p1n` | 閼伯 | [《史記・鄭世家》][24] | [JSON](i0s_qll_p1n.json) |
| `i0t_oxd_o9s` | 褚先生 | [《史記・三王世家》][42] | [JSON](i0t_oxd_o9s.json) |
| `i18_zjl_0e8` | 周顯王 | [《史記・蘇秦列傳》][51] | [JSON](i18_zjl_0e8.json) |
| `i1a_t74_swi` | 宋華子 | [《史記・齊太公世家》][14] | [JSON](i1a_t74_swi.json) |
| `i1r_rv4_xst` | 嬰齊 | [《史記・三王世家》][42] | [JSON](i1r_rv4_xst.json) |
| `i1w_xhk_9ko` | 務光 | [《史記・伯夷列傳》][43] | [JSON](i1w_xhk_9ko.json) |
| `i29_1mw_ghb` | 呉起 | [《史記・魏世家》][26] | [JSON](i29_1mw_ghb.json) |
| `i2g_tm1_38n` | 黔（荼異母兄） | [《史記・齊太公世家》][14] | [JSON](i2g_tm1_38n.json) |
| `i2k_2p5_wtv` | 白圭引古 | [《史記・魯仲連鄒陽列傳》][65] | [JSON](i2k_2p5_wtv.json) |
| `i30_zix_o1p` | 項梁 | [《史記・絳侯周勃世家》][39] | [JSON](i30_zix_o1p.json) |
| `i35_als_hdv` | 蕢聵 | [《史記・仲尼弟子列傳》][49] | [JSON](i35_als_hdv.json) |
| `i37_l7b_6n8` | 菑川王書信未名 | [《史記・吳王濞列傳》][88] | [JSON](i37_l7b_6n8.json) |
| `i3c_26z_spn` | 蒯通 | [《史記・張耳陳餘列傳》][71] | [JSON](i3c_26z_spn.json) |
| `i3f_9l9_g53` | 陳平 | [《史記・陳丞相世家》][38] | [JSON](i3f_9l9_g53.json) |
| `i3q_5yn_aat` | 餘（衛共伯） | [《史記・衛康叔世家》][19] | [JSON](i3q_5yn_aat.json) |
| `i3q_rxz_ou9` | 赤（秦將被虜者） | [《史記・晉世家》][21] | [JSON](i3q_rxz_ou9.json) |
| `i4l_f1t_g0j` | 子朝 | [《史記・趙世家》][25] | [JSON](i4l_f1t_g0j.json) |
| `i4m_8cq_inb` | 師己（童謠引者） | [《史記・魯周公世家》][15] | [JSON](i4m_8cq_inb.json) |
| `i56_shx_l9i` | 騶奭 | [《史記・孟子荀卿列傳》][56] | [JSON](i56_shx_l9i.json) |
| `i57_0fx_nlz` | 太史公 | [《史記・伍子胥列傳》][48] | [JSON](i57_0fx_nlz.json) |
| `i5r_tl5_rdl` | 華元 | [《史記・宋微子世家》][20] | [JSON](i5r_tl5_rdl.json) |
| `i5w_mgw_zh8` | 充 | [《史記・三王世家》][42] | [JSON](i5w_mgw_zh8.json) |
| `i5x_ejl_y1u` | 彊（曹幽伯） | [《史記・管蔡世家》][17] | [JSON](i5x_ejl_y1u.json) |
| `i5z_pha_qe4` | 衞靈公 | [《史記・趙世家》][25] | [JSON](i5z_pha_qe4.json) |
| `i60_oem_8mu` | 亞父 | [《史記・項羽本紀》][7] | [JSON](i60_oem_8mu.json) |
| `i6i_ttu_6a8` | 尉止 | [《史記・鄭世家》][24] | [JSON](i6i_ttu_6a8.json) |
| `i6s_ge7_oiz` | 御史大夫施 | [《史記・絳侯周勃世家》][39] | [JSON](i6s_ge7_oiz.json) |
| `i73_adp_pfg` | 田需 | [《史記・張儀列傳》][52] | [JSON](i73_adp_pfg.json) |
| `i74_7n6_nxx` | 魏王大梁被虜未名 | [《史記・魏公子列傳》][59] | [JSON](i74_7n6_nxx.json) |
| `i7a_22p_qda` | 句踐 | [《史記・越王勾踐世家》][23] | [JSON](i7a_22p_qda.json) |
| `i7a_rc8_hf1` | 糾母（魯女未名） | [《史記・齊太公世家》][14] | [JSON](i7a_rc8_hf1.json) |
| `i7b_17m_npx` | 皋陶（孔子世家形貌比擬傳說） | [《史記・孔子世家》][29] | [JSON](i7b_17m_npx.json) |
| `i7w_kp4_69q` | 公子如 | [《史記・鄭世家》][24] | [JSON](i7w_kp4_69q.json) |
| `i7z_9r1_d1w` | 王離 | [《史記・李斯列傳》][69] | [JSON](i7z_9r1_d1w.json) |
| `i83_1ys_gdj` | 辛伯 | [《史記・周本紀》][4] | [JSON](i83_1ys_gdj.json) |
| `i8e_7wk_5kj` | 城陽中尉未名 | [《史記・吳王濞列傳》][88] | [JSON](i8e_7wk_5kj.json) |
| `i8j_sze_ft5` | 魏襄王 | [《史記・田敬仲完世家》][28] | [JSON](i8j_sze_ft5.json) |
| `i8m_w3r_o5f` | 張耳 | [《史記・荊燕世家》][33] | [JSON](i8m_w3r_o5f.json) |
| `i8p_f0y_kea` | 張尚 | [《史記・楚元王世家》][32] | [JSON](i8p_f0y_kea.json) |
| `i8y_6lu_30h` | 周市 | [《史記・高祖本紀》][8] | [JSON](i8y_6lu_30h.json) |
| `i9s_j7z_8bo` | 子之引古 | [《史記・魯仲連鄒陽列傳》][65] | [JSON](i9s_j7z_8bo.json) |
| `ia8_8tw_gey` | 公山不狃 | [《史記・孔子世家》][29] | [JSON](ia8_8tw_gey.json) |
| `iai_csf_zlg` | 鄭幽公 | [《史記・韓世家》][27] | [JSON](iai_csf_zlg.json) |
| `ibi_qk6_07w` | 趙利 | [《史記・高祖本紀》][8] | [JSON](ibi_qk6_07w.json) |
| `ibu_a0b_ggu` | 袁盎 | [《史記・袁盎鼂錯列傳》][83] | [JSON](ibu_a0b_ggu.json) |
| `ic0_1fb_fg8` | 魏公子救邯鄲 | [《史記・魏公子列傳》][59] | [JSON](ic0_1fb_fg8.json) |
| `ic1_x9o_8rb` | 扁鵲 | [《史記・高祖本紀》][8] | [JSON](ic1_x9o_8rb.json) |
| `ic2_0dp_oms` | 文帝前后（本卷未名） | [《史記・孝景本紀》][11] | [JSON](ic2_0dp_oms.json) |
| `ic8_7be_6x3` | 蕭何 | [《史記・蕭相國世家》][35] | [JSON](ic8_7be_6x3.json) |
| `ica_cts_5j1` | 桓公引古 | [《史記・魯仲連鄒陽列傳》][65] | [JSON](ica_cts_5j1.json) |
| `icp_nrn_7pl` | 申差 | [《史記・秦本紀》][5]、[《史記・張儀列傳》][52] | [JSON](icp_nrn_7pl.json) |
| `id0_ryz_8tv` | 徐姬（齊桓公夫人） | [《史記・齊太公世家》][14] | [JSON](id0_ryz_8tv.json) |
| `id5_d3k_vsc` | 龐涓 | [《史記・孫子吳起列傳》][47] | [JSON](id5_d3k_vsc.json) |
| `ids_h4k_pn5` | 季連（楚篇祖系） | [《史記・楚世家》][22] | [JSON](ids_h4k_pn5.json) |
| `idu_gor_8a1` | 周章 | [《史記・陳涉世家》][30] | [JSON](idu_gor_8a1.json) |
| `ie0_5f2_2uz` | 子政母未名 | [《史記・呂不韋列傳》][67] | [JSON](ie0_5f2_2uz.json) |
| `ie6_nw9_g32` | 中衍 | [《史記・秦本紀》][5] | [JSON](ie6_nw9_g32.json) |
| `iev_czl_w1c` | 章邯 | [《史記・曹相國世家》][36] | [JSON](iev_czl_w1c.json) |
| `if1_4vk_fku` | 呂平 | [《史記・呂太后本紀》][9] | [JSON](if1_4vk_fku.json) |
| `if3_naf_6yw` | 湯 | [《史記・越王勾踐世家》][23] | [JSON](if3_naf_6yw.json) |
| `if4_wp6_d3d` | 蕭文終 | [《史記・三王世家》][42] | [JSON](if4_wp6_d3d.json) |
| `if7_vxj_m6q` | 韓哀侯 | [《史記・鄭世家》][24] | [JSON](if7_vxj_m6q.json) |
| `ifc_1dx_zrh` | 曹氏未詳名 | [《史記・張丞相列傳》][78] | [JSON](ifc_1dx_zrh.json) |
| `ifc_pry_e72` | 司馬卬 | [《史記・高祖本紀》][8] | [JSON](ifc_pry_e72.json) |
| `ifh_n0a_cwo` | 張丑 | [《史記・孟嘗君列傳》][57] | [JSON](ifh_n0a_cwo.json) |
| `ifp_vbc_yh6` | 陳鋒氏女 | [《史記・五帝本紀》][1] | [JSON](ifp_vbc_yh6.json) |
| `ifr_qn1_ibu` | 喬如（長翟） | [《史記・魯周公世家》][15] | [JSON](ifr_qn1_ibu.json) |
| `ify_oqo_7fy` | 鄭袖（楚懷王幸姬） | [《史記・楚世家》][22] | [JSON](ify_oqo_7fy.json) |
| `ig9_uk1_7rh` | 子玉（楚得臣） | [《史記・晉世家》][21] | [JSON](ig9_uk1_7rh.json) |
| `iga_nvl_wl4` | 劉媼 | [《史記・高祖本紀》][8] | [JSON](iga_nvl_wl4.json) |
| `igi_ttk_g03` | 公子咎 | [《史記・周本紀》][4] | [JSON](igi_ttk_g03.json) |
| `ih1_n37_pg3` | 后勝（引古） | [《史記・蒙恬列傳》][70] | [JSON](ih1_n37_pg3.json) |
| `iha_07s_i6a` | 周公 | [《史記・魯周公世家》][15] | [JSON](iha_07s_i6a.json) |
| `ihg_nx9_blj` | 燕姞 | [《史記・鄭世家》][24] | [JSON](ihg_nx9_blj.json) |
| `ihr_2dp_dws` | 師曹（衛琴師） | [《史記・衛康叔世家》][19] | [JSON](ihr_2dp_dws.json) |
| `ihr_z95_la8` | 司馬梗 | [《史記・秦本紀》][5]、[《史記・白起王翦列傳》][55] | [JSON](ihr_z95_la8.json) |
| `iht_32d_ovx` | 趙先王 | [《史記・張儀列傳》][52] | [JSON](iht_32d_ovx.json) |
| `iig_8e3_qx2` | 由余 | [《史記・秦本紀》][5] | [JSON](iig_8e3_qx2.json) |
| `ije_3uz_q79` | 智伯瑤 | [《史記・春申君列傳》][60] | [JSON](ije_3uz_q79.json) |
| `ijk_q79_sjg` | 夫槩 | [《史記・吳太伯世家》][13] | [JSON](ijk_q79_sjg.json) |
| `ik4_61m_hqn` | 薛君（御史大夫） | [《史記・張丞相列傳》][78] | [JSON](ik4_61m_hqn.json) |
| `ika_oa1_ubm` | 魏子所假粟賢者未名 | [《史記・孟嘗君列傳》][57] | [JSON](ika_oa1_ubm.json) |
| `iko_0gs_u68` | 吳起妻 | [《史記・孫子吳起列傳》][47] | [JSON](iko_0gs_u68.json) |
| `ikp_b3b_9i7` | 蕭何 | [《史記・留侯世家》][37] | [JSON](ikp_b3b_9i7.json) |
| `ikz_hn2_08f` | 穰侯（魏世家未名者） | [《史記・魏世家》][26] | [JSON](ikz_hn2_08f.json) |
| `il9_kpr_9zz` | 龍賈 | [《史記・蘇秦列傳》][51] | [JSON](il9_kpr_9zz.json) |
| `ild_qbl_r1q` | 越石父 | [《史記・管晏列傳》][44] | [JSON](ild_qbl_r1q.json) |
| `ile_1tb_ymg` | 周引功 | [《史記・白起王翦列傳》][55] | [JSON](ile_1tb_ymg.json) |
| `iln_cic_3d5` | 南公揭 | [《史記・秦本紀》][5] | [JSON](iln_cic_3d5.json) |
| `ilz_9fs_tfm` | 楚懷王 | [《史記・劉敬叔孫通列傳》][81] | [JSON](ilz_9fs_tfm.json) |
| `ima_dfc_4lp` | 周定王（楚篇問鼎者） | [《史記・楚世家》][22] | [JSON](ima_dfc_4lp.json) |
| `iml_mgn_ycw` | 關龍逢引古 | [《史記・李斯列傳》][69] | [JSON](iml_mgn_ycw.json) |
| `imo_djf_mce` | 桓公（考王弟） | [《史記・周本紀》][4] | [JSON](imo_djf_mce.json) |
| `imr_0y4_sn9` | 趙衰晉妻（趙世家未名者） | [《史記・趙世家》][25] | [JSON](imr_0y4_sn9.json) |
| `in3_sox_l50` | 卞隨 | [《史記・伯夷列傳》][43] | [JSON](in3_sox_l50.json) |
| `in5_znv_otq` | 胡陽 | [《史記・穰侯列傳》][54] | [JSON](in5_znv_otq.json) |
| `ind_hfs_rpw` | 黎鉏 | [《史記・孔子世家》][29] | [JSON](ind_hfs_rpw.json) |
| `iny_l7o_7n5` | 太史公 | [《史記・春申君列傳》][60] | [JSON](iny_l7o_7n5.json) |
| `io7_a32_npk` | 韓康子 | [《史記・魏世家》][26] | [JSON](io7_a32_npk.json) |
| `iob_qd9_w2s` | 建母（本卷未名） | [《史記・吳太伯世家》][13] | [JSON](iob_qd9_w2s.json) |
| `iok_1fq_m6d` | 叔向 | [《史記・田敬仲完世家》][28] | [JSON](iok_1fq_m6d.json) |
| `iop_qvt_un3` | 庚丁 | [《史記・殷本紀》][3] | [JSON](iop_qvt_un3.json) |
| `iot_q5p_yh1` | 濟南王未具名 | [《史記・扁鵲倉公列傳》][87] | [JSON](iot_q5p_yh1.json) |
| `ip6_ebi_1g6` | 平原 | [《史記・陳涉世家》][30] | [JSON](ip6_ebi_1g6.json) |
| `ipn_rl3_fnf` | 廉頗 | [《史記・陳涉世家》][30] | [JSON](ipn_rl3_fnf.json) |
| `iq6_mf0_9bs` | 商君引古未定 | [《史記・李斯列傳》][69] | [JSON](iq6_mf0_9bs.json) |
| `iqg_h1x_bml` | 盤庚 | [《史記・伍子胥列傳》][48] | [JSON](iqg_h1x_bml.json) |
| `iqm_u8b_z05` | 呂后 | [《史記・張耳陳餘列傳》][71] | [JSON](iqm_u8b_z05.json) |
| `iqs_91w_s5e` | 少典 | [《史記・五帝本紀》][1] | [JSON](iqs_91w_s5e.json) |
| `iqu_pas_2r5` | 齊宣王 | [《史記・蘇秦列傳》][51] | [JSON](iqu_pas_2r5.json) |
| `iqz_qdq_27b` | 商瞿母 | [《史記・仲尼弟子列傳》][49] | [JSON](iqz_qdq_27b.json) |
| `ir5_t3h_e35` | 田單 | [《史記・田單列傳》][64] | [JSON](ir5_t3h_e35.json) |
| `ird_cqk_5eh` | 樂羊 | [《史記・樂毅列傳》][62] | [JSON](ird_cqk_5eh.json) |
| `irl_hj6_qpd` | 蔡女（陳厲公妻） | [《史記・陳杞世家》][18] | [JSON](irl_hj6_qpd.json) |
| `irt_r82_b3b` | 帝嚳引古 | [《史記・屈原賈生列傳》][66] | [JSON](irt_r82_b3b.json) |
| `iry_fvs_zxc` | 欒布 | [《史記・吳王濞列傳》][88] | [JSON](iry_fvs_zxc.json) |
| `is3_9h6_hq6` | 周市 | [《史記・魏豹彭越列傳》][72] | [JSON](is3_9h6_hq6.json) |
| `is4_hi1_0mc` | 發根（游水人） | [《史記・孝武本紀》][12] | [JSON](is4_hi1_0mc.json) |
| `is6_glb_qw5` | 密康公之母 | [《史記・周本紀》][4] | [JSON](is6_glb_qw5.json) |
| `isb_fx9_9z9` | 吳王夫差引古 | [《史記・李斯列傳》][69] | [JSON](isb_fx9_9z9.json) |
| `isc_3cc_0cq` | 魏王蘇代過魏 | [《史記・蘇秦列傳》][51] | [JSON](isc_3cc_0cq.json) |
| `isl_ylr_h73` | 宋繆公 | [《史記・鄭世家》][24] | [JSON](isl_ylr_h73.json) |
| `it2_a12_ldj` | 呂后 | [《史記・魏豹彭越列傳》][72] | [JSON](it2_a12_ldj.json) |
| `it8_m2p_rrk` | 胡亥 | [《史記・秦始皇本紀》][6] | [JSON](it8_m2p_rrk.json) |
| `itn_zi2_il4` | 伊尹 | [《史記・殷本紀》][3] | [JSON](itn_zi2_il4.json) |
| `itv_sak_1j3` | 莒子（莊公六年朝齊） | [《史記・齊太公世家》][14] | [JSON](itv_sak_1j3.json) |
| `iu8_4tz_l19` | 淮陰侯未詳名 | [《史記・淮陰侯列傳》][74] | [JSON](iu8_4tz_l19.json) |
| `iuj_hq5_cqn` | 韓女（趙世家武靈王夫人未名者） | [《史記・趙世家》][25] | [JSON](iuj_hq5_cqn.json) |
| `iup_2pk_zgh` | 受降燕將未名 | [《史記・田單列傳》][64] | [JSON](iup_2pk_zgh.json) |
| `iv0_705_1c6` | 呂祿女 | [《史記・齊悼惠王世家》][34] | [JSON](iv0_705_1c6.json) |
| `iv3_1c9_df4` | 濟南王書信未名 | [《史記・吳王濞列傳》][88] | [JSON](iv3_1c9_df4.json) |
| `iw1_34w_8fh` | 昭侯（晉君） | [《史記・齊太公世家》][14]、[《史記・魯周公世家》][15] | [JSON](iw1_34w_8fh.json) |
| `iwp_3ea_wpr` | 呂省 | [《史記・晉世家》][21] | [JSON](iwp_3ea_wpr.json) |
| `iwz_utl_632` | 趙夙（獻公御戎） | [《史記・晉世家》][21] | [JSON](iwz_utl_632.json) |
| `ix4_u66_cn9` | 隨何 | [《史記・黥布列傳》][73] | [JSON](ix4_u66_cn9.json) |
| `ixq_92p_8b8` | 留（陳君） | [《史記・陳杞世家》][18] | [JSON](ixq_92p_8b8.json) |
| `iy8_wgd_wnk` | 湯 | [《史記・蘇秦列傳》][51] | [JSON](iy8_wgd_wnk.json) |
| `iyk_qvv_07j` | 樂叔 | [《史記・樂毅列傳》][62] | [JSON](iyk_qvv_07j.json) |
| `j0a_7ai_tbu` | 寬舒 | [《史記・孝武本紀》][12] | [JSON](j0a_7ai_tbu.json) |
| `j0b_1s6_k98` | 開方 | [《史記・齊太公世家》][14] | [JSON](j0b_1s6_k98.json) |
| `j0g_kpf_v3u` | 呂后長女 | [《史記・外戚世家》][31] | [JSON](j0g_kpf_v3u.json) |
| `j0k_8uz_am1` | 女房 | [《史記・殷本紀》][3] | [JSON](j0k_8uz_am1.json) |
| `j17_pm7_hng` | 王子虎（命晉伯使者） | [《史記・晉世家》][21] | [JSON](j17_pm7_hng.json) |
| `j1i_hx4_v15` | 馮亭 | [《史記・白起王翦列傳》][55] | [JSON](j1i_hx4_v15.json) |
| `j2b_w5a_xxk` | 薄太后 | [《史記・孝文本紀》][10]、[《史記・絳侯周勃世家》][39] | [JSON](j2b_w5a_xxk.json) |
| `j2k_9wg_9q8` | 公孫彊（曹司城） | [《史記・管蔡世家》][17] | [JSON](j2k_9wg_9q8.json) |
| `j2w_ldj_v0t` | 鄭昭公 | [《史記・秦本紀》][5] | [JSON](j2w_ldj_v0t.json) |
| `j31_jbm_64m` | 太史公 | [《史記・蕭相國世家》][35] | [JSON](j31_jbm_64m.json) |
| `j3c_ajp_44x` | 文王 | [《史記・周本紀》][4] | [JSON](j3c_ajp_44x.json) |
| `j42_va4_389` | 駒（荼異母兄） | [《史記・齊太公世家》][14] | [JSON](j42_va4_389.json) |
| `j4e_gam_0tl` | 韓信（楚王） | [《史記・樊酈滕灌列傳》][77] | [JSON](j4e_gam_0tl.json) |
| `j5e_759_c2b` | 姚卬 | [《史記・絳侯周勃世家》][39] | [JSON](j5e_759_c2b.json) |
| `j5l_wwv_wfo` | 張良 | [《史記・韓信盧綰列傳》][75] | [JSON](j5l_wwv_wfo.json) |
| `j5s_4zz_bos` | 仲尼（引文稱呼） | [《史記・秦始皇本紀》][6] | [JSON](j5s_4zz_bos.json) |
| `j66_0ti_bky` | 欒逞 | [《史記・田敬仲完世家》][28] | [JSON](j66_0ti_bky.json) |
| `j6b_h03_igz` | 潘崇（商臣傅） | [《史記・楚世家》][22] | [JSON](j6b_h03_igz.json) |
| `j6p_6jf_gjp` | 大夫種 | [《史記・伍子胥列傳》][48] | [JSON](j6p_6jf_gjp.json) |
| `j82_fk4_3t1` | 王戊 | [《史記・秦始皇本紀》][6] | [JSON](j82_fk4_3t1.json) |
| `j8g_yef_isr` | 彭越 | [《史記・季布欒布列傳》][82] | [JSON](j8g_yef_isr.json) |
| `j8l_ncd_k88` | 項籍 | [《史記・項羽本紀》][7] | [JSON](j8l_ncd_k88.json) |
| `j8n_xqp_bh6` | 湯 | [《史記・三王世家》][42] | [JSON](j8n_xqp_bh6.json) |
| `j8z_8ud_udc` | 眛（韓公子齊相） | [《史記・楚世家》][22] | [JSON](j8z_8ud_udc.json) |
| `j8z_yva_82g` | 蒙恬 | [《史記・蒙恬列傳》][70] | [JSON](j8z_yva_82g.json) |
| `j9e_3se_1wl` | 賈佗（楚篇文公股肱） | [《史記・晉世家》][21]、[《史記・楚世家》][22] | [JSON](j9e_3se_1wl.json) |
| `j9f_i2u_283` | 籍福 | [《史記・季布欒布列傳》][82] | [JSON](j9f_i2u_283.json) |
| `j9n_viq_5o8` | 九侯 | [《史記・殷本紀》][3] | [JSON](j9n_viq_5o8.json) |
| `j9r_60d_mah` | 成荊 | [《史記・范睢蔡澤列傳》][61] | [JSON](j9r_60d_mah.json) |
| `ja0_1pr_vhk` | 趙括 | [《史記・廉頗藺相如列傳》][63] | [JSON](ja0_1pr_vhk.json) |
| `ja1_60d_r62` | 李太后 | [《史記・梁孝王世家》][40] | [JSON](ja1_60d_r62.json) |
| `ja6_jit_b60` | 宮妾（師曹教琴者） | [《史記・衛康叔世家》][19] | [JSON](ja6_jit_b60.json) |
| `jai_n7f_2lj` | 扃 | [《史記・夏本紀》][2] | [JSON](jai_n7f_2lj.json) |
| `jau_d68_s2w` | 陰陵田父 | [《史記・項羽本紀》][7] | [JSON](jau_d68_s2w.json) |
| `jaw_b0s_ujn` | 穰苴 | [《史記・司馬穰苴列傳》][46] | [JSON](jaw_b0s_ujn.json) |
| `jb2_tak_5p8` | 華陽夫人 | [《史記・呂不韋列傳》][67] | [JSON](jb2_tak_5p8.json) |
| `jb9_8aa_47l` | 周勃 | [《史記・張釋之馮唐列傳》][84] | [JSON](jb9_8aa_47l.json) |
| `jc7_nxq_532` | 將閭 | [《史記・齊悼惠王世家》][34] | [JSON](jc7_nxq_532.json) |
| `jca_07t_vf9` | 魏王降秦 | [《史記・白起王翦列傳》][55] | [JSON](jca_07t_vf9.json) |
| `jcm_7e6_d1l` | 齊桓公 | [《史記・鄭世家》][24] | [JSON](jcm_7e6_d1l.json) |
| `jcn_rp4_qap` | 晏平仲 | [《史記・齊太公世家》][14] | [JSON](jcn_rp4_qap.json) |
| `jcz_daw_nab` | 杜原款（申生傅） | [《史記・晉世家》][21] | [JSON](jcz_daw_nab.json) |
| `jdl_lhw_qs9` | 陳軫 | [《史記・楚世家》][22] | [JSON](jdl_lhw_qs9.json) |
| `jdp_e3u_rug` | 鄭文公 | [《史記・周本紀》][4] | [JSON](jdp_e3u_rug.json) |
| `jdt_2io_mvu` | 秦嘉 | [《史記・黥布列傳》][73] | [JSON](jdt_2io_mvu.json) |
| `jdu_syy_7s5` | 鬼臾區 | [《史記・孝武本紀》][12] | [JSON](jdu_syy_7s5.json) |
| `jdu_x9n_5is` | 孔子兄之女 | [《史記・仲尼弟子列傳》][49] | [JSON](jdu_x9n_5is.json) |
| `je0_q20_ktu` | 繆公引古 | [《史記・魯仲連鄒陽列傳》][65] | [JSON](je0_q20_ktu.json) |
| `jej_8s3_01z` | 項羽 | [《史記・張丞相列傳》][78] | [JSON](jej_8s3_01z.json) |
| `jex_mvs_w6d` | 許昌 | [《史記・張丞相列傳》][78] | [JSON](jex_mvs_w6d.json) |
| `jf9_key_t5m` | 楚文王（伐蔡記事） | [《史記・管蔡世家》][17] | [JSON](jf9_key_t5m.json) |
| `jfl_hyw_13h` | 魏冉 | [《史記・孟嘗君列傳》][57] | [JSON](jfl_hyw_13h.json) |
| `jfs_7id_f6j` | 李牧破匈奴單于未名 | [《史記・廉頗藺相如列傳》][63] | [JSON](jfs_7id_f6j.json) |
| `jft_su5_rqv` | 魏武子（重耳五士） | [《史記・晉世家》][21] | [JSON](jft_su5_rqv.json) |
| `jg1_ag9_033` | 老子 | [《史記・老子韓非列傳》][45] | [JSON](jg1_ag9_033.json) |
| `jg7_dpd_2ev` | 趙簡子 | [《史記・晉世家》][21] | [JSON](jg7_dpd_2ev.json) |
| `jgd_o1y_l7r` | 文公夫人秦女（本篇未分辨者） | [《史記・晉世家》][21] | [JSON](jgd_o1y_l7r.json) |
| `jgf_03h_m8g` | 戚夫人 | [《史記・外戚世家》][31] | [JSON](jgf_03h_m8g.json) |
| `jgl_hok_5v6` | 呂祿 | [《史記・袁盎鼂錯列傳》][83] | [JSON](jgl_hok_5v6.json) |
| `jgm_x7n_bnl` | 晉昭公 | [《史記・扁鵲倉公列傳》][87] | [JSON](jgm_x7n_bnl.json) |
| `jh5_a7h_pvv` | 王臧 | [《史記・孝武本紀》][12] | [JSON](jh5_a7h_pvv.json) |
| `jh5_kh6_e9k` | 孟舒 | [《史記・田叔列傳》][86] | [JSON](jh5_kh6_e9k.json) |
| `jhx_psq_ykg` | 鮑叔牙（楚篇齊桓公輔） | [《史記・管晏列傳》][44] | [JSON](jhx_psq_ykg.json) |
| `ji9_1mz_ffy` | 欣（塞王） | [《史記・淮陰侯列傳》][74] | [JSON](ji9_1mz_ffy.json) |
| `jik_qff_1cj` | 秦王辭師未定 | [《史記・李斯列傳》][69] | [JSON](jik_qff_1cj.json) |
| `jit_1ud_8if` | 薛歐 | [《史記・高祖本紀》][8] | [JSON](jit_1ud_8if.json) |
| `jj8_r26_ani` | 主父偃 | [《史記・樂毅列傳》][62] | [JSON](jj8_r26_ani.json) |
| `jjm_xtb_fcj` | 扈輒 | [《史記・魏豹彭越列傳》][72] | [JSON](jjm_xtb_fcj.json) |
| `jki_ijf_2w1` | 高后 | [《史記・傅靳蒯成列傳》][80] | [JSON](jki_ijf_2w1.json) |
| `jko_7a4_o8v` | 薄太后 | [《史記・楚元王世家》][32] | [JSON](jko_7a4_o8v.json) |
| `jlk_1b3_sd7` | 趙惠文王 | [《史記・樂毅列傳》][62] | [JSON](jlk_1b3_sd7.json) |
| `jlp_iua_bsf` | 齊宣王 | [《史記・魏世家》][26] | [JSON](jlp_iua_bsf.json) |
| `jlv_zw9_bk3` | 齊懿仲 | [《史記・田敬仲完世家》][28] | [JSON](jlv_zw9_bk3.json) |
| `jm9_oxb_y3l` | 宋景公（滅曹記事） | [《史記・管蔡世家》][17] | [JSON](jm9_oxb_y3l.json) |
| `jmm_0ez_y53` | 陳筮 | [《史記・韓世家》][27] | [JSON](jmm_0ez_y53.json) |
| `jmz_qgu_bq0` | 晉靈公 | [《史記・晉世家》][21] | [JSON](jmz_qgu_bq0.json) |
| `jnf_7ry_g96` | 公仲 | [《史記・韓世家》][27] | [JSON](jnf_7ry_g96.json) |
| `jnv_s2c_9yv` | 秦孝公 | [《史記・蘇秦列傳》][51] | [JSON](jnv_s2c_9yv.json) |
| `jo4_4bf_0ra` | 劉澤 | [《史記・荊燕世家》][33] | [JSON](jo4_4bf_0ra.json) |
| `joh_mm0_i8m` | 蔡姬（齊桓公夫人） | [《史記・齊太公世家》][14]、[《史記・管蔡世家》][17] | [JSON](joh_mm0_i8m.json) |
| `joj_i7q_7hs` | 赦賈使者 | [《史記・司馬穰苴列傳》][46] | [JSON](joj_i7q_7hs.json) |
| `jom_371_0rj` | 帝摯 | [《史記・五帝本紀》][1] | [JSON](jom_371_0rj.json) |
| `joz_coh_yfm` | 伯夷 | [《史記・蘇秦列傳》][51] | [JSON](joz_coh_yfm.json) |
| `jp5_f3p_wwn` | 徐偃 | [《史記・孝武本紀》][12] | [JSON](jp5_f3p_wwn.json) |
| `jps_khx_p25` | 李克 | [《史記・魏世家》][26] | [JSON](jps_khx_p25.json) |
| `jps_m3k_hu4` | 厲王 | [《史記・周本紀》][4] | [JSON](jps_m3k_hu4.json) |
| `jqp_2f4_gts` | 宰予引古 | [《史記・李斯列傳》][69] | [JSON](jqp_2f4_gts.json) |
| `jqy_1fv_u7v` | 后稷 | [《史記・周本紀》][4] | [JSON](jqy_1fv_u7v.json) |
| `jri_o6f_o4j` | 少府延 | [《史記・呂太后本紀》][9] | [JSON](jri_o6f_o4j.json) |
| `jrn_qdf_10i` | 周武王 | [《史記・魏世家》][26] | [JSON](jrn_qdf_10i.json) |
| `jrv_ob5_feu` | 軒丘豹 | [《史記・梁孝王世家》][40] | [JSON](jrv_ob5_feu.json) |
| `jry_wlf_1x3` | 成君 | [《史記・周本紀》][4] | [JSON](jry_wlf_1x3.json) |
| `js1_fea_1s7` | 有若 | [《史記・仲尼弟子列傳》][49] | [JSON](js1_fea_1s7.json) |
| `js7_kf9_lr6` | 軍門都尉 | [《史記・絳侯周勃世家》][39] | [JSON](js7_kf9_lr6.json) |
| `jsc_g0v_p8m` | 繆賢交往燕王未名 | [《史記・廉頗藺相如列傳》][63] | [JSON](jsc_g0v_p8m.json) |
| `jsi_q8y_rdj` | 甯武子 | [《史記・孔子世家》][29] | [JSON](jsi_q8y_rdj.json) |
| `jsk_quz_7bh` | 單伯 | [《史記・鄭世家》][24] | [JSON](jsk_quz_7bh.json) |
| `jsn_gfv_ekd` | 孝矦（晉君） | [《史記・魯周公世家》][15] | [JSON](jsn_gfv_ekd.json) |
| `jt4_7tp_14h` | 衞武公（季札論樂稱） | [《史記・吳太伯世家》][13] | [JSON](jt4_7tp_14h.json) |
| `jt5_4xj_v0y` | 栗卿 | [《史記・萬石張叔列傳》][85] | [JSON](jt5_4xj_v0y.json) |
| `ju6_1ic_2zu` | 灌嬰 | [《史記・齊悼惠王世家》][34] | [JSON](ju6_1ic_2zu.json) |
| `jue_6ri_i2r` | 康叔 | [《史記・衛康叔世家》][19] | [JSON](jue_6ri_i2r.json) |
| `jug_ktd_id2` | 髙止（齊人奔燕） | [《史記・燕召公世家》][16] | [JSON](jug_ktd_id2.json) |
| `juw_kxg_h7c` | 太僕饒 | [《史記・扁鵲倉公列傳》][87] | [JSON](juw_kxg_h7c.json) |
| `jvf_vfb_six` | 王信 | [《史記・絳侯周勃世家》][39] | [JSON](jvf_vfb_six.json) |
| `jvl_f6r_3bd` | 晉獻公 | [《史記・劉敬叔孫通列傳》][81] | [JSON](jvl_f6r_3bd.json) |
| `jvm_ikp_id9` | 哀侯（晉曲沃弒君記事） | [《史記・晉世家》][21] | [JSON](jvm_ikp_id9.json) |
| `jvs_fct_yow` | 紂 | [《史記・鄭世家》][24] | [JSON](jvs_fct_yow.json) |
| `jvz_4m9_60q` | 魏公子勁 | [《史記・秦本紀》][5] | [JSON](jvz_4m9_60q.json) |
| `jy1_0ud_4bc` | 荊軻引古 | [《史記・刺客列傳》][68] | [JSON](jy1_0ud_4bc.json) |
| `jya_fko_ski` | 陳豨 | [《史記・田叔列傳》][86] | [JSON](jya_fko_ski.json) |
| `jyd_5a2_cil` | 趙高 | [《史記・樊酈滕灌列傳》][77] | [JSON](jyd_5a2_cil.json) |
| `jyh_v4j_8w6` | 王翦 | [《史記・蒙恬列傳》][70] | [JSON](jyh_v4j_8w6.json) |
| `jza_af1_m41` | 袁盎 | [《史記・袁盎鼂錯列傳》][83] | [JSON](jza_af1_m41.json) |
| `jzx_qcd_9mt` | 楚懷王 | [《史記・淮陰侯列傳》][74] | [JSON](jzx_qcd_9mt.json) |
| `k00_6q0_ths` | 徙木者 | [《史記・商君列傳》][50] | [JSON](k00_6q0_ths.json) |
| `k0h_8u3_zm7` | 介子推母（偕隱者） | [《史記・晉世家》][21] | [JSON](k0h_8u3_zm7.json) |
| `k0j_qxh_dti` | 韓姬 | [《史記・韓世家》][27] | [JSON](k0j_qxh_dti.json) |
| `k0p_up7_000` | 歩陽（韓原御者） | [《史記・晉世家》][21] | [JSON](k0p_up7_000.json) |
| `k12_clz_joc` | 陳豨 | [《史記・韓信盧綰列傳》][75] | [JSON](k12_clz_joc.json) |
| `k14_2gm_v9b` | 輒 | [《史記・仲尼弟子列傳》][49] | [JSON](k14_2gm_v9b.json) |
| `k19_j1k_5yo` | 昭公（燕宣公後） | [《史記・燕召公世家》][16] | [JSON](k19_j1k_5yo.json) |
| `k1h_vb6_4d2` | 虞仲 | [《史記・孔子世家》][29] | [JSON](k1h_vb6_4d2.json) |
| `k1p_er4_ei4` | 田榮 | [《史記・留侯世家》][37] | [JSON](k1p_er4_ei4.json) |
| `k1z_w9m_94t` | 李由 | [《史記・絳侯周勃世家》][39] | [JSON](k1z_w9m_94t.json) |
| `k21_yot_5tp` | 向壽 | [《史記・秦本紀》][5] | [JSON](k21_yot_5tp.json) |
| `k22_9pd_uu4` | 騶衍 | [《史記・孟子荀卿列傳》][56] | [JSON](k22_9pd_uu4.json) |
| `k2a_ash_121` | 羋戎 | [《史記・范睢蔡澤列傳》][61] | [JSON](k2a_ash_121.json) |
| `k2d_dp0_6dp` | 季友母（陳女未名） | [《史記・魯周公世家》][15] | [JSON](k2d_dp0_6dp.json) |
| `k2o_rtt_h2o` | 伊陟 | [《史記・殷本紀》][3] | [JSON](k2o_rtt_h2o.json) |
| `k2o_rv6_qyv` | 平原君 | [《史記・平原君虞卿列傳》][58] | [JSON](k2o_rv6_qyv.json) |
| `k2p_5ol_dwh` | 蒙驁 | [《史記・蒙恬列傳》][70] | [JSON](k2p_5ol_dwh.json) |
| `k2v_k0j_chh` | 城陽景王引稱待核 | [《史記・吳王濞列傳》][88] | [JSON](k2v_k0j_chh.json) |
| `k2v_rm5_7gw` | 祖乙 | [《史記・殷本紀》][3] | [JSON](k2v_rm5_7gw.json) |
| `k2w_1d2_5u5` | 趙孝成王 | [《史記・平原君虞卿列傳》][58] | [JSON](k2w_1d2_5u5.json) |
| `k31_jhi_wmb` | 榮如（鄋瞞記事） | [《史記・魯周公世家》][15] | [JSON](k31_jhi_wmb.json) |
| `k3g_1ud_spn` | 周女（晉成公母） | [《史記・晉世家》][21] | [JSON](k3g_1ud_spn.json) |
| `k41_zyq_5ik` | 子反 | [《史記・晉世家》][21] | [JSON](k41_zyq_5ik.json) |
| `k49_idc_dqx` | 秦襄公 | [《史記・楚世家》][22] | [JSON](k49_idc_dqx.json) |
| `k4b_0jv_rwa` | 祿（楚靈王太子） | [《史記・楚世家》][22] | [JSON](k4b_0jv_rwa.json) |
| `k4e_4tr_lg0` | 淮南厲王未詳名 | [《史記・酈生陸賈列傳》][79] | [JSON](k4e_4tr_lg0.json) |
| `k4e_7j3_ijr` | 楚靈王 | [《史記・楚世家》][22] | [JSON](k4e_7j3_ijr.json) |
| `k4r_wry_qcs` | 魏文子（請老辟克者） | [《史記・晉世家》][21] | [JSON](k4r_wry_qcs.json) |
| `k5g_3qk_0m4` | 申不害 | [《史記・老子韓非列傳》][45] | [JSON](k5g_3qk_0m4.json) |
| `k5j_rap_1cl` | 卜偃 | [《史記・魏世家》][26] | [JSON](k5j_rap_1cl.json) |
| `k62_9pj_sx2` | 徐君（季札訪問未名） | [《史記・吳太伯世家》][13] | [JSON](k62_9pj_sx2.json) |
| `k64_xyf_svi` | 顏淵 | [《史記・仲尼弟子列傳》][49] | [JSON](k64_xyf_svi.json) |
| `k6c_jbs_1gw` | 慶父（魯公子） | [《史記・魯周公世家》][15] | [JSON](k6c_jbs_1gw.json) |
| `k6e_9qv_u98` | 周武王 | [《史記・鄭世家》][24] | [JSON](k6e_9qv_u98.json) |
| `k6h_k25_ke7` | 公子職 | [《史記・趙世家》][25] | [JSON](k6h_k25_ke7.json) |
| `k7a_9ic_ynn` | 箕肆 | [《史記・絳侯周勃世家》][39] | [JSON](k7a_9ic_ynn.json) |
| `k7i_c3h_ssl` | 王賁 | [《史記・秦始皇本紀》][6] | [JSON](k7i_c3h_ssl.json) |
| `k7j_gr6_8nz` | 李信 | [《史記・白起王翦列傳》][55] | [JSON](k7j_gr6_8nz.json) |
| `k7m_99o_vv2` | 鄭伯（州吁伐鄭記事） | [《史記・衛康叔世家》][19] | [JSON](k7m_99o_vv2.json) |
| `k7t_lyq_qf2` | 張良 | [《史記・樊酈滕灌列傳》][77] | [JSON](k7t_lyq_qf2.json) |
| `k7x_gmp_ffr` | 伯翳 | [《史記・鄭世家》][24] | [JSON](k7x_gmp_ffr.json) |
| `k8d_2sn_e4f` | 唐雎 | [《史記・魏世家》][26] | [JSON](k8d_2sn_e4f.json) |
| `k8f_g8u_4xk` | 公子勝 | [《史記・趙世家》][25] | [JSON](k8f_g8u_4xk.json) |
| `k8n_rwt_70b` | 齊襄公 | [《史記・齊太公世家》][14] | [JSON](k8n_rwt_70b.json) |
| `k8p_ptb_xa1` | 武臣 | [《史記・張耳陳餘列傳》][71] | [JSON](k8p_ptb_xa1.json) |
| `k96_xfs_8qz` | 田既 | [《史記・曹相國世家》][36] | [JSON](k96_xfs_8qz.json) |
| `k9m_d4o_f34` | 程處 | [《史記・曹相國世家》][36] | [JSON](k9m_d4o_f34.json) |
| `ka5_rky_2fw` | 實沈 | [《史記・鄭世家》][24] | [JSON](ka5_rky_2fw.json) |
| `kab_d2z_04z` | 高皇帝（孔子世家祠孔未名者） | [《史記・孔子世家》][29] | [JSON](kab_d2z_04z.json) |
| `kb2_0cv_msr` | 左右閣都尉未名 | [《史記・扁鵲倉公列傳》][87] | [JSON](kb2_0cv_msr.json) |
| `kbh_40s_1r6` | 周最（賈生引文） | [《史記・秦始皇本紀》][6] | [JSON](kbh_40s_1r6.json) |
| `kbh_vr3_os9` | 曹無傷 | [《史記・項羽本紀》][7]、[《史記・高祖本紀》][8] | [JSON](kbh_vr3_os9.json) |
| `kc7_t2s_yot` | 倶酒（晉靜公） | [《史記・晉世家》][21] | [JSON](kc7_t2s_yot.json) |
| `kcm_epf_5gf` | 趙歇 | [《史記・張耳陳餘列傳》][71] | [JSON](kcm_epf_5gf.json) |
| `kcn_xi0_lu8` | 接子 | [《史記・孟子荀卿列傳》][56] | [JSON](kcn_xi0_lu8.json) |
| `kd7_n5o_quo` | 秦昭王 | [《史記・范睢蔡澤列傳》][61] | [JSON](kd7_n5o_quo.json) |
| `kdb_o6l_zgr` | 仲尼 | [《史記・孔子世家》][29] | [JSON](kdb_o6l_zgr.json) |
| `kdu_u61_y33` | 顏濁鄒 | [《史記・孔子世家》][29] | [JSON](kdu_u61_y33.json) |
| `kea_cx5_ey7` | 蒙嘉引古 | [《史記・刺客列傳》][68] | [JSON](kea_cx5_ey7.json) |
| `kei_2tq_702` | 靜（齊胡公） | [《史記・齊太公世家》][14] | [JSON](kei_2tq_702.json) |
| `kev_c6g_6me` | 邵滑 | [《史記・陳涉世家》][30] | [JSON](kev_c6g_6me.json) |
| `kez_re1_kcr` | 魏咎 | [《史記・秦始皇本紀》][6] | [JSON](kez_re1_kcr.json) |
| `kf1_6vh_y0w` | 秦靈公 | [《史記・魏世家》][26] | [JSON](kf1_6vh_y0w.json) |
| `kfg_ijy_wik` | 齊桓公 | [《史記・刺客列傳》][68] | [JSON](kfg_ijy_wik.json) |
| `kfh_9sk_v4e` | 田吸 | [《史記・田儋列傳》][76] | [JSON](kfh_9sk_v4e.json) |
| `kfj_bhr_cdz` | 祖甲 | [《史記・殷本紀》][3] | [JSON](kfj_bhr_cdz.json) |
| `kfu_u3t_85t` | 蘇意（故楚相） | [《史記・孝文本紀》][10] | [JSON](kfu_u3t_85t.json) |
| `kg1_doo_hgp` | 淳于越 | [《史記・秦始皇本紀》][6] | [JSON](kg1_doo_hgp.json) |
| `kg6_cm8_v76` | 丑（右宰） | [《史記・衛康叔世家》][19] | [JSON](kg6_cm8_v76.json) |
| `kgm_9od_w45` | 呂后 | [《史記・呂太后本紀》][9] | [JSON](kgm_9od_w45.json) |
| `kgo_dqk_ti0` | 去病 | [《史記・三王世家》][42] | [JSON](kgo_dqk_ti0.json) |
| `kh0_n9x_w13` | 趙成侯 | [《史記・魏世家》][26] | [JSON](kh0_n9x_w13.json) |
| `kh7_12u_kei` | 讙兜 | [《史記・五帝本紀》][1] | [JSON](kh7_12u_kei.json) |
| `kha_v9q_mku` | 子羽 | [《史記・留侯世家》][37] | [JSON](kha_v9q_mku.json) |
| `ki9_yjp_uo2` | 鄰人之父 | [《史記・老子韓非列傳》][45] | [JSON](ki9_yjp_uo2.json) |
| `kib_dnn_k5c` | 竇嬰 | [《史記・袁盎鼂錯列傳》][83] | [JSON](kib_dnn_k5c.json) |
| `kih_68x_38t` | 昭王 | [《史記・陳涉世家》][30] | [JSON](kih_68x_38t.json) |
| `kik_w6y_owb` | 毛遂 | [《史記・平原君虞卿列傳》][58] | [JSON](kik_w6y_owb.json) |
| `kil_ihw_kvb` | 武王 | [《史記・孔子世家》][29] | [JSON](kil_ihw_kvb.json) |
| `kiv_7ao_1e9` | 項梁 | [《史記・曹相國世家》][36] | [JSON](kiv_7ao_1e9.json) |
| `kk3_ifq_d3n` | 成陵君（魏世家未名者） | [《史記・魏世家》][26] | [JSON](kk3_ifq_d3n.json) |
| `kk7_tis_vis` | 伍子胥 | [《史記・越王勾踐世家》][23] | [JSON](kk7_tis_vis.json) |
| `kkh_3im_189` | 太史公 | [《史記・范睢蔡澤列傳》][61] | [JSON](kkh_3im_189.json) |
| `kkh_4au_tm8` | 魏王豹 | [《史記・留侯世家》][37] | [JSON](kkh_4au_tm8.json) |
| `kki_4ee_3i7` | 魯元 | [《史記・樊酈滕灌列傳》][77] | [JSON](kki_4ee_3i7.json) |
| `kkk_e2u_lm4` | 趙鞅 | [《史記・吳太伯世家》][13]、[《史記・齊太公世家》][14]、[《史記・燕召公世家》][16] | [JSON](kkk_e2u_lm4.json) |
| `kl1_9wf_nmq` | 孟姚 | [《史記・趙世家》][25] | [JSON](kl1_9wf_nmq.json) |
| `klu_n74_itc` | 榮聶政姊 | [《史記・刺客列傳》][68] | [JSON](klu_n74_itc.json) |
| `km2_zqy_p8q` | 越王句踐 | [《史記・仲尼弟子列傳》][49] | [JSON](km2_zqy_p8q.json) |
| `km5_8u3_9yt` | 陳平 | [《史記・淮陰侯列傳》][74] | [JSON](km5_8u3_9yt.json) |
| `km9_gzd_vly` | 南皮侯 | [《史記・絳侯周勃世家》][39] | [JSON](km9_gzd_vly.json) |
| `kmo_vp5_qe1` | 黃霸 | [《史記・張丞相列傳》][78] | [JSON](kmo_vp5_qe1.json) |
| `kmt_ukr_cid` | 筮史（趙世家夢占未名者） | [《史記・趙世家》][25] | [JSON](kmt_ukr_cid.json) |
| `kn3_k3k_rqr` | 呂不韋 | [《史記・樗里子甘茂列傳》][53] | [JSON](kn3_k3k_rqr.json) |
| `knn_gc3_gey` | 王離 | [《史記・張耳陳餘列傳》][71] | [JSON](knn_gc3_gey.json) |
| `knr_imw_ifj` | 鞠 | [《史記・周本紀》][4] | [JSON](knr_imw_ifj.json) |
| `knr_jfs_b93` | 趙武靈王 | [《史記・樂毅列傳》][62] | [JSON](knr_jfs_b93.json) |
| `knw_v4w_67q` | 公子赫 | [《史記・魏世家》][26] | [JSON](knw_v4w_67q.json) |
| `ko5_64e_ul3` | 畢萬（魏封邑） | [《史記・晉世家》][21] | [JSON](ko5_64e_ul3.json) |
| `kog_56u_1ip` | 韓不佞 | [《史記・趙世家》][25] | [JSON](kog_56u_1ip.json) |
| `kop_d5r_t5j` | 公孫昧 | [《史記・韓世家》][27] | [JSON](kop_d5r_t5j.json) |
| `koy_6jg_gcc` | 周勃 | [《史記・絳侯周勃世家》][39] | [JSON](koy_6jg_gcc.json) |
| `koz_25l_kwv` | 桃侯（項氏） | [《史記・項羽本紀》][7] | [JSON](koz_25l_kwv.json) |
| `kp0_vu0_i9h` | 垂 | [《史記・五帝本紀》][1] | [JSON](kp0_vu0_i9h.json) |
| `kpo_jte_1tu` | 白公引古未定 | [《史記・范睢蔡澤列傳》][61] | [JSON](kpo_jte_1tu.json) |
| `kpo_p95_52g` | 文王引古 | [《史記・平原君虞卿列傳》][58] | [JSON](kpo_p95_52g.json) |
| `kq7_8ds_8z7` | 盧綰 | [《史記・韓信盧綰列傳》][75] | [JSON](kq7_8ds_8z7.json) |
| `kq9_ezn_kth` | 力牧 | [《史記・五帝本紀》][1] | [JSON](kq9_ezn_kth.json) |
| `kqe_x0t_s25` | 蜀相壯 | [《史記・秦本紀》][5] | [JSON](kqe_x0t_s25.json) |
| `kr3_soq_kkq` | 暴捐 | [《史記・韓世家》][27] | [JSON](kr3_soq_kkq.json) |
| `kre_n61_feg` | 項嬰 | [《史記・淮陰侯列傳》][74] | [JSON](kre_n61_feg.json) |
| `krm_lrt_uca` | 昭王夫人（惠王藏身宮主未名） | [《史記・楚世家》][22] | [JSON](krm_lrt_uca.json) |
| `kru_906_knc` | 皇太后未名（文帝母語境） | [《史記・袁盎鼂錯列傳》][83] | [JSON](kru_906_knc.json) |
| `kry_3b2_phg` | 孔子 | [《史記・田敬仲完世家》][28] | [JSON](kry_3b2_phg.json) |
| `ktv_rwx_hp3` | 叔齊 | [《史記・伯夷列傳》][43] | [JSON](ktv_rwx_hp3.json) |
| `kvm_6zv_6ez` | 長公主 | [《史記・梁孝王世家》][40] | [JSON](kvm_6zv_6ez.json) |
| `kw9_rxv_wx3` | 叔孫輒 | [《史記・孔子世家》][29] | [JSON](kw9_rxv_wx3.json) |
| `kwa_ew6_bz3` | 衛桓公（楚篇弒君記事） | [《史記・楚世家》][22] | [JSON](kwa_ew6_bz3.json) |
| `kx9_xbq_xkd` | 繒賀 | [《史記・鄭世家》][24] | [JSON](kx9_xbq_xkd.json) |
| `kxl_a6t_r9a` | 劇孟母未名 | [《史記・袁盎鼂錯列傳》][83] | [JSON](kxl_a6t_r9a.json) |
| `kxp_dd5_h1g` | 程嬰 | [《史記・趙世家》][25] | [JSON](kxp_dd5_h1g.json) |
| `kxp_iel_l8n` | 曹圉 | [《史記・殷本紀》][3] | [JSON](kxp_iel_l8n.json) |
| `kxs_sv8_cbe` | 周聚 | [《史記・周本紀》][4] | [JSON](kxs_sv8_cbe.json) |
| `kxu_u93_88u` | 白起 | [《史記・白起王翦列傳》][55] | [JSON](kxu_u93_88u.json) |
| `kxz_6nu_h9u` | 猗頓 | [《史記・秦始皇本紀》][6] | [JSON](kxz_6nu_h9u.json) |
| `ky4_4k8_gjt` | 呂后 | [《史記・呂太后本紀》][9] | [JSON](ky4_4k8_gjt.json) |
| `ky5_nbu_cy2` | 后稷（孔子世家詩傳說） | [《史記・孔子世家》][29] | [JSON](ky5_nbu_cy2.json) |
| `kyh_08w_h4c` | 參（文帝子） | [《史記・孝文本紀》][10] | [JSON](kyh_08w_h4c.json) |
| `kyr_zck_x9u` | 原亢籍 | [《史記・仲尼弟子列傳》][49] | [JSON](kyr_zck_x9u.json) |
| `kzd_kqm_kjw` | 秦武王 | [《史記・趙世家》][25] | [JSON](kzd_kqm_kjw.json) |
| `kzp_s69_eh7` | 臧荼 | [《史記・張丞相列傳》][78] | [JSON](kzp_s69_eh7.json) |
| `kzr_urm_0fr` | 榮夷公 | [《史記・周本紀》][4] | [JSON](kzr_urm_0fr.json) |
| `kzu_rlu_w1o` | 乘馬絺 | [《史記・絳侯周勃世家》][39] | [JSON](kzu_rlu_w1o.json) |
| `kzv_cms_thu` | 郤克 | [《史記・韓世家》][27] | [JSON](kzv_cms_thu.json) |
| `kzy_ysk_775` | 神農 | [《史記・伯夷列傳》][43] | [JSON](kzy_ysk_775.json) |
| `l03_ht7_wwy` | 田單 | [《史記・田單列傳》][64] | [JSON](l03_ht7_wwy.json) |
| `l0i_j1y_txo` | 吳王僚 | [《史記・吳太伯世家》][13] | [JSON](l0i_j1y_txo.json) |
| `l0n_tbg_bml` | 子陽（鄭所殺者） | [《史記・楚世家》][22] | [JSON](l0n_tbg_bml.json) |
| `l0r_u7m_5kx` | 項羽 | [《史記・白起王翦列傳》][55] | [JSON](l0r_u7m_5kx.json) |
| `l1c_4cu_vc3` | 懿子 | [《史記・孔子世家》][29] | [JSON](l1c_4cu_vc3.json) |
| `l1q_uxi_bn7` | 鷄鳴客未名 | [《史記・孟嘗君列傳》][57] | [JSON](l1q_uxi_bn7.json) |
| `l1v_yo7_of0` | 知伯 | [《史記・趙世家》][25] | [JSON](l1v_yo7_of0.json) |
| `l1x_fpj_80w` | 代王嘉 | [《史記・刺客列傳》][68] | [JSON](l1x_fpj_80w.json) |
| `l24_c0r_qj2` | 扈輒 | [《史記・趙世家》][25] | [JSON](l24_c0r_qj2.json) |
| `l2j_rm8_h4z` | 秦昭王 | [《史記・范睢蔡澤列傳》][61] | [JSON](l2j_rm8_h4z.json) |
| `l2k_zrx_xfr` | 濟北王未詳名 | [《史記・樊酈滕灌列傳》][77] | [JSON](l2k_zrx_xfr.json) |
| `l2m_bae_5ox` | 簡公引古未定 | [《史記・李斯列傳》][69] | [JSON](l2m_bae_5ox.json) |
| `l34_njn_6uw` | 臧荼 | [《史記・高祖本紀》][8] | [JSON](l34_njn_6uw.json) |
| `l3n_6lt_37x` | 尾生 | [《史記・蘇秦列傳》][51] | [JSON](l3n_6lt_37x.json) |
| `l3w_spq_7qn` | 蘇秦 | [《史記・張儀列傳》][52] | [JSON](l3w_spq_7qn.json) |
| `l3x_dtn_i0u` | 李良 | [《史記・張耳陳餘列傳》][71] | [JSON](l3x_dtn_i0u.json) |
| `l44_3nw_9xe` | 魯使（齊頃宴使未名） | [《史記・晉世家》][21] | [JSON](l44_3nw_9xe.json) |
| `l4l_iz8_ao0` | 岐伯 | [《史記・孝武本紀》][12] | [JSON](l4l_iz8_ao0.json) |
| `l5c_h8i_d5q` | 衛子夫 | [《史記・外戚世家》][31] | [JSON](l5c_h8i_d5q.json) |
| `l5h_vix_jn2` | 莊舄 | [《史記・張儀列傳》][52] | [JSON](l5h_vix_jn2.json) |
| `l6c_cnc_j51` | 楚元王 | [《史記・三王世家》][42] | [JSON](l6c_cnc_j51.json) |
| `l6d_hvp_ot3` | 泗川守壯 | [《史記・高祖本紀》][8] | [JSON](l6d_hvp_ot3.json) |
| `l6g_8h9_eq0` | 太史公 | [《史記・司馬穰苴列傳》][46] | [JSON](l6g_8h9_eq0.json) |
| `l6g_or1_wuv` | 趙孝成王 | [《史記・平原君虞卿列傳》][58] | [JSON](l6g_or1_wuv.json) |
| `l6o_aeo_qrf` | 穰侯 | [《史記・蘇秦列傳》][51] | [JSON](l6o_aeo_qrf.json) |
| `l7w_xfi_scd` | 張相如 | [《史記・張釋之馮唐列傳》][84] | [JSON](l7w_xfi_scd.json) |
| `l7z_yra_bbp` | 昭夫人 | [《史記・伍子胥列傳》][48] | [JSON](l7z_yra_bbp.json) |
| `l80_d6q_mss` | 沛公 | [《史記・秦始皇本紀》][6] | [JSON](l80_d6q_mss.json) |
| `l87_n9v_y0p` | 太史噭引古 | [《史記・范睢蔡澤列傳》][61] | [JSON](l87_n9v_y0p.json) |
| `l8e_aho_h3v` | 嬰（太僕） | [《史記・孝文本紀》][10] | [JSON](l8e_aho_h3v.json) |
| `l8u_dr5_a97` | 丙戎 | [《史記・齊太公世家》][14] | [JSON](l8u_dr5_a97.json) |
| `l9e_fbr_36a` | 倉 | [《史記・韓世家》][27] | [JSON](l9e_fbr_36a.json) |
| `l9s_24a_7a3` | 趙括 | [《史記・白起王翦列傳》][55] | [JSON](l9s_24a_7a3.json) |
| `l9t_94i_2xm` | 郄（晉鄂侯） | [《史記・晉世家》][21] | [JSON](l9t_94i_2xm.json) |
| `l9w_b0y_aow` | 吳王濞 | [《史記・齊悼惠王世家》][34] | [JSON](l9w_b0y_aow.json) |
| `l9w_xva_6q0` | 霍公（趙世家未名者） | [《史記・趙世家》][25] | [JSON](l9w_xva_6q0.json) |
| `la6_9zc_6gy` | 栗腹 | [《史記・趙世家》][25] | [JSON](la6_9zc_6gy.json) |
| `lap_qc0_yqm` | 呂不韋姬（始皇生母） | [《史記・秦始皇本紀》][6] | [JSON](lap_qc0_yqm.json) |
| `lb8_4u3_h91` | 燕王（趙世家會趙未名者） | [《史記・趙世家》][25] | [JSON](lb8_4u3_h91.json) |
| `lb9_zwn_ril` | 魏文侯 | [《史記・韓世家》][27] | [JSON](lb9_zwn_ril.json) |
| `lbi_h7e_uq1` | 趙子兒 | [《史記・外戚世家》][31] | [JSON](lbi_h7e_uq1.json) |
| `lbj_a32_053` | 兒姁 | [《史記・外戚世家》][31] | [JSON](lbj_a32_053.json) |
| `lbk_uyq_t6e` | 英布 | [《史記・吳王濞列傳》][88] | [JSON](lbk_uyq_t6e.json) |
| `lbn_xjh_jgq` | 齊景公 | [《史記・趙世家》][25] | [JSON](lbn_xjh_jgq.json) |
| `lc0_4na_98y` | 張耳妻前夫未名 | [《史記・張耳陳餘列傳》][71] | [JSON](lc0_4na_98y.json) |
| `lc3_4nk_w3x` | 孝明皇帝（附載稱呼） | [《史記・秦始皇本紀》][6] | [JSON](lc3_4nk_w3x.json) |
| `lc5_if4_4x7` | 晏嬰 | [《史記・孔子世家》][29] | [JSON](lc5_if4_4x7.json) |
| `lco_j4z_fyv` | 應侯甘羅引古 | [《史記・樗里子甘茂列傳》][53] | [JSON](lco_j4z_fyv.json) |
| `lcu_lvw_vlk` | 子臧 | [《史記・吳太伯世家》][13] | [JSON](lcu_lvw_vlk.json) |
| `lcy_pp7_2tl` | 成王 | [《史記・梁孝王世家》][40] | [JSON](lcy_pp7_2tl.json) |
| `ld0_ysw_559` | 楚懷王 | [《史記・田儋列傳》][76] | [JSON](ld0_ysw_559.json) |
| `ld5_szi_vvn` | 嫪毐 | [《史記・呂不韋列傳》][67] | [JSON](ld5_szi_vvn.json) |
| `ldc_zat_qlt` | 荀櫟 | [《史記・趙世家》][25] | [JSON](ldc_zat_qlt.json) |
| `le1_189_mdi` | 裏克 | [《史記・鄭世家》][24] | [JSON](le1_189_mdi.json) |
| `le6_hlz_o1r` | 隨侯（楚武王伐隨時未名） | [《史記・楚世家》][22] | [JSON](le6_hlz_o1r.json) |
| `le8_eqh_ry0` | 夫子引言 | [《史記・孟子荀卿列傳》][56] | [JSON](le8_eqh_ry0.json) |
| `lef_ipu_r6b` | 夏姬 | [《史記・呂不韋列傳》][67] | [JSON](lef_ipu_r6b.json) |
| `leg_wk9_nkl` | 晉景公 | [《史記・鄭世家》][24] | [JSON](leg_wk9_nkl.json) |
| `lfk_aka_wnj` | 呂禮 | [《史記・秦本紀》][5] | [JSON](lfk_aka_wnj.json) |
| `lfp_pwy_rym` | 屈宜臼 | [《史記・韓世家》][27] | [JSON](lfp_pwy_rym.json) |
| `lfr_3b7_zf5` | 太史公 | [《史記・劉敬叔孫通列傳》][81] | [JSON](lfr_3b7_zf5.json) |
| `lg2_cqw_2hr` | 劇子 | [《史記・孟子荀卿列傳》][56] | [JSON](lg2_cqw_2hr.json) |
| `lg9_ysv_5h9` | 太史公 | [《史記・廉頗藺相如列傳》][63] | [JSON](lg9_ysv_5h9.json) |
| `lgb_gdh_ej5` | 葉公（攻白公者） | [《史記・陳杞世家》][18] | [JSON](lgb_gdh_ej5.json) |
| `lgg_491_wsg` | 大陸子方 | [《史記・齊太公世家》][14] | [JSON](lgg_491_wsg.json) |
| `lgm_7uk_8u5` | 周王赧（楚篇圖周時） | [《史記・楚世家》][22] | [JSON](lgm_7uk_8u5.json) |
| `lgo_cwi_085` | 公孫卿 | [《史記・孝武本紀》][12] | [JSON](lgo_cwi_085.json) |
| `lh3_8d0_lz0` | 去疾 | [《史記・鄭世家》][24] | [JSON](lh3_8d0_lz0.json) |
| `lha_b29_fa5` | 春申君 | [《史記・春申君列傳》][60] | [JSON](lha_b29_fa5.json) |
| `lhy_fkp_0h5` | 晉君（趙世家端氏屯留未名者） | [《史記・趙世家》][25] | [JSON](lhy_fkp_0h5.json) |
| `li0_ez8_1y0` | 張耳 | [《史記・張耳陳餘列傳》][71] | [JSON](li0_ez8_1y0.json) |
| `li0_tpv_g5x` | 周蘭 | [《史記・樊酈滕灌列傳》][77] | [JSON](li0_tpv_g5x.json) |
| `li9_cmb_8ci` | 滕公（本卷稱呼） | [《史記・樊酈滕灌列傳》][77] | [JSON](li9_cmb_8ci.json) |
| `lia_4xf_gye` | 景缺（楚將軍） | [《史記・秦本紀》][5]、[《史記・楚世家》][22] | [JSON](lia_4xf_gye.json) |
| `lid_w64_29w` | 申生姊（秦繆公夫人） | [《史記・晉世家》][21] | [JSON](lid_w64_29w.json) |
| `lin_xy2_4my` | 曲宮 | [《史記・蒙恬列傳》][70] | [JSON](lin_xy2_4my.json) |
| `lit_x7f_ld0` | 周氏未名（濮陽） | [《史記・季布欒布列傳》][82] | [JSON](lit_x7f_ld0.json) |
| `lj3_icg_1ft` | 召公 | [《史記・燕召公世家》][16] | [JSON](lj3_icg_1ft.json) |
| `lje_891_3sg` | 昭王四十年死太子未名 | [《史記・呂不韋列傳》][67] | [JSON](lje_891_3sg.json) |
| `ljo_u20_bkf` | 司馬錯 | [《史記・秦本紀》][5] | [JSON](ljo_u20_bkf.json) |
| `ljt_md6_814` | 徐厲 | [《史記・絳侯周勃世家》][39] | [JSON](ljt_md6_814.json) |
| `llf_tvb_j2l` | 伍子胥 | [《史記・季布欒布列傳》][82] | [JSON](llf_tvb_j2l.json) |
| `llx_tny_k7q` | 孔子 | [《史記・伍子胥列傳》][48] | [JSON](llx_tny_k7q.json) |
| `llz_pjb_0um` | 陳豨 | [《史記・蕭相國世家》][35] | [JSON](llz_pjb_0um.json) |
| `lmf_7u1_w81` | 趙王歇 | [《史記・秦始皇本紀》][6] | [JSON](lmf_7u1_w81.json) |
| `ln0_7gp_jh7` | 蘇駔 | [《史記・樊酈滕灌列傳》][77] | [JSON](ln0_7gp_jh7.json) |
| `lny_vft_7kt` | 蔡賜 | [《史記・陳涉世家》][30] | [JSON](lny_vft_7kt.json) |
| `lp3_npi_io0` | 韓信 | [《史記・田儋列傳》][76] | [JSON](lp3_npi_io0.json) |
| `lpb_qw7_82d` | 公孫賈 | [《史記・商君列傳》][50] | [JSON](lpb_qw7_82d.json) |
| `lpm_cci_4wd` | 所忠 | [《史記・萬石張叔列傳》][85] | [JSON](lpm_cci_4wd.json) |
| `lpu_67y_ydz` | 張良 | [《史記・淮陰侯列傳》][74] | [JSON](lpu_67y_ydz.json) |
| `lqh_592_x11` | 郤宛（費無忌所害者） | [《史記・楚世家》][22] | [JSON](lqh_592_x11.json) |
| `lqh_jlr_dl6` | 河上丈人 | [《史記・樂毅列傳》][62] | [JSON](lqh_jlr_dl6.json) |
| `lqk_1q1_r7h` | 瞽瞍（陳篇世系引語） | [《史記・陳杞世家》][18] | [JSON](lqk_1q1_r7h.json) |
| `lqk_mfk_vv9` | 康王后（樂成侯姊） | [《史記・孝武本紀》][12] | [JSON](lqk_mfk_vv9.json) |
| `lrj_utu_y6w` | 平原君趙勝 | [《史記・平原君虞卿列傳》][58] | [JSON](lrj_utu_y6w.json) |
| `lrl_ml0_321` | 周生（太史公所引） | [《史記・項羽本紀》][7] | [JSON](lrl_ml0_321.json) |
| `ls3_l6g_l7d` | 傅說引古 | [《史記・屈原賈生列傳》][66] | [JSON](ls3_l6g_l7d.json) |
| `lsb_qr2_i3q` | 胡亥客奉偽書未名 | [《史記・李斯列傳》][69] | [JSON](lsb_qr2_i3q.json) |
| `lse_2ct_dsn` | 九侯之女 | [《史記・殷本紀》][3] | [JSON](lse_2ct_dsn.json) |
| `lse_ja5_xl8` | 太史子餘 | [《史記・田敬仲完世家》][28] | [JSON](lse_ja5_xl8.json) |
| `lso_17e_oj8` | 二世（陳涉世家未名者） | [《史記・陳涉世家》][30] | [JSON](lso_17e_oj8.json) |
| `lt5_gcv_iqh` | 宣王 | [《史記・周本紀》][4] | [JSON](lt5_gcv_iqh.json) |
| `ltd_gf0_3zt` | 大夫種引古 | [《史記・范睢蔡澤列傳》][61] | [JSON](ltd_gf0_3zt.json) |
| `ltg_z7u_vhb` | 張良弟（留侯世家未名者） | [《史記・留侯世家》][37] | [JSON](ltg_z7u_vhb.json) |
| `ltn_go2_3eu` | 遠吏故事妾 | [《史記・蘇秦列傳》][51] | [JSON](ltn_go2_3eu.json) |
| `ltv_hb9_iam` | 猗頓 | [《史記・陳涉世家》][30] | [JSON](ltv_hb9_iam.json) |
| `lu3_ob9_3ri` | 白起 | [《史記・廉頗藺相如列傳》][63] | [JSON](lu3_ob9_3ri.json) |
| `lue_xus_em2` | 公甫文伯 | [《史記・平原君虞卿列傳》][58] | [JSON](lue_xus_em2.json) |
| `lui_r6i_tzm` | 東牟侯未詳名 | [《史記・樊酈滕灌列傳》][77] | [JSON](lui_r6i_tzm.json) |
| `lvy_0pn_yfg` | 熊渠（楚先祖） | [《史記・楚世家》][22] | [JSON](lvy_0pn_yfg.json) |
| `lwc_kea_ype` | 劉郢 | [《史記・孝文本紀》][10] | [JSON](lwc_kea_ype.json) |
| `lwe_fv2_m9g` | 劉濞 | [《史記・荊燕世家》][33] | [JSON](lwe_fv2_m9g.json) |
| `lwf_jb1_olp` | 邴歜（衛篇弒齊君記事） | [《史記・衛康叔世家》][19] | [JSON](lwf_jb1_olp.json) |
| `lwg_ae8_iku` | 鄧宗 | [《史記・陳涉世家》][30] | [JSON](lwg_ae8_iku.json) |
| `lwi_cje_46s` | 假神師卒未名 | [《史記・田單列傳》][64] | [JSON](lwi_cje_46s.json) |
| `lwi_l3d_a1t` | 周蘭 | [《史記・曹相國世家》][36] | [JSON](lwi_l3d_a1t.json) |
| `lwt_p4c_rd4` | 趙將莊 | [《史記・秦本紀》][5] | [JSON](lwt_p4c_rd4.json) |
| `lwx_fc0_0ce` | 李由 | [《史記・樊酈滕灌列傳》][77] | [JSON](lwx_fc0_0ce.json) |
| `lx4_rdl_gjt` | 梁鱣 | [《史記・仲尼弟子列傳》][49] | [JSON](lx4_rdl_gjt.json) |
| `lxk_xeh_f6r` | 張唐 | [《史記・樗里子甘茂列傳》][53] | [JSON](lxk_xeh_f6r.json) |
| `lxm_ezo_k4h` | 季平子（魯卿） | [《史記・魯周公世家》][15] | [JSON](lxm_ezo_k4h.json) |
| `lxx_qu4_p2d` | 秦昭王 | [《史記・范睢蔡澤列傳》][61] | [JSON](lxx_qu4_p2d.json) |
| `lyc_370_iba` | 賈子 | [《史記・伯夷列傳》][43] | [JSON](lyc_370_iba.json) |
| `lyd_084_byc` | 荊軻（引古） | [《史記・蒙恬列傳》][70] | [JSON](lyd_084_byc.json) |
| `lyd_90b_jn8` | 鄭子産（楚篇申會者） | [《史記・楚世家》][22] | [JSON](lyd_90b_jn8.json) |
| `lyd_jqi_yke` | 百里奚 | [《史記・老子韓非列傳》][45] | [JSON](lyd_jqi_yke.json) |
| `lyq_p1r_87n` | 賈夫人 | [《史記・五宗世家》][41] | [JSON](lyq_p1r_87n.json) |
| `lz2_9j4_p17` | 平原（四君稱呼） | [《史記・秦始皇本紀》][6] | [JSON](lz2_9j4_p17.json) |
| `lzo_8qz_eqd` | 司馬翦 | [《史記・周本紀》][4] | [JSON](lzo_8qz_eqd.json) |
| `lzo_cxh_egc` | 盜跖引古 | [《史記・李斯列傳》][69] | [JSON](lzo_cxh_egc.json) |
| `m0d_n8x_pj8` | 趙同 | [《史記・季布欒布列傳》][82] | [JSON](m0d_n8x_pj8.json) |
| `m0l_71n_b8f` | 仲姬（牙母） | [《史記・齊太公世家》][14] | [JSON](m0l_71n_b8f.json) |
| `m0s_giw_1h6` | 衛先生引古未定 | [《史記・魯仲連鄒陽列傳》][65] | [JSON](m0s_giw_1h6.json) |
| `m12_4ic_ro1` | 趙禹 | [《史記・趙世家》][25] | [JSON](m12_4ic_ro1.json) |
| `m18_nz2_htj` | 袁盎 | [《史記・袁盎鼂錯列傳》][83] | [JSON](m18_nz2_htj.json) |
| `m1q_tly_ucl` | 魏章 | [《史記・樗里子甘茂列傳》][53] | [JSON](m1q_tly_ucl.json) |
| `m1w_i0t_0na` | 五大夫賁 | [《史記・秦本紀》][5] | [JSON](m1w_i0t_0na.json) |
| `m2i_2sv_ioc` | 堯（引古） | [《史記・淮陰侯列傳》][74] | [JSON](m2i_2sv_ioc.json) |
| `m2o_06w_br9` | 公孫季功 | [《史記・刺客列傳》][68] | [JSON](m2o_06w_br9.json) |
| `m2o_ydx_9ap` | 任鄙 | [《史記・樗里子甘茂列傳》][53] | [JSON](m2o_ydx_9ap.json) |
| `m39_fok_wwo` | 魯君 | [《史記・孫子吳起列傳》][47] | [JSON](m39_fok_wwo.json) |
| `m3d_h2d_hni` | 新城三老董公 | [《史記・高祖本紀》][8] | [JSON](m3d_h2d_hni.json) |
| `m3x_qqp_18q` | 佛肸 | [《史記・孔子世家》][29] | [JSON](m3x_qqp_18q.json) |
| `m5g_nw3_pnt` | 范蠡 | [《史記・田叔列傳》][86] | [JSON](m5g_nw3_pnt.json) |
| `m5o_zsd_7jg` | 黥布 | [《史記・陳丞相世家》][38] | [JSON](m5o_zsd_7jg.json) |
| `m68_ewg_gly` | 黥布 | [《史記・酈生陸賈列傳》][79] | [JSON](m68_ewg_gly.json) |
| `m6b_39t_lpp` | 嚴君疾 | [《史記・秦本紀》][5] | [JSON](m6b_39t_lpp.json) |
| `m6w_e7i_lf7` | 牢 | [《史記・孔子世家》][29] | [JSON](m6w_e7i_lf7.json) |
| `m77_8py_m63` | 后處 | [《史記・仲尼弟子列傳》][49] | [JSON](m77_8py_m63.json) |
| `m77_em2_28k` | 重華引古 | [《史記・屈原賈生列傳》][66] | [JSON](m77_em2_28k.json) |
| `m77_uww_q13` | 齊威王引古 | [《史記・魯仲連鄒陽列傳》][65] | [JSON](m77_uww_q13.json) |
| `m83_eix_1n6` | 由余 | [《史記・商君列傳》][50] | [JSON](m83_eix_1n6.json) |
| `m8o_g61_go9` | 司馬夷 | [《史記・高祖本紀》][8] | [JSON](m8o_g61_go9.json) |
| `m8t_rxr_0s8` | 鄒忌 | [《史記・孟嘗君列傳》][57] | [JSON](m8t_rxr_0s8.json) |
| `m8w_63c_963` | 內史繇 | [《史記・扁鵲倉公列傳》][87] | [JSON](m8w_63c_963.json) |
| `m9h_fg1_y58` | 駔（荼異母兄） | [《史記・齊太公世家》][14] | [JSON](m9h_fg1_y58.json) |
| `m9l_x8u_wbq` | 放齊 | [《史記・五帝本紀》][1] | [JSON](m9l_x8u_wbq.json) |
| `m9r_3qk_l9z` | 戾（叔孫氏臣） | [《史記・魯周公世家》][15] | [JSON](m9r_3qk_l9z.json) |
| `mag_1sz_m8r` | 武丁引古 | [《史記・屈原賈生列傳》][66] | [JSON](mag_1sz_m8r.json) |
| `mag_s6n_b0c` | 廉頗 | [《史記・張釋之馮唐列傳》][84] | [JSON](mag_s6n_b0c.json) |
| `man_e6c_86g` | 嚭 | [《史記・吳太伯世家》][13] | [JSON](man_e6c_86g.json) |
| `map_u36_hry` | 唐八子 | [《史記・秦本紀》][5] | [JSON](map_u36_hry.json) |
| `mb1_jy6_k0x` | 周亞夫 | [《史記・張釋之馮唐列傳》][84] | [JSON](mb1_jy6_k0x.json) |
| `mc2_05b_5i5` | 晏子御者 | [《史記・管晏列傳》][44] | [JSON](mc2_05b_5i5.json) |
| `mc5_j8c_0oc` | 子輿 | [《史記・趙世家》][25] | [JSON](mc5_j8c_0oc.json) |
| `mc8_pmt_w8i` | 漆雕哆 | [《史記・仲尼弟子列傳》][49] | [JSON](mc8_pmt_w8i.json) |
| `mcm_2ok_nqa` | 崔杼 | [《史記・范睢蔡澤列傳》][61] | [JSON](mcm_2ok_nqa.json) |
| `mcx_6iv_rgc` | 嘉（周子南君） | [《史記・周本紀》][4] | [JSON](mcx_6iv_rgc.json) |
| `mcx_uqw_9lx` | 少帝未詳名 | [《史記・樊酈滕灌列傳》][77] | [JSON](mcx_uqw_9lx.json) |
| `mcy_59c_udi` | 隨何 | [《史記・黥布列傳》][73] | [JSON](mcy_59c_udi.json) |
| `mdf_bwd_v6b` | 雍糾 | [《史記・鄭世家》][24] | [JSON](mdf_bwd_v6b.json) |
| `mdg_x1d_buj` | 司馬耕 | [《史記・仲尼弟子列傳》][49] | [JSON](mdg_x1d_buj.json) |
| `mdk_l9p_342` | 桑距 | [《史記・五宗世家》][41] | [JSON](mdk_l9p_342.json) |
| `me7_83c_74z` | 樓煩（本卷稱呼） | [《史記・項羽本紀》][7] | [JSON](me7_83c_74z.json) |
| `mev_r3x_fuu` | 欒書 | [《史記・鄭世家》][24] | [JSON](mev_r3x_fuu.json) |
| `mex_tig_16z` | 蓋聶 | [《史記・刺客列傳》][68] | [JSON](mex_tig_16z.json) |
| `mf2_tm7_f9r` | 秦孝公 | [《史記・田敬仲完世家》][28] | [JSON](mf2_tm7_f9r.json) |
| `mfd_hor_95c` | 楚王信 | [《史記・傅靳蒯成列傳》][80] | [JSON](mfd_hor_95c.json) |
| `mfu_22v_exx` | 趙穿 | [《史記・鄭世家》][24] | [JSON](mfu_22v_exx.json) |
| `mgj_ry7_2x5` | 陶朱 | [《史記・陳涉世家》][30] | [JSON](mgj_ry7_2x5.json) |
| `mgl_q57_d7h` | 樊市人弟未名 | [《史記・樊酈滕灌列傳》][77] | [JSON](mgl_q57_d7h.json) |
| `mh6_5un_rq0` | 韓康子（殺知伯者） | [《史記・晉世家》][21] | [JSON](mh6_5un_rq0.json) |
| `mih_1jq_cr4` | 李牧（引古） | [《史記・蒙恬列傳》][70] | [JSON](mih_1jq_cr4.json) |
| `mih_vxs_rhx` | 高后 | [《史記・田叔列傳》][86] | [JSON](mih_vxs_rhx.json) |
| `mii_pxr_jrl` | 破石 | [《史記・扁鵲倉公列傳》][87] | [JSON](mii_pxr_jrl.json) |
| `mio_z5f_ri1` | 楚威王 | [《史記・蘇秦列傳》][51] | [JSON](mio_z5f_ri1.json) |
| `mj1_mir_ncl` | 昌（成弟） | [《史記・扁鵲倉公列傳》][87] | [JSON](mj1_mir_ncl.json) |
| `mj4_uma_km7` | 陳皇后 | [《史記・外戚世家》][31] | [JSON](mj4_uma_km7.json) |
| `mjm_mzj_yye` | 召平 | [《史記・齊悼惠王世家》][34] | [JSON](mjm_mzj_yye.json) |
| `mjn_ohc_9ca` | 漢皇太后 | [《史記・齊悼惠王世家》][34] | [JSON](mjn_ohc_9ca.json) |
| `mjq_bhc_w7f` | 涇陽君 | [《史記・范睢蔡澤列傳》][61] | [JSON](mjq_bhc_w7f.json) |
| `mjy_lip_a2o` | 藺相如 | [《史記・廉頗藺相如列傳》][63] | [JSON](mjy_lip_a2o.json) |
| `mky_p42_opm` | 呂臣 | [《史記・陳涉世家》][30] | [JSON](mky_p42_opm.json) |
| `mlk_3li_pp1` | 慶 | [《史記・三王世家》][42] | [JSON](mlk_3li_pp1.json) |
| `mll_3xo_v71` | 彭生 | [《史記・魯周公世家》][15] | [JSON](mll_3xo_v71.json) |
| `mlm_125_vha` | 丞非 | [《史記・三王世家》][42] | [JSON](mlm_125_vha.json) |
| `mly_cgz_aoz` | 章平 | [《史記・曹相國世家》][36] | [JSON](mly_cgz_aoz.json) |
| `mmc_e8p_5pf` | 玄武侯（項氏） | [《史記・項羽本紀》][7] | [JSON](mmc_e8p_5pf.json) |
| `mn3_4ru_eqc` | 角里先生 | [《史記・留侯世家》][37] | [JSON](mn3_4ru_eqc.json) |
| `mn6_y66_bl2` | 博士安 | [《史記・三王世家》][42] | [JSON](mn6_y66_bl2.json) |
| `mnl_60k_4y2` | 酈將軍（高祖發喪敘事） | [《史記・高祖本紀》][8] | [JSON](mnl_60k_4y2.json) |
| `mnl_vz0_79n` | 黃帝 | [《史記・趙世家》][25] | [JSON](mnl_vz0_79n.json) |
| `mnr_5w1_lyn` | 晉襄公引文候選 | [《史記・扁鵲倉公列傳》][87] | [JSON](mnr_5w1_lyn.json) |
| `mo4_tlr_3fh` | 尹佚 | [《史記・周本紀》][4] | [JSON](mo4_tlr_3fh.json) |
| `mp8_xcr_ihc` | 威壘 | [《史記・秦本紀》][5] | [JSON](mp8_xcr_ihc.json) |
| `mpf_qq9_bqk` | 突（鄭君） | [《史記・宋微子世家》][20] | [JSON](mpf_qq9_bqk.json) |
| `mpg_17j_5jq` | 蘇秦 | [《史記・陳涉世家》][30] | [JSON](mpg_17j_5jq.json) |
| `mpt_e3b_qvf` | 蕭公角 | [《史記・項羽本紀》][7] | [JSON](mpt_e3b_qvf.json) |
| `mpz_80p_uhj` | 楚平王 | [《史記・季布欒布列傳》][82] | [JSON](mpz_80p_uhj.json) |
| `mq3_lev_w2t` | 桀 | [《史記・劉敬叔孫通列傳》][81] | [JSON](mq3_lev_w2t.json) |
| `mq6_9sx_400` | 惠文后 | [《史記・秦本紀》][5] | [JSON](mq6_9sx_400.json) |
| `mqe_4d4_d1l` | 永巷長未名 | [《史記・扁鵲倉公列傳》][87] | [JSON](mqe_4d4_d1l.json) |
| `mqr_hfc_bzm` | 趙鞅 | [《史記・孔子世家》][29] | [JSON](mqr_hfc_bzm.json) |
| `mqt_zhu_byy` | 言偃 | [《史記・仲尼弟子列傳》][49] | [JSON](mqt_zhu_byy.json) |
| `mqw_09p_4c8` | 薄誘忌 | [《史記・孝武本紀》][12] | [JSON](mqw_09p_4c8.json) |
| `mrj_1jl_2tk` | 呂后 | [《史記・樊酈滕灌列傳》][77] | [JSON](mrj_1jl_2tk.json) |
| `mrk_rv8_zvi` | 屈丐 | [《史記・樗里子甘茂列傳》][53] | [JSON](mrk_rv8_zvi.json) |
| `mrt_kzm_qze` | 秦穆公引古 | [《史記・李斯列傳》][69] | [JSON](mrt_kzm_qze.json) |
| `msf_ogd_cah` | 平（晉孝侯） | [《史記・晉世家》][21] | [JSON](msf_ogd_cah.json) |
| `msp_sfc_drj` | 黥布 | [《史記・淮陰侯列傳》][74] | [JSON](msp_sfc_drj.json) |
| `msv_9r0_wtk` | 趙襄子 | [《史記・韓世家》][27] | [JSON](msv_9r0_wtk.json) |
| `mt4_h3l_bbn` | 齊王蘇代過魏 | [《史記・蘇秦列傳》][51] | [JSON](mt4_h3l_bbn.json) |
| `mtd_ixv_feg` | 呂不韋 | [《史記・呂不韋列傳》][67] | [JSON](mtd_ixv_feg.json) |
| `mtx_qs1_a5q` | 孝惠帝 | [《史記・齊悼惠王世家》][34] | [JSON](mtx_qs1_a5q.json) |
| `mua_01m_5ng` | 齊宗女（重耳妻） | [《史記・晉世家》][21] | [JSON](mua_01m_5ng.json) |
| `muc_6xp_2ap` | 楚王（韓世家雍氏議論未名者） | [《史記・韓世家》][27] | [JSON](muc_6xp_2ap.json) |
| `muq_vzr_tlr` | 蘇代 | [《史記・穰侯列傳》][54] | [JSON](muq_vzr_tlr.json) |
| `mvb_r8o_83y` | 葛嬰 | [《史記・陳涉世家》][30] | [JSON](mvb_r8o_83y.json) |
| `mvd_you_c2g` | 五大夫綰 | [《史記・范睢蔡澤列傳》][61] | [JSON](mvd_you_c2g.json) |
| `mvi_div_h0g` | 項梁 | [《史記・淮陰侯列傳》][74] | [JSON](mvi_div_h0g.json) |
| `mvm_6am_j2n` | 商均 | [《史記・五帝本紀》][1]、[《史記・夏本紀》][2] | [JSON](mvm_6am_j2n.json) |
| `mvv_bou_spk` | 周亞夫 | [《史記・齊悼惠王世家》][34] | [JSON](mvv_bou_spk.json) |
| `mvw_sno_xdr` | 王陵夫人未名 | [《史記・張丞相列傳》][78] | [JSON](mvw_sno_xdr.json) |
| `mw2_sla_iy2` | 蔡尉捐 | [《史記・秦本紀》][5] | [JSON](mw2_sla_iy2.json) |
| `mw3_2yt_n4a` | 趙穿 | [《史記・趙世家》][25] | [JSON](mw3_2yt_n4a.json) |
| `mwj_zlb_yqk` | 桀引古傳說 | [《史記・李斯列傳》][69] | [JSON](mwj_zlb_yqk.json) |
| `mwl_kmw_vo2` | 襄子姊（趙世家代王夫人未名者） | [《史記・趙世家》][25] | [JSON](mwl_kmw_vo2.json) |
| `mwr_na0_1in` | 周公引古 | [《史記・春申君列傳》][60] | [JSON](mwr_na0_1in.json) |
| `mww_f6f_st9` | 定王（介） | [《史記・周本紀》][4] | [JSON](mww_f6f_st9.json) |
| `mwy_yd6_bo5` | 楚共王 | [《史記・晉世家》][21] | [JSON](mwy_yd6_bo5.json) |
| `mx3_571_55a` | 蘇代 | [《史記・韓世家》][27] | [JSON](mx3_571_55a.json) |
| `mx7_r34_32m` | 田軫 | [《史記・田敬仲完世家》][28] | [JSON](mx7_r34_32m.json) |
| `myc_m95_z8x` | 小令尹 | [《史記・樗里子甘茂列傳》][53] | [JSON](myc_m95_z8x.json) |
| `myr_tln_x5c` | 項聲 | [《史記・高祖本紀》][8] | [JSON](myr_tln_x5c.json) |
| `mys_kcy_y9o` | 殷王 | [《史記・陳丞相世家》][38] | [JSON](mys_kcy_y9o.json) |
| `myy_zdg_6b6` | 柳下惠 | [《史記・孔子世家》][29] | [JSON](myy_zdg_6b6.json) |
| `mz0_im5_1m9` | 蒙驁 | [《史記・魏世家》][26] | [JSON](mz0_im5_1m9.json) |
| `mz9_446_wux` | 仲梁懷 | [《史記・孔子世家》][29] | [JSON](mz9_446_wux.json) |
| `mzh_t0y_wv2` | 夫差引古 | [《史記・樂毅列傳》][62] | [JSON](mzh_t0y_wv2.json) |
| `n1e_bz7_1di` | 賈生未詳名 | [《史記・張丞相列傳》][78] | [JSON](n1e_bz7_1di.json) |
| `n1i_qiv_h8g` | 桀引古 | [《史記・魯仲連鄒陽列傳》][65] | [JSON](n1i_qiv_h8g.json) |
| `n1j_kbh_u02` | 丞史未名（鼂錯） | [《史記・袁盎鼂錯列傳》][83] | [JSON](n1j_kbh_u02.json) |
| `n1u_sl2_yd6` | 秦繆公 | [《史記・商君列傳》][50] | [JSON](n1u_sl2_yd6.json) |
| `n22_unt_6ec` | 魏齊 | [《史記・范睢蔡澤列傳》][61] | [JSON](n22_unt_6ec.json) |
| `n2o_l90_fnm` | 韓非 | [《史記・老子韓非列傳》][45] | [JSON](n2o_l90_fnm.json) |
| `n39_fsx_avv` | 胡亥引古 | [《史記・魯仲連鄒陽列傳》][65] | [JSON](n39_fsx_avv.json) |
| `n3f_71l_idp` | 笑躄者美人未名 | [《史記・平原君虞卿列傳》][58] | [JSON](n3f_71l_idp.json) |
| `n3j_8ad_gsu` | 奡 | [《史記・仲尼弟子列傳》][49] | [JSON](n3j_8ad_gsu.json) |
| `n3t_awm_sp8` | 周丘 | [《史記・吳王濞列傳》][88] | [JSON](n3t_awm_sp8.json) |
| `n3u_8u6_lno` | 桀溺 | [《史記・仲尼弟子列傳》][49] | [JSON](n3u_8u6_lno.json) |
| `n49_17u_m8d` | 東周惠公 | [《史記・周本紀》][4] | [JSON](n49_17u_m8d.json) |
| `n4h_bu7_mse` | 宋女（允母） | [《史記・魯周公世家》][15] | [JSON](n4h_bu7_mse.json) |
| `n51_9zm_sqh` | 武乙 | [《史記・殷本紀》][3] | [JSON](n51_9zm_sqh.json) |
| `n5j_25r_qix` | 夾敖（楚王） | [《史記・吳太伯世家》][13]、[《史記・管蔡世家》][17]、[《史記・陳杞世家》][18] | [JSON](n5j_25r_qix.json) |
| `n5n_yhc_5k3` | 槐 | [《史記・夏本紀》][2] | [JSON](n5n_yhc_5k3.json) |
| `n6q_89m_21t` | 黔夫 | [《史記・田敬仲完世家》][28] | [JSON](n6q_89m_21t.json) |
| `n79_99b_tpt` | 魏哀王 | [《史記・張儀列傳》][52] | [JSON](n79_99b_tpt.json) |
| `n7c_afk_6o2` | 樓緩 | [《史記・趙世家》][25] | [JSON](n7c_afk_6o2.json) |
| `n7i_lqk_3xi` | 陳餘 | [《史記・張耳陳餘列傳》][71] | [JSON](n7i_lqk_3xi.json) |
| `n7k_r8y_fkr` | 知伯文子 | [《史記・趙世家》][25] | [JSON](n7k_r8y_fkr.json) |
| `n7l_j5p_4wl` | 王慶忌引古 | [《史記・范睢蔡澤列傳》][61] | [JSON](n7l_j5p_4wl.json) |
| `n7m_j5e_bt2` | 蒲守 | [《史記・樗里子甘茂列傳》][53] | [JSON](n7m_j5e_bt2.json) |
| `n7v_qo9_v4f` | 冉耕 | [《史記・仲尼弟子列傳》][49] | [JSON](n7v_qo9_v4f.json) |
| `n82_e6r_7z2` | 孫臏引古 | [《史記・魯仲連鄒陽列傳》][65] | [JSON](n82_e6r_7z2.json) |
| `n8l_nsk_o8v` | 釐王 | [《史記・周本紀》][4] | [JSON](n8l_nsk_o8v.json) |
| `n8l_wan_3tx` | 蘧伯玉（衛臣） | [《史記・衛康叔世家》][19] | [JSON](n8l_wan_3tx.json) |
| `n8s_n7s_r91` | 吳王濞 | [《史記・絳侯周勃世家》][39] | [JSON](n8s_n7s_r91.json) |
| `n90_dwg_o23` | 樊市人夫人未名 | [《史記・樊酈滕灌列傳》][77] | [JSON](n90_dwg_o23.json) |
| `n9g_om6_3cj` | 樗里子母 | [《史記・樗里子甘茂列傳》][53] | [JSON](n9g_om6_3cj.json) |
| `n9g_zzh_3ss` | 陳平 | [《史記・袁盎鼂錯列傳》][83] | [JSON](n9g_zzh_3ss.json) |
| `n9l_foh_qiq` | 秦皇帝 | [《史記・留侯世家》][37] | [JSON](n9l_foh_qiq.json) |
| `na8_45f_m80` | 麃公 | [《史記・秦始皇本紀》][6] | [JSON](na8_45f_m80.json) |
| `nad_18h_5jc` | 平陽公主 | [《史記・外戚世家》][31] | [JSON](nad_18h_5jc.json) |
| `naf_s08_xqw` | 犀首 | [《史記・秦本紀》][5] | [JSON](naf_s08_xqw.json) |
| `nap_df8_p65` | 澠池擬立趙太子未名 | [《史記・廉頗藺相如列傳》][63] | [JSON](nap_df8_p65.json) |
| `nbd_d27_t2w` | 曾參母 | [《史記・樗里子甘茂列傳》][53] | [JSON](nbd_d27_t2w.json) |
| `nbg_cps_9w9` | 魏安釐王 | [《史記・魯仲連鄒陽列傳》][65] | [JSON](nbg_cps_9w9.json) |
| `nbj_uzl_tr9` | 孔丘 | [《史記・商君列傳》][50] | [JSON](nbj_uzl_tr9.json) |
| `nbk_qg1_64o` | 楚王入周事件 | [《史記・樗里子甘茂列傳》][53] | [JSON](nbk_qg1_64o.json) |
| `nbw_mdv_b54` | 晏嬰 | [《史記・趙世家》][25] | [JSON](nbw_mdv_b54.json) |
| `nc4_msq_h8a` | 前少帝（呂太后本紀未名） | [《史記・呂太后本紀》][9] | [JSON](nc4_msq_h8a.json) |
| `ncc_ycr_r40` | 楚懷王 | [《史記・韓信盧綰列傳》][75] | [JSON](ncc_ycr_r40.json) |
| `nd8_vw5_w1w` | 蘧瑗 | [《史記・吳太伯世家》][13] | [JSON](nd8_vw5_w1w.json) |
| `nd9_pxv_3br` | 轅濤涂（陳大夫） | [《史記・陳杞世家》][18] | [JSON](nd9_pxv_3br.json) |
| `nda_3wa_ktc` | 衛長公主 | [《史記・曹相國世家》][36] | [JSON](nda_3wa_ktc.json) |
| `ndh_grt_skd` | 富人女故事 | [《史記・樗里子甘茂列傳》][53] | [JSON](ndh_grt_skd.json) |
| `ndp_kf2_zbo` | 袁盎 | [《史記・袁盎鼂錯列傳》][83] | [JSON](ndp_kf2_zbo.json) |
| `ndr_tb3_504` | 鮑叔牙 | [《史記・管晏列傳》][44] | [JSON](ndr_tb3_504.json) |
| `ne5_ers_49u` | 項梁 | [《史記・韓信盧綰列傳》][75] | [JSON](ne5_ers_49u.json) |
| `nec_2vd_5tr` | 悼王（猛） | [《史記・周本紀》][4] | [JSON](nec_2vd_5tr.json) |
| `nec_926_3u4` | 少師（微子問去留者） | [《史記・宋微子世家》][20] | [JSON](nec_926_3u4.json) |
| `neh_wop_6sz` | 韓廣 | [《史記・陳涉世家》][30] | [JSON](neh_wop_6sz.json) |
| `nek_dsn_nih` | 康王 | [《史記・周本紀》][4] | [JSON](nek_dsn_nih.json) |
| `nfi_mir_dew` | 子之 | [《史記・蘇秦列傳》][51] | [JSON](nfi_mir_dew.json) |
| `nfu_k8n_4jt` | 長安君（趙世家未名者） | [《史記・趙世家》][25] | [JSON](nfu_k8n_4jt.json) |
| `ngf_f1j_cj9` | 太公 | [《史記・伯夷列傳》][43] | [JSON](ngf_f1j_cj9.json) |
| `ngh_196_gz6` | 畢公 | [《史記・周本紀》][4] | [JSON](ngh_196_gz6.json) |
| `ngh_hjf_xnr` | 齊威王 | [《史記・魏世家》][26] | [JSON](ngh_hjf_xnr.json) |
| `ngl_ime_tgu` | 太史公 | [《史記・田儋列傳》][76] | [JSON](ngl_ime_tgu.json) |
| `ngn_nzv_4gr` | 齊景公 | [《史記・齊太公世家》][14] | [JSON](ngn_nzv_4gr.json) |
| `ngn_suh_k03` | 魯莊公 | [《史記・刺客列傳》][68] | [JSON](ngn_suh_k03.json) |
| `nhi_xsz_yal` | 陳豨 | [《史記・魏豹彭越列傳》][72] | [JSON](nhi_xsz_yal.json) |
| `nhk_xgq_7qk` | 燕王聊城未名 | [《史記・魯仲連鄒陽列傳》][65] | [JSON](nhk_xgq_7qk.json) |
| `nht_c38_x7o` | 魏惠王 | [《史記・田敬仲完世家》][28] | [JSON](nht_c38_x7o.json) |
| `nix_7ug_wxv` | 呂嬃 | [《史記・陳丞相世家》][38] | [JSON](nix_7ug_wxv.json) |
| `nj0_f2z_zlx` | 左徒 | [《史記・春申君列傳》][60] | [JSON](nj0_f2z_zlx.json) |
| `nj7_1td_y4z` | 閻樂 | [《史記・秦始皇本紀》][6] | [JSON](nj7_1td_y4z.json) |
| `njb_tt0_sz4` | 田忌 | [《史記・陳涉世家》][30] | [JSON](njb_tt0_sz4.json) |
| `njs_nws_8r1` | 鄭伯（楚莊王圍鄭時未名） | [《史記・楚世家》][22] | [JSON](njs_nws_8r1.json) |
| `nju_tpj_v74` | 子行 | [《史記・齊太公世家》][14] | [JSON](nju_tpj_v74.json) |
| `nk4_9wx_meg` | 公華 | [《史記・孔子世家》][29] | [JSON](nk4_9wx_meg.json) |
| `nka_xcg_d5x` | 鮑牧 | [《史記・田敬仲完世家》][28] | [JSON](nka_xcg_d5x.json) |
| `nlt_msz_iuz` | 焉氏（雍將軍） | [《史記・樊酈滕灌列傳》][77] | [JSON](nlt_msz_iuz.json) |
| `nmf_bg9_hdz` | 孔子 | [《史記・平原君虞卿列傳》][58] | [JSON](nmf_bg9_hdz.json) |
| `nml_3oq_o49` | 趙王遷 | [《史記・張釋之馮唐列傳》][84] | [JSON](nml_3oq_o49.json) |
| `nmp_5et_y55` | 南陽守齮 | [《史記・絳侯周勃世家》][39] | [JSON](nmp_5et_y55.json) |
| `nn2_9jj_i6n` | 魏昭王 | [《史記・樂毅列傳》][62] | [JSON](nn2_9jj_i6n.json) |
| `nna_uks_w03` | 子胥引古 | [《史記・魯仲連鄒陽列傳》][65] | [JSON](nna_uks_w03.json) |
| `nnj_520_wdk` | 簀中救范守者未名 | [《史記・范睢蔡澤列傳》][61] | [JSON](nnj_520_wdk.json) |
| `nnq_gau_71f` | 太史公 | [《史記・扁鵲倉公列傳》][87] | [JSON](nnq_gau_71f.json) |
| `nnw_99z_4e5` | 梁孝王 | [《史記・田叔列傳》][86] | [JSON](nnw_99z_4e5.json) |
| `nnz_8gm_bdk` | 田光 | [《史記・曹相國世家》][36] | [JSON](nnz_8gm_bdk.json) |
| `no0_6y9_swo` | 齊使者 | [《史記・孫子吳起列傳》][47] | [JSON](no0_6y9_swo.json) |
| `noa_3ci_b9s` | 鬼谷先生 | [《史記・蘇秦列傳》][51] | [JSON](noa_3ci_b9s.json) |
| `noi_rkl_11c` | 魏無知 | [《史記・陳丞相世家》][38] | [JSON](noi_rkl_11c.json) |
| `noy_49h_qor` | 漢惠帝 | [《史記・酈生陸賈列傳》][79] | [JSON](noy_49h_qor.json) |
| `np2_qh8_aoz` | 魏文侯（誅晉亂者） | [《史記・晉世家》][21] | [JSON](np2_qh8_aoz.json) |
| `npw_voa_yri` | 羌瘣 | [《史記・秦始皇本紀》][6] | [JSON](npw_voa_yri.json) |
| `npx_bl5_op1` | 宋厲公 | [《史記・孔子世家》][29] | [JSON](npx_bl5_op1.json) |
| `nq4_rjk_iab` | 褚先生 | [《史記・外戚世家》][31] | [JSON](nq4_rjk_iab.json) |
| `nq9_81y_9cv` | 陳勝 | [《史記・樊酈滕灌列傳》][77] | [JSON](nq9_81y_9cv.json) |
| `nqa_zlk_uu4` | 武蒲（魏申徒） | [《史記・高祖本紀》][8] | [JSON](nqa_zlk_uu4.json) |
| `nqp_02x_ekk` | 狐突（晉臣） | [《史記・晉世家》][21] | [JSON](nqp_02x_ekk.json) |
| `nqv_ba2_zh4` | 州吁 | [《史記・鄭世家》][24] | [JSON](nqv_ba2_zh4.json) |
| `nr3_tph_hhg` | 秦莊襄王 | [《史記・春申君列傳》][60] | [JSON](nr3_tph_hhg.json) |
| `nrd_0cq_zyz` | 趙奢 | [《史記・廉頗藺相如列傳》][63] | [JSON](nrd_0cq_zyz.json) |
| `nrp_vv5_hry` | 項籍 | [《史記・傅靳蒯成列傳》][80] | [JSON](nrp_vv5_hry.json) |
| `ns0_24x_hh0` | 大伯（引古） | [《史記・張耳陳餘列傳》][71] | [JSON](ns0_24x_hh0.json) |
| `ns2_4jx_cpp` | 肥誅 | [《史記・樊酈滕灌列傳》][77] | [JSON](ns2_4jx_cpp.json) |
| `ns5_o5x_fq0` | 黃長卿 | [《史記・扁鵲倉公列傳》][87] | [JSON](ns5_o5x_fq0.json) |
| `nsa_bp5_1dk` | 項莊 | [《史記・項羽本紀》][7] | [JSON](nsa_bp5_1dk.json) |
| `nsd_1cz_aqr` | 項羽 | [《史記・蕭相國世家》][35] | [JSON](nsd_1cz_aqr.json) |
| `nsr_p2m_2gw` | 鄭布 | [《史記・陳涉世家》][30] | [JSON](nsr_p2m_2gw.json) |
| `nt2_g7q_7db` | 內史肆 | [《史記・秦始皇本紀》][6] | [JSON](nt2_g7q_7db.json) |
| `nu2_ttq_hq0` | 華元御者（宋篇羊羹讀法未定） | [《史記・宋微子世家》][20] | [JSON](nu2_ttq_hq0.json) |
| `nu4_0wz_9o2` | 宮之奇（虞諫臣） | [《史記・晉世家》][21] | [JSON](nu4_0wz_9o2.json) |
| `nu5_o75_tzs` | 仲尼 | [《史記・孔子世家》][29] | [JSON](nu5_o75_tzs.json) |
| `nu5_qeg_7ly` | 董生未名 | [《史記・刺客列傳》][68] | [JSON](nu5_qeg_7ly.json) |
| `nu6_2qe_oza` | 周苛 | [《史記・韓信盧綰列傳》][75] | [JSON](nu6_2qe_oza.json) |
| `nuf_v4j_pps` | 潘父（弒昭侯者） | [《史記・晉世家》][21] | [JSON](nuf_v4j_pps.json) |
| `nuq_wqa_cu6` | 巻章（楚篇祖系） | [《史記・楚世家》][22] | [JSON](nuq_wqa_cu6.json) |
| `nuu_lz3_bxa` | 伍子胥引古 | [《史記・樂毅列傳》][62] | [JSON](nuu_lz3_bxa.json) |
| `nuz_py4_4la` | 太史公 | [《史記・季布欒布列傳》][82] | [JSON](nuz_py4_4la.json) |
| `nvf_r2k_j9y` | 竇嬰 | [《史記・袁盎鼂錯列傳》][83] | [JSON](nvf_r2k_j9y.json) |
| `nvj_8mb_5xv` | 董叔 | [《史記・趙世家》][25] | [JSON](nvj_8mb_5xv.json) |
| `nvm_7kp_nle` | 趙章 | [《史記・扁鵲倉公列傳》][87] | [JSON](nvm_7kp_nle.json) |
| `nvt_gxa_pdo` | 季武子（魯卿） | [《史記・魯周公世家》][15] | [JSON](nvt_gxa_pdo.json) |
| `nvv_s6a_cve` | 梁惠王 | [《史記・魏世家》][26] | [JSON](nvv_s6a_cve.json) |
| `nvw_f7a_z2i` | 大戊 | [《史記・趙世家》][25] | [JSON](nvw_f7a_z2i.json) |
| `nw9_lle_9jg` | 景駒 | [《史記・項羽本紀》][7] | [JSON](nw9_lle_9jg.json) |
| `nwx_f88_xfu` | 周亞夫 | [《史記・絳侯周勃世家》][39] | [JSON](nwx_f88_xfu.json) |
| `nxr_c7g_p9l` | 葛嬴 | [《史記・齊太公世家》][14] | [JSON](nxr_c7g_p9l.json) |
| `nyj_dya_hs8` | 顯王 | [《史記・周本紀》][4] | [JSON](nyj_dya_hs8.json) |
| `nz3_a9o_scr` | 止（晉烈公） | [《史記・晉世家》][21] | [JSON](nz3_a9o_scr.json) |
| `nz6_tdl_ub1` | 太史公 | [《史記・萬石張叔列傳》][85] | [JSON](nz6_tdl_ub1.json) |
| `nza_w1p_x8f` | 南宮公主 | [《史記・外戚世家》][31] | [JSON](nza_w1p_x8f.json) |
| `nzi_rg8_uik` | 扶蘇 | [《史記・劉敬叔孫通列傳》][81] | [JSON](nzi_rg8_uik.json) |
| `nzi_ufz_vr7` | 田榮 | [《史記・張耳陳餘列傳》][71] | [JSON](nzi_ufz_vr7.json) |
| `nzo_n0u_8s5` | 公孫喜 | [《史記・韓世家》][27] | [JSON](nzo_n0u_8s5.json) |
| `o0m_w07_a7p` | 戎姬 | [《史記・齊太公世家》][14] | [JSON](o0m_w07_a7p.json) |
| `o1f_8uz_3tk` | 元王 | [《史記・周本紀》][4] | [JSON](o1f_8uz_3tk.json) |
| `o1q_p6i_ehs` | 高祖（陳涉世家守冢未名者） | [《史記・陳涉世家》][30] | [JSON](o1q_p6i_ehs.json) |
| `o2h_3ag_bnw` | 蔡哀侯（楚篇被俘者） | [《史記・楚世家》][22] | [JSON](o2h_3ag_bnw.json) |
| `o2m_3n4_oi4` | 子西（楚令尹） | [《史記・陳杞世家》][18] | [JSON](o2m_3n4_oi4.json) |
| `o2m_km9_b1w` | 郅都 | [《史記・季布欒布列傳》][82] | [JSON](o2m_km9_b1w.json) |
| `o32_eo4_vyk` | 雲中守遬 | [《史記・絳侯周勃世家》][39] | [JSON](o32_eo4_vyk.json) |
| `o3p_xx6_xrf` | 荀卿 | [《史記・呂不韋列傳》][67] | [JSON](o3p_xx6_xrf.json) |
| `o3v_ms0_idw` | 栗腹 | [《史記・燕召公世家》][16]、[《史記・樂毅列傳》][62] | [JSON](o3v_ms0_idw.json) |
| `o3z_4md_e9l` | 太仆嬰 | [《史記・齊悼惠王世家》][34] | [JSON](o3z_4md_e9l.json) |
| `o4b_bje_i31` | 信陵（四君稱呼） | [《史記・秦始皇本紀》][6] | [JSON](o4b_bje_i31.json) |
| `o4h_qq4_taj` | 田既 | [《史記・田儋列傳》][76] | [JSON](o4h_qq4_taj.json) |
| `o58_d34_qul` | 楚令尹 | [《史記・孫子吳起列傳》][47] | [JSON](o58_d34_qul.json) |
| `o5b_urx_nop` | 銅鞮伯華 | [《史記・仲尼弟子列傳》][49] | [JSON](o5b_urx_nop.json) |
| `o5z_bzo_4kz` | 張孟同 | [《史記・趙世家》][25] | [JSON](o5z_bzo_4kz.json) |
| `o67_lsk_1vy` | 宦者平 | [《史記・扁鵲倉公列傳》][87] | [JSON](o67_lsk_1vy.json) |
| `o6u_xnt_ls1` | 樂毅 | [《史記・田敬仲完世家》][28] | [JSON](o6u_xnt_ls1.json) |
| `o77_eec_0oy` | 姜原 | [《史記・周本紀》][4] | [JSON](o77_eec_0oy.json) |
| `o7b_uyb_qu9` | 淖齒 | [《史記・范睢蔡澤列傳》][61] | [JSON](o7b_uyb_qu9.json) |
| `o7j_zzq_frd` | 灌夫 | [《史記・季布欒布列傳》][82] | [JSON](o7j_zzq_frd.json) |
| `o7y_cll_jk1` | 伊尹 | [《史記・絳侯周勃世家》][39] | [JSON](o7y_cll_jk1.json) |
| `o89_yle_8ou` | 公伯繚 | [《史記・仲尼弟子列傳》][49] | [JSON](o89_yle_8ou.json) |
| `o8a_jd0_o38` | 趙桓子（楚篇三晉記事） | [《史記・楚世家》][22] | [JSON](o8a_jd0_o38.json) |
| `o8m_hrx_01i` | 邦巽 | [《史記・仲尼弟子列傳》][49] | [JSON](o8m_hrx_01i.json) |
| `o8t_osi_6uw` | 師己 | [《史記・孔子世家》][29] | [JSON](o8t_osi_6uw.json) |
| `o8y_3ur_51e` | 膠西王未具名 | [《史記・扁鵲倉公列傳》][87] | [JSON](o8y_3ur_51e.json) |
| `o8z_o5j_2e8` | 司馬欣 | [《史記・項羽本紀》][7] | [JSON](o8z_o5j_2e8.json) |
| `o97_iv4_32f` | 陳女（周惠王后未名） | [《史記・陳杞世家》][18] | [JSON](o97_iv4_32f.json) |
| `o9d_ond_h44` | 太史公 | [《史記・伯夷列傳》][43] | [JSON](o9d_ond_h44.json) |
| `o9l_aen_3cx` | 比干引古 | [《史記・范睢蔡澤列傳》][61] | [JSON](o9l_aen_3cx.json) |
| `o9t_t9k_rc2` | 申之御（魏世家未名者） | [《史記・魏世家》][26] | [JSON](o9t_t9k_rc2.json) |
| `oa0_nm7_e6f` | 齊宣王 | [《史記・田敬仲完世家》][28]、[《史記・孟嘗君列傳》][57] | [JSON](oa0_nm7_e6f.json) |
| `oah_2x7_t4c` | 石作蜀 | [《史記・仲尼弟子列傳》][49] | [JSON](oah_2x7_t4c.json) |
| `oaj_udd_7d9` | 秦武王 | [《史記・樗里子甘茂列傳》][53] | [JSON](oaj_udd_7d9.json) |
| `ob6_rla_gka` | 伯夷（孤竹） | [《史記・周本紀》][4] | [JSON](ob6_rla_gka.json) |
| `ob7_g6i_7pp` | 項羽 | [《史記・項羽本紀》][7] | [JSON](ob7_g6i_7pp.json) |
| `oba_urn_khk` | 章邯 | [《史記・項羽本紀》][7] | [JSON](oba_urn_khk.json) |
| `obb_w0p_gfj` | 太史公 | [《史記・黥布列傳》][73] | [JSON](obb_w0p_gfj.json) |
| `obf_5py_0xk` | 罕父黑 | [《史記・仲尼弟子列傳》][49] | [JSON](obf_5py_0xk.json) |
| `obm_q7q_ig9` | 章邯 | [《史記・李斯列傳》][69] | [JSON](obm_q7q_ig9.json) |
| `obz_kz0_ohb` | 王子城父 | [《史記・齊太公世家》][14]、[《史記・魯周公世家》][15] | [JSON](obz_kz0_ohb.json) |
| `och_1lh_hgs` | 陳豨 | [《史記・傅靳蒯成列傳》][80] | [JSON](och_1lh_hgs.json) |
| `ocj_6o3_ax8` | 平原君引述 | [《史記・呂不韋列傳》][67] | [JSON](ocj_6o3_ax8.json) |
| `odj_0jk_o2z` | 外丙 | [《史記・殷本紀》][3] | [JSON](odj_0jk_o2z.json) |
| `odm_1yx_6o6` | 齊靈公 | [《史記・齊太公世家》][14] | [JSON](odm_1yx_6o6.json) |
| `odt_ipa_i2h` | 濟北王未具名 | [《史記・扁鵲倉公列傳》][87] | [JSON](odt_ipa_i2h.json) |
| `oeb_7jj_w9t` | 閼與秦間未名 | [《史記・廉頗藺相如列傳》][63] | [JSON](oeb_7jj_w9t.json) |
| `oef_17e_520` | 夫差 | [《史記・蘇秦列傳》][51] | [JSON](oef_17e_520.json) |
| `ofc_8ei_jb7` | 韓信 | [《史記・淮陰侯列傳》][74] | [JSON](ofc_8ei_jb7.json) |
| `off_msa_t3x` | 重黎（楚篇祖系） | [《史記・楚世家》][22] | [JSON](off_msa_t3x.json) |
| `ofo_goq_gfx` | 奄息 | [《史記・秦本紀》][5] | [JSON](ofo_goq_gfx.json) |
| `ofs_1tu_iml` | 樂乘（趙將） | [《史記・燕召公世家》][16] | [JSON](ofs_1tu_iml.json) |
| `oge_g2v_hqw` | 平（武遂侯） | [《史記・酈生陸賈列傳》][79] | [JSON](oge_g2v_hqw.json) |
| `ogh_zo9_46d` | 吳公未名 | [《史記・屈原賈生列傳》][66] | [JSON](ogh_zo9_46d.json) |
| `oh2_xep_h3c` | 咸宣 | [《史記・萬石張叔列傳》][85] | [JSON](oh2_xep_h3c.json) |
| `ohe_hlc_y40` | 閼路（杞哀公） | [《史記・陳杞世家》][18] | [JSON](ohe_hlc_y40.json) |
| `oho_r3f_c6y` | 堯 | [《史記・五帝本紀》][1] | [JSON](oho_r3f_c6y.json) |
| `ohw_icg_qzk` | 魯大師（孔子世家未名者） | [《史記・孔子世家》][29] | [JSON](ohw_icg_qzk.json) |
| `oie_tl5_yxn` | 桃侯舍 | [《史記・萬石張叔列傳》][85] | [JSON](oie_tl5_yxn.json) |
| `ois_7lo_cjv` | 閎夭引古 | [《史記・范睢蔡澤列傳》][61] | [JSON](ois_7lo_cjv.json) |
| `oiy_a5y_l1t` | 犀首 | [《史記・魏世家》][26] | [JSON](oiy_a5y_l1t.json) |
| `oj5_zy0_x0t` | 尹姬 | [《史記・外戚世家》][31] | [JSON](oj5_zy0_x0t.json) |
| `ojk_hex_iha` | 密康公 | [《史記・周本紀》][4] | [JSON](ojk_hex_iha.json) |
| `ojt_xkj_2fe` | 和 | [《史記・司馬穰苴列傳》][46] | [JSON](ojt_xkj_2fe.json) |
| `okm_lcf_o9z` | 衛惠公（莊公五年記事） | [《史記・魯周公世家》][15] | [JSON](okm_lcf_o9z.json) |
| `okz_ham_pdc` | 咎 | [《史記・魏豹彭越列傳》][72] | [JSON](okz_ham_pdc.json) |
| `olj_7ig_g6i` | 齊王（趙世家敗走未名者） | [《史記・趙世家》][25] | [JSON](olj_7ig_g6i.json) |
| `olo_0sp_7bd` | 申屠嘉 | [《史記・袁盎鼂錯列傳》][83] | [JSON](olo_0sp_7bd.json) |
| `olu_wyu_lcq` | 周公 | [《史記・梁孝王世家》][40] | [JSON](olu_wyu_lcq.json) |
| `om8_gee_15k` | 祭仲（鄭臣） | [《史記・宋微子世家》][20] | [JSON](om8_gee_15k.json) |
| `omb_zrk_gla` | 趙敬侯 | [《史記・魏世家》][26] | [JSON](omb_zrk_gla.json) |
| `omr_7qm_6el` | 楚王被虜未名 | [《史記・蒙恬列傳》][70] | [JSON](omr_7qm_6el.json) |
| `ona_sbo_027` | 齊王商於事件 | [《史記・張儀列傳》][52] | [JSON](ona_sbo_027.json) |
| `onj_4n3_xwi` | 呂臣 | [《史記・黥布列傳》][73] | [JSON](onj_4n3_xwi.json) |
| `onk_jwj_o75` | 孟賁 | [《史記・范睢蔡澤列傳》][61] | [JSON](onk_jwj_o75.json) |
| `onm_kp8_q59` | 原過 | [《史記・趙世家》][25] | [JSON](onm_kp8_q59.json) |
| `onm_mft_1q7` | 田會 | [《史記・齊太公世家》][14] | [JSON](onm_mft_1q7.json) |
| `onr_3p7_3bc` | 豎陽穀（子反侍者） | [《史記・晉世家》][21]、[《史記・楚世家》][22] | [JSON](onr_3p7_3bc.json) |
| `onv_2fg_67f` | 賈舉 | [《史記・齊太公世家》][14] | [JSON](onv_2fg_67f.json) |
| `oo9_jtx_rmv` | 王翳 | [《史記・項羽本紀》][7] | [JSON](oo9_jtx_rmv.json) |
| `oob_b0t_afn` | 史厭 | [《史記・周本紀》][4] | [JSON](oob_b0t_afn.json) |
| `op3_d14_c7u` | 豫讓 | [《史記・刺客列傳》][68] | [JSON](op3_d14_c7u.json) |
| `op4_zcc_7ds` | 簡公 | [《史記・田敬仲完世家》][28] | [JSON](op4_zcc_7ds.json) |
| `op6_1s5_jg7` | 湣公（燕成公後） | [《史記・燕召公世家》][16] | [JSON](op6_1s5_jg7.json) |
| `opw_myk_48z` | 髙信 | [《史記・趙世家》][25] | [JSON](opw_myk_48z.json) |
| `oqm_ilj_lmx` | 昭雎（楚懷王臣） | [《史記・楚世家》][22] | [JSON](oqm_ilj_lmx.json) |
| `or0_qxv_dk6` | 田不禮 | [《史記・趙世家》][25] | [JSON](or0_qxv_dk6.json) |
| `orq_rdx_tgp` | 伏生 | [《史記・袁盎鼂錯列傳》][83] | [JSON](orq_rdx_tgp.json) |
| `ors_7qn_a2p` | 太史公 | [《史記・樗里子甘茂列傳》][53] | [JSON](ors_7qn_a2p.json) |
| `os5_gkv_3ew` | 太史公 | [《史記・蘇秦列傳》][51] | [JSON](os5_gkv_3ew.json) |
| `otl_2v4_mdf` | 驪姬 | [《史記・劉敬叔孫通列傳》][81] | [JSON](otl_2v4_mdf.json) |
| `otn_s4j_ujp` | 秦昭王 | [《史記・范睢蔡澤列傳》][61] | [JSON](otn_s4j_ujp.json) |
| `otq_r9b_d3z` | 呂后 | [《史記・酈生陸賈列傳》][79] | [JSON](otq_r9b_d3z.json) |
| `otx_w5y_yup` | 武引古短稱 | [《史記・屈原賈生列傳》][66] | [JSON](otx_w5y_yup.json) |
| `ou4_46z_3ks` | 子我 | [《史記・田敬仲完世家》][28] | [JSON](ou4_46z_3ks.json) |
| `ou9_l91_4py` | 呂相（讓秦使者） | [《史記・晉世家》][21] | [JSON](ou9_l91_4py.json) |
| `oul_55f_fz3` | 韓子引古未定 | [《史記・李斯列傳》][69] | [JSON](oul_55f_fz3.json) |
| `oun_g6a_0lp` | 文王 | [《史記・越王勾踐世家》][23] | [JSON](oun_g6a_0lp.json) |
| `ov9_hou_2hp` | 曾子引古 | [《史記・魯仲連鄒陽列傳》][65] | [JSON](ov9_hou_2hp.json) |
| `ova_rch_fa4` | 彭越 | [《史記・韓信盧綰列傳》][75] | [JSON](ova_rch_fa4.json) |
| `ovj_6cb_2pq` | 魏冉 | [《史記・趙世家》][25] | [JSON](ovj_6cb_2pq.json) |
| `ovn_rwu_yum` | 平原君 | [《史記・白起王翦列傳》][55] | [JSON](ovn_rwu_yum.json) |
| `ovw_5og_8au` | 伯服 | [《史記・鄭世家》][24] | [JSON](ovw_5og_8au.json) |
| `ow0_2qg_73y` | 李園女弟未名 | [《史記・春申君列傳》][60] | [JSON](ow0_2qg_73y.json) |
| `ow4_qy6_bx5` | 樓緩 | [《史記・平原君虞卿列傳》][58] | [JSON](ow4_qy6_bx5.json) |
| `owc_ejf_uzp` | 紂比擬 | [《史記・蕭相國世家》][35] | [JSON](owc_ejf_uzp.json) |
| `owj_whw_zzm` | 禹（孔子世家會稽傳說） | [《史記・孔子世家》][29] | [JSON](owj_whw_zzm.json) |
| `own_mt9_gtl` | 芒卯 | [《史記・魏世家》][26] | [JSON](own_mt9_gtl.json) |
| `own_sic_s7j` | 孫武 | [《史記・孫子吳起列傳》][47] | [JSON](own_sic_s7j.json) |
| `owp_6qt_lzs` | 舜 | [《史記・蘇秦列傳》][51] | [JSON](owp_6qt_lzs.json) |
| `owu_71x_f0p` | 齊內史士 | [《史記・呂太后本紀》][9] | [JSON](owu_71x_f0p.json) |
| `ox6_lqa_iko` | 程滑（弒晉厲公記事） | [《史記・管蔡世家》][17] | [JSON](ox6_lqa_iko.json) |
| `oxa_rta_lvd` | 澹臺滅明 | [《史記・仲尼弟子列傳》][49] | [JSON](oxa_rta_lvd.json) |
| `oxi_zcr_uxa` | 高起 | [《史記・高祖本紀》][8] | [JSON](oxi_zcr_uxa.json) |
| `oy5_z21_yq3` | 髙共 | [《史記・趙世家》][25] | [JSON](oy5_z21_yq3.json) |
| `oya_xaf_3w8` | 宋最 | [《史記・絳侯周勃世家》][39] | [JSON](oya_xaf_3w8.json) |
| `oye_sta_uwq` | 青翟 | [《史記・三王世家》][42] | [JSON](oye_sta_uwq.json) |
| `oyh_wvt_2ku` | 芒卯 | [《史記・穰侯列傳》][54] | [JSON](oyh_wvt_2ku.json) |
| `oyl_i12_1y4` | 召（引古） | [《史記・淮陰侯列傳》][74] | [JSON](oyl_i12_1y4.json) |
| `oza_c7e_kas` | 驪姬 | [《史記・晉世家》][21] | [JSON](oza_c7e_kas.json) |
| `ozf_h3v_dmz` | 步叔乘 | [《史記・仲尼弟子列傳》][49] | [JSON](ozf_h3v_dmz.json) |
| `ozj_rzf_gki` | 太子免 | [《史記・田敬仲完世家》][28] | [JSON](ozj_rzf_gki.json) |
| `ozm_m75_ta9` | 呂他 | [《史記・呂太后本紀》][9] | [JSON](ozm_m75_ta9.json) |
| `ozo_bsb_cnj` | 鄭袖 | [《史記・屈原賈生列傳》][66] | [JSON](ozo_bsb_cnj.json) |
| `p00_7fd_aoy` | 正考父 | [《史記・孔子世家》][29] | [JSON](p00_7fd_aoy.json) |
| `p03_ogp_trh` | 湯（古王引語） | [《史記・酈生陸賈列傳》][79] | [JSON](p03_ogp_trh.json) |
| `p06_lrs_tg7` | 孫叔敖引古 | [《史記・魯仲連鄒陽列傳》][65] | [JSON](p06_lrs_tg7.json) |
| `p0f_4cj_em4` | 齊湣王 | [《史記・樗里子甘茂列傳》][53] | [JSON](p0f_4cj_em4.json) |
| `p0f_9en_kjq` | 邯（三秦王） | [《史記・淮陰侯列傳》][74] | [JSON](p0f_9en_kjq.json) |
| `p0q_m9t_btu` | 舜後母 | [《史記・五帝本紀》][1] | [JSON](p0q_m9t_btu.json) |
| `p19_kgn_48d` | 兒良 | [《史記・陳涉世家》][30] | [JSON](p19_kgn_48d.json) |
| `p1g_3h6_97x` | 茄 | [《史記・白起王翦列傳》][55] | [JSON](p1g_3h6_97x.json) |
| `p1o_prn_wyw` | 趙襄子 | [《史記・魏世家》][26] | [JSON](p1o_prn_wyw.json) |
| `p1q_4ay_bht` | 隰朋 | [《史記・齊太公世家》][14] | [JSON](p1q_4ay_bht.json) |
| `p2x_50r_b94` | 蘧伯玉 | [《史記・孔子世家》][29] | [JSON](p2x_50r_b94.json) |
| `p35_n0a_mxs` | 呂尚引古 | [《史記・魯仲連鄒陽列傳》][65] | [JSON](p35_n0a_mxs.json) |
| `p3d_pr7_9z3` | 黑臀 | [《史記・趙世家》][25] | [JSON](p3d_pr7_9z3.json) |
| `p3e_k23_i9f` | 周公 | [《史記・絳侯周勃世家》][39] | [JSON](p3e_k23_i9f.json) |
| `p3e_kto_76o` | 公杲 | [《史記・樊酈滕灌列傳》][77] | [JSON](p3e_kto_76o.json) |
| `p3l_pp3_n6i` | 皋陶 | [《史記・夏本紀》][2] | [JSON](p3l_pp3_n6i.json) |
| `p3v_9ns_snj` | 荀騅（景公卿） | [《史記・晉世家》][21] | [JSON](p3v_9ns_snj.json) |
| `p41_n3z_dlq` | 樓緩 | [《史記・穰侯列傳》][54] | [JSON](p41_n3z_dlq.json) |
| `p4b_qf7_603` | 趙武（趙庶子） | [《史記・趙世家》][25] | [JSON](p4b_qf7_603.json) |
| `p5c_373_050` | 仲由 | [《史記・仲尼弟子列傳》][49] | [JSON](p5c_373_050.json) |
| `p61_wfn_5e4` | 呂季主 | [《史記・梁孝王世家》][40] | [JSON](p61_wfn_5e4.json) |
| `p62_q55_4wr` | 伯 | [《史記・陳丞相世家》][38] | [JSON](p62_q55_4wr.json) |
| `p77_x5q_v4n` | 傅說 | [《史記・殷本紀》][3] | [JSON](p77_x5q_v4n.json) |
| `p7f_ppj_ib6` | 公林 | [《史記・孔子世家》][29] | [JSON](p7f_ppj_ib6.json) |
| `p7k_2z7_84m` | 魯仲連 | [《史記・魯仲連鄒陽列傳》][65] | [JSON](p7k_2z7_84m.json) |
| `p7v_f2l_8l5` | 繆嬴 | [《史記・秦本紀》][5] | [JSON](p7v_f2l_8l5.json) |
| `p7v_ue3_b2p` | 祝茲侯 | [《史記・孝文本紀》][10] | [JSON](p7v_ue3_b2p.json) |
| `p8d_lmw_68r` | 呂莊 | [《史記・呂太后本紀》][9] | [JSON](p8d_lmw_68r.json) |
| `p8h_p9d_wrc` | 長安君（趙世家悼襄王六年未名者） | [《史記・趙世家》][25] | [JSON](p8h_p9d_wrc.json) |
| `p92_3b3_lai` | 楚懷王 | [《史記・絳侯周勃世家》][39] | [JSON](p92_3b3_lai.json) |
| `p97_0nz_onl` | 熊毋康（楚篇早卒者） | [《史記・楚世家》][22] | [JSON](p97_0nz_onl.json) |
| `p9d_4b8_s3p` | 石乞（蒯聵使者） | [《史記・衛康叔世家》][19] | [JSON](p9d_4b8_s3p.json) |
| `p9g_3y5_dah` | 烏江亭長 | [《史記・項羽本紀》][7] | [JSON](p9g_3y5_dah.json) |
| `p9p_dej_4kd` | 秦惠王 | [《史記・趙世家》][25] | [JSON](p9p_dej_4kd.json) |
| `p9q_5fh_s2q` | 張耳妻未名 | [《史記・張耳陳餘列傳》][71] | [JSON](p9q_5fh_s2q.json) |
| `pag_8q8_jqn` | 陳桓子 | [《史記・吳太伯世家》][13] | [JSON](pag_8q8_jqn.json) |
| `pai_09n_rza` | 郤鉤（三郤記事） | [《史記・晉世家》][21] | [JSON](pai_09n_rza.json) |
| `par_wzx_6lu` | 宋戴公（孔子世家正考父所佐） | [《史記・孔子世家》][29] | [JSON](par_wzx_6lu.json) |
| `pbk_g9f_n8t` | 湯 | [《史記・留侯世家》][37] | [JSON](pbk_g9f_n8t.json) |
| `pc0_in1_8xo` | 孟武伯（魯卿） | [《史記・魯周公世家》][15] | [JSON](pc0_in1_8xo.json) |
| `pc3_yqm_327` | 廉頗 | [《史記・白起王翦列傳》][55] | [JSON](pc3_yqm_327.json) |
| `pc6_a84_ela` | 信陵君引述 | [《史記・呂不韋列傳》][67] | [JSON](pc6_a84_ela.json) |
| `pca_046_m1x` | 宗正使者 | [《史記・三王世家》][42] | [JSON](pca_046_m1x.json) |
| `pcg_qwq_2gj` | 相土 | [《史記・殷本紀》][3] | [JSON](pcg_qwq_2gj.json) |
| `pda_eev_m2h` | 師涓 | [《史記・殷本紀》][3] | [JSON](pda_eev_m2h.json) |
| `pda_r9u_qna` | 隰朋（楚篇齊桓公輔） | [《史記・齊太公世家》][14] | [JSON](pda_r9u_qna.json) |
| `pdd_ww5_imn` | 絳侯未詳名 | [《史記・張丞相列傳》][78] | [JSON](pdd_ww5_imn.json) |
| `pdn_whf_crz` | 樊噲 | [《史記・季布欒布列傳》][82] | [JSON](pdn_whf_crz.json) |
| `pen_hn0_sk9` | 和叔 | [《史記・五帝本紀》][1] | [JSON](pen_hn0_sk9.json) |
| `pew_ob7_n0k` | 田光 | [《史記・田儋列傳》][76] | [JSON](pew_ob7_n0k.json) |
| `pfc_5ld_w1l` | 曾參 | [《史記・樗里子甘茂列傳》][53] | [JSON](pfc_5ld_w1l.json) |
| `pft_5o1_zzt` | 釐負羈（曹人） | [《史記・晉世家》][21] | [JSON](pft_5o1_zzt.json) |
| `pg6_crd_4ug` | 良醫（高祖病中敘事） | [《史記・高祖本紀》][8] | [JSON](pg6_crd_4ug.json) |
| `pgu_6kt_nz1` | 橫（楚頃襄王） | [《史記・楚世家》][22] | [JSON](pgu_6kt_nz1.json) |
| `pgv_wze_yl1` | 武王 | [《史記・周本紀》][4] | [JSON](pgv_wze_yl1.json) |
| `pgv_xst_ss3` | 太公家令（高祖本紀） | [《史記・高祖本紀》][8] | [JSON](pgv_xst_ss3.json) |
| `pgw_7wx_2g6` | 王離 | [《史記・絳侯周勃世家》][39] | [JSON](pgw_7wx_2g6.json) |
| `pgz_pbh_533` | 公孫敢（衛門者） | [《史記・衛康叔世家》][19] | [JSON](pgz_pbh_533.json) |
| `pha_cmo_p9d` | 魏章 | [《史記・魏世家》][26] | [JSON](pha_cmo_p9d.json) |
| `phx_4fq_fnx` | 蘇代 | [《史記・蘇秦列傳》][51] | [JSON](phx_4fq_fnx.json) |
| `phx_lyu_9ym` | 賁郝 | [《史記・傅靳蒯成列傳》][80] | [JSON](phx_lyu_9ym.json) |
| `pia_0ku_1ts` | 堯 | [《史記・鄭世家》][24] | [JSON](pia_0ku_1ts.json) |
| `pic_g3r_frm` | 燕昭王 | [《史記・孟子荀卿列傳》][56] | [JSON](pic_g3r_frm.json) |
| `pie_655_z1d` | 絳侯（垓下敘事） | [《史記・絳侯周勃世家》][39] | [JSON](pie_655_z1d.json) |
| `pim_eqs_362` | 桀（引古） | [《史記・蒙恬列傳》][70] | [JSON](pim_eqs_362.json) |
| `pio_cvf_9l8` | 智伯 | [《史記・刺客列傳》][68] | [JSON](pio_cvf_9l8.json) |
| `pjg_qbb_v5f` | 楚悼王太子 | [《史記・孫子吳起列傳》][47] | [JSON](pjg_qbb_v5f.json) |
| `pkv_01i_t28` | 政 | [《史記・趙世家》][25] | [JSON](pkv_01i_t28.json) |
| `pl0_60l_400` | 秦穆公（引古） | [《史記・蒙恬列傳》][70] | [JSON](pl0_60l_400.json) |
| `pl1_jif_0x2` | 蕭公角 | [《史記・項羽本紀》][7] | [JSON](pl1_jif_0x2.json) |
| `plo_ezo_pmk` | 貫高 | [《史記・田叔列傳》][86] | [JSON](plo_ezo_pmk.json) |
| `pm2_ktg_h14` | 允格 | [《史記・鄭世家》][24] | [JSON](pm2_ktg_h14.json) |
| `pm7_yo7_kdw` | 種（引古） | [《史記・韓信盧綰列傳》][75] | [JSON](pm7_yo7_kdw.json) |
| `pmi_lcp_ocz` | 胡王書信未名 | [《史記・吳王濞列傳》][88] | [JSON](pmi_lcp_ocz.json) |
| `pmj_7wv_qbr` | 韓信母未名 | [《史記・淮陰侯列傳》][74] | [JSON](pmj_7wv_qbr.json) |
| `pmk_eyc_chr` | 公主（趙世家未名者） | [《史記・趙世家》][25] | [JSON](pmk_eyc_chr.json) |
| `pmn_f40_6n7` | 子（田世家髙唐守者讀法未定） | [《史記・田敬仲完世家》][28] | [JSON](pmn_f40_6n7.json) |
| `pn8_865_se4` | 魯君引古未名 | [《史記・魯仲連鄒陽列傳》][65] | [JSON](pn8_865_se4.json) |
| `pni_28v_4w0` | 秦繆公 | [《史記・趙世家》][25] | [JSON](pni_28v_4w0.json) |
| `pnl_mv7_etn` | 威烈王 | [《史記・周本紀》][4] | [JSON](pnl_mv7_etn.json) |
| `pnm_lcu_czk` | 秦孝公 | [《史記・商君列傳》][50] | [JSON](pnm_lcu_czk.json) |
| `pnp_ppe_lyv` | 晉獻公引文候選 | [《史記・扁鵲倉公列傳》][87] | [JSON](pnp_ppe_lyv.json) |
| `poc_jcs_zv6` | 曹沬 | [《史記・齊太公世家》][14] | [JSON](poc_jcs_zv6.json) |
| `poh_j7v_l00` | 奮揚 | [《史記・伍子胥列傳》][48] | [JSON](poh_j7v_l00.json) |
| `poh_mq2_1nz` | 茅焦 | [《史記・秦始皇本紀》][6]、[《史記・呂不韋列傳》][67] | [JSON](poh_mq2_1nz.json) |
| `pom_ycp_ha5` | 陳勝 | [《史記・陳涉世家》][30] | [JSON](pom_ycp_ha5.json) |
| `pos_l4q_b77` | 甘公 | [《史記・張耳陳餘列傳》][71] | [JSON](pos_l4q_b77.json) |
| `pp1_87w_hn3` | 孝惠 | [《史記・蕭相國世家》][35] | [JSON](pp1_87w_hn3.json) |
| `ppa_qmm_m9h` | 衛尉竭 | [《史記・秦始皇本紀》][6] | [JSON](ppa_qmm_m9h.json) |
| `ppa_vqy_d1e` | 周顯王（楚篇致胙者） | [《史記・楚世家》][22] | [JSON](ppa_vqy_d1e.json) |
| `pph_9jt_i6m` | 太后（趙世家孝成王新立未名者） | [《史記・趙世家》][25] | [JSON](pph_9jt_i6m.json) |
| `ppk_dnc_f2g` | 白公勝（楚亂記事） | [《史記・陳杞世家》][18] | [JSON](ppk_dnc_f2g.json) |
| `ppl_kwi_gwp` | 共尉 | [《史記・韓信盧綰列傳》][75] | [JSON](ppl_kwi_gwp.json) |
| `pr6_r4f_o9t` | 申徒狄引古 | [《史記・魯仲連鄒陽列傳》][65] | [JSON](pr6_r4f_o9t.json) |
| `psq_hux_tku` | 監止 | [《史記・齊太公世家》][14] | [JSON](psq_hux_tku.json) |
| `psw_5ck_539` | 項梁 | [《史記・魏豹彭越列傳》][72] | [JSON](psw_5ck_539.json) |
| `ptr_yh0_izm` | 韓終 | [《史記・秦始皇本紀》][6] | [JSON](ptr_yh0_izm.json) |
| `puc_9qz_obg` | 靳尚（楚懷王左右） | [《史記・楚世家》][22] | [JSON](puc_9qz_obg.json) |
| `puu_6hs_m4f` | 呂不韋 | [《史記・呂不韋列傳》][67] | [JSON](puu_6hs_m4f.json) |
| `pvp_ebv_zcb` | 宣太后 | [《史記・范睢蔡澤列傳》][61] | [JSON](pvp_ebv_zcb.json) |
| `pw5_1vd_2rt` | 趙襄王 | [《史記・樗里子甘茂列傳》][53] | [JSON](pw5_1vd_2rt.json) |
| `pwa_tqs_k31` | 秦繆公引古 | [《史記・廉頗藺相如列傳》][63] | [JSON](pwa_tqs_k31.json) |
| `pwg_394_bdd` | 昭明 | [《史記・殷本紀》][3] | [JSON](pwg_394_bdd.json) |
| `pwk_g11_hye` | 烈王 | [《史記・周本紀》][4] | [JSON](pwk_g11_hye.json) |
| `pwp_hh1_8da` | 蘇厲 | [《史記・蘇秦列傳》][51] | [JSON](pwp_hh1_8da.json) |
| `pwu_2l0_l7l` | 衞桓公 | [《史記・鄭世家》][24] | [JSON](pwu_2l0_l7l.json) |
| `pwx_jb9_qck` | 文祖 | [《史記・五帝本紀》][1] | [JSON](pwx_jb9_qck.json) |
| `px3_mrd_ys5` | 封鉅 | [《史記・孝武本紀》][12] | [JSON](px3_mrd_ys5.json) |
| `px3_yhj_4mg` | 秦王蘇代書信 | [《史記・蘇秦列傳》][51] | [JSON](px3_yhj_4mg.json) |
| `px7_dns_zoj` | 家仆徒（韓原右者） | [《史記・晉世家》][21] | [JSON](px7_dns_zoj.json) |
| `pxm_dwu_afr` | 膠西王太后未名 | [《史記・吳王濞列傳》][88] | [JSON](pxm_dwu_afr.json) |
| `py3_55c_1ad` | 郭隗 | [《史記・燕召公世家》][16] | [JSON](py3_55c_1ad.json) |
| `pyh_4xn_x4s` | 公夏首 | [《史記・仲尼弟子列傳》][49] | [JSON](pyh_4xn_x4s.json) |
| `pyt_ft7_8h4` | 曹窋 | [《史記・張丞相列傳》][78] | [JSON](pyt_ft7_8h4.json) |
| `pz6_lqa_ina` | 夏太后 | [《史記・秦始皇本紀》][6] | [JSON](pz6_lqa_ina.json) |
| `pzd_z9m_2de` | 鄂侯 | [《史記・殷本紀》][3] | [JSON](pzd_z9m_2de.json) |
| `pzh_osb_hmu` | 周文 | [《史記・張耳陳餘列傳》][71] | [JSON](pzh_osb_hmu.json) |
| `pzl_l3g_cu6` | 陳平 | [《史記・陳丞相世家》][38] | [JSON](pzl_l3g_cu6.json) |
| `pzm_tmt_z0y` | 夏徵舒（楚伐陳記事） | [《史記・陳杞世家》][18] | [JSON](pzm_tmt_z0y.json) |
| `pzz_h6y_gwp` | 太子（襄公卒後未名） | [《史記・魯周公世家》][15] | [JSON](pzz_h6y_gwp.json) |
| `q02_y8c_ljw` | 公子市 | [《史記・秦本紀》][5] | [JSON](q02_y8c_ljw.json) |
| `q0l_cnu_l8r` | 解福 | [《史記・樊酈滕灌列傳》][77] | [JSON](q0l_cnu_l8r.json) |
| `q10_w86_xi2` | 后稷 | [《史記・鄭世家》][24] | [JSON](q10_w86_xi2.json) |
| `q19_wxu_gyl` | 周將軍（楚） | [《史記・樊酈滕灌列傳》][77] | [JSON](q19_wxu_gyl.json) |
| `q1f_9q5_1ow` | 章邯 | [《史記・項羽本紀》][7] | [JSON](q1f_9q5_1ow.json) |
| `q1g_3v4_9ks` | 太史公 | [《史記・蒙恬列傳》][70] | [JSON](q1g_3v4_9ks.json) |
| `q1l_4by_ex6` | 欒布 | [《史記・楚元王世家》][32] | [JSON](q1l_4by_ex6.json) |
| `q1p_2kt_jve` | 蒲將軍 | [《史記・項羽本紀》][7] | [JSON](q1p_2kt_jve.json) |
| `q26_0h6_k7d` | 李齊 | [《史記・張釋之馮唐列傳》][84] | [JSON](q26_0h6_k7d.json) |
| `q29_h9w_sah` | 竇氏（文帝皇后） | [《史記・梁孝王世家》][40] | [JSON](q29_h9w_sah.json) |
| `q2q_a6e_9hs` | 雍齒 | [《史記・高祖本紀》][8] | [JSON](q2q_a6e_9hs.json) |
| `q2r_2vh_ic0` | 周最（本文讀法） | [《史記・周本紀》][4] | [JSON](q2r_2vh_ic0.json) |
| `q35_54a_f2z` | 趙悼襄王 | [《史記・燕召公世家》][16] | [JSON](q35_54a_f2z.json) |
| `q3n_t18_zql` | 秦始皇 | [《史記・白起王翦列傳》][55] | [JSON](q3n_t18_zql.json) |
| `q44_hia_lao` | 景翠 | [《史記・越王勾踐世家》][23] | [JSON](q44_hia_lao.json) |
| `q4a_jzq_0xh` | 李園（殺春申君者） | [《史記・春申君列傳》][60] | [JSON](q4a_jzq_0xh.json) |
| `q4s_qe2_uq2` | 齊湣王 | [《史記・韓世家》][27] | [JSON](q4s_qe2_uq2.json) |
| `q6j_g7r_on0` | 胤（出征者） | [《史記・夏本紀》][2] | [JSON](q6j_g7r_on0.json) |
| `q6l_n6t_fbt` | 卽墨大夫（田世家未名者） | [《史記・田敬仲完世家》][28] | [JSON](q6l_n6t_fbt.json) |
| `q6q_ax8_y9p` | 秦惠王 | [《史記・樗里子甘茂列傳》][53] | [JSON](q6q_ax8_y9p.json) |
| `q6w_xz2_x9x` | 蒯通 | [《史記・樂毅列傳》][62] | [JSON](q6w_xz2_x9x.json) |
| `q75_s04_chi` | 寵妾（衛州吁母） | [《史記・衛康叔世家》][19] | [JSON](q75_s04_chi.json) |
| `q78_d8z_wj2` | 樂臣公 | [《史記・樂毅列傳》][62] | [JSON](q78_d8z_wj2.json) |
| `q7p_z4x_qee` | 太子未具名 | [《史記・張釋之馮唐列傳》][84] | [JSON](q7p_z4x_qee.json) |
| `q7s_6hz_yak` | 少正卯 | [《史記・孔子世家》][29] | [JSON](q7s_6hz_yak.json) |
| `q7s_ogm_yr2` | 呂禮 | [《史記・孟嘗君列傳》][57] | [JSON](q7s_ogm_yr2.json) |
| `q7v_0kl_74r` | 楚相 | [《史記・張儀列傳》][52] | [JSON](q7v_0kl_74r.json) |
| `q83_hjg_lyd` | 御（宋成公弟） | [《史記・宋微子世家》][20] | [JSON](q83_hjg_lyd.json) |
| `q84_5hj_5q9` | 鄭朱 | [《史記・平原君虞卿列傳》][58] | [JSON](q84_5hj_5q9.json) |
| `q89_d6q_41w` | 監止 | [《史記・田敬仲完世家》][28] | [JSON](q89_d6q_41w.json) |
| `q8f_bos_spt` | 徐尚 | [《史記・陳涉世家》][30] | [JSON](q8f_bos_spt.json) |
| `q8m_d0c_kq3` | 楚莊王 | [《史記・楚世家》][22] | [JSON](q8m_d0c_kq3.json) |
| `q8p_lyu_m5n` | 智伯引古 | [《史記・范睢蔡澤列傳》][61] | [JSON](q8p_lyu_m5n.json) |
| `q8s_9ap_qhb` | 陳厲公 | [《史記・齊太公世家》][14] | [JSON](q8s_9ap_qhb.json) |
| `q98_n47_26l` | 他姬子廣陵王 | [《史記・外戚世家》][31] | [JSON](q98_n47_26l.json) |
| `q98_uzp_3g8` | 密姬 | [《史記・齊太公世家》][14] | [JSON](q98_uzp_3g8.json) |
| `q9f_hno_txx` | 常山守未名 | [《史記・韓信盧綰列傳》][75] | [JSON](q9f_hno_txx.json) |
| `q9h_7ls_c9r` | 屈丐 | [《史記・田敬仲完世家》][28] | [JSON](q9h_7ls_c9r.json) |
| `qa2_bme_epc` | 楚王戊 | [《史記・齊悼惠王世家》][34] | [JSON](qa2_bme_epc.json) |
| `qao_nbo_y9j` | 野（曹聲公） | [《史記・管蔡世家》][17] | [JSON](qao_nbo_y9j.json) |
| `qbd_5f1_qrr` | 信陵君 | [《史記・魏公子列傳》][59] | [JSON](qbd_5f1_qrr.json) |
| `qbg_2pe_t58` | 李牧 | [《史記・廉頗藺相如列傳》][63] | [JSON](qbg_2pe_t58.json) |
| `qbh_lsz_ipx` | 奇（棘蒲侯太子） | [《史記・孝文本紀》][10]、[《史記・袁盎鼂錯列傳》][83] | [JSON](qbh_lsz_ipx.json) |
| `qbl_dbr_jmj` | 范睢 | [《史記・范睢蔡澤列傳》][61] | [JSON](qbl_dbr_jmj.json) |
| `qbx_d2g_tda` | 息 | [《史記・三王世家》][42] | [JSON](qbx_d2g_tda.json) |
| `qbx_u8u_sch` | 趙午 | [《史記・田叔列傳》][86] | [JSON](qbx_u8u_sch.json) |
| `qco_jjb_gz1` | 懷（鄖公弟） | [《史記・楚世家》][22] | [JSON](qco_jjb_gz1.json) |
| `qcp_ou0_2g1` | 項羽 | [《史記・項羽本紀》][7] | [JSON](qcp_ou0_2g1.json) |
| `qcs_gl3_9g8` | 燕易王母 | [《史記・蘇秦列傳》][51] | [JSON](qcs_gl3_9g8.json) |
| `qdl_8tt_r4v` | 欒布 | [《史記・樊酈滕灌列傳》][77] | [JSON](qdl_8tt_r4v.json) |
| `qdr_5yn_8kr` | 陳餘 | [《史記・張耳陳餘列傳》][71] | [JSON](qdr_5yn_8kr.json) |
| `qe0_q7r_mlc` | 鄭國 | [《史記・仲尼弟子列傳》][49] | [JSON](qe0_q7r_mlc.json) |
| `qei_urq_n8p` | 光子乘羽 | [《史記・仲尼弟子列傳》][49] | [JSON](qei_urq_n8p.json) |
| `qej_ds3_yc4` | 武王 | [《史記・留侯世家》][37] | [JSON](qej_ds3_yc4.json) |
| `qep_rho_j32` | 負芻（末楚王） | [《史記・楚世家》][22] | [JSON](qep_rho_j32.json) |
| `qf1_qbc_81g` | 張春 | [《史記・韓信盧綰列傳》][75] | [JSON](qf1_qbc_81g.json) |
| `qff_r3w_1jo` | 魏媼 | [《史記・外戚世家》][31] | [JSON](qff_r3w_1jo.json) |
| `qfh_0ve_74z` | 太史公 | [《史記・樂毅列傳》][62] | [JSON](qfh_0ve_74z.json) |
| `qfk_7zb_jtn` | 龍且 | [《史記・曹相國世家》][36] | [JSON](qfk_7zb_jtn.json) |
| `qfu_p4d_ebc` | 張唐 | [《史記・秦本紀》][5] | [JSON](qfu_p4d_ebc.json) |
| `qfz_1hm_c5p` | 狄令未名 | [《史記・田儋列傳》][76] | [JSON](qfz_1hm_c5p.json) |
| `qg7_n12_fne` | 審食其 | [《史記・陳丞相世家》][38] | [JSON](qg7_n12_fne.json) |
| `qgn_r2c_qtv` | 簡狄 | [《史記・殷本紀》][3] | [JSON](qgn_r2c_qtv.json) |
| `qha_l8o_wxa` | 叔仲會 | [《史記・仲尼弟子列傳》][49] | [JSON](qha_l8o_wxa.json) |
| `qi8_m09_rfs` | 項羽 | [《史記・絳侯周勃世家》][39] | [JSON](qi8_m09_rfs.json) |
| `qj2_k5a_sq4` | 齊襄公 | [《史記・齊太公世家》][14] | [JSON](qj2_k5a_sq4.json) |
| `qj3_l69_xhu` | 周公黑肩 | [《史記・周本紀》][4] | [JSON](qj3_l69_xhu.json) |
| `qj3_rhh_t76` | 甯喜（衛臣） | [《史記・衛康叔世家》][19] | [JSON](qj3_rhh_t76.json) |
| `qjc_drk_933` | 奚容箴 | [《史記・仲尼弟子列傳》][49] | [JSON](qjc_drk_933.json) |
| `qjd_l2y_1nc` | 陳平 | [《史記・韓信盧綰列傳》][75] | [JSON](qjd_l2y_1nc.json) |
| `qje_fwa_r4b` | 祁午（祁傒子） | [《史記・晉世家》][21] | [JSON](qje_fwa_r4b.json) |
| `qji_mdf_7p6` | 田會 | [《史記・田敬仲完世家》][28] | [JSON](qji_mdf_7p6.json) |
| `qk9_ejk_fnc` | 洩父 | [《史記・周本紀》][4] | [JSON](qk9_ejk_fnc.json) |
| `qkg_mxc_rpe` | 大姬 | [《史記・孔子世家》][29] | [JSON](qkg_mxc_rpe.json) |
| `ql6_i85_646` | 御鞅 | [《史記・齊太公世家》][14] | [JSON](ql6_i85_646.json) |
| `qlb_dp8_dbu` | 叔向 | [《史記・趙世家》][25] | [JSON](qlb_dp8_dbu.json) |
| `qlj_fd6_5mz` | 鬼谷先生 | [《史記・張儀列傳》][52] | [JSON](qlj_fd6_5mz.json) |
| `qlq_xq2_1sm` | 御史大夫暴 | [《史記・田叔列傳》][86] | [JSON](qlq_xq2_1sm.json) |
| `qlu_yvc_mtu` | 許負 | [《史記・外戚世家》][31] | [JSON](qlu_yvc_mtu.json) |
| `qlv_q6m_tgs` | 呂不韋 | [《史記・李斯列傳》][69] | [JSON](qlv_q6m_tgs.json) |
| `qm1_2k5_hct` | 頎（晉孝公） | [《史記・晉世家》][21] | [JSON](qm1_2k5_hct.json) |
| `qms_rcb_628` | 王夫人兒姁 | [《史記・五宗世家》][41] | [JSON](qms_rcb_628.json) |
| `qmv_v0h_tbb` | 宋元公（內昭公議事） | [《史記・魯周公世家》][15] | [JSON](qmv_v0h_tbb.json) |
| `qn2_v9c_1mi` | 鞏朔（晉卿） | [《史記・晉世家》][21] | [JSON](qn2_v9c_1mi.json) |
| `qn5_cz0_l4x` | 鄒君引古未名 | [《史記・魯仲連鄒陽列傳》][65] | [JSON](qn5_cz0_l4x.json) |
| `qn9_spn_zzs` | 姚賈 | [《史記・老子韓非列傳》][45] | [JSON](qn9_spn_zzs.json) |
| `qna_m75_pj8` | 成王 | [《史記・魯周公世家》][15] | [JSON](qna_m75_pj8.json) |
| `qnn_6di_akv` | 宣伯 | [《史記・魯周公世家》][15] | [JSON](qnn_6di_akv.json) |
| `qnv_rb3_rx0` | 平公（燕共公後） | [《史記・燕召公世家》][16] | [JSON](qnv_rb3_rx0.json) |
| `qo2_3lx_e9d` | 周宣王 | [《史記・鄭世家》][24] | [JSON](qo2_3lx_e9d.json) |
| `qo2_xlt_6nu` | 環淵 | [《史記・孟子荀卿列傳》][56] | [JSON](qo2_xlt_6nu.json) |
| `qod_p13_dqs` | 秋（衛殤公） | [《史記・衛康叔世家》][19] | [JSON](qod_p13_dqs.json) |
| `qot_kkm_wa4` | 馮信 | [《史記・扁鵲倉公列傳》][87] | [JSON](qot_kkm_wa4.json) |
| `qou_l6b_mnc` | 執疵（越章王） | [《史記・楚世家》][22] | [JSON](qou_l6b_mnc.json) |
| `qow_wy0_7d2` | 鄧通 | [《史記・張丞相列傳》][78] | [JSON](qow_wy0_7d2.json) |
| `qpp_zx9_6a8` | 樗裏疾（楚篇合秦議者） | [《史記・楚世家》][22] | [JSON](qpp_zx9_6a8.json) |
| `qpw_pw5_eqn` | 屈原 | [《史記・屈原賈生列傳》][66] | [JSON](qpw_pw5_eqn.json) |
| `qpy_4ge_ve0` | 介子推（重耳從亡者） | [《史記・晉世家》][21] | [JSON](qpy_4ge_ve0.json) |
| `qqe_yxh_v49` | 常壽過（越大夫） | [《史記・楚世家》][22] | [JSON](qqe_yxh_v49.json) |
| `qqj_r6h_knh` | 伊引古短稱未定 | [《史記・魯仲連鄒陽列傳》][65] | [JSON](qqj_r6h_knh.json) |
| `qql_eij_rdk` | 皇父（宋司徒） | [《史記・魯周公世家》][15] | [JSON](qql_eij_rdk.json) |
| `qqr_l15_r9s` | 舜華 | [《史記・孔子世家》][29] | [JSON](qqr_l15_r9s.json) |
| `qqx_uyu_i1y` | 武王后 | [《史記・穰侯列傳》][54] | [JSON](qqx_uyu_i1y.json) |
| `qrh_7uu_bw4` | 劉禮 | [《史記・絳侯周勃世家》][39] | [JSON](qrh_7uu_bw4.json) |
| `qrk_ln3_p0h` | 禹 | [《史記・孟子荀卿列傳》][56] | [JSON](qrk_ln3_p0h.json) |
| `qrl_0tn_227` | 呂產女（恢后） | [《史記・呂太后本紀》][9] | [JSON](qrl_0tn_227.json) |
| `qs6_ntm_2ew` | 太史公 | [《史記・樊酈滕灌列傳》][77] | [JSON](qs6_ntm_2ew.json) |
| `qs9_zy4_2qs` | 顏祖 | [《史記・仲尼弟子列傳》][49] | [JSON](qs9_zy4_2qs.json) |
| `qsd_62h_s1a` | 賓須無（楚篇齊桓公輔） | [《史記・楚世家》][22] | [JSON](qsd_62h_s1a.json) |
| `qsj_qnd_c34` | 勃 | [《史記・五宗世家》][41] | [JSON](qsj_qnd_c34.json) |
| `qso_wkv_7aw` | 太史公 | [《史記・張耳陳餘列傳》][71] | [JSON](qso_wkv_7aw.json) |
| `qsp_sme_975` | 劇辛（燕將） | [《史記・燕召公世家》][16] | [JSON](qsp_sme_975.json) |
| `qtb_izn_j04` | 大將抵 | [《史記・絳侯周勃世家》][39] | [JSON](qtb_izn_j04.json) |
| `qtn_m4s_poh` | 不疑（孝惠後宮子稱） | [《史記・呂太后本紀》][9] | [JSON](qtn_m4s_poh.json) |
| `qto_bww_j2t` | 竇太后 | [《史記・梁孝王世家》][40] | [JSON](qto_bww_j2t.json) |
| `qtp_azl_g0w` | 秦嘉 | [《史記・項羽本紀》][7] | [JSON](qtp_azl_g0w.json) |
| `qug_x6h_3tb` | 卞莊子 | [《史記・張儀列傳》][52] | [JSON](qug_x6h_3tb.json) |
| `quo_167_x2v` | 田嬰 | [《史記・孟嘗君列傳》][57] | [JSON](quo_167_x2v.json) |
| `qup_ap8_dr6` | 范蠡陶朱公引古 | [《史記・范睢蔡澤列傳》][61] | [JSON](qup_ap8_dr6.json) |
| `qv2_833_5sf` | 公子糾引古 | [《史記・魯仲連鄒陽列傳》][65] | [JSON](qv2_833_5sf.json) |
| `qvb_bff_vk4` | 繆嬴（夷皋母） | [《史記・晉世家》][21] | [JSON](qvb_bff_vk4.json) |
| `qvb_gjo_odq` | 周宣王 | [《史記・楚世家》][22] | [JSON](qvb_gjo_odq.json) |
| `qvm_is4_7ub` | 伯夷 | [《史記・孟子荀卿列傳》][56] | [JSON](qvm_is4_7ub.json) |
| `qvv_4wo_748` | 趙襄子（殺知伯者） | [《史記・晉世家》][21] | [JSON](qvv_4wo_748.json) |
| `qw1_usz_nyt` | 鍼虎 | [《史記・秦本紀》][5] | [JSON](qw1_usz_nyt.json) |
| `qwm_l6t_ke6` | 太戊午 | [《史記・趙世家》][25] | [JSON](qwm_l6t_ke6.json) |
| `qxe_fr8_i1k` | 侍御史成 | [《史記・扁鵲倉公列傳》][87] | [JSON](qxe_fr8_i1k.json) |
| `qxu_jqe_evi` | 王武 | [《史記・曹相國世家》][36] | [JSON](qxu_jqe_evi.json) |
| `qy6_7i9_tgb` | 陳涉 | [《史記・田儋列傳》][76] | [JSON](qy6_7i9_tgb.json) |
| `qy6_uoo_bjf` | 中山君（魏世家相未名者） | [《史記・魏世家》][26] | [JSON](qy6_uoo_bjf.json) |
| `qyn_07y_0gt` | 趙同 | [《史記・袁盎鼂錯列傳》][83] | [JSON](qyn_07y_0gt.json) |
| `r01_ago_low` | 趙郝 | [《史記・平原君虞卿列傳》][58] | [JSON](r01_ago_low.json) |
| `r07_2q9_jzx` | 申差 | [《史記・韓世家》][27] | [JSON](r07_2q9_jzx.json) |
| `r07_7kq_kz5` | 趙旃（晉卿） | [《史記・晉世家》][21] | [JSON](r07_7kq_kz5.json) |
| `r0c_g3t_cbp` | 由余引古 | [《史記・李斯列傳》][69] | [JSON](r0c_g3t_cbp.json) |
| `r0d_t2p_zgq` | 薄皇后 | [《史記・外戚世家》][31] | [JSON](r0d_t2p_zgq.json) |
| `r0g_ulp_rps` | 奉車子侯（本卷未名） | [《史記・孝武本紀》][12] | [JSON](r0g_ulp_rps.json) |
| `r14_fgj_08p` | 楚悼王引古 | [《史記・范睢蔡澤列傳》][61] | [JSON](r14_fgj_08p.json) |
| `r1d_5m8_it7` | 烏獲 | [《史記・張儀列傳》][52] | [JSON](r1d_5m8_it7.json) |
| `r1o_twk_w6h` | 韓談 | [《史記・李斯列傳》][69] | [JSON](r1o_twk_w6h.json) |
| `r1p_b2x_kku` | 甯戚引古 | [《史記・魯仲連鄒陽列傳》][65] | [JSON](r1p_b2x_kku.json) |
| `r1r_ufk_7pb` | 楚昭王 | [《史記・孔子世家》][29] | [JSON](r1r_ufk_7pb.json) |
| `r21_e66_0v0` | 雍齒 | [《史記・陳丞相世家》][38] | [JSON](r21_e66_0v0.json) |
| `r2f_mtq_05s` | 魏冉 | [《史記・穰侯列傳》][54] | [JSON](r2f_mtq_05s.json) |
| `r2g_xfm_3ml` | 紂（引古） | [《史記・蒙恬列傳》][70] | [JSON](r2g_xfm_3ml.json) |
| `r2q_zyo_47q` | 紂 | [《史記・孫子吳起列傳》][47] | [JSON](r2q_zyo_47q.json) |
| `r2r_byo_ezj` | 孔悝 | [《史記・仲尼弟子列傳》][49] | [JSON](r2r_byo_ezj.json) |
| `r3c_eue_cqn` | 尉他 | [《史記・酈生陸賈列傳》][79] | [JSON](r3c_eue_cqn.json) |
| `r42_dd9_xyv` | 趙午 | [《史記・張耳陳餘列傳》][71] | [JSON](r42_dd9_xyv.json) |
| `r4c_ov4_t08` | 公西輿如 | [《史記・仲尼弟子列傳》][49] | [JSON](r4c_ov4_t08.json) |
| `r4g_c1v_yh0` | 高期 | [《史記・扁鵲倉公列傳》][87] | [JSON](r4g_c1v_yh0.json) |
| `r4u_mw5_3u3` | 太王 | [《史記・劉敬叔孫通列傳》][81] | [JSON](r4u_mw5_3u3.json) |
| `r4z_qa6_vhk` | 陳武 | [《史記・絳侯周勃世家》][39] | [JSON](r4z_qa6_vhk.json) |
| `r56_nsd_loo` | 獻公（燕簡公後） | [《史記・燕召公世家》][16] | [JSON](r56_nsd_loo.json) |
| `r5h_mrk_rov` | 成蟜 | [《史記・秦始皇本紀》][6] | [JSON](r5h_mrk_rov.json) |
| `r5i_kqz_a0i` | 趙既 | [《史記・樊酈滕灌列傳》][77] | [JSON](r5i_kqz_a0i.json) |
| `r5k_8ce_yre` | 齊襄王 | [《史記・田敬仲完世家》][28] | [JSON](r5k_8ce_yre.json) |
| `r5o_rck_hff` | 秦二世 | [《史記・劉敬叔孫通列傳》][81] | [JSON](r5o_rck_hff.json) |
| `r6c_fbu_uos` | 嬰 | [《史記・韓世家》][27] | [JSON](r6c_fbu_uos.json) |
| `r6o_knq_6a5` | 伍舉 | [《史記・伍子胥列傳》][48] | [JSON](r6o_knq_6a5.json) |
| `r6y_t2l_ntc` | 淮陰侯未詳名 | [《史記・張丞相列傳》][78] | [JSON](r6y_t2l_ntc.json) |
| `r7h_slc_6zt` | 戚夫人 | [《史記・呂太后本紀》][9] | [JSON](r7h_slc_6zt.json) |
| `r7t_6ys_2oo` | 成侯赤 | [《史記・孝文本紀》][10] | [JSON](r7t_6ys_2oo.json) |
| `r8b_5e8_6pj` | 荀卿 | [《史記・李斯列傳》][69] | [JSON](r8b_5e8_6pj.json) |
| `r8i_8gc_gvs` | 許由 | [《史記・伯夷列傳》][43] | [JSON](r8i_8gc_gvs.json) |
| `r97_1b3_zvn` | 高陵君顯 | [《史記・項羽本紀》][7] | [JSON](r97_1b3_zvn.json) |
| `r9f_r04_uk4` | 徐尚 | [《史記・秦始皇本紀》][6] | [JSON](r9f_r04_uk4.json) |
| `r9n_0vc_ywa` | 摢裏疾 | [《史記・樗里子甘茂列傳》][53] | [JSON](r9n_0vc_ywa.json) |
| `r9t_e2f_if5` | 皇欣 | [《史記・高祖本紀》][8] | [JSON](r9t_e2f_if5.json) |
| `raa_ahy_pza` | 子胥 | [《史記・張儀列傳》][52] | [JSON](raa_ahy_pza.json) |
| `rb3_2kn_s2q` | 石癸 | [《史記・鄭世家》][24] | [JSON](rb3_2kn_s2q.json) |
| `rbe_9wy_8fe` | 公西赤母 | [《史記・仲尼弟子列傳》][49] | [JSON](rbe_9wy_8fe.json) |
| `rbj_hsr_91v` | 扶蘇 | [《史記・陳涉世家》][30] | [JSON](rbj_hsr_91v.json) |
| `rbm_hun_lhl` | 公肩定 | [《史記・仲尼弟子列傳》][49] | [JSON](rbm_hun_lhl.json) |
| `rbn_65q_pnb` | 子貢 | [《史記・魯周公世家》][15] | [JSON](rbn_65q_pnb.json) |
| `rby_45j_475` | 豫讓妻未名 | [《史記・刺客列傳》][68] | [JSON](rby_45j_475.json) |
| `rcd_or9_g0a` | 公子荊（衞） | [《史記・吳太伯世家》][13] | [JSON](rcd_or9_g0a.json) |
| `rcf_f6n_ykv` | 公非 | [《史記・周本紀》][4] | [JSON](rcf_f6n_ykv.json) |
| `rcl_hpz_wh0` | 平原君夫人未名 | [《史記・魏公子列傳》][59] | [JSON](rcl_hpz_wh0.json) |
| `rcz_7hh_455` | 熙（魯煬公） | [《史記・魯周公世家》][15] | [JSON](rcz_7hh_455.json) |
| `rd1_5vy_m7g` | 子胥 | [《史記・越王勾踐世家》][23] | [JSON](rd1_5vy_m7g.json) |
| `rd5_bjt_8ed` | 炎帝 | [《史記・五帝本紀》][1] | [JSON](rd5_bjt_8ed.json) |
| `rd8_kwt_5iu` | 關龍逢（引古） | [《史記・蒙恬列傳》][70] | [JSON](rd8_kwt_5iu.json) |
| `rd8_urn_g2l` | 秦王政 | [《史記・秦始皇本紀》][6] | [JSON](rd8_urn_g2l.json) |
| `rdw_qwe_aa0` | 丞相哙未詳姓 | [《史記・傅靳蒯成列傳》][80] | [JSON](rdw_qwe_aa0.json) |
| `rec_qtq_9ve` | 司馬錯 | [《史記・秦本紀》][5] | [JSON](rec_qtq_9ve.json) |
| `rex_y36_0hj` | 李斯 | [《史記・孟子荀卿列傳》][56] | [JSON](rex_y36_0hj.json) |
| `rf6_xhq_gm3` | 范獻子（止平公自殺者） | [《史記・晉世家》][21] | [JSON](rf6_xhq_gm3.json) |
| `rfm_591_1ls` | 熊羆 | [《史記・五帝本紀》][1] | [JSON](rfm_591_1ls.json) |
| `rfo_sjy_tc6` | 后勝 | [《史記・秦始皇本紀》][6] | [JSON](rfo_sjy_tc6.json) |
| `rft_1rm_8b4` | 惠后 | [《史記・周本紀》][4] | [JSON](rft_1rm_8b4.json) |
| `rfv_455_l2f` | 被弒燕王（趙世家未名者） | [《史記・趙世家》][25] | [JSON](rfv_455_l2f.json) |
| `rg1_213_xlb` | 絳侯未詳名 | [《史記・酈生陸賈列傳》][79] | [JSON](rg1_213_xlb.json) |
| `rg9_4zo_6lu` | 輓父母（孔子世家郰人未名者） | [《史記・孔子世家》][29] | [JSON](rg9_4zo_6lu.json) |
| `rgr_7c1_3d1` | 顏刻 | [《史記・孔子世家》][29] | [JSON](rgr_7c1_3d1.json) |
| `rgy_07p_qo9` | 趙襄子 | [《史記・張儀列傳》][52] | [JSON](rgy_07p_qo9.json) |
| `rhi_qbz_3kh` | 廉絜 | [《史記・仲尼弟子列傳》][49] | [JSON](rhi_qbz_3kh.json) |
| `rhm_9nf_9q6` | 韓非 | [《史記・韓世家》][27] | [JSON](rhm_9nf_9q6.json) |
| `rhy_9fl_35p` | 龍賈 | [《史記・魏世家》][26] | [JSON](rhy_9fl_35p.json) |
| `rhz_4fw_u1u` | 今上未詳名 | [《史記・張丞相列傳》][78] | [JSON](rhz_4fw_u1u.json) |
| `ri1_1ov_ijz` | 晉頃公 | [《史記・韓世家》][27] | [JSON](ri1_1ov_ijz.json) |
| `ri2_8my_zxt` | 尾生所期女子 | [《史記・蘇秦列傳》][51] | [JSON](ri2_8my_zxt.json) |
| `ri4_ypz_y8z` | 聶政 | [《史記・刺客列傳》][68] | [JSON](ri4_ypz_y8z.json) |
| `rij_61e_5wf` | 秦商 | [《史記・仲尼弟子列傳》][49] | [JSON](rij_61e_5wf.json) |
| `rin_y2m_uyz` | 桓魋（宋司馬） | [《史記・宋微子世家》][20] | [JSON](rin_y2m_uyz.json) |
| `rjb_0hy_dsi` | 龍 | [《史記・五帝本紀》][1] | [JSON](rjb_0hy_dsi.json) |
| `rjw_tpy_t2f` | 絳短稱未定 | [《史記・屈原賈生列傳》][66] | [JSON](rjw_tpy_t2f.json) |
| `rk0_huv_709` | 中行偃（弒晉厲公記事） | [《史記・晉世家》][21] | [JSON](rk0_huv_709.json) |
| `rke_c0u_y8f` | 孝惠帝 | [《史記・傅靳蒯成列傳》][80] | [JSON](rke_c0u_y8f.json) |
| `rki_84e_ibd` | 番吾君（趙世家未名者） | [《史記・趙世家》][25] | [JSON](rki_84e_ibd.json) |
| `rkj_cs5_yob` | 魯句踐 | [《史記・刺客列傳》][68] | [JSON](rkj_cs5_yob.json) |
| `rkl_vgh_l0q` | 大鴻 | [《史記・五帝本紀》][1] | [JSON](rkl_vgh_l0q.json) |
| `rkn_3l3_3j3` | 褒姒 | [《史記・周本紀》][4] | [JSON](rkn_3l3_3j3.json) |
| `rku_4fv_h39` | 周太史（筮敬仲者未名） | [《史記・陳杞世家》][18] | [JSON](rku_4fv_h39.json) |
| `rky_s33_kuz` | 公西赤 | [《史記・仲尼弟子列傳》][49] | [JSON](rky_s33_kuz.json) |
| `rl7_3y6_td9` | 鄭高渠瞇 | [《史記・秦本紀》][5] | [JSON](rl7_3y6_td9.json) |
| `rlg_440_ab5` | 郎中令無擇 | [《史記・呂太后本紀》][9] | [JSON](rlg_440_ab5.json) |
| `rls_d4j_3x2` | 雍己 | [《史記・殷本紀》][3] | [JSON](rls_d4j_3x2.json) |
| `rm2_p1l_5a0` | 司城貞子 | [《史記・孔子世家》][29] | [JSON](rm2_p1l_5a0.json) |
| `rm7_r3k_g21` | 范文子（鄢陵晉臣） | [《史記・晉世家》][21] | [JSON](rm7_r3k_g21.json) |
| `rmu_iss_4in` | 王稽 | [《史記・范睢蔡澤列傳》][61] | [JSON](rmu_iss_4in.json) |
| `rmw_o1r_apv` | 秦將詐書者未名 | [《史記・張耳陳餘列傳》][71] | [JSON](rmw_o1r_apv.json) |
| `rn5_g2s_5hc` | 邵騷 | [《史記・張耳陳餘列傳》][71] | [JSON](rn5_g2s_5hc.json) |
| `rn7_nq0_gbl` | 叔仲（立嗣議事） | [《史記・魯周公世家》][15] | [JSON](rn7_nq0_gbl.json) |
| `rnc_beh_rpl` | 庶長朝 | [《史記・秦本紀》][5] | [JSON](rnc_beh_rpl.json) |
| `rnq_lt5_wgx` | 張黶 | [《史記・淮陰侯列傳》][74] | [JSON](rnq_lt5_wgx.json) |
| `ro0_0hy_dw9` | 都尉未名（守袁盎） | [《史記・袁盎鼂錯列傳》][83] | [JSON](ro0_0hy_dw9.json) |
| `ro3_15j_nvb` | 白起 | [《史記・白起王翦列傳》][55] | [JSON](ro3_15j_nvb.json) |
| `ro3_dr0_zwg` | 夫差 | [《史記・趙世家》][25] | [JSON](ro3_dr0_zwg.json) |
| `rop_352_k5s` | 楚威王 | [《史記・韓世家》][27] | [JSON](rop_352_k5s.json) |
| `roz_03s_y5n` | 金天氏 | [《史記・鄭世家》][24] | [JSON](roz_03s_y5n.json) |
| `rp7_jtw_344` | 漁父未名 | [《史記・屈原賈生列傳》][66] | [JSON](rp7_jtw_344.json) |
| `rpb_oth_6jb` | 施伯（魯人） | [《史記・魯周公世家》][15] | [JSON](rpb_oth_6jb.json) |
| `rpq_wnw_7p6` | 契（孔子世家詩傳說） | [《史記・孔子世家》][29] | [JSON](rpq_wnw_7p6.json) |
| `rpx_tx6_nuq` | 申黨 | [《史記・仲尼弟子列傳》][49] | [JSON](rpx_tx6_nuq.json) |
| `rq9_a9c_79b` | 張儀 | [《史記・屈原賈生列傳》][66] | [JSON](rq9_a9c_79b.json) |
| `rqi_av3_iy9` | 閻樂 | [《史記・秦始皇本紀》][6] | [JSON](rqi_av3_iy9.json) |
| `rqn_ani_vy5` | 高袪 | [《史記・張釋之馮唐列傳》][84] | [JSON](rqn_ani_vy5.json) |
| `rqv_zm4_apj` | 王蠋 | [《史記・田單列傳》][64] | [JSON](rqv_zm4_apj.json) |
| `rqz_7ra_6dw` | 屈固 | [《史記・伍子胥列傳》][48] | [JSON](rqz_7ra_6dw.json) |
| `rr9_kzs_uf6` | 亞父未詳名 | [《史記・項羽本紀》][7] | [JSON](rr9_kzs_uf6.json) |
| `rrg_m77_llr` | 泄公 | [《史記・張耳陳餘列傳》][71] | [JSON](rrg_m77_llr.json) |
| `rrj_dpd_03c` | 公孫固（宋大司馬） | [《史記・晉世家》][21] | [JSON](rrj_dpd_03c.json) |
| `rs1_k8n_bzl` | 莊賈 | [《史記・陳涉世家》][30] | [JSON](rs1_k8n_bzl.json) |
| `rs6_8vi_t6t` | 伍子胥 | [《史記・刺客列傳》][68] | [JSON](rs6_8vi_t6t.json) |
| `rsp_dwj_xp6` | 趙括母未名 | [《史記・廉頗藺相如列傳》][63] | [JSON](rsp_dwj_xp6.json) |
| `rta_39f_d5q` | 王陵 | [《史記・陳丞相世家》][38] | [JSON](rta_39f_d5q.json) |
| `rta_p7c_9tp` | 晉定公 | [《史記・晉世家》][21] | [JSON](rta_p7c_9tp.json) |
| `rtb_deo_xey` | 子良（楚莊王時鄭質子） | [《史記・楚世家》][22] | [JSON](rtb_deo_xey.json) |
| `ru1_bzw_3d6` | 田單 | [《史記・魯仲連鄒陽列傳》][65] | [JSON](ru1_bzw_3d6.json) |
| `ru3_ans_n12` | 樊噲 | [《史記・樊酈滕灌列傳》][77] | [JSON](ru3_ans_n12.json) |
| `rur_xf3_opk` | 太子母弟（昭公立時未名） | [《史記・魯周公世家》][15] | [JSON](rur_xf3_opk.json) |
| `ruz_4q7_qi2` | 軍正 | [《史記・司馬穰苴列傳》][46] | [JSON](ruz_4q7_qi2.json) |
| `rv0_y4t_8ew` | 塞王未詳名 | [《史記・樊酈滕灌列傳》][77] | [JSON](rv0_y4t_8ew.json) |
| `rv1_o3i_m12` | 田常 | [《史記・仲尼弟子列傳》][49] | [JSON](rv1_o3i_m12.json) |
| `rw2_ntu_kgz` | 內史保 | [《史記・絳侯周勃世家》][39] | [JSON](rw2_ntu_kgz.json) |
| `rwc_uls_sr7` | 御鞅 | [《史記・田敬仲完世家》][28] | [JSON](rwc_uls_sr7.json) |
| `rwg_skp_gbq` | 陳平（掾） | [《史記・張丞相列傳》][78] | [JSON](rwg_skp_gbq.json) |
| `rwn_9g8_fsv` | 張釋 | [《史記・呂太后本紀》][9] | [JSON](rwn_9g8_fsv.json) |
| `rwt_f3r_d8n` | 到滿 | [《史記・秦本紀》][5] | [JSON](rwt_f3r_d8n.json) |
| `rwy_xtw_1wg` | 孫武 | [《史記・吳太伯世家》][13] | [JSON](rwy_xtw_1wg.json) |
| `rwz_hdr_wfe` | 甘龍 | [《史記・商君列傳》][50] | [JSON](rwz_hdr_wfe.json) |
| `rx0_vif_1xq` | 陳餘 | [《史記・張耳陳餘列傳》][71] | [JSON](rx0_vif_1xq.json) |
| `rx1_qo2_g0z` | 淳于越 | [《史記・秦始皇本紀》][6] | [JSON](rx1_qo2_g0z.json) |
| `rx6_krw_dmb` | 向壽 | [《史記・樗里子甘茂列傳》][53] | [JSON](rx6_krw_dmb.json) |
| `rxn_o30_0j8` | 紂 | [《史記・留侯世家》][37] | [JSON](rxn_o30_0j8.json) |
| `rxt_koo_nas` | 陳豨 | [《史記・荊燕世家》][33] | [JSON](rxt_koo_nas.json) |
| `rz7_xfo_xse` | 田角 | [《史記・田儋列傳》][76] | [JSON](rz7_xfo_xse.json) |
| `rze_h3o_ds9` | 趙簡子 | [《史記・孔子世家》][29] | [JSON](rze_h3o_ds9.json) |
| `rzl_t6n_y63` | 黥布 | [《史記・傅靳蒯成列傳》][80] | [JSON](rzl_t6n_y63.json) |
| `rzu_4xv_cvs` | 俠累 | [《史記・韓世家》][27] | [JSON](rzu_4xv_cvs.json) |
| `rzv_0ll_3ty` | 烏獲 | [《史記・秦本紀》][5] | [JSON](rzv_0ll_3ty.json) |
| `s03_xve_mcm` | 老萊子 | [《史記・老子韓非列傳》][45] | [JSON](s03_xve_mcm.json) |
| `s07_jue_39p` | 章邯 | [《史記・黥布列傳》][73] | [JSON](s07_jue_39p.json) |
| `s0b_5z2_duo` | 秦泗川監平 | [《史記・高祖本紀》][8] | [JSON](s0b_5z2_duo.json) |
| `s0i_apu_j6d` | 樂頎 | [《史記・孔子世家》][29] | [JSON](s0i_apu_j6d.json) |
| `s0q_xk9_ho8` | 蒯通 | [《史記・田儋列傳》][76] | [JSON](s0q_xk9_ho8.json) |
| `s13_zwm_7o1` | 蕭何 | [《史記・酈生陸賈列傳》][79] | [JSON](s13_zwm_7o1.json) |
| `s1z_cdi_4i4` | 俞跗傳說引文候選 | [《史記・扁鵲倉公列傳》][87] | [JSON](s1z_cdi_4i4.json) |
| `s3a_ah3_epn` | 張羽 | [《史記・梁孝王世家》][40] | [JSON](s3a_ah3_epn.json) |
| `s3b_svm_zf2` | 先蔑（左行將） | [《史記・晉世家》][21] | [JSON](s3b_svm_zf2.json) |
| `s3i_wtz_ppu` | 吳太子 | [《史記・伍子胥列傳》][48] | [JSON](s3i_wtz_ppu.json) |
| `s3k_nnq_9e3` | 竇鳴犢 | [《史記・孔子世家》][29] | [JSON](s3k_nnq_9e3.json) |
| `s3t_6v0_13l` | 武王 | [《史記・商君列傳》][50] | [JSON](s3t_6v0_13l.json) |
| `s44_iy2_pf8` | 秦昭王 | [《史記・魏世家》][26] | [JSON](s44_iy2_pf8.json) |
| `s4g_oc3_eon` | 富丁 | [《史記・趙世家》][25] | [JSON](s4g_oc3_eon.json) |
| `s4y_bc6_4ay` | 簡王 | [《史記・周本紀》][4] | [JSON](s4y_bc6_4ay.json) |
| `s5o_lxl_fqe` | 項羽 | [《史記・曹相國世家》][36] | [JSON](s5o_lxl_fqe.json) |
| `s63_f1q_qe0` | 田臣思 | [《史記・田敬仲完世家》][28] | [JSON](s63_f1q_qe0.json) |
| `s6v_a1w_z3m` | 伍子胥（引古） | [《史記・韓信盧綰列傳》][75] | [JSON](s6v_a1w_z3m.json) |
| `s74_0jk_msn` | 召公（厲宣時） | [《史記・周本紀》][4] | [JSON](s74_0jk_msn.json) |
| `s7e_or3_oyt` | 韓宣惠王 | [《史記・留侯世家》][37] | [JSON](s7e_or3_oyt.json) |
| `s7q_qps_pba` | 仲行（子輿氏） | [《史記・秦本紀》][5] | [JSON](s7q_qps_pba.json) |
| `s7v_52b_lzt` | 暴鳶 | [《史記・秦本紀》][5] | [JSON](s7v_52b_lzt.json) |
| `s8f_9yk_r9y` | 太（平昌侯／濟川王） | [《史記・呂太后本紀》][9] | [JSON](s8f_9yk_r9y.json) |
| `s8f_r7z_fb9` | 晏圉 | [《史記・田敬仲完世家》][28] | [JSON](s8f_r7z_fb9.json) |
| `s8n_dgg_60b` | 絳侯未詳名 | [《史記・樊酈滕灌列傳》][77] | [JSON](s8n_dgg_60b.json) |
| `s94_frs_dd3` | 郅將軍（本卷稱呼） | [《史記・孝景本紀》][11] | [JSON](s94_frs_dd3.json) |
| `s9j_8ha_lfl` | 紀季 | [《史記・秦始皇本紀》][6] | [JSON](s9j_8ha_lfl.json) |
| `s9v_a49_lvg` | 王禹 | [《史記・扁鵲倉公列傳》][87] | [JSON](s9v_a49_lvg.json) |
| `sa0_w3e_z3k` | 太庚 | [《史記・殷本紀》][3] | [JSON](sa0_w3e_z3k.json) |
| `sa8_c1b_7dw` | 吳起母 | [《史記・孫子吳起列傳》][47] | [JSON](sa8_c1b_7dw.json) |
| `sac_peq_v1p` | 田解 | [《史記・田儋列傳》][76] | [JSON](sac_peq_v1p.json) |
| `sah_ey0_5lm` | 子義 | [《史記・趙世家》][25] | [JSON](sah_ey0_5lm.json) |
| `sai_s34_p2t` | 長萬 | [《史記・鄭世家》][24] | [JSON](sai_s34_p2t.json) |
| `sal_aqu_xun` | 蘇代初見燕王 | [《史記・蘇秦列傳》][51] | [JSON](sal_aqu_xun.json) |
| `sar_gso_hyw` | 欒枝（下軍將） | [《史記・晉世家》][21] | [JSON](sar_gso_hyw.json) |
| `sas_4gz_ch0` | 秦始皇帝 | [《史記・樗里子甘茂列傳》][53] | [JSON](sas_4gz_ch0.json) |
| `say_o5j_r3g` | 龐煖 | [《史記・趙世家》][25] | [JSON](say_o5j_r3g.json) |
| `saz_old_5fi` | 孟軻 | [《史記・孟子荀卿列傳》][56] | [JSON](saz_old_5fi.json) |
| `sba_huu_hk2` | 齊襄王 | [《史記・孟嘗君列傳》][57] | [JSON](sba_huu_hk2.json) |
| `sbf_boj_fhp` | 楚悼王 | [《史記・孫子吳起列傳》][47] | [JSON](sbf_boj_fhp.json) |
| `sbj_0xf_1ml` | 晉頃公 | [《史記・趙世家》][25] | [JSON](sbj_0xf_1ml.json) |
| `sbo_uaa_f2d` | 昌平君 | [《史記・秦始皇本紀》][6] | [JSON](sbo_uaa_f2d.json) |
| `sbr_lsz_xkh` | 申紀（楚篇齊臣） | [《史記・楚世家》][22] | [JSON](sbr_lsz_xkh.json) |
| `sc1_1r3_ts0` | 李園 | [《史記・春申君列傳》][60] | [JSON](sc1_1r3_ts0.json) |
| `sc7_m6w_634` | 魏豹 | [《史記・外戚世家》][31] | [JSON](sc7_m6w_634.json) |
| `sci_1hw_slc` | 曾參 | [《史記・袁盎鼂錯列傳》][83] | [JSON](sci_1hw_slc.json) |
| `sck_164_3hm` | 秦武王 | [《史記・穰侯列傳》][54] | [JSON](sck_164_3hm.json) |
| `scm_yn2_dzn` | 呂甥 | [《史記・晉世家》][21] | [JSON](scm_yn2_dzn.json) |
| `sd1_zvh_sby` | 渾沌 | [《史記・五帝本紀》][1] | [JSON](sd1_zvh_sby.json) |
| `sd2_qmy_yit` | 館豎子刺虎故事 | [《史記・張儀列傳》][52] | [JSON](sd2_qmy_yit.json) |
| `sd6_kzw_afm` | 鯫生（沛公所引） | [《史記・項羽本紀》][7] | [JSON](sd6_kzw_afm.json) |
| `sd8_6xr_wgg` | 髙偃（伐燕議事） | [《史記・燕召公世家》][16] | [JSON](sd8_6xr_wgg.json) |
| `sdj_vte_hhn` | 衛夫人 | [《史記・三王世家》][42] | [JSON](sdj_vte_hhn.json) |
| `sdm_4q5_qkw` | 騎劫 | [《史記・樂毅列傳》][62] | [JSON](sdm_4q5_qkw.json) |
| `sea_3dj_qak` | 隱公 | [《史記・孔子世家》][29] | [JSON](sea_3dj_qak.json) |
| `seb_ah3_ndx` | 淳于司馬未具名 | [《史記・扁鵲倉公列傳》][87] | [JSON](seb_ah3_ndx.json) |
| `seb_lin_831` | 陳勝 | [《史記・李斯列傳》][69] | [JSON](seb_lin_831.json) |
| `set_v0h_gnw` | 太史公 | [《史記・魏豹彭越列傳》][72] | [JSON](set_v0h_gnw.json) |
| `sf0_pwb_n3z` | 韓宣子 | [《史記・魏世家》][26] | [JSON](sf0_pwb_n3z.json) |
| `sf0_umg_486` | 呉廣 | [《史記・張耳陳餘列傳》][71] | [JSON](sf0_umg_486.json) |
| `sf6_0o6_mwx` | 釐公（燕湣公後） | [《史記・燕召公世家》][16] | [JSON](sf6_0o6_mwx.json) |
| `sf9_q7w_ymd` | 召平 | [《史記・蕭相國世家》][35] | [JSON](sf9_q7w_ymd.json) |
| `sfa_wwl_tt2` | 藺相如 | [《史記・廉頗藺相如列傳》][63] | [JSON](sfa_wwl_tt2.json) |
| `sfi_am6_zn4` | 徐夫人 | [《史記・刺客列傳》][68] | [JSON](sfi_am6_zn4.json) |
| `sgl_hjg_o48` | 公子卬 | [《史記・商君列傳》][50] | [JSON](sgl_hjg_o48.json) |
| `sha_lef_21n` | 常先 | [《史記・五帝本紀》][1] | [JSON](sha_lef_21n.json) |
| `shc_kdl_5w7` | 徐衍引古 | [《史記・魯仲連鄒陽列傳》][65] | [JSON](shc_kdl_5w7.json) |
| `shd_1wc_uva` | 蔡澤 | [《史記・范睢蔡澤列傳》][61] | [JSON](shd_1wc_uva.json) |
| `shg_xls_hq8` | 魯元公主 | [《史記・齊悼惠王世家》][34] | [JSON](shg_xls_hq8.json) |
| `shk_1za_du3` | 張耳 | [《史記・張丞相列傳》][78] | [JSON](shk_1za_du3.json) |
| `shn_ixr_kqt` | 申公 | [《史記・楚元王世家》][32] | [JSON](shn_ixr_kqt.json) |
| `si4_1zk_24j` | 劉舍 | [《史記・張丞相列傳》][78] | [JSON](si4_1zk_24j.json) |
| `sia_4uv_ddh` | 替代嬰兒（趙世家未名者） | [《史記・趙世家》][25] | [JSON](sia_4uv_ddh.json) |
| `sia_mjg_t9v` | 中山王（趙世家遷膚施未名者） | [《史記・趙世家》][25] | [JSON](sia_mjg_t9v.json) |
| `sif_3bc_k0b` | 公孫操 | [《史記・趙世家》][25] | [JSON](sif_3bc_k0b.json) |
| `sii_gh4_8vi` | 齊桓公 | [《史記・樗里子甘茂列傳》][53] | [JSON](sii_gh4_8vi.json) |
| `sj8_0u0_zdl` | 趙王舉平原未定 | [《史記・平原君虞卿列傳》][58] | [JSON](sj8_0u0_zdl.json) |
| `sj9_pfu_fwh` | 灌嬰 | [《史記・樊酈滕灌列傳》][77] | [JSON](sj9_pfu_fwh.json) |
| `sjb_oub_aik` | 薛公 | [《史記・黥布列傳》][73] | [JSON](sjb_oub_aik.json) |
| `sjh_rvy_vry` | 曾蒧 | [《史記・仲尼弟子列傳》][49] | [JSON](sjh_rvy_vry.json) |
| `sjs_nr4_k35` | 參胡（陸終次子） | [《史記・楚世家》][22] | [JSON](sjs_nr4_k35.json) |
| `sjw_0vl_axn` | 費中 | [《史記・殷本紀》][3] | [JSON](sjw_0vl_axn.json) |
| `sjy_up9_anz` | 項梁 | [《史記・陳涉世家》][30] | [JSON](sjy_up9_anz.json) |
| `sk4_hig_yhj` | 彊（齊公子質晉） | [《史記・齊太公世家》][14] | [JSON](sk4_hig_yhj.json) |
| `ski_kbw_ojw` | 郯子（齊桓公伐郯時） | [《史記・齊太公世家》][14] | [JSON](ski_kbw_ojw.json) |
| `sks_90w_uwt` | 偃（宋君） | [《史記・宋微子世家》][20] | [JSON](sks_90w_uwt.json) |
| `slb_gye_mot` | 原 | [《史記・鄭世家》][24] | [JSON](slb_gye_mot.json) |
| `slj_k2w_n4o` | 夏侯嬰 | [《史記・樊酈滕灌列傳》][77] | [JSON](slj_k2w_n4o.json) |
| `slm_sf2_yss` | 紀氏女 | [《史記・齊悼惠王世家》][34] | [JSON](slm_sf2_yss.json) |
| `sm1_q0n_pla` | 鄒之孤引古未名 | [《史記・魯仲連鄒陽列傳》][65] | [JSON](sm1_q0n_pla.json) |
| `smf_oqj_91f` | 王黃 | [《史記・荊燕世家》][33] | [JSON](smf_oqj_91f.json) |
| `smh_yhl_b8t` | 薄吾 | [《史記・扁鵲倉公列傳》][87] | [JSON](smh_yhl_b8t.json) |
| `smi_qcr_wtg` | 呂后 | [《史記・韓信盧綰列傳》][75] | [JSON](smi_qcr_wtg.json) |
| `smu_ylv_x6g` | 虞舜 | [《史記・趙世家》][25] | [JSON](smu_ylv_x6g.json) |
| `sn2_w9y_1ls` | 南宮括 | [《史記・周本紀》][4] | [JSON](sn2_w9y_1ls.json) |
| `sng_c8u_vn9` | 宰予 | [《史記・仲尼弟子列傳》][49] | [JSON](sng_c8u_vn9.json) |
| `snk_jy6_dgf` | 桓嬰 | [《史記・樊酈滕灌列傳》][77] | [JSON](snk_jy6_dgf.json) |
| `snv_pc0_zqe` | 鄂君 | [《史記・蕭相國世家》][35] | [JSON](snv_pc0_zqe.json) |
| `so1_ycw_xkv` | 欒布 | [《史記・孝文本紀》][10] | [JSON](so1_ycw_xkv.json) |
| `so8_5wd_zv6` | 燕君（趙世家子之為君時未名者） | [《史記・趙世家》][25] | [JSON](so8_5wd_zv6.json) |
| `sob_78r_4yi` | 揖（文帝子） | [《史記・孝文本紀》][10] | [JSON](sob_78r_4yi.json) |
| `soh_mp7_j16` | 荀林父（晉軍臣） | [《史記・晉世家》][21] | [JSON](soh_mp7_j16.json) |
| `sp8_b5m_c4b` | 益姑（杞文公） | [《史記・陳杞世家》][18] | [JSON](sp8_b5m_c4b.json) |
| `spf_7ot_c8s` | 陳渉 | [《史記・陳丞相世家》][38] | [JSON](spf_7ot_c8s.json) |
| `sph_y7q_7k9` | 周舍 | [《史記・趙世家》][25] | [JSON](sph_y7q_7k9.json) |
| `spo_czz_jlz` | 魏公子毋忌 | [《史記・張耳陳餘列傳》][71] | [JSON](spo_czz_jlz.json) |
| `sq3_9p2_9n3` | 敬王 | [《史記・周本紀》][4] | [JSON](sq3_9p2_9n3.json) |
| `sqb_xdi_hih` | 將行 | [《史記・三王世家》][42] | [JSON](sqb_xdi_hih.json) |
| `sqd_bzq_9qf` | 齊湣王 | [《史記・樂毅列傳》][62] | [JSON](sqd_bzq_9qf.json) |
| `sqf_hxb_q6t` | 張耳妻父客未名 | [《史記・張耳陳餘列傳》][71] | [JSON](sqf_hxb_q6t.json) |
| `sqj_ztt_459` | 薛澤 | [《史記・張丞相列傳》][78] | [JSON](sqj_ztt_459.json) |
| `sqk_n7e_eyk` | 膠東王未具名 | [《史記・萬石張叔列傳》][85] | [JSON](sqk_n7e_eyk.json) |
| `sqm_9mg_poc` | 許鈞 | [《史記・趙世家》][25] | [JSON](sqm_9mg_poc.json) |
| `sr6_5zr_1f3` | 龍且 | [《史記・高祖本紀》][8] | [JSON](sr6_5zr_1f3.json) |
| `srh_4ts_334` | 漢惠帝 | [《史記・張丞相列傳》][78] | [JSON](srh_4ts_334.json) |
| `ss6_lvt_mi1` | 秦御史 | [《史記・蕭相國世家》][35] | [JSON](ss6_lvt_mi1.json) |
| `ss9_tub_gzp` | 故濟北王阿母未名 | [《史記・扁鵲倉公列傳》][87] | [JSON](ss9_tub_gzp.json) |
| `ssp_whv_x4q` | 安期生 | [《史記・樂毅列傳》][62] | [JSON](ssp_whv_x4q.json) |
| `ssv_spo_859` | 羊勝 | [《史記・魯仲連鄒陽列傳》][65] | [JSON](ssv_spo_859.json) |
| `st2_0ng_tvo` | 樂巨公 | [《史記・田叔列傳》][86] | [JSON](st2_0ng_tvo.json) |
| `stm_voa_t08` | 共尉 | [《史記・荊燕世家》][33] | [JSON](stm_voa_t08.json) |
| `stp_bip_036` | 許章 | [《史記・曹相國世家》][36] | [JSON](stp_bip_036.json) |
| `sua_nwp_l10` | 柱天侯 | [《史記・曹相國世家》][36] | [JSON](sua_nwp_l10.json) |
| `suq_hns_wuy` | 韓成 | [《史記・留侯世家》][37] | [JSON](suq_hns_wuy.json) |
| `svc_81f_pkz` | 樂閒（昌國君） | [《史記・樂毅列傳》][62] | [JSON](svc_81f_pkz.json) |
| `svx_710_4bw` | 宰孔（周葵丘使者） | [《史記・晉世家》][21] | [JSON](svx_710_4bw.json) |
| `swf_ksm_2oo` | 宋雍氏女 | [《史記・鄭世家》][24] | [JSON](swf_ksm_2oo.json) |
| `sx2_wyn_nhr` | 穆王 | [《史記・周本紀》][4] | [JSON](sx2_wyn_nhr.json) |
| `sxb_x2z_83z` | 朱英 | [《史記・春申君列傳》][60] | [JSON](sxb_x2z_83z.json) |
| `sxx_7h5_sa5` | 施之常 | [《史記・仲尼弟子列傳》][49] | [JSON](sxx_7h5_sa5.json) |
| `sy5_s6h_9ex` | 鄭文公（重耳過國者） | [《史記・鄭世家》][24] | [JSON](sy5_s6h_9ex.json) |
| `sye_xwh_ac4` | 髙齕（齊臣） | [《史記・魯周公世家》][15] | [JSON](sye_xwh_ac4.json) |
| `syh_fxu_yad` | 薄昭 | [《史記・孝文本紀》][10] | [JSON](syh_fxu_yad.json) |
| `syn_6p6_j5m` | 酈寄 | [《史記・吳王濞列傳》][88] | [JSON](syn_6p6_j5m.json) |
| `syo_21l_kzx` | 曼丘臣 | [《史記・樊酈滕灌列傳》][77] | [JSON](syo_21l_kzx.json) |
| `syp_j9y_m2k` | 老子 | [《史記・外戚世家》][31] | [JSON](syp_j9y_m2k.json) |
| `syq_5uv_2me` | 散宜生 | [《史記・蕭相國世家》][35] | [JSON](syq_5uv_2me.json) |
| `syy_h2t_4ie` | 郤稱（邳鄭所列者） | [《史記・晉世家》][21] | [JSON](syy_h2t_4ie.json) |
| `sz3_vzm_j03` | 尾生 | [《史記・陳丞相世家》][38] | [JSON](sz3_vzm_j03.json) |
| `szm_m1e_tk3` | 秦相應侯 | [《史記・春申君列傳》][60] | [JSON](szm_m1e_tk3.json) |
| `t0l_25p_ekd` | 張儀 | [《史記・魏世家》][26] | [JSON](t0l_25p_ekd.json) |
| `t0n_23a_eiu` | 穰苴 | [《史記・絳侯周勃世家》][39] | [JSON](t0n_23a_eiu.json) |
| `t0t_f3v_4e2` | 御史大夫劫 | [《史記・秦始皇本紀》][6] | [JSON](t0t_f3v_4e2.json) |
| `t1l_80q_ezz` | 秦孝公 | [《史記・陳涉世家》][30] | [JSON](t1l_80q_ezz.json) |
| `t1n_om3_mux` | 平原趙君 | [《史記・平原君虞卿列傳》][58] | [JSON](t1n_om3_mux.json) |
| `t1o_7wt_c69` | 范吉射（攻趙鞅者） | [《史記・晉世家》][21] | [JSON](t1o_7wt_c69.json) |
| `t1w_zw1_4tj` | 菑川王未具名 | [《史記・扁鵲倉公列傳》][87] | [JSON](t1w_zw1_4tj.json) |
| `t2c_9za_jp3` | 田肯 | [《史記・高祖本紀》][8] | [JSON](t2c_9za_jp3.json) |
| `t2h_kfi_r1u` | 小子（晉小子侯） | [《史記・晉世家》][21] | [JSON](t2h_kfi_r1u.json) |
| `t2i_jjo_nr6` | 武公（周赧王遣說楚者） | [《史記・楚世家》][22] | [JSON](t2i_jjo_nr6.json) |
| `t2m_90g_lng` | 董安于 | [《史記・趙世家》][25] | [JSON](t2m_90g_lng.json) |
| `t2y_z4k_z0m` | 灌短稱未定 | [《史記・屈原賈生列傳》][66] | [JSON](t2y_z4k_z0m.json) |
| `t3i_7cb_8sn` | 司馬庚 | [《史記・韓世家》][27] | [JSON](t3i_7cb_8sn.json) |
| `t3y_v2v_ipe` | 中壬 | [《史記・殷本紀》][3] | [JSON](t3y_v2v_ipe.json) |
| `t42_s4d_p1c` | 嘉（趙丞相） | [《史記・孝景本紀》][11] | [JSON](t42_s4d_p1c.json) |
| `t4c_wnk_xx7` | 代王 | [《史記・張儀列傳》][52] | [JSON](t4c_wnk_xx7.json) |
| `t4f_4gt_n25` | 司徒（晉釐侯） | [《史記・晉世家》][21] | [JSON](t4f_4gt_n25.json) |
| `t4f_9pu_741` | 趙敬侯（滅晉記事） | [《史記・晉世家》][21] | [JSON](t4f_9pu_741.json) |
| `t4i_jir_a3t` | 周成王（引古） | [《史記・蒙恬列傳》][70] | [JSON](t4i_jir_a3t.json) |
| `t4l_gy5_dpj` | 趙同（被誅者） | [《史記・晉世家》][21] | [JSON](t4l_gy5_dpj.json) |
| `t4u_no9_s1q` | 啓 | [《史記・夏本紀》][2] | [JSON](t4u_no9_s1q.json) |
| `t59_hlv_ksa` | 仇牧（宋大夫） | [《史記・宋微子世家》][20] | [JSON](t59_hlv_ksa.json) |
| `t5c_bkc_aem` | 驪姬 | [《史記・趙世家》][25] | [JSON](t5c_bkc_aem.json) |
| `t5e_f83_p7l` | 太子未詳名 | [《史記・張丞相列傳》][78] | [JSON](t5e_f83_p7l.json) |
| `t5i_u1b_9w1` | 蘇厲 | [《史記・陳涉世家》][30] | [JSON](t5i_u1b_9w1.json) |
| `t5j_h0l_x87` | 倉海君 | [《史記・留侯世家》][37] | [JSON](t5j_h0l_x87.json) |
| `t5l_nxu_k7z` | 沃丁 | [《史記・殷本紀》][3] | [JSON](t5l_nxu_k7z.json) |
| `t5s_okc_gxg` | 周亞夫 | [《史記・絳侯周勃世家》][39] | [JSON](t5s_okc_gxg.json) |
| `t6k_vke_hya` | 周太史（楚昭王問赤雲者） | [《史記・楚世家》][22] | [JSON](t6k_vke_hya.json) |
| `t77_51t_vl7` | 韓申差 | [《史記・秦本紀》][5]、[《史記・張儀列傳》][52] | [JSON](t77_51t_vl7.json) |
| `t7i_qd8_pmb` | 蕭何 | [《史記・樊酈滕灌列傳》][77] | [JSON](t7i_qd8_pmb.json) |
| `t7k_3g1_qp3` | 塗山氏之女 | [《史記・夏本紀》][2] | [JSON](t7k_3g1_qp3.json) |
| `t7x_2x7_1fc` | 仲由（毀三桓城記事） | [《史記・仲尼弟子列傳》][49] | [JSON](t7x_2x7_1fc.json) |
| `t8b_b8w_pcn` | 國惠子 | [《史記・齊太公世家》][14] | [JSON](t8b_b8w_pcn.json) |
| `t8b_zxx_6ea` | 田駢 | [《史記・孟子荀卿列傳》][56] | [JSON](t8b_zxx_6ea.json) |
| `t8k_az0_xk2` | 魏惠王 | [《史記・孫子吳起列傳》][47] | [JSON](t8k_az0_xk2.json) |
| `t8t_xtf_6tp` | 傅豹 | [《史記・趙世家》][25] | [JSON](t8t_xtf_6tp.json) |
| `t90_dfp_2t1` | 項籍 | [《史記・萬石張叔列傳》][85] | [JSON](t90_dfp_2t1.json) |
| `t9r_yzu_a41` | 陳勝 | [《史記・陳涉世家》][30] | [JSON](t9r_yzu_a41.json) |
| `ta6_n0m_glj` | 太戊 | [《史記・殷本紀》][3] | [JSON](ta6_n0m_glj.json) |
| `tae_3uh_xsc` | 楚死事相張羽兄未名 | [《史記・吳王濞列傳》][88] | [JSON](tae_3uh_xsc.json) |
| `tal_mu5_li4` | 孟嘗君母未名 | [《史記・孟嘗君列傳》][57] | [JSON](tal_mu5_li4.json) |
| `taq_82s_0na` | 景公太子（田世家先卒未名者） | [《史記・田敬仲完世家》][28] | [JSON](taq_82s_0na.json) |
| `taw_n8v_eh1` | 中康 | [《史記・夏本紀》][2] | [JSON](taw_n8v_eh1.json) |
| `taz_6jd_auh` | 侯嬴 | [《史記・魏公子列傳》][59] | [JSON](taz_6jd_auh.json) |
| `tb2_zhz_mol` | 鐘離眛 | [《史記・項羽本紀》][7]、[《史記・高祖本紀》][8] | [JSON](tb2_zhz_mol.json) |
| `tba_8dy_6gi` | 太史公 | [《史記・三王世家》][42] | [JSON](tba_8dy_6gi.json) |
| `tbv_g3c_03d` | 唐眛 | [《史記・韓世家》][27] | [JSON](tbv_g3c_03d.json) |
| `tby_8vk_ybz` | 獻善馬者未名 | [《史記・孟子荀卿列傳》][56] | [JSON](tby_8vk_ybz.json) |
| `td7_pgx_t52` | 田文 | [《史記・范睢蔡澤列傳》][61] | [JSON](td7_pgx_t52.json) |
| `tdc_3s3_yak` | 重耳 | [《史記・越王勾踐世家》][23] | [JSON](tdc_3s3_yak.json) |
| `tdc_u89_vcd` | 獻謳者未名 | [《史記・孟子荀卿列傳》][56] | [JSON](tdc_u89_vcd.json) |
| `tdk_stf_mcl` | 越王引古未名 | [《史記・春申君列傳》][60] | [JSON](tdk_stf_mcl.json) |
| `tdm_363_0di` | 游（宋君） | [《史記・宋微子世家》][20] | [JSON](tdm_363_0di.json) |
| `tdu_jkc_cnu` | 呂祿女（後少帝皇后） | [《史記・呂太后本紀》][9] | [JSON](tdu_jkc_cnu.json) |
| `tdu_n2l_m4p` | 樂乘 | [《史記・樂毅列傳》][62] | [JSON](tdu_n2l_m4p.json) |
| `te1_972_sv6` | 陳平 | [《史記・陳丞相世家》][38] | [JSON](te1_972_sv6.json) |
| `teh_acc_5xb` | 葉公（救楚惠王者） | [《史記・楚世家》][22] | [JSON](teh_acc_5xb.json) |
| `ten_534_ssn` | 孔文子 | [《史記・孔子世家》][29] | [JSON](ten_534_ssn.json) |
| `tf4_u8e_55t` | 魏哆 | [《史記・趙世家》][25] | [JSON](tf4_u8e_55t.json) |
| `tfz_fnj_ejn` | 廉頗 | [《史記・廉頗藺相如列傳》][63] | [JSON](tfz_fnj_ejn.json) |
| `tgl_pzw_4ik` | 召忽 | [《史記・齊太公世家》][14] | [JSON](tgl_pzw_4ik.json) |
| `th9_jve_qre` | 田臧 | [《史記・陳涉世家》][30] | [JSON](th9_jve_qre.json) |
| `thb_vkl_7xq` | 尹潘 | [《史記・樊酈滕灌列傳》][77] | [JSON](thb_vkl_7xq.json) |
| `thg_zvp_v5y` | 戚夫人 | [《史記・呂太后本紀》][9] | [JSON](thg_zvp_v5y.json) |
| `thi_bqo_x8d` | 申包胥 | [《史記・伍子胥列傳》][48] | [JSON](thi_bqo_x8d.json) |
| `tib_iww_tkq` | 齊桓引古 | [《史記・屈原賈生列傳》][66] | [JSON](tib_iww_tkq.json) |
| `tic_otw_oo2` | 孔父（宋弒君記事） | [《史記・宋微子世家》][20] | [JSON](tic_otw_oo2.json) |
| `tid_ihl_36n` | 吳王夫差引古 | [《史記・范睢蔡澤列傳》][61] | [JSON](tid_ihl_36n.json) |
| `tik_tcq_8l1` | 魏襄王 | [《史記・張儀列傳》][52] | [JSON](tik_tcq_8l1.json) |
| `tin_46y_do7` | 魏相 | [《史記・張丞相列傳》][78] | [JSON](tin_46y_do7.json) |
| `tj3_uj7_2tc` | 齊明 | [《史記・陳涉世家》][30] | [JSON](tj3_uj7_2tc.json) |
| `tj9_mpe_fwt` | 田廣 | [《史記・酈生陸賈列傳》][79] | [JSON](tj9_mpe_fwt.json) |
| `tjg_uab_cmw` | 蔡女（陳文公妻、佗母） | [《史記・陳杞世家》][18] | [JSON](tjg_uab_cmw.json) |
| `tjk_5e2_wse` | 竇太后 | [《史記・梁孝王世家》][40] | [JSON](tjk_5e2_wse.json) |
| `tjx_q6x_kc7` | 墨翟 | [《史記・秦始皇本紀》][6] | [JSON](tjx_q6x_kc7.json) |
| `tk3_22k_8aq` | 妲己 | [《史記・外戚世家》][31] | [JSON](tk3_22k_8aq.json) |
| `tk5_g6e_rh8` | 淮南王未詳名 | [《史記・傅靳蒯成列傳》][80] | [JSON](tk5_g6e_rh8.json) |
| `tke_fad_hlp` | 哀姜 | [《史記・魯周公世家》][15] | [JSON](tke_fad_hlp.json) |
| `tks_56f_4ir` | 于定國 | [《史記・張丞相列傳》][78] | [JSON](tks_56f_4ir.json) |
| `tl9_dsb_r6q` | 白起 | [《史記・魏世家》][26] | [JSON](tl9_dsb_r6q.json) |
| `tlk_hmr_kra` | 朱房 | [《史記・陳涉世家》][30] | [JSON](tlk_hmr_kra.json) |
| `tlo_jrj_80q` | 壺叔（從亡賤臣） | [《史記・晉世家》][21] | [JSON](tlo_jrj_80q.json) |
| `tlt_5h1_n6y` | 太丁（湯子） | [《史記・殷本紀》][3] | [JSON](tlt_5h1_n6y.json) |
| `tmi_4aq_99e` | 襄公夫人王姬（宋弒昭記事） | [《史記・宋微子世家》][20] | [JSON](tmi_4aq_99e.json) |
| `tmz_gaj_scc` | 馮王孫（趙世家論贊引述者） | [《史記・趙世家》][25] | [JSON](tmz_gaj_scc.json) |
| `tnb_yrb_sgm` | 子西 | [《史記・孔子世家》][29] | [JSON](tnb_yrb_sgm.json) |
| `tnc_ag2_eej` | 曹丘生 | [《史記・季布欒布列傳》][82] | [JSON](tnc_ag2_eej.json) |
| `tne_qdd_8ct` | 華父督（宋弒君記事） | [《史記・宋微子世家》][20] | [JSON](tne_qdd_8ct.json) |
| `tnj_mx0_xgf` | 高后呂后 | [《史記・荊燕世家》][33] | [JSON](tnj_mx0_xgf.json) |
| `tod_lbz_fbe` | 絳侯未具名 | [《史記・袁盎鼂錯列傳》][83] | [JSON](tod_lbz_fbe.json) |
| `toi_62h_6fm` | 鄒衍（燕招賢記事） | [《史記・燕召公世家》][16] | [JSON](toi_62h_6fm.json) |
| `tp1_kws_nsp` | 智伯 | [《史記・酈生陸賈列傳》][79] | [JSON](tp1_kws_nsp.json) |
| `tpo_l9x_3k6` | 雍渠 | [《史記・孔子世家》][29] | [JSON](tpo_l9x_3k6.json) |
| `tpz_x3m_e0h` | 湯 | [《史記・殷本紀》][3] | [JSON](tpz_x3m_e0h.json) |
| `tq0_t3t_6i1` | 趙莊 | [《史記・趙世家》][25] | [JSON](tq0_t3t_6i1.json) |
| `tq2_jdt_200` | 楚懷王 | [《史記・張儀列傳》][52] | [JSON](tq2_jdt_200.json) |
| `tr1_c3f_b6q` | 橋牛 | [《史記・五帝本紀》][1] | [JSON](tr1_c3f_b6q.json) |
| `tr4_ynu_z9k` | 左成 | [《史記・周本紀》][4] | [JSON](tr4_ynu_z9k.json) |
| `trv_ybp_bes` | 呂娥姁 | [《史記・外戚世家》][31] | [JSON](trv_ybp_bes.json) |
| `trw_uc5_2fn` | 夜食客未名 | [《史記・孟嘗君列傳》][57] | [JSON](trw_uc5_2fn.json) |
| `ts3_cpa_655` | 公冶長 | [《史記・仲尼弟子列傳》][49] | [JSON](ts3_cpa_655.json) |
| `tsk_1dl_p70` | 孫子 | [《史記・魏世家》][26] | [JSON](tsk_1dl_p70.json) |
| `tsu_wyg_g69` | 段（楚篇鄭伯弟） | [《史記・楚世家》][22] | [JSON](tsu_wyg_g69.json) |
| `tt6_j7v_1k6` | 廬江王書信未名 | [《史記・吳王濞列傳》][88] | [JSON](tt6_j7v_1k6.json) |
| `tt9_rph_5c4` | 祿父 | [《史記・衛康叔世家》][19] | [JSON](tt9_rph_5c4.json) |
| `ttc_nht_1ih` | 呂后 | [《史記・袁盎鼂錯列傳》][83] | [JSON](ttc_nht_1ih.json) |
| `ttr_4h4_ofv` | 葛伯 | [《史記・殷本紀》][3] | [JSON](ttr_4h4_ofv.json) |
| `ttt_f6l_4dk` | 齊莊公 | [《史記・齊太公世家》][14] | [JSON](ttt_f6l_4dk.json) |
| `ttx_okj_hbd` | 桓王 | [《史記・周本紀》][4] | [JSON](ttx_okj_hbd.json) |
| `tua_sdl_ttd` | 大將軍光 | [《史記・三王世家》][42] | [JSON](tua_sdl_ttd.json) |
| `tup_apk_ufr` | 招（陳司徒） | [《史記・陳杞世家》][18] | [JSON](tup_apk_ufr.json) |
| `twa_vor_7j0` | 冉求 | [《史記・孔子世家》][29] | [JSON](twa_vor_7j0.json) |
| `twk_t4q_4oy` | 曹相國未名 | [《史記・樂毅列傳》][62] | [JSON](twk_t4q_4oy.json) |
| `txk_j5j_jty` | 景駒 | [《史記・留侯世家》][37] | [JSON](txk_j5j_jty.json) |
| `txm_ajy_ue2` | 伯嚭 | [《史記・仲尼弟子列傳》][49] | [JSON](txm_ajy_ue2.json) |
| `tym_v5p_rqb` | 曹參 | [《史記・齊悼惠王世家》][34] | [JSON](tym_v5p_rqb.json) |
| `tyq_61e_h7h` | 任鄙 | [《史記・范睢蔡澤列傳》][61] | [JSON](tyq_61e_h7h.json) |
| `tz2_ke2_7l1` | 宰（魯幽公） | [《史記・魯周公世家》][15] | [JSON](tz2_ke2_7l1.json) |
| `tzq_88y_69k` | 衛長公主 | [《史記・孝武本紀》][12] | [JSON](tzq_88y_69k.json) |
| `tzz_9l9_f83` | 王容 | [《史記・趙世家》][25] | [JSON](tzz_9l9_f83.json) |
| `u1j_dr2_488` | 潘尪（楚入鄭盟者） | [《史記・楚世家》][22] | [JSON](u1j_dr2_488.json) |
| `u23_jpf_vfr` | 秦始皇帝 | [《史記・范睢蔡澤列傳》][61] | [JSON](u23_jpf_vfr.json) |
| `u25_mhc_xap` | 楊喜 | [《史記・項羽本紀》][7] | [JSON](u25_mhc_xap.json) |
| `u2c_fe5_16n` | 唐勒 | [《史記・屈原賈生列傳》][66] | [JSON](u2c_fe5_16n.json) |
| `u2w_08q_du4` | 嘉（燕王） | [《史記・孝景本紀》][11] | [JSON](u2w_08q_du4.json) |
| `u39_e0i_cta` | 大廉 | [《史記・秦本紀》][5] | [JSON](u39_e0i_cta.json) |
| `u3e_wkp_awl` | 魏安釐王 | [《史記・高祖本紀》][8] | [JSON](u3e_wkp_awl.json) |
| `u3k_b05_ar4` | 魏文侯 | [《史記・田敬仲完世家》][28] | [JSON](u3k_b05_ar4.json) |
| `u3r_atd_rs4` | 孔子引古 | [《史記・范睢蔡澤列傳》][61] | [JSON](u3r_atd_rs4.json) |
| `u3z_lrd_8hy` | 張耳 | [《史記・白起王翦列傳》][55] | [JSON](u3z_lrd_8hy.json) |
| `u44_7c9_76m` | 燕太子丹（楚篇刺秦記事） | [《史記・刺客列傳》][68] | [JSON](u44_7c9_76m.json) |
| `u4n_65h_uqv` | 庶長奐 | [《史記・秦本紀》][5] | [JSON](u4n_65h_uqv.json) |
| `u4r_ktr_4qm` | 孫子 | [《史記・田敬仲完世家》][28] | [JSON](u4r_ktr_4qm.json) |
| `u4w_p3a_v09` | 吳起 | [《史記・孟子荀卿列傳》][56] | [JSON](u4w_p3a_v09.json) |
| `u5y_hy5_zv9` | 呂祿女（朱虛侯妻） | [《史記・呂太后本紀》][9] | [JSON](u5y_hy5_zv9.json) |
| `u60_ta3_108` | 郈昭伯 | [《史記・魯周公世家》][15] | [JSON](u60_ta3_108.json) |
| `u68_y0a_f8x` | 齊湣王 | [《史記・孟嘗君列傳》][57] | [JSON](u68_y0a_f8x.json) |
| `u7c_vw3_rqc` | 長妾（陳哀公留母） | [《史記・陳杞世家》][18] | [JSON](u7c_vw3_rqc.json) |
| `u7e_s3g_b9v` | 魏安釐王 | [《史記・魏公子列傳》][59] | [JSON](u7e_s3g_b9v.json) |
| `u7i_t8j_qye` | 發（夏王） | [《史記・夏本紀》][2] | [JSON](u7i_t8j_qye.json) |
| `u7n_hyp_nqf` | 孫臏 | [《史記・孫子吳起列傳》][47] | [JSON](u7n_hyp_nqf.json) |
| `u7o_pk8_4ra` | 楊干（悼公弟） | [《史記・晉世家》][21] | [JSON](u7o_pk8_4ra.json) |
| `u7v_btk_ix4` | 羅（孔氏宦者） | [《史記・衛康叔世家》][19] | [JSON](u7v_btk_ix4.json) |
| `u7w_vak_29r` | 周昌 | [《史記・張丞相列傳》][78] | [JSON](u7w_vak_29r.json) |
| `u8l_tag_llb` | 賈生（引文作者） | [《史記・秦始皇本紀》][6] | [JSON](u8l_tag_llb.json) |
| `u9a_v5a_08h` | 公叔 | [《史記・孫子吳起列傳》][47] | [JSON](u9a_v5a_08h.json) |
| `u9d_wjf_gyl` | 伯士 | [《史記・周本紀》][4] | [JSON](u9d_wjf_gyl.json) |
| `u9g_hel_37z` | 瑕（衛君） | [《史記・衛康叔世家》][19] | [JSON](u9g_hel_37z.json) |
| `u9r_its_tcv` | 齊明 | [《史記・秦始皇本紀》][6] | [JSON](u9r_its_tcv.json) |
| `ua9_ppz_afj` | 賈誼（附載姓名） | [《史記・秦始皇本紀》][6] | [JSON](ua9_ppz_afj.json) |
| `ua9_y2n_gay` | 公孫喜 | [《史記・秦本紀》][5] | [JSON](ua9_y2n_gay.json) |
| `uaj_1xw_87k` | 鮑生 | [《史記・蕭相國世家》][35] | [JSON](uaj_1xw_87k.json) |
| `uaj_dl7_7e4` | 王媼 | [《史記・高祖本紀》][8] | [JSON](uaj_dl7_7e4.json) |
| `uau_p7f_yfa` | 田常引古 | [《史記・李斯列傳》][69] | [JSON](uau_p7f_yfa.json) |
| `ub0_76o_vp6` | 薦髡客未名 | [《史記・孟子荀卿列傳》][56] | [JSON](ub0_76o_vp6.json) |
| `ub3_cl2_ez9` | 蔡澤御者未名 | [《史記・范睢蔡澤列傳》][61] | [JSON](ub3_cl2_ez9.json) |
| `ub5_3z9_j2d` | 桀 | [《史記・外戚世家》][31] | [JSON](ub5_3z9_j2d.json) |
| `ubr_cow_lxx` | 申豐（內昭公議事） | [《史記・魯周公世家》][15] | [JSON](ubr_cow_lxx.json) |
| `ubt_idy_jr8` | 公劉 | [《史記・周本紀》][4] | [JSON](ubt_idy_jr8.json) |
| `ubx_l5x_nk3` | 韓信 | [《史記・淮陰侯列傳》][74] | [JSON](ubx_l5x_nk3.json) |
| `uc6_slu_fup` | 蘇秦嫂 | [《史記・蘇秦列傳》][51] | [JSON](uc6_slu_fup.json) |
| `uc7_nlh_gy2` | 齊王（昭陽攻齊未名者） | [《史記・楚世家》][22] | [JSON](uc7_nlh_gy2.json) |
| `ucb_60l_f3r` | 公西葴 | [《史記・仲尼弟子列傳》][49] | [JSON](ucb_60l_f3r.json) |
| `ucb_cb1_qc0` | 田單 | [《史記・趙世家》][25] | [JSON](ucb_cb1_qc0.json) |
| `uce_o1a_usy` | 闔閭引古 | [《史記・范睢蔡澤列傳》][61] | [JSON](uce_o1a_usy.json) |
| `ucl_2oi_jyy` | 春申君引述 | [《史記・呂不韋列傳》][67] | [JSON](ucl_2oi_jyy.json) |
| `ud7_fy7_6vl` | 墨翟 | [《史記・孟子荀卿列傳》][56] | [JSON](ud7_fy7_6vl.json) |
| `udd_rob_10e` | 亳王 | [《史記・秦本紀》][5] | [JSON](udd_rob_10e.json) |
| `udo_oxl_psc` | 田常 | [《史記・田敬仲完世家》][28] | [JSON](udo_oxl_psc.json) |
| `udu_dyy_4wd` | 季布 | [《史記・季布欒布列傳》][82] | [JSON](udu_dyy_4wd.json) |
| `udv_t8d_js3` | 王襄 | [《史記・曹相國世家》][36] | [JSON](udv_t8d_js3.json) |
| `ue1_qha_ehn` | 趙文 | [《史記・趙世家》][25] | [JSON](ue1_qha_ehn.json) |
| `ueq_svp_knr` | 陳餘 | [《史記・田儋列傳》][76] | [JSON](ueq_svp_knr.json) |
| `ufz_ayn_ylh` | 魏成子 | [《史記・魏世家》][26] | [JSON](ufz_ayn_ylh.json) |
| `ug2_2v6_hbv` | 鄭安平 | [《史記・趙世家》][25] | [JSON](ug2_2v6_hbv.json) |
| `ug6_2ne_9hm` | 犀首書信 | [《史記・蘇秦列傳》][51] | [JSON](ug6_2ne_9hm.json) |
| `ug9_gi9_fvb` | 五大夫陵 | [《史記・白起王翦列傳》][55] | [JSON](ug9_gi9_fvb.json) |
| `ugq_ldt_klj` | 劇孟 | [《史記・袁盎鼂錯列傳》][83] | [JSON](ugq_ldt_klj.json) |
| `ugv_ua1_1vs` | 王黃 | [《史記・韓信盧綰列傳》][75] | [JSON](ugv_ua1_1vs.json) |
| `uhq_4sb_zzv` | 齊威（列國君主） | [《史記・秦本紀》][5]、[《史記・齊太公世家》][14]、[《史記・燕召公世家》][16]、[《史記・晉世家》][21] | [JSON](uhq_4sb_zzv.json) |
| `ui0_pob_f62` | 奉賜死使者未名 | [《史記・蒙恬列傳》][70] | [JSON](ui0_pob_f62.json) |
| `uik_lg2_lp8` | 卑梁大夫（吳楚邊童爭桑時） | [《史記・楚世家》][22] | [JSON](uik_lg2_lp8.json) |
| `uiz_ljv_jv9` | 華陽夫人姊未名 | [《史記・呂不韋列傳》][67] | [JSON](uiz_ljv_jv9.json) |
| `uj5_nzw_pnc` | 酈生 | [《史記・田儋列傳》][76] | [JSON](uj5_nzw_pnc.json) |
| `ujc_hbe_sle` | 庸職 | [《史記・齊太公世家》][14] | [JSON](ujc_hbe_sle.json) |
| `ujh_hyp_nxm` | 太史公署稱 | [《史記・吳王濞列傳》][88] | [JSON](ujh_hyp_nxm.json) |
| `ujq_cg1_bc8` | 田巴 | [《史記・魏豹彭越列傳》][72] | [JSON](ujq_cg1_bc8.json) |
| `uk3_s1y_7c7` | 呉回（楚篇祖系） | [《史記・楚世家》][22] | [JSON](uk3_s1y_7c7.json) |
| `uk8_q7t_7u9` | 廉頗 | [《史記・廉頗藺相如列傳》][63] | [JSON](uk8_q7t_7u9.json) |
| `ukp_lkb_cb5` | 主父偃 | [《史記・孝景本紀》][11] | [JSON](ukp_lkb_cb5.json) |
| `ul2_qk7_kpb` | 荊軻（楚篇刺秦記事） | [《史記・刺客列傳》][68] | [JSON](ul2_qk7_kpb.json) |
| `ula_gey_mz5` | 子玉 | [《史記・晉世家》][21] | [JSON](ula_gey_mz5.json) |
| `ula_wqu_naa` | 剛武侯（本卷稱呼） | [《史記・高祖本紀》][8] | [JSON](ula_wqu_naa.json) |
| `ulf_21j_keo` | 李由 | [《史記・傅靳蒯成列傳》][80] | [JSON](ulf_21j_keo.json) |
| `ull_jgp_wdx` | 孟舒 | [《史記・田叔列傳》][86] | [JSON](ull_jgp_wdx.json) |
| `ulx_s90_lom` | 丁夫人（方祠者） | [《史記・孝武本紀》][12] | [JSON](ulx_s90_lom.json) |
| `um1_nbo_c79` | 梁氏女（斑所說） | [《史記・魯周公世家》][15] | [JSON](um1_nbo_c79.json) |
| `umv_4mq_7sy` | 神君（長陵女子敘事） | [《史記・孝武本紀》][12] | [JSON](umv_4mq_7sy.json) |
| `un2_jcz_dkt` | 臧荼 | [《史記・樊酈滕灌列傳》][77] | [JSON](un2_jcz_dkt.json) |
| `un4_kak_hvp` | 梅鋗 | [《史記・高祖本紀》][8] | [JSON](un4_kak_hvp.json) |
| `uni_tuw_ndh` | 商君 | [《史記・孟子荀卿列傳》][56] | [JSON](uni_tuw_ndh.json) |
| `uo0_7bg_poy` | 公子刻 | [《史記・趙世家》][25] | [JSON](uo0_7bg_poy.json) |
| `uo2_h90_033` | 郎署長未名 | [《史記・袁盎鼂錯列傳》][83] | [JSON](uo2_h90_033.json) |
| `uol_spz_cq8` | 女子豎 | [《史記・扁鵲倉公列傳》][87] | [JSON](uol_spz_cq8.json) |
| `uon_qea_38x` | 里克 | [《史記・晉世家》][21] | [JSON](uon_qea_38x.json) |
| `uos_ju4_dzr` | 御史大夫德 | [《史記・秦始皇本紀》][6] | [JSON](uos_ju4_dzr.json) |
| `uoy_51x_n1t` | 晉鄙 | [《史記・魏公子列傳》][59] | [JSON](uoy_51x_n1t.json) |
| `upk_0j8_ffk` | 外黃徐子 | [《史記・魏世家》][26] | [JSON](upk_0j8_ffk.json) |
| `upp_fxr_c4e` | 項橐 | [《史記・樗里子甘茂列傳》][53] | [JSON](upp_fxr_c4e.json) |
| `upt_y7g_i6w` | 駟鈞 | [《史記・齊悼惠王世家》][34] | [JSON](upt_y7g_i6w.json) |
| `upx_wco_6uv` | 齊懿仲（欲妻敬仲者） | [《史記・田敬仲完世家》][28] | [JSON](upx_wco_6uv.json) |
| `uq6_74z_vtv` | 張儀 | [《史記・張儀列傳》][52] | [JSON](uq6_74z_vtv.json) |
| `uqb_kzh_4me` | 靳尚 | [《史記・屈原賈生列傳》][66] | [JSON](uqb_kzh_4me.json) |
| `uqj_7pn_biu` | 鄭桓公（初封記事） | [《史記・燕召公世家》][16] | [JSON](uqj_7pn_biu.json) |
| `uqv_78v_j7w` | 晁錯 | [《史記・楚元王世家》][32] | [JSON](uqv_78v_j7w.json) |
| `ur3_6rb_cp2` | 趙王遷母未名 | [《史記・張釋之馮唐列傳》][84] | [JSON](ur3_6rb_cp2.json) |
| `ura_fdp_bzb` | 楚先君善秦未定 | [《史記・春申君列傳》][60] | [JSON](ura_fdp_bzb.json) |
| `urg_hxe_47l` | 虞胡公 | [《史記・孔子世家》][29] | [JSON](urg_hxe_47l.json) |
| `urm_n3z_r4o` | 鉏商 | [《史記・孔子世家》][29] | [JSON](urm_n3z_r4o.json) |
| `us4_wc1_gnr` | 奚齊 | [《史記・鄭世家》][24] | [JSON](us4_wc1_gnr.json) |
| `usb_mt6_egg` | 史舉 | [《史記・樗里子甘茂列傳》][53] | [JSON](usb_mt6_egg.json) |
| `usk_ybs_z1y` | 桓子（田文子對話稱） | [《史記・齊太公世家》][14] | [JSON](usk_ybs_z1y.json) |
| `uss_tkl_hqe` | 管至父 | [《史記・鄭世家》][24] | [JSON](uss_tkl_hqe.json) |
| `usu_jat_0ky` | 燕王喜 | [《史記・燕召公世家》][16] | [JSON](usu_jat_0ky.json) |
| `usv_vhb_ltw` | 孝公（燕獻公後） | [《史記・燕召公世家》][16] | [JSON](usv_vhb_ltw.json) |
| `ut1_rtj_ckz` | 楚惠王 | [《史記・伍子胥列傳》][48] | [JSON](ut1_rtj_ckz.json) |
| `utj_s5y_tae` | 毛叔鄭 | [《史記・周本紀》][4] | [JSON](utj_s5y_tae.json) |
| `uum_4gg_y9d` | 春申君 | [《史記・春申君列傳》][60] | [JSON](uum_4gg_y9d.json) |
| `uvb_oh6_dx1` | 平津侯 | [《史記・三王世家》][42] | [JSON](uvb_oh6_dx1.json) |
| `uvj_ezk_crm` | 武臣姊未名 | [《史記・張耳陳餘列傳》][71] | [JSON](uvj_ezk_crm.json) |
| `uw3_qbv_8o0` | 義渠君 | [《史記・張儀列傳》][52] | [JSON](uw3_qbv_8o0.json) |
| `uw6_a0a_tjp` | 范增 | [《史記・項羽本紀》][7] | [JSON](uw6_a0a_tjp.json) |
| `uw8_ozw_5ux` | 齊太史少弟（復書獲免未名） | [《史記・齊太公世家》][14] | [JSON](uw8_ozw_5ux.json) |
| `uwb_l4e_1vn` | 武王 | [《史記・蘇秦列傳》][51] | [JSON](uwb_l4e_1vn.json) |
| `ux0_nvd_s8f` | 韓太子奐 | [《史記・秦本紀》][5] | [JSON](ux0_nvd_s8f.json) |
| `ux3_la0_38d` | 魯昭公夫人孟子 | [《史記・仲尼弟子列傳》][49] | [JSON](ux3_la0_38d.json) |
| `uxa_zs4_qpz` | 秦武王 | [《史記・韓世家》][27] | [JSON](uxa_zs4_qpz.json) |
| `uxv_exs_5k3` | 項冠 | [《史記・樊酈滕灌列傳》][77] | [JSON](uxv_exs_5k3.json) |
| `uxv_pg9_8rm` | 伯夷（舜時） | [《史記・五帝本紀》][1] | [JSON](uxv_pg9_8rm.json) |
| `uxz_hc8_v82` | 紀太后 | [《史記・齊悼惠王世家》][34] | [JSON](uxz_hc8_v82.json) |
| `uy0_hf3_44x` | 孟說 | [《史記・秦本紀》][5] | [JSON](uy0_hf3_44x.json) |
| `uy6_2ye_ba8` | 梁嬰父 | [《史記・趙世家》][25] | [JSON](uy6_2ye_ba8.json) |
| `uy7_vln_q60` | 曾參 | [《史記・蘇秦列傳》][51] | [JSON](uy7_vln_q60.json) |
| `uya_dno_ycg` | 威公（西周） | [《史記・周本紀》][4] | [JSON](uya_dno_ycg.json) |
| `uyb_9er_yx7` | 平原君未詳名 | [《史記・樊酈滕灌列傳》][77] | [JSON](uyb_9er_yx7.json) |
| `uyh_nd0_h9q` | 樂閒 | [《史記・趙世家》][25] | [JSON](uyh_nd0_h9q.json) |
| `uz9_8ps_vl5` | 鮑子 | [《史記・齊太公世家》][14] | [JSON](uz9_8ps_vl5.json) |
| `uzb_sfw_uqg` | 竇嬰 | [《史記・梁孝王世家》][40] | [JSON](uzb_sfw_uqg.json) |
| `uzn_i73_sy0` | 公孫杵臼 | [《史記・趙世家》][25] | [JSON](uzn_i73_sy0.json) |
| `v01_cr0_1bz` | 涇陽君 | [《史記・范睢蔡澤列傳》][61] | [JSON](v01_cr0_1bz.json) |
| `v0a_dlz_n5l` | 辰嬴（公子樂母） | [《史記・晉世家》][21] | [JSON](v0a_dlz_n5l.json) |
| `v0e_wn2_9y3` | 御者妻 | [《史記・管晏列傳》][44] | [JSON](v0e_wn2_9y3.json) |
| `v0m_yso_2h1` | 趙堯 | [《史記・韓信盧綰列傳》][75] | [JSON](v0m_yso_2h1.json) |
| `v0s_cot_5c5` | 田閒 | [《史記・田儋列傳》][76] | [JSON](v0s_cot_5c5.json) |
| `v0z_zyj_fu7` | 王后未名 | [《史記・扁鵲倉公列傳》][87] | [JSON](v0z_zyj_fu7.json) |
| `v11_x4e_ll7` | 商容引古 | [《史記・樂毅列傳》][62] | [JSON](v11_x4e_ll7.json) |
| `v14_tbx_p17` | 侯公 | [《史記・秦始皇本紀》][6] | [JSON](v14_tbx_p17.json) |
| `v1j_kao_7o7` | 熙（宋煬公） | [《史記・宋微子世家》][20] | [JSON](v1j_kao_7o7.json) |
| `v2h_v2x_1au` | 國惠子 | [《史記・田敬仲完世家》][28] | [JSON](v2h_v2x_1au.json) |
| `v2q_x8x_vdu` | 德侯子 | [《史記・楚元王世家》][32] | [JSON](v2q_x8x_vdu.json) |
| `v35_hyj_z4u` | 高傒 | [《史記・齊太公世家》][14] | [JSON](v35_hyj_z4u.json) |
| `v3e_767_ofn` | 蘇秦（楚篇約從者） | [《史記・楚世家》][22] | [JSON](v3e_767_ofn.json) |
| `v3p_uo6_w9s` | 蔡女（田世家厲公妻未名者） | [《史記・田敬仲完世家》][28] | [JSON](v3p_uo6_w9s.json) |
| `v3z_8l6_18t` | 公孫頎 | [《史記・魏世家》][26] | [JSON](v3z_8l6_18t.json) |
| `v41_yc5_b1j` | 齊王（魏世家甄會未名者） | [《史記・魏世家》][26] | [JSON](v41_yc5_b1j.json) |
| `v4i_ole_ea2` | 陳涉 | [《史記・留侯世家》][37] | [JSON](v4i_ole_ea2.json) |
| `v4m_7yp_xr3` | 楊熊 | [《史記・高祖本紀》][8] | [JSON](v4m_7yp_xr3.json) |
| `v4x_3qx_dy7` | 弓高侯穨當 | [《史記・吳王濞列傳》][88] | [JSON](v4x_3qx_dy7.json) |
| `v58_qtu_ger` | 齊景公 | [《史記・伍子胥列傳》][48] | [JSON](v58_qtu_ger.json) |
| `v5p_vbx_b25` | 魯君（孔子世家適周未名者） | [《史記・孔子世家》][29] | [JSON](v5p_vbx_b25.json) |
| `v5q_7pq_o70` | 嘉（江都丞相） | [《史記・孝景本紀》][11] | [JSON](v5q_7pq_o70.json) |
| `v64_zpv_387` | 鄭靈公 | [《史記・鄭世家》][24] | [JSON](v64_zpv_387.json) |
| `v6g_qb4_d96` | 華陽太后 | [《史記・秦始皇本紀》][6] | [JSON](v6g_qb4_d96.json) |
| `v6j_2xb_7i5` | 不窋 | [《史記・周本紀》][4] | [JSON](v6j_2xb_7i5.json) |
| `v6t_g69_7z5` | 夫差引古 | [《史記・屈原賈生列傳》][66] | [JSON](v6t_g69_7z5.json) |
| `v6z_ixw_j69` | 周天子 | [《史記・蘇秦列傳》][51] | [JSON](v6z_ixw_j69.json) |
| `v72_15y_ze8` | 趙何 | [《史記・趙世家》][25] | [JSON](v72_15y_ze8.json) |
| `v7p_b12_9nv` | 冉季 | [《史記・仲尼弟子列傳》][49] | [JSON](v7p_b12_9nv.json) |
| `v7s_dh4_n43` | 子良 | [《史記・穰侯列傳》][54] | [JSON](v7s_dh4_n43.json) |
| `v7t_9j0_gec` | 白起 | [《史記・白起王翦列傳》][55] | [JSON](v7t_9j0_gec.json) |
| `v89_58y_qe2` | 燕太子丹 | [《史記・刺客列傳》][68] | [JSON](v89_58y_qe2.json) |
| `v8l_ue6_un4` | 弦高 | [《史記・秦本紀》][5]、[《史記・晉世家》][21] | [JSON](v8l_ue6_un4.json) |
| `v8n_5n1_mxh` | 伍子胥（引古） | [《史記・蒙恬列傳》][70] | [JSON](v8n_5n1_mxh.json) |
| `v8p_pcs_28s` | 聲子（惠公妾） | [《史記・魯周公世家》][15] | [JSON](v8p_pcs_28s.json) |
| `v8v_2nz_wdy` | 韓信 | [《史記・淮陰侯列傳》][74] | [JSON](v8v_2nz_wdy.json) |
| `v8y_9sc_cso` | 簡公（燕平公後） | [《史記・燕召公世家》][16] | [JSON](v8y_9sc_cso.json) |
| `v94_2qu_ypp` | 公皙哀 | [《史記・仲尼弟子列傳》][49] | [JSON](v94_2qu_ypp.json) |
| `v9c_s4n_l8v` | 鄡單 | [《史記・仲尼弟子列傳》][49] | [JSON](v9c_s4n_l8v.json) |
| `v9o_9nn_wtg` | 窮奇 | [《史記・五帝本紀》][1] | [JSON](v9o_9nn_wtg.json) |
| `va0_zp5_6o9` | 昭魚 | [《史記・韓世家》][27] | [JSON](va0_zp5_6o9.json) |
| `vaf_6kj_3ee` | 槍 | [《史記・趙世家》][25] | [JSON](vaf_6kj_3ee.json) |
| `val_3ij_gm1` | 趙梁 | [《史記・趙世家》][25] | [JSON](val_3ij_gm1.json) |
| `vam_8kp_5bj` | 太幾 | [《史記・秦本紀》][5] | [JSON](vam_8kp_5bj.json) |
| `vax_w2r_0za` | 孫武 | [《史記・孫子吳起列傳》][47] | [JSON](vax_w2r_0za.json) |
| `vb0_0su_3ys` | 芒卯 | [《史記・穰侯列傳》][54] | [JSON](vb0_0su_3ys.json) |
| `vbv_64z_to1` | 項處 | [《史記・扁鵲倉公列傳》][87] | [JSON](vbv_64z_to1.json) |
| `vch_9iv_gip` | 平皋侯（項氏） | [《史記・項羽本紀》][7] | [JSON](vch_9iv_gip.json) |
| `vcv_x4a_x4s` | 太師（微子問去留者） | [《史記・宋微子世家》][20] | [JSON](vcv_x4a_x4s.json) |
| `vcx_92m_gj6` | 劉賈 | [《史記・荊燕世家》][33] | [JSON](vcx_92m_gj6.json) |
| `ve4_anx_qmk` | 蘇射 | [《史記・趙世家》][25] | [JSON](ve4_anx_qmk.json) |
| `ve8_hyx_yae` | 顏氏女（孔子世家母未名者） | [《史記・孔子世家》][29] | [JSON](ve8_hyx_yae.json) |
| `vfg_p2z_8kc` | 敬康 | [《史記・五帝本紀》][1] | [JSON](vfg_p2z_8kc.json) |
| `vfk_f6j_nf3` | 丞相平 | [《史記・齊悼惠王世家》][34] | [JSON](vfk_f6j_nf3.json) |
| `vg4_1z7_894` | 唐姬 | [《史記・五宗世家》][41] | [JSON](vg4_1z7_894.json) |
| `vgh_vi1_iy2` | 曹參 | [《史記・外戚世家》][31] | [JSON](vgh_vi1_iy2.json) |
| `vgn_ry9_ujs` | 留侯 | [《史記・魏豹彭越列傳》][72] | [JSON](vgn_ry9_ujs.json) |
| `vh3_zps_tus` | 齊釐公（楚篇桓公父） | [《史記・齊太公世家》][14] | [JSON](vh3_zps_tus.json) |
| `vhq_7q6_k1o` | 吳王未具名 | [《史記・扁鵲倉公列傳》][87] | [JSON](vhq_7q6_k1o.json) |
| `vht_3iv_u7e` | 周成王 | [《史記・鄭世家》][24] | [JSON](vht_3iv_u7e.json) |
| `vi8_p4p_cwj` | 校長未名 | [《史記・魏豹彭越列傳》][72] | [JSON](vi8_p4p_cwj.json) |
| `vih_hih_3uc` | 召公過 | [《史記・晉世家》][21] | [JSON](vih_hih_3uc.json) |
| `vjd_m6j_we3` | 周厲王 | [《史記・楚世家》][22] | [JSON](vjd_m6j_we3.json) |
| `vju_g6h_b0j` | 趙襄王未名 | [《史記・趙世家》][25] | [JSON](vju_g6h_b0j.json) |
| `vk1_9g9_a0u` | 龐涓 | [《史記・商君列傳》][50] | [JSON](vk1_9g9_a0u.json) |
| `vk6_egu_id7` | 王子綦 | [《史記・伍子胥列傳》][48] | [JSON](vk6_egu_id7.json) |
| `vk7_pxl_658` | 中行寅（攻趙鞅者） | [《史記・晉世家》][21] | [JSON](vk7_pxl_658.json) |
| `vl9_0uq_cgr` | 鄭安平 | [《史記・范睢蔡澤列傳》][61] | [JSON](vl9_0uq_cgr.json) |
| `vle_lyb_962` | 陽生 | [《史記・伍子胥列傳》][48] | [JSON](vle_lyb_962.json) |
| `vlh_nxo_p71` | 王朔 | [《史記・孝武本紀》][12] | [JSON](vlh_nxo_p71.json) |
| `vlp_yy3_ufh` | 平（泗水監） | [《史記・樊酈滕灌列傳》][77] | [JSON](vlp_yy3_ufh.json) |
| `vma_jxj_3e9` | 馮喜 | [《史記・張儀列傳》][52] | [JSON](vma_jxj_3e9.json) |
| `vmp_fmj_mjj` | 趙王遷（引古） | [《史記・蒙恬列傳》][70] | [JSON](vmp_fmj_mjj.json) |
| `vn0_yj1_dq4` | 燕太子丹 | [《史記・范睢蔡澤列傳》][61] | [JSON](vn0_yj1_dq4.json) |
| `vnb_l2e_06w` | 章平 | [《史記・樊酈滕灌列傳》][77] | [JSON](vnb_l2e_06w.json) |
| `vnj_9ny_oq5` | 冥（商先祖） | [《史記・殷本紀》][3] | [JSON](vnj_9ny_oq5.json) |
| `vnm_2mr_2d6` | 周殷 | [《史記・荊燕世家》][33] | [JSON](vnm_2mr_2d6.json) |
| `vnm_ppc_xjm` | 項梁 | [《史記・劉敬叔孫通列傳》][81] | [JSON](vnm_ppc_xjm.json) |
| `vns_z44_maf` | 田忌 | [《史記・孫子吳起列傳》][47] | [JSON](vns_z44_maf.json) |
| `vny_0sw_kdz` | 秦昭王 | [《史記・范睢蔡澤列傳》][61] | [JSON](vny_0sw_kdz.json) |
| `vo2_2ho_kyz` | 扈輒 | [《史記・廉頗藺相如列傳》][63] | [JSON](vo2_2ho_kyz.json) |
| `vo4_81a_ot0` | 知伯 | [《史記・韓世家》][27] | [JSON](vo4_81a_ot0.json) |
| `vo8_9o3_qgz` | 閼與被斬軍中候未名 | [《史記・廉頗藺相如列傳》][63] | [JSON](vo8_9o3_qgz.json) |
| `voa_fj1_ia2` | 晉悼公 | [《史記・韓世家》][27] | [JSON](voa_fj1_ia2.json) |
| `vod_kv8_1t1` | 晉獻公（楚篇文公受寵） | [《史記・晉世家》][21] | [JSON](vod_kv8_1t1.json) |
| `vog_yel_p0d` | 公叔座 | [《史記・商君列傳》][50] | [JSON](vog_yel_p0d.json) |
| `voy_rog_jbw` | 昭王 | [《史記・周本紀》][4] | [JSON](voy_rog_jbw.json) |
| `vp2_qeq_33j` | 楚王書信 | [《史記・蘇秦列傳》][51] | [JSON](vp2_qeq_33j.json) |
| `vp6_3oo_dqh` | 太史公 | [《史記・田叔列傳》][86] | [JSON](vp6_3oo_dqh.json) |
| `vqb_tym_qti` | 魏長吏 | [《史記・穰侯列傳》][54] | [JSON](vqb_tym_qti.json) |
| `vqd_bze_fwa` | 賈季（議立公子樂者） | [《史記・晉世家》][21] | [JSON](vqd_bze_fwa.json) |
| `vqs_vxf_0gt` | 宋孟 | [《史記・袁盎鼂錯列傳》][83] | [JSON](vqs_vxf_0gt.json) |
| `vqw_ylp_5mq` | 呂須 | [《史記・樊酈滕灌列傳》][77] | [JSON](vqw_ylp_5mq.json) |
| `vrl_dy3_665` | 晉平公 | [《史記・孔子世家》][29] | [JSON](vrl_dy3_665.json) |
| `vs5_lya_vft` | 市被（燕將軍） | [《史記・燕召公世家》][16] | [JSON](vs5_lya_vft.json) |
| `vs8_u6b_f8w` | 秦寧公 | [《史記・秦本紀》][5] | [JSON](vs8_u6b_f8w.json) |
| `vsk_gs2_qzw` | 虞舜 | [《史記・商君列傳》][50] | [JSON](vsk_gs2_qzw.json) |
| `vsl_ob5_pki` | 太史公 | [《史記・韓信盧綰列傳》][75] | [JSON](vsl_ob5_pki.json) |
| `vt0_ktk_oat` | 宋景公 | [《史記・鄭世家》][24] | [JSON](vt0_ktk_oat.json) |
| `vt0_wpy_kj2` | 太史公 | [《史記・平原君虞卿列傳》][58] | [JSON](vt0_wpy_kj2.json) |
| `vtc_vuv_ykj` | 析父（楚靈王問鼎答者） | [《史記・楚世家》][22] | [JSON](vtc_vuv_ykj.json) |
| `vti_onv_iur` | 秦穆公 | [《史記・扁鵲倉公列傳》][87] | [JSON](vti_onv_iur.json) |
| `vtj_31m_zlc` | 樂欬 | [《史記・仲尼弟子列傳》][49] | [JSON](vtj_31m_zlc.json) |
| `vtk_lf8_3ue` | 栗腹 | [《史記・廉頗藺相如列傳》][63] | [JSON](vtk_lf8_3ue.json) |
| `vtn_thh_540` | 申不害 | [《史記・老子韓非列傳》][45] | [JSON](vtn_thh_540.json) |
| `vud_z3k_zfc` | 上黨郡守（韓世家未名者） | [《史記・韓世家》][27] | [JSON](vud_z3k_zfc.json) |
| `vug_czu_mzb` | 莊生之婦（越世家未名者） | [《史記・越王勾踐世家》][23] | [JSON](vug_czu_mzb.json) |
| `vur_b8c_5er` | 娥 | [《史記・齊悼惠王世家》][34] | [JSON](vur_b8c_5er.json) |
| `vv0_3wv_i18` | 噲（袁盎兄） | [《史記・袁盎鼂錯列傳》][83] | [JSON](vv0_3wv_i18.json) |
| `vv9_ss8_28z` | 圉妻秦女（重耳再取者） | [《史記・晉世家》][21] | [JSON](vv9_ss8_28z.json) |
| `vvg_bgl_w1b` | 伯虔 | [《史記・仲尼弟子列傳》][49] | [JSON](vvg_bgl_w1b.json) |
| `vvg_rba_nwr` | 翟景 | [《史記・陳涉世家》][30] | [JSON](vvg_rba_nwr.json) |
| `vvt_6h5_czb` | 湯引古短稱 | [《史記・屈原賈生列傳》][66] | [JSON](vvt_6h5_czb.json) |
| `vvv_ws5_he1` | 齊緡王 | [《史記・高祖本紀》][8] | [JSON](vvv_ws5_he1.json) |
| `vw5_ynq_5fx` | 田溉 | [《史記・曹相國世家》][36] | [JSON](vw5_ynq_5fx.json) |
| `vwi_95l_l6d` | 目夷（宋襄公庶兄） | [《史記・宋微子世家》][20] | [JSON](vwi_95l_l6d.json) |
| `vx2_svu_k0q` | 白起 | [《史記・趙世家》][25] | [JSON](vx2_svu_k0q.json) |
| `vxa_usq_rlw` | 許由引古 | [《史記・范睢蔡澤列傳》][61] | [JSON](vxa_usq_rlw.json) |
| `vxj_epn_sti` | 陳司敗 | [《史記・仲尼弟子列傳》][49] | [JSON](vxj_epn_sti.json) |
| `vxt_uj1_8ym` | 鄭昌 | [《史記・高祖本紀》][8] | [JSON](vxt_uj1_8ym.json) |
| `vxv_vcf_nru` | 管夷吾管仲引古 | [《史記・范睢蔡澤列傳》][61] | [JSON](vxv_vcf_nru.json) |
| `vy3_65g_mwj` | 芮良夫 | [《史記・周本紀》][4] | [JSON](vy3_65g_mwj.json) |
| `vz1_0ed_6us` | 文王引古 | [《史記・魯仲連鄒陽列傳》][65] | [JSON](vz1_0ed_6us.json) |
| `vz1_n5y_mng` | 呂祿 | [《史記・絳侯周勃世家》][39] | [JSON](vz1_n5y_mng.json) |
| `vz2_xlj_noq` | 堯引古 | [《史記・魯仲連鄒陽列傳》][65] | [JSON](vz2_xlj_noq.json) |
| `w02_19o_60l` | 淮南王書信未名 | [《史記・吳王濞列傳》][88] | [JSON](w02_19o_60l.json) |
| `w05_x7q_foo` | 繆賢 | [《史記・廉頗藺相如列傳》][63] | [JSON](w05_x7q_foo.json) |
| `w06_m3y_ctg` | 知伯 | [《史記・田敬仲完世家》][28] | [JSON](w06_m3y_ctg.json) |
| `w0d_2f6_1ih` | 曼丘臣 | [《史記・韓信盧綰列傳》][75] | [JSON](w0d_2f6_1ih.json) |
| `w0i_qc3_tpy` | 許負 | [《史記・絳侯周勃世家》][39] | [JSON](w0i_qc3_tpy.json) |
| `w0m_43x_610` | 娵訾氏女 | [《史記・五帝本紀》][1] | [JSON](w0m_43x_610.json) |
| `w0u_fhy_mih` | 趙襄子 | [《史記・刺客列傳》][68] | [JSON](w0u_fhy_mih.json) |
| `w0v_vvq_ypt` | 臧昭伯 | [《史記・魯周公世家》][15] | [JSON](w0v_vvq_ypt.json) |
| `w12_vt2_dhx` | 魏獻子 | [《史記・趙世家》][25] | [JSON](w12_vt2_dhx.json) |
| `w1c_wq9_fly` | 太史公（田世家論贊敘述者） | [《史記・田敬仲完世家》][28] | [JSON](w1c_wq9_fly.json) |
| `w2n_7g1_30z` | 棓生 | [《史記・袁盎鼂錯列傳》][83] | [JSON](w2n_7g1_30z.json) |
| `w2z_v0m_3v8` | 段干子 | [《史記・魏世家》][26] | [JSON](w2z_v0m_3v8.json) |
| `w3g_k4m_zrn` | 常山尉未名 | [《史記・韓信盧綰列傳》][75] | [JSON](w3g_k4m_zrn.json) |
| `w49_0we_e97` | 齊王伐梁 | [《史記・張儀列傳》][52] | [JSON](w49_0we_e97.json) |
| `w4q_ozz_a8d` | 於陵子仲引古 | [《史記・魯仲連鄒陽列傳》][65] | [JSON](w4q_ozz_a8d.json) |
| `w58_lok_uuc` | 虞卿 | [《史記・平原君虞卿列傳》][58] | [JSON](w58_lok_uuc.json) |
| `w5h_6ah_6b1` | 勇之 | [《史記・孝武本紀》][12] | [JSON](w5h_6ah_6b1.json) |
| `w5l_qjq_vly` | 衛文公 | [《史記・齊太公世家》][14] | [JSON](w5l_qjq_vly.json) |
| `w5q_84t_ofs` | 共工（堯時） | [《史記・五帝本紀》][1] | [JSON](w5q_84t_ofs.json) |
| `w5z_z1e_gts` | 周公 | [《史記・外戚世家》][31] | [JSON](w5z_z1e_gts.json) |
| `w68_ebz_0ew` | 平原君夫人未名 | [《史記・魏公子列傳》][59] | [JSON](w68_ebz_0ew.json) |
| `w6d_z7t_geq` | 劉賈 | [《史記・荊燕世家》][33] | [JSON](w6d_z7t_geq.json) |
| `w6w_2q4_c9g` | 商君 | [《史記・魏世家》][26] | [JSON](w6w_2q4_c9g.json) |
| `w7a_pl5_1it` | 叔帶 | [《史記・周本紀》][4] | [JSON](w7a_pl5_1it.json) |
| `w7k_6hz_mb7` | 韓昭侯 | [《史記・孟嘗君列傳》][57] | [JSON](w7k_6hz_mb7.json) |
| `w7n_89s_g0v` | 孔子 | [《史記・魏世家》][26] | [JSON](w7n_89s_g0v.json) |
| `w85_8hh_ltq` | 商君 | [《史記・陳涉世家》][30] | [JSON](w85_8hh_ltq.json) |
| `w8i_dhi_044` | 御史大夫杜 | [《史記・田叔列傳》][86] | [JSON](w8i_dhi_044.json) |
| `w8q_z9a_0zz` | 陳子禽 | [《史記・仲尼弟子列傳》][49] | [JSON](w8q_z9a_0zz.json) |
| `w9b_n1i_kar` | 安王 | [《史記・周本紀》][4] | [JSON](w9b_n1i_kar.json) |
| `w9t_rdt_ue0` | 舜生母 | [《史記・五帝本紀》][1] | [JSON](w9t_rdt_ue0.json) |
| `wae_xmq_dqk` | 楊干 | [《史記・魏世家》][26] | [JSON](wae_xmq_dqk.json) |
| `wai_hue_j42` | 梁王未具名 | [《史記・袁盎鼂錯列傳》][83] | [JSON](wai_hue_j42.json) |
| `waq_xn7_9gj` | 范蜎 | [《史記・樗里子甘茂列傳》][53] | [JSON](waq_xn7_9gj.json) |
| `wb1_g5t_hhz` | 魏侈（范中行之仇） | [《史記・晉世家》][21] | [JSON](wb1_g5t_hhz.json) |
| `wbr_1v1_sld` | 魯哀公 | [《史記・孔子世家》][29] | [JSON](wbr_1v1_sld.json) |
| `wbt_5vf_2pz` | 病疽卒母 | [《史記・孫子吳起列傳》][47] | [JSON](wbt_5vf_2pz.json) |
| `wd1_1f4_qgv` | 李左車 | [《史記・淮陰侯列傳》][74] | [JSON](wd1_1f4_qgv.json) |
| `wdg_4ld_nde` | 縣成 | [《史記・仲尼弟子列傳》][49] | [JSON](wdg_4ld_nde.json) |
| `wdn_b4z_o7p` | 潘滿如 | [《史記・扁鵲倉公列傳》][87] | [JSON](wdn_b4z_o7p.json) |
| `wdr_m9a_k1r` | 辛甲 | [《史記・周本紀》][4] | [JSON](wdr_m9a_k1r.json) |
| `wds_1r8_9kx` | 驪姬弟（悼子母） | [《史記・晉世家》][21] | [JSON](wds_1r8_9kx.json) |
| `we8_3f9_z9b` | 廉頗 | [《史記・廉頗藺相如列傳》][63] | [JSON](we8_3f9_z9b.json) |
| `we8_mkq_luc` | 閔損 | [《史記・仲尼弟子列傳》][49] | [JSON](we8_mkq_luc.json) |
| `wex_fkp_gc1` | 舜 | [《史記・鄭世家》][24] | [JSON](wex_fkp_gc1.json) |
| `wf4_hj5_nah` | 屈原 | [《史記・張儀列傳》][52] | [JSON](wf4_hj5_nah.json) |
| `wf7_94x_t3j` | 公孫支引古 | [《史記・李斯列傳》][69] | [JSON](wf7_94x_t3j.json) |
| `wf8_9b9_kcq` | 周霸 | [《史記・孝武本紀》][12] | [JSON](wf8_9b9_kcq.json) |
| `wfj_i4s_mq5` | 離婁引古 | [《史記・屈原賈生列傳》][66] | [JSON](wfj_i4s_mq5.json) |
| `wfk_n4m_6x9` | 陳留令未名 | [《史記・酈生陸賈列傳》][79] | [JSON](wfk_n4m_6x9.json) |
| `wfm_qvc_ykk` | 荊王負芻 | [《史記・白起王翦列傳》][55] | [JSON](wfm_qvc_ykk.json) |
| `wfn_d71_zaw` | 夔 | [《史記・五帝本紀》][1] | [JSON](wfn_d71_zaw.json) |
| `wft_r8s_naw` | 申后 | [《史記・周本紀》][4] | [JSON](wft_r8s_naw.json) |
| `wfu_ts5_cyz` | 長衛姬（無詭母） | [《史記・齊太公世家》][14] | [JSON](wfu_ts5_cyz.json) |
| `wgh_mmm_fjq` | 燕仲父（惠王記事） | [《史記・燕召公世家》][16] | [JSON](wgh_mmm_fjq.json) |
| `wh6_u2c_0xc` | 楚王 | [《史記・三王世家》][42] | [JSON](wh6_u2c_0xc.json) |
| `whn_5w1_i1k` | 晏平仲 | [《史記・仲尼弟子列傳》][49] | [JSON](whn_5w1_i1k.json) |
| `whv_8wm_15e` | 孟説 | [《史記・趙世家》][25] | [JSON](whv_8wm_15e.json) |
| `wie_ryy_5wa` | 子產 | [《史記・伍子胥列傳》][48] | [JSON](wie_ryy_5wa.json) |
| `wj3_oa7_o6b` | 杜信 | [《史記・扁鵲倉公列傳》][87] | [JSON](wj3_oa7_o6b.json) |
| `wjf_wa5_eu9` | 彊（孝惠後宮子稱） | [《史記・呂太后本紀》][9] | [JSON](wjf_wa5_eu9.json) |
| `wjp_1iw_3qf` | 代王嘉 | [《史記・田敬仲完世家》][28] | [JSON](wjp_1iw_3qf.json) |
| `wka_94j_2k5` | 少姬 | [《史記・管晏列傳》][44] | [JSON](wka_94j_2k5.json) |
| `wl3_jss_lix` | 奚齊 | [《史記・劉敬叔孫通列傳》][81] | [JSON](wl3_jss_lix.json) |
| `wl6_i22_vjk` | 類犴反 | [《史記・梁孝王世家》][40] | [JSON](wl6_i22_vjk.json) |
| `wl7_s8c_f4l` | 晉定公 | [《史記・趙世家》][25] | [JSON](wl7_s8c_f4l.json) |
| `wle_6pj_6oo` | 吳起被延公主 | [《史記・孫子吳起列傳》][47] | [JSON](wle_6pj_6oo.json) |
| `wlx_03b_0j3` | 周苛 | [《史記・魏豹彭越列傳》][72] | [JSON](wlx_03b_0j3.json) |
| `wmx_rqf_b09` | 慶舍 | [《史記・趙世家》][25] | [JSON](wmx_rqf_b09.json) |
| `wn0_q61_j1n` | 報丙 | [《史記・殷本紀》][3] | [JSON](wn0_q61_j1n.json) |
| `wnb_fut_1ox` | 蘇秦舍人 | [《史記・張儀列傳》][52] | [JSON](wnb_fut_1ox.json) |
| `wnf_7c0_qa3` | 陽虎 | [《史記・孔子世家》][29] | [JSON](wnf_7c0_qa3.json) |
| `wng_nsz_uav` | 公孫龍 | [《史記・仲尼弟子列傳》][49] | [JSON](wng_nsz_uav.json) |
| `wnh_q01_kjg` | 扶蘇 | [《史記・李斯列傳》][69] | [JSON](wnh_q01_kjg.json) |
| `wnp_0s3_0eg` | 太尉弱 | [《史記・絳侯周勃世家》][39] | [JSON](wnp_0s3_0eg.json) |
| `wnp_vk6_qhe` | 冉求 | [《史記・仲尼弟子列傳》][49] | [JSON](wnp_vk6_qhe.json) |
| `wnq_h3v_yfm` | 種 | [《史記・越王勾踐世家》][23] | [JSON](wnq_h3v_yfm.json) |
| `wny_01o_f36` | 公子買（衛守者） | [《史記・晉世家》][21] | [JSON](wny_01o_f36.json) |
| `woj_cq6_ajq` | 嘉（呂台嗣王） | [《史記・呂太后本紀》][9] | [JSON](woj_cq6_ajq.json) |
| `wpi_4yz_de2` | 王姬（齊桓公夫人） | [《史記・齊太公世家》][14] | [JSON](wpi_4yz_de2.json) |
| `wpm_b14_e28` | 楚平王 | [《史記・刺客列傳》][68] | [JSON](wpm_b14_e28.json) |
| `wpr_zxu_kt8` | 衡山王書信未名 | [《史記・吳王濞列傳》][88] | [JSON](wpr_zxu_kt8.json) |
| `wpx_vms_opg` | 公孫光 | [《史記・扁鵲倉公列傳》][87] | [JSON](wpx_vms_opg.json) |
| `wq3_5dq_hx9` | 陳湣公 | [《史記・孔子世家》][29] | [JSON](wq3_5dq_hx9.json) |
| `wqd_ft2_k5v` | 林胡王（趙世家未名者） | [《史記・趙世家》][25] | [JSON](wqd_ft2_k5v.json) |
| `wqf_43e_laj` | 咎如長女（重耳狄妻） | [《史記・晉世家》][21] | [JSON](wqf_43e_laj.json) |
| `wr1_5wr_sx5` | 張廷尉未詳名 | [《史記・張丞相列傳》][78] | [JSON](wr1_5wr_sx5.json) |
| `wrg_tw6_e8v` | 灌嬰 | [《史記・樊酈滕灌列傳》][77] | [JSON](wrg_tw6_e8v.json) |
| `wrh_7px_ox5` | 紂 | [《史記・趙世家》][25] | [JSON](wrh_7px_ox5.json) |
| `wrp_npf_kym` | 田假 | [《史記・田儋列傳》][76] | [JSON](wrp_npf_kym.json) |
| `ws3_3yb_yzp` | 五羖大夫 | [《史記・商君列傳》][50] | [JSON](ws3_3yb_yzp.json) |
| `ws8_rns_8zp` | 戚將軍 | [《史記・曹相國世家》][36] | [JSON](ws8_rns_8zp.json) |
| `wsa_th4_9ud` | 弓高侯 | [《史記・絳侯周勃世家》][39] | [JSON](wsa_th4_9ud.json) |
| `wsa_z5d_frx` | 哀姜（文公長妃） | [《史記・魯周公世家》][15] | [JSON](wsa_z5d_frx.json) |
| `wsc_j2v_f87` | 逄丑父 | [《史記・齊太公世家》][14] | [JSON](wsc_j2v_f87.json) |
| `wse_abc_uqy` | 魏勃 | [《史記・齊悼惠王世家》][34] | [JSON](wse_abc_uqy.json) |
| `wsj_ypn_olf` | 公孫奭 | [《史記・樗里子甘茂列傳》][53] | [JSON](wsj_ypn_olf.json) |
| `wss_6f8_4rz` | 魏惠王 | [《史記・孟嘗君列傳》][57] | [JSON](wss_6f8_4rz.json) |
| `wt0_abc_2sk` | 隨會 | [《史記・晉世家》][21] | [JSON](wt0_abc_2sk.json) |
| `wti_7m6_wi5` | 蘇代 | [《史記・田敬仲完世家》][28] | [JSON](wti_7m6_wi5.json) |
| `wti_k6m_bak` | 魏犫（文公軍右） | [《史記・晉世家》][21]、[《史記・楚世家》][22] | [JSON](wti_k6m_bak.json) |
| `wuf_z4a_3vn` | 建的美人（未名） | [《史記・呂太后本紀》][9] | [JSON](wuf_z4a_3vn.json) |
| `wuo_ghc_ajx` | 荀卿 | [《史記・孟子荀卿列傳》][56] | [JSON](wuo_ghc_ajx.json) |
| `wup_r0j_c71` | 蹠引古短稱 | [《史記・魯仲連鄒陽列傳》][65] | [JSON](wup_r0j_c71.json) |
| `ww1_6jl_a71` | 公叔伯嬰 | [《史記・韓世家》][27] | [JSON](ww1_6jl_a71.json) |
| `wwb_4f9_co0` | 張良 | [《史記・齊悼惠王世家》][34] | [JSON](wwb_4f9_co0.json) |
| `wwc_yic_y3q` | 葉公 | [《史記・孔子世家》][29] | [JSON](wwc_yic_y3q.json) |
| `wwf_ocm_23f` | 太史公 | [《史記・留侯世家》][37] | [JSON](wwf_ocm_23f.json) |
| `wwz_8n8_w33` | 息侯（陳婚記事） | [《史記・管蔡世家》][17] | [JSON](wwz_8n8_w33.json) |
| `wxg_l3l_wre` | 魏齊 | [《史記・范睢蔡澤列傳》][61] | [JSON](wxg_l3l_wre.json) |
| `wxj_wmw_39e` | 彭生 | [《史記・魯周公世家》][15] | [JSON](wxj_wmw_39e.json) |
| `wxn_bku_mqy` | 絃髙 | [《史記・鄭世家》][24] | [JSON](wxn_bku_mqy.json) |
| `wxr_gch_zh5` | 田完 | [《史記・田敬仲完世家》][28] | [JSON](wxr_gch_zh5.json) |
| `wxu_0lr_f33` | 齊丞相未名 | [《史記・扁鵲倉公列傳》][87] | [JSON](wxu_0lr_f33.json) |
| `wxw_hns_6a2` | 齊威王 | [《史記・越王勾踐世家》][23] | [JSON](wxw_hns_6a2.json) |
| `wyk_owg_0tl` | 越人蒙引古 | [《史記・魯仲連鄒陽列傳》][65] | [JSON](wyk_owg_0tl.json) |
| `wyx_6d2_xxp` | 李悝 | [《史記・孟子荀卿列傳》][56] | [JSON](wyx_6d2_xxp.json) |
| `wz4_o0x_ez1` | 樊噲 | [《史記・樊酈滕灌列傳》][77] | [JSON](wz4_o0x_ez1.json) |
| `wzh_9d5_a6v` | 樊噲 | [《史記・樊酈滕灌列傳》][77] | [JSON](wzh_9d5_a6v.json) |
| `wzh_zgv_rkf` | 薛公 | [《史記・魏公子列傳》][59] | [JSON](wzh_zgv_rkf.json) |
| `wzo_s8b_vyg` | 胡武 | [《史記・陳涉世家》][30] | [JSON](wzo_s8b_vyg.json) |
| `x06_36x_8rd` | 魯昭公 | [《史記・孔子世家》][29] | [JSON](x06_36x_8rd.json) |
| `x08_b9c_uj2` | 韓宣子 | [《史記・鄭世家》][24] | [JSON](x08_b9c_uj2.json) |
| `x0b_9fw_ttm` | 殤公（宋弒君記事） | [《史記・宋微子世家》][20] | [JSON](x0b_9fw_ttm.json) |
| `x0e_ivo_wsa` | 項伯 | [《史記・樊酈滕灌列傳》][77] | [JSON](x0e_ivo_wsa.json) |
| `x1n_vdt_l94` | 將渠（燕大夫） | [《史記・燕召公世家》][16] | [JSON](x1n_vdt_l94.json) |
| `x2m_k5j_fdz` | 共王 | [《史記・周本紀》][4] | [JSON](x2m_k5j_fdz.json) |
| `x2p_rzw_i2t` | 司空季子（重耳秦婚記事） | [《史記・晉世家》][21] | [JSON](x2p_rzw_i2t.json) |
| `x2u_81x_m6e` | 仲山甫 | [《史記・周本紀》][4] | [JSON](x2u_81x_m6e.json) |
| `x2v_zid_ab0` | 叔虞 | [《史記・鄭世家》][24] | [JSON](x2v_zid_ab0.json) |
| `x34_rd3_mqi` | 趙孝成王 | [《史記・平原君虞卿列傳》][58] | [JSON](x34_rd3_mqi.json) |
| `x3c_d03_60b` | 宓不齊 | [《史記・仲尼弟子列傳》][49] | [JSON](x3c_d03_60b.json) |
| `x3j_j8y_j74` | 司馬尚 | [《史記・廉頗藺相如列傳》][63] | [JSON](x3j_j8y_j74.json) |
| `x49_k24_rm4` | 陳豨 | [《史記・韓信盧綰列傳》][75] | [JSON](x49_k24_rm4.json) |
| `x4b_g9c_33o` | 長桑君 | [《史記・扁鵲倉公列傳》][87] | [JSON](x4b_g9c_33o.json) |
| `x4k_z5z_vqm` | 費無忌 | [《史記・伍子胥列傳》][48] | [JSON](x4k_z5z_vqm.json) |
| `x4n_p1z_u9i` | 芮子 | [《史記・田敬仲完世家》][28] | [JSON](x4n_p1z_u9i.json) |
| `x4t_pbv_z7y` | 蕭相國 | [《史記・黥布列傳》][73] | [JSON](x4t_pbv_z7y.json) |
| `x5u_3mf_dc8` | 王廖 | [《史記・秦始皇本紀》][6] | [JSON](x5u_3mf_dc8.json) |
| `x89_ryb_yax` | 呂澤 | [《史記・留侯世家》][37] | [JSON](x89_ryb_yax.json) |
| `x8f_fyc_zvc` | 叔孫通 | [《史記・劉敬叔孫通列傳》][81] | [JSON](x8f_fyc_zvc.json) |
| `x8h_4i8_xwm` | 左相未具名 | [《史記・田叔列傳》][86] | [JSON](x8h_4i8_xwm.json) |
| `x8h_bgr_mc5` | 武（孝惠後宮子稱） | [《史記・呂太后本紀》][9] | [JSON](x8h_bgr_mc5.json) |
| `x8j_rqz_jry` | 陳勝 | [《史記・酈生陸賈列傳》][79] | [JSON](x8j_rqz_jry.json) |
| `x8n_oxv_xpj` | 衛君 | [《史記・樗里子甘茂列傳》][53] | [JSON](x8n_oxv_xpj.json) |
| `x8s_zva_utk` | 秦將（負芻二年伐楚未名者） | [《史記・楚世家》][22] | [JSON](x8s_zva_utk.json) |
| `x8u_5uo_ch7` | 魏文侯 | [《史記・仲尼弟子列傳》][49] | [JSON](x8u_5uo_ch7.json) |
| `x8u_6uv_esq` | 酈食其 | [《史記・酈生陸賈列傳》][79] | [JSON](x8u_6uv_esq.json) |
| `x99_1e5_dbn` | 楚威王 | [《史記・越王勾踐世家》][23] | [JSON](x99_1e5_dbn.json) |
| `x9j_eu1_vck` | 秦惠王 | [《史記・張儀列傳》][52] | [JSON](x9j_eu1_vck.json) |
| `x9l_eux_c3n` | 申陽 | [《史記・項羽本紀》][7]、[《史記・高祖本紀》][8] | [JSON](x9l_eux_c3n.json) |
| `x9q_ghs_z2s` | 蒯通 | [《史記・淮陰侯列傳》][74] | [JSON](x9q_ghs_z2s.json) |
| `xaa_ewn_4ro` | 臧荼 | [《史記・高祖本紀》][8] | [JSON](xaa_ewn_4ro.json) |
| `xbl_kip_rw4` | 申鮑胥（楚篇秦救使者） | [《史記・楚世家》][22] | [JSON](xbl_kip_rw4.json) |
| `xbm_dvk_k14` | 末喜 | [《史記・外戚世家》][31] | [JSON](xbm_dvk_k14.json) |
| `xbz_sh0_e2m` | 李斯 | [《史記・老子韓非列傳》][45] | [JSON](xbz_sh0_e2m.json) |
| `xcs_h9s_rgw` | 公孫痤 | [《史記・魏世家》][26] | [JSON](xcs_h9s_rgw.json) |
| `xcv_pkj_crw` | 汝賈（內昭公議事） | [《史記・魯周公世家》][15] | [JSON](xcv_pkj_crw.json) |
| `xcz_sby_ker` | 季孫 | [《史記・仲尼弟子列傳》][49] | [JSON](xcz_sby_ker.json) |
| `xd0_yc1_jd5` | 齊太史（崔杼弒君書者未名） | [《史記・齊太公世家》][14] | [JSON](xd0_yc1_jd5.json) |
| `xd1_b6x_v7v` | 孝文王 | [《史記・陳涉世家》][30] | [JSON](xd1_b6x_v7v.json) |
| `xd1_no8_2ar` | 蘧伯玉 | [《史記・仲尼弟子列傳》][49] | [JSON](xd1_no8_2ar.json) |
| `xdq_h9k_zzl` | 遷母（趙世家倡未名者） | [《史記・趙世家》][25] | [JSON](xdq_h9k_zzl.json) |
| `xea_8m8_6dh` | 驩（臨江王） | [《史記・高祖本紀》][8] | [JSON](xea_8m8_6dh.json) |
| `xer_mp5_agd` | 楚使者未名 | [《史記・黥布列傳》][73] | [JSON](xer_mp5_agd.json) |
| `xfa_rw3_95j` | 重耳 | [《史記・晉世家》][21] | [JSON](xfa_rw3_95j.json) |
| `xg3_url_fyn` | 留侯未詳名 | [《史記・張丞相列傳》][78] | [JSON](xg3_url_fyn.json) |
| `xg5_2en_bvd` | 柳下惠 | [《史記・仲尼弟子列傳》][49] | [JSON](xg5_2en_bvd.json) |
| `xga_n8f_29q` | 孝惠帝 | [《史記・外戚世家》][31] | [JSON](xga_n8f_29q.json) |
| `xgu_xke_x00` | 商鞅引古 | [《史記・李斯列傳》][69] | [JSON](xgu_xke_x00.json) |
| `xgw_at7_sju` | 陳女女弟（衛桓公母） | [《史記・衛康叔世家》][19] | [JSON](xgw_at7_sju.json) |
| `xgx_g4a_c28` | 趙兼 | [《史記・孝文本紀》][10] | [JSON](xgx_g4a_c28.json) |
| `xh0_ri6_7sg` | 餘祭 | [《史記・刺客列傳》][68] | [JSON](xh0_ri6_7sg.json) |
| `xh0_zdc_cq8` | 季勝 | [《史記・秦本紀》][5] | [JSON](xh0_zdc_cq8.json) |
| `xhe_1l6_pc9` | 齊王曾陽虛侯未具名 | [《史記・扁鵲倉公列傳》][87] | [JSON](xhe_1l6_pc9.json) |
| `xhk_2v1_pd8` | 魯君（孔子世家女樂未名者） | [《史記・孔子世家》][29] | [JSON](xhk_2v1_pd8.json) |
| `xhp_h3f_rus` | 緡（晉侯） | [《史記・晉世家》][21] | [JSON](xhp_h3f_rus.json) |
| `xhs_wj2_zbt` | 商容 | [《史記・殷本紀》][3] | [JSON](xhs_wj2_zbt.json) |
| `xi5_cuw_xu1` | 壤駟赤 | [《史記・仲尼弟子列傳》][49] | [JSON](xi5_cuw_xu1.json) |
| `xib_wbp_so4` | 紂 | [《史記・外戚世家》][31] | [JSON](xib_wbp_so4.json) |
| `xie_13c_5ho` | 趙嬰 | [《史記・秦始皇本紀》][6] | [JSON](xie_13c_5ho.json) |
| `xih_zlh_ppq` | 蘇厲 | [《史記・周本紀》][4]、[《史記・秦始皇本紀》][6] | [JSON](xih_zlh_ppq.json) |
| `xip_3lx_rpc` | 大業 | [《史記・趙世家》][25] | [JSON](xip_3lx_rpc.json) |
| `xix_lzk_s92` | 修 | [《史記・五宗世家》][41] | [JSON](xix_lzk_s92.json) |
| `xj1_qxh_afa` | 王紲 | [《史記・趙世家》][25] | [JSON](xj1_qxh_afa.json) |
| `xj8_5eq_dtl` | 酈山之女 | [《史記・秦本紀》][5] | [JSON](xj8_5eq_dtl.json) |
| `xjk_0i9_vc2` | 楚懷王 | [《史記・樗里子甘茂列傳》][53] | [JSON](xjk_0i9_vc2.json) |
| `xjx_97m_qss` | 郭同 | [《史記・樊酈滕灌列傳》][77] | [JSON](xjx_97m_qss.json) |
| `xk1_q1d_4tc` | 韓信舍人未名 | [《史記・淮陰侯列傳》][74] | [JSON](xk1_q1d_4tc.json) |
| `xkc_rp5_a3d` | 宣帝 | [《史記・三王世家》][42] | [JSON](xkc_rp5_a3d.json) |
| `xkn_0tx_45l` | 秦孝公 | [《史記・趙世家》][25] | [JSON](xkn_0tx_45l.json) |
| `xky_ebm_pdy` | 薄太后 | [《史記・吳王濞列傳》][88] | [JSON](xky_ebm_pdy.json) |
| `xlc_jrm_ei4` | 房君 | [《史記・陳涉世家》][30] | [JSON](xlc_jrm_ei4.json) |
| `xli_xkc_ts4` | 魯襄公 | [《史記・孔子世家》][29] | [JSON](xli_xkc_ts4.json) |
| `xlp_ihc_qm9` | 辛廖 | [《史記・魏世家》][26] | [JSON](xlp_ihc_qm9.json) |
| `xlt_9ml_n9i` | 魏公子未詳名（引古） | [《史記・韓信盧綰列傳》][75] | [JSON](xlt_9ml_n9i.json) |
| `xma_4rf_v7v` | 中行文子 | [《史記・趙世家》][25] | [JSON](xma_4rf_v7v.json) |
| `xmb_506_d88` | 胡傷（本文讀法） | [《史記・秦本紀》][5] | [JSON](xmb_506_d88.json) |
| `xmm_nkr_qbg` | 奉陽君 | [《史記・張儀列傳》][52] | [JSON](xmm_nkr_qbg.json) |
| `xna_g4h_5iz` | 樂毅 | [《史記・趙世家》][25] | [JSON](xna_g4h_5iz.json) |
| `xng_f7r_jcu` | 晉文公引文候選 | [《史記・扁鵲倉公列傳》][87] | [JSON](xng_f7r_jcu.json) |
| `xno_bw1_y99` | 武安君甘羅引古 | [《史記・樗里子甘茂列傳》][53] | [JSON](xno_bw1_y99.json) |
| `xnz_nos_gyp` | 內史勳 | [《史記・齊悼惠王世家》][34] | [JSON](xnz_nos_gyp.json) |
| `xo7_3fg_a18` | 楚懷王 | [《史記・楚世家》][22] | [JSON](xo7_3fg_a18.json) |
| `xo7_4es_usf` | 項燕 | [《史記・陳涉世家》][30] | [JSON](xo7_4es_usf.json) |
| `xoj_go3_gl0` | 竇廣國 | [《史記・外戚世家》][31] | [JSON](xoj_go3_gl0.json) |
| `xoj_ji6_85j` | 中行獻子 | [《史記・齊太公世家》][14] | [JSON](xoj_ji6_85j.json) |
| `xop_byp_p7d` | 虙戲 | [《史記・趙世家》][25] | [JSON](xop_byp_p7d.json) |
| `xow_e7w_ucx` | 子嬰 | [《史記・秦始皇本紀》][6] | [JSON](xow_e7w_ucx.json) |
| `xox_3lp_sy3` | 祝懽 | [《史記・商君列傳》][50] | [JSON](xox_3lp_sy3.json) |
| `xp2_dxz_zcn` | 馮敬 | [《史記・屈原賈生列傳》][66] | [JSON](xp2_dxz_zcn.json) |
| `xp4_n22_648` | 大夫種引古 | [《史記・魯仲連鄒陽列傳》][65] | [JSON](xp4_n22_648.json) |
| `xp8_oo8_cjo` | 大夫種（引古） | [《史記・淮陰侯列傳》][74] | [JSON](xp8_oo8_cjo.json) |
| `xpc_di7_68r` | 魏敬 | [《史記・孝文本紀》][10] | [JSON](xpc_di7_68r.json) |
| `xqc_j54_rtn` | 屈完 | [《史記・楚世家》][22] | [JSON](xqc_j54_rtn.json) |
| `xqf_p8o_1g5` | 穰侯 | [《史記・穰侯列傳》][54] | [JSON](xqf_p8o_1g5.json) |
| `xqg_126_3pd` | 秦哀公 | [《史記・伍子胥列傳》][48] | [JSON](xqg_126_3pd.json) |
| `xqw_bie_izn` | 衞靈公 | [《史記・仲尼弟子列傳》][49] | [JSON](xqw_bie_izn.json) |
| `xr0_7lg_823` | 晉平公 | [《史記・韓世家》][27] | [JSON](xr0_7lg_823.json) |
| `xru_mbd_dle` | 齊王受虞卿未名 | [《史記・平原君虞卿列傳》][58] | [JSON](xru_mbd_dle.json) |
| `xs7_jo2_pjd` | 燕文侯 | [《史記・蘇秦列傳》][51] | [JSON](xs7_jo2_pjd.json) |
| `xsl_5ma_w95` | 韓太子蒼 | [《史記・秦本紀》][5] | [JSON](xsl_5ma_w95.json) |
| `xsm_2m5_ptl` | 壽燭 | [《史記・穰侯列傳》][54] | [JSON](xsm_2m5_ptl.json) |
| `xsx_kri_47z` | 樓緩 | [《史記・陳涉世家》][30] | [JSON](xsx_kri_47z.json) |
| `xt3_8e7_hvi` | 說秦昭王者未名 | [《史記・孟嘗君列傳》][57] | [JSON](xt3_8e7_hvi.json) |
| `xt7_zq6_tu6` | 中丁 | [《史記・殷本紀》][3] | [JSON](xt7_zq6_tu6.json) |
| `xtl_sr1_di0` | 項悍 | [《史記・陳丞相世家》][38] | [JSON](xtl_sr1_di0.json) |
| `xtq_oi8_w82` | 比干 | [《史記・殷本紀》][3] | [JSON](xtq_oi8_w82.json) |
| `xtz_z8u_92p` | 張相如 | [《史記・張釋之馮唐列傳》][84] | [JSON](xtz_z8u_92p.json) |
| `xu3_wem_5h3` | 紂 | [《史記・劉敬叔孫通列傳》][81] | [JSON](xu3_wem_5h3.json) |
| `xu5_0nl_f5z` | 盜跖引古 | [《史記・屈原賈生列傳》][66] | [JSON](xu5_0nl_f5z.json) |
| `xu8_76t_ldg` | 卜偃（晉卜者） | [《史記・晉世家》][21] | [JSON](xu8_76t_ldg.json) |
| `xv2_ujg_1pe` | 楚王割東國未定 | [《史記・孟嘗君列傳》][57] | [JSON](xv2_ujg_1pe.json) |
| `xv5_hg2_v5w` | 馮劫 | [《史記・秦始皇本紀》][6] | [JSON](xv5_hg2_v5w.json) |
| `xv9_2k8_d07` | 周成王 | [《史記・劉敬叔孫通列傳》][81] | [JSON](xv9_2k8_d07.json) |
| `xvc_q9g_mkx` | 臧氏老（季氏所囚未名） | [《史記・魯周公世家》][15] | [JSON](xvc_q9g_mkx.json) |
| `xvh_vgj_xa2` | 成彊母（崔杼前妻未名） | [《史記・齊太公世家》][14] | [JSON](xvh_vgj_xa2.json) |
| `xvq_2vi_og2` | 秦昭王 | [《史記・田敬仲完世家》][28] | [JSON](xvq_2vi_og2.json) |
| `xw0_62h_nxt` | 家監未名 | [《史記・田叔列傳》][86] | [JSON](xw0_62h_nxt.json) |
| `xwc_7eh_kj1` | 上官大夫未名 | [《史記・屈原賈生列傳》][66] | [JSON](xwc_7eh_kj1.json) |
| `xwz_db0_zgf` | 李由 | [《史記・曹相國世家》][36] | [JSON](xwz_db0_zgf.json) |
| `xx0_5ue_hl1` | 劉賈 | [《史記・吳王濞列傳》][88] | [JSON](xx0_5ue_hl1.json) |
| `xx7_loh_2ge` | 郤克 | [《史記・齊太公世家》][14] | [JSON](xx7_loh_2ge.json) |
| `xx8_6pg_u24` | 簡公婦人（田世家檀臺未名者） | [《史記・田敬仲完世家》][28] | [JSON](xx8_6pg_u24.json) |
| `xx9_ni7_l9f` | 祖辛 | [《史記・殷本紀》][3] | [JSON](xx9_ni7_l9f.json) |
| `xxc_auu_pd9` | 袁生 | [《史記・高祖本紀》][8] | [JSON](xxc_auu_pd9.json) |
| `xxq_5y6_8sr` | 狐偃（咎犯） | [《史記・晉世家》][21] | [JSON](xxq_5y6_8sr.json) |
| `xxq_gha_m5y` | 猶（楚哀王） | [《史記・楚世家》][22] | [JSON](xxq_gha_m5y.json) |
| `xxs_ub0_7rv` | 龍且 | [《史記・淮陰侯列傳》][74] | [JSON](xxs_ub0_7rv.json) |
| `xxu_9lb_1z0` | 箕子引古 | [《史記・魯仲連鄒陽列傳》][65] | [JSON](xxu_9lb_1z0.json) |
| `xxw_nqn_rub` | 昭子 | [《史記・楚世家》][22] | [JSON](xxw_nqn_rub.json) |
| `xxy_58r_nto` | 秦惠王 | [《史記・屈原賈生列傳》][66] | [JSON](xxy_58r_nto.json) |
| `xy0_zdb_ssj` | 子餘（太史） | [《史記・齊太公世家》][14] | [JSON](xy0_zdb_ssj.json) |
| `xyx_811_vue` | 馮毋擇 | [《史記・秦始皇本紀》][6] | [JSON](xyx_811_vue.json) |
| `xz1_j5k_z0t` | 審食其 | [《史記・韓信盧綰列傳》][75] | [JSON](xz1_j5k_z0t.json) |
| `xz9_iik_30x` | 衛鞅（楚篇封商者） | [《史記・楚世家》][22] | [JSON](xz9_iik_30x.json) |
| `xzf_77f_8s2` | 公孫弘 | [《史記・齊悼惠王世家》][34] | [JSON](xzf_77f_8s2.json) |
| `xzi_8vn_cnc` | 蘇秦謀齊齊王 | [《史記・張儀列傳》][52] | [JSON](xzi_8vn_cnc.json) |
| `xzo_t0s_b50` | 王子中同 | [《史記・仲尼弟子列傳》][49] | [JSON](xzo_t0s_b50.json) |
| `xzr_i9s_mnp` | 東甌王（勇之所引） | [《史記・孝武本紀》][12] | [JSON](xzr_i9s_mnp.json) |
| `xzw_df5_9v1` | 吳起 | [《史記・秦始皇本紀》][6] | [JSON](xzw_df5_9v1.json) |
| `y0f_bts_55y` | 湯引古 | [《史記・穰侯列傳》][54] | [JSON](y0f_bts_55y.json) |
| `y16_e24_bef` | 景監 | [《史記・商君列傳》][50] | [JSON](y16_e24_bef.json) |
| `y1b_i8y_w08` | 臧荼 | [《史記・陳丞相世家》][38] | [JSON](y1b_i8y_w08.json) |
| `y1g_wr7_5l5` | 秦將軍（武關伏兵冒秦王者） | [《史記・楚世家》][22] | [JSON](y1g_wr7_5l5.json) |
| `y1m_88m_n1b` | 虢叔 | [《史記・鄭世家》][24] | [JSON](y1m_88m_n1b.json) |
| `y1q_rxv_87u` | 楚王書信未名 | [《史記・吳王濞列傳》][88] | [JSON](y1q_rxv_87u.json) |
| `y1s_5hf_3lv` | 子服景伯 | [《史記・仲尼弟子列傳》][49] | [JSON](y1s_5hf_3lv.json) |
| `y2h_l5o_9qj` | 蒙毅 | [《史記・李斯列傳》][69] | [JSON](y2h_l5o_9qj.json) |
| `y38_ic5_9vk` | 卜齮 | [《史記・魯周公世家》][15] | [JSON](y38_ic5_9vk.json) |
| `y3i_rsz_brn` | 韓厥 | [《史記・韓世家》][27] | [JSON](y3i_rsz_brn.json) |
| `y3p_prx_r3j` | 石 | [《史記・趙世家》][25] | [JSON](y3p_prx_r3j.json) |
| `y3u_g30_6et` | 鯀 | [《史記・夏本紀》][2] | [JSON](y3u_g30_6et.json) |
| `y4b_zoh_zh7` | 卿秦（燕將） | [《史記・燕召公世家》][16] | [JSON](y4b_zoh_zh7.json) |
| `y4k_kjc_vi6` | 燕王旦 | [《史記・外戚世家》][31] | [JSON](y4k_kjc_vi6.json) |
| `y4n_pw6_7ii` | 張子房 | [《史記・留侯世家》][37] | [JSON](y4n_pw6_7ii.json) |
| `y4s_39i_5t3` | 賀 | [《史記・三王世家》][42] | [JSON](y4s_39i_5t3.json) |
| `y54_2ib_yfh` | 孔子 | [《史記・孔子世家》][29] | [JSON](y54_2ib_yfh.json) |
| `y56_c4g_fbf` | 髙昭子 | [《史記・田敬仲完世家》][28] | [JSON](y56_c4g_fbf.json) |
| `y5g_euj_1xr` | 季文子（魯卿） | [《史記・魯周公世家》][15] | [JSON](y5g_euj_1xr.json) |
| `y5m_als_o73` | 范蠡（引古） | [《史記・淮陰侯列傳》][74] | [JSON](y5m_als_o73.json) |
| `y5r_0fi_saz` | 蕭（蕭曹用稱） | [《史記・韓信盧綰列傳》][75] | [JSON](y5r_0fi_saz.json) |
| `y5u_03o_sie` | 商君 | [《史記・魏世家》][26] | [JSON](y5u_03o_sie.json) |
| `y63_hvf_l13` | 宋湣公 | [《史記・鄭世家》][24] | [JSON](y63_hvf_l13.json) |
| `y6n_nmo_abl` | 韓景侯 | [《史記・鄭世家》][24] | [JSON](y6n_nmo_abl.json) |
| `y6v_c03_at3` | 賈生 | [《史記・屈原賈生列傳》][66] | [JSON](y6v_c03_at3.json) |
| `y6w_obg_omu` | 呂榮 | [《史記・呂太后本紀》][9] | [JSON](y6w_obg_omu.json) |
| `y6x_wmu_o70` | 趙簡子 | [《史記・韓世家》][27] | [JSON](y6x_wmu_o70.json) |
| `y6z_6wd_ezf` | 龍且 | [《史記・田儋列傳》][76] | [JSON](y6z_6wd_ezf.json) |
| `y70_ech_q74` | 滕公 | [《史記・黥布列傳》][73] | [JSON](y70_ech_q74.json) |
| `y7w_mwz_7db` | 曹參 | [《史記・曹相國世家》][36] | [JSON](y7w_mwz_7db.json) |
| `y81_o3y_nw3` | 周桓王 | [《史記・鄭世家》][24] | [JSON](y81_o3y_nw3.json) |
| `y81_z0r_svc` | 左人郢 | [《史記・仲尼弟子列傳》][49] | [JSON](y81_z0r_svc.json) |
| `y82_gm0_bbt` | 項他 | [《史記・樊酈滕灌列傳》][77] | [JSON](y82_gm0_bbt.json) |
| `y85_c3n_gfg` | 商鞅 | [《史記・蘇秦列傳》][51] | [JSON](y85_c3n_gfg.json) |
| `y8g_kfz_51h` | 張相如 | [《史記・張釋之馮唐列傳》][84] | [JSON](y8g_kfz_51h.json) |
| `y8v_od8_wtk` | 李信 | [《史記・刺客列傳》][68] | [JSON](y8v_od8_wtk.json) |
| `y9b_ziu_p6i` | 殷紂 | [《史記・商君列傳》][50] | [JSON](y9b_ziu_p6i.json) |
| `y9g_4wy_1m9` | 自相太子（魏世家未名者） | [《史記・魏世家》][26] | [JSON](y9g_4wy_1m9.json) |
| `y9g_gi6_sn7` | 任安 | [《史記・田叔列傳》][86] | [JSON](y9g_gi6_sn7.json) |
| `y9m_aj1_ara` | 參父（卷末世系） | [《史記・秦始皇本紀》][6] | [JSON](y9m_aj1_ara.json) |
| `y9m_l4i_das` | 徐甲 | [《史記・齊悼惠王世家》][34] | [JSON](y9m_l4i_das.json) |
| `y9v_ahh_z0x` | 穴熊（楚篇祖系） | [《史記・楚世家》][22] | [JSON](y9v_ahh_z0x.json) |
| `y9v_xi8_8n3` | 楚王卞和引古未名 | [《史記・魯仲連鄒陽列傳》][65] | [JSON](y9v_xi8_8n3.json) |
| `ya6_zdq_tu4` | 豫讓友未名 | [《史記・刺客列傳》][68] | [JSON](ya6_zdq_tu4.json) |
| `yad_hp5_rax` | 蒙恬 | [《史記・蒙恬列傳》][70] | [JSON](yad_hp5_rax.json) |
| `yav_84r_18q` | 常山王（武帝時未名） | [《史記・孝武本紀》][12] | [JSON](yav_84r_18q.json) |
| `ybb_2c4_8nx` | 公子知趙陰事客未名 | [《史記・魏公子列傳》][59] | [JSON](ybb_2c4_8nx.json) |
| `ybr_02v_5ux` | 趙王田獵未名 | [《史記・魏公子列傳》][59] | [JSON](ybr_02v_5ux.json) |
| `ybw_usv_89e` | 齊哀王未詳名 | [《史記・樊酈滕灌列傳》][77] | [JSON](ybw_usv_89e.json) |
| `ybw_y4h_z69` | 趙俊 | [《史記・趙世家》][25] | [JSON](ybw_y4h_z69.json) |
| `ybx_5gn_njg` | 田吸 | [《史記・樊酈滕灌列傳》][77] | [JSON](ybx_5gn_njg.json) |
| `ycg_exd_6oe` | 秦王（魏世家荊軻刺殺所指未名者） | [《史記・魏世家》][26] | [JSON](ycg_exd_6oe.json) |
| `ycl_yor_v0t` | 內史保 | [《史記・曹相國世家》][36] | [JSON](ycl_yor_v0t.json) |
| `yco_3yv_c8s` | 文王引古 | [《史記・范睢蔡澤列傳》][61] | [JSON](yco_3yv_c8s.json) |
| `ycr_d4w_b0x` | 則 | [《史記・齊悼惠王世家》][34] | [JSON](ycr_d4w_b0x.json) |
| `ycy_hv8_q6d` | 和仲 | [《史記・五帝本紀》][1] | [JSON](ycy_hv8_q6d.json) |
| `ye9_ftb_i0q` | 樊於期 | [《史記・刺客列傳》][68] | [JSON](ye9_ftb_i0q.json) |
| `yeg_27z_zzt` | 秦太后（韓世家羋戎姊未名者） | [《史記・韓世家》][27] | [JSON](yeg_27z_zzt.json) |
| `yeo_6mv_tut` | 中潏 | [《史記・秦本紀》][5] | [JSON](yeo_6mv_tut.json) |
| `yer_ylm_r9t` | 修成子仲 | [《史記・外戚世家》][31] | [JSON](yer_ylm_r9t.json) |
| `yes_bzi_dhx` | 衞君（魏世家未名者） | [《史記・魏世家》][26] | [JSON](yes_bzi_dhx.json) |
| `yfx_myv_qft` | 子西 | [《史記・楚世家》][22] | [JSON](yfx_myv_qft.json) |
| `yg1_ml2_61c` | 莊豹 | [《史記・樗里子甘茂列傳》][53] | [JSON](yg1_ml2_61c.json) |
| `ygr_80w_wp2` | 嬖姬（陳宣公款母） | [《史記・陳杞世家》][18] | [JSON](ygr_80w_wp2.json) |
| `yh1_ob5_1qm` | 魏太子申 | [《史記・魏世家》][26] | [JSON](yh1_ob5_1qm.json) |
| `yj2_zd2_kbu` | 國 | [《史記・趙世家》][25] | [JSON](yj2_zd2_kbu.json) |
| `yj4_x1h_xq0` | 侯嬴 | [《史記・魏公子列傳》][59] | [JSON](yj4_x1h_xq0.json) |
| `yj8_fds_vq5` | 驁 | [《史記・田敬仲完世家》][28] | [JSON](yj8_fds_vq5.json) |
| `yja_c73_i8o` | 顏聚 | [《史記・趙世家》][25]、[《史記・廉頗藺相如列傳》][63] | [JSON](yja_c73_i8o.json) |
| `yjq_7u5_fd1` | 楚懷王 | [《史記・留侯世家》][37] | [JSON](yjq_7u5_fd1.json) |
| `yjt_8w9_jgx` | 蔡兼 | [《史記・孝文本紀》][10] | [JSON](yjt_8w9_jgx.json) |
| `yk4_ms3_oy7` | 孟嘗君（楚篇田嬰子） | [《史記・楚世家》][22] | [JSON](yk4_ms3_oy7.json) |
| `yka_hay_sdj` | 任敖 | [《史記・張丞相列傳》][78] | [JSON](yka_hay_sdj.json) |
| `ykk_635_9eq` | 子思 | [《史記・孟子荀卿列傳》][56] | [JSON](ykk_635_9eq.json) |
| `ykw_i8p_jh3` | 愼到 | [《史記・孟子荀卿列傳》][56] | [JSON](ykw_i8p_jh3.json) |
| `ykz_dyf_q7h` | 田忌 | [《史記・秦始皇本紀》][6] | [JSON](ykz_dyf_q7h.json) |
| `yl3_vu7_xc8` | 周公旦（引古） | [《史記・蒙恬列傳》][70] | [JSON](yl3_vu7_xc8.json) |
| `ylb_xg7_6t9` | 王恬開 | [《史記・張釋之馮唐列傳》][84] | [JSON](ylb_xg7_6t9.json) |
| `ylo_ygy_hws` | 子反 | [《史記・晉世家》][21] | [JSON](ylo_ygy_hws.json) |
| `ym1_oml_zdw` | 伯宗 | [《史記・鄭世家》][24] | [JSON](ym1_oml_zdw.json) |
| `yma_ep3_js5` | 魏文侯 | [《史記・樗里子甘茂列傳》][53] | [JSON](yma_ep3_js5.json) |
| `ymc_cs7_t2f` | 曹宣公 | [《史記・吳太伯世家》][13] | [JSON](ymc_cs7_t2f.json) |
| `yme_rq2_21q` | 百里奚 | [《史記・孟子荀卿列傳》][56] | [JSON](yme_rq2_21q.json) |
| `yms_yqu_5yi` | 王齕 | [《史記・白起王翦列傳》][55] | [JSON](yms_yqu_5yi.json) |
| `ymw_kdn_zpz` | 大畢 | [《史記・周本紀》][4] | [JSON](ymw_kdn_zpz.json) |
| `ymz_578_wc0` | 秦二世 | [《史記・張釋之馮唐列傳》][84] | [JSON](ymz_578_wc0.json) |
| `yn0_whx_den` | 項伯 | [《史記・項羽本紀》][7] | [JSON](yn0_whx_den.json) |
| `yoi_fl7_1tg` | 齊王建（引古） | [《史記・蒙恬列傳》][70] | [JSON](yoi_fl7_1tg.json) |
| `yp2_s87_otm` | 燕太子丹 | [《史記・刺客列傳》][68] | [JSON](yp2_s87_otm.json) |
| `yp3_zjm_vup` | 廧咎如少女（趙世家未名者） | [《史記・趙世家》][25] | [JSON](yp3_zjm_vup.json) |
| `yp4_wb9_rwg` | 解揚 | [《史記・鄭世家》][24] | [JSON](yp4_wb9_rwg.json) |
| `ypb_4dr_10u` | 唐安 | [《史記・扁鵲倉公列傳》][87] | [JSON](ypb_4dr_10u.json) |
| `ypd_fmr_ydt` | 養由基 | [《史記・周本紀》][4] | [JSON](ypd_fmr_ydt.json) |
| `ypr_znm_81l` | 桓將軍未具名 | [《史記・吳王濞列傳》][88] | [JSON](ypr_znm_81l.json) |
| `yq9_p7b_qv4` | 韓不信（范中行之仇） | [《史記・晉世家》][21] | [JSON](yq9_p7b_qv4.json) |
| `yql_pki_bko` | 鬻子 | [《史記・周本紀》][4] | [JSON](yql_pki_bko.json) |
| `yqm_g1b_g6u` | 太子丹 | [《史記・樗里子甘茂列傳》][53] | [JSON](yqm_g1b_g6u.json) |
| `yqr_srv_j0g` | 魏桓子（殺知伯者） | [《史記・晉世家》][21] | [JSON](yqr_srv_j0g.json) |
| `yr4_cqs_3ya` | 蘇厲 | [《史記・趙世家》][25] | [JSON](yr4_cqs_3ya.json) |
| `yr6_rws_tx8` | 惠王 | [《史記・周本紀》][4] | [JSON](yr6_rws_tx8.json) |
| `yrc_rfa_m7q` | 桀引古 | [《史記・樂毅列傳》][62] | [JSON](yrc_rfa_m7q.json) |
| `yre_3um_pha` | 悍（屬國） | [《史記・孝文本紀》][10] | [JSON](yre_3um_pha.json) |
| `yrk_zdh_b9d` | 魏武侯（滅晉記事） | [《史記・晉世家》][21] | [JSON](yrk_zdh_b9d.json) |
| `ys4_jtg_6gu` | 芒卯 | [《史記・穰侯列傳》][54] | [JSON](ys4_jtg_6gu.json) |
| `ys4_x4f_ywp` | 齊宣王 | [《史記・老子韓非列傳》][45] | [JSON](ys4_x4f_ywp.json) |
| `ys7_zs9_61i` | 晉出公 | [《史記・趙世家》][25] | [JSON](ys7_zs9_61i.json) |
| `ysf_z9n_75l` | 楚王田需事件 | [《史記・張儀列傳》][52] | [JSON](ysf_z9n_75l.json) |
| `ysk_lvc_6ou` | 丞相偃 | [《史記・絳侯周勃世家》][39] | [JSON](ysk_lvc_6ou.json) |
| `yt0_0mx_ah5` | 石碏（衛諫臣） | [《史記・衛康叔世家》][19] | [JSON](yt0_0mx_ah5.json) |
| `yt5_lmc_jub` | 田駢 | [《史記・孟子荀卿列傳》][56] | [JSON](yt5_lmc_jub.json) |
| `yti_e9l_fle` | 高厚 | [《史記・齊太公世家》][14] | [JSON](yti_e9l_fle.json) |
| `ytl_g1y_wn3` | 子嬰 | [《史記・秦始皇本紀》][6] | [JSON](ytl_g1y_wn3.json) |
| `ytp_z6e_7yd` | 靳彊 | [《史記・項羽本紀》][7] | [JSON](ytp_z6e_7yd.json) |
| `yu4_0gm_gje` | 武臣 | [《史記・秦始皇本紀》][6] | [JSON](yu4_0gm_gje.json) |
| `yuo_kpg_rhg` | 閎夭 | [《史記・蕭相國世家》][35] | [JSON](yuo_kpg_rhg.json) |
| `yuq_yq1_oq6` | 公叔發（衞） | [《史記・吳太伯世家》][13] | [JSON](yuq_yq1_oq6.json) |
| `yv1_5v4_pjs` | 劉敬 | [《史記・劉敬叔孫通列傳》][81] | [JSON](yv1_5v4_pjs.json) |
| `yvi_fzl_2br` | 蒙嘉 | [《史記・刺客列傳》][68] | [JSON](yvi_fzl_2br.json) |
| `yvl_zaq_8e0` | 韓宣子 | [《史記・趙世家》][25] | [JSON](yvl_zaq_8e0.json) |
| `yvu_kzd_gnn` | 代王王后 | [《史記・外戚世家》][31] | [JSON](yvu_kzd_gnn.json) |
| `yvz_wen_i4n` | 呂馬童 | [《史記・項羽本紀》][7] | [JSON](yvz_wen_i4n.json) |
| `yw7_8ex_5co` | 東園公 | [《史記・留侯世家》][37] | [JSON](yw7_8ex_5co.json) |
| `ywi_8b8_8fv` | 公孫喜 | [《史記・魏世家》][26] | [JSON](ywi_8b8_8fv.json) |
| `ywp_lrf_bs0` | 代王（趙世家未名者） | [《史記・趙世家》][25] | [JSON](ywp_lrf_bs0.json) |
| `ywz_9xj_buq` | 周襄王 | [《史記・鄭世家》][24] | [JSON](ywz_9xj_buq.json) |
| `yx1_ywn_ylm` | 屈丐 | [《史記・屈原賈生列傳》][66] | [JSON](yx1_ywn_ylm.json) |
| `yy2_ghd_owh` | 子常（楚昭王臣） | [《史記・楚世家》][22] | [JSON](yy2_ghd_owh.json) |
| `yy2_xqa_njv` | 黥布 | [《史記・曹相國世家》][36] | [JSON](yy2_xqa_njv.json) |
| `yzf_1oe_uri` | 西伯昌 | [《史記・周本紀》][4] | [JSON](yzf_1oe_uri.json) |
| `yzg_zju_tse` | 廣利 | [《史記・外戚世家》][31] | [JSON](yzg_zju_tse.json) |
| `yzr_p69_1y0` | 陳平 | [《史記・張丞相列傳》][78] | [JSON](yzr_p69_1y0.json) |
| `yzt_6vt_wa5` | 窮蟬 | [《史記・五帝本紀》][1] | [JSON](yzt_6vt_wa5.json) |
| `z00_soe_xo2` | 平都 | [《史記・趙世家》][25] | [JSON](z00_soe_xo2.json) |
| `z0a_0yc_o18` | 即墨大夫未名 | [《史記・田單列傳》][64] | [JSON](z0a_0yc_o18.json) |
| `z0c_6ka_3bd` | 長（皇子） | [《史記・張丞相列傳》][78] | [JSON](z0c_6ka_3bd.json) |
| `z0v_ish_b9u` | 田光 | [《史記・刺客列傳》][68] | [JSON](z0v_ish_b9u.json) |
| `z16_hit_u7t` | 魯夫人（襄公女弟） | [《史記・魯周公世家》][15] | [JSON](z16_hit_u7t.json) |
| `z1h_j3h_k7e` | 髙辛氏 | [《史記・鄭世家》][24] | [JSON](z1h_j3h_k7e.json) |
| `z1t_d66_rx3` | 韓武子 | [《史記・魏世家》][26] | [JSON](z1t_d66_rx3.json) |
| `z1v_bog_yo6` | 翟璜 | [《史記・魏世家》][26] | [JSON](z1v_bog_yo6.json) |
| `z1v_d8t_kr6` | 雍 | [《史記・趙世家》][25] | [JSON](z1v_d8t_kr6.json) |
| `z2l_ycm_efi` | 太宰未名 | [《史記・黥布列傳》][73] | [JSON](z2l_ycm_efi.json) |
| `z2t_a1a_pjw` | 魚石（宋左師） | [《史記・宋微子世家》][20] | [JSON](z2t_a1a_pjw.json) |
| `z2v_yh8_x6u` | 楚王辭師未名 | [《史記・李斯列傳》][69] | [JSON](z2v_yh8_x6u.json) |
| `z37_ti3_yvl` | 孟女（莊公所愛） | [《史記・魯周公世家》][15] | [JSON](z37_ti3_yvl.json) |
| `z38_7dl_8of` | 史魚（衛篇季子所見者） | [《史記・衛康叔世家》][19] | [JSON](z38_7dl_8of.json) |
| `z3e_mtt_o3f` | 高永侯未具名 | [《史記・扁鵲倉公列傳》][87] | [JSON](z3e_mtt_o3f.json) |
| `z3i_xk4_rhj` | 湯 | [《史記・孫子吳起列傳》][47] | [JSON](z3i_xk4_rhj.json) |
| `z3m_gmf_gzf` | 齊桓公 | [《史記・田敬仲完世家》][28] | [JSON](z3m_gmf_gzf.json) |
| `z3q_36g_zqf` | 冉有 | [《史記・孔子世家》][29] | [JSON](z3q_36g_zqf.json) |
| `z3x_stp_h7o` | 齊襄王 | [《史記・穰侯列傳》][54] | [JSON](z3x_stp_h7o.json) |
| `z4e_mdk_ip3` | 守者吏未名 | [《史記・呂不韋列傳》][67] | [JSON](z4e_mdk_ip3.json) |
| `z4i_gl4_8un` | 費無忌 | [《史記・楚世家》][22] | [JSON](z4i_gl4_8un.json) |
| `z4k_uyh_8tr` | 漁父 | [《史記・伍子胥列傳》][48] | [JSON](z4k_uyh_8tr.json) |
| `z4p_57w_hfw` | 曹沫 | [《史記・刺客列傳》][68] | [JSON](z4p_57w_hfw.json) |
| `z5h_0si_ndg` | 秦女 | [《史記・伍子胥列傳》][48] | [JSON](z5h_0si_ndg.json) |
| `z6e_12m_z5v` | 虢仲（桓王伐曲沃使者） | [《史記・晉世家》][21] | [JSON](z6e_12m_z5v.json) |
| `z6g_h69_eva` | 丞相未名（元鼎五年罷） | [《史記・萬石張叔列傳》][85] | [JSON](z6g_h69_eva.json) |
| `z6l_cqj_6ts` | 射鴈者（勸楚頃襄王伐秦未名） | [《史記・楚世家》][22] | [JSON](z6l_cqj_6ts.json) |
| `z6m_hs4_r4a` | 陳平 | [《史記・樊酈滕灌列傳》][77] | [JSON](z6m_hs4_r4a.json) |
| `z7q_q8l_dcx` | 許由（讓天下引語） | [《史記・燕召公世家》][16] | [JSON](z7q_q8l_dcx.json) |
| `z90_wm5_kxf` | 履鞮（重耳追者） | [《史記・晉世家》][21] | [JSON](z90_wm5_kxf.json) |
| `z95_x33_jop` | 田榮 | [《史記・田儋列傳》][76] | [JSON](z95_x33_jop.json) |
| `z98_ddw_g89` | 韓安引古 | [《史記・李斯列傳》][69] | [JSON](z98_ddw_g89.json) |
| `z9k_f03_hq3` | 平原君 | [《史記・孝武本紀》][12] | [JSON](z9k_f03_hq3.json) |
| `z9s_kf9_ilc` | 上林尉未名 | [《史記・張釋之馮唐列傳》][84] | [JSON](z9s_kf9_ilc.json) |
| `z9y_ry1_zee` | 禹引古傳說 | [《史記・李斯列傳》][69] | [JSON](z9y_ry1_zee.json) |
| `za3_21s_pza` | 桓魋 | [《史記・孔子世家》][29] | [JSON](za3_21s_pza.json) |
| `zal_v7q_npx` | 友所愛姬（未名） | [《史記・呂太后本紀》][9] | [JSON](zal_v7q_npx.json) |
| `zba_qw2_7ne` | 儀行父（陳大夫） | [《史記・陳杞世家》][18] | [JSON](zba_qw2_7ne.json) |
| `zbd_q1x_hzd` | 公良孺 | [《史記・仲尼弟子列傳》][49] | [JSON](zbd_q1x_hzd.json) |
| `zbg_vy7_0bz` | 子反 | [《史記・鄭世家》][24] | [JSON](zbg_vy7_0bz.json) |
| `zbm_00e_awj` | 韓廣 | [《史記・陳涉世家》][30] | [JSON](zbm_00e_awj.json) |
| `zbn_rka_hlv` | 午 | [《史記・趙世家》][25] | [JSON](zbn_rka_hlv.json) |
| `zbs_mps_pf5` | 衛共姬（雍巫所寵） | [《史記・齊太公世家》][14] | [JSON](zbs_mps_pf5.json) |
| `zbu_bun_98q` | 魯姬子 | [《史記・秦本紀》][5] | [JSON](zbu_bun_98q.json) |
| `zbw_7zu_gv6` | 趙綰（武帝初公卿） | [《史記・孝武本紀》][12] | [JSON](zbw_7zu_gv6.json) |
| `zc4_kie_3tb` | 報丁 | [《史記・殷本紀》][3] | [JSON](zc4_kie_3tb.json) |
| `zdm_grc_6d2` | 韓玘引古 | [《史記・李斯列傳》][69] | [JSON](zdm_grc_6d2.json) |
| `zdt_mka_khc` | 齊威王 | [《史記・田敬仲完世家》][28] | [JSON](zdt_mka_khc.json) |
| `zdv_6wm_e1u` | 涇陽君 | [《史記・范睢蔡澤列傳》][61] | [JSON](zdv_6wm_e1u.json) |
| `ze0_kc1_agc` | 曹氏 | [《史記・齊悼惠王世家》][34] | [JSON](ze0_kc1_agc.json) |
| `ze3_vzo_049` | 梁伯（德成時） | [《史記・秦本紀》][5] | [JSON](ze3_vzo_049.json) |
| `zei_7yp_xzr` | 侯敞 | [《史記・樊酈滕灌列傳》][77] | [JSON](zei_7yp_xzr.json) |
| `zev_jx4_vaz` | 樗里子 | [《史記・穰侯列傳》][54] | [JSON](zev_jx4_vaz.json) |
| `zex_g0x_52d` | 田子莊何 | [《史記・仲尼弟子列傳》][49] | [JSON](zex_g0x_52d.json) |
| `zf3_s9n_ty5` | 牙（齊太子） | [《史記・齊太公世家》][14] | [JSON](zf3_s9n_ty5.json) |
| `zfk_w9y_0b8` | 百里奚（引古） | [《史記・淮陰侯列傳》][74] | [JSON](zfk_w9y_0b8.json) |
| `zg6_76t_xid` | 少翁 | [《史記・孝武本紀》][12] | [JSON](zg6_76t_xid.json) |
| `zg8_rjh_2jl` | 主父沙丘 | [《史記・范睢蔡澤列傳》][61] | [JSON](zg8_rjh_2jl.json) |
| `zh2_5e4_ikn` | 酈寄 | [《史記・楚元王世家》][32] | [JSON](zh2_5e4_ikn.json) |
| `zht_ze7_m2d` | 山／義／弘（後少帝） | [《史記・呂太后本紀》][9] | [JSON](zht_ze7_m2d.json) |
| `zi3_x31_9g6` | 周聚 | [《史記・陳涉世家》][30] | [JSON](zi3_x31_9g6.json) |
| `zip_jr2_0be` | 龍且 | [《史記・樊酈滕灌列傳》][77] | [JSON](zip_jr2_0be.json) |
| `zir_4c6_exy` | 肥（宋太子） | [《史記・宋微子世家》][20] | [JSON](zir_4c6_exy.json) |
| `ziy_qr8_mi9` | 夷維子引古 | [《史記・魯仲連鄒陽列傳》][65] | [JSON](ziy_qr8_mi9.json) |
| `zji_rm6_vl9` | 宋建 | [《史記・扁鵲倉公列傳》][87] | [JSON](zji_rm6_vl9.json) |
| `zjm_0fv_ke9` | 周幽王 | [《史記・楚世家》][22] | [JSON](zjm_0fv_ke9.json) |
| `zk2_9k4_xg5` | 史佚 | [《史記・晉世家》][21] | [JSON](zk2_9k4_xg5.json) |
| `zk3_4et_ajm` | 亞夫夫人 | [《史記・絳侯周勃世家》][39] | [JSON](zk3_4et_ajm.json) |
| `zkl_2cm_e8u` | 弗忌 | [《史記・秦本紀》][5]、[《史記・秦始皇本紀》][6] | [JSON](zkl_2cm_e8u.json) |
| `zmm_7qs_gt3` | 漆雕徒父 | [《史記・仲尼弟子列傳》][49] | [JSON](zmm_7qs_gt3.json) |
| `zmn_o2u_kwm` | 周宣王 | [《史記・趙世家》][25] | [JSON](zmn_o2u_kwm.json) |
| `zn2_vwj_e9n` | 北地都尉卬 | [《史記・孝文本紀》][10] | [JSON](zn2_vwj_e9n.json) |
| `zn6_9ne_atr` | 趙王遷（楚篇秦虜者） | [《史記・楚世家》][22] | [JSON](zn6_9ne_atr.json) |
| `zno_zup_85b` | 昌若 | [《史記・殷本紀》][3] | [JSON](zno_zup_85b.json) |
| `zo2_hd4_x73` | 子嬰 | [《史記・秦始皇本紀》][6] | [JSON](zo2_hd4_x73.json) |
| `zoh_v2m_0ol` | 甫侯 | [《史記・周本紀》][4] | [JSON](zoh_v2m_0ol.json) |
| `zp1_fiy_44m` | 秦非 | [《史記・仲尼弟子列傳》][49] | [JSON](zp1_fiy_44m.json) |
| `zp9_5vn_rqb` | 秦王馮驩遊說未定 | [《史記・孟嘗君列傳》][57] | [JSON](zp9_5vn_rqb.json) |
| `zpb_vdo_mka` | 大王去邠 | [《史記・孟子荀卿列傳》][56] | [JSON](zpb_vdo_mka.json) |
| `zpl_q9c_nur` | 智開 | [《史記・秦本紀》][5] | [JSON](zpl_q9c_nur.json) |
| `zpq_qyu_2sl` | 韓信 | [《史記・淮陰侯列傳》][74] | [JSON](zpq_qyu_2sl.json) |
| `zpv_ei1_hhy` | 齊湣王（陳篇滅宋記事） | [《史記・陳杞世家》][18]、[《史記・宋微子世家》][20] | [JSON](zpv_ei1_hhy.json) |
| `zqd_xej_g85` | 子輿 | [《史記・扁鵲倉公列傳》][87] | [JSON](zqd_xej_g85.json) |
| `zqx_760_8l5` | 周敬王 | [《史記・趙世家》][25] | [JSON](zqx_760_8l5.json) |
| `zqy_a21_8d3` | 任鄙 | [《史記・秦本紀》][5] | [JSON](zqy_a21_8d3.json) |
| `zqy_y5v_rf6` | 韓信 | [《史記・淮陰侯列傳》][74] | [JSON](zqy_y5v_rf6.json) |
| `zr7_8hl_01r` | 皋羊（陳相公） | [《史記・陳杞世家》][18] | [JSON](zr7_8hl_01r.json) |
| `zru_24j_blp` | 稷 | [《史記・仲尼弟子列傳》][49] | [JSON](zru_24j_blp.json) |
| `zs7_2hu_ho4` | 項燕 | [《史記・蒙恬列傳》][70] | [JSON](zs7_2hu_ho4.json) |
| `ztb_e3k_fzf` | 韓女 | [《史記・扁鵲倉公列傳》][87] | [JSON](ztb_e3k_fzf.json) |
| `ztm_j3g_k1n` | 昭公子（宋文公誅者未名） | [《史記・宋微子世家》][20] | [JSON](ztm_j3g_k1n.json) |
| `ztm_pmc_2w7` | 齊頃公母（蕭桐姪子） | [《史記・晉世家》][21] | [JSON](ztm_pmc_2w7.json) |
| `zu4_zoq_n1q` | 竇長君 | [《史記・季布欒布列傳》][82] | [JSON](zu4_zoq_n1q.json) |
| `zuk_d9k_nqk` | 鄒衍 | [《史記・孟子荀卿列傳》][56] | [JSON](zuk_d9k_nqk.json) |
| `zuk_pbo_x9s` | 范睢引古 | [《史記・范睢蔡澤列傳》][61] | [JSON](zuk_pbo_x9s.json) |
| `zul_9qs_fhz` | 庶長壯 | [《史記・秦本紀》][5] | [JSON](zul_9qs_fhz.json) |
| `zun_s94_rgs` | 春申君黃歇 | [《史記・春申君列傳》][60] | [JSON](zun_s94_rgs.json) |
| `zus_do8_z1q` | 范睢 | [《史記・范睢蔡澤列傳》][61] | [JSON](zus_do8_z1q.json) |
| `zuu_z5b_y3u` | 熊艾（楚先祖） | [《史記・楚世家》][22] | [JSON](zuu_z5b_y3u.json) |
| `zwm_75s_4li` | 馮亭 | [《史記・趙世家》][25] | [JSON](zwm_75s_4li.json) |
| `zwx_rs0_1lh` | 史鰍 | [《史記・吳太伯世家》][13] | [JSON](zwx_rs0_1lh.json) |
| `zx3_4gt_0uq` | 宋王（田世家出亡未名者） | [《史記・田敬仲完世家》][28] | [JSON](zx3_4gt_0uq.json) |
| `zx8_mjk_l6m` | 張儀 | [《史記・韓世家》][27] | [JSON](zx8_mjk_l6m.json) |
| `zxd_afr_2xg` | 黥布 | [《史記・黥布列傳》][73] | [JSON](zxd_afr_2xg.json) |
| `zxi_coo_7up` | 紂引古 | [《史記・李斯列傳》][69] | [JSON](zxi_coo_7up.json) |
| `zxu_7n3_ry9` | 宰夫（靈公所殺者未名） | [《史記・晉世家》][21] | [JSON](zxu_7n3_ry9.json) |
| `zxv_fao_cpq` | 周市 | [《史記・陳丞相世家》][38] | [JSON](zxv_fao_cpq.json) |
| `zy0_phw_hl6` | 門下前對者未名 | [《史記・平原君虞卿列傳》][58] | [JSON](zy0_phw_hl6.json) |
| `zy7_ewt_vzi` | 韓哀侯 | [《史記・刺客列傳》][68] | [JSON](zy7_ewt_vzi.json) |
| `zz5_41m_e35` | 韓王信 | [《史記・韓信盧綰列傳》][75] | [JSON](zz5_41m_e35.json) |
| `zzt_bu4_6zm` | 王齮 | [《史記・呂不韋列傳》][67] | [JSON](zzt_bu4_6zm.json) |
| `zzu_ykb_79u` | 齊湣王 | [《史記・范睢蔡澤列傳》][61] | [JSON](zzu_ykb_79u.json) |

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
