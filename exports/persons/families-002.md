# 人物 JSON 索引

可重建匯出，涵蓋目前已標註資料，包含明示選用的暫定跨篇同指；原 ID、證據與判讀均保留。並非全部史料或完整覆核。

程式可讀取 [index.json](index.json)，再依各筆 `path` 取得人物資料。重新產生：`python3 scripts/export_person_bundles.py`。

出生排行與籍貫結構化欄位仍在逐篇回填；缺欄位不代表來源沒有此資訊。提及頻次依固定見證的獨立位置計算；原始錨點完整保留，同位置節引重出另列raw／duplicate與對應群組，不代表來源權威度。

已接合父系見 [家族組裝資料](../../registry/family-assemblies.json)。`assembled_identity.person_id` 是共用家族根的組裝 ID，`source_person_ids` 保留各篇候選；父子及同指證據可由記錄 ID 回查。缺代節點另有 `ancestor_person_id`、`generation_distance` 與空值中間世代；父親空值不表示它另成一族。

點選家族標題可展開或收起後代。`*` 表示缺名世代，不建立人物，也不表示不同缺名位置是同一人。表內只列家族根後的 ID 尾碼；根人物以「根」表示，完整 ID 保留於家族標題及 JSON。最多提及來源另列一欄，同數並列；提及次數不代表史料優先權。已完成格式遷移的舊 ID 與 JSON 入口已撤除；待身份覆核的來源候選仍分存。

尚未連入同族的人物見 [獨立人物索引](unconnected.md)。

## 可展開家族


[第1頁](README.md) · [第2頁](families-002.md)

<details><summary><code>opr_t0a_l8g</code> 淳于公（齊太倉令）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 淳于公（齊太倉令） | [《史記・扁鵲倉公列傳》][709] | [JSON](opr_t0a_l8g.json) |
| `A` | 緹縈 | [《史記・扁鵲倉公列傳》][709] | [JSON](opr_t0a_l8g_A.json) |

</details>

<details><summary><code>osu_yvw_bwr</code> 熊惲（楚成王候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 熊惲 | [《史記・楚世家》][644] | [JSON](osu_yvw_bwr.json) |
| `A` | 職（楚成王欲立之子） | [《史記・楚世家》][644] | [JSON](osu_yvw_bwr_A.json) |

</details>

<details><summary><code>p4b_qf7_603</code> 趙武（趙庶子）（4 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 趙武（趙庶子） | [《史記・趙世家》][647] | [JSON](p4b_qf7_603.json) |
| `A` | 趙景叔 | [《史記・趙世家》][647] | [JSON](p4b_qf7_603_A.json) |
| `AA` | 趙鞅 | [《史記・趙世家》][647] | [JSON](p4b_qf7_603_AA.json) |
| `AAA` | 趙襄子毋卹 | [《史記・趙世家》][647] | [JSON](p4b_qf7_603_AAA.json) |

</details>

<details><summary><code>p6s_2qn_p8n</code> 平原侯植（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 平原侯植 | [《三國志・任城陳蕭王傳》][610] | [JSON](p6s_2qn_p8n.json) |
| `A` | 曹志〔字允恭〕 | [《晉書・曹志 庾峻 郭象 庾純 秦秀》][174] | [JSON](p6s_2qn_p8n_A.json) |

</details>

<details><summary><code>p93_tgr_t8r</code> 王遠（4 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 王遠 | [《南史・王弘》][498] | [JSON](p93_tgr_t8r.json) |
| `A` | 王僧祐 | [《南齊書・王秀之 王慈 蔡約 陸慧曉 顧憲之 蕭惠基》][391]、[《南史・王弘》][493] | [JSON](p93_tgr_t8r_A.json) |
| `AA` | 王籍〔字文海〕 | [《梁書・文學下》][306]、[《南史・王弘》][490] | [JSON](p93_tgr_t8r_AA.json) |
| `AAA` | 王碧（王籍子） | [《梁書・文學下》][306] | [JSON](p93_tgr_t8r_AAA.json) |

</details>

<details><summary><code>p9l_wy7_y7m</code> 魏文侯（孫吳列傳候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 魏文侯 | [《史記・孫子吳起列傳》][669] | [JSON](p9l_wy7_y7m.json) |
| `A` | 魏武侯 | [《史記・孫子吳起列傳》][669] | [JSON](p9l_wy7_y7m_A.json) |

</details>

<details><summary><code>pbz_pni_tco</code> 何偃（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 何偃 | [《宋書・羊欣 張敷 王微》][855] | [JSON](pbz_pni_tco.json) |
| `A` | 何戢 | [《南史・后妃上》][427]、[《南史・后妃上》][428] | [JSON](pbz_pni_tco_A.json) |
| `AA` | 何婧英 | [《南史・后妃上》][427]、[《南史・后妃上》][428] | [JSON](pbz_pni_tco_AA.json) |

</details>

<details><summary><code>pev_wez_mab</code> 宋富人（老韓列傳候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 宋富人 | [《史記・老子韓非列傳》][667] | [JSON](pev_wez_mab.json) |
| `A` | 富人之子 | [《史記・老子韓非列傳》][667] | [JSON](pev_wez_mab_A.json) |

</details>

<details><summary><code>pg6_rqk_vuk</code> 如姬父未名（魏公子列傳候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 如姬父未名 | [《史記・魏公子列傳》][681] | [JSON](pg6_rqk_vuk.json) |
| `A` | 如姬 | [《史記・魏公子列傳》][681] | [JSON](pg6_rqk_vuk_A.json) |

</details>

<details><summary><code>ph1_ms8_hyq</code> 亮〔孝懿蕭后祖；字保祚〕（7 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 亮〔孝懿蕭后祖；字保祚〕 | [《宋書・后妃》][818] | [JSON](ph1_ms8_hyq.json) |
| `A` | 蕭卓 | [《宋書・后妃》][818] | [JSON](ph1_ms8_hyq_A.json) |
| `AA` | 蕭文夀〔孝懿皇后〕 | [《宋書・后妃》][818] | [JSON](ph1_ms8_hyq_AA.json) |
| `AB` | 源之〔蕭卓子〕 | [《宋書・后妃》][818] | [JSON](ph1_ms8_hyq_AB.json) |
| `ABA` | 蕭思話 | [《南齊書・王僧虔 張緒》][364]、[《南史・王曇首》][511] | [JSON](ph1_ms8_hyq_ABA.json) |
| `ABAA` | 蕭惠基 | [《南齊書・王秀之 王慈 蔡約 陸慧曉 顧憲之 蕭惠基》][390]、[《南史・王曇首》][511] | [JSON](ph1_ms8_hyq_ABAA.json) |
| `ABAB` | 蕭惠明（蕭思話次子） | [《南史・王誕　王華　王惠　王彧》][544]、[《宋書・蕭思話 劉延孫》][876] | [JSON](ph1_ms8_hyq_ABAB.json) |

</details>

<details><summary><code>pib_5me_1wm</code> 陳肇之（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 陳肇之 | [《南齊書・皇后》][324]、[《南齊書・皇后》][323] | [JSON](pib_5me_1wm.json) |
| `A` | 陳道止 | [《南史・后妃上》][422]、[《南史・后妃上》][423] | [JSON](pib_5me_1wm_A.json) |

</details>

<details><summary><code>pj3_k53_wtj</code> 觸龍（趙世家左師候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 觸龍 | [《史記・趙世家》][647] | [JSON](pj3_k53_wtj.json) |
| `A` | 舒祺 | [《史記・趙世家》][647] | [JSON](pj3_k53_wtj_A.json) |

</details>

<details><summary><code>pme_eis_xqi</code> 司馬錯（7 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 司馬錯 | [《史記・秦本紀》][627] | [JSON](pme_eis_xqi.json) |
| `*A` | 司馬靳 | [《史記・太史公自序》][734] | [JSON](pme_eis_xqi_%2AA.json) |
| `*A*A` | 司馬昌 | [《史記・太史公自序》][734] | [JSON](pme_eis_xqi_%2AA%2AA.json) |
| `*A*AA` | 司馬無澤 | [《史記・太史公自序》][734] | [JSON](pme_eis_xqi_%2AA%2AAA.json) |
| `*A*AAA` | 司馬喜 | [《史記・太史公自序》][734] | [JSON](pme_eis_xqi_%2AA%2AAAA.json) |
| `*A*AAAA` | 司馬談 | [《史記・太史公自序》][734] | [JSON](pme_eis_xqi_%2AA%2AAAAA.json) |
| `*A*AAAAA` | 司馬遷 | [《史記・太史公自序》][734] | [JSON](pme_eis_xqi_%2AA%2AAAAAA.json) |

</details>

<details><summary><code>pne_ii9_42q</code> 王廣〔西揚州刺史〕（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 王廣〔西揚州刺史〕 | [《太平御覽・人事部八十一》][918] | [JSON](pne_ii9_42q.json) |
| `A` | 王氏〔西揚州刺史王廣女〕 | [《晉書・列女》][239]、[《晉書・列女》][238]、[《太平御覽・人事部八十一》][918]、[《太平御覽・宗親部九》][920] | [JSON](pne_ii9_42q_A.json) |

</details>

<details><summary><code>ptn_sz3_vro</code> 劉義慶（4 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 劉義慶 | [《宋書・謝靈運》][863] | [JSON](ptn_sz3_vro.json) |
| `A` | 臨川王義慶女（王僧達妻，未名） | [《宋書・王僧達 顏竣》][871] | [JSON](ptn_sz3_vro_A.json) |
| `B` | 劉燁（字景舒，臨川哀王） | [《南史・宋宗室及諸王上》][453] | [JSON](ptn_sz3_vro_B.json) |
| `BA` | 劉綽（宋宗室） | [《南史・后妃上》][445]、[《南史・后妃上》][446]、[《南史・宋宗室及諸王上》][453]、[《宋書・后妃》][820] | [JSON](ptn_sz3_vro_BA.json) |

</details>

<details><summary><code>pyb_nda_bwz</code> 鄖公與懷之父（伍胥列傳候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 鄖公與懷之父 | [《史記・伍子胥列傳》][670] | [JSON](pyb_nda_bwz.json) |
| `A` | 懷 | [《史記・伍子胥列傳》][670] | [JSON](pyb_nda_bwz_A.json) |

</details>

<details><summary><code>q1y_uet_htw</code> 伯州犁（伍胥列傳候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 伯州犁 | [《史記・伍子胥列傳》][670] | [JSON](q1y_uet_htw.json) |
| `*A` | 伯嚭 | [《史記・伍子胥列傳》][670] | [JSON](q1y_uet_htw_%2AA.json) |

</details>

<details><summary><code>q60_34y_1zh</code> 章（楚惠王）（5 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 章（楚惠王） | [《史記・楚世家》][644] | [JSON](q60_34y_1zh.json) |
| `A` | 中（楚簡王） | [《史記・楚世家》][644] | [JSON](q60_34y_1zh_A.json) |
| `AA` | 當（楚聲王） | [《史記・楚世家》][644] | [JSON](q60_34y_1zh_AA.json) |
| `AAA` | 熊疑（楚悼王） | [《史記・范睢蔡澤列傳》][683] | [JSON](q60_34y_1zh_AAA.json) |
| `AAAA` | 臧（楚肅王） | [《史記・楚世家》][644] | [JSON](q60_34y_1zh_AAAA.json) |

</details>

<details><summary><code>q63_4br_3of</code> 江德隣（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 江德隣 | [《南史・荀伯玉　崔祖思　蘇侃　虞悰　胡諧之　虞玩之　劉休　江祏》][583] | [JSON](q63_4br_3of.json) |
| `A` | 江祏 | [《南史・謝晦　謝裕　謝方明　謝靈運》][479] | [JSON](q63_4br_3of_A.json) |
| `B` | 江祀 | [《南史・謝晦　謝裕　謝方明　謝靈運》][479] | [JSON](q63_4br_3of_B.json) |

</details>

<details><summary><code>q69_35n_f3h</code> 公孫弘（平津侯主父列傳候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 公孫弘 | [《史記・平津侯主父列傳》][716] | [JSON](q69_35n_f3h.json) |
| `A` | 公孫度 | [《史記・平津侯主父列傳》][716] | [JSON](q69_35n_f3h_A.json) |

</details>

<details><summary><code>q6w_qm5_w2b</code> 丹（趙世家孝成王候選）（4 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 丹 | [《史記・平原君虞卿列傳》][680] | [JSON](q6w_qm5_w2b.json) |
| `A` | 偃 | [《史記・趙世家》][647] | [JSON](q6w_qm5_w2b_A.json) |
| `AA` | 趙王遷 | [《史記・趙世家》][647] | [JSON](q6w_qm5_w2b_AA.json) |
| `AB` | 代王嘉 | [《史記・秦始皇本紀》][628]、[《史記・六國年表》][981] | [JSON](q6w_qm5_w2b_AB.json) |

</details>

<details><summary><code>q71_dto_v57</code> 秦宜禄（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 秦宜禄 | [《三國志・諸夏侯曹傳》][597] | [JSON](q71_dto_v57.json) |
| `A` | 秦朗 | [《三國志・諸夏侯曹傳》][597] | [JSON](q71_dto_v57_A.json) |

</details>

<details><summary><code>q7c_rp0_s04</code> 趙主父（楚篇懷王奔趙時）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 趙主父（楚篇懷王奔趙時） | [《史記・楚世家》][644] | [JSON](q7c_rp0_s04.json) |
| `A` | 趙惠王（楚篇初立者） | [《史記・楚世家》][644] | [JSON](q7c_rp0_s04_A.json) |

</details>

<details><summary><code>q7m_r8k_2vn</code> 王僧朗（34 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 王僧朗 | [《南史・王誕　王華　王惠　王彧》][543]、[《南史・范岫　傅昭　孔休源　江革　徐勉　許懋　殷鈞》][590] | [JSON](q7m_r8k_2vn.json) |
| `A` | 王粹 | [《南史・王誕　王華　王惠　王彧》][529] | [JSON](q7m_r8k_2vn_A.json) |
| `AA` | 王奐 | [《南齊書・王奐 從弟繢 張沖》][398] | [JSON](q7m_r8k_2vn_AA.json) |
| `AAA` | 王琛 | [《南史・王誕　王華　王惠　王彧》][529] | [JSON](q7m_r8k_2vn_AAA.json) |
| `AAAA` | 王翊 | [《王翊墓誌・節錄》][39] | [JSON](q7m_r8k_2vn_AAAA.json) |
| `AAAAA` | 王令媛 | [《王令媛墓誌・節錄》][37] | [JSON](q7m_r8k_2vn_AAAAA.json) |
| `AAB` | 王融（王奐長子） | [《南齊書・王奐 從弟繢 張沖》][399]、[《南史・王誕　王華　王惠　王彧》][529] | [JSON](q7m_r8k_2vn_AAB.json) |
| `AAC` | 王彪（王奐第三子） | [《南齊書・王奐 從弟繢 張沖》][398] | [JSON](q7m_r8k_2vn_AAC.json) |
| `AAD` | 王爽（王彪弟） | [《南齊書・王奐 從弟繢 張沖》][398]、[《南齊書・王奐 從弟繢 張沖》][399]、[《南史・王誕　王華　王惠　王彧》][529] | [JSON](q7m_r8k_2vn_AAD.json) |
| `AAE` | 王弼（王彪弟） | [《南齊書・王奐 從弟繢 張沖》][398]、[《南齊書・王奐 從弟繢 張沖》][399]、[《南史・王誕　王華　王惠　王彧》][529] | [JSON](q7m_r8k_2vn_AAE.json) |
| `AAF` | 王秉（字文政） | [《魏書・王肅 宋弁》][937] | [JSON](q7m_r8k_2vn_AAF.json) |
| `AAG` | 王奐女（殷叡妻） | [《梁書・陸倕 到洽 明山賓 殷鈞 陸襄》][293]、[《南史・王誕　王華　王惠　王彧》][529] | [JSON](q7m_r8k_2vn_AAG.json) |
| `AB` | 王份 | [《梁書・王瞻 王志 王峻 王暕 子訓 王泰 王份 孫鍚 僉 張充 柳惲 蔡撙 江蒨》][281] | [JSON](q7m_r8k_2vn_AB.json) |
| `ABA` | 王琳 | [《梁書・王瞻 王志 王峻 王暕 子訓 王泰 王份 孫鍚 僉 張充 柳惲 蔡撙 江蒨》][281]、[《南史・王誕　王華　王惠　王彧》][524]、[《南史・王誕　王華　王惠　王彧》][525] | [JSON](q7m_r8k_2vn_ABA.json) |
| `ABAA` | 王銓 | [《南史・王誕　王華　王惠　王彧》][524] | [JSON](q7m_r8k_2vn_ABAA.json) |
| `ABAAA` | 王溥（字伯淮） | [《南史・王誕　王華　王惠　王彧》][524] | [JSON](q7m_r8k_2vn_ABAAA.json) |
| `ABAB` | 王錫 | [《南史・王誕　王華　王惠　王彧》][539] | [JSON](q7m_r8k_2vn_ABAB.json) |
| `ABABA` | 王㳬 | [《周書・列傳第40 蕭詧》][954] | [JSON](q7m_r8k_2vn_ABABA.json) |
| `ABABAA` | 王瓘 | [《周書・列傳第40 蕭詧》][954] | [JSON](q7m_r8k_2vn_ABABAA.json) |
| `ABABB` | 王湜 | [《梁書・王瞻 王志 王峻 王暕 子訓 王泰 王份 孫鍚 僉 張充 柳惲 蔡撙 江蒨》][280]、[《梁書・王瞻 王志 王峻 王暕 子訓 王泰 王份 孫鍚 僉 張充 柳惲 蔡撙 江蒨》][281]、[《南史・王誕　王華　王惠　王彧》][521]、[《南史・王誕　王華　王惠　王彧》][539]、[《周書・列傳第40 蕭詧》][954] | [JSON](q7m_r8k_2vn_ABABB.json) |
| `ABABBA` | 王懷 | [《周書・列傳第40 蕭詧》][954] | [JSON](q7m_r8k_2vn_ABABBA.json) |
| `ABAC` | 王通 | [《陳書・列傳第十一: 王沖 王通 袁敬》][25] | [JSON](q7m_r8k_2vn_ABAC.json) |
| `ABAD` | 王質 | [《南史・王誕　王華　王惠　王彧》][546] | [JSON](q7m_r8k_2vn_ABAD.json) |
| `ABAE` | 王固 | [《南史・王誕　王華　王惠　王彧》][526] | [JSON](q7m_r8k_2vn_ABAE.json) |
| `ABAEA` | 王寬 | [《陳書・列傳第十五: 謝哲 蕭乾 謝嘏 張種 王固 孔奐 蕭允》][27]、[《南史・王誕　王華　王惠　王彧》][526] | [JSON](q7m_r8k_2vn_ABAEA.json) |
| `ABAEB` | 陳廢帝王皇后（王固女，臨海王妃） | [《陳書・本紀第三: 世祖》][8]、[《陳書・本紀第四: 廢帝》][10]、[《陳書・皇后》][15]、[《南史・后妃下》][451] | [JSON](q7m_r8k_2vn_ABAEB.json) |
| `ABAF` | 王僉（字公會） | [《梁書・王瞻 王志 王峻 王暕 子訓 王泰 王份 孫鍚 僉 張充 柳惲 蔡撙 江蒨》][281] | [JSON](q7m_r8k_2vn_ABAF.json) |
| `ABAG` | 王勱（陳書字公濟、南史字公齊） | [《南史・王誕　王華　王惠　王彧》][534] | [JSON](q7m_r8k_2vn_ABAG.json) |
| `AC` | 王伷（王奐弟） | [《南齊書・王奐 從弟繢 張沖》][399]、[《南史・王誕　王華　王惠　王彧》][529] | [JSON](q7m_r8k_2vn_AC.json) |
| `ACA` | 王伷女（長沙王晃妃） | [《南齊書・王奐 從弟繢 張沖》][399]、[《南史・王誕　王華　王惠　王彧》][529] | [JSON](q7m_r8k_2vn_ACA.json) |
| `B` | 王貞風（明恭王皇后） | [《南史・后妃上》][445]、[《南史・后妃上》][446] | [JSON](q7m_r8k_2vn_B.json) |
| `C` | 王楷（王蘊父） | [《古今姓氏書辯證・卷十四》][47]、[《南史・王誕　王華　王惠　王彧》][544] | [JSON](q7m_r8k_2vn_C.json) |
| `D` | 王彧姊（宋書載墓開，未名） | — | [JSON](q7m_r8k_2vn_D.json) |
| `E` | 王氏（王僧朗女，殷元素妻） | — | [JSON](q7m_r8k_2vn_E.json) |

</details>

