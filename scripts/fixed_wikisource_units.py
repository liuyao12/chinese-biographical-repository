# coding: utf-8
"""Complete fixed Wikisource units, modern refs, and explicitly numeric uncle designations."""
from pathlib import Path
import hashlib,json,re

def source_errors(ch,root):
 # Trusted attached-subsection chapters cannot drop their source binding.
 try:from scripts.fixed_attached_subsection_selection import required_ref_error
 except ImportError:from fixed_attached_subsection_selection import required_ref_error
 required=required_ref_error(ch,root)
 if required:return required
 ref=ch.get('annotation',{}).get('fixed_wikisource_unit_ref')
 if ref is None:return []
 try:
  root=Path(root).resolve()
  def local(name):
   p=Path(name);assert not p.is_absolute()and p.parts[0]in('source-evidence','sources','corpus')and'..'not in p.parts
   q=root/p;assert q.resolve()==q and q.is_file();return q
  b=json.loads(local(ref).read_text())
  if b.get('record_type')=='fixed_wikisource_attached_subsection_selection':
   try:from scripts.fixed_attached_subsection_selection import errors as attached_errors
   except ImportError:from fixed_attached_subsection_selection import errors as attached_errors
   return attached_errors(ch,root,b)
  if b.get('record_type')=='fixed_wikisource_linked_heading_quote_biography':
   try:from scripts.fixed_linked_heading_biography import errors as linked_errors
   except ImportError:from fixed_linked_heading_biography import errors as linked_errors
   return linked_errors(ch,root,b)
  if b.get('record_type')=='fixed_wikisource_attached_biography_quotes':
   try:from scripts.fixed_attached_biography_quotes import errors as quoted_errors
   except ImportError:from fixed_attached_biography_quotes import errors as quoted_errors
   return quoted_errors(ch,root,b)
  if b.get('record_type')=='fixed_wikisource_biography_subsections_links':
   try:from scripts.fixed_biography_subsections import errors as subsection_errors
   except ImportError:from fixed_biography_subsections import errors as subsection_errors
   return subsection_errors(ch,root,b)
  if b.get('record_type')=='fixed_wikisource_plain_biography_year_templates':
   try:from scripts.fixed_plain_wikisource_biography import errors as plain_errors
   except ImportError:from fixed_plain_wikisource_biography import errors as plain_errors
   return plain_errors(ch,root,b)
  if b.get('record_type')=='fixed_wikisource_family_subsections':
   try:from scripts.fixed_wikisource_family_units import errors as family_errors
   except ImportError:from fixed_wikisource_family_units import errors as family_errors
   return family_errors(ch,root,b)
  rawb=local(b['raw_file']).read_bytes();raw=rawb.decode('utf-8',errors='strict');s=ch['source'];u=b['selection'];v=b['shared_appraisal']
  assert b['record_type']=='fixed_wikisource_complete_units'and type(b['source_revision'])is int and b['source_revision']==s['revision_id']and b['raw_file']==s['raw_path']
  assert hashlib.sha256(rawb).hexdigest()==b['raw_sha256']==s['raw_file_sha256']
  assert raw.count(u['opening_heading'])==raw.count(u['following_heading'])==1
  start,end=raw.index(u['opening_heading']),raw.index(u['following_heading']);assert start<end and (start,end)==(u['start'],u['end'])and raw[start:end]==u['raw']
  if v is not None:assert raw[v['start']:v['end']]==v['raw']and raw[v['start']:].startswith('史臣曰：')
  expected=[]
  for m in re.finditer(r'[^\n]+',u['raw']):
   if not m[0].startswith('='):expected.append((start+m.start(),start+m.end(),m[0]))
  if v is not None:expected.append((v['start'],v['end'],v['raw']))
  assert len(expected)==len(ch['paragraphs']);reports=[]
  for i,(p,(a,z,line))in enumerate(zip(ch['paragraphs'],expected)):
   loc=p['source_position'];positions=list(range(a,z));drop=set()
   for m in re.finditer(r'<ref>.*?</ref>',line):
    reports.append((p['id'],a+m.start(),a+m.end(),m[0]));drop.update(range(a+m.start(),a+m.end()))
   if line.startswith(':'):drop.add(a)
   positions=[x for x in positions if x not in drop]
   assert p['text']==''.join(raw[x]for x in positions)and loc['raw_character_offsets']==positions and loc['raw_start']==a and loc['raw_end']==z and loc['revision_id']==b['source_revision']
   assert loc['projection_sha256']==hashlib.sha256((json.dumps(positions,ensure_ascii=False,indent=2)+'\n').encode()).hexdigest()
   assert p['text_layer']=='received_chapter'and loc['source_layer']==('shared_historians_appraisal'if v is not None and i==len(expected)-1 else'received_biography')
   assert not any(key in layer for layer in (ch,s,b,p,loc)for key in ('annotator','attached_note_to_paragraph_id'))
  got=ch['annotation']['modern_collation_reports'];assert len(got)==len(reports)
  for note,expect in zip(got,reports):
   assert tuple(note[k]for k in ('paragraph_id','raw_start','raw_end','raw_text'))==expect and note['layer']=='modern_received_witness_collation_report'and note['image_verified']is False
  if v is None:
   assert 'shared_appraisal_context'not in ch['annotation']and all(p['source_position']['source_layer']=='received_biography'for p in ch['paragraphs'])
   return []
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

