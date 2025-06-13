PY_FILES := $(wildcard *.py)

run: uv
	@for file in $(PY_FILES); do \
		echo "Running $$file..."; \
		uv run python3 $$file; \
		echo; \
	done

uv:
	@which uv > /dev/null || pip install uv
