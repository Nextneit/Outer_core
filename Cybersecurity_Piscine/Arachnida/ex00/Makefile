# Spider Test Makefile
# Standard scraping tests based on validated URLs

SPIDER = python3 spider.py
DATA_DIR_BMP = ./data_bmp
DATA_DIR_PICSUM = ./data_picsum
DATA_DIR_BOOKS = ./data_books
DATA_DIR_RECURSIVE = ./data_recursive
DATA_DIR_DEPTH = ./data_depth

# Default test: non-recursive scraping on all URLs
test: clean test-urls
	@echo "\n[✓] All standard tests completed!"

# Test each URL individually (non-recursive)
test-urls:
	@echo "\n[TEST 1] Scraping BMP samples (non-recursive)..."
	@$(SPIDER) https://filesamples.com/formats/bmp -p $(DATA_DIR_BMP)
	@echo "\n[TEST 2] Scraping Picsum photos (non-recursive)..."
	@$(SPIDER) https://picsum.photos/images -p $(DATA_DIR_PICSUM)
	@echo "\n[TEST 3] Scraping Books.toscrape (non-recursive)..."
	@$(SPIDER) https://books.toscrape.com/ -p $(DATA_DIR_BOOKS)

# Test recursive scraping
test-recursive: clean
	@echo "\n[RECURSIVE TEST] Testing recursive scraping on books.toscrape (depth 2)..."
	@$(SPIDER) https://books.toscrape.com/ -r -l 2 -p $(DATA_DIR_RECURSIVE)

# Test different recursion depths
test-depth-2: clean
	@echo "\n[DEPTH TEST] Depth level 2..."
	@$(SPIDER) https://books.toscrape.com/ -r -l 2 -p $(DATA_DIR_DEPTH)

test-depth-5: clean
	@echo "\n[DEPTH TEST] Depth level 5..."
	@$(SPIDER) https://books.toscrape.com/ -r -l 5 -p $(DATA_DIR_DEPTH)

# Clean all test data directories
clean:
	@echo "[CLEAN] Removing test data directories..."
	@rm -rf $(DATA_DIR_BMP) $(DATA_DIR_PICSUM) $(DATA_DIR_BOOKS) $(DATA_DIR_RECURSIVE) $(DATA_DIR_DEPTH)
	@echo "[CLEAN] Done!"

# Help target
help:
	@echo "Spider Test Makefile - Available targets:"
	@echo ""
	@echo "  make test              - Run all standard tests (non-recursive)"
	@echo "  make test-urls         - Test all URLs individually"
	@echo "  make test-recursive    - Test recursive scraping (depth 2)"
	@echo "  make test-depth-2      - Test with recursion depth 2"
	@echo "  make test-depth-5      - Test with recursion depth 5"
	@echo "  make clean             - Remove all test data directories"
	@echo "  make help              - Show this help message"
	@echo ""
	@echo "Test URLs:"
	@echo "  1. https://filesamples.com/formats/bmp"
	@echo "  2. https://picsum.photos/images"
	@echo "  3. https://books.toscrape.com/"

.PHONY: test clean test-recursive test-depth-2 test-depth-5 test-urls help