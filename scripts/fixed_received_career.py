"""Fixed received biography career roles and local reign-year scope.
Finite complete-clause grammar, not name/ID matching or general NLU.
"""
from pathlib import Path
import json,hashlib,re
RECIPES={'unit001': {'template': '<r0>字<r3>太原陽曲人也',
             'slots': {'place0': {'record_kind': 'address',
                                  'recipient_mid_position': 0,
                                  'recipient_in_previous': False,
                                  'biography_topic': True,
                                  'date': None,
                                  'event_anchor': {'start': 5, 'end': 11, 'surface': '太原陽曲人也'},
                                  'relation': 'biographical_origin',
                                  'place': '太原陽曲'}},
             'same_person_groups': [['r0', 'r3']],
             'layer': 'received_chapter'},
 'unit002': {'template': '按郭氏譜<r4>祖<r6>{office1}父<r11>{office2}',
             'slots': {'office1': {'recipient_mid_position': 6,
                                   'recipient_in_previous': False,
                                   'kind': 'office',
                                   'mode': 'attestation',
                                   'stage': 'source_report',
                                   'date': None,
                                   'biography_topic': False},
                       'office2': {'recipient_mid_position': 11,
                                   'recipient_in_previous': False,
                                   'kind': 'office',
                                   'mode': 'attestation',
                                   'stage': 'source_report',
                                   'date': None,
                                   'biography_topic': False}},
             'same_person_groups': [['r4'], ['r6'], ['r11']],
             'layer': 'witness_appended_pei_songzhi_note'},
 'unit003': {'template': '{date0}舉孝廉除{office1}<r11>為五官將召<r18>署為{office2}轉為{office3}從征漢中<r38>還留征西將軍<r46>拒<r50>以<r53>為<r55>{office4}<r58>與<r60>戰<r62>時有疾不出<r68>遇害軍中擾擾<r75>收散卒推盪冦將軍<r84>為軍主諸營乃定其明日<r96>欲渡漢水來攻諸將議衆寡不敵<r110>便乘勝欲依水為陣以拒之<r122>曰此示弱而不足挫敵非筭也不如遠水為陣引而致之半濟而後擊<r150>可破也既陣<r156>疑不渡<r160>遂堅守示無還心以狀聞<r171>善之假<r176>節復以<r180>為{office5}<r184>即王位賜爵{office6}轉為{office7}又行{office8}䕶左將軍<r210>冠軍將軍<r216>討山賊<r221>盧水叛胡皆破平之關中始定民得安業',
             'slots': {'office1': {'recipient_mid_position': 18,
                                   'recipient_in_previous': False,
                                   'kind': 'office',
                                   'mode': 'grant',
                                   'stage': 'initial_appointment',
                                   'date': '建安中',
                                   'biography_topic': True},
                       'office2': {'recipient_mid_position': 18,
                                   'recipient_in_previous': False,
                                   'kind': 'office',
                                   'mode': 'grant',
                                   'stage': 'staff_appointment',
                                   'date': None,
                                   'biography_topic': True},
                       'office3': {'recipient_mid_position': 18,
                                   'recipient_in_previous': False,
                                   'kind': 'office',
                                   'mode': 'transfer',
                                   'stage': 'transfer',
                                   'date': None,
                                   'biography_topic': True},
                       'office4': {'recipient_mid_position': 18,
                                   'recipient_in_previous': False,
                                   'kind': 'office',
                                   'mode': 'grant',
                                   'stage': 'staff_appointment',
                                   'date': None,
                                   'biography_topic': True},
                       'office5': {'recipient_mid_position': 18,
                                   'recipient_in_previous': False,
                                   'kind': 'office',
                                   'mode': 'grant',
                                   'stage': 'reappointment',
                                   'date': None,
                                   'biography_topic': True},
                       'office6': {'recipient_mid_position': 18,
                                   'recipient_in_previous': False,
                                   'kind': 'noble_rank',
                                   'mode': 'grant',
                                   'stage': 'enfeoffment',
                                   'date': None,
                                   'biography_topic': True},
                       'office7': {'recipient_mid_position': 18,
                                   'recipient_in_previous': False,
                                   'kind': 'office',
                                   'mode': 'transfer',
                                   'stage': 'transfer',
                                   'date': None,
                                   'biography_topic': True},
                       'office8': {'recipient_mid_position': 18,
                                   'recipient_in_previous': False,
                                   'kind': 'office',
                                   'mode': 'grant',
                                   'stage': 'acting_office',
                                   'date': None,
                                   'biography_topic': True},
                       'death68': {'record_kind': 'life',
                                   'recipient_mid_position': 68,
                                   'recipient_in_previous': False,
                                   'biography_topic': False,
                                   'date': None,
                                   'event_anchor': {'start': 69, 'end': 71, 'surface': '遇害'},
                                   'event_type': 'death'},
                       'detail3': {'record_kind': 'detail',
                                   'recipient_mid_position': 18,
                                   'recipient_in_previous': False,
                                   'biography_topic': True,
                                   'date': None,
                                   'event_anchor': {'start': 3, 'end': 6, 'surface': '舉孝廉'},
                                   'detail_kind': 'recruitment_selection',
                                   'values': {'selection_source_term': '孝廉',
                                              'selection_mode': '舉',
                                              'office_appointment_inferred': False,
                                              'date_source_term': '建安中'}}},
             'same_person_groups': [['r11', 'r184'],
                                    ['r18', 'r53', 'r62', 'r75', 'r122', 'r160', 'r180'],
                                    ['r38', 'r171'],
                                    ['r46', 'r55', 'r58', 'r68'],
                                    ['r50', 'r60', 'r96', 'r110', 'r150', 'r156'],
                                    ['r84', 'r176', 'r210'],
                                    ['r216'],
                                    ['r221']],
             'layer': 'received_chapter'},
 'unit004': {'template': '{date0}奉使賀<r7>踐阼而道路得疾故計遠近為稽留及羣臣歡㑹<r28>正色責之曰昔<r35>㑹諸侯於塗山<r42>後至便行大戮今溥天同慶而<r56>最留遲何也<r62>對曰<r65>聞五帝先教導民以徳夏后政衰始用刑辟今<r84>遭唐虞之世是以自知免於<r96>之誅也<r101>悅之擢領{office1}封{office2}{date115}為真安定羌大帥<r124>反討破降之每羌胡來降<r136>輒先使人推問其親理男女多少年歲長幼及見一一知其欵曲訊問周至咸稱神明',
             'slots': {'office1': {'recipient_mid_position': 62,
                                   'recipient_in_previous': False,
                                   'kind': 'office',
                                   'mode': 'grant',
                                   'stage': 'concurrent_appointment',
                                   'date': '黃初元年',
                                   'biography_topic': True},
                       'office2': {'recipient_mid_position': 62,
                                   'recipient_in_previous': False,
                                   'kind': 'noble_rank',
                                   'mode': 'grant',
                                   'stage': 'enfeoffment',
                                   'date': '黃初元年',
                                   'biography_topic': True},
                       'place124': {'record_kind': 'address',
                                    'recipient_mid_position': 124,
                                    'recipient_in_previous': False,
                                    'biography_topic': False,
                                    'date': None,
                                    'event_anchor': {'start': 119, 'end': 126, 'surface': '安定羌大帥辟蹏'},
                                    'relation': 'source_locality_designation',
                                    'place': '安定'},
                       'detail115': {'record_kind': 'detail',
                                     'recipient_mid_position': 62,
                                     'recipient_in_previous': False,
                                     'biography_topic': True,
                                     'date': None,
                                     'event_anchor': {'start': 115, 'end': 119, 'surface': '五年為真'},
                                     'detail_kind': 'office_confirmation',
                                     'values': {'confirmation_source_term': '為真',
                                                'linked_holding_id': None,
                                                'date_source_term': '五年',
                                                'normalized_year': 224,
                                                'era_name': '黃初',
                                                'duration_years': None},
                                     'linked_slot': {'rule': 'unit004', 'slot': 'office1'}}},
             'same_person_groups': [['r7', 'r28', 'r101'], ['r35'], ['r42', 'r96'], ['r56', 'r62', 'r65', 'r84', 'r136'], ['r124']],
             'layer': 'received_chapter'},
 'unit005': {'template': '{date0}蜀相<r6>出祁山遣將軍<r15>至街亭<r20>屯列柳城<r26>擊<r29><r30>攻<r32>營皆破之又破隴西名羌<r43>於枹罕加{office1}{date53}蜀出鹵城是時隴右無榖議欲關中大運<r71>以威恩撫循羌胡家使出榖平其輸調軍食用足轉{office2}',
             'slots': {'office1': {'recipient_mid_position': 30,
                                   'recipient_in_previous': False,
                                   'kind': 'office',
                                   'mode': 'grant',
                                   'stage': 'additional_office',
                                   'date': '太和二年',
                                   'biography_topic': True},
                       'office2': {'recipient_mid_position': 30,
                                   'recipient_in_previous': False,
                                   'kind': 'office',
                                   'mode': 'transfer',
                                   'stage': 'transfer',
                                   'date': '五年',
                                   'biography_topic': True},
                       'place43': {'record_kind': 'address',
                                   'recipient_mid_position': 43,
                                   'recipient_in_previous': False,
                                   'biography_topic': False,
                                   'date': None,
                                   'event_anchor': {'start': 39, 'end': 45, 'surface': '隴西名羌唐蹏'},
                                   'relation': 'source_locality_designation',
                                   'place': '隴西'}},
             'same_person_groups': [['r6'], ['r15', 'r29'], ['r20', 'r32'], ['r26'], ['r30', 'r71'], ['r43']],
             'layer': 'received_chapter'},
 'unit007': {'template': '{date0}蜀將<r6>出隴西<r11>遂進軍追至彊中<r19>退遂討羌<r24>等按撫柔氐三千餘落拔徙以實關中遷{office1}涼州休屠胡<r50>等率種落二千餘家附雍州<r64>奏請使居安定之高平為民保障其後因置西川都尉轉拜{office2}領州如故',
             'slots': {'office1': {'recipient_mid_position': 11,
                                   'recipient_in_previous': False,
                                   'kind': 'office',
                                   'mode': 'transfer',
                                   'stage': 'promotion',
                                   'date': '正始元年',
                                   'biography_topic': True},
                       'office2': {'recipient_mid_position': 11,
                                   'recipient_in_previous': False,
                                   'kind': 'office',
                                   'mode': 'transfer',
                                   'stage': 'promotion',
                                   'date': None,
                                   'biography_topic': True,
                                   'date_qualification': {'kind': 'subsequent_event_year_unspecified',
                                                          'source_term': '其後',
                                                          'source_anchor': {'paragraph_id': 'c-sanguozhi-026-guohuai:unit007',
                                                                            'start': 78,
                                                                            'end': 80,
                                                                            'surface': '其後'},
                                                          'earlier_date_source_term': '正始元年',
                                                          'same_year_not_asserted': True}},
                       'place50': {'record_kind': 'address',
                                   'recipient_mid_position': 50,
                                   'recipient_in_previous': False,
                                   'biography_topic': False,
                                   'date': None,
                                   'event_anchor': {'start': 45, 'end': 53, 'surface': '涼州休屠胡梁元碧'},
                                   'relation': 'source_locality_designation',
                                   'place': '涼州'},
                       'detail91': {'record_kind': 'detail',
                                    'recipient_mid_position': 11,
                                    'recipient_in_previous': False,
                                    'biography_topic': True,
                                    'date': None,
                                    'event_anchor': {'start': 91, 'end': 95, 'surface': '領州如故'},
                                    'detail_kind': 'office_continuation',
                                    'values': {'continuation_source_term': '領州如故', 'linked_holding_id': None, 'end_year': None},
                                    'linked_slot': {'rule': 'unit004', 'slot': 'office1'}}},
             'same_person_groups': [['r6', 'r19'], ['r11', 'r64'], ['r24'], ['r50']],
             'layer': 'received_chapter'},
 'unit008': {'template': '{date0}<r2>伐蜀<r7>督諸軍為前鋒<r14>度勢不利輒拔軍出故不大敗還假<r29>節',
             'slots': {'detail28': {'record_kind': 'detail',
                                    'recipient_mid_position': 7,
                                    'recipient_in_previous': False,
                                    'biography_topic': True,
                                    'date': None,
                                    'event_anchor': {'start': 28, 'end': 31, 'surface': '假淮節'},
                                    'detail_kind': 'military_authority',
                                    'values': {'authority_source_term': '節',
                                               'action_source_term': '假',
                                               'office_holding_inferred': False,
                                               'date_source_term': '五年',
                                               'normalized_year': 244,
                                               'era_name': '正始'}}},
             'same_person_groups': [['r2'], ['r7', 'r14', 'r29']],
             'layer': 'received_chapter'},
 'unit009': {'template': '{date0}隴西南安金城西平諸羌<r12><r14><r16><r18>等相結叛亂攻圍城邑南招蜀兵涼州名胡<r38>復叛應之討蜀䕶軍<r49>督諸軍屯為翅<r58>軍始到狄道議者僉謂宜先討定枹罕内平惡羌外折賊謀<r82>策<r84>必來攻<r88>遂入渢中轉南迎<r96><r97>果攻為翅㑹<r103>軍適至<r107>遁退進討叛羌斬<r115><r117>降服者萬餘落',
             'slots': {'death115': {'record_kind': 'life',
                                    'recipient_mid_position': 115,
                                    'recipient_in_previous': False,
                                    'biography_topic': False,
                                    'date': '八年',
                                    'event_anchor': {'start': 114, 'end': 115, 'surface': '斬'},
                                    'event_type': 'death'},
                       'death117': {'record_kind': 'life',
                                    'recipient_mid_position': 117,
                                    'recipient_in_previous': False,
                                    'biography_topic': False,
                                    'date': '八年',
                                    'event_anchor': {'start': 114, 'end': 115, 'surface': '斬'},
                                    'event_type': 'death'},
                       'place38': {'record_kind': 'address',
                                   'recipient_mid_position': 38,
                                   'recipient_in_previous': False,
                                   'biography_topic': False,
                                   'date': None,
                                   'event_anchor': {'start': 34, 'end': 41, 'surface': '涼州名胡治無戴'},
                                   'relation': 'source_locality_designation',
                                   'place': '涼州'}},
             'same_person_groups': [['r12', 'r115'],
                                    ['r14', 'r117'],
                                    ['r16'],
                                    ['r18'],
                                    ['r38'],
                                    ['r49', 'r88', 'r96'],
                                    ['r58', 'r82', 'r103'],
                                    ['r84', 'r97', 'r107']],
             'layer': 'received_chapter'},
 'unit011': {'template': '<r0>出石營從彊川乃西迎<r11>留隂平太守<r19>於成重山築城歛破羌保質<r32>欲分兵取之諸將以<r41>衆西接彊胡<r47>以據險分軍兩持兵勢轉弱進不制<r62>退不拔<r66>非計也不如合而俱西及胡蜀未接絶其内外此伐交之兵也<r91>曰今往取<r96>出賊不意<r101>必狼顧比<r106>自致足以定<r112>且使<r115>疲於奔命兵不遠西而胡交自離此一舉而兩全之策也乃别遣<r141>等追<r146>於沓中<r150>自率諸軍就攻<r157>等<r159>果馳還救<r164>皆如<r167>計進封{office1}',
             'slots': {'office1': {'recipient_mid_position': 32,
                                   'recipient_in_previous': False,
                                   'kind': 'noble_rank',
                                   'mode': 'grant',
                                   'stage': 'rank_advancement',
                                   'date': None,
                                   'biography_topic': True}},
             'same_person_groups': [['r0', 'r41', 'r62', 'r101', 'r106', 'r115', 'r146', 'r159'],
                                    ['r11'],
                                    ['r19', 'r47', 'r66', 'r96', 'r112', 'r157', 'r164'],
                                    ['r32', 'r91', 'r150', 'r167'],
                                    ['r141']],
             'layer': 'received_chapter'},
 'unit012': {'template': '{date0}遷{office1}{office2}是歲與雍州刺史<r23>協策降蜀牙門將<r32>等於翅上',
             'slots': {'office1': {'recipient_mid_position': None,
                                   'recipient_in_previous': True,
                                   'kind': 'office',
                                   'mode': 'transfer',
                                   'stage': 'promotion',
                                   'date': '嘉平元年',
                                   'biography_topic': True},
                       'office2': {'recipient_mid_position': None,
                                   'recipient_in_previous': True,
                                   'kind': 'office',
                                   'mode': 'grant',
                                   'stage': 'concurrent_command',
                                   'date': '嘉平元年',
                                   'biography_topic': True}},
             'same_person_groups': [['r23'], ['r32']],
             'layer': 'received_chapter'},
 'unit013': {'template': '{date0}詔曰昔漢川之役幾至傾覆<r13>臨危濟難功書王府在關右三十餘年外征冦虜内綏民夷比歲以來摧破<r43>禽虜<r47>功績顯著<r53>甚嘉之今以<r59>為{office1}{office2}持節都督如故進封{office3}邑凡二千七百八十戸分三百戸封一子亭侯',
             'slots': {'office1': {'recipient_mid_position': 13,
                                   'recipient_in_previous': False,
                                   'kind': 'office',
                                   'mode': 'grant',
                                   'stage': 'appointment',
                                   'date': '二年',
                                   'biography_topic': True},
                       'office2': {'recipient_mid_position': 13,
                                   'recipient_in_previous': False,
                                   'kind': 'honorific',
                                   'mode': 'grant',
                                   'stage': 'ceremonial_privilege',
                                   'date': '二年',
                                   'biography_topic': True},
                       'office3': {'recipient_mid_position': 13,
                                   'recipient_in_previous': False,
                                   'kind': 'noble_rank',
                                   'mode': 'grant',
                                   'stage': 'rank_advancement',
                                   'date': '二年',
                                   'biography_topic': True},
                       'detail69': {'record_kind': 'detail',
                                    'recipient_mid_position': 13,
                                    'recipient_in_previous': False,
                                    'biography_topic': True,
                                    'date': None,
                                    'event_anchor': {'start': 69, 'end': 75, 'surface': '持節都督如故'},
                                    'detail_kind': 'military_authority_continuation',
                                    'values': {'authority_source_term': '持節',
                                               'command_continuation_source_term': '都督如故',
                                               'linked_holding_id': None,
                                               'all_offices_continued': False},
                                    'linked_slot': {'rule': 'unit012', 'slot': 'office2'}},
                       'detail22': {'record_kind': 'detail',
                                    'recipient_mid_position': 13,
                                    'recipient_in_previous': False,
                                    'biography_topic': True,
                                    'date': None,
                                    'event_anchor': {'start': 22, 'end': 29, 'surface': '在關右三十餘年'},
                                    'detail_kind': 'regional_service_duration',
                                    'values': {'place_source_name': '關右',
                                               'source_number': '三十',
                                               'duration_lower_bound': 30,
                                               'bound_operator': 'gt',
                                               'unit': '年',
                                               'exact_duration': None,
                                               'derived_start_year': None,
                                               'derived_end_year': None,
                                               'linked_holding_id': None}},
                       'detail80': {'record_kind': 'detail',
                                    'recipient_mid_position': 13,
                                    'recipient_in_previous': False,
                                    'biography_topic': True,
                                    'date': None,
                                    'event_anchor': {'start': 80, 'end': 89, 'surface': '邑凡二千七百八十戸'},
                                    'detail_kind': 'fief_household_count',
                                    'values': {'total': 2780,
                                               'total_source_number': '二千七百八十',
                                               'unit_source_name': '戸',
                                               'increase': None,
                                               'actual_revenue': None,
                                               'linked_holding_id': None},
                                    'linked_slot': {'rule': 'unit013', 'slot': 'office3'}},
                       'detail89': {'record_kind': 'detail',
                                    'recipient_mid_position': 13,
                                    'recipient_in_previous': False,
                                    'biography_topic': True,
                                    'date': None,
                                    'event_anchor': {'start': 89, 'end': 98, 'surface': '分三百戸封一子亭侯'},
                                    'detail_kind': 'unnamed_family_title_grants',
                                    'values': {'recipient_group_source_term': '一子',
                                               'recipient_person_ids': [],
                                               'biological_children_only': False,
                                               'grants': [{'source_rank': '亭侯',
                                                           'recipient_count': 1,
                                                           'source_number': '一',
                                                           'households': 300,
                                                           'household_source_number': '三百',
                                                           'household_unit': '戸'}]}}},
             'same_person_groups': [['r13', 'r59'], ['r43'], ['r47'], ['r53']],
             'layer': 'received_chapter'},
 'unit015': {'template': '{date0}薨追贈{office1}諡曰{office2}子<r15>嗣<r17>官至{office3}薨子<r26>嗣{date28}開建五等以<r36>著勲前朝改封{office4}',
             'slots': {'office1': {'recipient_mid_position': 36,
                                   'recipient_in_previous': False,
                                   'kind': 'office',
                                   'mode': 'posthumous_grant',
                                   'stage': 'posthumous_office',
                                   'date': '正元二年',
                                   'biography_topic': True},
                       'office2': {'recipient_mid_position': 36,
                                   'recipient_in_previous': False,
                                   'kind': 'honorific',
                                   'mode': 'posthumous_naming',
                                   'stage': 'posthumous_name',
                                   'date': '正元二年',
                                   'biography_topic': True},
                       'office3': {'recipient_mid_position': 17,
                                   'recipient_in_previous': False,
                                   'kind': 'office',
                                   'mode': 'attestation',
                                   'stage': 'reported_attainment',
                                   'date': None,
                                   'biography_topic': False},
                       'office4': {'recipient_mid_position': 26,
                                   'recipient_in_previous': False,
                                   'kind': 'noble_rank',
                                   'mode': 'grant',
                                   'stage': 'editorial_current_heir_regrant',
                                   'date': '咸熙中',
                                   'biography_topic': False},
                       'death36': {'record_kind': 'life',
                                   'recipient_mid_position': 36,
                                   'recipient_in_previous': False,
                                   'biography_topic': True,
                                   'date': '正元二年',
                                   'event_anchor': {'start': 4, 'end': 5, 'surface': '薨'},
                                   'event_type': 'death'},
                       'death17': {'record_kind': 'life',
                                   'recipient_mid_position': 17,
                                   'recipient_in_previous': False,
                                   'biography_topic': False,
                                   'date': None,
                                   'event_anchor': {'start': 24, 'end': 25, 'surface': '薨'},
                                   'event_type': 'death'},
                       'succession14': {'record_kind': 'succession',
                                        'recipient_mid_position': 15,
                                        'recipient_in_previous': False,
                                        'biography_topic': False,
                                        'date': None,
                                        'event_anchor': {'start': 14, 'end': 17, 'surface': '子統嗣'},
                                        'event_type': 'noble_title_succession'},
                       'succession25': {'record_kind': 'succession',
                                        'recipient_mid_position': 26,
                                        'recipient_in_previous': False,
                                        'biography_topic': False,
                                        'date': None,
                                        'event_anchor': {'start': 25, 'end': 28, 'surface': '子正嗣'},
                                        'event_type': 'noble_title_succession'}},
             'same_person_groups': [['r15', 'r17'], ['r26'], ['r36']],
             'layer': 'received_chapter'},
 'unit016': {'template': '晉諸公贊曰<r5>弟<r7>字<r9>有重名位至{office1}<r20><r22>皆<r25>女婿子<r29>字<r31>有器度幹用歴職著績終於{office2}次弟<r48>字<r50>{office3}知名早卒<r60>適<r62><r64>弟<r66>字<r68>{office4}<r74>子<r76>字<r78>山濤啓事稱<r85>高簡有雅量歴位{office5}{office6}',
             'slots': {'office1': {'recipient_mid_position': 7,
                                   'recipient_in_previous': False,
                                   'kind': 'office',
                                   'mode': 'attestation',
                                   'stage': 'source_report',
                                   'date': None,
                                   'biography_topic': False},
                       'office2': {'recipient_mid_position': 29,
                                   'recipient_in_previous': False,
                                   'kind': 'office',
                                   'mode': 'attestation',
                                   'stage': 'source_report',
                                   'date': None,
                                   'biography_topic': False},
                       'office3': {'recipient_mid_position': 48,
                                   'recipient_in_previous': False,
                                   'kind': 'office',
                                   'mode': 'attestation',
                                   'stage': 'source_report',
                                   'date': None,
                                   'biography_topic': False},
                       'office4': {'recipient_mid_position': 66,
                                   'recipient_in_previous': False,
                                   'kind': 'office',
                                   'mode': 'attestation',
                                   'stage': 'source_report',
                                   'date': None,
                                   'biography_topic': False},
                       'office5': {'recipient_mid_position': 76,
                                   'recipient_in_previous': False,
                                   'kind': 'office',
                                   'mode': 'attestation',
                                   'stage': 'source_report',
                                   'date': None,
                                   'biography_topic': False},
                       'office6': {'recipient_mid_position': 76,
                                   'recipient_in_previous': False,
                                   'kind': 'office',
                                   'mode': 'attestation',
                                   'stage': 'source_report',
                                   'date': None,
                                   'biography_topic': False},
                       'death48': {'record_kind': 'life',
                                   'recipient_mid_position': 48,
                                   'recipient_in_previous': False,
                                   'biography_topic': False,
                                   'date': None,
                                   'event_anchor': {'start': 58, 'end': 60, 'surface': '早卒'},
                                   'event_type': 'death'}},
             'same_person_groups': [['r5'],
                                    ['r7', 'r9', 'r25', 'r64'],
                                    ['r20'],
                                    ['r22'],
                                    ['r29', 'r31'],
                                    ['r48', 'r50'],
                                    ['r60'],
                                    ['r62'],
                                    ['r66', 'r68', 'r74'],
                                    ['r76', 'r78', 'r85']],
             'layer': 'witness_appended_pei_songzhi_note'}}

