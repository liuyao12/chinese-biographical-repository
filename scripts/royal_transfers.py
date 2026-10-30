# coding: utf-8
"""Bind an explicitly stated royal transfer to its source and prior holding."""
import re

def chronology_choice_errors(holding, paragraphs, chapters):
    choice=holding.get('chronology_source_choice')
    if not isinstance(choice,dict):return ['轉封紀年首選須有分存的來源判讀']
    evidence=choice.get('alternative_evidence');start=holding.get('effective_period',{}).get('start',{})
    alternate=paragraphs.get(evidence.get('paragraph_id')) if isinstance(evidence,dict) else None
    valid=(choice.get('status')=='editorial_provisional' and choice.get('human_reviewed') is False
           and isinstance(choice.get('rationale'),str) and bool(choice['rationale'].strip())
           and choice.get('preferred_source_expression')==start.get('date_expression')
           and bool(start.get('evidence')) and all(e.get('chapter_id')==choice.get('preferred_chapter_id') for e in start['evidence'])
           and alternate and alternate[0]==choice.get('alternative_chapter_id')==evidence.get('chapter_id')
           and chapters.get(alternate[0],{}).get('source_id')==evidence.get('source_id')
           and isinstance(evidence.get('quote'),str) and bool(evidence['quote']) and evidence['quote'] in alternate[1]['text']
           and isinstance(choice.get('alternative_source_term'),str) and bool(choice['alternative_source_term']) and choice['alternative_source_term'] in evidence['quote']
           and any(m.get('person_id')==holding.get('person_id') for m in alternate[1]['mentions']))
    fixed=False
    for ref in choice.get('references',[]):
        if not isinstance(ref,dict) or not isinstance(ref.get('quote'),str):continue
        quote=re.sub(r'[¶/\s]','',re.sub(r'<pb:[^>]*>','',ref['quote']));commit=ref.get('source_commit','');blob=ref.get('source_blob','')
        if 'display_quote' in ref and ref['display_quote']!=quote:return ['轉封紀年引文顯示不得改動原字']
        if (isinstance(commit,str) and re.fullmatch('[a-f0-9]{40}',commit)
                and isinstance(blob,str) and re.fullmatch('[a-f0-9]{40}',blob)
                and isinstance(ref.get('url'),str) and ref['url'].startswith('https://') and commit in ref['url']
                and ref.get('image_verified') is False and '孝文十二年徙王淮南五年復還王城陽' in quote):fixed=True
    return [] if valid and fixed else ['轉封紀年首選須對應實存的兩篇原句、同一人物與固定平行紀年，不得抹去年數差異']

def resumption_valid(holding, previous, holdings, mentions):
    """A return can elide 王, while retaining an actual pre-transfer rank word."""
    basis=holding.get('resumption_basis');transfer=holding.get('transfer_basis',{})
    keys={'earlier_holding_id','previous_source_title','return_source_term','status','rationale','human_reviewed'}
    if not isinstance(basis,dict) or set(basis)!=keys:return False
    earlier=holdings.get(basis.get('earlier_holding_id'));anchor=mentions.get(transfer.get('actor_mention_id'))
    dest=holding.get('jurisdictions',[]);origin=previous.get('jurisdictions',[]) if previous else []
    if not (earlier and anchor and previous and holding.get('title')=='王' and previous.get('title')=='王'
            and earlier.get('person_id')==holding.get('person_id') and earlier.get('kind')=='royal_rank'
            and earlier.get('mode')not in ('posthumous_grant','posthumous_enfeoffment','posthumous_naming')
            and previous.get('transfer_basis',{}).get('previous_holding_id')==earlier.get('id')
            and isinstance(dest,list) and len(dest)==1 and isinstance(origin,list) and len(origin)==1
            and isinstance(dest[0],dict) and isinstance(origin[0],dict)
            and isinstance(dest[0].get('source_name'),str) and isinstance(origin[0].get('source_name'),str)
            and dest[0]['source_name']!=origin[0]['source_name']
            and earlier.get('title')==dest[0]['source_name']+'王'
            and basis.get('previous_source_title')==origin[0]['source_name']+'王'
            and anchor[2].get('surface','').startswith(basis['previous_source_title'])
            and basis.get('return_source_term')=='復故'+dest[0]['source_name']
            and transfer.get('title_source_term')==basis['return_source_term']
            and transfer.get('source_term')=='徙'+anchor[2]['surface']+basis['return_source_term']
            and basis.get('status')=='editorial_provisional' and basis.get('human_reviewed') is False
            and isinstance(basis.get('rationale'),str) and bool(basis['rationale'].strip())):return False
    # This 王 is literally in the prior style, not a fabricated destination title.
    rank_start=anchor[2]['start']+len(origin[0]['source_name'])
    return any(a.get('person_mention_id')==anchor[2]['id'] and a.get('surface')=='王'
               and a.get('start')==rank_start and a.get('end')==rank_start+1
               and a.get('context_role')=='pre_transfer_rank' for a in holding.get('attestations',[]))

