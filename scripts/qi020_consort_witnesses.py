"""Verify source spans and personal authorities for collected Qi consort readings."""
import hashlib
import json
from pathlib import Path

EXPECTED = {'corpus/houhanshu/010a-qi020-madeng-assertions.json': 'c7d4a77f716a85f4d4e5d8bce70b875e2b8b21fd47356423eca35205c53bc098', 'corpus/houhanshu/010a-qi020-madeng.json': 'c30c63f2c309d8c3bb8108413b190c67ba52b5be98157659050364ba8a9a7d4f', 'corpus/houhanshu/010a-qi020-madeng.xml': 'cb02b5b15824bb78647afbfa1ed39c7dfe6f9efdfeebc966f24944074a2aba09', 'corpus/nanqishu/020-consorts-editorial-wyd.json': '2052cc263b0c318453db4b2165f49f4a7d2a9cfcb8ac2695878893d3ff8d1986', 'corpus/nanqishu/020-consorts-editorial-wyd.xml': '73d829d436efb34418d2a46f2fbe81108f384742d63d544a6bfb1be68042ec14', 'corpus/nanqishu/020-consorts-editorial.json': 'ea96e67fc8cdd7a409f33430a34f602eff3d9321995ccc03c8a32086bc497e1f', 'corpus/nanqishu/020-consorts-editorial.xml': 'b6d5c080cb849c64b5e55e41fd0bae5c58047856df316bbc7ea35178a8965b12', 'corpus/nanqishu/020-consorts-kaozheng-wyd.json': '2fae79ccbfd53e96714f903a2e8aaa9d0961a0db7fba2618f5cc26780c0ee4ef', 'corpus/nanqishu/020-consorts-kaozheng-wyd.xml': 'cb8bfcfb08ecdb272adbd569ccd612f6921af39ec198788c850d413d7f67fbe2', 'corpus/nanqishu/020-hanlanying-wyd-titles.json': 'd919bf3ebbd4deb030651c1984aa4dee4884de5ddea12bb4ca7ab5f5dfde13ee', 'corpus/nanqishu/020-hanlanying-wyd.json': '2666765ae6e8998d6cfd4d383196d68daf07e896176526730297df8a0e8395a6', 'corpus/nanqishu/020-hanlanying-wyd.xml': '167ca360a150bada95db5134716f3b453b374b121515b9f7130a713a7ef5b996', 'corpus/nanqishu/020-peihuizhao-wyd-assertions.json': '5437b5949da16d1f4651a94b12f4bb208e7d5ab9d491ad10a4c1c0dbabab103e', 'corpus/nanqishu/020-peihuizhao-wyd-life-events.json': '8a50952ea8fdb30f005a6e56e7762b017f2181ce49a571bdda73986b23159056', 'corpus/nanqishu/020-peihuizhao-wyd-titles.json': 'e2f786e9c6d3895502159134bec0fd2b010528895073ccfa79709ed1334b9b82', 'corpus/nanqishu/020-peihuizhao-wyd.json': '64187fb23a862f61f26c24e40b72afad783267b511c0415c402bab40185c5a06', 'corpus/nanqishu/020-peihuizhao-wyd.xml': '66ed58c8f19e41228b87364b8559e9f45f1e68ec8f9580bb05932f80069c1813', 'corpus/nanshi/011-hanlanying-izumo-titles.json': '5ba30189d0c74e22ddedf839c56bd55b8059d70fe64e570ff112eff4ed57bac4', 'corpus/nanshi/011-hanlanying-izumo.json': '815d56d502a0bc03de4df85f477fb38d30a28b4a1cbf80febf0bd1bb7d2fed62', 'corpus/nanshi/011-hanlanying-izumo.xml': 'e606313483be589d6529e05b8a389b435b442a3ee5e931eb32d68ca4ad55e654', 'corpus/nanshi/011-peihuizhao-izumo-assertions.json': 'c2bb86db01f9879bf04ec9e33b2162e3f99f84059fb766a796540520a3c25a76', 'corpus/nanshi/011-peihuizhao-izumo-life-events.json': '68d48b07513fe6e26d8fb13b2741ceb45eecb6be0138b8927a09c6fb1a49a197', 'corpus/nanshi/011-peihuizhao-izumo-titles.json': 'a6d81f4306ed8f0065ed03cdc2825d86f8e22afee03aec4a9de429dec8c4b47b', 'corpus/nanshi/011-peihuizhao-izumo.json': 'c43b56132bb2329aea82bb4541c647fc7c3331f66177d76537adb40d8c4283d7', 'corpus/nanshi/011-peihuizhao-izumo.xml': '9abaca13bf345cc10187e965163a9bf280de82ea9bba4eb09a6d737b3a7723d9', 'source-evidence/qi020-consort-audit/consorts-editorial-wyd-columns.txt': '7c36bcf25f9ab8824d179d65db8da4dbd1ca64fb04c1c8a3c950c45709aad119', 'source-evidence/qi020-consort-audit/consorts-editorial-wyd-reading.json': 'be38407ac1481ce6a839ad352a6f36c97164542f82352435c93f28007c78b126', 'source-evidence/qi020-consort-audit/digital-account-coverage.json': '7433d2c294b8aa56592f3c4498fe967326a18eeb439db82e341ef1e5d9073ba9', 'source-evidence/qi020-consort-audit/hanlanying-izumo-columns.txt': '32cfce94928cb3f74413aebe2c7cb73b8a135a09571550a21bd9ba31e44e10d0', 'source-evidence/qi020-consort-audit/hanlanying-izumo-reading.json': '5dc40269d07e2a13ed31f424869025a04fc5b7433e2f9e141905f43278ca8be9', 'source-evidence/qi020-consort-audit/hanlanying-wyd-columns.txt': '499a170130dff4adb3951abcf293877277bab5e8552607b5bee6ec236fa3c1b0', 'source-evidence/qi020-consort-audit/hanlanying-wyd-reading.json': '89648620b069a3afd3b326c12fa4d652aa46ed51f2c1fab3022773fc33609c26', 'source-evidence/qi020-consort-audit/hou10-ws8737760.wikitext': '2704d36cf6a11af9599e259603dba0ac330a092235df35061c36baa4795d396f', 'source-evidence/qi020-consort-audit/kaozheng-wyd-columns.txt': '7321945fbea2d8db3295e4ad22e19035753bfe0d4853b687d4ff701379a2ed80', 'source-evidence/qi020-consort-audit/kaozheng-wyd-reading.json': 'd11ee3c09fb699a0400b884aa5acbf251310521bad3dc625fa05cff2595cf80c', 'source-evidence/qi020-consort-audit/peihuizhao-izumo-columns.txt': 'e5f39ba1264146a566b51b42437a6fcd67b1fc83792ff282e247b2c8810b47f8', 'source-evidence/qi020-consort-audit/peihuizhao-izumo-reading.json': 'db218f43e08fad3f6eee82eff2a29c569a064539998750ff21c352f2749ac772', 'source-evidence/qi020-consort-audit/peihuizhao-wyd-columns.txt': '2bd501a8c124860f0369ad03439d83979a16fd6b974c02fe0ce6b24bacbac83a', 'source-evidence/qi020-consort-audit/peihuizhao-wyd-reading.json': '93b244e12307d7028890a303a94d45e18077d6707888b59f882d0d6e0d054550'}
CHAPTER_PATHS = {'c-houhanshu-010a-qi020-madeng': 'corpus/houhanshu/010a-qi020-madeng.json', 'c-nanqishu-020-consorts-editorial': 'corpus/nanqishu/020-consorts-editorial.json', 'c-nanqishu-020-peihuizhao-wyd': 'corpus/nanqishu/020-peihuizhao-wyd.json', 'c-nanqishu-020-hanlanying-wyd': 'corpus/nanqishu/020-hanlanying-wyd.json', 'c-nanshi-011-peihuizhao-izumo': 'corpus/nanshi/011-peihuizhao-izumo.json', 'c-nanshi-011-hanlanying-izumo': 'corpus/nanshi/011-hanlanying-izumo.json', 'c-nanqishu-020-consorts-editorial-wyd': 'corpus/nanqishu/020-consorts-editorial-wyd.json', 'c-nanqishu-020-consorts-kaozheng-wyd': 'corpus/nanqishu/020-consorts-kaozheng-wyd.json'}
def digest(blob):
    return hashlib.sha256(blob).hexdigest()
