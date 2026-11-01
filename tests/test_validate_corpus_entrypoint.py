"""The documented direct-file validator must resolve repository modules."""
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


class ValidatorEntrypointTests(unittest.TestCase):
    def test_direct_file_imports_from_an_unrelated_working_directory(self):
        script = ROOT / 'scripts' / 'validate_corpus.py'
        probe = '''
import runpy, sys
from pathlib import Path
script = Path(sys.argv[1])
sys.path.insert(0, str(script.parent))
runpy.run_path(str(script), run_name='validator_import_probe')
from scripts.era_stage_dates import KNOWN_ERAS
assert KNOWN_ERAS
assert sys.path.count(str(script.parent.parent)) == 1
'''
        with tempfile.TemporaryDirectory(prefix='cbr-validator-entrypoint-') as directory:
            result = subprocess.run(
                [sys.executable, '-I', '-B', '-c', probe, str(script)],
                cwd=directory, capture_output=True, text=True,
            )
        self.assertEqual(result.returncode, 0, result.stderr)
