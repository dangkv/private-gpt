# =============================================================================
# Service Management Makefile
# =============================================================================
# Manages ChromaDB, Ollama, and Streamlit services for development environment
#
# Usage: make <target>
# Example: make help
#
# Author: Development Team
# =============================================================================

# Variables
CHROMA_DB_PATH = data/chroma_db
STREAMLIT_APP = app.py
STREAMLIT_PORT = 8501
STREAMLIT_PID_FILE = .streamlit.pid

# =============================================================================
# HELP FUNCTION
# =============================================================================

.PHONY: help
help:
	@echo "=============================================="
	@echo "🚀 Service Management Commands"
	@echo "=============================================="
	@echo ""
	@echo "📦 Main Service Commands:"
	@echo "  start        - Start both Streamlit and Ollama services"
	@echo "  stop         - Stop both Streamlit and Ollama services"
	@echo "  status       - Check status of all services"
	@echo ""
	@echo "🌐 Streamlit Commands:"
	@echo "  streamlit-start   - Start Streamlit in background"
	@echo "  streamlit-stop    - Stop Streamlit service"
	@echo "  streamlit-reset   - Restart Streamlit (stop then start)"
	@echo "  streamlit-status  - Check Streamlit service status"
	@echo ""
	@echo "🤖 Ollama Commands:"
	@echo "  llm-start    - Start Ollama service"
	@echo "  llm-stop     - Stop Ollama service"
	@echo "  llm-status   - Check Ollama service status"
	@echo ""
	@echo "🗄️ Database Commands:"
	@echo "  db-drop      - Remove all ChromaDB files and directories"
	@echo "  db-reset     - Drop database and recreate empty directory"
	@echo "  db-check     - Check if database directory exists"
	@echo "  db-backup    - Create a backup of the database"
	@echo "  db-ingest    - Ingest unstructured documents into vector database"
	@echo ""
	@echo "=============================================="

# =============================================================================
# MAIN SERVICE COMMANDS
# =============================================================================

.PHONY: start stop status
start: llm-start streamlit-start
	@echo "🎉 All services started successfully!"

stop: streamlit-stop llm-stop
	@echo "🛑 All services stopped successfully!"

status: streamlit-status llm-status db-check
	@echo "📊 Status check complete!"

# =============================================================================
# STREAMLIT SERVICE MANAGEMENT
# =============================================================================

.PHONY: streamlit-start streamlit-stop streamlit-reset streamlit-status

streamlit-start:
	@echo "🌐 Starting Streamlit service..."
	@if [ -f $(STREAMLIT_PID_FILE) ]; then \
		echo "⚠️  Streamlit might already be running. Checking..."; \
		if kill -0 $$(cat $(STREAMLIT_PID_FILE)) 2>/dev/null; then \
			echo "✅ Streamlit is already running (PID: $$(cat $(STREAMLIT_PID_FILE)))"; \
			exit 0; \
		else \
			echo "🧹 Cleaning up stale PID file..."; \
			rm -f $(STREAMLIT_PID_FILE); \
		fi; \
	fi
	@streamlit run $(STREAMLIT_APP) --server.port $(STREAMLIT_PORT) --server.headless true > /dev/null 2>&1 & echo $$! > $(STREAMLIT_PID_FILE)
	@sleep 2
	@if [ -f $(STREAMLIT_PID_FILE) ] && kill -0 $$(cat $(STREAMLIT_PID_FILE)) 2>/dev/null; then \
		echo "✅ Streamlit started successfully (PID: $$(cat $(STREAMLIT_PID_FILE)))"; \
		echo "🌐 Access at: http://localhost:$(STREAMLIT_PORT)"; \
	else \
		echo "❌ Failed to start Streamlit"; \
		rm -f $(STREAMLIT_PID_FILE); \
	fi

streamlit-stop:
	@echo "🛑 Stopping Streamlit service..."
	@if [ -f $(STREAMLIT_PID_FILE) ]; then \
		if kill -0 $$(cat $(STREAMLIT_PID_FILE)) 2>/dev/null; then \
			kill $$(cat $(STREAMLIT_PID_FILE)); \
			rm -f $(STREAMLIT_PID_FILE); \
			echo "✅ Streamlit stopped successfully"; \
		else \
			echo "⚠️  Streamlit process not found, cleaning up PID file"; \
			rm -f $(STREAMLIT_PID_FILE); \
		fi; \
	else \
		echo "⚠️  Streamlit PID file not found, checking for running processes..."; \
		pkill -f "streamlit run" && echo "✅ Streamlit processes terminated" || echo "ℹ️  No Streamlit processes found"; \
	fi

