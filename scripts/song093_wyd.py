"""按殿本三個單元的逐欄錄文、頁次及圖像流雜湊查核。"""
import hashlib,json
from pathlib import Path
IDS=['c-songshu-093-wanghongzhi-wyd', 'c-songshu-093-wangtansheng-wyd', 'c-songshu-093-ruanwanling-wyd']
HASHES={'source-evidence/song093-wanghongzhi/song093-wyd-columns.json': '7005396408858629e8e208fdffa1e799be772858e876ab228a51cdb332ffad18', 'source-evidence/song093-wyd/reading.json': '61e157c9db7ce62e087a01f2b86f8a72605c96b29c87b26bc713c3e7ec89123e', 'source-evidence/song093-wyd/frames.json': 'b74a2b8e41a931bddb91961842e6210ec0804e5b712dfa1383b1cfbf1b7f7bfe', 'source-evidence/song093-wyd/columns.txt': 'b7170dce6be9a5980d5373556ef7d70d8234d1f7af16af3aa30bf21f6e707b20'}
PROPOSALS={'tp-song093-wyd-nanman': ('c-songshu-093-wanghongzhi-wyd', 'c-songshu-093-wanghongzhi-wyd:p001', '38b71b84cf43d2b9c881c8d4ebf84e4c31c6751d2876ab5d372bd6a2de061eea', '524166dcf2a3bd30c4e32bca90112535285380501cb2e1cdb1669585410ac6bd'), 'tp-song093-wyd-youjun': ('c-songshu-093-wanghongzhi-wyd', 'c-songshu-093-wanghongzhi-wyd:p001', '38b71b84cf43d2b9c881c8d4ebf84e4c31c6751d2876ab5d372bd6a2de061eea', 'fd7e538b60d72be62a510adb6e16510d6acef3aa83dbcf9a3bcfc1832baa1ffe'), 'tp-song093-wyd-xuzhou': ('c-songshu-093-wanghongzhi-wyd', 'c-songshu-093-wanghongzhi-wyd:p001', '38b71b84cf43d2b9c881c8d4ebf84e4c31c6751d2876ab5d372bd6a2de061eea', '153bf90628fac74b1acf81887e1e051b4cbd070e1036b23edd4f8e47090ccf15'), 'tp-song093-wyd-yuanwai': ('c-songshu-093-wanghongzhi-wyd', 'c-songshu-093-wanghongzhi-wyd:p001', '38b71b84cf43d2b9c881c8d4ebf84e4c31c6751d2876ab5d372bd6a2de061eea', 'b890645b0d5cc348b10b7f68eb75201952773dab04382ab75f6907a9c9e95a1b'), 'tp-song093-wyd-shuzi': ('c-songshu-093-wanghongzhi-wyd', 'c-songshu-093-wanghongzhi-wyd:p001', '38b71b84cf43d2b9c881c8d4ebf84e4c31c6751d2876ab5d372bd6a2de061eea', '9928cdf3db99b0dac198acd8dbab49894a3857bd5b5d51097d7c2ec11c2b76ba'), 'tp-song093-wyd-tongzhi': ('c-songshu-093-wanghongzhi-wyd', 'c-songshu-093-wanghongzhi-wyd:p001', '38b71b84cf43d2b9c881c8d4ebf84e4c31c6751d2876ab5d372bd6a2de061eea', 'bb40bf482763c0cbaa1b1bd9204c8a8aac2bc6300d96b0b1050e30b076873098'), 'tp-song093-wyd-mishu': ('c-songshu-093-ruanwanling-wyd', 'c-songshu-093-ruanwanling-wyd:p001', 'f29bb9a9b2327d0b36ff0e52cc77bd9c6917d772404ef65805a597c3c48a179f', 'c70ebeabd089602d177791c700fb4d90af9d4ac340f78ef4e6a3630e1743e206'), 'tp-song093-wyd-jishi': ('c-songshu-093-ruanwanling-wyd', 'c-songshu-093-ruanwanling-wyd:p001', 'f29bb9a9b2327d0b36ff0e52cc77bd9c6917d772404ef65805a597c3c48a179f', 'fc4794ac0d9920c88babd21b0dd87c25556c90565d56c9c7b3952a05221377c3')}
FRAMES='source-evidence/song093-wyd/frames.json'
LEDGER='source-evidence/song093-wanghongzhi/song093-wyd-columns.json'