def canonical(doc):
    return (json.dumps(doc,ensure_ascii=False,indent=2)+'\n').encode()
def checked(root,path):
    f=Path(root).resolve()/path
    if f.resolve()!=f:
        raise ValueError('資料路徑')
    b=f.read_bytes()
    if path in EXPECTED and digest(b)!=EXPECTED[path]:
        raise ValueError('固定來源指紋')
    return b

def chapter_errors(c,root):
    if c.get('id') not in CHAPTER_PATHS:
        return []
    try:
        file=CHAPTER_PATHS[c['id']]
        if digest(canonical(c))!=EXPECTED[file]:
            raise ValueError('篇章')
        src=c['source']
        raw=checked(root,src['raw_path'])
        if digest(raw)!=src['raw_file_sha256']:
            raise ValueError('版本')
        if src['image_verified']:
            proof=json.loads(checked(root,c['annotation']['print_projection_ref']))
            cols={x['column']:x for x in proof['columns']}
            for p in c['paragraphs']:
                strings=[]
                for part in p['source_position']['column_projection']:
                    col=cols[part['column']]
                    if any(part[k]!=col[k]for k in ('pdf_page','half','leaf','column_from_right','url')):
                        raise ValueError('頁欄')
                    a=part['start']-col['physical_start'];b=part['end']-col['physical_start']
                    if not 0<=a<b<=len(col['reading']) or col['reading'][a:b]!=part['text']:
                        raise ValueError('冊頁內實際欄位')
                    strings.append(part['text'])
                if ''.join(strings)!=p['text']:
                    raise ValueError('篇與欄')
        else:
            text=raw.decode()
            for p in c['paragraphs']:
                pos=p['source_position']
                if ''.join(text[n]for n in pos['raw_character_offsets'])!=p['text']:
                    raise ValueError('原文與校注')
        for path in EXPECTED:
            if path.startswith(file[:-5]+'-') and path.endswith(('-assertions.json','-life-events.json','-titles.json')):
                checked(root,path)
        return []
    except (ValueError,KeyError,IndexError,OSError,TypeError):
        return ['齊后妃卷原文、刊本實際欄位與分層證據未合。']

