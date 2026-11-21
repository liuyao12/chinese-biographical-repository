"""Wang Gui's birth mother and younger paternal uncle in the same fixed biographical opening."""
from hashlib import sha256

def valid(claim,evidence,chapters,root):
    try:
        chapter=chapters[evidence['chapter_id']]
        if chapter['id']!='c-nanshi-022-wanggui' or chapter['source']['revision_id']!=1477957:
            return False
        p=next(p for p in chapter['paragraphs'] if p['id']==evidence['paragraph_id'])
        raw=(root/chapter['source']['raw_path']).read_bytes();text=p['text'];s=raw.decode()
        if (sha256(raw).hexdigest()!=chapter['source']['raw_file_sha256'] or
            text!=''.join(s[k] for k in p['source_position']['raw_character_offsets']) or text!=evidence['quote']):
            return False
        q=claim['qualifiers'];b=q['reading_basis'];mentions={m['id']:m for m in p['mentions'] if m['kind']=='person'}
        mentions.update({m['id']:m for m in chapter['annotation']['person_reference_occurrences'] if m['paragraph_id']==p['id']})
        sub=mentions[b['subject_anchor_id']];obj=mentions[b['object_anchor_id']]
        term,word={'mother':('所生母','所生母'),'paternal_uncle':('叔父暕','暕')}[claim['predicate']]
        return (text.startswith('規字威明，八歲丁所生母憂') and text.count(term)==1 and sub['start']==0 and sub['surface']=='規'
                and claim['subject_person_id']==sub['person_id'] and claim['object_person_id']==obj['person_id']
                and sub['person_id']!=obj['person_id'] and obj['surface']==word and q['source_term']==term
                and obj['end']==text.index(term)+len(term) and text[obj['start']:obj['end']]==word)
    except (KeyError,ValueError,IndexError,TypeError,StopIteration):return False
