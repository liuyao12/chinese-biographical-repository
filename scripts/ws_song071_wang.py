"""《宋書》卷七十一固定數位修訂的親屬證據與身後贈諡。"""
import hashlib
import json
from pathlib import Path
try:
    from scripts.fixed_wikisource_units import source_errors
except ImportError:
    from fixed_wikisource_units import source_errors

CID = 'c-songshu-071-wangsengchuo-ws'
SID = 's-songshu-071-wangsengchuo-ws2485515'
PROOF = 'source-evidence/song071-wang/ws2485515-unit.json'
RAW = 'sources/witnesses/song071-ws2485515.wikitext'
FRAMES = 'source-evidence/song071-wang/ws-kinship-frames.json'
PROOF_SHA = 'f8ebab1af434f2bcd1805fb4cd31912e899b449629391729c60a1828934a873d'
RAW_SHA = '271e5293fbe7a8cd22a724319792d4fd87887c8e245cf84ca64daf6595528d57'
FRAMES_SHA = '35f93e63523e8677e85c1e2b0c3308ae15ad9b8dde1173366d929eb9eb8c1bb1'

def checked(root, path, digest):
    base = Path(root).resolve()
    file = base / path
    if file.resolve() != file or hashlib.sha256(file.read_bytes()).hexdigest() != digest:
        raise ValueError('固定來源雜湊不合')
    return file

def errors(ch, root):
    if ch.get('id') != CID:
        return []
    try:
        checked(root, PROOF, PROOF_SHA)
        checked(root, RAW, RAW_SHA)
        if (ch['source_id'] != SID or ch['source']['revision_id'] != 2485515
                or ch['source']['raw_path'] != RAW or ch['annotation']['fixed_wikisource_unit_ref'] != PROOF
                or ch['source']['image_verified'] is not False):
            raise ValueError('修訂或來源憑據')
        if ch['annotation']['human_reviewed'] is not False:
            raise ValueError('覆核層')
        return source_errors(ch, root)
    except (KeyError, ValueError, TypeError, OSError):
        return ['宋書卷71固定數位本與原卷修訂或逐字投影不合']

def kin_valid(a, ch, root):
    try:
        if ch['id'] != CID or errors(ch, root):
            return False
        k = a['qualifiers']['ws_song071_kin_frame']
        frame = json.loads(checked(root, FRAMES, FRAMES_SHA).read_text())[k]
        if (a['id'] != 'a-song071-ws-' + k or a['predicate'] != frame['predicate']
                or a['qualifiers']['source_term'] != frame['term'] or a['status'] != 'source_attested'):
            return False
        paragraphs = {p['id']: p for p in ch['paragraphs']}
        evidence = {}
        for role in frame['roles']:
            field, pid, clause, surface, person = (role[x] for x in ('field','paragraph_id','clause','surface','person_id'))
            p = paragraphs[pid]
            if p['text'].count(clause) != 1 or clause.count(surface) != 1:
                return False
            i = p['text'].index(clause) + clause.index(surface)
            if field.endswith('_reference_id'):
                hits = [r for r in ch['annotation']['person_reference_occurrences']
                        if r['paragraph_id'] == pid and r['referent_role'] == 'third_person']
            else:
                hits = [m for m in p['mentions'] if m['kind'] == 'person']
            hit, = [m for m in hits if m['start'] == i and m['end'] == i + len(surface) and m['surface'] == surface]
            if hit['person_id'] != person or a[field.split('_')[0] + '_person_id'] != person:
                return False
            ev = evidence.setdefault(pid,dict(work_id='w-songshu',book_id='b-songshu-071',source_id=SID,
                                             chapter_id=CID,paragraph_id=pid,quote=p['text']))
            ev[field] = hit['id']
        return a['evidence'] == list(evidence.values())
    except (KeyError, IndexError, ValueError, TypeError, OSError):
        return False

WANG = '7r6_k52_qji_ABAAAAEA'
EMPEROR = 'hx8_st4_jdd'

def award_valid(h,ch,events,root):
    try:
        if ch['id']!=CID or errors(ch,root):return False
        mode,term,kind={
            '散騎常侍':('posthumous_grant','追贈散騎常侍、金紫光祿大夫','office'),
            '金紫光祿大夫':('posthumous_grant','追贈散騎常侍、金紫光祿大夫','office'),
            '愍侯':('posthumous_naming','諡曰愍侯','honorific'),
        }[h['title']]
        b=h['naming_basis' if mode=='posthumous_naming' else 'posthumous_basis']
        p=ch['paragraphs'][3];text=p['text'];e,=h['evidence'];t,=h['attestations']
        def anchor(word):
            i=text.index(word)
            return dict(paragraph_id=p['id'],start=i,end=i+len(word),surface=word)
        d=events[b['death_event_id']]
        m,=(m for m in p['mentions'] if m['surface']=='僧綽' and m['start']==text.index('得僧綽所啟')+1)
        r,=(r for r in ch['annotation']['person_reference_occurrences'] if r['paragraph_id']==p['id']
            and r['start']==text.index('世祖即位') and r['surface']=='世祖')
        return (h['person_id']==m['person_id']==d['person_id']==WANG and r['person_id']==EMPEROR
                and b['recipient_person_mention_id']==t['person_mention_id']==e['person_mention_id']==m['id']
                and b['issuer_person_reference_id']==r['id'] and b['kind']=='song071_ws_wang_posthumous_awards'
                and (h['mode'],h['kind'],h['status'])==(mode,kind,'source_attested')
                and b['evidence']==d['evidence']==[e] and d['id']=='le-song071-ws-sengchuo'
                and d['status']=='source_attested' and d['source_anchor']==anchor('收害')
                and b['source_term']==term and b['source_anchor']==anchor(term)
                and e['quote']==text and e['source_id']==SID and e['chapter_id']==CID and e['paragraph_id']==p['id']
                and t['usage']=='posthumous_usage' and all(t[k]==v for k,v in anchor(h['title']).items())
                and h['effective_period']['start']==dict(status='source_event',event_type=mode,date_expression=None,evidence=[e]))
    except (KeyError,ValueError,TypeError,OSError):
        return False
