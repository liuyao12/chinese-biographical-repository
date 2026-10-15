# coding: utf-8
import json
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def read(p):return json.loads((ROOT/p).read_text())
def para(n,i):return next(p for p in read(f'corpus/shiji/{n:03}.json')['paragraphs'] if p['id'].endswith(f':p{i:03}'))
def ids(p,s):return {m['person_id'] for m in p['mentions'] if m['surface']==s and m['kind']=='person'}

class ZhangOpeningIdentityTests(unittest.TestCase):
    def test_opening_campaigns_reconcile_people_not_events(self):
        p=para(96,1)
        for surface,pid in [('淮陰侯','ofc_8ei_jb7'),('陳餘','rx0_vif_1xq'),('張耳','agx_sqm_4ou'),('耳','agx_sqm_4ou'),('趙王敖','agx_sqm_4ou_A'),('臧荼','xaa_ewn_4ro')]:
            self.assertEqual(ids(p,surface),{pid})
        self.assertIn('蒼得陳餘',p['text'])
        self.assertIn('斬陳餘泜水上',para(89,23)['text'])
        self.assertIn('斬成安君泜水上',para(92,10)['text'])

    def test_retrospective_huaiyin_title_has_no_campaign_grant_date(self):
        h=next(x for x in read('corpus/shiji/096-titles.json')['holdings'] if x['id']=='th-shiji096-105')
        self.assertEqual((h['person_id'],h['mode']),('ofc_8ei_jb7','attestation'))
        self.assertEqual(h['effective_period']['start']['status'],'unknown')
        self.assertIsNone(h['effective_period']['start']['date_expression'])
        self.assertIn('以爲淮陰侯',para(92,23)['text'])
        self.assertEqual(ids(para(95,20),'韓信'),{'l9e_fbr_36a_*A'})

    def test_xiao_cao_short_forms_follow_han_court_context(self):
        self.assertEqual(ids(para(96,2),'蕭何'),{'xd8_uww_5ok'})
        for i in [4,5,20]:
            self.assertEqual(ids(para(96,i),'蕭'),{'xd8_uww_5ok'})
            self.assertEqual(ids(para(96,i),'曹'),{'37j_16p_7n8'})
        self.assertEqual(ids(para(96,10),'曹窋'),{'37j_16p_7n8_A'})
        self.assertEqual(ids(para(96,23),'陳平'),{'rwg_skp_gbq'})

    def test_zhangao_inherits_evidenced_father_and_not_liuchang_paternity(self):
        self.assertEqual(ids(para(118,1),'趙王張敖'),{'agx_sqm_4ou_A'})
        bundle=read('exports/persons/agx_sqm_4ou_A.json')
        fathers=[a for a in bundle['relations'] if a['subject_person_id']=='agx_sqm_4ou_A' and a['predicate']=='father']
        self.assertTrue(any(a['object_person_id']=='agx_sqm_4ou' and any('子敖嗣立' in e['quote'] for e in a['evidence']) for a in fathers))
        self.assertFalse(any(a['predicate']=='father' and a['subject_person_id']=='yqp_nlb_p1p_AF' and a['object_person_id']=='agx_sqm_4ou_A' for a in bundle['relations']))

    def test_huainan_successor_is_not_predecessor_or_unnamed_father(self):
        p=para(96,2)
        self.assertEqual(ids(p,'黥布'),{'zxd_afr_2xg'})
        self.assertEqual(ids(p,'皇子長'),{'yqp_nlb_p1p_AF'})
        self.assertEqual(ids(para(118,2),'淮南王黥布'),{'zxd_afr_2xg'})
        a=read('corpus/shiji/096-assertions.json')['assertions']
        father=next(x for x in a if x['subject_person_id']=='796_nkw_0jz_A' and x['predicate']=='father')
        self.assertEqual(father['object_person_id'],'796_nkw_0jz')
        self.assertNotEqual(father['object_person_id'],'5do_703_rfz')

    def test_twelve_retired_candidates_have_no_registry_or_export(self):
        people={x['id'] for x in read('registry/persons.json')['persons']}
        for old in ['r6y_t2l_ntc','65r_40m_v04','shk_1za_du3','41m_4yl_j39','zs9_uq9_odj','kzp_s69_eh7','15d_u8k_luo','9dx_y3b_try','ifc_1dx_zrh','e4c_pkg_cq7','7o5_xwk_v9c','z0c_6ka_3bd']:
            self.assertNotIn(old,people)
            self.assertFalse((ROOT/f'exports/persons/{old}.json').exists())
            self.assertFalse((ROOT/f'data/corpus/profiles/{old}.json').exists())

