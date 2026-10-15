# coding: utf-8
"""由已標記年表及既有 CBR 人物檔產生無 NLU 的閱讀器人物資料。"""
import json
from collections import defaultdict
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
def build(root=ROOT):
    ROOT = root
    catalog = json.loads((ROOT/'data/corpus/index.json').read_text())
    chapters = {x.get('chapter_id'):x for x in catalog['chapters']}
    people = json.loads((ROOT/'data/corpus/persons.json').read_text())
    name_records = json.loads((ROOT/'data/corpus/profile-names.json').read_text())['records']
    candidates = {p['id']:p for p in json.loads((ROOT/'data/historical-tables/person-candidates.json').read_text())['persons']}
    table_mentions = defaultdict(list)
    for path in sorted((ROOT/'data/historical-tables').glob('shiji-*.json')):
        table = json.loads(path.read_text())
        for fragment in table['fragments']:
            for row in fragment['rows']:
                for cell in row['cells']:
                    for m in cell['person_mentions']:
                        table_mentions[m['person_id']].append({'table_id':table['id'],'cell_id':cell['id'],'title':table['title'],'quote':cell['text'],'year':row['year'],'mention':m})
    bundles = json.loads((ROOT/'exports/persons/index.json').read_text())
    for pid in set(people) | {p['person_id'] for p in bundles['persons']}:
        table_mentions.setdefault(pid, [])
    out = ROOT/'data/corpus/profiles'; out.mkdir(exist_ok=True)
    # Only the current registry/index and table mentions define this directory;
    # retired IDs are removed after all source references have been migrated.
    for path in out.glob('*.json'):
        if path.stem != 'index' and path.stem not in table_mentions: path.unlink()
    for pid, cells in sorted(table_mentions.items()):
        if pid in candidates:
            candidate = candidates[pid]
            profile = {'schema_version':1,'id':pid,'canonical_person_id':pid,'label':candidate['label'],'identity_note':candidate['identity_note'],'review':'source_local_candidate','names':[candidate['source_surface']],'titles':[],'addresses':[],'occurrences':[],'table_occurrences':cells,'sources':[],'relations':[],'related_people':{},'dates':[]}
            (out/f'{pid}.json').write_text(json.dumps(profile,ensure_ascii=False,indent=2)+'\n')
            continue
        b = json.loads((ROOT/'exports/persons'/f'{pid}.json').read_text())
        own = set(b['person_ids']); ps = {p['id']:p for p in b['passages']}
        groups = defaultdict(list)
        for m in b['mentions']: groups[m['chapter_id']].append(m)
        occurrences = []
        for cid, ms in sorted(groups.items(), key=lambda x:chapters.get(x[0],{}).get('number',999)):
            ch = chapters.get(cid)
            if not ch: continue
            m = ms[0]; p = ps[m['paragraph_id']]; start = max(0,m['start']-35)
            occurrences.append({'number':ch['number'],'category':ch['category'],'title':ch['title'],'paragraph_id':p['id'],'count':len(ms),'quote':p['text'][start:m['end']+100]})
        titles = []
        for x in b['title_holdings']:
            if x['person_id'] not in own: continue
            period = x.get('effective_period',{}); bounds=[]
            for key in ('start','end'):
                z=period.get(key,{}); d=z.get('normalized_date') or {}; value=d.get('era_year')
                try:
                    from .date_ranges import year_range_label
                except ImportError:
                    from date_ranges import year_range_label
                if z.get('normalized_date_range'):
                    bounds.append(year_range_label(z['normalized_date_range']))
                    continue
                bounds.append((f'西元{"前" if d.get("era")=="BCE" else ""}{value}年（暫定）' if value else z.get('date_expression')) or '未定')
            titles.append(dict(x, period=' → '.join(bounds)))
        addresses=[dict(x, term=x.get('source_term') or x['place']['source_name'], quote=x['evidence'][0]['quote']) for x in b['address_assertions'] if x['person_id'] in own]
        non_alias_mentions = {d['preferred_reading']['person_mention_id'] for d in b.get('identity_decisions', [])
                              if d.get('preferred_reading', {}).get('source_spelling_is_not_alias') is True}
        names=[]
        for p in b['persons']:
            if p['id'] in own:
                for a in p.get('aliases',[]):
                    if a.get('mention_ids') and set(a['mention_ids']).issubset(non_alias_mentions):
                        continue
                    s=a['surface']
                    if s not in names:names.append(s)
        for cell in cells:
            surface = cell['mention']['surface']
            if surface not in names: names.append(surface)
        profile={'schema_version':1,'id':pid,'canonical_person_id':b['canonical_person_id'],'label':people.get(pid, {}).get('label', next((p['label'] for p in b['persons'] if p['id'] == pid), pid)),'identity_note':people.get(pid, {}).get('identity_note'),'review':'ai_provisional','names':names,'titles':titles,'addresses':addresses,'occurrences':occurrences,'table_occurrences':cells,'sources':b['sources'],'relations':[x for x in b['relations'] if x['subject_person_id'] in own],'related_people':{p['id']:p['label'] for p in b['persons']},'dates':[x for x in b['date_normalizations'] if x.get('person_id') in own]}
        preferred_readings = [dict(d['preferred_reading'], decision_id=d['id']) for d in b.get('identity_decisions', []) if d.get('preferred_reading')]
        if preferred_readings:
            profile['preferred_readings'] = preferred_readings
        if b.get('unresolved_identity_cases'):
            profile['unresolved_identity_cases'] = b['unresolved_identity_cases']
        readings = [d for d in b.get('identity_decisions', []) if d.get('references')]
        if readings:
            profile['reading_decisions'] = readings
        profile['name_components'] = [r for r in name_records if r['person_id'] in own]
        profile['person_ids'] = b['person_ids']
        profile['relations'] = b['relations']
        profile['preferred_relations'] = b.get('preferred_relations', b['relations'])
        if b.get('assembled_identity'):
            profile['assembled_identity'] = b['assembled_identity']
        if b.get('assembled_children'):
            profile['assembled_children'] = b['assembled_children']
        profile['age_assertions'] = b.get('age_assertions', [])
        profile['life_events'] = [x for x in b.get('life_events', []) if x['person_id'] in own]
        profile['life_event_date_decisions'] = b.get('life_event_date_decisions', [])
        profile['selected_life_event_dates'] = b.get('selected_life_event_dates', [])
        if b.get('reported_variants'):
            profile['reported_variants'] = b['reported_variants']
        (out/f'{pid}.json').write_text(json.dumps(profile,ensure_ascii=False,indent=2)+'\n')
    entries = []
    for pid in sorted(table_mentions):
        p = json.loads((out/f'{pid}.json').read_text())
        entries.append({'id':pid,'label':p['label'],'names':p['names'],'path':f'data/corpus/profiles/{pid}.json','review':p['review']})
    (out/'index.json').write_text(json.dumps({'schema_version':1,'profiles':entries},ensure_ascii=False,indent=2)+'\n')
    print('閱讀器人物資料：', len(table_mentions), '份 ID 檔（含同指別名，不是不同人物總數）')
if __name__=='__main__': build()
