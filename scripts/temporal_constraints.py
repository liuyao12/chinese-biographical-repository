"""來源日期約束的結構驗證與年份交集；不執行自然語言判讀。"""
from __future__ import annotations

_DATE_KEYS = {"calendar", "year_system", "precision", "year", "inclusive"}
_DATE_OPTIONAL = {"month", "day", "era_id"}
_OPERATORS = {"equals", "within_interval", "not_before", "not_after", "after_event", "not_before_event"}
_RULES = {"person_alive_at_event_implies_death_not_before"}


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


def _quote_contains_mention(paragraph, quote, mention_id, person_id):
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
    return any(i <= start and end <= i + len(quote)
               for i in range(len(text)) if text.startswith(quote, i))


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
                if (not isinstance(derivation, dict)
                        or derivation.get("rule_id") not in _RULES
                        or not isinstance(derivation.get("input_event_id"), str)
                        or derivation.get("input_event_id") not in events):
                    errors.append(f"衍生日期約束須引用已登記規則及輸入事件：{cid}")
                else:
                    input_id = derivation["input_event_id"]
                    input_event = events[input_id]
                    if input_event.get("person_id") != person_id:
                        errors.append(f"日期約束輸入事件人物不符：{cid}")
                    if operator != "not_before" or target is None or target.get("event_type") != "death":
                        errors.append(f"在世推導規則僅能產生同一人物的死亡下界：{cid}")
                    if (input_id == target_id or input_event.get("event_type") != "visit"
                            or input_event.get("participant_role") != "visited_person"
                            or not input_event.get("date_expression")
                            or not (input_event.get("normalized_date") or input_event.get("normalized_date_range"))):
                        errors.append(f"在世推導須使用有日期的被訪者事件且不得自我引用：{cid}")
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
                if not isinstance(related_id, str) or related_id not in events or any(k in item for k in ("bound", "interval")):
                    errors.append(f"相對事件約束缺少有效 related_event_id 或含有多餘界限：{cid}")
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
                if not isinstance(quote, str) or not quote or quote not in paragraph.get("text", ""):
                    errors.append(f"日期約束引文不在原段中：{cid}")
                    continue
                if not _quote_contains_mention(paragraph, quote, mention_id, person_id):
                    errors.append(f"日期約束人物錨點不在引文內：{cid}")
                errors.extend(f"{message}：{cid}" for message in _temporal_claim_errors(citation, item))
                if mode == "derived" and isinstance(derivation, dict):
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


def intersect_year_constraints(constraints):
    """Intersect year-only absolute bounds with identical calendar coordinates.

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
