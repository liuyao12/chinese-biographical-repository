"""Validate the shared 令 in the received clause 歷餘姚、錢塘令."""
import hashlib
from pathlib import Path

def valid(holding, chapter, root):
    try:
        source=chapter['source']
        if chapter['book_id']!='b-liangshu-050' or source['revision_id']!=1514482:
            return False
        raw=(Path(root)/source['raw_path']).read_bytes()
        if hashlib.sha256(raw).hexdigest()!=source['raw_file_sha256']:
            return False
        text=raw.decode().splitlines()[78].removeprefix('　　')
        clause='歷餘姚、錢塘令，並以放免。'
        p=next(p for p in chapter['paragraphs'] if p['source_position']['first_line']==79)
        a,=holding['attestations']
        first=chapter['paragraphs'][0]['mentions'][0]
        person=next(m for m in p['mentions'] if m['id']==a['person_mention_id'])
        origin=text.index(clause)
        return (text==p['text'] and text.count(clause)==1 and
                first['surface']=='王籍' and first['start']==0 and person['surface']=='籍' and
                first['person_id']==person['person_id']==holding['person_id'] and
                a['paragraph_id']==p['id'] and a['surface']=='餘姚' and
                (a['start'],a['end'])==(origin+1,origin+3) and
                holding['title']==a['surface']+text[origin+6] and
                holding['shared_title_suffix']==dict(kind='liang050_received_county_pair',
                    paragraph_id=p['id'],start=origin+6,end=origin+7,surface='令',
                    source_clause=clause) and holding['kind']=='office')
    except (KeyError,ValueError,StopIteration,OSError,IndexError,TypeError):
        return False
