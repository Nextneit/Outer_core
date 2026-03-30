help:
	@echo "stockholm - Makefile targets:"
	@echo "  make start         - Build and start the container"
	@echo "  make stop          - Stop the container"
	@echo "  make down          - Stop and remove container"
	@echo "  make clean         - Remove image and container"
	@echo "  make logs          - Show container logs"
	@echo "  make bash          - Open bash shell in container"
	@echo "  make create-files  - Create sample files for testing"
	@echo ""
	@echo "Usage examples inside container:"
	@echo "  stockholm               - Encrypt files in ~/infection"
	@echo "  stockholm -h            - Show help"
	@echo "  stockholm -v            - Show version"
	@echo "  stockholm -r KEY        - Decrypt files using KEY"
	@echo "  stockholm -s            - Run silently (no output)"
	@echo ""
	@echo "  make help          - Show this message"

start:
	docker-compose build
	docker-compose up -d
	@echo "✓ Stockholm container started"

stop:
	docker-compose stop
	@echo "✓ Container stopped"

down:
	docker-compose down
	@echo "✓ Container removed"

clean:
	docker-compose down --rmi all
	rm -rf ./infection
	@echo "✓ Image and container cleaned"

logs:
	docker-compose logs -f stockholm

bash:
	docker-compose exec stockholm /bin/bash

create-files:
	@echo "Cleaning old files from /root/infection..."
	@docker-compose exec stockholm bash -c 'rm -f /root/infection/*.ft /root/infection/*.txt /root/infection/*.json'
	@echo "Creating fresh test files in /root/infection..."
	@docker-compose exec stockholm bash -c 'printf "This is a test file for Stockholm ransomware testing.\n\nContent created on $$(date).\nYou can use this file to verify encryption/decryption functionality.\n\nStockholm is designed to handle various file types and encrypt their contents using Fernet encryption.\n" > /root/infection/sample_document.txt'
	@docker-compose exec stockholm bash -c 'printf "{\n  \"test_data\": {\n    \"project\": \"Stockholm\",\n    \"description\": \"Ransomware encryption testing framework\",\n    \"files\": [\"important_document.txt\", \"data.json\", \"config.yaml\"],\n    \"encryption_method\": \"Fernet\",\n    \"status\": \"ready_for_testing\"\n  }\n}\n" > /root/infection/config.json'
	@docker-compose exec stockholm ls -lah /root/infection/
	@echo "✓ Test files created at /root/infection/"
	@echo ""
	@echo "Next steps:"
	@echo "  make bash                    # Enter container"
	@echo "  stockholm                    # Encrypt files (inside container)"

.PHONY: help start stop down clean logs bash create-files test
