# 人物 JSON 索引

可重建匯出，涵蓋目前已標註資料，包含明示選用的暫定跨篇同指；原 ID、證據與判讀均保留。並非全部史料或完整覆核。

程式可讀取 [index.json](index.json)，再依各筆 `path` 取得人物資料。重新產生：`python3 scripts/export_person_bundles.py`。

出生排行與籍貫結構化欄位仍在逐篇回填；缺欄位不代表來源沒有此資訊。

已接合父系見 [家族組裝資料](../../registry/family-assemblies.json)。`assembled_identity.person_id` 是共用家族根的組裝 ID，`source_person_ids` 保留各篇候選；父子及同指證據可由記錄 ID 回查。缺代節點另有 `ancestor_person_id`、`generation_distance` 與空值中間世代；父親空值不表示它另成一族。

點選家族標題可展開或收起後代。`*` 表示缺名世代，不建立人物，也不表示不同缺名位置是同一人。表內只列家族根後的 ID 尾碼；根人物以「根」表示，完整 ID 保留於家族標題及 JSON。最多提及來源另列一欄，同數並列；提及次數不代表史料優先權。已完成格式遷移的舊 ID 與 JSON 入口已撤除；待身份覆核的來源候選仍分存。

尚未連入同族的人物見 [獨立人物索引](unconnected.md)。

## 可展開家族


[第1頁](README.md)

<details><summary><code>04o_yps_sg0</code> 張湯（汲鄭列傳候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 張湯 | [《史記・酷吏列傳》][108] | [JSON](04o_yps_sg0.json) |
| `A` | 安世 | [《史記・酷吏列傳》][108] | [JSON](04o_yps_sg0_A.json) |

</details>

<details><summary><code>04u_gq0_nke</code> 鼂錯父未名（袁盎鼂錯列傳候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 鼂錯父未名 | [《史記・袁盎鼂錯列傳》][87] | [JSON](04u_gq0_nke.json) |
| `A` | 鼂錯 | [《史記・袁盎鼂錯列傳》][87] | [JSON](04u_gq0_nke_A.json) |

</details>

<details><summary><code>06i_k5v_922</code> 申侯（鄭世家武姜父候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 申侯 | [《史記・鄭世家》][28] | [JSON](06i_k5v_922.json) |
| `A` | 武姜 | [《史記・鄭世家》][28] | [JSON](06i_k5v_922_A.json) |

</details>

<details><summary><code>0ad_dbw_97q</code> 晉昭公（4 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 晉昭公 | [《史記・晉世家》][25] | [JSON](0ad_dbw_97q.json) |
| `A` | 雍（戴子晉昭公子） | [《史記・晉世家》][25] | [JSON](0ad_dbw_97q_A.json) |
| `AA` | 忌（戴子子） | [《史記・晉世家》][25] | [JSON](0ad_dbw_97q_AA.json) |
| `AAA` | 驕（晉哀公） | [《史記・晉世家》][25] | [JSON](0ad_dbw_97q_AAA.json) |

</details>

<details><summary><code>0bu_skv_qsr</code> 呂青（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 呂青 | [《史記・項羽本紀》][11]、[《史記・高祖本紀》][12] | [JSON](0bu_skv_qsr.json) |
| `A` | 呂臣 | [《史記・項羽本紀》][11]、[《史記・高祖本紀》][12] | [JSON](0bu_skv_qsr_A.json) |

</details>

<details><summary><code>0hs_fg6_1qj</code> 田榮（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 田榮 | [《史記・田儋列傳》][80] | [JSON](0hs_fg6_1qj.json) |
| `A` | 廣（田榮子） | [《史記・酈生陸賈列傳》][83] | [JSON](0hs_fg6_1qj_A.json) |
| `B` | 田廣 | [《史記・田儋列傳》][80] | [JSON](0hs_fg6_1qj_B.json) |

</details>

<details><summary><code>0s7_r72_j8q</code> 魯武公（4 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 魯武公 | [《史記・魯周公世家》][19] | [JSON](0s7_r72_j8q.json) |
| `A` | 括（魯武公長子） | [《史記・魯周公世家》][19] | [JSON](0s7_r72_j8q_A.json) |
| `AA` | 伯御（魯君） | [《史記・魯周公世家》][19] | [JSON](0s7_r72_j8q_AA.json) |
| `B` | 戲（魯懿公） | [《史記・魯周公世家》][19] | [JSON](0s7_r72_j8q_B.json) |

</details>

<details><summary><code>0us_j8h_to7</code> 假（老韓列傳候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 假 | [《史記・老子韓非列傳》][49] | [JSON](0us_j8h_to7.json) |
| `A` | 解 | [《史記・老子韓非列傳》][49] | [JSON](0us_j8h_to7_A.json) |

</details>

<details><summary><code>0xt_iyn_d3t</code> 趙夙（趙世家候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 趙夙 | [《史記・趙世家》][29] | [JSON](0xt_iyn_d3t.json) |
| `A` | 共孟 | [《史記・趙世家》][29] | [JSON](0xt_iyn_d3t_A.json) |

</details>

<details><summary><code>113_odk_emq</code> 衞綰（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 衞綰 | [《史記・萬石張叔列傳》][89] | [JSON](113_odk_emq.json) |
| `A` | 信（衞綰子） | [《史記・萬石張叔列傳》][89] | [JSON](113_odk_emq_A.json) |

</details>

<details><summary><code>128_4ab_z34</code> 熊延（楚君）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 熊延（楚君） | [《史記・楚世家》][26] | [JSON](128_4ab_z34.json) |
| `A` | 熊勇（楚君） | [《史記・楚世家》][26] | [JSON](128_4ab_z34_A.json) |

</details>

<details><summary><code>1g3_02y_oor</code> 太公望（5 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 太公望 | [《史記・齊太公世家》][18] | [JSON](1g3_02y_oor.json) |
| `A` | 丁公呂伋 | [《史記・齊太公世家》][18] | [JSON](1g3_02y_oor_A.json) |
| `AA` | 得（齊乙公） | [《史記・齊太公世家》][18] | [JSON](1g3_02y_oor_AA.json) |
| `AAA` | 慈母（齊癸公） | [《史記・齊太公世家》][18] | [JSON](1g3_02y_oor_AAA.json) |
| `AAAA` | 不辰（齊哀公） | [《史記・齊太公世家》][18] | [JSON](1g3_02y_oor_AAAA.json) |

</details>

<details><summary><code>1h3_vs7_t8h</code> 齊湣王（燕篇）（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 齊湣王（燕篇） | [《史記・燕召公世家》][20] | [JSON](1h3_vs7_t8h.json) |
| `A` | 襄王（齊湣王子） | [《史記・田敬仲完世家》][32] | [JSON](1h3_vs7_t8h_A.json) |
| `AA` | 齊王建 | [《史記・田敬仲完世家》][32] | [JSON](1h3_vs7_t8h_AA.json) |

</details>

<details><summary><code>1hf_1k0_bnj</code> 夷仲年（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 夷仲年 | [《史記・齊太公世家》][18]、[《史記・十二諸侯年表》][119] | [JSON](1hf_1k0_bnj.json) |
| `A` | 公孫無知 | [《史記・齊太公世家》][18] | [JSON](1hf_1k0_bnj_A.json) |

</details>

<details><summary><code>1l4_2pq_e7w</code> 熊通（楚武王候選）（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 熊通 | [《史記・楚世家》][26] | [JSON](1l4_2pq_e7w.json) |
| `A` | 熊貲（楚文王） | [《史記・楚世家》][26] | [JSON](1l4_2pq_e7w_A.json) |
| `AA` | 熊艱（莊敖） | [《史記・楚世家》][26] | [JSON](1l4_2pq_e7w_AA.json) |

</details>

<details><summary><code>1pc_mnq_z0c</code> 懿公（燕文公後）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 懿公（燕文公後） | [《史記・燕召公世家》][20] | [JSON](1pc_mnq_z0c.json) |
| `A` | 惠公（燕懿公子） | [《史記・燕召公世家》][20] | [JSON](1pc_mnq_z0c_A.json) |

</details>

<details><summary><code>1y5_eke_4gl</code> 陽慶（扁鵲倉公列傳候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 陽慶 | [《史記・扁鵲倉公列傳》][91] | [JSON](1y5_eke_4gl.json) |
| `A` | 殷（慶子） | [《史記・扁鵲倉公列傳》][91] | [JSON](1y5_eke_4gl_A.json) |

</details>

<details><summary><code>1za_blw_7lb</code> 伯魯（趙世家候選）（6 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 伯魯 | [《史記・趙世家》][29] | [JSON](1za_blw_7lb.json) |
| `A` | 周 | [《史記・趙世家》][29] | [JSON](1za_blw_7lb_A.json) |
| `AA` | 浣 | [《史記・趙世家》][29] | [JSON](1za_blw_7lb_AA.json) |
| `AAA` | 籍 | [《史記・趙世家》][29] | [JSON](1za_blw_7lb_AAA.json) |
| `AAAA` | 章 | [《史記・趙世家》][29] | [JSON](1za_blw_7lb_AAAA.json) |
| `AAAAA` | 種 | [《史記・趙世家》][29] | [JSON](1za_blw_7lb_AAAAA.json) |

</details>

<details><summary><code>27j_f4p_jwp</code> 李廣（7 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 李廣 | [《史記・李將軍列傳》][95] | [JSON](27j_f4p_jwp.json) |
| `A` | 李敢 | [《史記・李將軍列傳》][95] | [JSON](27j_f4p_jwp_A.json) |
| `AA` | 李敢女（未名） | [《史記・李將軍列傳》][95] | [JSON](27j_f4p_jwp_AA.json) |
| `AB` | 禹（李敢男） | [《史記・李將軍列傳》][95] | [JSON](27j_f4p_jwp_AB.json) |
| `B` | 當戸 | [《史記・李將軍列傳》][95] | [JSON](27j_f4p_jwp_B.json) |
| `BA` | 李陵 | [《史記・李將軍列傳》][95] | [JSON](27j_f4p_jwp_BA.json) |
| `C` | 椒 | [《史記・李將軍列傳》][95] | [JSON](27j_f4p_jwp_C.json) |

</details>

<details><summary><code>2d3_fsd_1dh</code> 楚成王（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 楚成王 | [《史記・晉世家》][25] | [JSON](2d3_fsd_1dh.json) |
| `A` | 楚商臣 | [《史記・陳杞世家》][22] | [JSON](2d3_fsd_1dh_A.json) |

</details>

<details><summary><code>2v6_0g1_ve2</code> 衍（宋微仲）（12 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 衍（宋微仲） | [《史記・宋微子世家》][24] | [JSON](2v6_0g1_ve2.json) |
| `A` | 稽（宋公） | [《史記・宋微子世家》][24] | [JSON](2v6_0g1_ve2_A.json) |
| `AA` | 申（宋丁公） | [《史記・宋微子世家》][24] | [JSON](2v6_0g1_ve2_AA.json) |
| `AAA` | 共（宋湣公） | [《史記・宋微子世家》][24] | [JSON](2v6_0g1_ve2_AAA.json) |
| `AAAA` | 鮒祀（宋厲公） | [《史記・宋微子世家》][24] | [JSON](2v6_0g1_ve2_AAAA.json) |
| `AAAAA` | 舉（宋釐公） | [《史記・宋微子世家》][24] | [JSON](2v6_0g1_ve2_AAAAA.json) |
| `AAAAAA` | 覵（宋惠公） | [《史記・宋微子世家》][24] | [JSON](2v6_0g1_ve2_AAAAAA.json) |
| `AAAAAAA` | 哀公（宋惠公子） | [《史記・宋微子世家》][24] | [JSON](2v6_0g1_ve2_AAAAAAA.json) |
| `AAAAAAAA` | 戴公（宋哀公子） | [《史記・宋微子世家》][24] | [JSON](2v6_0g1_ve2_AAAAAAAA.json) |
| `AAAAAAAAA` | 司空（宋武公） | [《史記・宋微子世家》][24] | [JSON](2v6_0g1_ve2_AAAAAAAAA.json) |
| `AAAAAAAAAA` | 宋女（魯惠公夫人） | [《史記・宋微子世家》][24] | [JSON](2v6_0g1_ve2_AAAAAAAAAA.json) |
| `AAAAAAAAAB` | 力（宋宣公） | [《史記・宋微子世家》][24] | [JSON](2v6_0g1_ve2_AAAAAAAAAB.json) |

</details>

<details><summary><code>37j_16p_7n8</code> 曹參（6 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 曹參 | [《史記・曹相國世家》][40] | [JSON](37j_16p_7n8.json) |
| `A` | 窋 | [《史記・曹相國世家》][40] | [JSON](37j_16p_7n8_A.json) |
| `AA` | 奇 | [《史記・曹相國世家》][40] | [JSON](37j_16p_7n8_AA.json) |
| `AAA` | 時 | [《史記・曹相國世家》][40] | [JSON](37j_16p_7n8_AAA.json) |
| `AAAA` | 襄 | [《史記・衛將軍驃騎列傳》][97] | [JSON](37j_16p_7n8_AAAA.json) |
| `AAAAA` | 宗 | [《史記・曹相國世家》][40] | [JSON](37j_16p_7n8_AAAAA.json) |

</details>

<details><summary><code>3jf_ce1_jy2</code> 昆莫父（未名）（大宛列傳候選）（5 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 昆莫父（未名） | [《史記・大宛列傳》][109] | [JSON](3jf_ce1_jy2.json) |
| `A` | 昆莫 | [《史記・大宛列傳》][109] | [JSON](3jf_ce1_jy2_A.json) |
| `AA` | 大祿 | [《史記・大宛列傳》][109] | [JSON](3jf_ce1_jy2_AA.json) |
| `AB` | 大祿兄（未名太子） | [《史記・大宛列傳》][109] | [JSON](3jf_ce1_jy2_AB.json) |
| `ABA` | 岑娶 | [《史記・大宛列傳》][109] | [JSON](3jf_ce1_jy2_ABA.json) |

</details>

<details><summary><code>3te_z66_d5a</code> 張敖（外戚世家候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 張敖 | [《史記・外戚世家》][35] | [JSON](3te_z66_d5a.json) |
| `A` | 孝惠皇后 | [《史記・外戚世家》][35] | [JSON](3te_z66_d5a_A.json) |

</details>

<details><summary><code>3tw_nq2_gyn</code> 霍去病（外戚世家候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 霍去病 | [《史記・衛將軍驃騎列傳》][97] | [JSON](3tw_nq2_gyn.json) |
| `A` | 嬗 | [《史記・衛將軍驃騎列傳》][97] | [JSON](3tw_nq2_gyn_A.json) |

</details>

<details><summary><code>42z_cse_1ka</code> 熊良夫（楚宣王）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 熊良夫（楚宣王） | [《史記・楚世家》][26] | [JSON](42z_cse_1ka.json) |
| `A` | 熊商（楚威王） | [《史記・楚世家》][26] | [JSON](42z_cse_1ka_A.json) |

</details>

<details><summary><code>46a_tvp_dq9</code> 秦獻公（魏世家候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 秦獻公 | [《史記・魏世家》][30] | [JSON](46a_tvp_dq9.json) |
| `A` | 秦孝公 | [《史記・魏世家》][30] | [JSON](46a_tvp_dq9_A.json) |

</details>

<details><summary><code>49g_7az_e4i</code> 李斯（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 李斯 | [《史記・李斯列傳》][73] | [JSON](49g_7az_e4i.json) |
| `A` | 李由 | [《史記・李斯列傳》][73] | [JSON](49g_7az_e4i_A.json) |
| `B` | 李斯中子未名 | [《史記・李斯列傳》][73] | [JSON](49g_7az_e4i_B.json) |

</details>

<details><summary><code>4w5_b4e_vf5</code> 王翁孺（14 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 王翁孺 | [《漢書・元后傳》][4] | [JSON](4w5_b4e_vf5.json) |
| `A` | 王禁 | [《漢書・元后傳》][4] | [JSON](4w5_b4e_vf5_A.json) |
| `AA` | 君俠 | [《漢書・元后傳》][4] | [JSON](4w5_b4e_vf5_AA.json) |
| `AB` | 政君 | [《漢書・元后傳》][4] | [JSON](4w5_b4e_vf5_AB.json) |
| `AC` | 君力 | [《漢書・元后傳》][4] | [JSON](4w5_b4e_vf5_AC.json) |
| `AD` | 君弟 | [《漢書・元后傳》][4] | [JSON](4w5_b4e_vf5_AD.json) |
| `AE` | 鳳 | [《漢書・元后傳》][4] | [JSON](4w5_b4e_vf5_AE.json) |
| `AF` | 曼 | [《漢書・元后傳》][4] | [JSON](4w5_b4e_vf5_AF.json) |
| `AG` | 譚 | [《漢書・元后傳》][4] | [JSON](4w5_b4e_vf5_AG.json) |
| `AH` | 崇 | [《漢書・元后傳》][4] | [JSON](4w5_b4e_vf5_AH.json) |
| `AI` | 商 | [《漢書・元后傳》][4] | [JSON](4w5_b4e_vf5_AI.json) |
| `AJ` | 立 | [《漢書・元后傳》][4] | [JSON](4w5_b4e_vf5_AJ.json) |
| `AK` | 根 | [《漢書・元后傳》][4] | [JSON](4w5_b4e_vf5_AK.json) |
| `AL` | 逢時 | [《漢書・元后傳》][4] | [JSON](4w5_b4e_vf5_AL.json) |

</details>

<details><summary><code>4wv_6og_mwb</code> 申無宇（芋尹）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 申無宇（芋尹） | [《史記・楚世家》][26] | [JSON](4wv_6og_mwb.json) |
| `A` | 申亥（收葬楚靈王者） | [《史記・楚世家》][26] | [JSON](4wv_6og_mwb_A.json) |

</details>

<details><summary><code>4xe_ms4_pr9</code> 夢者（曹亡敘事未名）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 夢者（曹亡敘事未名） | [《史記・管蔡世家》][21] | [JSON](4xe_ms4_pr9.json) |
| `A` | 夢者子（未名） | [《史記・管蔡世家》][21] | [JSON](4xe_ms4_pr9_A.json) |

</details>

<details><summary><code>4yg_ete_09a</code> 柴武（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 柴武 | [《史記・韓信盧綰列傳》][79] | [JSON](4yg_ete_09a.json) |
| `A` | 奇（柴武子） | [《史記・淮南衡山列傳》][104] | [JSON](4yg_ete_09a_A.json) |

</details>

<details><summary><code>505_n4y_p39</code> 秦開（匈奴列傳候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 秦開 | [《史記・匈奴列傳》][96] | [JSON](505_n4y_p39.json) |
| `*A` | 秦舞陽 | [《史記・刺客列傳》][72] | [JSON](505_n4y_p39_%2AA.json) |

</details>

<details><summary><code>50h_gqe_1p1</code> 具（魯獻公）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 具（魯獻公） | [《史記・魯周公世家》][19] | [JSON](50h_gqe_1p1.json) |
| `A` | 濞（魯真公） | [《史記・魯周公世家》][19]、[《史記・三代世表》][118] | [JSON](50h_gqe_1p1_A.json) |

</details>

<details><summary><code>5bo_dxd_69k</code> 冉雍父（弟子列傳候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 冉雍父 | [《史記・仲尼弟子列傳》][53] | [JSON](5bo_dxd_69k.json) |
| `A` | 冉雍 | [《史記・仲尼弟子列傳》][53] | [JSON](5bo_dxd_69k_A.json) |

</details>

<details><summary><code>5dd_l1c_6g8</code> 衛青（外戚世家候選）（5 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 衛青 | [《史記・衛將軍驃騎列傳》][97] | [JSON](5dd_l1c_6g8.json) |
| `A` | 衛青子陰安侯 | [《史記・衛將軍驃騎列傳》][97] | [JSON](5dd_l1c_6g8_A.json) |
| `B` | 衛青子發干侯 | [《史記・衛將軍驃騎列傳》][97] | [JSON](5dd_l1c_6g8_B.json) |
| `C` | 衛青子宜春侯（來源候選；預設不接父系） | [《史記・外戚世家》][35] | [JSON](5dd_l1c_6g8_C.json) |
| `D` | 衛伉 | [《史記・衛將軍驃騎列傳》][97] | [JSON](5dd_l1c_6g8_D.json) |

</details>

<details><summary><code>5dm_e40_rqh</code> 古公亶父（28 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 古公亶父 | [《史記・周本紀》][8] | [JSON](5dm_e40_rqh.json) |
| `A` | 仲雍 | [《史記・吳太伯世家》][17] | [JSON](5dm_e40_rqh_A.json) |
| `AA` | 季簡 | [《史記・吳太伯世家》][17] | [JSON](5dm_e40_rqh_AA.json) |
| `AAA` | 叔達 | [《史記・吳太伯世家》][17] | [JSON](5dm_e40_rqh_AAA.json) |
| `AAAA` | 周章（吳君） | [《史記・吳太伯世家》][17] | [JSON](5dm_e40_rqh_AAAA.json) |
| `AAAAA` | 熊遂 | [《史記・吳太伯世家》][17] | [JSON](5dm_e40_rqh_AAAAA.json) |
| `AAAAAA` | 柯相 | [《史記・吳太伯世家》][17] | [JSON](5dm_e40_rqh_AAAAAA.json) |
| `AAAAAAA` | 彊鳩夷 | [《史記・吳太伯世家》][17] | [JSON](5dm_e40_rqh_AAAAAAA.json) |
| `AAAAAAAA` | 餘橋疑吾 | [《史記・吳太伯世家》][17] | [JSON](5dm_e40_rqh_AAAAAAAA.json) |
| `AAAAAAAAA` | 柯盧 | [《史記・吳太伯世家》][17] | [JSON](5dm_e40_rqh_AAAAAAAAA.json) |
| `AAAAAAAAAA` | 周繇 | [《史記・吳太伯世家》][17] | [JSON](5dm_e40_rqh_AAAAAAAAAA.json) |
| `AAAAAAAAAAA` | 屈羽 | [《史記・吳太伯世家》][17] | [JSON](5dm_e40_rqh_AAAAAAAAAAA.json) |
| `AAAAAAAAAAAA` | 夷吾（吳君） | [《史記・吳太伯世家》][17] | [JSON](5dm_e40_rqh_AAAAAAAAAAAA.json) |
| `AAAAAAAAAAAAA` | 禽處 | [《史記・吳太伯世家》][17] | [JSON](5dm_e40_rqh_AAAAAAAAAAAAA.json) |
| `AAAAAAAAAAAAAA` | 轉（吳君） | [《史記・吳太伯世家》][17] | [JSON](5dm_e40_rqh_AAAAAAAAAAAAAA.json) |
| `AAAAAAAAAAAAAAA` | 頗髙 | [《史記・吳太伯世家》][17] | [JSON](5dm_e40_rqh_AAAAAAAAAAAAAAA.json) |
| `AAAAAAAAAAAAAAAA` | 句卑 | [《史記・吳太伯世家》][17] | [JSON](5dm_e40_rqh_AAAAAAAAAAAAAAAA.json) |
| `AAAAAAAAAAAAAAAAA` | 去齊 | [《史記・吳太伯世家》][17] | [JSON](5dm_e40_rqh_AAAAAAAAAAAAAAAAA.json) |
| `AAAAAAAAAAAAAAAAAA` | 壽夢 | [《史記・吳太伯世家》][17] | [JSON](5dm_e40_rqh_AAAAAAAAAAAAAAAAAA.json) |
| `AAAAAAAAAAAAAAAAAAA` | 諸樊 | [《史記・吳太伯世家》][17] | [JSON](5dm_e40_rqh_AAAAAAAAAAAAAAAAAAA.json) |
| `AAAAAAAAAAAAAAAAAAAA` | 闔閭 | [《史記・吳太伯世家》][17] | [JSON](5dm_e40_rqh_AAAAAAAAAAAAAAAAAAAA.json) |
| `AAAAAAAAAAAAAAAAAAAAA` | 夫差 | [《史記・越王勾踐世家》][27] | [JSON](5dm_e40_rqh_AAAAAAAAAAAAAAAAAAAAA.json) |
| `AAAAAAAAAAAAAAAAAAB` | 餘祭 | [《史記・吳太伯世家》][17] | [JSON](5dm_e40_rqh_AAAAAAAAAAAAAAAAAAB.json) |
| `AAAAAAAAAAAAAAAAAAC` | 餘眛 | [《史記・吳太伯世家》][17] | [JSON](5dm_e40_rqh_AAAAAAAAAAAAAAAAAAC.json) |
| `AAAAAAAAAAAAAAAAAACA` | 僚（吳王） | [《史記・吳太伯世家》][17] | [JSON](5dm_e40_rqh_AAAAAAAAAAAAAAAAAACA.json) |
| `AAAAAAAAAAAAAAAAAAD` | 季札 | [《史記・吳太伯世家》][17] | [JSON](5dm_e40_rqh_AAAAAAAAAAAAAAAAAAD.json) |
| `B` | 太伯 | [《史記・吳太伯世家》][17] | [JSON](5dm_e40_rqh_B.json) |
| `C` | 虞仲 | [《史記・周本紀》][8] | [JSON](5dm_e40_rqh_C.json) |

