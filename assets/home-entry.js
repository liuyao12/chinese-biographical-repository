/** Keep existing hash-addressed ECCP links while making the bare URL a library entrance. */
let installed = false;
async function open() {
  const home = !location.hash;
  document.body.classList.toggle('library-home', home);
  document.getElementById('home-library').hidden = !home;
  document.getElementById('workspace').hidden = home;
  document.querySelector('.context-bar').hidden = home;
  if (home) import('./home-catalog.js').then(m => m.loadHomeCatalog()).catch(console.error);
  if (!home && !installed) {
    installed = true;
    await Promise.all([
      import('./app.js'), import('./person-links.js'), import('./reader-context.js'),
      import('./entity-hover.js'), import('./text-unit-links.js')
    ]);
  }
}
window.addEventListener('hashchange', () => open().catch(console.error));
open().catch(console.error);
