# 人物 JSON 索引

可重建匯出，涵蓋目前已標註資料，包含明示選用的暫定跨篇同指；原 ID、證據與判讀均保留。並非全部史料或完整覆核。

程式可讀取 [index.json](index.json)，再依各筆 `path` 取得人物資料。重新產生：`python3 scripts/export_person_bundles.py`。

出生排行與籍貫結構化欄位仍在逐篇回填；缺欄位不代表來源沒有此資訊。提及頻次依固定見證的獨立位置計算；原始錨點完整保留，同位置節引重出另列raw／duplicate與對應群組，不代表來源權威度。

已接合父系見 [家族組裝資料](../../registry/family-assemblies.json)。`assembled_identity.person_id` 是共用家族根的組裝 ID，`source_person_ids` 保留各篇候選；父子及同指證據可由記錄 ID 回查。缺代節點另有 `ancestor_person_id`、`generation_distance` 與空值中間世代；父親空值不表示它另成一族。

點選家族標題可展開或收起後代。`*` 表示缺名世代，不建立人物，也不表示不同缺名位置是同一人。表內只列家族根後的 ID 尾碼；根人物以「根」表示，完整 ID 保留於家族標題及 JSON。最多提及來源另列一欄，同數並列；提及次數不代表史料優先權。已完成格式遷移的舊 ID 與 JSON 入口已撤除；待身份覆核的來源候選仍分存。

尚未連入同族的人物見 [獨立人物索引](unconnected.md)。

## 可展開家族


[第1頁](README.md) · [第2頁](families-002.md) · [第3頁](families-003.md)

<details><summary><code>f04_rc9_xqn</code> 太史敫（田世家候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 太史敫 | [《史記・田敬仲完世家》][1171] | [JSON](f04_rc9_xqn.json) |
| `A` | 君王后 | [《史記・田敬仲完世家》][1171] | [JSON](f04_rc9_xqn_A.json) |

</details>

<details><summary><code>f2z_47w_81j</code> 商玄石（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 商玄石 | [《宋書・謝晦》][1358]、[《宋書・謝晦》][1359] | [JSON](f2z_47w_81j.json) |
| `A` | 商懷福 | [《宋書・謝晦》][1358]、[《宋書・謝晦》][1359] | [JSON](f2z_47w_81j_A.json) |

</details>

<details><summary><code>f41_ulg_3u1</code> 衛滿（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 衛滿 | [《史記・朝鮮列傳》][1240] | [JSON](f41_ulg_3u1.json) |
| `*A` | 右渠 | [《史記・朝鮮列傳》][1240] | [JSON](f41_ulg_3u1_%2AA.json) |
| `*AA` | 長（右渠子） | [《史記・朝鮮列傳》][1240] | [JSON](f41_ulg_3u1_%2AAA.json) |

</details>

<details><summary><code>f56_938_997</code> 周瑜（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 周瑜 | [《三國志・周瑜魯肅呂蒙傳》][1065] | [JSON](f56_938_997.json) |
| `A` | 周氏〔周瑜女、孫登妃〕 | [《三國志・張嚴程闞薛傳》][1053]、[《三國志・周瑜魯肅呂蒙傳》][1065] | [JSON](f56_938_997_A.json) |
| `B` | 周胤 | [《三國志・周瑜魯肅呂蒙傳》][1065] | [JSON](f56_938_997_B.json) |

</details>

<details><summary><code>f84_da6_42a</code> 孔愉（5 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 孔愉 | [《晉書・孔愉 丁潭 陶回》][308] | [JSON](f84_da6_42a.json) |
| `A` | 孔誾（孔愉子、孔靖父） | [《南史・孔靖　孔琳之　殷景仁》][897] | [JSON](f84_da6_42a_A.json) |
| `AA` | 孔靖（字季恭，晉書作靜） | [《南史・孔靖　孔琳之　殷景仁》][897] | [JSON](f84_da6_42a_AA.json) |
| `AAA` | 孔靈運（孔琇之父） | [《南齊書・良政》][694]、[《南齊書・良政》][695] | [JSON](f84_da6_42a_AAA.json) |
| `AAAA` | 孔琇之（會稽山陰人，孔靈運子） | [《南齊書・良政》][695] | [JSON](f84_da6_42a_AAAA.json) |

</details>

<details><summary><code>f89_ad1_61d</code> 王凌（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 王凌 | [《三國志・王毌丘諸葛鄧鍾傳》][994] | [JSON](f89_ad1_61d.json) |
| `A` | 王廣 | [《三國志・王毌丘諸葛鄧鍾傳》][994] | [JSON](f89_ad1_61d_A.json) |

</details>

<details><summary><code>f8d_j5p_nop</code> 孔防叔（孔子世家候選）（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 孔防叔 | [《史記・孔子世家》][1172] | [JSON](f8d_j5p_nop.json) |
| `A` | 伯夏 | [《史記・孔子世家》][1172] | [JSON](f8d_j5p_nop_A.json) |
| `AA` | 叔梁紇 | [《史記・孔子世家》][1172] | [JSON](f8d_j5p_nop_AA.json) |

</details>

<details><summary><code>f90_933_c35</code> 猗盧（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 猗盧 | [《南齊書・魏虜》][710] | [JSON](f90_933_c35.json) |
| `A` | 日律孫 | [《晉書・王沈 荀顗 荀勖 馮紞》][208] | [JSON](f90_933_c35_A.json) |

</details>

<details><summary><code>faf_5al_ikw</code> 鄭武公（老韓列傳候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 鄭武公 | [《史記・老子韓非列傳》][1188] | [JSON](faf_5al_ikw.json) |
| `A` | 鄭武公之子 | [《史記・老子韓非列傳》][1188] | [JSON](faf_5al_ikw_A.json) |

</details>

<details><summary><code>fcu_pw8_tkw</code> 蔡興宗（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 蔡興宗 | [《南齊書・王秀之 王慈 蔡約 陸慧曉 顧憲之 蕭惠基》][649]、[《南齊書・王融 謝朓》][659]、[《南齊書・袁彖 孔稚珪 劉繪》][664]、[《南齊書・良政》][695]、[《南史・謝晦　謝裕　謝方明　謝靈運》][799]、[《南史・王曇首》][823]、[《南史・王曇首》][830]、[《南史・王曇首》][829]、[《宋書・徐湛之 江湛 王僧綽》][1514]、[《宋書・徐湛之 江湛 王僧綽》][1512]、[《宋書・徐湛之 江湛 王僧綽》][1513] | [JSON](fcu_pw8_tkw.json) |
| `A` | 蔡約 | [《南齊書・王秀之 王慈 蔡約 陸慧曉 顧憲之 蕭惠基》][649] | [JSON](fcu_pw8_tkw_A.json) |

</details>

<details><summary><code>fd3_tly_1lo</code> 沸（魯魏公）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 沸（魯魏公） | [《史記・魯周公世家》][1158] | [JSON](fd3_tly_1lo.json) |
| `A` | 擢（魯厲公） | [《史記・魯周公世家》][1158]、[《史記・三代世表》][1678] | [JSON](fd3_tly_1lo_A.json) |

</details>

<details><summary><code>fd5_0ae_506</code> 屈丐〔崔浩傳夏主〕（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 屈丐〔崔浩傳夏主〕 | [《宋書・朱齡石 毛脩之 傅弘之》][1411]、[《宋書・朱齡石 毛脩之 傅弘之》][1414]、[《魏書・崔浩》][1611] | [JSON](fd5_0ae_506.json) |
| `A` | 赫連璝（赫連勃勃長子，宋書作瓌） | [《宋書・朱齡石 毛脩之 傅弘之》][1411] | [JSON](fd5_0ae_506_A.json) |

</details>

<details><summary><code>fdb_6pb_gux</code> 蒯聵（太史公自序候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 蒯聵 | [《史記・太史公自序》][1255] | [JSON](fdb_6pb_gux.json) |
| `***A` | 司馬卬 | [《史記・高祖本紀》][1150]、[《史記・太史公自序》][1255] | [JSON](fdb_6pb_gux_%2A%2A%2AA.json) |

</details>

<details><summary><code>ffc_ea1_a8f</code> 范寧（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 范寧 | [《晉書・王湛 荀崧 范汪 劉惔 張憑 韓伯》][292] | [JSON](ffc_ea1_a8f.json) |
| `A` | 范泰 | [《宋書・趙倫之 王懿 張邵》][1377]、[《宋書・范泰 王准之 王韶之 荀伯子》][1495] | [JSON](ffc_ea1_a8f_A.json) |

</details>

<details><summary><code>fh0_oxc_05e</code> 韋旭（韋世康祖）（4 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 韋旭（韋世康祖） | [《隋書・列傳第12 韋世康 柳機》][1582] | [JSON](fh0_oxc_05e.json) |
| `A` | 韋夐（韋世康父） | [《隋書・列傳第12 韋世康 柳機》][1582] | [JSON](fh0_oxc_05e_A.json) |
| `AA` | 韋世康（京兆杜陵） | [《隋書・列傳第12 韋世康 柳機》][1582]、[《隋書・列傳第12 韋世康 柳機》][1583] | [JSON](fh0_oxc_05e_AA.json) |
| `AB` | 韋洸（字世穆） | [《隋書・列傳第12 韋世康 柳機》][1582] | [JSON](fh0_oxc_05e_AB.json) |

</details>

<details><summary><code>fjm_eo3_0zz</code> 始興王憺（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 始興王憺 | [《南史・王裕之　王鎮之　王韶之　王悅之　王准之》][886]、[《南史・王裕之　王鎮之　王韶之　王悅之　王准之》][871] | [JSON](fjm_eo3_0zz.json) |
| `A` | 繁昌主 | [《梁書・王瞻 王志 王峻 王暕 子訓 王泰 王份 孫鍚 僉 張充 柳惲 蔡撙 江蒨》][404]、[《南史・王裕之　王鎮之　王韶之　王悅之　王准之》][886]、[《南史・王裕之　王鎮之　王韶之　王悅之　王准之》][871] | [JSON](fjm_eo3_0zz_A.json) |

</details>

<details><summary><code>fmh_dmt_cql</code> 汲黯（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 汲黯 | [《史記・汲鄭列傳》][1245] | [JSON](fmh_dmt_cql.json) |
| `A` | 汲偃 | [《漢書・張馮汲鄭傳》][105]、[《史記・汲鄭列傳》][1245] | [JSON](fmh_dmt_cql_A.json) |

</details>

<details><summary><code>fo7_f8v_rmf</code> 梁武帝衍（14 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 梁武帝衍 | [《梁書・謝朏 弟子覽》][389] | [JSON](fo7_f8v_rmf.json) |
| `A` | 蕭玉姚 | [《梁書・皇后》][380]、[《梁書・皇后》][381]、[《梁書・陸倕 到洽 明山賓 殷鈞 陸襄》][427]、[《南史・后妃下》][762] | [JSON](fo7_f8v_rmf_A.json) |
| `B` | 蕭玉婉 | [《梁書・皇后》][380]、[《梁書・皇后》][381]、[《南史・后妃下》][762] | [JSON](fo7_f8v_rmf_B.json) |
| `C` | 蕭績（字世謹） | [《梁書・高祖三王》][445] | [JSON](fo7_f8v_rmf_C.json) |
| `CA` | 蕭會理（字長才，南康王績子） | [《梁書・高祖三王》][442] | [JSON](fo7_f8v_rmf_CA.json) |
| `CB` | 蕭通理（字仲宣，祁陽侯） | [《梁書・高祖三王》][442] | [JSON](fo7_f8v_rmf_CB.json) |
| `CC` | 蕭乂理（字季英，安樂侯） | [《梁書・高祖三王》][451] | [JSON](fo7_f8v_rmf_CC.json) |
| `D` | 蕭紀（武陵王） | [《梁書・高祖三王》][441]、[《梁書・豫章王綜 武陵王紀 臨賀王正德 河東王譽》][488] | [JSON](fo7_f8v_rmf_D.json) |
| `E` | 蕭玉志（梁安吉公主，王實妻） | [《南史・王誕　王華　王惠　王彧》][862] | [JSON](fo7_f8v_rmf_E.json) |
| `F` | 梁永嘉公主（王銓妻） | [《南史・王誕　王華　王惠　王彧》][844]、[《文獻通考・卷二百五十八》][1629] | [JSON](fo7_f8v_rmf_F.json) |
| `G` | 蕭續（梁廬陵威王） | [《梁書・高祖三王》][450] | [JSON](fo7_f8v_rmf_G.json) |
| `GA` | 蕭安（梁書所載蕭續長子） | [《梁書・高祖三王》][450] | [JSON](fo7_f8v_rmf_GA.json) |
| `H` | 蕭玉嬛（梁永康公主） | [《梁書・皇后》][381]、[《南史・后妃下》][762] | [JSON](fo7_f8v_rmf_H.json) |
| `I` | 長城公主（梁武帝女、柳偃妻） | [《陳書・皇后》][27] | [JSON](fo7_f8v_rmf_I.json) |

</details>

<details><summary><code>fom_gr9_c8v</code> 孫叔敖（循吏列傳候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 孫叔敖 | [《史記・循吏列傳》][1244]、[《史記・滑稽列傳》][1251] | [JSON](fom_gr9_c8v.json) |
| `A` | 孫叔敖子（未名） | [《史記・滑稽列傳》][1251] | [JSON](fom_gr9_c8v_A.json) |

</details>

<details><summary><code>fp6_ia6_7yw</code> 孔子（11 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 孔子 | [《史記・孔子世家》][1172] | [JSON](fp6_ia6_7yw.json) |
| `A` | 鯉 | [《史記・孔子世家》][1172] | [JSON](fp6_ia6_7yw_A.json) |
| `AA` | 伋 | [《史記・孔子世家》][1172] | [JSON](fp6_ia6_7yw_AA.json) |
| `AAA` | 白 | [《史記・孔子世家》][1172] | [JSON](fp6_ia6_7yw_AAA.json) |
| `AAAA` | 求 | [《史記・孔子世家》][1172] | [JSON](fp6_ia6_7yw_AAAA.json) |
| `AAAAA` | 箕 | [《史記・孔子世家》][1172] | [JSON](fp6_ia6_7yw_AAAAA.json) |
| `AAAAAA` | 穿 | [《史記・孔子世家》][1172] | [JSON](fp6_ia6_7yw_AAAAAA.json) |
| `AAAAAAA` | 子慎 | [《史記・孔子世家》][1172] | [JSON](fp6_ia6_7yw_AAAAAAA.json) |
| `AAAAAAAA` | 鮒 | [《史記・孔子世家》][1172] | [JSON](fp6_ia6_7yw_AAAAAAAA.json) |
| `B` | 孔鯉 | [《史記・仲尼弟子列傳》][1192] | [JSON](fp6_ia6_7yw_B.json) |
| `C` | 孔子之女 | [《史記・仲尼弟子列傳》][1192] | [JSON](fp6_ia6_7yw_C.json) |

</details>

<details><summary><code>fs1_z3i_d4r</code> 趙遐（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 趙遐 | [《崔混墓誌・節錄》][82] | [JSON](fs1_z3i_d4r.json) |
| `A` | 趙氏（崔混妻） | [《崔混墓誌・節錄》][82] | [JSON](fs1_z3i_d4r_A.json) |

</details>

<details><summary><code>fsr_uvs_8av</code> 蔣欽（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 蔣欽 | [《三國志・程黃韓蔣周陳董甘淩徐潘丁傳》][1075] | [JSON](fsr_uvs_8av.json) |
| `A` | 蔣壹 | [《三國志・程黃韓蔣周陳董甘淩徐潘丁傳》][1075] | [JSON](fsr_uvs_8av_A.json) |

</details>

<details><summary><code>fum_370_iq6</code> 結〔楊播高祖〕（28 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 結〔楊播高祖〕 | [《魏書・楊播》][1618] | [JSON](fum_370_iq6.json) |
| `A` | 珍〔楊播曾祖〕 | [《魏書・楊播》][1618]、[《魏書・楊播》][1619] | [JSON](fum_370_iq6_A.json) |
| `AA` | 真〔楊播祖〕 | [《楊舒墓誌・全文》][93]、[《魏書・楊播》][1618]、[《魏書・楊播》][1619] | [JSON](fum_370_iq6_AA.json) |
| `AAA` | 懿〔楊播父〕 | [《魏書・楊播》][1618] | [JSON](fum_370_iq6_AAA.json) |
| `AAAA` | 楊播 | [《魏書・楊播》][1618] | [JSON](fum_370_iq6_AAAA.json) |
| `AAAAA` | 侃〔楊播子，字士業〕 | [《魏書・楊播》][1618] | [JSON](fum_370_iq6_AAAAA.json) |
| `AAAAAA` | 師沖〔楊侃長子，北史作師仲〕 | [《魏書・楊播》][1618] | [JSON](fum_370_iq6_AAAAAA.json) |
| `AAAAAB` | 純陀〔楊侃嗣子〕 | [《魏書・楊播》][1618] | [JSON](fum_370_iq6_AAAAAB.json) |
| `AAAB` | 楊椿 | [《魏書・楊播》][1619] | [JSON](fum_370_iq6_AAAB.json) |
| `AAABA` | 楊昱 | [《魏書・楊播》][1619] | [JSON](fum_370_iq6_AAABA.json) |
| `AAABAA` | 孝邕〔楊昱子〕 | [《魏書・楊播》][1619] | [JSON](fum_370_iq6_AAABAA.json) |
| `AAAC` | 穎〔楊椿弟，字惠哲〕 | [《魏書・楊播》][1619] | [JSON](fum_370_iq6_AAAC.json) |
| `AAACA` | 叔良〔楊穎子〕 | [《魏書・楊播》][1619] | [JSON](fum_370_iq6_AAACA.json) |
| `AAAD` | 順〔楊穎弟，字延和〕 | [《魏書・楊播》][1619] | [JSON](fum_370_iq6_AAAD.json) |
| `AAADA` | 辯〔楊順子，字僧達〕 | [《魏書・楊播》][1619] | [JSON](fum_370_iq6_AAADA.json) |
| `AAADB` | 仲宣〔楊順子〕 | [《魏書・楊播》][1619] | [JSON](fum_370_iq6_AAADB.json) |
| `AAADBA` | 玄就〔楊仲宣子〕 | [《魏書・楊播》][1619] | [JSON](fum_370_iq6_AAADBA.json) |
| `AAADC` | 測〔楊仲宣弟〕 | [《魏書・楊播》][1619] | [JSON](fum_370_iq6_AAADC.json) |
| `AAADD` | 稚卿〔楊測弟〕 | [《魏書・楊播》][1619] | [JSON](fum_370_iq6_AAADD.json) |
| `AAAE` | 楊津〔字羅漢，本名延祚〕 | [《魏書・楊播》][1620] | [JSON](fum_370_iq6_AAAE.json) |
| `AAAEA` | 楊遁〔字山才，津長子〕 | [《魏書・楊播》][1620] | [JSON](fum_370_iq6_AAAEA.json) |
| `AAAEB` | 楊逸〔字遵道，津第二子〕 | [《魏書・楊播》][1620] | [JSON](fum_370_iq6_AAAEB.json) |
| `AAAEC` | 楊謐〔字遵智，逸弟〕 | [《魏書・楊播》][1620] | [JSON](fum_370_iq6_AAAEC.json) |
| `AAAED` | 楊遵彥〔謐弟〕 | [《北齊書・補列傳第二六 楊愔 燕子獻 宋欽道 鄭頤》][2] | [JSON](fum_370_iq6_AAAED.json) |
| `AAAF` | 楊暐〔字延季，津弟〕 | [《魏書・楊播》][1620] | [JSON](fum_370_iq6_AAAF.json) |
| `AAAFA` | 楊元讓〔暐子〕 | [《魏書・楊播》][1620] | [JSON](fum_370_iq6_AAAFA.json) |
| `AAB` | 洛州恒農簡公〔楊舒墓誌父〕 | [《楊舒墓誌・全文》][93] | [JSON](fum_370_iq6_AAB.json) |
| `AABA` | 舒〔楊昱第六叔〕 | [《楊舒墓誌・全文》][93] | [JSON](fum_370_iq6_AABA.json) |

</details>

<details><summary><code>fv1_k6x_jeu</code> 虛閭權渠單于（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 虛閭權渠單于 | [《漢書・匈奴傳》][113] | [JSON](fv1_k6x_jeu.json) |
| `A` | 呼韓邪單于（稽侯狦） | [《漢書・匈奴傳》][113] | [JSON](fv1_k6x_jeu_A.json) |

</details>

<details><summary><code>fvm_66f_0k3</code> 周緤（4 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 周緤 | [《史記・傅靳蒯成列傳》][1223] | [JSON](fvm_66f_0k3.json) |
| `A` | 周昌（蒯成侯之子） | [《漢書・樊酈滕灌傅靳周傳》][104]、[《史記・傅靳蒯成列傳》][1223]、[《史記・高祖功臣侯者年表》][1683] | [JSON](fvm_66f_0k3_A.json) |
| `C` | 周應 | [《漢書・樊酈滕灌傅靳周傳》][104] | [JSON](fvm_66f_0k3_C.json) |
| `CA` | 周仲居 | [《史記・高祖功臣侯者年表》][1683] | [JSON](fvm_66f_0k3_CA.json) |

</details>

<details><summary><code>g7w_9tv_iqb</code> 王僧辯（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 王僧辯 | [《梁書・裴邃 兄子之高 之平 之橫 夏侯亶 弟夔 魚弘附 韋放》][431] | [JSON](g7w_9tv_iqb.json) |
| `A` | 王僧辯女（杜龕妻） | [《南史・江子一　胡僧祐　徐文盛　陰子春　杜崱　王琳　張彪》][960] | [JSON](g7w_9tv_iqb_A.json) |

</details>

<details><summary><code>g83_41s_o52</code> 焦文珪（南安氐人，焦度祖）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 焦文珪（南安氐人，焦度祖） | [《南齊書・薛淵 戴僧靜 桓康 焦度 曹虎》][545] | [JSON](g83_41s_o52.json) |
| `*A` | 焦度（字文續） | [《南齊書・薛淵 戴僧靜 桓康 焦度 曹虎》][545] | [JSON](g83_41s_o52_%2AA.json) |

</details>

<details><summary><code>g9h_5ih_ug1</code> 伍奢（伍胥列傳候選）（4 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 伍奢 | [《史記・伍子胥列傳》][1191] | [JSON](g9h_5ih_ug1.json) |
| `A` | 伍子胥 | [《史記・伍子胥列傳》][1191] | [JSON](g9h_5ih_ug1_A.json) |
| `AA` | 伍子胥之子 | [《史記・伍子胥列傳》][1191] | [JSON](g9h_5ih_ug1_AA.json) |
| `B` | 伍尚 | [《史記・伍子胥列傳》][1191] | [JSON](g9h_5ih_ug1_B.json) |

</details>

<details><summary><code>ga6_jt5_6g1</code> 圉（衛孔文子）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 圉（衛孔文子） | [《史記・衛康叔世家》][1162] | [JSON](ga6_jt5_6g1.json) |
| `A` | 悝（衛孔氏） | [《史記・衛康叔世家》][1162] | [JSON](ga6_jt5_6g1_A.json) |

</details>

<details><summary><code>gcb_rf3_coi</code> 費王（晉穆侯）（4 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 費王（晉穆侯） | [《史記・晉世家》][1164] | [JSON](gcb_rf3_coi.json) |
| `A` | 仇（晉文侯） | [《史記・晉世家》][1164] | [JSON](gcb_rf3_coi_A.json) |
| `AA` | 伯（晉昭侯） | [《史記・晉世家》][1164] | [JSON](gcb_rf3_coi_AA.json) |
| `B` | 成師（曲沃桓叔） | [《史記・晉世家》][1164] | [JSON](gcb_rf3_coi_B.json) |

</details>

<details><summary><code>gcu_93j_y97</code> 鄭遵（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 鄭遵 | [《南史・范泰　荀伯子　徐廣　鄭鮮之　裴松之　何承天》][909] | [JSON](gcu_93j_y97.json) |
| `A` | 鄭鮮之 | [《南史・范泰　荀伯子　徐廣　鄭鮮之　裴松之　何承天》][909] | [JSON](gcu_93j_y97_A.json) |

</details>

<details><summary><code>gdj_k53_v1x</code> 王翦（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 王翦 | [《史記・白起王翦列傳》][1198] | [JSON](gdj_k53_v1x.json) |
| `*A` | 王離 | [《史記・白起王翦列傳》][1198] | [JSON](gdj_k53_v1x_%2AA.json) |
| `A` | 王賁 | [《史記・白起王翦列傳》][1198] | [JSON](gdj_k53_v1x_A.json) |

</details>

<details><summary><code>ghg_5p7_q21</code> 遂（杞釐公）（4 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 遂（杞釐公） | [《史記・陳杞世家》][1161] | [JSON](ghg_5p7_q21.json) |
| `A` | 維（杞湣公） | [《史記・陳杞世家》][1161] | [JSON](ghg_5p7_q21_A.json) |
| `AA` | 敕（杞出公） | [《史記・陳杞世家》][1161] | [JSON](ghg_5p7_q21_AA.json) |
| `AAA` | 春（杞簡公） | [《史記・陳杞世家》][1161] | [JSON](ghg_5p7_q21_AAA.json) |

</details>

<details><summary><code>gjl_f5h_2a6</code> 劉景猷（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 劉景猷 | [《南齊書・皇后》][528]、[《南齊書・皇后》][529]、[《南史・后妃上》][728]、[《南史・后妃上》][729] | [JSON](gjl_f5h_2a6.json) |
| `A` | 劉惠端 | [《南齊書・皇后》][528]、[《南齊書・皇后》][529]、[《南史・后妃上》][728]、[《南史・后妃上》][729]、[《昭明文選・卷五十八》][1632]、[《昭明文選・卷五十八》][1633]、[《昭明文選・卷五十八》][1634] | [JSON](gjl_f5h_2a6_A.json) |
| `B` | 劉暄 | [《南齊書・王晏 蕭諶 蕭坦之 江祏》][616] | [JSON](gjl_f5h_2a6_B.json) |

</details>

<details><summary><code>gke_14h_1xk</code> 宇（燕王）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 宇（燕王） | [《三國志・三少帝紀》][969]、[《三國志・諸夏侯曹傳》][970] | [JSON](gke_14h_1xk.json) |
| `A` | 曹奐〔字景明〕 | [《三國志・三少帝紀》][969] | [JSON](gke_14h_1xk_A.json) |

</details>

<details><summary><code>gm4_alk_hn7</code> 劉玄之（7 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 劉玄之 | [《南齊書・皇后》][519]、[《南齊書・皇后》][518]、[《南史・后妃上》][730]、[《南史・后妃上》][731] | [JSON](gm4_alk_hn7.json) |
| `A` | 劉壽之 | [《南齊書・皇后》][519]、[《南齊書・皇后》][518]、[《南史・后妃上》][730]、[《南史・后妃上》][731] | [JSON](gm4_alk_hn7_A.json) |
| `AA` | 劉智容 | [《南史・后妃上》][730]、[《南史・后妃上》][731] | [JSON](gm4_alk_hn7_AA.json) |
| `AB` | 劉興道 | [《南齊書・皇后》][519]、[《南齊書・皇后》][518] | [JSON](gm4_alk_hn7_AB.json) |
| `AC` | 劉文蔚 | [《南齊書・皇后》][519]、[《南齊書・皇后》][518] | [JSON](gm4_alk_hn7_AC.json) |
| `AD` | 劉義徽 | [《南齊書・皇后》][519]、[《南齊書・皇后》][518] | [JSON](gm4_alk_hn7_AD.json) |
| `AE` | 劉義倫 | [《南齊書・皇后》][519]、[《南齊書・皇后》][518] | [JSON](gm4_alk_hn7_AE.json) |

</details>

<details><summary><code>gn7_br7_32m</code> 伯州犁（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 伯州犁 | [《史記・吳太伯世家》][1156] | [JSON](gn7_br7_32m.json) |
| `*A` | 伯嚭 | [《史記・吳太伯世家》][1156] | [JSON](gn7_br7_32m_%2AA.json) |

</details>

<details><summary><code>goh_vpj_95z</code> 高賓（高熲父）（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 高賓（高熲父） | [《隋書・列傳第6 高熲 蘇威》][1581] | [JSON](goh_vpj_95z.json) |
| `A` | 高熲（字昭玄，一名敏） | [《隋書・列傳第6 高熲 蘇威》][1581] | [JSON](goh_vpj_95z_A.json) |
| `AA` | 高德弘（高熲子） | [《資治通鑑・隋紀一》][1673] | [JSON](goh_vpj_95z_AA.json) |

</details>

<details><summary><code>gpf_jcl_85k</code> 胡隨（胡藩祖）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 胡隨（胡藩祖） | [《宋書・胡藩 劉康祖 垣護之 張興世》][1450] | [JSON](gpf_jcl_85k.json) |
| `A` | 胡仲任（胡藩父） | [《宋書・胡藩 劉康祖 垣護之 張興世》][1450] | [JSON](gpf_jcl_85k_A.json) |

</details>

<details><summary><code>gqj_xdu_8rf</code> 張騫（李將軍列傳候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 張騫 | [《史記・大宛列傳》][1248] | [JSON](gqj_xdu_8rf.json) |
| `A` | 張騫子（未名） | [《史記・大宛列傳》][1248] | [JSON](gqj_xdu_8rf_A.json) |

</details>

<details><summary><code>gtj_19g_u2l</code> 殷道矜（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 殷道矜 | [《南齊書・王奐 從弟繢 張沖》][674] | [JSON](gtj_19g_u2l.json) |
| `A` | 殷恒（字昭度，殷道矜子） | [《南齊書・王奐 從弟繢 張沖》][674] | [JSON](gtj_19g_u2l_A.json) |

</details>

<details><summary><code>gts_42q_flu</code> 睔（鄭世家成公候選）（7 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 睔 | [《史記・鄭世家》][1167] | [JSON](gts_42q_flu.json) |
| `A` | 惲 | [《史記・鄭世家》][1167] | [JSON](gts_42q_flu_A.json) |
| `AA` | 嘉 | [《史記・鄭世家》][1167] | [JSON](gts_42q_flu_AA.json) |
| `AAA` | 寧 | [《史記・鄭世家》][1167] | [JSON](gts_42q_flu_AAA.json) |
| `AAAA` | 蠆 | [《史記・鄭世家》][1167] | [JSON](gts_42q_flu_AAAA.json) |
| `AAAAA` | 勝 | [《史記・鄭世家》][1167] | [JSON](gts_42q_flu_AAAAA.json) |
| `AAAAAA` | 易 | [《史記・鄭世家》][1167] | [JSON](gts_42q_flu_AAAAAA.json) |

</details>

<details><summary><code>gyg_hql_qdj</code> 慕容永（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 慕容永 | [《晉書・溫嶠 郗鑒》][277] | [JSON](gyg_hql_qdj.json) |
| `A` | 慕容弘〔常山公、慕容永子〕 | [《晉書・溫嶠 郗鑒》][277]、[《資治通鑑・晉紀三十》][1658] | [JSON](gyg_hql_qdj_A.json) |

</details>

<details><summary><code>gzc_9vs_o43</code> 孟嘉〔字萬年〕（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 孟嘉〔字萬年〕 | [《晉書・叛臣一》][345] | [JSON](gzc_9vs_o43.json) |
| `A` | 孟氏〔孟嘉第四女、陶淵明母〕 | — | [JSON](gzc_9vs_o43_A.json) |

</details>

<details><summary><code>h15_bxq_n5u</code> 周優〔周翼父〕（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 周優〔周翼父〕 | [《世說新語・德行》][1260] | [JSON](h15_bxq_n5u.json) |
| `A` | 周翼〔字子卿，郗鑒外甥〕 | [《世說新語・德行》][1260] | [JSON](h15_bxq_n5u_A.json) |

</details>

<details><summary><code>h1w_44g_vef</code> 張孟（魏其武安侯列傳候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 張孟 | [《史記・魏其武安列傳》][1232] | [JSON](h1w_44g_vef.json) |
| `A` | 灌夫 | [《史記・魏其武安列傳》][1232] | [JSON](h1w_44g_vef_A.json) |

</details>

<details><summary><code>h4f_d5f_vdl</code> 蟬封（大宛列傳候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 蟬封 | [《史記・大宛列傳》][1248] | [JSON](h4f_d5f_vdl.json) |
| `A` | 蟬封子（入質，未名） | [《史記・大宛列傳》][1248] | [JSON](h4f_d5f_vdl_A.json) |

</details>

<details><summary><code>h6m_t08_wbd</code> 顧向（5 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 顧向 | [《三國志・張顧諸葛步傳》][1042] | [JSON](h6m_t08_wbd.json) |
| `A` | 顧悌 | [《三國志・張顧諸葛步傳》][1042] | [JSON](h6m_t08_wbd_A.json) |
| `AA` | 顧彥〔顧悌子〕 | [《三國志・張顧諸葛步傳》][1042] | [JSON](h6m_t08_wbd_AA.json) |
| `AB` | 顧禮 | [《三國志・張顧諸葛步傳》][1042] | [JSON](h6m_t08_wbd_AB.json) |
| `AC` | 顧謙 | [《三國志・張顧諸葛步傳》][1042] | [JSON](h6m_t08_wbd_AC.json) |

</details>

<details><summary><code>h7n_w5t_i1c</code> 曹休未名祖父（7 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 曹休未名祖父 | [《三國志・諸夏侯曹傳》][970] | [JSON](h7n_w5t_i1c.json) |
| `A` | 曹休未名父 | [《三國志・諸夏侯曹傳》][970] | [JSON](h7n_w5t_i1c_A.json) |
| `AA` | 曹休 | [《三國志・諸夏侯曹傳》][970] | [JSON](h7n_w5t_i1c_AA.json) |
| `AAA` | 肇（曹攄祖、曹休子） | [《三國志・諸夏侯曹傳》][970] | [JSON](h7n_w5t_i1c_AAA.json) |
| `AAA*A` | 曹顏遠 | [《晉書・良吏》][320] | [JSON](h7n_w5t_i1c_AAA%2AA.json) |
| `AAAA` | 興（肇子） | [《三國志・諸夏侯曹傳》][970] | [JSON](h7n_w5t_i1c_AAAA.json) |
| `AAB` | 纂（肇弟） | [《三國志・諸夏侯曹傳》][970] | [JSON](h7n_w5t_i1c_AAB.json) |

</details>

<details><summary><code>h9n_acw_xpo</code> 戴碩子（法興父）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 戴碩子（法興父） | [《宋書・恩倖》][1574] | [JSON](h9n_acw_xpo.json) |
| `A` | 戴法興（會稽山陰人） | [《宋書・恩倖》][1574] | [JSON](h9n_acw_xpo_A.json) |

</details>

<details><summary><code>hb9_2gq_205</code> 袁昂〔吳郡不降梁〕（5 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 袁昂〔吳郡不降梁〕 | [《南史・王曇首》][835] | [JSON](hb9_2gq_205.json) |
| `A` | 袁君正（梁吳郡太守，字世忠） | [《南史・袁湛》][895] | [JSON](hb9_2gq_205_A.json) |
| `AA` | 袁樞（陳尚書左僕射，字踐言） | [《陳書・列傳第十一: 王沖 王通 袁敬》][55] | [JSON](hb9_2gq_205_AA.json) |
| `B` | 袁敬（陳左光祿大夫，字子恭） | [《陳書・列傳第十一: 王沖 王通 袁敬》][54] | [JSON](hb9_2gq_205_B.json) |
| `BA` | 袁元友（袁敬子） | [《陳書・列傳第十一: 王沖 王通 袁敬》][54] | [JSON](hb9_2gq_205_BA.json) |

</details>

<details><summary><code>hgm_jvn_hle</code> 晉武帝（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 晉武帝 | [《晉書・王沈 荀顗 荀勖 馮紞》][208] | [JSON](hgm_jvn_hle.json) |
| `A` | 襄城公主〔晉武帝女、王敦妻〕 | [《晉書・叛臣一》][344] | [JSON](hgm_jvn_hle_A.json) |
| `B` | 滎陽公主〔晉武帝女〕 | [《晉書・鄭袤 李胤 盧欽 華表 石鑒 溫羨》][228] | [JSON](hgm_jvn_hle_B.json) |

</details>

<details><summary><code>hx8_hzi_iq5</code> 孫處（字季高）（4 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 孫處（字季高） | [《宋書・孫處 蒯恩 劉鍾 虞丘進》][1438] | [JSON](hx8_hzi_iq5.json) |
| `A` | 孫宗世（孫處子） | [《宋書・孫處 蒯恩 劉鍾 虞丘進》][1437]、[《宋書・孫處 蒯恩 劉鍾 虞丘進》][1441] | [JSON](hx8_hzi_iq5_A.json) |
| `AA` | 孫欽公（孫宗世子） | [《宋書・孫處 蒯恩 劉鍾 虞丘進》][1437]、[《宋書・孫處 蒯恩 劉鍾 虞丘進》][1439] | [JSON](hx8_hzi_iq5_AA.json) |
| `AAA` | 孫彥祖（孫欽公子） | [《宋書・孫處 蒯恩 劉鍾 虞丘進》][1437]、[《宋書・孫處 蒯恩 劉鍾 虞丘進》][1440] | [JSON](hx8_hzi_iq5_AAA.json) |

</details>

<details><summary><code>hx8_st4_jdd</code> 宋孝武帝駿（15 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 宋孝武帝駿 | [《宋書・殷淳 張暢 何偃 江智淵》][1494] | [JSON](hx8_st4_jdd.json) |
| `A` | 安固公主（宋孝武女） | [《梁書・王瞻 王志 王峻 王暕 子訓 王泰 王份 孫鍚 僉 張充 柳惲 蔡撙 江蒨》][410]、[《梁書・王瞻 王志 王峻 王暕 子訓 王泰 王份 孫鍚 僉 張充 柳惲 蔡撙 江蒨》][409]、[《南史・王曇首》][840]、[《南史・王曇首》][839] | [JSON](hx8_st4_jdd_A.json) |
| `B` | 永嘉王子仁 | [《宋書・孝武十四王》][1531] | [JSON](hx8_st4_jdd_B.json) |
| `C` | 劉楚玉（山陰公主） | [《南齊書・王琨 張岱 褚炫 何戢 王延之 阮韜》][550]、[《南史・后妃上》][744]、[《南史・后妃上》][745]、[《宋書・后妃》][1351] | [JSON](hx8_st4_jdd_C.json) |
| `D` | 劉楚佩（臨淮康哀公主） | [《南史・后妃上》][744]、[《南史・后妃上》][745]、[《宋書・后妃》][1351] | [JSON](hx8_st4_jdd_D.json) |
| `E` | 劉楚琇（宋孝武皇女） | [《南史・后妃上》][744]、[《南史・后妃上》][745]、[《宋書・后妃》][1351] | [JSON](hx8_st4_jdd_E.json) |
| `F` | 劉脩明（康樂公主） | [《南齊書・徐孝嗣 沈文季》][637]、[《南史・后妃上》][744]、[《南史・后妃上》][745]、[《宋書・后妃》][1351] | [JSON](hx8_st4_jdd_F.json) |
| `G` | 臨汝公主（宋孝武帝女，江斆妻） | [《南齊書・江斆 何昌㝢 謝𤅢 王思遠》][628]、[《南齊書・江斆 何昌㝢 謝𤅢 王思遠》][629]、[《南史・王誕　王華　王惠　王彧》][865] | [JSON](hx8_st4_jdd_G.json) |
| `H` | 劉子真（始安王，字孝貞） | [《宋書・孝武十四王》][1526] | [JSON](hx8_st4_jdd_H.json) |
| `I` | 劉子產（宋臨賀王，字孝仁） | [《宋書・文九王》][1516] | [JSON](hx8_st4_jdd_I.json) |
| `J` | 劉子羽（齊敬王，字孝英） | [《宋書・孝武十四王》][1529] | [JSON](hx8_st4_jdd_J.json) |
| `K` | 劉子雲（晉陵孝王，字孝舉） | [《宋書・孝武十四王》][1529] | [JSON](hx8_st4_jdd_K.json) |
| `L` | 劉子文（宋孝武皇子） | [《宋書・孝武十四王》][1527] | [JSON](hx8_st4_jdd_L.json) |
| `M` | 劉子師（南海哀王，字孝友） | [《宋書・孝武十四王》][1528] | [JSON](hx8_st4_jdd_M.json) |
| `N` | 宋孝武帝第十二皇女（子鸞同生妹） | — | [JSON](hx8_st4_jdd_N.json) |

</details>

<details><summary><code>hxn_tox_kna</code> 宗叔獻（宗靈秀父）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 宗叔獻（宗靈秀父） | [《宋書・朱脩之 宗愨 王玄謨》][1522] | [JSON](hxn_tox_kna.json) |
| `A` | 宗靈秀（宋黃門侍郎） | [《宋書・朱脩之 宗愨 王玄謨》][1522] | [JSON](hxn_tox_kna_A.json) |

</details>

<details><summary><code>i08_s4b_5bb</code> 王晏〔齊尚書令〕（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 王晏〔齊尚書令〕 | [《南史・王裕之　王鎮之　王韶之　王悅之　王准之》][882] | [JSON](i08_s4b_5bb.json) |
| `A` | 王德元（王晏子，初名湛） | [《南齊書・王晏 蕭諶 蕭坦之 江祏》][617]、[《南史・王裕之　王鎮之　王韶之　王悅之　王准之》][869] | [JSON](i08_s4b_5bb_A.json) |
| `B` | 王德和（王德元弟） | [《南齊書・王晏 蕭諶 蕭坦之 江祏》][617] | [JSON](i08_s4b_5bb_B.json) |

</details>

<details><summary><code>i30_mjq_6q8</code> 呂公（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 呂公 | [《史記・高祖本紀》][1150] | [JSON](i30_mjq_6q8.json) |
| `A` | 呂后 | [《史記・呂后本紀》][1151] | [JSON](i30_mjq_6q8_A.json) |

</details>

<details><summary><code>i3f_9l9_g53</code> 陳平（5 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 陳平 | [《史記・陳丞相世家》][1181] | [JSON](i3f_9l9_g53.json) |
| `**A` | 陳掌 | [《史記・陳丞相世家》][1181] | [JSON](i3f_9l9_g53_%2A%2AA.json) |
| `A` | 買 | [《史記・陳丞相世家》][1181] | [JSON](i3f_9l9_g53_A.json) |
| `AA` | 恢 | [《史記・陳丞相世家》][1181] | [JSON](i3f_9l9_g53_AA.json) |
| `AAA` | 何 | [《史記・陳丞相世家》][1181] | [JSON](i3f_9l9_g53_AAA.json) |

</details>

<details><summary><code>i5r_vby_q00</code> 殷禮（4 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 殷禮 | [《三國志・張顧諸葛步傳》][1040] | [JSON](i5r_vby_q00.json) |
| `A` | 殷基 | [《三國志・張顧諸葛步傳》][1040] | [JSON](i5r_vby_q00_A.json) |
| `AA` | 殷巨 | [《三國志・張顧諸葛步傳》][1040] | [JSON](i5r_vby_q00_AA.json) |
| `AB` | 殷祐 | [《三國志・張顧諸葛步傳》][1040] | [JSON](i5r_vby_q00_AB.json) |

</details>

<details><summary><code>i7a_22p_qda</code> 句踐（7 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 句踐 | [《史記・越王勾踐世家》][1166] | [JSON](i7a_22p_qda.json) |
| `A` | 鼫與 | [《史記・越王勾踐世家》][1166] | [JSON](i7a_22p_qda_A.json) |
| `AA` | 不壽 | [《史記・越王勾踐世家》][1166] | [JSON](i7a_22p_qda_AA.json) |
| `AAA` | 翁 | [《史記・越王勾踐世家》][1166] | [JSON](i7a_22p_qda_AAA.json) |
| `AAAA` | 翳 | [《史記・越王勾踐世家》][1166] | [JSON](i7a_22p_qda_AAAA.json) |
| `AAAAA` | 之侯 | [《史記・越王勾踐世家》][1166] | [JSON](i7a_22p_qda_AAAAA.json) |
| `AAAAAA` | 無彊 | [《史記・越王勾踐世家》][1166] | [JSON](i7a_22p_qda_AAAAAA.json) |

</details>

<details><summary><code>i8i_rvh_4lp</code> 燬（衛文公）（8 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 燬（衛文公） | [《史記・衛康叔世家》][1162] | [JSON](i8i_rvh_4lp.json) |
| `A` | 鄭（衛成公） | [《史記・衛康叔世家》][1162] | [JSON](i8i_rvh_4lp_A.json) |
| `AA` | 遫（衛穆公） | [《史記・衛康叔世家》][1162] | [JSON](i8i_rvh_4lp_AA.json) |
| `AAA` | 臧（衛定公） | [《史記・衛康叔世家》][1162] | [JSON](i8i_rvh_4lp_AAA.json) |
| `AAAA` | 衎（衛獻公） | [《史記・衛康叔世家》][1162] | [JSON](i8i_rvh_4lp_AAAA.json) |
| `AAAAA` | 惡（衛襄公） | [《史記・衛康叔世家》][1162] | [JSON](i8i_rvh_4lp_AAAAA.json) |
| `AAAAAA` | 元（衛靈公） | [《史記・衛康叔世家》][1162] | [JSON](i8i_rvh_4lp_AAAAAA.json) |
| `AAAAAAA` | 郢（衛子南） | [《史記・衛康叔世家》][1162] | [JSON](i8i_rvh_4lp_AAAAAAA.json) |

</details>

<details><summary><code>i9w_mm6_m7t</code> 顧謙（字公讓，顧覬之高祖）（4 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 顧謙（字公讓，顧覬之高祖） | [《宋書・劉秀之 顧琛 顧覬之》][1533] | [JSON](i9w_mm6_m7t.json) |
| `*A` | 顧崇（大司農，顧覬之祖） | [《宋書・劉秀之 顧琛 顧覬之》][1533] | [JSON](i9w_mm6_m7t_%2AA.json) |
| `*AA` | 顧黃老（司徒左西掾） | [《宋書・劉秀之 顧琛 顧覬之》][1533] | [JSON](i9w_mm6_m7t_%2AAA.json) |
| `*AAA` | 顧覬之（字偉仁，山陰令） | [《南齊書・張融 周顒》][612] | [JSON](i9w_mm6_m7t_%2AAAA.json) |

</details>

<details><summary><code>ibt_i7u_ykp</code> 呂蒙〔字子明〕（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 呂蒙〔字子明〕 | [《三國志・周瑜魯肅呂蒙傳》][1064] | [JSON](ibt_i7u_ykp.json) |
| `A` | 呂霸 | [《三國志・周瑜魯肅呂蒙傳》][1064] | [JSON](ibt_i7u_ykp_A.json) |

</details>

<details><summary><code>iby_117_6rw</code> 黃蓋（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 黃蓋 | [《三國志・程黃韓蔣周陳董甘淩徐潘丁傳》][1074] | [JSON](iby_117_6rw.json) |
| `A` | 黃柄 | [《三國志・程黃韓蔣周陳董甘淩徐潘丁傳》][1074] | [JSON](iby_117_6rw_A.json) |

</details>

<details><summary><code>icd_mkz_d9n</code> 陳宣帝頊（10 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 陳宣帝頊 | [《陳書・列傳第十七: 沈君理 王瑒 陸繕》][61]、[《陳書・列傳第十七: 沈君理 王瑒 陸繕》][63] | [JSON](icd_mkz_d9n.json) |
| `A` | 陳叔寶（陳後主） | [《陳書・列傳第三十: 始興王叔陵 新安王伯固》][79] | [JSON](icd_mkz_d9n_A.json) |
| `AA` | 陳深（字承源，陳後主皇太子） | [《陳書・列傳第二十二: 世祖九王 高宗二十九王 後主諸子》][76] | [JSON](icd_mkz_d9n_AA.json) |
| `AB` | 陳胤（字承業，吳興王） | [《陳書・列傳第二十二: 世祖九王 高宗二十九王 後主諸子》][74] | [JSON](icd_mkz_d9n_AB.json) |
| `AC` | 陳莊（字承肅，會稽王） | [《陳書・列傳第二十二: 世祖九王 高宗二十九王 後主諸子》][76] | [JSON](icd_mkz_d9n_AC.json) |
| `AD` | 陳虔（字承恪，南海王） | [《陳書・列傳第二十二: 世祖九王 高宗二十九王 後主諸子》][76] | [JSON](icd_mkz_d9n_AD.json) |
| `AE` | 陳恬（字承惔，錢塘王） | [《陳書・列傳第二十二: 世祖九王 高宗二十九王 後主諸子》][76] | [JSON](icd_mkz_d9n_AE.json) |
| `B` | 陳叔陵（陳宣帝第二子，始興王） | [《陳書・列傳第三十: 始興王叔陵 新安王伯固》][79] | [JSON](icd_mkz_d9n_B.json) |
| `C` | 陳叔獻（字子恭，河東王） | [《陳書・列傳第二十二: 世祖九王 高宗二十九王 後主諸子》][71] | [JSON](icd_mkz_d9n_C.json) |
| `D` | 陳叔堅（字子成，陳宣帝第四子） | [《陳書・列傳第二十二: 世祖九王 高宗二十九王 後主諸子》][72] | [JSON](icd_mkz_d9n_D.json) |

</details>

<details><summary><code>icr_lwq_9mp</code> 孫匡（4 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 孫匡 | [《三國志・宗室傳》][1033] | [JSON](icr_lwq_9mp.json) |
| `A` | 孫泰〔孫匡子、曹氏甥〕 | [《三國志・宗室傳》][1033] | [JSON](icr_lwq_9mp_A.json) |
| `AA` | 孫秀〔孫泰子、吳夏口督奔晉〕 | [《三國志・宗室傳》][1033] | [JSON](icr_lwq_9mp_AA.json) |
| `AAA` | 孫儉〔孫秀子、字仲節〕 | [《三國志・宗室傳》][1033] | [JSON](icr_lwq_9mp_AAA.json) |

</details>

<details><summary><code>ier_lqj_x4q</code> 郗愔（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 郗愔 | [《晉書・溫嶠 郗鑒》][273] | [JSON](ier_lqj_x4q.json) |
| `A` | 郗融 | [《晉書・溫嶠 郗鑒》][279]、[《晉書・溫嶠 郗鑒》][278] | [JSON](ier_lqj_x4q_A.json) |
| `B` | 郗沖 | [《晉書・溫嶠 郗鑒》][279]、[《晉書・溫嶠 郗鑒》][278] | [JSON](ier_lqj_x4q_B.json) |

</details>

<details><summary><code>iij_zqi_k5l</code> 齊平公（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 齊平公 | [《史記・齊太公世家》][1157] | [JSON](iij_zqi_k5l.json) |
| `A` | 積（齊宣公） | [《史記・齊太公世家》][1157] | [JSON](iij_zqi_k5l_A.json) |
| `AA` | 貸（齊康公） | [《史記・齊太公世家》][1157] | [JSON](iij_zqi_k5l_AA.json) |

</details>

<details><summary><code>ijh_3fs_6u2</code> 豫章王嶷（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 豫章王嶷 | [《南齊書・高逸》][702] | [JSON](ijh_3fs_6u2.json) |
| `A` | 蕭子恪（齊豫章王嶷第二子） | [《梁書・蕭子恪 弟子範 子顯 子雲》][460]、[《南齊書・武十七王》][586] | [JSON](ijh_3fs_6u2_A.json) |
| `B` | 蕭子範（梁書卷七作子范，字景則） | [《梁書・蕭子恪 弟子範 子顯 子雲》][460] | [JSON](ijh_3fs_6u2_B.json) |

</details>

<details><summary><code>inr_w1g_bu5</code> 子襄（孔子世家候選）（7 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 子襄 | [《史記・孔子世家》][1172] | [JSON](inr_w1g_bu5.json) |
| `A` | 忠 | [《史記・孔子世家》][1172] | [JSON](inr_w1g_bu5_A.json) |
| `AA` | 武 | [《史記・孔子世家》][1172] | [JSON](inr_w1g_bu5_AA.json) |
| `AAA` | 延年 | [《史記・孔子世家》][1172] | [JSON](inr_w1g_bu5_AAA.json) |
| `AAB` | 安國 | [《史記・孔子世家》][1172] | [JSON](inr_w1g_bu5_AAB.json) |
| `AABA` | 卬 | [《史記・孔子世家》][1172] | [JSON](inr_w1g_bu5_AABA.json) |
| `AABAA` | 驩 | [《史記・孔子世家》][1172] | [JSON](inr_w1g_bu5_AABAA.json) |

</details>

<details><summary><code>ipq_o9t_wdh</code> 南郡王長懋（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 南郡王長懋 | [《南齊書・張融 周顒》][614] | [JSON](ipq_o9t_wdh.json) |
| `A` | 蕭昭秀（字懷尚，巴陵王） | [《南齊書・文二王 明七王》][681] | [JSON](ipq_o9t_wdh_A.json) |
| `B` | 蕭昭粲（文惠太子第四子，桂陽王） | [《南齊書・文二王 明七王》][681] | [JSON](ipq_o9t_wdh_B.json) |

</details>

<details><summary><code>itp_cr4_7pm</code> 沈法深（沈妙容父）（4 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 沈法深（沈妙容父） | [《陳書・皇后》][28]、[《陳書・皇后》][31]、[《南史・后妃下》][759] | [JSON](itp_cr4_7pm.json) |
| `A` | 沈妙容（陳文帝皇后） | [《陳書・皇后》][28]、[《陳書・皇后》][31]、[《陳書・列傳第二十二: 世祖九王 高宗二十九王 後主諸子》][73]、[《南史・后妃下》][759] | [JSON](itp_cr4_7pm_A.json) |
| `B` | 沈欽（沈妙容兄） | [《陳書・皇后》][28]、[《南史・后妃下》][759] | [JSON](itp_cr4_7pm_B.json) |
| `BA` | 沈觀（沈欽子） | [《陳書・皇后》][28]、[《陳書・皇后》][31]、[《南史・后妃下》][759] | [JSON](itp_cr4_7pm_BA.json) |

</details>

<details><summary><code>iuc_mqu_3jm</code> 周魴（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 周魴 | [《三國志・賀全呂周鍾離傳》][1115] | [JSON](iuc_mqu_3jm.json) |
| `A` | 周處〔字子隱，周魴子〕 | [《三國志・賀全呂周鍾離傳》][1115] | [JSON](iuc_mqu_3jm_A.json) |

</details>

<details><summary><code>iuq_5o2_wum</code> 江逌（江秉之祖，晉太常）（5 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 江逌（江秉之祖，晉太常） | [《宋書・良吏》][1551] | [JSON](iuq_5o2_wum.json) |
| `A` | 江纂（給事中，江秉之父） | [《宋書・良吏》][1551] | [JSON](iuq_5o2_wum_A.json) |
| `AA` | 江秉之（字玄叔） | [《宋書・良吏》][1551] | [JSON](iuq_5o2_wum_AA.json) |
| `AAA` | 江徽（江秉之子，吳令） | [《宋書・良吏》][1552] | [JSON](iuq_5o2_wum_AAA.json) |
| `AAAA` | 江謐（字令和，江徽子） | [《南齊書・江謐 荀伯玉》][546] | [JSON](iuq_5o2_wum_AAAA.json) |

</details>

<details><summary><code>ixk_6fg_v6f</code> 竇后父（外戚世家候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 竇后父 | [《史記・外戚世家》][1174] | [JSON](ixk_6fg_v6f.json) |
| `A` | 竇太后（孝文帝皇后） | [《史記・梁孝王世家》][1183] | [JSON](ixk_6fg_v6f_A.json) |

</details>

<details><summary><code>izi_e36_p1g</code> 虞翻（4 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 虞翻 | [《三國志・虞陸張駱陸吾朱傳》][1096] | [JSON](izi_e36_p1g.json) |
| `A` | 虞忠 | [《三國志・虞陸張駱陸吾朱傳》][1095] | [JSON](izi_e36_p1g_A.json) |
| `B` | 虞聳 | [《三國志・虞陸張駱陸吾朱傳》][1095] | [JSON](izi_e36_p1g_B.json) |
| `C` | 虞昺 | [《三國志・虞陸張駱陸吾朱傳》][1095] | [JSON](izi_e36_p1g_C.json) |

</details>

<details><summary><code>j32_wtj_khz</code> 袁盎父未名（袁盎鼂錯列傳候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 袁盎父未名 | [《史記・袁盎鼂錯列傳》][1226] | [JSON](j32_wtj_khz.json) |
| `A` | 袁盎 | [《史記・袁盎鼂錯列傳》][1226] | [JSON](j32_wtj_khz_A.json) |

</details>

<details><summary><code>j6f_ufq_av2</code> 沈瑀（字伯瑜）（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 沈瑀（字伯瑜） | [《陳書・列傳第十三: 沈炯 虞荔 馬樞》][57] | [JSON](j6f_ufq_av2.json) |
| `A` | 沈續（王府記室參軍） | [《陳書・列傳第十三: 沈炯 虞荔 馬樞》][57] | [JSON](j6f_ufq_av2_A.json) |
| `AA` | 沈炯（字禮明） | [《陳書・列傳第十三: 沈炯 虞荔 馬樞》][57]、[《梁書・韋粲 江子一 弟子四 子五 張嵊 沈浚 柳敬禮》][465] | [JSON](j6f_ufq_av2_AA.json) |

</details>

<details><summary><code>jfc_0dt_42a</code> 顧秘（5 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 顧秘 | [《晉書・羅憲 滕脩 馬隆 胡奮 陶璜 吾彥 張光 趙誘》][255]、[《晉書・王舒 王廙 虞潭 顧眾 張闓》][295]、[《三國志・張顧諸葛步傳》][1042] | [JSON](jfc_0dt_42a.json) |
| `A` | 顧衆 | [《晉書・王舒 王廙 虞潭 顧眾 張闓》][295] | [JSON](jfc_0dt_42a_A.json) |
| `AA` | 顧昌 | [《晉書・王舒 王廙 虞潭 顧眾 張闓》][295] | [JSON](jfc_0dt_42a_AA.json) |
| `AB` | 顧會 | [《晉書・王舒 王廙 虞潭 顧眾 張闓》][295] | [JSON](jfc_0dt_42a_AB.json) |
| `B` | 顧參 | [《晉書・羅憲 滕脩 馬隆 胡奮 陶璜 吾彥 張光 趙誘》][255] | [JSON](jfc_0dt_42a_B.json) |

</details>

<details><summary><code>jg1_ag9_033</code> 老子（孔子世家候選）（4 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 老子 | [《史記・老子韓非列傳》][1188] | [JSON](jg1_ag9_033.json) |
| `A` | 宗 | [《史記・老子韓非列傳》][1188] | [JSON](jg1_ag9_033_A.json) |
| `AA` | 注 | [《史記・老子韓非列傳》][1188] | [JSON](jg1_ag9_033_AA.json) |
| `AAA` | 宮 | [《史記・老子韓非列傳》][1188] | [JSON](jg1_ag9_033_AAA.json) |

</details>

<details><summary><code>jgo_o5m_l1f</code> 劉秉（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 劉秉 | [《南齊書・王秀之 王慈 蔡約 陸慧曉 顧憲之 蕭惠基》][655] | [JSON](jgo_o5m_l1f.json) |
| `A` | 劉秉女（王慈妻） | [《南齊書・王秀之 王慈 蔡約 陸慧曉 顧憲之 蕭惠基》][653] | [JSON](jgo_o5m_l1f_A.json) |

</details>

<details><summary><code>jhj_lss_ks5</code> 顧徽（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 顧徽 | [《三國志・張顧諸葛步傳》][1042] | [JSON](jhj_lss_ks5.json) |
| `A` | 顧裕〔字季則〕 | [《三國志・張顧諸葛步傳》][1042] | [JSON](jhj_lss_ks5_A.json) |

</details>

<details><summary><code>jjl_irg_zke</code> 盧綰父未名（韓信盧綰列傳候選）（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 盧綰父未名 | [《史記・韓信盧綰列傳》][1218] | [JSON](jjl_irg_zke.json) |
| `A` | 盧綰 | [《史記・韓信盧綰列傳》][1218] | [JSON](jjl_irg_zke_A.json) |
| `A*A` | 盧他之 | [《史記・韓信盧綰列傳》][1218] | [JSON](jjl_irg_zke_A%2AA.json) |

</details>

<details><summary><code>jo4_4bf_0ra</code> 劉澤（5 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 劉澤 | [《史記・荊燕世家》][1176] | [JSON](jo4_4bf_0ra.json) |
| `A` | 嘉（燕康王） | [《史記・荊燕世家》][1176] | [JSON](jo4_4bf_0ra_A.json) |
| `AA` | 定國 | [《史記・荊燕世家》][1176] | [JSON](jo4_4bf_0ra_AA.json) |
| `AAA` | 定國所生男（荊燕世家未名者） | [《史記・荊燕世家》][1176] | [JSON](jo4_4bf_0ra_AAA.json) |
| `AB` | 田蚡夫人（燕康王女，未名） | [《史記・魏其武安列傳》][1232] | [JSON](jo4_4bf_0ra_AB.json) |

</details>

<details><summary><code>jqx_jns_jae</code> 虞豫（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 虞豫 | [《晉書・后妃下》][199] | [JSON](jqx_jns_jae.json) |
| `A` | 虞孟母 | [《晉書・后妃下》][199] | [JSON](jqx_jns_jae_A.json) |

</details>

<details><summary><code>jru_oiq_x0q</code> 楚成王（鄭世家候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 楚成王 | [《史記・鄭世家》][1167] | [JSON](jru_oiq_x0q.json) |
| `A` | 商臣 | [《史記・鄭世家》][1167] | [JSON](jru_oiq_x0q_A.json) |

</details>

<details><summary><code>jss_82r_1ct</code> 陸萬載（陸慧曉祖，侍中）（8 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 陸萬載（陸慧曉祖，侍中） | [《南齊書・王秀之 王慈 蔡約 陸慧曉 顧憲之 蕭惠基》][651]、[《南齊書・王秀之 王慈 蔡約 陸慧曉 顧憲之 蕭惠基》][652] | [JSON](jss_82r_1ct.json) |
| `A` | 陸子真（陸慧曉父，宋海陵太守） | [《南齊書・王秀之 王慈 蔡約 陸慧曉 顧憲之 蕭惠基》][651] | [JSON](jss_82r_1ct_A.json) |
| `AA` | 陸慧曉（字叔明，陳書作惠曉） | [《南齊書・王秀之 王慈 蔡約 陸慧曉 顧憲之 蕭惠基》][651] | [JSON](jss_82r_1ct_AA.json) |
| `AAA` | 陸任（梁御史中丞，陸繕父） | [《陳書・列傳第十七: 沈君理 王瑒 陸繕》][61]、[《南史・陸澄　陸慧曉　陸杲》][936] | [JSON](jss_82r_1ct_AAA.json) |
| `AAAA` | 陸繕（字士繻，諡安子） | [《陳書・列傳第十七: 沈君理 王瑒 陸繕》][61] | [JSON](jss_82r_1ct_AAAA.json) |
| `AAAAA` | 陸辯惠（字敬仁，南史作辯慧） | [《陳書・列傳第十七: 沈君理 王瑒 陸繕》][61] | [JSON](jss_82r_1ct_AAAAA.json) |
| `AAAB` | 陸繕兄（陸見賢父，名未載） | — | [JSON](jss_82r_1ct_AAAB.json) |
| `AAABA` | 陸見賢（陸繕兄子，諡平子） | [《陳書・列傳第十七: 沈君理 王瑒 陸繕》][61] | [JSON](jss_82r_1ct_AAABA.json) |

</details>

<details><summary><code>jx9_cov_qe0</code> 欒布（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 欒布 | [《史記・季布欒布列傳》][1225] | [JSON](jx9_cov_qe0.json) |
| `A` | 賁（欒布子） | [《史記・季布欒布列傳》][1225]、[《史記・惠景間侯者年表》][1684] | [JSON](jx9_cov_qe0_A.json) |

</details>

<details><summary><code>jyf_yg2_dqk</code> 沈劭之（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 沈劭之 | [《宋書・薛安都 沈文秀 崔道固》][1544] | [JSON](jyf_yg2_dqk.json) |
| `A` | 沈文秀 | [《南齊書・劉懷珍 李安民 王玄載》][541] | [JSON](jyf_yg2_dqk_A.json) |

</details>

<details><summary><code>jyx_72x_8t2</code> 褚淵（4 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 褚淵 | [《南齊書・徐孝嗣 沈文季》][635] | [JSON](jyx_72x_8t2.json) |
| `A` | 褚蓁 | [《梁書・王規 劉瑴 宗懍 王承 褚翔 蕭介 從父兄洽 褚球 劉孺 弟覽 遵 劉潛 弟孝勝 孝威 孝先 殷芸 蕭幾》][463]、[《南齊書・武十七王》][594]、[《南史・齊武帝諸子　文惠諸子　明帝諸子》][919] | [JSON](jyx_72x_8t2_A.json) |
| `AA` | 褚向（字景政） | [《梁書・王規 劉瑴 宗懍 王承 褚翔 蕭介 從父兄洽 褚球 劉孺 弟覽 遵 劉潛 弟孝勝 孝威 孝先 殷芸 蕭幾》][463] | [JSON](jyx_72x_8t2_AA.json) |
| `AAA` | 褚翔 | [《梁書・王規 劉瑴 宗懍 王承 褚翔 蕭介 從父兄洽 褚球 劉孺 弟覽 遵 劉潛 弟孝勝 孝威 孝先 殷芸 蕭幾》][463] | [JSON](jyx_72x_8t2_AAA.json) |

</details>

<details><summary><code>k2p_5ol_dwh</code> 蒙驁（4 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 蒙驁 | [《史記・蒙恬列傳》][1213] | [JSON](k2p_5ol_dwh.json) |
| `A` | 蒙武 | [《史記・蒙恬列傳》][1213] | [JSON](k2p_5ol_dwh_A.json) |
| `AA` | 蒙恬 | [《史記・蒙恬列傳》][1213] | [JSON](k2p_5ol_dwh_AA.json) |
| `AB` | 蒙毅 | [《史記・蒙恬列傳》][1213] | [JSON](k2p_5ol_dwh_AB.json) |

</details>

<details><summary><code>k5z_d58_n7p</code> 熊元（楚考烈王）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 熊元（楚考烈王） | [《史記・春申君列傳》][1203] | [JSON](k5z_d58_n7p.json) |
| `A` | 悍（楚幽王） | [《史記・春申君列傳》][1203] | [JSON](k5z_d58_n7p_A.json) |

</details>

<details><summary><code>khh_wth_u1d</code> 謝承（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 謝承 | [《三國志・妃嬪傳》][1023] | [JSON](khh_wth_u1d.json) |
| `A` | 謝崇 | [《三國志・妃嬪傳》][1023] | [JSON](khh_wth_u1d_A.json) |

</details>

<details><summary><code>kix_r92_2ed</code> 齊世祖賾（21 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 齊世祖賾 | [《南齊書・魏虜》][710] | [JSON](kix_r92_2ed.json) |
| `A` | 蕭子敬（安陸王） | [《南史・齊武帝諸子　文惠諸子　明帝諸子》][924] | [JSON](kix_r92_2ed_A.json) |
| `B` | 蕭子琳 | [《南齊書・武十七王》][594] | [JSON](kix_r92_2ed_B.json) |
| `C` | 蕭子罕（南海王） | [《南齊書・武十七王》][587] | [JSON](kix_r92_2ed_C.json) |
| `D` | 吳縣公主（齊武帝長女） | [《南齊書・王秀之 王慈 蔡約 陸慧曉 顧憲之 蕭惠基》][653] | [JSON](kix_r92_2ed_D.json) |
| `E` | 廬陵王子卿 | [《南齊書・武十七王》][603] | [JSON](kix_r92_2ed_E.json) |
| `F` | 蕭子貞（字雲松） | [《南齊書・武十七王》][584]、[《南齊書・武十七王》][610] | [JSON](kix_r92_2ed_F.json) |
| `G` | 蕭子響（字雲音，魚復侯） | [《南齊書・武十七王》][607] | [JSON](kix_r92_2ed_G.json) |
| `H` | 蕭子明（字雲光，西陽王） | [《南齊書・武十七王》][601] | [JSON](kix_r92_2ed_H.json) |
| `I` | 蕭子真（字雲仙，建安王） | [《南齊書・武十七王》][589] | [JSON](kix_r92_2ed_I.json) |
| `J` | 蕭子峻（字雲嵩，衡陽王） | [《南齊書・武十七王》][598] | [JSON](kix_r92_2ed_J.json) |
| `K` | 蕭子倫（字雲宗，巴陵王） | [《南齊書・武十七王》][597] | [JSON](kix_r92_2ed_K.json) |
| `L` | 蕭子岳（字雲嶠，臨賀王） | [《南齊書・武十七王》][608] | [JSON](kix_r92_2ed_L.json) |
| `M` | 蕭子文（字雲儒，西陽王） | [《南齊書・武十七王》][604] | [JSON](kix_r92_2ed_M.json) |
| `N` | 蕭子珉（字雲璵，永陽王） | [《南齊書・宗室》][639]、[《南齊書・宗室》][641] | [JSON](kix_r92_2ed_N.json) |
| `O` | 蕭子建（字雲立，湘東王） | [《南齊書・武十七王》][588] | [JSON](kix_r92_2ed_O.json) |
| `P` | 蕭子夏（字雲廣，南郡王） | [《南齊書・武十七王》][605] | [JSON](kix_r92_2ed_P.json) |
| `Q` | 齊武帝第六子（早亡，名未載） | — | [JSON](kix_r92_2ed_Q.json) |
| `R` | 齊武帝第十二子（早亡，名未載） | — | [JSON](kix_r92_2ed_R.json) |
| `S` | 齊武帝第十五子（早亡，名未載） | — | [JSON](kix_r92_2ed_S.json) |
| `T` | 齊武帝第二十二子（早亡，名未載） | — | [JSON](kix_r92_2ed_T.json) |

</details>

<details><summary><code>koy_6jg_gcc</code> 周勃（6 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 周勃 | [《史記・絳侯周勃世家》][1182] | [JSON](koy_6jg_gcc.json) |
| `A` | 勝之 | [《史記・絳侯周勃世家》][1182] | [JSON](koy_6jg_gcc_A.json) |
| `B` | 堅 | [《史記・絳侯周勃世家》][1182] | [JSON](koy_6jg_gcc_B.json) |
| `BA` | 建德 | [《史記・絳侯周勃世家》][1182] | [JSON](koy_6jg_gcc_BA.json) |
| `C` | 周亞夫 | [《史記・絳侯周勃世家》][1182] | [JSON](koy_6jg_gcc_C.json) |
| `CA` | 亞夫子 | [《史記・絳侯周勃世家》][1182] | [JSON](koy_6jg_gcc_CA.json) |

</details>

<details><summary><code>ks4_7z0_n17</code> 吳祺（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 吳祺 | [《三國志・妃嬪傳》][1022] | [JSON](ks4_7z0_n17.json) |
| `A` | 吳纂 | [《三國志・妃嬪傳》][1022] | [JSON](ks4_7z0_n17_A.json) |

</details>

<details><summary><code>kt8_3kv_44r</code> 頑（衛昭伯）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 頑（衛昭伯） | [《史記・衛康叔世家》][1162] | [JSON](kt8_3kv_44r.json) |
| `A` | 申（衛戴公） | [《史記・衛康叔世家》][1162] | [JSON](kt8_3kv_44r_A.json) |

</details>

<details><summary><code>ktk_wbg_wnm</code> 鄧公（袁盎鼂錯列傳候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 鄧公 | [《史記・袁盎鼂錯列傳》][1226] | [JSON](ktk_wbg_wnm.json) |
| `A` | 章（鄧公子） | [《史記・袁盎鼂錯列傳》][1226] | [JSON](ktk_wbg_wnm_A.json) |

</details>

<details><summary><code>l3c_zg4_f7z</code> 宋襄公（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 宋襄公 | [《史記・宋微子世家》][1163] | [JSON](l3c_zg4_f7z.json) |
| `A` | 王臣（宋成公） | [《史記・宋微子世家》][1163] | [JSON](l3c_zg4_f7z_A.json) |
| `AA` | 杵臼（宋昭公） | [《史記・宋微子世家》][1163] | [JSON](l3c_zg4_f7z_AA.json) |

</details>

<details><summary><code>l8e_pxu_xre</code> 武公（趙世家趙君候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 武公 | [《史記・趙世家》][1168] | [JSON](l8e_pxu_xre.json) |
| `A` | 朝 | [《史記・趙世家》][1168] | [JSON](l8e_pxu_xre_A.json) |

</details>

<details><summary><code>l9e_fbr_36a</code> 倉（韓世家襄王候選）（9 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 倉 | [《史記・韓世家》][1170] | [JSON](l9e_fbr_36a.json) |
| `*A` | 韓王信（韓太尉） | [《史記・韓信盧綰列傳》][1218] | [JSON](l9e_fbr_36a_%2AA.json) |
| `*AA` | 韓王信太子未名 | [《史記・韓信盧綰列傳》][1218] | [JSON](l9e_fbr_36a_%2AAA.json) |
| `*AAA` | 韓嬰 | [《史記・韓信盧綰列傳》][1218] | [JSON](l9e_fbr_36a_%2AAAA.json) |
| `*AB` | 韓穨當 | [《史記・韓信盧綰列傳》][1218] | [JSON](l9e_fbr_36a_%2AAB.json) |
| `*AB*A` | 韓嫣 | [《史記・佞幸列傳》][1250] | [JSON](l9e_fbr_36a_%2AAB%2AA.json) |
| `*AB*B` | 韓說 | [《史記・東越列傳》][1239] | [JSON](l9e_fbr_36a_%2AAB%2AB.json) |
| `*AB*B*A` | 韓曾 | [《史記・韓信盧綰列傳》][1218] | [JSON](l9e_fbr_36a_%2AAB%2AB%2AA.json) |
| `*AB*BA` | 韓說子未名 | [《史記・韓信盧綰列傳》][1218] | [JSON](l9e_fbr_36a_%2AAB%2ABA.json) |

</details>

<details><summary><code>lc5_nwz_ikf</code> 襲之〔宣之繼者〕（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 襲之〔宣之繼者〕 | [《宋書・后妃》][1350] | [JSON](lc5_nwz_ikf.json) |
| `A` | 祖憐〔襲之子〕 | [《宋書・后妃》][1350] | [JSON](lc5_nwz_ikf_A.json) |

</details>

<details><summary><code>lc6_cup_v9c</code> 稱（魯孝公）（5 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 稱（魯孝公） | [《史記・魯周公世家》][1158] | [JSON](lc6_cup_v9c.json) |
| `A` | 弗湟（魯惠公） | [《史記・魯周公世家》][1158] | [JSON](lc6_cup_v9c_A.json) |
| `AA` | 魯隱公 | [《史記・魯周公世家》][1158] | [JSON](lc6_cup_v9c_AA.json) |
| `AB` | 魯桓公 | [《史記・魯周公世家》][1158] | [JSON](lc6_cup_v9c_AB.json) |
| `ABA` | 季友（成季） | [《史記・魯周公世家》][1158] | [JSON](lc6_cup_v9c_ABA.json) |

</details>

<details><summary><code>lca_ywj_jjx</code> 李遜（九真太守）（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 李遜（九真太守） | [《宋書・良吏》][1550] | [JSON](lca_ywj_jjx.json) |
| `A` | 李弈（李遜子） | [《宋書・良吏》][1549] | [JSON](lca_ywj_jjx_A.json) |
| `B` | 李脫（交州李遜子） | [《宋書・良吏》][1549] | [JSON](lca_ywj_jjx_B.json) |

</details>

<details><summary><code>lcc_msq_vdt</code> 露（曹靖公）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 露（曹靖公） | [《史記・管蔡世家》][1160] | [JSON](lcc_msq_vdt.json) |
| `A` | 伯陽（曹君） | [《史記・管蔡世家》][1160] | [JSON](lcc_msq_vdt_A.json) |

</details>

<details><summary><code>li9_cmb_8ci</code> 滕公（本卷稱呼）（4 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 滕公（本卷稱呼） | [《史記・樊酈滕灌列傳》][1220] | [JSON](li9_cmb_8ci.json) |
| `A` | 夏侯灶 | [《史記・樊酈滕灌列傳》][1220] | [JSON](li9_cmb_8ci_A.json) |
| `AA` | 夏侯賜 | [《史記・樊酈滕灌列傳》][1220] | [JSON](li9_cmb_8ci_AA.json) |
| `AAA` | 夏侯頗 | [《史記・樊酈滕灌列傳》][1220] | [JSON](li9_cmb_8ci_AAA.json) |

</details>

<details><summary><code>lii_454_vuv</code> 陸遜（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 陸遜 | [《三國志・陸遜傳》][1101] | [JSON](lii_454_vuv.json) |
| `A` | 陸延 | [《三國志・陸遜傳》][1101] | [JSON](lii_454_vuv_A.json) |

</details>

<details><summary><code>liq_ch0_j1l</code> 侯文捍（南史作捍）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 侯文捍（南史作捍） | [《陳書・列傳第二: 杜僧明 周文育 侯安都》][35]、[《南史・杜僧明　周文育　侯瑱　侯安都　歐陽頠　黃法𣰰　淳于量　章昭達　吳明徹》][962] | [JSON](liq_ch0_j1l.json) |
| `A` | 侯安都（字成師） | [《陳書・列傳第二: 杜僧明 周文育 侯安都》][35]、[《南史・杜僧明　周文育　侯瑱　侯安都　歐陽頠　黃法𣰰　淳于量　章昭達　吳明徹》][962] | [JSON](liq_ch0_j1l_A.json) |

</details>

<details><summary><code>ll1_7jh_vr0</code> 鄭合（6 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 鄭合 | [《晉書・后妃下》][199] | [JSON](ll1_7jh_vr0.json) |
| `A` | 鄭愷 | [《晉書・后妃下》][199] | [JSON](ll1_7jh_vr0_A.json) |
| `AA` | 鄭阿春 | [《晉書・后妃下》][199] | [JSON](ll1_7jh_vr0_AA.json) |
| `AB` | 鄭氏（阿春妹，王褒妻） | [《晉書・后妃下》][199] | [JSON](ll1_7jh_vr0_AB.json) |
| `AC` | 鄭氏（阿春三妹，劉傭妻） | [《晉書・后妃下》][199] | [JSON](ll1_7jh_vr0_AC.json) |
| `AD` | 鄭氏（阿春幼妹，李氏妻） | [《晉書・后妃下》][199] | [JSON](ll1_7jh_vr0_AD.json) |

</details>

<details><summary><code>lmu_nbm_rzo</code> 燮（陳平公）（21 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 燮（陳平公） | [《史記・陳杞世家》][1161] | [JSON](lmu_nbm_rzo.json) |
| `A` | 圉（陳文公） | [《史記・陳杞世家》][1161] | [JSON](lmu_nbm_rzo_A.json) |
| `AA` | 佗（陳厲公） | [《史記・陳杞世家》][1161] | [JSON](lmu_nbm_rzo_AA.json) |
| `AAA` | 完（敬仲） | [《史記・田敬仲完世家》][1171] | [JSON](lmu_nbm_rzo_AAA.json) |
| `AAAA` | 稚孟夷 | [《史記・田敬仲完世家》][1171] | [JSON](lmu_nbm_rzo_AAAA.json) |
| `AAAAA` | 湣孟莊 | [《史記・田敬仲完世家》][1171] | [JSON](lmu_nbm_rzo_AAAAA.json) |
| `AAAAAA` | 田文子須無 | [《史記・田敬仲完世家》][1171] | [JSON](lmu_nbm_rzo_AAAAAA.json) |
| `AAAAAAA` | 田桓子無宇 | [《史記・田敬仲完世家》][1171] | [JSON](lmu_nbm_rzo_AAAAAAA.json) |
| `AAAAAAAA` | 武子開 | [《史記・田敬仲完世家》][1171] | [JSON](lmu_nbm_rzo_AAAAAAAA.json) |
| `AAAAAAAB` | 田釐子乞 | [《史記・田敬仲完世家》][1171] | [JSON](lmu_nbm_rzo_AAAAAAAB.json) |
| `AAAAAAABA` | 田常 | [《史記・田敬仲完世家》][1171] | [JSON](lmu_nbm_rzo_AAAAAAABA.json) |
| `AAAAAAABAA` | 田襄子盤 | [《史記・田敬仲完世家》][1171] | [JSON](lmu_nbm_rzo_AAAAAAABAA.json) |
| `AAAAAAABAAA` | 田莊子白 | [《史記・田敬仲完世家》][1171] | [JSON](lmu_nbm_rzo_AAAAAAABAAA.json) |
| `AAAAAAABAAAA` | 太公和 | [《史記・田敬仲完世家》][1171] | [JSON](lmu_nbm_rzo_AAAAAAABAAAA.json) |
| `AAAAAAABAAAAA` | 桓公午 | [《史記・扁鵲倉公列傳》][1230] | [JSON](lmu_nbm_rzo_AAAAAAABAAAAA.json) |
| `AAAAAAABAAAAAA` | 因齊 | [《史記・田敬仲完世家》][1171] | [JSON](lmu_nbm_rzo_AAAAAAABAAAAAA.json) |
| `AAAAAAABAAAAAAA` | 辟彊 | [《史記・田敬仲完世家》][1171]、[《史記・孟嘗君列傳》][1200] | [JSON](lmu_nbm_rzo_AAAAAAABAAAAAAA.json) |
| `AAAAAAABAAAAAAAA` | 齊湣王 | [《史記・孟嘗君列傳》][1200] | [JSON](lmu_nbm_rzo_AAAAAAABAAAAAAAA.json) |
| `AB` | 鮑（陳桓公） | [《史記・陳杞世家》][1161] | [JSON](lmu_nbm_rzo_AB.json) |
| `ABA` | 免（陳桓公太子） | [《史記・陳杞世家》][1161] | [JSON](lmu_nbm_rzo_ABA.json) |
| `ABB` | 躍（陳利公） | [《史記・陳杞世家》][1161] | [JSON](lmu_nbm_rzo_ABB.json) |

</details>

<details><summary><code>lpo_z63_vzb</code> 諸葛瑾（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 諸葛瑾 | [《三國志・張顧諸葛步傳》][1050] | [JSON](lpo_z63_vzb.json) |
| `A` | 諸葛氏〔諸葛瑾女、張承妻〕 | [《三國志・張顧諸葛步傳》][1044] | [JSON](lpo_z63_vzb_A.json) |
| `B` | 諸葛融 | [《三國志・張顧諸葛步傳》][1051] | [JSON](lpo_z63_vzb_B.json) |

</details>

<details><summary><code>lrg_cze_g1l</code> 蘇峻（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 蘇峻 | [《晉書・溫嶠 郗鑒》][272]、[《晉書・庾亮》][289]、[《晉書・叛臣三》][351] | [JSON](lrg_cze_g1l.json) |
| `A` | 蘇碩 | [《晉書・叛臣三》][351] | [JSON](lrg_cze_g1l_A.json) |

</details>

<details><summary><code>lt4_hpv_4ku</code> 武成王（燕君）（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 武成王（燕君） | [《史記・燕召公世家》][1159] | [JSON](lt4_hpv_4ku.json) |
| `A` | 孝王（燕君） | [《史記・燕召公世家》][1159] | [JSON](lt4_hpv_4ku_A.json) |
| `AA` | 燕王喜 | [《史記・燕召公世家》][1159] | [JSON](lt4_hpv_4ku_AA.json) |

</details>

<details><summary><code>lwx_9yq_ad7</code> 紂（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 紂 | [《史記・殷本紀》][1145] | [JSON](lwx_9yq_ad7.json) |
| `A` | 武庚 | [《史記・衛康叔世家》][1162] | [JSON](lwx_9yq_ad7_A.json) |

</details>

<details><summary><code>lxy_zsx_o2z</code> 崔參〔清河、溫嶠外祖〕（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 崔參〔清河、溫嶠外祖〕 | [《世說新語・尤悔》][1327] | [JSON](lxy_zsx_o2z.json) |
| `A` | 清河崔氏〔溫嶠母〕 | [《晉書・溫嶠 郗鑒》][272]、[《世說新語・尤悔》][1327] | [JSON](lxy_zsx_o2z_A.json) |

</details>

<details><summary><code>m0b_b5e_153</code> 田常（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 田常 | [《史記・齊太公世家》][1157] | [JSON](m0b_b5e_153.json) |
| `**A` | 田和 | [《史記・六國年表》][1680] | [JSON](m0b_b5e_153_%2A%2AA.json) |

</details>

<details><summary><code>m4d_lon_pyg</code> 王廣之（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 王廣之 | [《南齊書・劉懷珍 李安民 王玄載》][538] | [JSON](m4d_lon_pyg.json) |
| `A` | 王珍國（字德重） | [《梁書・王珍國 馬仙琕 張齊》][397] | [JSON](m4d_lon_pyg_A.json) |

</details>

<details><summary><code>m5k_t3s_umk</code> 簫宏〔臨川王，楊舒墓誌〕（4 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 簫宏〔臨川王，楊舒墓誌〕 | [《梁書・太祖五王》][416] | [JSON](m5k_t3s_umk.json) |
| `A` | 蕭正德（字公和，臨賀王） | [《南史・梁宗室上》][941] | [JSON](m5k_t3s_umk_A.json) |
| `B` | 蕭正立（字公山，建安侯） | [《梁書・太祖五王》][416] | [JSON](m5k_t3s_umk_B.json) |
| `BA` | 蕭賁（字世文，建安侯） | [《梁書・太祖五王》][416]、[《梁書・韋粲 江子一 弟子四 子五 張嵊 沈浚 柳敬禮》][469] | [JSON](m5k_t3s_umk_BA.json) |

</details>

<details><summary><code>m8d_pnd_ias</code> 惠侯（燕君）（10 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 惠侯（燕君） | [《史記・燕召公世家》][1159] | [JSON](m8d_pnd_ias.json) |
| `A` | 釐侯（燕君） | [《史記・燕召公世家》][1159] | [JSON](m8d_pnd_ias_A.json) |
| `AA` | 頃侯（燕君） | [《史記・燕召公世家》][1159] | [JSON](m8d_pnd_ias_AA.json) |
| `AAA` | 哀侯（燕君） | [《史記・燕召公世家》][1159] | [JSON](m8d_pnd_ias_AAA.json) |
| `AAAA` | 鄭侯（燕君） | [《史記・燕召公世家》][1159] | [JSON](m8d_pnd_ias_AAAA.json) |
| `AAAAA` | 繆侯（燕君） | [《史記・燕召公世家》][1159] | [JSON](m8d_pnd_ias_AAAAA.json) |
| `AAAAAA` | 宣侯（燕君） | [《史記・燕召公世家》][1159] | [JSON](m8d_pnd_ias_AAAAAA.json) |
| `AAAAAAA` | 桓侯（燕君） | [《史記・燕召公世家》][1159] | [JSON](m8d_pnd_ias_AAAAAAA.json) |
| `AAAAAAAA` | 燕莊公 | [《史記・齊太公世家》][1157]、[《史記・燕召公世家》][1159] | [JSON](m8d_pnd_ias_AAAAAAAA.json) |
| `AAAAAAAAA` | 襄公（燕君） | [《史記・燕召公世家》][1159] | [JSON](m8d_pnd_ias_AAAAAAAAA.json) |

</details>

<details><summary><code>m8n_ntm_79h</code> 盧植（16 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 盧植 | [《後漢書・吳延史盧趙列傳》][125] | [JSON](m8n_ntm_79h.json) |
| `A` | 盧毓 | [《三國志・桓二陳徐衞盧傳》][989] | [JSON](m8n_ntm_79h_A.json) |
| `A*A` | 藩〔盧毓孫〕 | [《三國志・桓二陳徐衞盧傳》][989] | [JSON](m8n_ntm_79h_A%2AA.json) |
| `AA` | 盧欽〔舉王衍者〕 | [《晉書・鄭袤 李胤 盧欽 華表 石鑒 溫羨》][230] | [JSON](m8n_ntm_79h_AA.json) |
| `AAA` | 盧浮 | [《三國志・桓二陳徐衞盧傳》][989] | [JSON](m8n_ntm_79h_AAA.json) |
| `AB` | 盧珽 | [《三國志・桓二陳徐衞盧傳》][989] | [JSON](m8n_ntm_79h_AB.json) |
| `ABA` | 皓〔盧珽子〕 | [《三國志・桓二陳徐衞盧傳》][989] | [JSON](m8n_ntm_79h_ABA.json) |
| `ABB` | 盧志 | [《晉書・鄭袤 李胤 盧欽 華表 石鑒 溫羨》][232] | [JSON](m8n_ntm_79h_ABB.json) |
| `ABBA` | 盧諶 | [《晉書・鄭袤 李胤 盧欽 華表 石鑒 溫羨》][228] | [JSON](m8n_ntm_79h_ABBA.json) |
| `ABBA**A` | 盧循 | [《宋書・良吏》][1549] | [JSON](m8n_ntm_79h_ABBA%2A%2AA.json) |
| `ABBA*A` | 盧嘏（盧循父） | [《晉書・叛臣三》][350]、[《宋書・孫處 蒯恩 劉鍾 虞丘進》][1438]、[《宋書・良吏》][1549] | [JSON](m8n_ntm_79h_ABBA%2AA.json) |
| `ABBAA` | 偃〔盧諶子〕 | [《魏書・燕鳳 許謙 張衮 崔玄伯 鄧淵》][1609]、[《魏書・燕鳳 許謙 張衮 崔玄伯 鄧淵》][1610] | [JSON](m8n_ntm_79h_ABBAA.json) |
| `ABBAAA` | 邈〔偃子〕 | [《魏書・燕鳳 許謙 張衮 崔玄伯 鄧淵》][1609]、[《魏書・燕鳳 許謙 張衮 崔玄伯 鄧淵》][1610]、[《魏書・盧玄》][1616] | [JSON](m8n_ntm_79h_ABBAAA.json) |
| `ABBAAAA` | 盧玄〔字子真〕 | [《魏書・盧玄》][1616] | [JSON](m8n_ntm_79h_ABBAAAA.json) |
| `ABBB` | 盧謐〔盧志子〕 | [《晉書・鄭袤 李胤 盧欽 華表 石鑒 溫羨》][232] | [JSON](m8n_ntm_79h_ABBB.json) |
| `ABBC` | 盧詵〔盧志子〕 | [《晉書・鄭袤 李胤 盧欽 華表 石鑒 溫羨》][232] | [JSON](m8n_ntm_79h_ABBC.json) |

</details>

<details><summary><code>m9n_b6v_wo0</code> 梁孝王（本卷未名）（5 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 梁孝王（本卷未名） | [《史記・孝景本紀》][1153] | [JSON](m9n_b6v_wo0.json) |
| `A` | 明（梁孝王子） | [《史記・孝景本紀》][1153] | [JSON](m9n_b6v_wo0_A.json) |
| `B` | 彭離（梁孝王子） | [《史記・孝景本紀》][1153] | [JSON](m9n_b6v_wo0_B.json) |
| `C` | 定（梁孝王子） | [《史記・孝景本紀》][1153] | [JSON](m9n_b6v_wo0_C.json) |
| `D` | 不識（梁孝王子） | [《史記・孝景本紀》][1153] | [JSON](m9n_b6v_wo0_D.json) |

</details>

<details><summary><code>mad_l88_njl</code> 王珪之（撰《齊職儀》）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 王珪之（撰《齊職儀》） | [《南齊書・文學》][691] | [JSON](mad_l88_njl.json) |
| `A` | 王顥（王珪之子） | [《南齊書・文學》][691]、[《南史・王裕之　王鎮之　王韶之　王悅之　王准之》][875] | [JSON](mad_l88_njl_A.json) |

</details>

<details><summary><code>maz_aq2_t5g</code> 季勝（趙世家祖系候選）（4 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 季勝 | [《史記・趙世家》][1168] | [JSON](maz_aq2_t5g.json) |
| `A` | 孟增 | [《史記・趙世家》][1168] | [JSON](maz_aq2_t5g_A.json) |
| `AA` | 衡父 | [《史記・趙世家》][1168] | [JSON](maz_aq2_t5g_AA.json) |
| `AAA` | 造父 | [《史記・趙世家》][1168] | [JSON](maz_aq2_t5g_AAA.json) |

</details>

<details><summary><code>mfd_id2_bu3</code> 劉乂（脩武令）（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 劉乂（脩武令） | [《劉媚子石墓誌・全文》][84] | [JSON](mfd_id2_bu3.json) |
| `A` | 劉璞（光祿勳、東昌男） | [《劉媚子磚墓誌・現可釋讀部分》][83]、[《劉媚子石墓誌・全文》][84] | [JSON](mfd_id2_bu3_A.json) |
| `AA` | 劉媚子（王建之妻） | [《劉媚子磚墓誌・現可釋讀部分》][83]、[《劉媚子石墓誌・全文》][84] | [JSON](mfd_id2_bu3_AA.json) |

</details>

<details><summary><code>mgh_3bh_rit</code> 周厲王（鄭世家候選）（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 周厲王 | [《史記・鄭世家》][1167] | [JSON](mgh_3bh_rit.json) |
| `A` | 友 | [《史記・鄭世家》][1167] | [JSON](mgh_3bh_rit_A.json) |
| `AA` | 掘突 | [《史記・鄭世家》][1167] | [JSON](mgh_3bh_rit_AA.json) |

</details>

<details><summary><code>mj8_5ic_4kk</code> 殷道鸞（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 殷道鸞 | [《宋書・謝晦》][1358]、[《宋書・謝晦》][1359] | [JSON](mj8_5ic_4kk.json) |
| `A` | 殷琰 | [《宋書・胡藩 劉康祖 垣護之 張興世》][1475] | [JSON](mj8_5ic_4kk_A.json) |

</details>

<details><summary><code>mnv_izb_7w3</code> 蕭景〔吳平侯〕（4 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 蕭景〔吳平侯〕 | [《梁書・裴子野 顧協 徐摛 鮑泉》][452]、[《南史・梁宗室上》][940] | [JSON](mnv_izb_7w3.json) |
| `A` | 蕭勸（字文肅） | [《南史・梁宗室上》][940] | [JSON](mnv_izb_7w3_A.json) |
| `B` | 蕭勉（字文祗） | [《南史・梁宗室上》][940] | [JSON](mnv_izb_7w3_B.json) |
| `C` | 蕭勃（曲江鄕侯） | [《陳書・列傳第十一: 王沖 王通 袁敬》][51]、[《南史・王誕　王華　王惠　王彧》][854]、[《南史・梁宗室上》][940] | [JSON](mnv_izb_7w3_C.json) |

</details>

<details><summary><code>mo6_e25_hpq</code> 張允（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 張允 | [《三國志・虞陸張駱陸吾朱傳》][1097] | [JSON](mo6_e25_hpq.json) |
| `A` | 張祗 | [《三國志・虞陸張駱陸吾朱傳》][1097] | [JSON](mo6_e25_hpq_A.json) |

</details>

<details><summary><code>ms3_fa1_ps9</code> 田生（荊燕世家候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 田生 | [《史記・荊燕世家》][1176] | [JSON](ms3_fa1_ps9.json) |
| `A` | 田生子 | [《史記・荊燕世家》][1176] | [JSON](ms3_fa1_ps9_A.json) |

</details>

<details><summary><code>muq_yy8_8er</code> 寤生（鄭世家莊公候選）（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 寤生 | [《史記・鄭世家》][1167] | [JSON](muq_yy8_8er.json) |
| `A` | 忽 | [《史記・鄭世家》][1167] | [JSON](muq_yy8_8er_A.json) |
| `B` | 突 | [《史記・鄭世家》][1167] | [JSON](muq_yy8_8er_B.json) |

</details>

<details><summary><code>mwc_md4_l0g</code> 王含（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 王含 | [《晉書・叛臣一》][344] | [JSON](mwc_md4_l0g.json) |
| `A` | 王應 | [《晉書・叛臣一》][344] | [JSON](mwc_md4_l0g_A.json) |
| `B` | 王瑜〔王含子、散騎常侍〕 | [《晉書・叛臣一》][344] | [JSON](mwc_md4_l0g_B.json) |

</details>

<details><summary><code>mxz_qw8_acd</code> 王揖（4 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 王揖 | [《南史・王曇首》][836]、[《南史・王曇首》][840] | [JSON](mxz_qw8_acd.json) |
| `A` | 王筠 | [《梁書・王僧孺 張率 劉孝綽 王筠》][457]、[《梁書・王僧孺 張率 劉孝綽 王筠》][456] | [JSON](mxz_qw8_acd_A.json) |
| `AA` | 王祥（王筠子） | [《南史・王曇首》][838]、[《南史・王曇首》][837]、[《隋書・文學》][1587] | [JSON](mxz_qw8_acd_AA.json) |
| `AAA` | 王胄（字承基） | [《隋書・文學》][1587] | [JSON](mxz_qw8_acd_AAA.json) |

</details>

<details><summary><code>n0i_g82_0n2</code> 蒯聵（衛莊公）（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 蒯聵（衛莊公） | [《史記・衛康叔世家》][1162] | [JSON](n0i_g82_0n2.json) |
| `A` | 輒（衛出公） | [《史記・衛康叔世家》][1162] | [JSON](n0i_g82_0n2_A.json) |
| `AA` | 出公子（衛黔所攻者未名） | [《史記・衛康叔世家》][1162] | [JSON](n0i_g82_0n2_AA.json) |

</details>

<details><summary><code>n2x_d8l_n0d</code> 嵇翰（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 嵇翰 | [《晉書・忠義》][318] | [JSON](n2x_d8l_n0d.json) |
| `*A` | 嵇曠 | [《晉書・忠義》][318] | [JSON](n2x_d8l_n0d_%2AA.json) |

</details>

<details><summary><code>n3u_6wg_kay</code> 隆（張次公父）（衛將軍驃騎列傳候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 隆（張次公父） | [《史記・衛將軍驃騎列傳》][1236] | [JSON](n3u_6wg_kay.json) |
| `A` | 張次公 | [《史記・衛將軍驃騎列傳》][1236] | [JSON](n3u_6wg_kay_A.json) |

</details>

<details><summary><code>n4f_fqh_04q</code> 易王（燕君）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 易王（燕君） | [《史記・蘇秦列傳》][1194] | [JSON](n4f_fqh_04q.json) |
| `A` | 燕噲（本篇燕君） | [《史記・燕召公世家》][1159] | [JSON](n4f_fqh_04q_A.json) |

</details>

<details><summary><code>nbb_y6s_bfz</code> 明玩（明僧紹祖）（7 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 明玩（明僧紹祖） | [《南齊書・高逸》][699]、[《南齊書・高逸》][702] | [JSON](nbb_y6s_bfz.json) |
| `A` | 明略（明僧紹父） | [《南齊書・高逸》][699]、[《南齊書・高逸》][702] | [JSON](nbb_y6s_bfz_A.json) |
| `AA` | 明僧紹（字承烈，一字休烈） | [《南齊書・高逸》][702] | [JSON](nbb_y6s_bfz_AA.json) |
| `AAA` | 明山賓（字孝若） | [《梁書・陸倕 到洽 明山賓 殷鈞 陸襄》][424] | [JSON](nbb_y6s_bfz_AAA.json) |
| `AAAA` | 明震（字興道，明山賓子） | [《梁書・陸倕 到洽 明山賓 殷鈞 陸襄》][424] | [JSON](nbb_y6s_bfz_AAAA.json) |
| `AAB` | 明元琳（南齊書明僧紹傳字仲璋） | [《南齊書・高逸》][700]、[《南齊書・高逸》][702] | [JSON](nbb_y6s_bfz_AAB.json) |
| `AAC` | 明仲璋（梁書明山賓傳之兄，南史與元琳並列） | [《梁書・陸倕 到洽 明山賓 殷鈞 陸襄》][424]、[《南史・劉瓛　明僧紹　庾易　劉虬》][939] | [JSON](nbb_y6s_bfz_AAC.json) |

</details>

<details><summary><code>nbl_2bu_99w</code> 王舒（4 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 王舒 | [《晉書・王舒 王廙 虞潭 顧眾 張闓》][301] | [JSON](nbl_2bu_99w.json) |
| `A` | 王晏之 | [《晉書・王舒 王廙 虞潭 顧眾 張闓》][301] | [JSON](nbl_2bu_99w_A.json) |
| `AA` | 王崐之 | [《晉書・王舒 王廙 虞潭 顧眾 張闓》][301] | [JSON](nbl_2bu_99w_AA.json) |
| `AAA` | 王陋之 | [《晉書・王舒 王廙 虞潭 顧眾 張闓》][301] | [JSON](nbl_2bu_99w_AAA.json) |

</details>

<details><summary><code>nf1_c66_863</code> 楊季主（游俠列傳候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 楊季主 | [《史記・游俠列傳》][1249] | [JSON](nf1_c66_863.json) |
| `A` | 楊季主子（未名縣掾） | [《史記・游俠列傳》][1249] | [JSON](nf1_c66_863_A.json) |

</details>

<details><summary><code>nfj_6w2_8mn</code> 增（魏世家景湣王候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 增 | [《史記・魏世家》][1169] | [JSON](nfj_6w2_8mn.json) |
| `A` | 假 | [《史記・魏世家》][1169] | [JSON](nfj_6w2_8mn_A.json) |

</details>

<details><summary><code>ngw_hmv_7k0</code> 蕭爰之（蕭景先祖）（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 蕭爰之（蕭景先祖） | [《南齊書・蕭景先 蕭赤斧 子穎冑》][575] | [JSON](ngw_hmv_7k0.json) |
| `A` | 蕭敬宗（蕭景先父） | [《南齊書・蕭景先 蕭赤斧 子穎冑》][575] | [JSON](ngw_hmv_7k0_A.json) |
| `AA` | 蕭景先（本名道先，齊中領軍） | [《南齊書・蕭景先 蕭赤斧 子穎冑》][575] | [JSON](ngw_hmv_7k0_AA.json) |

</details>

<details><summary><code>nkd_lkj_t7g</code> 周榮（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 周榮 | [《後漢書・袁張韓周列傳》][119] | [JSON](nkd_lkj_t7g.json) |
| `A` | 周興〔後漢周榮子、周景父〕 | [《後漢書・袁張韓周列傳》][120] | [JSON](nkd_lkj_t7g_A.json) |

</details>

<details><summary><code>ntv_ei7_aqh</code> 吳範（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 吳範 | [《三國志・吳範劉惇趙達傳》][1127] | [JSON](ntv_ei7_aqh.json) |
| `A` | 吳範長子〔未具名、先卒〕 | [《三國志・吳範劉惇趙達傳》][1127] | [JSON](ntv_ei7_aqh_A.json) |
| `B` | 吳範少子〔未具名、黃武五年尚幼〕 | [《三國志・吳範劉惇趙達傳》][1127] | [JSON](ntv_ei7_aqh_B.json) |

</details>

<details><summary><code>nuf_tb9_fjs</code> 竇嬰父（未名）（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 竇嬰父（未名） | [《史記・魏其武安列傳》][1232] | [JSON](nuf_tb9_fjs.json) |
| `A` | 竇嬰 | [《史記・魏其武安列傳》][1232] | [JSON](nuf_tb9_fjs_A.json) |
| `AA` | 竇嬰子未名 | [《史記・魏其武安列傳》][1232] | [JSON](nuf_tb9_fjs_AA.json) |

</details>

<details><summary><code>nxl_qt6_cpl</code> 畢萬（魏世家候選）（9 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 畢萬 | [《史記・魏世家》][1169] | [JSON](nxl_qt6_cpl.json) |
| `A` | 魏武子 | [《史記・魏世家》][1169] | [JSON](nxl_qt6_cpl_A.json) |
| `AA` | 魏悼子 | [《史記・魏世家》][1169] | [JSON](nxl_qt6_cpl_AA.json) |
| `AAA` | 魏絳 | [《史記・魏世家》][1169] | [JSON](nxl_qt6_cpl_AAA.json) |
| `AAAA` | 魏嬴 | [《史記・魏世家》][1169] | [JSON](nxl_qt6_cpl_AAAA.json) |
| `AAAAA` | 魏獻子 | [《史記・魏世家》][1169] | [JSON](nxl_qt6_cpl_AAAAA.json) |
| `AAAAAA` | 魏侈 | [《史記・魏世家》][1169] | [JSON](nxl_qt6_cpl_AAAAAA.json) |
| `AAAAAA*A` | 魏桓子 | [《史記・魏世家》][1169] | [JSON](nxl_qt6_cpl_AAAAAA%2AA.json) |
| `AAAAAA*A*A` | 都 | [《史記・魏世家》][1169] | [JSON](nxl_qt6_cpl_AAAAAA%2AA%2AA.json) |

</details>

<details><summary><code>nye_x8g_zwl</code> 陳桓公鮑（田世家候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 陳桓公鮑 | [《史記・田敬仲完世家》][1171] | [JSON](nye_x8g_zwl.json) |
| `A` | 陳莊公林 | [《史記・田敬仲完世家》][1171] | [JSON](nye_x8g_zwl_A.json) |

</details>

<details><summary><code>o0l_em5_5v9</code> 吳芮（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 吳芮 | [《史記・高祖本紀》][1150] | [JSON](o0l_em5_5v9.json) |
| `A` | 臣（吳芮子） | [《史記・呂后本紀》][1151]、[《史記・黥布列傳》][1216]、[《史記・漢興以來諸侯王年表》][1682] | [JSON](o0l_em5_5v9_A.json) |
| `B` | 英布妻未名 | [《史記・黥布列傳》][1216] | [JSON](o0l_em5_5v9_B.json) |

</details>

<details><summary><code>odl_r9a_hli</code> 戴顒（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 戴顒 | [《南史・張邵》][906]、[《宋書・隱逸》][1573] | [JSON](odl_r9a_hli.json) |
| `A` | 戴顒女（張沖母，未具名） | — | [JSON](odl_r9a_hli_A.json) |

</details>

<details><summary><code>ogi_smr_m75</code> 文聘（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 文聘 | [《三國志・陸遜傳》][1101] | [JSON](ogi_smr_m75.json) |
| `A` | 文休 | [《三國志・陸遜傳》][1101] | [JSON](ogi_smr_m75_A.json) |

</details>

<details><summary><code>oix_a6t_ovk</code> 朱治〔字君理〕（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 朱治〔字君理〕 | [《三國志・朱治朱然呂範朱桓傳》][1087] | [JSON](oix_a6t_ovk.json) |
| `A` | 朱才〔朱治子、字君業〕 | [《三國志・朱治朱然呂範朱桓傳》][1087] | [JSON](oix_a6t_ovk_A.json) |

</details>

<details><summary><code>opr_t0a_l8g</code> 淳于公（齊太倉令）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 淳于公（齊太倉令） | [《史記・扁鵲倉公列傳》][1230] | [JSON](opr_t0a_l8g.json) |
| `A` | 緹縈 | [《史記・扁鵲倉公列傳》][1230] | [JSON](opr_t0a_l8g_A.json) |

</details>

<details><summary><code>osu_yvw_bwr</code> 熊惲（楚成王候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 熊惲 | [《史記・楚世家》][1165] | [JSON](osu_yvw_bwr.json) |
| `A` | 職（楚成王欲立之子） | [《史記・楚世家》][1165] | [JSON](osu_yvw_bwr_A.json) |

</details>

<details><summary><code>otw_1ui_wba</code> 胡藩（8 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 胡藩 | [《宋書・胡藩 劉康祖 垣護之 張興世》][1450] | [JSON](otw_1ui_wba.json) |
| `A` | 胡隆世（胡藩子） | [《宋書・胡藩 劉康祖 垣護之 張興世》][1448]、[《宋書・胡藩 劉康祖 垣護之 張興世》][1452] | [JSON](otw_1ui_wba_A.json) |
| `AA` | 胡乾秀（胡隆世子） | [《宋書・胡藩 劉康祖 垣護之 張興世》][1448]、[《宋書・胡藩 劉康祖 垣護之 張興世》][1453] | [JSON](otw_1ui_wba_AA.json) |
| `B` | 胡遵世（胡藩第十四子） | [《宋書・胡藩 劉康祖 垣護之 張興世》][1448]、[《宋書・胡藩 劉康祖 垣護之 張興世》][1455] | [JSON](otw_1ui_wba_B.json) |
| `C` | 胡誕世（胡藩第十六子） | [《宋書・胡藩 劉康祖 垣護之 張興世》][1448] | [JSON](otw_1ui_wba_C.json) |
| `D` | 胡茂世（胡藩第十七子） | [《宋書・胡藩 劉康祖 垣護之 張興世》][1448]、[《宋書・胡藩 劉康祖 垣護之 張興世》][1449] | [JSON](otw_1ui_wba_D.json) |
| `E` | 胡景世（誕世兄） | [《宋書・胡藩 劉康祖 垣護之 張興世》][1448]、[《宋書・胡藩 劉康祖 垣護之 張興世》][1451] | [JSON](otw_1ui_wba_E.json) |
| `F` | 胡寶世（景世弟） | [《宋書・胡藩 劉康祖 垣護之 張興世》][1448]、[《宋書・胡藩 劉康祖 垣護之 張興世》][1451] | [JSON](otw_1ui_wba_F.json) |

</details>

<details><summary><code>p2p_gqb_6ar</code> 士燮〔交阯，字威彥〕（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 士燮〔交阯，字威彥〕 | [《三國志・劉繇太史慈士燮傳》][1011] | [JSON](p2p_gqb_6ar.json) |
| `A` | 士廞（士燮子，質於吳） | [《三國志・劉繇太史慈士燮傳》][1011] | [JSON](p2p_gqb_6ar_A.json) |

</details>

<details><summary><code>p4b_qf7_603</code> 趙武（趙庶子）（4 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 趙武（趙庶子） | [《史記・趙世家》][1168] | [JSON](p4b_qf7_603.json) |
| `A` | 趙景叔 | [《史記・趙世家》][1168] | [JSON](p4b_qf7_603_A.json) |
| `AA` | 趙鞅 | [《史記・趙世家》][1168] | [JSON](p4b_qf7_603_AA.json) |
| `AAA` | 趙襄子毋卹 | [《史記・趙世家》][1168] | [JSON](p4b_qf7_603_AAA.json) |

</details>

<details><summary><code>p6n_a0q_flh</code> 程普〔字德謀〕（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 程普〔字德謀〕 | [《三國志・程黃韓蔣周陳董甘淩徐潘丁傳》][1068] | [JSON](p6n_a0q_flh.json) |
| `A` | 程咨 | [《三國志・程黃韓蔣周陳董甘淩徐潘丁傳》][1068] | [JSON](p6n_a0q_flh_A.json) |

</details>

<details><summary><code>p6s_2qn_p8n</code> 平原侯植（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 平原侯植 | [《三國志・任城陳蕭王傳》][985] | [JSON](p6s_2qn_p8n.json) |
| `A` | 曹志〔字允恭〕 | [《晉書・曹志 庾峻 郭象 庾純 秦秀》][241] | [JSON](p6s_2qn_p8n_A.json) |

</details>

<details><summary><code>p93_tgr_t8r</code> 王遠（4 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 王遠 | [《南史・王弘》][818] | [JSON](p93_tgr_t8r.json) |
| `A` | 王僧祐 | [《南齊書・王秀之 王慈 蔡約 陸慧曉 顧憲之 蕭惠基》][656]、[《南史・王弘》][813] | [JSON](p93_tgr_t8r_A.json) |
| `AA` | 王籍〔字文海〕 | [《梁書・文學下》][481]、[《南史・王弘》][810] | [JSON](p93_tgr_t8r_AA.json) |
| `AAA` | 王碧（王籍子） | [《梁書・文學下》][481] | [JSON](p93_tgr_t8r_AAA.json) |

</details>

<details><summary><code>p9l_wy7_y7m</code> 魏文侯（孫吳列傳候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 魏文侯 | [《史記・孫子吳起列傳》][1190] | [JSON](p9l_wy7_y7m.json) |
| `A` | 魏武侯 | [《史記・孫子吳起列傳》][1190] | [JSON](p9l_wy7_y7m_A.json) |

</details>

<details><summary><code>pac_tt7_hs3</code> 潘濬（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 潘濬 | [《三國志・潘濬陸凱傳》][1120] | [JSON](pac_tt7_hs3.json) |
| `A` | 潘翥 | [《三國志・潘濬陸凱傳》][1120] | [JSON](pac_tt7_hs3_A.json) |
| `B` | 潘氏〔潘濬女、建昌侯孫慮妻〕 | [《三國志・潘濬陸凱傳》][1120] | [JSON](pac_tt7_hs3_B.json) |

</details>

<details><summary><code>pbz_pni_tco</code> 何偃（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 何偃 | [《宋書・羊欣 張敷 王微》][1500] | [JSON](pbz_pni_tco.json) |
| `A` | 何戢 | [《南齊書・王琨 張岱 褚炫 何戢 王延之 阮韜》][550] | [JSON](pbz_pni_tco_A.json) |
| `AA` | 何婧英 | [《南史・后妃上》][725]、[《南史・后妃上》][726] | [JSON](pbz_pni_tco_AA.json) |

</details>

<details><summary><code>pev_wez_mab</code> 宋富人（老韓列傳候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 宋富人 | [《史記・老子韓非列傳》][1188] | [JSON](pev_wez_mab.json) |
| `A` | 富人之子 | [《史記・老子韓非列傳》][1188] | [JSON](pev_wez_mab_A.json) |

</details>

<details><summary><code>pg6_rqk_vuk</code> 如姬父未名（魏公子列傳候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 如姬父未名 | [《史記・魏公子列傳》][1202] | [JSON](pg6_rqk_vuk.json) |
| `A` | 如姬 | [《史記・魏公子列傳》][1202] | [JSON](pg6_rqk_vuk_A.json) |

</details>

<details><summary><code>pgd_uvb_jwn</code> 羊瞻（南中郎長史）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 羊瞻（南中郎長史） | [《宋書・后妃》][1347] | [JSON](pgd_uvb_jwn.json) |
| `A` | 羊瞻女（宋前廢帝為太子時良娣） | — | [JSON](pgd_uvb_jwn_A.json) |

</details>

<details><summary><code>ph1_ms8_hyq</code> 亮〔孝懿蕭后祖；字保祚〕（7 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 亮〔孝懿蕭后祖；字保祚〕 | [《宋書・后妃》][1350] | [JSON](ph1_ms8_hyq.json) |
| `A` | 蕭卓 | [《宋書・后妃》][1350] | [JSON](ph1_ms8_hyq_A.json) |
| `AA` | 蕭文夀〔孝懿皇后〕 | [《宋書・后妃》][1350] | [JSON](ph1_ms8_hyq_AA.json) |
| `AB` | 源之〔蕭卓子〕 | [《宋書・后妃》][1350] | [JSON](ph1_ms8_hyq_AB.json) |
| `ABA` | 蕭思話 | [《宋書・胡藩 劉康祖 垣護之 張興世》][1472] | [JSON](ph1_ms8_hyq_ABA.json) |
| `ABAA` | 蕭惠基 | [《南齊書・王秀之 王慈 蔡約 陸慧曉 顧憲之 蕭惠基》][655] | [JSON](ph1_ms8_hyq_ABAA.json) |
| `ABAB` | 蕭惠明（蕭思話次子） | [《南史・王誕　王華　王惠　王彧》][864]、[《宋書・蕭思話 劉延孫》][1525] | [JSON](ph1_ms8_hyq_ABAB.json) |

</details>

<details><summary><code>pib_5me_1wm</code> 陳肇之（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 陳肇之 | [《南齊書・皇后》][508]、[《南齊書・皇后》][507] | [JSON](pib_5me_1wm.json) |
| `A` | 陳道止 | [《南史・后妃上》][719]、[《南史・后妃上》][720] | [JSON](pib_5me_1wm_A.json) |

</details>

<details><summary><code>pj3_k53_wtj</code> 觸龍（趙世家左師候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 觸龍 | [《史記・趙世家》][1168] | [JSON](pj3_k53_wtj.json) |
| `A` | 舒祺 | [《史記・趙世家》][1168] | [JSON](pj3_k53_wtj_A.json) |

</details>

<details><summary><code>pme_eis_xqi</code> 司馬錯（7 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 司馬錯 | [《史記・秦本紀》][1147] | [JSON](pme_eis_xqi.json) |
| `*A` | 司馬靳 | [《史記・太史公自序》][1255] | [JSON](pme_eis_xqi_%2AA.json) |
| `*A*A` | 司馬昌 | [《史記・太史公自序》][1255] | [JSON](pme_eis_xqi_%2AA%2AA.json) |
| `*A*AA` | 司馬無澤 | [《史記・太史公自序》][1255] | [JSON](pme_eis_xqi_%2AA%2AAA.json) |
| `*A*AAA` | 司馬喜 | [《史記・太史公自序》][1255] | [JSON](pme_eis_xqi_%2AA%2AAAA.json) |
| `*A*AAAA` | 司馬談 | [《史記・太史公自序》][1255] | [JSON](pme_eis_xqi_%2AA%2AAAAA.json) |
| `*A*AAAAA` | 司馬遷 | [《史記・太史公自序》][1255] | [JSON](pme_eis_xqi_%2AA%2AAAAAA.json) |

</details>

<details><summary><code>pne_ii9_42q</code> 王廣〔西揚州刺史〕（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 王廣〔西揚州刺史〕 | [《太平御覽・人事部八十一》][1598] | [JSON](pne_ii9_42q.json) |
| `A` | 王氏〔西揚州刺史王廣女〕 | [《晉書・列女》][333]、[《晉書・列女》][332]、[《太平御覽・人事部八十一》][1598]、[《太平御覽・宗親部九》][1600] | [JSON](pne_ii9_42q_A.json) |

</details>

<details><summary><code>ptn_sz3_vro</code> 劉義慶（4 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 劉義慶 | [《宋書・謝靈運》][1511] | [JSON](ptn_sz3_vro.json) |
| `A` | 臨川王義慶女（王僧達妻，未名） | [《宋書・王僧達 顏竣》][1520] | [JSON](ptn_sz3_vro_A.json) |
| `B` | 劉燁（字景舒，臨川哀王） | [《南史・宋宗室及諸王上》][768] | [JSON](ptn_sz3_vro_B.json) |
| `BA` | 劉綽（宋宗室） | [《南史・后妃上》][746]、[《南史・后妃上》][747]、[《南史・宋宗室及諸王上》][768]、[《宋書・后妃》][1352] | [JSON](ptn_sz3_vro_BA.json) |

</details>

<details><summary><code>pyb_nda_bwz</code> 鄖公與懷之父（伍胥列傳候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 鄖公與懷之父 | [《史記・伍子胥列傳》][1191] | [JSON](pyb_nda_bwz.json) |
| `A` | 懷 | [《史記・伍子胥列傳》][1191] | [JSON](pyb_nda_bwz_A.json) |

</details>

<details><summary><code>q1y_uet_htw</code> 伯州犁（伍胥列傳候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 伯州犁 | [《史記・伍子胥列傳》][1191] | [JSON](q1y_uet_htw.json) |
| `*A` | 伯嚭 | [《史記・伍子胥列傳》][1191] | [JSON](q1y_uet_htw_%2AA.json) |

</details>

<details><summary><code>q4c_ppp_p5h</code> 徐熙（濮陽太守）（6 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 徐熙（濮陽太守） | [《南史・張邵》][907] | [JSON](q4c_ppp_p5h.json) |
| `A` | 徐秋夫（射陽令） | [《南史・張邵》][907] | [JSON](q4c_ppp_p5h_A.json) |
| `AA` | 徐道度（蘭陵太守，徐文伯父） | [《南史・張邵》][907] | [JSON](q4c_ppp_p5h_AA.json) |
| `AAA` | 徐文伯（字德秀，徐道度子） | [《南史・張邵》][907] | [JSON](q4c_ppp_p5h_AAA.json) |
| `AB` | 徐叔向（徐嗣伯父） | [《南史・張邵》][907] | [JSON](q4c_ppp_p5h_AB.json) |
| `ABA` | 徐嗣伯（字叔紹，徐叔向子） | [《南史・張邵》][907] | [JSON](q4c_ppp_p5h_ABA.json) |

</details>

<details><summary><code>q60_34y_1zh</code> 章（楚惠王）（5 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 章（楚惠王） | [《史記・楚世家》][1165] | [JSON](q60_34y_1zh.json) |
| `A` | 中（楚簡王） | [《史記・楚世家》][1165] | [JSON](q60_34y_1zh_A.json) |
| `AA` | 當（楚聲王） | [《史記・楚世家》][1165] | [JSON](q60_34y_1zh_AA.json) |
| `AAA` | 熊疑（楚悼王） | [《史記・范睢蔡澤列傳》][1204] | [JSON](q60_34y_1zh_AAA.json) |
| `AAAA` | 臧（楚肅王） | [《史記・楚世家》][1165] | [JSON](q60_34y_1zh_AAAA.json) |

</details>

<details><summary><code>q63_4br_3of</code> 江德隣（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 江德隣 | [《南史・荀伯玉　崔祖思　蘇侃　虞悰　胡諧之　虞玩之　劉休　江祏》][931] | [JSON](q63_4br_3of.json) |
| `A` | 江祏 | [《南齊書・王晏 蕭諶 蕭坦之 江祏》][616] | [JSON](q63_4br_3of_A.json) |
| `B` | 江祀 | [《南齊書・王晏 蕭諶 蕭坦之 江祏》][616] | [JSON](q63_4br_3of_B.json) |

</details>

<details><summary><code>q69_35n_f3h</code> 公孫弘（平津侯主父列傳候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 公孫弘 | [《史記・平津侯主父列傳》][1237] | [JSON](q69_35n_f3h.json) |
| `A` | 公孫度 | [《史記・平津侯主父列傳》][1237] | [JSON](q69_35n_f3h_A.json) |

</details>

<details><summary><code>q6w_qm5_w2b</code> 丹（趙世家孝成王候選）（4 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 丹 | [《史記・平原君虞卿列傳》][1201] | [JSON](q6w_qm5_w2b.json) |
| `A` | 偃 | [《史記・趙世家》][1168] | [JSON](q6w_qm5_w2b_A.json) |
| `AA` | 趙王遷 | [《史記・趙世家》][1168] | [JSON](q6w_qm5_w2b_AA.json) |
| `AB` | 代王嘉 | [《史記・秦始皇本紀》][1148]、[《史記・六國年表》][1680] | [JSON](q6w_qm5_w2b_AB.json) |

</details>

<details><summary><code>q71_dto_v57</code> 秦宜禄（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 秦宜禄 | [《三國志・諸夏侯曹傳》][971] | [JSON](q71_dto_v57.json) |
| `A` | 秦朗 | [《三國志・諸夏侯曹傳》][971] | [JSON](q71_dto_v57_A.json) |

</details>

<details><summary><code>q7c_rp0_s04</code> 趙主父（楚篇懷王奔趙時）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 趙主父（楚篇懷王奔趙時） | [《史記・楚世家》][1165] | [JSON](q7c_rp0_s04.json) |
| `A` | 趙惠王（楚篇初立者） | [《史記・楚世家》][1165] | [JSON](q7c_rp0_s04_A.json) |

</details>

<details><summary><code>q7m_r8k_2vn</code> 王僧朗（35 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 王僧朗 | [《南史・王誕　王華　王惠　王彧》][863]、[《南史・范岫　傅昭　孔休源　江革　徐勉　許懋　殷鈞》][959] | [JSON](q7m_r8k_2vn.json) |
| `A` | 王粹 | [《南史・王誕　王華　王惠　王彧》][849] | [JSON](q7m_r8k_2vn_A.json) |
| `AA` | 王奐 | [《南齊書・王奐 從弟繢 張沖》][667] | [JSON](q7m_r8k_2vn_AA.json) |
| `AAA` | 王琛 | [《南史・王誕　王華　王惠　王彧》][849] | [JSON](q7m_r8k_2vn_AAA.json) |
| `AAAA` | 王翊 | [《王翊墓誌・節錄》][90] | [JSON](q7m_r8k_2vn_AAAA.json) |
| `AAAAA` | 王令媛 | [《王令媛墓誌・節錄》][88] | [JSON](q7m_r8k_2vn_AAAAA.json) |
| `AAB` | 王融（王奐長子） | [《南齊書・王奐 從弟繢 張沖》][668]、[《南史・王誕　王華　王惠　王彧》][849] | [JSON](q7m_r8k_2vn_AAB.json) |
| `AAC` | 王彪（王奐第三子） | [《南齊書・王奐 從弟繢 張沖》][667] | [JSON](q7m_r8k_2vn_AAC.json) |
| `AAD` | 王爽（王彪弟） | [《南齊書・王奐 從弟繢 張沖》][667]、[《南齊書・王奐 從弟繢 張沖》][668]、[《南史・王誕　王華　王惠　王彧》][849] | [JSON](q7m_r8k_2vn_AAD.json) |
| `AAE` | 王弼（王彪弟） | [《南齊書・王奐 從弟繢 張沖》][667]、[《南齊書・王奐 從弟繢 張沖》][668]、[《南史・王誕　王華　王惠　王彧》][849] | [JSON](q7m_r8k_2vn_AAE.json) |
| `AAF` | 王秉（字文政） | [《魏書・王肅 宋弁》][1622] | [JSON](q7m_r8k_2vn_AAF.json) |
| `AAG` | 王奐女（殷叡妻） | [《梁書・陸倕 到洽 明山賓 殷鈞 陸襄》][425]、[《南史・王誕　王華　王惠　王彧》][849] | [JSON](q7m_r8k_2vn_AAG.json) |
| `AB` | 王份 | [《梁書・王瞻 王志 王峻 王暕 子訓 王泰 王份 孫鍚 僉 張充 柳惲 蔡撙 江蒨》][402] | [JSON](q7m_r8k_2vn_AB.json) |
| `ABA` | 王琳 | [《梁書・王瞻 王志 王峻 王暕 子訓 王泰 王份 孫鍚 僉 張充 柳惲 蔡撙 江蒨》][402]、[《南史・王誕　王華　王惠　王彧》][844]、[《南史・王誕　王華　王惠　王彧》][845] | [JSON](q7m_r8k_2vn_ABA.json) |
| `ABAA` | 王銓 | [《南史・王誕　王華　王惠　王彧》][844] | [JSON](q7m_r8k_2vn_ABAA.json) |
| `ABAAA` | 王溥（字伯淮） | [《南史・王誕　王華　王惠　王彧》][844] | [JSON](q7m_r8k_2vn_ABAAA.json) |
| `ABAB` | 王錫 | [《南史・王誕　王華　王惠　王彧》][859] | [JSON](q7m_r8k_2vn_ABAB.json) |
| `ABABA` | 王㳬 | [《周書・列傳第40 蕭詧》][1643] | [JSON](q7m_r8k_2vn_ABABA.json) |
| `ABABAA` | 王瓘 | [《周書・列傳第40 蕭詧》][1643] | [JSON](q7m_r8k_2vn_ABABAA.json) |
| `ABABB` | 王湜 | [《梁書・王瞻 王志 王峻 王暕 子訓 王泰 王份 孫鍚 僉 張充 柳惲 蔡撙 江蒨》][400]、[《梁書・王瞻 王志 王峻 王暕 子訓 王泰 王份 孫鍚 僉 張充 柳惲 蔡撙 江蒨》][402]、[《南史・王誕　王華　王惠　王彧》][841]、[《南史・王誕　王華　王惠　王彧》][859]、[《周書・列傳第40 蕭詧》][1643] | [JSON](q7m_r8k_2vn_ABABB.json) |
| `ABABBA` | 王懷 | [《周書・列傳第40 蕭詧》][1643] | [JSON](q7m_r8k_2vn_ABABBA.json) |
| `ABAC` | 王通 | [《陳書・列傳第十一: 王沖 王通 袁敬》][53] | [JSON](q7m_r8k_2vn_ABAC.json) |
| `ABAD` | 王質 | [《南史・王誕　王華　王惠　王彧》][866] | [JSON](q7m_r8k_2vn_ABAD.json) |
| `ABAE` | 王固 | [《南史・王誕　王華　王惠　王彧》][846] | [JSON](q7m_r8k_2vn_ABAE.json) |
| `ABAEA` | 王寬 | [《陳書・列傳第十五: 謝哲 蕭乾 謝嘏 張種 王固 孔奐 蕭允》][59]、[《南史・王誕　王華　王惠　王彧》][846] | [JSON](q7m_r8k_2vn_ABAEA.json) |
| `ABAEB` | 陳廢帝王皇后（王固女，臨海王妃） | [《陳書・本紀第三: 世祖》][12]、[《陳書・本紀第四: 廢帝》][14]、[《陳書・皇后》][30]、[《陳書・皇后》][31]、[《南史・后妃下》][753] | [JSON](q7m_r8k_2vn_ABAEB.json) |
| `ABAF` | 王僉（字公會） | [《梁書・王瞻 王志 王峻 王暕 子訓 王泰 王份 孫鍚 僉 張充 柳惲 蔡撙 江蒨》][402] | [JSON](q7m_r8k_2vn_ABAF.json) |
| `ABAFA` | 王氏（梁敬帝皇后、王僉女） | [《梁書・敬帝》][375]、[《南史・后妃下》][756] | [JSON](q7m_r8k_2vn_ABAFA.json) |
| `ABAG` | 王勱（陳書字公濟、南史字公齊） | [《陳書・列傳第十一: 王沖 王通 袁敬》][51] | [JSON](q7m_r8k_2vn_ABAG.json) |
| `AC` | 王伷（王奐弟） | [《南齊書・王奐 從弟繢 張沖》][668]、[《南史・王誕　王華　王惠　王彧》][849] | [JSON](q7m_r8k_2vn_AC.json) |
| `ACA` | 王伷女（長沙王晃妃） | [《南齊書・王奐 從弟繢 張沖》][668]、[《南史・王誕　王華　王惠　王彧》][849] | [JSON](q7m_r8k_2vn_ACA.json) |
| `B` | 王貞風（明恭王皇后） | [《南史・后妃上》][746]、[《南史・后妃上》][747] | [JSON](q7m_r8k_2vn_B.json) |
| `C` | 王楷（王蘊父） | [《古今姓氏書辯證・卷十四》][98]、[《南史・王誕　王華　王惠　王彧》][864] | [JSON](q7m_r8k_2vn_C.json) |
| `D` | 王彧姊（宋書載墓開，未名） | — | [JSON](q7m_r8k_2vn_D.json) |
| `E` | 王氏（王僧朗女，殷元素妻） | — | [JSON](q7m_r8k_2vn_E.json) |

</details>

<details><summary><code>q8m_d0c_kq3</code> 楚莊王（13 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 楚莊王 | [《史記・楚世家》][1165] | [JSON](q8m_d0c_kq3.json) |
| `A` | 審（楚共王） | [《史記・楚世家》][1165] | [JSON](q8m_d0c_kq3_A.json) |
| `AA` | 招（楚康王） | [《史記・楚世家》][1165] | [JSON](q8m_d0c_kq3_AA.json) |
| `AAA` | 員（郟敖） | [《史記・楚世家》][1165] | [JSON](q8m_d0c_kq3_AAA.json) |
| `AAAA` | 莫（郟敖子） | [《史記・楚世家》][1165] | [JSON](q8m_d0c_kq3_AAAA.json) |
| `AAAB` | 平夏（郟敖子） | [《史記・楚世家》][1165] | [JSON](q8m_d0c_kq3_AAAB.json) |
| `AB` | 圍 | [《史記・楚世家》][1165] | [JSON](q8m_d0c_kq3_AB.json) |
| `AC` | 子比（楚初王） | [《史記・楚世家》][1165] | [JSON](q8m_d0c_kq3_AC.json) |
| `AD` | 子皙（楚令尹） | [《史記・楚世家》][1165] | [JSON](q8m_d0c_kq3_AD.json) |
| `AE` | 楚平王 | [《史記・楚世家》][1165] | [JSON](q8m_d0c_kq3_AE.json) |
| `AEA` | 楚昭王 | [《史記・楚世家》][1165] | [JSON](q8m_d0c_kq3_AEA.json) |
| `AEB` | 楚太子建 | [《史記・伍子胥列傳》][1191] | [JSON](q8m_d0c_kq3_AEB.json) |
| `AEBA` | 白公勝 | [《史記・伍子胥列傳》][1191] | [JSON](q8m_d0c_kq3_AEBA.json) |

</details>

<details><summary><code>qdt_1oy_jci</code> 杵臼（陳宣公）（7 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 杵臼（陳宣公） | [《史記・陳杞世家》][1161] | [JSON](qdt_1oy_jci.json) |
| `A` | 款（陳穆公） | [《史記・陳杞世家》][1161] | [JSON](qdt_1oy_jci_A.json) |
| `AA` | 朔（陳共公） | [《史記・陳杞世家》][1161] | [JSON](qdt_1oy_jci_AA.json) |
| `AAA` | 平國（陳靈公） | [《史記・陳杞世家》][1161] | [JSON](qdt_1oy_jci_AAA.json) |
| `AAAA` | 午（陳成公） | [《史記・陳杞世家》][1161] | [JSON](qdt_1oy_jci_AAAA.json) |
| `AAAAA` | 哀公（陳君） | [《史記・陳杞世家》][1161] | [JSON](qdt_1oy_jci_AAAAA.json) |
| `B` | 御寇（陳宣公太子） | [《史記・陳杞世家》][1161] | [JSON](qdt_1oy_jci_B.json) |

</details>

<details><summary><code>qg7_n12_fne</code> 審食其（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 審食其 | [《史記・酈生陸賈列傳》][1222] | [JSON](qg7_n12_fne.json) |
| `*A` | 審卿 | [《史記・淮南衡山列傳》][1243] | [JSON](qg7_n12_fne_%2AA.json) |

</details>

<details><summary><code>qh8_95j_eh2</code> 獻舞（蔡哀侯）（10 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 獻舞（蔡哀侯） | [《史記・管蔡世家》][1160] | [JSON](qh8_95j_eh2.json) |
| `A` | 肸（蔡繆侯） | [《史記・管蔡世家》][1160] | [JSON](qh8_95j_eh2_A.json) |
| `AA` | 果（蔡莊侯） | [《史記・管蔡世家》][1160] | [JSON](qh8_95j_eh2_AA.json) |
| `AAA` | 申（蔡文侯） | [《史記・管蔡世家》][1160] | [JSON](qh8_95j_eh2_AAA.json) |
| `AAAA` | 固（蔡景侯） | [《史記・管蔡世家》][1160] | [JSON](qh8_95j_eh2_AAAA.json) |
| `AAAAA` | 般（蔡靈侯） | [《史記・管蔡世家》][1160] | [JSON](qh8_95j_eh2_AAAAA.json) |
| `AAAAAA` | 友（蔡隱太子） | [《史記・管蔡世家》][1160] | [JSON](qh8_95j_eh2_AAAAAA.json) |
| `AAAAAAA` | 東國（蔡悼侯） | [《史記・管蔡世家》][1160] | [JSON](qh8_95j_eh2_AAAAAAA.json) |
| `AAAAB` | 廬（蔡平侯） | [《史記・管蔡世家》][1160] | [JSON](qh8_95j_eh2_AAAAB.json) |
| `AAAABA` | 平侯子（被東國攻者未名） | [《史記・管蔡世家》][1160] | [JSON](qh8_95j_eh2_AAAABA.json) |

</details>

<details><summary><code>qhp_lk5_t1e</code> 李延年父（未名）（佞幸列傳候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 李延年父（未名） | [《史記・佞幸列傳》][1250] | [JSON](qhp_lk5_t1e.json) |
| `A` | 李延年 | [《史記・佞幸列傳》][1250] | [JSON](qhp_lk5_t1e_A.json) |

</details>

<details><summary><code>qid_wbb_2pi</code> 孔景偉（孔範曾祖）（4 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 孔景偉（孔範曾祖） | [《南史・恩倖》][967] | [JSON](qid_wbb_2pi.json) |
| `A` | 孔滔（孔範祖） | [《南史・恩倖》][967] | [JSON](qid_wbb_2pi_A.json) |
| `AA` | 孔岱（孔範父） | [《南史・恩倖》][967] | [JSON](qid_wbb_2pi_AA.json) |
| `AAA` | 孔範（字法言） | [《南史・恩倖》][967] | [JSON](qid_wbb_2pi_AAA.json) |

</details>

<details><summary><code>qil_wym_gc2</code> 歐陽景達（歐陽頠祖）（4 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 歐陽景達（歐陽頠祖） | [《陳書・列傳第三: 侯瑱 歐陽頠 吳明徹 裴子烈》][38] | [JSON](qil_wym_gc2.json) |
| `A` | 歐陽僧寶（歐陽頠父） | [《陳書・列傳第三: 侯瑱 歐陽頠 吳明徹 裴子烈》][38] | [JSON](qil_wym_gc2_A.json) |
| `AA` | 歐陽頠（字靖世） | [《陳書・列傳第三: 侯瑱 歐陽頠 吳明徹 裴子烈》][38]、[《陳書・列傳第十一: 王沖 王通 袁敬》][54] | [JSON](qil_wym_gc2_AA.json) |
| `AAA` | 歐陽紇（歐陽頠子，字奉聖） | [《陳書・列傳第十一: 王沖 王通 袁敬》][54] | [JSON](qil_wym_gc2_AAA.json) |

</details>

<details><summary><code>qjs_3hl_6ck</code> 公子發（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 公子發 | [《春秋左傳注疏・卷三十》][1677] | [JSON](qjs_3hl_6ck.json) |
| `A` | 子産 | [《史記・鄭世家》][1167] | [JSON](qjs_3hl_6ck_A.json) |

</details>

<details><summary><code>qkm_hps_nmk</code> 劉爽（劉秀之祖）（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 劉爽（劉秀之祖） | [《宋書・劉秀之 顧琛 顧覬之》][1534] | [JSON](qkm_hps_nmk.json) |
| `A` | 劉仲道（劉秀之父） | [《宋書・劉秀之 顧琛 顧覬之》][1534] | [JSON](qkm_hps_nmk_A.json) |
| `AA` | 劉秀之（字道寶） | [《宋書・劉秀之 顧琛 顧覬之》][1534] | [JSON](qkm_hps_nmk_AA.json) |

</details>

<details><summary><code>qkt_yf2_rsg</code> 阮長之（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 阮長之 | [《宋書・良吏》][1557] | [JSON](qkt_yf2_rsg.json) |
| `A` | 阮師門（原鄉令） | [《南史・循吏》][966]、[《宋書・良吏》][1558] | [JSON](qkt_yf2_rsg_A.json) |

</details>

<details><summary><code>qok_ik2_99j</code> 壽（齊悼惠王世家候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 壽 | [《史記・齊悼惠王世家》][1177] | [JSON](qok_ik2_99j.json) |
| `A` | 次景 | [《史記・齊悼惠王世家》][1177] | [JSON](qok_ik2_99j_A.json) |

</details>

<details><summary><code>qsd_v11_ya1</code> 宏（王懿祖）（4 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 宏（王懿祖） | [《南史・王懿　到彥之　垣護之　張興世》][892]、[《宋書・趙倫之 王懿 張邵》][1364]、[《宋書・趙倫之 王懿 張邵》][1363] | [JSON](qsd_v11_ya1.json) |
| `A` | 苖（王懿父） | [《南史・王懿　到彥之　垣護之　張興世》][892]、[《宋書・趙倫之 王懿 張邵》][1364]、[《宋書・趙倫之 王懿 張邵》][1363] | [JSON](qsd_v11_ya1_A.json) |
| `AA` | 王仲徳〔劉義隆鎮北將軍〕 | [《宋書・趙倫之 王懿 張邵》][1364]、[《宋書・趙倫之 王懿 張邵》][1363] | [JSON](qsd_v11_ya1_AA.json) |
| `AAA` | 正脩（王懿子） | [《南史・王懿　到彥之　垣護之　張興世》][891]、[《宋書・趙倫之 王懿 張邵》][1364]、[《宋書・趙倫之 王懿 張邵》][1363] | [JSON](qsd_v11_ya1_AAA.json) |

</details>

<details><summary><code>qvt_eq1_lcf</code> 蕭道賜（12 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 蕭道賜 | [《梁書・武帝上》][363] | [JSON](qvt_eq1_lcf.json) |
| `A` | 蕭順之 | [《資治通鑑・齊紀三》][1663] | [JSON](qvt_eq1_lcf_A.json) |
| `AA` | 蕭恢 | [《梁書・太祖五王》][414] | [JSON](qvt_eq1_lcf_AA.json) |
| `AAA` | 蕭循（宜豐侯） | [《陳書・列傳第十一: 王沖 王通 袁敬》][51]、[《南史・王誕　王華　王惠　王彧》][854]、[《資治通鑑・梁紀二十》][1672] | [JSON](qvt_eq1_lcf_AAA.json) |
| `AAB` | 蕭範（字世儀，鄱陽王） | [《梁書・裴邃 兄子之高 之平 之橫 夏侯亶 弟夔 魚弘附 韋放》][431] | [JSON](qvt_eq1_lcf_AAB.json) |
| `AABA` | 蕭嗣（字長胤） | [《梁書・太祖五王》][415]、[《梁書・裴邃 兄子之高 之平 之橫 夏侯亶 弟夔 魚弘附 韋放》][431]、[《梁書・韋粲 江子一 弟子四 子五 張嵊 沈浚 柳敬禮》][471] | [JSON](qvt_eq1_lcf_AABA.json) |
| `AB` | 蕭令嫕（義興昭長公主） | [《南史・王誕　王華　王惠　王彧》][844] | [JSON](qvt_eq1_lcf_AB.json) |
| `AC` | 蕭懿（長沙宣武王） | [《南齊書・魏虜》][710] | [JSON](qvt_eq1_lcf_AC.json) |
| `ACA` | 蕭淵明（梁貞陽侯，長沙宣武王懿子） | [《梁書・裴邃 兄子之高 之平 之橫 夏侯亶 弟夔 魚弘附 韋放》][437] | [JSON](qvt_eq1_lcf_ACA.json) |
| `AD` | 蕭敷（永陽昭王） | [《梁書・皇后》][383]、[《南史・后妃下》][764]、[《南史・后妃下》][766] | [JSON](qvt_eq1_lcf_AD.json) |
| `AE` | 蕭暢（衡陽宣王） | [《南齊書・宗室》][640] | [JSON](qvt_eq1_lcf_AE.json) |
| `AF` | 蕭偉（南平元襄王） | [《梁書・太祖五王》][412] | [JSON](qvt_eq1_lcf_AF.json) |

</details>

<details><summary><code>qxa_jm7_zmy</code> 黔（衛悼公）（10 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 黔（衛悼公） | [《史記・衛康叔世家》][1162] | [JSON](qxa_jm7_zmy.json) |
| `A` | 弗（衛敬公） | [《史記・衛康叔世家》][1162] | [JSON](qxa_jm7_zmy_A.json) |
| `AA` | 糾（衛昭公） | [《史記・衛康叔世家》][1162] | [JSON](qxa_jm7_zmy_AA.json) |
| `AB` | 適（衛公子） | [《史記・衛康叔世家》][1162] | [JSON](qxa_jm7_zmy_AB.json) |
| `ABA` | 穨（衛愼公） | [《史記・衛康叔世家》][1162] | [JSON](qxa_jm7_zmy_ABA.json) |
| `ABAA` | 訓（衛聲公） | [《史記・衛康叔世家》][1162] | [JSON](qxa_jm7_zmy_ABAA.json) |
| `ABAAA` | 遫（衛成侯） | [《史記・衛康叔世家》][1162] | [JSON](qxa_jm7_zmy_ABAAA.json) |
| `ABAAAA` | 平侯（衛成侯子） | [《史記・衛康叔世家》][1162] | [JSON](qxa_jm7_zmy_ABAAAA.json) |
| `ABAAAAA` | 嗣君（衛平侯子） | [《史記・衛康叔世家》][1162] | [JSON](qxa_jm7_zmy_ABAAAAA.json) |
| `ABAAAAAA` | 懷君（衛嗣君子） | [《史記・衛康叔世家》][1162] | [JSON](qxa_jm7_zmy_ABAAAAAA.json) |

</details>

<details><summary><code>qy1_adc_gam</code> 晉（衛宣公）（6 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 晉（衛宣公） | [《史記・衛康叔世家》][1162] | [JSON](qy1_adc_gam.json) |
| `A` | 伋（衛宣公太子） | [《史記・衛康叔世家》][1162] | [JSON](qy1_adc_gam_A.json) |
| `AA` | 太子伋之子（未名） | [《史記・衛康叔世家》][1162] | [JSON](qy1_adc_gam_AA.json) |
| `B` | 壽（衛宣公子） | [《史記・衛康叔世家》][1162] | [JSON](qy1_adc_gam_B.json) |
| `C` | 朔（衛惠公） | [《史記・衛康叔世家》][1162] | [JSON](qy1_adc_gam_C.json) |
| `CA` | 赤（衛懿公） | [《史記・衛康叔世家》][1162] | [JSON](qy1_adc_gam_CA.json) |

</details>

<details><summary><code>r5n_x7v_cwf</code> 彪〔孝穆趙后祖；字世範〕（8 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 彪〔孝穆趙后祖；字世範〕 | [《宋書・后妃》][1350] | [JSON](r5n_x7v_cwf.json) |
| `A` | 趙裔 | [《宋書・后妃》][1350] | [JSON](r5n_x7v_cwf_A.json) |
| `AA` | 宣之〔趙裔長子〕 | [《宋書・后妃》][1350] | [JSON](r5n_x7v_cwf_AA.json) |
| `AB` | 趙安〔孝穆皇后；本見證，高祖之母〕 | [《宋書・后妃》][1350] | [JSON](r5n_x7v_cwf_AB.json) |
| `AC` | 倫之〔宣之弟〕 | [《宋書・趙倫之 王懿 張邵》][1377] | [JSON](r5n_x7v_cwf_AC.json) |
| `ACA` | 趙伯符（字潤遠） | [《宋書・趙倫之 王懿 張邵》][1376] | [JSON](r5n_x7v_cwf_ACA.json) |
| `ACA*A` | 趙勗（趙伯符孫） | [《宋書・趙倫之 王懿 張邵》][1375]、[《宋書・趙倫之 王懿 張邵》][1379] | [JSON](r5n_x7v_cwf_ACA%2AA.json) |
| `ACAA` | 趙倩（趙伯符子） | [《宋書・趙倫之 王懿 張邵》][1375]、[《宋書・趙倫之 王懿 張邵》][1378] | [JSON](r5n_x7v_cwf_ACAA.json) |

</details>

<details><summary><code>r6c_fhk_jo9</code> 韓太傅（儒林列傳候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 韓太傅 | [《史記・儒林列傳》][1246] | [JSON](r6c_fhk_jo9.json) |
| `*A` | 韓生孫商 | [《史記・儒林列傳》][1246] | [JSON](r6c_fhk_jo9_%2AA.json) |

</details>

<details><summary><code>r9u_j0z_xtb</code> 秦侯（5 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 秦侯 | [《史記・秦本紀》][1147] | [JSON](r9u_j0z_xtb.json) |
| `A` | 公伯 | [《史記・秦本紀》][1147] | [JSON](r9u_j0z_xtb_A.json) |
| `AA` | 秦仲 | [《史記・秦本紀》][1147] | [JSON](r9u_j0z_xtb_AA.json) |
| `AAA` | 秦莊公 | [《史記・秦本紀》][1147] | [JSON](r9u_j0z_xtb_AAA.json) |
| `AAAA` | 世父 | [《史記・秦本紀》][1147] | [JSON](r9u_j0z_xtb_AAAA.json) |

</details>

<details><summary><code>ra9_o4d_rli</code> 竇長君（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 竇長君 | [《史記・外戚世家》][1174]、[《史記・季布欒布列傳》][1225] | [JSON](ra9_o4d_rli.json) |
| `A` | 彭祖 | [《史記・外戚世家》][1174] | [JSON](ra9_o4d_rli_A.json) |

</details>

<details><summary><code>rdo_wsn_30x</code> 東樓公（杞君）（8 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 東樓公（杞君） | [《史記・陳杞世家》][1161] | [JSON](rdo_wsn_30x.json) |
| `A` | 西樓公（杞君） | [《史記・陳杞世家》][1161] | [JSON](rdo_wsn_30x_A.json) |
| `AA` | 題公（杞君） | [《史記・陳杞世家》][1161] | [JSON](rdo_wsn_30x_AA.json) |
| `AAA` | 謀娶公（杞君） | [《史記・陳杞世家》][1161] | [JSON](rdo_wsn_30x_AAA.json) |
| `AAAA` | 武公（杞君） | [《史記・陳杞世家》][1161] | [JSON](rdo_wsn_30x_AAAA.json) |
| `AAAAA` | 靖公（杞君） | [《史記・陳杞世家》][1161] | [JSON](rdo_wsn_30x_AAAAA.json) |
| `AAAAAA` | 共公（杞君） | [《史記・陳杞世家》][1161] | [JSON](rdo_wsn_30x_AAAAAA.json) |
| `AAAAAAA` | 德公（杞君） | [《史記・陳杞世家》][1161] | [JSON](rdo_wsn_30x_AAAAAAA.json) |

</details>

<details><summary><code>rex_cs0_mfo</code> 鮑革（宋文公）（12 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 鮑革（宋文公） | [《史記・宋微子世家》][1163] | [JSON](rex_cs0_mfo.json) |
| `A` | 瑕（宋共公） | [《史記・宋微子世家》][1163] | [JSON](rex_cs0_mfo_A.json) |
| `AA` | 戌（本版宋平公） | [《史記・宋微子世家》][1163] | [JSON](rex_cs0_mfo_AA.json) |
| `AAA` | 佐（宋元公） | [《史記・宋微子世家》][1163] | [JSON](rex_cs0_mfo_AAA.json) |
| `AAAA` | 頭曼（宋景公） | [《史記・宋微子世家》][1163] | [JSON](rex_cs0_mfo_AAAA.json) |
| `AAAB` | 褍秦（宋元公少子） | [《史記・宋微子世家》][1163] | [JSON](rex_cs0_mfo_AAAB.json) |
| `AAABA` | 糾（宋公孫） | [《史記・宋微子世家》][1163] | [JSON](rex_cs0_mfo_AAABA.json) |
| `AAABAA` | 特（後宋昭公） | [《史記・宋微子世家》][1163] | [JSON](rex_cs0_mfo_AAABAA.json) |
| `AAABAAA` | 購由（宋悼公） | [《史記・宋微子世家》][1163] | [JSON](rex_cs0_mfo_AAABAAA.json) |
| `AAABAAAA` | 田（宋休公） | [《史記・宋微子世家》][1163] | [JSON](rex_cs0_mfo_AAABAAAA.json) |
| `AAABAAAAA` | 辟兵（宋辟公） | [《史記・宋微子世家》][1163] | [JSON](rex_cs0_mfo_AAABAAAAA.json) |
| `AAABAAAAAA` | 剔成（宋君） | [《史記・宋微子世家》][1163] | [JSON](rex_cs0_mfo_AAABAAAAAA.json) |

</details>

<details><summary><code>rl6_a40_3hj</code> 馮唐祖父未名（張釋之馮唐列傳候選）（4 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 馮唐祖父未名 | [《史記・張釋之馮唐列傳》][1227] | [JSON](rl6_a40_3hj.json) |
| `A` | 馮唐父未名 | [《史記・張釋之馮唐列傳》][1227] | [JSON](rl6_a40_3hj_A.json) |
| `AA` | 馮唐 | [《史記・張釋之馮唐列傳》][1227] | [JSON](rl6_a40_3hj_AA.json) |
| `AAA` | 馮遂 | [《史記・張釋之馮唐列傳》][1227] | [JSON](rl6_a40_3hj_AAA.json) |

</details>

<details><summary><code>rlk_lzd_86c</code> 澄〔王衍弟，荊州刺史〕（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 澄〔王衍弟，荊州刺史〕 | [《晉書・山濤 王戎 郭舒 樂廣》][217] | [JSON](rlk_lzd_86c.json) |
| `A` | 王詹〔王澄長子〕 | [《晉書・山濤 王戎 郭舒 樂廣》][217] | [JSON](rlk_lzd_86c_A.json) |
| `B` | 王徽〔王澄子，右軍司馬〕 | [《世說新語・言語》][1264] | [JSON](rlk_lzd_86c_B.json) |

</details>

<details><summary><code>rlv_clg_euu</code> 丕鄭（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 丕鄭 | [《史記・晉世家》][1164] | [JSON](rlv_clg_euu.json) |
| `A` | 丕豹 | [《史記・秦本紀》][1147] | [JSON](rlv_clg_euu_A.json) |

</details>

<details><summary><code>roi_rz4_ute</code> 張昭（吳，字子布）（6 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 張昭（吳，字子布） | [《三國志・張顧諸葛步傳》][1047] | [JSON](roi_rz4_ute.json) |
| `A` | 張休 | [《三國志・張顧諸葛步傳》][1046] | [JSON](roi_rz4_ute_A.json) |
| `B` | 張承 | [《三國志・張顧諸葛步傳》][1044] | [JSON](roi_rz4_ute_B.json) |
| `BA` | 張震 | [《三國志・張顧諸葛步傳》][1044] | [JSON](roi_rz4_ute_BA.json) |
| `BB` | 張氏〔張承女、孫和嫡妃〕 | [《三國志・吳主五子傳》][1106] | [JSON](roi_rz4_ute_BB.json) |
| `BC` | 張氏〔張承女、陸景母〕 | [《三國志・陸遜傳》][1100] | [JSON](roi_rz4_ute_BC.json) |

</details>

<details><summary><code>rpj_ksb_fh9</code> 陳武〔吳字子烈、陳表父〕（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 陳武〔吳字子烈、陳表父〕 | [《三國志・程黃韓蔣周陳董甘淩徐潘丁傳》][1069] | [JSON](rpj_ksb_fh9.json) |
| `A` | 陳脩 | [《三國志・程黃韓蔣周陳董甘淩徐潘丁傳》][1067]、[《三國志・程黃韓蔣周陳董甘淩徐潘丁傳》][1069] | [JSON](rpj_ksb_fh9_A.json) |
| `AA` | 陳延 | [《三國志・程黃韓蔣周陳董甘淩徐潘丁傳》][1067] | [JSON](rpj_ksb_fh9_AA.json) |

</details>

<details><summary><code>rr8_o9c_jc1</code> 負芻（曹成公）（4 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 負芻（曹成公） | [《史記・管蔡世家》][1160] | [JSON](rr8_o9c_jc1.json) |
| `A` | 勝（曹武公） | [《史記・管蔡世家》][1160] | [JSON](rr8_o9c_jc1_A.json) |
| `AA` | 平公（曹武公子） | [《史記・管蔡世家》][1160] | [JSON](rr8_o9c_jc1_AA.json) |
| `AAA` | 午（曹悼公） | [《史記・管蔡世家》][1160] | [JSON](rr8_o9c_jc1_AAA.json) |

</details>

<details><summary><code>rsj_lxc_cbh</code> 橋公（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 橋公 | [《三國志・周瑜魯肅呂蒙傳》][1065] | [JSON](rsj_lxc_cbh.json) |
| `A` | 大橋〔橋公女、孫策所納〕 | [《三國志・周瑜魯肅呂蒙傳》][1065] | [JSON](rsj_lxc_cbh_A.json) |
| `B` | 小橋〔橋公女、周瑜所納〕 | [《三國志・周瑜魯肅呂蒙傳》][1065] | [JSON](rsj_lxc_cbh_B.json) |

</details>

<details><summary><code>rtd_v0b_nyn</code> 蕭綱（6 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 蕭綱 | [《梁書・陸倕 到洽 明山賓 殷鈞 陸襄》][417]、[《梁書・陸倕 到洽 明山賓 殷鈞 陸襄》][420]、[《梁書・裴邃 兄子之高 之平 之橫 夏侯亶 弟夔 魚弘附 韋放》][431]、[《梁書・裴邃 兄子之高 之平 之橫 夏侯亶 弟夔 魚弘附 韋放》][435]、[《梁書・高祖三王》][441]、[《梁書・文學下》][486]、[《梁書・文學下》][485]、[《南史・謝晦　謝裕　謝方明　謝靈運》][800]、[《南史・王曇首》][824]、[《南史・王曇首》][838]、[《南史・王曇首》][837]、[《南史・梁簡文帝諸子　　元帝諸子》][947] | [JSON](rtd_v0b_nyn.json) |
| `A` | 蕭大器（宣城王，哀太子） | [《梁書・昭明太子 哀太子 愍懷太子》][385] | [JSON](rtd_v0b_nyn_A.json) |
| `B` | 梁余姚公主（王溥妻） | [《南史・王誕　王華　王惠　王彧》][844]、[《文獻通考・卷二百五十八》][1629] | [JSON](rtd_v0b_nyn_B.json) |
| `C` | 蕭大連（梁南郡王，字仁靖） | [《梁書・太宗十一王 世祖二子》][476] | [JSON](rtd_v0b_nyn_C.json) |
| `D` | 蕭妙䂮（梁長山公主，南史作妙挈） | [《梁書・皇后》][379]、[《南史・后妃下》][761] | [JSON](rtd_v0b_nyn_D.json) |
| `E` | 蕭大心（梁尋陽王，初封當陽公） | [《梁書・裴邃 兄子之高 之平 之橫 夏侯亶 弟夔 魚弘附 韋放》][431] | [JSON](rtd_v0b_nyn_E.json) |

</details>

<details><summary><code>rvc_bqx_v5w</code> 湘東王繹（5 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 湘東王繹 | [《梁書・高祖三王》][449] | [JSON](rvc_bqx_v5w.json) |
| `A` | 蕭方等（忠壯世子，字實相） | [《梁書・太宗十一王 世祖二子》][478] | [JSON](rvc_bqx_v5w_A.json) |
| `B` | 蕭含貞（益昌公主） | [《梁書・皇后》][382]、[《南史・后妃下》][763] | [JSON](rvc_bqx_v5w_B.json) |
| `C` | 蕭方諸（貞惠世子，字智相） | [《梁書・太宗十一王 世祖二子》][478] | [JSON](rvc_bqx_v5w_C.json) |
| `D` | 蕭方矩（改名元良，愍懷太子） | [《陳書・列傳第十一: 王沖 王通 袁敬》][48] | [JSON](rvc_bqx_v5w_D.json) |

</details>

<details><summary><code>s11_z5r_y2z</code> 東方朔（滑稽列傳候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 東方朔 | [《史記・滑稽列傳》][1251] | [JSON](s11_z5r_y2z.json) |
| `A` | 東方朔子（未名） | [《史記・滑稽列傳》][1251] | [JSON](s11_z5r_y2z_A.json) |

</details>

<details><summary><code>s52_ysc_gyl</code> 太史慈（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 太史慈 | [《三國志・劉繇太史慈士燮傳》][1012] | [JSON](s52_ysc_gyl.json) |
| `A` | 太史享（太史慈子，字元復） | [《三國志・劉繇太史慈士燮傳》][1012] | [JSON](s52_ysc_gyl_A.json) |

</details>

<details><summary><code>sj9_pfu_fwh</code> 灌嬰（4 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 灌嬰 | [《史記・樊酈滕灌列傳》][1220] | [JSON](sj9_pfu_fwh.json) |
| `*A` | 灌賢 | [《史記・魏其武安列傳》][1232] | [JSON](sj9_pfu_fwh_%2AA.json) |
| `A` | 灌阿 | [《史記・樊酈滕灌列傳》][1220] | [JSON](sj9_pfu_fwh_A.json) |
| `AA` | 灌彊 | [《史記・樊酈滕灌列傳》][1220] | [JSON](sj9_pfu_fwh_AA.json) |

</details>

<details><summary><code>sjw_4mo_dlf</code> 徐生（儒林列傳候選）（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 徐生 | [《史記・儒林列傳》][1246] | [JSON](sjw_4mo_dlf.json) |
| `*A` | 徐延 | [《史記・儒林列傳》][1246] | [JSON](sjw_4mo_dlf_%2AA.json) |
| `*B` | 徐襄 | [《史記・儒林列傳》][1246] | [JSON](sjw_4mo_dlf_%2AB.json) |

</details>

<details><summary><code>sk1_f2q_pzy</code> 周景（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 周景 | [《三國志・周瑜魯肅呂蒙傳》][1065] | [JSON](sk1_f2q_pzy.json) |
| `A` | 周忠 | [《後漢書・袁張韓周列傳》][121]、[《三國志・周瑜魯肅呂蒙傳》][1065] | [JSON](sk1_f2q_pzy_A.json) |
| `AA` | 周暉〔忠子、洛陽令〕 | [《後漢書・袁張韓周列傳》][121] | [JSON](sk1_f2q_pzy_AA.json) |

</details>

<details><summary><code>sm1_jfi_7k2</code> 王獻之（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 王獻之 | [《晉書・王羲之》][310] | [JSON](sm1_jfi_7k2.json) |
| `A` | 王神愛 | [《晉書・安帝 恭帝》][185]、[《晉書・后妃下》][198]、[《太平御覽・皇親部十五》][1592] | [JSON](sm1_jfi_7k2_A.json) |

</details>

<details><summary><code>sn4_yf4_esv</code> 蒯恩（字道恩）（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 蒯恩（字道恩） | [《宋書・孫處 蒯恩 劉鍾 虞丘進》][1427] | [JSON](sn4_yf4_esv.json) |
| `A` | 蒯國才（蒯恩子） | [《宋書・孫處 蒯恩 劉鍾 虞丘進》][1426]、[《宋書・孫處 蒯恩 劉鍾 虞丘進》][1428] | [JSON](sn4_yf4_esv_A.json) |
| `AA` | 蒯慧度（蒯國才子） | [《宋書・孫處 蒯恩 劉鍾 虞丘進》][1426]、[《宋書・孫處 蒯恩 劉鍾 虞丘進》][1429] | [JSON](sn4_yf4_esv_AA.json) |

</details>

<details><summary><code>sno_cph_i2h</code> 周泰〔吳字幼平〕（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 周泰〔吳字幼平〕 | [《三國志・程黃韓蔣周陳董甘淩徐潘丁傳》][1079] | [JSON](sno_cph_i2h.json) |
| `A` | 周邵 | [《三國志・程黃韓蔣周陳董甘淩徐潘丁傳》][1079] | [JSON](sno_cph_i2h_A.json) |

</details>

<details><summary><code>snv_2iq_jes</code> 步騭（4 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 步騭 | [《三國志・張顧諸葛步傳》][1037] | [JSON](snv_2iq_jes.json) |
| `A` | 步協 | [《三國志・張顧諸葛步傳》][1037] | [JSON](snv_2iq_jes_A.json) |
| `AA` | 步璣 | [《三國志・張顧諸葛步傳》][1037] | [JSON](snv_2iq_jes_AA.json) |
| `AB` | 步璿 | [《三國志・張顧諸葛步傳》][1037] | [JSON](snv_2iq_jes_AB.json) |

</details>

<details><summary><code>spx_gk1_rrr</code> 徐湛之（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 徐湛之 | [《南史・王曇首》][830]、[《宋書・徐湛之 江湛 王僧綽》][1514]、[《宋書・徐湛之 江湛 王僧綽》][1512]、[《宋書・徐湛之 江湛 王僧綽》][1513] | [JSON](spx_gk1_rrr.json) |
| `A` | 徐湛之女（隨王誕妃，未名） | [《宋書・徐湛之 江湛 王僧綽》][1514] | [JSON](spx_gk1_rrr_A.json) |

</details>

<details><summary><code>sqi_qy6_6bu</code> 杜靈啓（杜崱祖）（5 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 杜靈啓（杜崱祖） | [《梁書・胡僧祐 徐文盛 杜崱 兄岸 弟幼安 兄子龕 陰子春》][479] | [JSON](sqi_qy6_6bu.json) |
| `A` | 杜懷寶（杜崱父） | [《梁書・胡僧祐 徐文盛 杜崱 兄岸 弟幼安 兄子龕 陰子春》][479] | [JSON](sqi_qy6_6bu_A.json) |
| `AA` | 杜崱（京兆杜陵） | [《梁書・胡僧祐 徐文盛 杜崱 兄岸 弟幼安 兄子龕 陰子春》][479] | [JSON](sqi_qy6_6bu_AA.json) |
| `AB` | 杜岑（杜崱兄） | [《梁書・胡僧祐 徐文盛 杜崱 兄岸 弟幼安 兄子龕 陰子春》][479] | [JSON](sqi_qy6_6bu_AB.json) |
| `ABA` | 杜龕（杜岑子，王僧辯婿） | [《南史・江子一　胡僧祐　徐文盛　陰子春　杜崱　王琳　張彪》][960] | [JSON](sqi_qy6_6bu_ABA.json) |

</details>

<details><summary><code>sy5_s6h_9ex</code> 鄭文公（重耳過國者）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 鄭文公（重耳過國者） | [《史記・鄭世家》][1167] | [JSON](sy5_s6h_9ex.json) |
| `A` | 蘭 | [《史記・鄭世家》][1167] | [JSON](sy5_s6h_9ex_A.json) |

</details>

<details><summary><code>syc_ik6_bq5</code> 顧奉（7 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 顧奉 | [《三國志・張顧諸葛步傳》][1042] | [JSON](syc_ik6_bq5.json) |
| `**A` | 顧雍 | [《三國志・張顧諸葛步傳》][1042] | [JSON](syc_ik6_bq5_%2A%2AA.json) |
| `**AA` | 顧邵 | [《三國志・張顧諸葛步傳》][1040] | [JSON](syc_ik6_bq5_%2A%2AAA.json) |
| `**AAA` | 顧譚 | [《三國志・張顧諸葛步傳》][1041] | [JSON](syc_ik6_bq5_%2A%2AAAA.json) |
| `**AAB` | 顧承 | [《三國志・張顧諸葛步傳》][1041] | [JSON](syc_ik6_bq5_%2A%2AAAB.json) |
| `**AB` | 顧裕〔一名穆〕 | [《三國志・張顧諸葛步傳》][1042] | [JSON](syc_ik6_bq5_%2A%2AAB.json) |
| `**AC` | 顧濟 | [《三國志・張顧諸葛步傳》][1042] | [JSON](syc_ik6_bq5_%2A%2AAC.json) |

</details>

<details><summary><code>szg_rhg_18d</code> 嚴畯（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 嚴畯 | [《三國志・張嚴程闞薛傳》][1059] | [JSON](szg_rhg_18d.json) |
| `A` | 嚴凱 | [《三國志・張嚴程闞薛傳》][1059] | [JSON](szg_rhg_18d_A.json) |
| `B` | 嚴爽 | [《三國志・張嚴程闞薛傳》][1059] | [JSON](szg_rhg_18d_B.json) |

</details>

<details><summary><code>t6q_oe6_hom</code> 伏生（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 伏生 | [《史記・儒林列傳》][1246] | [JSON](t6q_oe6_hom.json) |
| `*A` | 伏生孫（未名） | [《史記・儒林列傳》][1246] | [JSON](t6q_oe6_hom_%2AA.json) |

</details>

<details><summary><code>t6x_0wm_0k5</code> 陸徽（字休猷，益州刺史）（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 陸徽（字休猷，益州刺史） | [《宋書・良吏》][1554] | [JSON](t6x_0wm_0k5.json) |
| `A` | 陸叡（陸徽子，陸杲父） | [《南史・陸澄　陸慧曉　陸杲》][935]、[《宋書・良吏》][1555] | [JSON](t6x_0wm_0k5_A.json) |
| `AA` | 陸杲（字明霞） | [《南史・陸澄　陸慧曉　陸杲》][935] | [JSON](t6x_0wm_0k5_AA.json) |

</details>

<details><summary><code>t7q_vt4_ktj</code> 山（齊獻公）（7 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 山（齊獻公） | [《史記・齊太公世家》][1157] | [JSON](t7q_vt4_ktj.json) |
| `A` | 壽（齊武公） | [《史記・齊太公世家》][1157] | [JSON](t7q_vt4_ktj_A.json) |
| `AA` | 無忌（齊厲公） | [《史記・齊太公世家》][1157] | [JSON](t7q_vt4_ktj_AA.json) |
| `AAA` | 赤（齊文公） | [《史記・齊太公世家》][1157] | [JSON](t7q_vt4_ktj_AAA.json) |
| `AAAA` | 脫（齊成公） | [《史記・齊太公世家》][1157] | [JSON](t7q_vt4_ktj_AAAA.json) |
| `AAAAA` | 購（齊莊公） | [《史記・齊太公世家》][1157] | [JSON](t7q_vt4_ktj_AAAAA.json) |
| `AAAAAA` | 祿甫（齊釐公） | [《史記・齊太公世家》][1157] | [JSON](t7q_vt4_ktj_AAAAAA.json) |

</details>

<details><summary><code>t8a_uoo_qhb</code> 虞丘進（字豫之）（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 虞丘進（字豫之） | [《宋書・孫處 蒯恩 劉鍾 虞丘進》][1444] | [JSON](t8a_uoo_qhb.json) |
| `A` | 虞丘耕（虞丘進子） | [《宋書・孫處 蒯恩 劉鍾 虞丘進》][1442]、[《宋書・孫處 蒯恩 劉鍾 虞丘進》][1443] | [JSON](t8a_uoo_qhb_A.json) |
| `AA` | 虞丘襲祖（虞丘耕子） | [《宋書・孫處 蒯恩 劉鍾 虞丘進》][1442]、[《宋書・孫處 蒯恩 劉鍾 虞丘進》][1446] | [JSON](t8a_uoo_qhb_AA.json) |

</details>

<details><summary><code>tkc_9z3_91l</code> 朱建（酈生陸賈列傳候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 朱建 | [《史記・酈生陸賈列傳》][1222] | [JSON](tkc_9z3_91l.json) |
| `A` | 朱建子未名 | [《史記・酈生陸賈列傳》][1222] | [JSON](tkc_9z3_91l_A.json) |

</details>

<details><summary><code>tpj_u6z_dq1</code> 劉景彥（劉師知父）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 劉景彥（劉師知父） | [《陳書・列傳第十: 趙知禮 蔡景歷 劉師知 謝岐》][45] | [JSON](tpj_u6z_dq1.json) |
| `A` | 劉師知（陳中書舍人） | [《陳書・皇后》][31] | [JSON](tpj_u6z_dq1_A.json) |

</details>

<details><summary><code>tvq_5nw_rqn</code> 徐孝嗣（4 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 徐孝嗣 | [《南齊書・徐孝嗣 沈文季》][637] | [JSON](tvq_5nw_rqn.json) |
| `A` | 徐緄（徐孝嗣子） | [《梁書・皇后》][382]、[《南史・后妃下》][763]、[《南史・劉穆之　徐羨之　傅亮　檀道濟》][771]、[《南史・劉穆之　徐羨之　傅亮　檀道濟》][772] | [JSON](tvq_5nw_rqn_A.json) |
| `AA` | 徐昭佩（梁湘東王妃） | [《梁書・太宗十一王 世祖二子》][478]、[《南史・后妃下》][763] | [JSON](tvq_5nw_rqn_AA.json) |
| `AB` | 徐君蒨（字懷簡，徐緄子） | [《南史・劉穆之　徐羨之　傅亮　檀道濟》][771] | [JSON](tvq_5nw_rqn_AB.json) |

</details>

<details><summary><code>twd_erg_kmz</code> 陶侃（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 陶侃 | [《晉書・溫嶠 郗鑒》][272] | [JSON](twd_erg_kmz.json) |
| `A` | 陶氏〔陶侃第十女、孟嘉妻〕 | — | [JSON](twd_erg_kmz_A.json) |

</details>

<details><summary><code>txj_z8z_5me</code> 肅侯（趙世家候選）（4 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 肅侯 | [《史記・趙世家》][1168] | [JSON](txj_z8z_5me.json) |
| `A` | 趙武靈王 | [《史記・趙世家》][1168] | [JSON](txj_z8z_5me_A.json) |
| `AA` | 公子章 | [《史記・趙世家》][1168] | [JSON](txj_z8z_5me_AA.json) |
| `AB` | 何 | [《史記・趙世家》][1168] | [JSON](txj_z8z_5me_AB.json) |

</details>

<details><summary><code>tyh_fzo_pb6</code> 懷慎（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 懷慎 | [《宋書・王鎮惡 檀韶 向靖 劉懷慎 劉粹》][1361]、[《宋書・劉懷肅 孟懷玉 劉敬宣 檀祗》][1386]、[《宋書・劉懷肅 孟懷玉 劉敬宣 檀祗》][1388] | [JSON](tyh_fzo_pb6.json) |
| `A` | 劉榮祖（劉懷慎庶長子） | [《宋書・王鎮惡 檀韶 向靖 劉懷慎 劉粹》][1361]、[《宋書・朱齡石 毛脩之 傅弘之》][1419] | [JSON](tyh_fzo_pb6_A.json) |

</details>

<details><summary><code>tz9_dhl_ifo</code> 樛樂（南越列傳候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 樛樂 | [《史記・南越列傳》][1238] | [JSON](tz9_dhl_ifo.json) |
| `A` | 廣德 | [《史記・建元以來侯者年表》][1685] | [JSON](tz9_dhl_ifo_A.json) |

</details>

<details><summary><code>u3k_51j_4ul</code> 薛廣（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 薛廣 | [《宋書・薛安都 沈文秀 崔道固》][1546] | [JSON](u3k_51j_4ul.json) |
| `A` | 薛安都 | [《北史・崔光 崔亮》][9]、[《魏書・燕鳳 許謙 張衮 崔玄伯 鄧淵》][1608] | [JSON](u3k_51j_4ul_A.json) |

</details>

<details><summary><code>u3z_kcn_2cf</code> 崔敬友（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 崔敬友 | [《崔混墓誌・節錄》][82] | [JSON](u3z_kcn_2cf.json) |
| `A` | 崔鵾 | [《北史・崔光 崔亮》][8]、[《崔鴻墓誌・節錄》][81]、[《魏書・崔光》][1625] | [JSON](u3z_kcn_2cf_A.json) |
| `B` | 崔鷫 | [《崔鴻墓誌・節錄》][81] | [JSON](u3z_kcn_2cf_B.json) |

</details>

<details><summary><code>u40_zod_c8p</code> 虞𩦎（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 虞𩦎 | [《晉書・王舒 王廙 虞潭 顧眾 張闓》][302]、[《世說新語・品藻》][1299] | [JSON](u40_zod_c8p.json) |
| `A` | 虞谷 | [《晉書・王舒 王廙 虞潭 顧眾 張闓》][302] | [JSON](u40_zod_c8p_A.json) |

</details>

<details><summary><code>u61_ylg_6av</code> 石季龍（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 石季龍 | [《晉書・陳騫 裴秀》][201] | [JSON](u61_ylg_6av.json) |
| `A` | 石世 | [《晉書・孝宗穆帝 哀帝 廢帝海西公》][176] | [JSON](u61_ylg_6av_A.json) |

</details>

<details><summary><code>u87_cc1_7vm</code> 田儋（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 田儋 | [《史記・田儋列傳》][1219] | [JSON](u87_cc1_7vm.json) |
| `A` | 田市 | [《史記・田儋列傳》][1219] | [JSON](u87_cc1_7vm_A.json) |

</details>

<details><summary><code>u9s_w6j_8mc</code> 桓顥（42 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 桓顥 | [《晉書・桓彝》][290] | [JSON](u9s_w6j_8mc.json) |
| `A` | 桓彝 | [《晉書・桓彝》][290] | [JSON](u9s_w6j_8mc_A.json) |
| `AA` | 桓溫 | [《晉書・叛臣一》][343] | [JSON](u9s_w6j_8mc_AA.json) |
| `AAA` | 桓熙 | [《晉書・叛臣一》][343] | [JSON](u9s_w6j_8mc_AAA.json) |
| `AAB` | 桓濟 | [《晉書・叛臣一》][343] | [JSON](u9s_w6j_8mc_AAB.json) |
| `AABA` | 桓亮 | [《晉書・叛臣二》][347] | [JSON](u9s_w6j_8mc_AABA.json) |
| `AAC` | 桓歆 | [《晉書・叛臣二》][347] | [JSON](u9s_w6j_8mc_AAC.json) |
| `AAD` | 桓禕 | [《晉書・叛臣一》][343] | [JSON](u9s_w6j_8mc_AAD.json) |
| `AAE` | 桓偉 | [《晉書・叛臣二》][347] | [JSON](u9s_w6j_8mc_AAE.json) |
| `AAEA` | 桓浚 | [《晉書・叛臣二》][347] | [JSON](u9s_w6j_8mc_AAEA.json) |
| `AAEB` | 桓邈 | [《晉書・叛臣二》][347] | [JSON](u9s_w6j_8mc_AAEB.json) |
| `AAF` | 桓玄 | [《晉書・叛臣二》][347] | [JSON](u9s_w6j_8mc_AAF.json) |
| `AAFA` | 桓升 | [《晉書・叛臣二》][347] | [JSON](u9s_w6j_8mc_AAFA.json) |
| `AAG` | 桓氏（字伯子，桓溫第二女） | [《世說新語・方正》][1277] | [JSON](u9s_w6j_8mc_AAG.json) |
| `AB` | 桓雲 | [《晉書・桓彝》][290] | [JSON](u9s_w6j_8mc_AB.json) |
| `AB*A` | 桓放之 | [《晉書・叛臣二》][347] | [JSON](u9s_w6j_8mc_AB%2AA.json) |
| `ABA` | 桓序 | [《宋書・劉懷肅 孟懷玉 劉敬宣 檀祗》][1387] | [JSON](u9s_w6j_8mc_ABA.json) |
| `AC` | 桓豁 | [《晉書・桓彝》][290] | [JSON](u9s_w6j_8mc_AC.json) |
| `ACA` | 桓石虔 | [《晉書・桓彝》][290] | [JSON](u9s_w6j_8mc_ACA.json) |
| `ACAA` | 桓誕 | [《晉書・桓彝》][290] | [JSON](u9s_w6j_8mc_ACAA.json) |
| `ACAB` | 桓洪 | [《晉書・桓彝》][290] | [JSON](u9s_w6j_8mc_ACAB.json) |
| `ACAC` | 桓振 | [《晉書・桓彝》][290] | [JSON](u9s_w6j_8mc_ACAC.json) |
| `ACB` | 桓石秀 | [《晉書・桓彝》][290] | [JSON](u9s_w6j_8mc_ACB.json) |
| `ACBA` | 桓稚玉 | [《晉書・桓彝》][290] | [JSON](u9s_w6j_8mc_ACBA.json) |
| `ACC` | 桓石民 | [《晉書・桓彝》][290] | [JSON](u9s_w6j_8mc_ACC.json) |
| `ACD` | 桓石生 | [《晉書・桓彝》][290] | [JSON](u9s_w6j_8mc_ACD.json) |
| `ACE` | 桓石綏 | [《晉書・桓彝》][290] | [JSON](u9s_w6j_8mc_ACE.json) |
| `ACF` | 桓石康 | [《晉書・叛臣二》][347] | [JSON](u9s_w6j_8mc_ACF.json) |
| `ACG` | 桓權 | [《晉書・叛臣二》][347] | [JSON](u9s_w6j_8mc_ACG.json) |
| `AD` | 桓秘 | [《晉書・桓彝》][290] | [JSON](u9s_w6j_8mc_AD.json) |
| `ADA` | 桓蔚 | [《晉書・叛臣二》][347] | [JSON](u9s_w6j_8mc_ADA.json) |
| `AE` | 桓沖 | [《晉書・桓彝》][290] | [JSON](u9s_w6j_8mc_AE.json) |
| `AEA` | 桓嗣 | [《晉書・桓彝》][290] | [JSON](u9s_w6j_8mc_AEA.json) |
| `AEAA` | 桓胤 | [《晉書・叛臣二》][347] | [JSON](u9s_w6j_8mc_AEAA.json) |
| `AEB` | 桓謙 | [《晉書・桓彝》][290] | [JSON](u9s_w6j_8mc_AEB.json) |
| `AEC` | 桓修 | [《晉書・桓彝》][290] | [JSON](u9s_w6j_8mc_AEC.json) |
| `AECA` | 桓修長女〔王琨妻〕 | — | [JSON](u9s_w6j_8mc_AECA.json) |
| `AECB` | 桓修小女〔庾敬度妻〕 | — | [JSON](u9s_w6j_8mc_AECB.json) |
| `AED` | 桓崇 | [《晉書・桓彝》][290] | [JSON](u9s_w6j_8mc_AED.json) |
| `AEE` | 桓弘 | [《晉書・桓彝》][290]、[《晉書・叛臣二》][347] | [JSON](u9s_w6j_8mc_AEE.json) |
| `AEF` | 桓羨 | [《晉書・桓彝》][290] | [JSON](u9s_w6j_8mc_AEF.json) |
| `AEG` | 桓怡 | [《晉書・桓彝》][290] | [JSON](u9s_w6j_8mc_AEG.json) |

</details>

<details><summary><code>uay_2h8_ps8</code> 師（陳悼太子）（4 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 師（陳悼太子） | [《史記・陳杞世家》][1161] | [JSON](uay_2h8_ps8.json) |
| `A` | 吳（陳惠公） | [《史記・陳杞世家》][1161] | [JSON](uay_2h8_ps8_A.json) |
| `AA` | 柳（陳懷公） | [《史記・陳杞世家》][1161] | [JSON](uay_2h8_ps8_AA.json) |
| `AAA` | 越（陳湣公） | [《史記・陳杞世家》][1161] | [JSON](uay_2h8_ps8_AAA.json) |

</details>

<details><summary><code>uei_vr9_n3j</code> 竇長君（絳侯周勃世家候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 竇長君 | [《史記・絳侯周勃世家》][1182] | [JSON](uei_vr9_n3j.json) |
| `A` | 彭祖 | [《史記・絳侯周勃世家》][1182] | [JSON](uei_vr9_n3j_A.json) |

</details>

<details><summary><code>ufr_eoj_xit</code> 石奢父（未名）（循吏列傳候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 石奢父（未名） | [《史記・循吏列傳》][1244] | [JSON](ufr_eoj_xit.json) |
| `A` | 石奢 | [《史記・循吏列傳》][1244] | [JSON](ufr_eoj_xit_A.json) |

</details>

<details><summary><code>uij_ufp_1a6</code> 賈弼之（南史作弼）（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 賈弼之（南史作弼） | [《南齊書・文學》][689]、[《南齊書・文學》][690] | [JSON](uij_ufp_1a6.json) |
| `A` | 賈匪之（譜家，賈弼之子） | [《南史・江淹　任昉　王僧孺》][957] | [JSON](uij_ufp_1a6_A.json) |
| `AA` | 賈淵（字希鏡，南史作深） | [《南齊書・文學》][690] | [JSON](uij_ufp_1a6_AA.json) |

</details>

<details><summary><code>uj9_x5q_yir</code> 宋義（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 宋義 | [《史記・項羽本紀》][1149] | [JSON](uj9_x5q_yir.json) |
| `A` | 宋襄 | [《史記・項羽本紀》][1149] | [JSON](uj9_x5q_yir_A.json) |

</details>

<details><summary><code>us5_6hk_3qm</code> 屠者（留侯世家候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 屠者 | [《史記・留侯世家》][1180] | [JSON](us5_6hk_3qm.json) |
| `A` | 秦嶢下軍將 | [《史記・留侯世家》][1180] | [JSON](us5_6hk_3qm_A.json) |

</details>

<details><summary><code>uti_8b5_tcd</code> 蔡款（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 蔡款 | [《三國志・張顧諸葛步傳》][1044] | [JSON](uti_8b5_tcd.json) |
| `A` | 蔡條 | [《三國志・張顧諸葛步傳》][1044] | [JSON](uti_8b5_tcd_A.json) |
| `B` | 蔡機 | [《三國志・張顧諸葛步傳》][1044] | [JSON](uti_8b5_tcd_B.json) |

</details>

<details><summary><code>uud_qa6_4u1</code> 郁（杞平公）（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 郁（杞平公） | [《史記・陳杞世家》][1161] | [JSON](uud_qa6_4u1.json) |
| `A` | 成（杞悼公） | [《史記・陳杞世家》][1161] | [JSON](uud_qa6_4u1_A.json) |
| `AA` | 乞（杞隱公） | [《史記・陳杞世家》][1161] | [JSON](uud_qa6_4u1_AA.json) |

</details>

<details><summary><code>uxk_94s_ndu</code> 丁固（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 丁固 | [《三國志・虞陸張駱陸吾朱傳》][1096] | [JSON](uxk_94s_ndu.json) |
| `A` | 丁彌 | [《三國志・虞陸張駱陸吾朱傳》][1089]、[《三國志・虞陸張駱陸吾朱傳》][1096] | [JSON](uxk_94s_ndu_A.json) |

</details>

<details><summary><code>v0t_lw5_yr1</code> 李敏〔漢河內太守〕（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 李敏〔漢河內太守〕 | [《晉書・鄭袤 李胤 盧欽 華表 石鑒 溫羨》][227] | [JSON](v0t_lw5_yr1.json) |
| `A` | 李信〔李胤父〕 | [《晉書・鄭袤 李胤 盧欽 華表 石鑒 溫羨》][227] | [JSON](v0t_lw5_yr1_A.json) |

</details>

<details><summary><code>v4f_db2_eqv</code> 潘璋〔字文珪〕（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 潘璋〔字文珪〕 | [《三國志・程黃韓蔣周陳董甘淩徐潘丁傳》][1077] | [JSON](v4f_db2_eqv.json) |
| `A` | 潘平 | [《三國志・程黃韓蔣周陳董甘淩徐潘丁傳》][1077] | [JSON](v4f_db2_eqv_A.json) |

</details>

<details><summary><code>v8m_39s_b9x</code> 寇脩之（字延期，寇讚、寇謙之父）（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 寇脩之（字延期，寇讚、寇謙之父） | [《魏書・薛辯 寇贊 酈範 韓秀 堯暄》][1614] | [JSON](v8m_39s_b9x.json) |
| `A` | 寇讚（字奉國） | [《魏書・薛辯 寇贊 酈範 韓秀 堯暄》][1614] | [JSON](v8m_39s_b9x_A.json) |
| `B` | 寇謙之（字輔真，嵩高道士） | [《魏書・薛辯 寇贊 酈範 韓秀 堯暄》][1614] | [JSON](v8m_39s_b9x_B.json) |

</details>

<details><summary><code>v9j_1fp_kma</code> 檀憑（宋書卷九十七所載檀和之父）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 檀憑（宋書卷九十七所載檀和之父） | [《宋書・夷蠻》][1575] | [JSON](v9j_1fp_kma.json) |
| `A` | 檀和之（雲杜縣子） | [《宋書・夷蠻》][1575] | [JSON](v9j_1fp_kma_A.json) |

</details>

<details><summary><code>vcd_ee3_q63</code> 劉鍾（字世之）（5 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 劉鍾（字世之） | [《宋書・孫處 蒯恩 劉鍾 虞丘進》][1435] | [JSON](vcd_ee3_q63.json) |
| `A` | 劉敬義（劉鍾子） | [《宋書・孫處 蒯恩 劉鍾 虞丘進》][1430]、[《宋書・孫處 蒯恩 劉鍾 虞丘進》][1434] | [JSON](vcd_ee3_q63_A.json) |
| `AA` | 劉國重（劉敬義子） | [《南齊書・徐孝嗣 沈文季》][635]、[《宋書・孫處 蒯恩 劉鍾 虞丘進》][1430]、[《宋書・孫處 蒯恩 劉鍾 虞丘進》][1432] | [JSON](vcd_ee3_q63_AA.json) |
| `B` | 劉敬順（劉鍾次子） | [《宋書・孫處 蒯恩 劉鍾 虞丘進》][1430] | [JSON](vcd_ee3_q63_B.json) |
| `BA` | 劉國須（劉敬順子） | [《宋書・孫處 蒯恩 劉鍾 虞丘進》][1430]、[《宋書・孫處 蒯恩 劉鍾 虞丘進》][1431] | [JSON](vcd_ee3_q63_BA.json) |

</details>

<details><summary><code>vcm_d77_tsz</code> 昌〔祖沖之祖〕（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 昌〔祖沖之祖〕 | [《南齊書・文學》][692] | [JSON](vcm_d77_tsz.json) |
| `A` | 朔之〔祖沖之父〕 | [《南齊書・文學》][692] | [JSON](vcm_d77_tsz_A.json) |
| `AA` | 祖沖之 | [《南齊書・文學》][692] | [JSON](vcm_d77_tsz_AA.json) |

</details>

<details><summary><code>vew_yxo_3j1</code> 甘寧（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 甘寧 | [《三國志・程黃韓蔣周陳董甘淩徐潘丁傳》][1072] | [JSON](vew_yxo_3j1.json) |
| `A` | 甘瓌〔甘寧子〕 | [《三國志・程黃韓蔣周陳董甘淩徐潘丁傳》][1072] | [JSON](vew_yxo_3j1_A.json) |

</details>

<details><summary><code>vfh_ufx_cdv</code> 張慶之（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 張慶之 | [《崔鴻墓誌・節錄》][81]、[《崔混墓誌・節錄》][82] | [JSON](vfh_ufx_cdv.json) |
| `A` | 張氏（崔鴻妻） | [《崔混墓誌・節錄》][82] | [JSON](vfh_ufx_cdv_A.json) |

</details>

<details><summary><code>vgg_tso_418</code> 月氏王（被殺）（大宛列傳候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 月氏王（被殺） | [《史記・大宛列傳》][1248] | [JSON](vgg_tso_418.json) |
| `A` | 月氏太子（繼王） | [《史記・大宛列傳》][1248] | [JSON](vgg_tso_418_A.json) |

</details>

<details><summary><code>vhf_729_g6z</code> 王誕〔張邵早年府主〕（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 王誕〔張邵早年府主〕 | [《宋書・庾悅 王誕 謝景仁 袁湛 褚叔度》][1482] | [JSON](vhf_729_g6z.json) |
| `A` | 王詡（王誕子） | [《南史・王誕　王華　王惠　王彧》][843]、[《南史・王誕　王華　王惠　王彧》][842]、[《宋書・庾悅 王誕 謝景仁 袁湛 褚叔度》][1482] | [JSON](vhf_729_g6z_A.json) |

</details>

<details><summary><code>vhw_07a_wzm</code> 孔惔（淳之祖）（6 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 孔惔（淳之祖） | [《宋書・隱逸》][1573] | [JSON](vhw_07a_wzm.json) |
| `A` | 孔粲（淳之父） | [《宋書・隱逸》][1573] | [JSON](vhw_07a_wzm_A.json) |
| `AA` | 孔淳之 | [《宋書・隱逸》][1573] | [JSON](vhw_07a_wzm_AA.json) |
| `AAA` | 孔尚 | [《宋書・隱逸》][1573] | [JSON](vhw_07a_wzm_AAA.json) |
| `AB` | 孔默之 | [《宋書・隱逸》][1573] | [JSON](vhw_07a_wzm_AB.json) |
| `ABA` | 孔熙先 | [《宋書・胡藩 劉康祖 垣護之 張興世》][1448]、[《宋書・胡藩 劉康祖 垣護之 張興世》][1455]、[《宋書・隱逸》][1573] | [JSON](vhw_07a_wzm_ABA.json) |

</details>

<details><summary><code>vl3_bta_0h1</code> 全尚（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 全尚 | [《三國志・諸葛滕二孫濮陽傳》][1132] | [JSON](vl3_bta_0h1.json) |
| `A` | 全氏〔孫亮皇后、全尚女〕 | [《三國志・三嗣主傳》][1005]、[《三國志・妃嬪傳》][1020] | [JSON](vl3_bta_0h1_A.json) |
| `B` | 全紀（全尚子，黃門侍郎） | [《三國志・諸葛滕二孫濮陽傳》][1132] | [JSON](vl3_bta_0h1_B.json) |

</details>

<details><summary><code>vna_am7_jn5</code> 韋賢（張丞相列傳候選）（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 韋賢 | [《史記・張丞相列傳》][1221] | [JSON](vna_am7_jn5.json) |
| `A` | 韋玄成 | [《史記・張丞相列傳》][1221] | [JSON](vna_am7_jn5_A.json) |
| `B` | 韋賢長子未名 | [《史記・張丞相列傳》][1221] | [JSON](vna_am7_jn5_B.json) |

</details>

<details><summary><code>vpy_180_2oi</code> 昧〔裴松之祖〕（7 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 昧〔裴松之祖〕 | [《南史・范泰　荀伯子　徐廣　鄭鮮之　裴松之　何承天》][908]、[《宋書・鄭鮮之 裴松之 何承天》][1506] | [JSON](vpy_180_2oi.json) |
| `A` | 珪〔裴松之父〕 | [《南史・范泰　荀伯子　徐廣　鄭鮮之　裴松之　何承天》][908]、[《宋書・鄭鮮之 裴松之 何承天》][1506] | [JSON](vpy_180_2oi_A.json) |
| `AA` | 裴松之 | [《南史・范泰　荀伯子　徐廣　鄭鮮之　裴松之　何承天》][908]、[《宋書・鄭鮮之 裴松之 何承天》][1506] | [JSON](vpy_180_2oi_AA.json) |
| `AAA` | 駰〔裴松之子〕 | [《南史・范泰　荀伯子　徐廣　鄭鮮之　裴松之　何承天》][908] | [JSON](vpy_180_2oi_AAA.json) |
| `AAAA` | 昭明〔裴子野父〕 | [《南史・范泰　荀伯子　徐廣　鄭鮮之　裴松之　何承天》][908] | [JSON](vpy_180_2oi_AAAA.json) |
| `AAAAA` | 裴子野 | [《南史・范泰　荀伯子　徐廣　鄭鮮之　裴松之　何承天》][908] | [JSON](vpy_180_2oi_AAAAA.json) |
| `AAAAAA` | 謇〔子野子；南史作騫〕 | [《梁書・裴子野 顧協 徐摛 鮑泉》][452]、[《南史・范泰　荀伯子　徐廣　鄭鮮之　裴松之　何承天》][908] | [JSON](vpy_180_2oi_AAAAAA.json) |

</details>

<details><summary><code>vs4_n7e_1qh</code> 武（曹繆公）（8 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 武（曹繆公） | [《史記・管蔡世家》][1160] | [JSON](vs4_n7e_1qh.json) |
| `A` | 終生（曹桓公） | [《史記・管蔡世家》][1160] | [JSON](vs4_n7e_1qh_A.json) |
| `AA` | 夕姑（曹莊公） | [《史記・管蔡世家》][1160] | [JSON](vs4_n7e_1qh_AA.json) |
| `AAA` | 夷（曹釐公） | [《史記・管蔡世家》][1160] | [JSON](vs4_n7e_1qh_AAA.json) |
| `AAAA` | 班（曹昭公） | [《史記・管蔡世家》][1160] | [JSON](vs4_n7e_1qh_AAAA.json) |
| `AAAAA` | 襄（曹共公） | [《史記・管蔡世家》][1160] | [JSON](vs4_n7e_1qh_AAAAA.json) |
| `AAAAAA` | 壽（曹文公） | [《史記・管蔡世家》][1160] | [JSON](vs4_n7e_1qh_AAAAAA.json) |
| `AAAAAAA` | 彊（曹宣公） | [《史記・管蔡世家》][1160] | [JSON](vs4_n7e_1qh_AAAAAAA.json) |

</details>

<details><summary><code>vs9_1es_k35</code> 田氏（鄭阿春前夫）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 田氏（鄭阿春前夫） | [《晉書・后妃下》][199] | [JSON](vs9_1es_k35.json) |
| `A` | 鄭阿春前婚所生子（未名） | [《晉書・后妃下》][199] | [JSON](vs9_1es_k35_A.json) |

</details>

<details><summary><code>vtp_lo9_0af</code> 裴邃〔楊侃傳〕（4 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 裴邃〔楊侃傳〕 | [《梁書・裴邃 兄子之高 之平 之橫 夏侯亶 弟夔 魚弘附 韋放》][429] | [JSON](vtp_lo9_0af.json) |
| `A` | 裴之禮（裴邃子，字子義） | [《梁書・裴邃 兄子之高 之平 之橫 夏侯亶 弟夔 魚弘附 韋放》][432] | [JSON](vtp_lo9_0af_A.json) |
| `AA` | 裴政（裴之禮子，字德表） | [《隋書・列傳第31 李諤 鮑宏 裴政 柳莊 源師 郎茂 高構 張虔威 榮毗 陸知命 房彥謙》][1585] | [JSON](vtp_lo9_0af_AA.json) |
| `AAA` | 裴南金（裴政子，隋膳部郎） | [《隋書・列傳第31 李諤 鮑宏 裴政 柳莊 源師 郎茂 高構 張虔威 榮毗 陸知命 房彥謙》][1585] | [JSON](vtp_lo9_0af_AAA.json) |

</details>

<details><summary><code>vtu_yuj_kdz</code> 齊王建（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 齊王建 | [《史記・秦始皇本紀》][1148]、[《史記・田儋列傳》][1219] | [JSON](vtu_yuj_kdz.json) |
| `*A` | 田安 | [《史記・項羽本紀》][1149]、[《史記・田儋列傳》][1219] | [JSON](vtu_yuj_kdz_%2AA.json) |

</details>

<details><summary><code>vty_3n0_0ed</code> 病疽卒父（孫吳列傳候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 病疽卒父 | [《史記・孫子吳起列傳》][1190] | [JSON](vty_3n0_0ed.json) |
| `A` | 病疽卒 | [《史記・孫子吳起列傳》][1190] | [JSON](vty_3n0_0ed_A.json) |

</details>

<details><summary><code>vwy_7cv_69j</code> 桓子（趙世家候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 桓子 | [《史記・趙世家》][1168] | [JSON](vwy_7cv_69j.json) |
| `A` | 桓子之子（趙世家未名者） | [《史記・趙世家》][1168] | [JSON](vwy_7cv_69j_A.json) |

</details>

<details><summary><code>vzp_xqn_w3p</code> 張布（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 張布 | [《三國志・三嗣主傳》][1006] | [JSON](vzp_xqn_w3p.json) |
| `A` | 張氏〔張布女、孫皓美人〕 | [《三國志・妃嬪傳》][1016] | [JSON](vzp_xqn_w3p_A.json) |
| `B` | 張氏〔張布長女、馮純前妻〕 | [《三國志・妃嬪傳》][1016] | [JSON](vzp_xqn_w3p_B.json) |

</details>

<details><summary><code>w3a_mm0_hw1</code> 劉昶（平原劉懷珍祖）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 劉昶（平原劉懷珍祖） | [《南齊書・劉懷珍 李安民 王玄載》][535] | [JSON](w3a_mm0_hw1.json) |
| `*A` | 劉懷珍（字道玉） | [《南齊書・劉懷珍 李安民 王玄載》][535]、[《南齊書・劉懷珍 李安民 王玄載》][538]、[《南史・庾杲之　王諶　孔珪　劉懷珍》][938] | [JSON](w3a_mm0_hw1_%2AA.json) |

</details>

<details><summary><code>w44_37v_bcb</code> 和（宋穆公）（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 和（宋穆公） | [《史記・宋微子世家》][1163] | [JSON](w44_37v_bcb.json) |
| `A` | 馮（宋莊公） | [《史記・宋微子世家》][1163] | [JSON](w44_37v_bcb_A.json) |
| `AA` | 捷（宋湣公） | [《史記・宋微子世家》][1163] | [JSON](w44_37v_bcb_AA.json) |

</details>

<details><summary><code>w4m_9tw_147</code> 齊明帝鸞（9 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 齊明帝鸞 | [《南齊書・裴叔業 崔慧景 張欣泰》][686] | [JSON](w4m_9tw_147.json) |
| `A` | 蕭寶卷 | [《南齊書・裴叔業 崔慧景 張欣泰》][686] | [JSON](w4m_9tw_147_A.json) |
| `AA` | 蕭誦（齊東昏侯皇太子） | [《建康實錄・卷十五》][131]、[《建康實錄・卷十五》][132]、[《南齊書・皇后》][510]、[《南齊書・皇后》][509]、[《南史・廢帝鬱林王　廢帝海陵恭王　高宗明皇帝　廢帝東昏侯　和帝》][716]、[《南史・后妃上》][721]、[《南史・后妃上》][722]、[《資治通鑑・齊紀十》][1667] | [JSON](w4m_9tw_147_AA.json) |
| `B` | 蕭寶玄 | [《南齊書・裴叔業 崔慧景 張欣泰》][686] | [JSON](w4m_9tw_147_B.json) |
| `C` | 蕭寶義 | [《南齊書・文二王 明七王》][681] | [JSON](w4m_9tw_147_C.json) |
| `D` | 蕭寶夤（字智亮） | [《南齊書・文二王 明七王》][681] | [JSON](w4m_9tw_147_D.json) |
| `E` | 蕭寶源（字智淵） | [《南齊書・文二王 明七王》][681] | [JSON](w4m_9tw_147_E.json) |
| `F` | 齊和帝寶融（字智昭） | [《南齊書・裴叔業 崔慧景 張欣泰》][686] | [JSON](w4m_9tw_147_F.json) |
| `G` | 山陰公主（齊明帝長女） | [《南史・后妃上》][721]、[《南史・后妃上》][722] | [JSON](w4m_9tw_147_G.json) |

</details>

<details><summary><code>w8j_vnd_rs4</code> 傅寬（4 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 傅寬 | [《漢書・樊酈滕灌傅靳周傳》][104] | [JSON](w8j_vnd_rs4.json) |
| `A` | 傅精 | [《史記・傅靳蒯成列傳》][1223]、[《史記・高祖功臣侯者年表》][1683] | [JSON](w8j_vnd_rs4_A.json) |
| `AA` | 傅則 | [《史記・傅靳蒯成列傳》][1223]、[《史記・高祖功臣侯者年表》][1683] | [JSON](w8j_vnd_rs4_AA.json) |
| `AAA` | 傅偃 | [《史記・高祖功臣侯者年表》][1683] | [JSON](w8j_vnd_rs4_AAA.json) |

</details>

<details><summary><code>wa7_8nj_l6g</code> 孫暠（4 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 孫暠 | [《三國志・虞陸張駱陸吾朱傳》][1096] | [JSON](wa7_8nj_l6g.json) |
| `A` | 孫綽〔孫暠子、孫綝父〕 | [《三國志・宗室傳》][1032] | [JSON](wa7_8nj_l6g_A.json) |
| `B` | 孫超 | [《三國志・宗室傳》][1032] | [JSON](wa7_8nj_l6g_B.json) |
| `C` | 孫恭 | [《三國志・宗室傳》][1032]、[《三國志・諸葛滕二孫濮陽傳》][1133] | [JSON](wa7_8nj_l6g_C.json) |

</details>

<details><summary><code>war_qdw_fs5</code> 陸倕（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 陸倕 | [《梁書・陸倕 到洽 明山賓 殷鈞 陸襄》][420] | [JSON](war_qdw_fs5.json) |
| `A` | 陸纘（陸倕第四子） | [《梁書・陸倕 到洽 明山賓 殷鈞 陸襄》][420]、[《南史・陸澄　陸慧曉　陸杲》][934] | [JSON](war_qdw_fs5_A.json) |
| `B` | 陸緬（南史陸倕傳「次緬」） | [《南史・陸澄　陸慧曉　陸杲》][934] | [JSON](war_qdw_fs5_B.json) |

</details>

<details><summary><code>wc5_hn7_a5w</code> 羊繇（車騎掾）（5 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 羊繇（車騎掾） | [《世說新語・方正》][1276] | [JSON](wc5_hn7_a5w.json) |
| `A` | 羊忱（字長和） | [《世說新語・方正》][1276] | [JSON](wc5_hn7_a5w_A.json) |
| `AA` | 羊權（黃門郎） | [《南史・羊欣　羊玄保　沈演之　江夷　江秉之》][912] | [JSON](wc5_hn7_a5w_AA.json) |
| `AAA` | 羊不疑（桂陽太守） | [《南史・羊欣　羊玄保　沈演之　江夷　江秉之》][912] | [JSON](wc5_hn7_a5w_AAA.json) |
| `AAAA` | 羊徽（字敬猷） | [《南史・羊欣　羊玄保　沈演之　江夷　江秉之》][912] | [JSON](wc5_hn7_a5w_AAAA.json) |

</details>

<details><summary><code>wch_0gk_whm</code> 郗燁（南史作曄，郗徽父）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 郗燁（南史作曄，郗徽父） | [《梁書・皇后》][381] | [JSON](wch_0gk_whm.json) |
| `A` | 郗泛（郗燁子） | [《梁書・皇后》][381] | [JSON](wch_0gk_whm_A.json) |

</details>

<details><summary><code>wgt_wdg_vkv</code> 滕胤（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 滕胤 | [《三國志・諸葛滕二孫濮陽傳》][1132] | [JSON](wgt_wdg_vkv.json) |
| `A` | 滕氏〔滕胤女、吳纂妻〕 | [《三國志・妃嬪傳》][1022] | [JSON](wgt_wdg_vkv_A.json) |

</details>

<details><summary><code>wip_vh5_2zm</code> 朱綽〔襄陽戰時〕（5 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 朱綽〔襄陽戰時〕 | [《宋書・朱齡石 毛脩之 傅弘之》][1417]、[《宋書・朱齡石 毛脩之 傅弘之》][1420] | [JSON](wip_vh5_2zm.json) |
| `A` | 朱齡石 | [《宋書・朱齡石 毛脩之 傅弘之》][1422] | [JSON](wip_vh5_2zm_A.json) |
| `AA` | 朱景符 | [《宋書・朱齡石 毛脩之 傅弘之》][1417]、[《宋書・朱齡石 毛脩之 傅弘之》][1418]、[《宋書・朱齡石 毛脩之 傅弘之》][1421] | [JSON](wip_vh5_2zm_AA.json) |
| `AAA` | 朱祖宣 | [《宋書・朱齡石 毛脩之 傅弘之》][1417]、[《宋書・朱齡石 毛脩之 傅弘之》][1418] | [JSON](wip_vh5_2zm_AAA.json) |
| `AAB` | 朱隆 | [《宋書・朱齡石 毛脩之 傅弘之》][1417]、[《宋書・朱齡石 毛脩之 傅弘之》][1418]、[《宋書・朱齡石 毛脩之 傅弘之》][1423] | [JSON](wip_vh5_2zm_AAB.json) |

</details>

<details><summary><code>wjt_htu_081</code> 頭曼（匈奴列傳）（13 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 頭曼（匈奴列傳） | [《史記・匈奴列傳》][1235] | [JSON](wjt_htu_081.json) |
| `A` | 冒頓（匈奴列傳第6段） | [《史記・匈奴列傳》][1235] | [JSON](wjt_htu_081_A.json) |
| `AA` | 稽粥（匈奴列傳第18至20段） | [《史記・匈奴列傳》][1235] | [JSON](wjt_htu_081_AA.json) |
| `AAA` | 軍臣（匈奴列傳第27段） | [《史記・匈奴列傳》][1235] | [JSON](wjt_htu_081_AAA.json) |
| `AAAA` | 於單（匈奴列傳第31至32段） | [《史記・匈奴列傳》][1235] | [JSON](wjt_htu_081_AAAA.json) |
| `AAB` | 伊稚斜（匈奴列傳第31至32段） | [《史記・衛將軍驃騎列傳》][1236] | [JSON](wjt_htu_081_AAB.json) |
| `AABA` | 烏維（匈奴列傳第42至43段） | [《史記・匈奴列傳》][1235] | [JSON](wjt_htu_081_AABA.json) |
| `AABAA` | 烏師廬（匈奴列傳第49段） | [《史記・匈奴列傳》][1235] | [JSON](wjt_htu_081_AABAA.json) |
| `AABAAA` | 兒單于之子（未名） | [《史記・匈奴列傳》][1235] | [JSON](wjt_htu_081_AABAAA.json) |
| `AABB` | 呴犁湖（匈奴列傳第53段） | [《史記・匈奴列傳》][1235] | [JSON](wjt_htu_081_AABB.json) |
| `AABC` | 且鞮侯（匈奴列傳第56段） | [《史記・匈奴列傳》][1235] | [JSON](wjt_htu_081_AABC.json) |
| `AABCA` | 且鞮侯之女（未名，妻李陵者） | [《史記・李將軍列傳》][1234]、[《史記・匈奴列傳》][1235] | [JSON](wjt_htu_081_AABCA.json) |
| `B` | 少子（匈奴列傳第6段） | [《史記・匈奴列傳》][1235] | [JSON](wjt_htu_081_B.json) |

</details>

<details><summary><code>wow_07g_swu</code> 毛修之（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 毛修之 | [《宋書・朱齡石 毛脩之 傅弘之》][1414] | [JSON](wow_07g_swu.json) |
| `A` | 毛元矯（毛脩之子） | [《宋書・朱齡石 毛脩之 傅弘之》][1413]、[《宋書・朱齡石 毛脩之 傅弘之》][1414]、[《宋書・朱齡石 毛脩之 傅弘之》][1415] | [JSON](wow_07g_swu_A.json) |
| `B` | 毛法仁（毛脩之子） | [《魏書・嚴棱 毛修之 唐和 劉休賓 房法夀》][1615] | [JSON](wow_07g_swu_B.json) |

</details>

<details><summary><code>wtu_qvi_0rz</code> 李矩（李充父）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 李矩（李充父） | [《晉書・文苑》][323] | [JSON](wtu_qvi_0rz.json) |
| `A` | 李充 | [《晉書・文苑》][323] | [JSON](wtu_qvi_0rz_A.json) |

</details>

<details><summary><code>wuz_dky_0ki</code> 賀齊（4 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 賀齊 | [《三國志・賀全呂周鍾離傳》][1110] | [JSON](wuz_dky_0ki.json) |
| `A` | 賀達 | [《三國志・賀全呂周鍾離傳》][1110] | [JSON](wuz_dky_0ki_A.json) |
| `AA` | 賀質〔賀達子、虎牙將軍〕 | [《三國志・賀全呂周鍾離傳》][1110] | [JSON](wuz_dky_0ki_AA.json) |
| `B` | 賀景 | [《三國志・賀全呂周鍾離傳》][1110] | [JSON](wuz_dky_0ki_B.json) |

</details>

<details><summary><code>wuz_yxe_b9k</code> 齊景公（4 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 齊景公 | [《史記・齊太公世家》][1157] | [JSON](wuz_yxe_b9k.json) |
| `A` | 齊悼公 | [《史記・齊太公世家》][1157] | [JSON](wuz_yxe_b9k_A.json) |
| `AA` | 齊簡公 | [《史記・齊太公世家》][1157] | [JSON](wuz_yxe_b9k_AA.json) |
| `B` | 孺子（齊） | [《史記・齊太公世家》][1157] | [JSON](wuz_yxe_b9k_B.json) |

</details>

<details><summary><code>x18_cng_88g</code> 鄭默〔郭奕傳中庶子〕（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 鄭默〔郭奕傳中庶子〕 | [《晉書・鄭袤 李胤 盧欽 華表 石鑒 溫羨》][237] | [JSON](x18_cng_88g.json) |
| `A` | 鄭球〔字子瑜〕 | [《晉書・鄭袤 李胤 盧欽 華表 石鑒 溫羨》][238] | [JSON](x18_cng_88g_A.json) |
| `B` | 鄭豫〔鄭默子〕 | [《晉書・鄭袤 李胤 盧欽 華表 石鑒 溫羨》][237]、[《晉書・鄭袤 李胤 盧欽 華表 石鑒 溫羨》][238]、[《三國志・任蘇杜鄭倉傳》][982] | [JSON](x18_cng_88g_B.json) |

</details>

<details><summary><code>x3q_cqm_dup</code> 竟陵王子良（4 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 竟陵王子良 | [《南齊書・武十七王》][593] | [JSON](x3q_cqm_dup.json) |
| `A` | 蕭昭胄 | [《南齊書・武十七王》][586] | [JSON](x3q_cqm_dup_A.json) |
| `AA` | 蕭周（昭冑子，監利侯；南史作同） | [《南齊書・武十七王》][586]、[《南史・齊武帝諸子　文惠諸子　明帝諸子》][923] | [JSON](x3q_cqm_dup_AA.json) |
| `B` | 蕭昭穎（永新侯，昭冑弟） | [《南齊書・武十七王》][586] | [JSON](x3q_cqm_dup_B.json) |

</details>

<details><summary><code>x50_1p7_qkk</code> 魯莊公（10 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 魯莊公 | [《史記・魯周公世家》][1158] | [JSON](x50_1p7_qkk.json) |
| `A` | 魯湣公 | [《史記・魯周公世家》][1158] | [JSON](x50_1p7_qkk_A.json) |
| `B` | 魯釐公 | [《史記・魯周公世家》][1158] | [JSON](x50_1p7_qkk_B.json) |
| `BA` | 興（魯文公） | [《史記・魯周公世家》][1158] | [JSON](x50_1p7_qkk_BA.json) |
| `BAA` | 惡（文公子） | [《史記・魯周公世家》][1158] | [JSON](x50_1p7_qkk_BAA.json) |
| `BAB` | 視（文公子） | [《史記・魯周公世家》][1158] | [JSON](x50_1p7_qkk_BAB.json) |
| `BAC` | 俀（魯宣公） | [《史記・魯周公世家》][1158] | [JSON](x50_1p7_qkk_BAC.json) |
| `BACA` | 黑肱（魯成公） | [《史記・魯周公世家》][1158] | [JSON](x50_1p7_qkk_BACA.json) |
| `BACAA` | 午（魯襄公） | [《史記・魯周公世家》][1158] | [JSON](x50_1p7_qkk_BACAA.json) |
| `C` | 斑（莊公子） | [《史記・魯周公世家》][1158] | [JSON](x50_1p7_qkk_C.json) |

</details>

<details><summary><code>x90_vgz_2uf</code> 王翹之（晉光祿大夫）（5 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 王翹之（晉光祿大夫） | [《南史・王裕之　王鎮之　王韶之　王悅之　王准之》][879]、[《宋書・隱逸》][1569] | [JSON](x90_vgz_2uf.json) |
| `A` | 王望之（王素曾祖） | [《南史・王裕之　王鎮之　王韶之　王悅之　王准之》][879] | [JSON](x90_vgz_2uf_A.json) |
| `AA` | 王泰之（王素祖） | [《南史・王裕之　王鎮之　王韶之　王悅之　王准之》][879] | [JSON](x90_vgz_2uf_AA.json) |
| `AAA` | 王元弘（平固令） | [《南史・王裕之　王鎮之　王韶之　王悅之　王准之》][879] | [JSON](x90_vgz_2uf_AAA.json) |
| `AAAA` | 王素（字休業） | [《宋書・隱逸》][1569] | [JSON](x90_vgz_2uf_AAAA.json) |

</details>

<details><summary><code>xaa_ewn_4ro</code> 臧荼（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 臧荼 | [《史記・樊酈滕灌列傳》][1220] | [JSON](xaa_ewn_4ro.json) |
| `A` | 衍（臧荼子） | [《史記・韓信盧綰列傳》][1218] | [JSON](xaa_ewn_4ro_A.json) |

</details>

<details><summary><code>xd8_uww_5ok</code> 蕭何（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 蕭何 | [《史記・蕭相國世家》][1178] | [JSON](xd8_uww_5ok.json) |
| `*A` | 系（蕭何孫） | [《史記・孝景本紀》][1153] | [JSON](xd8_uww_5ok_%2AA.json) |

</details>

<details><summary><code>xgd_r31_cmr</code> 崔杼（4 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 崔杼 | [《史記・齊太公世家》][1157] | [JSON](xgd_r31_cmr.json) |
| `A` | 成（崔杼子） | [《史記・齊太公世家》][1157] | [JSON](xgd_r31_cmr_A.json) |
| `B` | 彊（崔杼子） | [《史記・齊太公世家》][1157] | [JSON](xgd_r31_cmr_B.json) |
| `C` | 明（崔杼子） | [《史記・齊太公世家》][1157] | [JSON](xgd_r31_cmr_C.json) |

</details>

<details><summary><code>xgx_g4a_c28</code> 趙兼（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 趙兼 | [《史記・孝文本紀》][1152]、[《史記・淮南衡山列傳》][1243]、[《史記・酷吏列傳》][1247]、[《史記・惠景間侯者年表》][1684] | [JSON](xgx_g4a_c28.json) |
| `A` | 周陽由 | [《史記・酷吏列傳》][1247] | [JSON](xgx_g4a_c28_A.json) |

</details>

<details><summary><code>xke_dj3_6ba</code> 褚䂮（15 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 褚䂮 | [《晉書・王沈 荀顗 荀勖 馮紞》][208]、[《晉書・外戚》][324] | [JSON](xke_dj3_6ba.json) |
| `A` | 褚洽 | [《晉書・外戚》][324] | [JSON](xke_dj3_6ba_A.json) |
| `AA` | 褚裒 | [《晉書・外戚》][324] | [JSON](xke_dj3_6ba_AA.json) |
| `AAA` | 褚歆 | [《晉書・外戚》][324] | [JSON](xke_dj3_6ba_AAA.json) |
| `AAAA` | 褚爽 | [《晉書・外戚》][325] | [JSON](xke_dj3_6ba_AAAA.json) |
| `AAAAA` | 褚秀之 | [《晉書・外戚》][325]、[《南齊書・褚淵 淵弟澄 徐嗣 王儉》][530]、[《南齊書・王琨 張岱 褚炫 何戢 王延之 阮韜》][548]、[《南齊書・江斆 何昌㝢 謝𤅢 王思遠》][628]、[《南史・褚裕之》][899]、[《宋書・庾悅 王誕 謝景仁 袁湛 褚叔度》][1480]、[《宋書・庾悅 王誕 謝景仁 袁湛 褚叔度》][1481] | [JSON](xke_dj3_6ba_AAAAA.json) |
| `AAAAAA` | 褚法顯（鄱陽太守） | [《南齊書・王琨 張岱 褚炫 何戢 王延之 阮韜》][548]、[《南史・褚裕之》][900] | [JSON](xke_dj3_6ba_AAAAAA.json) |
| `AAAAAAA` | 褚炤（字彥宣） | [《南齊書・王琨 張岱 褚炫 何戢 王延之 阮韜》][549]、[《南史・褚裕之》][900] | [JSON](xke_dj3_6ba_AAAAAAA.json) |
| `AAAAB` | 褚炎之 | [《晉書・外戚》][325] | [JSON](xke_dj3_6ba_AAAAB.json) |
| `AAAAC` | 褚喻之 | [《南史・褚裕之》][898]、[《宋書・庾悅 王誕 謝景仁 袁湛 褚叔度》][1479] | [JSON](xke_dj3_6ba_AAAAC.json) |
| `AAAACA` | 褚寂之（褚叔度第二子） | [《南史・褚裕之》][898]、[《宋書・庾悅 王誕 謝景仁 袁湛 褚叔度》][1479] | [JSON](xke_dj3_6ba_AAAACA.json) |
| `AAAACAA` | 褚曖（褚寂之子） | [《南史・王誕　王華　王惠　王彧》][865]、[《南史・褚裕之》][898]、[《宋書・庾悅 王誕 謝景仁 袁湛 褚叔度》][1479] | [JSON](xke_dj3_6ba_AAAACAA.json) |
| `AAAAD` | 褚靈媛 | [《晉書・后妃下》][193] | [JSON](xke_dj3_6ba_AAAAD.json) |
| `AAAAE` | 褚淡之（字仲源） | [《宋書・庾悅 王誕 謝景仁 袁湛 褚叔度》][1481] | [JSON](xke_dj3_6ba_AAAAE.json) |
| `AAB` | 褚蒜子 | [《晉書・后妃下》][194] | [JSON](xke_dj3_6ba_AAB.json) |

</details>

<details><summary><code>xms_rnf_fpk</code> 何洪（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 何洪 | [《三國志・妃嬪傳》][1016] | [JSON](xms_rnf_fpk.json) |
| `A` | 何邈 | [《三國志・妃嬪傳》][1016] | [JSON](xms_rnf_fpk_A.json) |

</details>

<details><summary><code>xny_prn_zyi</code> 酈商（6 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 酈商 | [《史記・樊酈滕灌列傳》][1220] | [JSON](xny_prn_zyi.json) |
| `A` | 酈寄 | [《史記・樊酈滕灌列傳》][1220] | [JSON](xny_prn_zyi_A.json) |
| `B` | 酈堅 | [《史記・樊酈滕灌列傳》][1220] | [JSON](xny_prn_zyi_B.json) |
| `BA` | 酈遂成 | [《史記・樊酈滕灌列傳》][1220] | [JSON](xny_prn_zyi_BA.json) |
| `BAA` | 酈世宗 | [《史記・樊酈滕灌列傳》][1220] | [JSON](xny_prn_zyi_BAA.json) |
| `BAAA` | 酈終根 | [《史記・樊酈滕灌列傳》][1220] | [JSON](xny_prn_zyi_BAAA.json) |

</details>

<details><summary><code>xrt_zof_cbt</code> 和（衛武公）（4 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 和（衛武公） | [《史記・衛康叔世家》][1162] | [JSON](xrt_zof_cbt.json) |
| `A` | 揚（衛莊公） | [《史記・衛康叔世家》][1162] | [JSON](xrt_zof_cbt_A.json) |
| `AA` | 州吁（衛君） | [《史記・衛康叔世家》][1162] | [JSON](xrt_zof_cbt_AA.json) |
| `AB` | 完（衛桓公） | [《史記・衛康叔世家》][1162] | [JSON](xrt_zof_cbt_AB.json) |

</details>

<details><summary><code>xtk_38i_cg1</code> 沈穆夫（沈田子、沈林子父）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 沈穆夫（沈田子、沈林子父） | [《南史・沈約　范雲》][951] | [JSON](xtk_38i_cg1.json) |
| `A` | 沈田子（字敬光） | [《南史・沈約　范雲》][951]、[《宋書・趙倫之 王懿 張邵》][1377]、[《宋書・朱齡石 毛脩之 傅弘之》][1411]、[《宋書・孫處 蒯恩 劉鍾 虞丘進》][1438] | [JSON](xtk_38i_cg1_A.json) |

</details>

<details><summary><code>xxh_xtr_3f9</code> 袁豹（5 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 袁豹 | [《宋書・庾悅 王誕 謝景仁 袁湛 褚叔度》][1486] | [JSON](xxh_xtr_3f9.json) |
| `A` | 袁洵 | [《梁書・袁昂 子君正》][453]、[《南齊書・袁彖 孔稚珪 劉繪》][663]、[《南齊書・袁彖 孔稚珪 劉繪》][664]、[《宋書・庾悅 王誕 謝景仁 袁湛 褚叔度》][1486] | [JSON](xxh_xtr_3f9_A.json) |
| `AA` | 袁顗 | [《南齊書・袁彖 孔稚珪 劉繪》][664]、[《宋書・胡藩 劉康祖 垣護之 張興世》][1475] | [JSON](xxh_xtr_3f9_AA.json) |
| `AB` | 袁覬 | [《南齊書・袁彖 孔稚珪 劉繪》][664] | [JSON](xxh_xtr_3f9_AB.json) |
| `ABA` | 袁氏（竟陵王子良妃） | [《南齊書・皇后》][521]、[《南齊書・皇后》][520]、[《南齊書・武十七王》][585]、[《南齊書・武十七王》][593]、[《南史・后妃上》][734]、[《南史・后妃上》][735] | [JSON](xxh_xtr_3f9_ABA.json) |

</details>

<details><summary><code>y0c_hok_598</code> 李同父未名（平原君虞卿列傳候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 李同父未名 | [《史記・平原君虞卿列傳》][1201] | [JSON](y0c_hok_598.json) |
| `A` | 李同 | [《史記・平原君虞卿列傳》][1201] | [JSON](y0c_hok_598_A.json) |

</details>

<details><summary><code>y3i_rsz_brn</code> 韓厥（14 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 韓厥 | [《史記・韓世家》][1170] | [JSON](y3i_rsz_brn.json) |
| `A` | 韓宣子 | [《史記・韓世家》][1170] | [JSON](y3i_rsz_brn_A.json) |
| `AA` | 韓貞子 | [《史記・韓世家》][1170] | [JSON](y3i_rsz_brn_AA.json) |
| `AAA` | 韓簡子 | [《史記・韓世家》][1170] | [JSON](y3i_rsz_brn_AAA.json) |
| `AAAA` | 韓莊子 | [《史記・韓世家》][1170] | [JSON](y3i_rsz_brn_AAAA.json) |
| `AAAAA` | 韓康子 | [《史記・韓世家》][1170] | [JSON](y3i_rsz_brn_AAAAA.json) |
| `AAAAAA` | 武子 | [《史記・韓世家》][1170] | [JSON](y3i_rsz_brn_AAAAAA.json) |
| `AAAAAAA` | 虔 | [《史記・韓世家》][1170] | [JSON](y3i_rsz_brn_AAAAAAA.json) |
| `AAAAAAAA` | 取 | [《史記・韓世家》][1170] | [JSON](y3i_rsz_brn_AAAAAAAA.json) |
| `AAAAAAAAA` | 韓文侯 | [《史記・韓世家》][1170] | [JSON](y3i_rsz_brn_AAAAAAAAA.json) |
| `AAAAAAAAAA` | 韓哀侯 | [《史記・韓世家》][1170] | [JSON](y3i_rsz_brn_AAAAAAAAAA.json) |
| `AAAAAAAAAAA` | 韓懿侯 | [《史記・韓世家》][1170] | [JSON](y3i_rsz_brn_AAAAAAAAAAA.json) |
| `AAAAAAAAAAAA` | 韓昭侯 | [《史記・韓世家》][1170] | [JSON](y3i_rsz_brn_AAAAAAAAAAAA.json) |
| `AAAAAAAAAAAAA` | 宣惠王 | [《史記・韓世家》][1170] | [JSON](y3i_rsz_brn_AAAAAAAAAAAAA.json) |

</details>

<details><summary><code>y3u_i0l_ztj</code> 韓宣王（趙世家候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 韓宣王 | [《史記・趙世家》][1168] | [JSON](y3u_i0l_ztj.json) |
| `A` | 倉 | [《史記・趙世家》][1168] | [JSON](y3u_i0l_ztj_A.json) |

</details>

<details><summary><code>y4i_pjk_4gn</code> 季歷（47 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 季歷 | [《史記・周本紀》][1146] | [JSON](y4i_pjk_4gn.json) |
| `A` | 西伯昌 | [《史記・周本紀》][1146] | [JSON](y4i_pjk_4gn_A.json) |
| `AA` | 周武王 | [《史記・周本紀》][1146] | [JSON](y4i_pjk_4gn_AA.json) |
| `AAA` | 晉唐叔 | [《史記・晉世家》][1164] | [JSON](y4i_pjk_4gn_AAA.json) |
| `AAAA` | 燮（晉侯） | [《史記・晉世家》][1164] | [JSON](y4i_pjk_4gn_AAAA.json) |
| `AAAAA` | 寧族（晉武侯） | [《史記・晉世家》][1164] | [JSON](y4i_pjk_4gn_AAAAA.json) |
| `AAAAAA` | 服人（晉成侯） | [《史記・晉世家》][1164] | [JSON](y4i_pjk_4gn_AAAAAA.json) |
| `AAAAAAA` | 福（晉厲侯） | [《史記・晉世家》][1164] | [JSON](y4i_pjk_4gn_AAAAAAA.json) |
| `AAAAAAAA` | 宜臼（晉靖侯） | [《史記・晉世家》][1164] | [JSON](y4i_pjk_4gn_AAAAAAAA.json) |
| `AAAAAAAA*A` | 欒賓（靖侯庶孫） | [《史記・晉世家》][1164] | [JSON](y4i_pjk_4gn_AAAAAAAA%2AA.json) |
| `AB` | 管叔 | [《史記・管蔡世家》][1160] | [JSON](y4i_pjk_4gn_AB.json) |
| `AC` | 蔡叔 | [《史記・管蔡世家》][1160] | [JSON](y4i_pjk_4gn_AC.json) |
| `ACA` | 胡（蔡仲） | [《史記・管蔡世家》][1160] | [JSON](y4i_pjk_4gn_ACA.json) |
| `ACAA` | 荒（蔡伯） | [《史記・管蔡世家》][1160] | [JSON](y4i_pjk_4gn_ACAA.json) |
| `ACAAA` | 宮侯（蔡君） | [《史記・管蔡世家》][1160] | [JSON](y4i_pjk_4gn_ACAAA.json) |
| `ACAAAA` | 厲侯（蔡君） | [《史記・管蔡世家》][1160] | [JSON](y4i_pjk_4gn_ACAAAA.json) |
| `ACAAAAA` | 武侯（蔡君） | [《史記・管蔡世家》][1160] | [JSON](y4i_pjk_4gn_ACAAAAA.json) |
| `ACAAAAAA` | 夷侯（蔡君） | [《史記・管蔡世家》][1160] | [JSON](y4i_pjk_4gn_ACAAAAAA.json) |
| `ACAAAAAAA` | 所事（蔡釐侯） | [《史記・管蔡世家》][1160] | [JSON](y4i_pjk_4gn_ACAAAAAAA.json) |
| `ACAAAAAAAA` | 興（蔡共侯） | [《史記・管蔡世家》][1160] | [JSON](y4i_pjk_4gn_ACAAAAAAAA.json) |
| `ACAAAAAAAAA` | 戴侯（蔡君） | [《史記・管蔡世家》][1160] | [JSON](y4i_pjk_4gn_ACAAAAAAAAA.json) |
| `ACAAAAAAAAAA` | 措父（蔡宣侯） | [《史記・管蔡世家》][1160] | [JSON](y4i_pjk_4gn_ACAAAAAAAAAA.json) |
| `ACAAAAAAAAAAA` | 封人（蔡桓侯） | [《史記・管蔡世家》][1160] | [JSON](y4i_pjk_4gn_ACAAAAAAAAAAA.json) |
| `AD` | 周公 | [《史記・魯周公世家》][1158] | [JSON](y4i_pjk_4gn_AD.json) |
| `ADA` | 伯禽 | [《史記・魯周公世家》][1158] | [JSON](y4i_pjk_4gn_ADA.json) |
| `ADAA` | 酋（魯考公） | [《史記・魯周公世家》][1158]、[《史記・三代世表》][1678] | [JSON](y4i_pjk_4gn_ADAA.json) |
| `AE` | 衛康叔封 | [《史記・衛康叔世家》][1162] | [JSON](y4i_pjk_4gn_AE.json) |
| `AEA` | 康伯（衛康叔子） | [《史記・衛康叔世家》][1162] | [JSON](y4i_pjk_4gn_AEA.json) |
| `AEAA` | 考伯（衛君） | [《史記・衛康叔世家》][1162] | [JSON](y4i_pjk_4gn_AEAA.json) |
| `AEAAA` | 嗣伯（衛君） | [《史記・衛康叔世家》][1162] | [JSON](y4i_pjk_4gn_AEAAA.json) |
| `AEAAAA` | 偼伯（衛君） | [《史記・衛康叔世家》][1162] | [JSON](y4i_pjk_4gn_AEAAAA.json) |
| `AEAAAAA` | 靖伯（衛君） | [《史記・衛康叔世家》][1162] | [JSON](y4i_pjk_4gn_AEAAAAA.json) |
| `AEAAAAAA` | 貞伯（衛君） | [《史記・衛康叔世家》][1162] | [JSON](y4i_pjk_4gn_AEAAAAAA.json) |
| `AEAAAAAAA` | 頃侯（衛君） | [《史記・衛康叔世家》][1162] | [JSON](y4i_pjk_4gn_AEAAAAAAA.json) |
| `AEAAAAAAAA` | 釐侯（衛君） | [《史記・衛康叔世家》][1162] | [JSON](y4i_pjk_4gn_AEAAAAAAAA.json) |
| `AF` | 伯邑考（文王長子） | [《史記・管蔡世家》][1160] | [JSON](y4i_pjk_4gn_AF.json) |
| `AG` | 曹叔振鐸 | [《史記・管蔡世家》][1160] | [JSON](y4i_pjk_4gn_AG.json) |
| `AGA` | 脾（曹太伯） | [《史記・管蔡世家》][1160] | [JSON](y4i_pjk_4gn_AGA.json) |
| `AGAA` | 平（曹仲君） | [《史記・管蔡世家》][1160] | [JSON](y4i_pjk_4gn_AGAA.json) |
| `AGAAA` | 侯（曹宮伯） | [《史記・管蔡世家》][1160] | [JSON](y4i_pjk_4gn_AGAAA.json) |
| `AGAAAA` | 云（曹孝伯） | [《史記・管蔡世家》][1160] | [JSON](y4i_pjk_4gn_AGAAAA.json) |
| `AGAAAAA` | 喜（曹夷伯） | [《史記・管蔡世家》][1160] | [JSON](y4i_pjk_4gn_AGAAAAA.json) |
| `AH` | 成叔武（文王子） | [《史記・管蔡世家》][1160] | [JSON](y4i_pjk_4gn_AH.json) |
| `AI` | 霍叔處（文王子） | [《史記・管蔡世家》][1160] | [JSON](y4i_pjk_4gn_AI.json) |
| `AJ` | 冉季載（文王少子） | [《史記・管蔡世家》][1160] | [JSON](y4i_pjk_4gn_AJ.json) |
| `B` | 虢叔 | [《史記・秦本紀》][1147]、[《史記・晉世家》][1164] | [JSON](y4i_pjk_4gn_B.json) |
| `C` | 虢仲（王季子） | [《史記・晉世家》][1164] | [JSON](y4i_pjk_4gn_C.json) |

</details>

<details><summary><code>y4x_cmp_976</code> 孫靜（12 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 孫靜 | [《三國志・宗室傳》][1032] | [JSON](y4x_cmp_976.json) |
| `A` | 孫瑜 | [《三國志・宗室傳》][1036] | [JSON](y4x_cmp_976_A.json) |
| `AA` | 孫彌〔孫瑜子〕 | [《三國志・宗室傳》][1036] | [JSON](y4x_cmp_976_AA.json) |
| `AB` | 孫熙〔孫瑜子〕 | [《三國志・宗室傳》][1036] | [JSON](y4x_cmp_976_AB.json) |
| `AC` | 孫耀 | [《三國志・宗室傳》][1036] | [JSON](y4x_cmp_976_AC.json) |
| `AD` | 孫曼 | [《三國志・宗室傳》][1036] | [JSON](y4x_cmp_976_AD.json) |
| `AE` | 孫紘 | [《三國志・宗室傳》][1036] | [JSON](y4x_cmp_976_AE.json) |
| `B` | 孫皎 | [《三國志・宗室傳》][1031] | [JSON](y4x_cmp_976_B.json) |
| `BA` | 孫胤 | [《三國志・宗室傳》][1031] | [JSON](y4x_cmp_976_BA.json) |
| `C` | 孫奐 | [《三國志・宗室傳》][1030] | [JSON](y4x_cmp_976_C.json) |
| `CA` | 孫承 | [《三國志・宗室傳》][1030] | [JSON](y4x_cmp_976_CA.json) |
| `D` | 孫謙〔孫靜子〕 | [《三國志・宗室傳》][1032] | [JSON](y4x_cmp_976_D.json) |

</details>

<details><summary><code>y73_ysx_y5x</code> 王牢（王玄謨祖）（7 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 王牢（王玄謨祖） | [《宋書・朱脩之 宗愨 王玄謨》][1522] | [JSON](y73_ysx_y5x.json) |
| `A` | 王秀（王玄謨父） | [《宋書・朱脩之 宗愨 王玄謨》][1522] | [JSON](y73_ysx_y5x_A.json) |
| `AA` | 王玄謨 | [《宋書・朱脩之 宗愨 王玄謨》][1522] | [JSON](y73_ysx_y5x_AA.json) |
| `AAA` | 王深（王玄謨子） | [《南史・王鎮惡　朱齡石　毛脩之　傅弘之　朱脩之　王玄謨》][778]、[《宋書・朱脩之 宗愨 王玄謨》][1521] | [JSON](y73_ysx_y5x_AAA.json) |
| `AAAA` | 王繢（王深子，王玄謨孫） | [《南史・王鎮惡　朱齡石　毛脩之　傅弘之　朱脩之　王玄謨》][778]、[《宋書・朱脩之 宗愨 王玄謨》][1521] | [JSON](y73_ysx_y5x_AAAA.json) |
| `AAB` | 王寬（王玄謨子） | [《南齊書・劉懷珍 李安民 王玄載》][537] | [JSON](y73_ysx_y5x_AAB.json) |
| `AAC` | 王瞻（字明遠，一字叔鸞，王玄謨子） | [《南史・王鎮惡　朱齡石　毛脩之　傅弘之　朱脩之　王玄謨》][782] | [JSON](y73_ysx_y5x_AAC.json) |

</details>

<details><summary><code>y97_huh_vuz</code> 秦襄公（34 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 秦襄公 | [《史記・秦本紀》][1147] | [JSON](y97_huh_vuz.json) |
| `A` | 秦文公 | [《史記・秦本紀》][1147] | [JSON](y97_huh_vuz_A.json) |
| `AA` | 靜公（卷末世系） | [《史記・秦始皇本紀》][1148] | [JSON](y97_huh_vuz_AA.json) |
| `AAA` | 憲公（卷末世系） | [《史記・秦始皇本紀》][1148] | [JSON](y97_huh_vuz_AAA.json) |
| `AAAA` | 秦德公 | [《史記・秦本紀》][1147] | [JSON](y97_huh_vuz_AAAA.json) |
| `AAAAA` | 秦穆公 | [《史記・秦本紀》][1147] | [JSON](y97_huh_vuz_AAAAA.json) |
| `AAAAAA` | 秦康公 | [《史記・秦本紀》][1147] | [JSON](y97_huh_vuz_AAAAAA.json) |
| `AAAAAAA` | 秦共公 | [《史記・秦本紀》][1147] | [JSON](y97_huh_vuz_AAAAAAA.json) |
| `AAAAAAAA` | 秦桓公 | [《史記・秦本紀》][1147] | [JSON](y97_huh_vuz_AAAAAAAA.json) |
| `AAAAAAAAA` | 秦景公 | [《史記・秦本紀》][1147] | [JSON](y97_huh_vuz_AAAAAAAAA.json) |
| `AAAAAAAAAA` | 秦哀公 | [《史記・秦本紀》][1147] | [JSON](y97_huh_vuz_AAAAAAAAAA.json) |
| `AAAAAAAAAAA` | 秦夷公 | [《史記・秦本紀》][1147] | [JSON](y97_huh_vuz_AAAAAAAAAAA.json) |
| `AAAAAAAAAAAA` | 秦惠公（夷公子） | [《史記・秦本紀》][1147] | [JSON](y97_huh_vuz_AAAAAAAAAAAA.json) |
| `AAAAAAAAAAAAA` | 秦悼公 | [《史記・秦本紀》][1147]、[《史記・秦始皇本紀》][1148] | [JSON](y97_huh_vuz_AAAAAAAAAAAAA.json) |
| `AAAAAAAAAAAAAA` | 秦厲共公 | [《史記・秦本紀》][1147] | [JSON](y97_huh_vuz_AAAAAAAAAAAAAA.json) |
| `AAAAAAAAAAAAAAA` | 秦躁公 | [《史記・秦本紀》][1147] | [JSON](y97_huh_vuz_AAAAAAAAAAAAAAA.json) |
| `AAAAAAAAAAAAAB` | 剌龔公（本文字形） | [《史記・秦始皇本紀》][1148] | [JSON](y97_huh_vuz_AAAAAAAAAAAAAB.json) |
| `AAAAAAAAAAAAABA` | 秦懷公 | [《史記・秦本紀》][1147] | [JSON](y97_huh_vuz_AAAAAAAAAAAAABA.json) |
| `AAAAAAAAAAAAABAA` | 昭子（秦懷公太子） | [《史記・秦本紀》][1147] | [JSON](y97_huh_vuz_AAAAAAAAAAAAABAA.json) |
| `AAAAAAAAAAAAABAAA` | 秦靈公 | [《史記・秦本紀》][1147] | [JSON](y97_huh_vuz_AAAAAAAAAAAAABAAA.json) |
| `AAAAAAAAAAAAABAAAA` | 秦獻公 | [《史記・秦本紀》][1147] | [JSON](y97_huh_vuz_AAAAAAAAAAAAABAAAA.json) |
| `AAAAAAAAAAAAABAAAAA` | 秦孝公 | [《史記・商君列傳》][1193] | [JSON](y97_huh_vuz_AAAAAAAAAAAAABAAAAA.json) |
| `AAAAAAAAAAAAABAAAAAA` | 秦惠王 | [《史記・張儀列傳》][1195] | [JSON](y97_huh_vuz_AAAAAAAAAAAAABAAAAAA.json) |
| `AAAAAAAAAAAAABAAAAAAA` | 秦武王 | [《史記・樗里子甘茂列傳》][1196] | [JSON](y97_huh_vuz_AAAAAAAAAAAAABAAAAAAA.json) |
| `AAAAAAAAAAAAABAAAAAAB` | 秦惠王女（燕太子婦） | [《史記・燕召公世家》][1159] | [JSON](y97_huh_vuz_AAAAAAAAAAAAABAAAAAAB.json) |
| `AAAAAAAAAAAAABAB` | 秦簡公 | [《史記・秦本紀》][1147] | [JSON](y97_huh_vuz_AAAAAAAAAAAAABAB.json) |
| `AAAAAAAAAAAAABABA` | 秦惠公（簡公子） | [《史記・秦本紀》][1147] | [JSON](y97_huh_vuz_AAAAAAAAAAAAABABA.json) |
| `AAAAAAAAAAAAABABAA` | 出子（秦惠公子） | [《史記・秦本紀》][1147] | [JSON](y97_huh_vuz_AAAAAAAAAAAAABABAA.json) |
| `AAAAAAAAAB` | 畢公（秦卷末世系） | [《史記・秦始皇本紀》][1148] | [JSON](y97_huh_vuz_AAAAAAAAAB.json) |
| `AAAAB` | 秦宣公 | [《史記・秦本紀》][1147] | [JSON](y97_huh_vuz_AAAAB.json) |
| `AAAAC` | 秦成公 | [《史記・秦本紀》][1147] | [JSON](y97_huh_vuz_AAAAC.json) |
| `AAAB` | 秦武公 | [《史記・秦本紀》][1147] | [JSON](y97_huh_vuz_AAAB.json) |
| `AAABA` | 白（秦武公子） | [《史記・秦本紀》][1147] | [JSON](y97_huh_vuz_AAABA.json) |
| `AAAC` | 出子 | [《史記・秦本紀》][1147] | [JSON](y97_huh_vuz_AAAC.json) |

</details>

<details><summary><code>yaj_2vc_98w</code> 吳廣（趙世家娃嬴父候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 吳廣 | [《史記・趙世家》][1168]、[《史記・六國年表》][1680] | [JSON](yaj_2vc_98w.json) |
| `A` | 娃嬴 | [《史記・趙世家》][1168] | [JSON](yaj_2vc_98w_A.json) |

</details>

<details><summary><code>yay_w6f_lis</code> 渾邪（公孫賀父）（衛將軍驃騎列傳候選）（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 渾邪（公孫賀父） | [《史記・衛將軍驃騎列傳》][1236] | [JSON](yay_w6f_lis.json) |
| `A` | 公孫賀 | [《史記・衛將軍驃騎列傳》][1236] | [JSON](yay_w6f_lis_A.json) |
| `AA` | 敬聲（公孫賀子） | [《史記・衛將軍驃騎列傳》][1236] | [JSON](yay_w6f_lis_AA.json) |

</details>

<details><summary><code>yd9_rqt_a0v</code> 悦〔玄伯祖，北史作悅〕（8 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 悦〔玄伯祖，北史作悅〕 | [《魏書・燕鳳 許謙 張衮 崔玄伯 鄧淵》][1609]、[《魏書・燕鳳 許謙 張衮 崔玄伯 鄧淵》][1610] | [JSON](yd9_rqt_a0v.json) |
| `A` | 潛〔玄伯父〕 | [《魏書・燕鳳 許謙 張衮 崔玄伯 鄧淵》][1609] | [JSON](yd9_rqt_a0v_A.json) |
| `AA` | 崔宏 | [《魏書・燕鳳 許謙 張衮 崔玄伯 鄧淵》][1609] | [JSON](yd9_rqt_a0v_AA.json) |
| `AAA` | 簡〔玄伯次子，一名覽〕 | [《魏書・燕鳳 許謙 張衮 崔玄伯 鄧淵》][1609] | [JSON](yd9_rqt_a0v_AAA.json) |
| `AAB` | 崔浩 | [《魏書・崔浩》][1611] | [JSON](yd9_rqt_a0v_AAB.json) |
| `AABA` | 崔浩女〔盧遐妻，未名〕 | [《魏書・刁雍 王慧龍 韓延之 袁式》][1613] | [JSON](yd9_rqt_a0v_AABA.json) |
| `AAC` | 崔恬 | [《魏書・燕鳳 許謙 張衮 崔玄伯 鄧淵》][1609] | [JSON](yd9_rqt_a0v_AAC.json) |
| `AACA` | 崔恬女〔王慧龍妻，未名〕 | [《魏書・刁雍 王慧龍 韓延之 袁式》][1613] | [JSON](yd9_rqt_a0v_AACA.json) |

</details>

<details><summary><code>yfa_tz5_3ge</code> 王韶之（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 王韶之 | [《宋書・范泰 王准之 王韶之 荀伯子》][1496] | [JSON](yfa_tz5_3ge.json) |
| `A` | 王曄（王韶之子） | [《南史・王裕之　王鎮之　王韶之　王悅之　王准之》][877]、[《南史・王裕之　王鎮之　王韶之　王悅之　王准之》][876]、[《宋書・范泰 王准之 王韶之 荀伯子》][1496] | [JSON](yfa_tz5_3ge_A.json) |

</details>

<details><summary><code>yfm_7fm_2ei</code> 崔朝（6 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 崔朝 | [《後漢書・崔駰列傳》][122] | [JSON](yfm_7fm_2ei.json) |
| `A` | 崔舒 | [《後漢書・崔駰列傳》][122] | [JSON](yfm_7fm_2ei_A.json) |
| `AA` | 崔篆 | [《後漢書・崔駰列傳》][122] | [JSON](yfm_7fm_2ei_AA.json) |
| `AAA` | 崔毅 | [《後漢書・崔駰列傳》][122] | [JSON](yfm_7fm_2ei_AAA.json) |
| `AAAA` | 崔駰 | [《後漢書・崔駰列傳》][122] | [JSON](yfm_7fm_2ei_AAAA.json) |
| `AAAAA` | 崔瑗 | [《後漢書・崔駰列傳》][122] | [JSON](yfm_7fm_2ei_AAAAA.json) |

</details>

<details><summary><code>yhm_h9f_8p0</code> 范蠡（越世家候選）（4 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 范蠡 | [《史記・越王勾踐世家》][1166] | [JSON](yhm_h9f_8p0.json) |
| `A` | 朱公長男（越世家未名者） | [《史記・越王勾踐世家》][1166] | [JSON](yhm_h9f_8p0_A.json) |
| `B` | 朱公中男（越世家未名者） | [《史記・越王勾踐世家》][1166] | [JSON](yhm_h9f_8p0_B.json) |
| `C` | 朱公少子（越世家未名者） | [《史記・越王勾踐世家》][1166] | [JSON](yhm_h9f_8p0_C.json) |

</details>

<details><summary><code>yht_8tu_hv4</code> 齊景公（田世家候選）（4 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 齊景公 | [《史記・田敬仲完世家》][1171] | [JSON](yht_8tu_hv4.json) |
| `A` | 荼 | [《史記・田敬仲完世家》][1171] | [JSON](yht_8tu_hv4_A.json) |
| `B` | 陽生 | [《史記・田敬仲完世家》][1171] | [JSON](yht_8tu_hv4_B.json) |
| `BA` | 壬 | [《史記・田敬仲完世家》][1171] | [JSON](yht_8tu_hv4_BA.json) |

</details>

<details><summary><code>yi6_2hu_y7e</code> 袁僧惠（宜都太守）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 袁僧惠（宜都太守） | [《宋書・后妃》][1347] | [JSON](yi6_2hu_y7e.json) |
| `A` | 袁僧惠女（宋前廢帝為太子時保林） | — | [JSON](yi6_2hu_y7e_A.json) |

</details>

<details><summary><code>ykp_uqh_6be</code> 張仲子（張興世父，宋書及南史見）（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 張仲子（張興世父，宋書及南史見） | [《宋書・胡藩 劉康祖 垣護之 張興世》][1474] | [JSON](ykp_uqh_6be.json) |
| `A` | 張興世（字文德，本名世，竟陵人） | [《宋書・胡藩 劉康祖 垣護之 張興世》][1475] | [JSON](ykp_uqh_6be_A.json) |
| `AA` | 張欣業（宋書記當嗣張興世爵） | [《宋書・胡藩 劉康祖 垣護之 張興世》][1473] | [JSON](ykp_uqh_6be_AA.json) |

</details>

<details><summary><code>ylb_ttg_8dr</code> 百里傒（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 百里傒 | [《史記・秦本紀》][1147] | [JSON](ylb_ttg_8dr.json) |
| `A` | 孟明視 | [《史記・秦本紀》][1147] | [JSON](ylb_ttg_8dr_A.json) |

</details>

<details><summary><code>ymr_gcs_kii</code> 熊嚴（楚君）（10 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 熊嚴（楚君） | [《史記・楚世家》][1165] | [JSON](ymr_gcs_kii.json) |
| `A` | 伯霜（熊霜） | [《史記・楚世家》][1165] | [JSON](ymr_gcs_kii_A.json) |
| `B` | 仲雪（熊嚴子） | [《史記・楚世家》][1165] | [JSON](ymr_gcs_kii_B.json) |
| `C` | 叔堪（熊嚴子） | [《史記・楚世家》][1165] | [JSON](ymr_gcs_kii_C.json) |
| `D` | 季徇（熊徇） | [《史記・楚世家》][1165] | [JSON](ymr_gcs_kii_D.json) |
| `DA` | 熊咢（楚君） | [《史記・楚世家》][1165] | [JSON](ymr_gcs_kii_DA.json) |
| `DAA` | 熊儀（若敖） | [《史記・楚世家》][1165] | [JSON](ymr_gcs_kii_DAA.json) |
| `DAAA` | 熊坎（霄敖） | [《史記・楚世家》][1165] | [JSON](ymr_gcs_kii_DAAA.json) |
| `DAAAA` | 熊眴（蚡冒） | [《史記・楚世家》][1165] | [JSON](ymr_gcs_kii_DAAAA.json) |
| `DAAAAA` | 蚡冒子（熊通所弒未名者） | [《史記・楚世家》][1165] | [JSON](ymr_gcs_kii_DAAAAA.json) |

</details>

<details><summary><code>yoo_ox0_545</code> 荀淑（51 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 荀淑 | [《後漢書・荀韓鍾陳列傳》][123] | [JSON](yoo_ox0_545.json) |
| `A` | 荀儉 | [《後漢書・荀韓鍾陳列傳》][123] | [JSON](yoo_ox0_545_A.json) |
| `AA` | 荀恱 | [《後漢書・荀韓鍾陳列傳》][123] | [JSON](yoo_ox0_545_AA.json) |
| `B` | 荀緄 | [《三國志・二荀賈傳》][973] | [JSON](yoo_ox0_545_B.json) |
| `BA` | 荀彧 | [《三國志・二荀賈傳》][973] | [JSON](yoo_ox0_545_BA.json) |
| `BAA` | 荀顗 | [《晉書・王沈 荀顗 荀勖 馮紞》][208] | [JSON](yoo_ox0_545_BAA.json) |
| `BAB` | 荀惲 | [《三國志・二荀賈傳》][973] | [JSON](yoo_ox0_545_BAB.json) |
| `BABA` | 荀甝 | [《三國志・二荀賈傳》][973] | [JSON](yoo_ox0_545_BABA.json) |
| `BABAA` | 荀頵 | [《三國志・二荀賈傳》][973] | [JSON](yoo_ox0_545_BABAA.json) |
| `BABAAA` | 荀崧 | [《晉書・王湛 荀崧 范汪 劉惔 張憑 韓伯》][294] | [JSON](yoo_ox0_545_BABAAA.json) |
| `BABAAAA` | 荀蕤 | [《晉書・王湛 荀崧 范汪 劉惔 張憑 韓伯》][294] | [JSON](yoo_ox0_545_BABAAAA.json) |
| `BABAAAAA` | 荀籍 | [《晉書・王湛 荀崧 范汪 劉惔 張憑 韓伯》][293]、[《晉書・王湛 荀崧 范汪 劉惔 張憑 韓伯》][294] | [JSON](yoo_ox0_545_BABAAAAA.json) |
| `BABAAAB` | 荀羨 | [《晉書・王湛 荀崧 范汪 劉惔 張憑 韓伯》][294] | [JSON](yoo_ox0_545_BABAAAB.json) |
| `BABAAABA` | 荀猗 | [《宋書・范泰 王准之 王韶之 荀伯子》][1498] | [JSON](yoo_ox0_545_BABAAABA.json) |
| `BABAAABAA` | 荀伯子 | [《宋書・范泰 王准之 王韶之 荀伯子》][1498] | [JSON](yoo_ox0_545_BABAAABAA.json) |
| `BABAAABAAA` | 荀赤松 | [《宋書・范泰 王准之 王韶之 荀伯子》][1498] | [JSON](yoo_ox0_545_BABAAABAAA.json) |
| `BABAAAC` | 荀灌 | [《晉書・列女》][340]、[《晉書・列女》][338] | [JSON](yoo_ox0_545_BABAAAC.json) |
| `BABB` | 荀霬 | [《三國志・二荀賈傳》][973] | [JSON](yoo_ox0_545_BABB.json) |
| `BABBA` | 荀愷 | [《三國志・二荀賈傳》][973] | [JSON](yoo_ox0_545_BABBA.json) |
| `BABBB` | 荀憺 | [《三國志・二荀賈傳》][973] | [JSON](yoo_ox0_545_BABBB.json) |
| `BABBC` | 荀悝 | [《三國志・二荀賈傳》][973] | [JSON](yoo_ox0_545_BABBC.json) |
| `BAC` | 荀俁 | [《三國志・二荀賈傳》][973] | [JSON](yoo_ox0_545_BAC.json) |
| `BACA` | 荀寓 | [《三國志・二荀賈傳》][973] | [JSON](yoo_ox0_545_BACA.json) |
| `BACAA` | 荀羽 | [《三國志・二荀賈傳》][973] | [JSON](yoo_ox0_545_BACAA.json) |
| `BAD` | 荀詵 | [《三國志・二荀賈傳》][973] | [JSON](yoo_ox0_545_BAD.json) |
| `BAE` | 荀粲 | [《三國志・二荀賈傳》][973] | [JSON](yoo_ox0_545_BAE.json) |
| `BAF` | 荀氏（陳群妻，荀顗姊） | [《晉書・王沈 荀顗 荀勖 馮紞》][208]、[《三國志・二荀賈傳》][973] | [JSON](yoo_ox0_545_BAF.json) |
| `BB` | 荀衍 | [《三國志・二荀賈傳》][973] | [JSON](yoo_ox0_545_BB.json) |
| `BBA` | 荀紹 | [《三國志・二荀賈傳》][973] | [JSON](yoo_ox0_545_BBA.json) |
| `BBAA` | 荀融 | [《三國志・二荀賈傳》][973] | [JSON](yoo_ox0_545_BBAA.json) |
| `BC` | 荀諶 | [《三國志・二荀賈傳》][973] | [JSON](yoo_ox0_545_BC.json) |
| `BCA` | 荀閎 | [《三國志・二荀賈傳》][973] | [JSON](yoo_ox0_545_BCA.json) |
| `C` | 荀靖 | [《後漢書・荀韓鍾陳列傳》][123] | [JSON](yoo_ox0_545_C.json) |
| `D` | 荀燾 | [《後漢書・荀韓鍾陳列傳》][123] | [JSON](yoo_ox0_545_D.json) |
| `E` | 荀汪 | [《後漢書・荀韓鍾陳列傳》][123] | [JSON](yoo_ox0_545_E.json) |
| `F` | 荀爽 | [《後漢書・荀韓鍾陳列傳》][123] | [JSON](yoo_ox0_545_F.json) |
| `FA` | 荀棐 | [《晉書・王沈 荀顗 荀勖 馮紞》][208] | [JSON](yoo_ox0_545_FA.json) |
| `FAA` | 荀肸 | [《晉書・王沈 荀顗 荀勖 馮紞》][208] | [JSON](yoo_ox0_545_FAA.json) |
| `FAAA` | 荀勖 | [《晉書・王沈 荀顗 荀勖 馮紞》][208] | [JSON](yoo_ox0_545_FAAA.json) |
| `FAAAA` | 荀藩 | [《晉書・王沈 荀顗 荀勖 馮紞》][208] | [JSON](yoo_ox0_545_FAAAA.json) |
| `FAAAAA` | 邃（荀藩子） | [《晉書・王沈 荀顗 荀勖 馮紞》][208] | [JSON](yoo_ox0_545_FAAAAA.json) |
| `FAAAAAA` | 汪（荀邃子） | [《晉書・王沈 荀顗 荀勖 馮紞》][208] | [JSON](yoo_ox0_545_FAAAAAA.json) |
| `FAAAAB` | 闓（荀藩子） | [《晉書・王沈 荀顗 荀勖 馮紞》][208] | [JSON](yoo_ox0_545_FAAAAB.json) |
| `FAAAABA` | 達（荀闓子） | [《晉書・王沈 荀顗 荀勖 馮紞》][208] | [JSON](yoo_ox0_545_FAAAABA.json) |
| `FAAAB` | 荀輯 | [《晉書・王沈 荀顗 荀勖 馮紞》][208] | [JSON](yoo_ox0_545_FAAAB.json) |
| `FAAABA` | 畯（荀輯子） | [《晉書・王沈 荀顗 荀勖 馮紞》][208] | [JSON](yoo_ox0_545_FAAABA.json) |
| `FAAABB` | 荀綽 | [《晉書・王沈 荀顗 荀勖 馮紞》][208] | [JSON](yoo_ox0_545_FAAABB.json) |
| `FAAAC` | 荀組 | [《晉書・王沈 荀顗 荀勖 馮紞》][208] | [JSON](yoo_ox0_545_FAAAC.json) |
| `FAAACA` | 奕（荀組子） | [《晉書・王沈 荀顗 荀勖 馮紞》][208] | [JSON](yoo_ox0_545_FAAACA.json) |
| `G` | 荀肅 | [《後漢書・荀韓鍾陳列傳》][123] | [JSON](yoo_ox0_545_G.json) |
| `H` | 荀專 | [《後漢書・荀韓鍾陳列傳》][123] | [JSON](yoo_ox0_545_H.json) |

</details>

<details><summary><code>yph_dkb_w4w</code> 申屠嘉（4 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 申屠嘉 | [《史記・張丞相列傳》][1221] | [JSON](yph_dkb_w4w.json) |
| `A` | 申屠蔑 | [《史記・張丞相列傳》][1221] | [JSON](yph_dkb_w4w_A.json) |
| `AA` | 申屠去病 | [《史記・張丞相列傳》][1221] | [JSON](yph_dkb_w4w_AA.json) |
| `AAA` | 申屠臾 | [《史記・張丞相列傳》][1221] | [JSON](yph_dkb_w4w_AAA.json) |

</details>

<details><summary><code>yqp_nlb_p1p</code> 太公（漢王父稱）（125 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 太公（漢王父稱） | [《史記・高祖本紀》][1150] | [JSON](yqp_nlb_p1p.json) |
| `A` | 高祖 | [《史記・高祖本紀》][1150] | [JSON](yqp_nlb_p1p_A.json) |
| `AA` | 孝惠（本卷稱呼） | [《史記・呂后本紀》][1151] | [JSON](yqp_nlb_p1p_AA.json) |
| `AB` | 劉肥 | [《史記・齊悼惠王世家》][1177] | [JSON](yqp_nlb_p1p_AB.json) |
| `ABA` | 齊哀王（本卷未名） | [《史記・齊悼惠王世家》][1177] | [JSON](yqp_nlb_p1p_ABA.json) |
| `ABB` | 卬（膠西王） | [《史記・吳王濞列傳》][1231] | [JSON](yqp_nlb_p1p_ABB.json) |
| `ABBA` | 膠西王太子德 | [《史記・吳王濞列傳》][1231] | [JSON](yqp_nlb_p1p_ABBA.json) |
| `ABC` | 興居（齊悼惠王子） | [《史記・齊悼惠王世家》][1177] | [JSON](yqp_nlb_p1p_ABC.json) |
| `ABD` | 辟光（濟南王） | [《史記・齊悼惠王世家》][1177] | [JSON](yqp_nlb_p1p_ABD.json) |
| `ABE` | 雄渠（膠東王） | [《史記・齊悼惠王世家》][1177]、[《史記・吳王濞列傳》][1231] | [JSON](yqp_nlb_p1p_ABE.json) |
| `ABF` | 章（城陽景王） | [《史記・齊悼惠王世家》][1177] | [JSON](yqp_nlb_p1p_ABF.json) |
| `ABFA` | 喜（城陽共王） | [《史記・齊悼惠王世家》][1177]、[《史記・漢興以來諸侯王年表》][1682] | [JSON](yqp_nlb_p1p_ABFA.json) |
| `ABFAA` | 延校勘建未定 | [《史記・齊悼惠王世家》][1177] | [JSON](yqp_nlb_p1p_ABFAA.json) |
| `ABFAAA` | 義 | [《史記・齊悼惠王世家》][1177] | [JSON](yqp_nlb_p1p_ABFAAA.json) |
| `ABFAAAA` | 武城陽惠王 | [《史記・齊悼惠王世家》][1177] | [JSON](yqp_nlb_p1p_ABFAAAA.json) |
| `ABFAAAAA` | 順 | [《史記・齊悼惠王世家》][1177] | [JSON](yqp_nlb_p1p_ABFAAAAA.json) |
| `ABFAAAAAA` | 恢城陽戴王 | [《史記・齊悼惠王世家》][1177] | [JSON](yqp_nlb_p1p_ABFAAAAAA.json) |
| `ABFAAAAAAA` | 景城陽末王 | [《史記・齊悼惠王世家》][1177] | [JSON](yqp_nlb_p1p_ABFAAAAAAA.json) |
| `ABFAB` | 劉福 | [《史記・東越列傳》][1239]、[《史記・建元以來侯者年表》][1685]、[《史記・建元已來王子侯者年表》][1686] | [JSON](yqp_nlb_p1p_ABFAB.json) |
| `ABFAC` | 劉齒 | [《史記・建元已來王子侯者年表》][1686] | [JSON](yqp_nlb_p1p_ABFAC.json) |
| `ABG` | 賢（菑川王） | [《史記・齊悼惠王世家》][1177]、[《史記・吳王濞列傳》][1231] | [JSON](yqp_nlb_p1p_ABG.json) |
| `ABH` | 志（濟北王，後王菑川） | [《史記・齊悼惠王世家》][1177] | [JSON](yqp_nlb_p1p_ABH.json) |
| `ABHA` | 建菑川靖王 | [《史記・齊悼惠王世家》][1177] | [JSON](yqp_nlb_p1p_ABHA.json) |
| `ABHAA` | 遺 | [《史記・齊悼惠王世家》][1177] | [JSON](yqp_nlb_p1p_ABHAA.json) |
| `ABHAAA` | 終古 | [《史記・齊悼惠王世家》][1177] | [JSON](yqp_nlb_p1p_ABHAAA.json) |
| `ABHAAAA` | 尚菑川孝王 | [《史記・齊悼惠王世家》][1177] | [JSON](yqp_nlb_p1p_ABHAAAA.json) |
| `ABHAAAAA` | 橫 | [《史記・齊悼惠王世家》][1177] | [JSON](yqp_nlb_p1p_ABHAAAAA.json) |
| `ABI` | 齊孝王將閭 | [《史記・齊悼惠王世家》][1177] | [JSON](yqp_nlb_p1p_ABI.json) |
| `AC` | 恒（高祖子） | [《史記・孝文本紀》][1152] | [JSON](yqp_nlb_p1p_AC.json) |
| `ACA` | 孝景帝 | [《史記・梁孝王世家》][1183] | [JSON](yqp_nlb_p1p_ACA.json) |
| `ACAA` | 孝武皇帝 | [《史記・孝武本紀》][1154] | [JSON](yqp_nlb_p1p_ACAA.json) |
| `ACAAA` | 閎（齊王） | [《史記・三王世家》][1185] | [JSON](yqp_nlb_p1p_ACAAA.json) |
| `ACAAB` | 旦 | [《史記・三王世家》][1185] | [JSON](yqp_nlb_p1p_ACAAB.json) |
| `ACAABA` | 安定侯子 | [《史記・三王世家》][1185] | [JSON](yqp_nlb_p1p_ACAABA.json) |
| `ACAABB` | 建 | [《史記・三王世家》][1185] | [JSON](yqp_nlb_p1p_ACAABB.json) |
| `ACAAC` | 胥 | [《史記・三王世家》][1185] | [JSON](yqp_nlb_p1p_ACAAC.json) |
| `ACAACA` | 朝陽侯子 | [《史記・三王世家》][1185] | [JSON](yqp_nlb_p1p_ACAACA.json) |
| `ACAACB` | 平曲侯子 | [《史記・三王世家》][1185] | [JSON](yqp_nlb_p1p_ACAACB.json) |
| `ACAACC` | 南利侯子 | [《史記・三王世家》][1185] | [JSON](yqp_nlb_p1p_ACAACC.json) |
| `ACAACD` | 弘 | [《史記・三王世家》][1185] | [JSON](yqp_nlb_p1p_ACAACD.json) |
| `ACAAD` | 據 | [《史記・田叔列傳》][1229] | [JSON](yqp_nlb_p1p_ACAAD.json) |
| `ACAAE` | 昭帝 | [《史記・三王世家》][1185] | [JSON](yqp_nlb_p1p_ACAAE.json) |
| `ACAAF` | 昌邑哀王髆 | [《漢書・武五子傳》][109] | [JSON](yqp_nlb_p1p_ACAAF.json) |
| `ACAAFA` | 賀（海昬侯） | [《漢書・武五子傳》][109] | [JSON](yqp_nlb_p1p_ACAAFA.json) |
| `ACAB` | 德 | [《史記・五宗世家》][1184] | [JSON](yqp_nlb_p1p_ACAB.json) |
| `ACABA` | 不害 | [《史記・五宗世家》][1184] | [JSON](yqp_nlb_p1p_ACABA.json) |
| `ACABAA` | 基 | [《史記・五宗世家》][1184] | [JSON](yqp_nlb_p1p_ACABAA.json) |
| `ACABAAA` | 授 | [《史記・五宗世家》][1184]、[《史記・漢興以來諸侯王年表》][1682] | [JSON](yqp_nlb_p1p_ACABAAA.json) |
| `ACAC` | 閼于 | [《史記・五宗世家》][1184] | [JSON](yqp_nlb_p1p_ACAC.json) |
| `ACAD` | 發 | [《史記・五宗世家》][1184] | [JSON](yqp_nlb_p1p_ACAD.json) |
| `ACADA` | 庸 | [《史記・五宗世家》][1184]、[《史記・漢興以來諸侯王年表》][1682] | [JSON](yqp_nlb_p1p_ACADA.json) |
| `ACADAA` | 鮒鮈 | [《史記・五宗世家》][1184] | [JSON](yqp_nlb_p1p_ACADAA.json) |
| `ACAE` | 乘 | [《史記・五宗世家》][1184] | [JSON](yqp_nlb_p1p_ACAE.json) |
| `ACAF` | 趙王彭祖 | [《史記・五宗世家》][1184] | [JSON](yqp_nlb_p1p_ACAF.json) |
| `ACAG` | 舜（景帝子） | [《史記・五宗世家》][1184] | [JSON](yqp_nlb_p1p_ACAG.json) |
| `ACAGA` | 棁 | [《史記・五宗世家》][1184] | [JSON](yqp_nlb_p1p_ACAGA.json) |
| `ACAGB` | 平 | [《史記・五宗世家》][1184] | [JSON](yqp_nlb_p1p_ACAGB.json) |
| `ACAGC` | 商 | [《史記・五宗世家》][1184] | [JSON](yqp_nlb_p1p_ACAGC.json) |
| `ACAGCA` | 安世 | [《史記・五宗世家》][1184] | [JSON](yqp_nlb_p1p_ACAGCA.json) |
| `ACAH` | 栗太子（本卷未名） | [《史記・五宗世家》][1184] | [JSON](yqp_nlb_p1p_ACAH.json) |
| `ACAI` | 勝（景帝子） | [《史記・五宗世家》][1184] | [JSON](yqp_nlb_p1p_ACAI.json) |
| `ACAIA` | 昌 | [《史記・五宗世家》][1184]、[《史記・漢興以來諸侯王年表》][1682] | [JSON](yqp_nlb_p1p_ACAIA.json) |
| `ACAIAA` | 昆侈 | [《史記・五宗世家》][1184] | [JSON](yqp_nlb_p1p_ACAIAA.json) |
| `ACAJ` | 越（景帝子） | [《史記・五宗世家》][1184] | [JSON](yqp_nlb_p1p_ACAJ.json) |
| `ACAJA` | 齊 | [《史記・五宗世家》][1184] | [JSON](yqp_nlb_p1p_ACAJA.json) |
| `ACAK` | 非（汝南王） | [《史記・五宗世家》][1184] | [JSON](yqp_nlb_p1p_ACAK.json) |
| `ACAKA` | 建 | [《史記・五宗世家》][1184] | [JSON](yqp_nlb_p1p_ACAKA.json) |
| `ACAL` | 餘（淮陽王） | [《史記・田叔列傳》][1229] | [JSON](yqp_nlb_p1p_ACAL.json) |
| `ACALA` | 光 | [《史記・五宗世家》][1184] | [JSON](yqp_nlb_p1p_ACALA.json) |
| `ACAM` | 寄（景帝子） | [《史記・五宗世家》][1184] | [JSON](yqp_nlb_p1p_ACAM.json) |
| `ACAMA` | 賢 | [《史記・五宗世家》][1184] | [JSON](yqp_nlb_p1p_ACAMA.json) |
| `ACAMAA` | 膠東慶 | [《史記・五宗世家》][1184] | [JSON](yqp_nlb_p1p_ACAMAA.json) |
| `ACAMB` | 六安慶 | [《史記・五宗世家》][1184] | [JSON](yqp_nlb_p1p_ACAMB.json) |
| `ACAN` | 端 | [《史記・五宗世家》][1184] | [JSON](yqp_nlb_p1p_ACAN.json) |
| `ACB` | 梁懷王 | [《史記・屈原賈生列傳》][1209] | [JSON](yqp_nlb_p1p_ACB.json) |
| `ACC` | 參 | [《史記・梁孝王世家》][1183] | [JSON](yqp_nlb_p1p_ACC.json) |
| `ACCA` | 登 | [《史記・梁孝王世家》][1183] | [JSON](yqp_nlb_p1p_ACCA.json) |
| `ACCAA` | 義 | [《史記・梁孝王世家》][1183] | [JSON](yqp_nlb_p1p_ACCAA.json) |
| `ACD` | 勝 | [《史記・梁孝王世家》][1183] | [JSON](yqp_nlb_p1p_ACD.json) |
| `ACE` | 孝文帝女公主 | [《史記・絳侯周勃世家》][1182] | [JSON](yqp_nlb_p1p_ACE.json) |
| `ACF` | 嫖（長公主） | [《史記・外戚世家》][1174] | [JSON](yqp_nlb_p1p_ACF.json) |
| `ACG` | 梁孝王武 | [《史記・梁孝王世家》][1183] | [JSON](yqp_nlb_p1p_ACG.json) |
| `ACGA` | 買 | [《史記・梁孝王世家》][1183] | [JSON](yqp_nlb_p1p_ACGA.json) |
| `ACGAA` | 襄 | [《史記・梁孝王世家》][1183] | [JSON](yqp_nlb_p1p_ACGAA.json) |
| `ACGAAA` | 無傷 | [《史記・梁孝王世家》][1183] | [JSON](yqp_nlb_p1p_ACGAAA.json) |
| `ACGB` | 明 | [《史記・梁孝王世家》][1183] | [JSON](yqp_nlb_p1p_ACGB.json) |
| `ACGC` | 彭離 | [《史記・梁孝王世家》][1183] | [JSON](yqp_nlb_p1p_ACGC.json) |
| `ACGD` | 定 | [《史記・梁孝王世家》][1183] | [JSON](yqp_nlb_p1p_ACGD.json) |
| `ACGE` | 不識 | [《史記・梁孝王世家》][1183] | [JSON](yqp_nlb_p1p_ACGE.json) |
| `AD` | 恢（高祖子） | [《史記・呂后本紀》][1151] | [JSON](yqp_nlb_p1p_AD.json) |
| `AE` | 友（高祖子） | [《史記・呂后本紀》][1151] | [JSON](yqp_nlb_p1p_AE.json) |
| `AEA` | 遂（趙幽王子） | [《史記・楚元王世家》][1175] | [JSON](yqp_nlb_p1p_AEA.json) |
| `AEB` | 辟彊（趙幽王子） | [《史記・孝文本紀》][1152]、[《史記・楚元王世家》][1175]、[《史記・漢興以來諸侯王年表》][1682] | [JSON](yqp_nlb_p1p_AEB.json) |
| `AEBA` | 福 | [《史記・楚元王世家》][1175]、[《史記・漢興以來諸侯王年表》][1682] | [JSON](yqp_nlb_p1p_AEBA.json) |
| `AF` | 長（高祖子） | [《史記・淮南衡山列傳》][1243] | [JSON](yqp_nlb_p1p_AF.json) |
| `AFA` | 淮南王安 | [《史記・淮南衡山列傳》][1243] | [JSON](yqp_nlb_p1p_AFA.json) |
| `AFAA` | 陵（淮南王女） | [《史記・淮南衡山列傳》][1243] | [JSON](yqp_nlb_p1p_AFAA.json) |
| `AFAB` | 不害 | [《史記・淮南衡山列傳》][1243] | [JSON](yqp_nlb_p1p_AFAB.json) |
| `AFABA` | 建（不害子） | [《史記・淮南衡山列傳》][1243] | [JSON](yqp_nlb_p1p_AFABA.json) |
| `AFAC` | 淮南太子遷 | [《史記・淮南衡山列傳》][1243] | [JSON](yqp_nlb_p1p_AFAC.json) |
| `AFB` | 濟北王勃 | [《史記・淮南衡山列傳》][1243] | [JSON](yqp_nlb_p1p_AFB.json) |
| `AFC` | 衡山王賜 | [《史記・淮南衡山列傳》][1243] | [JSON](yqp_nlb_p1p_AFC.json) |
| `AFCA` | 爽（衡山太子） | [《史記・淮南衡山列傳》][1243] | [JSON](yqp_nlb_p1p_AFCA.json) |
| `AFCB` | 孝（衡山王子） | [《史記・淮南衡山列傳》][1243] | [JSON](yqp_nlb_p1p_AFCB.json) |
| `AFCC` | 無采 | [《史記・淮南衡山列傳》][1243] | [JSON](yqp_nlb_p1p_AFCC.json) |
| `AFD` | 東城侯良 | [《史記・淮南衡山列傳》][1243]、[《史記・惠景間侯者年表》][1684] | [JSON](yqp_nlb_p1p_AFD.json) |
| `AG` | 建（高祖子） | [《史記・高祖本紀》][1150]、[《史記・呂后本紀》][1151]、[《史記・漢興以來諸侯王年表》][1682] | [JSON](yqp_nlb_p1p_AG.json) |
| `AH` | 如意（高祖子） | [《史記・呂后本紀》][1151] | [JSON](yqp_nlb_p1p_AH.json) |
| `AI` | 魯元（本卷稱呼） | [《史記・呂后本紀》][1151] | [JSON](yqp_nlb_p1p_AI.json) |
| `B` | 伯 | [《史記・楚元王世家》][1175] | [JSON](yqp_nlb_p1p_B.json) |
| `BA` | 信羹頡侯 | [《史記・楚元王世家》][1175] | [JSON](yqp_nlb_p1p_BA.json) |
| `C` | 仲 | [《史記・高祖本紀》][1150]、[《史記・吳王濞列傳》][1231] | [JSON](yqp_nlb_p1p_C.json) |
| `CA` | 劉濞 | [《史記・吳王濞列傳》][1231] | [JSON](yqp_nlb_p1p_CA.json) |
| `CAA` | 吳太子被殺未名 | [《漢書・荊燕吳傳》][103]、[《史記・吳王濞列傳》][1231] | [JSON](yqp_nlb_p1p_CAA.json) |
| `CAB` | 吳王少子未名 | [《漢書・荊燕吳傳》][103]、[《史記・吳王濞列傳》][1231] | [JSON](yqp_nlb_p1p_CAB.json) |
| `CAD` | 子華 | [《史記・吳王濞列傳》][1231] | [JSON](yqp_nlb_p1p_CAD.json) |
| `CAE` | 駒（吳王太子；《史記》作子駒） | [《漢書・荊燕吳傳》][103]、[《史記・吳王濞列傳》][1231] | [JSON](yqp_nlb_p1p_CAE.json) |
| `D` | 劉交 | [《史記・楚元王世家》][1175] | [JSON](yqp_nlb_p1p_D.json) |
| `DA` | 藝（楚元王子） | [《史記・孝景本紀》][1153] | [JSON](yqp_nlb_p1p_DA.json) |
| `DB` | 禮（楚元王子） | [《史記・楚元王世家》][1175] | [JSON](yqp_nlb_p1p_DB.json) |
| `DBA` | 道 | [《史記・楚元王世家》][1175] | [JSON](yqp_nlb_p1p_DBA.json) |
| `DBAA` | 注 | [《史記・楚元王世家》][1175] | [JSON](yqp_nlb_p1p_DBAA.json) |
| `DBAAA` | 純 | [《史記・楚元王世家》][1175] | [JSON](yqp_nlb_p1p_DBAAA.json) |
| `DC` | 郢 | [《史記・儒林列傳》][1246] | [JSON](yqp_nlb_p1p_DC.json) |
| `DCA` | 戊（楚王） | [《史記・吳王濞列傳》][1231] | [JSON](yqp_nlb_p1p_DCA.json) |

</details>

<details><summary><code>yt0_0mx_ah5</code> 石碏（衛諫臣）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 石碏（衛諫臣） | [《史記・衛康叔世家》][1162] | [JSON](yt0_0mx_ah5.json) |
| `A` | 石厚 | [《春秋左傳注疏・卷2》][1674] | [JSON](yt0_0mx_ah5_A.json) |

</details>

<details><summary><code>z0l_1wp_de1</code> 趙破奴（匈奴列傳第44段）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 趙破奴（匈奴列傳第44段） | [《史記・匈奴列傳》][1235] | [JSON](z0l_1wp_de1.json) |
| `A` | 安國（趙破奴子） | [《史記・衛將軍驃騎列傳》][1236] | [JSON](z0l_1wp_de1_A.json) |

</details>

<details><summary><code>z0n_1jd_fda</code> 胡奮（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 胡奮 | [《晉書・后妃上》][192]、[《三國志・桓二陳徐衞盧傳》][988]、[《三國志・三嗣主傳》][1004] | [JSON](z0n_1jd_fda.json) |
| `A` | 胡芳〔武帝貴嬪〕 | [《晉書・后妃上》][192] | [JSON](z0n_1jd_fda_A.json) |

</details>

<details><summary><code>z5z_p09_02j</code> 孫孺（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 孫孺 | [《三國志・宗室傳》][1027] | [JSON](z5z_p09_02j.json) |
| `A` | 孫香〔字文陽〕 | [《三國志・宗室傳》][1027] | [JSON](z5z_p09_02j_A.json) |

</details>

<details><summary><code>z8c_kq5_fri</code> 安成康王秀〔梁〕（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 安成康王秀〔梁〕 | [《梁書・裴子野 顧協 徐摛 鮑泉》][452]、[《梁書・太祖五王》][413]、[《梁書・陸倕 到洽 明山賓 殷鈞 陸襄》][420] | [JSON](z8c_kq5_fri.json) |
| `A` | 蕭機（安成煬王，字智通） | [《陳書・列傳第十一: 王沖 王通 袁敬》][48] | [JSON](z8c_kq5_fri_A.json) |

</details>

<details><summary><code>z8l_wje_08d</code> 卜商（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 卜商 | [《史記・仲尼弟子列傳》][1192] | [JSON](z8l_wje_08d.json) |
| `A` | 卜商之子 | [《史記・仲尼弟子列傳》][1192] | [JSON](z8l_wje_08d_A.json) |

</details>

<details><summary><code>z8m_9y0_s2w</code> 江統〔字應元〕（5 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 江統〔字應元〕 | [《晉書・江統 孫楚》][253]、[《晉書・叛臣一》][344]、[《梁書・韋粲 江子一 弟子四 子五 張嵊 沈浚 柳敬禮》][467]、[《南史・江子一　胡僧祐　徐文盛　陰子春　杜崱　王琳　張彪》][961] | [JSON](z8m_9y0_s2w.json) |
| `*****A` | 江法成（奉朝請） | [《梁書・韋粲 江子一 弟子四 子五 張嵊 沈浚 柳敬禮》][467]、[《南史・江子一　胡僧祐　徐文盛　陰子春　杜崱　王琳　張彪》][961] | [JSON](z8m_9y0_s2w_%2A%2A%2A%2A%2AA.json) |
| `*****AA` | 江子一（《梁書》字元貞） | [《梁書・韋粲 江子一 弟子四 子五 張嵊 沈浚 柳敬禮》][467] | [JSON](z8m_9y0_s2w_%2A%2A%2A%2A%2AAA.json) |
| `*****AB` | 江子四（江子一弟） | [《梁書・韋粲 江子一 弟子四 子五 張嵊 沈浚 柳敬禮》][465]、[《梁書・韋粲 江子一 弟子四 子五 張嵊 沈浚 柳敬禮》][467] | [JSON](z8m_9y0_s2w_%2A%2A%2A%2A%2AAB.json) |
| `*****AC` | 江子五（江子一弟） | [《梁書・韋粲 江子一 弟子四 子五 張嵊 沈浚 柳敬禮》][467] | [JSON](z8m_9y0_s2w_%2A%2A%2A%2A%2AAC.json) |

</details>

<details><summary><code>z9d_qn5_wg8</code> 路人（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 路人 | [《史記・朝鮮列傳》][1240] | [JSON](z9d_qn5_wg8.json) |
| `A` | 最 | [《史記・建元以來侯者年表》][1685] | [JSON](z9d_qn5_wg8_A.json) |

</details>

<details><summary><code>z9e_8iy_7ah</code> 崔輯（4 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 崔輯 | [《魏書・燕鳳 許謙 張衮 崔玄伯 鄧淵》][1608] | [JSON](z9e_8iy_7ah.json) |
| `A` | 崔攸之 | [《北史・崔光 崔亮》][9]、[《魏書・燕鳳 許謙 張衮 崔玄伯 鄧淵》][1608] | [JSON](z9e_8iy_7ah_A.json) |
| `B` | 崔目連 | [《北史・崔光 崔亮》][9]、[《魏書・燕鳳 許謙 張衮 崔玄伯 鄧淵》][1608] | [JSON](z9e_8iy_7ah_B.json) |
| `C` | 崔修之 | [《北史・崔光 崔亮》][9] | [JSON](z9e_8iy_7ah_C.json) |

</details>

<details><summary><code>zan_qcc_jy5</code> 陳文公（田世家候選）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 陳文公 | [《史記・田敬仲完世家》][1171] | [JSON](zan_qcc_jy5.json) |
| `A` | 陳厲公他 | [《史記・田敬仲完世家》][1171] | [JSON](zan_qcc_jy5_A.json) |

</details>

<details><summary><code>zba_hzr_ebw</code> 馬援（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 馬援 | [《三國志・徐胡二王傳》][992] | [JSON](zba_hzr_ebw.json) |
| `A` | 漢明德馬皇后（伏波將軍馬援小女） | [《後漢書・皇后紀》][117] | [JSON](zba_hzr_ebw_A.json) |

</details>

<details><summary><code>zf4_z2k_9s8</code> 章道蓋（齊廣平太守）（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 章道蓋（齊廣平太守） | [《陳書・列傳第五: 黃法抃 淳于量 章昭達》][40] | [JSON](zf4_z2k_9s8.json) |
| `A` | 章法尚（梁揚州議曹從事） | [《陳書・列傳第五: 黃法抃 淳于量 章昭達》][40] | [JSON](zf4_z2k_9s8_A.json) |
| `AA` | 章昭達（字伯通） | [《陳書・列傳第五: 黃法抃 淳于量 章昭達》][40] | [JSON](zf4_z2k_9s8_AA.json) |

</details>

<details><summary><code>zk0_g6b_nbq</code> 伍奢（楚篇候選）（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 伍奢 | [《史記・楚世家》][1165] | [JSON](zk0_g6b_nbq.json) |
| `A` | 伍尚 | [《史記・楚世家》][1165] | [JSON](zk0_g6b_nbq_A.json) |
| `B` | 伍胥 | [《史記・楚世家》][1165] | [JSON](zk0_g6b_nbq_B.json) |

</details>

<details><summary><code>zql_k3t_8ro</code> 先軫（重耳五士）（2 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 先軫（重耳五士） | [《史記・晉世家》][1164] | [JSON](zql_k3t_8ro.json) |
| `A` | 先縠（右行將） | [《史記・晉世家》][1164] | [JSON](zql_k3t_8ro_A.json) |

</details>

<details><summary><code>zrx_2ip_d1p</code> 張負（陳丞相世家候選）（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 張負 | [《史記・陳丞相世家》][1181] | [JSON](zrx_2ip_d1p.json) |
| `*A` | 張氏女 | [《史記・陳丞相世家》][1181] | [JSON](zrx_2ip_d1p_%2AA.json) |
| `A` | 張仲 | [《史記・陳丞相世家》][1181] | [JSON](zrx_2ip_d1p_A.json) |

</details>

<details><summary><code>zuf_v5v_18s</code> 孟懷玉（3 名）</summary>

| ID 尾碼 | 人物 | 最多提及來源 | JSON |
|---|---|---|---|
| `根` | 孟懷玉 | [《宋書・劉懷肅 孟懷玉 劉敬宣 檀祗》][1393] | [JSON](zuf_v5v_18s.json) |
| `A` | 孟元（孟懷玉子） | [《宋書・劉懷肅 孟懷玉 劉敬宣 檀祗》][1391]、[《宋書・劉懷肅 孟懷玉 劉敬宣 檀祗》][1398] | [JSON](zuf_v5v_18s_A.json) |
| `B` | 孟慧熙（孟懷玉子） | [《宋書・劉懷肅 孟懷玉 劉敬宣 檀祗》][1391] | [JSON](zuf_v5v_18s_B.json) |

</details>

[2]: https://zh.wikisource.org/w/index.php?oldid=2432527
[8]: https://zh.wikisource.org/w/index.php?title=北史/卷044&oldid=2183262
[9]: https://zh.wikisource.org/w/index.php?title=北史/卷044&oldid=2183262
[12]: https://zh.wikisource.org/w/index.php?oldid=2361318
[14]: https://zh.wikisource.org/w/index.php?oldid=8231316
[27]: https://zh.wikisource.org/w/index.php?oldid=2015446
[28]: https://zh.wikisource.org/w/index.php?oldid=2015446
[30]: https://zh.wikisource.org/w/index.php?oldid=2015446
[31]: https://commons.wikimedia.org/w/index.php?oldid=997527595
[35]: https://zh.wikisource.org/w/index.php?oldid=1750028
[38]: https://zh.wikisource.org/w/index.php?oldid=1488469
[40]: https://zh.wikisource.org/w/index.php?oldid=1488472
[45]: https://zh.wikisource.org/w/index.php?oldid=2261985
[48]: https://zh.wikisource.org/w/index.php?oldid=1544244
[51]: https://zh.wikisource.org/w/index.php?oldid=1544244
[53]: https://zh.wikisource.org/w/index.php?oldid=1544244
[54]: https://zh.wikisource.org/w/index.php?oldid=1544244
[55]: https://zh.wikisource.org/w/index.php?oldid=1544244
[57]: https://zh.wikisource.org/w/index.php?oldid=2132781
[59]: https://zh.wikisource.org/w/index.php?title=陳書/卷21&oldid=1511909
[61]: https://zh.wikisource.org/w/index.php?oldid=1514496
[63]: https://zh.wikisource.org/w/index.php?oldid=1514496
[71]: https://zh.wikisource.org/w/index.php?oldid=2581394
[72]: https://zh.wikisource.org/w/index.php?oldid=2581394
[73]: https://zh.wikisource.org/w/index.php?oldid=2581394
[74]: https://zh.wikisource.org/w/index.php?oldid=2581394
[76]: https://zh.wikisource.org/w/index.php?oldid=2581394
[79]: https://zh.wikisource.org/w/index.php?oldid=1530928
[81]: https://www.sohu.com/a/259439652_258370
[82]: https://guji.10huan.com/Article/7147_7165.html
[83]: https://imgsoflfg-1302780771.cos.ap-shanghai.myqcloud.com/lfgimgs/94b58f207eda4759b6d188b00fc826c6p5.jpg
[84]: https://lfglib.cn/wp-content/uploads/lfgimgs/gujicover/94b58f207eda4759b6d188b00fc826c6p1.jpg
[88]: https://www.i-repository.net/il/cont/01/G0000721f/000/756/000756292.jpg
[90]: https://www.sohu.com/a/279761580_738227
[93]: http://csid.zju.edu.cn/tomb/stone/detail?id=40288b955bd07752015bfb74a80002de
[98]: https://zh.wikisource.org/w/index.php?oldid=636080
[103]: https://zh.wikisource.org/w/index.php?title=漢書/卷035&oldid=2605377
[104]: https://zh.wikisource.org/w/index.php?title=漢書/卷041&oldid=2342290
[105]: https://github.com/kanripo/KR2a0007/blob/683113d4baf6febecaf2ccb7913df87c4d68d454/KR2a0007_050.txt
[109]: https://github.com/kanripo/KR2a0007/blob/683113d4baf6febecaf2ccb7913df87c4d68d454/KR2a0007_063.txt
[113]: https://zh.wikisource.org/w/index.php?oldid=2605445
[117]: https://zh.wikisource.org/w/index.php?oldid=8737760
[119]: https://zh.wikisource.org/w/index.php?oldid=2191216
[120]: https://zh.wikisource.org/w/index.php?oldid=2191216
[121]: https://zh.wikisource.org/w/index.php?oldid=2191216
[122]: https://zh.wikisource.org/w/index.php?title=後漢書/卷52&oldid=1956641
[123]: https://github.com/kanripo/KR2a0009/blob/6db36b6dcbe843b825354c22e9be9193d0137c04/KR2a0009_092.txt
[125]: https://github.com/kanripo/KR2a0009/blob/6db36b6dcbe843b825354c22e9be9193d0137c04/KR2a0009_094.txt
[131]: https://commons.wikimedia.org/w/index.php?oldid=1269465774
[132]: https://zh.wikisource.org/w/index.php?oldid=740760
[176]: https://raw.githubusercontent.com/kanripo/KR2a0015/82291520954e5af1fdade894971a2f5810fd4e31/KR2a0015_008.txt
[185]: https://zh.wikisource.org/w/index.php?oldid=2567072
[192]: https://zh.wikisource.org/w/index.php?oldid=2479706
[193]: https://zh.wikisource.org/w/index.php?oldid=1543614
[194]: https://zh.wikisource.org/w/index.php?oldid=1543614
[198]: https://zh.wikisource.org/w/index.php?oldid=1543614
[199]: https://zh.wikisource.org/w/index.php?title=%E6%99%89%E6%9B%B8%2F%E5%8D%B7032&oldid=1543614
[201]: https://zh.wikisource.org/w/index.php?title=%E6%99%89%E6%9B%B8%2F%E5%8D%B7035&oldid=2506399
[208]: https://zh.wikisource.org/w/index.php?title=晉書/卷039&oldid=2108782
[217]: https://zh.wikisource.org/w/index.php?oldid=2618531
[227]: https://zh.wikisource.org/w/index.php?oldid=1775345
[228]: https://zh.wikisource.org/w/index.php?oldid=1775345
[230]: https://zh.wikisource.org/w/index.php?oldid=1775345
[232]: https://zh.wikisource.org/w/index.php?oldid=1775345
[237]: https://zh.wikisource.org/w/index.php?oldid=1775345
[238]: https://zh.wikisource.org/w/index.php?oldid=1775345
[241]: https://zh.wikisource.org/w/index.php?oldid=2305862
[253]: https://zh.wikisource.org/w/index.php?oldid=1557685
[255]: https://zh.wikisource.org/w/index.php?oldid=2413329
[272]: https://zh.wikisource.org/w/index.php?oldid=2592755
[273]: https://zh.wikisource.org/w/index.php?oldid=2592755
[277]: https://zh.wikisource.org/w/index.php?oldid=2592755
[278]: https://commons.wikimedia.org/w/index.php?oldid=1047611719
[279]: https://zh.wikisource.org/w/index.php?oldid=2592755
[289]: https://zh.wikisource.org/w/index.php?oldid=2296501
[290]: https://zh.wikisource.org/w/index.php?title=晉書/卷074&oldid=1536331
[292]: https://zh.wikisource.org/w/index.php?title=晉書/卷075&oldid=2645530
[293]: https://zh.wikisource.org/w/index.php?title=%E6%99%89%E6%9B%B8+%28%E5%9B%9B%E5%BA%AB%E5%85%A8%E6%9B%B8%E6%9C%AC%29%2F%E5%8D%B7075&oldid=761900
[294]: https://zh.wikisource.org/w/index.php?title=晉書/卷075&oldid=2645530
[295]: https://zh.wikisource.org/w/index.php?oldid=2180533
[301]: https://zh.wikisource.org/w/index.php?oldid=2180533
[302]: https://zh.wikisource.org/w/index.php?oldid=2180533
[308]: https://zh.wikisource.org/w/index.php?oldid=1506266
[310]: https://zh.wikisource.org/w/index.php?oldid=2603570
[318]: https://zh.wikisource.org/w/index.php?title=%E6%99%89%E6%9B%B8%2F%E5%8D%B7089&oldid=2835777
[320]: https://zh.wikisource.org/w/index.php?title=晉書/卷090&oldid=2835599
[323]: https://zh.wikisource.org/w/index.php?oldid=2835641
[324]: https://zh.wikisource.org/w/index.php?oldid=1548000
[325]: https://zh.wikisource.org/w/index.php?oldid=1548000
[332]: https://commons.wikimedia.org/w/index.php?oldid=979438884
[333]: https://zh.wikisource.org/w/index.php?oldid=2625341
[338]: https://commons.wikimedia.org/w/index.php?oldid=979438884
[340]: https://zh.wikisource.org/w/index.php?title=晉書/卷096&oldid=2625341
[343]: https://zh.wikisource.org/w/index.php?title=晉書/卷098&oldid=2614273
[344]: https://zh.wikisource.org/w/index.php?oldid=2614273
[345]: https://zh.wikisource.org/w/index.php?oldid=2614273
[347]: https://zh.wikisource.org/w/index.php?title=晉書/卷099&oldid=2644703
[350]: https://zh.wikisource.org/w/index.php?oldid=2614279
[351]: https://zh.wikisource.org/w/index.php?title=%E6%99%89%E6%9B%B8%2F%E5%8D%B7100&oldid=2614279
[363]: https://zh.wikisource.org/w/index.php?oldid=1729539
[375]: https://zh.wikisource.org/w/index.php?oldid=2311629
[379]: https://zh.wikisource.org/w/index.php?oldid=1566494
[380]: https://zh.wikisource.org/w/index.php?title=梁書/卷07&oldid=1566494
[381]: https://zh.wikisource.org/w/index.php?oldid=1566494
[382]: https://zh.wikisource.org/w/index.php?oldid=1566494
[383]: https://zh.wikisource.org/w/index.php?oldid=1566494
[385]: https://zh.wikisource.org/w/index.php?oldid=1538023
[389]: https://zh.wikisource.org/w/index.php?title=梁書/卷15&oldid=1506954
[397]: https://zh.wikisource.org/w/index.php?oldid=1508017
[400]: https://zh.wikisource.org/w/index.php?title=梁書/卷21&oldid=1544250
[402]: https://zh.wikisource.org/w/index.php?title=梁書/卷21&oldid=1544250
[404]: https://zh.wikisource.org/w/index.php?oldid=1544250
[409]: https://commons.wikimedia.org/w/index.php?oldid=902340163
[410]: https://zh.wikisource.org/w/index.php?oldid=1544250
[412]: https://zh.wikisource.org/w/index.php?oldid=1513347
[413]: https://zh.wikisource.org/w/index.php?oldid=1513347
[414]: https://zh.wikisource.org/w/index.php?oldid=1513347
[415]: https://zh.wikisource.org/w/index.php?oldid=1513347
[416]: https://zh.wikisource.org/w/index.php?oldid=1513347
[417]: https://zh.wikisource.org/w/index.php?oldid=1511478
[420]: https://zh.wikisource.org/w/index.php?oldid=1511478
[424]: https://zh.wikisource.org/w/index.php?oldid=1511478
[425]: https://zh.wikisource.org/w/index.php?oldid=1511478
[427]: https://zh.wikisource.org/w/index.php?oldid=1511478
[429]: https://zh.wikisource.org/w/index.php?oldid=1511902
[431]: https://zh.wikisource.org/w/index.php?oldid=1511902
[432]: https://zh.wikisource.org/w/index.php?oldid=1511902
[435]: https://zh.wikisource.org/w/index.php?oldid=1511902
[437]: https://zh.wikisource.org/w/index.php?oldid=1511902
[441]: https://zh.wikisource.org/w/index.php?oldid=1538079
[442]: https://zh.wikisource.org/w/index.php?oldid=1538079
[445]: https://zh.wikisource.org/w/index.php?oldid=1538079
[449]: https://zh.wikisource.org/w/index.php?oldid=1538079
[450]: https://zh.wikisource.org/w/index.php?oldid=1538079
[451]: https://zh.wikisource.org/w/index.php?oldid=1538079
[452]: https://zh.wikisource.org/w/index.php?title=%E6%A2%81%E6%9B%B8%2F%E5%8D%B730&oldid=1508510
[453]: https://zh.wikisource.org/w/index.php?oldid=1530926
[456]: https://commons.wikimedia.org/wiki/File:NLC892-411999017142-12700_二十四史_第167冊.pdf
[457]: https://zh.wikisource.org/w/index.php?oldid=1514481
[460]: https://zh.wikisource.org/w/index.php?oldid=1552297
[463]: https://zh.wikisource.org/w/index.php?oldid=1512987
[465]: https://zh.wikisource.org/w/index.php?oldid=2087360
[467]: https://zh.wikisource.org/w/index.php?oldid=2087360
[469]: https://zh.wikisource.org/w/index.php?oldid=2087360
[471]: https://zh.wikisource.org/w/index.php?oldid=2087360
[476]: https://zh.wikisource.org/w/index.php?oldid=2376749
[478]: https://zh.wikisource.org/w/index.php?oldid=2376749
[479]: https://zh.wikisource.org/w/index.php?oldid=2197034
[481]: https://zh.wikisource.org/w/index.php?oldid=1514482
[485]: https://commons.wikimedia.org/w/index.php?oldid=703777627
[486]: https://zh.wikisource.org/w/index.php?title=梁書/卷50&oldid=1514482
[488]: https://zh.wikisource.org/w/index.php?oldid=1530936
[507]: https://commons.wikimedia.org/w/index.php?oldid=703777584
[508]: https://zh.wikisource.org/w/index.php?oldid=2074177
[509]: https://commons.wikimedia.org/w/index.php?oldid=703777584
[510]: https://zh.wikisource.org/w/index.php?oldid=2074177
[518]: https://commons.wikimedia.org/w/index.php?oldid=703777584
[519]: https://zh.wikisource.org/w/index.php?title=南齊書/卷20&oldid=2074177
[520]: https://commons.wikimedia.org/w/index.php?oldid=703777584
[521]: https://zh.wikisource.org/w/index.php?title=南齊書/卷20&oldid=2074177
[528]: https://commons.wikimedia.org/w/index.php?oldid=703777584
[529]: https://zh.wikisource.org/w/index.php?title=南齊書/卷20&oldid=2074177
[530]: https://zh.wikisource.org/w/index.php?oldid=1545488
[535]: https://zh.wikisource.org/w/index.php?oldid=1508012
[537]: https://zh.wikisource.org/w/index.php?oldid=1508012
[538]: https://zh.wikisource.org/w/index.php?oldid=1508012
[541]: https://zh.wikisource.org/w/index.php?oldid=1508012
[545]: https://zh.wikisource.org/w/index.php?oldid=1513917
[546]: https://zh.wikisource.org/w/index.php?oldid=2062531
[548]: https://zh.wikisource.org/w/index.php?oldid=1513918
[549]: https://zh.wikisource.org/w/index.php?oldid=1513918
[550]: https://zh.wikisource.org/w/index.php?oldid=1513918
[575]: https://zh.wikisource.org/w/index.php?oldid=2273226
[584]: https://zh.wikisource.org/w/index.php?oldid=2272748
[585]: https://zh.wikisource.org/w/index.php?title=南齊書/卷40&oldid=2272748
[586]: https://zh.wikisource.org/w/index.php?oldid=2272748
[587]: https://zh.wikisource.org/w/index.php?oldid=2272748
[588]: https://zh.wikisource.org/w/index.php?oldid=2272748
[589]: https://zh.wikisource.org/w/index.php?oldid=2272748
[593]: https://zh.wikisource.org/w/index.php?oldid=2272748
[594]: https://zh.wikisource.org/w/index.php?oldid=2272748
[597]: https://zh.wikisource.org/w/index.php?oldid=2272748
[598]: https://zh.wikisource.org/w/index.php?oldid=2272748
[601]: https://zh.wikisource.org/w/index.php?oldid=2272748
[603]: https://zh.wikisource.org/w/index.php?oldid=2272748
[604]: https://zh.wikisource.org/w/index.php?oldid=2272748
[605]: https://zh.wikisource.org/w/index.php?oldid=2272748
[607]: https://zh.wikisource.org/w/index.php?oldid=2272748
[608]: https://zh.wikisource.org/w/index.php?oldid=2272748
[610]: https://zh.wikisource.org/w/index.php?oldid=2272748
[612]: https://zh.wikisource.org/w/index.php?oldid=2044621
[614]: https://zh.wikisource.org/w/index.php?oldid=2044621
[616]: https://zh.wikisource.org/w/index.php?oldid=1507997
[617]: https://zh.wikisource.org/w/index.php?oldid=1507997
[628]: https://zh.wikisource.org/w/index.php?oldid=2400356
[629]: https://zh.wikisource.org/w/index.php?oldid=2400356
[635]: https://zh.wikisource.org/w/index.php?oldid=1507959
[637]: https://zh.wikisource.org/w/index.php?oldid=1507959
[639]: https://zh.wikisource.org/w/index.php?oldid=2273185
[640]: https://zh.wikisource.org/w/index.php?oldid=2273185
[641]: https://zh.wikisource.org/w/index.php?oldid=2273185
[649]: https://zh.wikisource.org/w/index.php?oldid=1511897
[651]: https://zh.wikisource.org/w/index.php?oldid=1511897
[652]: https://zh.wikisource.org/w/index.php?oldid=1511897
[653]: https://zh.wikisource.org/w/index.php?oldid=1511897
[655]: https://zh.wikisource.org/w/index.php?oldid=1511897
[656]: https://zh.wikisource.org/w/index.php?title=%E5%8D%97%E9%BD%8A%E6%9B%B8%2F%E5%8D%B746&oldid=1511897
[659]: https://zh.wikisource.org/w/index.php?title=南齊書/卷47&oldid=1492435
[663]: https://zh.wikisource.org/w/index.php?title=南齊書/卷48&oldid=1511898
[664]: https://zh.wikisource.org/w/index.php?oldid=1511898
[667]: https://zh.wikisource.org/w/index.php?oldid=2261984
[668]: https://zh.wikisource.org/w/index.php?oldid=2261984
[674]: https://zh.wikisource.org/w/index.php?oldid=2261984
[681]: https://zh.wikisource.org/w/index.php?oldid=2272731
[686]: https://zh.wikisource.org/w/index.php?oldid=1504716
[689]: https://zh.wikisource.org/w/index.php?oldid=2371079
[690]: https://zh.wikisource.org/w/index.php?oldid=2371079
[691]: https://zh.wikisource.org/w/index.php?oldid=2371079
[692]: https://github.com/kanripo/KR2a0017/blob/787dd9a7da495542e8f17c26c96900ce37b2c211/KR2a0017_052.txt
[694]: https://zh.wikisource.org/w/index.php?oldid=1501803
[695]: https://zh.wikisource.org/w/index.php?oldid=1501803
[699]: https://zh.wikisource.org/w/index.php?oldid=1762878
[700]: https://zh.wikisource.org/w/index.php?oldid=1762878
[702]: https://zh.wikisource.org/w/index.php?oldid=1762878
[710]: https://zh.wikisource.org/w/index.php?oldid=1999801
[716]: https://zh.wikisource.org/w/index.php?oldid=2027696
[719]: https://commons.wikimedia.org/w/index.php?oldid=1298729844
[720]: https://zh.wikisource.org/w/index.php?oldid=2288359
[721]: https://commons.wikimedia.org/w/index.php?oldid=1298729844
[722]: https://zh.wikisource.org/w/index.php?oldid=2288359
[725]: https://commons.wikimedia.org/w/index.php?oldid=1298729844
[726]: https://zh.wikisource.org/w/index.php?oldid=2288359
[728]: https://commons.wikimedia.org/w/index.php?oldid=1298729844
[729]: https://zh.wikisource.org/w/index.php?oldid=2288359
[730]: https://commons.wikimedia.org/w/index.php?oldid=1298729844
[731]: https://zh.wikisource.org/w/index.php?oldid=2288359
[734]: https://commons.wikimedia.org/w/index.php?oldid=1298729844
[735]: https://zh.wikisource.org/w/index.php?title=南史/卷11&oldid=2288359
[744]: https://commons.wikimedia.org/w/index.php?oldid=1298729844
[745]: https://zh.wikisource.org/w/index.php?oldid=2288359
[746]: https://commons.wikimedia.org/w/index.php?oldid=1298729844
[747]: https://zh.wikisource.org/w/index.php?oldid=2288359
[753]: https://zh.wikisource.org/w/index.php?oldid=2060595
[756]: https://zh.wikisource.org/w/index.php?oldid=2060595
[759]: https://zh.wikisource.org/w/index.php?oldid=2060595
[761]: https://zh.wikisource.org/w/index.php?oldid=2060595
[762]: https://zh.wikisource.org/w/index.php?oldid=2060595
[763]: https://zh.wikisource.org/w/index.php?oldid=2060595
[764]: https://zh.wikisource.org/w/index.php?oldid=2060595
[766]: https://zh.wikisource.org/w/index.php?oldid=2060595
[768]: https://zh.wikisource.org/w/index.php?oldid=2268660
[771]: https://zh.wikisource.org/w/index.php?oldid=1659582
[772]: https://zh.wikisource.org/w/index.php?oldid=1659582
[778]: https://zh.wikisource.org/w/index.php?oldid=1963381
[782]: https://zh.wikisource.org/w/index.php?oldid=1963381
[799]: https://zh.wikisource.org/w/index.php?title=南史/卷19&oldid=1531762
[800]: https://zh.wikisource.org/w/index.php?title=南史/卷19&oldid=1531762
[810]: https://zh.wikisource.org/w/index.php?oldid=1752646
[813]: https://zh.wikisource.org/w/index.php?oldid=1752646
[818]: https://zh.wikisource.org/w/index.php?oldid=1752646
[823]: https://zh.wikisource.org/w/index.php?oldid=1477957
[824]: https://zh.wikisource.org/w/index.php?oldid=1477957
[829]: https://commons.wikimedia.org/wiki/File:NLC892-411999017142-12360_二十四史_第246冊.pdf
[830]: https://zh.wikisource.org/w/index.php?title=南史/卷22&oldid=1477957
[835]: https://zh.wikisource.org/w/index.php?oldid=1477957
[836]: https://zh.wikisource.org/w/index.php?oldid=1477957
[837]: https://commons.wikimedia.org/wiki/File:NLC892-411999017142-12360_二十四史_第246冊.pdf
[838]: https://zh.wikisource.org/w/index.php?oldid=1477957
[839]: https://zh.wikisource.org/w/index.php?oldid=1477957
[840]: https://github.com/kanripo/KR2a0024/blob/3c7bdbb072bf8e1eb70d134a94570c4b8de058ea/KR2a0024_022.txt
[841]: https://zh.wikisource.org/w/index.php?title=南史/卷23&oldid=2478204
[842]: https://commons.wikimedia.org/wiki/File:NLC892-411999017142-12361_二十四史_第247冊.pdf
[843]: https://zh.wikisource.org/w/index.php?oldid=2478204
[844]: https://zh.wikisource.org/w/index.php?oldid=2478204
[845]: https://zh.wikisource.org/w/index.php?title=南史/卷23&oldid=2478204
[846]: https://zh.wikisource.org/w/index.php?oldid=2478204
[849]: https://zh.wikisource.org/w/index.php?oldid=2478204
[854]: https://zh.wikisource.org/w/index.php?oldid=2478204
[859]: https://zh.wikisource.org/w/index.php?oldid=2478204
[862]: https://zh.wikisource.org/w/index.php?oldid=2478204
[863]: https://zh.wikisource.org/w/index.php?oldid=2478204
[864]: https://zh.wikisource.org/w/index.php?oldid=2478204
[865]: https://zh.wikisource.org/w/index.php?oldid=2478204
[866]: https://zh.wikisource.org/w/index.php?oldid=2478204
[869]: https://zh.wikisource.org/w/index.php?oldid=1765279
[871]: https://commons.wikimedia.org/w/index.php?oldid=1158108475
[875]: https://zh.wikisource.org/w/index.php?oldid=1765279
[876]: https://commons.wikimedia.org/wiki/File:NLC892-411999017142-12361_%E4%BA%8C%E5%8D%81%E5%9B%9B%E5%8F%B2_%E7%AC%AC247%E5%86%8A.pdf
[877]: https://zh.wikisource.org/w/index.php?oldid=1765279
[879]: https://zh.wikisource.org/w/index.php?oldid=1765279
[882]: https://zh.wikisource.org/w/index.php?oldid=1765279
[886]: https://zh.wikisource.org/w/index.php?title=%E5%8D%97%E5%8F%B2%2F%E5%8D%B724&oldid=1765279
[891]: https://zh.wikisource.org/w/index.php?oldid=12757141
[892]: https://upload.wikimedia.org/wikipedia/commons/a/a5/NLC892-411999017142-12361_%E4%BA%8C%E5%8D%81%E5%9B%9B%E5%8F%B2_%E7%AC%AC247%E5%86%8A.pdf#page=49
[895]: https://zh.wikisource.org/w/index.php?oldid=1477359
[897]: https://zh.wikisource.org/w/index.php?oldid=1611067
[898]: https://zh.wikisource.org/w/index.php?oldid=1511857
[899]: https://zh.wikisource.org/w/index.php?oldid=1511857
[900]: https://zh.wikisource.org/w/index.php?oldid=1511857
[906]: https://zh.wikisource.org/w/index.php?oldid=1494939
[907]: https://zh.wikisource.org/w/index.php?oldid=1494939
[908]: https://zh.wikisource.org/w/index.php?title=%E5%8D%97%E5%8F%B2%2F%E5%8D%B733&oldid=1554233
[909]: https://zh.wikisource.org/w/index.php?title=南史/卷33&oldid=1554233
[912]: https://zh.wikisource.org/w/index.php?oldid=1489333
[919]: https://zh.wikisource.org/w/index.php?oldid=2027785
[923]: https://zh.wikisource.org/w/index.php?oldid=2027785
[924]: https://zh.wikisource.org/w/index.php?oldid=2027785
[931]: https://zh.wikisource.org/w/index.php?oldid=2598501
[934]: https://zh.wikisource.org/w/index.php?oldid=2493997
[935]: https://zh.wikisource.org/w/index.php?oldid=2493997
[936]: https://zh.wikisource.org/w/index.php?oldid=2493997
[938]: https://zh.wikisource.org/w/index.php?oldid=12945115
[939]: https://zh.wikisource.org/w/index.php?oldid=1748892
[940]: https://zh.wikisource.org/w/index.php?oldid=2027179
[941]: https://zh.wikisource.org/w/index.php?oldid=2027179
[947]: https://zh.wikisource.org/w/index.php?oldid=2063857
[951]: https://zh.wikisource.org/w/index.php?oldid=1484916
[957]: https://zh.wikisource.org/w/index.php?oldid=1553912
[959]: https://zh.wikisource.org/w/index.php?oldid=1495505
[960]: https://zh.wikisource.org/w/index.php?oldid=1748895
[961]: https://zh.wikisource.org/w/index.php?oldid=1748895
[962]: https://zh.wikisource.org/w/index.php?oldid=1748897
[966]: https://zh.wikisource.org/w/index.php?oldid=1748901
[967]: https://zh.wikisource.org/w/index.php?oldid=2124272
[969]: https://zh.wikisource.org/w/index.php?oldid=8746774
[970]: https://raw.githubusercontent.com/kanripo/KR2a0012/214fcafa79894355909c9d8c2c1533089e7791c6/KR2a0012_009.txt
[971]: https://raw.githubusercontent.com/kanripo/KR2a0012/214fcafa79894355909c9d8c2c1533089e7791c6/KR2a0012_009.txt
[973]: https://github.com/kanripo/KR2a0012/blob/214fcafa79894355909c9d8c2c1533089e7791c6/KR2a0012_010.txt
[982]: https://zh.wikisource.org/w/index.php?oldid=2610840
[985]: https://github.com/kanripo/KR2a0012/blob/214fcafa79894355909c9d8c2c1533089e7791c6/KR2a0012_019.txt
[988]: https://raw.githubusercontent.com/kanripo/KR2a0012/214fcafa79894355909c9d8c2c1533089e7791c6/KR2a0012_022.txt
[989]: https://raw.githubusercontent.com/kanripo/KR2a0012/214fcafa79894355909c9d8c2c1533089e7791c6/KR2a0012_022.txt
[992]: https://github.com/kanripo/KR2a0012/blob/214fcafa79894355909c9d8c2c1533089e7791c6/KR2a0012_027.txt
[994]: https://github.com/kanripo/KR2a0012/blob/214fcafa79894355909c9d8c2c1533089e7791c6/KR2a0012_028.txt
[1004]: https://zh.wikisource.org/w/index.php?oldid=2085142
[1005]: https://zh.wikisource.org/w/index.php?oldid=2085142
[1006]: https://zh.wikisource.org/w/index.php?oldid=2085142
[1011]: https://zh.wikisource.org/w/index.php?oldid=2075209
[1012]: https://zh.wikisource.org/w/index.php?oldid=2075209
[1016]: https://zh.wikisource.org/w/index.php?oldid=2085144
[1020]: https://zh.wikisource.org/w/index.php?oldid=2085144
[1022]: https://zh.wikisource.org/w/index.php?oldid=2085144
[1023]: https://zh.wikisource.org/w/index.php?oldid=2085144
[1027]: https://zh.wikisource.org/w/index.php?oldid=12758417
[1030]: https://zh.wikisource.org/w/index.php?oldid=12758417
[1031]: https://zh.wikisource.org/w/index.php?oldid=12758417
[1032]: https://zh.wikisource.org/w/index.php?oldid=12758417
[1033]: https://zh.wikisource.org/w/index.php?oldid=12758417
[1036]: https://zh.wikisource.org/w/index.php?oldid=12758417
[1037]: https://zh.wikisource.org/w/index.php?oldid=2085149
[1040]: https://zh.wikisource.org/w/index.php?oldid=2085149
[1041]: https://zh.wikisource.org/w/index.php?oldid=2085149
[1042]: https://zh.wikisource.org/w/index.php?oldid=2085149
[1044]: https://zh.wikisource.org/w/index.php?oldid=2085149
[1046]: https://zh.wikisource.org/w/index.php?oldid=2085149
[1047]: https://zh.wikisource.org/w/index.php?oldid=2085149
[1050]: https://zh.wikisource.org/w/index.php?oldid=2085149
[1051]: https://zh.wikisource.org/w/index.php?oldid=2085149
[1053]: https://zh.wikisource.org/w/index.php?oldid=2086397
[1059]: https://zh.wikisource.org/w/index.php?oldid=2086397
[1064]: https://zh.wikisource.org/w/index.php?oldid=2387393
[1065]: https://zh.wikisource.org/w/index.php?oldid=2387393
[1067]: https://zh.wikisource.org/w/index.php?oldid=2603286
[1068]: https://zh.wikisource.org/w/index.php?oldid=2603286
[1069]: https://zh.wikisource.org/w/index.php?oldid=2603286
[1072]: https://zh.wikisource.org/w/index.php?oldid=2603286
[1074]: https://zh.wikisource.org/w/index.php?oldid=2603286
[1075]: https://zh.wikisource.org/w/index.php?oldid=2603286
[1077]: https://zh.wikisource.org/w/index.php?oldid=2603286
[1079]: https://zh.wikisource.org/w/index.php?oldid=2603286
[1087]: https://zh.wikisource.org/w/index.php?oldid=12760859
[1089]: https://zh.wikisource.org/w/index.php?oldid=2638131
[1095]: https://zh.wikisource.org/w/index.php?oldid=2638131
[1096]: https://zh.wikisource.org/w/index.php?oldid=2638131
[1097]: https://zh.wikisource.org/w/index.php?oldid=2638131
[1100]: https://zh.wikisource.org/w/index.php?oldid=2131313
[1101]: https://zh.wikisource.org/w/index.php?oldid=2131313
[1106]: https://zh.wikisource.org/w/index.php?oldid=2085159
[1110]: https://zh.wikisource.org/w/index.php?oldid=2120830
[1115]: https://zh.wikisource.org/w/index.php?oldid=2120830
[1120]: https://zh.wikisource.org/w/index.php?oldid=2085162
[1127]: https://zh.wikisource.org/w/index.php?oldid=2188657
[1132]: https://zh.wikisource.org/w/index.php?oldid=2263487
[1133]: https://zh.wikisource.org/w/index.php?oldid=2263487
[1145]: https://zh.wikisource.org/w/index.php?title=史記/卷003&oldid=7909145
[1146]: https://zh.wikisource.org/w/index.php?title=史記/卷004&oldid=7909147
[1147]: https://zh.wikisource.org/w/index.php?title=史記/卷005&oldid=8744286
[1148]: https://zh.wikisource.org/w/index.php?title=史記/卷006&oldid=7907969
[1149]: https://zh.wikisource.org/w/index.php?title=史記/卷007&oldid=5978360
[1150]: https://zh.wikisource.org/w/index.php?title=史記/卷008&oldid=2440965
[1151]: https://zh.wikisource.org/w/index.php?title=史記/卷009&oldid=2087062
[1152]: https://zh.wikisource.org/w/index.php?title=史記/卷010&oldid=2599229
[1153]: https://zh.wikisource.org/w/index.php?title=史記/卷011&oldid=2520527
[1154]: https://zh.wikisource.org/w/index.php?title=史記/卷012&oldid=8733061
[1156]: https://zh.wikisource.org/w/index.php?title=史記/卷031&oldid=7909287
[1157]: https://zh.wikisource.org/w/index.php?title=史記/卷032&oldid=445042
[1158]: https://zh.wikisource.org/w/index.php?title=史記/魯周公世家&oldid=7909289
[1159]: https://zh.wikisource.org/w/index.php?title=史記/卷034&oldid=2559287
[1160]: https://zh.wikisource.org/w/index.php?title=史記/卷035&oldid=8737302
[1161]: https://zh.wikisource.org/w/index.php?title=史記/卷036&oldid=2588525
[1162]: https://zh.wikisource.org/w/index.php?title=史記/卷037&oldid=5977124
[1163]: https://zh.wikisource.org/w/index.php?title=史記/卷038&oldid=8737306
[1164]: https://zh.wikisource.org/w/index.php?title=史記/卷039&oldid=2588534
[1165]: https://zh.wikisource.org/w/index.php?title=史記/卷040&oldid=8736796
[1166]: https://zh.wikisource.org/w/index.php?title=史記/卷041&oldid=2018395
[1167]: https://zh.wikisource.org/w/index.php?title=史記/卷042&oldid=2016409
[1168]: https://zh.wikisource.org/w/index.php?title=史記/卷043&oldid=7903603
[1169]: https://zh.wikisource.org/w/index.php?title=史記/卷044&oldid=7903606
[1170]: https://zh.wikisource.org/w/index.php?title=史記/卷045&oldid=7903607
[1171]: https://zh.wikisource.org/w/index.php?title=史記/卷046&oldid=2560838
[1172]: https://zh.wikisource.org/w/index.php?title=史記/卷047&oldid=7903609
[1174]: https://zh.wikisource.org/w/index.php?title=史記/卷049&oldid=7903610
[1175]: https://zh.wikisource.org/w/index.php?title=史記/卷050&oldid=8737728
[1176]: https://zh.wikisource.org/w/index.php?title=史記/卷051&oldid=2380315
[1177]: https://zh.wikisource.org/w/index.php?title=史記/卷052&oldid=5977113
[1178]: https://zh.wikisource.org/w/index.php?title=史記/卷053&oldid=2087971
[1180]: https://zh.wikisource.org/w/index.php?title=史記/卷055&oldid=2666612
[1181]: https://zh.wikisource.org/w/index.php?title=史記/卷056&oldid=1961615
[1182]: https://zh.wikisource.org/w/index.php?title=史記/卷057&oldid=1569360
[1183]: https://zh.wikisource.org/w/index.php?title=史記/卷058&oldid=8735555
[1184]: https://zh.wikisource.org/w/index.php?title=史記/卷059&oldid=2621125
[1185]: https://zh.wikisource.org/w/index.php?title=史記/卷060&oldid=7909290
[1188]: https://zh.wikisource.org/w/index.php?title=史記/卷063&oldid=7903601
[1190]: https://zh.wikisource.org/w/index.php?title=史記/卷065&oldid=2567048
[1191]: https://zh.wikisource.org/w/index.php?title=史記/卷066&oldid=2621138
[1192]: https://zh.wikisource.org/w/index.php?title=史記/卷067&oldid=7869003
[1193]: https://zh.wikisource.org/w/index.php?title=史記/卷068&oldid=8764712
[1194]: https://zh.wikisource.org/w/index.php?title=史記/卷069&oldid=2621145
[1195]: https://zh.wikisource.org/w/index.php?title=史記/卷070&oldid=2621148
[1196]: https://zh.wikisource.org/w/index.php?title=史記/卷071&oldid=2621152
[1198]: https://zh.wikisource.org/w/index.php?title=史記/卷073&oldid=7909285
[1200]: https://zh.wikisource.org/w/index.php?title=史記/卷075&oldid=1965692
[1201]: https://zh.wikisource.org/w/index.php?title=史記/卷076&oldid=7909284
[1202]: https://zh.wikisource.org/w/index.php?title=史記/卷077&oldid=367917
[1203]: https://zh.wikisource.org/w/index.php?title=史記/卷078&oldid=2089016
[1204]: https://zh.wikisource.org/w/index.php?title=史記/卷079&oldid=2549307
[1209]: https://zh.wikisource.org/w/index.php?title=史記/卷084&oldid=1568305
[1213]: https://zh.wikisource.org/w/index.php?title=史記/卷088&oldid=1965690
[1216]: https://zh.wikisource.org/w/index.php?title=史記/卷091&oldid=2509940
[1218]: https://zh.wikisource.org/w/index.php?title=史記/卷093&oldid=368019
[1219]: https://zh.wikisource.org/w/index.php?title=史記/卷094&oldid=2171897
[1220]: https://zh.wikisource.org/w/index.php?title=史記/卷095&oldid=2298709
[1221]: https://zh.wikisource.org/w/index.php?title=史記/卷096&oldid=8770206
[1222]: https://zh.wikisource.org/w/index.php?title=史記/卷097&oldid=1383195
[1223]: https://zh.wikisource.org/w/index.php?title=史記/卷098&oldid=1490318
[1225]: https://zh.wikisource.org/w/index.php?title=史記/卷100&oldid=1965696
[1226]: https://zh.wikisource.org/w/index.php?title=史記/卷101&oldid=368092
[1227]: https://zh.wikisource.org/w/index.php?title=史記/卷102&oldid=1753957
[1229]: https://zh.wikisource.org/w/index.php?title=史記/卷104&oldid=8739534
[1230]: https://zh.wikisource.org/w/index.php?title=史記/卷105&oldid=8842726
[1231]: https://zh.wikisource.org/w/index.php?title=史記/卷106&oldid=405869
[1232]: https://zh.wikisource.org/w/index.php?title=史記/卷107&oldid=2540571
[1234]: https://zh.wikisource.org/w/index.php?title=史記/卷109&oldid=1765440
[1235]: https://zh.wikisource.org/w/index.php?title=史記/卷110&oldid=8735645
[1236]: https://zh.wikisource.org/w/index.php?title=史記/卷111&oldid=8730225
[1237]: https://zh.wikisource.org/w/index.php?title=史記/卷112&oldid=2089420
[1238]: https://zh.wikisource.org/w/index.php?title=史記/卷113&oldid=8735632
[1239]: https://zh.wikisource.org/w/index.php?title=史記/卷114&oldid=8735633
[1240]: https://zh.wikisource.org/w/index.php?title=史記/卷115&oldid=439220
[1243]: https://zh.wikisource.org/w/index.php?title=史記/卷118&oldid=7904122
[1244]: https://zh.wikisource.org/w/index.php?title=史記/卷119&oldid=7904123
[1245]: https://zh.wikisource.org/w/index.php?title=史記/卷120&oldid=9166127
[1246]: https://zh.wikisource.org/w/index.php?title=史記/卷121&oldid=8735621
[1247]: https://zh.wikisource.org/w/index.php?title=史記/卷122&oldid=7904124
[1248]: https://zh.wikisource.org/w/index.php?title=史記/卷123&oldid=8736799
[1249]: https://zh.wikisource.org/w/index.php?title=史記/卷124&oldid=367994
[1250]: https://zh.wikisource.org/w/index.php?title=史記/卷125&oldid=2273599
[1251]: https://zh.wikisource.org/w/index.php?title=史記/卷126&oldid=2609358
[1255]: https://zh.wikisource.org/w/index.php?title=史記/卷130&oldid=2609362
[1260]: https://zh.wikisource.org/w/index.php?oldid=2567459
[1264]: https://zh.wikisource.org/w/index.php?oldid=2567463
[1276]: https://zh.wikisource.org/w/index.php?oldid=2567462
[1277]: https://zh.wikisource.org/w/index.php?oldid=2567462
[1299]: https://zh.wikisource.org/w/index.php?oldid=1532655
[1327]: https://zh.wikisource.org/w/index.php?oldid=1500491
[1347]: https://zh.wikisource.org/w/index.php?oldid=2634831
[1350]: https://raw.githubusercontent.com/kanripo/KR2a0016/e80c057667e3c8684f11d5088251e10244d5a264/KR2a0016_041.txt
[1351]: https://zh.wikisource.org/w/index.php?oldid=2634831
[1352]: https://zh.wikisource.org/w/index.php?oldid=2634831
[1358]: https://commons.wikimedia.org/w/index.php?title=File:NLC892-411999017142-12779_%E4%BA%8C%E5%8D%81%E5%9B%9B%E5%8F%B2_%E7%AC%AC144%E5%86%8A.pdf&oldid=979637198
[1359]: https://zh.wikisource.org/w/index.php?title=%E5%AE%8B%E6%9B%B8/%E5%8D%B744&oldid=1746033
[1361]: https://zh.wikisource.org/w/index.php?oldid=2196532
[1363]: https://zh.wikisource.org/w/index.php?oldid=2118581
[1364]: https://raw.githubusercontent.com/kanripo/KR2a0016/e80c057667e3c8684f11d5088251e10244d5a264/KR2a0016_046.txt
[1375]: https://zh.wikisource.org/w/index.php?oldid=2118581
[1376]: https://zh.wikisource.org/w/index.php?oldid=2118581
[1377]: https://zh.wikisource.org/w/index.php?oldid=2118581
[1378]: https://zh.wikisource.org/w/index.php?oldid=2118581
[1379]: https://zh.wikisource.org/w/index.php?oldid=2118581
[1386]: https://raw.githubusercontent.com/kanripo/KR2a0016/e80c057667e3c8684f11d5088251e10244d5a264/KR2a0016_047.txt
[1387]: https://zh.wikisource.org/w/index.php?oldid=2190557
[1388]: https://zh.wikisource.org/w/index.php?oldid=2190557
[1391]: https://zh.wikisource.org/w/index.php?oldid=2190557
[1393]: https://zh.wikisource.org/w/index.php?oldid=2190557
[1398]: https://zh.wikisource.org/w/index.php?oldid=2190557
[1411]: https://zh.wikisource.org/w/index.php?oldid=1791560
[1413]: https://zh.wikisource.org/w/index.php?oldid=1791560
[1414]: https://zh.wikisource.org/w/index.php?oldid=1791560
[1415]: https://zh.wikisource.org/w/index.php?oldid=1791560
[1417]: https://zh.wikisource.org/w/index.php?oldid=1791560
[1418]: https://zh.wikisource.org/w/index.php?oldid=1791560
[1419]: https://zh.wikisource.org/w/index.php?oldid=1791560
[1420]: https://zh.wikisource.org/w/index.php?oldid=1791560
[1421]: https://zh.wikisource.org/w/index.php?oldid=1791560
[1422]: https://zh.wikisource.org/w/index.php?oldid=1791560
[1423]: https://zh.wikisource.org/w/index.php?oldid=1791560
[1426]: https://zh.wikisource.org/w/index.php?oldid=2118585
[1427]: https://zh.wikisource.org/w/index.php?oldid=2118585
[1428]: https://zh.wikisource.org/w/index.php?oldid=2118585
[1429]: https://zh.wikisource.org/w/index.php?oldid=2118585
[1430]: https://zh.wikisource.org/w/index.php?oldid=2118585
[1431]: https://zh.wikisource.org/w/index.php?oldid=2118585
[1432]: https://zh.wikisource.org/w/index.php?oldid=2118585
[1434]: https://zh.wikisource.org/w/index.php?oldid=2118585
[1435]: https://zh.wikisource.org/w/index.php?oldid=2118585
[1437]: https://zh.wikisource.org/w/index.php?oldid=2118585
[1438]: https://zh.wikisource.org/w/index.php?oldid=2118585
[1439]: https://zh.wikisource.org/w/index.php?oldid=2118585
[1440]: https://zh.wikisource.org/w/index.php?oldid=2118585
[1441]: https://zh.wikisource.org/w/index.php?oldid=2118585
[1442]: https://zh.wikisource.org/w/index.php?oldid=2118585
[1443]: https://zh.wikisource.org/w/index.php?oldid=2118585
[1444]: https://zh.wikisource.org/w/index.php?oldid=2118585
[1446]: https://zh.wikisource.org/w/index.php?oldid=2118585
[1448]: https://zh.wikisource.org/w/index.php?oldid=2371899
[1449]: https://zh.wikisource.org/w/index.php?oldid=2371899
[1450]: https://zh.wikisource.org/w/index.php?oldid=2371899
[1451]: https://zh.wikisource.org/w/index.php?oldid=2371899
[1452]: https://zh.wikisource.org/w/index.php?oldid=2371899
[1453]: https://zh.wikisource.org/w/index.php?oldid=2371899
[1455]: https://zh.wikisource.org/w/index.php?oldid=2371899
[1472]: https://zh.wikisource.org/w/index.php?oldid=2371899
[1473]: https://zh.wikisource.org/w/index.php?oldid=2371899
[1474]: https://zh.wikisource.org/w/index.php?oldid=2371899
[1475]: https://zh.wikisource.org/w/index.php?oldid=2371899
[1479]: https://zh.wikisource.org/w/index.php?oldid=2190655
[1480]: https://zh.wikisource.org/w/index.php?oldid=2190655
[1481]: https://zh.wikisource.org/w/index.php?oldid=2190655
[1482]: https://zh.wikisource.org/w/index.php?oldid=2190655
[1486]: https://zh.wikisource.org/w/index.php?title=宋書/卷52&oldid=2190655
[1494]: https://raw.githubusercontent.com/kanripo/KR2a0016/e80c057667e3c8684f11d5088251e10244d5a264/KR2a0016_059.txt
[1495]: https://zh.wikisource.org/w/index.php?title=宋書/卷60&oldid=1996694
[1496]: https://zh.wikisource.org/w/index.php?oldid=1996694
[1498]: https://zh.wikisource.org/w/index.php?title=%E5%AE%8B%E6%9B%B8/%E5%8D%B760&oldid=1996694
[1500]: https://github.com/kanripo/KR2a0016/blob/e80c057667e3c8684f11d5088251e10244d5a264/KR2a0016_062.txt
[1506]: https://zh.wikisource.org/w/index.php?title=%E5%AE%8B%E6%9B%B8%2F%E5%8D%B764&oldid=1748217
[1511]: https://raw.githubusercontent.com/kanripo/KR2a0016/e80c057667e3c8684f11d5088251e10244d5a264/KR2a0016_067.txt
[1512]: https://zh.wikisource.org/w/index.php?title=宋書/卷71&oldid=2485515
[1513]: https://commons.wikimedia.org/wiki/File:NLC892-411999017142-12246_二十四史_第148冊.pdf
[1514]: https://github.com/kanripo/KR2a0016/blob/e80c057667e3c8684f11d5088251e10244d5a264/KR2a0016_071.txt
[1516]: https://zh.wikisource.org/w/index.php?oldid=1997159
[1520]: https://zh.wikisource.org/w/index.php?title=宋書/卷75&oldid=1997722
[1521]: https://zh.wikisource.org/w/index.php?oldid=1997726
[1522]: https://zh.wikisource.org/w/index.php?oldid=1997726
[1525]: https://zh.wikisource.org/w/index.php?oldid=2069112
[1526]: https://zh.wikisource.org/w/index.php?oldid=2261200
[1527]: https://zh.wikisource.org/w/index.php?oldid=2261200
[1528]: https://commons.wikimedia.org/w/index.php?oldid=1229668893
[1529]: https://zh.wikisource.org/w/index.php?oldid=2261200
[1531]: https://zh.wikisource.org/w/index.php?title=宋書/卷80&oldid=2261200
[1533]: https://zh.wikisource.org/w/index.php?oldid=2069213
[1534]: https://zh.wikisource.org/w/index.php?oldid=2069213
[1544]: https://zh.wikisource.org/w/index.php?title=宋書/卷88&oldid=2069210
[1546]: https://zh.wikisource.org/w/index.php?title=宋書/卷88&oldid=2069210
[1549]: https://zh.wikisource.org/w/index.php?oldid=2195614
[1550]: https://zh.wikisource.org/w/index.php?oldid=2195614
[1551]: https://zh.wikisource.org/w/index.php?oldid=2195614
[1552]: https://zh.wikisource.org/w/index.php?oldid=2195614
[1554]: https://zh.wikisource.org/w/index.php?oldid=2195614
[1555]: https://zh.wikisource.org/w/index.php?oldid=2195614
[1557]: https://zh.wikisource.org/w/index.php?oldid=2195614
[1558]: https://zh.wikisource.org/w/index.php?oldid=2195614
[1569]: https://zh.wikisource.org/w/index.php?oldid=1962755
[1573]: https://zh.wikisource.org/w/index.php?title=%E5%AE%8B%E6%9B%B8%2F%E5%8D%B793&oldid=1962755
[1574]: https://zh.wikisource.org/w/index.php?oldid=2195835
[1575]: https://zh.wikisource.org/w/index.php?oldid=2638628
[1581]: https://zh.wikisource.org/w/index.php?oldid=11122985
[1582]: https://zh.wikisource.org/w/index.php?oldid=2180354
[1583]: https://zh.wikisource.org/w/index.php?oldid=582080
[1585]: https://zh.wikisource.org/w/index.php?oldid=2180374
[1587]: https://zh.wikisource.org/w/index.php?title=隋書/卷76&oldid=2616529
[1592]: https://zh.wikisource.org/w/index.php?oldid=2607174
[1598]: https://zh.wikisource.org/w/index.php?oldid=2587734
[1600]: https://zh.wikisource.org/w/index.php?oldid=2587825
[1608]: https://zh.wikisource.org/w/index.php?title=魏書/卷24&oldid=2021236
[1609]: https://raw.githubusercontent.com/kanripo/KR2a0020/17b6525eb5aaa878b9640f5a61e90da934ce5fc4/KR2a0020_024.txt
[1610]: https://zh.wikisource.org/w/index.php?oldid=2021236
[1611]: https://raw.githubusercontent.com/kanripo/KR2a0020/17b6525eb5aaa878b9640f5a61e90da934ce5fc4/KR2a0020_035.txt
[1613]: https://github.com/kanripo/KR2a0020/blob/17b6525eb5aaa878b9640f5a61e90da934ce5fc4/KR2a0020_038.txt
[1614]: https://zh.wikisource.org/w/index.php?oldid=1516111
[1615]: https://zh.wikisource.org/w/index.php?oldid=1516113
[1616]: https://zh.wikisource.org/w/index.php?oldid=2120299
[1618]: https://zh.wikisource.org/w/index.php?title=%E9%AD%8F%E6%9B%B8%2F%E5%8D%B758&oldid=2087998
[1619]: https://zh.wikisource.org/w/index.php?title=%E9%AD%8F%E6%9B%B8%2F%E5%8D%B758&oldid=2087998
[1620]: https://zh.wikisource.org/w/index.php?title=%E9%AD%8F%E6%9B%B8%2F%E5%8D%B758&oldid=2087998
[1622]: https://zh.wikisource.org/w/index.php?oldid=1513418
[1625]: https://zh.wikisource.org/w/index.php?title=魏書/卷67&oldid=468068
[1629]: https://zh.wikisource.org/w/index.php?oldid=760052
[1632]: https://commons.wikimedia.org/w/index.php?oldid=1130546999
[1633]: https://zh.wikisource.org/w/index.php?oldid=2004220
[1634]: https://commons.wikimedia.org/w/index.php?oldid=1130546999
[1643]: https://zh.wikisource.org/w/index.php?title=周書/卷48&oldid=2432546
[1658]: https://zh.wikisource.org/w/index.php?oldid=1497680
[1663]: https://zh.wikisource.org/w/index.php?oldid=803179
[1667]: https://zh.wikisource.org/w/index.php?oldid=803184
[1672]: https://zh.wikisource.org/w/index.php?oldid=2310031
[1673]: https://zh.wikisource.org/w/index.php?oldid=1960991
[1674]: https://zh.wikisource.org/w/index.php?oldid=2689999
[1677]: https://github.com/kanripo/KR1e0004/blob/685a6ddca22d98535cac38038afdff7308273d23/KR1e0004_030.txt#L776-L776
[1678]: https://zh.wikisource.org/w/index.php?title=史記/卷013&oldid=2606991
[1680]: https://zh.wikisource.org/w/index.php?title=史記/卷015&oldid=2607002
[1682]: https://zh.wikisource.org/w/index.php?title=史記/卷017&oldid=2607010
[1683]: https://zh.wikisource.org/w/index.php?title=史記/卷018&oldid=9484995
[1684]: https://zh.wikisource.org/w/index.php?title=史記/卷019&oldid=6359260
[1685]: https://zh.wikisource.org/w/index.php?title=史記/卷020&oldid=2607036
[1686]: https://zh.wikisource.org/w/index.php?title=史記/卷021&oldid=2607037
