help:
	@echo 'Make for some simple commands            '
	@echo '                                         '
	@echo ' Usage:                                  '
	@echo '     make lint    flake8 the codebase    '
	@echo '     make test    run unit tests         '

lint:
	flake8 ./erc

test:
	pytest erc/tests -v --cov=erc --cov-report term-missing