<details><summary><code>q8m_d0c_kq3</code> 楚莊王（13 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 楚莊王 | [《史記・楚世家》][644] | [JSON](q8m_d0c_kq3.json) |
| `A` | 審（楚共王） | [《史記・楚世家》][644] | [JSON](q8m_d0c_kq3_A.json) |
| `AA` | 招（楚康王） | [《史記・楚世家》][644] | [JSON](q8m_d0c_kq3_AA.json) |
| `AAA` | 員（郟敖） | [《史記・楚世家》][644] | [JSON](q8m_d0c_kq3_AAA.json) |
| `AAAA` | 莫（郟敖子） | [《史記・楚世家》][644] | [JSON](q8m_d0c_kq3_AAAA.json) |
| `AAAB` | 平夏（郟敖子） | [《史記・楚世家》][644] | [JSON](q8m_d0c_kq3_AAAB.json) |
| `AB` | 圍 | [《史記・楚世家》][644] | [JSON](q8m_d0c_kq3_AB.json) |
| `AC` | 子比（楚初王） | [《史記・楚世家》][644] | [JSON](q8m_d0c_kq3_AC.json) |
| `AD` | 子皙（楚令尹） | [《史記・楚世家》][644] | [JSON](q8m_d0c_kq3_AD.json) |
| `AE` | 楚平王 | [《史記・楚世家》][644] | [JSON](q8m_d0c_kq3_AE.json) |
| `AEA` | 楚昭王 | [《史記・楚世家》][644] | [JSON](q8m_d0c_kq3_AEA.json) |
| `AEB` | 楚太子建 | [《史記・伍子胥列傳》][670] | [JSON](q8m_d0c_kq3_AEB.json) |
| `AEBA` | 白公勝 | [《史記・伍子胥列傳》][670] | [JSON](q8m_d0c_kq3_AEBA.json) |

</details>

<details><summary><code>qdt_1oy_jci</code> 杵臼（陳宣公）（7 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 杵臼（陳宣公） | [《史記・陳杞世家》][640] | [JSON](qdt_1oy_jci.json) |
| `A` | 款（陳穆公） | [《史記・陳杞世家》][640] | [JSON](qdt_1oy_jci_A.json) |
| `AA` | 朔（陳共公） | [《史記・陳杞世家》][640] | [JSON](qdt_1oy_jci_AA.json) |
| `AAA` | 平國（陳靈公） | [《史記・陳杞世家》][640] | [JSON](qdt_1oy_jci_AAA.json) |
| `AAAA` | 午（陳成公） | [《史記・陳杞世家》][640] | [JSON](qdt_1oy_jci_AAAA.json) |
| `AAAAA` | 哀公（陳君） | [《史記・陳杞世家》][640] | [JSON](qdt_1oy_jci_AAAAA.json) |
| `B` | 御寇（陳宣公太子） | [《史記・陳杞世家》][640] | [JSON](qdt_1oy_jci_B.json) |

</details>

<details><summary><code>qg7_n12_fne</code> 審食其（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 審食其 | [《史記・酈生陸賈列傳》][701] | [JSON](qg7_n12_fne.json) |
| `*A` | 審卿 | [《史記・淮南衡山列傳》][722] | [JSON](qg7_n12_fne_%2AA.json) |

</details>

<details><summary><code>qh8_95j_eh2</code> 獻舞（蔡哀侯）（10 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 獻舞（蔡哀侯） | [《史記・管蔡世家》][639] | [JSON](qh8_95j_eh2.json) |
| `A` | 肸（蔡繆侯） | [《史記・管蔡世家》][639] | [JSON](qh8_95j_eh2_A.json) |
| `AA` | 果（蔡莊侯） | [《史記・管蔡世家》][639] | [JSON](qh8_95j_eh2_AA.json) |
| `AAA` | 申（蔡文侯） | [《史記・管蔡世家》][639] | [JSON](qh8_95j_eh2_AAA.json) |
| `AAAA` | 固（蔡景侯） | [《史記・管蔡世家》][639] | [JSON](qh8_95j_eh2_AAAA.json) |
| `AAAAA` | 般（蔡靈侯） | [《史記・管蔡世家》][639] | [JSON](qh8_95j_eh2_AAAAA.json) |
| `AAAAAA` | 友（蔡隱太子） | [《史記・管蔡世家》][639] | [JSON](qh8_95j_eh2_AAAAAA.json) |
| `AAAAAAA` | 東國（蔡悼侯） | [《史記・管蔡世家》][639] | [JSON](qh8_95j_eh2_AAAAAAA.json) |
| `AAAAB` | 廬（蔡平侯） | [《史記・管蔡世家》][639] | [JSON](qh8_95j_eh2_AAAAB.json) |
| `AAAABA` | 平侯子（被東國攻者未名） | [《史記・管蔡世家》][639] | [JSON](qh8_95j_eh2_AAAABA.json) |

</details>

<details><summary><code>qhp_lk5_t1e</code> 李延年父（未名）（佞幸列傳候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 李延年父（未名） | [《史記・佞幸列傳》][729] | [JSON](qhp_lk5_t1e.json) |
| `A` | 李延年 | [《史記・佞幸列傳》][729] | [JSON](qhp_lk5_t1e_A.json) |

</details>

<details><summary><code>qid_wbb_2pi</code> 孔景偉（孔範曾祖）（4 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 孔景偉（孔範曾祖） | [《南史・恩倖》][593] | [JSON](qid_wbb_2pi.json) |
| `A` | 孔滔（孔範祖） | [《南史・恩倖》][593] | [JSON](qid_wbb_2pi_A.json) |
| `AA` | 孔岱（孔範父） | [《南史・恩倖》][593] | [JSON](qid_wbb_2pi_AA.json) |
| `AAA` | 孔範（字法言） | [《南史・恩倖》][593] | [JSON](qid_wbb_2pi_AAA.json) |

</details>

<details><summary><code>qil_wym_gc2</code> 歐陽景達（歐陽頠祖）（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 歐陽景達（歐陽頠祖） | [《陳書・列傳第三: 侯瑱 歐陽頠 吳明徹 裴子烈》][18] | [JSON](qil_wym_gc2.json) |
| `A` | 歐陽僧寶（歐陽頠父） | [《陳書・列傳第三: 侯瑱 歐陽頠 吳明徹 裴子烈》][18] | [JSON](qil_wym_gc2_A.json) |
| `AA` | 歐陽頠（字靖世） | [《陳書・列傳第三: 侯瑱 歐陽頠 吳明徹 裴子烈》][18] | [JSON](qil_wym_gc2_AA.json) |

</details>

<details><summary><code>qjs_3hl_6ck</code> 公子發（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 公子發 | [《春秋左傳注疏・卷三十》][978] | [JSON](qjs_3hl_6ck.json) |
| `A` | 子産 | [《史記・鄭世家》][646] | [JSON](qjs_3hl_6ck_A.json) |

</details>

<details><summary><code>qkm_hps_nmk</code> 劉爽（劉秀之祖）（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 劉爽（劉秀之祖） | [《宋書・劉秀之 顧琛 顧覬之》][879] | [JSON](qkm_hps_nmk.json) |
| `A` | 劉仲道（劉秀之父） | [《宋書・劉秀之 顧琛 顧覬之》][879] | [JSON](qkm_hps_nmk_A.json) |
| `AA` | 劉秀之（字道寶） | [《宋書・劉秀之 顧琛 顧覬之》][879] | [JSON](qkm_hps_nmk_AA.json) |

</details>

<details><summary><code>qok_ik2_99j</code> 壽（齊悼惠王世家候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 壽 | [《史記・齊悼惠王世家》][656] | [JSON](qok_ik2_99j.json) |
| `A` | 次景 | [《史記・齊悼惠王世家》][656] | [JSON](qok_ik2_99j_A.json) |

</details>

<details><summary><code>qsd_v11_ya1</code> 宏（王懿祖）（4 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 宏（王懿祖） | [《南史・王懿　到彥之　垣護之　張興世》][564]、[《宋書・趙倫之 王懿 張邵》][829]、[《宋書・趙倫之 王懿 張邵》][828] | [JSON](qsd_v11_ya1.json) |
| `A` | 苖（王懿父） | [《南史・王懿　到彥之　垣護之　張興世》][564]、[《宋書・趙倫之 王懿 張邵》][829]、[《宋書・趙倫之 王懿 張邵》][828] | [JSON](qsd_v11_ya1_A.json) |
| `AA` | 王仲徳〔劉義隆鎮北將軍〕 | [《宋書・趙倫之 王懿 張邵》][829]、[《宋書・趙倫之 王懿 張邵》][828] | [JSON](qsd_v11_ya1_AA.json) |
| `AAA` | 正脩（王懿子） | [《南史・王懿　到彥之　垣護之　張興世》][563]、[《宋書・趙倫之 王懿 張邵》][829]、[《宋書・趙倫之 王懿 張邵》][828] | [JSON](qsd_v11_ya1_AAA.json) |

</details>

<details><summary><code>qvt_eq1_lcf</code> 蕭道賜（9 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 蕭道賜 | [《梁書・武帝上》][266] | [JSON](qvt_eq1_lcf.json) |
| `A` | 蕭順之 | [《梁書・武帝中》][269] | [JSON](qvt_eq1_lcf_A.json) |
| `AA` | 蕭恢 | [《梁書・太祖五王》][291] | [JSON](qvt_eq1_lcf_AA.json) |
| `AAA` | 蕭循（宜豐侯） | [《南史・王誕　王華　王惠　王彧》][534]、[《資治通鑑・梁紀二十》][975] | [JSON](qvt_eq1_lcf_AAA.json) |
| `AB` | 蕭令嫕（義興昭長公主） | [《南史・王誕　王華　王惠　王彧》][524] | [JSON](qvt_eq1_lcf_AB.json) |
| `AC` | 蕭懿（長沙宣武王） | [《南史・后妃下》][452] | [JSON](qvt_eq1_lcf_AC.json) |
| `AD` | 蕭敷（永陽昭王） | [《南史・后妃下》][452] | [JSON](qvt_eq1_lcf_AD.json) |
| `AE` | 蕭暢（衡陽宣王） | [《南史・后妃下》][452] | [JSON](qvt_eq1_lcf_AE.json) |
| `AF` | 蕭偉（南平元襄王） | [《梁書・太祖五王》][290] | [JSON](qvt_eq1_lcf_AF.json) |

</details>

<details><summary><code>qxa_jm7_zmy</code> 黔（衛悼公）（10 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 黔（衛悼公） | [《史記・衛康叔世家》][641] | [JSON](qxa_jm7_zmy.json) |
| `A` | 弗（衛敬公） | [《史記・衛康叔世家》][641] | [JSON](qxa_jm7_zmy_A.json) |
| `AA` | 糾（衛昭公） | [《史記・衛康叔世家》][641] | [JSON](qxa_jm7_zmy_AA.json) |
| `AB` | 適（衛公子） | [《史記・衛康叔世家》][641] | [JSON](qxa_jm7_zmy_AB.json) |
| `ABA` | 穨（衛愼公） | [《史記・衛康叔世家》][641] | [JSON](qxa_jm7_zmy_ABA.json) |
| `ABAA` | 訓（衛聲公） | [《史記・衛康叔世家》][641] | [JSON](qxa_jm7_zmy_ABAA.json) |
| `ABAAA` | 遫（衛成侯） | [《史記・衛康叔世家》][641] | [JSON](qxa_jm7_zmy_ABAAA.json) |
| `ABAAAA` | 平侯（衛成侯子） | [《史記・衛康叔世家》][641] | [JSON](qxa_jm7_zmy_ABAAAA.json) |
| `ABAAAAA` | 嗣君（衛平侯子） | [《史記・衛康叔世家》][641] | [JSON](qxa_jm7_zmy_ABAAAAA.json) |
| `ABAAAAAA` | 懷君（衛嗣君子） | [《史記・衛康叔世家》][641] | [JSON](qxa_jm7_zmy_ABAAAAAA.json) |

</details>

<details><summary><code>qy1_adc_gam</code> 晉（衛宣公）（6 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 晉（衛宣公） | [《史記・衛康叔世家》][641] | [JSON](qy1_adc_gam.json) |
| `A` | 伋（衛宣公太子） | [《史記・衛康叔世家》][641] | [JSON](qy1_adc_gam_A.json) |
| `AA` | 太子伋之子（未名） | [《史記・衛康叔世家》][641] | [JSON](qy1_adc_gam_AA.json) |
| `B` | 壽（衛宣公子） | [《史記・衛康叔世家》][641] | [JSON](qy1_adc_gam_B.json) |
| `C` | 朔（衛惠公） | [《史記・衛康叔世家》][641] | [JSON](qy1_adc_gam_C.json) |
| `CA` | 赤（衛懿公） | [《史記・衛康叔世家》][641] | [JSON](qy1_adc_gam_CA.json) |

</details>

<details><summary><code>r5n_x7v_cwf</code> 彪〔孝穆趙后祖；字世範〕（5 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 彪〔孝穆趙后祖；字世範〕 | [《宋書・后妃》][818] | [JSON](r5n_x7v_cwf.json) |
| `A` | 趙裔 | [《宋書・后妃》][818] | [JSON](r5n_x7v_cwf_A.json) |
| `AA` | 宣之〔趙裔長子〕 | [《宋書・后妃》][818] | [JSON](r5n_x7v_cwf_AA.json) |
| `AB` | 趙安〔孝穆皇后；本見證，高祖之母〕 | [《宋書・后妃》][818] | [JSON](r5n_x7v_cwf_AB.json) |
| `AC` | 倫之〔宣之弟〕 | [《宋書・后妃》][818] | [JSON](r5n_x7v_cwf_AC.json) |

</details>

<details><summary><code>r6c_fhk_jo9</code> 韓太傅（儒林列傳候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 韓太傅 | [《史記・儒林列傳》][725] | [JSON](r6c_fhk_jo9.json) |
| `*A` | 韓生孫商 | [《史記・儒林列傳》][725] | [JSON](r6c_fhk_jo9_%2AA.json) |

</details>

<details><summary><code>r9u_j0z_xtb</code> 秦侯（5 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 秦侯 | [《史記・秦本紀》][627] | [JSON](r9u_j0z_xtb.json) |
| `A` | 公伯 | [《史記・秦本紀》][627] | [JSON](r9u_j0z_xtb_A.json) |
| `AA` | 秦仲 | [《史記・秦本紀》][627] | [JSON](r9u_j0z_xtb_AA.json) |
| `AAA` | 秦莊公 | [《史記・秦本紀》][627] | [JSON](r9u_j0z_xtb_AAA.json) |
| `AAAA` | 世父 | [《史記・秦本紀》][627] | [JSON](r9u_j0z_xtb_AAAA.json) |

</details>

<details><summary><code>ra9_o4d_rli</code> 竇長君（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 竇長君 | [《史記・外戚世家》][653]、[《史記・季布欒布列傳》][704] | [JSON](ra9_o4d_rli.json) |
| `A` | 彭祖 | [《史記・外戚世家》][653] | [JSON](ra9_o4d_rli_A.json) |

</details>

<details><summary><code>rdo_wsn_30x</code> 東樓公（杞君）（8 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 東樓公（杞君） | [《史記・陳杞世家》][640] | [JSON](rdo_wsn_30x.json) |
| `A` | 西樓公（杞君） | [《史記・陳杞世家》][640] | [JSON](rdo_wsn_30x_A.json) |
| `AA` | 題公（杞君） | [《史記・陳杞世家》][640] | [JSON](rdo_wsn_30x_AA.json) |
| `AAA` | 謀娶公（杞君） | [《史記・陳杞世家》][640] | [JSON](rdo_wsn_30x_AAA.json) |
| `AAAA` | 武公（杞君） | [《史記・陳杞世家》][640] | [JSON](rdo_wsn_30x_AAAA.json) |
| `AAAAA` | 靖公（杞君） | [《史記・陳杞世家》][640] | [JSON](rdo_wsn_30x_AAAAA.json) |
| `AAAAAA` | 共公（杞君） | [《史記・陳杞世家》][640] | [JSON](rdo_wsn_30x_AAAAAA.json) |
| `AAAAAAA` | 德公（杞君） | [《史記・陳杞世家》][640] | [JSON](rdo_wsn_30x_AAAAAAA.json) |

</details>

<details><summary><code>rex_cs0_mfo</code> 鮑革（宋文公）（12 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 鮑革（宋文公） | [《史記・宋微子世家》][642] | [JSON](rex_cs0_mfo.json) |
| `A` | 瑕（宋共公） | [《史記・宋微子世家》][642] | [JSON](rex_cs0_mfo_A.json) |
| `AA` | 戌（本版宋平公） | [《史記・宋微子世家》][642] | [JSON](rex_cs0_mfo_AA.json) |
| `AAA` | 佐（宋元公） | [《史記・宋微子世家》][642] | [JSON](rex_cs0_mfo_AAA.json) |
| `AAAA` | 頭曼（宋景公） | [《史記・宋微子世家》][642] | [JSON](rex_cs0_mfo_AAAA.json) |
| `AAAB` | 褍秦（宋元公少子） | [《史記・宋微子世家》][642] | [JSON](rex_cs0_mfo_AAAB.json) |
| `AAABA` | 糾（宋公孫） | [《史記・宋微子世家》][642] | [JSON](rex_cs0_mfo_AAABA.json) |
| `AAABAA` | 特（後宋昭公） | [《史記・宋微子世家》][642] | [JSON](rex_cs0_mfo_AAABAA.json) |
| `AAABAAA` | 購由（宋悼公） | [《史記・宋微子世家》][642] | [JSON](rex_cs0_mfo_AAABAAA.json) |
| `AAABAAAA` | 田（宋休公） | [《史記・宋微子世家》][642] | [JSON](rex_cs0_mfo_AAABAAAA.json) |
| `AAABAAAAA` | 辟兵（宋辟公） | [《史記・宋微子世家》][642] | [JSON](rex_cs0_mfo_AAABAAAAA.json) |
| `AAABAAAAAA` | 剔成（宋君） | [《史記・宋微子世家》][642] | [JSON](rex_cs0_mfo_AAABAAAAAA.json) |

</details>

<details><summary><code>rl6_a40_3hj</code> 馮唐祖父未名（張釋之馮唐列傳候選）（4 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 馮唐祖父未名 | [《史記・張釋之馮唐列傳》][706] | [JSON](rl6_a40_3hj.json) |
| `A` | 馮唐父未名 | [《史記・張釋之馮唐列傳》][706] | [JSON](rl6_a40_3hj_A.json) |
| `AA` | 馮唐 | [《史記・張釋之馮唐列傳》][706] | [JSON](rl6_a40_3hj_AA.json) |
| `AAA` | 馮遂 | [《史記・張釋之馮唐列傳》][706] | [JSON](rl6_a40_3hj_AAA.json) |

</details>

<details><summary><code>rlk_lzd_86c</code> 澄〔王衍弟，荊州刺史〕（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 澄〔王衍弟，荊州刺史〕 | [《晉書・山濤 王戎 郭舒 樂廣》][150] | [JSON](rlk_lzd_86c.json) |
| `A` | 王詹〔王澄長子〕 | [《晉書・山濤 王戎 郭舒 樂廣》][150] | [JSON](rlk_lzd_86c_A.json) |
| `B` | 王徽〔王澄子，右軍司馬〕 | [《世說新語・言語》][743] | [JSON](rlk_lzd_86c_B.json) |

</details>

<details><summary><code>rlv_clg_euu</code> 丕鄭（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 丕鄭 | [《史記・晉世家》][643] | [JSON](rlv_clg_euu.json) |
| `A` | 丕豹 | [《史記・秦本紀》][627] | [JSON](rlv_clg_euu_A.json) |

</details>

<details><summary><code>rr8_o9c_jc1</code> 負芻（曹成公）（4 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 負芻（曹成公） | [《史記・管蔡世家》][639] | [JSON](rr8_o9c_jc1.json) |
| `A` | 勝（曹武公） | [《史記・管蔡世家》][639] | [JSON](rr8_o9c_jc1_A.json) |
| `AA` | 平公（曹武公子） | [《史記・管蔡世家》][639] | [JSON](rr8_o9c_jc1_AA.json) |
| `AAA` | 午（曹悼公） | [《史記・管蔡世家》][639] | [JSON](rr8_o9c_jc1_AAA.json) |

</details>

<details><summary><code>rtd_v0b_nyn</code> 蕭綱（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 蕭綱 | [《梁書・文學下》][311]、[《梁書・文學下》][310]、[《南史・謝晦　謝裕　謝方明　謝靈運》][480]、[《南史・王曇首》][504]、[《南史・王曇首》][518]、[《南史・王曇首》][517] | [JSON](rtd_v0b_nyn.json) |
| `A` | 蕭大器（宣城王，哀太子） | [《梁書・昭明太子 哀太子 愍懷太子》][273] | [JSON](rtd_v0b_nyn_A.json) |
| `B` | 梁余姚公主（王溥妻） | [《南史・王誕　王華　王惠　王彧》][524]、[《文獻通考・卷二百五十八》][944] | [JSON](rtd_v0b_nyn_B.json) |

</details>

