"""Read the unnamed brother, his son and the two appointments as censor in Chen 23."""
try:
    from scripts.chenshu023_shenjunli import located, named
except ImportError:
    from chenshu023_shenjunli import located, named

CHAPTER = 'c-chenshu-023-lushan-complete'
SHAN = 'jss_82r_1ct_AAAA'
ELDER = 'jss_82r_1ct_AAAB'
JIANXIAN = 'jss_82r_1ct_AAABA'
NEPHEW = '繕兄子見賢，亦方雅'
DECLINED = '除司徒右長史，御史中丞，以父任所終，固辭不就。'


def fixed(p, e, chapter):
    return (chapter['id'] == CHAPTER and chapter['source']['revision_id'] == p['source_position']['revision_id'] == 1514496
            and p['id'] == e['paragraph_id'] and chapter['id'] == e['chapter_id']
            and chapter['source_id'] == e['source_id'] and p['text'] == e['quote'])


def family_valid(row, e, chapter):
    try:
        p=chapter['paragraphs'][5]
        if row['predicate'] == 'father':
            subject,other,side,field,person,word=JIANXIAN,ELDER,'object','subject_person_mention_id',JIANXIAN,'見賢'
        elif row['predicate'] == 'brother':
            subject,other,side,field,person,word=ELDER,SHAN,'subject','object_person_mention_id',SHAN,'繕'
        else:
            return False
        ref,=(r for r in chapter['annotation']['person_reference_occurrences'] if r['id'] == e[side+'_person_reference_id'])
        q=row['qualifiers']
        return (fixed(p,e,chapter) and row['subject_person_id'] == subject and row['object_person_id'] == other
                and row['status'] == 'source_attested' and q['source_term'] == '繕兄子見賢'
                and q['reading_basis']['kind'] == 'chen023_lu_nephew' and p['text'].startswith(NEPHEW)
                and ref['person_id'] == ELDER and ref['referent_role'] == 'third_person' and ref['paragraph_id'] == p['id']
                and located(ref,p,NEPHEW,'兄') and located(q['reading_basis']['role_anchor'],p,NEPHEW,'兄')
                and named(p,e,field,person,NEPHEW,word))
    except (KeyError,IndexError,TypeError,ValueError):
        return False


def proposal_valid(row, chapter):
    try:
        p=chapter['paragraphs'][1]
        e,=row['evidence']
        return (fixed(p,e,chapter) and row['title'] == '御史中丞' and row['person_id'] == SHAN
                and row['person_mention_id'] == e['person_mention_id']
                and row['proposal_kind'] == 'unassumed_appointment' and row['outcome'] == 'not_assumed'
                and row['appointment_stage'] == 'appointment' and row['non_assumption_kind'] == 'did_not_take_up'
                and named(p,e,'person_mention_id',SHAN,'繕幼有志尚','繕')
                and located(row['role_anchor'],p,DECLINED,'御史中丞')
                and located(row['appointment_anchor'],p,DECLINED,'除') and located(row['non_assumption_anchor'],p,DECLINED,'固辭不就'))
    except (KeyError,IndexError,TypeError,ValueError):
        return False
