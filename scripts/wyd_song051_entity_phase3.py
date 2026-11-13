"""Exact entity-markup overlay for the locked Songshu 051 phase2 chapter."""
from pathlib import Path
import copy
import hashlib
import json

try:
    from scripts.validation_context import memoized
    from scripts import wyd_song051_yixin as phase2
except ImportError:
    from validation_context import memoized
    import wyd_song051_yixin as phase2

CH = 'corpus/songshu/051-wyd1739.json'
CID = 'c-songshu-051-wyd1739-zongshi'
REF = 'source-evidence/song051-wyd1739-zongshi/entity-markup-phase3-contract.json'
CONTRACT_SHA = '5fe21384604b3767c7edc5064bcc09310eb96bb7aa893a22ece50f8fd3a1e638'


def need(ok, message):
    if not ok:
        raise ValueError('武英殿宋051人物標記第三層：' + message)


def load(root, path):
    root = Path(root).resolve()
    target = (root / path).resolve()
    need(target.is_relative_to(root), '契約路徑越界')
    return json.loads(target.read_bytes())


def same(left, right):
    return phase2.same(left, right)


@memoized(0)
def contract(root):
    root = Path(root).resolve()
    path = (root / REF).resolve()
    need(path.is_relative_to(root / 'source-evidence'), '契約路徑越界')
    raw = path.read_bytes()
    need(hashlib.sha256(raw).hexdigest() == CONTRACT_SHA, '固定標記契約 SHA 不符')
    result = json.loads(raw)
    need(result.get('chapter_id') == CID and result.get('phase') == 'song051_entity_markup_phase3', '章／階段不符')
    parent_path = result.get('parent_contract_path')
    need(parent_path == phase2.REF and result.get('parent_contract_sha256') == phase2.CONTRACT_SHA, '第二層契約來源不符')
    return result


def layer_chapter(root, parent):
    c = contract(root)
    chapter = copy.deepcopy(parent)
    chapter['annotation']['additional_annotation_layers'] = [copy.deepcopy(c['layer_metadata'])]
    if c.get('cross_chapter_references'):
        chapter['cross_chapter_references'] = copy.deepcopy(c['cross_chapter_references'])
    for row in c['markers']:
        paragraph = next((p for p in chapter['paragraphs'] if p['id'] == row['paragraph_id']), None)
        need(paragraph is not None, '標記段落不在固定第二層章內')
        marker = copy.deepcopy(row['marker'])
        need(paragraph['text'][marker['start']:marker['end']] == marker['surface'], '標記字面／位置不符')
        need(not any(m['id'] == marker['id'] for m in paragraph['mentions']), 'MID 碰撞')
        paragraph['mentions'].append(marker)
        paragraph['mentions'].sort(key=lambda item: item['start'])
        paragraph['annotation_status'] = 'in_progress'
    return chapter