</details>

<details><summary><code>5if_pf6_zos</code> 郭解父（未名）（游俠列傳候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 郭解父（未名） | [《史記・游俠列傳》][110] | [JSON](5if_pf6_zos.json) |
| `A` | 郭解 | [《史記・游俠列傳》][110] | [JSON](5if_pf6_zos_A.json) |

</details>

<details><summary><code>5km_89r_9jr</code> 元君（衛嗣君弟）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 元君（衛嗣君弟） | [《史記・衛康叔世家》][23] | [JSON](5km_89r_9jr.json) |
| `A` | 衛君角 | [《史記・衛康叔世家》][23] | [JSON](5km_89r_9jr_A.json) |

</details>

<details><summary><code>5pw_05i_uhv</code> 平（本文燕昭王）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 平（本文燕昭王） | [《史記・樂毅列傳》][66] | [JSON](5pw_05i_uhv.json) |
| `A` | 惠王（燕昭王子） | [《史記・樂毅列傳》][66] | [JSON](5pw_05i_uhv_A.json) |

</details>

<details><summary><code>5xt_rg8_7zs</code> 項燕（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 項燕 | [《史記・秦始皇本紀》][10]、[《史記・六國年表》][120] | [JSON](5xt_rg8_7zs.json) |
| `A` | 項梁 | [《史記・項羽本紀》][11] | [JSON](5xt_rg8_7zs_A.json) |

</details>

<details><summary><code>69x_se2_859</code> 邴吉（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 邴吉 | [《史記・張丞相列傳》][82] | [JSON](69x_se2_859.json) |
| `A` | 邴顯 | [《史記・張丞相列傳》][82] | [JSON](69x_se2_859_A.json) |

</details>

<details><summary><code>6bn_yfc_lzi</code> 田叔（梁孝王世家候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 田叔 | [《史記・田叔列傳》][90] | [JSON](6bn_yfc_lzi.json) |
| `A` | 田仁 | [《史記・田叔列傳》][90] | [JSON](6bn_yfc_lzi_A.json) |

</details>

<details><summary><code>6d6_eg1_o3a</code> 王仲（外戚世家候選）（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 王仲 | [《史記・外戚世家》][35] | [JSON](6d6_eg1_o3a.json) |
| `A` | 王太后 | [《史記・外戚世家》][35] | [JSON](6d6_eg1_o3a_A.json) |
| `B` | 信 | [《史記・外戚世家》][35] | [JSON](6d6_eg1_o3a_B.json) |

</details>

<details><summary><code>6di_ywz_ju4</code> 莊伯（晉曲沃弒君記事）（13 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 莊伯（晉曲沃弒君記事） | [《史記・晉世家》][25] | [JSON](6di_ywz_ju4.json) |
| `A` | 稱（曲沃／晉武公） | [《史記・晉世家》][25] | [JSON](6di_ywz_ju4_A.json) |
| `AA` | 晉獻公 | [《史記・晉世家》][25] | [JSON](6di_ywz_ju4_AA.json) |
| `AAA` | 晉文公 | [《史記・晉世家》][25] | [JSON](6di_ywz_ju4_AAA.json) |
| `AAAA` | 伯鯈（重耳子） | [《史記・晉世家》][25] | [JSON](6di_ywz_ju4_AAAA.json) |
| `AAAB` | 叔劉（重耳子） | [《史記・晉世家》][25] | [JSON](6di_ywz_ju4_AAAB.json) |
| `AAAC` | 黑臀（晉成公） | [《史記・晉世家》][25] | [JSON](6di_ywz_ju4_AAAC.json) |
| `AAAD` | 晉襄公 | [《史記・晉世家》][25] | [JSON](6di_ywz_ju4_AAAD.json) |
| `AAADA` | 捷（晉襄公少子桓叔） | [《史記・晉世家》][25] | [JSON](6di_ywz_ju4_AAADA.json) |
| `AAADAA` | 談（惠伯） | [《史記・晉世家》][25] | [JSON](6di_ywz_ju4_AAADAA.json) |
| `AAADAAA` | 晉悼公 | [《史記・晉世家》][25] | [JSON](6di_ywz_ju4_AAADAAA.json) |
| `AAB` | 申生 | [《史記・晉世家》][25] | [JSON](6di_ywz_ju4_AAB.json) |
| `AAC` | 奚齊 | [《史記・晉世家》][25] | [JSON](6di_ywz_ju4_AAC.json) |

</details>

<details><summary><code>6ks_x4x_dbf</code> 臧荼（外戚世家候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 臧荼 | [《史記・外戚世家》][35] | [JSON](6ks_x4x_dbf.json) |
| `*A` | 臧兒 | [《史記・外戚世家》][35] | [JSON](6ks_x4x_dbf_%2AA.json) |

</details>

<details><summary><code>6oy_t19_ywe</code> 秦惠王（蘇秦列傳候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 秦惠王 | [《史記・蘇秦列傳》][55] | [JSON](6oy_t19_ywe.json) |
| `A` | 秦惠王女 | [《史記・蘇秦列傳》][55] | [JSON](6oy_t19_ywe_A.json) |

</details>

<details><summary><code>6r8_jki_snj</code> 趙兼（酷吏列傳候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 趙兼 | [《史記・酷吏列傳》][108] | [JSON](6r8_jki_snj.json) |
| `A` | 周陽由 | [《史記・酷吏列傳》][108] | [JSON](6r8_jki_snj_A.json) |

</details>

<details><summary><code>6wx_fr3_b2e</code> 滿（陳胡公）（8 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 滿（陳胡公） | [《史記・陳杞世家》][22] | [JSON](6wx_fr3_b2e.json) |
| `A` | 犀侯（陳申公） | [《史記・陳杞世家》][22] | [JSON](6wx_fr3_b2e_A.json) |
| `AA` | 突（陳孝公） | [《史記・陳杞世家》][22] | [JSON](6wx_fr3_b2e_AA.json) |
| `AAA` | 圉戎（陳慎公） | [《史記・陳杞世家》][22] | [JSON](6wx_fr3_b2e_AAA.json) |
| `AAAA` | 寧（陳幽公） | [《史記・陳杞世家》][22] | [JSON](6wx_fr3_b2e_AAAA.json) |
| `AAAAA` | 孝（陳釐公） | [《史記・陳杞世家》][22] | [JSON](6wx_fr3_b2e_AAAAA.json) |
| `AAAAAA` | 靈（陳武公） | [《史記・陳杞世家》][22] | [JSON](6wx_fr3_b2e_AAAAAA.json) |
| `AAAAAAA` | 說（陳夷公） | [《史記・陳杞世家》][22] | [JSON](6wx_fr3_b2e_AAAAAAA.json) |

</details>

<details><summary><code>766_5dq_zws</code> 朱家（季布欒布列傳候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 朱家 | [《史記・季布欒布列傳》][86] | [JSON](766_5dq_zws.json) |
| `A` | 朱家子未名 | [《史記・季布欒布列傳》][86] | [JSON](766_5dq_zws_A.json) |

</details>

<details><summary><code>78u_8ii_bnr</code> 專諸（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 專諸 | [《史記・刺客列傳》][72] | [JSON](78u_8ii_bnr.json) |
| `A` | 專諸子（本卷未名） | [《史記・吳太伯世家》][17]、[《史記・刺客列傳》][72] | [JSON](78u_8ii_bnr_A.json) |

</details>

<details><summary><code>796_nkw_0jz</code> 張蒼父未名（張丞相列傳候選）（4 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 張蒼父未名 | [《史記・張丞相列傳》][82] | [JSON](796_nkw_0jz.json) |
| `A` | 張蒼 | [《史記・張丞相列傳》][82] | [JSON](796_nkw_0jz_A.json) |
| `AA` | 張蒼子未名（康侯） | [《史記・張丞相列傳》][82] | [JSON](796_nkw_0jz_AA.json) |
| `AAA` | 張類 | [《史記・張丞相列傳》][82] | [JSON](796_nkw_0jz_AAA.json) |

</details>

<details><summary><code>7du_pfa_2s5</code> 蹇叔（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 蹇叔 | [《史記・秦本紀》][9] | [JSON](7du_pfa_2s5.json) |
| `A` | 西乞術 | [《史記・秦本紀》][9]、[《史記・晉世家》][25] | [JSON](7du_pfa_2s5_A.json) |
| `B` | 白乙丙 | [《史記・秦本紀》][9]、[《史記・晉世家》][25] | [JSON](7du_pfa_2s5_B.json) |

</details>

<details><summary><code>7dv_lqp_y4z</code> 靳歙（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 靳歙 | [《漢書・樊酈滕灌傅靳周傳》][3] | [JSON](7dv_lqp_y4z.json) |
| `A` | 靳亭 | [《史記・高祖功臣侯者年表》][123] | [JSON](7dv_lqp_y4z_A.json) |

</details>

<details><summary><code>7mz_d13_9ka</code> 田氏（外戚世家候選）（4 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 田氏 | [《史記・外戚世家》][35] | [JSON](7mz_d13_9ka.json) |
| `A` | 田蚡 | [《史記・魏其武安侯列傳》][93] | [JSON](7mz_d13_9ka_A.json) |
| `AA` | 恬（田蚡子） | [《史記・魏其武安侯列傳》][93] | [JSON](7mz_d13_9ka_AA.json) |
| `B` | 勝 | [《史記・外戚世家》][35]、[《史記・魏其武安侯列傳》][93] | [JSON](7mz_d13_9ka_B.json) |

</details>

<details><summary><code>7s2_h0m_msl</code> 蘇（曹戴伯）（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 蘇（曹戴伯） | [《史記・管蔡世家》][21] | [JSON](7s2_h0m_msl.json) |
| `A` | 兕（曹惠伯） | [《史記・管蔡世家》][21] | [JSON](7s2_h0m_msl_A.json) |
| `AA` | 石甫（曹惠伯子） | [《史記・管蔡世家》][21] | [JSON](7s2_h0m_msl_AA.json) |

</details>

<details><summary><code>7tm_3ss_4on</code> 周苛（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 周苛 | [《史記・張丞相列傳》][82] | [JSON](7tm_3ss_4on.json) |
| `*A` | 平（周苛孫） | [《史記・孝景本紀》][15] | [JSON](7tm_3ss_4on_%2AA.json) |
| `A` | 周成 | [《史記・張丞相列傳》][82] | [JSON](7tm_3ss_4on_A.json) |

</details>

<details><summary><code>7uk_oqn_ymk</code> 陳宣公杵臼（田世家候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 陳宣公杵臼 | [《史記・田敬仲完世家》][32] | [JSON](7uk_oqn_ymk.json) |
| `A` | 御寇 | [《史記・田敬仲完世家》][32] | [JSON](7uk_oqn_ymk_A.json) |

</details>

<details><summary><code>8im_m5e_cpy</code> 甘茂（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 甘茂 | [《史記・樗里子甘茂列傳》][57] | [JSON](8im_m5e_cpy.json) |
| `*A` | 甘羅 | [《史記・樗里子甘茂列傳》][57] | [JSON](8im_m5e_cpy_%2AA.json) |

</details>

<details><summary><code>8rw_c97_jpz</code> 梁伯（晉惠公外家）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 梁伯（晉惠公外家） | [《史記・晉世家》][25] | [JSON](8rw_c97_jpz.json) |
| `A` | 梁伯女（圉母） | [《史記・晉世家》][25] | [JSON](8rw_c97_jpz_A.json) |

</details>

<details><summary><code>8xz_mlj_r3c</code> 韓千秋（南越列傳候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 韓千秋 | [《史記・南越列傳》][99] | [JSON](8xz_mlj_r3c.json) |
| `A` | 延年 | [《史記・建元以來侯者年表》][125] | [JSON](8xz_mlj_r3c_A.json) |

</details>

<details><summary><code>98i_dd4_aof</code> 多同（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 多同 | [《史記・西南夷列傳》][102] | [JSON](98i_dd4_aof.json) |
| `A` | 多同子 | [《史記・西南夷列傳》][102] | [JSON](98i_dd4_aof_A.json) |

</details>

<details><summary><code>995_xas_r98</code> 申（蔡昭侯）（6 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 申（蔡昭侯） | [《史記・管蔡世家》][21] | [JSON](995_xas_r98.json) |
| `A` | 朔（蔡成侯） | [《史記・管蔡世家》][21] | [JSON](995_xas_r98_A.json) |
| `AA` | 產（蔡聲侯） | [《史記・管蔡世家》][21]、[《史記・六國年表》][120] | [JSON](995_xas_r98_AA.json) |
| `AAA` | 元侯（蔡君） | [《史記・管蔡世家》][21] | [JSON](995_xas_r98_AAA.json) |
| `AAAA` | 齊（蔡末侯） | [《史記・管蔡世家》][21] | [JSON](995_xas_r98_AAAA.json) |
| `B` | 蔡昭侯質吳子（未名） | [《史記・管蔡世家》][21] | [JSON](995_xas_r98_B.json) |

</details>

<details><summary><code>9nr_qwg_vuf</code> 叔孫宣伯（魯）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 叔孫宣伯（魯） | [《史記・齊太公世家》][18] | [JSON](9nr_qwg_vuf.json) |
| `A` | 景公母（叔孫宣伯女） | [《史記・齊太公世家》][18] | [JSON](9nr_qwg_vuf_A.json) |

</details>

<details><summary><code>9oa_4bh_lmd</code> 鄭伯（楚莊王圍鄭時）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 鄭伯（楚莊王圍鄭時） | [《史記・鄭世家》][28] | [JSON](9oa_4bh_lmd.json) |
| `A` | 沸 | [《史記・鄭世家》][28] | [JSON](9oa_4bh_lmd_A.json) |

</details>

<details><summary><code>9w2_c77_53m</code> 齊桓公（12 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 齊桓公 | [《史記・齊太公世家》][18] | [JSON](9w2_c77_53m.json) |
| `A` | 元（齊惠公） | [《史記・齊太公世家》][18] | [JSON](9w2_c77_53m_A.json) |
| `AA` | 無野（齊頃公） | [《史記・齊太公世家》][18] | [JSON](9w2_c77_53m_AA.json) |
| `AAA` | 環（齊靈公） | [《史記・齊太公世家》][18] | [JSON](9w2_c77_53m_AAA.json) |
| `AAAA` | 齊莊公（崔杼時） | [《史記・齊太公世家》][18] | [JSON](9w2_c77_53m_AAAA.json) |
| `B` | 無詭（齊桓公子） | [《史記・齊太公世家》][18] | [JSON](9w2_c77_53m_B.json) |
| `C` | 昭（齊孝公） | [《史記・齊太公世家》][18] | [JSON](9w2_c77_53m_C.json) |
| `D` | 潘（齊昭公） | [《史記・齊太公世家》][18] | [JSON](9w2_c77_53m_D.json) |
| `DA` | 舍（齊昭公子） | [《史記・齊太公世家》][18] | [JSON](9w2_c77_53m_DA.json) |
| `E` | 商人（齊懿公） | [《史記・齊太公世家》][18] | [JSON](9w2_c77_53m_E.json) |
| `F` | 雍（齊桓公子） | [《史記・齊太公世家》][18]、[《史記・楚世家》][26] | [JSON](9w2_c77_53m_F.json) |
| `G` | 齊姜（申生母） | [《史記・晉世家》][25] | [JSON](9w2_c77_53m_G.json) |

</details>

<details><summary><code>9yf_c3t_x2w</code> 衛君父引古未名（李斯列傳候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 衛君父引古未名 | [《史記・李斯列傳》][73] | [JSON](9yf_c3t_x2w.json) |
| `A` | 衛君引古未名 | [《史記・李斯列傳》][73] | [JSON](9yf_c3t_x2w_A.json) |

</details>

<details><summary><code>9zj_vf7_86a</code> 薄氏父（外戚世家候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 薄氏父 | [《史記・外戚世家》][35] | [JSON](9zj_vf7_86a.json) |
| `A` | 薄太后（孝文帝母） | [《史記・外戚世家》][35] | [JSON](9zj_vf7_86a_A.json) |

</details>

<details><summary><code>a13_5fp_pek</code> 梁襄王（趙世家候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 梁襄王 | [《史記・趙世家》][29] | [JSON](a13_5fp_pek.json) |
| `A` | 嗣 | [《史記・趙世家》][29] | [JSON](a13_5fp_pek_A.json) |

</details>

<details><summary><code>a7k_sl0_d7u</code> 金王孫（外戚世家候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 金王孫 | [《史記・外戚世家》][35] | [JSON](a7k_sl0_d7u.json) |
| `A` | 修成君 | [《史記・外戚世家》][35] | [JSON](a7k_sl0_d7u_A.json) |

</details>

<details><summary><code>a9m_987_rss</code> 叔牙（莊公弟）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 叔牙（莊公弟） | [《史記・魯周公世家》][19] | [JSON](a9m_987_rss.json) |
| `A` | 叔牙子（未名） | [《史記・魯周公世家》][19] | [JSON](a9m_987_rss_A.json) |

</details>

<details><summary><code>a9v_t0d_3va</code> 晉惠公（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 晉惠公 | [《史記・晉世家》][25] | [JSON](a9v_t0d_3va.json) |
| `A` | 晉懷公 | [《史記・晉世家》][25] | [JSON](a9v_t0d_3va_A.json) |
| `B` | 妾（梁伯女所生女） | [《史記・晉世家》][25] | [JSON](a9v_t0d_3va_B.json) |

</details>

<details><summary><code>acg_se3_w5x</code> 周呂侯（呂后兄）（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 周呂侯（呂后兄） | [《史記・呂太后本紀》][13] | [JSON](acg_se3_w5x.json) |
| `A` | 呂台 | [《史記・呂太后本紀》][13] | [JSON](acg_se3_w5x_A.json) |
| `B` | 呂產 | [《史記・呂太后本紀》][13] | [JSON](acg_se3_w5x_B.json) |

</details>

<details><summary><code>afj_vl8_7fu</code> 安丘侯説（萬石張叔列傳候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 安丘侯説 | [《史記・萬石張叔列傳》][89] | [JSON](afj_vl8_7fu.json) |
| `A` | 張歐 | [《史記・萬石張叔列傳》][89] | [JSON](afj_vl8_7fu_A.json) |

</details>

<details><summary><code>agx_sqm_4ou</code> 張耳（5 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 張耳 | [《史記・張耳陳餘列傳》][75] | [JSON](agx_sqm_4ou.json) |
| `A` | 張敖 | [《史記・張耳陳餘列傳》][75] | [JSON](agx_sqm_4ou_A.json) |
| `AA` | 張偃 | [《史記・呂太后本紀》][13]、[《史記・張耳陳餘列傳》][75] | [JSON](agx_sqm_4ou_AA.json) |
| `AB` | 張壽 | [《史記・張耳陳餘列傳》][75] | [JSON](agx_sqm_4ou_AB.json) |
| `AC` | 張侈 | [《史記・張耳陳餘列傳》][75] | [JSON](agx_sqm_4ou_AC.json) |

</details>

<details><summary><code>ao3_0fy_d45</code> 秦昭王（6 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 秦昭王 | [《史記・范睢蔡澤列傳》][65] | [JSON](ao3_0fy_d45.json) |
| `A` | 秦孝文王 | [《史記・呂不韋列傳》][71] | [JSON](ao3_0fy_d45_A.json) |
| `AA` | 秦莊襄王 | [《史記・呂不韋列傳》][71] | [JSON](ao3_0fy_d45_AA.json) |
| `AAA` | 秦始皇帝 | [《史記・秦始皇本紀》][10] | [JSON](ao3_0fy_d45_AAA.json) |
| `AAAA` | 胡亥 | [《史記・秦始皇本紀》][10] | [JSON](ao3_0fy_d45_AAAA.json) |
| `AAAB` | 扶蘇 | [《史記・李斯列傳》][73] | [JSON](ao3_0fy_d45_AAAB.json) |

</details>

<details><summary><code>ath_xsq_n4i</code> 魯定公（11 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 魯定公 | [《史記・魯周公世家》][19] | [JSON](ath_xsq_n4i.json) |
| `A` | 魯哀公 | [《史記・魯周公世家》][19] | [JSON](ath_xsq_n4i_A.json) |
| `AA` | 寧（魯悼公） | [《史記・魯周公世家》][19] | [JSON](ath_xsq_n4i_AA.json) |
| `AAA` | 嘉（魯元公） | [《史記・魯周公世家》][19] | [JSON](ath_xsq_n4i_AAA.json) |
| `AAAA` | 顯（魯穆公） | [《史記・魯周公世家》][19] | [JSON](ath_xsq_n4i_AAAA.json) |
| `AAAAA` | 奮（魯共公） | [《史記・魯周公世家》][19] | [JSON](ath_xsq_n4i_AAAAA.json) |
| `AAAAAA` | 屯（魯康公） | [《史記・魯周公世家》][19] | [JSON](ath_xsq_n4i_AAAAAA.json) |
| `AAAAAAA` | 匽（魯景公） | [《史記・魯周公世家》][19] | [JSON](ath_xsq_n4i_AAAAAAA.json) |
| `AAAAAAAA` | 叔（魯平公） | [《史記・魯周公世家》][19] | [JSON](ath_xsq_n4i_AAAAAAAA.json) |
| `AAAAAAAAA` | 賈（魯文公） | [《史記・魯周公世家》][19] | [JSON](ath_xsq_n4i_AAAAAAAAA.json) |
| `AAAAAAAAAA` | 讎（魯頃公） | [《史記・魯周公世家》][19] | [JSON](ath_xsq_n4i_AAAAAAAAAA.json) |

