# coding: utf-8
"""Complete fixed Wikisource units, modern refs, and explicitly numeric uncle designations."""
from pathlib import Path
import hashlib,json,re

def source_errors(ch,root):
 ref=ch.get('annotation',{}).get('fixed_wikisource_unit_ref')
 if ref is None:return []
 try:
  root=Path(root).resolve()
  def local(name):
   p=Path(name);assert not p.is_absolute()and p.parts[0]in('source-evidence','sources','corpus')and'..'not in p.parts
   q=root/p;assert q.resolve()==q and q.is_file();return q
  b=json.loads(local(ref).read_text());rawb=local(b['raw_file']).read_bytes();raw=rawb.decode('utf-8',errors='strict');s=ch['source'];u=b['selection'];v=b['shared_appraisal']
  assert b['record_type']=='fixed_wikisource_complete_units'and type(b['source_revision'])is int and b['source_revision']==s['revision_id']and b['raw_file']==s['raw_path']
  assert hashlib.sha256(rawb).hexdigest()==b['raw_sha256']==s['raw_file_sha256']
  assert raw.count(u['opening_heading'])==raw.count(u['following_heading'])==1
  start,end=raw.index(u['opening_heading']),raw.index(u['following_heading']);assert start<end and (start,end)==(u['start'],u['end'])and raw[start:end]==u['raw']
  assert raw[v['start']:v['end']]==v['raw']and raw[v['start']:].startswith('史臣曰：')
  expected=[]
  for m in re.finditer(r'[^\n]+',u['raw']):
   if not m[0].startswith('='):expected.append((start+m.start(),start+m.end(),m[0]))
  expected.append((v['start'],v['end'],v['raw']));assert len(expected)==len(ch['paragraphs']);reports=[]
  for i,(p,(a,z,line))in enumerate(zip(ch['paragraphs'],expected)):
   loc=p['source_position'];positions=list(range(a,z));drop=set()
   for m in re.finditer(r'<ref>.*?</ref>',line):
    reports.append((p['id'],a+m.start(),a+m.end(),m[0]));drop.update(range(a+m.start(),a+m.end()))
   if line.startswith(':'):drop.add(a)
   positions=[x for x in positions if x not in drop]
   assert p['text']==''.join(raw[x]for x in positions)and loc['raw_character_offsets']==positions and loc['raw_start']==a and loc['raw_end']==z and loc['revision_id']==b['source_revision']
   assert loc['projection_sha256']==hashlib.sha256((json.dumps(positions,ensure_ascii=False,indent=2)+'\n').encode()).hexdigest()
   assert p['text_layer']=='received_chapter'and loc['source_layer']==('shared_historians_appraisal'if i==len(expected)-1 else'received_biography')
   assert not any(key in layer for layer in (ch,s,b,p,loc)for key in ('annotator','attached_note_to_paragraph_id'))
  got=ch['annotation']['modern_collation_reports'];assert len(got)==len(reports)
  for note,expect in zip(got,reports):
   assert tuple(note[k]for k in ('paragraph_id','raw_start','raw_end','raw_text'))==expect and note['layer']=='modern_received_witness_collation_report'and note['image_verified']is False
  ctx=ch['annotation']['shared_appraisal_context'];assert ctx['same_witness']is True and ctx['independent_witness']is False and ctx['existing_chapter_id']==v['source_chapter_id']and ctx['existing_paragraph_id']==v['source_paragraph_id']
  # Read the actual native shared witness, not a saved fragment or duplicate vote.
  matches=[]
  for f in(root/'corpus').glob('*/*.json'):
   d=json.loads(f.read_text())
   if d.get('record_type')=='marked_chapter'and d['id']==ctx['existing_chapter_id']:matches.append(d)
  old,=matches;op=next(p for p in old['paragraphs']if p['id']==ctx['existing_paragraph_id'])
  assert old['source']['revision_id']==s['revision_id']and old['source']['raw_file_sha256']==s['raw_file_sha256']and op['text']==v['raw']==ch['paragraphs'][-1]['text']
  return []
 except(AssertionError,KeyError,ValueError,TypeError,OSError,IndexError,StopIteration):return ['固定維基文庫完整單元、原行投影、校勘層或同見證共評資格不符']

