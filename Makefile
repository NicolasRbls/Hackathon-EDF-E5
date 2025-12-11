.PHONY: work up down test

# Default target
work: up
	@echo "🚀 Starting Backend..."
	@cd backend && . venv/bin/activate && uvicorn app.main:app --reload

# Start Database Container
up:
	@echo "🐳 Checking/Starting Database..."
	@if [ -z "$$(docker ps -q -f name=edf_hackathon_db)" ]; then \
		docker compose up -d db; \
		echo "⏳ Waiting for Database to be ready..."; \
		sleep 3; \
	else \
		echo "✅ Database is already running."; \
	fi

# Stop Database Container
down:
	@docker compose down

# Run Tests
test:
	@cd backend && . venv/bin/activate && pytest tests/

# Install/Update Dependencies (including new Postgres driver)
install:
	@cd backend && . venv/bin/activate && pip install -r requirements.txt