</details>

<details><summary><code>b1r_inb_fts</code> 樊噲（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 樊噲 | [《史記・樊酈滕灌列傳》][81] | [JSON](b1r_inb_fts.json) |
| `A` | 樊市人 | [《史記・樊酈滕灌列傳》][81] | [JSON](b1r_inb_fts_A.json) |
| `B` | 樊伉 | [《史記・樊酈滕灌列傳》][81] | [JSON](b1r_inb_fts_B.json) |

</details>

<details><summary><code>bm8_bzq_1ee</code> 觀起（蔡大夫）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 觀起（蔡大夫） | [《史記・楚世家》][26] | [JSON](bm8_bzq_1ee.json) |
| `A` | 觀從（楚變亂謀者） | [《史記・楚世家》][26] | [JSON](bm8_bzq_1ee_A.json) |

</details>

<details><summary><code>bn4_lhp_9h1</code> 姑容（杞桓公）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 姑容（杞桓公） | [《史記・陳杞世家》][22] | [JSON](bn4_lhp_9h1.json) |
| `A` | 丐（杞孝公） | [《史記・陳杞世家》][22] | [JSON](bn4_lhp_9h1_A.json) |

</details>

<details><summary><code>buv_igi_gpn</code> 帝乙（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 帝乙 | [《史記・殷本紀》][7] | [JSON](buv_igi_gpn.json) |
| `A` | 微子啓 | [《史記・宋微子世家》][24] | [JSON](buv_igi_gpn_A.json) |

</details>

<details><summary><code>bvb_d1z_fd0</code> 尉佗（6 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 尉佗 | [《史記・南越列傳》][99] | [JSON](bvb_d1z_fd0.json) |
| `*A` | 胡 | [《史記・南越列傳》][99] | [JSON](bvb_d1z_fd0_%2AA.json) |
| `*AA` | 嬰齊 | [《史記・南越列傳》][99] | [JSON](bvb_d1z_fd0_%2AAA.json) |
| `*AAA` | 興 | [《史記・南越列傳》][99] | [JSON](bvb_d1z_fd0_%2AAAA.json) |
| `*AAB` | 次公 | [《史記・南越列傳》][99] | [JSON](bvb_d1z_fd0_%2AAAB.json) |
| `*AAC` | 建德 | [《史記・南越列傳》][99] | [JSON](bvb_d1z_fd0_%2AAAC.json) |

</details>

<details><summary><code>bwv_ob8_6xi</code> 共敖（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 共敖 | [《史記・項羽本紀》][11]、[《史記・秦楚之際月表》][121] | [JSON](bwv_ob8_6xi.json) |
| `A` | 共尉 | [《史記・荊燕世家》][37]、[《史記・秦楚之際月表》][121] | [JSON](bwv_ob8_6xi_A.json) |

</details>

<details><summary><code>c0i_eah_y59</code> 咎（韓世家釐王候選）（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 咎 | [《史記・韓世家》][31] | [JSON](c0i_eah_y59.json) |
| `A` | 桓惠王 | [《史記・韓世家》][31] | [JSON](c0i_eah_y59_A.json) |
| `AA` | 韓王安 | [《史記・韓世家》][31]、[《史記・六國年表》][120] | [JSON](c0i_eah_y59_AA.json) |

</details>

<details><summary><code>c19_xxo_r8f</code> 直不疑（萬石張叔列傳候選）（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 直不疑 | [《史記・萬石張叔列傳》][89] | [JSON](c19_xxo_r8f.json) |
| `*A` | 望（直不疑孫） | [《史記・萬石張叔列傳》][89] | [JSON](c19_xxo_r8f_%2AA.json) |
| `A` | 相如（直不疑子） | [《史記・萬石張叔列傳》][89] | [JSON](c19_xxo_r8f_A.json) |

</details>

<details><summary><code>c1t_5mz_5ia</code> 晉昭公（趙世家候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 晉昭公 | [《史記・趙世家》][29] | [JSON](c1t_5mz_5ia.json) |
| `**A` | 驕 | [《史記・趙世家》][29] | [JSON](c1t_5mz_5ia_%2A%2AA.json) |

</details>

<details><summary><code>c2w_s7g_en0</code> 楚懷王（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 楚懷王 | [《史記・楚世家》][26] | [JSON](c2w_s7g_en0.json) |
| `*A` | 楚懷王心 | [《史記・高祖本紀》][12] | [JSON](c2w_s7g_en0_%2AA.json) |
| `A` | 子蘭（楚懷王子） | [《史記・屈原賈生列傳》][70] | [JSON](c2w_s7g_en0_A.json) |

</details>

<details><summary><code>cek_1yy_pne</code> 奄父（趙世家候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 奄父 | [《史記・趙世家》][29] | [JSON](cek_1yy_pne.json) |
| `A` | 叔帶 | [《史記・趙世家》][29] | [JSON](cek_1yy_pne_A.json) |

</details>

<details><summary><code>cjd_ybv_2wu</code> 蜚廉（趙世家祖系候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 蜚廉 | [《史記・趙世家》][29] | [JSON](cjd_ybv_2wu.json) |
| `A` | 惡來 | [《史記・趙世家》][29] | [JSON](cjd_ybv_2wu_A.json) |

</details>

<details><summary><code>dm0_58v_50i</code> 趙衰（5 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 趙衰 | [《史記・晉世家》][25] | [JSON](dm0_58v_50i.json) |
| `A` | 趙盾 | [《史記・晉世家》][25] | [JSON](dm0_58v_50i_A.json) |
| `B` | 趙同 | [《史記・趙世家》][29] | [JSON](dm0_58v_50i_B.json) |
| `C` | 趙括 | [《史記・趙世家》][29] | [JSON](dm0_58v_50i_C.json) |
| `D` | 趙嬰齊 | [《史記・趙世家》][29] | [JSON](dm0_58v_50i_D.json) |

</details>

<details><summary><code>dq6_ovk_58c</code> 張釋之（張釋之馮唐列傳候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 張釋之 | [《史記・張釋之馮唐列傳》][88] | [JSON](dq6_ovk_58c.json) |
| `A` | 張摯 | [《史記・張釋之馮唐列傳》][88] | [JSON](dq6_ovk_58c_A.json) |

</details>

<details><summary><code>e00_pe1_zri</code> 無諸（東越列傳候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 無諸 | [《史記・東越列傳》][100] | [JSON](e00_pe1_zri.json) |
| `*A` | 丑 | [《史記・東越列傳》][100] | [JSON](e00_pe1_zri_%2AA.json) |

</details>

<details><summary><code>ea5_zvr_hlp</code> 張良（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 張良 | [《史記・留侯世家》][41] | [JSON](ea5_zvr_hlp.json) |
| `A` | 張辟彊 | [《史記・呂太后本紀》][13] | [JSON](ea5_zvr_hlp_A.json) |
| `B` | 不疑 | [《史記・留侯世家》][41] | [JSON](ea5_zvr_hlp_B.json) |

</details>

<details><summary><code>ei2_qej_czn</code> 公乘氏（張耳陳餘列傳候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 公乘氏 | [《史記・張耳陳餘列傳》][75] | [JSON](ei2_qej_czn.json) |
| `A` | 陳餘妻未名 | [《史記・張耳陳餘列傳》][75] | [JSON](ei2_qej_czn_A.json) |

</details>

<details><summary><code>ei7_fai_lvy</code> 丑（鄭世家共公候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 丑 | [《史記・鄭世家》][28] | [JSON](ei7_fai_lvy.json) |
| `A` | 已 | [《史記・鄭世家》][28] | [JSON](ei7_fai_lvy_A.json) |

</details>

<details><summary><code>esh_e0a_jrw</code> 石奮父未名（萬石張叔列傳候選）（7 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 石奮父未名 | [《史記・萬石張叔列傳》][89] | [JSON](esh_e0a_jrw.json) |
| `A` | 石奮 | [《史記・萬石張叔列傳》][89] | [JSON](esh_e0a_jrw_A.json) |
| `AA` | 建（石奮長子） | [《史記・萬石張叔列傳》][89] | [JSON](esh_e0a_jrw_AA.json) |
| `AB` | 甲（石奮次子失名佔位） | [《史記・萬石張叔列傳》][89] | [JSON](esh_e0a_jrw_AB.json) |
| `AC` | 乙（石奮次子失名佔位） | [《史記・萬石張叔列傳》][89] | [JSON](esh_e0a_jrw_AC.json) |
| `AD` | 慶（石奮子） | [《史記・萬石張叔列傳》][89] | [JSON](esh_e0a_jrw_AD.json) |
| `ADA` | 德（石慶中子） | [《史記・萬石張叔列傳》][89] | [JSON](esh_e0a_jrw_ADA.json) |

</details>

<details><summary><code>eva_gs1_9n5</code> 魏文侯（趙世家候選）（7 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 魏文侯 | [《史記・趙世家》][29] | [JSON](eva_gs1_9n5.json) |
| `A` | 撃 | [《史記・魏世家》][30] | [JSON](eva_gs1_9n5_A.json) |
| `AA` | 罃 | [《史記・魏世家》][30] | [JSON](eva_gs1_9n5_AA.json) |
| `AAA` | 襄王 | [《史記・魏世家》][30] | [JSON](eva_gs1_9n5_AAA.json) |
| `AAAA` | 哀王 | [《史記・魏世家》][30] | [JSON](eva_gs1_9n5_AAAA.json) |
| `AAAAA` | 昭王 | [《史記・魏世家》][30] | [JSON](eva_gs1_9n5_AAAAA.json) |
| `AAAAAA` | 安釐王 | [《史記・魏公子列傳》][63] | [JSON](eva_gs1_9n5_AAAAAA.json) |

</details>

<details><summary><code>eya_qj3_tev</code> 酈食其（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 酈食其 | [《史記・酈生陸賈列傳》][83] | [JSON](eya_qj3_tev.json) |
| `A` | 疥（酈食其子） | [《史記・酈生陸賈列傳》][83] | [JSON](eya_qj3_tev_A.json) |

</details>

<details><summary><code>f04_rc9_xqn</code> 太史敫（田世家候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 太史敫 | [《史記・田敬仲完世家》][32] | [JSON](f04_rc9_xqn.json) |
| `A` | 君王后 | [《史記・田敬仲完世家》][32] | [JSON](f04_rc9_xqn_A.json) |

</details>

<details><summary><code>f41_ulg_3u1</code> 衛滿（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 衛滿 | [《史記・朝鮮列傳》][101] | [JSON](f41_ulg_3u1.json) |
| `*A` | 右渠 | [《史記・朝鮮列傳》][101] | [JSON](f41_ulg_3u1_%2AA.json) |
| `*AA` | 長（右渠子） | [《史記・朝鮮列傳》][101] | [JSON](f41_ulg_3u1_%2AAA.json) |

</details>

<details><summary><code>f8d_j5p_nop</code> 孔防叔（孔子世家候選）（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 孔防叔 | [《史記・孔子世家》][33] | [JSON](f8d_j5p_nop.json) |
| `A` | 伯夏 | [《史記・孔子世家》][33] | [JSON](f8d_j5p_nop_A.json) |
| `AA` | 叔梁紇 | [《史記・孔子世家》][33] | [JSON](f8d_j5p_nop_AA.json) |

</details>

<details><summary><code>faf_5al_ikw</code> 鄭武公（老韓列傳候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 鄭武公 | [《史記・老子韓非列傳》][49] | [JSON](faf_5al_ikw.json) |
| `A` | 鄭武公之子 | [《史記・老子韓非列傳》][49] | [JSON](faf_5al_ikw_A.json) |

</details>

<details><summary><code>fd3_tly_1lo</code> 沸（魯魏公）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 沸（魯魏公） | [《史記・魯周公世家》][19] | [JSON](fd3_tly_1lo.json) |
| `A` | 擢（魯厲公） | [《史記・魯周公世家》][19]、[《史記・三代世表》][118] | [JSON](fd3_tly_1lo_A.json) |

</details>

<details><summary><code>fdb_6pb_gux</code> 蒯聵（太史公自序候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 蒯聵 | [《史記・太史公自序》][116] | [JSON](fdb_6pb_gux.json) |
| `***A` | 司馬卬 | [《史記・太史公自序》][116] | [JSON](fdb_6pb_gux_%2A%2A%2AA.json) |

</details>

<details><summary><code>fmh_dmt_cql</code> 汲黯（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 汲黯 | [《史記・汲鄭列傳》][106] | [JSON](fmh_dmt_cql.json) |
| `A` | 汲偃 | [《史記・汲鄭列傳》][106] | [JSON](fmh_dmt_cql_A.json) |

</details>

<details><summary><code>fom_gr9_c8v</code> 孫叔敖（循吏列傳候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 孫叔敖 | [《史記・循吏列傳》][105]、[《史記・滑稽列傳》][112] | [JSON](fom_gr9_c8v.json) |
| `A` | 孫叔敖子（未名） | [《史記・滑稽列傳》][112] | [JSON](fom_gr9_c8v_A.json) |

</details>

<details><summary><code>fp6_ia6_7yw</code> 孔子（11 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 孔子 | [《史記・孔子世家》][33] | [JSON](fp6_ia6_7yw.json) |
| `A` | 鯉 | [《史記・孔子世家》][33] | [JSON](fp6_ia6_7yw_A.json) |
| `AA` | 伋 | [《史記・孔子世家》][33] | [JSON](fp6_ia6_7yw_AA.json) |
| `AAA` | 白 | [《史記・孔子世家》][33] | [JSON](fp6_ia6_7yw_AAA.json) |
| `AAAA` | 求 | [《史記・孔子世家》][33] | [JSON](fp6_ia6_7yw_AAAA.json) |
| `AAAAA` | 箕 | [《史記・孔子世家》][33] | [JSON](fp6_ia6_7yw_AAAAA.json) |
| `AAAAAA` | 穿 | [《史記・孔子世家》][33] | [JSON](fp6_ia6_7yw_AAAAAA.json) |
| `AAAAAAA` | 子慎 | [《史記・孔子世家》][33] | [JSON](fp6_ia6_7yw_AAAAAAA.json) |
| `AAAAAAAA` | 鮒 | [《史記・孔子世家》][33] | [JSON](fp6_ia6_7yw_AAAAAAAA.json) |
| `B` | 孔鯉 | [《史記・仲尼弟子列傳》][53] | [JSON](fp6_ia6_7yw_B.json) |
| `C` | 孔子之女 | [《史記・仲尼弟子列傳》][53] | [JSON](fp6_ia6_7yw_C.json) |

</details>

<details><summary><code>fvm_66f_0k3</code> 周緤（4 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 周緤 | [《史記・傅靳蒯成列傳》][84] | [JSON](fvm_66f_0k3.json) |
| `A` | 周昌（蒯成侯之子） | [《漢書・樊酈滕灌傅靳周傳》][3]、[《史記・傅靳蒯成列傳》][84]、[《史記・高祖功臣侯者年表》][123] | [JSON](fvm_66f_0k3_A.json) |
| `C` | 周應 | [《漢書・樊酈滕灌傅靳周傳》][3] | [JSON](fvm_66f_0k3_C.json) |
| `CA` | 周仲居 | [《史記・高祖功臣侯者年表》][123] | [JSON](fvm_66f_0k3_CA.json) |

</details>

<details><summary><code>g9h_5ih_ug1</code> 伍奢（伍胥列傳候選）（4 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 伍奢 | [《史記・伍子胥列傳》][52] | [JSON](g9h_5ih_ug1.json) |
| `A` | 伍子胥 | [《史記・伍子胥列傳》][52] | [JSON](g9h_5ih_ug1_A.json) |
| `AA` | 伍子胥之子 | [《史記・伍子胥列傳》][52] | [JSON](g9h_5ih_ug1_AA.json) |
| `B` | 伍尚 | [《史記・伍子胥列傳》][52] | [JSON](g9h_5ih_ug1_B.json) |

</details>

<details><summary><code>ga6_jt5_6g1</code> 圉（衛孔文子）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 圉（衛孔文子） | [《史記・衛康叔世家》][23] | [JSON](ga6_jt5_6g1.json) |
| `A` | 悝（衛孔氏） | [《史記・衛康叔世家》][23] | [JSON](ga6_jt5_6g1_A.json) |

</details>

<details><summary><code>gcb_rf3_coi</code> 費王（晉穆侯）（4 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 費王（晉穆侯） | [《史記・晉世家》][25] | [JSON](gcb_rf3_coi.json) |
| `A` | 仇（晉文侯） | [《史記・晉世家》][25] | [JSON](gcb_rf3_coi_A.json) |
| `AA` | 伯（晉昭侯） | [《史記・晉世家》][25] | [JSON](gcb_rf3_coi_AA.json) |
| `B` | 成師（曲沃桓叔） | [《史記・晉世家》][25] | [JSON](gcb_rf3_coi_B.json) |

</details>

<details><summary><code>gdj_k53_v1x</code> 王翦（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 王翦 | [《史記・白起王翦列傳》][59] | [JSON](gdj_k53_v1x.json) |
| `*A` | 王離 | [《史記・白起王翦列傳》][59] | [JSON](gdj_k53_v1x_%2AA.json) |
| `A` | 王賁 | [《史記・白起王翦列傳》][59] | [JSON](gdj_k53_v1x_A.json) |

</details>

<details><summary><code>ghg_5p7_q21</code> 遂（杞釐公）（4 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 遂（杞釐公） | [《史記・陳杞世家》][22] | [JSON](ghg_5p7_q21.json) |
| `A` | 維（杞湣公） | [《史記・陳杞世家》][22] | [JSON](ghg_5p7_q21_A.json) |
| `AA` | 敕（杞出公） | [《史記・陳杞世家》][22] | [JSON](ghg_5p7_q21_AA.json) |
| `AAA` | 春（杞簡公） | [《史記・陳杞世家》][22] | [JSON](ghg_5p7_q21_AAA.json) |

</details>

<details><summary><code>gn7_br7_32m</code> 伯州犁（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 伯州犁 | [《史記・吳太伯世家》][17] | [JSON](gn7_br7_32m.json) |
| `*A` | 伯嚭 | [《史記・吳太伯世家》][17] | [JSON](gn7_br7_32m_%2AA.json) |

</details>

<details><summary><code>gqj_xdu_8rf</code> 張騫（李將軍列傳候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 張騫 | [《史記・大宛列傳》][109] | [JSON](gqj_xdu_8rf.json) |
| `A` | 張騫子（未名） | [《史記・大宛列傳》][109] | [JSON](gqj_xdu_8rf_A.json) |

</details>

<details><summary><code>gts_42q_flu</code> 睔（鄭世家成公候選）（8 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 睔 | [《史記・鄭世家》][28] | [JSON](gts_42q_flu.json) |
| `A` | 惲 | [《史記・鄭世家》][28] | [JSON](gts_42q_flu_A.json) |
| `AA` | 嘉 | [《史記・鄭世家》][28] | [JSON](gts_42q_flu_AA.json) |
| `AAA` | 寧 | [《史記・鄭世家》][28] | [JSON](gts_42q_flu_AAA.json) |
| `AAAA` | 蠆 | [《史記・鄭世家》][28] | [JSON](gts_42q_flu_AAAA.json) |
| `AAAAA` | 勝 | [《史記・鄭世家》][28] | [JSON](gts_42q_flu_AAAAA.json) |
| `AAAAAA` | 易 | [《史記・鄭世家》][28] | [JSON](gts_42q_flu_AAAAAA.json) |
| `B` | 子産 | [《史記・鄭世家》][28] | [JSON](gts_42q_flu_B.json) |

</details>

<details><summary><code>h1w_44g_vef</code> 張孟（魏其武安侯列傳候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 張孟 | [《史記・魏其武安侯列傳》][93] | [JSON](h1w_44g_vef.json) |
| `A` | 灌夫 | [《史記・魏其武安侯列傳》][93] | [JSON](h1w_44g_vef_A.json) |

</details>

<details><summary><code>h4f_d5f_vdl</code> 蟬封（大宛列傳候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 蟬封 | [《史記・大宛列傳》][109] | [JSON](h4f_d5f_vdl.json) |
| `A` | 蟬封子（入質，未名） | [《史記・大宛列傳》][109] | [JSON](h4f_d5f_vdl_A.json) |

</details>

<details><summary><code>i30_mjq_6q8</code> 呂公（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 呂公 | [《史記・高祖本紀》][12] | [JSON](i30_mjq_6q8.json) |
| `A` | 呂后 | [《史記・呂太后本紀》][13] | [JSON](i30_mjq_6q8_A.json) |

</details>

<details><summary><code>i3f_9l9_g53</code> 陳平（5 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 陳平 | [《史記・陳丞相世家》][42] | [JSON](i3f_9l9_g53.json) |
| `**A` | 陳掌 | [《史記・陳丞相世家》][42] | [JSON](i3f_9l9_g53_%2A%2AA.json) |
| `A` | 買 | [《史記・陳丞相世家》][42] | [JSON](i3f_9l9_g53_A.json) |
| `AA` | 恢 | [《史記・陳丞相世家》][42] | [JSON](i3f_9l9_g53_AA.json) |
| `AAA` | 何 | [《史記・陳丞相世家》][42] | [JSON](i3f_9l9_g53_AAA.json) |

</details>

<details><summary><code>i7a_22p_qda</code> 句踐（7 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 句踐 | [《史記・越王勾踐世家》][27] | [JSON](i7a_22p_qda.json) |
| `A` | 鼫與 | [《史記・越王勾踐世家》][27] | [JSON](i7a_22p_qda_A.json) |
| `AA` | 不壽 | [《史記・越王勾踐世家》][27] | [JSON](i7a_22p_qda_AA.json) |
| `AAA` | 翁 | [《史記・越王勾踐世家》][27] | [JSON](i7a_22p_qda_AAA.json) |
| `AAAA` | 翳 | [《史記・越王勾踐世家》][27] | [JSON](i7a_22p_qda_AAAA.json) |
| `AAAAA` | 之侯 | [《史記・越王勾踐世家》][27] | [JSON](i7a_22p_qda_AAAAA.json) |
| `AAAAAA` | 無彊 | [《史記・越王勾踐世家》][27] | [JSON](i7a_22p_qda_AAAAAA.json) |

</details>

<details><summary><code>i8i_rvh_4lp</code> 燬（衛文公）（8 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 燬（衛文公） | [《史記・衛康叔世家》][23] | [JSON](i8i_rvh_4lp.json) |
| `A` | 鄭（衛成公） | [《史記・衛康叔世家》][23] | [JSON](i8i_rvh_4lp_A.json) |
| `AA` | 遫（衛穆公） | [《史記・衛康叔世家》][23] | [JSON](i8i_rvh_4lp_AA.json) |
| `AAA` | 臧（衛定公） | [《史記・衛康叔世家》][23] | [JSON](i8i_rvh_4lp_AAA.json) |
| `AAAA` | 衎（衛獻公） | [《史記・衛康叔世家》][23] | [JSON](i8i_rvh_4lp_AAAA.json) |
| `AAAAA` | 惡（衛襄公） | [《史記・衛康叔世家》][23] | [JSON](i8i_rvh_4lp_AAAAA.json) |
| `AAAAAA` | 元（衛靈公） | [《史記・衛康叔世家》][23] | [JSON](i8i_rvh_4lp_AAAAAA.json) |
| `AAAAAAA` | 郢（衛子南） | [《史記・衛康叔世家》][23] | [JSON](i8i_rvh_4lp_AAAAAAA.json) |

