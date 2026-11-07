"""Literal quotation boundaries for opt-in narrative-only source spans."""


def unquoted_span(text, start, end):
    """Check brackets from the paragraph start, including already-open speech."""
    if (not isinstance(text, str) or type(start) is not int or type(end) is not int
            or not 0 <= start < end <= len(text)):
        return False
    pairs = {'「': '」', '『': '』', '“': '”', '‘': '’'}
    closes = set(pairs.values())
    stack = []
    for i, character in enumerate(text[:end]):
        if i == start and stack:
            return False
        if character in pairs:
            if i >= start:
                return False
            stack.append(pairs[character])
        elif character in closes:
            if not stack or stack.pop() != character or i >= start:
                return False
    return not stack