def witness(ch,root,reference):
 root=Path(root).resolve();rel=Path(reference['path']);path=root/rel
 assert set(reference)=={'path','sha256'}and not rel.is_absolute()and'..'not in rel.parts and rel.parts[0]=='source-evidence'and path.resolve()==path
 raw=path.read_bytes();assert hashlib.sha256(raw).hexdigest()==reference['sha256'];w=json.loads(raw);assert w['chapter_id']==ch['id']and w['source_commit']==ch['source']['source_commit']and w['raw_sha256']==ch['source']['raw_file_sha256']and w['raw_file']==ch['source']['raw_path']
 assert w['units']==[dict(paragraph_id=p['id'],text=p['text'],text_layer=p['text_layer'],source_position=p['source_position'])for p in ch['paragraphs']]
 rp=Path(w['raw_file']);pp=root/rp;assert not rp.is_absolute()and'..'not in rp.parts and rp.parts[0]=='sources'and pp.resolve()==pp
 rb=pp.read_bytes();assert hashlib.sha256(rb).hexdigest()==w['raw_sha256'];rt=rb.decode();ls=rt.splitlines(keepends=True)
 for p in ch['paragraphs']:
  fr=p['source_position']['source_fragments'];assert ''.join(x['text']for x in fr)==p['text']
  for x in fr:
   assert ls[x['line']-1][x['raw_start']:x['raw_end']]==x['text'];offset=sum(len(y)for y in ls[:x['line']-1])+x['raw_start'];note=rt[:offset].count('(')>rt[:offset].count(')')
   if p['text_layer']in('received_chapter','witness_appended_pei_songzhi_note'):assert note==(p['text_layer']=='witness_appended_pei_songzhi_note')
 return {'path':rel.as_posix(),'sha256':hashlib.sha256(raw).hexdigest()}
