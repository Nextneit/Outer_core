# ft_otp - One-Time Password (TOTP) Generator Makefile

PYTHON = ./.venv/bin/python3
PIP = ./.venv/bin/pip3
OTP_SCRIPT = ft_otp.py
KEY_HEX_FILE = key.hex
TEST_KEY_FILE = test_key.hex
OTP_KEY_FILE = ft_otp.key
FERNET_KEY_FILE = ft_otp.fernet

# Default target
all: install $(KEY_HEX_FILE)
	@$(PYTHON) $(OTP_SCRIPT) -g $(KEY_HEX_FILE)

# Install dependencies in virtual environment
install:
	@if [ ! -d "./.venv" ]; then \
		echo "[→] Creating virtual environment..."; \
		python3 -m venv .venv; \
	fi
	@echo "[→] Installing dependencies..."
	@$(PIP) install -q -r requirements.txt
	@echo "[✓] Installation complete!"

# Generate random 64-character hex key file
$(KEY_HEX_FILE):
	@python3 -c "import os; print(os.urandom(32).hex(), end='')" > $(KEY_HEX_FILE)
	@echo "[✓] Random key file generated: $(KEY_HEX_FILE)"

# Clean up generated files and virtual environment
clean:
	@echo "[→] Cleaning up..."
	@rm -rf .venv
	@rm -f $(KEY_HEX_FILE)
	@rm -f $(OTP_KEY_FILE)
	@rm -f $(FERNET_KEY_FILE)
	@rm -f $(TEST_KEY_FILE)
	@find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	@find . -type f -name "*.pyc" -delete
	@echo "[✓] Clean complete!"

# Test 1: Generate and save a TOTP key
test-gen:
	@echo "\n[TEST 1] Generating and saving a TOTP key..."
	@TEST_HEX="c42c3cc306414141592f772691f47fbf4d2c2263ae34e7b4b9137d128d6d2a7d"; \
	echo "$$TEST_HEX" > $(TEST_KEY_FILE); \
	echo "  → Created key file: $(TEST_KEY_FILE)"; \
	$(PYTHON) $(OTP_SCRIPT) -g $(TEST_KEY_FILE)
	@if [ -f "$(OTP_KEY_FILE)" ]; then \
		echo "  → Key file created successfully!"; \
	fi

# Test 2: Generate TOTP from saved key
test-totp:
	@echo "\n[TEST 2] Generating TOTP from key file..."
	@if [ -f "$(OTP_KEY_FILE)" ]; then \
		echo "  → Current TOTP:"; \
		$(PYTHON) $(OTP_SCRIPT) -k $(OTP_KEY_FILE); \
	else \
		echo "  ERROR: No key file found. Run 'make test-gen' first."; \
		exit 1; \
	fi

# Test 3: Test with invalid key (too short)
test-invalid-short:
	@echo "\n[TEST 3] Testing invalid key (too short)..."
	@echo "abc123" > /tmp/invalid_short.hex; \
	echo "  → Attempting to load invalid hex key..."; \
	$(PYTHON) $(OTP_SCRIPT) -g /tmp/invalid_short.hex 2>&1 || echo "  → Correctly rejected short key"; \
	rm -f /tmp/invalid_short.hex

# Test 4: Test with invalid hex characters
test-invalid-hex:
	@echo "\n[TEST 4] Testing invalid hex characters..."
	@echo "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx" > /tmp/invalid_hex.hex; \
	echo "  → Attempting to load invalid hex key..."; \
	$(PYTHON) $(OTP_SCRIPT) -g /tmp/invalid_hex.hex 2>&1 || echo "  → Correctly rejected invalid hex"; \
	rm -f /tmp/invalid_hex.hex

# Test 5: Test help message
test-help:
	@echo "\n[TEST 5] Displaying help message..."
	@$(PYTHON) $(OTP_SCRIPT) -h

# Run all tests
test: install test-gen test-totp test-invalid-short test-invalid-hex test-help
	@echo "\n[✓] All ft_otp tests completed!"

# Run the script with custom arguments
run: install $(KEY_HEX_FILE)
	@$(PYTHON) $(OTP_SCRIPT) -k $(OTP_KEY_FILE)

# Rebuild: clean everything and run from scratch
re: clean all
	@echo "\n[✓] Rebuild complete!"

# Quick help
help:
	@echo "ft_otp - One-Time Password Generator"
	@echo ""
	@echo "Available targets:"
	@echo "  make              - Generate random key, install deps, and save encrypted key"
	@echo "  make install      - Setup virtual environment and install dependencies"
	@echo "  make run          - Generate TOTP from encrypted key file"
	@echo "  make re           - Clean everything and rebuild from scratch"
	@echo "  make clean        - Remove all generated files"
	@echo "  make test         - Run all validation tests"
	@echo "  make help         - Show this help message"
	@echo ""
	@echo "Test targets:"
	@echo "  make test-gen     - Test key generation from file (-g flag)"
	@echo "  make test-totp    - Test TOTP generation (-k flag)"
	@echo "  make test-invalid-short - Validate rejection of short keys"
	@echo "  make test-invalid-hex   - Validate rejection of invalid hex"
	@echo "  make test-help    - Display script help"
	@echo ""
	@echo "Workflow:"
	@echo "  make              # Generate key.hex (random) and save encrypted"
	@echo "  make run          # Generate TOTP from the encrypted key"
	@echo "  make re           # Start fresh: clean and redo everything"

.PHONY: all install clean test test-gen test-totp test-invalid-short test-invalid-hex test-help run re help