</details>

<details><summary><code>ibz_19q_kow</code> 劉郢（儒林列傳候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 劉郢 | [《史記・儒林列傳》][107] | [JSON](ibz_19q_kow.json) |
| `A` | 楚太子戊 | [《史記・儒林列傳》][107] | [JSON](ibz_19q_kow_A.json) |

</details>

<details><summary><code>iij_zqi_k5l</code> 齊平公（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 齊平公 | [《史記・齊太公世家》][18] | [JSON](iij_zqi_k5l.json) |
| `A` | 積（齊宣公） | [《史記・齊太公世家》][18] | [JSON](iij_zqi_k5l_A.json) |
| `AA` | 貸（齊康公） | [《史記・齊太公世家》][18] | [JSON](iij_zqi_k5l_AA.json) |

</details>

<details><summary><code>inr_w1g_bu5</code> 子襄（孔子世家候選）（7 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 子襄 | [《史記・孔子世家》][33] | [JSON](inr_w1g_bu5.json) |
| `A` | 忠 | [《史記・孔子世家》][33] | [JSON](inr_w1g_bu5_A.json) |
| `AA` | 武 | [《史記・孔子世家》][33] | [JSON](inr_w1g_bu5_AA.json) |
| `AAA` | 延年 | [《史記・孔子世家》][33] | [JSON](inr_w1g_bu5_AAA.json) |
| `AAB` | 安國 | [《史記・孔子世家》][33] | [JSON](inr_w1g_bu5_AAB.json) |
| `AABA` | 卬 | [《史記・孔子世家》][33] | [JSON](inr_w1g_bu5_AABA.json) |
| `AABAA` | 驩 | [《史記・孔子世家》][33] | [JSON](inr_w1g_bu5_AABAA.json) |

</details>

<details><summary><code>ixk_6fg_v6f</code> 竇后父（外戚世家候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 竇后父 | [《史記・外戚世家》][35] | [JSON](ixk_6fg_v6f.json) |
| `A` | 竇太后（孝文帝皇后） | [《史記・梁孝王世家》][44] | [JSON](ixk_6fg_v6f_A.json) |

</details>

<details><summary><code>j32_wtj_khz</code> 袁盎父未名（袁盎鼂錯列傳候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 袁盎父未名 | [《史記・袁盎鼂錯列傳》][87] | [JSON](j32_wtj_khz.json) |
| `A` | 袁盎 | [《史記・袁盎鼂錯列傳》][87] | [JSON](j32_wtj_khz_A.json) |

</details>

<details><summary><code>jg1_ag9_033</code> 老子（孔子世家候選）（4 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 老子 | [《史記・老子韓非列傳》][49] | [JSON](jg1_ag9_033.json) |
| `A` | 宗 | [《史記・老子韓非列傳》][49] | [JSON](jg1_ag9_033_A.json) |
| `AA` | 注 | [《史記・老子韓非列傳》][49] | [JSON](jg1_ag9_033_AA.json) |
| `AAA` | 宮 | [《史記・老子韓非列傳》][49] | [JSON](jg1_ag9_033_AAA.json) |

</details>

<details><summary><code>jjl_irg_zke</code> 盧綰父未名（韓信盧綰列傳候選）（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 盧綰父未名 | [《史記・韓信盧綰列傳》][79] | [JSON](jjl_irg_zke.json) |
| `A` | 盧綰 | [《史記・韓信盧綰列傳》][79] | [JSON](jjl_irg_zke_A.json) |
| `A*A` | 盧他之 | [《史記・韓信盧綰列傳》][79] | [JSON](jjl_irg_zke_A%2AA.json) |

</details>

<details><summary><code>jo4_4bf_0ra</code> 劉澤（5 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 劉澤 | [《史記・荊燕世家》][37] | [JSON](jo4_4bf_0ra.json) |
| `A` | 嘉（燕康王） | [《史記・荊燕世家》][37] | [JSON](jo4_4bf_0ra_A.json) |
| `AA` | 定國 | [《史記・荊燕世家》][37] | [JSON](jo4_4bf_0ra_AA.json) |
| `AAA` | 定國所生男（荊燕世家未名者） | [《史記・荊燕世家》][37] | [JSON](jo4_4bf_0ra_AAA.json) |
| `AB` | 田蚡夫人（燕康王女，未名） | [《史記・魏其武安侯列傳》][93] | [JSON](jo4_4bf_0ra_AB.json) |

</details>

<details><summary><code>jru_oiq_x0q</code> 楚成王（鄭世家候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 楚成王 | [《史記・鄭世家》][28] | [JSON](jru_oiq_x0q.json) |
| `A` | 商臣 | [《史記・鄭世家》][28] | [JSON](jru_oiq_x0q_A.json) |

</details>

<details><summary><code>jx9_cov_qe0</code> 欒布（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 欒布 | [《史記・季布欒布列傳》][86] | [JSON](jx9_cov_qe0.json) |
| `A` | 賁（欒布子） | [《史記・季布欒布列傳》][86]、[《史記・惠景間侯者年表》][124] | [JSON](jx9_cov_qe0_A.json) |

</details>

<details><summary><code>k2p_5ol_dwh</code> 蒙驁（4 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 蒙驁 | [《史記・蒙恬列傳》][74] | [JSON](k2p_5ol_dwh.json) |
| `A` | 蒙武 | [《史記・蒙恬列傳》][74] | [JSON](k2p_5ol_dwh_A.json) |
| `AA` | 蒙恬 | [《史記・蒙恬列傳》][74] | [JSON](k2p_5ol_dwh_AA.json) |
| `AB` | 蒙毅 | [《史記・蒙恬列傳》][74] | [JSON](k2p_5ol_dwh_AB.json) |

</details>

<details><summary><code>k5z_d58_n7p</code> 熊元（楚考烈王）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 熊元（楚考烈王） | [《史記・春申君列傳》][64] | [JSON](k5z_d58_n7p.json) |
| `A` | 悍（楚幽王） | [《史記・春申君列傳》][64] | [JSON](k5z_d58_n7p_A.json) |

</details>

<details><summary><code>koy_6jg_gcc</code> 周勃（6 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 周勃 | [《史記・絳侯周勃世家》][43] | [JSON](koy_6jg_gcc.json) |
| `A` | 勝之 | [《史記・絳侯周勃世家》][43] | [JSON](koy_6jg_gcc_A.json) |
| `B` | 堅 | [《史記・絳侯周勃世家》][43] | [JSON](koy_6jg_gcc_B.json) |
| `BA` | 建德 | [《史記・絳侯周勃世家》][43] | [JSON](koy_6jg_gcc_BA.json) |
| `C` | 周亞夫 | [《史記・絳侯周勃世家》][43] | [JSON](koy_6jg_gcc_C.json) |
| `CA` | 亞夫子 | [《史記・絳侯周勃世家》][43] | [JSON](koy_6jg_gcc_CA.json) |

</details>

<details><summary><code>kt8_3kv_44r</code> 頑（衛昭伯）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 頑（衛昭伯） | [《史記・衛康叔世家》][23] | [JSON](kt8_3kv_44r.json) |
| `A` | 申（衛戴公） | [《史記・衛康叔世家》][23] | [JSON](kt8_3kv_44r_A.json) |

</details>

<details><summary><code>ktk_wbg_wnm</code> 鄧公（袁盎鼂錯列傳候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 鄧公 | [《史記・袁盎鼂錯列傳》][87] | [JSON](ktk_wbg_wnm.json) |
| `A` | 章（鄧公子） | [《史記・袁盎鼂錯列傳》][87] | [JSON](ktk_wbg_wnm_A.json) |

</details>

<details><summary><code>l3c_zg4_f7z</code> 宋襄公（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 宋襄公 | [《史記・宋微子世家》][24] | [JSON](l3c_zg4_f7z.json) |
| `A` | 王臣（宋成公） | [《史記・宋微子世家》][24] | [JSON](l3c_zg4_f7z_A.json) |
| `AA` | 杵臼（宋昭公） | [《史記・宋微子世家》][24] | [JSON](l3c_zg4_f7z_AA.json) |

</details>

<details><summary><code>l8e_pxu_xre</code> 武公（趙世家趙君候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 武公 | [《史記・趙世家》][29] | [JSON](l8e_pxu_xre.json) |
| `A` | 朝 | [《史記・趙世家》][29] | [JSON](l8e_pxu_xre_A.json) |

</details>

<details><summary><code>l9e_fbr_36a</code> 倉（韓世家襄王候選）（9 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 倉 | [《史記・韓世家》][31] | [JSON](l9e_fbr_36a.json) |
| `*A` | 韓王信（韓太尉） | [《史記・韓信盧綰列傳》][79] | [JSON](l9e_fbr_36a_%2AA.json) |
| `*AA` | 韓王信太子未名 | [《史記・韓信盧綰列傳》][79] | [JSON](l9e_fbr_36a_%2AAA.json) |
| `*AAA` | 韓嬰 | [《史記・韓信盧綰列傳》][79] | [JSON](l9e_fbr_36a_%2AAAA.json) |
| `*AB` | 韓穨當 | [《史記・韓信盧綰列傳》][79] | [JSON](l9e_fbr_36a_%2AAB.json) |
| `*AB*A` | 韓嫣 | [《史記・佞幸列傳》][111] | [JSON](l9e_fbr_36a_%2AAB%2AA.json) |
| `*AB*B` | 韓說 | [《史記・東越列傳》][100] | [JSON](l9e_fbr_36a_%2AAB%2AB.json) |
| `*AB*B*A` | 韓曾 | [《史記・韓信盧綰列傳》][79] | [JSON](l9e_fbr_36a_%2AAB%2AB%2AA.json) |
| `*AB*BA` | 韓說子未名 | [《史記・韓信盧綰列傳》][79] | [JSON](l9e_fbr_36a_%2AAB%2ABA.json) |

</details>

<details><summary><code>lc6_cup_v9c</code> 稱（魯孝公）（5 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 稱（魯孝公） | [《史記・魯周公世家》][19] | [JSON](lc6_cup_v9c.json) |
| `A` | 弗湟（魯惠公） | [《史記・魯周公世家》][19] | [JSON](lc6_cup_v9c_A.json) |
| `AA` | 魯隱公 | [《史記・魯周公世家》][19] | [JSON](lc6_cup_v9c_AA.json) |
| `AB` | 魯桓公 | [《史記・魯周公世家》][19] | [JSON](lc6_cup_v9c_AB.json) |
| `ABA` | 季友（成季） | [《史記・魯周公世家》][19] | [JSON](lc6_cup_v9c_ABA.json) |

</details>

<details><summary><code>lcc_msq_vdt</code> 露（曹靖公）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 露（曹靖公） | [《史記・管蔡世家》][21] | [JSON](lcc_msq_vdt.json) |
| `A` | 伯陽（曹君） | [《史記・管蔡世家》][21] | [JSON](lcc_msq_vdt_A.json) |

</details>

<details><summary><code>li9_cmb_8ci</code> 滕公（本卷稱呼）（4 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 滕公（本卷稱呼） | [《史記・樊酈滕灌列傳》][81] | [JSON](li9_cmb_8ci.json) |
| `A` | 夏侯灶 | [《史記・樊酈滕灌列傳》][81] | [JSON](li9_cmb_8ci_A.json) |
| `AA` | 夏侯賜 | [《史記・樊酈滕灌列傳》][81] | [JSON](li9_cmb_8ci_AA.json) |
| `AAA` | 夏侯頗 | [《史記・樊酈滕灌列傳》][81] | [JSON](li9_cmb_8ci_AAA.json) |

</details>

<details><summary><code>lmu_nbm_rzo</code> 燮（陳平公）（21 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 燮（陳平公） | [《史記・陳杞世家》][22] | [JSON](lmu_nbm_rzo.json) |
| `A` | 圉（陳文公） | [《史記・陳杞世家》][22] | [JSON](lmu_nbm_rzo_A.json) |
| `AA` | 佗（陳厲公） | [《史記・陳杞世家》][22] | [JSON](lmu_nbm_rzo_AA.json) |
| `AAA` | 完（敬仲） | [《史記・田敬仲完世家》][32] | [JSON](lmu_nbm_rzo_AAA.json) |
| `AAAA` | 稚孟夷 | [《史記・田敬仲完世家》][32] | [JSON](lmu_nbm_rzo_AAAA.json) |
| `AAAAA` | 湣孟莊 | [《史記・田敬仲完世家》][32] | [JSON](lmu_nbm_rzo_AAAAA.json) |
| `AAAAAA` | 田文子須無 | [《史記・田敬仲完世家》][32] | [JSON](lmu_nbm_rzo_AAAAAA.json) |
| `AAAAAAA` | 田桓子無宇 | [《史記・田敬仲完世家》][32] | [JSON](lmu_nbm_rzo_AAAAAAA.json) |
| `AAAAAAAA` | 武子開 | [《史記・田敬仲完世家》][32] | [JSON](lmu_nbm_rzo_AAAAAAAA.json) |
| `AAAAAAAB` | 田釐子乞 | [《史記・田敬仲完世家》][32] | [JSON](lmu_nbm_rzo_AAAAAAAB.json) |
| `AAAAAAABA` | 田常 | [《史記・田敬仲完世家》][32] | [JSON](lmu_nbm_rzo_AAAAAAABA.json) |
| `AAAAAAABAA` | 田襄子盤 | [《史記・田敬仲完世家》][32] | [JSON](lmu_nbm_rzo_AAAAAAABAA.json) |
| `AAAAAAABAAA` | 田莊子白 | [《史記・田敬仲完世家》][32] | [JSON](lmu_nbm_rzo_AAAAAAABAAA.json) |
| `AAAAAAABAAAA` | 太公和 | [《史記・田敬仲完世家》][32] | [JSON](lmu_nbm_rzo_AAAAAAABAAAA.json) |
| `AAAAAAABAAAAA` | 桓公午 | [《史記・扁鵲倉公列傳》][91] | [JSON](lmu_nbm_rzo_AAAAAAABAAAAA.json) |
| `AAAAAAABAAAAAA` | 因齊 | [《史記・田敬仲完世家》][32] | [JSON](lmu_nbm_rzo_AAAAAAABAAAAAA.json) |
| `AAAAAAABAAAAAAA` | 辟彊 | [《史記・田敬仲完世家》][32]、[《史記・孟嘗君列傳》][61] | [JSON](lmu_nbm_rzo_AAAAAAABAAAAAAA.json) |
| `AAAAAAABAAAAAAAA` | 齊湣王 | [《史記・孟嘗君列傳》][61] | [JSON](lmu_nbm_rzo_AAAAAAABAAAAAAAA.json) |
| `AB` | 鮑（陳桓公） | [《史記・陳杞世家》][22] | [JSON](lmu_nbm_rzo_AB.json) |
| `ABA` | 免（陳桓公太子） | [《史記・陳杞世家》][22] | [JSON](lmu_nbm_rzo_ABA.json) |
| `ABB` | 躍（陳利公） | [《史記・陳杞世家》][22] | [JSON](lmu_nbm_rzo_ABB.json) |

</details>

<details><summary><code>lt4_hpv_4ku</code> 武成王（燕君）（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 武成王（燕君） | [《史記・燕召公世家》][20] | [JSON](lt4_hpv_4ku.json) |
| `A` | 孝王（燕君） | [《史記・燕召公世家》][20] | [JSON](lt4_hpv_4ku_A.json) |
| `AA` | 燕王喜 | [《史記・燕召公世家》][20] | [JSON](lt4_hpv_4ku_AA.json) |

</details>

<details><summary><code>lwx_9yq_ad7</code> 紂（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 紂 | [《史記・殷本紀》][7] | [JSON](lwx_9yq_ad7.json) |
| `A` | 武庚 | [《史記・衛康叔世家》][23] | [JSON](lwx_9yq_ad7_A.json) |

</details>

<details><summary><code>m0b_b5e_153</code> 田常（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 田常 | [《史記・齊太公世家》][18] | [JSON](m0b_b5e_153.json) |
| `**A` | 田和 | [《史記・六國年表》][120] | [JSON](m0b_b5e_153_%2A%2AA.json) |

</details>

<details><summary><code>m8d_pnd_ias</code> 惠侯（燕君）（10 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 惠侯（燕君） | [《史記・燕召公世家》][20] | [JSON](m8d_pnd_ias.json) |
| `A` | 釐侯（燕君） | [《史記・燕召公世家》][20] | [JSON](m8d_pnd_ias_A.json) |
| `AA` | 頃侯（燕君） | [《史記・燕召公世家》][20] | [JSON](m8d_pnd_ias_AA.json) |
| `AAA` | 哀侯（燕君） | [《史記・燕召公世家》][20] | [JSON](m8d_pnd_ias_AAA.json) |
| `AAAA` | 鄭侯（燕君） | [《史記・燕召公世家》][20] | [JSON](m8d_pnd_ias_AAAA.json) |
| `AAAAA` | 繆侯（燕君） | [《史記・燕召公世家》][20] | [JSON](m8d_pnd_ias_AAAAA.json) |
| `AAAAAA` | 宣侯（燕君） | [《史記・燕召公世家》][20] | [JSON](m8d_pnd_ias_AAAAAA.json) |
| `AAAAAAA` | 桓侯（燕君） | [《史記・燕召公世家》][20] | [JSON](m8d_pnd_ias_AAAAAAA.json) |
| `AAAAAAAA` | 燕莊公 | [《史記・齊太公世家》][18]、[《史記・燕召公世家》][20] | [JSON](m8d_pnd_ias_AAAAAAAA.json) |
| `AAAAAAAAA` | 襄公（燕君） | [《史記・燕召公世家》][20] | [JSON](m8d_pnd_ias_AAAAAAAAA.json) |

</details>

<details><summary><code>m9n_b6v_wo0</code> 梁孝王（本卷未名）（5 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 梁孝王（本卷未名） | [《史記・孝景本紀》][15] | [JSON](m9n_b6v_wo0.json) |
| `A` | 明（梁孝王子） | [《史記・孝景本紀》][15] | [JSON](m9n_b6v_wo0_A.json) |
| `B` | 彭離（梁孝王子） | [《史記・孝景本紀》][15] | [JSON](m9n_b6v_wo0_B.json) |
| `C` | 定（梁孝王子） | [《史記・孝景本紀》][15] | [JSON](m9n_b6v_wo0_C.json) |
| `D` | 不識（梁孝王子） | [《史記・孝景本紀》][15] | [JSON](m9n_b6v_wo0_D.json) |

</details>

<details><summary><code>maz_aq2_t5g</code> 季勝（趙世家祖系候選）（4 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 季勝 | [《史記・趙世家》][29] | [JSON](maz_aq2_t5g.json) |
| `A` | 孟增 | [《史記・趙世家》][29] | [JSON](maz_aq2_t5g_A.json) |
| `AA` | 衡父 | [《史記・趙世家》][29] | [JSON](maz_aq2_t5g_AA.json) |
| `AAA` | 造父 | [《史記・趙世家》][29] | [JSON](maz_aq2_t5g_AAA.json) |

</details>

<details><summary><code>mgh_3bh_rit</code> 周厲王（鄭世家候選）（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 周厲王 | [《史記・鄭世家》][28] | [JSON](mgh_3bh_rit.json) |
| `A` | 友 | [《史記・鄭世家》][28] | [JSON](mgh_3bh_rit_A.json) |
| `AA` | 掘突 | [《史記・鄭世家》][28] | [JSON](mgh_3bh_rit_AA.json) |

</details>

<details><summary><code>ms3_fa1_ps9</code> 田生（荊燕世家候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 田生 | [《史記・荊燕世家》][37] | [JSON](ms3_fa1_ps9.json) |
| `A` | 田生子 | [《史記・荊燕世家》][37] | [JSON](ms3_fa1_ps9_A.json) |

</details>

<details><summary><code>muq_yy8_8er</code> 寤生（鄭世家莊公候選）（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 寤生 | [《史記・鄭世家》][28] | [JSON](muq_yy8_8er.json) |
| `A` | 忽 | [《史記・鄭世家》][28] | [JSON](muq_yy8_8er_A.json) |
| `B` | 突 | [《史記・鄭世家》][28] | [JSON](muq_yy8_8er_B.json) |

</details>

<details><summary><code>n0i_g82_0n2</code> 蒯聵（衛莊公）（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 蒯聵（衛莊公） | [《史記・衛康叔世家》][23] | [JSON](n0i_g82_0n2.json) |
| `A` | 輒（衛出公） | [《史記・衛康叔世家》][23] | [JSON](n0i_g82_0n2_A.json) |
| `AA` | 出公子（衛黔所攻者未名） | [《史記・衛康叔世家》][23] | [JSON](n0i_g82_0n2_AA.json) |

</details>

<details><summary><code>n3u_6wg_kay</code> 隆（張次公父）（衛將軍驃騎列傳候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 隆（張次公父） | [《史記・衛將軍驃騎列傳》][97] | [JSON](n3u_6wg_kay.json) |
| `A` | 張次公 | [《史記・衛將軍驃騎列傳》][97] | [JSON](n3u_6wg_kay_A.json) |

</details>

<details><summary><code>n4f_fqh_04q</code> 易王（燕君）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 易王（燕君） | [《史記・蘇秦列傳》][55] | [JSON](n4f_fqh_04q.json) |
| `A` | 燕噲（本篇燕君） | [《史記・燕召公世家》][20] | [JSON](n4f_fqh_04q_A.json) |

</details>

<details><summary><code>nf1_c66_863</code> 楊季主（游俠列傳候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 楊季主 | [《史記・游俠列傳》][110] | [JSON](nf1_c66_863.json) |
| `A` | 楊季主子（未名縣掾） | [《史記・游俠列傳》][110] | [JSON](nf1_c66_863_A.json) |

</details>

<details><summary><code>nfj_6w2_8mn</code> 增（魏世家景湣王候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 增 | [《史記・魏世家》][30] | [JSON](nfj_6w2_8mn.json) |
| `A` | 假 | [《史記・魏世家》][30] | [JSON](nfj_6w2_8mn_A.json) |

</details>

<details><summary><code>nuf_tb9_fjs</code> 竇嬰父（未名）（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 竇嬰父（未名） | [《史記・魏其武安侯列傳》][93] | [JSON](nuf_tb9_fjs.json) |
| `A` | 竇嬰 | [《史記・魏其武安侯列傳》][93] | [JSON](nuf_tb9_fjs_A.json) |
| `AA` | 竇嬰子未名 | [《史記・魏其武安侯列傳》][93] | [JSON](nuf_tb9_fjs_AA.json) |

</details>

