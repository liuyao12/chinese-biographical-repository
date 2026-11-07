"""Only explicit biography-opening 母 and child尊母 title clauses."""
def maternal_title_scope_valid(a,paragraphs):
 try:
  q=a['qualifiers'];e=a['evidence'][0];cid,p=paragraphs[e['paragraph_id']];t=p['text'];ms={m['id']:m for m in p['mentions']};s=ms[e['subject_person_mention_id']];o=ms[e['object_person_mention_id']]
  if (a['predicate']!='maternal_role'or set(q)!={'source_term','role','biological_mother','father_person_id'}
      or q['role']!='mother_unspecified'or q['biological_mother']is not None or q['father_person_id']is not None
      or q['source_term']!='母'+o['surface']or t[o['start']-1:o['end']]!=q['source_term']
      or s['person_id']!=a['subject_person_id']or o['person_id']!=a['object_person_id']or (s['kind']!='person'or o['kind']!='person')
      or cid!=e['chapter_id']or e['quote']!=t or len(a['evidence'])!=1):return False
  # A named child immediately precedes 尊母. It cannot be a different emperor earlier in the paragraph.
  if s['end']+2==o['start']and t[s['end']:o['start']]=='尊母':return True
  if _gifted_parents_biography(a,p,s,o):return True
  # This biography's opening personal name and explicit parent formula precede 母.
  opening=next((m for m in p['mentions']if m['start']==0 and m['person_id']==a['subject_person_id']),None)
  if not opening:return False
  prefix=t[opening['end']:o['start']]
  return(prefix.startswith('諱')and prefix.endswith('中子也母')and len(prefix)<=32
         and not any(ch in prefix for ch in '曰云：：「『')
         and any(m['person_id']==a['subject_person_id']and opening['end']<=m['start']<o['start']for m in p['mentions']))
 except(KeyError,TypeError,StopIteration):return False

def _gifted_parents_biography(a, p, s, o):
    """Biography-topic parents in 贈父〈office〉〈name〉〈title〉，母〈clan〉〈title〉."""
    import re
    t = p['text']
    if p.get('text_layer') != 'received_chapter':
        return False
    marks = p['mentions']
    for m in (s, o):
        if (type(m.get('start')) is not int or type(m.get('end')) is not int
                or not 0 <= m['start'] < m['end'] <= len(t)
                or t[m['start']:m['end']] != m['surface']):
            return False
    if (s['start'] != 0 or not s['surface'].endswith(('皇后', '王妃', '皇帝'))
            or not t[s['end']:].startswith('諱')
            or s['person_id'] == o['person_id']):
        return False
    names = [m for m in marks if m.get('kind') == 'person'
             and m.get('start') == s['end'] + 1
             and m.get('person_id') == s['person_id']
             and type(m.get('end')) is int
             and t[m['start']:m['end']] == m.get('surface')
             and t[m['end']:].startswith('，')]
    if len(names) != 1:
        return False
    left = t.rfind('。', 0, o['start']) + 1
    end = t.find('。', o['end'])
    if end < 0 or not t[left:].startswith('贈父'):
        return False
    if any(c in t[:end] for c in '曰云：:「」『』'):
        return False
    parents = [m for m in marks if m.get('kind') == 'person'
               and left <= m.get('start', -1) < o['start']]
    if len(parents) != 1:
        return False
    f = parents[0]
    if (type(f.get('start')) is not int or type(f.get('end')) is not int
            or not left + 2 < f['start'] < f['end'] < o['start']
            or t[f['start']:f['end']] != f.get('surface')
            or f.get('person_id') in (s['person_id'], o['person_id'])):
        return False
    # Only office/title wording occupies the gaps; named intermediaries or
    # kinship narratives are not part of this compact parents-grant formula.
    office = r'[\u3400-\u9fff]{1,12}(?:郎|卿|大夫|將軍|太守|刺史|校尉|尚書)'
    title = r'[\u3400-\u9fff]{1,12}(?:卿|大夫|將軍|侯|公|王)'
    before = t[left + 2:f['start']]
    after = t[f['end']:o['start']]
    mother_title = t[o['end']:end]
    if (not re.fullmatch(office, before)
            or not after.endswith('，母')
            or not re.fullmatch(title, after[:-2])
            or not re.fullmatch(r'[\u3400-\u9fff]{1,12}(?:鄉君|縣君|郡君|夫人)', mother_title)
            or any(c in before + after[:-2] + mother_title for c in '父母子女兄弟祖孫曰云')):
        return False
    return not any(m.get('kind') in ('person', 'pronoun')
                   and left <= m.get('start', -1) < end
                   and m['id'] not in (f['id'], o['id']) for m in marks)