@memoized(0)
def project_phase2(root, current):
    root = Path(root).resolve()
    actual = load(root, CH)
    need(same(current, actual), '所給 current 章與磁碟不同')
    c = contract(root)
    metadata = actual.get('annotation', {}).get('additional_annotation_layers')
    need(metadata == [c['layer_metadata']], '第三層 metadata 漂移／有未列層')
    parent_contract = phase2.contract(root)
    roles = phase2.collect(actual, parent_contract)
    parent = phase2.phase_chapter(parent_contract, roles)
    expected = layer_chapter(root, parent)
    need(same(actual, expected), '原文、第二層錨點或第三層標記不符固定契約')

    registry_rows = load(root, 'registry/persons.json')['persons']
    people = {p['id']: p for p in registry_rows}
    need(len(people) == len(registry_rows), '人物 registry 有重複 ID')
    for row in c['markers']:
        marker = row['marker']
        person = people.get(marker['person_id'])
        need(person is not None, '標記人物未登記：' + marker['person_id'])
        if row.get('alias_surface') is not False:
            need(any(a.get('surface') == marker['surface'] and marker['id'] in a.get('mention_ids', [])
                     for a in person.get('aliases', [])), '人物 alias 未反向連到錨點：' + marker['id'])
        paragraph = next(p for p in actual['paragraphs'] if p['id'] == row['paragraph_id'])
        evidence = {k: actual[k] for k in ('work_id', 'book_id', 'source_id')}
        evidence.update(chapter_id=CID, paragraph_id=paragraph['id'], mention_id=marker['id'], quote=marker['surface'])
        need(evidence in person.get('evidence', []), '人物 evidence 未反向連到錨點：' + marker['id'])

    life_path = c.get('life_events_path')
    life_raw = (root / life_path).read_bytes()
    need(hashlib.sha256(life_raw).hexdigest() == c.get('life_events_sha256'), 'phase3生平事件資料 SHA 不符')
    life_set = json.loads(life_raw)
    need(life_set.get('record_type') == 'person_life_event_assertion_set' and life_set.get('chapter_id') == CID,
         'phase3生平事件資料篇章不符')
    mention_index = {m['id']: m for p in actual.get('paragraphs', []) for m in p.get('mentions', [])}
    mention_index.update({r['marker']['id']: r['marker'] for r in c['markers']})
    for event in life_set.get('events', []):
        anchor = event.get('source_anchor', {})
        paragraph = next((p for p in actual['paragraphs'] if p['id'] == anchor.get('paragraph_id')), None)
        need(paragraph is not None and paragraph['text'][anchor.get('start', -1):anchor.get('end', -1)] == anchor.get('surface'),
             'phase3生平事件來源錨點不符：' + event.get('id', ''))
        for ev in event.get('evidence', []):
            mid = ev.get('person_mention_id')
            if mid:
                mention = mention_index.get(mid)
                need(mention is not None and mention.get('person_id') == event.get('person_id'),
                     'phase3生平事件人物提及不符：' + event.get('id', ''))
    assertion_path = c.get('assertions_path')
    assertion_raw = (root / assertion_path).read_bytes()
    need(hashlib.sha256(assertion_raw).hexdigest() == c.get('assertions_sha256'), 'phase3親屬資料 SHA 不符')
    assertion_set = json.loads(assertion_raw)
    need(assertion_set.get('record_type') == 'person_assertion_set' and assertion_set.get('chapter_id') == CID, 'phase3親屬資料篇章不符')
    father = next((a for a in assertion_set.get('assertions', []) if a.get('id') == 'a-song051-phase3-diaomi-father'), None)
    relation_markers = {
        role: next(row['marker'] for row in c['markers']
                   if row['paragraph_id'] == CID + ':p005' and row['role_key'] == role)
        for role in ('DiaoMi', 'DiaoKui')
    }
    need(father is not None and father.get('predicate') == 'father' and father.get('subject_person_id') == c['new_person_roles']['DiaoMi']
         and father.get('object_person_id') == relation_markers['DiaoKui']['person_id']
         and father.get('status') == 'source_attested' and father.get('qualifiers', {}).get('source_term') == '刁逵子彌'
         and father.get('evidence', [{}])[0].get('subject_person_mention_id') == relation_markers['DiaoMi']['id']
         and father.get('evidence', [{}])[0].get('object_person_mention_id') == relation_markers['DiaoKui']['id'], '刁彌父子證據／錨點不符')

    identity_path = c.get('identity_decisions_path')
    identity_raw = (root / identity_path).read_bytes()
    need(hashlib.sha256(identity_raw).hexdigest() == c.get('identity_decisions_sha256'), '身份判讀記錄 SHA 不符')
    identity_set = json.loads(identity_raw)
    need(identity_set.get('record_type') == 'person_identity_decision_set' and identity_set.get('chapter_id') == CID,
         '身份判讀記錄篇章不符')
    decisions = {d['id']: d for d in identity_set.get('decisions', [])}
    need(len(decisions) == len(identity_set.get('decisions', [])), '身份判讀 ID 重複')
    for role, person_id in c['new_person_roles'].items():
        decision = decisions.get('d-song051-phase3-' + role.lower())
        expected_mids = {row['marker']['id'] for row in c['markers'] if row['role_key'] == role}
        need(decision is not None and decision.get('person_id') == person_id, '新人物身份判讀缺漏：' + role)
        need(set(decision.get('identification_basis', {}).get('target_mention_ids', [])) == expected_mids,
             '新人物身份判讀未涵蓋全部標記：' + role
        )

    name_path = c.get('name_components_path')
    name_raw = (root / name_path).read_bytes()
    need(hashlib.sha256(name_raw).hexdigest() == c.get('name_components_sha256'), '姓名構件記錄 SHA 不符')
    name_set = json.loads(name_raw)
    need(name_set.get('record_type') == 'person_name_component_set' and name_set.get('chapter_id') == CID,
         '姓名構件記錄篇章不符')
    name_rows = name_set.get('records', [])
    need(len({row.get('id') for row in name_rows}) == len(name_rows), '姓名構件 ID 重複')
    for name in name_rows:
        mention = next((row for row in c['markers'] if row['marker']['id'] == name.get('person_mention_id')), None)
        need(mention is not None and mention['marker']['person_id'] == name.get('person_id'), '姓名構件沒有本層人物錨點')
        paragraph = next(p for p in actual['paragraphs'] if p['id'] == name['paragraph_id'])
        need(name.get('quote') == paragraph['text'], '姓名構件引文不等於完整原段')

    return parent


def source_errors(chapter, root):
    if not isinstance(chapter, dict) or chapter.get('id') != CID:
        return []
    layers = chapter.get('annotation', {}).get('additional_annotation_layers')
    if layers is None:
        return []
    try:
        project_phase2(root, chapter)
        return []
    except (ValueError, KeyError, TypeError, OSError, UnicodeError, StopIteration, AttributeError) as exc:
        return ['武英殿宋051人物標記第三層：' + str(exc)]
