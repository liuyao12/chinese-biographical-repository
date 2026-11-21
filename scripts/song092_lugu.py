"""Derive Lu Gu's grandfather from the two named endpoints of Lu Xun's biography."""
def valid(a,e,c):
    if a.get('id')!='a-song092-lugu-chen' or a.get('predicate')!='grandfather' or c['id']!='c-jinshu-100-luxun-ancestry' or c['source']['revision_id']!=2614279:return False
    if len(a['evidence'])!=2 or len(c['paragraphs'])!=2 or e not in a['evidence']:return False
    first,last=c['paragraphs'];one,two=a['evidence']
    if [p['source_position']['first_line']for p in (first,last)]!=[143,151]:return False
    if (first['text']!='盧循，字於先，小名元龍，司空從事中郎諶之曾孫也。'
        or not last['text'].startswith('循勢屈，知不免') or not last['text'].endswith('因自投于水。慧度取其屍斬之，及其父嘏；同黨盡獲，傳首京都。')):return False
    if a['qualifiers']['source_term']!='諶之曾孫' or a['qualifiers'].get('lineage')!='paternal':return False
    if [(x['paragraph_id'],x['quote'])for x in (one,two)]!=[(p['id'],p['text'])for p in (first,last)]:return False
    def which(p,word,mid=None):
        rows=[m for m in p['mentions']if m['surface']==word and (mid is None or m['id']==mid) and p['text'][m['start']:m['end']]==word]
        return rows[0]['person_id'] if len(rows)==1 else None
    return (which(first,'盧循')==which(last,'循')=='m8n_ntm_79h_ABBA**A'
            and which(first,'諶',one['object_person_mention_id'])==a['object_person_id']=='m8n_ntm_79h_ABBA'
            and which(last,'嘏',two['subject_person_mention_id'])==a['subject_person_id']=='m8n_ntm_79h_ABBA*A')