<details><summary><code>s11_z5r_y2z</code> 東方朔（滑稽列傳候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 東方朔 | [《史記・滑稽列傳》][730] | [JSON](s11_z5r_y2z.json) |
| `A` | 東方朔子（未名） | [《史記・滑稽列傳》][730] | [JSON](s11_z5r_y2z_A.json) |

</details>

<details><summary><code>sj9_pfu_fwh</code> 灌嬰（4 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 灌嬰 | [《史記・樊酈滕灌列傳》][699] | [JSON](sj9_pfu_fwh.json) |
| `*A` | 灌賢 | [《史記・魏其武安列傳》][711] | [JSON](sj9_pfu_fwh_%2AA.json) |
| `A` | 灌阿 | [《史記・樊酈滕灌列傳》][699] | [JSON](sj9_pfu_fwh_A.json) |
| `AA` | 灌彊 | [《史記・樊酈滕灌列傳》][699] | [JSON](sj9_pfu_fwh_AA.json) |

</details>

<details><summary><code>sjw_4mo_dlf</code> 徐生（儒林列傳候選）（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 徐生 | [《史記・儒林列傳》][725] | [JSON](sjw_4mo_dlf.json) |
| `*A` | 徐延 | [《史記・儒林列傳》][725] | [JSON](sjw_4mo_dlf_%2AA.json) |
| `*B` | 徐襄 | [《史記・儒林列傳》][725] | [JSON](sjw_4mo_dlf_%2AB.json) |

</details>

<details><summary><code>sm1_jfi_7k2</code> 王獻之（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 王獻之 | [《晉書・王羲之》][221] | [JSON](sm1_jfi_7k2.json) |
| `A` | 王神愛 | [《晉書・安帝 恭帝》][120]、[《晉書・后妃下》][133]、[《太平御覽・皇親部十五》][912] | [JSON](sm1_jfi_7k2_A.json) |

</details>

<details><summary><code>spx_gk1_rrr</code> 徐湛之（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 徐湛之 | [《南史・王曇首》][510]、[《宋書・徐湛之 江湛 王僧綽》][866]、[《宋書・徐湛之 江湛 王僧綽》][864]、[《宋書・徐湛之 江湛 王僧綽》][865] | [JSON](spx_gk1_rrr.json) |
| `A` | 徐湛之女（隨王誕妃，未名） | [《宋書・徐湛之 江湛 王僧綽》][866] | [JSON](spx_gk1_rrr_A.json) |

</details>

<details><summary><code>sqi_qy6_6bu</code> 杜靈啓（杜崱祖）（5 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 杜靈啓（杜崱祖） | [《梁書・胡僧祐 徐文盛 杜崱 兄岸 弟幼安 兄子龕 陰子春》][305] | [JSON](sqi_qy6_6bu.json) |
| `A` | 杜懷寶（杜崱父） | [《梁書・胡僧祐 徐文盛 杜崱 兄岸 弟幼安 兄子龕 陰子春》][305] | [JSON](sqi_qy6_6bu_A.json) |
| `AA` | 杜崱（京兆杜陵） | [《梁書・胡僧祐 徐文盛 杜崱 兄岸 弟幼安 兄子龕 陰子春》][305] | [JSON](sqi_qy6_6bu_AA.json) |
| `AB` | 杜岑（杜崱兄） | [《梁書・胡僧祐 徐文盛 杜崱 兄岸 弟幼安 兄子龕 陰子春》][305] | [JSON](sqi_qy6_6bu_AB.json) |
| `ABA` | 杜龕（杜岑子，王僧辯婿） | [《南史・江子一　胡僧祐　徐文盛　陰子春　杜崱　王琳　張彪》][591] | [JSON](sqi_qy6_6bu_ABA.json) |

</details>

<details><summary><code>sy5_s6h_9ex</code> 鄭文公（重耳過國者）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 鄭文公（重耳過國者） | [《史記・鄭世家》][646] | [JSON](sy5_s6h_9ex.json) |
| `A` | 蘭 | [《史記・鄭世家》][646] | [JSON](sy5_s6h_9ex_A.json) |

</details>

<details><summary><code>t6q_oe6_hom</code> 伏生（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 伏生 | [《史記・儒林列傳》][725] | [JSON](t6q_oe6_hom.json) |
| `*A` | 伏生孫（未名） | [《史記・儒林列傳》][725] | [JSON](t6q_oe6_hom_%2AA.json) |

</details>

<details><summary><code>t7q_vt4_ktj</code> 山（齊獻公）（7 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 山（齊獻公） | [《史記・齊太公世家》][636] | [JSON](t7q_vt4_ktj.json) |
| `A` | 壽（齊武公） | [《史記・齊太公世家》][636] | [JSON](t7q_vt4_ktj_A.json) |
| `AA` | 無忌（齊厲公） | [《史記・齊太公世家》][636] | [JSON](t7q_vt4_ktj_AA.json) |
| `AAA` | 赤（齊文公） | [《史記・齊太公世家》][636] | [JSON](t7q_vt4_ktj_AAA.json) |
| `AAAA` | 脫（齊成公） | [《史記・齊太公世家》][636] | [JSON](t7q_vt4_ktj_AAAA.json) |
| `AAAAA` | 購（齊莊公） | [《史記・齊太公世家》][636] | [JSON](t7q_vt4_ktj_AAAAA.json) |
| `AAAAAA` | 祿甫（齊釐公） | [《史記・齊太公世家》][636] | [JSON](t7q_vt4_ktj_AAAAAA.json) |

</details>

<details><summary><code>tkc_9z3_91l</code> 朱建（酈生陸賈列傳候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 朱建 | [《史記・酈生陸賈列傳》][701] | [JSON](tkc_9z3_91l.json) |
| `A` | 朱建子未名 | [《史記・酈生陸賈列傳》][701] | [JSON](tkc_9z3_91l_A.json) |

</details>

<details><summary><code>twd_erg_kmz</code> 陶侃（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 陶侃 | [《晉書・溫嶠 郗鑒》][194] | [JSON](twd_erg_kmz.json) |
| `A` | 陶氏〔陶侃第十女、孟嘉妻〕 | — | [JSON](twd_erg_kmz_A.json) |

</details>

<details><summary><code>txj_z8z_5me</code> 肅侯（趙世家候選）（4 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 肅侯 | [《史記・趙世家》][647] | [JSON](txj_z8z_5me.json) |
| `A` | 趙武靈王 | [《史記・趙世家》][647] | [JSON](txj_z8z_5me_A.json) |
| `AA` | 公子章 | [《史記・趙世家》][647] | [JSON](txj_z8z_5me_AA.json) |
| `AB` | 何 | [《史記・趙世家》][647] | [JSON](txj_z8z_5me_AB.json) |

</details>

<details><summary><code>tz9_dhl_ifo</code> 樛樂（南越列傳候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 樛樂 | [《史記・南越列傳》][717] | [JSON](tz9_dhl_ifo.json) |
| `A` | 廣德 | [《史記・建元以來侯者年表》][986] | [JSON](tz9_dhl_ifo_A.json) |

</details>

<details><summary><code>u3k_51j_4ul</code> 薛廣（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 薛廣 | [《宋書・薛安都 沈文秀 崔道固》][891] | [JSON](u3k_51j_4ul.json) |
| `A` | 薛安都 | [《北史・崔光 崔亮》][6]、[《魏書・燕鳳 許謙 張衮 崔玄伯 鄧淵》][926] | [JSON](u3k_51j_4ul_A.json) |

</details>

<details><summary><code>u3z_kcn_2cf</code> 崔敬友（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 崔敬友 | [《崔混墓誌・節錄》][31] | [JSON](u3z_kcn_2cf.json) |
| `A` | 崔鵾 | [《北史・崔光 崔亮》][5]、[《崔鴻墓誌・節錄》][30]、[《魏書・崔光》][940] | [JSON](u3z_kcn_2cf_A.json) |
| `B` | 崔鷫 | [《崔鴻墓誌・節錄》][30] | [JSON](u3z_kcn_2cf_B.json) |

</details>

<details><summary><code>u61_ylg_6av</code> 石季龍（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 石季龍 | [《晉書・陳騫 裴秀》][136] | [JSON](u61_ylg_6av.json) |
| `A` | 石世 | [《晉書・孝宗穆帝 哀帝 廢帝海西公》][111] | [JSON](u61_ylg_6av_A.json) |

</details>

<details><summary><code>u87_cc1_7vm</code> 田儋（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 田儋 | [《史記・田儋列傳》][698] | [JSON](u87_cc1_7vm.json) |
| `A` | 田市 | [《史記・田儋列傳》][698] | [JSON](u87_cc1_7vm_A.json) |

</details>

<details><summary><code>u9s_w6j_8mc</code> 桓顥（42 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 桓顥 | [《晉書・桓彝》][208] | [JSON](u9s_w6j_8mc.json) |
| `A` | 桓彝 | [《晉書・桓彝》][208] | [JSON](u9s_w6j_8mc_A.json) |
| `AA` | 桓溫 | [《晉書・叛臣一》][249] | [JSON](u9s_w6j_8mc_AA.json) |
| `AAA` | 桓熙 | [《晉書・叛臣一》][249] | [JSON](u9s_w6j_8mc_AAA.json) |
| `AAB` | 桓濟 | [《晉書・叛臣一》][249] | [JSON](u9s_w6j_8mc_AAB.json) |
| `AABA` | 桓亮 | [《晉書・叛臣二》][253] | [JSON](u9s_w6j_8mc_AABA.json) |
| `AAC` | 桓歆 | [《晉書・叛臣二》][253] | [JSON](u9s_w6j_8mc_AAC.json) |
| `AAD` | 桓禕 | [《晉書・叛臣一》][249] | [JSON](u9s_w6j_8mc_AAD.json) |
| `AAE` | 桓偉 | [《晉書・叛臣二》][253] | [JSON](u9s_w6j_8mc_AAE.json) |
| `AAEA` | 桓浚 | [《晉書・叛臣二》][253] | [JSON](u9s_w6j_8mc_AAEA.json) |
| `AAEB` | 桓邈 | [《晉書・叛臣二》][253] | [JSON](u9s_w6j_8mc_AAEB.json) |
| `AAF` | 桓玄 | [《晉書・叛臣二》][253] | [JSON](u9s_w6j_8mc_AAF.json) |
| `AAFA` | 桓升 | [《晉書・叛臣二》][253] | [JSON](u9s_w6j_8mc_AAFA.json) |
| `AAG` | 桓氏（字伯子，桓溫第二女） | [《世說新語・方正》][756] | [JSON](u9s_w6j_8mc_AAG.json) |
| `AB` | 桓雲 | [《晉書・桓彝》][208] | [JSON](u9s_w6j_8mc_AB.json) |
| `AB*A` | 桓放之 | [《晉書・叛臣二》][253] | [JSON](u9s_w6j_8mc_AB%2AA.json) |
| `ABA` | 桓序 | [《晉書・桓彝》][208] | [JSON](u9s_w6j_8mc_ABA.json) |
| `AC` | 桓豁 | [《晉書・桓彝》][208] | [JSON](u9s_w6j_8mc_AC.json) |
| `ACA` | 桓石虔 | [《晉書・桓彝》][208] | [JSON](u9s_w6j_8mc_ACA.json) |
| `ACAA` | 桓誕 | [《晉書・桓彝》][208] | [JSON](u9s_w6j_8mc_ACAA.json) |
| `ACAB` | 桓洪 | [《晉書・桓彝》][208] | [JSON](u9s_w6j_8mc_ACAB.json) |
| `ACAC` | 桓振 | [《晉書・桓彝》][208] | [JSON](u9s_w6j_8mc_ACAC.json) |
| `ACB` | 桓石秀 | [《晉書・桓彝》][208] | [JSON](u9s_w6j_8mc_ACB.json) |
| `ACBA` | 桓稚玉 | [《晉書・桓彝》][208] | [JSON](u9s_w6j_8mc_ACBA.json) |
| `ACC` | 桓石民 | [《晉書・桓彝》][208] | [JSON](u9s_w6j_8mc_ACC.json) |
| `ACD` | 桓石生 | [《晉書・桓彝》][208] | [JSON](u9s_w6j_8mc_ACD.json) |
| `ACE` | 桓石綏 | [《晉書・桓彝》][208] | [JSON](u9s_w6j_8mc_ACE.json) |
| `ACF` | 桓石康 | [《晉書・叛臣二》][253] | [JSON](u9s_w6j_8mc_ACF.json) |
| `ACG` | 桓權 | [《晉書・叛臣二》][253] | [JSON](u9s_w6j_8mc_ACG.json) |
| `AD` | 桓秘 | [《晉書・桓彝》][208] | [JSON](u9s_w6j_8mc_AD.json) |
| `ADA` | 桓蔚 | [《晉書・叛臣二》][253] | [JSON](u9s_w6j_8mc_ADA.json) |
| `AE` | 桓沖 | [《晉書・桓彝》][208] | [JSON](u9s_w6j_8mc_AE.json) |
| `AEA` | 桓嗣 | [《晉書・桓彝》][208] | [JSON](u9s_w6j_8mc_AEA.json) |
| `AEAA` | 桓胤 | [《晉書・叛臣二》][253] | [JSON](u9s_w6j_8mc_AEAA.json) |
| `AEB` | 桓謙 | [《晉書・桓彝》][208] | [JSON](u9s_w6j_8mc_AEB.json) |
| `AEC` | 桓修 | [《晉書・桓彝》][208] | [JSON](u9s_w6j_8mc_AEC.json) |
| `AECA` | 桓修長女〔王琨妻〕 | — | [JSON](u9s_w6j_8mc_AECA.json) |
| `AECB` | 桓修小女〔庾敬度妻〕 | — | [JSON](u9s_w6j_8mc_AECB.json) |
| `AED` | 桓崇 | [《晉書・桓彝》][208] | [JSON](u9s_w6j_8mc_AED.json) |
| `AEE` | 桓弘 | [《晉書・桓彝》][208]、[《晉書・叛臣二》][253] | [JSON](u9s_w6j_8mc_AEE.json) |
| `AEF` | 桓羨 | [《晉書・桓彝》][208] | [JSON](u9s_w6j_8mc_AEF.json) |
| `AEG` | 桓怡 | [《晉書・桓彝》][208] | [JSON](u9s_w6j_8mc_AEG.json) |

</details>

<details><summary><code>uay_2h8_ps8</code> 師（陳悼太子）（4 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 師（陳悼太子） | [《史記・陳杞世家》][640] | [JSON](uay_2h8_ps8.json) |
| `A` | 吳（陳惠公） | [《史記・陳杞世家》][640] | [JSON](uay_2h8_ps8_A.json) |
| `AA` | 柳（陳懷公） | [《史記・陳杞世家》][640] | [JSON](uay_2h8_ps8_AA.json) |
| `AAA` | 越（陳湣公） | [《史記・陳杞世家》][640] | [JSON](uay_2h8_ps8_AAA.json) |

</details>

<details><summary><code>uei_vr9_n3j</code> 竇長君（絳侯周勃世家候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 竇長君 | [《史記・絳侯周勃世家》][661] | [JSON](uei_vr9_n3j.json) |
| `A` | 彭祖 | [《史記・絳侯周勃世家》][661] | [JSON](uei_vr9_n3j_A.json) |

</details>

<details><summary><code>ufr_eoj_xit</code> 石奢父（未名）（循吏列傳候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 石奢父（未名） | [《史記・循吏列傳》][723] | [JSON](ufr_eoj_xit.json) |
| `A` | 石奢 | [《史記・循吏列傳》][723] | [JSON](ufr_eoj_xit_A.json) |

</details>

<details><summary><code>uij_ufp_1a6</code> 賈弼之（南史作弼）（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 賈弼之（南史作弼） | [《南齊書・文學》][414] | [JSON](uij_ufp_1a6.json) |
| `A` | 賈匪之（譜家，賈弼之子） | [《南史・江淹　任昉　王僧孺》][589] | [JSON](uij_ufp_1a6_A.json) |
| `AA` | 賈淵（字希鏡，南史作深） | [《南齊書・文學》][414] | [JSON](uij_ufp_1a6_AA.json) |

</details>

<details><summary><code>uj9_x5q_yir</code> 宋義（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 宋義 | [《史記・項羽本紀》][629] | [JSON](uj9_x5q_yir.json) |
| `A` | 宋襄 | [《史記・項羽本紀》][629] | [JSON](uj9_x5q_yir_A.json) |

</details>

<details><summary><code>us5_6hk_3qm</code> 屠者（留侯世家候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 屠者 | [《史記・留侯世家》][659] | [JSON](us5_6hk_3qm.json) |
| `A` | 秦嶢下軍將 | [《史記・留侯世家》][659] | [JSON](us5_6hk_3qm_A.json) |

</details>

<details><summary><code>uud_qa6_4u1</code> 郁（杞平公）（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 郁（杞平公） | [《史記・陳杞世家》][640] | [JSON](uud_qa6_4u1.json) |
| `A` | 成（杞悼公） | [《史記・陳杞世家》][640] | [JSON](uud_qa6_4u1_A.json) |
| `AA` | 乞（杞隱公） | [《史記・陳杞世家》][640] | [JSON](uud_qa6_4u1_AA.json) |

</details>

<details><summary><code>v0t_lw5_yr1</code> 李敏〔漢河內太守〕（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 李敏〔漢河內太守〕 | [《晉書・鄭袤 李胤 盧欽 華表 石鑒 溫羨》][160] | [JSON](v0t_lw5_yr1.json) |
| `A` | 李信〔李胤父〕 | [《晉書・鄭袤 李胤 盧欽 華表 石鑒 溫羨》][160] | [JSON](v0t_lw5_yr1_A.json) |

</details>

<details><summary><code>vcm_d77_tsz</code> 昌〔祖沖之祖〕（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 昌〔祖沖之祖〕 | [《南齊書・文學》][416] | [JSON](vcm_d77_tsz.json) |
| `A` | 朔之〔祖沖之父〕 | [《南齊書・文學》][416] | [JSON](vcm_d77_tsz_A.json) |
| `AA` | 祖沖之 | [《南齊書・文學》][416] | [JSON](vcm_d77_tsz_AA.json) |

</details>

<details><summary><code>vfh_ufx_cdv</code> 張慶之（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 張慶之 | [《崔鴻墓誌・節錄》][30]、[《崔混墓誌・節錄》][31] | [JSON](vfh_ufx_cdv.json) |
| `A` | 張氏（崔鴻妻） | [《崔混墓誌・節錄》][31] | [JSON](vfh_ufx_cdv_A.json) |

</details>

<details><summary><code>vgg_tso_418</code> 月氏王（被殺）（大宛列傳候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 月氏王（被殺） | [《史記・大宛列傳》][727] | [JSON](vgg_tso_418.json) |
| `A` | 月氏太子（繼王） | [《史記・大宛列傳》][727] | [JSON](vgg_tso_418_A.json) |

</details>

<details><summary><code>vhf_729_g6z</code> 王誕〔張邵早年府主〕（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 王誕〔張邵早年府主〕 | [《宋書・庾悅 王誕 謝景仁 袁湛 褚叔度》][837] | [JSON](vhf_729_g6z.json) |
| `A` | 王詡（王誕子） | [《南史・王誕　王華　王惠　王彧》][523]、[《南史・王誕　王華　王惠　王彧》][522]、[《宋書・庾悅 王誕 謝景仁 袁湛 褚叔度》][837] | [JSON](vhf_729_g6z_A.json) |

</details>

<details><summary><code>vhw_07a_wzm</code> 孔惔（淳之祖）（6 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 孔惔（淳之祖） | [《宋書・隱逸》][900] | [JSON](vhw_07a_wzm.json) |
| `A` | 孔粲（淳之父） | [《宋書・隱逸》][900] | [JSON](vhw_07a_wzm_A.json) |
| `AA` | 孔淳之 | [《宋書・隱逸》][900] | [JSON](vhw_07a_wzm_AA.json) |
| `AAA` | 孔尚 | [《宋書・隱逸》][900] | [JSON](vhw_07a_wzm_AAA.json) |
| `AB` | 孔默之 | [《宋書・隱逸》][900] | [JSON](vhw_07a_wzm_AB.json) |
| `ABA` | 孔熙先 | [《宋書・隱逸》][900] | [JSON](vhw_07a_wzm_ABA.json) |

</details>

<details><summary><code>vna_am7_jn5</code> 韋賢（張丞相列傳候選）（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 韋賢 | [《史記・張丞相列傳》][700] | [JSON](vna_am7_jn5.json) |
| `A` | 韋玄成 | [《史記・張丞相列傳》][700] | [JSON](vna_am7_jn5_A.json) |
| `B` | 韋賢長子未名 | [《史記・張丞相列傳》][700] | [JSON](vna_am7_jn5_B.json) |

</details>

