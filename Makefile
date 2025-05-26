.PHONY: install list format lint test all clean synth deploy diff destroy

install:
	@echo "Installing dependencies..."
	pip install -r requirements.txt

list:
	@echo "Listing installed packages..."
	pip list

format:
	@echo "Formatting code with Black..."
	black .

lint:
	@echo "Linting code with Pylint..."
	pylint --disable=R,C backend app.py

test:
	@echo "Running tests..."
	pytest -vv ./backend/tests/unit/test_backend_stack.py

synth:
	@echo "Synthesizing the CDK app..."
	cdk synth

diff:
	@echo "Showing diff against deployed stack..."
	cdk diff

destroy:
	@echo "Destroying the CDK stack..."
	cdk destroy --force

clean:
	@echo "Cleaning up __pycache__ and .pytest_cache..."
	find . -type d -name "__pycache__" -exec rm -r {} + || true
	rm -rf .pytest_cache

build: format lint test synth

deploy: build
	@echo "Deploying the application..."
	cdk deploy --require-approval never