class ZhangCourtIdentityTests(unittest.TestCase):
    def test_attempted_prince_change_does_not_make_ruyi_crown_prince(self):
        p=para(96,5)
        self.assertEqual(ids(p,'太子'),{'yqp_nlb_p1p_AA'})
        self.assertEqual(ids(p,'如意'),{'yqp_nlb_p1p_AH'})
        self.assertEqual(ids(para(96,16),'孝惠'),{'yqp_nlb_p1p_AA'})
        self.assertEqual(ids(para(54,15),'惠帝'),{'yqp_nlb_p1p_AA'})
        self.assertIn('而立戚姬子如意為太子',p['text'])
        holdings=read('corpus/shiji/096-titles.json')['holdings']
        self.assertFalse(any(h['person_id']=='yqp_nlb_p1p_AH' and h['title']=='太子' for h in holdings))

    def test_family_and_mother_references_follow_distinct_people(self):
        self.assertEqual(ids(para(96,5),'戚姬'),{'thg_zvp_v5y'})
        self.assertEqual(ids(para(96,6),'戚夫人'),{'thg_zvp_v5y'})
        self.assertEqual(ids(para(96,8),'戚氏'),{'thg_zvp_v5y'})
        self.assertEqual(ids(para(96,8),'高后'),{'i30_mjq_6q8_A'})
        b=read('exports/persons/yqp_nlb_p1p_AH.json')
        self.assertTrue(any(a['subject_person_id']=='yqp_nlb_p1p_AH' and a['predicate']=='mother' and a['object_person_id']=='thg_zvp_v5y' for a in b['relations']))

    def test_new_king_and_xiangji_mentions_have_exact_boundaries(self):
        for i,start,surface,pid in [(8,18,'王','yqp_nlb_p1p_AH'),(10,para(96,10)['text'].index('項籍'),'項籍','ob7_g6i_7pp')]:
            p=para(96,i);m=next(m for m in p['mentions'] if m['start']==start)
            self.assertEqual((m['surface'],m['end'],m['person_id']),(surface,start+len(surface),pid))
            self.assertEqual(p['text'][m['start']:m['end']],surface)
        self.assertIn('周昌令王稱疾不行',para(96,8)['text'])

    def test_court_officers_and_same_name_clerk_remain_distinct(self):
        self.assertEqual(ids(para(96,5),'留侯'),{'ea5_zvr_hlp'})
        self.assertEqual(ids(para(96,7),'陳豨'),{'1xx_s1v_svn'})
        self.assertEqual(ids(para(96,11),'絳侯'),{'koy_6jg_gcc'})
        self.assertEqual(ids(para(96,20),'陳平'),{'i3f_9l9_g53'})
        self.assertEqual(ids(para(96,23),'陳平'),{'rwg_skp_gbq'})
        self.assertEqual(ids(para(96,10),'曹窋'),{'37j_16p_7n8_A'})
        self.assertEqual(ids(para(9,27),'平陽侯窋'),{'37j_16p_7n8_A'})
        self.assertEqual(ids(para(57,8),'呂祿'),{'561_608_i0z'})

    def test_current_emperor_scope_does_not_override_later_emperors(self):
        self.assertEqual(ids(para(96,19),'今上'),{'yqp_nlb_p1p_ACAA'})
        self.assertEqual(ids(para(96,21),'孝武'),{'yqp_nlb_p1p_ACAA'})
        self.assertNotIn('yqp_nlb_p1p_ACAA',ids(para(96,24),'孝宣帝'))
        self.assertNotIn('yqp_nlb_p1p_ACAA',ids(para(96,27),'孝元帝'))

    def test_sixteen_court_candidates_are_retired(self):
        people={p['id'] for p in read('registry/persons.json')['persons']}
        for pid in ['t5e_f83_p7l','srh_4ts_334','5f6_5r4_eni','9t0_psw_zf3','6a5_ca8_2a8','7p1_uko_gaz','xg3_url_fyn','jej_8s3_01z','ht8_t4d_vbc','pdd_ww5_imn','yzr_p69_1y0','pyt_ft7_8h4','865_tu4_a4b','9ul_wlf_q1k','vz1_n5y_mng','rhz_4fw_u1u']:
            self.assertNotIn(pid,people)
            self.assertFalse((ROOT/f'exports/persons/{pid}.json').exists())
            self.assertFalse((ROOT/f'data/corpus/profiles/{pid}.json').exists())

    def test_unenacted_title_is_exported_separately_from_actual_holdings(self):
        c=read('corpus/shiji/096.json');p=para(96,5)
        m=next(m for m in p['mentions'] if m['id']=='c-shiji-096-zhang:m005-0102')
        self.assertEqual((m['surface'],m['kind'],m['person_id']),('太子','unresolved',None))
        proposal=c['annotation']['title_proposals'][0]
        b=read('exports/persons/yqp_nlb_p1p_AH.json')
        self.assertIn(proposal,b['title_proposals'])
        self.assertEqual((proposal['person_id'],proposal['outcome']),('yqp_nlb_p1p_AH','not_enacted'))
        hui=read('exports/persons/yqp_nlb_p1p_AA.json')
        self.assertNotIn(m['id'],{x['id'] for x in hui['mentions']})
        from scripts.validate_corpus import title_proposal_errors
        self.assertEqual(title_proposal_errors(proposal,c,{'yqp_nlb_p1p_AH'}),[])

    def test_title_proposal_rejects_wrong_holder_person_role_and_missing_quote_anchor(self):
        import copy
        from scripts.validate_corpus import title_proposal_errors
        c=read('corpus/shiji/096.json');proposal=c['annotation']['title_proposals'][0]
        for changes in [{'person_id':'yqp_nlb_p1p_AA'}, {'outcome':'enacted'}, {'role_mention_id':'c-shiji-096-zhang:m005-0091'}]:
            broken=dict(proposal,**changes)
            self.assertTrue(title_proposal_errors(broken,c,{'yqp_nlb_p1p_AA','yqp_nlb_p1p_AH'}))
        broken=copy.deepcopy(proposal);broken['evidence'][0]['quote']='太子'
        self.assertTrue(title_proposal_errors(broken,c,{'yqp_nlb_p1p_AH'}))

