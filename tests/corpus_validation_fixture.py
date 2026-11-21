"""Copy source data used by tests that run the complete corpus validator."""

import shutil


def copy_validation_inputs(source, destination):
    for name in ('registry', 'corpus', 'sources', 'source-evidence',
                 'data/historical-tables', 'data/works'):
        shutil.copytree(source / name, destination / name)

    (destination / 'data/corpus').mkdir(parents=True)
    for name in ('profile-names.json', 'chapter-directory.json'):
        shutil.copy2(source / 'data/corpus' / name, destination / 'data/corpus' / name)
