"""任用後未受或未赴任，與未實行的立號提議分開。"""


def unassumed_role(proposal, paragraph):
    role = next((m for m in paragraph.get('mentions', [])
                 if m['id'] == proposal.get('role_mention_id')), None)
    if role and role.get('kind') == 'non_person' and role.get('lexical_role') == 'offered_office':
        try: from scripts.lexical_annotations import non_person_errors
        except ImportError: from lexical_annotations import non_person_errors
        if not non_person_errors(role, paragraph['text']):
            return dict(role, kind='unresolved')
    if role:
        return role
    anchor = proposal.get('role_anchor')
    if (not isinstance(anchor, dict) or set(anchor) != {'paragraph_id', 'start', 'end', 'surface'}
            or anchor['paragraph_id'] != paragraph['id']
            or type(anchor['start']) is not int or type(anchor['end']) is not int
            or not 0 <= anchor['start'] < anchor['end'] <= len(paragraph['text'])
            or paragraph['text'][anchor['start']:anchor['end']] != anchor['surface']):
        return None
    return dict(anchor, kind='unresolved', person_id=None)


def unassumed_appointment_valid(proposal, chapter):
    if chapter.get('id') == 'c-nanshi-024-wangsiyuan':
        try: from scripts.nanshi024_wangsiyuan import proposal_valid as nan24siy_proposal_valid
        except ImportError: from nanshi024_wangsiyuan import proposal_valid as nan24siy_proposal_valid
        return nan24siy_proposal_valid(proposal, chapter)
    if chapter.get('id') == 'c-nanshi-024-wangyan':
        try: from scripts.nanshi024_wangyan import proposal_valid as nan24yan_proposal_valid
        except ImportError: from nanshi024_wangyan import proposal_valid as nan24yan_proposal_valid
        return nan24yan_proposal_valid(proposal, chapter)
    if chapter.get('id') == 'c-epitaph-wangjianzhi-full':
        try: from scripts.xiangshan_m9_epitaphs import proposal_valid as xm9_proposal_valid
        except ImportError: from xiangshan_m9_epitaphs import proposal_valid as xm9_proposal_valid
        return xm9_proposal_valid(proposal, chapter)
    if chapter.get('id') in ['c-songshu-093-wanghongzhi-wyd', 'c-songshu-093-ruanwanling-wyd']:
        try: from scripts.song093_wyd import proposal_valid as s93wyd_proposal
        except ImportError: from song093_wyd import proposal_valid as s93wyd_proposal
        return s93wyd_proposal(proposal,chapter)
    if proposal.get('id','').startswith('tp-nanshi024-wanghongzhi-'):
        try: from scripts.nanshi024_wanghongzhi import proposal_valid as n24hong_proposal
        except ImportError: from nanshi024_wanghongzhi import proposal_valid as n24hong_proposal
        return n24hong_proposal(proposal,chapter)
    if chapter.get('id') == 'c-songshu-093-ruanwanling':
        try: from scripts.nanshi024_ruanwanling import proposal_valid as nan24rw_proposal_valid
        except ImportError: from nanshi024_ruanwanling import proposal_valid as nan24rw_proposal_valid
        return nan24rw_proposal_valid(proposal, chapter)
    if chapter.get('id') == 'c-songshu-093-wangsu':
        try: from scripts.nanshi024_wangsu import proposal_valid as nan24su_proposal_valid
        except ImportError: from nanshi024_wangsu import proposal_valid as nan24su_proposal_valid
        return nan24su_proposal_valid(proposal, chapter)
    if chapter.get('id') == 'c-nanqishu-052-wangqunzhi':
        try: from scripts.nanshi024_wangqunzhi import proposal_valid as nan24qun_proposal_valid
        except ImportError: from nanshi024_wangqunzhi import proposal_valid as nan24qun_proposal_valid
        return nan24qun_proposal_valid(proposal, chapter)
    if proposal.get('source_refusal_form') == 'jin098_huan_chengxiang':
        try: from scripts.jin098_huan_final import refused
        except ImportError: from jin098_huan_final import refused
        return refused(proposal, chapter)
    if proposal.get('source_refusal_form') == 'jin098_huan_taiwei':
        try: from scripts.jin098_huan_taiwei import valid as huan_taiwei_valid
        except ImportError: from jin098_huan_taiwei import valid as huan_taiwei_valid
        return huan_taiwei_valid(proposal, chapter)
    if chapter.get('id') == 'c-nanshi-059-wangsengru':
        try: from scripts.nanshi059_wangsengru import proposal_valid as nan59sr_proposal_valid
        except ImportError: from nanshi059_wangsengru import proposal_valid as nan59sr_proposal_valid
        return nan59sr_proposal_valid(proposal, chapter)
    if chapter.get('id') == 'c-liangshu-033-wangsengru':
        try: from scripts.liang033_wangsengru import proposal_valid as liang33sr_proposal_valid
        except ImportError: from liang033_wangsengru import proposal_valid as liang33sr_proposal_valid
        return liang33sr_proposal_valid(proposal, chapter)
    if chapter.get('id') == 'c-nanshi-023-wangyu-jingwen':
        try: from scripts.nan023_wangyu import proposal_valid as nan23yu_proposal_valid
        except ImportError: from nan023_wangyu import proposal_valid as nan23yu_proposal_valid
        return nan23yu_proposal_valid(proposal, chapter)
    if chapter.get('id') == 'c-nanshi-023-wangmai':
        try: from scripts.nan023_wangmai import proposal_valid as nan23mai_proposal_valid
        except ImportError: from nan023_wangmai import proposal_valid as nan23mai_proposal_valid
        return nan23mai_proposal_valid(proposal, chapter)
    if chapter.get('id') == 'c-nanshi-023-wangtong-gongda':
        try: from scripts.nan023_wangtong import proposal_valid as nan23tong_proposal_valid
        except ImportError: from nan023_wangtong import proposal_valid as nan23tong_proposal_valid
        return nan23tong_proposal_valid(proposal, chapter)
    if chapter.get('id') == 'c-nanshi-023-wangxi-qian':
        try: from scripts.nan023_wangxi import proposal_valid as nan23xi_proposal_valid
        except ImportError: from nan023_wangxi import proposal_valid as nan23xi_proposal_valid
        return nan23xi_proposal_valid(proposal, chapter)
    if chapter.get('id') == 'c-nanshi-023-wanghui':
        try: from scripts.nan023_wanghui import proposal_valid as nan23hui_proposal_valid
        except ImportError: from nan023_wanghui import proposal_valid as nan23hui_proposal_valid
        return nan23hui_proposal_valid(proposal, chapter)
    if chapter.get('id') == 'c-nanshi-023-wangliang':
        try: from scripts.nan023_wangliang import proposal_valid as nan23liang_proposal_valid
        except ImportError: from nan023_wangliang import proposal_valid as nan23liang_proposal_valid
        return nan23liang_proposal_valid(proposal, chapter)
    if chapter.get('id') == 'c-nanshi-023-wangying-shi':
        try: from scripts.nan023_wangying import proposal_valid as nan23ying_proposal_valid
        except ImportError: from nan023_wangying import proposal_valid as nan23ying_proposal_valid
        return nan23ying_proposal_valid(proposal, chapter)
    if proposal.get('non_assumption_kind') == 'superseded_by_accepted_alternative':
        try: from scripts.song066_readings import proposed_valid
        except ImportError: from song066_readings import proposed_valid
        return proposed_valid(proposal, chapter)
    if chapter.get('id') == 'c-nanshi-023-wangdan-gu-yan-wyd':
        try: from scripts.nan023_print import proposal_valid as nan23p_proposal_valid
        except ImportError: from nan023_print import proposal_valid as nan23p_proposal_valid
        return nan23p_proposal_valid(proposal, chapter)
    if chapter.get('id') == 'c-nanshi-023-wangdan-gu-yan':
        try: from scripts.nan023_digital import proposal_valid as nan23dan_proposal_valid
        except ImportError: from nan023_digital import proposal_valid as nan23dan_proposal_valid
        return nan23dan_proposal_valid(proposal, chapter)
    if chapter.get('id') == 'c-songshu-052-wangdan':
        try: from scripts.song052_wangdan import proposal_valid as wangdan52_proposal_valid
        except ImportError: from song052_wangdan import proposal_valid as wangdan52_proposal_valid
        return wangdan52_proposal_valid(proposal, chapter)
    if chapter.get('id') == 'c-songshu-052-xieshu':
        try: from scripts.song052_xieshu import proposal_valid as xieshu52_proposal_valid
        except ImportError: from song052_xieshu import proposal_valid as xieshu52_proposal_valid
        return xieshu52_proposal_valid(proposal, chapter)
    if chapter.get('id') == 'c-liangshu-021-wangjian-sons-context':
        try: from scripts.liang021_wangjiansihui import proposal_valid as sih21_proposal_valid
        except ImportError: from liang021_wangjiansihui import proposal_valid as sih21_proposal_valid
        return sih21_proposal_valid(proposal, chapter)
    if chapter.get('id') == 'c-liangshu-021-wangfen':
        try: from scripts.liang021_wangfen_family import proposal_valid as wf21_proposal_valid
        except ImportError: from liang021_wangfen_family import proposal_valid as wf21_proposal_valid
        return wf21_proposal_valid(proposal, chapter)
    if chapter.get('id') == 'c-liangshu-021-wangjun-wangcong':
        try: from scripts.liang021_wangjun import proposal_valid as j21_proposal_valid
        except ImportError: from liang021_wangjun import proposal_valid as j21_proposal_valid
        return j21_proposal_valid(proposal, chapter)
    if chapter.get('id') == 'c-liangshu-021-wangtai-wangyun':
        try: from scripts.liang021_wangtai_readings import proposal_valid
        except ImportError: from liang021_wangtai_readings import proposal_valid
        return proposal_valid(proposal, chapter)
    if chapter.get('id') in ('c-liangshu-033-wangyun', 'c-liangshu-033-wangyun-wyd'):
        try: from scripts.liang033_wangyun_witness import declined_valid
        except ImportError: from liang033_wangyun_witness import declined_valid
        return declined_valid(proposal, chapter)
    if proposal.get('jin080_office_form') == 'summoned_and_declined':
        try: from scripts.jin080_xizhi import unassumed_valid
        except ImportError: from jin080_xizhi import unassumed_valid
        return unassumed_valid(proposal, chapter)
    if 'source_career_role' in proposal:
        try:
            from scripts.received_career_roles import unassumed_valid
        except ImportError:
            from received_career_roles import unassumed_valid
        return unassumed_valid(proposal, chapter)

    if 'resumed_decline_context' in proposal:
        try:
            from scripts.resumed_biography_lifecycle import declined_valid
        except ImportError:
            from resumed_biography_lifecycle import declined_valid
        return declined_valid(proposal, chapter)
    if 'elided_appointment_context' in proposal:
        try:
            from scripts.song047_title_semantics import elided_decline_valid
        except ImportError:
            from song047_title_semantics import elided_decline_valid
        return elided_decline_valid(proposal, chapter)
    if (proposal.get('proposal_kind') != 'unassumed_appointment' or proposal.get('outcome') != 'not_assumed'
            or proposal.get('status') != 'contextual_provisional' or proposal.get('human_reviewed') is not False
            or len(proposal.get('evidence', [])) != 1):
        return False
    e = proposal['evidence'][0]
    p = next((p for p in chapter.get('paragraphs', []) if p['id'] == e.get('paragraph_id')), None)
    if (not p or e.get('chapter_id') != chapter.get('id')
            or any(e.get(k) != chapter.get(k) for k in ['work_id', 'book_id', 'source_id'])):
        return False
    quote = e.get('quote')
    if not isinstance(quote, str) or not quote or quote not in p['text']:
        return False
    ms = {m['id']: m for m in p['mentions']}
    person, role = ms.get(proposal.get('person_mention_id')), unassumed_role(proposal, p)
    carried = False
    if e.get('context') is not None:
        try:
            from scripts.subject_continuation import prior_subject_valid
        except ModuleNotFoundError:
            from subject_continuation import prior_subject_valid
        context = e['context']
        carried = prior_subject_valid(context, e, proposal.get('person_id'), chapter)
        if not carried or context.get('person_mention_id') != proposal.get('person_mention_id'):
            return False
        prior = next(p for p in chapter['paragraphs'] if p['id'] == context['paragraph_id'])
        person = next((m for m in prior['mentions'] if m['id'] == context['person_mention_id']), None)
    if (not person or not role or person.get('kind') != 'person'
            or person.get('person_id') != proposal.get('person_id')
            or role.get('kind') != 'unresolved' or role.get('person_id') is not None
            or role.get('surface') != proposal.get('title')):
        return False
    def anchor(value):
        return (isinstance(value, dict) and set(value) == {'paragraph_id','start','end','surface'}
                and value.get('paragraph_id') == p['id'] and type(value.get('start')) is int
                and type(value.get('end')) is int and 0 <= value['start'] < value['end'] <= len(p['text'])
                and p['text'][value['start']:value['end']] == value.get('surface'))
    appointment, refusal = proposal.get('appointment_anchor'), proposal.get('non_assumption_anchor')
    if not anchor(appointment) or not anchor(refusal):
        return False
    verbs = ['進號','引為','引爲','召為','召爲','徙','遷','尋加','轉','除','改除','加','以為','征補','徵','徴','徵為','徵爲','命為','命爲','請為','請爲','補','辟','復除','又除','出為','出爲',
             '以'+person['surface']+'為','以'+person['surface']+'爲']
    terms = {'declined':['固辭不起','固辭開府','固辭不拜','以疾固辭，未行而卒','苦讓，遂不受','讓不拜','固讓不拜','固讓'],
             'did_not_take_up':['稱疾不起','並不行','未之職','不拜','皆不就','不就','並不就','竝不就','竝不拜','未拜','終以不拜','竟不拜','又不就']}
    if proposal.get('source_refusal_form') == 'jin044_returned_seal':
        text = p['text']; named = person['surface']
        subject_clause = '今以'+named+'為司空'
        if (p.get('source_position',{}).get('revision_id') != 1775345
                or named != '袤' or role['surface'] != '司空'
                or text.count(subject_clause) != 1 or appointment['start'] != text.index(subject_clause) + 1
                or role['start'] != text.index(subject_clause) + len(subject_clause)-2
                or text.count(named+'前後辭讓，遣息稱上送印綬')!=1
                or refusal['surface'] != '固辭，久之見許'
                or not text[refusal['end']:].startswith('，以侯就第，拜儀同三司')):
            return False
        terms['did_not_take_up'] = [*terms['did_not_take_up'], refusal['surface']]
    if proposal.get('source_refusal_form') == 'jin044_huaheng':
        fixed = {'光祿勳': ('即召恆，補光祿勳。恆到，未及拜，更以為衛將軍','補','未及拜'),
                 '護軍': ('王敦表轉恆為護軍，疾病不拜','轉','不拜'),
                 '左光祿大夫': ('遷左光祿大夫、開府，常侍如故，固讓未拜','遷','未拜'),
                 '開府': ('遷左光祿大夫、開府，常侍如故，固讓未拜','遷','未拜')}
        rule = fixed.get(role['surface'])
        if (not rule or p['source_position']['revision_id']!=1775345 or person['surface']!='恆'
                or p['text'].count(rule[0])!=1 or (appointment['surface'],refusal['surface'])!=rule[1:]):return False
        pos=p['text'].index(rule[0])
        return all(x['start']==pos+rule[0].index(x['surface']) and x['end']==x['start']+len(x['surface']) for x in [role,appointment,refusal])
    if proposal.get('source_refusal_form') == 'jin044_huaqiao':
        clause='出為安平太守。辭親老不行，更拜散騎常侍'
        if p['source_position']['revision_id']!=1775345 or p['text'].count(clause)!=1 or person['start']!=0 or person['surface']!='嶠':return False
        pos=p['text'].index(clause)
        return ((role['start'],role['surface'])==(pos+2,'安平太守') and (appointment['start'],appointment['surface'])==(pos,'出為') and (refusal['start'],refusal['surface'])==(pos+10,'不行'))
    if proposal.get('source_refusal_form') == 'jin043_shanjian':
        clause = '曆鎮軍將軍、荊州刺史，領南蠻校尉，不行'
        expected = {'鎮軍將軍':'曆', '荊州刺史':'曆', '南蠻校尉':'領'}
        term = expected.get(role['surface'])
        if (not term or p['id'] != 'c-jinshu-043-shanjian:line050' or p['source_position']['revision_id'] != 2618531
                or person['person_id'] != '82k_3oi_qf8' or (appointment['surface'], refusal['surface']) != (term, '不行')
                or p['text'].count(clause) != 1):
            return False
        pos = p['text'].index(clause)
        return all(x['start'] == pos+clause.index(x['surface']) and x['end'] == x['start']+len(x['surface'])
                   for x in (role, appointment, refusal))
    if proposal.get('source_refusal_form') == 'jin043_shantao':
        clause = '後除太常卿，以疾不就'
        return (p.get('source_position', {}).get('revision_id') == 2618531
                and p['id'] == 'c-jinshu-043-shantao:line023' and p['text'].startswith(clause)
                and person['person_id'] == '96a_987_925' and '濤年逾耳順' in p['text']
                and (role['start'], role['end'], role['surface']) == (2, 5, '太常卿')
                and (appointment['start'], appointment['end'], appointment['surface']) == (1, 2, '除')
                and (refusal['start'], refusal['end'], refusal['surface']) == (8, 10, '不就'))
    stage = proposal.get('appointment_stage')
    invitation = appointment['surface'] in ('請為', '請爲')
    if (stage not in (None, 'invitation', 'appointment')
            or invitation and stage != 'invitation'
            or stage == 'invitation' and not invitation):
        return False
    if appointment['surface'] == '征' and role['surface'] == '吏部郎' and p['text'][appointment['start']-5:refusal['end']] == '湣帝即位，征吏部郎，不拜':
        verbs = [*verbs, '征']
    if (appointment['surface'] == '領' and appointment['end'] == role['start']
            and p['text'][role['end']:refusal['start']] in ('', '，')
            and refusal['surface'] == '未拜'):
        verbs.append('領')
    if (appointment['surface'] in ('用為', '用爲') and appointment['end'] == role['start']
            and p['text'][role['end']:refusal['start']] in ('，', '') and refusal['surface'] == '固辭年老'
            and person['surface'] == '璟' and person['person_id'] == '684_eaa_511_AAA'
            and role['surface'] == '侍中' and p['text'][appointment['start']-2:appointment['start']] == '高祖'
            and chapter['id'] in ('c-liangshu-050-xiezheng', 'c-liangshu-050-xiezheng-wyd')):
        verbs.append(appointment['surface'])
        terms['declined'].append('固辭年老')
    postposed_summons = (appointment['surface'] in ('徵', '徴')
                        and appointment['start'] == role['end']
                        and appointment['end'] <= refusal['start'])
    if (appointment['surface'] not in verbs or refusal['surface'] not in terms.get(proposal.get('non_assumption_kind'), [])
            or (not carried and person['end'] > role['start'])
            or (appointment['end'] > role['start'] and not postposed_summons)
            or role['end'] > refusal['start']):
        return False
    if carried and 'source_continuity' in e['context']:
        if e['context']['source_continuity']['target_prefix_anchor']['end'] < refusal['end']:
            return False
    if refusal['surface'] == '固辭不起':
        try:
            from .jin_facts_boundaries import resumed_invitation_refusal_valid
        except ImportError:
            from jin_facts_boundaries import resumed_invitation_refusal_valid
        if not resumed_invitation_refusal_valid(proposal,p,person,role,appointment,refusal,carried):
            return False
    if refusal['surface'] == '稱疾不起':
        try:
            from .jin_facts_boundaries import grouped_non_assumption_valid
        except ImportError:
            from jin_facts_boundaries import grouped_non_assumption_valid
        if not grouped_non_assumption_valid(proposal, p, person, role, appointment, refusal, carried):
            return False
    if refusal['surface'] == '固辭不拜' and not full_declining_subject_valid(proposal, p, person, refusal):
        return False
    if refusal['surface'] == '固辭開府' and role['surface'] not in ('開府', '開府儀同三司'):
        return False
    if refusal['surface'] == '不拜' and refusal['start'] > 0 and p['text'][refusal['start']-1] in ('讓', '辭'):
        return False
    # A named prince inside 廬陵王師 is the patron, not another appointee.
    patrons = proposal.get('patron_person_mention_ids', [])
    patron_refs = proposal.get('patron_person_reference_ids', [])
    contextual_patrons = [
        r['id'] for r in chapter['annotation'].get('person_reference_occurrences', [])
        if r['paragraph_id'] == p['id'] and r.get('referent_role') == 'third_person'
        and r['person_id'] != proposal['person_id']
        and r['start'] == role['start'] and r['end'] == role['end'] - 1
        and role['surface'] == r['surface'] + '師'
    ]
    if patron_refs or contextual_patrons:
        if patrons or len(contextual_patrons) != 1 or patron_refs != contextual_patrons:
            return False
    if (not isinstance(patrons, list) or len(set(patrons)) != len(patrons)
            or any(mid not in ms for mid in patrons)):
        return False
    if patrons:
        if len(patrons) != 1:
            return False
        patron = ms[patrons[0]]
        if (patron.get('kind') != 'person' or patron.get('person_id') == proposal['person_id']
                or patron['start'] != role['start'] or patron['end'] >= role['end']
                or role['surface'] != patron['surface'] + '師'):
            return False
    # Other named recipients still cannot be silently bypassed.
    if any(m.get('kind') == 'person' and m.get('person_id') != proposal['person_id']
           and m['id'] not in patrons
           and appointment['end'] <= m['start'] < role['end'] for m in p['mentions']):
        return False
    return any(i <= (appointment['start'] if carried else min(person['start'], appointment['start'])) and refusal['end'] <= i + len(quote)
               for i in range(len(p['text'])) if p['text'].startswith(quote, i))