<details><summary><code>nxl_qt6_cpl</code> 畢萬（魏世家候選）（9 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 畢萬 | [《史記・魏世家》][30] | [JSON](nxl_qt6_cpl.json) |
| `A` | 魏武子 | [《史記・魏世家》][30] | [JSON](nxl_qt6_cpl_A.json) |
| `AA` | 魏悼子 | [《史記・魏世家》][30] | [JSON](nxl_qt6_cpl_AA.json) |
| `AAA` | 魏絳 | [《史記・魏世家》][30] | [JSON](nxl_qt6_cpl_AAA.json) |
| `AAAA` | 魏嬴 | [《史記・魏世家》][30] | [JSON](nxl_qt6_cpl_AAAA.json) |
| `AAAAA` | 魏獻子 | [《史記・魏世家》][30] | [JSON](nxl_qt6_cpl_AAAAA.json) |
| `AAAAAA` | 魏侈 | [《史記・魏世家》][30] | [JSON](nxl_qt6_cpl_AAAAAA.json) |
| `AAAAAA*A` | 魏桓子 | [《史記・魏世家》][30] | [JSON](nxl_qt6_cpl_AAAAAA%2AA.json) |
| `AAAAAA*A*A` | 都 | [《史記・魏世家》][30] | [JSON](nxl_qt6_cpl_AAAAAA%2AA%2AA.json) |

</details>

<details><summary><code>nye_x8g_zwl</code> 陳桓公鮑（田世家候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 陳桓公鮑 | [《史記・田敬仲完世家》][32] | [JSON](nye_x8g_zwl.json) |
| `A` | 陳莊公林 | [《史記・田敬仲完世家》][32] | [JSON](nye_x8g_zwl_A.json) |

</details>

<details><summary><code>o0l_em5_5v9</code> 吳芮（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 吳芮 | [《史記・高祖本紀》][12] | [JSON](o0l_em5_5v9.json) |
| `A` | 臣（吳芮子） | [《史記・呂太后本紀》][13]、[《史記・黥布列傳》][77]、[《史記・漢興以來諸侯王年表》][122] | [JSON](o0l_em5_5v9_A.json) |
| `B` | 英布妻未名 | [《史記・黥布列傳》][77] | [JSON](o0l_em5_5v9_B.json) |

</details>

<details><summary><code>opr_t0a_l8g</code> 淳于公（齊太倉令）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 淳于公（齊太倉令） | [《史記・扁鵲倉公列傳》][91] | [JSON](opr_t0a_l8g.json) |
| `A` | 緹縈 | [《史記・扁鵲倉公列傳》][91] | [JSON](opr_t0a_l8g_A.json) |

</details>

<details><summary><code>osu_yvw_bwr</code> 熊惲（楚成王候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 熊惲 | [《史記・楚世家》][26] | [JSON](osu_yvw_bwr.json) |
| `A` | 職（楚成王欲立之子） | [《史記・楚世家》][26] | [JSON](osu_yvw_bwr_A.json) |

</details>

<details><summary><code>p4b_qf7_603</code> 趙武（趙庶子）（4 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 趙武（趙庶子） | [《史記・趙世家》][29] | [JSON](p4b_qf7_603.json) |
| `A` | 趙景叔 | [《史記・趙世家》][29] | [JSON](p4b_qf7_603_A.json) |
| `AA` | 趙鞅 | [《史記・趙世家》][29] | [JSON](p4b_qf7_603_AA.json) |
| `AAA` | 趙襄子毋卹 | [《史記・趙世家》][29] | [JSON](p4b_qf7_603_AAA.json) |

</details>

<details><summary><code>p9l_wy7_y7m</code> 魏文侯（孫吳列傳候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 魏文侯 | [《史記・孫子吳起列傳》][51] | [JSON](p9l_wy7_y7m.json) |
| `A` | 魏武侯 | [《史記・孫子吳起列傳》][51] | [JSON](p9l_wy7_y7m_A.json) |

</details>

<details><summary><code>pev_wez_mab</code> 宋富人（老韓列傳候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 宋富人 | [《史記・老子韓非列傳》][49] | [JSON](pev_wez_mab.json) |
| `A` | 富人之子 | [《史記・老子韓非列傳》][49] | [JSON](pev_wez_mab_A.json) |

</details>

<details><summary><code>pg6_rqk_vuk</code> 如姬父未名（魏公子列傳候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 如姬父未名 | [《史記・魏公子列傳》][63] | [JSON](pg6_rqk_vuk.json) |
| `A` | 如姬 | [《史記・魏公子列傳》][63] | [JSON](pg6_rqk_vuk_A.json) |

</details>

<details><summary><code>pj3_k53_wtj</code> 觸龍（趙世家左師候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 觸龍 | [《史記・趙世家》][29] | [JSON](pj3_k53_wtj.json) |
| `A` | 舒祺 | [《史記・趙世家》][29] | [JSON](pj3_k53_wtj_A.json) |

</details>

<details><summary><code>pme_eis_xqi</code> 司馬錯（太史公自序候選）（7 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 司馬錯 | [《史記・太史公自序》][116] | [JSON](pme_eis_xqi.json) |
| `*A` | 司馬靳 | [《史記・太史公自序》][116] | [JSON](pme_eis_xqi_%2AA.json) |
| `*A*A` | 司馬昌 | [《史記・太史公自序》][116] | [JSON](pme_eis_xqi_%2AA%2AA.json) |
| `*A*AA` | 司馬無澤 | [《史記・太史公自序》][116] | [JSON](pme_eis_xqi_%2AA%2AAA.json) |
| `*A*AAA` | 司馬喜 | [《史記・太史公自序》][116] | [JSON](pme_eis_xqi_%2AA%2AAAA.json) |
| `*A*AAAA` | 司馬談 | [《史記・太史公自序》][116] | [JSON](pme_eis_xqi_%2AA%2AAAAA.json) |
| `*A*AAAAA` | 司馬遷 | [《史記・太史公自序》][116] | [JSON](pme_eis_xqi_%2AA%2AAAAAA.json) |

</details>

<details><summary><code>pyb_nda_bwz</code> 鄖公與懷之父（伍胥列傳候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 鄖公與懷之父 | [《史記・伍子胥列傳》][52] | [JSON](pyb_nda_bwz.json) |
| `A` | 懷 | [《史記・伍子胥列傳》][52] | [JSON](pyb_nda_bwz_A.json) |

</details>

<details><summary><code>q1y_uet_htw</code> 伯州犁（伍胥列傳候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 伯州犁 | [《史記・伍子胥列傳》][52] | [JSON](q1y_uet_htw.json) |
| `*A` | 伯嚭 | [《史記・伍子胥列傳》][52] | [JSON](q1y_uet_htw_%2AA.json) |

</details>

<details><summary><code>q60_34y_1zh</code> 章（楚惠王）（5 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 章（楚惠王） | [《史記・楚世家》][26] | [JSON](q60_34y_1zh.json) |
| `A` | 中（楚簡王） | [《史記・楚世家》][26] | [JSON](q60_34y_1zh_A.json) |
| `AA` | 當（楚聲王） | [《史記・楚世家》][26] | [JSON](q60_34y_1zh_AA.json) |
| `AAA` | 熊疑（楚悼王） | [《史記・范睢蔡澤列傳》][65] | [JSON](q60_34y_1zh_AAA.json) |
| `AAAA` | 臧（楚肅王） | [《史記・楚世家》][26] | [JSON](q60_34y_1zh_AAAA.json) |

</details>

<details><summary><code>q69_35n_f3h</code> 公孫弘（平津侯主父列傳候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 公孫弘 | [《史記・平津侯主父列傳》][98] | [JSON](q69_35n_f3h.json) |
| `A` | 公孫度 | [《史記・平津侯主父列傳》][98] | [JSON](q69_35n_f3h_A.json) |

</details>

<details><summary><code>q6w_qm5_w2b</code> 丹（趙世家孝成王候選）（4 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 丹 | [《史記・平原君虞卿列傳》][62] | [JSON](q6w_qm5_w2b.json) |
| `A` | 偃 | [《史記・趙世家》][29] | [JSON](q6w_qm5_w2b_A.json) |
| `AA` | 趙王遷 | [《史記・趙世家》][29] | [JSON](q6w_qm5_w2b_AA.json) |
| `AB` | 代王嘉 | [《史記・秦始皇本紀》][10]、[《史記・六國年表》][120] | [JSON](q6w_qm5_w2b_AB.json) |

</details>

<details><summary><code>q7c_rp0_s04</code> 趙主父（楚篇懷王奔趙時）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 趙主父（楚篇懷王奔趙時） | [《史記・楚世家》][26] | [JSON](q7c_rp0_s04.json) |
| `A` | 趙惠王（楚篇初立者） | [《史記・楚世家》][26] | [JSON](q7c_rp0_s04_A.json) |

</details>

<details><summary><code>q8m_d0c_kq3</code> 楚莊王（13 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 楚莊王 | [《史記・楚世家》][26] | [JSON](q8m_d0c_kq3.json) |
| `A` | 審（楚共王） | [《史記・楚世家》][26] | [JSON](q8m_d0c_kq3_A.json) |
| `AA` | 招（楚康王） | [《史記・楚世家》][26] | [JSON](q8m_d0c_kq3_AA.json) |
| `AAA` | 員（郟敖） | [《史記・楚世家》][26] | [JSON](q8m_d0c_kq3_AAA.json) |
| `AAAA` | 莫（郟敖子） | [《史記・楚世家》][26] | [JSON](q8m_d0c_kq3_AAAA.json) |
| `AAAB` | 平夏（郟敖子） | [《史記・楚世家》][26] | [JSON](q8m_d0c_kq3_AAAB.json) |
| `AB` | 圍 | [《史記・楚世家》][26] | [JSON](q8m_d0c_kq3_AB.json) |
| `AC` | 子比（楚初王） | [《史記・楚世家》][26] | [JSON](q8m_d0c_kq3_AC.json) |
| `AD` | 子皙（楚令尹） | [《史記・楚世家》][26] | [JSON](q8m_d0c_kq3_AD.json) |
| `AE` | 楚平王 | [《史記・楚世家》][26] | [JSON](q8m_d0c_kq3_AE.json) |
| `AEA` | 楚昭王 | [《史記・楚世家》][26] | [JSON](q8m_d0c_kq3_AEA.json) |
| `AEB` | 楚太子建 | [《史記・伍子胥列傳》][52] | [JSON](q8m_d0c_kq3_AEB.json) |
| `AEBA` | 白公勝 | [《史記・伍子胥列傳》][52] | [JSON](q8m_d0c_kq3_AEBA.json) |

</details>

<details><summary><code>qdt_1oy_jci</code> 杵臼（陳宣公）（7 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 杵臼（陳宣公） | [《史記・陳杞世家》][22] | [JSON](qdt_1oy_jci.json) |
| `A` | 款（陳穆公） | [《史記・陳杞世家》][22] | [JSON](qdt_1oy_jci_A.json) |
| `AA` | 朔（陳共公） | [《史記・陳杞世家》][22] | [JSON](qdt_1oy_jci_AA.json) |
| `AAA` | 平國（陳靈公） | [《史記・陳杞世家》][22] | [JSON](qdt_1oy_jci_AAA.json) |
| `AAAA` | 午（陳成公） | [《史記・陳杞世家》][22] | [JSON](qdt_1oy_jci_AAAA.json) |
| `AAAAA` | 哀公（陳君） | [《史記・陳杞世家》][22] | [JSON](qdt_1oy_jci_AAAAA.json) |
| `B` | 御寇（陳宣公太子） | [《史記・陳杞世家》][22] | [JSON](qdt_1oy_jci_B.json) |

</details>

<details><summary><code>qg7_n12_fne</code> 審食其（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 審食其 | [《史記・酈生陸賈列傳》][83] | [JSON](qg7_n12_fne.json) |
| `*A` | 審卿 | [《史記・淮南衡山列傳》][104] | [JSON](qg7_n12_fne_%2AA.json) |

</details>

<details><summary><code>qh8_95j_eh2</code> 獻舞（蔡哀侯）（10 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 獻舞（蔡哀侯） | [《史記・管蔡世家》][21] | [JSON](qh8_95j_eh2.json) |
| `A` | 肸（蔡繆侯） | [《史記・管蔡世家》][21] | [JSON](qh8_95j_eh2_A.json) |
| `AA` | 果（蔡莊侯） | [《史記・管蔡世家》][21] | [JSON](qh8_95j_eh2_AA.json) |
| `AAA` | 申（蔡文侯） | [《史記・管蔡世家》][21] | [JSON](qh8_95j_eh2_AAA.json) |
| `AAAA` | 固（蔡景侯） | [《史記・管蔡世家》][21] | [JSON](qh8_95j_eh2_AAAA.json) |
| `AAAAA` | 般（蔡靈侯） | [《史記・管蔡世家》][21] | [JSON](qh8_95j_eh2_AAAAA.json) |
| `AAAAAA` | 友（蔡隱太子） | [《史記・管蔡世家》][21] | [JSON](qh8_95j_eh2_AAAAAA.json) |
| `AAAAAAA` | 東國（蔡悼侯） | [《史記・管蔡世家》][21] | [JSON](qh8_95j_eh2_AAAAAAA.json) |
| `AAAAB` | 廬（蔡平侯） | [《史記・管蔡世家》][21] | [JSON](qh8_95j_eh2_AAAAB.json) |
| `AAAABA` | 平侯子（被東國攻者未名） | [《史記・管蔡世家》][21] | [JSON](qh8_95j_eh2_AAAABA.json) |

</details>

<details><summary><code>qhp_lk5_t1e</code> 李延年父（未名）（佞幸列傳候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 李延年父（未名） | [《史記・佞幸列傳》][111] | [JSON](qhp_lk5_t1e.json) |
| `A` | 李延年 | [《史記・佞幸列傳》][111] | [JSON](qhp_lk5_t1e_A.json) |

</details>

<details><summary><code>qok_ik2_99j</code> 壽（齊悼惠王世家候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 壽 | [《史記・齊悼惠王世家》][38] | [JSON](qok_ik2_99j.json) |
| `A` | 次景 | [《史記・齊悼惠王世家》][38] | [JSON](qok_ik2_99j_A.json) |

</details>

<details><summary><code>qxa_jm7_zmy</code> 黔（衛悼公）（10 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 黔（衛悼公） | [《史記・衛康叔世家》][23] | [JSON](qxa_jm7_zmy.json) |
| `A` | 弗（衛敬公） | [《史記・衛康叔世家》][23] | [JSON](qxa_jm7_zmy_A.json) |
| `AA` | 糾（衛昭公） | [《史記・衛康叔世家》][23] | [JSON](qxa_jm7_zmy_AA.json) |
| `AB` | 適（衛公子） | [《史記・衛康叔世家》][23] | [JSON](qxa_jm7_zmy_AB.json) |
| `ABA` | 穨（衛愼公） | [《史記・衛康叔世家》][23] | [JSON](qxa_jm7_zmy_ABA.json) |
| `ABAA` | 訓（衛聲公） | [《史記・衛康叔世家》][23] | [JSON](qxa_jm7_zmy_ABAA.json) |
| `ABAAA` | 遫（衛成侯） | [《史記・衛康叔世家》][23] | [JSON](qxa_jm7_zmy_ABAAA.json) |
| `ABAAAA` | 平侯（衛成侯子） | [《史記・衛康叔世家》][23] | [JSON](qxa_jm7_zmy_ABAAAA.json) |
| `ABAAAAA` | 嗣君（衛平侯子） | [《史記・衛康叔世家》][23] | [JSON](qxa_jm7_zmy_ABAAAAA.json) |
| `ABAAAAAA` | 懷君（衛嗣君子） | [《史記・衛康叔世家》][23] | [JSON](qxa_jm7_zmy_ABAAAAAA.json) |

</details>

<details><summary><code>qy1_adc_gam</code> 晉（衛宣公）（6 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 晉（衛宣公） | [《史記・衛康叔世家》][23] | [JSON](qy1_adc_gam.json) |
| `A` | 伋（衛宣公太子） | [《史記・衛康叔世家》][23] | [JSON](qy1_adc_gam_A.json) |
| `AA` | 太子伋之子（未名） | [《史記・衛康叔世家》][23] | [JSON](qy1_adc_gam_AA.json) |
| `B` | 壽（衛宣公子） | [《史記・衛康叔世家》][23] | [JSON](qy1_adc_gam_B.json) |
| `C` | 朔（衛惠公） | [《史記・衛康叔世家》][23] | [JSON](qy1_adc_gam_C.json) |
| `CA` | 赤（衛懿公） | [《史記・衛康叔世家》][23] | [JSON](qy1_adc_gam_CA.json) |

</details>

<details><summary><code>r6c_fhk_jo9</code> 韓太傅（儒林列傳候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 韓太傅 | [《史記・儒林列傳》][107] | [JSON](r6c_fhk_jo9.json) |
| `*A` | 韓生孫商 | [《史記・儒林列傳》][107] | [JSON](r6c_fhk_jo9_%2AA.json) |

</details>

<details><summary><code>r9u_j0z_xtb</code> 秦侯（5 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 秦侯 | [《史記・秦本紀》][9] | [JSON](r9u_j0z_xtb.json) |
| `A` | 公伯 | [《史記・秦本紀》][9] | [JSON](r9u_j0z_xtb_A.json) |
| `AA` | 秦仲 | [《史記・秦本紀》][9] | [JSON](r9u_j0z_xtb_AA.json) |
| `AAA` | 秦莊公 | [《史記・秦本紀》][9] | [JSON](r9u_j0z_xtb_AAA.json) |
| `AAAA` | 世父 | [《史記・秦本紀》][9] | [JSON](r9u_j0z_xtb_AAAA.json) |

</details>

<details><summary><code>ra9_o4d_rli</code> 竇長君（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 竇長君 | [《史記・外戚世家》][35]、[《史記・季布欒布列傳》][86] | [JSON](ra9_o4d_rli.json) |
| `A` | 彭祖 | [《史記・外戚世家》][35] | [JSON](ra9_o4d_rli_A.json) |

</details>

<details><summary><code>rdo_wsn_30x</code> 東樓公（杞君）（8 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 東樓公（杞君） | [《史記・陳杞世家》][22] | [JSON](rdo_wsn_30x.json) |
| `A` | 西樓公（杞君） | [《史記・陳杞世家》][22] | [JSON](rdo_wsn_30x_A.json) |
| `AA` | 題公（杞君） | [《史記・陳杞世家》][22] | [JSON](rdo_wsn_30x_AA.json) |
| `AAA` | 謀娶公（杞君） | [《史記・陳杞世家》][22] | [JSON](rdo_wsn_30x_AAA.json) |
| `AAAA` | 武公（杞君） | [《史記・陳杞世家》][22] | [JSON](rdo_wsn_30x_AAAA.json) |
| `AAAAA` | 靖公（杞君） | [《史記・陳杞世家》][22] | [JSON](rdo_wsn_30x_AAAAA.json) |
| `AAAAAA` | 共公（杞君） | [《史記・陳杞世家》][22] | [JSON](rdo_wsn_30x_AAAAAA.json) |
| `AAAAAAA` | 德公（杞君） | [《史記・陳杞世家》][22] | [JSON](rdo_wsn_30x_AAAAAAA.json) |

</details>

<details><summary><code>rex_cs0_mfo</code> 鮑革（宋文公）（12 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 鮑革（宋文公） | [《史記・宋微子世家》][24] | [JSON](rex_cs0_mfo.json) |
| `A` | 瑕（宋共公） | [《史記・宋微子世家》][24] | [JSON](rex_cs0_mfo_A.json) |
| `AA` | 戌（本版宋平公） | [《史記・宋微子世家》][24] | [JSON](rex_cs0_mfo_AA.json) |
| `AAA` | 佐（宋元公） | [《史記・宋微子世家》][24] | [JSON](rex_cs0_mfo_AAA.json) |
| `AAAA` | 頭曼（宋景公） | [《史記・宋微子世家》][24] | [JSON](rex_cs0_mfo_AAAA.json) |
| `AAAB` | 褍秦（宋元公少子） | [《史記・宋微子世家》][24] | [JSON](rex_cs0_mfo_AAAB.json) |
| `AAABA` | 糾（宋公孫） | [《史記・宋微子世家》][24] | [JSON](rex_cs0_mfo_AAABA.json) |
| `AAABAA` | 特（後宋昭公） | [《史記・宋微子世家》][24] | [JSON](rex_cs0_mfo_AAABAA.json) |
| `AAABAAA` | 購由（宋悼公） | [《史記・宋微子世家》][24] | [JSON](rex_cs0_mfo_AAABAAA.json) |
| `AAABAAAA` | 田（宋休公） | [《史記・宋微子世家》][24] | [JSON](rex_cs0_mfo_AAABAAAA.json) |
| `AAABAAAAA` | 辟兵（宋辟公） | [《史記・宋微子世家》][24] | [JSON](rex_cs0_mfo_AAABAAAAA.json) |
| `AAABAAAAAA` | 剔成（宋君） | [《史記・宋微子世家》][24] | [JSON](rex_cs0_mfo_AAABAAAAAA.json) |

</details>

<details><summary><code>rl6_a40_3hj</code> 馮唐祖父未名（張釋之馮唐列傳候選）（4 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 馮唐祖父未名 | [《史記・張釋之馮唐列傳》][88] | [JSON](rl6_a40_3hj.json) |
| `A` | 馮唐父未名 | [《史記・張釋之馮唐列傳》][88] | [JSON](rl6_a40_3hj_A.json) |
| `AA` | 馮唐 | [《史記・張釋之馮唐列傳》][88] | [JSON](rl6_a40_3hj_AA.json) |
| `AAA` | 馮遂 | [《史記・張釋之馮唐列傳》][88] | [JSON](rl6_a40_3hj_AAA.json) |

</details>

<details><summary><code>rlv_clg_euu</code> 丕鄭（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 丕鄭 | [《史記・晉世家》][25] | [JSON](rlv_clg_euu.json) |
| `A` | 丕豹 | [《史記・秦本紀》][9] | [JSON](rlv_clg_euu_A.json) |

</details>

<details><summary><code>rr8_o9c_jc1</code> 負芻（曹成公）（4 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 負芻（曹成公） | [《史記・管蔡世家》][21] | [JSON](rr8_o9c_jc1.json) |
| `A` | 勝（曹武公） | [《史記・管蔡世家》][21] | [JSON](rr8_o9c_jc1_A.json) |
| `AA` | 平公（曹武公子） | [《史記・管蔡世家》][21] | [JSON](rr8_o9c_jc1_AA.json) |
| `AAA` | 午（曹悼公） | [《史記・管蔡世家》][21] | [JSON](rr8_o9c_jc1_AAA.json) |

</details>

<details><summary><code>s11_z5r_y2z</code> 東方朔（滑稽列傳候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 東方朔 | [《史記・滑稽列傳》][112] | [JSON](s11_z5r_y2z.json) |
| `A` | 東方朔子（未名） | [《史記・滑稽列傳》][112] | [JSON](s11_z5r_y2z_A.json) |

</details>

