"""陶淵明孟府君傳所錄的三代、兩個未具名女子與親屬人稱。"""
import hashlib

def context_valid(context, evidence, person_id, chapter):
    if context.get('kind') != 'tao_meng_death_subject' or context.get('person_id') != person_id or chapter.get('id') != 'c-taoyuanmingji-006-jin098-mengjia':
        return False
    try:
        head, later = (next(p for p in chapter['paragraphs'] if p['id'] == key) for key in (context['head_paragraph_id'], evidence['paragraph_id']))
        named = next(m for m in head['mentions'] if m['id'] == context['name_mention_id'])
        referred = next(r for r in chapter['annotation']['person_reference_occurrences'] if r['id'] == context['person_reference_id'])
        return (named['person_id'] == referred['person_id'] == person_id and named['surface']=='嘉' and head['text'].startswith('君諱嘉，字萬年')
                and later['id'].endswith(':last-illness') and referred['paragraph_id'] == later['id']
                and later['text'][referred['start']:referred['end']] == referred['surface'] == '君'
                and later['text'].startswith('溫從容謂君曰') and later['text'].endswith('後以疾終於家，年五十一。')
                and evidence['chapter_id']==chapter['id'] and evidence['source_id']==chapter['source_id'] and evidence['quote']==later['text'])
    except (KeyError, TypeError, StopIteration):
        return False

def kin_valid(assertion, evidence, chapter, root):
    try:
        q=assertion['qualifiers'];term=q['source_term'];p=next(p for p in chapter['paragraphs'] if p['id']==evidence['paragraph_id'])
        if chapter['id']!='c-taoyuanmingji-006-jin098-mengjia' or evidence['chapter_id']!=chapter['id'] or evidence['source_id']!=chapter['source_id'] or evidence['quote']!=p['text']:
            return False
        raw=(root/chapter['source']['raw_path']).read_bytes();aq=p['source_quote']
        if hashlib.sha256(raw).hexdigest()!=chapter['source']['raw_file_sha256'] or raw.decode()[aq['raw_start']:aq['raw_end']]!=aq['quote']:return False
        refs={r['id']:r for r in chapter['annotation']['person_reference_occurrences'] if r['paragraph_id']==p['id']};names={m['id']:m for m in p['mentions'] if m['kind']=='person'}
        def anchor(side):
            rid=evidence.get(side+'_person_reference_id');result=refs[rid] if rid is not None else names[evidence[side+'_person_mention_id']]
            if p['text'][result['start']:result['end']]!=result['surface'] or result['person_id']!=assertion[side+'_person_id']:raise ValueError
            return result['surface']
        s,o=anchor('subject'),anchor('object')
        if p['id'].endswith(':marriage'):
            return (p['text']=='君少失父，奉母、二弟居。娶大司馬長沙桓公陶侃第十女，' and ((assertion['predicate'],s,o,term) in
                    [('spouse','君','第十女','娶大司馬長沙桓公陶侃第十女'),('father','第十女','陶侃','陶侃第十女')]))
        return (p['id'].endswith(':author') and p['text']=='淵明先親，君之第四女也。' and
                (assertion['predicate'],s,o,term) in [('mother','淵明','先親','先親，君之第四女也'),('father','第四女','君','君之第四女')])
    except (KeyError,TypeError,ValueError,StopIteration,OSError):
        return False
