help:
	@echo "vaccine - Makefile targets:"
	@echo "  make                - Start DVWA and Juice Shop targets (default)"
	@echo "  make start          - Create .venv, install requirements and start targets"
	@echo "  make stop           - Stop running containers"
	@echo "  make down           - Stop and remove containers/networks"
	@echo "  make clean          - Remove containers, caches, output and .venv"
	@echo "  make logs           - Stream target logs"
	@echo "  make run URL=...    - Run vaccine locally against URL"
	@echo "  make test           - Run unit tests"
	@echo "  make check          - Start DVWA and run unit tests"
	@echo "  make re             - Full reset and start"

start:
	python3 -m venv .venv
	. .venv/bin/activate && pip install --upgrade pip && pip install -r requirements.txt
	docker compose up -d
	@echo "[+] Entorno virtual creado en: .venv"
	@echo "[+] Dependencias instaladas desde requirements.txt"
	@echo "[+] DVWA disponible en: http://localhost:8080"
	@echo "[+] Juice Shop (SQLite) disponible en: http://localhost:3000"
	@echo "[+] Entornos de prueba levantados"

stop:
	docker compose stop

down:
	docker compose down

clean:
	docker compose down -v --rmi local
	@if [ -d .venv ]; then \
		bash -c "source .venv/bin/activate && deactivate" 2>/dev/null || true; \
		rm -rf .venv; \
	fi
	find . -type d -name '__pycache__' -prune -exec rm -rf {} +
	rm -rf output
	@echo "[+] Entorno limpiado"

logs:
	docker compose logs -f dvwa_target juice_shop

test:
	python3 -m unittest discover -s tests -v

check: start test

re: clean start

run:
	@if [ -z "$(URL)" ]; then \
		echo "[!] Uso: make run URL='http://localhost:8080/vulnerabilities/sqli/?id=1&Submit=Submit'"; \
		exit 1; \
	fi
	python3 vaccine.py "$(URL)"

# Compatibilidad con nombres previos
up: start

.PHONY: all help start stop up down clean logs run test check re