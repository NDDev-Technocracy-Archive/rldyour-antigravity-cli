set shell := ["bash", "-euo", "pipefail", "-c"]

# Lists the repository commands.
default:
    @just --list

# Prepares the locked validation environment without building packages.
setup:
    uv sync --locked --group ci --no-install-project --no-build

# Checks source files and workflows without builds or network access.
check:
    just --fmt --check
    python3 .github/ci/check_source.py
    actionlint
    uv run --offline --locked --no-sync --group ci zizmor --offline --no-progress .github

# Formats the command declarations.
fix:
    just --fmt

# Runs the existing adapter validation, hook smoke and pytest coverage gates.
test:
    RLDYOUR_VALIDATE_LIVE_ANTIGRAVITY=0 uv run --offline --locked --no-sync --group ci bash scripts/validate_fast.sh

# Runs every existing release-readiness check and checks the source archive.
verify: check
    RLDYOUR_VALIDATE_LIVE_ANTIGRAVITY=0 uv run --offline --locked --no-sync --group ci bash scripts/validate_release.sh
    just build

# Builds the tracked source archive and rejects forbidden entries.
build:
    python3 .github/ci/archive.py

# Checks the native configuration on each supported operating system.
check-config:
    python3 scripts/validate_gemini_config.py --strict
