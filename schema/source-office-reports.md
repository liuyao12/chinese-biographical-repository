# 來源官爵角色、批評資格、職掌與承嗣

`source_office_role` 保存完整本傳局部任職語法的角色/欄位位置，逐字重建當句；受任者綁傳首及句中明名，不用同段最近人名。轉任仍用既有`office_transfer_basis`，僅增「轉為」動詞；爵號改封支援「改封某為某爵」，前爵未名可空。所有任終未知，死年不填終年或追贈年。

`source_qualification.kind: reported_office_challenged_by_commentary` 限來源持稱`mode: attestation`。必有引書、批評段同一人物、作者與「本傳某不為某官未詳某所由知之」原句兩端，`preferred_historical_office_assertion_id: null`。不能變為實任授職或把古注批評抹去。此型不宣稱現代校勘已定。

`biographical_source_detail_set` 的`source_detail_pattern`分完整語法：任職後典選舉、具名總署行臺、詔某群體受某節度、前後累計增邑並賜子弟若干爵位。來源欄位各自精確位置，整句依字段順序重建，不能把另一個同字數詞當本欄。職掌不造官號；受節度的群體不變為本人官名。累計增邑保`aggregation: cumulative_across_unspecified_awards`，總額與實收留null，原單位尸不校戶。子弟保來源群體、各爵人數與空recipient_person_ids，不能全作親生子或造個體。

`noble_title_succession` 事件可用具名子嗣及無嗣弟紹封兩通用語法：前任、嗣者和重複引用依實際錨點驗證，`title`與`holding_id`均null。這是原文明載的承嗣事件，不是假定已知爵名的holding，也不改生父/收養/排行。具體爵名若日後據別處解析，須另存編輯判讀與其來源，不能把父親或諡號的字面用稱借作本人直接稱號錨。

同階段征西簡稱以既有人物標記作來源用稱，same_stage_holding_id連本次征西將軍持職；不是新任命或全域別名。jurisdictions保存并州、雍州、雍涼合稱與淮北原語，今地及地點ID均空。子弟欄biological_children_only=false表示此來源群體不能限定為親生子，並非斷言具體受封人的生物學構成。

## 官稱紀年與事件觀察

`source_office_date_binding` 為既有持職另加紀年證據，不新增官稱或覆寫原角色語法。驗證器先移除日期增量，重新檢查原 `source_office_role`，再依下列證據型別驗證新增日期。綁定保留本段指紋、固定來源修訂、受任者與先任者的逐字人物錨；不能只按同名或最近段落借年。

- `source_named_era_phase` 沿用 `civil_era_ranges`。年號「初」「中」保留原詞與完整年號範圍，不以「初」直接等同元年，也不選一個中間年份。
- `phase_and_in_office_upper` 分存原年號範圍 `era_phase_range` 及獨立同事件的在職上界。只有上下界共同夾定時，才另存數值始年；陳泰嘉平初原界為249–254，郭淮傳同年與雍州刺史陳泰降句安的記載另給249的上界。原範圍不因此消失。
- `dead_predecessor_successor` 同時檢查先任卒年、明文接任及同年已在職的平行事件。陳泰代郭淮的征西將軍、假節、都督雍涼各自保留原角色欄位，以完整帝紀與郭淮傳夾定255，沒有搬用郭淮卒日或填任終。
- `battle_in_office_observation` 只補 `attestations[].normalized_date`，不能新增 `effective_period.start`。陳泰敘事中的「後年」原字保留，255來自另一份同場戰役的明確紀年，不由「後年」算作前一年加一。

固定原始見證位於 `source-evidence/source-office-event-dates/primary/`，逐檔 SHA-256、固定修訂、全文投影、完整選錄範圍與字位錨可在本庫核對；這些外證並不表示其整卷已匯入原生正文。原生資料與所有編輯換算均保持 `human_reviewed: false`，未核書影。

職掌的 `date_observation.kind: source_duty_event_observation_window` 與持職年界分開。其 `duration: false`、`tenure_boundary: false` 必須保留；`earliest`、`latest` 只界定此職掌在同一敘事事件中出現的時間範圍。陳泰「總署行臺」見於257–258年平叛事件，不等於已證其兩年任期，也不把此年借給另一場孫峻出淮泗時的鎮軍、假節、督淮北三職。人物頁顯示這項限定，機讀包保留證據及精度，來源不明者仍留空。

## 具名子列、兄弟任官與本紀死亡外證

`source_family_office_frame` 目前支援具名五子授列侯、三名弟弟分列任官兩種完整句式。名單的每一人物與所屬官爵欄位均有字位，省略「為」不表示把下一官職借給上一人；名單順序不作出生排行。具名五子可各自保存授爵，但匿名群體的人數不能反造具名持爵者。`preceding_named_death` 明記本次授子爵在其父死亡之後，不等於子本人獲身後爵，也不因此指定授爵年。

`source_family_duty_frame` 使「侍講」等本句職掌連到實際官稱。`independent_substantive_office: false` 表示沒有把這個職掌另造為實官。明示「某弟某」的 `source_clause_binding` 另保兩端人物及原詞，只加 `relative_birth_order` 的長幼不等式，不補兩人的絕對序數。

`named_annal_biographical_death` 只換算已存在的傳記死亡記載。本傳傳首、死亡短稱與同版帝紀的全名死亡事件須可共同核對；固定原始檔、前一年至本年完整連續單元、年號首見及正文／古注層界逐項保留。外證的月日仍留引文，數值僅年精度；沒有把本紀日期冒作本傳原載，也不從病中返回某地推出死亡地，或把死亡年轉成所有持職的任終。此型目前以《三國志》固定 Kanripo 見證驗證，不宣稱能解析任意年表或所有曆制。

## 逐句職歷角色框架

`source_career_role` 為有限、已閱讀的完整職歷句式：固定語法中的人物角色及官稱、共享尾字、數詞、年月欄位逐字重建，綁定段落SHA、固定修訂與當前人物提及。正文的省略主語另與傳首同指核對；古注附傳使用該句明名主語。不可把同段他人官名借給主傳人物。`mode: attestation` 的「並至」只記來源報告；追贈、再任及行職各錄，不把亡年作任終。

梁譙、安平廣平共享「太守」以 `shared_title_suffix` 保存兩個來源錨；展開稱號是編輯顯示，沒有改動正文或推成同時兼任。`office_duration` 保「在職三年」數值3及關聯的侍中持職，反算始年與任終均空。`unnamed_family_title_grants` 的一子高亭侯保人數1且具名受封人列表空；`fief_household_count` 的二十三百戸保2300及原單位戸，不推實收。

`source_career_role` 亦供未赴任記錄：散騎與中書侍郎是收到二稱，均 `effective_service_attested: false`，不把元帝之初換為精確任年。離官細節分 illness/dismissal/disability 等來源結果，僅連明確同序的前職；未知職名者不填，不宣稱一切職爵同時終止。地方任官不是籍貫。
