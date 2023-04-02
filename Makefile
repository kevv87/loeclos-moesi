PY = python3

default: test_all

test_all:
	$(PY) -m test.test

test_processors:
	${PY} -m test.test_processors

test_memory:
	${PY} -m test.test_memory

test_bus:
	${PY} -m test.test_bus

test_observer:
	${PY} -m test.test_observer

