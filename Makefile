#! /usr/bin/make

default: all
.PHONY: default


lint: requirements
	pycodestyle *.py
.PHONY: lint

requirements:
	pip install -r requirements.txt

test: requirements
	python tests.py
.PHONY: test


all: requirements lint test
.PHONY: all