def ordinal_uncle_valid(a,paragraphs):
 try:
  q=a['qualifiers'];n=q['source_uncle_ordinal'];assert set(n)=={'value','source_number','source_term','scope'}and n['scope']=='source_uncle_designation_not_father_son_birth_order'
  try:from scripts.chinese_civil_years import numeral
  except ImportError:from chinese_civil_years import numeral
  assert type(n['value'])is int and 0<n['value']==numeral(n['source_number'])and n['source_term']=='第'+n['source_number']+'叔'
  assert a['predicate']=='paternal_uncle'and a['subject_person_id']!=a['object_person_id']and a['status']=='source_attested'and a['human_reviewed']is False
  e,=a['evidence'];cid,p=paragraphs[e['paragraph_id']];ms={m['id']:m for m in p['mentions']};child=ms[e['subject_person_mention_id']];uncle=ms[e['object_person_mention_id']]
  assert cid==e['chapter_id']and p['text_layer']=='received_chapter'and e['quote']==p['text']and child['person_id']==a['subject_person_id']and uncle['person_id']==a['object_person_id']and child['kind']==uncle['kind']=='person'
  assert p['text'][child['end']:uncle['start']]==n['source_term']and q['source_term']==n['source_term']+uncle['surface']
  pre=p['text'][:child['start']];assert pre.count('「')==pre.count('」')and pre.count('『')==pre.count('』')and (not pre or pre[-1]in '。；，')
  return True
 except(AssertionError,KeyError,ValueError,TypeError,IndexError):return False

def kin_age_designation_valid(age,ch,root):
 """A source's quoted number for a named speaker's father; not an exact-age adjudication."""
 try:
  try:from scripts.chinese_civil_years import numeral
  except ImportError:from chinese_civil_years import numeral
  b=age['kin_age_designation'];assert set(b)=={'kind','speaker_person_id','speaker_mention_id','subject_mention_id','speech_start_anchor','father_assertion_id','number_anchor','precision'}and b['kind']=='quoted_father_age_designation'and b['precision']=='quoted_rounded_age_not_exact'
  assert age['reporting_status']=='quoted_kin_age_designation'and age['age_context']=={'kind':'during_life'}and age['counting']=='unspecified_source_age'and age['birth_year']is None and age['status']=='source_attested'and age['human_reviewed']is False
  q=age['approximation'];assert set(q)=={'kind','target_age'}and q['kind']=='quoted_kin_age_designation'and type(q['target_age'])is int and q['target_age']>0 and age['value']is None and 'bounds'not in age and numeral(age['source_number'])==q['target_age']and age['source_term']==age['source_number']+'老父'
  e,=age['evidence'];p=next(p for p in ch['paragraphs']if p['id']==e['paragraph_id']);ms={m['id']:m for m in p['mentions']};speaker=ms[b['speaker_mention_id']];subject=ms[b['subject_mention_id']];speech=b['speech_start_anchor'];number=b['number_anchor'];t=p['text']
  def exact(a):return set(a)=={'paragraph_id','start','end','surface'}and a['paragraph_id']==p['id']and type(a['start'])is int and type(a['end'])is int and 0<=a['start']<a['end']<=len(t)and t[a['start']:a['end']]==a['surface']
  assert all(e[k]==ch[k]for k in ('work_id','book_id','source_id'))and e['chapter_id']==ch['id']and e['quote']==t and e['person_mention_id']==subject['id']and p['text_layer']=='received_chapter'
  assert speaker['kind']==subject['kind']=='person'and speaker['person_id']==b['speaker_person_id']and subject['person_id']==age['person_id']and speaker['person_id']!=subject['person_id']
  assert exact(speech)and exact(number)and speech['surface']==speaker['surface']+'答曰：「'and speech['start']==speaker['start']and number['surface']==age['source_number']and number['start']==subject['start']and number['end']+2==subject['end']and subject['surface']==age['source_term']
  assert speech['end']<=subject['start']<subject['end']<=t.index('」',speech['end'])and'「'not in t[speech['end']:subject['start']]
  pre=t[:speech['start']];assert pre.count('「')==pre.count('」')and pre.count('『')==pre.count('』')
  found=[]
  for f in(Path(root)/'corpus').glob('*/*-assertions.json'):
   d=json.loads(f.read_text())
   if d.get('chapter_id')==ch['id']:found.extend(a for a in d.get('assertions',[])if a['id']==b['father_assertion_id'])
  a,=found;assert a['predicate']=='father'and a['subject_person_id']==speaker['person_id']and a['object_person_id']==subject['person_id']and a['status']=='source_attested'
  return True
 except(AssertionError,KeyError,ValueError,TypeError,OSError,IndexError,StopIteration):return False
