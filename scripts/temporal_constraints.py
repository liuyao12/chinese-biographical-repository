"""來源日期約束的結構驗證與年份交集；不執行自然語言判讀。"""
from __future__ import annotations

_DATE_KEYS = {"calendar", "year_system", "precision", "year", "inclusive"}
_DATE_OPTIONAL = {"month", "day", "era_id"}
_OPERATORS = {"equals", "within_interval", "not_before", "not_after", "after_event", "not_before_event"}
_RULES = {
    "person_alive_at_event_implies_death_not_before",
    "narrative_sequence_implies_event_order",
}


def _date_errors(value, label):
    if not isinstance(value, dict):
        return [f"{label}須為日期物件"]
    keys = set(value)
    required = _DATE_KEYS
    errors = []
    if not required.issubset(keys) or keys - required - _DATE_OPTIONAL:
        errors.append(f"{label}欄位不符日期值格式")
    for key in ("calendar", "year_system", "precision"):
        if not isinstance(value.get(key), str) or not value[key]:
            errors.append(f"{label}.{key}須有明確值")
    if value.get("year_system") not in ("astronomical", "historical", "regnal"):
        errors.append(f"{label}.year_system須為絕對年序或年號序數年")
    if type(value.get("year")) is not int:
        errors.append(f"{label}.year須為整數")
    elif value.get("year_system") == "historical" and value["year"] == 0:
        errors.append(f"{label}.year不得使用歷史紀年中不存在的公元零年")
    elif value.get("year_system") == "regnal" and value["year"] < 1:
        errors.append(f"{label}.year年號序數須大於零")
    if type(value.get("inclusive")) is not bool:
        errors.append(f"{label}.inclusive須為布林值")
    precision = value.get("precision")
    if precision not in ("year", "month", "day"):
        errors.append(f"{label}.precision無效")
    if precision in ("month", "day") and (type(value.get("month")) is not int or not 1 <= value["month"] <= 12):
        errors.append(f"{label}月精度須有有效月份")
    if precision == "year" and ("month" in value or "day" in value):
        errors.append(f"{label}年精度不得含月份或日期")
    if precision == "month" and "day" in value:
        errors.append(f"{label}月精度不得含日期")
    if precision == "day" and (type(value.get("day")) is not int or not 1 <= value["day"] <= 31):
        errors.append(f"{label}日精度須有有效日期")
    if value.get("year_system") == "regnal":
        if not isinstance(value.get("era_id"), str) or not value["era_id"]:
            errors.append(f"{label}年號序數年須有 era_id")
    elif "era_id" in value:
        errors.append(f"{label}絕對年不得帶 era_id")
    return errors


def _coordinate(value):
    return tuple(value.get(k) for k in ("calendar", "year_system", "precision", "era_id"))


def _quote_contains_mention(paragraph, quote, mention_id, person_id, quote_start=None, quote_end=None):
    text = paragraph.get("text", "")
    if not isinstance(text, str) or not isinstance(quote, str):
        return False
    mention = next((m for m in paragraph.get("mentions", [])
                   if isinstance(m, dict) and m.get("id") == mention_id), None)
    if mention is None or mention.get("person_id") != person_id:
        return False
    start, end, surface = mention.get("start"), mention.get("end"), mention.get("surface")
    if (type(start) is not int or type(end) is not int or not isinstance(surface, str)
            or not 0 <= start < end <= len(text) or text[start:end] != surface):
        return False
    if type(quote_start) is not int or type(quote_end) is not int:
        return False
    return (text[quote_start:quote_end] == quote
            and quote_start <= start < end <= quote_end)