def royal_transfer_errors(holding, holdings, paragraphs, mentions, *, chapters=None, root=None):
    if holding.get('transfer_basis',{}).get('kind')=='fixed_jin031_title_change':
        try:from scripts.fixed_jin031_jia_remaining_titles import transfer_valid
        except ImportError:from fixed_jin031_jia_remaining_titles import transfer_valid
        return [] if transfer_valid(holding,holdings,paragraphs,mentions,chapters,root) else ['031公主改封須完整本源、同人前爵與同證終始']
    if (isinstance(holding.get('transfer_basis'), dict)
            and holding['transfer_basis'].get('kind') == 'elided_rank_regrant'):
        try:
            from scripts.elided_royal_regrants import elided_royal_regrant_errors
        except ImportError:
            from elided_royal_regrants import elided_royal_regrant_errors
        return elided_royal_regrant_errors(holding, holdings, paragraphs, mentions)
    basis = holding.get('transfer_basis')
    keys = {'previous_holding_id', 'source_term', 'title_source_term', 'actor_mention_id', 'evidence'}
    if not isinstance(basis, dict) or set(basis) != keys:
        return ['徙王須明示前王號、原詞、人物錨點及同次來源']
    previous = holdings.get(basis['previous_holding_id'])
    start = holding.get('effective_period', {}).get('start', {})
    if not (holding.get('mode') == 'transfer' and holding.get('kind') == 'royal_rank'
            and previous and previous.get('id') != holding.get('id')
            and previous.get('person_id') == holding.get('person_id') and previous.get('kind') == 'royal_rank'
            and previous.get('mode') not in ('posthumous_grant', 'posthumous_enfeoffment', 'posthumous_naming')
            and start.get('status') == 'source_event' and start.get('event_type') == 'transfer'
            and basis.get('evidence') == start.get('evidence') and bool(basis['evidence'])):
        return ['徙王須指同人的原王號與明示徙封起點，不得當繼位或跨人移接']
    old_end = previous.get('effective_period', {}).get('end', {})
    if not (old_end.get('status') == 'source_event' and old_end.get('event_type') == 'explicit_end'
            and old_end.get('evidence') == basis['evidence']
            and all(old_end.get(k) == start.get(k) for k in ('date_expression', 'normalized_date', 'normalized_date_range'))):
        return ['徙王新始與前號明示終點須為同一事件與同一日期，不得借死亡補終期']
    term, title_term = basis.get('source_term'), basis.get('title_source_term')
    nominal = (isinstance(term, str) and isinstance(title_term, str)
               and title_term == holding['title'] and '徙為' + title_term in term)
    places = holding.get('jurisdictions', [])
    resumption = resumption_valid(holding, previous, holdings, mentions)
    if 'resumption_basis' in holding and not resumption:
        return ['復故王地須連同人的此前王地、原稱與復故原詞，不得補造目的地王號錨點']
    predicative = (holding.get('title') == '王' and isinstance(places, list) and len(places) == 1
                   and isinstance(places[0], dict) and isinstance(places[0].get('source_name'), str)
                   and title_term == '王' + places[0]['source_name'] and isinstance(term, str)
                   and '徙' + previous['title'] + title_term in term)
    if not (nominal or predicative or resumption) or previous['title'] == holding['title'] and previous.get('jurisdictions') == holding.get('jurisdictions'):
        return ['徙王原詞須明言新王號或王某地，不得由任意地名重排稱號']
    anchor = mentions.get(basis.get('actor_mention_id'))
    if not (anchor and anchor[2].get('kind') == 'person'
            and anchor[2].get('person_id') == holding['person_id'] and (anchor[2].get('surface') == previous['title'] or resumption)):
        return ['徙王人物錨點須指同人的原王號']
    for evidence in basis['evidence']:
        hit = paragraphs.get(evidence.get('paragraph_id'))
        if not hit or anchor[1] != evidence.get('paragraph_id'):
            return ['徙王人物與引句段落不符']
        text = hit[1]['text']; quote = evidence.get('quote')
        starts = [i for i in range(len(text)) if text.startswith(term, i)]
        eligible = [i for i in starts if i <= anchor[2]['start'] < anchor[2]['end'] <= i + len(term)]
        if not (isinstance(quote, str) and quote in text and term in quote and eligible
                and any(not any(m.get('kind') == 'person' and m.get('person_id') != holding['person_id']
                                and i <= m['start'] < i + len(term) for m in hit[1]['mentions']) for i in eligible)):
            return ['徙王原詞須包含原王錨點，不得跨另一人物拼接授任']
    seen = {holding['id']}; cursor = previous
    while cursor:
        if cursor['id'] in seen:
            return ['徙王前職引用不得循環']
        seen.add(cursor['id']); cursor = holdings.get(cursor.get('transfer_basis', {}).get('previous_holding_id'))
    return []
