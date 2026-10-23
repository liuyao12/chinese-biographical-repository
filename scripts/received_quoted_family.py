"""Finite received body/note family syntax; source roles, no person/name allowlist."""
from pathlib import Path
import hashlib,re,json
FRAMES={
 'annotated_head_ancestor_offices':'按{work}<head>祖<grandfather>{grandfather_office}父<father>{father_office}',
 'named_parent_child':'<parent>子<child>',
 'named_elder_younger':'<older>弟<younger>',
 'wife_named_brother_sister':'<husband><wife_repeat><brother>之<wife>',
 'named_woman_marriage':'<wife>適<husband>',
 'sons_after_explicit_sons_in_law':'<affine1><affine2>皆<parent>女婿子<child>字{style}有器度幹用歴職著績終於{office}次弟<younger>字{younger_style}{younger_office}知名早卒',
 'biography_death_son_grandson_succession':'{deathdate}薨追贈{postoffice}諡曰{postname}子<child>嗣<child_repeat>官至{child_office}薨子<grandchild>嗣{era}中開建五等以<head>著勲前朝改封{rank}'
}
def analyse(a,paragraphs,chapters,root):
 b=a['qualifiers']['source_kinship_frame'];e,=a['evidence'];cid,p=paragraphs[e['paragraph_id']];ch=chapters[cid];t=p['text'];ms={m['id']:m for m in p['mentions']};r={k:ms[v]for k,v in b['roles'].items()};f=b['fields'];s=b['scope_anchor'];rule=b['rule']
 assert set(b)=={'kind','rule','roles','fields','scope_anchor','source_revision','paragraph_sha256','source_layer','human_reviewed','fixed_witness_reference'}and b['kind']=='received_quoted_family_frame'and b['human_reviewed']is False
 assert b['source_revision']==ch['source']['revision_id']and b['paragraph_sha256']==hashlib.sha256(t.encode()).hexdigest()and b['source_layer']==p['text_layer']and p['text_layer']in('received_chapter','witness_appended_pei_songzhi_note')
 assert e['quote']==t and e['chapter_id']==ch['id']and all(e[k]==ch[k]for k in('work_id','book_id','source_id'))
 root=Path(root).resolve();receipt=b['fixed_witness_reference'];assert set(receipt)=={'path','sha256'};rr=Path(receipt['path']);rp=root/rr;assert not rr.is_absolute()and'..'not in rr.parts and rr.parts[0]=='source-evidence'and rp.resolve()==rp
 rb=rp.read_bytes();assert hashlib.sha256(rb).hexdigest()==receipt['sha256'];w=json.loads(rb);u=next(x for x in w['units']if x['paragraph_id']==p['id']);assert w['chapter_id']==ch['id']and w['source_commit']==ch['source']['source_commit']and w['raw_sha256']==ch['source']['raw_file_sha256']and w['raw_file']==ch['source']['raw_path']and u=={'paragraph_id':p['id'],'text':t,'text_layer':p['text_layer'],'source_position':p['source_position']}
 rel=Path(ch['source']['raw_path']);rawpath=root/rel;assert not rel.is_absolute()and'..'not in rel.parts and rel.parts[0]in('sources','source-evidence')and rawpath.resolve()==rawpath
 raw=rawpath.read_bytes();assert hashlib.sha256(raw).hexdigest()==ch['source']['raw_file_sha256'];rawtext=raw.decode();lines=rawtext.splitlines(keepends=True);frags=p['source_position']['source_fragments'];assert ''.join(x['text']for x in frags)==t
 for x in frags:
  assert lines[x['line']-1][x['raw_start']:x['raw_end']]==x['text']
  offset=sum(len(v)for v in lines[:x['line']-1])+x['raw_start'];note=rawtext[:offset].count('(')>rawtext[:offset].count(')');assert note==(p['text_layer']=='witness_appended_pei_songzhi_note')
 assert p['source_position']['source_layer']=={'received_chapter':'received_biography','witness_appended_pei_songzhi_note':'pei_annotation'}[p['text_layer']]
 def exact(x):return set(x)=={'paragraph_id','start','end','surface'}and x['paragraph_id']==p['id']and type(x['start'])is int and type(x['end'])is int and 0<=x['start']<x['end']<=len(t)and t[x['start']:x['end']]==x['surface']
 assert exact(s)and(not s['start']or t[s['start']-1]not in'非不未無')
 pos=s['start'];usedr=set();usedf=set()
 for tok in re.split(r'(<[^>]+>|\{[^}]+\})',FRAMES[rule]):
  if not tok:continue
  if tok[0]=='<':
   key=tok[1:-1];m=r[key];assert m['kind']=='person'and m['start']==pos and t[m['start']:m['end']]==m['surface'];pos=m['end'];usedr.add(key)
  elif tok[0]=='{':
   key=tok[1:-1];x=f[key];assert exact(x)and x['start']==pos and len(x['surface'])<=20 and not any(c in x['surface']for c in'曰云未非無不。；！？「」『』');pos=x['end'];usedf.add(key)
  else:assert t.startswith(tok,pos);pos+=len(tok)
 assert pos==s['end']and set(r)==usedr and set(f)==usedf
 assert len({m['person_id']for k,m in r.items()if not k.endswith('_repeat')})==len([k for k in r if not k.endswith('_repeat')])
 for key,m in r.items():
  if key.endswith('_repeat'):assert m['person_id']==r[key[:-7]]['person_id']
 if 'head'in r:
  h=ch['paragraphs'][0];hm=h['mentions'][0];assert hm['start']==0 and h['text'][hm['end']:].startswith('字')and hm['person_id']==r['head']['person_id']
 for m in p['mentions']:
  if m['kind']=='person'and s['start']<=m['start']<s['end']:
   if m['id']in b['roles'].values():continue
   owners={'style':'child','younger_style':'younger'}if rule=='sons_after_explicit_sons_in_law'else{}
   assert any(f[k]['start']<=m['start']<m['end']<=f[k]['end']and m['person_id']==r[v]['person_id']for k,v in owners.items())
 return ch,p,r,f,rule