def _unit_clause(ch,b,root):
 assert not source_errors(ch,root)
 p=next(p for p in ch['paragraphs']if p['id']==b['paragraph_id']);t=p['text'];a=b['clause_anchor'];assert b['source_revision']==ch['source']['revision_id']and b['paragraph_sha256']==hashlib.sha256(t.encode()).hexdigest()
 assert set(a)=={'paragraph_id','start','end','surface'}and a['paragraph_id']==p['id']and type(a['start'])is int and type(a['end'])is int and 0<=a['start']<a['end']<=len(t)and t[a['start']:a['end']]==a['surface']
 pre=t[:a['start']];assert pre.count('「')==pre.count('」')and pre.count('『')==pre.count('』')and not any(x in a['surface']for x in '「」『』')and(not pre or pre[-1]in '，。；')
 return p,a,{m['id']:m for m in p['mentions']}

def unit_son_count_valid(report,ch,root,parse):
 try:
  b=report['received_unit_count_binding'];p,a,ms=_unit_clause(ch,b,root);m=ms[b['parent_mention_id']];n=report['source_number'];e,=report['evidence']
  return (b['kind']=='named_parent_total_sons'and m['kind']=='person'and m['person_id']==report['parent_person_id']and m['start']==a['start']and a['surface']==m['surface']+'有'+n+'子'and report['source_term']=='有'+n+'子'and type(report['reported_count'])is int and 0<report['reported_count']==parse(n)and report['count_scope']=='sons_of_parent'and report['named_member_person_ids']==[]and report['complete_named_list']is False and report['status']=='source_attested'and report['human_reviewed']is False and e=={**{k:ch[k]for k in('work_id','book_id','source_id')},'chapter_id':ch['id'],'paragraph_id':p['id'],'quote':p['text'],'person_mention_id':m['id']})
 except(KeyError,ValueError,TypeError,OSError,AssertionError,StopIteration):return False

def unit_group_age_bound_valid(age,ch,root,parse):
 try:
  b=age['received_unit_age_binding'];p,a,ms=_unit_clause(ch,b,root);members=[ms[m]for m in b['member_mention_ids']];n=age['source_number'];e,=age['evidence'];bounds={'lower':parse(n),'lower_inclusive':False,'upper':None,'upper_inclusive':None}
  assert b['kind']=='fully_named_group_over_age'and len(members)>=2 and len({m['person_id']for m in members})==len(members)and all(m['kind']=='person'for m in members)
  cursor=a['start']
  for m in members:assert m['start']==cursor;cursor=m['end']+1
  assert a['surface']=='、'.join(m['surface']for m in members)+'年過'+n and age['source_term']=='年過'+n and age['person_id']in[m['person_id']for m in members]
  own=next(m for m in members if m['person_id']==age['person_id'])
  return age['value']is None and age['bounds']==bounds and bounds['lower']is not None and age['group_reference']=={'person_ids':[m['person_id']for m in members],'naming_term':'、'.join(m['surface']for m in members),'complete_named_group':True}and age['age_context']=={'kind':'during_life'}and age['birth_year']is None and age['counting']=='unspecified_source_age'and age['status']=='source_attested'and age['human_reviewed']is False and e=={**{k:ch[k]for k in('work_id','book_id','source_id')},'chapter_id':ch['id'],'paragraph_id':p['id'],'quote':p['text'],'person_mention_id':own['id']}
 except(KeyError,ValueError,TypeError,OSError,AssertionError,StopIteration):return False