def analyse(rec,ch,root):
 b=rec['received_source_frame'];p=next(p for p in ch['paragraphs']if p['id']==b['paragraph_id']);t=p['text'];recipe=RECIPES[b['rule']];ms={m['id']:m for m in p['mentions']};roles={k:ms[v]for k,v in b['roles'].items()};fs=b['fields']
 assert b['kind']=='fixed_received_career_frame'and b['human_reviewed']is False and b['source_revision']==ch['source']['revision_id']and b['paragraph_sha256']==hashlib.sha256(t.encode()).hexdigest()and recipe['layer']==p['text_layer']and b['fixed_witness_reference']==witness(ch,root,b['fixed_witness_reference'])
 pos=0;ur=set();uf=set()
 for tok in re.split(r'(<[^>]+>|\{[^}]+\})',recipe['template']):
  if not tok:continue
  if tok.startswith('<'):
   k=tok[1:-1];m=roles[k];assert m['kind']=='person'and m['start']==pos and t[m['start']:m['end']]==m['surface'];pos=m['end'];ur.add(k)
  elif tok.startswith('{'):
   k=tok[1:-1];f=fs[k];assert set(f)=={'paragraph_id','start','end','surface'}and f['paragraph_id']==p['id']and f['start']==pos and t[f['start']:f['end']]==f['surface']and f['end']>f['start'];pos=f['end'];uf.add(k)
  else:assert t.startswith(tok,pos);pos+=len(tok)
 assert pos==len(t)and set(roles)==ur and set(fs)==uf
 assert {m['id']for m in p['mentions']if m['kind']=='person'and not any(f['start']<=m['start']<m['end']<=f['end']for f in fs.values())}==set(b['roles'].values())
 for group in recipe['same_person_groups']:assert len({roles[k]['person_id']for k in group})==1
 return p,roles,fs,recipe