class ZhangFamilyLifeTests(unittest.TestCase):
    def test_four_generations_share_evidenced_paths_not_age_order(self):
        people={p['id']:p for p in read('registry/persons.json')['persons']}
        line=['796_nkw_0jz','796_nkw_0jz_A','796_nkw_0jz_AA','796_nkw_0jz_AAA']
        for parent,child in zip(line,line[1:]):
            path=people[child]['family_path']
            self.assertEqual((path['parent_person_id'],path['generation_distance'],path['connection']),(parent,1,'father'))
            self.assertTrue(path['evidence'])
        self.assertEqual(ids(para(96,15),'父'),{'796_nkw_0jz'})
        self.assertIn('未名',people[line[0]]['label'])
        self.assertNotIn('長', [a['surface'] for a in people[line[0]]['aliases']])
        self.assertEqual(ids(para(96,14),'康侯'),{line[2]})
        self.assertEqual(ids(para(96,15),'類'),{line[3]})

    def test_self_preface_and_table_name_follow_same_person(self):
        self.assertEqual(ids(para(130,108),'蒼'),{'796_nkw_0jz_A'})
        self.assertEqual(ids(para(130,142),'張蒼'),{'796_nkw_0jz_A'})
        table=read('data/historical-tables/shiji-022.json')
        cell=next(c for f in table['fragments'] for row in f['rows'] for c in row['cells'] if c['id']=='shiji-022-t1-r055-c02')
        self.assertEqual({m['person_id'] for m in cell['person_mentions'] if m['surface']=='張蒼'},{'796_nkw_0jz_A'})

    def test_death_ranges_preserve_two_calendar_years_in_api(self):
        events=read('corpus/shiji/096-life-events.json')['events']
        self.assertEqual(len(events),16)
        for pid,earliest,latest in [('796_nkw_0jz_A',153,152),('yph_dkb_w4w',156,155)]:
            e=next(e for e in events if e['person_id']==pid)
            self.assertNotIn('normalized_date',e)
            d=e['normalized_date_range']
            self.assertEqual((d['earliest']['era_year'],d['latest']['era_year']),(earliest,latest))
            self.assertEqual(d['earliest']['year'],1-earliest)
            b=read(f'exports/persons/{pid}.json')
            self.assertTrue(any(x['record_id']==e['id'] for x in b['date_range_normalizations']))
            self.assertFalse(any(x['record_id']==e['id'] for x in b['date_normalizations']))
            self.assertTrue(any(r['scope']=='received_calendar_rule' and '十月為歲首' in r['quote'] for r in d['references']))

    def test_bounded_hundred_age_does_not_create_birth_or_exact_age(self):
        b=read('exports/persons/796_nkw_0jz_A.json')
        age=next(a for a in b['age_assertions'] if a['id']=='age-shiji096-001')
        self.assertIsNone(age['value']);self.assertIsNone(age['birth_year'])
        self.assertEqual(age['bounds'],{'lower':100,'lower_inclusive':False,'upper':None,'upper_inclusive':None})
        self.assertEqual((age['source_term'],age['reporting_status']),('百有餘歲','direct_report'))
        self.assertFalse(any(e['event_type']=='birth' for e in b['life_events']))

    def test_relative_death_intervals_are_not_regnal_years_or_ages(self):
        events=read('corpus/shiji/096-life-events.json')['events']
        chang=next(e for e in events if e['person_id']=='gfr_55l_72s')
        self.assertEqual(chang['date_expression'],'謝病不朝見，三歲而死')
        self.assertNotIn('normalized_date',chang);self.assertNotIn('normalized_date_range',chang)
        for pid in ['796_nkw_0jz_AA','yph_dkb_w4w_A','yph_dkb_w4w_AA']:
            e=next(e for e in events if e['person_id']==pid)
            self.assertIsNone(e['date_expression'])
            self.assertNotIn('normalized_date',e)

    def test_death_does_not_fill_all_title_endpoints(self):
        h=next(h for h in read('corpus/shiji/096-titles.json')['holdings'] if h['id']=='th-shiji096-006')
        self.assertEqual(h['person_id'],'796_nkw_0jz_A')
        self.assertEqual(h['effective_period']['end']['status'],'unknown')
        self.assertNotIn('normalized_date_range',h['effective_period']['end'])

    def test_rebased_and_duplicate_person_ids_are_retired(self):
        people={p['id'] for p in read('registry/persons.json')['persons']}
        for old in ['68u_x4k_2k4','68u_x4k_2k4_A','68u_x4k_2k4_AA','cf6_ekq_84s']:
            self.assertNotIn(old,people)
            self.assertFalse((ROOT/f'exports/persons/{old}.json').exists())
            self.assertFalse((ROOT/f'data/corpus/profiles/{old}.json').exists())

