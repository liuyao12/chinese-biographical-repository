import {orderChildren} from './sibling-order.js';
// Traverse source relations and separately attributed assembly edges, never stored ancestor chains.
export async function traceFamily(person, load) {
  const own = p => new Set(p.person_ids || [p.id]);
  function mergeEvidence(map, entry) {
    const previous = map.get(entry.id);
    if (!previous) { map.set(entry.id, entry); return; }
    const direct = previous.role === 'assembly_inferred' && entry.role !== 'assembly_inferred'
      && !entry.unavailable && !entry.cycle;
    if (direct) map.set(entry.id, {...entry, evidence: [...entry.evidence, ...previous.evidence]});
    else previous.evidence.push(...entry.evidence);
  }

  function related(p, kind) {
    const ids = own(p), result = new Map();
    for (const r of p.preferred_relations || p.relations || []) {
      if (r.qualifiers?.adopted_for_family_tree === false) continue;
      const subject = ids.has(r.subject_person_id), object = ids.has(r.object_person_id);
      let id;
      if (kind === 'father' && subject && r.predicate === 'father') id = r.object_person_id;
      // A source's son/daughter assertion does not establish the parent's sex.
      // Only explicitly typed father/mother edges are used for upper generations.
      if (kind === 'mother' && subject && r.predicate === 'mother') id = r.object_person_id;
      if (kind === 'adoptive_father' && subject && r.predicate === 'adoptive_father') id = r.object_person_id;
      if (kind === 'adopted_children' && object && r.predicate === 'adoptive_father') id = r.subject_person_id;
      if (['grandfather', 'great_grandfather'].includes(kind) && subject && r.predicate === kind
          && r.qualifiers?.lineage !== 'maternal') id = r.object_person_id;
      if (kind === 'spouse' && r.predicate === 'spouse') id = subject ? r.object_person_id : object ? r.subject_person_id : null;
      if (kind === 'children' && object && ['father', 'mother'].includes(r.predicate)) id = r.subject_person_id;
      if (kind === 'children' && subject && ['son', 'daughter'].includes(r.predicate)) id = r.object_person_id;
      if (id && !ids.has(id)) {
        if (!result.has(id)) result.set(id, {id, evidence: [], role: r.qualifiers?.parentage_role});
        result.get(id).evidence.push(...(r.evidence || []));
        if (kind === 'spouse' && r.qualifiers?.marriage_termination?.kind === 'divorce') {
          result.get(id).marriage_status = 'source_attested_divorce';
        }
      }
    }
    function assemblyEdge(row, id) {
      const connection = row?.parent_connection;
      if (!id || ids.has(id) || result.has(id) || !row.assembly_id
          || !['editorial_preferred', 'contextual_provisional'].includes(row.status)
          || connection?.status !== 'contextual_provisional'
          || !['shared_father_through_sibling', 'shared_father_through_sibling_chain', 'parent_between_consecutive_ancestors', 'parent_through_paternal_uncle'].includes(connection.type)
          || !connection.rationale || !connection.references?.length) return;
      result.set(id, {id, role: 'assembly_inferred', inference_note: connection.rationale,
        evidence: connection.references.map(ref => ({quote: ref.quote, chapter_id: ref.chapter_id, paragraph_id: ref.paragraph_id}))});
    }
    if (kind === 'father' && ids.has(p.assembled_identity?.person_id)) {
      assemblyEdge(p.assembled_identity, p.assembled_identity.parent_person_id);
    }
    if (['grandfather', 'great_grandfather'].includes(kind)) {
      const row = p.assembled_identity, connection = row?.ancestor_connection;
      const id = row?.ancestor_person_id;
      if (row?.connection === kind && ids.has(row.person_id) && id && !ids.has(id)
          && !result.has(id) && row.assembly_id
          && ['editorial_preferred', 'contextual_provisional'].includes(row.status)
          && connection?.type === 'shared_ancestor_through_sibling'
          && connection.status === 'contextual_provisional'
          && connection.rationale && connection.references?.length) {
        result.set(id, {id, role: 'assembly_inferred', inference_note: connection.rationale,
          evidence: connection.references.map(ref => ({quote: ref.quote, chapter_id: ref.chapter_id, paragraph_id: ref.paragraph_id}))});
      }
    }
    if (kind === 'children') {
      for (const row of p.assembled_children || []) {
        if (ids.has(row.parent_person_id)) assemblyEdge(row, row.person_id);
      }
    }
    return [...result.values()];
  }
  async function resolve(entries) {
    const resolved = await Promise.all(entries.map(async entry => {
      try {const p = await load(entry.id); return {...entry, person: p, id: [...own(p)].sort()[0], label: p.label};}
      catch {return {...entry, label: person.related_people?.[entry.id] || entry.id, unavailable: true};}
    }));
    const unique = new Map();
    for (const entry of resolved) mergeEvidence(unique, entry);
    return [...unique.values()];
  }
  const ancestors = [];
  const deferred = new Map();
  let frontier = [{person, path: own(person)}];
  for (let generation = 1; generation <= 3; generation++) {
    const next = [], row = [];
    for (const branch of frontier) {
      for (const [offset, kind] of [[1, 'grandfather'], [2, 'great_grandfather']]) {
        const target = generation + offset;
        if (target > 3) continue;
        const explicit = await resolve(related(branch.person, kind));
        if (!deferred.has(target)) deferred.set(target, []);
        deferred.get(target).push(...explicit.map(parent => ({parent, path: branch.path})));
      }
      const parents = await resolve(related(branch.person, 'father'));
      for (const parent of parents) {
        const cycle = parent.person && [...own(parent.person)].some(id => branch.path.has(id));
        row.push({...parent, cycle: Boolean(cycle)});
        if (parent.person && !cycle) next.push({person: parent.person, path: new Set([...branch.path, ...own(parent.person)])});
      }
    }
    for (const {parent, path} of deferred.get(generation) || []) {
      const cycle = parent.person && [...own(parent.person)].some(id => path.has(id));
      row.push({...parent, cycle: Boolean(cycle), explicitAncestor: true});
      if (parent.person && !cycle) next.push({person: parent.person, path: new Set([...path, ...own(parent.person)])});
    }
    const unique = new Map();
    for (const entry of row) mergeEvidence(unique, entry);
    ancestors.push([...unique.values()]); frontier = next;
  }
  const [mother, spouses, children] = await Promise.all(['mother', 'spouse', 'children'].map(kind => resolve(related(person, kind))));
  const ordered = orderChildren(children, person);
  const [adoptiveFather, adoptedChildren] = await Promise.all(
    ['adoptive_father', 'adopted_children'].map(kind => resolve(related(person, kind))));
  return {ancestors, mother, spouses, children: ordered.entries,
    ...(adoptiveFather.length ? {adoptive_father: adoptiveFather} : {}),
    ...(adoptedChildren.length ? {adopted_children: adoptedChildren} : {}),
    ...(ordered.conflicts.length ? {child_order_conflicts: ordered.conflicts} : {})};
}