def recipient(rec,ch,root):
 p,rs,fs,recipe=analyse(rec,ch,root);slot=recipe['slots'][rec['received_source_frame']['slot']];head=ch['paragraphs'][0]['mentions'][0]
 if slot['recipient_in_previous']:
  i=ch['paragraphs'].index(p);prev=ch['paragraphs'][i-1];m=next(m for m in prev['mentions']if m['person_id']==head['person_id']);assert p['text_layer']=='received_chapter'and prev['text_layer']=='received_chapter'
 else:m=next(m for m in rs.values()if m['start']==slot['recipient_mid_position'])
 if slot['biography_topic']:assert m['person_id']==head['person_id']and head['start']==0 and ch['paragraphs'][0]['text'][head['end']:].startswith('字')
 return p,m,fs,slot

def holding_valid(h,ch,root):
 try:
  p,m,fs,s=recipient(h,ch,root);assert s.get('record_kind','holding')=='holding';key=h['received_source_frame']['slot'];f=fs[key];e,=h['evidence'];a,=h['attestations'];assert h['person_id']==m['person_id']and h['title']==f['surface']and h['kind']==s['kind']and h['mode']==s['mode']and h['appointment_role']==s['stage']and h['status']=='source_attested'and h['human_reviewed']is False
  ev=dict(work_id=ch['work_id'],book_id=ch['book_id'],source_id=ch['source_id'],chapter_id=ch['id'],paragraph_id=p['id'],quote=p['text'],person_mention_id=m['id'])
  if s['recipient_in_previous']:
   prev=ch['paragraphs'][ch['paragraphs'].index(p)-1];ev['context']=dict(kind='previous_paragraph_subject',paragraph_id=prev['id'],person_mention_id=m['id'],quote=prev['text']);assert a['context']==ev['context']
  assert e==ev and all(a[k]==f[k]for k in('paragraph_id','start','end','surface'))and a['person_mention_id']==m['id']and a['date_expression']is None
  unknown=dict(status='unknown',date_expression=None,evidence=[]);start=unknown if s['mode']=='attestation'else dict(status='source_event',event_type=s['mode'],date_expression=s['date'],evidence=h['evidence']);actual=h['effective_period']['start']
  if 'normalized_date'in actual:
   assert s['date']and local_date_valid(actual['normalized_date'],ch,root,h,'start');start['normalized_date']=actual['normalized_date']
  if 'normalized_date_range'in actual:
   try:from scripts.date_ranges import year_range_errors
   except ImportError:from date_ranges import year_range_errors
   w=actual['normalized_date_range'];assert not year_range_errors(w,h['evidence'],s['date'],root=root)and w['source_expression']==s['date']and w['original_quote']==p['text']and w['evidence']==h['evidence'];start['normalized_date_range']=w
  if 'date_qualification'in s:assert h['date_qualification']==s['date_qualification']
  else:assert 'date_qualification'not in h
  assert h['effective_period']==dict(start=start,end=unknown)
  return True
 except(KeyError,TypeError,ValueError,AssertionError,StopIteration,OSError,IndexError):return False

