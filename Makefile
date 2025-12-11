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

# Stop and Remove Volumes (Reset DB)
reset:
	@echo "🧨 Resetting Database (Wiping Data)..."
	@docker compose down -v
	@echo "✅ Database reset complete. Run 'make work' to restart."

# Run Tests
test:
	@cd backend && . venv/bin/activate && pytest tests/

# Install/Update Dependencies (including new Postgres driver)
install:
	@cd backend && . venv/bin/activate && pip install -r requirements.txt

# Import Data from CSV
load-data:
	@echo "📥 Importing Data from CSV..."
	@cd backend && . venv/bin/activate && python -m app.import_data