<details><summary><code>vpy_180_2oi</code> 昧〔裴松之祖〕（7 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 昧〔裴松之祖〕 | [《南史・范泰　荀伯子　徐廣　鄭鮮之　裴松之　何承天》][572]、[《宋書・鄭鮮之 裴松之 何承天》][860] | [JSON](vpy_180_2oi.json) |
| `A` | 珪〔裴松之父〕 | [《南史・范泰　荀伯子　徐廣　鄭鮮之　裴松之　何承天》][572]、[《宋書・鄭鮮之 裴松之 何承天》][860] | [JSON](vpy_180_2oi_A.json) |
| `AA` | 裴松之 | [《南史・范泰　荀伯子　徐廣　鄭鮮之　裴松之　何承天》][572]、[《宋書・鄭鮮之 裴松之 何承天》][860] | [JSON](vpy_180_2oi_AA.json) |
| `AAA` | 駰〔裴松之子〕 | [《南史・范泰　荀伯子　徐廣　鄭鮮之　裴松之　何承天》][572] | [JSON](vpy_180_2oi_AAA.json) |
| `AAAA` | 昭明〔裴子野父〕 | [《南史・范泰　荀伯子　徐廣　鄭鮮之　裴松之　何承天》][572] | [JSON](vpy_180_2oi_AAAA.json) |
| `AAAAA` | 裴子野 | [《南史・范泰　荀伯子　徐廣　鄭鮮之　裴松之　何承天》][572] | [JSON](vpy_180_2oi_AAAAA.json) |
| `AAAAAA` | 謇〔子野子；南史作騫〕 | [《梁書・裴子野 顧協 徐摛 鮑泉》][297]、[《南史・范泰　荀伯子　徐廣　鄭鮮之　裴松之　何承天》][572] | [JSON](vpy_180_2oi_AAAAAA.json) |

</details>

<details><summary><code>vs4_n7e_1qh</code> 武（曹繆公）（8 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 武（曹繆公） | [《史記・管蔡世家》][639] | [JSON](vs4_n7e_1qh.json) |
| `A` | 終生（曹桓公） | [《史記・管蔡世家》][639] | [JSON](vs4_n7e_1qh_A.json) |
| `AA` | 夕姑（曹莊公） | [《史記・管蔡世家》][639] | [JSON](vs4_n7e_1qh_AA.json) |
| `AAA` | 夷（曹釐公） | [《史記・管蔡世家》][639] | [JSON](vs4_n7e_1qh_AAA.json) |
| `AAAA` | 班（曹昭公） | [《史記・管蔡世家》][639] | [JSON](vs4_n7e_1qh_AAAA.json) |
| `AAAAA` | 襄（曹共公） | [《史記・管蔡世家》][639] | [JSON](vs4_n7e_1qh_AAAAA.json) |
| `AAAAAA` | 壽（曹文公） | [《史記・管蔡世家》][639] | [JSON](vs4_n7e_1qh_AAAAAA.json) |
| `AAAAAAA` | 彊（曹宣公） | [《史記・管蔡世家》][639] | [JSON](vs4_n7e_1qh_AAAAAAA.json) |

</details>

<details><summary><code>vs9_1es_k35</code> 田氏（鄭阿春前夫）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 田氏（鄭阿春前夫） | [《晉書・后妃下》][134] | [JSON](vs9_1es_k35.json) |
| `A` | 鄭阿春前婚所生子（未名） | [《晉書・后妃下》][134] | [JSON](vs9_1es_k35_A.json) |

</details>

<details><summary><code>vtu_yuj_kdz</code> 齊王建（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 齊王建 | [《史記・秦始皇本紀》][628]、[《史記・田儋列傳》][698] | [JSON](vtu_yuj_kdz.json) |
| `*A` | 田安 | [《史記・項羽本紀》][629]、[《史記・田儋列傳》][698] | [JSON](vtu_yuj_kdz_%2AA.json) |

</details>

<details><summary><code>vty_3n0_0ed</code> 病疽卒父（孫吳列傳候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 病疽卒父 | [《史記・孫子吳起列傳》][669] | [JSON](vty_3n0_0ed.json) |
| `A` | 病疽卒 | [《史記・孫子吳起列傳》][669] | [JSON](vty_3n0_0ed_A.json) |

</details>

<details><summary><code>vwy_7cv_69j</code> 桓子（趙世家候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 桓子 | [《史記・趙世家》][647] | [JSON](vwy_7cv_69j.json) |
| `A` | 桓子之子（趙世家未名者） | [《史記・趙世家》][647] | [JSON](vwy_7cv_69j_A.json) |

</details>

<details><summary><code>w3a_mm0_hw1</code> 劉昶（平原劉懷珍祖）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 劉昶（平原劉懷珍祖） | [《南齊書・劉懷珍 李安民 王玄載》][345] | [JSON](w3a_mm0_hw1.json) |
| `*A` | 劉懷珍（字道玉） | [《南齊書・劉懷珍 李安民 王玄載》][345]、[《南齊書・劉懷珍 李安民 王玄載》][348]、[《南史・庾杲之　王諶　孔珪　劉懷珍》][585] | [JSON](w3a_mm0_hw1_%2AA.json) |

</details>

<details><summary><code>w44_37v_bcb</code> 和（宋穆公）（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 和（宋穆公） | [《史記・宋微子世家》][642] | [JSON](w44_37v_bcb.json) |
| `A` | 馮（宋莊公） | [《史記・宋微子世家》][642] | [JSON](w44_37v_bcb_A.json) |
| `AA` | 捷（宋湣公） | [《史記・宋微子世家》][642] | [JSON](w44_37v_bcb_AA.json) |

</details>

<details><summary><code>w4m_9tw_147</code> 齊明帝鸞（9 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 齊明帝鸞 | [《南齊書・江斆 何昌㝢 謝𤅢 王思遠》][385] | [JSON](w4m_9tw_147.json) |
| `A` | 蕭寶卷 | [《建康實錄・卷十五》][70] | [JSON](w4m_9tw_147_A.json) |
| `AA` | 蕭誦（齊東昏侯皇太子） | [《建康實錄・卷十五》][70]、[《建康實錄・卷十五》][71]、[《南齊書・皇后》][326]、[《南齊書・皇后》][325]、[《南史・廢帝鬱林王　廢帝海陵恭王　高宗明皇帝　廢帝東昏侯　和帝》][419]、[《南史・后妃上》][424]、[《南史・后妃上》][425]、[《資治通鑑・齊紀十》][974] | [JSON](w4m_9tw_147_AA.json) |
| `B` | 蕭寶玄 | [《南齊書・明帝》][318]、[《南齊書・王融 謝朓》][394]、[《南齊書・文二王 明七王》][413]、[《南史・謝晦　謝裕　謝方明　謝靈運》][479] | [JSON](w4m_9tw_147_B.json) |
| `C` | 蕭寶義 | [《南齊書・文二王 明七王》][413] | [JSON](w4m_9tw_147_C.json) |
| `D` | 蕭寶夤（字智亮） | [《魏書・楊播》][934] | [JSON](w4m_9tw_147_D.json) |
| `E` | 蕭寶源（字智淵） | [《南齊書・文二王 明七王》][412] | [JSON](w4m_9tw_147_E.json) |
| `F` | 齊和帝寶融（字智昭） | [《南齊書・和帝》][320]、[《南齊書・皇后》][338]、[《南齊書・皇后》][337]、[《南史・后妃上》][441]、[《南史・后妃上》][442] | [JSON](w4m_9tw_147_F.json) |
| `G` | 山陰公主（齊明帝長女） | [《南史・后妃上》][424]、[《南史・后妃上》][425] | [JSON](w4m_9tw_147_G.json) |

</details>

<details><summary><code>w8j_vnd_rs4</code> 傅寬（4 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 傅寬 | [《漢書・樊酈滕灌傅靳周傳》][53] | [JSON](w8j_vnd_rs4.json) |
| `A` | 傅精 | [《史記・傅靳蒯成列傳》][702]、[《史記・高祖功臣侯者年表》][984] | [JSON](w8j_vnd_rs4_A.json) |
| `AA` | 傅則 | [《史記・傅靳蒯成列傳》][702]、[《史記・高祖功臣侯者年表》][984] | [JSON](w8j_vnd_rs4_AA.json) |
| `AAA` | 傅偃 | [《史記・高祖功臣侯者年表》][984] | [JSON](w8j_vnd_rs4_AAA.json) |

</details>

<details><summary><code>wc5_hn7_a5w</code> 羊繇（車騎掾）（5 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 羊繇（車騎掾） | [《世說新語・方正》][755] | [JSON](wc5_hn7_a5w.json) |
| `A` | 羊忱（字長和） | [《世說新語・方正》][755] | [JSON](wc5_hn7_a5w_A.json) |
| `AA` | 羊權（黃門郎） | [《南史・羊欣　羊玄保　沈演之　江夷　江秉之》][574] | [JSON](wc5_hn7_a5w_AA.json) |
| `AAA` | 羊不疑（桂陽太守） | [《南史・羊欣　羊玄保　沈演之　江夷　江秉之》][574] | [JSON](wc5_hn7_a5w_AAA.json) |
| `AAAA` | 羊徽（字敬猷） | [《南史・羊欣　羊玄保　沈演之　江夷　江秉之》][574] | [JSON](wc5_hn7_a5w_AAAA.json) |

</details>

<details><summary><code>wjt_htu_081</code> 頭曼（匈奴列傳）（13 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 頭曼（匈奴列傳） | [《史記・匈奴列傳》][714] | [JSON](wjt_htu_081.json) |
| `A` | 冒頓（匈奴列傳第6段） | [《史記・匈奴列傳》][714] | [JSON](wjt_htu_081_A.json) |
| `AA` | 稽粥（匈奴列傳第18至20段） | [《史記・匈奴列傳》][714] | [JSON](wjt_htu_081_AA.json) |
| `AAA` | 軍臣（匈奴列傳第27段） | [《史記・匈奴列傳》][714] | [JSON](wjt_htu_081_AAA.json) |
| `AAAA` | 於單（匈奴列傳第31至32段） | [《史記・匈奴列傳》][714] | [JSON](wjt_htu_081_AAAA.json) |
| `AAB` | 伊稚斜（匈奴列傳第31至32段） | [《史記・衛將軍驃騎列傳》][715] | [JSON](wjt_htu_081_AAB.json) |
| `AABA` | 烏維（匈奴列傳第42至43段） | [《史記・匈奴列傳》][714] | [JSON](wjt_htu_081_AABA.json) |
| `AABAA` | 烏師廬（匈奴列傳第49段） | [《史記・匈奴列傳》][714] | [JSON](wjt_htu_081_AABAA.json) |
| `AABAAA` | 兒單于之子（未名） | [《史記・匈奴列傳》][714] | [JSON](wjt_htu_081_AABAAA.json) |
| `AABB` | 呴犁湖（匈奴列傳第53段） | [《史記・匈奴列傳》][714] | [JSON](wjt_htu_081_AABB.json) |
| `AABC` | 且鞮侯（匈奴列傳第56段） | [《史記・匈奴列傳》][714] | [JSON](wjt_htu_081_AABC.json) |
| `AABCA` | 且鞮侯之女（未名，妻李陵者） | [《史記・李將軍列傳》][713]、[《史記・匈奴列傳》][714] | [JSON](wjt_htu_081_AABCA.json) |
| `B` | 少子（匈奴列傳第6段） | [《史記・匈奴列傳》][714] | [JSON](wjt_htu_081_B.json) |

</details>

<details><summary><code>wtu_qvi_0rz</code> 李矩（李充父）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 李矩（李充父） | [《晉書・文苑》][231] | [JSON](wtu_qvi_0rz.json) |
| `A` | 李充 | [《晉書・文苑》][231] | [JSON](wtu_qvi_0rz_A.json) |

</details>

<details><summary><code>wuz_yxe_b9k</code> 齊景公（4 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 齊景公 | [《史記・齊太公世家》][636] | [JSON](wuz_yxe_b9k.json) |
| `A` | 齊悼公 | [《史記・齊太公世家》][636] | [JSON](wuz_yxe_b9k_A.json) |
| `AA` | 齊簡公 | [《史記・齊太公世家》][636] | [JSON](wuz_yxe_b9k_AA.json) |
| `B` | 孺子（齊） | [《史記・齊太公世家》][636] | [JSON](wuz_yxe_b9k_B.json) |

</details>

<details><summary><code>x18_cng_88g</code> 鄭默〔郭奕傳中庶子〕（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 鄭默〔郭奕傳中庶子〕 | [《晉書・鄭袤 李胤 盧欽 華表 石鑒 溫羨》][170] | [JSON](x18_cng_88g.json) |
| `A` | 鄭球〔字子瑜〕 | [《晉書・鄭袤 李胤 盧欽 華表 石鑒 溫羨》][171] | [JSON](x18_cng_88g_A.json) |
| `B` | 鄭豫〔鄭默子〕 | [《晉書・鄭袤 李胤 盧欽 華表 石鑒 溫羨》][170]、[《晉書・鄭袤 李胤 盧欽 華表 石鑒 溫羨》][171]、[《三國志・任蘇杜鄭倉傳》][607] | [JSON](x18_cng_88g_B.json) |

</details>

<details><summary><code>x3q_cqm_dup</code> 竟陵王子良（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 竟陵王子良 | [《南史・王弘》][491] | [JSON](x3q_cqm_dup.json) |
| `A` | 蕭昭胄 | [《南史・袁湛》][565] | [JSON](x3q_cqm_dup_A.json) |

</details>

<details><summary><code>x50_1p7_qkk</code> 魯莊公（10 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 魯莊公 | [《史記・魯周公世家》][637] | [JSON](x50_1p7_qkk.json) |
| `A` | 魯湣公 | [《史記・魯周公世家》][637] | [JSON](x50_1p7_qkk_A.json) |
| `B` | 魯釐公 | [《史記・魯周公世家》][637] | [JSON](x50_1p7_qkk_B.json) |
| `BA` | 興（魯文公） | [《史記・魯周公世家》][637] | [JSON](x50_1p7_qkk_BA.json) |
| `BAA` | 惡（文公子） | [《史記・魯周公世家》][637] | [JSON](x50_1p7_qkk_BAA.json) |
| `BAB` | 視（文公子） | [《史記・魯周公世家》][637] | [JSON](x50_1p7_qkk_BAB.json) |
| `BAC` | 俀（魯宣公） | [《史記・魯周公世家》][637] | [JSON](x50_1p7_qkk_BAC.json) |
| `BACA` | 黑肱（魯成公） | [《史記・魯周公世家》][637] | [JSON](x50_1p7_qkk_BACA.json) |
| `BACAA` | 午（魯襄公） | [《史記・魯周公世家》][637] | [JSON](x50_1p7_qkk_BACAA.json) |
| `C` | 斑（莊公子） | [《史記・魯周公世家》][637] | [JSON](x50_1p7_qkk_C.json) |

</details>

<details><summary><code>x90_vgz_2uf</code> 王翹之（晉光祿大夫）（5 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 王翹之（晉光祿大夫） | [《南史・王裕之　王鎮之　王韶之　王悅之　王准之》][555]、[《宋書・隱逸》][897] | [JSON](x90_vgz_2uf.json) |
| `A` | 王望之（王素曾祖） | [《南史・王裕之　王鎮之　王韶之　王悅之　王准之》][555] | [JSON](x90_vgz_2uf_A.json) |
| `AA` | 王泰之（王素祖） | [《南史・王裕之　王鎮之　王韶之　王悅之　王准之》][555] | [JSON](x90_vgz_2uf_AA.json) |
| `AAA` | 王元弘（平固令） | [《南史・王裕之　王鎮之　王韶之　王悅之　王准之》][555] | [JSON](x90_vgz_2uf_AAA.json) |
| `AAAA` | 王素（字休業） | [《宋書・隱逸》][897] | [JSON](x90_vgz_2uf_AAAA.json) |

</details>

<details><summary><code>xaa_ewn_4ro</code> 臧荼（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 臧荼 | [《史記・樊酈滕灌列傳》][699] | [JSON](xaa_ewn_4ro.json) |
| `A` | 衍（臧荼子） | [《史記・韓信盧綰列傳》][697] | [JSON](xaa_ewn_4ro_A.json) |

</details>

<details><summary><code>xd8_uww_5ok</code> 蕭何（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 蕭何 | [《史記・蕭相國世家》][657] | [JSON](xd8_uww_5ok.json) |
| `*A` | 系（蕭何孫） | [《史記・孝景本紀》][633] | [JSON](xd8_uww_5ok_%2AA.json) |

</details>

<details><summary><code>xgd_r31_cmr</code> 崔杼（4 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 崔杼 | [《史記・齊太公世家》][636] | [JSON](xgd_r31_cmr.json) |
| `A` | 成（崔杼子） | [《史記・齊太公世家》][636] | [JSON](xgd_r31_cmr_A.json) |
| `B` | 彊（崔杼子） | [《史記・齊太公世家》][636] | [JSON](xgd_r31_cmr_B.json) |
| `C` | 明（崔杼子） | [《史記・齊太公世家》][636] | [JSON](xgd_r31_cmr_C.json) |

</details>

<details><summary><code>xgx_g4a_c28</code> 趙兼（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 趙兼 | [《史記・孝文本紀》][632]、[《史記・淮南衡山列傳》][722]、[《史記・酷吏列傳》][726]、[《史記・惠景間侯者年表》][985] | [JSON](xgx_g4a_c28.json) |
| `A` | 周陽由 | [《史記・酷吏列傳》][726] | [JSON](xgx_g4a_c28_A.json) |

</details>

<details><summary><code>xke_dj3_6ba</code> 褚䂮（13 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 褚䂮 | [《晉書・王沈 荀顗 荀勖 馮紞》][141]、[《晉書・外戚》][232] | [JSON](xke_dj3_6ba.json) |
| `A` | 褚洽 | [《晉書・外戚》][232] | [JSON](xke_dj3_6ba_A.json) |
| `AA` | 褚裒 | [《晉書・外戚》][232] | [JSON](xke_dj3_6ba_AA.json) |
| `AAA` | 褚歆 | [《晉書・外戚》][232] | [JSON](xke_dj3_6ba_AAA.json) |
| `AAAA` | 褚爽 | [《晉書・外戚》][233] | [JSON](xke_dj3_6ba_AAAA.json) |
| `AAAAA` | 褚秀之 | [《晉書・外戚》][233]、[《南齊書・褚淵 淵弟澄 徐嗣 王儉》][341]、[《南史・褚裕之》][568]、[《宋書・庾悅 王誕 謝景仁 袁湛 褚叔度》][835]、[《宋書・庾悅 王誕 謝景仁 袁湛 褚叔度》][836] | [JSON](xke_dj3_6ba_AAAAA.json) |
| `AAAAB` | 褚炎之 | [《晉書・外戚》][233] | [JSON](xke_dj3_6ba_AAAAB.json) |
| `AAAAC` | 褚喻之 | [《南史・褚裕之》][567]、[《宋書・庾悅 王誕 謝景仁 袁湛 褚叔度》][834] | [JSON](xke_dj3_6ba_AAAAC.json) |
| `AAAACA` | 褚寂之（褚叔度第二子） | [《南史・褚裕之》][567]、[《宋書・庾悅 王誕 謝景仁 袁湛 褚叔度》][834] | [JSON](xke_dj3_6ba_AAAACA.json) |
| `AAAACAA` | 褚曖（褚寂之子） | [《南史・王誕　王華　王惠　王彧》][545]、[《南史・褚裕之》][567]、[《宋書・庾悅 王誕 謝景仁 袁湛 褚叔度》][834] | [JSON](xke_dj3_6ba_AAAACAA.json) |
| `AAAAD` | 褚靈媛 | [《晉書・后妃下》][128] | [JSON](xke_dj3_6ba_AAAAD.json) |
| `AAAAE` | 褚淡之（字仲源） | [《宋書・庾悅 王誕 謝景仁 袁湛 褚叔度》][836] | [JSON](xke_dj3_6ba_AAAAE.json) |
| `AAB` | 褚蒜子 | [《晉書・后妃下》][129] | [JSON](xke_dj3_6ba_AAB.json) |

</details>

<details><summary><code>xny_prn_zyi</code> 酈商（6 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 酈商 | [《史記・樊酈滕灌列傳》][699] | [JSON](xny_prn_zyi.json) |
| `A` | 酈寄 | [《史記・樊酈滕灌列傳》][699] | [JSON](xny_prn_zyi_A.json) |
| `B` | 酈堅 | [《史記・樊酈滕灌列傳》][699] | [JSON](xny_prn_zyi_B.json) |
| `BA` | 酈遂成 | [《史記・樊酈滕灌列傳》][699] | [JSON](xny_prn_zyi_BA.json) |
| `BAA` | 酈世宗 | [《史記・樊酈滕灌列傳》][699] | [JSON](xny_prn_zyi_BAA.json) |
| `BAAA` | 酈終根 | [《史記・樊酈滕灌列傳》][699] | [JSON](xny_prn_zyi_BAAA.json) |

</details>