ERA_SPANS={'建安':(196,220),'黃初':(220,226),'太和':(227,233),'青龍':(233,237),'景初':(237,239),'正始':(240,249),'嘉平':(249,254),'正元':(254,256),'甘露':(256,259),'景元':(260,264),'咸熙':(264,265)}
NUM={'元':1,'一':1,'二':2,'三':3,'四':4,'五':5,'六':6,'七':7,'八':8,'九':9,'十':10}
DATE_RE=re.compile('('+'|'.join(ERA_SPANS)+')(?:([元一二三四五六七八九十]+)年|[初中末])?|([元一二三四五六七八九十]+)年')
def local_scope(ch,target_pid,target_pos,root,reference):
 witness(ch,root,reference);era=None;last=None;full=None;seen=[]
 for p in ch['paragraphs']:
  if p['text_layer']!='received_chapter':
   if p['id']==target_pid:raise AssertionError('notes cannot inherit body chronology')
   continue
  for x in DATE_RE.finditer(p['text']):
   if p['id']==target_pid and x.start()>target_pos:break
   if x[1]:era=x[1];full=dict(paragraph_id=p['id'],start=x.start(),end=x.end(),surface=x.group());last=None
   number=x[2]or x[3]
   if era:
    row=dict(paragraph_id=p['id'],start=x.start(),end=x.end(),surface=x.group(),era_name=era,source_number=number,regnal_year=NUM[number]if number else None)
    seen.append(row);last=row if number else None
  if p['id']==target_pid:break
 assert last and full and last['paragraph_id']==target_pid and last['start']==target_pos
 lo=next(i for i,p in enumerate(ch['paragraphs'])if p['id']==full['paragraph_id']);hi=next(i for i,p in enumerate(ch['paragraphs'])if p['id']==target_pid)
 interval=[dict(paragraph_id=p['id'],text=p['text'],text_layer=p['text_layer'],sha256=hashlib.sha256(p['text'].encode()).hexdigest())for p in ch['paragraphs'][lo:hi+1]]
 dates=[x for x in seen if next(i for i,p in enumerate(ch['paragraphs'])if p['id']==x['paragraph_id'])>=lo]
 return dict(kind='same_biography_received_regnal_interval',full_era_anchor=full,target_anchor=last,interval=interval,ordered_dates=dates,fixed_witness_reference=witness(ch,root,reference))

