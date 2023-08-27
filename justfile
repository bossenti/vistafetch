# fix imports with autoflake
autoflake:
    poetry run autoflake -r vistafetch tests

# apply code formatting with black
black:
    poetry run black vistafetch tests  -t py38 -t py39 -t py310 -t py311

# run static type checking with mypy
mypy:
    poetry run mypy vistafetch

# apply linting with ruff
ruff:
    poetry run ruff check vistafetch/**/*.py tests/**/*.py  --fix-only

# run pre-configured poetry lock
poetry-lock:
    poetry lock --no-update

# run pre-configured poetry install
poetry-install:
    poetry install --with dev --all-extras

# run a check (ideally before comitting)
check: autoflake black mypy
    poetry run ruff check vistafetch/ tests/

# run pre-commit check
pre-commit:
	git ls-files -- 'vistafetch/**/*' | xargs poetry run pre-commit run --verbose --files

# prettify your code (linting & formatting is applied)
pretty: autoflake ruff black

# run all unit tests
unit-tests:
	poetry run pytest --cov=vistafetch --cov-fail-under=90 --cov-report term-missing:skip-covered --no-cov-on-fail tests/