<details><summary><code>xrt_zof_cbt</code> 和（衛武公）（4 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 和（衛武公） | [《史記・衛康叔世家》][641] | [JSON](xrt_zof_cbt.json) |
| `A` | 揚（衛莊公） | [《史記・衛康叔世家》][641] | [JSON](xrt_zof_cbt_A.json) |
| `AA` | 州吁（衛君） | [《史記・衛康叔世家》][641] | [JSON](xrt_zof_cbt_AA.json) |
| `AB` | 完（衛桓公） | [《史記・衛康叔世家》][641] | [JSON](xrt_zof_cbt_AB.json) |

</details>

<details><summary><code>xxh_xtr_3f9</code> 袁豹（5 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 袁豹 | [《宋書・庾悅 王誕 謝景仁 袁湛 褚叔度》][841] | [JSON](xxh_xtr_3f9.json) |
| `A` | 袁洵 | [《南齊書・袁彖 孔稚珪 劉繪》][395]、[《宋書・庾悅 王誕 謝景仁 袁湛 褚叔度》][841] | [JSON](xxh_xtr_3f9_A.json) |
| `AA` | 袁顗 | [《南史・王誕　王華　王惠　王彧》][543]、[《南史・袁湛》][565]、[《宋書・庾悅 王誕 謝景仁 袁湛 褚叔度》][841] | [JSON](xxh_xtr_3f9_AA.json) |
| `AB` | 袁覬 | [《南齊書・袁彖 孔稚珪 劉繪》][395]、[《南史・袁湛》][565]、[《宋書・庾悅 王誕 謝景仁 袁湛 褚叔度》][841] | [JSON](xxh_xtr_3f9_AB.json) |
| `ABA` | 袁氏（竟陵王子良妃） | [《南齊書・皇后》][332]、[《南齊書・武十七王》][377]、[《南史・后妃上》][434] | [JSON](xxh_xtr_3f9_ABA.json) |

</details>

<details><summary><code>y0c_hok_598</code> 李同父未名（平原君虞卿列傳候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 李同父未名 | [《史記・平原君虞卿列傳》][680] | [JSON](y0c_hok_598.json) |
| `A` | 李同 | [《史記・平原君虞卿列傳》][680] | [JSON](y0c_hok_598_A.json) |

</details>

<details><summary><code>y3i_rsz_brn</code> 韓厥（14 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 韓厥 | [《史記・韓世家》][649] | [JSON](y3i_rsz_brn.json) |
| `A` | 韓宣子 | [《史記・韓世家》][649] | [JSON](y3i_rsz_brn_A.json) |
| `AA` | 韓貞子 | [《史記・韓世家》][649] | [JSON](y3i_rsz_brn_AA.json) |
| `AAA` | 韓簡子 | [《史記・韓世家》][649] | [JSON](y3i_rsz_brn_AAA.json) |
| `AAAA` | 韓莊子 | [《史記・韓世家》][649] | [JSON](y3i_rsz_brn_AAAA.json) |
| `AAAAA` | 韓康子 | [《史記・韓世家》][649] | [JSON](y3i_rsz_brn_AAAAA.json) |
| `AAAAAA` | 武子 | [《史記・韓世家》][649] | [JSON](y3i_rsz_brn_AAAAAA.json) |
| `AAAAAAA` | 虔 | [《史記・韓世家》][649] | [JSON](y3i_rsz_brn_AAAAAAA.json) |
| `AAAAAAAA` | 取 | [《史記・韓世家》][649] | [JSON](y3i_rsz_brn_AAAAAAAA.json) |
| `AAAAAAAAA` | 韓文侯 | [《史記・韓世家》][649] | [JSON](y3i_rsz_brn_AAAAAAAAA.json) |
| `AAAAAAAAAA` | 韓哀侯 | [《史記・韓世家》][649] | [JSON](y3i_rsz_brn_AAAAAAAAAA.json) |
| `AAAAAAAAAAA` | 韓懿侯 | [《史記・韓世家》][649] | [JSON](y3i_rsz_brn_AAAAAAAAAAA.json) |
| `AAAAAAAAAAAA` | 韓昭侯 | [《史記・韓世家》][649] | [JSON](y3i_rsz_brn_AAAAAAAAAAAA.json) |
| `AAAAAAAAAAAAA` | 宣惠王 | [《史記・韓世家》][649] | [JSON](y3i_rsz_brn_AAAAAAAAAAAAA.json) |

</details>

<details><summary><code>y3u_i0l_ztj</code> 韓宣王（趙世家候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 韓宣王 | [《史記・趙世家》][647] | [JSON](y3u_i0l_ztj.json) |
| `A` | 倉 | [《史記・趙世家》][647] | [JSON](y3u_i0l_ztj_A.json) |

</details>

<details><summary><code>y4i_pjk_4gn</code> 季歷（47 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 季歷 | [《史記・周本紀》][626] | [JSON](y4i_pjk_4gn.json) |
| `A` | 西伯昌 | [《史記・周本紀》][626] | [JSON](y4i_pjk_4gn_A.json) |
| `AA` | 周武王 | [《史記・周本紀》][626] | [JSON](y4i_pjk_4gn_AA.json) |
| `AAA` | 晉唐叔 | [《史記・晉世家》][643] | [JSON](y4i_pjk_4gn_AAA.json) |
| `AAAA` | 燮（晉侯） | [《史記・晉世家》][643] | [JSON](y4i_pjk_4gn_AAAA.json) |
| `AAAAA` | 寧族（晉武侯） | [《史記・晉世家》][643] | [JSON](y4i_pjk_4gn_AAAAA.json) |
| `AAAAAA` | 服人（晉成侯） | [《史記・晉世家》][643] | [JSON](y4i_pjk_4gn_AAAAAA.json) |
| `AAAAAAA` | 福（晉厲侯） | [《史記・晉世家》][643] | [JSON](y4i_pjk_4gn_AAAAAAA.json) |
| `AAAAAAAA` | 宜臼（晉靖侯） | [《史記・晉世家》][643] | [JSON](y4i_pjk_4gn_AAAAAAAA.json) |
| `AAAAAAAA*A` | 欒賓（靖侯庶孫） | [《史記・晉世家》][643] | [JSON](y4i_pjk_4gn_AAAAAAAA%2AA.json) |
| `AB` | 管叔 | [《史記・管蔡世家》][639] | [JSON](y4i_pjk_4gn_AB.json) |
| `AC` | 蔡叔 | [《史記・管蔡世家》][639] | [JSON](y4i_pjk_4gn_AC.json) |
| `ACA` | 胡（蔡仲） | [《史記・管蔡世家》][639] | [JSON](y4i_pjk_4gn_ACA.json) |
| `ACAA` | 荒（蔡伯） | [《史記・管蔡世家》][639] | [JSON](y4i_pjk_4gn_ACAA.json) |
| `ACAAA` | 宮侯（蔡君） | [《史記・管蔡世家》][639] | [JSON](y4i_pjk_4gn_ACAAA.json) |
| `ACAAAA` | 厲侯（蔡君） | [《史記・管蔡世家》][639] | [JSON](y4i_pjk_4gn_ACAAAA.json) |
| `ACAAAAA` | 武侯（蔡君） | [《史記・管蔡世家》][639] | [JSON](y4i_pjk_4gn_ACAAAAA.json) |
| `ACAAAAAA` | 夷侯（蔡君） | [《史記・管蔡世家》][639] | [JSON](y4i_pjk_4gn_ACAAAAAA.json) |
| `ACAAAAAAA` | 所事（蔡釐侯） | [《史記・管蔡世家》][639] | [JSON](y4i_pjk_4gn_ACAAAAAAA.json) |
| `ACAAAAAAAA` | 興（蔡共侯） | [《史記・管蔡世家》][639] | [JSON](y4i_pjk_4gn_ACAAAAAAAA.json) |
| `ACAAAAAAAAA` | 戴侯（蔡君） | [《史記・管蔡世家》][639] | [JSON](y4i_pjk_4gn_ACAAAAAAAAA.json) |
| `ACAAAAAAAAAA` | 措父（蔡宣侯） | [《史記・管蔡世家》][639] | [JSON](y4i_pjk_4gn_ACAAAAAAAAAA.json) |
| `ACAAAAAAAAAAA` | 封人（蔡桓侯） | [《史記・管蔡世家》][639] | [JSON](y4i_pjk_4gn_ACAAAAAAAAAAA.json) |
| `AD` | 周公 | [《史記・魯周公世家》][637] | [JSON](y4i_pjk_4gn_AD.json) |
| `ADA` | 伯禽 | [《史記・魯周公世家》][637] | [JSON](y4i_pjk_4gn_ADA.json) |
| `ADAA` | 酋（魯考公） | [《史記・魯周公世家》][637]、[《史記・三代世表》][979] | [JSON](y4i_pjk_4gn_ADAA.json) |
| `AE` | 衛康叔封 | [《史記・衛康叔世家》][641] | [JSON](y4i_pjk_4gn_AE.json) |
| `AEA` | 康伯（衛康叔子） | [《史記・衛康叔世家》][641] | [JSON](y4i_pjk_4gn_AEA.json) |
| `AEAA` | 考伯（衛君） | [《史記・衛康叔世家》][641] | [JSON](y4i_pjk_4gn_AEAA.json) |
| `AEAAA` | 嗣伯（衛君） | [《史記・衛康叔世家》][641] | [JSON](y4i_pjk_4gn_AEAAA.json) |
| `AEAAAA` | 偼伯（衛君） | [《史記・衛康叔世家》][641] | [JSON](y4i_pjk_4gn_AEAAAA.json) |
| `AEAAAAA` | 靖伯（衛君） | [《史記・衛康叔世家》][641] | [JSON](y4i_pjk_4gn_AEAAAAA.json) |
| `AEAAAAAA` | 貞伯（衛君） | [《史記・衛康叔世家》][641] | [JSON](y4i_pjk_4gn_AEAAAAAA.json) |
| `AEAAAAAAA` | 頃侯（衛君） | [《史記・衛康叔世家》][641] | [JSON](y4i_pjk_4gn_AEAAAAAAA.json) |
| `AEAAAAAAAA` | 釐侯（衛君） | [《史記・衛康叔世家》][641] | [JSON](y4i_pjk_4gn_AEAAAAAAAA.json) |
| `AF` | 伯邑考（文王長子） | [《史記・管蔡世家》][639] | [JSON](y4i_pjk_4gn_AF.json) |
| `AG` | 曹叔振鐸 | [《史記・管蔡世家》][639] | [JSON](y4i_pjk_4gn_AG.json) |
| `AGA` | 脾（曹太伯） | [《史記・管蔡世家》][639] | [JSON](y4i_pjk_4gn_AGA.json) |
| `AGAA` | 平（曹仲君） | [《史記・管蔡世家》][639] | [JSON](y4i_pjk_4gn_AGAA.json) |
| `AGAAA` | 侯（曹宮伯） | [《史記・管蔡世家》][639] | [JSON](y4i_pjk_4gn_AGAAA.json) |
| `AGAAAA` | 云（曹孝伯） | [《史記・管蔡世家》][639] | [JSON](y4i_pjk_4gn_AGAAAA.json) |
| `AGAAAAA` | 喜（曹夷伯） | [《史記・管蔡世家》][639] | [JSON](y4i_pjk_4gn_AGAAAAA.json) |
| `AH` | 成叔武（文王子） | [《史記・管蔡世家》][639] | [JSON](y4i_pjk_4gn_AH.json) |
| `AI` | 霍叔處（文王子） | [《史記・管蔡世家》][639] | [JSON](y4i_pjk_4gn_AI.json) |
| `AJ` | 冉季載（文王少子） | [《史記・管蔡世家》][639] | [JSON](y4i_pjk_4gn_AJ.json) |
| `B` | 虢叔 | [《史記・秦本紀》][627]、[《史記・晉世家》][643] | [JSON](y4i_pjk_4gn_B.json) |
| `C` | 虢仲（王季子） | [《史記・晉世家》][643] | [JSON](y4i_pjk_4gn_C.json) |

</details>

<details><summary><code>y73_ysx_y5x</code> 王牢（王玄謨祖）（7 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 王牢（王玄謨祖） | [《宋書・朱脩之 宗愨 王玄謨》][873] | [JSON](y73_ysx_y5x.json) |
| `A` | 王秀（王玄謨父） | [《宋書・朱脩之 宗愨 王玄謨》][873] | [JSON](y73_ysx_y5x_A.json) |
| `AA` | 王玄謨 | [《宋書・朱脩之 宗愨 王玄謨》][873] | [JSON](y73_ysx_y5x_AA.json) |
| `AAA` | 王深（王玄謨子） | [《南史・王鎮惡　朱齡石　毛脩之　傅弘之　朱脩之　王玄謨》][460]、[《宋書・朱脩之 宗愨 王玄謨》][872] | [JSON](y73_ysx_y5x_AAA.json) |
| `AAAA` | 王繢（王深子，王玄謨孫） | [《南史・王鎮惡　朱齡石　毛脩之　傅弘之　朱脩之　王玄謨》][460]、[《宋書・朱脩之 宗愨 王玄謨》][872] | [JSON](y73_ysx_y5x_AAAA.json) |
| `AAB` | 王寬（王玄謨子） | [《南齊書・劉懷珍 李安民 王玄載》][347] | [JSON](y73_ysx_y5x_AAB.json) |
| `AAC` | 王瞻（字明遠，一字叔鸞，王玄謨子） | [《南史・王鎮惡　朱齡石　毛脩之　傅弘之　朱脩之　王玄謨》][464] | [JSON](y73_ysx_y5x_AAC.json) |

</details>

<details><summary><code>y97_huh_vuz</code> 秦襄公（34 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 秦襄公 | [《史記・秦本紀》][627] | [JSON](y97_huh_vuz.json) |
| `A` | 秦文公 | [《史記・秦本紀》][627] | [JSON](y97_huh_vuz_A.json) |
| `AA` | 靜公（卷末世系） | [《史記・秦始皇本紀》][628] | [JSON](y97_huh_vuz_AA.json) |
| `AAA` | 憲公（卷末世系） | [《史記・秦始皇本紀》][628] | [JSON](y97_huh_vuz_AAA.json) |
| `AAAA` | 秦德公 | [《史記・秦本紀》][627] | [JSON](y97_huh_vuz_AAAA.json) |
| `AAAAA` | 秦穆公 | [《史記・秦本紀》][627] | [JSON](y97_huh_vuz_AAAAA.json) |
| `AAAAAA` | 秦康公 | [《史記・秦本紀》][627] | [JSON](y97_huh_vuz_AAAAAA.json) |
| `AAAAAAA` | 秦共公 | [《史記・秦本紀》][627] | [JSON](y97_huh_vuz_AAAAAAA.json) |
| `AAAAAAAA` | 秦桓公 | [《史記・秦本紀》][627] | [JSON](y97_huh_vuz_AAAAAAAA.json) |
| `AAAAAAAAA` | 秦景公 | [《史記・秦本紀》][627] | [JSON](y97_huh_vuz_AAAAAAAAA.json) |
| `AAAAAAAAAA` | 秦哀公 | [《史記・秦本紀》][627] | [JSON](y97_huh_vuz_AAAAAAAAAA.json) |
| `AAAAAAAAAAA` | 秦夷公 | [《史記・秦本紀》][627] | [JSON](y97_huh_vuz_AAAAAAAAAAA.json) |
| `AAAAAAAAAAAA` | 秦惠公（夷公子） | [《史記・秦本紀》][627] | [JSON](y97_huh_vuz_AAAAAAAAAAAA.json) |
| `AAAAAAAAAAAAA` | 秦悼公 | [《史記・秦本紀》][627]、[《史記・秦始皇本紀》][628] | [JSON](y97_huh_vuz_AAAAAAAAAAAAA.json) |
| `AAAAAAAAAAAAAA` | 秦厲共公 | [《史記・秦本紀》][627] | [JSON](y97_huh_vuz_AAAAAAAAAAAAAA.json) |
| `AAAAAAAAAAAAAAA` | 秦躁公 | [《史記・秦本紀》][627] | [JSON](y97_huh_vuz_AAAAAAAAAAAAAAA.json) |
| `AAAAAAAAAAAAAB` | 剌龔公（本文字形） | [《史記・秦始皇本紀》][628] | [JSON](y97_huh_vuz_AAAAAAAAAAAAAB.json) |
| `AAAAAAAAAAAAABA` | 秦懷公 | [《史記・秦本紀》][627] | [JSON](y97_huh_vuz_AAAAAAAAAAAAABA.json) |
| `AAAAAAAAAAAAABAA` | 昭子（秦懷公太子） | [《史記・秦本紀》][627] | [JSON](y97_huh_vuz_AAAAAAAAAAAAABAA.json) |
| `AAAAAAAAAAAAABAAA` | 秦靈公 | [《史記・秦本紀》][627] | [JSON](y97_huh_vuz_AAAAAAAAAAAAABAAA.json) |
| `AAAAAAAAAAAAABAAAA` | 秦獻公 | [《史記・秦本紀》][627] | [JSON](y97_huh_vuz_AAAAAAAAAAAAABAAAA.json) |
| `AAAAAAAAAAAAABAAAAA` | 秦孝公 | [《史記・商君列傳》][672] | [JSON](y97_huh_vuz_AAAAAAAAAAAAABAAAAA.json) |
| `AAAAAAAAAAAAABAAAAAA` | 秦惠王 | [《史記・張儀列傳》][674] | [JSON](y97_huh_vuz_AAAAAAAAAAAAABAAAAAA.json) |
| `AAAAAAAAAAAAABAAAAAAA` | 秦武王 | [《史記・樗里子甘茂列傳》][675] | [JSON](y97_huh_vuz_AAAAAAAAAAAAABAAAAAAA.json) |
| `AAAAAAAAAAAAABAAAAAAB` | 秦惠王女（燕太子婦） | [《史記・燕召公世家》][638] | [JSON](y97_huh_vuz_AAAAAAAAAAAAABAAAAAAB.json) |
| `AAAAAAAAAAAAABAB` | 秦簡公 | [《史記・秦本紀》][627] | [JSON](y97_huh_vuz_AAAAAAAAAAAAABAB.json) |
| `AAAAAAAAAAAAABABA` | 秦惠公（簡公子） | [《史記・秦本紀》][627] | [JSON](y97_huh_vuz_AAAAAAAAAAAAABABA.json) |
| `AAAAAAAAAAAAABABAA` | 出子（秦惠公子） | [《史記・秦本紀》][627] | [JSON](y97_huh_vuz_AAAAAAAAAAAAABABAA.json) |
| `AAAAAAAAAB` | 畢公（秦卷末世系） | [《史記・秦始皇本紀》][628] | [JSON](y97_huh_vuz_AAAAAAAAAB.json) |
| `AAAAB` | 秦宣公 | [《史記・秦本紀》][627] | [JSON](y97_huh_vuz_AAAAB.json) |
| `AAAAC` | 秦成公 | [《史記・秦本紀》][627] | [JSON](y97_huh_vuz_AAAAC.json) |
| `AAAB` | 秦武公 | [《史記・秦本紀》][627] | [JSON](y97_huh_vuz_AAAB.json) |
| `AAABA` | 白（秦武公子） | [《史記・秦本紀》][627] | [JSON](y97_huh_vuz_AAABA.json) |
| `AAAC` | 出子 | [《史記・秦本紀》][627] | [JSON](y97_huh_vuz_AAAC.json) |

</details>

<details><summary><code>yaj_2vc_98w</code> 吳廣（趙世家娃嬴父候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 吳廣 | [《史記・趙世家》][647]、[《史記・六國年表》][981] | [JSON](yaj_2vc_98w.json) |
| `A` | 娃嬴 | [《史記・趙世家》][647] | [JSON](yaj_2vc_98w_A.json) |

</details>

<details><summary><code>yay_w6f_lis</code> 渾邪（公孫賀父）（衛將軍驃騎列傳候選）（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 渾邪（公孫賀父） | [《史記・衛將軍驃騎列傳》][715] | [JSON](yay_w6f_lis.json) |
| `A` | 公孫賀 | [《史記・衛將軍驃騎列傳》][715] | [JSON](yay_w6f_lis_A.json) |
| `AA` | 敬聲（公孫賀子） | [《史記・衛將軍驃騎列傳》][715] | [JSON](yay_w6f_lis_AA.json) |

</details>

