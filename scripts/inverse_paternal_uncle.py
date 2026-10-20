"""Literal inverse copulas only; not an inferred father or kinship distance."""
import re

def inverse_uncle_direction(p,subjects,objects,term):
 t=p['text']
 for s in subjects:
  for o in objects:
   # uncle + named nephew + 之叔父; both marked names abut literally.
   if o['end']==s['start']and t[s['end']:].startswith('之叔父')and '叔父'in term:return True
   # Biography opening uncle字... [nephew's office] nephew伯父也.
   gap=t[o['end']:s['start']]
   head=(o['start']==0 or (re.fullmatch(r'[^曰云，。；：]{1,12}曰',t[:o['start']])and not any(m.get('kind')=='person'and m['start']<o['start']for m in p.get('mentions',[]))))
   if (head and o['end']<s['start']and re.fullmatch(r'字[^之曰云：，。；]{1,16}',gap)
       and t[s['end']:].startswith('伯父也')and'伯父'in term
       and not any(m.get('kind')=='person'and o['end']<=m['start']<s['start']and m.get('person_id')!=o.get('person_id')for m in p.get('mentions',[]))):return True
 return False
