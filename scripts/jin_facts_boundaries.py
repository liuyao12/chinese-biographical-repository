"""原詞受約束的年登、並稱疾不起、追復及連續紀年邊界。"""
import hashlib,re

def grouped_non_assumption_valid(proposal,p,person,role,appointment,refusal,carried):
    if not carried or appointment['surface']!='除' or refusal['surface']!='稱疾不起':return False
    text=p['text'];segment=text[appointment['end']:refusal['start']]
    if not segment.endswith('，並'):return False
    titles=segment[:-2].split('、')
    if len(titles)<2 or any(not t or re.search('[。；：！？「」曰]',t)for t in titles):return False
    start=appointment['end'];members=[]
    for title in titles:members.append((start,start+len(title),title));start+=len(title)+1
    if (role['start'],role['end'],role['surface'])not in members:return False
    # The same carried topic must explicitly resume after the entire shared refusal.
    resumed=next((m for m in p['mentions']if m.get('kind')=='person'and m.get('person_id')==proposal['person_id']and m['start']>=refusal['end']),None)
    return bool(resumed)and not any(m.get('kind')=='person'and appointment['end']<=m['start']<refusal['end']for m in p['mentions'])

def posthumous_restoration_valid(event,chapters,events):
    try:
        if event['restoration_kind']!='posthumous_restore_unnamed_office' or event['event_type']!='office_restoration':return False
        if event.get('date_expression')is not None or event.get('normalized_date')is not None:return False
        e,=event['evidence'];c=chapters[e['chapter_id']];p=next(p for p in c['paragraphs']if p['id']==e['paragraph_id']);m=next(m for m in p['mentions']if m['id']==e['person_mention_id']);a=event['source_anchor']
        if m.get('person_id')!=event['person_id']or m.get('kind')!='person':return False
        expected='詔追復'+m['surface']+'本官'
        if event['source_term']!=expected or a!={'paragraph_id':p['id'],'start':m['start']-3,'end':m['end']+2,'surface':expected}or p['text'][a['start']:a['end']]!=expected:return False
        death=events[event['death_event_id']]
        if death['event_type']!='death'or death['person_id']!=event['person_id']or death['status']!='source_attested':return False
        order={p['id']:i for i,p in enumerate(c['paragraphs'])}
        return e['quote']==p['text']and bool(death['evidence'])and all(d['chapter_id']==c['id']and order[d['paragraph_id']]<order[p['id']]for d in death['evidence'])and event['human_reviewed']is False
    except (KeyError,TypeError,ValueError,StopIteration):return False

def continuous_annal_valid(date,parse):
    try:
        m=date['regnal_year_mapping'];refs=date['references'];modern=refs[m['reference_index']];ref=refs[m['context_reference_index']];s=ref['section'];ctx=date['annal_year_reference'];raw=s['raw_quote'];lines=raw.splitlines();lo,hi=s['source_lines'];era=m['era_name'];n=m['regnal_year'];first=m['start_ce_year'];last=m['end_ce_year'];num=m['source_number'];start,end=s['year_source_lines']
        if ctx['format']!='kanripo_continuous_year'or m['kind']!='annal_ce_regnal_era_span'or parse(num)!=n or m.get('target_regnal_year')!=n or date.get('era_year')!=date.get('year') or date['year']!=first+n-1 or date['era']!='CE'or not first<=date['year']<=last:return False
        if len(lines)!=hi-lo+1 or hashlib.sha256(raw.encode()).hexdigest()!=s['raw_quote_sha256']or ctx['section_id']!=s['id']:return False
        # Explicit era-year-one, sequential year headings, no alternative era between.
        clean=lambda x:x[:-1]if x.endswith('¶')else x
        body=[clean(x)for x in lines]
        if not body[0].startswith(era+'元年')or not(lo<start<=end<hi)or not body[start-lo].startswith(num+'年')or not body[end-lo+1].startswith(s['next_year_number']+'年')or parse(s['next_year_number'])!=n+1:return False
        headings=[(i,t)for i,t in enumerate(body)if re.match(r'^[元一二三四五六七八九十]+年',t)]
        if [parse(re.match(r'^([元一二三四五六七八九十]+)年',t)[1])for i,t in headings]!=list(range(2,n+2)):return False
        if sum('改元'in x for x in body)>1 or any(re.match(r'^[^<\s]{2}元年',x)for x in body[1:]):return False
        projected=''.join(x for x in body[start-lo:end-lo+1]if not re.fullmatch(r'<pb:[^>]+>',x))
        e,=date['evidence']
        return projected==date['original_quote']==e['quote']and date['source_expression']==num+'年'and ref['scope']=='primary_annal_year_section_context'and ref['quote']==raw and ref['source_revision']==s['source_revision']and ref['image_verified']is False and ref['url'].startswith('https://')and modern['scope']=='modern_era_year_equivalence_only'and modern['columns']['era_name']==era and modern['columns']['first_year']==str(first)and modern['columns']['last_year']==str(last)and ctx['event_paragraph_id']==e['paragraph_id']and all(ref[k]==e[k]for k in ['work_id','book_id','chapter_id','source_id'])
    except (KeyError,TypeError,ValueError,IndexError):return False

def continuous_annal_binding_valid(date,chapter):
    try:
        ctx=date['annal_year_reference'];r=date['references'][date['regnal_year_mapping']['context_reference_index']];s=r['section'];p=next(p for p in chapter['paragraphs']if p['id']==ctx['event_paragraph_id']);pos=p['source_position'];src=chapter['source']
        return s in src['annal_year_sections']and src['revision_id']==r['source_revision']==s['source_revision']==pos['revision_id']and p['text']==date['original_quote']and [pos['first_line'],pos['last_line']]==s['year_source_lines']and all(r[k]==chapter['id'if k=='chapter_id'else k]for k in ['work_id','book_id','chapter_id','source_id'])
    except (KeyError,TypeError,ValueError,StopIteration):return False


def resumed_invitation_refusal_valid(proposal,p,person,role,appointment,refusal,carried):
    if not carried or proposal.get('appointment_stage')!='invitation'or appointment['surface']not in ['請為','請爲']or refusal['surface']!='固辭不起':return False
    if appointment['end']!=role['start']:return False
    resumed=next((m for m in p['mentions']if m.get('kind')=='person'and m.get('person_id')==proposal['person_id']and m['end']==refusal['start']),None)
    return bool(resumed)and resumed['start']>role['end']and p['text'][resumed['start']-1]in '」』'and not any(m.get('kind')=='person'and m.get('person_id')!=proposal['person_id']and resumed['start']<=m['start']<refusal['end']for m in p['mentions'])
