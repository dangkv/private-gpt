.PHONY: start stop status

start:
	brew services start ollama

stop:
	brew services stop ollama

status:
	brew services list | grep ollama
