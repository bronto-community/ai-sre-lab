# Operating the Storefront. Nothing here is visible to the agent: it reads
# telemetry and the storefront repo, never this directory.
SHELL := /bin/bash
REPO ?= ../storefront
SHAS := $(shell cat ../.storefront-shas 2>/dev/null)
GOOD_SHA := $(word 2,$(subst =, ,$(word 1,$(SHAS))))
BAD_SHA  := $(word 2,$(subst =, ,$(word 2,$(SHAS))))

COMPOSE := docker compose --env-file .env --env-file .deploy-state

.PHONY: up down logs status traces deploy release rollback psp-slow heal shas

up: .deploy  ## bring the platform up on the current good release
	@$(COMPOSE) up -d --build collector psp
	@$(MAKE) --no-print-directory deploy SHA=$(GOOD_SHA) VERSION=3.1.0 SERVICES="web checkout payments catalog"
	@$(COMPOSE) up -d --build loadgen
	@echo
	@echo "Storefront is up on $(GOOD_SHA) (v3.1.0)."
	@echo "Leave it ~10 minutes before doing anything else: an investigator"
	@echo "with no baseline has nothing to compare against."

.deploy:
	@git clone -q $(REPO) .deploy
	@touch .env .deploy-state

# Deploy a commit. This is the only mechanism -- there is no 'break it' switch,
# because a deploy of a real commit is what actually happens.
deploy: .deploy
	@git -C .deploy fetch -q origin && git -C .deploy checkout -q $(SHA)
	@printf 'GIT_COMMIT=%s\nCHECKOUT_VERSION=%s\n' "$(SHA)" "$(VERSION)" > .deploy-state
	@$(COMPOSE) up -d --build --no-deps $(SERVICES)
	@echo "deployed $(SHA) ($(VERSION)) to: $(SERVICES)"

release:  ## ship the latest release of checkout-api
	@$(MAKE) --no-print-directory deploy SHA=$(BAD_SHA) VERSION=3.2.0 SERVICES=checkout
	@echo "Symptoms take ~60s to appear in p95."

rollback heal:  ## put checkout-api back on the previous release
	@$(MAKE) --no-print-directory deploy SHA=$(GOOD_SHA) VERSION=3.1.0 SERVICES=checkout

psp-slow:  ## the third-party processor degrades
	@PSP_LATENCY_MS=1500 $(COMPOSE) up -d --force-recreate --no-deps psp
	@echo "The PSP is slow now. Nothing in your telemetry will say so."

psp-ok:
	@$(COMPOSE) up -d --force-recreate --no-deps psp

status:  ## what the customer is experiencing
	@$(COMPOSE) logs --tail 6 loadgen

traces:  ## raw telemetry, if no backend is wired up
	@$(COMPOSE) logs --tail 40 collector

shas:
	@cat ../.storefront-shas

down:
	docker compose down -v; rm -rf .deploy .deploy-state

logs:
	$(COMPOSE) logs -f
