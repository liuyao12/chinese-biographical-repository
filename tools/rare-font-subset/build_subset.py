# coding: utf-8
import sys,json,hashlib
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parent/'python-packages'))
from fontTools.ttLib import TTFont
from fontTools import subset
p=Path(__file__).parent;src=p/'upstream/BabelStoneHan.ttf';assert hashlib.sha256(src.read_bytes()).hexdigest()=='d8bb747b3fdccd84a60bd0aa56bb90937270d0bd15f1101cd8f2a5a3709dd0a3','upstream font version/hash changed'
f=TTFont(src);chars=json.loads((p/'chars.json').read_text());cp={ord(x)for x in chars};assert cp<=f.getBestCmap().keys()
(p/'ARPHIC-PUBLIC-LICENSE.txt').write_text(next(n.toUnicode() for n in f['name'].names if n.nameID==13));(p/'UPSTREAM-NOTICES.txt').write_text('\n'.join(n.toUnicode()for n in f['name'].names if n.nameID in [0,7,8,9,10,11,12,13,14]))
o=subset.Options();o.name_IDs=['*'];o.name_legacy=True;o.name_languages=['*'];o.recalc_timestamp=False;s=subset.Subsetter(options=o);s.populate(unicodes=cp);s.subset(f)
for n in f['name'].names:
 if n.nameID in [1,3,4,6,16,18]:
  name='CBR Historical Rare Fallback' if n.nameID!=6 else 'CBRHistoricalRareFallback-Regular'
  n.string=name.encode(n.getEncoding())
 if n.nameID in [2,17]:n.string='Regular'.encode(n.getEncoding())
notice='Modified 2026-10-20 by CBR contributors: retained only U+2239E,U+244F0,U+248E5,U+24F35,U+2664D,U+26D4F,U+2C4B3; converted TTF to WOFF2; renamed CBR Historical Rare Fallback. Original glyph outlines and Unicode mappings retained. Distributed under the original Arphic Public License; no warranty.'
for n in f['name'].names:
 if n.nameID==10:n.string=(n.toUnicode()+'\n'+notice).encode(n.getEncoding(),errors='replace')
f['name'].setName(notice,10,3,1,0x409)
f['name'].setName(notice,10,1,0,0)
f.recalcTimestamp=False
f.flavor='woff2';f.save(p/'cbr-historical-rare-fallback.woff2');q=TTFont(p/'cbr-historical-rare-fallback.woff2');assert set(q.getBestCmap())==cp
r={'upstream_url':'https://www.babelstone.co.uk/Fonts/Download/BabelStoneHan.ttf','version':'16.0.3','license':'Original Arphic Public License, retained in full','upstream_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'upstream_bytes':src.stat().st_size,'subset_bytes':(p/'cbr-historical-rare-fallback.woff2').stat().st_size,'subset_sha256':hashlib.sha256((p/'cbr-historical-rare-fallback.woff2').read_bytes()).hexdigest(),'codepoints':[f'U+{c:X}' for c in sorted(cp)],'scope':'Only seven supplementary-plane characters occurring in the three selected source units; expandable subset, not complete historical CJK coverage','normalization_or_character_replacement':False}
(p/'subset-manifest.json').write_text(json.dumps(r,indent=2));print(json.dumps(r,indent=2))
