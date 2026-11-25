function documentPath(row) {
  if (row.chapter_ref) {
    if (!/^data\/corpus\/[a-z0-9-]+\/[a-zA-Z0-9_-]+\.json$/.test(row.chapter_ref)) throw Error('無效的篇章路徑');
    return row.chapter_ref;
  }
  const tid = row.table_source_ref || (row.quote_ref === 'cell' && row.table_id);
  if (!tid) return null;
  if (!/^[a-z0-9-]+$/.test(tid)) throw Error('無效的表格 ID');
  return `data/historical-tables/${tid}.json`;
}

export function indexPassageDocument(doc) {
  if (doc.record_type === 'marked_chapter') {
    return {doc, texts: new Map(doc.paragraphs.map(p => [p.id, p.text]))};
  }
  const texts = new Map();
  for (const fragment of doc.fragments) for (const row of fragment.rows) {
    for (const cell of row.cells) texts.set(cell.id, cell.text);
  }
  return {doc, texts};
}

const fields = ['sources', 'occurrences', 'table_occurrences'];
function fullQuotePath(row) {
  const path = row.quote_passage_ref;
  if (!/^(?:data\/corpus\/[a-z0-9-]+\/[a-zA-Z0-9_-]+|data\/historical-tables\/[a-z0-9-]+)\.json$/.test(path)) throw Error('無效的引文路徑');
  return path;
}

function visitQuotes(value, callback) {
  if (!value || typeof value !== 'object') return value;
  let row = value;
  for (const [key, child] of Object.entries(value)) {
    const expanded = visitQuotes(child, callback);
    if (expanded === child) continue;
    if (row === value) row = Array.isArray(value) ? value.slice() : {...value};
    row[key] = expanded;
  }
  return 'quote_passage_ref' in row ? callback(row, fullQuotePath(row)) : row;
}

export function expandProfile(profile, lookup) {
  const result = {...visitQuotes(profile, (row, path) => {
    const {doc, texts} = lookup(path);
    const table = !row.paragraph_id;
    const witness = table ? doc.source : doc;
    const id = row.paragraph_id || row.table_cell_id || row.cell_id;
    const expected = {work_id:witness.work_id, book_id:witness.book_id,
      chapter_id:table ? witness.chapter_id : doc.id, source_id:table ? witness.id : doc.source_id};
    if (table) Object.assign(expected, {table_id:doc.id, source_revision:witness.revision});
    if (!texts.has(id) || 'quote' in row || Object.entries(expected).some(([k,v]) => k in row && row[k] !== v)) throw Error('引文與見證不符');
    const {quote_passage_ref, ...rest} = row;
    return {...rest, quote:texts.get(id)};
  })};
  for (const field of fields) {
    if (!result[field]?.some(row => documentPath(row))) continue;
    result[field] = result[field].map(row => {
      const path = documentPath(row);
      if (!path) return row;
      const {doc, texts} = lookup(path);
      if (!row.chapter_ref) {
        if (doc.id !== (row.table_source_ref || row.table_id)) throw Error('表格與見證不符');
        if (field === 'sources') {
          const {table_source_ref, ...rest} = row;
          if (doc.source.id !== rest.source_id || doc.source.chapter_id !== rest.chapter_id ||
              doc.source.book_id !== rest.book_id || doc.source.work_id !== rest.work_id) throw Error('表格來源不符');
          return {...rest, source: doc.source};
        }
        const {quote_ref, ...rest} = row;
        const id = row.table_cell_id || row.cell_id;
        if (!texts.has(id)) throw Error('表格引文無效');
        return {...rest, quote: texts.get(id)};
      }
      if (doc.id !== row.chapter_id || doc.book_id !== row.book_id ||
          doc.work_id !== row.work_id || doc.source_id !== row.source_id) throw Error('篇章與見證不符');
      const {chapter_ref, quote_span, ...rest} = row;
      if (field === 'sources') return {...rest, source: doc.source};
      if (!texts.has(row.paragraph_id) || !Array.isArray(quote_span) ||
          quote_span.length !== 2 || !quote_span.every(Number.isSafeInteger)) throw Error('段落引文無效');
      const text = Array.from(texts.get(row.paragraph_id));
      const [start, end] = quote_span;
      if (start < 0 || end < start || end > text.length) throw Error('段落引文超出正文');
      return {...rest, quote: text.slice(start, end).join('')};
    });
  }
  return result;
}

const loaded = new Map();
export async function resolveProfilePassages(profile) {
  const paths = new Set(fields.flatMap(field => (profile[field] || []).map(documentPath)).filter(Boolean));
  visitQuotes(profile, (row, path) => { paths.add(path); return row; });
  const indexed = new Map();
  await Promise.all([...paths].map(async path => {
    if (!loaded.has(path)) loaded.set(path, fetch(path).then(async response => {
      if (!response.ok) throw Error('無法載入引文來源');
      return indexPassageDocument(await response.json());
    }).catch(error => { loaded.delete(path); throw error; }));
    indexed.set(path, await loaded.get(path));
  }));
  return expandProfile(profile, path => indexed.get(path));
}
