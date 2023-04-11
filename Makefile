PY = python3

main: 
	$(PY) -m code.main

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

test_cache:
	${PY} -m test.test_cache

test_cache_processor:
	${PY} -m test.integration.cache_processor

