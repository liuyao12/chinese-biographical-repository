const p = new URLSearchParams(location.hash.slice(1));
const number = p.get('table') === 'shiji-015' ? 15 : 14;
p.set('chapter', String(number)); p.set('category', 'biao');
location.replace('shiji.html#' + p);
