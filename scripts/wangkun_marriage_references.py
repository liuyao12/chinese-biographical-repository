"""Recheck the two arranged marriages and subsequent wife's father against the fixed chapter."""
from hashlib import sha256


def valid(a, e, chapter, root):
    try:
        source = chapter['source'];raw = (root / source['raw_path']).read_bytes()
        if sha256(raw).hexdigest()!=source['raw_file_sha256'] or source['revision_id']!=2478204 or chapter['id']!='c-nanshi-023-wangkun':return False
        b=a['qualifiers']['reading_basis'];n=b['line'];p=next(p for p in chapter['paragraphs'] if p['id']==e['paragraph_id']);ls=raw.decode().splitlines();t=p['text'];tn=a['qualifiers']['source_term']
        if t!=ls[n-1] or t!=e['quote'] or e['source_id']!=chapter['source_id'] or e['chapter_id']!=chapter['id']:return False
        cases={(63,'樂玄女','father'):('女','樂玄','懌後娶南陽樂玄女，無子'),(63,'懌後娶南陽樂玄女','spouse'):('懌','女','懌後娶南陽樂玄女，無子'),(65,'嫁其二女，大女','father'):('大女','其','嫁其二女。華為琨娶大女'),(65,'嫁其二女，小女','father'):('小女','其','嫁其二女。華為琨娶大女，以小女適潁川庾敬度'),(65,'為琨娶大女','spouse'):('琨','大女','華為琨娶大女'),(65,'以小女適潁川庾敬度','spouse'):('庾敬度','小女','以小女適潁川庾敬度'),(69,'寵子新安王','father'):('新安王','上','上以琨忠實，徙為寵子新安王')}
        subject,obj,frame=cases[(n,b['case'],a['predicate'])];span=t.index(frame);end=span+len(frame); assert t.count(frame)==1 and tn in frame
        refs={r['id']:r for r in chapter['annotation']['person_reference_occurrences']if r['paragraph_id']==p['id']}; refs.update({m['id']:m for m in p['mentions']if m['kind']=='person'})
        for key,word in [('subject',subject),('object',obj)]:
            r=refs[b[key+'_anchor_id']]
            if not (r['surface']==word and r['person_id']==a[key+'_person_id'] and span<=r['start']<r['end']<=end and t[r['start']:r['end']]==word):return False
        return b['source_quote']==frame and b['start']==span and b['end']==end
    except (KeyError,IndexError,ValueError,StopIteration,AssertionError,TypeError):return False
