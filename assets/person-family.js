import {orderChildren} from './sibling-order.js';
// Read validated namespace metadata; its unnamed structural slot is never loaded as a person.
export async function namespaceNavigation(person, load) {
  const row = person.assembled_identity, group = row?.collateral_root_group;
  if (!row?.namespace_id || row.root_person_id !== null
      || group?.type !== 'unknown_shared_father_from_qualified_first_cousins'
      || group.status !== 'contextual_provisional' || !Array.isArray(group.references) || !group.references.length
      || !Array.isArray(group.root_person_ids)
      || group.common_parent_person_id !== null || group.common_parent_name !== null
      || group.common_parent_registered !== false || group.relative_age !== 'unknown'
      || new Set(group.root_person_ids).size !== 2
      || group.root_person_ids.some(id => id === row.namespace_id || !id.startsWith(row.namespace_id + '_'))) return null;
  const roots = await Promise.all(group.root_person_ids.map(async id => {
    let data;
    try { data = await load(id); } catch { data = null; }
    return {id, label: data?.label || id, ...(data ? {person: data} : {unavailable: true}),
      role: 'assembly_inferred', inference_note: group.rationale, evidence: group.references};
  }));
  return {namespace_id: row.namespace_id, entry_person_id: row.namespace_entry_person_id,
    roots, common_parent_person_id: null, qualification: 'assembly_inferred',
    inference_note: group.rationale, evidence: group.references};
}

