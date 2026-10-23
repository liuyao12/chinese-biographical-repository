"""Editorial surname from one role-bound same-source paternal father/grandfather.
No assembly edge, structural ID, label, clan residence or inferred parent is used.
"""
import hashlib,re
KIND='contextual_surname_from_bound_paternal_ancestor'
def validate(name,names,chapters,assertions):
 try:
  b=name['surname_basis'];assert set(b)=={'kind','status','human_reviewed','rationale','source_name_record_id','assertion_id','source_role','generation_distance','evidence','source_frame'}
  assert b['kind']==KIND and b['status']=='contextual_provisional'and b['human_reviewed']is False and b['rationale'].strip()
  assert name['status']=='contextual_provisional'and name['human_reviewed']is False
  matches=[n for n in names if n.get('id')==b['source_name_record_id']];assert len(matches)==1;seed=matches[0]
  assert seed.get('surname')and seed.get('ming')and not seed.get('surname_basis')and seed['surname']==name['surname']and seed['chapter_id']==name['chapter_id']and seed['paragraph_id']==name['paragraph_id']
  c=chapters[name['chapter_id']];p=next(p for p in c['paragraphs']if p['id']==name['paragraph_id']);t=p['text'];assert p['text_layer']=='received_chapter'and name['quote']==seed['quote']==t
  def mark(mid,pid):
   z=[m for m in p['mentions']if m['id']==mid];assert len(z)==1;m=z[0];assert m['kind']=='person'and m['person_id']==pid and type(m['start'])is int and type(m['end'])is int and 0<=m['start']<m['end']<=len(t)and t[m['start']:m['end']]==m['surface'];return m
  s=mark(seed['person_mention_id'],seed['person_id']);target=mark(name['person_mention_id'],name['person_id']);assert s['start']==0 and s['surface']==seed['surname']+seed['ming']and re.match(r'^[，,]?字',t[s['end']:])and target['surface']==name['ming']and target['person_id']!=s['person_id']
  aa=[a for a in assertions if a['id']==b['assertion_id']];assert len(aa)==1;a=aa[0];role=b['source_role'];assert role in('father','grandfather')and b['generation_distance']=={'father':1,'grandfather':2}[role]and type(b['generation_distance'])is int
  assert a['predicate']==role and a['status']=='source_attested'and a['subject_person_id']==seed['person_id']and a['object_person_id']==name['person_id']and a['qualifiers']['lineage']=='paternal'and not a['qualifiers'].get('adoptive')
  e,=a['evidence'];assert b['evidence']==e and e['quote']==t and e['chapter_id']==c['id']and e['paragraph_id']==p['id']and e['source_id']==c['source_id']and e['work_id']==c['work_id']and e['book_id']==c['book_id']and e['subject_person_mention_id']==s['id']and e['object_person_mention_id']==target['id']
  binding=a['qualifiers']['source_clause_binding'];assert binding['rule']=='close_family_unpunctuated_head_grandfather_father'and binding['roles']['head']==s['id']and binding['roles'][role]==target['id']
  f=b['source_frame'];assert set(f)=={'source_revision','raw_sha256','paragraph_sha256'}and isinstance(f['source_revision'],str)and f['source_revision']and f['source_revision']==c['source']['revision_id']==binding['revision_id']
  assert isinstance(f['raw_sha256'],str)and re.fullmatch('[0-9a-f]{64}',f['raw_sha256'])and f['raw_sha256']==c['source']['raw_sha256']and f['paragraph_sha256']==hashlib.sha256(t.encode()).hexdigest()==binding['paragraph_sha256']
  try:from .biography_close_family import valid as source_valid
  except ImportError:from biography_close_family import valid as source_valid
  assert source_valid(a,{p['id']:(c['id'],p)})
 except(AssertionError,KeyError,StopIteration,TypeError,IndexError,ValueError,AttributeError):
  raise ValueError('Bound paternal surname requires one source-attested role-bound father/grandfather, exact full-name seed and complete same-source evidence; no assembly or ID inference')
