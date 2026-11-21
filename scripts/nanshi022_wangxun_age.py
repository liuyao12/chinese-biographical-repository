"""Age sixteen resumes the preceding explicitly stated age thirteen in Wang Xun's account."""
from hashlib import sha256
def valid(age, chapter, root):
    try:
        if (chapter['id']!='c-nanshi-022-wangxun' or chapter['source']['revision_id']!=1477957
                or age['age_context']!={'kind':'during_life'} or age['value']!=16
                or age['source_number']!=age['source_term'] or age['source_term']!='十六'):
            return False
        event=age['elliptical_age_basis'];e,=age['evidence']
        p=next(p for p in chapter['paragraphs']if p['id']==e['paragraph_id']);t=p['text'];raw=(root/chapter['source']['raw_path']).read_bytes();s=raw.decode();word='年十三，暕亡，憂毀，家人莫識。十六召見文德殿'
        source=next(a for a in chapter['annotation']['age_assertions']if a['id']==event['preceding_age_id'])
        m=next(m for m in p['mentions']if m['id']==e['person_mention_id'])
        return (sha256(raw).hexdigest()==chapter['source']['raw_file_sha256'] and
                t==''.join(s[k]for k in p['source_position']['raw_character_offsets']) and t.count(word)==1
                and event['source_clause']==word and m['person_id']==age['person_id']==source['person_id']
                and source['value']==13 and source['source_term']=='年十三' and e['quote']==t
                and source['evidence'][0]['paragraph_id']==p['id'] and e['chapter_id']==chapter['id'])
    except (ValueError,TypeError,IndexError,KeyError,StopIteration):return False
