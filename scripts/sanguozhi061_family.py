"""吳書卷十六的族子、族弟、從兄與引書姨兄。"""
RULES={
'a-wu061-lukai-2':('lukai','021','kinship_unspecified','丞相遜族子也','陸凱字敬風','陸凱','丞相遜族子','遜'),
'a-wu061-lukai-3':('lukai','042','kinship_unspecified','族弟喜，抗','凱陳：','凱','族弟喜，抗','喜'),
'a-wu061-lukai-4':('lukai','042','kinship_unspecified','族弟喜，抗','凱陳：','凱','族弟喜，抗','抗'),
'a-wu061-luyin-2':('luyin','072','agnatic_cousin','與從兄禕','子式嗣','式','與從兄禕','禕'),
'a-wu061-jiangwan-cousin':('panjun','014-pei04-02','maternal_cousin','濬姨兄零陵蒋琬','濬姨兄','濬','零陵蒋琬','蒋琬'),
}
STRUCTURE=dict(lineage='maternal',generation_difference=0,collateral=True,maternal_path='mother_sister_son',distance=None,common_ancestor_person_id=None,subject_relative_age='younger')
def anchor(p,context,word):
 if p['text'].count(context)!=1:return None
 a=p['text'].index(context)+context.index(word)
 return next((m for m in p['mentions']if m['kind']=='person'and m['surface']==word and m['start']==a and m['end']==a+len(word)),None)
def valid(a,paragraphs):
 rule=RULES.get(a.get('id'))
 if not rule or len(a.get('evidence',[]))!=1:return False
 slug,line,pred,term,sc,sw,oc,ow=rule;cid='c-sanguozhi-061-'+slug;pid=cid+':line'+line;e=a['evidence'][0];h=paragraphs.get(pid)
 if not h or h[0]!=cid or (e.get('chapter_id'),e.get('paragraph_id'))!=(cid,pid):return False
 p=h[1];q={'source_term':term}
 if pred=='maternal_cousin':q['kinship_structure']=STRUCTURE
 if a.get('predicate')!=pred or a.get('qualifiers')!=q or e.get('quote')!=p['text']or p['source_position'].get('revision_id')!=2085162:return False
 for role,ctx,w in [('subject',sc,sw),('object',oc,ow)]:
  m=anchor(p,ctx,w)
  if not m or (a.get(role+'_person_id'),e.get(role+'_person_mention_id'))!=(m['person_id'],m['id']):return False
 return True