<details><summary><code>sj9_pfu_fwh</code> 灌嬰（4 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 灌嬰 | [《史記・樊酈滕灌列傳》][81] | [JSON](sj9_pfu_fwh.json) |
| `*A` | 灌賢 | [《史記・魏其武安侯列傳》][93] | [JSON](sj9_pfu_fwh_%2AA.json) |
| `A` | 灌阿 | [《史記・樊酈滕灌列傳》][81] | [JSON](sj9_pfu_fwh_A.json) |
| `AA` | 灌彊 | [《史記・樊酈滕灌列傳》][81] | [JSON](sj9_pfu_fwh_AA.json) |

</details>

<details><summary><code>sjw_4mo_dlf</code> 徐生（儒林列傳候選）（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 徐生 | [《史記・儒林列傳》][107] | [JSON](sjw_4mo_dlf.json) |
| `*A` | 徐延 | [《史記・儒林列傳》][107] | [JSON](sjw_4mo_dlf_%2AA.json) |
| `*B` | 徐襄 | [《史記・儒林列傳》][107] | [JSON](sjw_4mo_dlf_%2AB.json) |

</details>

<details><summary><code>sy5_s6h_9ex</code> 鄭文公（重耳過國者）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 鄭文公（重耳過國者） | [《史記・鄭世家》][28] | [JSON](sy5_s6h_9ex.json) |
| `A` | 蘭 | [《史記・鄭世家》][28] | [JSON](sy5_s6h_9ex_A.json) |

</details>

<details><summary><code>t6q_oe6_hom</code> 伏生（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 伏生 | [《史記・儒林列傳》][107] | [JSON](t6q_oe6_hom.json) |
| `*A` | 伏生孫（未名） | [《史記・儒林列傳》][107] | [JSON](t6q_oe6_hom_%2AA.json) |

</details>

<details><summary><code>t7q_vt4_ktj</code> 山（齊獻公）（7 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 山（齊獻公） | [《史記・齊太公世家》][18] | [JSON](t7q_vt4_ktj.json) |
| `A` | 壽（齊武公） | [《史記・齊太公世家》][18] | [JSON](t7q_vt4_ktj_A.json) |
| `AA` | 無忌（齊厲公） | [《史記・齊太公世家》][18] | [JSON](t7q_vt4_ktj_AA.json) |
| `AAA` | 赤（齊文公） | [《史記・齊太公世家》][18] | [JSON](t7q_vt4_ktj_AAA.json) |
| `AAAA` | 脫（齊成公） | [《史記・齊太公世家》][18] | [JSON](t7q_vt4_ktj_AAAA.json) |
| `AAAAA` | 購（齊莊公） | [《史記・齊太公世家》][18] | [JSON](t7q_vt4_ktj_AAAAA.json) |
| `AAAAAA` | 祿甫（齊釐公） | [《史記・齊太公世家》][18] | [JSON](t7q_vt4_ktj_AAAAAA.json) |

</details>

<details><summary><code>tkc_9z3_91l</code> 朱建（酈生陸賈列傳候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 朱建 | [《史記・酈生陸賈列傳》][83] | [JSON](tkc_9z3_91l.json) |
| `A` | 朱建子未名 | [《史記・酈生陸賈列傳》][83] | [JSON](tkc_9z3_91l_A.json) |

</details>

<details><summary><code>txj_z8z_5me</code> 肅侯（趙世家候選）（4 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 肅侯 | [《史記・趙世家》][29] | [JSON](txj_z8z_5me.json) |
| `A` | 趙武靈王 | [《史記・趙世家》][29] | [JSON](txj_z8z_5me_A.json) |
| `AA` | 公子章 | [《史記・趙世家》][29] | [JSON](txj_z8z_5me_AA.json) |
| `AB` | 何 | [《史記・趙世家》][29] | [JSON](txj_z8z_5me_AB.json) |

</details>

<details><summary><code>tz9_dhl_ifo</code> 樛樂（南越列傳候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 樛樂 | [《史記・南越列傳》][99] | [JSON](tz9_dhl_ifo.json) |
| `A` | 廣德 | [《史記・建元以來侯者年表》][125] | [JSON](tz9_dhl_ifo_A.json) |

</details>

<details><summary><code>u87_cc1_7vm</code> 田儋（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 田儋 | [《史記・田儋列傳》][80] | [JSON](u87_cc1_7vm.json) |
| `A` | 田市 | [《史記・田儋列傳》][80] | [JSON](u87_cc1_7vm_A.json) |

</details>

<details><summary><code>uay_2h8_ps8</code> 師（陳悼太子）（4 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 師（陳悼太子） | [《史記・陳杞世家》][22] | [JSON](uay_2h8_ps8.json) |
| `A` | 吳（陳惠公） | [《史記・陳杞世家》][22] | [JSON](uay_2h8_ps8_A.json) |
| `AA` | 柳（陳懷公） | [《史記・陳杞世家》][22] | [JSON](uay_2h8_ps8_AA.json) |
| `AAA` | 越（陳湣公） | [《史記・陳杞世家》][22] | [JSON](uay_2h8_ps8_AAA.json) |

</details>

<details><summary><code>uei_vr9_n3j</code> 竇長君（絳侯周勃世家候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 竇長君 | [《史記・絳侯周勃世家》][43] | [JSON](uei_vr9_n3j.json) |
| `A` | 彭祖 | [《史記・絳侯周勃世家》][43] | [JSON](uei_vr9_n3j_A.json) |

</details>

<details><summary><code>ufr_eoj_xit</code> 石奢父（未名）（循吏列傳候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 石奢父（未名） | [《史記・循吏列傳》][105] | [JSON](ufr_eoj_xit.json) |
| `A` | 石奢 | [《史記・循吏列傳》][105] | [JSON](ufr_eoj_xit_A.json) |

</details>

<details><summary><code>uj9_x5q_yir</code> 宋義（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 宋義 | [《史記・項羽本紀》][11] | [JSON](uj9_x5q_yir.json) |
| `A` | 宋襄 | [《史記・項羽本紀》][11] | [JSON](uj9_x5q_yir_A.json) |

</details>

<details><summary><code>us5_6hk_3qm</code> 屠者（留侯世家候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 屠者 | [《史記・留侯世家》][41] | [JSON](us5_6hk_3qm.json) |
| `A` | 秦嶢下軍將 | [《史記・留侯世家》][41] | [JSON](us5_6hk_3qm_A.json) |

</details>

<details><summary><code>uud_qa6_4u1</code> 郁（杞平公）（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 郁（杞平公） | [《史記・陳杞世家》][22] | [JSON](uud_qa6_4u1.json) |
| `A` | 成（杞悼公） | [《史記・陳杞世家》][22] | [JSON](uud_qa6_4u1_A.json) |
| `AA` | 乞（杞隱公） | [《史記・陳杞世家》][22] | [JSON](uud_qa6_4u1_AA.json) |

</details>

<details><summary><code>vgg_tso_418</code> 月氏王（被殺）（大宛列傳候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 月氏王（被殺） | [《史記・大宛列傳》][109] | [JSON](vgg_tso_418.json) |
| `A` | 月氏太子（繼王） | [《史記・大宛列傳》][109] | [JSON](vgg_tso_418_A.json) |

</details>

<details><summary><code>vna_am7_jn5</code> 韋賢（張丞相列傳候選）（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 韋賢 | [《史記・張丞相列傳》][82] | [JSON](vna_am7_jn5.json) |
| `A` | 韋玄成 | [《史記・張丞相列傳》][82] | [JSON](vna_am7_jn5_A.json) |
| `B` | 韋賢長子未名 | [《史記・張丞相列傳》][82] | [JSON](vna_am7_jn5_B.json) |

</details>

<details><summary><code>vs4_n7e_1qh</code> 武（曹繆公）（8 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 武（曹繆公） | [《史記・管蔡世家》][21] | [JSON](vs4_n7e_1qh.json) |
| `A` | 終生（曹桓公） | [《史記・管蔡世家》][21] | [JSON](vs4_n7e_1qh_A.json) |
| `AA` | 夕姑（曹莊公） | [《史記・管蔡世家》][21] | [JSON](vs4_n7e_1qh_AA.json) |
| `AAA` | 夷（曹釐公） | [《史記・管蔡世家》][21] | [JSON](vs4_n7e_1qh_AAA.json) |
| `AAAA` | 班（曹昭公） | [《史記・管蔡世家》][21] | [JSON](vs4_n7e_1qh_AAAA.json) |
| `AAAAA` | 襄（曹共公） | [《史記・管蔡世家》][21] | [JSON](vs4_n7e_1qh_AAAAA.json) |
| `AAAAAA` | 壽（曹文公） | [《史記・管蔡世家》][21] | [JSON](vs4_n7e_1qh_AAAAAA.json) |
| `AAAAAAA` | 彊（曹宣公） | [《史記・管蔡世家》][21] | [JSON](vs4_n7e_1qh_AAAAAAA.json) |

</details>

<details><summary><code>vtu_yuj_kdz</code> 齊王建（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 齊王建 | [《史記・秦始皇本紀》][10]、[《史記・田儋列傳》][80] | [JSON](vtu_yuj_kdz.json) |
| `*A` | 田安 | [《史記・項羽本紀》][11]、[《史記・田儋列傳》][80] | [JSON](vtu_yuj_kdz_%2AA.json) |

</details>

<details><summary><code>vty_3n0_0ed</code> 病疽卒父（孫吳列傳候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 病疽卒父 | [《史記・孫子吳起列傳》][51] | [JSON](vty_3n0_0ed.json) |
| `A` | 病疽卒 | [《史記・孫子吳起列傳》][51] | [JSON](vty_3n0_0ed_A.json) |

</details>

<details><summary><code>vwy_7cv_69j</code> 桓子（趙世家候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 桓子 | [《史記・趙世家》][29] | [JSON](vwy_7cv_69j.json) |
| `A` | 桓子之子（趙世家未名者） | [《史記・趙世家》][29] | [JSON](vwy_7cv_69j_A.json) |

</details>

<details><summary><code>w44_37v_bcb</code> 和（宋穆公）（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 和（宋穆公） | [《史記・宋微子世家》][24] | [JSON](w44_37v_bcb.json) |
| `A` | 馮（宋莊公） | [《史記・宋微子世家》][24] | [JSON](w44_37v_bcb_A.json) |
| `AA` | 捷（宋湣公） | [《史記・宋微子世家》][24] | [JSON](w44_37v_bcb_AA.json) |

</details>

<details><summary><code>w8j_vnd_rs4</code> 傅寬（4 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 傅寬 | [《漢書・樊酈滕灌傅靳周傳》][3] | [JSON](w8j_vnd_rs4.json) |
| `A` | 傅精 | [《史記・傅靳蒯成列傳》][84]、[《史記・高祖功臣侯者年表》][123] | [JSON](w8j_vnd_rs4_A.json) |
| `AA` | 傅則 | [《史記・傅靳蒯成列傳》][84]、[《史記・高祖功臣侯者年表》][123] | [JSON](w8j_vnd_rs4_AA.json) |
| `AAA` | 傅偃 | [《史記・高祖功臣侯者年表》][123] | [JSON](w8j_vnd_rs4_AAA.json) |

</details>

<details><summary><code>wjt_htu_081</code> 頭曼（匈奴列傳）（13 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 頭曼（匈奴列傳） | [《史記・匈奴列傳》][96] | [JSON](wjt_htu_081.json) |
| `A` | 冒頓（匈奴列傳第6段） | [《史記・匈奴列傳》][96] | [JSON](wjt_htu_081_A.json) |
| `AA` | 稽粥（匈奴列傳第18至20段） | [《史記・匈奴列傳》][96] | [JSON](wjt_htu_081_AA.json) |
| `AAA` | 軍臣（匈奴列傳第27段） | [《史記・匈奴列傳》][96] | [JSON](wjt_htu_081_AAA.json) |
| `AAAA` | 於單（匈奴列傳第31至32段） | [《史記・匈奴列傳》][96] | [JSON](wjt_htu_081_AAAA.json) |
| `AAB` | 伊稚斜（匈奴列傳第31至32段） | [《史記・衛將軍驃騎列傳》][97] | [JSON](wjt_htu_081_AAB.json) |
| `AABA` | 烏維（匈奴列傳第42至43段） | [《史記・匈奴列傳》][96] | [JSON](wjt_htu_081_AABA.json) |
| `AABAA` | 烏師廬（匈奴列傳第49段） | [《史記・匈奴列傳》][96] | [JSON](wjt_htu_081_AABAA.json) |
| `AABAAA` | 兒單于之子（未名） | [《史記・匈奴列傳》][96] | [JSON](wjt_htu_081_AABAAA.json) |
| `AABB` | 呴犁湖（匈奴列傳第53段） | [《史記・匈奴列傳》][96] | [JSON](wjt_htu_081_AABB.json) |
| `AABC` | 且鞮侯（匈奴列傳第56段） | [《史記・匈奴列傳》][96] | [JSON](wjt_htu_081_AABC.json) |
| `AABCA` | 且鞮侯之女（未名，妻李陵者） | [《史記・李將軍列傳》][95]、[《史記・匈奴列傳》][96] | [JSON](wjt_htu_081_AABCA.json) |
| `B` | 少子（匈奴列傳第6段） | [《史記・匈奴列傳》][96] | [JSON](wjt_htu_081_B.json) |

</details>

<details><summary><code>wuz_yxe_b9k</code> 齊景公（4 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 齊景公 | [《史記・齊太公世家》][18] | [JSON](wuz_yxe_b9k.json) |
| `A` | 齊悼公 | [《史記・齊太公世家》][18] | [JSON](wuz_yxe_b9k_A.json) |
| `AA` | 齊簡公 | [《史記・齊太公世家》][18] | [JSON](wuz_yxe_b9k_AA.json) |
| `B` | 孺子（齊） | [《史記・齊太公世家》][18] | [JSON](wuz_yxe_b9k_B.json) |

</details>

<details><summary><code>x50_1p7_qkk</code> 魯莊公（10 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 魯莊公 | [《史記・魯周公世家》][19] | [JSON](x50_1p7_qkk.json) |
| `A` | 魯湣公 | [《史記・魯周公世家》][19] | [JSON](x50_1p7_qkk_A.json) |
| `B` | 魯釐公 | [《史記・魯周公世家》][19] | [JSON](x50_1p7_qkk_B.json) |
| `BA` | 興（魯文公） | [《史記・魯周公世家》][19] | [JSON](x50_1p7_qkk_BA.json) |
| `BAA` | 惡（文公子） | [《史記・魯周公世家》][19] | [JSON](x50_1p7_qkk_BAA.json) |
| `BAB` | 視（文公子） | [《史記・魯周公世家》][19] | [JSON](x50_1p7_qkk_BAB.json) |
| `BAC` | 俀（魯宣公） | [《史記・魯周公世家》][19] | [JSON](x50_1p7_qkk_BAC.json) |
| `BACA` | 黑肱（魯成公） | [《史記・魯周公世家》][19] | [JSON](x50_1p7_qkk_BACA.json) |
| `BACAA` | 午（魯襄公） | [《史記・魯周公世家》][19] | [JSON](x50_1p7_qkk_BACAA.json) |
| `C` | 斑（莊公子） | [《史記・魯周公世家》][19] | [JSON](x50_1p7_qkk_C.json) |

</details>

<details><summary><code>xaa_ewn_4ro</code> 臧荼（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 臧荼 | [《史記・樊酈滕灌列傳》][81] | [JSON](xaa_ewn_4ro.json) |
| `A` | 衍（臧荼子） | [《史記・韓信盧綰列傳》][79] | [JSON](xaa_ewn_4ro_A.json) |

</details>

<details><summary><code>xd8_uww_5ok</code> 蕭何（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 蕭何 | [《史記・蕭相國世家》][39] | [JSON](xd8_uww_5ok.json) |
| `*A` | 系（蕭何孫） | [《史記・孝景本紀》][15] | [JSON](xd8_uww_5ok_%2AA.json) |

</details>

<details><summary><code>xgd_r31_cmr</code> 崔杼（4 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 崔杼 | [《史記・齊太公世家》][18] | [JSON](xgd_r31_cmr.json) |
| `A` | 成（崔杼子） | [《史記・齊太公世家》][18] | [JSON](xgd_r31_cmr_A.json) |
| `B` | 彊（崔杼子） | [《史記・齊太公世家》][18] | [JSON](xgd_r31_cmr_B.json) |
| `C` | 明（崔杼子） | [《史記・齊太公世家》][18] | [JSON](xgd_r31_cmr_C.json) |

</details>

<details><summary><code>xny_prn_zyi</code> 酈商（6 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 酈商 | [《史記・樊酈滕灌列傳》][81] | [JSON](xny_prn_zyi.json) |
| `A` | 酈寄 | [《史記・樊酈滕灌列傳》][81] | [JSON](xny_prn_zyi_A.json) |
| `B` | 酈堅 | [《史記・樊酈滕灌列傳》][81] | [JSON](xny_prn_zyi_B.json) |
| `BA` | 酈遂成 | [《史記・樊酈滕灌列傳》][81] | [JSON](xny_prn_zyi_BA.json) |
| `BAA` | 酈世宗 | [《史記・樊酈滕灌列傳》][81] | [JSON](xny_prn_zyi_BAA.json) |
| `BAAA` | 酈終根 | [《史記・樊酈滕灌列傳》][81] | [JSON](xny_prn_zyi_BAAA.json) |

</details>

<details><summary><code>xrt_zof_cbt</code> 和（衛武公）（4 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 和（衛武公） | [《史記・衛康叔世家》][23] | [JSON](xrt_zof_cbt.json) |
| `A` | 揚（衛莊公） | [《史記・衛康叔世家》][23] | [JSON](xrt_zof_cbt_A.json) |
| `AA` | 州吁（衛君） | [《史記・衛康叔世家》][23] | [JSON](xrt_zof_cbt_AA.json) |
| `AB` | 完（衛桓公） | [《史記・衛康叔世家》][23] | [JSON](xrt_zof_cbt_AB.json) |

</details>

<details><summary><code>y0c_hok_598</code> 李同父未名（平原君虞卿列傳候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 李同父未名 | [《史記・平原君虞卿列傳》][62] | [JSON](y0c_hok_598.json) |
| `A` | 李同 | [《史記・平原君虞卿列傳》][62] | [JSON](y0c_hok_598_A.json) |

</details>

<details><summary><code>y3i_rsz_brn</code> 韓厥（14 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 韓厥 | [《史記・韓世家》][31] | [JSON](y3i_rsz_brn.json) |
| `A` | 韓宣子 | [《史記・韓世家》][31] | [JSON](y3i_rsz_brn_A.json) |
| `AA` | 韓貞子 | [《史記・韓世家》][31] | [JSON](y3i_rsz_brn_AA.json) |
| `AAA` | 韓簡子 | [《史記・韓世家》][31] | [JSON](y3i_rsz_brn_AAA.json) |
| `AAAA` | 韓莊子 | [《史記・韓世家》][31] | [JSON](y3i_rsz_brn_AAAA.json) |
| `AAAAA` | 韓康子 | [《史記・韓世家》][31] | [JSON](y3i_rsz_brn_AAAAA.json) |
| `AAAAAA` | 武子 | [《史記・韓世家》][31] | [JSON](y3i_rsz_brn_AAAAAA.json) |
| `AAAAAAA` | 虔 | [《史記・韓世家》][31] | [JSON](y3i_rsz_brn_AAAAAAA.json) |
| `AAAAAAAA` | 取 | [《史記・韓世家》][31] | [JSON](y3i_rsz_brn_AAAAAAAA.json) |
| `AAAAAAAAA` | 韓文侯 | [《史記・韓世家》][31] | [JSON](y3i_rsz_brn_AAAAAAAAA.json) |
| `AAAAAAAAAA` | 韓哀侯 | [《史記・韓世家》][31] | [JSON](y3i_rsz_brn_AAAAAAAAAA.json) |
| `AAAAAAAAAAA` | 韓懿侯 | [《史記・韓世家》][31] | [JSON](y3i_rsz_brn_AAAAAAAAAAA.json) |
| `AAAAAAAAAAAA` | 韓昭侯 | [《史記・韓世家》][31] | [JSON](y3i_rsz_brn_AAAAAAAAAAAA.json) |
| `AAAAAAAAAAAAA` | 宣惠王 | [《史記・韓世家》][31] | [JSON](y3i_rsz_brn_AAAAAAAAAAAAA.json) |

</details>

<details><summary><code>y3u_i0l_ztj</code> 韓宣王（趙世家候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 韓宣王 | [《史記・趙世家》][29] | [JSON](y3u_i0l_ztj.json) |
| `A` | 倉 | [《史記・趙世家》][29] | [JSON](y3u_i0l_ztj_A.json) |

</details>