def valid(a,paragraphs,chapters,root):
 try:
  ch,p,r,f,rule=analyse(a,paragraphs,chapters,root);q=a['qualifiers'];e,=a['evidence'];s=next(m for m in p['mentions']if m['id']==e['subject_person_mention_id']);o=next(m for m in p['mentions']if m['id']==e['object_person_mention_id']);assert a['status']=='source_attested'and a['human_reviewed']is False and s['person_id']==a['subject_person_id']and o['person_id']==a['object_person_id']and s['person_id']!=o['person_id']
  allowed=[]
  if rule=='annotated_head_ancestor_offices':allowed=[('father','head','father','父'+r['father']['surface']),('grandfather','head','grandfather','祖'+r['grandfather']['surface'])]
  elif rule=='named_parent_child':allowed=[('father','child','parent','子')]
  elif rule=='named_elder_younger':allowed=[('brother','younger','older',r['older']['surface']+'弟'+r['younger']['surface'])]
  elif rule=='wife_named_brother_sister':
   assert r['wife']['surface']=='妹'and r['wife_repeat']['surface']=='妻';allowed=[('spouse','wife','husband','妻'),('sister','wife','brother','妹')]
  elif rule=='named_woman_marriage':assert r['wife']['surface']=='女';allowed=[('spouse','wife','husband','適')]
  elif rule=='sons_after_explicit_sons_in_law':allowed=[('father','child','parent','子'),('brother','younger','child','次弟'),('father_in_law','affine1','parent','女婿'),('father_in_law','affine2','parent','女婿')]
  elif rule=='biography_death_son_grandson_succession':allowed=[('father','child','head','子'),('father','grandchild','child_repeat','子')]
  match=[x for x in allowed if x[0]==a['predicate']and r[x[1]]['id']==s['id']and r[x[2]]['id']==o['id']];assert len(match)==1 and q['source_term']==match[0][3]
  expected={'source_term','source_kinship_frame'}
  if a['predicate']in('father','grandfather'):
   expected.add('lineage');assert q['lineage']=='paternal'
  if a['predicate']in('brother','sister'):
   expected.add('relative_birth_order');assert q['relative_birth_order']=={'older_person_id':o['person_id'],'younger_person_id':s['person_id'],'operator':'lt','older_ordinal':None,'younger_ordinal':None,'scope':'siblings'}
  if a['predicate']=='father_in_law':
   expected|={'spouse_person_id','spouse_identity_status'};assert q['spouse_person_id']is None and q['spouse_identity_status']=='not_identified_by_this_clause'
  assert set(q)==expected
  return True
 except(KeyError,TypeError,ValueError,AssertionError,StopIteration,OSError,IndexError):return False
