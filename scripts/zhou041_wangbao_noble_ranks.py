"""Two explicit Zhou041 noble ranks; biography topic is the recipient."""
import hashlib
import json
from pathlib import Path
try:
    from scripts.zhou041_wangbao_profile_facts import same, expand
except ImportError:
    from zhou041_wangbao_profile_facts import same, expand

REF = 'source-evidence/zhou041-wangbao-ws2432538/explicit-noble-ranks-contract.json'
SHA = '7b475cbafc8d73bc5e84e24388ac9d1e6b8c0dabec4b50255d9c9352e13770b2'
KIND = 'fixed_zhou041_explicit_noble_rank'


def source_record(root, chapter, roles):
    root = Path(root).resolve()
    path = root / REF
    assert path.is_file() and not path.is_symlink() and path.resolve().is_relative_to(root)
    raw = path.read_bytes()
    assert hashlib.sha256(raw).hexdigest() == SHA
    contract = json.loads(raw)
    assert chapter['id'] == contract['chapter_id']
    topic = next(m for p in chapter['paragraphs'] for m in p['mentions'] if m['id'] == contract['recipient_topic_mid'])
    assert topic['kind'] == 'person' and topic['person_id'] == roles['$bao']
    rowpath = root / contract['observed_ruler_row_path']
    assert rowpath.is_file() and not rowpath.is_symlink() and rowpath.resolve().is_relative_to(root)
    rowbytes = rowpath.read_bytes()
    assert hashlib.sha256(rowbytes).hexdigest() == contract['observed_ruler_row_sha256']
    observed = json.loads(rowbytes)
    assert observed['reference']['accession_year'] == observed['reference']['final_year'] == 557
    assert observed['reference']['row_as_web_reader'] == '南北朝 北周 | 〔北周〕孝閔帝 | 557 557'
    assert observed['image_verified'] is False and observed['human_reviewed'] is False
    expected = expand(contract['template'], roles)
    paragraphs = {p['id']: p for p in chapter['paragraphs']}
    mentions = {m['id']: m for p in chapter['paragraphs'] for m in p['mentions']}
    for holding in expected['holdings']:
        binding = holding['source_career_role']
        assert holding['person_id'] == roles['$bao']
        assert mentions[binding['recipient_topic_mention_id']]['person_id'] == roles['$bao']
        assert mentions[binding['recipient_mention_id']]['person_id'] == roles['$bao']
        for field in ('source_clause_anchor', 'title_anchor'):
            anchor = binding[field]
            assert paragraphs[anchor['paragraph_id']]['text'][anchor['start']:anchor['end']] == anchor['surface']
        assert binding['title_anchor']['surface'] == holding['title']
        if binding['slot'] == 'nanchang':
            assert holding['mode'] == 'accession' and binding['source_clause_anchor']['surface'] == '襲爵' + holding['title']
        else:
            assert binding['slot'] == 'shiquan' and holding['mode'] == 'grant'
            ruler = mentions[binding['ruler_mention_id']]
            assert ruler['person_id'] == roles['$xiaomin'] != holding['person_id']
            assert binding['source_clause_anchor']['surface'] == ruler['surface'] + '踐阼，封' + holding['title'] + '，邑三百戶'
        assert holding['effective_period']['end'] == {'status': 'unknown', 'date_expression': None, 'evidence': []}
        date = holding['effective_period']['start'].get('normalized_date')
        if binding['slot'] == 'nanchang':
            assert date is None
        else:
            assert isinstance(date, dict) and date['year'] == date['era_year'] == observed['reference']['accession_year']
            assert date['era'] == 'CE' and date['precision'] == 'year' and date['calendar'] == 'chinese_civil'
            assert date['source_expression'] == ruler['surface'] + '踐阼'
            assert date['regnal_year_mapping'] == {'kind': 'fixed_zhou041_xiaomin_accession', 'ruler_mention_id': binding['ruler_mention_id'], 'reference_index': 0}
            assert date['references'][0]['url'] == observed['reference']['url']
            assert date['references'][0]['quote'] == observed['reference']['row_as_web_reader']
            assert date['original_quote'] == holding['evidence'][0]['quote'] and date['evidence'] == holding['evidence']
            assert date['human_reviewed'] is False and 'month' not in date and 'day' not in date
    actual = root / contract['title_path']
    assert actual.is_file() and not actual.is_symlink() and actual.resolve().is_relative_to(root)
    assert same(json.loads(actual.read_bytes()), expected)
    return expected


def guard_catalog(root, person_id, records, chapter, roles):
    expected = source_record(root, chapter, roles)
    if person_id == roles['$bao']:
        assert sum(same(row, expected) for row in records) == 1


def holding_valid(holding, chapter, root):
    try:
        try:
            from scripts.fixed_zhou041_wangbao import proof
        except ImportError:
            from fixed_zhou041_wangbao import proof
        actual, _, roles = proof(root)
        assert same(chapter, actual)
        expected = source_record(root, actual, roles)
        return sum(same(holding, h) for h in expected['holdings']) == 1
    except (AssertionError, ValueError, TypeError, KeyError, OSError, StopIteration):
        return False


def date_valid(date, holding, endpoint, chapters, root):
    """557 belongs only to this grant's source accession context, not a lifespan."""
    try:
        try:
            from scripts.fixed_zhou041_wangbao import proof
        except ImportError:
            from fixed_zhou041_wangbao import proof
        chapter, _, roles = proof(root)
        assert endpoint == 'start' and same(chapters[chapter['id']], chapter)
        expected = source_record(root, chapter, roles)['holdings'][1]
        assert same(holding, expected)
        return same(date, expected['effective_period']['start']['normalized_date'])
    except (AssertionError, KeyError, TypeError, ValueError, OSError, StopIteration):
        return False
