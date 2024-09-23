PACKAGE = opcdiag

.PHONY: accept clean coverage readme register test sdist upload

help:
	@echo "Please use \`make <target>' where <target> is one or more of"
	@echo "  accept      run acceptance tests using behave"
	@echo "  build       generate a source distribution and wheel into dist/"
	@echo "  clean       delete intermediate work product and start fresh"
	@echo "  cleandocs   delete generated HTML documentation"
	@echo "  coverage    run unit tests with coverage"
	@echo "  docs        generate HTML documentation with Sphinx"
	@echo "  test        run unit tests"
	@echo "  test-upload upload distribution artifacts in dist/ to Test-PyPI"
	@echo "  upload      upload distribution artifacts in dist/ to PyPI"

.PHONY: accept
accept:
	uv run behave --stop

.PHONY: build
build:
	rm -rf dist
	uv build

.PHONY: clean
clean:
	find . -type f -name \*.pyc -exec rm {} \;
	rm -rf dist *.egg-info .coverage .DS_Store

.PHONY: cleandocs
cleandocs:
	$(MAKE) -C docs clean

.PHONY: coverage
coverage:
	uv run pytest --cov-report term-missing --cov=$(PACKAGE) --cov=tests tests/

.PHONY: docs
docs:
	$(MAKE) -C docs html

.PHONY: test
test:
	uv run pytest tests

.PHONY: test-upload
test-upload: build
	uv run twine upload --repository testpypi dist/*

.PHONY: upload
upload:
	uv run twine upload dist/*
