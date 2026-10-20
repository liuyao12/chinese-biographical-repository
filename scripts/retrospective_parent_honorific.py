"""Named parent honour expressed by 尊...曰...皇后, not a living queen office."""
import re,hashlib

def parent_honorific_grant_valid(h,paragraphs):
 try:
  b=h['posthumous_basis'];es=b['evidence'];start=h['effective_period']['start'];term=b['source_term'];s=b['named_parent_honorific']
  if (h['mode']!='posthumous_grant'or h['kind']!='honorific'or set(b)!={'source_term','evidence','named_parent_honorific'}
      or set(s)!={'kind','issuer_person_id','issuer_mention_id','recipient_mention_id','relationship_term','honorific_anchor','grant_anchor','death_year','status','human_reviewed','primary_context'}
      or s['kind']!='retrospective_parent_empress_honorific'or s['relationship_term']not in('母','祖母')
      or s['death_year']is not None or s['status']!='editorial_provisional'or s['human_reviewed']is not False
      or len(es)!=1 or not all(e in h['evidence']for e in es)or es!=start['evidence']or start.get('date_expression')is not None
      or start.get('event_type')!='posthumous_grant'or not re.fullmatch(r'[^太母后]{1,8}皇后',h['title'])):return False
  e=es[0];cid,p=paragraphs[e['paragraph_id']];ms={m['id']:m for m in p['mentions']};issuer=ms[s['issuer_mention_id']];recipient=ms[s['recipient_mention_id']]
  if (cid!=e['chapter_id']or e['quote']!=p['text']or issuer.get('person_id')!=s['issuer_person_id']
      or recipient.get('person_id')!=h['person_id']or issuer['person_id']==recipient['person_id']
      or issuer.get('kind')!='person'or recipient.get('kind')!='person'):return False
  a,g=s['honorific_anchor'],s['grant_anchor']
  def exact(v):return set(v)=={'paragraph_id','start','end','surface'}and v['paragraph_id']==p['id']and p['text'][v['start']:v['end']]==v['surface']and 0<=v['start']<v['end']<=len(p['text'])
  expected=issuer['surface']+'尊'+s['relationship_term']+recipient['surface']+'曰'+h['title']
  return(primary_posthumous_context_valid(s['primary_context'],h,recipient['surface'])and exact(a)and exact(g)and a['surface']==h['title']and g['surface']==term==expected
         and g['start']==issuer['start']and recipient['end']+1==a['start']and a['end']==g['end']
         and p.get('text_layer')=='witness_appended_lixian_note'
         and any(t['paragraph_id']==p['id']and t['start']==a['start']and t['end']==a['end']and t['usage']=='posthumous_usage'for t in h['attestations']))
 except(KeyError,TypeError,ValueError):return False


def primary_posthumous_context_valid(b,h,recipient):
 """Qualification only: independently fixed complete primary unit, no new death/year."""
 try:
  if b['kind']!='fixed_primary_death_before_honorific'or b['recipient_person_id']!=h['person_id']or b['title']!=h['title']or b['human_reviewed']is not False:return False
  src=b['source'];u=b['unit'];raw=src['raw_text'];text=u['text'];first,last=u['raw_lines'];H=lambda s:hashlib.sha256(s.encode()).hexdigest()
  if (H(raw)!=src['raw_sha256']or H(text)!=u['text_sha256']or not(1<=first<=last<=len(raw.splitlines()))
      or ''.join(raw.splitlines(keepends=True)[first-1:last])!=text or src['baseedition']!='WYG'
      or not re.fullmatch('[0-9a-f]{40}',src['commit'])or src['image_verified']is not False
      or src['url']!='https://raw.githubusercontent.com/kanripo/KR2a0009/'+src['commit']+'/'+src['filename']
      or '#+PROPERTY: BASEEDITION WYG'not in raw):return False
  aa=b['anchors']
  if set(aa)!={'subject','death','grant','identity'}:return False
  for a in aa.values():
   if not(0<=a['start']<a['end']<=len(text))or text[a['start']:a['end']]!=a['surface']or a['raw_line_start']!=first+text[:a['start']].count('\n'):return False
  sub,dead,grant,identity=(aa[k]for k in ('subject','death','grant','identity'))
  # Historical/editorial co-reference is explicit in the bound complete unit;
  # a raw 尊母 formula in 009 alone never passes this branch.
  if recipient not in sub['surface']or sub['start']>dead['start']or dead['end']>grant['start']:return False
  if not re.fullmatch(r'(?:貴人姊妹以憂卒|二貴人同時飲藥自殺|遂鴆殺'+re.escape(recipient)+')',dead['surface']):return False
  alignment=b['title_alignment']
  if alignment['kind']!='same_recipient_same_honorific_grant'or alignment['annal_title']!=h['title']or alignment['human_reviewed']is not False or not alignment['rationale']or not grant['surface'].endswith(alignment['primary_title']):return False
  folded=lambda v:re.sub(r'[¶\n]','',v).replace('隠','隱').replace('皇后','后')
  if not folded(grant['surface']).endswith(folded(h['title']))or not re.search(r'(?:追諡|尊諡)(?:¶\n)?曰',grant['surface']):return False
  if not identity['surface']or not b['editorial_linkage']:return False
  return True
 except(KeyError,TypeError,ValueError,IndexError):return False