def _temporal_claim_errors(citation, item):
    claim = citation.get("temporal_claim")
    errors = []
    quote = citation.get("quote")
    if not isinstance(claim, dict):
        return ["缺 temporal_claim"]
    source_term, start, end = claim.get("source_term"), claim.get("start"), claim.get("end")
    if (not isinstance(source_term, str) or not source_term
            or type(start) is not int or type(end) is not int
            or not isinstance(quote, str) or not 0 <= start < end <= len(quote)
            or quote[start:end] != source_term):
        errors.append("日期詞錨點與引句不符")
        return errors
    forms = [key for key in ("normalized_date", "normalized_interval", "normalized_relation") if key in claim]
    if len(forms) != 1:
        errors.append("temporal_claim 須且只能有一種正規化結果")
        return errors
    form = forms[0]
    operator = item.get("operator")
    if operator in ("equals", "not_before", "not_after"):
        if form != "normalized_date" or claim.get("normalized_date") != item.get("bound"):
            errors.append("引文正規化日期與約束界限不符")
    elif operator == "within_interval":
        if form != "normalized_interval" or claim.get("normalized_interval") != item.get("interval"):
            errors.append("引文正規化日期範圍與約束區間不符")
    elif operator in ("after_event", "not_before_event"):
        relation = claim.get("normalized_relation")
        if (form != "normalized_relation" or not isinstance(relation, dict)
                or relation != {"operator": operator, "related_event_id": item.get("related_event_id")}):
            errors.append("引文正規化事件關係與約束不符")
    else:
        errors.append("未知日期約束運算子")
    return errors


