"""Minimum explicit families and qualified missing-father placements for WYD044."""
import copy
CID='c-songshu-044-wyd1739-xiehui'
def assertions(ch,roles):
 ps={p['id'].split(':')[-1]:p for p in ch['paragraphs']}
 def mark(p,key):return next(m for m in p['mentions']if m.get('source_role_key')==key)
 def fact(key,pid,subject,predicate,obj,term,start=None,extra=None):
  p=ps[pid];s=mark(p,subject);o=mark(p,obj);at=p['text'].index(term)if start is None else start
  q={'source_term':term};q.update(extra or{})
  return {'id':'a-song044-wyd-'+key,'subject_person_id':roles[subject],'predicate':predicate,'object_person_id':roles[obj],'status':'source_attested','qualifiers':q,'evidence':[{'work_id':ch['work_id'],'book_id':ch['book_id'],'chapter_id':CID,'source_id':ch['source_id'],'paragraph_id':p['id'],'quote':p['text'],'relationship_anchor':{'paragraph_id':p['id'],'start':at,'end':at+len(term),'surface':term},'subject_person_mention_id':s['id'],'object_person_mention_id':o['id']}],'interpretation_note':'保留本源原詞、端點及主語範圍；未推同母、生日或其他子女生母。','reviewer':'Codex（AI代理）','human_reviewed':False,'model':None}
 out=[fact('hui-father','p001','hui','father','chong','父重',extra={'lineage':'paternal'}),fact('hui-grandfather','p001','hui','grandfather','lang','祖朗',extra={'lineage':'paternal'}),fact('xuan-brother','p001','xuan-brother','brother','hui','兄絢'),fact('shixiu-father','p003','shixiu','father','hui','長子世休',extra={'lineage':'paternal'}),fact('shiji-father','p016','shiji','father','xuan-brother','世基絢之子也',extra={'lineage':'paternal'}),fact('huaifu-father','p017','huaifu','father','shangxuanshi','其子懷福',extra={'lineage':'paternal'}),fact('wife-cao','p003','hui','spouse','wife-cao','妻曹'),fact('dun-brother','p008','xiedun','brother','hui','弟遯')]
 out[3]['qualifiers']['birth_order']={'parent_person_id':roles['hui'],'scope':'sons_of_parent','ordinal':1,'position':'eldest','interpretation_status':'source_attested'}
 for index,older,younger in [(2,'xuan-brother','hui'),(7,'hui','xiedun')]:
  out[index]['qualifiers']['relative_birth_order']={'older_person_id':roles[older],'younger_person_id':roles[younger],'operator':'lt','scope':'siblings','older_ordinal':None,'younger_ordinal':None}
 for key,pid,term in [('shao','p004','兄子著作佐郎紹'),('shiyou','p008','兄子世猷')]:
  out.append(fact(key+'-uncle',pid,key,'paternal_uncle','hui',term,extra={'source_clause_binding':{'kind':'wyd_song044_biographical_xiongzi','nephew_role':key}}))
 return {'format_version':'0.2','record_type':'person_assertion_set','chapter_id':CID,'assertions':out}

def reference(a,ch):
 return dict(a['evidence'][0],assertion_id=a['id'],scope='本源完整段；組裝推導與明文分開，未造中間父親。',url=ch['source'].get('url')or ch['source'].get('permalink'))
def assembly_delta(before,people,ch,roles,facts):
 after=copy.deepcopy(before);by={a['id']:a for a in facts['assertions']};family=next(a for a in after['assemblies']if a['id']=='family-chenjun-xie-lang')
 def row(role,parent,source):return {'person_id':roles[role],'representative_source_person_id':roles[role],'source_person_ids':[roles[role]],'identity_equivalence_decision_ids':[],'parent_person_id':roles[parent]if parent else None,'source_assertion_id':source}
 additions=[]
 for role,parent,aid in [('shixiu','hui','shixiu-father'),('shiji','xuan-brother','shiji-father')]:additions.append(row(role,parent,'a-song044-wyd-'+aid))
 r=row('xiedun','chong',None);r['parent_connection']={'type':'shared_father_through_sibling','sibling_person_id':roles['hui'],'sibling_assertion_id':'a-song044-wyd-dun-brother','sibling_father_assertion_id':'a-song044-wyd-hui-father','status':'contextual_provisional','human_reviewed':False,'rationale':'本源晦弟遯與晦明父重，首選共同父；不是遯父重原文明說，不推同母。','references':[reference(by['a-song044-wyd-dun-brother'],ch),reference(by['a-song044-wyd-hui-father'],ch)]};additions.append(r)
 for role in ['shao','shiyou']:
  r=row(role,None,None);r.update({'ancestor_person_id':roles['chong'],'connection':'grandfather','generation_distance':2,'intermediate_person_ids':[None],'interpretation_note':'晦兄子與晦父重限定推定祖重；闕一父代，未建父人、不指定絢、不推兩侄同父。','ancestor_connection':{'type':'wyd_song044_paternal_nephew_to_uncle_father','uncle_person_id':roles['hui'],'nephew_assertion_id':'a-song044-wyd-'+role+'-uncle','uncle_father_assertion_id':'a-song044-wyd-hui-father','status':'contextual_provisional','human_reviewed':False,'rationale':'有據近系編輯推導，非原文明祖；星號只是未知一代，不代表兩侄共享某已知父。','references':[reference(by['a-song044-wyd-'+role+'-uncle'],ch),reference(by['a-song044-wyd-hui-father'],ch)]}});additions.append(r)
 for r in additions:
  old=[x for x in family['members']if x['person_id']==r['person_id']]
  if old:
   if old!=[r]:raise ValueError('宋044家族新行與現役不同')
  else:family['members'].append(r)
 sid='family-song044-wyd-shangxuanshi';members=[row('shangxuanshi',None,None),row('huaifu','shangxuanshi','a-song044-wyd-huaifu-father')];new={'id':sid,'root_person_id':roles['shangxuanshi'],'label':'商玄石與懷福：本源明父子','status':'editorial_preferred','human_reviewed':False,'reviewer':'Codex（AI代理）','rationale':'只按本源其子懷福；不補母或姓氏成分。','members':members}
 old=[a for a in after['assemblies']if a['id']==sid]
 if old:
  if old!=[new]:raise ValueError('宋044商氏組裝與現役不同')
 else:after['assemblies'].append(new)
 return after
