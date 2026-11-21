"""Verify the relationships expressly reported at the first three openings of Southern History 24."""
WANG='7r6_k52_qji_ABDABAA'
HE='7r6_k52_qji_ABDABAAD'
KONG='7r6_k52_qji_ABDABAAE'
WIFE='fml_n0s_qtz'
XUAN='u9s_w6j_8mc_AAF'
CASES={
 'wife':(15,'spouse','妻弟荊州刺史桓玄','敬弘少有清尚，起家本國左常侍、衞軍參軍。性恬靜，樂山水，求爲天門太守。及之郡，妻弟荊州刺史桓玄', (WIFE,39,'妻',False),(WANG,0,'敬弘',False)),
 'sister':(15,'sister','妻弟荊州刺史桓玄','妻弟荊州刺史桓玄遣信要令過己，敬弘至巴陵，謂人曰：「靈寶正當欲見其姊', (WIFE,39,'妻',False),(XUAN,45,'桓玄',False)),
 'he-father':(23,'father','女適尚書僕射何尚之弟述之','女適尚書僕射何尚之弟述之。敬弘嘗往何氏看女',(HE,103,'女',True),(WANG,116,'敬弘',False)),
 'he-marriage':(23,'spouse','女適尚書僕射何尚之弟述之','女適尚書僕射何尚之弟述之。敬弘嘗往何氏看女',(HE,103,'女',True),('6dq_9ln_mo9',113,'述之',False)),
 'kong-father':(23,'father','臣女幼','上將爲廬陵王納其女，辭曰：「臣女幼，既許孔淳之息。」',(KONG,198,'女',True),(WANG,197,'臣',True)),
}
def valid(a,e,ch):
    try:
        bit=a['qualifiers']['nanshi024_reported_kin']
        ln,kind,term,clause,subject,obj=CASES[bit]
        pid=f'c-nanshi-024-wang-family:line{ln:03}'
        p,=(p for p in ch['paragraphs'] if p['id']==pid)
        if (ch['id']!='c-nanshi-024-wang-family' or ch['source']['revision_id']!=1765279
                or e['paragraph_id']!=pid or e['chapter_id']!=ch['id'] or p['text']!=e['quote']
                or p['text'].count(clause)!=1 or a['qualifiers']['source_term']!=term or a['predicate']!=kind
                or a['status']!='source_attested' or len(a['evidence'])!=1):return False
        for side,(person,i,word,ref) in [('subject',subject),('object',obj)]:
            pool=ch['annotation']['person_reference_occurrences'] if ref else p['mentions']
            key=side+('_person_reference_id' if ref else '_person_mention_id')
            row,=(r for r in pool if r['id']==e[key])
            if (a[side+'_person_id']!=person or row['person_id']!=person or row['surface']!=word
                    or row['start']!=i or row['end']!=i+len(word) or p['text'][i:i+len(word)]!=word
                    or (ref and row['paragraph_id']!=pid) or (not ref and row['kind']!='person')):return False
        return True
    except (KeyError,TypeError,IndexError,ValueError):
        return False