def errors(records, chapters, person_ids):
    """Validate every temporal constraint against event, person, passage and mention records."""
    errors = []
    pids = set(person_ids)
    events = {}
    for record in records:
        if record.get("record_type") in ("person_life_event_assertion_set", "table_person_life_event_assertion_set", "person_event_assertion_set"):
            for event in record.get("events", []):
                event_id = event.get("id")
                if isinstance(event_id, str) and event_id:
                    events[event_id] = event
    seen = set()
    all_constraints = {}
    for record in records:
        if record.get("record_type") == "temporal_constraint_set":
            for constraint in record.get("constraints", []):
                if isinstance(constraint, dict) and isinstance(constraint.get("id"), str):
                    all_constraints[constraint["id"]] = constraint
    paragraph_index = {
        paragraph.get("id"): (chapter, paragraph)
        for chapter in chapters.values()
        for paragraph in chapter.get("paragraphs", [])
    }
    for record in records:
        if record.get("record_type") != "temporal_constraint_set":
            continue
        root_chapter_id = record.get("chapter_id")
        root_chapter = chapters.get(root_chapter_id) if isinstance(root_chapter_id, str) else None
        if (record.get("format_version") != "0.1" or not isinstance(root_chapter, dict)
                or any(record.get(k) != root_chapter.get(k) for k in ("work_id", "book_id", "source_id"))):
            errors.append("日期約束集著作、卷、來源或篇章 ID 不符")
        constraints = record.get("constraints")
        if not isinstance(constraints, list):
            errors.append("日期約束集須有 constraints 陣列")
            continue
        for item in constraints:
            if not isinstance(item, dict):
                errors.append("日期約束須為物件")
                continue
            cid = item.get("id")
            if not isinstance(cid, str) or not cid or cid in seen:
                errors.append("日期約束 ID 缺失或重複")
            else:
                seen.add(cid)
            person_id = item.get("person_id")
            if not isinstance(person_id, str) or person_id not in pids:
                errors.append(f"日期約束人物 ID 不存在：{cid}")
            target_id = item.get("target_event_id")
            target = events.get(target_id) if isinstance(target_id, str) else None
            if target is None or target.get("person_id") != person_id:
                errors.append(f"日期約束目標事件不存在或人物不符：{cid}")
            operator = item.get("operator")
            if operator not in _OPERATORS:
                errors.append(f"日期約束運算子無效：{cid}")
            mode = item.get("assertion_mode")
            if mode not in ("direct", "derived"):
                errors.append(f"日期約束須標明 direct 或 derived：{cid}")
            derivation = item.get("derivation")
            if mode == "derived":
                if not isinstance(derivation, dict) or derivation.get("rule_id") not in _RULES:
                    errors.append(f"衍生日期約束須引用已登記規則：{cid}")
                elif derivation.get("rule_id") == "person_alive_at_event_implies_death_not_before":
                    if not isinstance(derivation.get("input_event_id"), str) or derivation.get("input_event_id") not in events:
                        errors.append(f"在世推導須引用已登記輸入事件：{cid}")
                        input_event = None
                    else:
                        input_event = events[derivation["input_event_id"]]
                    if input_event is None:
                        pass
                    else:
                        input_id = derivation["input_event_id"]
                        if input_event.get("person_id") != person_id:
                            errors.append(f"日期約束輸入事件人物不符：{cid}")
                        if operator != "not_before" or target is None or target.get("event_type") != "death":
                            errors.append(f"在世推導規則僅能產生同一人物的死亡下界：{cid}")
                        if (input_id == target_id or input_event.get("event_type") != "visit"
                                or input_event.get("participant_role") != "visited_person"
                                or not input_event.get("date_expression")
                                or not isinstance(input_event.get("normalized_date"), dict)):
                            errors.append(f"在世推導須使用有精確正規化日期的被訪者事件且不得自我引用：{cid}")
                        elif item.get("bound") != input_event["normalized_date"]:
                            errors.append(f"死亡下界必須等於訪問事件的正規化日期：{cid}")
                elif derivation.get("rule_id") == "narrative_sequence_implies_event_order":
                    valid_relation = (
                        operator == "after_event" and target is not None
                        and isinstance(derivation.get("ordering_basis"), str)
                        and derivation.get("ordering_basis") == "narrative_sequence"
                        and derivation.get("condition_status") == "conditionally_accepted"
                        and derivation.get("review_status") in ("agent_reviewed", "human_reviewed")
                        and item.get("human_reviewed") is (derivation.get("review_status") == "human_reviewed")
                        and isinstance(item.get("related_event_id"), str)
                        and item.get("related_event_id") in events
                        and item.get("related_event_id") != target_id
                    )
                    if not valid_relation:
                        errors.append(f"敘事次序事件關係須經代理或真人覆核並明示條件；human_reviewed 須如實標記：{cid}")
                    if isinstance(derivation.get("input_constraint_ids"), list):
                        errors.append(f"事件次序原子約束不得再以推導輸入約束取代來源引文：{cid}")
            elif derivation is not None:
                errors.append(f"直接日期約束不得附 derivation：{cid}")
            if operator in ("equals", "not_before", "not_after"):
                if "interval" in item or "related_event_id" in item:
                    errors.append(f"日期約束欄位與運算子不符：{cid}")
                errors.extend(_date_errors(item.get("bound"), f"{cid}.bound"))
                if operator == "equals" and isinstance(item.get("bound"), dict) and item["bound"].get("inclusive") is not True:
                    errors.append(f"等值日期約束必須包含其唯一日期：{cid}")
            elif operator == "within_interval":
                interval = item.get("interval")
                if not isinstance(interval, dict) or set(interval) != {"earliest", "latest"}:
                    errors.append(f"區間約束須含 earliest 與 latest：{cid}")
                    interval = {}
                for side in ("earliest", "latest"):
                    value = interval.get(side)
                    if value is not None:
                        errors.extend(_date_errors(value, f"{cid}.interval.{side}"))
                lower, upper = interval.get("earliest"), interval.get("latest")
                if lower is None and upper is None:
                    errors.append(f"區間約束不可兩端皆無界：{cid}")
                if (isinstance(lower, dict) and isinstance(upper, dict)
                        and not _date_errors(lower, f"{cid}.interval.earliest")
                        and not _date_errors(upper, f"{cid}.interval.latest")):
                    if _coordinate(lower) != _coordinate(upper) or lower["year"] > upper["year"]:
                        errors.append(f"區間約束端點座標不相容或順序錯誤：{cid}")
                    elif lower["year"] == upper["year"] and not (lower["inclusive"] and upper["inclusive"]):
                        errors.append(f"區間約束同年端點形成空集：{cid}")
            elif operator in ("after_event", "not_before_event"):
                related_id = item.get("related_event_id")
                if (not isinstance(related_id, str) or related_id not in events
                        or related_id == target_id or any(k in item for k in ("bound", "interval"))):
                    errors.append(f"相對事件約束缺少有效且不同於目標事件的 related_event_id，或含有多餘界限：{cid}")
            if type(item.get("human_reviewed")) is not bool:
                errors.append(f"日期約束 human_reviewed 須為布林值：{cid}")
            evidence = item.get("evidence")
            if not isinstance(evidence, list) or not evidence:
                errors.append(f"日期約束缺來源引文：{cid}")
                continue
            for citation in evidence:
                if not isinstance(citation, dict):
                    errors.append(f"日期約束引文須為物件：{cid}")
                    continue
                if "constraint_id" in citation:
                    ref_id = citation.get("constraint_id")
                    if (mode != "derived" or not isinstance(ref_id, str)
                            or ref_id not in all_constraints
                            or not isinstance(derivation, dict)
                            or ref_id not in derivation.get("input_constraint_ids", [])):
                        errors.append(f"推導引文須引用 derivation 所列的既存輸入約束：{cid}")
                    continue
                pid = citation.get("paragraph_id")
                hit = paragraph_index.get(pid)
                quote = citation.get("quote")
                mention_id = citation.get("person_mention_id")
                if not hit:
                    errors.append(f"日期約束引文段落不存在：{cid}")
                    continue
                chapter, paragraph = hit
                if any(citation.get(k) != chapter.get(k) for k in ("work_id", "book_id", "source_id", "chapter_id")):
                    errors.append(f"日期約束引文來源座標不符：{cid}")
                paragraph_text = paragraph.get("text")
                quote_start, quote_end = citation.get("quote_start"), citation.get("quote_end")
                if (not isinstance(quote, str) or not quote or not isinstance(paragraph_text, str)
                        or quote not in paragraph_text
                        or type(quote_start) is not int or type(quote_end) is not int
                        or not 0 <= quote_start < quote_end <= len(paragraph_text)
                        or paragraph_text[quote_start:quote_end] != quote):
                    errors.append(f"日期約束引文不在原段中或未以字元位置精確錨定：{cid}")
                    continue
                if not _quote_contains_mention(paragraph, quote, mention_id, person_id, quote_start, quote_end):
                    errors.append(f"日期約束人物錨點不在引文內：{cid}")
                errors.extend(f"{message}：{cid}" for message in _temporal_claim_errors(citation, item))
                if mode == "derived" and isinstance(derivation, dict):
                    if derivation.get("rule_id") == "narrative_sequence_implies_event_order":
                        related_event = events.get(item.get("related_event_id"))
                        related_person_id = related_event.get("person_id") if isinstance(related_event, dict) else None
                        if (isinstance(related_person_id, str) and related_person_id != person_id
                                and not _quote_contains_mention(
                                    paragraph, quote, citation.get("related_person_mention_id"), related_person_id,
                                    quote_start, quote_end
                                )):
                            errors.append(f"跨人物事件次序引文須錨定兩位人物：{cid}")
                        continue
                    input_event = events.get(derivation.get("input_event_id"))
                    temporal_claim = citation.get("temporal_claim", {})
                    if input_event is not None:
                        if temporal_claim.get("source_term") != input_event.get("date_expression"):
                            errors.append(f"在世推導日期詞須與輸入事件紀年相同：{cid}")
                        if not any(
                            e.get("paragraph_id") == pid and e.get("quote") == quote
                            and e.get("person_mention_id") == mention_id
                            for e in input_event.get("evidence", [])
                        ):
                            errors.append(f"在世推導引文須是輸入事件的原始證據：{cid}")
    return errors