def full_declining_subject_valid(proposal, paragraph, person, refusal):
    """The new full phrase cannot hide a switched decliner inside a conversation."""
    scope = proposal.get('refusal_subject_scope')
    text = paragraph['text']
    if scope is None:
        segment = text[person['end']:refusal['start']]
        return ('曰' not in segment and not any(m.get('kind') == 'person'
                and m.get('person_id') != proposal['person_id']
                and person['end'] <= m['start'] < refusal['end'] for m in paragraph['mentions']))
    try:
        if (set(scope) != {'kind','subject_mention_id','speech_introducer_anchor','speech_anchor','resumption_anchor','human_reviewed'}
                or scope['kind'] != 'same_named_speaker_after_direct_speech' or scope['human_reviewed'] is not False):
            return False
        subject = next(m for m in paragraph['mentions'] if m['id'] == scope['subject_mention_id'])
        intro, speech, resumed = [scope[k] for k in ['speech_introducer_anchor','speech_anchor','resumption_anchor']]
        for a in (intro, speech, resumed):
            if (set(a) != {'paragraph_id','start','end','surface'} or a['paragraph_id'] != paragraph['id']
                    or type(a['start']) is not int or type(a['end']) is not int
                    or not 0 <= a['start'] < a['end'] <= len(text) or text[a['start']:a['end']] != a['surface']):
                return False
        role = unassumed_role(proposal, paragraph)
        return (role is not None and intro['start'] >= role['end']
                and subject.get('kind') == 'person' and subject.get('person_id') == proposal['person_id']
                and subject['start'] == intro['start'] and intro['surface'].startswith(subject['surface']+'謂')
                and intro['surface'].endswith('曰') and intro['end'] == speech['start']
                and speech['end'] == resumed['start'] and resumed['surface'] == '乃固辭不拜'
                and resumed['start']+1 == refusal['start'] and resumed['end'] == refusal['end']
                and not any(m.get('kind') == 'person' and m.get('person_id') != proposal['person_id']
                            and speech['end'] <= m['start'] < resumed['end'] for m in paragraph['mentions']))
    except (KeyError,TypeError,ValueError,StopIteration):
        return False