def unit_numbered_son_valid(claim,paragraphs,chapters,root):
 try:
  b=claim['qualifiers']['source_clause_binding'];e,=claim['evidence'];ch=chapters[e['chapter_id']];p,a,ms=_unit_clause(ch,b,root);child=ms[e['subject_person_mention_id']];parent=ms[e['object_person_mention_id']];order=claim['qualifiers']['birth_order'];term='長子'if order['ordinal']==1 else '第'+order['source_number']+'子'
  assert b['kind']=='named_parent_sending_numbered_son'and claim['predicate']=='father'and child['person_id']==claim['subject_person_id']and parent['person_id']==claim['object_person_id']and parent['end']<=a['start']and child['end']==a['end']and a['surface']in('遣'+term+child['surface'],'乃遣'+term+child['surface'])
  assert child['kind']==parent['kind']=='person'and claim['status']=='source_attested'and order['source_term']==term and order['interpretation_status']=='source_attested'and order['parent_person_id']==parent['person_id']and order['scope']=='sons_of_parent'and type(order['ordinal'])is int and order['ordinal']>0 and order['position']==('eldest'if order['ordinal']==1 else'unspecified')
  if order['ordinal']!=1:
   try:from scripts.chinese_civil_years import numeral
   except ImportError:from chinese_civil_years import numeral
   assert numeral(order['source_number'])==order['ordinal']
  previous=[m for m in p['mentions']if m['kind']=='person'and m['end']<=a['start']];assert previous and max(previous,key=lambda m:m['end'])['id']==parent['id']
  return e['quote']==p['text']and e['paragraph_id']==p['id']and claim['human_reviewed']is False and child['person_id']!=parent['person_id']
 except(KeyError,ValueError,TypeError,OSError,AssertionError,StopIteration):return False

def biography_former_ming_valid(name,p):
 try:
  b=name['former_ming_basis'];t=p['text'];ms={m['id']:m for m in p['mentions']};current=ms[b['current_name_mention_id']];former=ms[b['former_name_mention_id']];ruler=ms[b['ruler_mention_id']];marker=b['source_marker_anchor'];grant=b['grant_anchor']
  assert b['kind']=='biography_original_name_then_ruler_renaming'and b['human_reviewed']is False and b['rationale'].strip()and b['source_revision']==p['source_position']['revision_id']and b['paragraph_sha256']==hashlib.sha256(t.encode()).hexdigest()and name['quote']==t and name['paragraph_id']==p['id']and name['person_mention_id']==current['id']and p['text_layer']=='received_chapter'and not any(k in p for k in('annotator','attached_note_to_paragraph_id'))
  def exact(a):return set(a)=={'paragraph_id','start','end','surface'}and a['paragraph_id']==p['id']and type(a['start'])is int and type(a['end'])is int and 0<=a['start']<a['end']<=len(t)and t[a['start']:a['end']]==a['surface']
  assert exact(marker)and exact(grant)and marker['surface']=='本名'and marker['end']==former['start']and former['surface']==name['former_ming']and current['surface']==name['ming']and current['person_id']==former['person_id']==name['person_id']and ruler['person_id']!=name['person_id']and all(m['kind']=='person'for m in(current,former,ruler))
  assert current['start']==0 or (current['start']>1 and t[current['start']-1]=='弟'and any(m['kind']=='person'and m['start']==0 and m['end']==current['start']-1 and m['person_id']!=name['person_id']for m in p['mentions']))
  assert t[current['end']:marker['start']]=='，字'+name['zi']+'，'and t[former['end']:ruler['start']]=='，'and grant['start']==ruler['start']and grant['surface']==ruler['surface']+'賜名焉'and t[grant['end']:].startswith('。')and name['former_ming']!=name['ming']
  return True
 except(KeyError,ValueError,TypeError,AssertionError,StopIteration):return False
