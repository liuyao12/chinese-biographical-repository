/** Preserve disclosure and reading position when the same chapter changes UI language. */
export function captureReadingState(root, viewport = globalThis.window) {
  const nodes = [...root.querySelectorAll('details')].filter(node => !node.closest?.('.table-person-card'));
  const chapterId = root.querySelector('article.corpus-text')?.dataset.chapterId;
  if (!chapterId) return null;
  const scrollX = Number.isFinite(viewport?.scrollX) ? viewport.scrollX : 0;
  const scrollY = Number.isFinite(viewport?.scrollY) ? viewport.scrollY : 0;
  const state = {chapterId, openDetails: nodes.map(n => n.open), scrollX, scrollY};
  if (scrollY > 0) {
    for (const node of root.querySelectorAll('[data-source-text], [data-interpretation-id]')) {
      if (node.closest?.('.table-person-card')) continue;
      const rect = node.getBoundingClientRect();
      if (rect.top <= 0 && rect.bottom > 0) {
        state.anchor = node.hasAttribute('data-interpretation-id')
          ? {kind: 'referent', key: node.dataset.interpretationId, top: rect.top}
          : {kind: 'paragraph', key: node.id, top: rect.top};
        break;
      }
    }
  }
  return state;
}
export function restoreReadingState(root, state, viewport = globalThis.window) {
  if (!state || root.querySelector('article.corpus-text')?.dataset.chapterId !== state.chapterId) return;
  const nodes = [...root.querySelectorAll('details')].filter(node => !node.closest?.('.table-person-card'));
  if (nodes.length === state.openDetails.length) nodes.forEach((node, i) => { node.open = state.openDetails[i]; });
  let targetY = state.scrollY;
  if (state.anchor) {
    const selector = state.anchor.kind === 'referent' ? '[data-interpretation-id]' : '[data-source-text]';
    const anchor = [...root.querySelectorAll(selector)].find(node =>
      (state.anchor.kind === 'referent' ? node.dataset.interpretationId : node.id) === state.anchor.key);
    if (anchor) targetY = (viewport?.scrollY || 0) + anchor.getBoundingClientRect().top - state.anchor.top;
  }
  viewport?.scrollTo(state.scrollX, targetY);
}

/** Capture before translated chrome reflows; only the matching render may consume it. */
export function createLanguageReadingTransition(getRoot, getContext) {
  let pending = null, active = null;
  return {
    before() {
      const context = getContext();
      const state = active?.ticket === context.ticket && active.hash === context.hash
        ? active.state : captureReadingState(getRoot());
      pending = {...context, state};
    },
    start(keep, current) {
      const saved = pending, context = getContext();
      pending = null; active = null;
      if (!keep) return null;
      const state = saved
        ? (saved.ticket === current - 1 && saved.hash === context.hash ? saved.state : null)
        : captureReadingState(getRoot());
      if (state) active = {ticket:current, hash:context.hash, state};
      return state;
    },
    finish(current) { if (active?.ticket === current) active = null; }
  };
}