<details><summary><code>yd9_rqt_a0v</code> 悦〔玄伯祖，北史作悅〕（8 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 悦〔玄伯祖，北史作悅〕 | [《魏書・燕鳳 許謙 張衮 崔玄伯 鄧淵》][927]、[《魏書・燕鳳 許謙 張衮 崔玄伯 鄧淵》][928] | [JSON](yd9_rqt_a0v.json) |
| `A` | 潛〔玄伯父〕 | [《魏書・燕鳳 許謙 張衮 崔玄伯 鄧淵》][927] | [JSON](yd9_rqt_a0v_A.json) |
| `AA` | 崔宏 | [《魏書・燕鳳 許謙 張衮 崔玄伯 鄧淵》][927] | [JSON](yd9_rqt_a0v_AA.json) |
| `AAA` | 簡〔玄伯次子，一名覽〕 | [《魏書・燕鳳 許謙 張衮 崔玄伯 鄧淵》][927] | [JSON](yd9_rqt_a0v_AAA.json) |
| `AAB` | 崔浩 | [《魏書・崔浩》][929] | [JSON](yd9_rqt_a0v_AAB.json) |
| `AABA` | 崔浩女〔盧遐妻，未名〕 | [《魏書・刁雍 王慧龍 韓延之 袁式》][930] | [JSON](yd9_rqt_a0v_AABA.json) |
| `AAC` | 崔恬 | [《魏書・燕鳳 許謙 張衮 崔玄伯 鄧淵》][927] | [JSON](yd9_rqt_a0v_AAC.json) |
| `AACA` | 崔恬女〔王慧龍妻，未名〕 | [《魏書・刁雍 王慧龍 韓延之 袁式》][930] | [JSON](yd9_rqt_a0v_AACA.json) |

</details>

<details><summary><code>yfa_tz5_3ge</code> 王韶之（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 王韶之 | [《宋書・范泰 王准之 王韶之 荀伯子》][851] | [JSON](yfa_tz5_3ge.json) |
| `A` | 王曄（王韶之子） | [《南史・王裕之　王鎮之　王韶之　王悅之　王准之》][554]、[《南史・王裕之　王鎮之　王韶之　王悅之　王准之》][553]、[《宋書・范泰 王准之 王韶之 荀伯子》][851] | [JSON](yfa_tz5_3ge_A.json) |

</details>

<details><summary><code>yfm_7fm_2ei</code> 崔朝（6 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 崔朝 | [《後漢書・崔駰列傳》][62] | [JSON](yfm_7fm_2ei.json) |
| `A` | 崔舒 | [《後漢書・崔駰列傳》][62] | [JSON](yfm_7fm_2ei_A.json) |
| `AA` | 崔篆 | [《後漢書・崔駰列傳》][62] | [JSON](yfm_7fm_2ei_AA.json) |
| `AAA` | 崔毅 | [《後漢書・崔駰列傳》][62] | [JSON](yfm_7fm_2ei_AAA.json) |
| `AAAA` | 崔駰 | [《後漢書・崔駰列傳》][62] | [JSON](yfm_7fm_2ei_AAAA.json) |
| `AAAAA` | 崔瑗 | [《後漢書・崔駰列傳》][62] | [JSON](yfm_7fm_2ei_AAAAA.json) |

</details>

<details><summary><code>yhm_h9f_8p0</code> 范蠡（越世家候選）（4 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 范蠡 | [《史記・越王勾踐世家》][645] | [JSON](yhm_h9f_8p0.json) |
| `A` | 朱公長男（越世家未名者） | [《史記・越王勾踐世家》][645] | [JSON](yhm_h9f_8p0_A.json) |
| `B` | 朱公中男（越世家未名者） | [《史記・越王勾踐世家》][645] | [JSON](yhm_h9f_8p0_B.json) |
| `C` | 朱公少子（越世家未名者） | [《史記・越王勾踐世家》][645] | [JSON](yhm_h9f_8p0_C.json) |

</details>

<details><summary><code>yht_8tu_hv4</code> 齊景公（田世家候選）（4 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 齊景公 | [《史記・田敬仲完世家》][650] | [JSON](yht_8tu_hv4.json) |
| `A` | 荼 | [《史記・田敬仲完世家》][650] | [JSON](yht_8tu_hv4_A.json) |
| `B` | 陽生 | [《史記・田敬仲完世家》][650] | [JSON](yht_8tu_hv4_B.json) |
| `BA` | 壬 | [《史記・田敬仲完世家》][650] | [JSON](yht_8tu_hv4_BA.json) |

</details>

<details><summary><code>ylb_ttg_8dr</code> 百里傒（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 百里傒 | [《史記・秦本紀》][627] | [JSON](ylb_ttg_8dr.json) |
| `A` | 孟明視 | [《史記・秦本紀》][627] | [JSON](ylb_ttg_8dr_A.json) |

</details>

<details><summary><code>ymr_gcs_kii</code> 熊嚴（楚君）（10 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 熊嚴（楚君） | [《史記・楚世家》][644] | [JSON](ymr_gcs_kii.json) |
| `A` | 伯霜（熊霜） | [《史記・楚世家》][644] | [JSON](ymr_gcs_kii_A.json) |
| `B` | 仲雪（熊嚴子） | [《史記・楚世家》][644] | [JSON](ymr_gcs_kii_B.json) |
| `C` | 叔堪（熊嚴子） | [《史記・楚世家》][644] | [JSON](ymr_gcs_kii_C.json) |
| `D` | 季徇（熊徇） | [《史記・楚世家》][644] | [JSON](ymr_gcs_kii_D.json) |
| `DA` | 熊咢（楚君） | [《史記・楚世家》][644] | [JSON](ymr_gcs_kii_DA.json) |
| `DAA` | 熊儀（若敖） | [《史記・楚世家》][644] | [JSON](ymr_gcs_kii_DAA.json) |
| `DAAA` | 熊坎（霄敖） | [《史記・楚世家》][644] | [JSON](ymr_gcs_kii_DAAA.json) |
| `DAAAA` | 熊眴（蚡冒） | [《史記・楚世家》][644] | [JSON](ymr_gcs_kii_DAAAA.json) |
| `DAAAAA` | 蚡冒子（熊通所弒未名者） | [《史記・楚世家》][644] | [JSON](ymr_gcs_kii_DAAAAA.json) |

</details>

<details><summary><code>yoo_ox0_545</code> 荀淑（51 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 荀淑 | [《後漢書・荀韓鍾陳列傳》][63] | [JSON](yoo_ox0_545.json) |
| `A` | 荀儉 | [《後漢書・荀韓鍾陳列傳》][63] | [JSON](yoo_ox0_545_A.json) |
| `AA` | 荀恱 | [《後漢書・荀韓鍾陳列傳》][63] | [JSON](yoo_ox0_545_AA.json) |
| `B` | 荀緄 | [《三國志・二荀賈傳》][599] | [JSON](yoo_ox0_545_B.json) |
| `BA` | 荀彧 | [《三國志・二荀賈傳》][599] | [JSON](yoo_ox0_545_BA.json) |
| `BAA` | 荀顗 | [《晉書・王沈 荀顗 荀勖 馮紞》][141] | [JSON](yoo_ox0_545_BAA.json) |
| `BAB` | 荀惲 | [《三國志・二荀賈傳》][599] | [JSON](yoo_ox0_545_BAB.json) |
| `BABA` | 荀甝 | [《三國志・二荀賈傳》][599] | [JSON](yoo_ox0_545_BABA.json) |
| `BABAA` | 荀頵 | [《三國志・二荀賈傳》][599] | [JSON](yoo_ox0_545_BABAA.json) |
| `BABAAA` | 荀崧 | [《晉書・王湛 荀崧 范汪 劉惔 張憑 韓伯》][212] | [JSON](yoo_ox0_545_BABAAA.json) |
| `BABAAAA` | 荀蕤 | [《晉書・王湛 荀崧 范汪 劉惔 張憑 韓伯》][212] | [JSON](yoo_ox0_545_BABAAAA.json) |
| `BABAAAAA` | 荀籍 | [《晉書・王湛 荀崧 范汪 劉惔 張憑 韓伯》][211]、[《晉書・王湛 荀崧 范汪 劉惔 張憑 韓伯》][212] | [JSON](yoo_ox0_545_BABAAAAA.json) |
| `BABAAAB` | 荀羨 | [《晉書・王湛 荀崧 范汪 劉惔 張憑 韓伯》][212] | [JSON](yoo_ox0_545_BABAAAB.json) |
| `BABAAABA` | 荀猗 | [《宋書・范泰 王准之 王韶之 荀伯子》][853] | [JSON](yoo_ox0_545_BABAAABA.json) |
| `BABAAABAA` | 荀伯子 | [《宋書・范泰 王准之 王韶之 荀伯子》][853] | [JSON](yoo_ox0_545_BABAAABAA.json) |
| `BABAAABAAA` | 荀赤松 | [《宋書・范泰 王准之 王韶之 荀伯子》][853] | [JSON](yoo_ox0_545_BABAAABAAA.json) |
| `BABAAAC` | 荀灌 | [《晉書・列女》][246]、[《晉書・列女》][244] | [JSON](yoo_ox0_545_BABAAAC.json) |
| `BABB` | 荀霬 | [《三國志・二荀賈傳》][599] | [JSON](yoo_ox0_545_BABB.json) |
| `BABBA` | 荀愷 | [《三國志・二荀賈傳》][599] | [JSON](yoo_ox0_545_BABBA.json) |
| `BABBB` | 荀憺 | [《三國志・二荀賈傳》][599] | [JSON](yoo_ox0_545_BABBB.json) |
| `BABBC` | 荀悝 | [《三國志・二荀賈傳》][599] | [JSON](yoo_ox0_545_BABBC.json) |
| `BAC` | 荀俁 | [《三國志・二荀賈傳》][599] | [JSON](yoo_ox0_545_BAC.json) |
| `BACA` | 荀寓 | [《三國志・二荀賈傳》][599] | [JSON](yoo_ox0_545_BACA.json) |
| `BACAA` | 荀羽 | [《三國志・二荀賈傳》][599] | [JSON](yoo_ox0_545_BACAA.json) |
| `BAD` | 荀詵 | [《三國志・二荀賈傳》][599] | [JSON](yoo_ox0_545_BAD.json) |
| `BAE` | 荀粲 | [《三國志・二荀賈傳》][599] | [JSON](yoo_ox0_545_BAE.json) |
| `BAF` | 荀氏（陳群妻，荀顗姊） | [《晉書・王沈 荀顗 荀勖 馮紞》][141]、[《三國志・二荀賈傳》][599] | [JSON](yoo_ox0_545_BAF.json) |
| `BB` | 荀衍 | [《三國志・二荀賈傳》][599] | [JSON](yoo_ox0_545_BB.json) |
| `BBA` | 荀紹 | [《三國志・二荀賈傳》][599] | [JSON](yoo_ox0_545_BBA.json) |
| `BBAA` | 荀融 | [《三國志・二荀賈傳》][599] | [JSON](yoo_ox0_545_BBAA.json) |
| `BC` | 荀諶 | [《三國志・二荀賈傳》][599] | [JSON](yoo_ox0_545_BC.json) |
| `BCA` | 荀閎 | [《三國志・二荀賈傳》][599] | [JSON](yoo_ox0_545_BCA.json) |
| `C` | 荀靖 | [《後漢書・荀韓鍾陳列傳》][63] | [JSON](yoo_ox0_545_C.json) |
| `D` | 荀燾 | [《後漢書・荀韓鍾陳列傳》][63] | [JSON](yoo_ox0_545_D.json) |
| `E` | 荀汪 | [《後漢書・荀韓鍾陳列傳》][63] | [JSON](yoo_ox0_545_E.json) |
| `F` | 荀爽 | [《後漢書・荀韓鍾陳列傳》][63] | [JSON](yoo_ox0_545_F.json) |
| `FA` | 荀棐 | [《晉書・王沈 荀顗 荀勖 馮紞》][141] | [JSON](yoo_ox0_545_FA.json) |
| `FAA` | 荀肸 | [《晉書・王沈 荀顗 荀勖 馮紞》][141] | [JSON](yoo_ox0_545_FAA.json) |
| `FAAA` | 荀勖 | [《晉書・王沈 荀顗 荀勖 馮紞》][141] | [JSON](yoo_ox0_545_FAAA.json) |
| `FAAAA` | 荀藩 | [《晉書・王沈 荀顗 荀勖 馮紞》][141] | [JSON](yoo_ox0_545_FAAAA.json) |
| `FAAAAA` | 邃（荀藩子） | [《晉書・王沈 荀顗 荀勖 馮紞》][141] | [JSON](yoo_ox0_545_FAAAAA.json) |
| `FAAAAAA` | 汪（荀邃子） | [《晉書・王沈 荀顗 荀勖 馮紞》][141] | [JSON](yoo_ox0_545_FAAAAAA.json) |
| `FAAAAB` | 闓（荀藩子） | [《晉書・王沈 荀顗 荀勖 馮紞》][141] | [JSON](yoo_ox0_545_FAAAAB.json) |
| `FAAAABA` | 達（荀闓子） | [《晉書・王沈 荀顗 荀勖 馮紞》][141] | [JSON](yoo_ox0_545_FAAAABA.json) |
| `FAAAB` | 荀輯 | [《晉書・王沈 荀顗 荀勖 馮紞》][141] | [JSON](yoo_ox0_545_FAAAB.json) |
| `FAAABA` | 畯（荀輯子） | [《晉書・王沈 荀顗 荀勖 馮紞》][141] | [JSON](yoo_ox0_545_FAAABA.json) |
| `FAAABB` | 荀綽 | [《晉書・王沈 荀顗 荀勖 馮紞》][141] | [JSON](yoo_ox0_545_FAAABB.json) |
| `FAAAC` | 荀組 | [《晉書・王沈 荀顗 荀勖 馮紞》][141] | [JSON](yoo_ox0_545_FAAAC.json) |
| `FAAACA` | 奕（荀組子） | [《晉書・王沈 荀顗 荀勖 馮紞》][141] | [JSON](yoo_ox0_545_FAAACA.json) |
| `G` | 荀肅 | [《後漢書・荀韓鍾陳列傳》][63] | [JSON](yoo_ox0_545_G.json) |
| `H` | 荀專 | [《後漢書・荀韓鍾陳列傳》][63] | [JSON](yoo_ox0_545_H.json) |

</details>

<details><summary><code>yph_dkb_w4w</code> 申屠嘉（4 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 申屠嘉 | [《史記・張丞相列傳》][700] | [JSON](yph_dkb_w4w.json) |
| `A` | 申屠蔑 | [《史記・張丞相列傳》][700] | [JSON](yph_dkb_w4w_A.json) |
| `AA` | 申屠去病 | [《史記・張丞相列傳》][700] | [JSON](yph_dkb_w4w_AA.json) |
| `AAA` | 申屠臾 | [《史記・張丞相列傳》][700] | [JSON](yph_dkb_w4w_AAA.json) |

</details>

