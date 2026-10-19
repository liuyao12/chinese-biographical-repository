"""正文以外的紀年語境；只輸出已驗證之年，不填生卒／任職欄。"""
import hashlib,json,re
from pathlib import Path

def digest(b): return hashlib.sha256(b).hexdigest()
def errors(record, root, paragraphs=None):
    es=[]
    def ck(ok,msg):
        if not ok:es.append(msg)
    try:
        ck(record['record_type']=='calendar_context_assertion_set' and record['schema_version']==1,'紀年集型別不符')
        ck(len({r['id'] for r in record['records']})==len(record['records']),'紀年ID重複')
        for r in record['records']:
            s=r['source'];path=Path(root)/s['file']
            ck(not Path(s['file']).is_absolute() and '..' not in Path(s['file']).parts,'來源路徑不得逸出root')
            raw=path.read_bytes();ls=raw.decode().splitlines()
            ck(digest(raw)==s['sha256'],'原始來源雜湊不符')
            ck(str(s['revision_id']) in s['url'] and s['url'].startswith('https://zh.wikisource.org/w/index.php?'),'修訂網址不符')
            ctx=r['context_lines'];numbers=[c['line'] for c in ctx]
            ck(numbers==list(range(min(numbers),max(numbers)+1)),'相鄰原行不完整')
            for c in ctx:ck(c['text']==ls[c['line']-1] and c['sha256']==digest(c['text'].encode()),'原行或逐行雜湊不符')
            n=r['raw_line'];text=r['full_paragraph'];a=r['anchor'];b=r['basis'];d=r['normalized_date'];scope=r['scope']
            ck(n in numbers and ls[n-1].lstrip('　 ')==text,'正文與原行不符')
            ck(text[a['start']:a['end']]==a['surface']==r['original_expression'],'日期字元錨點不符')
            ck(0<=scope['start']<=a['start']<a['end']<=scope['end']<=len(text) and text[scope['start']:scope['end']]==scope['quote'],'作用域不符')
            ck(d['calendar']=='chinese_civil' and d['precision']=='year' and d['status']=='editorial_provisional','不得搬動中國曆年或冒充日精度')
            ck(r['image_verified'] is False and r['human_reviewed'] is False and r['model'] is None,'覆核層不符')
            if paragraphs is not None:ck(paragraphs.get(a['paragraph_id'])==text,'篇章原文不符')
            if b['kind']=='same_biographical_timeline_era_continuation':
                c=r['continuity'];prev=c['antecedent_line'];heading=c['unit_heading_line']
                ck(ls[heading-1]==c['unit_heading'] and c['subject'] in c['unit_heading'],'傳主標題不符')
                ck(c['antecedent_term']==b['era_original']+'初' and c['antecedent_term'] in ls[prev-1] and '亮' in ls[prev-1],'年號／同傳主證據不符')
                ck(c['intervening_raw_lines']==list(range(prev+1,n)) and all(not ls[j-1].strip() for j in range(prev+1,n)),'承前正文中斷')
                ck(not any(ls[j-1].lstrip().startswith('=') for j in range(heading+1,n)),'傳文標題中斷')
                ck(c['initial_period_is_year_one'] is False,'不得把初當元年')
                ref=json.loads((Path(root)/c['era_reference']).read_text())
                ck(ref['era']==b['era_reference_form'] and ref['source_orthography']==b['era_original'] and ref['first_year']==b['first_ce_year'],'換算表不符')
                ck(digest((Path(root)/'sources/calendar-context/moe-era-table-page2.html').read_bytes())==ref['response_sha256'],'年號表雜湊不符')
                ck(ref['first_year']==275 and ref['last_year']==280 and b['first_ce_year']==275 and ref['era']=='咸寧','本批年號表列值須為咸寧275至280')
                ck(r['original_expression']=='三年' and b['regnal_year']==3 and d['year']==ref['first_year']+2,'明文年數不符')
                ck(scope['end']==text.index('頃之'),'不得越過頃之套年')
            elif b['kind']=='digital_editorial_year_heading':
                p=r['paratext'];h=p['heading_line'];line=ls[h-1]
                ck(p['layer']=='digital_editorial_paratext' and p['heading_is_body'] is False,'數位年題不得冒充正文')
                ck(h in numbers and line==p['raw_heading'] and digest(line.encode())==p['heading_sha256'],'數位年題原行不符')
                ck('咸和四年（己丑、公元三二九年）' in line and p['era']=='咸和' and p['regnal_year']==4 and p['sexagenary_year']=='己丑' and p['numeral_ce']==d['year']==329,'數位年題年數不符')
                ck(h<n and not any(re.search(r'公元.+年|^\s*=',ls[j-1]) for j in range(h+1,n)),'數位年題至正文間另有年題／標題')
                cut=text.index('丁亥')
                ck((a['surface']=='二月，丙戌' and scope['start']==0 and scope['end']==cut) or (a['surface']=='丁亥' and scope['start']==cut and scope['end']==len(text)),'丙戌／丁亥作用域不得混用')
            else:es.append('未支持的紀年依據')
    except (KeyError,TypeError,ValueError,OSError,IndexError) as exc:es.append('紀年結構錯誤：'+str(exc))
    return es

def validate(root):
    paragraphs={}
    for f in (Path(root)/'corpus').rglob('*.json'):
        d=json.loads(f.read_text())
        for p in d.get('paragraphs',[]):paragraphs[p['id']]=p['text']
    out=[]
    for f in (Path(root)/'corpus/calendar-contexts').glob('*.json'):
        out.extend(errors(json.loads(f.read_text()),root,paragraphs))
    return out

def dates_for_span(record,paragraph_id,start,end):
    """僅整段落在日期範圍內才提供候選年；不自行寫入事件。"""
    return [dict(r['normalized_date'],context_id=r['id']) for r in record['records'] if r['anchor']['paragraph_id']==paragraph_id and r['scope']['start']<=start<end<=r['scope']['end']]
