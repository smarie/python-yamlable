# yamlable

*Convert Python objects to YAML and back.*

[![Build Status](https://travis-ci.org/smarie/python-yamlable.svg?branch=master)](https://travis-ci.org/smarie/python-yamlable) [![Tests Status](https://smarie.github.io/python-yamlable/junit/junit-badge.svg?dummy=8484744)](https://smarie.github.io/python-yamlable/junit/report.html) [![codecov](https://codecov.io/gh/smarie/python-yamlable/branch/master/graph/badge.svg)](https://codecov.io/gh/smarie/python-yamlable) [![Documentation](https://img.shields.io/badge/docs-latest-blue.svg)](https://smarie.github.io/python-yamlable/) [![PyPI](https://img.shields.io/badge/PyPI-yamlable-blue.svg)](https://pypi.python.org/pypi/yamlable/)

**This is the readme for developers.** The documentation for users is available here: [https://smarie.github.io/python-yamlable/](https://smarie.github.io/python-yamlable/)

## Want to contribute ?

Contributions are welcome ! Simply fork this project on github, commit your contributions, and create pull requests.

Here is a non-exhaustive list of interesting open topics: [https://github.com/smarie/python-yamlable/issues](https://github.com/smarie/python-yamlable/issues)

## Running the tests

This project uses `pytest`.

```bash
pytest -v yamlable/tests/
```

You may need to install requirements for setup beforehand, using 

```bash
pip install -r ci_tools/requirements-test.txt
```

## Packaging

This project uses `setuptools_scm` to synchronise the version number. Therefore the following command should be used for development snapshots as well as official releases: 

```bash
python setup.py egg_info bdist_wheel rotate -m.whl -k3
```

You need to [generate code](##building-from-sources--notes-on-this-projects-design-principles) before packaging.

You also may need to install requirements for setup beforehand, using 

```bash
pip install -r ci_tools/requirements-setup.txt
```

## Generating the documentation page

This project uses `mkdocs` to generate its documentation page. Therefore building a local copy of the doc page may be done using:

```bash
mkdocs build
```

You may need to install requirements for doc beforehand, using 

```bash
pip install -r ci_tools/requirements-doc.txt
```

## Generating the test reports

The following commands generate the html test report and the associated badge. 

```bash
pytest --junitxml=junit.xml -v yamlable/tests/
ant -f ci_tools/generate-junit-html.xml
python ci_tools/generate-junit-badge.py
```

### PyPI Releasing memo

This project is now automatically deployed to PyPI when a tag is created. Anyway, for manual deployment we can use:

```bash
twine upload dist/* -r pypitest
twine upload dist/*
```