<details><summary><code>yqp_nlb_p1p</code> 太公（漢王父稱）（125 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 太公（漢王父稱） | [《史記・高祖本紀》][630] | [JSON](yqp_nlb_p1p.json) |
| `A` | 高祖 | [《史記・高祖本紀》][630] | [JSON](yqp_nlb_p1p_A.json) |
| `AA` | 孝惠（本卷稱呼） | [《史記・呂后本紀》][631] | [JSON](yqp_nlb_p1p_AA.json) |
| `AB` | 劉肥 | [《史記・齊悼惠王世家》][656] | [JSON](yqp_nlb_p1p_AB.json) |
| `ABA` | 齊哀王（本卷未名） | [《史記・齊悼惠王世家》][656] | [JSON](yqp_nlb_p1p_ABA.json) |
| `ABB` | 卬（膠西王） | [《史記・吳王濞列傳》][710] | [JSON](yqp_nlb_p1p_ABB.json) |
| `ABBA` | 膠西王太子德 | [《史記・吳王濞列傳》][710] | [JSON](yqp_nlb_p1p_ABBA.json) |
| `ABC` | 興居（齊悼惠王子） | [《史記・齊悼惠王世家》][656] | [JSON](yqp_nlb_p1p_ABC.json) |
| `ABD` | 辟光（濟南王） | [《史記・齊悼惠王世家》][656] | [JSON](yqp_nlb_p1p_ABD.json) |
| `ABE` | 雄渠（膠東王） | [《史記・齊悼惠王世家》][656]、[《史記・吳王濞列傳》][710] | [JSON](yqp_nlb_p1p_ABE.json) |
| `ABF` | 章（城陽景王） | [《史記・齊悼惠王世家》][656] | [JSON](yqp_nlb_p1p_ABF.json) |
| `ABFA` | 喜（城陽共王） | [《史記・齊悼惠王世家》][656]、[《史記・漢興以來諸侯王年表》][983] | [JSON](yqp_nlb_p1p_ABFA.json) |
| `ABFAA` | 延校勘建未定 | [《史記・齊悼惠王世家》][656] | [JSON](yqp_nlb_p1p_ABFAA.json) |
| `ABFAAA` | 義 | [《史記・齊悼惠王世家》][656] | [JSON](yqp_nlb_p1p_ABFAAA.json) |
| `ABFAAAA` | 武城陽惠王 | [《史記・齊悼惠王世家》][656] | [JSON](yqp_nlb_p1p_ABFAAAA.json) |
| `ABFAAAAA` | 順 | [《史記・齊悼惠王世家》][656] | [JSON](yqp_nlb_p1p_ABFAAAAA.json) |
| `ABFAAAAAA` | 恢城陽戴王 | [《史記・齊悼惠王世家》][656] | [JSON](yqp_nlb_p1p_ABFAAAAAA.json) |
| `ABFAAAAAAA` | 景城陽末王 | [《史記・齊悼惠王世家》][656] | [JSON](yqp_nlb_p1p_ABFAAAAAAA.json) |
| `ABFAB` | 劉福 | [《史記・東越列傳》][718]、[《史記・建元以來侯者年表》][986]、[《史記・建元已來王子侯者年表》][987] | [JSON](yqp_nlb_p1p_ABFAB.json) |
| `ABFAC` | 劉齒 | [《史記・建元已來王子侯者年表》][987] | [JSON](yqp_nlb_p1p_ABFAC.json) |
| `ABG` | 賢（菑川王） | [《史記・齊悼惠王世家》][656]、[《史記・吳王濞列傳》][710] | [JSON](yqp_nlb_p1p_ABG.json) |
| `ABH` | 志（濟北王，後王菑川） | [《史記・齊悼惠王世家》][656] | [JSON](yqp_nlb_p1p_ABH.json) |
| `ABHA` | 建菑川靖王 | [《史記・齊悼惠王世家》][656] | [JSON](yqp_nlb_p1p_ABHA.json) |
| `ABHAA` | 遺 | [《史記・齊悼惠王世家》][656] | [JSON](yqp_nlb_p1p_ABHAA.json) |
| `ABHAAA` | 終古 | [《史記・齊悼惠王世家》][656] | [JSON](yqp_nlb_p1p_ABHAAA.json) |
| `ABHAAAA` | 尚菑川孝王 | [《史記・齊悼惠王世家》][656] | [JSON](yqp_nlb_p1p_ABHAAAA.json) |
| `ABHAAAAA` | 橫 | [《史記・齊悼惠王世家》][656] | [JSON](yqp_nlb_p1p_ABHAAAAA.json) |
| `ABI` | 齊孝王將閭 | [《史記・齊悼惠王世家》][656] | [JSON](yqp_nlb_p1p_ABI.json) |
| `AC` | 恒（高祖子） | [《史記・孝文本紀》][632] | [JSON](yqp_nlb_p1p_AC.json) |
| `ACA` | 孝景帝 | [《史記・梁孝王世家》][662] | [JSON](yqp_nlb_p1p_ACA.json) |
| `ACAA` | 孝武皇帝 | [《史記・孝武本紀》][634] | [JSON](yqp_nlb_p1p_ACAA.json) |
| `ACAAA` | 閎（齊王） | [《史記・三王世家》][664] | [JSON](yqp_nlb_p1p_ACAAA.json) |
| `ACAAB` | 旦 | [《史記・三王世家》][664] | [JSON](yqp_nlb_p1p_ACAAB.json) |
| `ACAABA` | 安定侯子 | [《史記・三王世家》][664] | [JSON](yqp_nlb_p1p_ACAABA.json) |
| `ACAABB` | 建 | [《史記・三王世家》][664] | [JSON](yqp_nlb_p1p_ACAABB.json) |
| `ACAAC` | 胥 | [《史記・三王世家》][664] | [JSON](yqp_nlb_p1p_ACAAC.json) |
| `ACAACA` | 朝陽侯子 | [《史記・三王世家》][664] | [JSON](yqp_nlb_p1p_ACAACA.json) |
| `ACAACB` | 平曲侯子 | [《史記・三王世家》][664] | [JSON](yqp_nlb_p1p_ACAACB.json) |
| `ACAACC` | 南利侯子 | [《史記・三王世家》][664] | [JSON](yqp_nlb_p1p_ACAACC.json) |
| `ACAACD` | 弘 | [《史記・三王世家》][664] | [JSON](yqp_nlb_p1p_ACAACD.json) |
| `ACAAD` | 據 | [《史記・田叔列傳》][708] | [JSON](yqp_nlb_p1p_ACAAD.json) |
| `ACAAE` | 昭帝 | [《史記・三王世家》][664] | [JSON](yqp_nlb_p1p_ACAAE.json) |
| `ACAAF` | 昌邑哀王髆 | [《漢書・武五子傳》][56] | [JSON](yqp_nlb_p1p_ACAAF.json) |
| `ACAAFA` | 賀（海昬侯） | [《漢書・武五子傳》][56] | [JSON](yqp_nlb_p1p_ACAAFA.json) |
| `ACAB` | 德 | [《史記・五宗世家》][663] | [JSON](yqp_nlb_p1p_ACAB.json) |
| `ACABA` | 不害 | [《史記・五宗世家》][663] | [JSON](yqp_nlb_p1p_ACABA.json) |
| `ACABAA` | 基 | [《史記・五宗世家》][663] | [JSON](yqp_nlb_p1p_ACABAA.json) |
| `ACABAAA` | 授 | [《史記・五宗世家》][663]、[《史記・漢興以來諸侯王年表》][983] | [JSON](yqp_nlb_p1p_ACABAAA.json) |
| `ACAC` | 閼于 | [《史記・五宗世家》][663] | [JSON](yqp_nlb_p1p_ACAC.json) |
| `ACAD` | 發 | [《史記・五宗世家》][663] | [JSON](yqp_nlb_p1p_ACAD.json) |
| `ACADA` | 庸 | [《史記・五宗世家》][663]、[《史記・漢興以來諸侯王年表》][983] | [JSON](yqp_nlb_p1p_ACADA.json) |
| `ACADAA` | 鮒鮈 | [《史記・五宗世家》][663] | [JSON](yqp_nlb_p1p_ACADAA.json) |
| `ACAE` | 乘 | [《史記・五宗世家》][663] | [JSON](yqp_nlb_p1p_ACAE.json) |
| `ACAF` | 趙王彭祖 | [《史記・五宗世家》][663] | [JSON](yqp_nlb_p1p_ACAF.json) |
| `ACAG` | 舜（景帝子） | [《史記・五宗世家》][663] | [JSON](yqp_nlb_p1p_ACAG.json) |
| `ACAGA` | 棁 | [《史記・五宗世家》][663] | [JSON](yqp_nlb_p1p_ACAGA.json) |
| `ACAGB` | 平 | [《史記・五宗世家》][663] | [JSON](yqp_nlb_p1p_ACAGB.json) |
| `ACAGC` | 商 | [《史記・五宗世家》][663] | [JSON](yqp_nlb_p1p_ACAGC.json) |
| `ACAGCA` | 安世 | [《史記・五宗世家》][663] | [JSON](yqp_nlb_p1p_ACAGCA.json) |
| `ACAH` | 栗太子（本卷未名） | [《史記・五宗世家》][663] | [JSON](yqp_nlb_p1p_ACAH.json) |
| `ACAI` | 勝（景帝子） | [《史記・五宗世家》][663] | [JSON](yqp_nlb_p1p_ACAI.json) |
| `ACAIA` | 昌 | [《史記・五宗世家》][663]、[《史記・漢興以來諸侯王年表》][983] | [JSON](yqp_nlb_p1p_ACAIA.json) |
| `ACAIAA` | 昆侈 | [《史記・五宗世家》][663] | [JSON](yqp_nlb_p1p_ACAIAA.json) |
| `ACAJ` | 越（景帝子） | [《史記・五宗世家》][663] | [JSON](yqp_nlb_p1p_ACAJ.json) |
| `ACAJA` | 齊 | [《史記・五宗世家》][663] | [JSON](yqp_nlb_p1p_ACAJA.json) |
| `ACAK` | 非（汝南王） | [《史記・五宗世家》][663] | [JSON](yqp_nlb_p1p_ACAK.json) |
| `ACAKA` | 建 | [《史記・五宗世家》][663] | [JSON](yqp_nlb_p1p_ACAKA.json) |
| `ACAL` | 餘（淮陽王） | [《史記・田叔列傳》][708] | [JSON](yqp_nlb_p1p_ACAL.json) |
| `ACALA` | 光 | [《史記・五宗世家》][663] | [JSON](yqp_nlb_p1p_ACALA.json) |
| `ACAM` | 寄（景帝子） | [《史記・五宗世家》][663] | [JSON](yqp_nlb_p1p_ACAM.json) |
| `ACAMA` | 賢 | [《史記・五宗世家》][663] | [JSON](yqp_nlb_p1p_ACAMA.json) |
| `ACAMAA` | 膠東慶 | [《史記・五宗世家》][663] | [JSON](yqp_nlb_p1p_ACAMAA.json) |
| `ACAMB` | 六安慶 | [《史記・五宗世家》][663] | [JSON](yqp_nlb_p1p_ACAMB.json) |
| `ACAN` | 端 | [《史記・五宗世家》][663] | [JSON](yqp_nlb_p1p_ACAN.json) |
| `ACB` | 梁懷王 | [《史記・屈原賈生列傳》][688] | [JSON](yqp_nlb_p1p_ACB.json) |
| `ACC` | 參 | [《史記・梁孝王世家》][662] | [JSON](yqp_nlb_p1p_ACC.json) |
| `ACCA` | 登 | [《史記・梁孝王世家》][662] | [JSON](yqp_nlb_p1p_ACCA.json) |
| `ACCAA` | 義 | [《史記・梁孝王世家》][662] | [JSON](yqp_nlb_p1p_ACCAA.json) |
| `ACD` | 勝 | [《史記・梁孝王世家》][662] | [JSON](yqp_nlb_p1p_ACD.json) |
| `ACE` | 孝文帝女公主 | [《史記・絳侯周勃世家》][661] | [JSON](yqp_nlb_p1p_ACE.json) |
| `ACF` | 嫖（長公主） | [《史記・外戚世家》][653] | [JSON](yqp_nlb_p1p_ACF.json) |
| `ACG` | 梁孝王武 | [《史記・梁孝王世家》][662] | [JSON](yqp_nlb_p1p_ACG.json) |
| `ACGA` | 買 | [《史記・梁孝王世家》][662] | [JSON](yqp_nlb_p1p_ACGA.json) |
| `ACGAA` | 襄 | [《史記・梁孝王世家》][662] | [JSON](yqp_nlb_p1p_ACGAA.json) |
| `ACGAAA` | 無傷 | [《史記・梁孝王世家》][662] | [JSON](yqp_nlb_p1p_ACGAAA.json) |
| `ACGB` | 明 | [《史記・梁孝王世家》][662] | [JSON](yqp_nlb_p1p_ACGB.json) |
| `ACGC` | 彭離 | [《史記・梁孝王世家》][662] | [JSON](yqp_nlb_p1p_ACGC.json) |
| `ACGD` | 定 | [《史記・梁孝王世家》][662] | [JSON](yqp_nlb_p1p_ACGD.json) |
| `ACGE` | 不識 | [《史記・梁孝王世家》][662] | [JSON](yqp_nlb_p1p_ACGE.json) |
| `AD` | 恢（高祖子） | [《史記・呂后本紀》][631] | [JSON](yqp_nlb_p1p_AD.json) |
| `AE` | 友（高祖子） | [《史記・呂后本紀》][631] | [JSON](yqp_nlb_p1p_AE.json) |
| `AEA` | 遂（趙幽王子） | [《史記・楚元王世家》][654] | [JSON](yqp_nlb_p1p_AEA.json) |
| `AEB` | 辟彊（趙幽王子） | [《史記・孝文本紀》][632]、[《史記・楚元王世家》][654]、[《史記・漢興以來諸侯王年表》][983] | [JSON](yqp_nlb_p1p_AEB.json) |
| `AEBA` | 福 | [《史記・楚元王世家》][654]、[《史記・漢興以來諸侯王年表》][983] | [JSON](yqp_nlb_p1p_AEBA.json) |
| `AF` | 長（高祖子） | [《史記・淮南衡山列傳》][722] | [JSON](yqp_nlb_p1p_AF.json) |
| `AFA` | 淮南王安 | [《史記・淮南衡山列傳》][722] | [JSON](yqp_nlb_p1p_AFA.json) |
| `AFAA` | 陵（淮南王女） | [《史記・淮南衡山列傳》][722] | [JSON](yqp_nlb_p1p_AFAA.json) |
| `AFAB` | 不害 | [《史記・淮南衡山列傳》][722] | [JSON](yqp_nlb_p1p_AFAB.json) |
| `AFABA` | 建（不害子） | [《史記・淮南衡山列傳》][722] | [JSON](yqp_nlb_p1p_AFABA.json) |
| `AFAC` | 淮南太子遷 | [《史記・淮南衡山列傳》][722] | [JSON](yqp_nlb_p1p_AFAC.json) |
| `AFB` | 濟北王勃 | [《史記・淮南衡山列傳》][722] | [JSON](yqp_nlb_p1p_AFB.json) |
| `AFC` | 衡山王賜 | [《史記・淮南衡山列傳》][722] | [JSON](yqp_nlb_p1p_AFC.json) |
| `AFCA` | 爽（衡山太子） | [《史記・淮南衡山列傳》][722] | [JSON](yqp_nlb_p1p_AFCA.json) |
| `AFCB` | 孝（衡山王子） | [《史記・淮南衡山列傳》][722] | [JSON](yqp_nlb_p1p_AFCB.json) |
| `AFCC` | 無采 | [《史記・淮南衡山列傳》][722] | [JSON](yqp_nlb_p1p_AFCC.json) |
| `AFD` | 東城侯良 | [《史記・淮南衡山列傳》][722]、[《史記・惠景間侯者年表》][985] | [JSON](yqp_nlb_p1p_AFD.json) |
| `AG` | 建（高祖子） | [《史記・高祖本紀》][630]、[《史記・呂后本紀》][631]、[《史記・漢興以來諸侯王年表》][983] | [JSON](yqp_nlb_p1p_AG.json) |
| `AH` | 如意（高祖子） | [《史記・呂后本紀》][631] | [JSON](yqp_nlb_p1p_AH.json) |
| `AI` | 魯元（本卷稱呼） | [《史記・呂后本紀》][631] | [JSON](yqp_nlb_p1p_AI.json) |
| `B` | 伯 | [《史記・楚元王世家》][654] | [JSON](yqp_nlb_p1p_B.json) |
| `BA` | 信羹頡侯 | [《史記・楚元王世家》][654] | [JSON](yqp_nlb_p1p_BA.json) |
| `C` | 仲 | [《史記・高祖本紀》][630]、[《史記・吳王濞列傳》][710] | [JSON](yqp_nlb_p1p_C.json) |
| `CA` | 劉濞 | [《史記・吳王濞列傳》][710] | [JSON](yqp_nlb_p1p_CA.json) |
| `CAA` | 吳太子被殺未名 | [《漢書・荊燕吳傳》][52]、[《史記・吳王濞列傳》][710] | [JSON](yqp_nlb_p1p_CAA.json) |
| `CAB` | 吳王少子未名 | [《漢書・荊燕吳傳》][52]、[《史記・吳王濞列傳》][710] | [JSON](yqp_nlb_p1p_CAB.json) |
| `CAD` | 子華 | [《史記・吳王濞列傳》][710] | [JSON](yqp_nlb_p1p_CAD.json) |
| `CAE` | 駒（吳王太子；《史記》作子駒） | [《漢書・荊燕吳傳》][52]、[《史記・吳王濞列傳》][710] | [JSON](yqp_nlb_p1p_CAE.json) |
| `D` | 劉交 | [《史記・楚元王世家》][654] | [JSON](yqp_nlb_p1p_D.json) |
| `DA` | 藝（楚元王子） | [《史記・孝景本紀》][633] | [JSON](yqp_nlb_p1p_DA.json) |
| `DB` | 禮（楚元王子） | [《史記・楚元王世家》][654] | [JSON](yqp_nlb_p1p_DB.json) |
| `DBA` | 道 | [《史記・楚元王世家》][654] | [JSON](yqp_nlb_p1p_DBA.json) |
| `DBAA` | 注 | [《史記・楚元王世家》][654] | [JSON](yqp_nlb_p1p_DBAA.json) |
| `DBAAA` | 純 | [《史記・楚元王世家》][654] | [JSON](yqp_nlb_p1p_DBAAA.json) |
| `DC` | 郢 | [《史記・儒林列傳》][725] | [JSON](yqp_nlb_p1p_DC.json) |
| `DCA` | 戊（楚王） | [《史記・吳王濞列傳》][710] | [JSON](yqp_nlb_p1p_DCA.json) |

</details>

<details><summary><code>z0l_1wp_de1</code> 趙破奴（匈奴列傳第44段）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 趙破奴（匈奴列傳第44段） | [《史記・匈奴列傳》][714] | [JSON](z0l_1wp_de1.json) |
| `A` | 安國（趙破奴子） | [《史記・衛將軍驃騎列傳》][715] | [JSON](z0l_1wp_de1_A.json) |

</details>

<details><summary><code>z0n_1jd_fda</code> 胡奮（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 胡奮 | [《晉書・后妃上》][127]、[《三國志・桓二陳徐衞盧傳》][612] | [JSON](z0n_1jd_fda.json) |
| `A` | 胡芳〔武帝貴嬪〕 | [《晉書・后妃上》][127] | [JSON](z0n_1jd_fda_A.json) |

</details>

<details><summary><code>z8l_wje_08d</code> 卜商（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 卜商 | [《史記・仲尼弟子列傳》][671] | [JSON](z8l_wje_08d.json) |
| `A` | 卜商之子 | [《史記・仲尼弟子列傳》][671] | [JSON](z8l_wje_08d_A.json) |

</details>

<details><summary><code>z9d_qn5_wg8</code> 路人（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 路人 | [《史記・朝鮮列傳》][719] | [JSON](z9d_qn5_wg8.json) |
| `A` | 最 | [《史記・建元以來侯者年表》][986] | [JSON](z9d_qn5_wg8_A.json) |

</details>

<details><summary><code>z9e_8iy_7ah</code> 崔輯（4 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 崔輯 | [《魏書・燕鳳 許謙 張衮 崔玄伯 鄧淵》][926] | [JSON](z9e_8iy_7ah.json) |
| `A` | 崔攸之 | [《北史・崔光 崔亮》][6]、[《魏書・燕鳳 許謙 張衮 崔玄伯 鄧淵》][926] | [JSON](z9e_8iy_7ah_A.json) |
| `B` | 崔目連 | [《北史・崔光 崔亮》][6]、[《魏書・燕鳳 許謙 張衮 崔玄伯 鄧淵》][926] | [JSON](z9e_8iy_7ah_B.json) |
| `C` | 崔修之 | [《北史・崔光 崔亮》][6] | [JSON](z9e_8iy_7ah_C.json) |

</details>

<details><summary><code>zan_qcc_jy5</code> 陳文公（田世家候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 陳文公 | [《史記・田敬仲完世家》][650] | [JSON](zan_qcc_jy5.json) |
| `A` | 陳厲公他 | [《史記・田敬仲完世家》][650] | [JSON](zan_qcc_jy5_A.json) |

</details>

<details><summary><code>zk0_g6b_nbq</code> 伍奢（楚篇候選）（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 伍奢 | [《史記・楚世家》][644] | [JSON](zk0_g6b_nbq.json) |
| `A` | 伍尚 | [《史記・楚世家》][644] | [JSON](zk0_g6b_nbq_A.json) |
| `B` | 伍胥 | [《史記・楚世家》][644] | [JSON](zk0_g6b_nbq_B.json) |

</details>

<details><summary><code>zql_k3t_8ro</code> 先軫（重耳五士）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 先軫（重耳五士） | [《史記・晉世家》][643] | [JSON](zql_k3t_8ro.json) |
| `A` | 先縠（右行將） | [《史記・晉世家》][643] | [JSON](zql_k3t_8ro_A.json) |

</details>

<details><summary><code>zrx_2ip_d1p</code> 張負（陳丞相世家候選）（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 張負 | [《史記・陳丞相世家》][660] | [JSON](zrx_2ip_d1p.json) |
| `*A` | 張氏女 | [《史記・陳丞相世家》][660] | [JSON](zrx_2ip_d1p_%2AA.json) |
| `A` | 張仲 | [《史記・陳丞相世家》][660] | [JSON](zrx_2ip_d1p_A.json) |

</details>

<details><summary><code>zwr_jel_e3l</code> 齊宣公（田世家候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 齊宣公 | [《史記・田敬仲完世家》][650] | [JSON](zwr_jel_e3l.json) |
| `A` | 康公貸 | [《史記・田敬仲完世家》][650] | [JSON](zwr_jel_e3l_A.json) |

</details>

