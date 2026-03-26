help:
	@echo "ft_onion - Makefile targets:"
	@echo "  make start    - Build and start the container"
	@echo "  make stop     - Stop the container"
	@echo "  make clean    - Remove image and container"
	@echo "  make test-ssh - Test SSH connection (port 2222)"
	@echo "  make test-web - Test web server (port 8080)"
	@echo "  make check    - Verify all services"
	@echo "  make help     - Show this message"

start:
	docker-compose build
	docker-compose up -d

stop:
	docker-compose down

clean:
	docker-compose down --rmi all

test-ssh:
	ssh user42@localhost -p 2222

test-web:
	curl -v http://localhost:8080

check:
	@echo "📍 Dirección Tor .onion:"
	@docker-compose exec ft_onion cat /var/lib/tor/hidden_service/hostname
	@echo "\n🔍 Estado del contenedor:"
	@docker-compose ps
	@echo "\n✓ Servicios activos:"
	@docker-compose exec ft_onion ps aux | grep -E "nginx|tor|sshd" | grep -v grep
	@echo "\n✅ Verificación completada"


.PHONY: start stop clean test-ssh test-web check help
