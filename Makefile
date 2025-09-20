# ====================================================================================
#
#   Wake up... The Matrix-Hub has you.
#   This Makefile is the construct program for your project.
#   Run `make help` to see available commands.
#
# ====================================================================================

# // ---[ System & Environment ]--- //
.DEFAULT_GOAL := help
SHELL := /usr/bin/env bash
.PHONY: all help setup install install-bff install-ui run-bff dev-ui build-ui build-lib publish-testpypi publish-pypi docs-install docs-build docs-serve docs-deploy docker-build-bff docker-build-ui docker-push-bff docker-push-ui ce-create-bff ce-update-bff ce-create-ui ce-create-secrets doctor clean

# // ---[ Variables ]--- //
VENV := .venv
PYTHON := $(VENV)/bin/python

# Docker & Cloud Engine
REGISTRY ?= us.icr.io
NAMESPACE ?= <namespace>
IMAGE_TAG ?= latest

# Terminal Colors
BRIGHT_GREEN := $(shell tput -T screen setaf 10)
DIM_GREEN := $(shell tput -T screen setaf 2)
RESET := $(shell tput -T screen sgr0)

# // ---[ Core Workflow ]--- //

help: ## 🐇 Follow the white rabbit (show this help message)
	@echo
	@echo "$(BRIGHT_GREEN)TRANSMISSION INCOMING... ACCESSING CONSTRUCT PROGRAMS...$(RESET)"
	@echo "Usage: make <program>"
	@echo
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z0-9_-]+:.*?## / {printf "  $(BRIGHT_GREEN)%-24s$(RESET) $(DIM_GREEN)%s$(RESET)\n", $$1, $$2}' $(MAKEFILE_LIST)
	@echo

setup: $(VENV)/bin/activate ## 🔌 Jack into the main construct (.venv)
$(VENV)/bin/activate:
	@echo "$(DIM_GREEN)-> Constructing main virtual environment...$(RESET)"
	python3 -m venv $(VENV)
	$(PYTHON) -m pip install --no-cache-dir --upgrade pip setuptools wheel

install: setup install-bff install-ui docs-install ## 💉 Load all required programs and constructs
	@echo "$(BRIGHT_GREEN)--> All systems loaded. You know kung fu.$(RESET)"

