PY = python3

default: test_all

test_all:
	$(PY) -m test.test

test_processors:
	${PY} -m test.test_processors

test_memory:
	${PY} -m test.test_memory
