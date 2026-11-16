# 固定完整見證的角色綁定親屬與家族報告

沿 `fixed_witness_person_fact_slots`：完整固定raw/revision/獨立source投影、全段每一人物位置與同指組、語義槽逐值校驗，不能只因某人同段出現即移給其另一人物。native逐assertion明驗，runtime既有全槽guard拒漏行、重行與去binding。有限可信JSON recipe是已覆核的解讀，不是任意來源程式或一般古文NLU。

一般father/mother/spouse/sibling/grandfather保現有方向；brother的主體是客體的兄弟。前母保存maternal_role prior_mother，不生母/繼母。蔡氏生母是前母明生發、祜同母兄承與031/034母系來源對讀的有資格首選；照養發另raised_by。明長子倫序1，其他弟只相對小於，不造2/3/4或父名。宗祀ritual_successor_of不等法定收養；暨/伊拒命用source detail proposal_status not_accepted，不寫已承嗣。

`kinship_unspecified` 的有限分支 `fixed_received_collateral_appellation` 保原稱、客體相對主體的世代差（負數為客體早代）、父/母系或未明路徑、unknown connecting_person_ids與exact_distance。從甥/甥不可直接補中間母或斷血緣；舅子保存母系同代稱用資格。

「祜兄玄孫之子法興」以法興→祜代差-5、玄孫4＋之子1、unnamed_ancestor_role older_brother(reference=祜,person_id=null)機讀保存。兄是誰及中間各代未知，不選發/承，不把祜當直祖；父系共根只是收到族系語境的provisional解讀，不擴遠祖。

來源家族報告將「退告諸子」「家無胤嗣」「位至公而無子」分敘述範圍，individual_count=null，不寫全局子女零值。九世世官只報家世代數9，不造九名祖先或個別官職。女夫為一具體未名婿、father_in_law指岳父，spouse/child_person_id未知不創女兒身份。

所有原有來源模型與native hooks保留；此分支僅嚴格通過完整有限見證role recipe才接受，不能以人物ID白名單略過來源角色。