<details><summary><code>y4i_pjk_4gn</code> 季歷（47 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 季歷 | [《史記・周本紀》][8] | [JSON](y4i_pjk_4gn.json) |
| `A` | 西伯昌 | [《史記・周本紀》][8] | [JSON](y4i_pjk_4gn_A.json) |
| `AA` | 周武王 | [《史記・周本紀》][8] | [JSON](y4i_pjk_4gn_AA.json) |
| `AAA` | 晉唐叔 | [《史記・晉世家》][25] | [JSON](y4i_pjk_4gn_AAA.json) |
| `AAAA` | 燮（晉侯） | [《史記・晉世家》][25] | [JSON](y4i_pjk_4gn_AAAA.json) |
| `AAAAA` | 寧族（晉武侯） | [《史記・晉世家》][25] | [JSON](y4i_pjk_4gn_AAAAA.json) |
| `AAAAAA` | 服人（晉成侯） | [《史記・晉世家》][25] | [JSON](y4i_pjk_4gn_AAAAAA.json) |
| `AAAAAAA` | 福（晉厲侯） | [《史記・晉世家》][25] | [JSON](y4i_pjk_4gn_AAAAAAA.json) |
| `AAAAAAAA` | 宜臼（晉靖侯） | [《史記・晉世家》][25] | [JSON](y4i_pjk_4gn_AAAAAAAA.json) |
| `AAAAAAAA*A` | 欒賓（靖侯庶孫） | [《史記・晉世家》][25] | [JSON](y4i_pjk_4gn_AAAAAAAA%2AA.json) |
| `AB` | 管叔 | [《史記・管蔡世家》][21] | [JSON](y4i_pjk_4gn_AB.json) |
| `AC` | 蔡叔 | [《史記・管蔡世家》][21] | [JSON](y4i_pjk_4gn_AC.json) |
| `ACA` | 胡（蔡仲） | [《史記・管蔡世家》][21] | [JSON](y4i_pjk_4gn_ACA.json) |
| `ACAA` | 荒（蔡伯） | [《史記・管蔡世家》][21] | [JSON](y4i_pjk_4gn_ACAA.json) |
| `ACAAA` | 宮侯（蔡君） | [《史記・管蔡世家》][21] | [JSON](y4i_pjk_4gn_ACAAA.json) |
| `ACAAAA` | 厲侯（蔡君） | [《史記・管蔡世家》][21] | [JSON](y4i_pjk_4gn_ACAAAA.json) |
| `ACAAAAA` | 武侯（蔡君） | [《史記・管蔡世家》][21] | [JSON](y4i_pjk_4gn_ACAAAAA.json) |
| `ACAAAAAA` | 夷侯（蔡君） | [《史記・管蔡世家》][21] | [JSON](y4i_pjk_4gn_ACAAAAAA.json) |
| `ACAAAAAAA` | 所事（蔡釐侯） | [《史記・管蔡世家》][21] | [JSON](y4i_pjk_4gn_ACAAAAAAA.json) |
| `ACAAAAAAAA` | 興（蔡共侯） | [《史記・管蔡世家》][21] | [JSON](y4i_pjk_4gn_ACAAAAAAAA.json) |
| `ACAAAAAAAAA` | 戴侯（蔡君） | [《史記・管蔡世家》][21] | [JSON](y4i_pjk_4gn_ACAAAAAAAAA.json) |
| `ACAAAAAAAAAA` | 措父（蔡宣侯） | [《史記・管蔡世家》][21] | [JSON](y4i_pjk_4gn_ACAAAAAAAAAA.json) |
| `ACAAAAAAAAAAA` | 封人（蔡桓侯） | [《史記・管蔡世家》][21] | [JSON](y4i_pjk_4gn_ACAAAAAAAAAAA.json) |
| `AD` | 周公 | [《史記・魯周公世家》][19] | [JSON](y4i_pjk_4gn_AD.json) |
| `ADA` | 伯禽 | [《史記・魯周公世家》][19] | [JSON](y4i_pjk_4gn_ADA.json) |
| `ADAA` | 酋（魯考公） | [《史記・魯周公世家》][19]、[《史記・三代世表》][118] | [JSON](y4i_pjk_4gn_ADAA.json) |
| `AE` | 衛康叔封 | [《史記・衛康叔世家》][23] | [JSON](y4i_pjk_4gn_AE.json) |
| `AEA` | 康伯（衛康叔子） | [《史記・衛康叔世家》][23] | [JSON](y4i_pjk_4gn_AEA.json) |
| `AEAA` | 考伯（衛君） | [《史記・衛康叔世家》][23] | [JSON](y4i_pjk_4gn_AEAA.json) |
| `AEAAA` | 嗣伯（衛君） | [《史記・衛康叔世家》][23] | [JSON](y4i_pjk_4gn_AEAAA.json) |
| `AEAAAA` | 偼伯（衛君） | [《史記・衛康叔世家》][23] | [JSON](y4i_pjk_4gn_AEAAAA.json) |
| `AEAAAAA` | 靖伯（衛君） | [《史記・衛康叔世家》][23] | [JSON](y4i_pjk_4gn_AEAAAAA.json) |
| `AEAAAAAA` | 貞伯（衛君） | [《史記・衛康叔世家》][23] | [JSON](y4i_pjk_4gn_AEAAAAAA.json) |
| `AEAAAAAAA` | 頃侯（衛君） | [《史記・衛康叔世家》][23] | [JSON](y4i_pjk_4gn_AEAAAAAAA.json) |
| `AEAAAAAAAA` | 釐侯（衛君） | [《史記・衛康叔世家》][23] | [JSON](y4i_pjk_4gn_AEAAAAAAAA.json) |
| `AF` | 伯邑考（文王長子） | [《史記・管蔡世家》][21] | [JSON](y4i_pjk_4gn_AF.json) |
| `AG` | 曹叔振鐸 | [《史記・管蔡世家》][21] | [JSON](y4i_pjk_4gn_AG.json) |
| `AGA` | 脾（曹太伯） | [《史記・管蔡世家》][21] | [JSON](y4i_pjk_4gn_AGA.json) |
| `AGAA` | 平（曹仲君） | [《史記・管蔡世家》][21] | [JSON](y4i_pjk_4gn_AGAA.json) |
| `AGAAA` | 侯（曹宮伯） | [《史記・管蔡世家》][21] | [JSON](y4i_pjk_4gn_AGAAA.json) |
| `AGAAAA` | 云（曹孝伯） | [《史記・管蔡世家》][21] | [JSON](y4i_pjk_4gn_AGAAAA.json) |
| `AGAAAAA` | 喜（曹夷伯） | [《史記・管蔡世家》][21] | [JSON](y4i_pjk_4gn_AGAAAAA.json) |
| `AH` | 成叔武（文王子） | [《史記・管蔡世家》][21] | [JSON](y4i_pjk_4gn_AH.json) |
| `AI` | 霍叔處（文王子） | [《史記・管蔡世家》][21] | [JSON](y4i_pjk_4gn_AI.json) |
| `AJ` | 冉季載（文王少子） | [《史記・管蔡世家》][21] | [JSON](y4i_pjk_4gn_AJ.json) |
| `B` | 虢叔 | [《史記・秦本紀》][9]、[《史記・晉世家》][25] | [JSON](y4i_pjk_4gn_B.json) |
| `C` | 虢仲（王季子） | [《史記・晉世家》][25] | [JSON](y4i_pjk_4gn_C.json) |

</details>

<details><summary><code>y97_huh_vuz</code> 秦襄公（34 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 秦襄公 | [《史記・秦本紀》][9] | [JSON](y97_huh_vuz.json) |
| `A` | 秦文公 | [《史記・秦本紀》][9] | [JSON](y97_huh_vuz_A.json) |
| `AA` | 靜公（卷末世系） | [《史記・秦始皇本紀》][10] | [JSON](y97_huh_vuz_AA.json) |
| `AAA` | 憲公（卷末世系） | [《史記・秦始皇本紀》][10] | [JSON](y97_huh_vuz_AAA.json) |
| `AAAA` | 秦德公 | [《史記・秦本紀》][9] | [JSON](y97_huh_vuz_AAAA.json) |
| `AAAAA` | 秦穆公 | [《史記・秦本紀》][9] | [JSON](y97_huh_vuz_AAAAA.json) |
| `AAAAAA` | 秦康公 | [《史記・秦本紀》][9] | [JSON](y97_huh_vuz_AAAAAA.json) |
| `AAAAAAA` | 秦共公 | [《史記・秦本紀》][9] | [JSON](y97_huh_vuz_AAAAAAA.json) |
| `AAAAAAAA` | 秦桓公 | [《史記・秦本紀》][9] | [JSON](y97_huh_vuz_AAAAAAAA.json) |
| `AAAAAAAAA` | 秦景公 | [《史記・秦本紀》][9] | [JSON](y97_huh_vuz_AAAAAAAAA.json) |
| `AAAAAAAAAA` | 秦哀公 | [《史記・秦本紀》][9] | [JSON](y97_huh_vuz_AAAAAAAAAA.json) |
| `AAAAAAAAAAA` | 秦夷公 | [《史記・秦本紀》][9] | [JSON](y97_huh_vuz_AAAAAAAAAAA.json) |
| `AAAAAAAAAAAA` | 秦惠公（夷公子） | [《史記・秦本紀》][9] | [JSON](y97_huh_vuz_AAAAAAAAAAAA.json) |
| `AAAAAAAAAAAAA` | 秦悼公 | [《史記・秦本紀》][9]、[《史記・秦始皇本紀》][10] | [JSON](y97_huh_vuz_AAAAAAAAAAAAA.json) |
| `AAAAAAAAAAAAAA` | 秦厲共公 | [《史記・秦本紀》][9] | [JSON](y97_huh_vuz_AAAAAAAAAAAAAA.json) |
| `AAAAAAAAAAAAAAA` | 秦躁公 | [《史記・秦本紀》][9] | [JSON](y97_huh_vuz_AAAAAAAAAAAAAAA.json) |
| `AAAAAAAAAAAAAB` | 剌龔公（本文字形） | [《史記・秦始皇本紀》][10] | [JSON](y97_huh_vuz_AAAAAAAAAAAAAB.json) |
| `AAAAAAAAAAAAABA` | 秦懷公 | [《史記・秦本紀》][9] | [JSON](y97_huh_vuz_AAAAAAAAAAAAABA.json) |
| `AAAAAAAAAAAAABAA` | 昭子（秦懷公太子） | [《史記・秦本紀》][9] | [JSON](y97_huh_vuz_AAAAAAAAAAAAABAA.json) |
| `AAAAAAAAAAAAABAAA` | 秦靈公 | [《史記・秦本紀》][9] | [JSON](y97_huh_vuz_AAAAAAAAAAAAABAAA.json) |
| `AAAAAAAAAAAAABAAAA` | 秦獻公 | [《史記・秦本紀》][9] | [JSON](y97_huh_vuz_AAAAAAAAAAAAABAAAA.json) |
| `AAAAAAAAAAAAABAAAAA` | 秦孝公 | [《史記・商君列傳》][54] | [JSON](y97_huh_vuz_AAAAAAAAAAAAABAAAAA.json) |
| `AAAAAAAAAAAAABAAAAAA` | 秦惠王 | [《史記・張儀列傳》][56] | [JSON](y97_huh_vuz_AAAAAAAAAAAAABAAAAAA.json) |
| `AAAAAAAAAAAAABAAAAAAA` | 秦武王 | [《史記・樗里子甘茂列傳》][57] | [JSON](y97_huh_vuz_AAAAAAAAAAAAABAAAAAAA.json) |
| `AAAAAAAAAAAAABAAAAAAB` | 秦惠王女（燕太子婦） | [《史記・燕召公世家》][20] | [JSON](y97_huh_vuz_AAAAAAAAAAAAABAAAAAAB.json) |
| `AAAAAAAAAAAAABAB` | 秦簡公 | [《史記・秦本紀》][9] | [JSON](y97_huh_vuz_AAAAAAAAAAAAABAB.json) |
| `AAAAAAAAAAAAABABA` | 秦惠公（簡公子） | [《史記・秦本紀》][9] | [JSON](y97_huh_vuz_AAAAAAAAAAAAABABA.json) |
| `AAAAAAAAAAAAABABAA` | 出子（秦惠公子） | [《史記・秦本紀》][9] | [JSON](y97_huh_vuz_AAAAAAAAAAAAABABAA.json) |
| `AAAAAAAAAB` | 畢公（秦卷末世系） | [《史記・秦始皇本紀》][10] | [JSON](y97_huh_vuz_AAAAAAAAAB.json) |
| `AAAAB` | 秦宣公 | [《史記・秦本紀》][9] | [JSON](y97_huh_vuz_AAAAB.json) |
| `AAAAC` | 秦成公 | [《史記・秦本紀》][9] | [JSON](y97_huh_vuz_AAAAC.json) |
| `AAAB` | 秦武公 | [《史記・秦本紀》][9] | [JSON](y97_huh_vuz_AAAB.json) |
| `AAABA` | 白（秦武公子） | [《史記・秦本紀》][9] | [JSON](y97_huh_vuz_AAABA.json) |
| `AAAC` | 出子 | [《史記・秦本紀》][9] | [JSON](y97_huh_vuz_AAAC.json) |

</details>

<details><summary><code>yaj_2vc_98w</code> 吳廣（趙世家娃嬴父候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 吳廣 | [《史記・趙世家》][29]、[《史記・六國年表》][120] | [JSON](yaj_2vc_98w.json) |
| `A` | 娃嬴 | [《史記・趙世家》][29] | [JSON](yaj_2vc_98w_A.json) |

</details>

<details><summary><code>yay_w6f_lis</code> 渾邪（公孫賀父）（衛將軍驃騎列傳候選）（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 渾邪（公孫賀父） | [《史記・衛將軍驃騎列傳》][97] | [JSON](yay_w6f_lis.json) |
| `A` | 公孫賀 | [《史記・衛將軍驃騎列傳》][97] | [JSON](yay_w6f_lis_A.json) |
| `AA` | 敬聲（公孫賀子） | [《史記・衛將軍驃騎列傳》][97] | [JSON](yay_w6f_lis_AA.json) |

</details>

<details><summary><code>yhm_h9f_8p0</code> 范蠡（越世家候選）（4 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 范蠡 | [《史記・越王勾踐世家》][27] | [JSON](yhm_h9f_8p0.json) |
| `A` | 朱公長男（越世家未名者） | [《史記・越王勾踐世家》][27] | [JSON](yhm_h9f_8p0_A.json) |
| `B` | 朱公中男（越世家未名者） | [《史記・越王勾踐世家》][27] | [JSON](yhm_h9f_8p0_B.json) |
| `C` | 朱公少子（越世家未名者） | [《史記・越王勾踐世家》][27] | [JSON](yhm_h9f_8p0_C.json) |

</details>

<details><summary><code>yht_8tu_hv4</code> 齊景公（田世家候選）（4 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 齊景公 | [《史記・田敬仲完世家》][32] | [JSON](yht_8tu_hv4.json) |
| `A` | 荼 | [《史記・田敬仲完世家》][32] | [JSON](yht_8tu_hv4_A.json) |
| `B` | 陽生 | [《史記・田敬仲完世家》][32] | [JSON](yht_8tu_hv4_B.json) |
| `BA` | 壬 | [《史記・田敬仲完世家》][32] | [JSON](yht_8tu_hv4_BA.json) |

</details>

<details><summary><code>ylb_ttg_8dr</code> 百里傒（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 百里傒 | [《史記・秦本紀》][9] | [JSON](ylb_ttg_8dr.json) |
| `A` | 孟明視 | [《史記・秦本紀》][9] | [JSON](ylb_ttg_8dr_A.json) |

</details>

<details><summary><code>ymr_gcs_kii</code> 熊嚴（楚君）（10 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 熊嚴（楚君） | [《史記・楚世家》][26] | [JSON](ymr_gcs_kii.json) |
| `A` | 伯霜（熊霜） | [《史記・楚世家》][26] | [JSON](ymr_gcs_kii_A.json) |
| `B` | 仲雪（熊嚴子） | [《史記・楚世家》][26] | [JSON](ymr_gcs_kii_B.json) |
| `C` | 叔堪（熊嚴子） | [《史記・楚世家》][26] | [JSON](ymr_gcs_kii_C.json) |
| `D` | 季徇（熊徇） | [《史記・楚世家》][26] | [JSON](ymr_gcs_kii_D.json) |
| `DA` | 熊咢（楚君） | [《史記・楚世家》][26] | [JSON](ymr_gcs_kii_DA.json) |
| `DAA` | 熊儀（若敖） | [《史記・楚世家》][26] | [JSON](ymr_gcs_kii_DAA.json) |
| `DAAA` | 熊坎（霄敖） | [《史記・楚世家》][26] | [JSON](ymr_gcs_kii_DAAA.json) |
| `DAAAA` | 熊眴（蚡冒） | [《史記・楚世家》][26] | [JSON](ymr_gcs_kii_DAAAA.json) |
| `DAAAAA` | 蚡冒子（熊通所弒未名者） | [《史記・楚世家》][26] | [JSON](ymr_gcs_kii_DAAAAA.json) |

</details>

<details><summary><code>yph_dkb_w4w</code> 申屠嘉（4 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 申屠嘉 | [《史記・張丞相列傳》][82] | [JSON](yph_dkb_w4w.json) |
| `A` | 申屠蔑 | [《史記・張丞相列傳》][82] | [JSON](yph_dkb_w4w_A.json) |
| `AA` | 申屠去病 | [《史記・張丞相列傳》][82] | [JSON](yph_dkb_w4w_AA.json) |
| `AAA` | 申屠臾 | [《史記・張丞相列傳》][82] | [JSON](yph_dkb_w4w_AAA.json) |

</details>

