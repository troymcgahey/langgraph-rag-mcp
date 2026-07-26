#To run unit tests
uv run pytest -m "not integration"

#To run integration tests
uv run pytest -m integration -v