def calculate_temporal_constraint_results(constraints):
    """Calculate each event's year interval and conditionally propagate narrative order.

    A later event's inclusive upper year bounds an earlier event at the same
    year precision. Results retain both source constraint IDs and explicitly
    conditional narrative-order assumptions.
    """
    by_target = {}
    event_relations = []
    unhandled_relations = []
    for item in constraints:
        target_id = item.get("target_event_id")
        derivation = item.get("derivation")
        rule_id = derivation.get("rule_id") if isinstance(derivation, dict) else None
        if isinstance(target_id, str) and item.get("operator") not in ("after_event", "not_before_event"):
            by_target.setdefault(target_id, []).append(item)
        if (item.get("operator") == "after_event"
                and rule_id == "narrative_sequence_implies_event_order"):
            event_relations.append(item)
        elif item.get("operator") in ("after_event", "not_before_event"):
            unhandled_relations.append(item)

    results = {}
    for event_id, items in by_target.items():
        try:
            results[event_id] = intersect_year_constraints(items)
        except ValueError:
            # Preserve incompatible or malformed source constraints without
            # aborting the person bundle/API calculation.
            results[event_id] = {
                "status": "incomplete", "coordinate": None,
                "earliest": None, "latest": None, "conflict": False,
                "unsupported_constraint_ids": sorted(
                    item.get("id") for item in items if isinstance(item.get("id"), str)
                ),
            }
    derivations = {event_id: [] for event_id in results}
    unsupported = {event_id: [] for event_id in results}
    for relation in unhandled_relations:
        relation_id = relation.get("id")
        for event_id in (relation.get("target_event_id"), relation.get("related_event_id")):
            if isinstance(event_id, str):
                unsupported.setdefault(event_id, []).append(relation_id)
    # Only explicitly accepted and honestly labeled order edges contribute
    # to cycle detection; rejected suggestions must not poison accepted data.
    candidate_relations = []
    for relation in event_relations:
        earlier_id = relation.get("related_event_id")
        relation_derivation = relation.get("derivation", {})
        condition = relation_derivation.get("condition_status")
        relation_id = relation.get("id")
        if (relation.get("assertion_mode") != "derived"
                or relation_derivation.get("ordering_basis") != "narrative_sequence"
                or relation_derivation.get("review_status") not in ("agent_reviewed", "human_reviewed")
                or relation.get("human_reviewed") is not (relation_derivation.get("review_status") == "human_reviewed")
                or condition != "conditionally_accepted"):
            unsupported.setdefault(earlier_id, []).append(relation_id)
            continue
        candidate_relations.append(relation)

    adjacency = {}
    for relation in candidate_relations:
        earlier = relation.get("related_event_id")
        later = relation.get("target_event_id")
        if isinstance(earlier, str) and isinstance(later, str):
            adjacency.setdefault(earlier, set()).add(later)

    cyclic_relation_ids = set()
    for relation in candidate_relations:
        earlier = relation.get("related_event_id")
        later = relation.get("target_event_id")
        if not isinstance(earlier, str) or not isinstance(later, str):
            continue
        pending = [later]
        reached = set()
        while pending:
            current = pending.pop()
            if current == earlier:
                cyclic_relation_ids.add(relation.get("id"))
                break
            if current in reached:
                continue
            reached.add(current)
            pending.extend(adjacency.get(current, ()))

    usable_relations = []
    for relation in candidate_relations:
        earlier_id = relation.get("related_event_id")
        later_id = relation.get("target_event_id")
        relation_id = relation.get("id")
        if relation_id in cyclic_relation_ids:
            unsupported.setdefault(earlier_id, []).append(relation_id)
            unsupported.setdefault(later_id, []).append(relation_id)
            continue
        usable_relations.append(relation)

    # The accepted graph is acyclic after cyclic edges are removed. Process
    # edges from later topological levels to earlier ones so every event's
    # outgoing upper bounds settle before those bounds are used upstream.
    nodes = set()
    indegree = {}
    for earlier, later_nodes in adjacency.items():
        nodes.add(earlier)
        nodes.update(later_nodes)
        for later in later_nodes:
            indegree[later] = indegree.get(later, 0) + 1
    levels = {node: 0 for node in nodes}
    pending_nodes = sorted(node for node in nodes if indegree.get(node, 0) == 0)
    while pending_nodes:
        current = pending_nodes.pop(0)
        for later in sorted(adjacency.get(current, ())):
            levels[later] = max(levels[later], levels[current] + 1)
            indegree[later] -= 1
            if indegree[later] == 0:
                pending_nodes.append(later)
                pending_nodes.sort()
    usable_relations.sort(key=lambda relation: (
        -levels.get(relation.get("related_event_id"), 0), str(relation.get("id", ""))
    ))

    # This order is independent of JSON input order and prevents retaining a
    # bound from an event that becomes conflicted farther down the chain.
    synthetic_by_relation = {}
    synthetic_by_id = {}
    failed_relations = set()

    def expand_constraint_ids(ids, seen=None):
        seen = set() if seen is None else seen
        expanded = []
        for constraint_id in ids:
            if constraint_id in seen:
                continue
            provenance = synthetic_by_id.get(constraint_id)
            if provenance is None:
                expanded.append(constraint_id)
            else:
                expanded.extend(expand_constraint_ids(provenance, seen | {constraint_id}))
        return list(dict.fromkeys(expanded))

    while True:
        changed = False
        for relation in usable_relations:
            relation_id = relation.get("id")
            if relation_id in failed_relations:
                continue
            earlier_id = relation.get("related_event_id")
            later_id = relation.get("target_event_id")
            later_result = results.get(later_id)
            if isinstance(later_result, dict) and later_result.get("conflict"):
                failed_relations.add(relation_id)
                unsupported.setdefault(earlier_id, []).append(relation_id)
                continue
            latest = later_result.get("latest") if isinstance(later_result, dict) else None
            if (not latest or not isinstance(later_result.get("coordinate"), dict)
                    or later_result["coordinate"].get("precision") != "year"):
                continue

            coordinate = later_result["coordinate"]
            bound = dict(coordinate, year=latest["year"], inclusive=latest["inclusive"])
            relation_inputs = sorted(set(
                expand_constraint_ids(latest.get("constraint_ids", [])) + [relation_id]
            ))
            synthetic = synthetic_by_relation.get(relation_id)
            is_new = synthetic is None
            prior_bound = synthetic.get("bound") if synthetic is not None else None
            prior_provenance = synthetic_by_id.get(synthetic.get("id")) if synthetic is not None else None
            if synthetic is not None:
                old = synthetic["bound"]
                tighter = (bound["year"] < old["year"]
                           or bound["year"] == old["year"]
                           and old["inclusive"] and not bound["inclusive"])
                provenance_changed = prior_provenance != relation_inputs
                if not tighter and not provenance_changed:
                    continue
                if tighter:
                    synthetic["bound"] = bound
            else:
                tighter = True
                provenance_changed = True
                synthetic = {
                    "id": "derived-upper:" + str(earlier_id) + ":" + str(relation_id),
                    "target_event_id": earlier_id,
                    "operator": "not_after",
                    "bound": bound,
                }
                synthetic_by_relation[relation_id] = synthetic
                by_target.setdefault(earlier_id, []).append(synthetic)
            synthetic_by_id[synthetic["id"]] = relation_inputs

            try:
                updated = intersect_year_constraints(by_target[earlier_id])
            except (KeyError, TypeError, ValueError):
                if is_new:
                    by_target[earlier_id].remove(synthetic)
                    del synthetic_by_relation[relation_id]
                    synthetic_by_id.pop(synthetic["id"], None)
                else:
                    synthetic["bound"] = prior_bound
                    synthetic_by_id[synthetic["id"]] = prior_provenance
                failed_relations.add(relation_id)
                unsupported.setdefault(earlier_id, []).append(relation_id)
                continue

            results[earlier_id] = updated
            entries = derivations.setdefault(earlier_id, [])
            entry = next((d for d in entries if d.get("relation_id") == relation_id), None)
            if entry is None:
                entries.append({
                    "relation_id": relation_id,
                    "rule_id": "event_precedes_bounded_event_implies_not_after",
                    "input_constraint_ids": relation_inputs,
                    "condition_status": "conditionally_accepted",
                    "ordering_basis": relation_derivation.get("ordering_basis"),
                    "derived_bound": bound,
                })
            else:
                entry.update({
                    "input_constraint_ids": relation_inputs,
                    "derived_bound": bound,
                })
            changed = changed or is_new or tighter or provenance_changed
        if not changed:
            break

    # Relations whose later event never acquired a comparable upper bound
    # remain explicit incomplete inputs on the earlier event.
    propagated = {d.get("relation_id") for entries in derivations.values() for d in entries}
    for relation in usable_relations:
        relation_id = relation.get("id")
        if relation_id not in propagated:
            unsupported.setdefault(relation.get("related_event_id"), []).append(relation_id)

    for event_id, items in unsupported.items():
        if event_id not in results and items:
            results[event_id] = {
                "status": "incomplete", "coordinate": None,
                "earliest": None, "latest": None, "conflict": False,
                "unsupported_constraint_ids": sorted(set(items)),
            }
    for event_id, result in results.items():
        result["derivations"] = derivations.get(event_id, [])
        result["conditional_assumptions"] = [
            d["ordering_basis"] for d in derivations.get(event_id, [])
        ]
        if unsupported.get(event_id):
            result["unsupported_constraint_ids"] = sorted(set(
                result.get("unsupported_constraint_ids", []) + unsupported[event_id]
            ))
            result["status"] = "incomplete"
        elif derivations.get(event_id) and not result.get("conflict"):
            result["status"] = "conditional"
    return results