<details><summary><code>yqp_nlb_p1p</code> 太公（漢王父稱）（122 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 太公（漢王父稱） | [《史記・高祖本紀》][12] | [JSON](yqp_nlb_p1p.json) |
| `A` | 高祖 | [《史記・高祖本紀》][12] | [JSON](yqp_nlb_p1p_A.json) |
| `AA` | 孝惠（本卷稱呼） | [《史記・呂太后本紀》][13] | [JSON](yqp_nlb_p1p_AA.json) |
| `AB` | 劉肥 | [《史記・齊悼惠王世家》][38] | [JSON](yqp_nlb_p1p_AB.json) |
| `ABA` | 齊哀王（本卷未名） | [《史記・齊悼惠王世家》][38] | [JSON](yqp_nlb_p1p_ABA.json) |
| `ABB` | 卬（膠西王） | [《史記・吳王濞列傳》][92] | [JSON](yqp_nlb_p1p_ABB.json) |
| `ABBA` | 膠西王太子德 | [《史記・吳王濞列傳》][92] | [JSON](yqp_nlb_p1p_ABBA.json) |
| `ABC` | 興居（齊悼惠王子） | [《史記・齊悼惠王世家》][38] | [JSON](yqp_nlb_p1p_ABC.json) |
| `ABD` | 辟光（濟南王） | [《史記・齊悼惠王世家》][38] | [JSON](yqp_nlb_p1p_ABD.json) |
| `ABE` | 雄渠（膠東王） | [《史記・齊悼惠王世家》][38]、[《史記・吳王濞列傳》][92] | [JSON](yqp_nlb_p1p_ABE.json) |
| `ABF` | 章（城陽景王） | [《史記・齊悼惠王世家》][38] | [JSON](yqp_nlb_p1p_ABF.json) |
| `ABFA` | 喜（城陽共王） | [《史記・齊悼惠王世家》][38] | [JSON](yqp_nlb_p1p_ABFA.json) |
| `ABFAA` | 延校勘建未定 | [《史記・齊悼惠王世家》][38] | [JSON](yqp_nlb_p1p_ABFAA.json) |
| `ABFAAA` | 義 | [《史記・齊悼惠王世家》][38] | [JSON](yqp_nlb_p1p_ABFAAA.json) |
| `ABFAAAA` | 武城陽惠王 | [《史記・齊悼惠王世家》][38] | [JSON](yqp_nlb_p1p_ABFAAAA.json) |
| `ABFAAAAA` | 順 | [《史記・齊悼惠王世家》][38] | [JSON](yqp_nlb_p1p_ABFAAAAA.json) |
| `ABFAAAAAA` | 恢城陽戴王 | [《史記・齊悼惠王世家》][38] | [JSON](yqp_nlb_p1p_ABFAAAAAA.json) |
| `ABFAAAAAAA` | 景城陽末王 | [《史記・齊悼惠王世家》][38] | [JSON](yqp_nlb_p1p_ABFAAAAAAA.json) |
| `ABFAB` | 劉福 | [《史記・東越列傳》][100]、[《史記・建元以來侯者年表》][125]、[《史記・建元已來王子侯者年表》][126] | [JSON](yqp_nlb_p1p_ABFAB.json) |
| `ABFAC` | 劉齒 | [《史記・建元已來王子侯者年表》][126] | [JSON](yqp_nlb_p1p_ABFAC.json) |
| `ABG` | 賢（菑川王） | [《史記・齊悼惠王世家》][38]、[《史記・吳王濞列傳》][92] | [JSON](yqp_nlb_p1p_ABG.json) |
| `ABH` | 志（濟北王，後王菑川） | [《史記・齊悼惠王世家》][38] | [JSON](yqp_nlb_p1p_ABH.json) |
| `ABHA` | 建菑川靖王 | [《史記・齊悼惠王世家》][38] | [JSON](yqp_nlb_p1p_ABHA.json) |
| `ABHAA` | 遺 | [《史記・齊悼惠王世家》][38] | [JSON](yqp_nlb_p1p_ABHAA.json) |
| `ABHAAA` | 終古 | [《史記・齊悼惠王世家》][38] | [JSON](yqp_nlb_p1p_ABHAAA.json) |
| `ABHAAAA` | 尚菑川孝王 | [《史記・齊悼惠王世家》][38] | [JSON](yqp_nlb_p1p_ABHAAAA.json) |
| `ABHAAAAA` | 橫 | [《史記・齊悼惠王世家》][38] | [JSON](yqp_nlb_p1p_ABHAAAAA.json) |
| `ABI` | 齊孝王將閭 | [《史記・齊悼惠王世家》][38] | [JSON](yqp_nlb_p1p_ABI.json) |
| `AC` | 恒（高祖子） | [《史記・孝文本紀》][14] | [JSON](yqp_nlb_p1p_AC.json) |
| `ACA` | 文帝太子（本卷未名） | [《史記・梁孝王世家》][44] | [JSON](yqp_nlb_p1p_ACA.json) |
| `ACAA` | 徹（景帝子） | [《史記・孝武本紀》][16] | [JSON](yqp_nlb_p1p_ACAA.json) |
| `ACAAA` | 閎（齊王） | [《史記・三王世家》][46] | [JSON](yqp_nlb_p1p_ACAAA.json) |
| `ACAAB` | 旦 | [《史記・三王世家》][46] | [JSON](yqp_nlb_p1p_ACAAB.json) |
| `ACAABA` | 安定侯子 | [《史記・三王世家》][46] | [JSON](yqp_nlb_p1p_ACAABA.json) |
| `ACAABB` | 建 | [《史記・三王世家》][46] | [JSON](yqp_nlb_p1p_ACAABB.json) |
| `ACAAC` | 胥 | [《史記・三王世家》][46] | [JSON](yqp_nlb_p1p_ACAAC.json) |
| `ACAACA` | 朝陽侯子 | [《史記・三王世家》][46] | [JSON](yqp_nlb_p1p_ACAACA.json) |
| `ACAACB` | 平曲侯子 | [《史記・三王世家》][46] | [JSON](yqp_nlb_p1p_ACAACB.json) |
| `ACAACC` | 南利侯子 | [《史記・三王世家》][46] | [JSON](yqp_nlb_p1p_ACAACC.json) |
| `ACAACD` | 弘 | [《史記・三王世家》][46] | [JSON](yqp_nlb_p1p_ACAACD.json) |
| `ACAAD` | 據 | [《史記・田叔列傳》][90] | [JSON](yqp_nlb_p1p_ACAAD.json) |
| `ACAAE` | 昭帝 | [《史記・三王世家》][46] | [JSON](yqp_nlb_p1p_ACAAE.json) |
| `ACAB` | 德 | [《史記・五宗世家》][45] | [JSON](yqp_nlb_p1p_ACAB.json) |
| `ACABA` | 不害 | [《史記・五宗世家》][45] | [JSON](yqp_nlb_p1p_ACABA.json) |
| `ACABAA` | 基 | [《史記・五宗世家》][45] | [JSON](yqp_nlb_p1p_ACABAA.json) |
| `ACABAAA` | 授 | [《史記・五宗世家》][45]、[《史記・漢興以來諸侯王年表》][122] | [JSON](yqp_nlb_p1p_ACABAAA.json) |
| `ACAC` | 閼于 | [《史記・五宗世家》][45] | [JSON](yqp_nlb_p1p_ACAC.json) |
| `ACAD` | 發 | [《史記・五宗世家》][45] | [JSON](yqp_nlb_p1p_ACAD.json) |
| `ACADA` | 庸 | [《史記・五宗世家》][45]、[《史記・漢興以來諸侯王年表》][122] | [JSON](yqp_nlb_p1p_ACADA.json) |
| `ACADAA` | 鮒鮈 | [《史記・五宗世家》][45] | [JSON](yqp_nlb_p1p_ACADAA.json) |
| `ACAE` | 乘 | [《史記・五宗世家》][45] | [JSON](yqp_nlb_p1p_ACAE.json) |
| `ACAF` | 廣川王（徙趙王未名） | [《史記・五宗世家》][45] | [JSON](yqp_nlb_p1p_ACAF.json) |
| `ACAG` | 舜（景帝子） | [《史記・五宗世家》][45] | [JSON](yqp_nlb_p1p_ACAG.json) |
| `ACAGA` | 棁 | [《史記・五宗世家》][45] | [JSON](yqp_nlb_p1p_ACAGA.json) |
| `ACAGB` | 平 | [《史記・五宗世家》][45] | [JSON](yqp_nlb_p1p_ACAGB.json) |
| `ACAGC` | 商 | [《史記・五宗世家》][45] | [JSON](yqp_nlb_p1p_ACAGC.json) |
| `ACAGCA` | 安世 | [《史記・五宗世家》][45] | [JSON](yqp_nlb_p1p_ACAGCA.json) |
| `ACAH` | 栗太子（本卷未名） | [《史記・五宗世家》][45] | [JSON](yqp_nlb_p1p_ACAH.json) |
| `ACAI` | 勝（景帝子） | [《史記・五宗世家》][45] | [JSON](yqp_nlb_p1p_ACAI.json) |
| `ACAIA` | 昌 | [《史記・五宗世家》][45]、[《史記・漢興以來諸侯王年表》][122] | [JSON](yqp_nlb_p1p_ACAIA.json) |
| `ACAIAA` | 昆侈 | [《史記・五宗世家》][45] | [JSON](yqp_nlb_p1p_ACAIAA.json) |
| `ACAJ` | 越（景帝子） | [《史記・五宗世家》][45] | [JSON](yqp_nlb_p1p_ACAJ.json) |
| `ACAJA` | 齊 | [《史記・五宗世家》][45] | [JSON](yqp_nlb_p1p_ACAJA.json) |
| `ACAK` | 非（汝南王） | [《史記・五宗世家》][45] | [JSON](yqp_nlb_p1p_ACAK.json) |
| `ACAKA` | 建 | [《史記・五宗世家》][45] | [JSON](yqp_nlb_p1p_ACAKA.json) |
| `ACAL` | 餘（淮陽王） | [《史記・田叔列傳》][90] | [JSON](yqp_nlb_p1p_ACAL.json) |
| `ACALA` | 光 | [《史記・五宗世家》][45] | [JSON](yqp_nlb_p1p_ACALA.json) |
| `ACAM` | 寄（景帝子） | [《史記・五宗世家》][45] | [JSON](yqp_nlb_p1p_ACAM.json) |
| `ACAMA` | 賢 | [《史記・五宗世家》][45] | [JSON](yqp_nlb_p1p_ACAMA.json) |
| `ACAMAA` | 膠東慶 | [《史記・五宗世家》][45] | [JSON](yqp_nlb_p1p_ACAMAA.json) |
| `ACAMB` | 六安慶 | [《史記・五宗世家》][45] | [JSON](yqp_nlb_p1p_ACAMB.json) |
| `ACAN` | 端（景帝子） | [《史記・五宗世家》][45] | [JSON](yqp_nlb_p1p_ACAN.json) |
| `ACB` | 梁懷王 | [《史記・屈原賈生列傳》][70] | [JSON](yqp_nlb_p1p_ACB.json) |
| `ACC` | 參 | [《史記・梁孝王世家》][44] | [JSON](yqp_nlb_p1p_ACC.json) |
| `ACCA` | 登 | [《史記・梁孝王世家》][44] | [JSON](yqp_nlb_p1p_ACCA.json) |
| `ACCAA` | 義 | [《史記・梁孝王世家》][44] | [JSON](yqp_nlb_p1p_ACCAA.json) |
| `ACD` | 勝 | [《史記・梁孝王世家》][44] | [JSON](yqp_nlb_p1p_ACD.json) |
| `ACE` | 孝文帝女公主 | [《史記・絳侯周勃世家》][43] | [JSON](yqp_nlb_p1p_ACE.json) |
| `ACF` | 嫖（長公主） | [《史記・外戚世家》][35] | [JSON](yqp_nlb_p1p_ACF.json) |
| `ACG` | 武（文帝子） | [《史記・梁孝王世家》][44] | [JSON](yqp_nlb_p1p_ACG.json) |
| `ACGA` | 買 | [《史記・梁孝王世家》][44] | [JSON](yqp_nlb_p1p_ACGA.json) |
| `ACGAA` | 襄 | [《史記・梁孝王世家》][44] | [JSON](yqp_nlb_p1p_ACGAA.json) |
| `ACGAAA` | 無傷 | [《史記・梁孝王世家》][44] | [JSON](yqp_nlb_p1p_ACGAAA.json) |
| `ACGB` | 明 | [《史記・梁孝王世家》][44] | [JSON](yqp_nlb_p1p_ACGB.json) |
| `ACGC` | 彭離 | [《史記・梁孝王世家》][44] | [JSON](yqp_nlb_p1p_ACGC.json) |
| `ACGD` | 定 | [《史記・梁孝王世家》][44] | [JSON](yqp_nlb_p1p_ACGD.json) |
| `ACGE` | 不識 | [《史記・梁孝王世家》][44] | [JSON](yqp_nlb_p1p_ACGE.json) |
| `AD` | 恢（高祖子） | [《史記・呂太后本紀》][13] | [JSON](yqp_nlb_p1p_AD.json) |
| `AE` | 友（高祖子） | [《史記・呂太后本紀》][13] | [JSON](yqp_nlb_p1p_AE.json) |
| `AEA` | 遂（趙幽王子） | [《史記・楚元王世家》][36] | [JSON](yqp_nlb_p1p_AEA.json) |
| `AEB` | 辟彊（趙幽王子） | [《史記・孝文本紀》][14]、[《史記・楚元王世家》][36]、[《史記・漢興以來諸侯王年表》][122] | [JSON](yqp_nlb_p1p_AEB.json) |
| `AEBA` | 福 | [《史記・楚元王世家》][36]、[《史記・漢興以來諸侯王年表》][122] | [JSON](yqp_nlb_p1p_AEBA.json) |
| `AF` | 長（高祖子） | [《史記・淮南衡山列傳》][104] | [JSON](yqp_nlb_p1p_AF.json) |
| `AFA` | 淮南王安 | [《史記・淮南衡山列傳》][104] | [JSON](yqp_nlb_p1p_AFA.json) |
| `AFAA` | 陵（淮南王女） | [《史記・淮南衡山列傳》][104] | [JSON](yqp_nlb_p1p_AFAA.json) |
| `AFAB` | 不害 | [《史記・淮南衡山列傳》][104] | [JSON](yqp_nlb_p1p_AFAB.json) |
| `AFABA` | 建（不害子） | [《史記・淮南衡山列傳》][104] | [JSON](yqp_nlb_p1p_AFABA.json) |
| `AFB` | 勃（劉長子） | [《史記・淮南衡山列傳》][104] | [JSON](yqp_nlb_p1p_AFB.json) |
| `AFC` | 賜（劉長子） | [《史記・淮南衡山列傳》][104] | [JSON](yqp_nlb_p1p_AFC.json) |
| `AFCA` | 爽（衡山太子） | [《史記・淮南衡山列傳》][104] | [JSON](yqp_nlb_p1p_AFCA.json) |
| `AFCB` | 孝（衡山王子） | [《史記・淮南衡山列傳》][104] | [JSON](yqp_nlb_p1p_AFCB.json) |
| `AFCC` | 無采 | [《史記・淮南衡山列傳》][104] | [JSON](yqp_nlb_p1p_AFCC.json) |
| `AFD` | 良（劉長子） | [《史記・淮南衡山列傳》][104] | [JSON](yqp_nlb_p1p_AFD.json) |
| `AG` | 建（高祖子） | [《史記・高祖本紀》][12]、[《史記・呂太后本紀》][13]、[《史記・漢興以來諸侯王年表》][122] | [JSON](yqp_nlb_p1p_AG.json) |
| `AH` | 如意（高祖子） | [《史記・呂太后本紀》][13] | [JSON](yqp_nlb_p1p_AH.json) |
| `AI` | 魯元（本卷稱呼） | [《史記・呂太后本紀》][13] | [JSON](yqp_nlb_p1p_AI.json) |
| `B` | 伯 | [《史記・楚元王世家》][36] | [JSON](yqp_nlb_p1p_B.json) |
| `BA` | 信羹頡侯 | [《史記・楚元王世家》][36] | [JSON](yqp_nlb_p1p_BA.json) |
| `C` | 仲 | [《史記・高祖本紀》][12]、[《史記・吳王濞列傳》][92] | [JSON](yqp_nlb_p1p_C.json) |
| `CA` | 劉濞 | [《史記・吳王濞列傳》][92] | [JSON](yqp_nlb_p1p_CA.json) |
| `CAA` | 吳太子被殺未名 | [《漢書・荊燕吳王傳》][2]、[《史記・吳王濞列傳》][92] | [JSON](yqp_nlb_p1p_CAA.json) |
| `CAB` | 吳王少子未名 | [《漢書・荊燕吳王傳》][2]、[《史記・吳王濞列傳》][92] | [JSON](yqp_nlb_p1p_CAB.json) |
| `CAD` | 子華 | [《史記・吳王濞列傳》][92] | [JSON](yqp_nlb_p1p_CAD.json) |
| `CAE` | 駒（吳王太子；《史記》作子駒） | [《漢書・荊燕吳王傳》][2]、[《史記・吳王濞列傳》][92] | [JSON](yqp_nlb_p1p_CAE.json) |
| `D` | 劉交 | [《史記・楚元王世家》][36] | [JSON](yqp_nlb_p1p_D.json) |
| `DA` | 藝（楚元王子） | [《史記・孝景本紀》][15] | [JSON](yqp_nlb_p1p_DA.json) |
| `DB` | 禮（楚元王子） | [《史記・楚元王世家》][36] | [JSON](yqp_nlb_p1p_DB.json) |
| `DBA` | 道 | [《史記・楚元王世家》][36] | [JSON](yqp_nlb_p1p_DBA.json) |
| `DBAA` | 注 | [《史記・楚元王世家》][36] | [JSON](yqp_nlb_p1p_DBAA.json) |
| `DBAAA` | 純 | [《史記・楚元王世家》][36] | [JSON](yqp_nlb_p1p_DBAAA.json) |
| `DC` | 郢 | [《史記・楚元王世家》][36] | [JSON](yqp_nlb_p1p_DC.json) |
| `DCA` | 戊（楚王） | [《史記・吳王濞列傳》][92] | [JSON](yqp_nlb_p1p_DCA.json) |

</details>

<details><summary><code>z0l_1wp_de1</code> 趙破奴（匈奴列傳第44段）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 趙破奴（匈奴列傳第44段） | [《史記・匈奴列傳》][96] | [JSON](z0l_1wp_de1.json) |
| `A` | 安國（趙破奴子） | [《史記・衛將軍驃騎列傳》][97] | [JSON](z0l_1wp_de1_A.json) |

</details>

<details><summary><code>z8l_wje_08d</code> 卜商（弟子列傳候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 卜商 | [《史記・仲尼弟子列傳》][53] | [JSON](z8l_wje_08d.json) |
| `A` | 卜商之子 | [《史記・仲尼弟子列傳》][53] | [JSON](z8l_wje_08d_A.json) |

</details>

<details><summary><code>z9d_qn5_wg8</code> 路人（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 路人 | [《史記・朝鮮列傳》][101] | [JSON](z9d_qn5_wg8.json) |
| `A` | 最 | [《史記・建元以來侯者年表》][125] | [JSON](z9d_qn5_wg8_A.json) |

</details>

<details><summary><code>zan_qcc_jy5</code> 陳文公（田世家候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 陳文公 | [《史記・田敬仲完世家》][32] | [JSON](zan_qcc_jy5.json) |
| `A` | 陳厲公他 | [《史記・田敬仲完世家》][32] | [JSON](zan_qcc_jy5_A.json) |

</details>

<details><summary><code>zk0_g6b_nbq</code> 伍奢（楚篇候選）（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 伍奢 | [《史記・楚世家》][26] | [JSON](zk0_g6b_nbq.json) |
| `A` | 伍尚 | [《史記・楚世家》][26] | [JSON](zk0_g6b_nbq_A.json) |
| `B` | 伍胥 | [《史記・楚世家》][26] | [JSON](zk0_g6b_nbq_B.json) |

</details>

<details><summary><code>zql_k3t_8ro</code> 先軫（重耳五士）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 先軫（重耳五士） | [《史記・晉世家》][25] | [JSON](zql_k3t_8ro.json) |
| `A` | 先縠（右行將） | [《史記・晉世家》][25] | [JSON](zql_k3t_8ro_A.json) |

</details>

<details><summary><code>zrx_2ip_d1p</code> 張負（陳丞相世家候選）（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 張負 | [《史記・陳丞相世家》][42] | [JSON](zrx_2ip_d1p.json) |
| `*A` | 張氏女 | [《史記・陳丞相世家》][42] | [JSON](zrx_2ip_d1p_%2AA.json) |
| `A` | 張仲 | [《史記・陳丞相世家》][42] | [JSON](zrx_2ip_d1p_A.json) |

</details>

<details><summary><code>zwr_jel_e3l</code> 齊宣公（田世家候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 齊宣公 | [《史記・田敬仲完世家》][32] | [JSON](zwr_jel_e3l.json) |
| `A` | 康公貸 | [《史記・田敬仲完世家》][32] | [JSON](zwr_jel_e3l_A.json) |

</details>

[2]: https://zh.wikisource.org/w/index.php?title=漢書/卷035&oldid=2605377
[3]: https://zh.wikisource.org/w/index.php?title=漢書/卷041&oldid=2342290
[4]: https://github.com/kanripo/KR2a0007/blob/683113d4baf6febecaf2ccb7913df87c4d68d454/KR2a0007_098.txt
[7]: https://zh.wikisource.org/w/index.php?title=史記/卷003&oldid=7909145
[8]: https://zh.wikisource.org/w/index.php?title=史記/卷004&oldid=7909147
[9]: https://zh.wikisource.org/w/index.php?title=史記/卷005&oldid=8744286
[10]: https://zh.wikisource.org/w/index.php?title=史記/卷006&oldid=7907969
[11]: https://zh.wikisource.org/w/index.php?title=史記/卷007&oldid=5978360
[12]: https://zh.wikisource.org/w/index.php?title=史記/卷008&oldid=2440965
[13]: https://zh.wikisource.org/w/index.php?title=史記/卷009&oldid=2087062
[14]: https://zh.wikisource.org/w/index.php?title=史記/卷010&oldid=2599229
[15]: https://zh.wikisource.org/w/index.php?title=史記/卷011&oldid=2520527
[16]: https://zh.wikisource.org/w/index.php?title=史記/卷012&oldid=8733061
[17]: https://zh.wikisource.org/w/index.php?title=史記/卷031&oldid=7909287
[18]: https://zh.wikisource.org/w/index.php?title=史記/卷032&oldid=445042
[19]: https://zh.wikisource.org/w/index.php?title=史記/魯周公世家&oldid=7909289
[20]: https://zh.wikisource.org/w/index.php?title=史記/卷034&oldid=2559287
[21]: https://zh.wikisource.org/w/index.php?title=史記/卷035&oldid=8737302
[22]: https://zh.wikisource.org/w/index.php?title=史記/卷036&oldid=2588525
[23]: https://zh.wikisource.org/w/index.php?title=史記/卷037&oldid=5977124
[24]: https://zh.wikisource.org/w/index.php?title=史記/卷038&oldid=8737306
[25]: https://zh.wikisource.org/w/index.php?title=史記/卷039&oldid=2588534
[26]: https://zh.wikisource.org/w/index.php?title=史記/卷040&oldid=8736796
[27]: https://zh.wikisource.org/w/index.php?title=史記/卷041&oldid=2018395
[28]: https://zh.wikisource.org/w/index.php?title=史記/卷042&oldid=2016409
[29]: https://zh.wikisource.org/w/index.php?title=史記/卷043&oldid=7903603
[30]: https://zh.wikisource.org/w/index.php?title=史記/卷044&oldid=7903606
[31]: https://zh.wikisource.org/w/index.php?title=史記/卷045&oldid=7903607
[32]: https://zh.wikisource.org/w/index.php?title=史記/卷046&oldid=2560838
[33]: https://zh.wikisource.org/w/index.php?title=史記/卷047&oldid=7903609
[35]: https://zh.wikisource.org/w/index.php?title=史記/卷049&oldid=7903610
[36]: https://zh.wikisource.org/w/index.php?title=史記/卷050&oldid=8737728
[37]: https://zh.wikisource.org/w/index.php?title=史記/卷051&oldid=2380315
[38]: https://zh.wikisource.org/w/index.php?title=史記/卷052&oldid=5977113
[39]: https://zh.wikisource.org/w/index.php?title=史記/卷053&oldid=2087971
[40]: https://zh.wikisource.org/w/index.php?title=史記/卷054&oldid=1490182
[41]: https://zh.wikisource.org/w/index.php?title=史記/卷055&oldid=2666612
[42]: https://zh.wikisource.org/w/index.php?title=史記/卷056&oldid=1961615
[43]: https://zh.wikisource.org/w/index.php?title=史記/卷057&oldid=1569360
[44]: https://zh.wikisource.org/w/index.php?title=史記/卷058&oldid=8735555
[45]: https://zh.wikisource.org/w/index.php?title=史記/卷059&oldid=2621125
[46]: https://zh.wikisource.org/w/index.php?title=史記/卷060&oldid=7909290
[49]: https://zh.wikisource.org/w/index.php?title=史記/卷063&oldid=7903601
[51]: https://zh.wikisource.org/w/index.php?title=史記/卷065&oldid=2567048
[52]: https://zh.wikisource.org/w/index.php?title=史記/卷066&oldid=2621138
[53]: https://zh.wikisource.org/w/index.php?title=史記/卷067&oldid=7869003
[54]: https://zh.wikisource.org/w/index.php?title=史記/卷068&oldid=8764712
[55]: https://zh.wikisource.org/w/index.php?title=史記/卷069&oldid=2621145
[56]: https://zh.wikisource.org/w/index.php?title=史記/卷070&oldid=2621148
[57]: https://zh.wikisource.org/w/index.php?title=史記/卷071&oldid=2621152
[59]: https://zh.wikisource.org/w/index.php?title=史記/卷073&oldid=7909285
[61]: https://zh.wikisource.org/w/index.php?title=史記/卷075&oldid=1965692
[62]: https://zh.wikisource.org/w/index.php?title=史記/卷076&oldid=7909284
[63]: https://zh.wikisource.org/w/index.php?title=史記/卷077&oldid=367917
[64]: https://zh.wikisource.org/w/index.php?title=史記/卷078&oldid=2089016
[65]: https://zh.wikisource.org/w/index.php?title=史記/卷079&oldid=2549307
[66]: https://zh.wikisource.org/w/index.php?title=史記/卷080&oldid=2089316
[70]: https://zh.wikisource.org/w/index.php?title=史記/卷084&oldid=1568305
[71]: https://zh.wikisource.org/w/index.php?title=史記/卷085&oldid=2027911
[72]: https://zh.wikisource.org/w/index.php?title=史記/卷086&oldid=2388562
[73]: https://zh.wikisource.org/w/index.php?title=史記/卷087&oldid=2364605
[74]: https://zh.wikisource.org/w/index.php?title=史記/卷088&oldid=1965690
[75]: https://zh.wikisource.org/w/index.php?title=史記/卷089&oldid=8744143
[77]: https://zh.wikisource.org/w/index.php?title=史記/卷091&oldid=2509940
[79]: https://zh.wikisource.org/w/index.php?title=史記/卷093&oldid=368019
[80]: https://zh.wikisource.org/w/index.php?title=史記/卷094&oldid=2171897
[81]: https://zh.wikisource.org/w/index.php?title=史記/卷095&oldid=2298709
[82]: https://zh.wikisource.org/w/index.php?title=史記/卷096&oldid=8770206
[83]: https://zh.wikisource.org/w/index.php?title=史記/卷097&oldid=1383195
[84]: https://zh.wikisource.org/w/index.php?title=史記/卷098&oldid=1490318
[86]: https://zh.wikisource.org/w/index.php?title=史記/卷100&oldid=1965696
[87]: https://zh.wikisource.org/w/index.php?title=史記/卷101&oldid=368092
[88]: https://zh.wikisource.org/w/index.php?title=史記/卷102&oldid=1753957
[89]: https://zh.wikisource.org/w/index.php?title=史記/卷103&oldid=2096814
[90]: https://zh.wikisource.org/w/index.php?title=史記/卷104&oldid=8739534
[91]: https://zh.wikisource.org/w/index.php?title=史記/卷105&oldid=8842726
[92]: https://zh.wikisource.org/w/index.php?title=史記/卷106&oldid=405869
[93]: https://zh.wikisource.org/w/index.php?title=史記/卷107&oldid=2540571
[95]: https://zh.wikisource.org/w/index.php?title=史記/卷109&oldid=1765440
[96]: https://zh.wikisource.org/w/index.php?title=史記/卷110&oldid=8735645
[97]: https://zh.wikisource.org/w/index.php?title=史記/卷111&oldid=8730225
[98]: https://zh.wikisource.org/w/index.php?title=史記/卷112&oldid=2089420
[99]: https://zh.wikisource.org/w/index.php?title=史記/卷113&oldid=8735632
[100]: https://zh.wikisource.org/w/index.php?title=史記/卷114&oldid=8735633
[101]: https://zh.wikisource.org/w/index.php?title=史記/卷115&oldid=439220
[102]: https://zh.wikisource.org/w/index.php?title=史記/卷116&oldid=7903636
[104]: https://zh.wikisource.org/w/index.php?title=史記/卷118&oldid=7904122
[105]: https://zh.wikisource.org/w/index.php?title=史記/卷119&oldid=7904123
[106]: https://zh.wikisource.org/w/index.php?title=史記/卷120&oldid=9166127
[107]: https://zh.wikisource.org/w/index.php?title=史記/卷121&oldid=8735621
[108]: https://zh.wikisource.org/w/index.php?title=史記/卷122&oldid=7904124
[109]: https://zh.wikisource.org/w/index.php?title=史記/卷123&oldid=8736799
[110]: https://zh.wikisource.org/w/index.php?title=史記/卷124&oldid=367994
[111]: https://zh.wikisource.org/w/index.php?title=史記/卷125&oldid=2273599
[112]: https://zh.wikisource.org/w/index.php?title=史記/卷126&oldid=2609358
[116]: https://zh.wikisource.org/w/index.php?title=史記/卷130&oldid=2609362
[118]: https://zh.wikisource.org/w/index.php?title=史記/卷013&oldid=2606991
[119]: https://zh.wikisource.org/w/index.php?title=史記/卷014&oldid=2607001
[120]: https://zh.wikisource.org/w/index.php?title=史記/卷015&oldid=2607002
[121]: https://zh.wikisource.org/w/index.php?title=史記/卷016&oldid=2607007
[122]: https://zh.wikisource.org/w/index.php?title=史記/卷017&oldid=2607010
[123]: https://zh.wikisource.org/w/index.php?title=史記/卷018&oldid=9484995
[124]: https://zh.wikisource.org/w/index.php?title=史記/卷019&oldid=6359260
[125]: https://zh.wikisource.org/w/index.php?title=史記/卷020&oldid=2607036
[126]: https://zh.wikisource.org/w/index.php?title=史記/卷021&oldid=2607037
