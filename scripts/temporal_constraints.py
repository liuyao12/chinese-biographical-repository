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
    if "era_id" in value and (not isinstance(value["era_id"], str) or not value["era_id"]):
        errors.append(f"{label}.era_id須為非空字串")
    return errors


def _coordinate(value):
    return tuple(value.get(k) for k in ("calendar", "year_system", "precision", "era_id"))


def errors(records, chapters, person_ids):
    """Validate every temporal constraint against event, person, passage and mention records."""
    errors = []
    pids = set(person_ids)
    events = {}
    for record in records:
        if record.get("record_type") in ("person_life_event_assertion_set", "table_person_life_event_assertion_set", "person_event_assertion_set"):
            for event in record.get("events", []):
                events[event.get("id")] = event
    seen = set()
    paragraph_index = {
        paragraph.get("id"): (chapter, paragraph)
        for chapter in chapters.values()
        for paragraph in chapter.get("paragraphs", [])
    }
    for record in records:
        if record.get("record_type") != "temporal_constraint_set":
            continue
        root_chapter = chapters.get(record.get("chapter_id"))
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
            if person_id not in pids:
                errors.append(f"日期約束人物 ID 不存在：{cid}")
            target_id = item.get("target_event_id")
            target = events.get(target_id)
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
                        or derivation.get("input_event_id") not in events):
                    errors.append(f"衍生日期約束須引用已登記規則及輸入事件：{cid}")
                elif events[derivation["input_event_id"]].get("person_id") != person_id:
                    errors.append(f"日期約束輸入事件人物不符：{cid}")
            elif derivation is not None:
                errors.append(f"直接日期約束不得附 derivation：{cid}")
            if operator in ("equals", "not_before", "not_after"):
                if "interval" in item or "related_event_id" in item:
                    errors.append(f"日期約束欄位與運算子不符：{cid}")
                errors.extend(_date_errors(item.get("bound"), f"{cid}.bound"))
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
                if related_id not in events or any(k in item for k in ("bound", "interval")):
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
                mention = next((m for m in paragraph.get("mentions", []) if m.get("id") == mention_id), None)
                if (mention is None or mention.get("person_id") != person_id
                        or not any(i <= mention.get("start", -1) and mention.get("end", 0) <= i + len(quote)
                                   for i in range(len(paragraph.get("text", "")))
                                   if paragraph["text"].startswith(quote, i))):
                    errors.append(f"日期約束人物錨點不在引文內：{cid}")
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
    for item in constraints:
        op = item.get("operator")
        if op not in ("equals", "within_interval", "not_before", "not_after"):
            raise ValueError("僅能交集絕對日期界限")
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
        "coordinate": ({"calendar": coordinate[0], "year_system": coordinate[1],
                        "precision": coordinate[2], "era_id": coordinate[3]}
                       if coordinate is not None else None),
        "earliest": ({"year": lower, "inclusive": lower_inclusive, "constraint_ids": lower_ids}
                     if lower is not None else None),
        "latest": ({"year": upper, "inclusive": upper_inclusive, "constraint_ids": upper_ids}
                   if upper is not None else None),
        "conflict": conflict,
    }
