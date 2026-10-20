"""任用後未受或未赴任，與未實行的立號提議分開。"""


def unassumed_role(proposal, paragraph):
    role = next((m for m in paragraph.get('mentions', [])
                 if m['id'] == proposal.get('role_mention_id')), None)
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
    stage = proposal.get('appointment_stage')
    invitation = appointment['surface'] in ('請為', '請爲')
    if (stage not in (None, 'invitation', 'appointment')
            or invitation and stage != 'invitation'
            or stage == 'invitation' and not invitation):
        return False
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
