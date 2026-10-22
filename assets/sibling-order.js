// Apply source constraints without assigning unrecorded ordinals or using ID suffixes.
export function orderChildren(entries, parent) {
  const aliases = new Map();
  for (const e of entries) for (const id of [e.id, ...(e.person?.person_ids || [])]) aliases.set(id, e.id);
  const ids = entries.map(e => e.id), allowed = new Set(ids);
  const edges = new Map(ids.map(id => [id, new Set()]));
  const add = (a, b) => {a = aliases.get(a); b = aliases.get(b); if (a && b && a !== b) edges.get(a).add(b);};
  const parentIds = new Set(parent.person_ids || [parent.id]);
  const relations = [parent, ...entries.map(e => e.person).filter(Boolean)]
    .flatMap(p => p.preferred_relations || p.relations || []);
  const numbered = [], groups = new Map();
  const members = new Set(), sons = new Set(), daughters = new Set();
  const mark = (set, id) => {const canonical = aliases.get(id); if (canonical) set.add(canonical);};
  // A child edge establishes this parent's scope, but does not itself establish sex.
  // Qualified assembly entries are already source-attributed children from traceFamily.
  for (const e of entries) if (e.role === 'assembly_inferred' && (parent.assembled_children || []).some(row =>
      aliases.get(row.person_id) === e.id && parentIds.has(row.parent_person_id) && row.assembly_id
      && ['editorial_preferred', 'contextual_provisional'].includes(row.status)
      && row.parent_connection?.status === 'contextual_provisional'
      && ['shared_father_through_sibling', 'shared_father_through_sibling_chain',
        'parent_between_consecutive_ancestors', 'parent_between_body_and_attached_note_ancestors',
        'parent_through_paternal_uncle'].includes(row.parent_connection.type)
      && row.parent_connection.rationale && row.parent_connection.references?.length)) members.add(e.id);
  for (const r of relations) {
    const q = r.qualifiers || {};
    if (q.adopted_for_family_tree === false) continue;
    if (['father', 'mother'].includes(r.predicate) && parentIds.has(r.object_person_id)) mark(members, r.subject_person_id);
    if (['son', 'daughter'].includes(r.predicate) && parentIds.has(r.subject_person_id)) mark(members, r.object_person_id);
    // Brother/sister identifies only the subject's sex; the object may be a sister/brother.
    if (r.predicate === 'brother') mark(sons, r.subject_person_id);
    if (r.predicate === 'sister') mark(daughters, r.subject_person_id);
    if (r.predicate === 'son') mark(sons, r.object_person_id);
    if (r.predicate === 'daughter') mark(daughters, r.object_person_id);
    const relative = q.relative_birth_order;
    if (relative?.scope === 'siblings' && relative.operator === 'lt') add(relative.older_person_id, relative.younger_person_id);
    const order = q.birth_order;
    if (['father', 'mother'].includes(r.predicate) && parentIds.has(r.object_person_id)
        && parentIds.has(order?.parent_person_id) && Number.isInteger(order.ordinal) && order.ordinal > 0
        && ['sons_of_parent', 'daughters_of_parent', 'children_of_parent'].includes(order.scope)
        && aliases.has(r.subject_person_id)) numbered.push({id:r.subject_person_id, ...order});
    const group = q.source_sibling_group;
    if (group?.id && Array.isArray(group.member_roles) && Array.isArray(group.member_person_ids)
        && group.member_person_ids.length === group.reported_count
        && new Set(group.member_person_ids).size === group.reported_count
        && new Set(group.member_person_ids.map(id => aliases.get(id))).size === group.reported_count
        && group.member_person_ids.every(id => aliases.has(id))) {
      const list = groups.get(group.id) || [];
      list.push(group); groups.set(group.id, list);
    }
  }
  for (const n of numbered) {
    if (n.scope === 'sons_of_parent') mark(sons, n.id);
    if (n.scope === 'daughters_of_parent') mark(daughters, n.id);
  }
  // A sole attested first ordinal precedes unnumbered members only within its
  // demonstrated scope. Do not manufacture other ordinals or rank unknown-sex children.
  for (const n of numbered) if (n.ordinal === 1
      && (n.scope === 'children_of_parent' || !(sons.has(aliases.get(n.id)) && daughters.has(aliases.get(n.id))))) {
    const sameScope = n.scope === 'sons_of_parent' ? sons : n.scope === 'daughters_of_parent' ? daughters : members;
    for (const id of sameScope) if (members.has(id)
        && (n.scope === 'children_of_parent' || !(sons.has(id) && daughters.has(id)))) add(n.id, id);
  }
  for (const a of numbered) for (const b of numbered) {
    if (a.scope === b.scope && a.parent_person_id === b.parent_person_id && a.ordinal < b.ordinal) add(a.id, b.id);
  }
  for (const variants of groups.values()) {
    // Conflicting reports sharing an ID are not combined into a fabricated complete group.
    const group = variants[0];
    if (variants.some(g => JSON.stringify(g) !== JSON.stringify(group))) continue;
    const roles = group.member_roles;
    if (roles.length !== group.reported_count || new Set(roles.map(r => r.person_id)).size !== roles.length
        || roles.some(r => !group.member_person_ids.includes(r.person_id))) continue;
    for (const a of roles) for (const b of roles) {
      if (a.position === 'eldest' || b.position === 'youngest'
          || Number.isInteger(a.ordinal) && Number.isInteger(b.ordinal) && a.ordinal < b.ordinal) add(a.person_id, b.person_id);
    }
    // Only a complete, small reported group can imply the remaining slots. Nothing is written back.
    if (roles.length > 8) continue;
    const possibilities = [];
    function visit(path, remaining) {
      if (!remaining.length) {possibilities.push(path); return;}
      const slot = path.length + 1;
      for (const role of remaining) {
        if (role.ordinal != null && role.ordinal !== slot || role.position === 'eldest' && slot !== 1
            || role.position === 'youngest' && slot !== roles.length) continue;
        const id = aliases.get(role.person_id);
        if (remaining.some(other => other !== role && edges.get(aliases.get(other.person_id)).has(id))) continue;
        visit([...path, role.person_id], remaining.filter(r => r !== role));
      }
    }
    visit([], roles);
    if (!possibilities.length) continue;
    for (const a of roles) for (const b of roles) {
      if (a !== b && possibilities.every(p => p.indexOf(a.person_id) < p.indexOf(b.person_id))) add(a.person_id, b.person_id);
    }
  }
  // Collapse contradictory cycles, retain source order inside them, then sort the remaining constraints.
  let index = 0;
  const stack = [], active = new Set(), indices = new Map(), low = new Map(), components = [];
  function connect(id) {
    indices.set(id, index); low.set(id, index++); stack.push(id); active.add(id);
    for (const next of edges.get(id)) {
      if (!indices.has(next)) {connect(next); low.set(id, Math.min(low.get(id), low.get(next)));}
      else if (active.has(next)) low.set(id, Math.min(low.get(id), indices.get(next)));
    }
    if (low.get(id) === indices.get(id)) {
      const part = []; let next;
      do {next = stack.pop(); active.delete(next); part.push(next);} while (next !== id);
      part.sort((a, b) => ids.indexOf(a) - ids.indexOf(b)); components.push(part);
    }
  }
  for (const id of ids) if (!indices.has(id)) connect(id);
  const componentOf = new Map(); components.forEach((part, i) => part.forEach(id => componentOf.set(id, i)));
  const outgoing = components.map(() => new Set()), incoming = components.map(() => 0);
  for (const [a, targets] of edges) for (const b of targets) {
    const x = componentOf.get(a), y = componentOf.get(b);
    if (x !== y && !outgoing[x].has(y)) {outgoing[x].add(y); incoming[y]++;}
  }
  const ordered = [], ready = components.map((_, i) => i).filter(i => incoming[i] === 0);
  while (ready.length) {
    ready.sort((a, b) => ids.indexOf(components[a][0]) - ids.indexOf(components[b][0]));
    const i = ready.shift(); ordered.push(...components[i]);
    for (const j of outgoing[i]) if (--incoming[j] === 0) ready.push(j);
  }
  const byId = new Map(entries.map(e => [e.id, e]));
  return {entries:ordered.filter(id => allowed.has(id)).map(id => byId.get(id)),
    conflicts:components.filter(part => part.length > 1)};
}
