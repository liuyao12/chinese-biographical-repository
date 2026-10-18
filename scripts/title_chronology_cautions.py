"""Bind an unresolved title chronology warning to received text and native cells."""
import re
try:
    from .table_evidence import table_cell
except ImportError:
    from table_evidence import table_cell


def chronology_caution_errors(decision, tables, chapters, paragraphs):
    caution = decision.get('chronology_caution')
    if caution is None:
        return []
    errors = []
    def check(ok, message):
        if not ok:
            errors.append(message)
    if not isinstance(caution, dict):
        return ['爵年未定記錄須為物件']
    pid = decision.get('person_id')
    check(caution.get('kind') == 'unresolved_title_chronology'
          and caution.get('status') == 'unresolved'
          and caution.get('person_id') == pid
          and caution.get('identity_basis') == 'explicit_commentary'
          and caution.get('no_tenure_interpolation') is True
          and caution.get('human_reviewed') is False
          and caution.get('model') is None
          and bool(caution.get('rationale')), '爵年未定須明示人物、未定狀態及不得內插在爵')
    for reference in decision.get('references', []):
        if 'display_quote' not in reference:
            continue
        raw = reference.get('quote')
        valid = (isinstance(raw, str) and reference.get('quote_format') == 'kanripo_line_wrapped'
                 and isinstance(reference.get('source_commit'), str)
                 and re.fullmatch('[0-9a-f]{40}', reference['source_commit']) is not None
                 and reference['source_commit'] in reference.get('url', '')
                 and reference.get('image_verified') is False)
        plain = re.sub(r'\s|¶|/', '', re.sub(r'<pb:[^>]*>', '', raw)) if isinstance(raw, str) else None
        check(valid and reference['display_quote'] == plain,
              '爵年未定注說顯示只可移除指定數位分行與頁標，不得改原字')
    event = caution.get('event_evidence', {})
    if not isinstance(event, dict):
        return errors + ['爵年未定本事須為來源物件']
    chapter = chapters.get(event.get('chapter_id'), {})
    hit = paragraphs.get(event.get('paragraph_id'))
    quote = event.get('quote')
    paragraph = hit[1] if hit else {}
    mention = next((m for m in paragraph.get('mentions', [])
                    if m['id'] == event.get('person_mention_id')), None)
    check(bool(hit) and hit[0] == event.get('chapter_id')
          and quote == paragraph.get('text') and bool(quote)
          and all(event.get(k) == chapter.get(v) for k,v in
                  [('work_id','work_id'),('book_id','book_id'),('chapter_id','id'),('source_id','source_id')])
          and event.get('source_revision') == chapter.get('source', {}).get('revision_id'),
          '爵年未定本事須有固定篇文及完整原段')
    check(bool(mention) and mention.get('person_id') == pid
          and type(mention.get('start')) is int and type(mention.get('end')) is int
          and isinstance(quote,str) and 0 <= mention['start'] < mention['end'] <= len(quote)
          and quote[mention['start']:mention['end']] == mention.get('surface'),
          '爵年未定本事須有同人逐字錨點')
    for key in ('date_term', 'event_term'):
        check(isinstance(event.get(key), str) and bool(event[key])
              and isinstance(quote, str) and event[key] in quote,
              '爵年未定須保留本事紀年及事件原詞')
    if mention and isinstance(quote, str) and isinstance(event.get('event_term'), str) and event['event_term'] in quote:
        term = event['event_term']
        check(any(i <= mention['start'] < mention['end'] <= i + len(term)
                  for i in range(len(quote)) if quote.startswith(term, i)),
              '本事事件原詞須包含所指人物，不得借另一人的事件')
    accounts = caution.get('table_accounts', [])
    if not isinstance(accounts, list) or len(accounts) < 2:
        return errors + ['爵年未定須列至少兩個有據原表記錄']
    if not all(isinstance(e, dict) for e in accounts):
        return errors + ['爵年未定原表記錄須為來源物件']
    keys = [(e.get('table_id'), e.get('table_cell_id')) for e in accounts]
    check(len(set(keys)) == len(keys), '爵年未定原格不得重複當成獨立證據')
    for account in accounts:
        table = tables.get(account.get('table_id'))
        if not table:
            errors.append('爵年未定原表不存在')
            continue
        source = table['source']
        cell = table_cell(table, account.get('table_cell_id'))
        check(account.get('kind') == 'table_cell' and 'paragraph_id' not in account
              and all(account.get(k) == source.get(v) for k,v in
                      [('work_id','work_id'),('book_id','book_id'),('chapter_id','chapter_id'),
                       ('source_id','id'),('source_revision','revision')]),
              '爵年未定原格須保留著作、卷篇與固定版本')
        if not cell:
            errors.append('爵年未定原格不存在')
            continue
        check(account.get('quote') == cell['text'], '爵年未定須保留完整原格')
        anchor = next((m for m in cell.get('person_mentions', [])
                       if m['id'] == account.get('person_mention_id')), None)
        check(bool(anchor) and anchor.get('person_id') == pid
              and type(anchor.get('start')) is int and type(anchor.get('end')) is int
              and 0 <= anchor['start'] < anchor['end'] <= len(cell['text'])
              and cell['text'][anchor['start']:anchor['end']] == anchor.get('surface'),
              '爵年未定原表須有同人逐字錨點')
        terms = account.get('event_terms')
        check(isinstance(terms, list) and bool(terms)
              and all(isinstance(term, str) and bool(term) and term in cell['text'] for term in terms),
              '爵年未定各封免原詞須見於本格，不改字調和')
    return errors
