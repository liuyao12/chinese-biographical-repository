"""One current test-fixture identity field, independently source-bound to Jin Wudi.
The Liang family capture/contract and all unrelated fixture fields stay unchanged.
"""
import copy
FIXTURE='tests/fixtures/nanqi033-wangsengqian/person-ids.json'
def project_jinwu_fixture(expected,path,root,people=None,chapters=None):
 if path!=FIXTURE:return expected
 try:from scripts.sima_current_legacy_projection import _state
 except ImportError:from sima_current_legacy_projection import _state
 _,roles,historical=_state(root,people,chapters)
 assert isinstance(expected,dict)and isinstance(expected.get('jinwu'),str)and expected['jinwu']in(historical['wudi'],roles['wudi'])
 out=copy.deepcopy(expected);out['jinwu']=roles['wudi'];return out
