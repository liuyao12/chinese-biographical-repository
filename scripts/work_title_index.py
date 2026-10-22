"""Public canonical titles of every registered work, including citation-only works."""
from pathlib import Path
import json,re,argparse
ROOT=Path(__file__).resolve().parents[1]
def outputs(root=ROOT):
 root=Path(root);works=json.loads((root/'registry/works.json').read_text())['works'];rows=[];seen=set()
 for work in works:
  wid,title=work['id'],work['title']
  if not isinstance(wid,str)or not re.fullmatch('w-[a-z0-9-]+',wid)or wid in seen or not isinstance(title,str)or not title.strip():raise ValueError('Invalid canonical work title')
  citation=work.get('citation_title',title)
  if not isinstance(citation,str) or not citation.strip():raise ValueError('Invalid citation title')
  row={'id':wid,'title':citation}
  if 'citation_qualification' in work:
   qualification=work['citation_qualification']
   if not isinstance(qualification,str) or not qualification.strip():raise ValueError('Invalid citation qualification')
   row['qualification']=qualification
  seen.add(wid);rows.append(row)
 data={'schema_version':1,'source_registry':'registry/works.json','works':rows}
 return{root/'data/corpus/work-titles.json':(json.dumps(data,ensure_ascii=False,indent=2)+'\n').encode()}
def run(root=ROOT):
 for p,data in outputs(root).items():p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(data)
if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--root',type=Path,default=ROOT);run(parser.parse_args().root)
