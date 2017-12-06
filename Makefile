build: init
	python3 setup.py build

init:
	pip install -r requirements.txt

install:
	python3 setup.py install

.PHONY: build init install
