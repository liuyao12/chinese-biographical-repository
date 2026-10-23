"""Complete epitaph name introduction followed by titled grandfather/father clauses."""
import hashlib,re
KIND='epitaph_named_head_titled_ancestors'
def valid(c,rs,b):
 assert set(b)=={'kind','paragraph_id','source_id','paragraph_sha256','roles'} and b['kind']==KIND
 p,=c['paragraphs'];t=p['text'];assert p['text_layer']=='epitaph_as_modernly_transcribed'
 assert b['paragraph_id']==p['id'] and b['source_id']==c['source_id'] and b['paragraph_sha256']==hashlib.sha256(t.encode()).hexdigest()
 w=c['source']['transcription_witness'];assert w['kind']=='institutional_database_epitaph_transcription' and w['original_stone_or_rubbing_image_verified'] is False
 ms={m['id']:m for m in p['mentions']};assert set(b['roles'])=={'surname','head','zi','grandfather','grandchild','father','son'}
 roles={k:ms[v]for k,v in b['roles'].items()}
 for m in roles.values():assert m['kind']=='person' and m.get('person_id') and t[m['start']:m['end']]==m['surface']
 S=lambda k:roles[k]['surface'];I=lambda k:roles[k]['person_id']
 assert len({I(k)for k in ('head','father','grandfather')})==3
 assert all(I(k)==I('head')for k in ('surname','zi','grandchild','son'))
 # Every role is positioned by the complete introduction, never by nearest title/name.
 pre=r'(?P<title>[^。非不未無]+)墓誌銘。君姓(?P<surname>[^，。非不未無]+)，諱(?P<head>[^，。非不未無]+)，字(?P<zi>[^，。非不未無]+)，(?P<origin>[^。非不未無]+人也)。(?P<grandfather>[^，。非不未無]+府君)之(?P<grandchild>孫)，(?P<father>[^，。非不未無]+公)之(?P<son>第(?P<number>[一二三四五六七八九十]+)子)。'
 hit=re.match(pre,t);assert hit
 for k in roles:assert S(k)==hit[k] and (roles[k]['start'],roles[k]['end'])==hit.span(k)
 try:from scripts.validate_corpus import source_age_number
 except ImportError:from validate_corpus import source_age_number
 ordinal=source_age_number(hit['number']);assert type(ordinal)is int and ordinal>0
 assert all(r['record_type']=='person_assertion_set'for r in rs)
 aa=[a for r in rs for a in r['assertions']];assert len(aa)==2
 expected={'father':('father','son'),'grandfather':('grandfather','grandchild')}
 for a in aa:
  role,term=expected.pop(a['predicate']);q=a['qualifiers'];assert a['subject_person_id']==I('head') and a['object_person_id']==I(role)
  assert a['status']=='source_attested' and a['human_reviewed'] is False
  extra={'birth_order':{'parent_person_id':I('father'),'scope':'sons_of_parent','ordinal':ordinal,'position':'unspecified','interpretation_status':'source_attested'}} if role=='father' else {'lineage':'paternal','generation_difference':-2}
  assert q=={'source_term':S(term),'source_clause_binding':b,**extra}
  e,=a['evidence'];assert e=={'work_id':c['work_id'],'book_id':c['book_id'],'source_id':c['source_id'],'chapter_id':c['id'],'paragraph_id':p['id'],'quote':t,'subject_person_mention_id':roles[term]['id'],'object_person_mention_id':roles[role]['id']}
