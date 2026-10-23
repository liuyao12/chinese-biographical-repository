"""作品成書、版本與出土履歷；未知不由數位修訂日推算。"""
from pathlib import Path
import argparse
import json

ROOT = Path(__file__).resolve().parents[1]
PATH = 'registry/work-provenance.json'


def inventory(root):
    works = json.loads((root / 'registry/works.json').read_text())['works']
    result = {w['id']: w['title'] for w in works}
    index = root / 'data/works/index.json'
    if index.exists():
        for filename in json.loads(index.read_text())['works']:
            item = json.loads((index.parent / filename).read_text())
            result[item['id']] = item['title']
    return result


def source_inventory(root):
    result = {}
    for path in sorted((root / 'corpus').glob('*/*.json')):
        item = json.loads(path.read_text())
        if item.get('record_type') == 'marked_chapter':
            result[item['source_id']] = item['work_id']
    tables = root / 'data/historical-tables/index.json'
    if tables.exists():
        for entry in json.loads(tables.read_text())['tables']:
            item = json.loads((root / entry['path']).read_text())['source']
            sid = item.get('source_id') or item.get('id')
            if sid:
                result[sid] = item['work_id']
    return result


def unknown():
    return {'status': 'not_researched', 'assertions': []}


def scaffold(root):
    path = root / PATH
    data = json.loads(path.read_text()) if path.exists() else {
        'schema_version': 1, 'references': {}, 'editions': {}, 'works': {}, 'text_bases': {}}
    for wid, title in inventory(root).items():
        data['works'].setdefault(wid, {
            'work_id': wid, 'title': title, 'transmission': 'not_researched',
            'composition': unknown(), 'earliest_extant_edition': unknown(),
            'burial': unknown(), 'excavation': unknown(), 'human_reviewed': False})
    for sid, wid in source_inventory(root).items():
        data['text_bases'].setdefault(sid, {'source_id': sid, 'work_id': wid,
            'status': 'not_researched', 'edition_id': None,
            'earliest_extant_basis_edition_id': None, 'reference_ids': [],
            'note': '數位來源的修訂號另存於正文 source；不能作成書或古本年代。'})
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')
    return data



def public_reference_url(value):
    if not isinstance(value,str) or any(c.isspace() or ord(c)<32 or ord(c)==127 for c in value):return False
    try:
        from urllib.parse import urlsplit
        u=urlsplit(value)
        return u.scheme in ('http','https') and bool(u.hostname) and u.username is None and u.password is None
    except ValueError:return False

def validate(data, root=None):
    assert data['schema_version'] == 1
    refs, editions = data['references'], data['editions']
    def references(ids):
        assert ids and all(r in refs for r in ids), '年代／版本斷言須有可回查依據'
    def date(value):
        assert value['calendar'] in ('chinese_civil', 'gregorian', 'common_era_year'), '須明示曆法'
        assert value['year_numbering'] in ('historical_no_year_zero', 'astronomical')
        start, end = value['start_year'], value['end_year']
        assert type(start) is int and type(end) is int and start <= end
        if value['year_numbering'] == 'historical_no_year_zero':
            assert start != 0 and end != 0
        assert value['precision'] in ('day', 'month', 'year', 'range')
        if value['precision'] in ('day', 'month'):
            assert start == end and 1 <= value['month'] <= 12
        if value['precision'] == 'day':
            assert 1 <= value['day'] <= 31
    for ref in refs.values():
        assert ref['title'] and public_reference_url(ref['url'])
        assert ref['access_scope'] and ref['human_reviewed'] is False
    for eid, edition in editions.items():
        assert edition['id'] == eid and edition['work_id'] in data['works']
        assert edition['extent'] in ('fragment', 'incomplete', 'complete', 'not_established')
        references(edition['reference_ids'])
        if edition.get('date') is not None:
            date(edition['date'])
    for wid, work in data['works'].items():
        assert work['work_id'] == wid and work['human_reviewed'] is False
        assert work['transmission'] in ('received', 'excavated', 'not_researched')
        for field in ('composition', 'earliest_extant_edition', 'burial', 'excavation'):
            record = work[field]
            assert record['status'] in ('not_researched', 'unknown', 'reported', 'disputed')
            if record['status'] in ('not_researched', 'unknown'):
                assert not record['assertions'], '未知不能同時給確定日期'
            else:
                assert record['assertions']
            for assertion in record['assertions']:
                references(assertion['reference_ids'])
                assert assertion['qualification']
                if assertion.get('date') is not None:
                    date(assertion['date'])
                if field == 'composition':
                    assert assertion.get('event_kind', 'authorship') not in ('digital_revision', 'accessed', 'excavation', 'death'), '修訂、存取、出土及卒年不能作成書事件'
                    assert assertion['layer'] in ('attributed_original', 'compilation', 'completion', 'continuation', 'revision', 'commentary', 'lu_shanjing_continuation', 'ye_sen_supplement'), '數位修訂或出土不是成書事件'
                if field == 'earliest_extant_edition':
                    assert editions[assertion['edition_id']]['work_id'] == wid
                    assert assertion['scope'] in ('fragment', 'incomplete', 'complete', 'known_witness_only')
                if field == 'excavation':
                    assert assertion['event_kind'] in ('reported_unearthing', 'excavation_campaign', 'discovery')
                    assert 'place_as_reported' in assertion
        for event in work.get('paratext_events', []):
            references(event['reference_ids'])
            date(event['date'])
            assert event['qualification'] and event['event_kind'] == 'abstract_submitted'
        if work['transmission'] == 'received':
            assert not work['excavation']['assertions'] and not work['burial']['assertions']
    for sid, basis in data['text_bases'].items():
        assert basis['source_id'] == sid and basis['work_id'] in data['works']
        assert basis['status'] in ('not_researched', 'unknown', 'documented')
        ids = [basis['edition_id'], basis['earliest_extant_basis_edition_id']]
        if basis['status'] != 'documented':
            assert ids == [None, None]
        else:
            references(basis['reference_ids'])
            assert basis['edition_id'] is not None
        for eid in filter(None, ids):
            assert editions[eid]['work_id'] == basis['work_id'], '底本不能指向其他作品'
    if root is not None:
        assert set(data['works']) == set(inventory(root)), '作品履歷須涵蓋兩套作品登記'
        assert {sid: b['work_id'] for sid, b in data['text_bases'].items()} == source_inventory(root)
    if root is not None:
        try:
            from scripts.pei_work_authorities import validate as validate_pei_work_authorities
        except ImportError:
            from pei_work_authorities import validate as validate_pei_work_authorities
        validate_pei_work_authorities(data, root)
    return data


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--scaffold', action='store_true')
    args = parser.parse_args()
    data = scaffold(ROOT) if args.scaffold else json.loads((ROOT / PATH).read_text())
    validate(data, ROOT)
    print('作品履歷：', len(data['works']), '作品；', len(data['text_bases']), '正文見證')
