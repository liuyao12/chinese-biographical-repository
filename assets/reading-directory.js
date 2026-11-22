const compact = window.matchMedia('(max-width:800px)');
const directory = document.getElementById('chapter-directory');
let reading = false;

function sizeDirectory() {
  directory.open = !compact.matches || !reading;
}

compact.addEventListener('change', sizeDirectory);

export function setReadingDirectory(hasSelection) {
  reading = hasSelection;
  sizeDirectory();
  const switcher = document.querySelector('.work-switch');
  if (switcher) switcher.open = false;
}
