#!/usr/bin/env -S just --justfile

# Set shell to bash
set shell := ["/bin/bash", "-c"]

# Semgrep configuration variables
SEMGREP_ARGS := "--use-git-ignore --metrics=off --force-color --disable-version-check --experimental --dataflow-traces --sarif --timeout=0"
SEMGREP_RULES := "-c p/default -c p/python -c p/php -c p/c -c p/rust -c p/apex -c p/nginx -c p/terraform -c p/csharp -c p/nextjs -c p/golang -c p/nodejs -c p/kotlin -c p/django -c p/docker -c p/kubernetes -c p/lockfiles -c p/supply-chain -c p/headless-browser -c p/expressjs -c p/cpp-audit -c p/mobsfscan -c p/ruby -c p/java -c p/javascript -c p/typescript -c p/bandit -c p/flask -c p/gosec -c p/flawfinder -c p/gitleaks -c p/eslint -c p/phpcs-security-audit -c p/react -c p/brakeman -c p/findsecbugs -c p/secrets -c p/sql-injection -c p/jwt -c p/insecure-transport -c p/command-injection -c p/security-code-scan -c p/xss"

# Show available recipes (default recipe)
default:
    @just --list --unsorted

# Cleanup tmp files
clean:
    @find . -type f -name '*.pyc' -delete 2>/dev/null || true
    @find . -type d -name '__pycache__' -delete 2>/dev/null || true
    @find . -type f -name '*.DS_Store' -delete 2>/dev/null || true

# FOR DOCO ONLY - Run these one at a time, do not call this recipe directly
setup:
    @echo "FOR DOCO ONLY - Run these one at a time, do not call this recipe directly:"
    @echo "  uv python install"
    @echo "  uv venv"
    @echo "  source .venv/bin/activate"
    @echo "  uv sync"
    @echo "  uv build"
    @echo "  uv pip install dist/ssvc-*-py3-none-any.whl"
    @echo "  uv pip install \".\""

# Upload to PyPI
publish: clean
    @rm -rf dist build 2>/dev/null || true
    uv build
    uv publish
    git commit -a -s -m "feat: $(uv tree -q | head -1 | awk '{print $2}')"
    git tag --force "$(uv tree -q | head -1 | awk '{print $2}')"
    git push
    git push --tags --force

# Get app updates
update:
    uv lock -U

# Install dependencies
install:
    uv sync

# Generate SARIF from Semgrep and OSV Scanner for this project
sarif: clean
    osv-scanner --format sarif --call-analysis=all -r . | jq >osv.sarif.json
    semgrep {{SEMGREP_ARGS}} {{SEMGREP_RULES}} | jq >semgrep.sarif.json

# Generate CycloneDX SBOM from pip-audit for this project
sbom: clean
    uv pip install ".[sec]"
    uv run pip-audit -f cyclonedx-json | jq >ssvc.cdx.json

# Show current package version
version:
    @uv tree -q | head -1 | awk '{print $2}'

# Run tests with coverage
test: clean
    uv pip install ".[test]"
    uv run coverage run -m pytest --nf
    uv run coverage report -m --fail-under=100
    uv run coverage-badge -f -o coverage.svg

# Watch for changes (using entr if available)
watch:
    @if command -v entr >/dev/null 2>&1; then \
        find . -name "*.py" | entr -c just test; \
    else \
        echo "Install 'entr' for file watching: apt-get install entr or brew install entr"; \
        exit 1; \
    fi

# Build distribution packages
build:
    uv build

# Validate YAML methodology files against schema
validate-methodologies:
    uv run python scripts/validate_methodologies.py

# Generate SSVC plugins from YAML configurations
generate-plugins: validate-methodologies
    uv run python scripts/generate_plugins.py

