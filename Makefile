CONFIG_PATH ?= config.json
image := defyes
path := defyes tests
repo_dir := $(shell git rev-parse --show-toplevel)
docker_base_run := docker run --rm -i \
  -v $(PWD):/repo \
  -v $(PWD)/.tmp:/tmp \
  -v /home/fito/laburo/karpatkey/src/karpatkit/src/karpatkit:/usr/local/lib/python3.10/site-packages/karpatkit -v /home/fito/laburo/karpatkey/src/karpatkit/src/defabipedia:/usr/local/lib/python3.10/site-packages/defabipedia \
  -e HOME=/repo/.home \
  -e KKIT_CACHE_ENABLE=$(KKIT_CACHE_ENABLE) \
  -e KKIT_CACHE_CLEAR=$(KKIT_CACHE_CLEAR) \
  -e CONFIG_PATH=$(CONFIG_PATH)
docker_root_run := $(docker_base_run) -e USER=root
docker_user_run := $(docker_base_run) -e USER=$(USER) --user $$(id -u):$$(id -g)



.PHONY: install-pre-commit
install-pre-commit: build
	@cp $(repo_dir)/.pre-commit $(repo_dir)/.git/hooks/pre-commit
	@echo "The pre-commit hook has been installed."


.PHONY: build
build:
	@docker build -t $(image) .


.PHONY: build-if-no-image
build-if-no-image:
	@docker inspect --type=image $(image) > /dev/null || docker build -t $(image) .


.PHONY: shell
shell: build-if-no-image
	@$(docker_user_run) -t $(image) bash


.PHONY: rootshell
rootshell: build-if-no-image
	@$(docker_root_run) -t $(image) bash


.PHONY: test
test: build-if-no-image
	@$(docker_user_run) $(image) pytest -v


.PHONY: lint-black
lint-black: build-if-no-image
	@echo "Check black..."
	@echo "=============="
	@$(docker_user_run) $(image) black --fast --check $(path)


.PHONY: lint-isort
lint-isort: build-if-no-image
	@echo "Check isort..."
	@echo "=============="
	@$(docker_user_run) $(image) isort --check $(path)


.PHONY: lint-flake8
lint-flake8: build-if-no-image
	@echo "Check flake8..."
	@echo "==============="
	@$(docker_user_run) $(image) flake8 $(path)


.PHONY: lint
lint: lint-black lint-isort lint-flake8
	@echo "Linter rules [OK]"


.PHONY: black
black: build-if-no-image  ## Apply black.
	@echo
	@echo "Applying black..."
	@echo "================="
	@echo
	@$(docker_user_run) $(image) black --fast $(path)
	@echo


.PHONY: isort
isort: build-if-no-image  ## Apply isort.
	@echo "Applying isort..."
	@echo "================="
	@echo
	@$(docker_user_run) $(image) isort $(path)


.PHONY: pretty
pretty: isort black


.PHONY: autogenerate
autogenerate: build-if-no-image
	@$(docker_user_run) -t $(image) python -m defyes.generator


.PHONY: cacheclear
cacheclear: build-if-no-image
	@echo "Clearing the API requests cache..."
	@echo "=================================="
	@echo
	@$(docker_user_run) $(image) python -c "import karpatkit.cache as c; c.clear()"
