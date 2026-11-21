"""Verify the name anchors and the intervening transmitted lines for 石碏 and 其子厚."""
from hashlib import sha256
import re
def valid(a,c,root):
    try:
        s=c['source'];data=(root/s['raw_path']).read_bytes();text=data.decode()
        if c['id']!='c-zuozhuan-zhushu-002-jin076-roll-close' or s['revision_id']!=2689999 or sha256(data).hexdigest()!=s['raw_file_sha256']:return False
        child,names=c['paragraphs'];ev_name,ev_child=a['evidence']
        if (a['predicate']!='father' or a['qualifiers']!={'source_term':'其子厚','reading_basis':{'kind':'jin076_shihou'}} or
                child['text']!='其子厚與州吁游，禁之，不可。' or names['text']!='石碏使其宰獳羊肩涖殺石厚于陳。'):
            return False
        for p,e in [(child,ev_child),(names,ev_name)]:
            q=p['source_quote'];lo,hi=q['raw_start'],q['raw_end']
            if e['chapter_id']!=c['id'] or e['paragraph_id']!=p['id'] or text[lo:hi]!=q['quote'] or e['quote']!=p['text'] or q['quote']!=p['text']:return False
        # Recover the transmitted context while keeping the physically interleaved commentary out.
        lo=text.rindex('石碏諫曰：',0,child['source_quote']['raw_start']);hi=child['source_quote']['raw_end']
        lo=text.rindex('{{+|',0,lo);received=''.join(re.findall(r'^\{\{\+\|([^{}]+)\}\}',text[lo:text.index('}}',hi)+2],re.M))
        if not ('石碏諫曰：「臣聞愛子，教之以義方，'in received and '弗聽。其子厚與州吁游，禁之，不可。'in received):return False
        for p,form,field,e,anchor in [(names,'石碏','object',ev_name,'object_person_mention_id'),(names,'石厚','subject',ev_name,'subject_person_mention_id'),(child,'厚','subject',ev_child,'person_mention_id')]:
            m=next(m for m in p['mentions']if m['id']==e[anchor]);start=p['text'].index(form)
            if (m['kind'],m['person_id'],m['start'],m['end'],m['surface'])!=('person',a[field+'_person_id'],start,start+len(form),form):return False
        return a['subject_person_id']!=a['object_person_id']
    except (ValueError,TypeError,KeyError,IndexError,StopIteration,OSError):return False