def digest(s):return hashlib.sha256(s.encode()).hexdigest()
def h(v):return digest(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
def source(root,name):
    base=Path(root).resolve();p=base/name
    if p!=p.resolve() or not p.is_relative_to(base):raise ValueError('路徑')
    text=p.read_text()
    if digest(text)!=HASHES[name]:raise ValueError('版本指紋')
    return text

def frame(ch,root):return json.loads(source(root,FRAMES))[ch['id']]

def errors(ch,root):
    if ch.get('id') not in IDS:return []
    try:
        target=frame(ch,root);p,=ch['paragraphs'];so=ch['source'];ledger=json.loads(source(root,LEDGER));r=json.loads(source(root,'source-evidence/song093-wyd/reading.json'))
        columns=ledger['columns'];rows={(v['page'],v['leaf_side'],v['column']):v['quote'] for v in columns}
        if len(rows)!=44 or len(ledger['page_images'])!=3:raise ValueError('原頁')
        original=source(root,target['source_path']);t=''.join(v['quote']for v in columns)
        if original!=''.join(f"{v['page']:02}{v['leaf_side']}{v['column']:02} {v['quote']}\n"for v in columns):raise ValueError('逐欄')
        unit,=[x for x in r['print_collation']['sources'] if x['chapter_id']==ch['id']]
        if so['revision_id']!='cbr-ai-transcription-sha256:'+digest(original) or so['raw_file_sha256']!=digest(original) or so['image_verified'] is not True:raise ValueError('底本')
        pr=p['source_position']['column_projection']
        if h([p['source_position']])!=target['positions_sha256'] or p['text']!=t[unit['start']:unit['end']] or p['text']!=''.join(v['text']for v in pr):raise ValueError('原段')
        for v in pr:
            text=rows[v['pdf_page'],'R' if v['half']=='右' else 'L',v['column_from_right']]
            if not 0<=v['start']<v['end']<=len(text) or text[v['start']:v['end']]!=v['text']:raise ValueError('原欄裁界')
        if (p['annotation_status']!='reviewed' or digest(p['text'])!=target['body_sha256'] or ch['text_sha256']!=target['body_sha256'] or h(ch['annotation'])!=target['annotation_sha256'] or h([p['mentions']])!=target['mentions_sha256']):raise ValueError('稱謂與官事')
        return []
    except (KeyError,ValueError,OSError,TypeError,IndexError):return ['宋書殿本卷九十三固定原欄、讀法或原圖指紋不符']

def kin_valid(record,ch,root):return ch['id']in IDS and not errors(ch,root) and record in frame(ch,root)['kin']
def death_valid(record,e,ch,root):return ch['id']in IDS and not errors(ch,root) and record in frame(ch,root)['life'] and record['evidence']==[e]
def side_errors(record,ch,root,key):
    if ch['id']not in IDS:return []
    try:
        field={'assertions':'kin','holdings':'offices','events':'life'}[key]
        if record[key]!=frame(ch,root)[field]:raise ValueError('原證')
        return []
    except (KeyError,ValueError,OSError,TypeError):return ['宋書卷九十三殿本逐項讀法與直接字位不符']

def proposal_valid(row,ch):
    try:
        cid,pid,text_hash,record_hash=PROPOSALS[row['id']];p,=ch['paragraphs']
        if (ch['id'],p['id'],digest(p['text']),h(row))!=(cid,pid,text_hash,record_hash):return False
        return all(v['paragraph_id']==pid and p['text'][v['start']:v['end']]==v['surface'] for v in (row['role_anchor'],row['non_assumption_anchor'],row['appointment_anchor']))
    except (KeyError,ValueError,OSError,TypeError):return False