def temporal_constraint_closure(constraints, person_ids):
    """Return a stable dependency closure of constraints touching these people/events."""
    selected = {c["id"]: c for c in constraints
                if isinstance(c, dict) and isinstance(c.get("id"), str)
                and c.get("person_id") in set(person_ids)}
    changed = True
    while changed:
        changed = False
        linked_events = {event_id for c in selected.values()
                         for event_id in (c.get("target_event_id"), c.get("related_event_id"))
                         if isinstance(event_id, str)}
        input_ids = {input_id for c in selected.values()
                     for input_id in (c.get("derivation", {}).get("input_constraint_ids", [])
                                      if isinstance(c.get("derivation"), dict) else [])
                     if isinstance(input_id, str)}
        for c in constraints:
            if not isinstance(c, dict) or c.get("id") in selected:
                continue
            if (c.get("id") in input_ids or c.get("target_event_id") in linked_events
                    or c.get("related_event_id") in linked_events):
                if isinstance(c.get("id"), str):
                    selected[c["id"]] = c
                    changed = True
    return list(selected.values())


def intersect_year_constraints(constraints):
    """Intersect year-only bounds that share one calendar and year-system coordinate.

    Returns bound years and contributing constraint IDs; an empty intersection is
    preserved as conflict=True rather than silently choosing a source.
    """
    lower = None
    upper = None
    coordinate = None
    lower_ids = []
    upper_ids = []
    unsupported_ids = []
    for item in constraints:
        op = item.get("operator")
        if op not in ("equals", "within_interval", "not_before", "not_after"):
            unsupported_ids.append(item.get("id"))
            continue
        if op == "equals":
            value = item.get("bound")
            if not isinstance(value, dict) or value.get("inclusive") is not True:
                raise ValueError("等值日期約束必須包含其唯一日期")
        bounds = []
        if op == "within_interval":
            interval = item.get("interval", {})
            bounds = [("earliest", interval.get("earliest")), ("latest", interval.get("latest"))]
        elif op == "equals":
            bounds = [("earliest", item.get("bound")), ("latest", item.get("bound"))]
        elif op == "not_before":
            bounds = [("earliest", item.get("bound"))]
        else:
            bounds = [("latest", item.get("bound"))]
        for side, value in bounds:
            if value is None:
                continue
            if value.get("precision") != "year" or type(value.get("year")) is not int:
                raise ValueError("年份交集只接受已正規化的年精度日期")
            here = _coordinate(value)
            if coordinate is None:
                coordinate = here
            elif here != coordinate:
                raise ValueError("日期界限座標不同，須先作有來源的轉換")
            number = value["year"]
            inclusive = value.get("inclusive") is True
            target = lower if side == "earliest" else upper
            ids = lower_ids if side == "earliest" else upper_ids
            if target is None or (number > target if side == "earliest" else number < target):
                if side == "earliest":
                    lower = number
                    lower_inclusive = inclusive
                else:
                    upper = number
                    upper_inclusive = inclusive
                ids.clear()
                ids.append(item.get("id"))
            elif number == target:
                ids.append(item.get("id"))
                if side == "earliest":
                    lower_inclusive = lower_inclusive and inclusive
                else:
                    upper_inclusive = upper_inclusive and inclusive
    if lower is not None and "lower_inclusive" not in locals():
        lower_inclusive = True
    if upper is not None and "upper_inclusive" not in locals():
        upper_inclusive = True
    conflict = (lower is not None and upper is not None
                and (lower > upper or lower == upper and not (lower_inclusive and upper_inclusive)))
    return {
        "status": ("incomplete" if unsupported_ids else "complete"
                   if lower is not None or upper is not None else "no_constraints"),
        "coordinate": ({"calendar": coordinate[0], "year_system": coordinate[1],
                        "precision": coordinate[2], "era_id": coordinate[3]}
                       if coordinate is not None else None),
        "earliest": ({"year": lower, "inclusive": lower_inclusive, "constraint_ids": lower_ids}
                     if lower is not None else None),
        "latest": ({"year": upper, "inclusive": upper_inclusive, "constraint_ids": upper_ids}
                   if upper is not None else None),
        "conflict": conflict,
        "unsupported_constraint_ids": unsupported_ids,
    }