// Traverse source relations and separately attributed assembly edges, never stored ancestor chains.
export async function traceFamily(person, load) {
  const own = p => new Set(p.person_ids || [p.id]);
  function mergeEvidence(map, entry) {
    const previous = map.get(entry.id);
    if (!previous) { map.set(entry.id, entry); return; }
    const paths = [...(previous.ancestry_paths || []), ...(entry.ancestry_paths || [])];
    if (paths.some(p => p.qualification === 'assembly_inferred')) {
      const rank = x => x.cycle ? 0 : x.role === 'assembly_inferred' ? 1 : 2;
      const best = rank(entry) > rank(previous) ? entry : previous;
      // Do not relabel an inferred route's quotation as the selected direct
      // grandparent assertion. Both routes retain their original step evidence.
      const directEvidence = [previous, entry].filter(x => rank(x) === 2).flatMap(x => x.evidence);
      const allPaths = [...new Map(paths.map(p => [JSON.stringify(p), p])).values()];
      const merged = {...best, evidence: rank(best) === 2 ? directEvidence : best.evidence,
        ancestry_paths: allPaths};
      const available = [previous, entry].find(x => x.person && !x.unavailable && !x.cycle);
      if (available) {
        merged.person = available.person; merged.label = available.label;
        delete merged.unavailable;
        merged.ancestry_paths = allPaths.map(p => ({...p, unavailable: false}));
      }
      map.set(entry.id, merged);
      return;
    }
    const direct = previous.role === 'assembly_inferred' && entry.role !== 'assembly_inferred'
      && !entry.unavailable && !entry.cycle;
    if (direct) map.set(entry.id, {...entry, evidence: [...entry.evidence, ...previous.evidence]});
    else previous.evidence.push(...entry.evidence);
    if (paths.length) map.get(entry.id).ancestry_paths = paths;
  }

  function related(p, kind) {
    const ids = own(p), result = new Map();
    const pending = (p.unresolved_relation_identity_groups || []).filter(g => g.status === 'unresolved' && g.predicate === 'spouse' && g.same_person === null && g.distinct_people === null);
    for (const r of p.preferred_relations || p.relations || []) {
      if (pending.some(g => g.assertion_ids.includes(r.id))) continue;
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
          || !['shared_father_through_sibling', 'shared_father_through_sibling_chain', 'parent_between_consecutive_ancestors', 'parent_between_body_and_attached_note_ancestors', 'parent_through_paternal_uncle', 'parent_from_nephew_named_father_and_grandfather'].includes(connection.type)
          || !connection.rationale || !connection.references?.length) return;
      result.set(id, {id, role: 'assembly_inferred', inference_note: connection.rationale,
        evidence: connection.references.map(ref => ({...ref}))});
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
          && ['shared_ancestor_through_sibling', 'ancestor_through_paternal_uncle'].includes(connection?.type)
          && connection.status === 'contextual_provisional'
          && connection.rationale && connection.references?.length) {
        result.set(id, {id, role: 'assembly_inferred', inference_note: connection.rationale,
          evidence: connection.references.map(ref => ({...ref}))});
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
  function qualifyAncestor(parent, branch, relationship, distance) {
    const step = {from_person_id: branch.resolvedId || branch.person.id, to_person_id: parent.id,
      from_label: branch.person.label || branch.person.id, to_label: parent.label || parent.id,
      relationship, generation_distance: distance,
      qualification: parent.role === 'assembly_inferred' ? 'assembly_inferred' : 'source_linked',
      inference_note: parent.inference_note || null, evidence: [...parent.evidence]};
    const steps = [...(branch.ancestrySteps || []), step];
    const inferred = steps.some(x => x.qualification === 'assembly_inferred');
    const cycle = Boolean(parent.person && [...own(parent.person)].some(id => branch.path.has(id)));
    const route = {person_ids: [steps[0].from_person_id, ...steps.map(x => x.to_person_id)],
      qualification: inferred ? 'assembly_inferred' : 'source_linked',
      cycle, unavailable: Boolean(parent.unavailable), lookup_unavailable: Boolean(parent.unavailable), steps};
    const out = {...parent, cycle, ancestry_paths: [route]};
    if (inferred) {
      out.role = 'assembly_inferred';
      out.inference_note = steps.filter(x => x.qualification === 'assembly_inferred')
        .map(x => x.inference_note).filter(Boolean).join('；');
    }
    return out;
  }
  const ancestors = [];
  const deferred = new Map();
  let frontier = [{person, path: own(person), resolvedId: person.id, ancestrySteps: []}];
  for (let generation = 1; generation <= 3; generation++) {
    const next = [], row = [], nextCandidates = [];
    for (const branch of frontier) {
      for (const [offset, kind] of [[1, 'grandfather'], [2, 'great_grandfather']]) {
        const target = generation + offset;
        if (target > 3) continue;
        const explicit = await resolve(related(branch.person, kind));
        if (!deferred.has(target)) deferred.set(target, []);
        deferred.get(target).push(...explicit.map(parent => ({parent: qualifyAncestor(parent, branch, kind, offset + 1), path: branch.path})));
      }
      const parents = await resolve(related(branch.person, 'father'));
      for (const parent of parents) {
        const qualified = qualifyAncestor(parent, branch, 'father', 1);
        row.push(qualified);
        nextCandidates.push({parent: qualified, path: branch.path});
      }
    }
    for (const {parent, path} of deferred.get(generation) || []) {
      row.push({...parent, explicitAncestor: true});
      nextCandidates.push({parent, path});
    }
    const unique = new Map();
    for (const entry of row) mergeEvidence(unique, entry);
    for (const candidate of nextCandidates) {
      const merged = unique.get(candidate.parent.id);
      const recovery = merged?.ancestry_paths?.some(p => p.qualification === 'assembly_inferred');
      const loaded = candidate.parent.person || (recovery ? merged.person : null);
      if (loaded && !candidate.parent.cycle) next.push({person: loaded,
        path: new Set([...candidate.path, ...own(loaded)]), resolvedId: candidate.parent.id,
        ancestrySteps: candidate.parent.ancestry_paths[0].steps});
    }
    ancestors.push([...unique.values()].map(entry => {
      if (entry.ancestry_paths?.some(p => p.qualification === 'assembly_inferred')) return entry;
      // Pure source-linked routes keep the exact pre-extension public shape.
      const {ancestry_paths, ...legacy} = entry;
      return legacy;
    })); frontier = next;
  }
  const [mother, spouses, children] = await Promise.all(['mother', 'spouse', 'children'].map(kind => resolve(related(person, kind))));
  const ordered = orderChildren(children, person);
  const [adoptiveFather, adoptedChildren] = await Promise.all(
    ['adoptive_father', 'adopted_children'].map(kind => resolve(related(person, kind))));
  const unresolvedSpouseGroups = (person.unresolved_relation_identity_groups || []).filter(g => g.status === 'unresolved' && g.predicate === 'spouse' && g.same_person === null && g.distinct_people === null && [g.common_person_id, ...g.candidate_person_ids].some(id => own(person).has(id)));
  const familyNamespace = await namespaceNavigation(person, load);
  return {ancestors, mother, spouses, children: ordered.entries,
    ...(familyNamespace ? {family_namespace: familyNamespace} : {}),
    ...(unresolvedSpouseGroups.length ? {unresolved_spouse_groups: unresolvedSpouseGroups} : {}),
    ...(adoptiveFather.length ? {adoptive_father: adoptiveFather} : {}),
    ...(adoptedChildren.length ? {adopted_children: adoptedChildren} : {}),
    ...(ordered.conflicts.length ? {child_order_conflicts: ordered.conflicts} : {})};
}