def frame(record,chapter,root,kind):
    cid=chapter.get('id')
    if cid not in CHAPTER_PATHS:
        return False
    try:
        file=CHAPTER_PATHS[cid]
        if digest(canonical(chapter))!=EXPECTED[file]:
            return False
        suffix='-assertions.json' if kind=='assertions' else '-life-events.json'
        data=json.loads(checked(root,file[:-5]+suffix))
        if record not in data[kind]:
            return False
        pars={p['id']:p for p in chapter['paragraphs']}
        for ev in record['evidence']:
            p=pars[ev['paragraph_id']]
            if ev['quote'] not in p['text']:
                return False
            pool={m['id']:m for m in p['mentions']}
            pool.update({r['id']:r for r in chapter['annotation']['person_reference_occurrences'] if r['paragraph_id']==p['id']})
            if kind=='assertions':
                pairs=[('subject_person',record['subject_person_id']),('object_person',record['object_person_id'])]
                if record['qualifiers']['source_term'] not in ev['quote']:return False
            else:
                pairs=[('person',record['person_id'])]
                a=record['source_anchor']
                if p['text'][a['start']:a['end']]!=record['source_term'] or record['date_expression'] not in ev['quote']:return False
            for prefix,person in pairs:
                mids=[ev[prefix+s]for s in ('_mention_id','_reference_id')if prefix+s in ev]
                if len(mids)!=1 or pool[mids[0]]['person_id']!=person:
                    return False
        return True
    except (KeyError,OSError,ValueError,IndexError,TypeError):return False

def cover(inventory,witnesses):
    for book,first,last in [('b-nanqishu-020',14,52),('b-nanshi-011',92,139)]:
        survey,raw=witnesses[book]
        counts={n:[0]*len(raw[n-1]) for n in range(first,last+1) if raw[n-1].strip() and not raw[n-1].startswith('=')}
        for row in inventory['biographies']:
            if row['book_id']!=book or not first<=row['first_line']<=last:continue
            assert row['item_reviewed'] and row['chapter_id'],row['title']
            for s in [row,*row.get('continuation_spans',[])]:
                assert first<=s['first_line']<=s['last_line']<=last,row['title']
                for n in range(s['first_line'],s['last_line']+1):
                    if n not in counts:continue
                    start=s['start_codepoint'] if n==s['first_line']else 0
                    stop=s['end_codepoint'] if n==s['last_line']else len(counts[n])
                    for j in range(start,stop):counts[n][j]+=1
        for n,arr in counts.items():
            for j,v in enumerate(arr):
                assert v==1 or raw[n-1][j].isspace(),(book,n,j,v)
