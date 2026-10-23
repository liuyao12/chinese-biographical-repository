"""Source-bound surname reading across complete units of one fixed received witness.
No structural ID, assembly edge, label, surname guess or NLU is consulted.
"""
from pathlib import Path
import json,hashlib,re
KIND='contextual_surname_from_bound_received_family_units'

def validate(name,names,chapters,assertions,root):
 try:
  assert root is not None;root=Path(root).resolve();b=name['surname_basis']
  assert set(b)=={'kind','status','human_reviewed','rationale','source_name_record_id','source_full_quote','source_units','seed_frame','steps'}and b['kind']==KIND and b['status']=='contextual_provisional'and b['human_reviewed']is False and b['rationale'].strip()and name['status']=='contextual_provisional'and name['human_reviewed']is False
  try:from .fixed_wikisource_units import source_errors,unit_numbered_son_valid
  except ImportError:from fixed_wikisource_units import source_errors,unit_numbered_son_valid
  units=b['source_units'];assert isinstance(units,list)and 1<=len(units)<=3;cs={};ps={};frames=[]
  for u in units:
   assert set(u)=={'chapter_id','native_path','work_id','book_id','source_id','source_revision','raw_path','raw_file_sha256'}
   rel=Path(u['native_path']);q=root/rel;assert not rel.is_absolute()and rel.parts[0]=='corpus'and'..'not in rel.parts and q.resolve()==q and q.is_file()
   ch=chapters[u['chapter_id']];assert ch==json.loads(q.read_bytes())and ch['id']not in cs and ch['annotation'].get('fixed_wikisource_unit_ref')and not source_errors(ch,root)
   s=ch['source'];assert all(u[k]==ch[k]for k in('work_id','book_id','source_id'))and u['source_revision']==s['revision_id']and u['raw_path']==s['raw_path']and u['raw_file_sha256']==s['raw_file_sha256']
   frames.append((u['work_id'],u['book_id'],u['source_revision'],u['raw_file_sha256']));cs[ch['id']]=ch
   for p in ch['paragraphs']:assert p['id']not in ps;ps[p['id']]=(ch,p)
  assert len(set(frames))==1
  def frame(f):
   assert set(f)=={'chapter_id','paragraph_id','paragraph_sha256','source_revision','raw_sha256'};c,p=ps[f['paragraph_id']];assert f['chapter_id']==c['id']and f['source_revision']==c['source']['revision_id']==p['source_position']['revision_id']and f['raw_sha256']==c['source']['raw_file_sha256']and f['paragraph_sha256']==hashlib.sha256(p['text'].encode()).hexdigest()and p['text_layer']=='received_chapter';return c,p
  def mark(p,mid,pid):
   m,=[m for m in p['mentions']if m['id']==mid];assert m['kind']=='person'and m['person_id']==pid and type(m['start'])is int and type(m['end'])is int and 0<=m['start']<m['end']<=len(p['text'])and p['text'][m['start']:m['end']]==m['surface'];return m
  def outside(p,a,z):
   pre=p['text'][:a];assert pre.count('「')==pre.count('」')and pre.count('『')==pre.count('』')and not any(x in p['text'][a:z]for x in '「」『』')
  seed,=[n for n in names if n.get('id')==b['source_name_record_id']];assert not seed.get('surname_basis')and seed['surname']and seed['ming']and seed['surname']==name['surname'];sc,sp=frame(b['seed_frame']);assert seed['chapter_id']==sc['id']and seed['paragraph_id']==sp['id']and seed['quote']==sp['text']==b['source_full_quote'];sm=mark(sp,seed['person_mention_id'],seed['person_id']);assert sm['surface']==seed['surname']+seed['ming']
  tc,tp=ps[name['paragraph_id']];assert tc['id']==name['chapter_id']and name['quote']==tp['text'];tm=mark(tp,name['person_mention_id'],name['person_id']);assert tm['surface']==name['ming']
  aa={a['id']:a for a in assertions};assert len(aa)==len(assertions);steps=b['steps'];assert isinstance(steps,list)and 1<=len(steps)<=5;current=seed['person_id'];seen={current};used=set();generation=0
  for step in steps:
   assert set(step)=={'assertion_id','from_person_id','to_person_id','traversal','generation_before','generation_after','evidence','source_frames','role_binding'}and step['assertion_id']not in used and step['from_person_id']==current and step['to_person_id']not in seen
   a=aa[step['assertion_id']];q=a['qualifiers'];assert a['status']=='source_attested'and not q.get('adoptive')and not q.get('sworn')and not q.get('same_mother_only')and q.get('shared_father')is not False and q.get('lineage')not in('maternal','non_paternal')and step['evidence']==a['evidence']and type(step['generation_before'])is int and type(step['generation_after'])is int and step['generation_before']==generation
   fs=step['source_frames'];assert len(fs)==len({e['paragraph_id']for e in a['evidence']})and {f['paragraph_id']for f in fs}=={e['paragraph_id']for e in a['evidence']}
   for f in fs:frame(f)
   for e in a['evidence']:
    c,p=ps[e['paragraph_id']];assert all(e[k]==c[k]for k in('work_id','book_id','source_id'))and e['chapter_id']==c['id']and e['quote']==p['text']
   role=step['role_binding'];dest=step['to_person_id']
   if step['traversal']=='older_to_younger':
    assert a['predicate']=='brother'and a['object_person_id']==current and a['subject_person_id']==dest and step['generation_after']==generation
    e,=a['evidence'];c,p=ps[e['paragraph_id']];old=mark(p,e['object_person_mention_id'],current);young=mark(p,e['subject_person_mention_id'],dest)
    if role=={'kind':'named_older_di_younger'}:
     try:from .named_family_offices import sibling_order_valid
     except ImportError:from named_family_offices import sibling_order_valid
     assert q['source_clause_binding']['kind']=='named_older_di_younger'and sibling_order_valid(a,{p['id']:(c['id'],p)})
    else:
     assert set(role)=={'kind','source_anchor'}and role['kind']=='literal_named_younger_xiong_older';anchor=role['source_anchor'];assert anchor=={'paragraph_id':p['id'],'start':young['start'],'end':old['end'],'surface':young['surface']+'兄'+old['surface']}and p['text'][young['end']:old['start']]=='兄'and q['source_term']==anchor['surface'];outside(p,young['start'],old['end']);assert young['start']==0 or p['text'][young['start']-1]in '，。；'
     order=q['relative_birth_order'];assert order['older_person_id']==current and order['younger_person_id']==dest and order['operator']=='lt'
   elif step['traversal']=='father_to_child':
    assert a['predicate']=='father'and a['object_person_id']==current and a['subject_person_id']==dest and step['generation_after']==generation+1
    if role=={'kind':'named_parent_sending_numbered_son'}:assert unit_numbered_son_valid(a,{pid:(c['id'],p)for pid,(c,p)in ps.items()},cs,root)
    else:
     assert role=={'kind':'adjacent_biography_named_subject_son'};pe,ce=a['evidence'];pc,pp=ps[pe['paragraph_id']];cc,cp=ps[ce['paragraph_id']];assert pc['id']==cc['id'];ordered=[p['id']for p in pc['paragraphs']];assert ordered.index(cp['id'])==ordered.index(pp['id'])+1
     ctx=a['context'];assert ctx['kind']=='adjacent_paragraphs'and ctx['status']=='contextual_provisional'and ctx['human_reviewed']is False and ctx['paragraph_ids']==[pp['id'],cp['id']]
     parent=mark(pp,pe['object_person_mention_id'],current);child=mark(cp,ce['subject_person_mention_id'],dest);term=q['source_term'];assert term in('子'+child['surface'],'長子'+child['surface'])and cp['text'].startswith(term+'，')and child['end']==len(term);outside(cp,0,child['end'])
     heads=[m for m in pp['mentions']if m['kind']=='person'and m['start']==0 and m['person_id']!=current];assert any(pp['text'][:parent['end']]==m['surface']+join+parent['surface']and pp['text'][parent['end']:].startswith(('，字','。'))for m in heads for join in('弟','族弟'));outside(pp,0,parent['end'])
     assert not any(x in pp['text']for x in '「」『』')
     for other in pp['mentions']:
      if other['kind']!='person'or other['person_id']==current or other['start']==0:continue
      # A named imperial designation immediately followed by 初 is a date,
      # not a biography-subject switch. Other named ancestry roles need
      # their own existing source assertion for this exact parent subject.
      if other['surface'].endswith('帝')and pp['text'][other['end']:].startswith('初，')and pp['text'][other['start']-1]in '，。；':continue
      ancestry=[x for x in aa.values()if x['predicate']in('father','grandfather')and x['subject_person_id']==current and x['object_person_id']==other['person_id']and any(e['paragraph_id']==pp['id']and e['quote']==pp['text']and e.get('object_person_mention_id')==other['id']for e in x['evidence'])]
      assert ancestry and any(pp['text'][other['start']-len(role):other['start']]==role for role in('祖','父'))
    generation+=1
   elif step['traversal']in('child_to_father','child_to_paternal_grandfather'):
    distance=1 if step['traversal']=='child_to_father'else 2;assert a['predicate']==('father'if distance==1 else'grandfather')and a['subject_person_id']==current and a['object_person_id']==dest and step['generation_after']==generation-distance
    assert set(role)=={'kind','companion_assertion_id'}and role['kind']=='biography_named_zu_fu_sequence';comp=aa[role['companion_assertion_id']];father=a if distance==1 else comp;grand=comp if distance==1 else a;assert father['status']==grand['status']=='source_attested'and all(not r['qualifiers'].get('adoptive')and not r['qualifiers'].get('sworn')for r in(father,grand))and father['predicate']=='father'and grand['predicate']=='grandfather'and father['subject_person_id']==grand['subject_person_id']==current and grand['qualifiers']['lineage']=='paternal'and father['qualifiers'].get('lineage')not in('maternal','non_paternal')
    fe,=father['evidence'];ge,=grand['evidence'];assert fe['paragraph_id']==ge['paragraph_id']and fe['quote']==ge['quote'];c,p=ps[fe['paragraph_id']];assert all(e[k]==c[k]for e in(fe,ge)for k in('work_id','book_id','source_id'))and fe['chapter_id']==ge['chapter_id']==c['id'];subject=mark(p,fe['subject_person_mention_id'],current);fm=mark(p,fe['object_person_mention_id'],father['object_person_id']);gm=mark(p,ge['object_person_mention_id'],grand['object_person_id']);heads=[m for m in p['mentions']if m['kind']=='person'and m['start']==0 and m['person_id']!=current];assert any(p['text'][:subject['end']+1]==m['surface']+'族弟'+subject['surface']+'。'for m in heads)
    assert gm['start']==subject['end']+2 and p['text'][gm['start']-1:gm['start']]=='祖'and p['text'][fm['start']-1:fm['start']]=='父'and gm['end']<fm['start']and p['text'][fm['start']-2:fm['start']]!='母父'and father['qualifiers']['source_term']=='父'+fm['surface']and grand['qualifiers']['source_term']=='祖'+gm['surface']
    outside(p,subject['end']+1,fm['end']);segment=p['text'][subject['end']+1:fm['end']];assert not any(x in segment for x in('外祖','云','非','未','不','或'))and not any(m['kind']=='person'and gm['start']<=m['start']<fm['end']and m['person_id']not in {father['object_person_id'],grand['object_person_id']}for m in p['mentions']);allowed_says={m.start()+1 for m in re.finditer(r'諡曰[^曰，。；「」『』]{1,4}[，。]',segment)};assert all(m.start()in allowed_says for m in re.finditer('曰',segment));generation-=distance
   else:raise AssertionError('No agnatic-cousin/spouse/adoption/inferred-assembly surname path')
   current=dest;seen.add(current);used.add(a['id'])
  assert current==name['person_id']
 except(AssertionError,KeyError,ValueError,TypeError,OSError,IndexError,StopIteration,AttributeError):raise ValueError('Received-family surname requires complete same-witness units, original full-name seed, exact source relationship roles/spans and bounded generations; no family-ID inference')
