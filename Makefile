.PHONY: setup build up down migrate makemigrations test logs shell clean

# One-command complete setup (Builds images, starts containers, applies migrations)
setup: build up migrate
	@echo "Setup complete! API is running at http://localhost:8000/"

# Build Docker images
build:
	docker-compose build

# Start all containers (Web, Redis, Celery) in the background
up:
	docker-compose up -d

# Stop all running containers
down:
	docker-compose down

# Apply database migrations
migrate:
	docker-compose exec web python manage.py migrate

# Create new database migrations
makemigrations:
	docker-compose exec web python manage.py makemigrations

# Run the 14-test suite
test:
	docker-compose exec web python manage.py test

# Stream live container logs
logs:
	docker-compose logs -f

# Access Django interactive shell
shell:
	docker-compose exec web python manage.py shell

# Stop containers and wipe database volumes for a fresh reset
clean:
	docker-compose down -v