clean: ## 🧹 Unplug and erase all local constructs
	@echo "$(DIM_GREEN)-> Purging constructs and unplugging from the Matrix...$(RESET)"
	rm -rf $(VENV) apps/bff/.venv ui/matrixhub-admin/node_modules
	rm -rf libs/matrixlink/dist libs/matrixlink/*.egg-info site
	find . -type d -name "__pycache__" -exec rm -rf {} +
	@echo "$(BRIGHT_GREEN)--> System clean. The line is clear.$(RESET)"

# // ---[ Service Installation & Execution ]--- //

install-bff: setup ## 📲 Install the Backend-for-Frontend program
	@echo "$(DIM_GREEN)-> Loading BFF sub-construct and dependencies...$(RESET)"
	cd apps/bff && \
		python3 -m venv .venv && \
		. .venv/bin/activate && \
		pip install --no-cache-dir -r requirements.txt && \
		pip install --no-cache-dir -e ../../libs/matrixlink

install-ui: ## 🧩 Prepare Admin UI dependencies
	@echo "$(DIM_GREEN)-> Installing UI dependencies...$(RESET)"
	cd ui/matrixhub-admin && npm ci --no-fund --no-audit

run-bff: ## ▶️ Run the core BFF program (foreground)
	@echo "$(BRIGHT_GREEN)-> Engaging BFF program... broadcasting on port 8080 (press CTRL+C to stop)...$(RESET)"
	cd apps/bff && . .venv/bin/activate && \
		export CLOUD_PROVIDER=local && \
		export MCP_BASE_URL=$${MCP_BASE_URL:-http://localhost:4444} && \
		uvicorn app.main:app --host 0.0.0.0 --port 8080

dev-ui: ## 👁️ Run the Admin UI in dev mode (foreground)
	@echo "$(BRIGHT_GREEN)-> UI surveillance active on port 3000 (press CTRL+C to stop)...$(RESET)"
	cd ui/matrixhub-admin && npm run dev

# // ---[ Build & Publish ]--- //

build-ui: install-ui ## 🏗️ Compile the Admin UI static image
	@echo "$(DIM_GREEN)-> Compiling static UI construct...$(RESET)"
	cd ui/matrixhub-admin && npm run build

build-lib: setup ## 📦 Package the MatrixLink construct (library)
	@echo "$(DIM_GREEN)-> Packaging the MatrixLink construct for distribution...$(RESET)"
	cd libs/matrixlink && $(PYTHON) -m pip install --no-cache-dir --upgrade build && $(PYTHON) -m build

publish-testpypi: build-lib ## 📡 Broadcast MatrixLink to the test network (TestPyPI)
	@echo "$(DIM_GREEN)-> Broadcasting construct to TestPyPI training network...$(RESET)"
	cd libs/matrixlink && $(PYTHON) -m pip install --no-cache-dir --upgrade twine && \
		$(PYTHON) -m twine upload --repository-url https://test.pypi.org/legacy/ dist/*

publish-pypi: build-lib ## 📡 Broadcast MatrixLink to the public network (PyPI)
	@echo "$(BRIGHT_GREEN)-> Broadcasting construct to Zion Mainframe (PyPI)...$(RESET)"
	cd libs/matrixlink && $(PYTHON) -m pip install --no-cache-dir --upgrade twine && \
		$(PYTHON) -m twine upload dist/*

# // ---[ Documentation ]--- //

docs-install: setup ## 📚 Load the Architect's tools (MkDocs)
	@echo "$(DIM_GREEN)-> Loading Architect's blueprint tools...$(RESET)"
	$(PYTHON) -m pip install --no-cache-dir mkdocs mkdocs-material

docs-build: docs-install ## 📑 Compile the Architect's records
	@echo "$(DIM_GREEN)-> Compiling Architect's blueprints into static site...$(RESET)"
	$(PYTHON) -m mkdocs build -f mkdocs.yml --strict

docs-serve: docs-install ## 📜 View the Architect's blueprints live
	@echo "$(BRIGHT_GREEN)-> Accessing blueprints... live feed at http://localhost:8000$(RESET)"
	@$(PYTHON) -m mkdocs serve -f mkdocs.yml

docs-deploy: docs-build ## 🌍 Publish blueprints to the public consciousness (GitHub Pages)
	@echo "$(BRIGHT_GREEN)-> Broadcasting blueprints to the global network...$(RESET)"
	@$(PYTHON) -m mkdocs gh-deploy -f mkdocs.yml --force

# // ---[ Containerization & Deployment ]--- //

docker-build-bff: ## 📦 Encapsulate BFF in a transport pod (Docker image)
	@echo "$(DIM_GREEN)-> Building pod for BFF program...$(RESET)"
	docker build -f apps/bff/Dockerfile -t $(REGISTRY)/$(NAMESPACE)/bff:$(IMAGE_TAG) .

docker-build-ui: build-ui ## 📦 Encapsulate UI in a transport pod (Docker image)
	@echo "$(DIM_GREEN)-> Building pod for UI program...$(RESET)"
	docker build -f ui/matrixhub-admin/Dockerfile -t $(REGISTRY)/$(NAMESPACE)/matrixhub-admin:$(IMAGE_TAG) ui/matrixhub-admin

docker-push-bff: ## 🚢 Send BFF pod to the docking bay (registry)
	@echo "$(BRIGHT_GREEN)-> Transmitting BFF pod to $(REGISTRY)...$(RESET)"
	docker push $(REGISTRY)/$(NAMESPACE)/bff:$(IMAGE_TAG)

docker-push-ui: ## 🚢 Send UI pod to the docking bay (registry)
	@echo "$(BRIGHT_GREEN)-> Transmitting UI pod to $(REGISTRY)...$(RESET)"
	docker push $(REGISTRY)/$(NAMESPACE)/matrixhub-admin:$(IMAGE_TAG)

ce-create-bff: ## 🚀 Launch BFF program into the Code Engine mainframe
	@echo "$(BRIGHT_GREEN)-> Launching BFF program into the CE Mainframe...$(RESET)"
	REGISTRY=$(REGISTRY) NAMESPACE=$(NAMESPACE) TAG=$(IMAGE_TAG) ./infra/ce/bff-app-create.sh

ce-update-bff: ## ✨ Upgrade the live BFF program image
	@echo "$(BRIGHT_GREEN)-> Upgrading live BFF instance in the CE Mainframe...$(RESET)"
	REGISTRY=$(REGISTRY) NAMESPACE=$(NAMESPACE) TAG=$(IMAGE_TAG) ./infra/ce/bff-app-update.sh

ce-create-ui: ## 🚀 Launch Admin UI into the Code Engine mainframe
	@echo "$(BRIGHT_GREEN)-> Launching Admin UI into the CE Mainframe...$(RESET)"
	REGISTRY=$(REGISTRY) NAMESPACE=$(NAMESPACE) TAG=$(IMAGE_TAG) ./infra/ce/admin-ui-create.sh

ce-create-secrets: ## 🔑 Inject secret codes into the mainframe
	@echo "$(DIM_GREEN)-> Injecting operator secrets into the CE Mainframe...$(RESET)"
	./infra/secrets/create-secrets.sh

# // ---[ Diagnostics ]--- //

doctor: ## 🩺 Print toolchain versions (quick diagnostics)
	@echo "$(BRIGHT_GREEN)--- System Diagnostics ---$(RESET)"
	@echo "Python 3:"
	@which python3 && python3 --version
	@echo "\nNode:"
	@which node && node --version
	@echo "\nNPM:"
	@which npm && npm --version
	@echo "\nProject Virtualenv ($(VENV)):"
	@if [ -x "$(PYTHON)" ]; then $(PYTHON) --version; else echo "Not found."; fi