class ZhangContinuationTests(unittest.TestCase):
    def test_bare_chancellor_follows_shentujia_not_office_building(self):
        for n,starts in [(17,[46,63,241,257,284]),(18,[140])]:
            p=para(96,n)
            for start in starts:
                m=next(m for m in p['mentions'] if m['start']==start)
                self.assertEqual((m['surface'],m['person_id']),('丞相','yph_dkb_w4w'))
        self.assertFalse(any(m['start'] in (125,163) for m in para(96,17)['mentions']))

    def test_proposed_chancellorship_is_not_guangguo_appointment(self):
        c=read('corpus/shiji/096.json')
        t=next(x for x in c['annotation']['title_proposals'] if x['id']=='tp-shiji096-002')
        self.assertEqual((t['person_id'],t['outcome']),('xoj_go3_gl0','not_enacted'))
        m=next(m for m in para(96,16)['mentions'] if m['id']==t['role_mention_id'])
        self.assertEqual((m['surface'],m['person_id'],m['kind']),('丞相',None,'unresolved'))
        self.assertFalse(any(h['person_id']=='xoj_go3_gl0' and h['title']=='丞相' for h in read('corpus/shiji/096-titles.json')['holdings']))

    def test_father_poison_and_son_execution_remain_separate(self):
        ev=read('corpus/shiji/101-life-events.json')['events']
        father=next(x for x in ev if x['source_term']=='遂飲藥死')
        son=next(x for x in ev if x['source_term']=='上令鼂錯衣朝衣斬東市')
        self.assertEqual(father['person_id'],'04u_gq0_nke')
        self.assertEqual(son['person_id'],'04u_gq0_nke_A')
        self.assertIsNone(father['date_expression'])
        self.assertNotIn('normalized_date',father)
        self.assertEqual(ids(para(96,18),'晁錯'),{'04u_gq0_nke_A'})
        self.assertEqual(ids(para(101,19),'鼂錯'),{'04u_gq0_nke_A'})
        self.assertIn('歐血',para(96,18)['text'])
        self.assertIn('丞相遂發病死',para(101,18)['text'])

    def test_ningxing_rulers_follow_each_narrative_period(self):
        for surface,pid in [('高祖','yqp_nlb_p1p_A'),('孝惠','yqp_nlb_p1p_AA'),('孝文','yqp_nlb_p1p_AC')]:
            self.assertEqual(ids(para(125,1),surface),{pid})
        self.assertEqual(ids(para(125,2),'太子'),{'yqp_nlb_p1p_ACA'})
        self.assertEqual(ids(para(125,2),'今天子'),{'yqp_nlb_p1p_ACAA'})

    def test_twenty_four_retired_candidates_leave_no_public_alias_files(self):
        people={p['id'] for p in read('registry/persons.json')['persons']}
        olds=['8ve_l7c_yz3','uqv_78v_j7w','ccv_1jr_0jn','7mt_qrc_04e','ef9_2e4_amv','z6w_dj2_cmc','cic_28p_bjp','n1e_bz7_1di','eba_45k_rot','5xc_h44_k0y','olo_0sp_7bd','9xr_uju_djo','si4_1zk_24j','ut8_ibh_dll','oye_sta_uwq','ys2_3lx_sdi','qza_o7u_0m7','s6p_kl2_f9g','ut6_wbc_3ca','6fi_7i1_821','948_i7p_bip','oe1_3l9_1fc','qoz_qmk_3kn','edz_j1e_1qg']
        for old in olds:
            self.assertNotIn(old,people)
            self.assertFalse((ROOT/f'exports/persons/{old}.json').exists())
            self.assertFalse((ROOT/f'data/corpus/profiles/{old}.json').exists())