def local_date_valid(date,ch,root,bound_record,bound_role):
 try:
  assert bound_record is not None and bound_role in('start','life_event');p,m,fs,s=recipient(bound_record,ch,root);literal=s['date'];matches=[f for f in fs.values()if f['surface']==literal];assert len(matches)==1;f=matches[0];scope=local_scope(ch,p['id'],f['start'],root,bound_record['received_source_frame']['fixed_witness_reference']);last=scope['target_anchor'];era=last['era_name'];num=last['regnal_year'];first,end=ERA_SPANS[era];year=first+num-1
  assert date['regnal_year_mapping']==dict(kind='fixed_received_local_regnal_year',era_name=era,source_number=last['source_number'],regnal_year=num,start_ce_year=first,end_ce_year=end,reference_index=0,scope=scope)
  assert date['source_expression']==literal and date['original_quote']==p['text']and date['evidence']==bound_record['evidence']and date['era']=='CE'and date['era_year']==date['year']==year and year<=end and date['year_numbering']=='astronomical'and date['precision']=='year'and date['calendar']=='chinese_civil'and date['status']=='editorial_provisional'and date['human_reviewed']is False
  r,=date['references'];assert r==dict(url='https://dict.revised.moe.edu.tw/appendix.jsp?ID=3&page=1',quote=era,scope='modern_era_year_equivalence_only',columns=dict(era_name=era,first_year=str(first),last_year=str(end),dynasty='東漢'if era=='建安'else'魏'))
  # Actual record recipient and title remain bound even if an otherwise valid date block was copied consistently.
  ev=dict(work_id=ch['work_id'],book_id=ch['book_id'],source_id=ch['source_id'],chapter_id=ch['id'],paragraph_id=p['id'],quote=p['text'],person_mention_id=m['id'])
  if s['recipient_in_previous']:
   previous=ch['paragraphs'][ch['paragraphs'].index(p)-1];ev['context']=dict(kind='previous_paragraph_subject',paragraph_id=previous['id'],person_mention_id=m['id'],quote=previous['text'])
  assert bound_record['person_id']==m['person_id']and bound_record['evidence']==[ev]and bound_record['status']=='source_attested'and bound_record['human_reviewed']is False
  if bound_role=='start':assert s.get('record_kind','holding')=='holding'and bound_record['title']==fs[bound_record['received_source_frame']['slot']]['surface']and bound_record['kind']==s['kind']and bound_record['mode']==s['mode']and bound_record['appointment_role']==s['stage']and bound_record['effective_period']['start']['date_expression']==literal
  else:assert s['record_kind']=='life'and bound_record['event_type']==s['event_type']and bound_record['source_term']==s['event_anchor']['surface']and bound_record['date_expression']==literal
  return True
 except(KeyError,TypeError,ValueError,AssertionError,StopIteration,OSError,IndexError):return False


