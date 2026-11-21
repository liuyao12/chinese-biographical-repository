"""Verify the Shi family readings against the separate museum accession and column."""
from hashlib import sha256
from pathlib import Path

RULES = {
    '新00013648': [
        ('father','侍中太尉昌安元公第二子也','石尠','侍中太尉昌安元公'),
        ('father','長子定','定','石尠'),('father','小子邁','邁','石尠'),
        ('father','庶子恭嗣','恭','石尠'),('father','女字令脩','令脩','石尠'),
        ('spouse','夫人廣平臨水劉氏','石尠','阿容'),('spouse','夫人琅邪陽都諸葛氏','石尠','男姊'),
        ('father','阿容父字世穎','阿容','世穎'),('father','男姊父字長茂','男姊','長茂'),
        ('spouse','女字令脩適黃門侍郎江安侯穎川陳世範','令脩','陳世範')],
    '新00013649': [('grandfather','太尉昌安元公之第三孫','石定','太尉昌安元公'),
        ('father','尚書城陽鄉侯之適子也','石定','尚書城陽鄉侯'),
        ('brother','定與弟邁','邁','定'),('spouse','妻沛國劉氏','石定','貴華'),
        ('father','貴華父字終嘏','貴華','終嘏')]}
def role(a,e,c):
    p, = c['paragraphs']; t=p['text']; q=a['qualifiers']; accession=c['source']['accession']
    if e['quote']!=t or e['chapter_id']!=c['id'] or e['source_id']!=c['source_id'] or e['paragraph_id']!=p['id']:return False
    names={m['id']:m for m in p['mentions'] if m['kind']=='person'}
    refs={r['id']:r for r in c['annotation']['person_reference_occurrences'] if r['paragraph_id']==p['id'] and r['referent_role']=='third_person'}
    s=names[e['subject_person_mention_id']];o=refs[e['object_reference_id']] if 'object_reference_id' in e else names[e['object_person_mention_id']]
    term=q['source_term']
    return ((a['predicate'],term,s['surface'],o['surface']) in RULES[accession]
            and a['subject_person_id']==s['person_id'] and a['object_person_id']==o['person_id']
            and t[s['start']:s['end']]==s['surface'] and t[o['start']:o['end']]==o['surface']
            and t.count(term)==1 and q['stone_reading']==dict(kind='shijian_rubbing_kin',accession=accession))
def assertion_valid(a,e,c,chapters):
    try:
        if not role(a,e,c):return False
        if not e.get('object_reference_id'):return True
        obj=next(r for r in c['annotation']['person_reference_occurrences']if r['id']==e['object_reference_id'])
        if '昌安元公' in obj['surface']:
            book=chapters['c-jinshu-044-shijian'];p=book['paragraphs'][0]
            return any(m['surface']=='石鑒' and m['start']==0 and m['person_id']==a['object_person_id']for m in p['mentions'])and '封昌安縣侯' in book['paragraphs'][1]['text']and '諡曰元' in book['paragraphs'][1]['text']
        mate=chapters['c-epitaph-shixian-excerpts']['paragraphs'][0]
        return obj['surface']=='尚書城陽鄉侯' and '尚書征虜將軍幽州刺史城陽簡侯' in mate['text'] and '長子定字庶公' in mate['text'] and any(m['surface']=='石尠'and m['person_id']==a['object_person_id']for m in mate['mentions'])and any(m['surface']=='庶公'and m['person_id']==a['subject_person_id']for m in mate['mentions'])
    except (KeyError,StopIteration,TypeError,ValueError):return False
def validate(c,rs,b):
    p,=c['paragraphs'];src=c['source'];t=p['text'];acc=src['accession']
    assert acc in RULES and b['accession']==acc and b['paragraph_sha256']==sha256(t.encode()).hexdigest() and src['image_verified']is True
    assert sha256(t.encode()).hexdigest()==HASHES[acc]
    assert c['source']['transcription_witness']['kind']=='rubbing_reproduction_excerpts'
    assert {k['representation']for k in src['image_witnesses']}=={'rubbing_reproduction','collection_object_photograph'}
    assert len(src['image_witnesses'])==(5 if acc=='新00013648' else 2)
    bound=[];urls={k['face']:k['url']for k in src['image_witnesses']}
    for row in src['column_positions']:
        assert row['column_from_right']>0 and row['image_url']==urls[row['face']]
        assert t[row['start']:row['end']]==row['text']
        bound.extend(range(row['start'],row['end']))
    assert bound==[i for i,char in enumerate(t)if char!='\n']
    by={rec['record_type']:rec for rec in rs}
    aa=by['person_assertion_set']['assertions'];assert len(aa)==len(RULES[acc])
    assert {a['qualifiers']['source_term']for a in aa}=={r[1]for r in RULES[acc]}
    assert all(len(a['evidence'])==1 and role(a,a['evidence'][0],c)for a in aa)
    de=by['person_life_event_assertion_set']['events'];assert all(a['event_type']=='death' and a['date_expression']=='七日' and a['source_term'] in t and a['evidence'][0]['quote']==t for a in de)
    bu,=by['person_event_assertion_set']['events'];assert bu['event_type']=='burial' and bu['date_expression']=='二年七月十九日' and bu['source_term'] in t
    n={m['surface']:m['person_id']for m in p['mentions']if m['kind']=='person'}
    assert bu['person_id']==n['石尠'if acc=='新00013648'else'石定']
    assert {a['person_id']for a in de}==({n['石尠']}if acc=='新00013648'else {n['石定'],n['邁']})

HASHES = {'新00013649': '1057397366963af09d8b97f05de1b44a45c497596d6032edc1253c42ac0d9f32', '新00013648': '599e77e7da139e2142c4ef93dc8c74ed2f875f8a71361eac7063fe8b23dd8146'}
