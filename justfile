# fix imports with autoflake
autoflake:
    uv run autoflake -r vistafetch tests

# apply code formatting with black
format:
    uv run ruff format vistafetch tests

# run static type checking with mypy
mypy:
    uv run mypy vistafetch

# apply linting with ruff
ruff:
    uv run ruff check vistafetch/**/*.py tests/**/*.py  --fix-only

# run pre-configured dependency lock
lock-deps:
    uv lock --frozen

# run pre-configured dependency install
install-deps:
    uv sync --group dev --all-extras

# run a check (ideally before comitting)
check: autoflake format mypy
    uv run ruff check vistafetch/ tests/

# run pre-commit check
pre-commit:
	git ls-files -- 'vistafetch/**/*' | xargs poetry run pre-commit run --verbose --files

# prettify your code (linting & formatting is applied)
pretty: autoflake ruff format

# run all unit tests
unit-tests:
    export TZ="UTC"; uv run pytest --cov=vistafetch --cov-fail-under=90 --cov-report term-missing:skip-covered --no-cov-on-fail tests/
