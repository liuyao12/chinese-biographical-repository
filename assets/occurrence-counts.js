/** Frequency is a count of validated positions, never source authority. */
export function principalOccurrences(occurrences = []) {
  const rows = [...occurrences].sort((a,b) => b.count - a.count);
  return rows.length ? rows.filter(row => row.count === rows[0].count) : [];
}
export function occurrenceCountLabel(row) {
  if (row.counting_policy !== 'independent_fixed_witness_occurrences') return `${row.count} 處標記`;
  return row.duplicate_count
    ? `${row.count} 處獨立位置 · ${row.raw_count} 個原始錨點（同位置重出 ${row.duplicate_count}）`
    : `${row.count} 處獨立位置`;
}
