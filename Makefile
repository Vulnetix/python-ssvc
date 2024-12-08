SHELL := /bin/bash
.PHONY: help

help: ## This help.
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

.DEFAULT_GOAL := help

SEMGREP_ARGS=--use-git-ignore --metrics=off --force-color --disable-version-check --experimental --dataflow-traces --sarif --timeout=0
SEMGREP_RULES=-c p/default -c p/python -c p/php -c p/c -c p/rust -c p/apex -c p/nginx -c p/terraform -c p/csharp -c p/nextjs -c p/golang -c p/nodejs -c p/kotlin -c p/django -c p/docker -c p/kubernetes -c p/lockfiles -c p/supply-chain -c p/headless-browser -c p/expressjs -c p/cpp-audit -c p/mobsfscan -c p/ruby -c p/java -c p/javascript -c p/typescript -c p/bandit -c p/flask -c p/gosec -c p/flawfinder -c p/gitleaks -c p/eslint -c p/phpcs-security-audit -c p/react -c p/brakeman -c p/findsecbugs -c p/secrets -c p/sql-injection -c p/jwt -c p/insecure-transport -c p/command-injection -c p/security-code-scan -c p/xss

clean: ## Cleanup tmp files
	@find . -type f -name '*.pyc' -delete 2>/dev/null
	@find . -type d -name '__pycache__' -delete 2>/dev/null
	@find . -type f -name '*.DS_Store' -delete 2>/dev/null

setup: ## FOR DOCO ONLY - Run these one at a time, do not call this target directly
	uv python install
	uv venv
	source .venv/bin/activate	
	uv sync
	uv build
	uv pip install dist/ssvc-*-py3-none-any.whl
	uv pip install "."

update: ## update and lock
	uv lock -U

test: clean ## pytest with coverage
	uv pip install ".[test]"
	uv run coverage run -m pytest --nf
	uv run coverage report -m --fail-under=100
	uv run coverage-badge -f -o coverage.svg

publish: clean ## upload to pypi.org
	@rm -rf dist build 2>/dev/null
	uv build
	uv publish
	git commit -a -s -m 'feat: $(shell uv tree -q | head -1 | awk '{print $2}')'
	git tag --force $(shell uv tree -q | head -1 | awk '{print $2}')
	git push
	git push --tags --force

sarif: clean ## generate SARIF from Semgrep for this project
	osv-scanner --format sarif --call-analysis=all -r . | jq >osv.sarif.json
	semgrep $(SEMGREP_ARGS) $(SEMGREP_RULES) | jq >semgrep.sarif.json

sbom: ## generate CycloneDX for this project
	uv pip install ".[sec]"
	uv run pip-audit -f cyclonedx-json | jq > ssvc.cdx.json