[5]: https://zh.wikisource.org/w/index.php?title=北史/卷044&oldid=2183262
[6]: https://zh.wikisource.org/w/index.php?title=北史/卷044&oldid=2183262
[8]: https://zh.wikisource.org/w/index.php?oldid=2361318
[10]: https://zh.wikisource.org/w/index.php?oldid=8231316
[15]: https://zh.wikisource.org/w/index.php?oldid=2015446
[18]: https://zh.wikisource.org/w/index.php?oldid=1488469
[25]: https://zh.wikisource.org/w/index.php?oldid=1544244
[27]: https://zh.wikisource.org/w/index.php?title=陳書/卷21&oldid=1511909
[30]: https://www.sohu.com/a/259439652_258370
[31]: https://guji.10huan.com/Article/7147_7165.html
[37]: https://www.i-repository.net/il/cont/01/G0000721f/000/756/000756292.jpg
[39]: https://www.sohu.com/a/279761580_738227
[47]: https://zh.wikisource.org/w/index.php?oldid=636080
[52]: https://zh.wikisource.org/w/index.php?title=漢書/卷035&oldid=2605377
[53]: https://zh.wikisource.org/w/index.php?title=漢書/卷041&oldid=2342290
[56]: https://github.com/kanripo/KR2a0007/blob/683113d4baf6febecaf2ccb7913df87c4d68d454/KR2a0007_063.txt
[62]: https://zh.wikisource.org/w/index.php?title=後漢書/卷52&oldid=1956641
[63]: https://github.com/kanripo/KR2a0009/blob/6db36b6dcbe843b825354c22e9be9193d0137c04/KR2a0009_092.txt
[70]: https://commons.wikimedia.org/w/index.php?oldid=1269465774
[71]: https://zh.wikisource.org/w/index.php?oldid=740760
[111]: https://raw.githubusercontent.com/kanripo/KR2a0015/82291520954e5af1fdade894971a2f5810fd4e31/KR2a0015_008.txt
[120]: https://zh.wikisource.org/w/index.php?oldid=2567072
[127]: https://zh.wikisource.org/w/index.php?oldid=2479706
[128]: https://zh.wikisource.org/w/index.php?oldid=1543614
[129]: https://zh.wikisource.org/w/index.php?oldid=1543614
[133]: https://zh.wikisource.org/w/index.php?oldid=1543614
[134]: https://zh.wikisource.org/w/index.php?title=%E6%99%89%E6%9B%B8%2F%E5%8D%B7032&oldid=1543614
[136]: https://zh.wikisource.org/w/index.php?title=%E6%99%89%E6%9B%B8%2F%E5%8D%B7035&oldid=2506399
[141]: https://zh.wikisource.org/w/index.php?title=晉書/卷039&oldid=2108782
[150]: https://zh.wikisource.org/w/index.php?oldid=2618531
[160]: https://zh.wikisource.org/w/index.php?oldid=1775345
[170]: https://zh.wikisource.org/w/index.php?oldid=1775345
[171]: https://zh.wikisource.org/w/index.php?oldid=1775345
[174]: https://zh.wikisource.org/w/index.php?oldid=2305862
[194]: https://zh.wikisource.org/w/index.php?oldid=2592755
[208]: https://zh.wikisource.org/w/index.php?title=晉書/卷074&oldid=1536331
[211]: https://zh.wikisource.org/w/index.php?title=%E6%99%89%E6%9B%B8+%28%E5%9B%9B%E5%BA%AB%E5%85%A8%E6%9B%B8%E6%9C%AC%29%2F%E5%8D%B7075&oldid=761900
[212]: https://zh.wikisource.org/w/index.php?title=晉書/卷075&oldid=2645530
[221]: https://zh.wikisource.org/w/index.php?oldid=2603570
[231]: https://zh.wikisource.org/w/index.php?oldid=2835641
[232]: https://zh.wikisource.org/w/index.php?oldid=1548000
[233]: https://zh.wikisource.org/w/index.php?oldid=1548000
[238]: https://commons.wikimedia.org/w/index.php?oldid=979438884
[239]: https://zh.wikisource.org/w/index.php?oldid=2625341
[244]: https://commons.wikimedia.org/w/index.php?oldid=979438884
[246]: https://zh.wikisource.org/w/index.php?title=晉書/卷096&oldid=2625341
[249]: https://zh.wikisource.org/w/index.php?title=晉書/卷098&oldid=2614273
[253]: https://zh.wikisource.org/w/index.php?title=晉書/卷099&oldid=2644703
[266]: https://zh.wikisource.org/w/index.php?oldid=1729539
[269]: https://zh.wikisource.org/w/index.php?oldid=2401748
[273]: https://zh.wikisource.org/w/index.php?oldid=1538023
[280]: https://zh.wikisource.org/w/index.php?title=梁書/卷21&oldid=1544250
[281]: https://zh.wikisource.org/w/index.php?title=梁書/卷21&oldid=1544250
[290]: https://zh.wikisource.org/w/index.php?oldid=1513347
[291]: https://zh.wikisource.org/w/index.php?oldid=1513347
[293]: https://zh.wikisource.org/w/index.php?oldid=1511478
[297]: https://zh.wikisource.org/w/index.php?title=%E6%A2%81%E6%9B%B8%2F%E5%8D%B730&oldid=1508510
[305]: https://zh.wikisource.org/w/index.php?oldid=2197034
[306]: https://zh.wikisource.org/w/index.php?oldid=1514482
[310]: https://commons.wikimedia.org/w/index.php?oldid=703777627
[311]: https://zh.wikisource.org/w/index.php?title=梁書/卷50&oldid=1514482
[318]: https://zh.wikisource.org/w/index.php?title=南齊書/卷6&oldid=2311630
[320]: https://zh.wikisource.org/w/index.php?oldid=2312010
[323]: https://commons.wikimedia.org/w/index.php?oldid=703777584
[324]: https://zh.wikisource.org/w/index.php?oldid=2074177
[325]: https://commons.wikimedia.org/w/index.php?oldid=703777584
[326]: https://zh.wikisource.org/w/index.php?oldid=2074177
[332]: https://zh.wikisource.org/w/index.php?title=南齊書/卷20&oldid=2074177
[337]: https://commons.wikimedia.org/w/index.php?oldid=703777584
[338]: https://zh.wikisource.org/w/index.php?oldid=2074177
[341]: https://zh.wikisource.org/w/index.php?oldid=1545488
[345]: https://zh.wikisource.org/w/index.php?oldid=1508012
[347]: https://zh.wikisource.org/w/index.php?oldid=1508012
[348]: https://zh.wikisource.org/w/index.php?oldid=1508012
[364]: https://github.com/kanripo/KR2a0017/blob/787dd9a7da495542e8f17c26c96900ce37b2c211/KR2a0017_033.txt
[377]: https://zh.wikisource.org/w/index.php?title=南齊書/卷40&oldid=2272748
[385]: https://zh.wikisource.org/w/index.php?title=南齊書/卷43&oldid=2400356
[390]: https://zh.wikisource.org/w/index.php?oldid=1511897
[391]: https://zh.wikisource.org/w/index.php?title=%E5%8D%97%E9%BD%8A%E6%9B%B8%2F%E5%8D%B746&oldid=1511897
[394]: https://zh.wikisource.org/w/index.php?title=南齊書/卷47&oldid=1492435
[395]: https://zh.wikisource.org/w/index.php?title=南齊書/卷48&oldid=1511898
[398]: https://zh.wikisource.org/w/index.php?oldid=2261984
[399]: https://zh.wikisource.org/w/index.php?oldid=2261984
[412]: https://zh.wikisource.org/w/index.php?oldid=2272731
[413]: https://zh.wikisource.org/w/index.php?title=南齊書/卷50&oldid=2272731
[414]: https://zh.wikisource.org/w/index.php?oldid=2371079
[416]: https://github.com/kanripo/KR2a0017/blob/787dd9a7da495542e8f17c26c96900ce37b2c211/KR2a0017_052.txt
[419]: https://zh.wikisource.org/w/index.php?oldid=2027696
[422]: https://commons.wikimedia.org/w/index.php?oldid=1298729844
[423]: https://zh.wikisource.org/w/index.php?oldid=2288359
[424]: https://commons.wikimedia.org/w/index.php?oldid=1298729844
[425]: https://zh.wikisource.org/w/index.php?oldid=2288359
[427]: https://commons.wikimedia.org/w/index.php?oldid=1298729844
[428]: https://zh.wikisource.org/w/index.php?oldid=2288359
[434]: https://zh.wikisource.org/w/index.php?title=南史/卷11&oldid=2288359
[441]: https://commons.wikimedia.org/w/index.php?oldid=1298729844
[442]: https://zh.wikisource.org/w/index.php?oldid=2288359
[445]: https://commons.wikimedia.org/w/index.php?oldid=1298729844
[446]: https://zh.wikisource.org/w/index.php?oldid=2288359
[451]: https://zh.wikisource.org/w/index.php?oldid=2060595
[452]: https://zh.wikisource.org/w/index.php?oldid=2060595
[453]: https://zh.wikisource.org/w/index.php?oldid=2268660
[460]: https://zh.wikisource.org/w/index.php?oldid=1963381
[464]: https://zh.wikisource.org/w/index.php?oldid=1963381
[479]: https://zh.wikisource.org/w/index.php?title=南史/卷19&oldid=1531762
[480]: https://zh.wikisource.org/w/index.php?title=南史/卷19&oldid=1531762
[490]: https://zh.wikisource.org/w/index.php?oldid=1752646
[491]: https://zh.wikisource.org/w/index.php?oldid=1752646
[493]: https://zh.wikisource.org/w/index.php?oldid=1752646
[498]: https://zh.wikisource.org/w/index.php?oldid=1752646
[504]: https://zh.wikisource.org/w/index.php?oldid=1477957
[510]: https://zh.wikisource.org/w/index.php?title=南史/卷22&oldid=1477957
[511]: https://zh.wikisource.org/w/index.php?oldid=1477957
[517]: https://commons.wikimedia.org/wiki/File:NLC892-411999017142-12360_二十四史_第246冊.pdf
[518]: https://zh.wikisource.org/w/index.php?oldid=1477957
[521]: https://zh.wikisource.org/w/index.php?title=南史/卷23&oldid=2478204
[522]: https://commons.wikimedia.org/wiki/File:NLC892-411999017142-12361_二十四史_第247冊.pdf
[523]: https://zh.wikisource.org/w/index.php?oldid=2478204
[524]: https://zh.wikisource.org/w/index.php?oldid=2478204
[525]: https://zh.wikisource.org/w/index.php?title=南史/卷23&oldid=2478204
[526]: https://zh.wikisource.org/w/index.php?oldid=2478204
[529]: https://zh.wikisource.org/w/index.php?oldid=2478204
[534]: https://zh.wikisource.org/w/index.php?oldid=2478204
[539]: https://zh.wikisource.org/w/index.php?oldid=2478204
[543]: https://zh.wikisource.org/w/index.php?oldid=2478204
[544]: https://zh.wikisource.org/w/index.php?oldid=2478204
[545]: https://zh.wikisource.org/w/index.php?oldid=2478204
[546]: https://zh.wikisource.org/w/index.php?oldid=2478204
[553]: https://commons.wikimedia.org/wiki/File:NLC892-411999017142-12361_%E4%BA%8C%E5%8D%81%E5%9B%9B%E5%8F%B2_%E7%AC%AC247%E5%86%8A.pdf
[554]: https://zh.wikisource.org/w/index.php?oldid=1765279
[555]: https://zh.wikisource.org/w/index.php?oldid=1765279
[563]: https://zh.wikisource.org/w/index.php?oldid=12757141
[564]: https://upload.wikimedia.org/wikipedia/commons/a/a5/NLC892-411999017142-12361_%E4%BA%8C%E5%8D%81%E5%9B%9B%E5%8F%B2_%E7%AC%AC247%E5%86%8A.pdf#page=49
[565]: https://zh.wikisource.org/w/index.php?title=南史/卷26&oldid=1477359
[567]: https://zh.wikisource.org/w/index.php?oldid=1511857
[568]: https://zh.wikisource.org/w/index.php?oldid=1511857
[572]: https://zh.wikisource.org/w/index.php?title=%E5%8D%97%E5%8F%B2%2F%E5%8D%B733&oldid=1554233
[574]: https://zh.wikisource.org/w/index.php?oldid=1489333
[583]: https://zh.wikisource.org/w/index.php?oldid=2598501
[585]: https://zh.wikisource.org/w/index.php?oldid=12945115
[589]: https://zh.wikisource.org/w/index.php?oldid=1553912
[590]: https://zh.wikisource.org/w/index.php?oldid=1495505
[591]: https://zh.wikisource.org/w/index.php?oldid=1748895
[593]: https://zh.wikisource.org/w/index.php?oldid=2124272
[597]: https://raw.githubusercontent.com/kanripo/KR2a0012/214fcafa79894355909c9d8c2c1533089e7791c6/KR2a0012_009.txt
[599]: https://github.com/kanripo/KR2a0012/blob/214fcafa79894355909c9d8c2c1533089e7791c6/KR2a0012_010.txt
[607]: https://zh.wikisource.org/w/index.php?oldid=2610840
[610]: https://github.com/kanripo/KR2a0012/blob/214fcafa79894355909c9d8c2c1533089e7791c6/KR2a0012_019.txt
[612]: https://raw.githubusercontent.com/kanripo/KR2a0012/214fcafa79894355909c9d8c2c1533089e7791c6/KR2a0012_022.txt
[626]: https://zh.wikisource.org/w/index.php?title=史記/卷004&oldid=7909147
[627]: https://zh.wikisource.org/w/index.php?title=史記/卷005&oldid=8744286
[628]: https://zh.wikisource.org/w/index.php?title=史記/卷006&oldid=7907969
[629]: https://zh.wikisource.org/w/index.php?title=史記/卷007&oldid=5978360
[630]: https://zh.wikisource.org/w/index.php?title=史記/卷008&oldid=2440965
[631]: https://zh.wikisource.org/w/index.php?title=史記/卷009&oldid=2087062
[632]: https://zh.wikisource.org/w/index.php?title=史記/卷010&oldid=2599229
[633]: https://zh.wikisource.org/w/index.php?title=史記/卷011&oldid=2520527
[634]: https://zh.wikisource.org/w/index.php?title=史記/卷012&oldid=8733061
[636]: https://zh.wikisource.org/w/index.php?title=史記/卷032&oldid=445042
[637]: https://zh.wikisource.org/w/index.php?title=史記/魯周公世家&oldid=7909289
[638]: https://zh.wikisource.org/w/index.php?title=史記/卷034&oldid=2559287
[639]: https://zh.wikisource.org/w/index.php?title=史記/卷035&oldid=8737302
[640]: https://zh.wikisource.org/w/index.php?title=史記/卷036&oldid=2588525
[641]: https://zh.wikisource.org/w/index.php?title=史記/卷037&oldid=5977124
[642]: https://zh.wikisource.org/w/index.php?title=史記/卷038&oldid=8737306
[643]: https://zh.wikisource.org/w/index.php?title=史記/卷039&oldid=2588534
[644]: https://zh.wikisource.org/w/index.php?title=史記/卷040&oldid=8736796
[645]: https://zh.wikisource.org/w/index.php?title=史記/卷041&oldid=2018395
[646]: https://zh.wikisource.org/w/index.php?title=史記/卷042&oldid=2016409
[647]: https://zh.wikisource.org/w/index.php?title=史記/卷043&oldid=7903603
[649]: https://zh.wikisource.org/w/index.php?title=史記/卷045&oldid=7903607
[650]: https://zh.wikisource.org/w/index.php?title=史記/卷046&oldid=2560838
[653]: https://zh.wikisource.org/w/index.php?title=史記/卷049&oldid=7903610
[654]: https://zh.wikisource.org/w/index.php?title=史記/卷050&oldid=8737728
[656]: https://zh.wikisource.org/w/index.php?title=史記/卷052&oldid=5977113
[657]: https://zh.wikisource.org/w/index.php?title=史記/卷053&oldid=2087971
[659]: https://zh.wikisource.org/w/index.php?title=史記/卷055&oldid=2666612
[660]: https://zh.wikisource.org/w/index.php?title=史記/卷056&oldid=1961615
[661]: https://zh.wikisource.org/w/index.php?title=史記/卷057&oldid=1569360
[662]: https://zh.wikisource.org/w/index.php?title=史記/卷058&oldid=8735555
[663]: https://zh.wikisource.org/w/index.php?title=史記/卷059&oldid=2621125
[664]: https://zh.wikisource.org/w/index.php?title=史記/卷060&oldid=7909290
[667]: https://zh.wikisource.org/w/index.php?title=史記/卷063&oldid=7903601
[669]: https://zh.wikisource.org/w/index.php?title=史記/卷065&oldid=2567048
[670]: https://zh.wikisource.org/w/index.php?title=史記/卷066&oldid=2621138
[671]: https://zh.wikisource.org/w/index.php?title=史記/卷067&oldid=7869003
[672]: https://zh.wikisource.org/w/index.php?title=史記/卷068&oldid=8764712
[674]: https://zh.wikisource.org/w/index.php?title=史記/卷070&oldid=2621148
[675]: https://zh.wikisource.org/w/index.php?title=史記/卷071&oldid=2621152
[680]: https://zh.wikisource.org/w/index.php?title=史記/卷076&oldid=7909284
[681]: https://zh.wikisource.org/w/index.php?title=史記/卷077&oldid=367917
[683]: https://zh.wikisource.org/w/index.php?title=史記/卷079&oldid=2549307
[688]: https://zh.wikisource.org/w/index.php?title=史記/卷084&oldid=1568305
[697]: https://zh.wikisource.org/w/index.php?title=史記/卷093&oldid=368019
[698]: https://zh.wikisource.org/w/index.php?title=史記/卷094&oldid=2171897
[699]: https://zh.wikisource.org/w/index.php?title=史記/卷095&oldid=2298709
[700]: https://zh.wikisource.org/w/index.php?title=史記/卷096&oldid=8770206
[701]: https://zh.wikisource.org/w/index.php?title=史記/卷097&oldid=1383195
[702]: https://zh.wikisource.org/w/index.php?title=史記/卷098&oldid=1490318
[704]: https://zh.wikisource.org/w/index.php?title=史記/卷100&oldid=1965696
[706]: https://zh.wikisource.org/w/index.php?title=史記/卷102&oldid=1753957
[708]: https://zh.wikisource.org/w/index.php?title=史記/卷104&oldid=8739534
[709]: https://zh.wikisource.org/w/index.php?title=史記/卷105&oldid=8842726
[710]: https://zh.wikisource.org/w/index.php?title=史記/卷106&oldid=405869
[711]: https://zh.wikisource.org/w/index.php?title=史記/卷107&oldid=2540571
[713]: https://zh.wikisource.org/w/index.php?title=史記/卷109&oldid=1765440
[714]: https://zh.wikisource.org/w/index.php?title=史記/卷110&oldid=8735645
[715]: https://zh.wikisource.org/w/index.php?title=史記/卷111&oldid=8730225
[716]: https://zh.wikisource.org/w/index.php?title=史記/卷112&oldid=2089420
[717]: https://zh.wikisource.org/w/index.php?title=史記/卷113&oldid=8735632
[718]: https://zh.wikisource.org/w/index.php?title=史記/卷114&oldid=8735633
[719]: https://zh.wikisource.org/w/index.php?title=史記/卷115&oldid=439220
[722]: https://zh.wikisource.org/w/index.php?title=史記/卷118&oldid=7904122
[723]: https://zh.wikisource.org/w/index.php?title=史記/卷119&oldid=7904123
[725]: https://zh.wikisource.org/w/index.php?title=史記/卷121&oldid=8735621
[726]: https://zh.wikisource.org/w/index.php?title=史記/卷122&oldid=7904124
[727]: https://zh.wikisource.org/w/index.php?title=史記/卷123&oldid=8736799
[729]: https://zh.wikisource.org/w/index.php?title=史記/卷125&oldid=2273599
[730]: https://zh.wikisource.org/w/index.php?title=史記/卷126&oldid=2609358
[734]: https://zh.wikisource.org/w/index.php?title=史記/卷130&oldid=2609362
[743]: https://zh.wikisource.org/w/index.php?oldid=2567463
[755]: https://zh.wikisource.org/w/index.php?oldid=2567462
[756]: https://zh.wikisource.org/w/index.php?oldid=2567462
[818]: https://raw.githubusercontent.com/kanripo/KR2a0016/e80c057667e3c8684f11d5088251e10244d5a264/KR2a0016_041.txt
[820]: https://zh.wikisource.org/w/index.php?oldid=2634831
[828]: https://zh.wikisource.org/w/index.php?oldid=2118581
[829]: https://raw.githubusercontent.com/kanripo/KR2a0016/e80c057667e3c8684f11d5088251e10244d5a264/KR2a0016_046.txt
[834]: https://zh.wikisource.org/w/index.php?oldid=2190655
[835]: https://zh.wikisource.org/w/index.php?oldid=2190655
[836]: https://zh.wikisource.org/w/index.php?oldid=2190655
[837]: https://zh.wikisource.org/w/index.php?oldid=2190655
[841]: https://zh.wikisource.org/w/index.php?title=宋書/卷52&oldid=2190655
[851]: https://zh.wikisource.org/w/index.php?oldid=1996694
[853]: https://zh.wikisource.org/w/index.php?title=%E5%AE%8B%E6%9B%B8/%E5%8D%B760&oldid=1996694
[855]: https://github.com/kanripo/KR2a0016/blob/e80c057667e3c8684f11d5088251e10244d5a264/KR2a0016_062.txt
[860]: https://zh.wikisource.org/w/index.php?title=%E5%AE%8B%E6%9B%B8%2F%E5%8D%B764&oldid=1748217
[863]: https://raw.githubusercontent.com/kanripo/KR2a0016/e80c057667e3c8684f11d5088251e10244d5a264/KR2a0016_067.txt
[864]: https://zh.wikisource.org/w/index.php?title=宋書/卷71&oldid=2485515
[865]: https://commons.wikimedia.org/wiki/File:NLC892-411999017142-12246_二十四史_第148冊.pdf
[866]: https://github.com/kanripo/KR2a0016/blob/e80c057667e3c8684f11d5088251e10244d5a264/KR2a0016_071.txt
[871]: https://zh.wikisource.org/w/index.php?title=宋書/卷75&oldid=1997722
[872]: https://zh.wikisource.org/w/index.php?oldid=1997726
[873]: https://zh.wikisource.org/w/index.php?oldid=1997726
[876]: https://zh.wikisource.org/w/index.php?oldid=2069112
[879]: https://zh.wikisource.org/w/index.php?oldid=2069213
[891]: https://zh.wikisource.org/w/index.php?title=宋書/卷88&oldid=2069210
[897]: https://zh.wikisource.org/w/index.php?oldid=1962755
[900]: https://zh.wikisource.org/w/index.php?title=%E5%AE%8B%E6%9B%B8%2F%E5%8D%B793&oldid=1962755
[912]: https://zh.wikisource.org/w/index.php?oldid=2607174
[918]: https://zh.wikisource.org/w/index.php?oldid=2587734
[920]: https://zh.wikisource.org/w/index.php?oldid=2587825
[926]: https://zh.wikisource.org/w/index.php?title=魏書/卷24&oldid=2021236
[927]: https://raw.githubusercontent.com/kanripo/KR2a0020/17b6525eb5aaa878b9640f5a61e90da934ce5fc4/KR2a0020_024.txt
[928]: https://zh.wikisource.org/w/index.php?oldid=2021236
[929]: https://raw.githubusercontent.com/kanripo/KR2a0020/17b6525eb5aaa878b9640f5a61e90da934ce5fc4/KR2a0020_035.txt
[930]: https://github.com/kanripo/KR2a0020/blob/17b6525eb5aaa878b9640f5a61e90da934ce5fc4/KR2a0020_038.txt
[934]: https://zh.wikisource.org/w/index.php?title=%E9%AD%8F%E6%9B%B8%2F%E5%8D%B758&oldid=2087998
[937]: https://zh.wikisource.org/w/index.php?oldid=1513418
[940]: https://zh.wikisource.org/w/index.php?title=魏書/卷67&oldid=468068
[944]: https://zh.wikisource.org/w/index.php?oldid=760052
[954]: https://zh.wikisource.org/w/index.php?title=周書/卷48&oldid=2432546
[974]: https://zh.wikisource.org/w/index.php?oldid=803184
[975]: https://zh.wikisource.org/w/index.php?oldid=2310031
[978]: https://github.com/kanripo/KR1e0004/blob/685a6ddca22d98535cac38038afdff7308273d23/KR1e0004_030.txt#L776-L776
[979]: https://zh.wikisource.org/w/index.php?title=史記/卷013&oldid=2606991
[981]: https://zh.wikisource.org/w/index.php?title=史記/卷015&oldid=2607002
[983]: https://zh.wikisource.org/w/index.php?title=史記/卷017&oldid=2607010
[984]: https://zh.wikisource.org/w/index.php?title=史記/卷018&oldid=9484995
[985]: https://zh.wikisource.org/w/index.php?title=史記/卷019&oldid=6359260
[986]: https://zh.wikisource.org/w/index.php?title=史記/卷020&oldid=2607036
[987]: https://zh.wikisource.org/w/index.php?title=史記/卷021&oldid=2607037
