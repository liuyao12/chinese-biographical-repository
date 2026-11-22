"""Verify a relationship against a fixed-revision sentence, kin term, and both people's anchors."""
import hashlib,json
from pathlib import Path

def valid(a,e,c,root):
    try:
        unit=a['qualifiers']['reading_basis']['unit']; path=Path(root)/'source-evidence/song092-officials'/(unit+'-kin.json')
        if unit not in TRUSTED or hashlib.sha256(path.read_bytes()).hexdigest()!=TRUSTED[unit]:return False
        spec=json.loads(path.read_bytes())[a['id']];p,=[p for p in c['paragraphs'] if p['id']==e['paragraph_id']==spec['paragraph_id']]
        if (c['id'],c['source']['revision_id'],c['source']['raw_file_sha256'],p['source_position']['first_line'],a['predicate'])!=(spec['chapter_id'],spec['revision'],spec['raw_sha256'],spec['line'],spec['predicate']):return False
        text=p['text'];term=a['qualifiers']['source_term']
        if term!=spec['kin_term'] or text.count(term)!=1 or e['quote']!=text or hashlib.sha256(text.encode()).hexdigest()!=spec['quote_sha256']:return False
        refs=[x for x in c['annotation'].get('person_reference_occurrences',[])if x['paragraph_id']==p['id']]
        for x in spec['anchors']:
            role=x['role'];m,=[m for m in [*p['mentions'],*refs]if m['id']==x['id']]
            field=role+('_person_reference_id' if 'referent_role' in m else '_person_mention_id')
            if e[field]!=m['id'] or m['person_id']!=x['person_id'] or m['person_id']!=a[role+'_person_id']:return False
            start,end=m['start'],m['end'];ctx=x['context']
            if (start,end,m['surface'])!=(x['start'],x['end'],x['surface']) or text[start:end]!=x['surface'] or text.count(ctx)!=1 or not(text.index(ctx)<=start<end<=text.index(ctx)+len(ctx)):return False
        return True
    except (KeyError,IndexError,OSError,TypeError,ValueError):return False

TRUSTED = {'bingzhi': 'fb1bc5410f6b5e6597ce9ffe5c43d1ec928f0c2d54eee848c8c0a90c1cb38477', 'changzhi': '57316971dcd09c3f199897ef5c9684f693df9a29fbeb098a55cf176e3142b579', 'duhongwen': '5a4c8c43b542c88d8bda40a743e8474c49e7a431f2d9f6ccbea4163b3deb8e38', 'duhuidu': '2dfc05fdcdbd0edf039a5fa7fa4525a85fc8f8e736ebd248838f2c422a82072b', 'duyuan': '7471d0d3f562d8a776985f251e024347626585ee7168989359f45599ca91299e', 'jianghui': '9f4c922e02e857b5e1a41f192da3e2b5d662f256172e1789b4fad31b1abe9bc0', 'jiangmi': 'cf4c37b249ebe1a9bd2c51b42adfe101f0ee64d042091213e734ec0baf1f2679', 'luhui': 'f2064ee2311928685ebcbddfc747372926a04f3f328d6f6dac3a1e483587cb8e', 'lurui': 'c97b854f82694d31340de2c16e3be539a6ac1e306ba2341446a080b788ee6539', 'shimen': '83e4dbe537f30e43381ca1e40782de4cb7f4eed7a3301d99801c7d05e362970b', 'wangjie-qianqi': '5aa2c9c62b8de9e3dc9fd99b1147b9617cdbeb6ae219332702062659cfa63838', 'xuhuo': '84cb50e7225a291a3daae405f13c264da4d6929f0e00380f7866f5d66946f29c'}
