"""Validate excerpts transcribed from a published inscription on a web page."""

import hashlib
import json
from pathlib import Path


KIND = 'published_web_inscription_excerpts'


def source_errors(chapter, root, works, books):
    try:
        source = chapter['source']
        witness = source['transcription_witness']
        assert witness['kind'] == KIND and witness['reported_transcription_author']
        assert witness['original_stone_or_rubbing_image_verified'] is False
        assert witness['excavation_publication_plate_verified'] is False and source['image_verified'] is False
        assert source['review_status'] == 'text_checked' and chapter['annotation']['human_reviewed'] is False
        assert source['revision_id'] is None and source['license_scope'] == 'classical_inscription_text_only'
        assert source['text_scope'] == 'partial_chapter' and not source.get('image_witnesses')
        assert works[chapter['work_id']]['work_type'] == 'single_epitaph'
        book = books[chapter['book_id']]
        assert book['unit_kind'] == 'editorial_single_text_container' and book['number'] is None
        directory = (Path(root) / 'source-evidence').resolve()
        path = (Path(root) / witness['capture_path']).resolve()
        assert path.is_relative_to(directory) and path.suffix == '.json'
        capture = json.loads(path.read_text(encoding='utf-8'))
        assert capture['url'] == source['permalink'] == source['url']
        assert capture['original_plate_examined'] is False and capture['original_stone_examined'] is False
        assert capture['scope'] == 'selected_classical_passages'
        assert capture['inscription_heading'] and capture['reported_source']
        assert capture['provider'] == source['provider'] and capture['accessed_on'] == source['accessed_on']
        assert chapter['paragraphs'] and len(capture['passages']) == len(chapter['paragraphs'])
        for p, excerpt in zip(chapter['paragraphs'], capture['passages']):
            assert p['text_layer'] == 'epitaph_as_modernly_transcribed'
            assert p['text'] == excerpt['text'] and p['witness_locator']['locus'] == excerpt['locator']
            assert p['witness_locator']['selected_text_sha256'] == excerpt['sha256']
            assert hashlib.sha256(p['text'].encode()).hexdigest() == excerpt['sha256']
        return []
    except (KeyError, ValueError, TypeError, OSError, AssertionError):
        return ['墓誌網頁節錄缺實際見證、逐段文字指紋，或誤稱已核圖版']


def facts_valid(chapter, records):
    """The culprit is recorded by the histories; preserve the inscription's lacuna."""
    try:
        head, narrative, family = chapter['paragraphs']
        subject = next(m for m in head['mentions'] if m['surface'] == '混' and m['start'] == 2)
        assert head['text'].startswith('君諱混，字子元，')
        assert '遂乃飲粒不？，聲泣相」繼。' in narrative['text'] and '亡父鴻，字彥鸞' in family['text']
        event_sets = {r['record_type']: r['events'] for r in records if 'events' in r}
        death, = event_sets['person_life_event_assertion_set']
        reburial, = event_sets['person_event_assertion_set']
        for event, typ, expression, month, day in (
            (death, 'death', '元象元年二月五日', 2, '五日'),
            (reburial, 'burial', '其年十一月五日庚申', 11, '五日'),
        ):
            assert event['event_type'] == typ and event['person_id'] == subject['person_id']
            assert event['date_expression'] == expression and event['normalized_date']['year'] == 538
            evidence, = event['evidence']
            assert evidence['paragraph_id'] == narrative['id'] and evidence['person_mention_id'] == subject['id']
            assert evidence['quote'] == narrative['text'] and evidence['context']['paragraph_id'] == head['id']
            parts = event['epitaph_date_parts']
            assert (parts['month'], parts['day']) == (month, 5)
            i = narrative['text'].index(expression)
            month_text = '二月' if month == 2 else '十一月'
            for key, string in (('month_anchor', month_text), ('day_anchor', day)):
                a = parts[key]
                assert a['paragraph_id'] == narrative['id'] and a['surface'] == string
                assert a['start'] == i + expression.index(string) and a['end'] == a['start'] + len(string)
        assert death['source_term'] == '奄至物故' and not death.get('death_agent')
        assert reburial['burial_kind'] == 'reburial' and reburial['burial_action_anchor']['surface'] == '遷窆'
        return True
    except (KeyError, ValueError, TypeError, StopIteration, AssertionError):
        return False
