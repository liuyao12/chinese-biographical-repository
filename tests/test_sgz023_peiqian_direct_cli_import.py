from pathlib import Path
import subprocess,sys,unittest,json,os
ROOT=Path(__file__).resolve().parents[1]
class DirectCliImport(unittest.TestCase):
 def test_actual_direct_module_path_office_departure(self):
  # Python starts with scripts as sys.path[0], exactly like direct validate_corpus.py.
  code="""import sys,json
from pathlib import Path
sys.path[:]=[str(Path.cwd()/'scripts')]+[p for p in sys.path if p not in ('',str(Path.cwd()))]
from fixed_peiqian_structural import office_end_valid
r=Path.cwd();h=next(h for h in json.loads((r/'corpus/sanguozhi/023-peiqian-titles.json').read_text())['holdings']if h['id']=='th-sgz023-peiqian-pqt-049');ch=json.loads((r/'corpus/sanguozhi/023-peiqian.json').read_text());assert office_end_valid(h,ch,r)
h['person_id']='wrong';assert office_end_valid(h,ch,r) is False
"""
  p=subprocess.run([sys.executable,'-c',code],cwd=ROOT,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'),capture_output=True,text=True);self.assertEqual(p.returncode,0,p.stderr)
