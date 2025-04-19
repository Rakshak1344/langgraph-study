install:
	poetry install

lint:
	poetry run isort src/ tests/
	poetry run black src/ tests/

test:
	poetry run pytest -v

studio:
	poetry run langgraph studio

run:
	poetry run python src/advanced_rag_graph/main.py
