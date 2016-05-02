PIP=venv/bin/pip
PYTHON=venv/bin/python
PYTEST=venv/bin/py.test

venv: venv/bin/activate

venv/bin/activate: requirements.txt
	test -d venv || virtualenv venv
	venv/bin/pip install -Ur requirements.txt
	touch venv/bin/activate

devbuild: venv
	${PIP} install --editable .

test: venv
	${PYTEST} tests
