# coding: utf-8
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

class TianDanIdentityTests(unittest.TestCase):
    def paragraph(self, number, index):
        return json.loads((ROOT / f'corpus/shiji/{number}.json').read_text())['paragraphs'][index-1]

    def ids(self, paragraph, surface):
        return {m['person_id'] for m in paragraph['mentions'] if m['surface']==surface}

    def test_qi_campaign_and_short_forms_link_to_same_people(self):
        p=self.paragraph('094',9)
        for surface,pid in [('韓信','ofc_8ei_jb7'),('酈生','eya_qj3_tev'),('曹參','37j_16p_7n8'),('灌嬰','sj9_pfu_fwh'),('嬰','sj9_pfu_fwh')]:
            self.assertEqual(self.ids(p,surface),{pid})
        self.assertEqual(self.ids(self.paragraph('094',13),'淮陰'),{'ofc_8ei_jb7'})
        self.assertEqual(self.ids(self.paragraph('094',14),'酈生'),{'eya_qj3_tev'})
        self.assertEqual(self.ids(self.paragraph('093',3),'韓王信'),{'l9e_fbr_36a_*A'})
        self.assertIn('酈生言其弟酈商',self.paragraph('097',4)['text'])

    def test_implicit_subject_context_does_not_invent_name_anchor(self):
        p=self.paragraph('095',25)
        self.assertNotIn('灌嬰',p['text'])
        self.assertFalse(any(m.get('person_id')=='sj9_pfu_fwh' for m in p['mentions']))
        rows=json.loads((ROOT/'corpus/shiji/094-equivalences.json').read_text())['decisions']
        decision=next(d for d in rows if d['id']=='eq-shiji094-qi-campaign-guanying')
        context=decision['references'][0]
        self.assertEqual(context['paragraph_id'],p['id'])
        self.assertEqual(context['quote'],p['text'])
        self.assertIn('得齊守相田光',context['quote'])
        self.assertIn('漢將灌嬰追得齊守相田光',self.paragraph('094',9)['text'])
        self.assertIn('得故齊王田廣相田光',self.paragraph('054',5)['text'])
        self.assertIn('嬰遷為御史大夫',self.paragraph('095',24)['text'])

    def test_qi_campaign_candidate_files_retired(self):
        people={p['id'] for p in json.loads((ROOT/'registry/persons.json').read_text())['persons']}
        for pid in ('lp3_npi_io0','uj5_nzw_pnc','349_zmu_2u4','1wk_2dd_421'):
            self.assertNotIn(pid,people)
            self.assertFalse((ROOT/f'exports/persons/{pid}.json').exists())
            self.assertFalse((ROOT/f'data/corpus/profiles/{pid}.json').exists())

    def test_opening_people_and_two_huai_kings_stay_distinct(self):
        self.assertEqual(self.ids(self.paragraph('094',2),'陳涉'),{'pom_ycp_ha5'})
        self.assertEqual(self.ids(self.paragraph('094',2),'周市'),{'i8y_6lu_30h'})
        self.assertEqual(self.ids(self.paragraph('094',3),'魏王'),{'kez_re1_kcr'})
        self.assertEqual(self.ids(self.paragraph('094',3),'魏王咎'),{'kez_re1_kcr'})
        self.assertEqual(self.ids(self.paragraph('094',4),'項梁'),{'5xt_rg8_7zs_A'})
        self.assertEqual(self.ids(self.paragraph('094',5),'楚懷王'),{'c2w_s7g_en0_*A'})
        p=self.paragraph('007',6)
        self.assertIn('自懷王入秦不反',p['text'])
        self.assertIn('求楚懷王孫心',p['text'])
        self.assertEqual(self.ids(p,'懷王'),{'c2w_s7g_en0','c2w_s7g_en0_*A'})

    def test_tian_jian_xian_keeps_literal_characters_and_refusal_attribution(self):
        self.assertEqual(self.ids(self.paragraph('094',3),'田間'),{'27q_nw7_jv8'})
        self.assertEqual(self.ids(self.paragraph('094',4),'田閒'),{'27q_nw7_jv8'})
        self.assertIn('楚懷王曰：「田假與國之王',self.paragraph('094',5)['text'])
        self.assertIn('項梁曰：「田假為與國之王',self.paragraph('007',7)['text'])

    def test_opening_candidate_files_retired(self):
        people={p['id'] for p in json.loads((ROOT/'registry/persons.json').read_text())['persons']}
        for pid in ('qy6_7i9_tgb','8ht_nw8_3lv','is3_9h6_hq6','5dl_6xj_187','okz_ham_pdc','8h7_82d_vjr','ld0_ysw_559','dgh_7wa_4c5'):
            self.assertNotIn(pid,people)
            self.assertFalse((ROOT/f'exports/persons/{pid}.json').exists())
            self.assertFalse((ROOT/f'data/corpus/profiles/{pid}.json').exists())

    def test_remaining_campaign_people_use_each_shared_event(self):
        p=self.paragraph('094',9)
        for surface,pid in [('龍且','sr6_5zr_1f3'),('彭越','9qt_orl_5f2'),('華無傷','bbt_vs5_5ka'),('田解','sac_peq_v1p'),('田光','pew_ob7_n0k'),('田既','o4h_qq4_taj'),('田吸','kfh_9sk_v4e')]:
            self.assertEqual(self.ids(p,surface),{pid})
        self.assertEqual(self.ids(self.paragraph('094',7),'陳餘'),{'rx0_vif_1xq'})
        self.assertEqual(self.ids(self.paragraph('094',10),'酈商'),{'xny_prn_zyi'})
        self.assertEqual(self.ids(self.paragraph('054',5),'田廣'),{'0hs_fg6_1qj_B'})
        self.assertEqual(self.ids(self.paragraph('095',25),'華毋傷'),{'bbt_vs5_5ka'})

    def test_qi_minister_is_not_yan_assassin_and_tian_guang_keeps_father(self):
        all_mentions=[m for p in json.loads((ROOT/'corpus/shiji/086.json').read_text())['paragraphs'] for m in p['mentions']]
        self.assertTrue(any(m.get('person_id')=='z0v_ish_b9u' and m['surface']=='田光' for m in all_mentions))
        self.assertFalse(any(m.get('person_id')=='pew_ob7_n0k' for m in all_mentions))
        people={p['id']:p for p in json.loads((ROOT/'registry/persons.json').read_text())['persons']}
        self.assertEqual(people['0hs_fg6_1qj_B']['family_path']['parent_person_id'],'0hs_fg6_1qj')
        self.assertIn('立田榮子廣為齊王',self.paragraph('094',8)['text'])

    def test_remaining_campaign_candidate_files_retired(self):
        people={p['id'] for p in json.loads((ROOT/'registry/persons.json').read_text())['persons']}
        for pid in ('ueq_svp_knr','y6z_6wd_ezf','qfk_7zb_jtn','zip_jr2_0be','27w_87k_66k','ecl_t01_cwr','14d_o9y_nd0','6mp_d5b_nax','hr1_cou_3hm','nnz_8gm_bdk','dnb_rcf_15u','k96_xfs_8qz','ybx_5gn_njg'):
            self.assertNotIn(pid,people)
            self.assertFalse((ROOT/f'exports/persons/{pid}.json').exists())
            self.assertFalse((ROOT/f'data/corpus/profiles/{pid}.json').exists())

    def test_death_reports_exclude_intentions_and_preserve_heard_death(self):
        rows=json.loads((ROOT/'corpus/shiji/094-life-events.json').read_text())['events']
        self.assertEqual(len(rows),12)
        self.assertTrue(all(e['event_type']=='death' for e in rows))
        self.assertFalse(any(e['person_id'] in {'5q3_f2w_w1e','ob7_g6i_7pp'} for e in rows))
        heard=next(e for e in rows if e['person_id']=='0hs_fg6_1qj_B')
        self.assertEqual(heard['source_term'],'橫聞齊王死')
        self.assertIn('死亡消息',heard['interpretation_note'])
        self.assertNotIn('normalized_date',heard)
        self.assertNotIn('normalized_date',next(e for e in rows if e['person_id']=='6r7_9o6_c1i'))

    def test_death_years_use_calendar_month_not_regnal_month_sequence(self):
        rows=json.loads((ROOT/'corpus/shiji/094-life-events.json').read_text())['events']
        expected={'u87_cc1_7vm':208,'u87_cc1_7vm_A':206,'vtu_yuj_kdz_*A':206,'0hs_fg6_1qj':205}
        for pid,year in expected.items():
            e=next(e for e in rows if e['person_id']==pid);d=e['normalized_date']
            self.assertIsNone(e['date_expression'])
            self.assertEqual(d['era_year'],year)
            self.assertEqual(d['year'],1-year)
            self.assertEqual(d['basis']['kind'],'parallel_event')
        shi=next(e for e in rows if e['person_id']=='u87_cc1_7vm_A')['normalized_date']
        self.assertTrue(any(r['quote']=='二十四。田榮擊殺市。' for r in shi['references']))
        self.assertTrue(any(r['quote']=='六月' and r['scope']=='received_calendar_month_attestation' for r in shi['references']))
        an=next(e for e in rows if e['person_id']=='vtu_yuj_kdz_*A')['normalized_date']
        self.assertTrue(any(r['quote']=='六。田榮擊殺安。' for r in an['references']))
        self.assertTrue(any(r['quote']=='七月' and r['scope']=='received_calendar_month_attestation' for r in an['references']))

    def test_death_places_are_not_birth_or_burial_places(self):
        rows=json.loads((ROOT/'corpus/shiji/094-addresses.json').read_text())['assertions']
        heng=[a for a in rows if a['person_id']=='6r7_9o6_c1i']
        self.assertEqual({(a['relation'],a['place']['source_name']) for a in heng},{('death_place','尸鄉廄置'),('residence','島中')})
        self.assertFalse(any(a['relation'] in {'birth_place','burial_place'} for a in rows))
        self.assertTrue(all(a['place']['modern_identification'] is None for a in rows))
        self.assertTrue(any(a['person_id']=='u87_cc1_7vm_A' and a['place']['source_name']=='即墨' for a in rows))
        self.assertTrue(any(a['person_id']=='0hs_fg6_1qj' and a['place']['source_name']=='平原' for a in rows))

    def test_royal_grant_years_keep_original_titles_and_unknown_death_end(self):
        rows={h['id']:h for h in json.loads((ROOT/'corpus/shiji/094-titles.json').read_text())['holdings']}
        for hid,year in [('002',209),('008',208),('011',206),('013',206),('014',206),('016',206),('017',205)]:
            b=rows['th-shiji094-'+hid]['effective_period']['start']
            self.assertIsNone(b['date_expression'])
            self.assertEqual(b['normalized_date']['era_year'],year)
            self.assertEqual(b['normalized_date']['basis']['kind'],'parallel_event')
        shi=rows['th-shiji094-008']
        self.assertEqual(shi['effective_period']['end']['event_type'],'deposition')
        self.assertEqual(shi['effective_period']['end']['normalized_date']['era_year'],206)
        jiaodong=rows['th-shiji094-011']
        self.assertEqual(jiaodong['title'],'王')
        self.assertEqual([x['source_name'] for x in jiaodong['jurisdictions']],['膠東'])
        self.assertEqual(jiaodong['effective_period']['end']['status'],'unknown')

    def test_tian_rong_grant_preserves_different_event_order(self):
        rows=json.loads((ROOT/'corpus/shiji/094-titles.json').read_text())['holdings']
        h=next(h for h in rows if h['id']=='th-shiji094-016')
        date=h['effective_period']['start']['normalized_date']
        self.assertIn('本傳先殺田安而後自立',date['rationale'])
        self.assertIn('六月田榮始、七月殺安',date['rationale'])
        self.assertTrue(any(r['quote']=='六月' for r in date['references']))
        p=self.paragraph('094',7)['text']
        self.assertLess(p.index('還攻殺濟北王安'),p.index('於是田榮乃自立為齊王'))

    def test_month_table_short_names_identify_victims_and_family(self):
        x=json.loads((ROOT/'data/historical-tables/shiji-016.json').read_text())
        cells={c['id']:c for f in x['fragments'] for r in f['rows'] for c in r['cells']}
        for cid,surface,pid in [('shiji-016-t2-r006-c10','市','u87_cc1_7vm_A'),('shiji-016-t2-r007-c09','安','vtu_yuj_kdz_*A'),('shiji-016-t2-r013-c08','項籍','ob7_g6i_7pp'),('shiji-016-t2-r013-c08','榮','0hs_fg6_1qj'),('shiji-016-t1-r003-c05','橫','6r7_9o6_c1i')]:
            self.assertTrue(any(m['surface']==surface and m['person_id']==pid for m in cells[cid]['person_mentions']))
        self.assertEqual(cells['shiji-016-t2-r006-c10']['text'],'二十四。田榮擊殺市。')
        self.assertEqual(cells['shiji-016-t2-r007-c09']['text'],'六。田榮擊殺安。')

    def test_tian_xian_parallel_reading_keeps_received_surface(self):
        c=json.loads((ROOT/'corpus/shiji/094.json').read_text())
        v=next(v for v in c['annotation']['reported_variants'] if v['id']=='rv-shiji094-tianxian')
        self.assertEqual(v['received_reading'],'田間')
        self.assertEqual(v['reported_reading'],'田閒')
        self.assertEqual(v['person_ids'],['27q_nw7_jv8'])
        self.assertFalse(v['adopted']);self.assertFalse(v['image_verified'])
        self.assertIn('田間為將',self.paragraph('094',3)['text'])

    def test_unresolved_commentary_year_does_not_override_table_year(self):
        rows=json.loads((ROOT/'corpus/shiji/094-life-events.json').read_text())['events']
        d=next(e for e in rows if e['person_id']=='0hs_fg6_1qj')['normalized_date']
        self.assertEqual(d['era_year'],205)
        ref=next(r for r in d['references'] if r['scope']=='commentary_chronology_unresolved_not_adopted')
        self.assertEqual(ref['quote'],'三年正月。')
        self.assertEqual(ref['revision_id'],2514764)
        self.assertIn('所屬紀年尚待核定',d['rationale'])

    def test_parent_and_son_names_are_separate_without_replacing_child_anchor(self):
        for index,mid,parent_name,parent_id,child_name,child_id in [(4,'c-shiji-094-tiandan:m004-0096','田儋','u87_cc1_7vm','市','u87_cc1_7vm_A'),(8,'c-shiji-094-tiandan:m008-0128','田榮','0hs_fg6_1qj','廣','0hs_fg6_1qj_B')]:
            p=self.paragraph('094',index);child=next(m for m in p['mentions'] if m['id']==mid);parent=next(m for m in p['mentions'] if m['id']==mid+'-parent')
            self.assertEqual((child['surface'],child['person_id']),(child_name,child_id))
            self.assertEqual((parent['surface'],parent['person_id']),(parent_name,parent_id))
            self.assertEqual(p['text'][parent['end']:child['start']],'子')
            self.assertIn(parent_name+'子'+child_name,p['text'])

    def test_kinship_phrase_is_evidence_but_not_a_sons_name(self):
        people={p['id']:p for p in json.loads((ROOT/'registry/persons.json').read_text())['persons']}
        for pid,phrase,short in [('u87_cc1_7vm_A','田儋子市','市'),('0hs_fg6_1qj_B','田榮子廣','廣')]:
            self.assertNotIn(phrase,[a['surface'] for a in people[pid]['aliases']])
            self.assertIn(short,[a['surface'] for a in people[pid]['aliases']])
        rows=json.loads((ROOT/'corpus/shiji/094-assertions.json').read_text())['assertions']
        self.assertTrue(any(a['subject_person_id']=='0hs_fg6_1qj_B' and a['object_person_id']=='0hs_fg6_1qj' and a['predicate']=='father' for a in rows))

    def test_adjacent_qi_kings_follow_the_subject_change(self):
        p=self.paragraph('094',9);marks={m['start']:m for m in p['mentions']}
        for start,pid in [(172,'0hs_fg6_1qj_B'),(218,'0hs_fg6_1qj_B'),(225,'6r7_9o6_c1i')]:
            self.assertEqual((marks[start]['surface'],marks[start]['person_id']),('齊王',pid))
        self.assertIn('橫聞齊王死，自立為齊王',p['text'])

    def test_emperor_address_is_scoped_usage_not_a_new_grant(self):
        p=self.paragraph('094',11)
        self.assertEqual(self.ids(p,'天子'),{'yqp_nlb_p1p_A'})
        self.assertEqual(self.ids(p,'陛下'),{'yqp_nlb_p1p_A'})
        self.assertEqual(self.ids(self.paragraph('094',10),'皇帝'),{'yqp_nlb_p1p_A'})
        rows=json.loads((ROOT/'corpus/shiji/094-titles.json').read_text())['holdings']
        for title in ['天子','陛下']:
            h=next(h for h in rows if h['title']==title)
            self.assertEqual(h['mode'],'attestation')
            self.assertEqual(h['effective_period']['start']['status'],'unknown')
            self.assertEqual(h['effective_period']['end']['status'],'unknown')
