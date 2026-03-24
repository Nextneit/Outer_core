# Scorpion Test Makefile
# Quick tests for metadata extraction, stripping, and modification

SCORPION = ./.venv/bin/python3 scorpion.py
DATA_BMP = ../ex00/data_bmp
DATA_PICSUM = ../ex00/data_picsum
DATA_TENOR = ../ex00/data_tenor
TEST_IMG = ncruz-ga.png
TEST_OUTPUT_DIR = ./test_output

# Default test: run all quick tests
test: install test-extract test-strip test-set
	@echo "\n[✓] All Scorpion tests completed!"


# Test 1: Extract and display metadata
test-extract:
	@echo "\n[TEST 1] Extracting metadata from images..."
	@if [ -f "$(TEST_IMG)" ]; then \
		echo "  → From $(TEST_IMG):"; \
		$(SCORPION) $(TEST_IMG); \
	fi
	@jpg=$$(ls $(DATA_PICSUM)/*.jpg 2>/dev/null | head -1); \
	if [ -f "$$jpg" ]; then \
		echo "\n  → From JPG ($(DATA_PICSUM)):"; \
		$(SCORPION) "$$jpg"; \
	fi
	@bmp=$$(ls $(DATA_BMP)/*.bmp 2>/dev/null | head -1); \
	if [ -f "$$bmp" ]; then \
		echo "\n  → From BMP ($(DATA_BMP)):"; \
		$(SCORPION) "$$bmp"; \
	fi
	@gif=$$(ls $(DATA_TENOR)/*.gif 2>/dev/null | head -1); \
	if [ -f "$$gif" ]; then \
		echo "\n  → From GIF ($(DATA_TENOR)):"; \
		$(SCORPION) "$$gif"; \
	fi

# Test 2: Strip metadata from image
test-strip:
	@echo "\n[TEST 2] Stripping metadata..."
	@mkdir -p $(TEST_OUTPUT_DIR)
	@jpg=$$(ls $(DATA_PICSUM)/*.jpg 2>/dev/null | head -1); \
	if [ -f "$$jpg" ]; then \
		echo "  → BEFORE (Original metadata):"; \
		$(SCORPION) "$$jpg"; \
		echo ""; \
		$(SCORPION) "$$jpg" --strip --out $(TEST_OUTPUT_DIR)/cleaned_$$(basename $$jpg); \
		echo ""; \
		echo "  → AFTER (Cleaned metadata):"; \
		$(SCORPION) $(TEST_OUTPUT_DIR)/cleaned_$$(basename $$jpg); \
	else \
		echo "[SKIP] No JPEG test image available in $(DATA_PICSUM)"; \
	fi

# Test 3: Set metadata
test-set:
	@echo "\n[TEST 3] Modifying metadata..."
	@mkdir -p $(TEST_OUTPUT_DIR)
	@jpg=$$(ls $(DATA_PICSUM)/*.jpg 2>/dev/null | head -1); \
	if [ -f "$$jpg" ]; then \
		echo "  → BEFORE (Original metadata):"; \
		$(SCORPION) "$$jpg"; \
		echo ""; \
		$(SCORPION) "$$jpg" \
			--set "0th.ImageDescription=Modified by Scorpion" \
			--set "0th.Artist=Security Team" \
			--out $(TEST_OUTPUT_DIR)/modified_$$(basename $$jpg); \
		echo ""; \
		echo "  → AFTER (Modified metadata):"; \
		$(SCORPION) $(TEST_OUTPUT_DIR)/modified_$$(basename $$jpg); \
	else \
		echo "[SKIP] No JPEG test image available in $(DATA_PICSUM)"; \
	fi

# Verify modified files
test-verify: test-strip test-set
	@echo "\n[VERIFY] Checking test outputs..."
	@ls -lh $(TEST_OUTPUT_DIR)/ 2>/dev/null || echo "No test outputs yet"

# Clean test outputs and virtual environment
clean:
	@echo "[CLEAN] Removing test output directory and virtual environment..."
	@rm -rf $(TEST_OUTPUT_DIR) .venv
	@echo "[CLEAN] Done!"

# Setup virtual environment and install dependencies
.venv:
	@echo "[SETUP] Creating virtual environment..."
	python3 -m venv .venv
	@echo "[OK] Virtual environment created at ./.venv"

install: .venv
	@echo "[INSTALL] Installing dependencies from requirements.txt..."
	./.venv/bin/pip install --upgrade pip
	./.venv/bin/pip install -r requirements.txt
	@echo "[OK] All dependencies installed. Activate with: source ./.venv/bin/activate"

# Help
help:
	@echo "Scorpion Test Makefile - Available targets:"
	@echo ""
	@echo "  make install           - Create venv and install dependencies"
	@echo "  make test              - Run all tests (extract, strip, set)"
	@echo "  make test-extract      - Extract and display metadata (JPG/BMP/GIF)"
	@echo "  make test-strip        - Strip metadata from JPEG"
	@echo "  make test-set          - Modify metadata in JPEG"
	@echo "  make test-verify       - Verify test outputs exist"
	@echo "  make clean             - Remove test outputs"
	@echo "  make help              - Show this help"
	@echo ""
	@echo "Supported Formats:"
	@echo "  ✓ JPEG: Full EXIF editing + stripping"
	@echo "  ✓ PNG:  Text metadata editing + stripping"
	@echo "  ○ BMP/GIF: Metadata viewing only (no editing)"
	@echo ""
	@echo "Data Sources (from ex00 Spider):"
	@echo "  - $(DATA_PICSUM)/ (JPG images)"
	@echo "  - $(DATA_BMP)/ (BMP images)"
	@echo "  - $(DATA_TENOR)/ (GIF images)"
	@echo "  - $(TEST_IMG) (if exists in current dir)"

.PHONY: test test-extract test-strip test-set test-verify clean install help