def nonholding_valid(rec,ch,root,expected_kind,holdings=None):
 try:
  p,m,fs,s=recipient(rec,ch,root);assert s['record_kind']==expected_kind and rec['person_id']==m['person_id']and rec['human_reviewed']is False and rec['status']=='source_attested';e,=rec['evidence'];assert e==dict(work_id=ch['work_id'],book_id=ch['book_id'],source_id=ch['source_id'],chapter_id=ch['id'],paragraph_id=p['id'],quote=p['text'],person_mention_id=m['id']);a=dict(paragraph_id=p['id'],**s['event_anchor']);assert p['text'][a['start']:a['end']]==a['surface']and rec['source_term']==a['surface']
  if expected_kind=='life':
   assert rec['event_type']==s['event_type']and rec['date_expression']==s['date']
   if s['date']:assert local_date_valid(rec['normalized_date'],ch,root,rec,'life_event')
   else:assert 'normalized_date'not in rec and 'normalized_date_range'not in rec
  elif expected_kind=='address':assert rec['relation']==s['relation']and rec['place']==dict(source_name=s['place'],place_id=None,modern_identification=None)and rec['date_expression']is None
  elif expected_kind=='detail':
   assert rec['kind']==s['detail_kind']and rec['source_anchor']==a and rec['source_revision']==ch['source']['revision_id']and rec['paragraph_sha256']==rec['received_source_frame']['paragraph_sha256']and rec['date_expression']is None
   # A technical holding ID is a reference, not an identity proof. Check linked holding's actual person and source syntax.
   expected=dict(s['values']);actual=rec['values'];assert set(actual)==set(expected)
   if 'linked_slot'in s:
    k=actual['linked_holding_id'];assert holdings is not None and k in holdings;h=holdings[k];assert h['person_id']==rec['person_id']and h['received_source_frame']['rule']==s['linked_slot']['rule']and h['received_source_frame']['slot']==s['linked_slot']['slot']and holding_valid(h,ch,root);expected['linked_holding_id']=k
   assert actual==expected
   if 'normalized_year'in actual:
    f=next(f for f in fs.values()if f['surface']==actual['date_source_term']);scope=local_scope(ch,p['id'],f['start'],root,rec['received_source_frame']['fixed_witness_reference']);x=scope['target_anchor'];assert x['era_name']==actual['era_name']and ERA_SPANS[x['era_name']][0]+x['regnal_year']-1==actual['normalized_year']
  elif expected_kind=='succession':assert rec['event_type']=='noble_title_succession'and rec['title']is None and rec['predecessor_person_id']is None and rec['date_expression']is None
  return True
 except(KeyError,TypeError,ValueError,AssertionError,StopIteration,OSError,IndexError):return False
