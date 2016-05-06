install:
	@pip install -e .
	@pip install -r requirements-dev.txt

test: testclean
	@py.test -s -x --cov=. --cov-report term-missing --verbose --durations=5 #--pep8

testclean:
	@rm -Rf photorenamer/test/__pycache__
	@rm -Rf .cache
	@rm -f .coverage