streamlit-reset: streamlit-stop streamlit-start
	@echo "🔄 Streamlit service reset complete!"

streamlit-status:
	@echo "📊 Streamlit service status:"
	@if [ -f $(STREAMLIT_PID_FILE) ]; then \
		if kill -0 $$(cat $(STREAMLIT_PID_FILE)) 2>/dev/null; then \
			echo "✅ Streamlit is running (PID: $$(cat $(STREAMLIT_PID_FILE)))"; \
			echo "🌐 Access at: http://localhost:$(STREAMLIT_PORT)"; \
		else \
			echo "❌ Streamlit is not running (stale PID file)"; \
		fi; \
	else \
		echo "❌ Streamlit is not running (no PID file)"; \
	fi

# =============================================================================
# OLLAMA SERVICE MANAGEMENT
# =============================================================================

.PHONY: llm-start llm-stop llm-status

llm-start:
	@echo "🤖 Starting Ollama service..."
	@brew services start ollama
	@echo "✅ Ollama service started"

llm-stop:
	@echo "🛑 Stopping Ollama service..."
	@brew services stop ollama
	@echo "✅ Ollama service stopped"

llm-status:
	@echo "📊 Ollama service status:"
	@brew services list | grep ollama || echo "❌ Ollama service not found"

# =============================================================================
# DATABASE MANAGEMENT
# =============================================================================

.PHONY: db-drop db-reset db-check db-backup db-ingest

db-drop:
	@echo "🗑️  Dropping ChromaDB database..."
	@if [ -d "$(CHROMA_DB_PATH)" ]; then \
		rm -rf $(CHROMA_DB_PATH); \
		echo "✅ Database dropped successfully from: $(CHROMA_DB_PATH)"; \
	else \
		echo "⚠️  Database directory not found: $(CHROMA_DB_PATH)"; \
	fi

db-reset: db-drop
	@echo "🔄 Resetting ChromaDB database..."
	@mkdir -p $(CHROMA_DB_PATH)
	@echo "✅ Database reset complete: $(CHROMA_DB_PATH)"

db-check:
	@echo "📊 Database status:"
	@if [ -d "$(CHROMA_DB_PATH)" ]; then \
		echo "✅ Database directory exists: $(CHROMA_DB_PATH)"; \
		echo "📁 Directory contents:"; \
		ls -la $(CHROMA_DB_PATH) 2>/dev/null || echo "   (empty)"; \
	else \
		echo "❌ Database directory not found: $(CHROMA_DB_PATH)"; \
	fi

db-backup:
	@echo "💾 Creating backup of ChromaDB database..."
	@if [ -d "$(CHROMA_DB_PATH)" ]; then \
		backup_name="chroma_backup_$$(date +%Y%m%d_%H%M%S)"; \
		cp -r $(CHROMA_DB_PATH) "$$backup_name"; \
		echo "✅ Backup created: $$backup_name"; \
	else \
		echo "⚠️  Database directory not found: $(CHROMA_DB_PATH)"; \
	fi

db-ingest:
	@echo "📥 Starting document ingestion process..."
	@if [ ! -d "$(CHROMA_DB_PATH)" ]; then \
		echo "⚠️  Database directory not found. Creating..."; \
		mkdir -p $(CHROMA_DB_PATH); \
	fi
	@echo "🔄 Processing unstructured data into vector database..."
	@python scripts/ingest_documents.py
	@echo "✅ Document ingestion completed successfully!"

# Update the help function by adding this line to the Database Commands section:
#  db-ingest    - Ingest unstructured documents into vector database

# =============================================================================
# CLEANUP AND MAINTENANCE
# =============================================================================

.PHONY: clean clean-all

clean:
	@echo "🧹 Cleaning up temporary files..."
	@rm -f $(STREAMLIT_PID_FILE)
	@echo "✅ Cleanup complete"

clean-all: stop clean
	@echo "🧹 Deep cleaning all services and temporary files..."
	@echo "✅ Deep cleanup complete"

# =============================================================================
# DEFAULT TARGET
# =============================================================================

.DEFAULT_GOAL := help
