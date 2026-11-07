"""One received allusion resolved by primary courtesy-name and crying-at-road-end context."""
import copy,hashlib,json
from pathlib import Path
REF='source-evidence/zhou041-wangbao-ws2432538/sizong-primary-resolution.json'
SHA='c0ab4a2e4348196841818f687752f811837fa89826119e6958c3908f53c2b9fd'
CID='c-zhoushu-041-wangbao-ws2432538'
def same(a,b):
 if type(a)is not type(b):return False
 if isinstance(a,dict):return a.keys()==b.keys()and all(same(a[k],b[k])for k in a)
 if isinstance(a,list):return len(a)==len(b)and all(same(x,y)for x,y in zip(a,b))
 return a==b
def read(root,rel):
 root=Path(root).resolve();p=root/rel;assert not Path(rel).is_absolute()and'..'not in Path(rel).parts and p.resolve()==p and p.is_file();return p.read_bytes()
def capsule(root):
 raw=read(root,REF);assert hashlib.sha256(raw).hexdigest()==SHA;c=json.loads(raw);p=c['primary'];assert p['current_rendered_body_read']is True and p['fixed_permalink_body_read']is False and p['original_wikitext_obtained']is False and p['actual_print_edition']is None and p['image_verified']is False and p['human_reviewed']is False
 assert '阮籍，字嗣宗' in p['complete_opening_paragraph']and'車跡所窮，輒慟哭而反' in p['complete_crying_paragraph'];assert hashlib.sha256(read(root,c['observation_path'])).hexdigest()==c['observation_sha256'];return c
def current_person(root,people):
 c=capsule(root);s=c['catalog_seed'];source=json.loads(read(root,s['path']));assert source['id']==s['chapter_id']and hashlib.sha256((json.dumps(source['source'],ensure_ascii=False,indent=2)+'\n').encode()).hexdigest()==s['source_sha256'];p,=[p for p in source['paragraphs']if p['id']==s['paragraph_id']];assert hashlib.sha256(p['text'].encode()).hexdigest()==s['paragraph_text_sha256'];m,=[m for m in p['mentions']if m['id']==s['marker']['id']];assert same({k:v for k,v in m.items()if k!='person_id'},s['marker'])and m['kind']=='person'and p['text'][m['start']:m['end']]=='阮籍';pid=m['person_id'];assert pid in people;actor=people[pid];assert [e for e in actor['evidence']if e.get('mention_id')==m['id']]==[s['reverse']];assert any(a['surface']=='阮籍'and m['id']in a['mention_ids']for a in actor['aliases']);return c,pid
def validate_primary(root,roles,people,binding):
 assert binding=={'path':REF,'sha256':SHA};c,pid=current_person(root,people);assert roles['$sizong']==pid;return c,pid
def project_prior(ch,root,people):
 """Advance this old AI semantic judgment, retaining its captured bytes externally.

 Only one marker/case and the explicitly reviewed coverage note change. Source
 acquisition/modern note/raw text, all other markers and unknown metadata survive.
 """
 c,pid=current_person(root,people)
 if ch.get('record_type')=='identity_decision_set':
  assert ch['chapter_id']==CID
  try:from scripts.fixed_zhou041_wangbao import REF as source_ref,SHA as source_sha
  except ImportError:from fixed_zhou041_wangbao import REF as source_ref,SHA as source_sha
  raw=read(root,source_ref);assert hashlib.sha256(raw).hexdigest()==source_sha;source_contract=json.loads(raw)
  rel='corpus/zhoushu/041-wangbao-ws2432538-identities.json';decision,=[v for v in source_contract['sidecar_templates'][rel]['decisions']if v['id']==c['semantic_delta']['remove_case_id']]
  decision=copy.deepcopy(decision);assert decision['person_id']=='$sizong';decision['person_id']=pid
  out=copy.deepcopy(ch);assert not any(v['id']==decision['id']for v in out['decisions']);out['decisions'].append(decision);return out
 assert ch['id']==CID;out=copy.deepcopy(ch);d=c['semantic_delta'];pairs=[(p,i,m)for p in out['paragraphs']for i,m in enumerate(p['mentions'])if m['id']==c['target_mid']];assert len(pairs)==1;p,i,m=pairs[0];assert same({k:v for k,v in m.items()if k!='candidate_person_ids'},d['before_marker_without_candidate_ids']);assert p['text'].startswith('嗣宗窮途，楊朱歧路。');new=copy.deepcopy(d['after_marker_without_pid']);new['person_id']=pid;p['mentions'][i]=new
 a=out['annotation'];cases=a['unresolved_identity_cases'];assert sum(x['id']==d['remove_case_id']for x in cases)==1;a['unresolved_identity_cases']=[x for x in cases if x['id']!=d['remove_case_id']];assert a['coverage']==d['coverage_before'];a['coverage']=d['coverage_after'];ix=d['limitation_index'];assert a['limitations'][ix]==d['limitation_before'];a['limitations'][ix]=d['limitation_after'];r=copy.deepcopy(d['resolved_review_without_pid']);r['person_id']=pid;a.setdefault('resolved_identity_reviews',[]).append(r);return out

def project_prior_xml(text,root,people):
 from html import escape
 c,pid=current_person(root,people);mid=c['target_mid'];old='<rs id="'+escape(mid,quote=True)+'" type="unresolved">嗣宗</rs>';new='<persName id="'+escape(mid,quote=True)+'" ref="'+escape(pid,quote=True)+'">嗣宗</persName>';assert text.count(old)==1;return text.replace(old,new)
