


# Builds
venv:
	test -d venv || (mkdir venv; python3 -m venv "venv")
	. venv/bin/activate;
	touch venv/touchfile

install: venv
	pip install -Ur requirements.txt

build: install

run: venv
	python rcv/manage.py runserver