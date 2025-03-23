.PHONY: test test-db test-run test-down

test-db:
	docker-compose -f ../docker-compose.test.yml up -d
	sleep 3

test-run:
	ENV_TYPE=testing PYTHONPATH=$(shell dirname $(shell pwd)) poetry run alembic upgrade head
	ENV_TYPE=testing poetry run pytest

test-down:
	docker-compose -f ../docker-compose.test.yml down

test: test-db
	@$(MAKE) test-run; status=$$?; $(MAKE) test-down; exit $$status