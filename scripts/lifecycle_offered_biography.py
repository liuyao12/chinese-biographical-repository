"""Small literal lifecycle bindings; all roles are resolved from source anchors."""
def end_valid(h,paras,mentions):
 try:
  b=h['end_basis'];e,=b['evidence'];_,p=paras[e['paragraph_id']];t=p['text'];m=mentions[e['person_mention_id']][2];title=h['title'];att,=h['attestations'];end=h['effective_period']['end']
  if e['quote']!=t or m['person_id']!=h['person_id']or att['person_mention_id']!=m['id']or t[att['start']:att['end']]!=title or end['evidence']!=b['evidence']or end['event_type']!='explicit_end'or end['status']!='source_event':return False
  if b['kind']=='named_last_office_mourning_leave':return b['source_term']=='以父憂去職'and title=='太子舍人'and t[att['start']-1:att['end']+len('，以父憂去職。服闋，復爲舍人')]=='遷太子舍人，以父憂去職。服闋，復爲舍人'and t.startswith('起家撫軍法曹行參軍，遷') and m['surface']=='朏'
  if b['kind']=='named_son_office_removed_for_slaughtering_cattle':return b['source_term']=='坐殺牛免官'and t.startswith('子'+m['surface']+'，官至'+title+'，坐殺牛免官，卒於家。')and m['start']==1 and att['start']==m['end']+3
  return False
 except(KeyError,TypeError,ValueError):return False

def gift_valid(h,paras,mentions,life_events):
 try:
  b=h['posthumous_basis'];e,=b['evidence'];_,p=paras[e['paragraph_id']];t=p['text'];m=mentions[b['recipient_person_mention_id']][2];r=mentions[b['sovereign_person_mention_id']][2];a,=h['attestations']
  return (set(b)=={'kind','source_term','death_term','grant_term','recipient_person_mention_id','sovereign_person_mention_id','evidence'}and e['quote']==t==b['source_term']and e['person_mention_id']==m['id']and m['person_id']==h['person_id']and r['person_id']!=m['person_id']and r['surface']=='輿駕'and b['death_term']=='是冬薨於府'and b['grant_term']=='贈侍中、司徒'and h['title']in ('侍中','司徒')and m['end']<t.index(b['death_term'])<r['start']<t.index(b['grant_term'])<a['end']and t[m['start']:m['end']]=='朏'and '時年六十六。輿駕出臨哭，詔給東園秘器'in t and t[a['start']:a['end']]==h['title']and h['mode']=='posthumous_grant')
 except(KeyError,TypeError,ValueError):return False