# Verify checksums of all generated files from documentation metadata
verify-checksums:
    #!/bin/bash
    echo "Verifying checksums of generated files..."
    for doc in docs/*.md; do
        if [ -f "$doc" ]; then
            py_path=$(rg -N "path: src/ssvc/plugins/.*\.py" --only-matching "$doc" 2>/dev/null | head -1 | sed 's/path: //' || true)
            py_checksum=$(rg -N "checksum: [a-f0-9]+" --only-matching "$doc" 2>/dev/null | head -1 | sed 's/checksum: //' || true)
            if [ -n "$py_path" ] && [ -n "$py_checksum" ] && [ -f "$py_path" ]; then
                echo "Verifying $py_path..."
                echo "$py_checksum  $py_path" | sha1sum -c || echo "CHECKSUM MISMATCH: $py_path"
            fi
        fi
    done
    echo "Checksum verification complete."

# Run full development cycle: generate plugins, test
dev: generate-plugins test

# Lint and format (using ruff if available)
lint:
    @if command -v ruff >/dev/null 2>&1; then \
        ruff check .; \
        ruff format --check .; \
    else \
        echo "Install 'ruff' for linting: uv add --dev ruff"; \
    fi

# Format code
format:
    @if command -v ruff >/dev/null 2>&1; then \
        ruff format .; \
    else \
        echo "Install 'ruff' for formatting: uv add --dev ruff"; \
    fi

# Clean all generated files and dependencies
clean-all: clean
    rm -rf .venv dist build .pytest_cache .coverage
    rm -f *.sarif.json *.cdx.json coverage.svg

# Quick check: test without coverage
check: generate-plugins
    uv run pytest --tb=short

# Container management
# Build the development container
container-build:
    podman build -t ssvc-python-dev -f Containerfile .

# Run container with file mounts for development
container-run:
    podman run -it --rm \
        --name ssvc-python-dev \
        -v "$(pwd):/workspace:Z" \
        -p 8000:8000 \
        -p 5000:5000 \
        -p 3000:3000 \
        ssvc-python-dev

# Start interactive development session
container-dev: container-build
    podman run -d --rm \
        --name ssvc-python-dev \
        -v "$(pwd):/workspace:Z" \
        -p 8000:8000 \
        -p 5000:5000 \
        -p 3000:3000 \
        -w /workspace \
        ssvc-python-dev

# Execute command in running container
container-exec command="sh":
    podman exec -it ssvc-python-dev {{command}}

# Clean up container images
container-clean:
    @echo "Stopping and removing containers..."
    podman stop ssvc-python-dev 2>/dev/null || true
    podman rm ssvc-python-dev 2>/dev/null || true
    @echo "Removing images..."
    podman rmi localhost/ssvc-python-dev:latest 2>/dev/null || true
    podman rmi ssvc-python-dev 2>/dev/null || true
    @echo "Cleaning up unused containers and images..."
    podman container prune -f 2>/dev/null || true
    podman image prune -f 2>/dev/null || true
    @echo "Cleanup complete!"

# Force clean up everything (use with caution)
container-clean-all:
    @echo "Force stopping all containers..."
    podman stop --all 2>/dev/null || true
    @echo "Removing all containers..."
    podman rm --all 2>/dev/null || true
    @echo "Removing all images..."
    podman rmi --all --force 2>/dev/null || true
    @echo "System cleanup..."
    podman system prune --all --force 2>/dev/null || true
    @echo "Nuclear cleanup complete!"

# Run tests inside container
container-test: container-build
    podman run --rm \
        -v "$(pwd):/workspace:Z" \
        -w /workspace \
        ssvc-python-dev \
        sh -c "uv sync && just test"

# Run build inside container
container-build-app: container-build
    podman run --rm \
        -v "$(pwd):/workspace:Z" \
        -w /workspace \
        ssvc-python-dev \
        sh -c "uv sync && uv build"

# Preview generated plugins (shows what would be generated)
preview-plugins:
    uv run python scripts/generate_plugins.py --dry-run

# Install development dependencies
dev-install:
    uv add --dev pytest coverage pytest-cov coverage-badge ruff mypy

# Type checking with mypy
typecheck:
    @if command -v mypy >/dev/null 2>&1; then \
        uv run mypy src/; \
    else \
        echo "Install 'mypy' for type checking: uv add --dev mypy"; \
    fi

# Run all quality checks
qa: lint typecheck test
    @echo "✅ All quality checks passed!"

# Generate and test everything
all: clean generate-plugins qa build
    @echo "🚀 Complete build and test cycle finished!"