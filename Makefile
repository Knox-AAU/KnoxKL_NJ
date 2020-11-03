PYTHON=python3
DEBUG_FLAGS=-v debug -l

clean:
	rm -rf ./__pycache__ ./.pytest_cache ./**/__pycache__

run:
	$(PYTHON) app.py


run-debug: 
	$(PYTHON) app.py $(DEBUG_FLAGS)