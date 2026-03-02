CC = gcc
CFLAGS = -Wall -Wextra -Werror

COLLEEN = Colleen
GRACE = Grace
SULLY = Sully

all: $(COLLEEN) $(GRACE) $(SULLY)

$(COLLEEN): $(COLLEEN).c
	$(CC) $(CFLAGS) $(COLLEEN).c -o $(COLLEEN)

$(GRACE): $(GRACE).c
	$(CC) $(CFLAGS) $(GRACE).c -o $(GRACE)

$(SULLY): $(SULLY).c
	$(CC) $(CFLAGS) $(SULLY).c -o $(SULLY)

clean:
	rm -f $(COLLEEN) $(GRACE) $(SULLY)
	rm -f tmp_Colleen Grace_kid.c
	rm -f Sully_* tmp_Sully*

fclean: clean

re: fclean all

test_colleen: $(COLLEEN)
	@echo "Testing Colleen..."
	@./$(COLLEEN) > tmp_Colleen
	@if diff $(COLLEEN).c tmp_Colleen > /dev/null 2>&1; then \
		echo "✓ Colleen test passed!"; \
	else \
		echo "✗ Colleen test failed"; \
		diff $(COLLEEN).c tmp_Colleen; \
	fi
	@rm -f tmp_Colleen

test_grace: $(GRACE)
	@echo "Testing Grace..."
	@rm -f Grace_kid.c
	@./$(GRACE)
	@if [ -f Grace_kid.c ]; then \
		if diff $(GRACE).c Grace_kid.c > /dev/null 2>&1; then \
			echo "✓ Grace test passed!"; \
		else \
			echo "✗ Grace test failed"; \
			diff $(GRACE).c Grace_kid.c; \
		fi; \
	else \
		echo "✗ Grace_kid.c was not created"; \
	fi

test_sully: $(SULLY)
	@echo "Testing Sully..."
	@rm -f Sully_* tmp_Sully*
	@./$(SULLY)
	@count=$$(ls -1 Sully* 2>/dev/null | wc -l); \
	if [ $$count -eq 13 ]; then \
		echo "✓ Sully test passed! (13 files generated)"; \
		ls -1 Sully* | sort; \
	else \
		echo "✗ Sully test failed (expected 13 files, got $$count)"; \
		ls -1 Sully*; \
	fi

test: test_colleen test_grace test_sully

.PHONY: all clean fclean re test test_colleen test_grace test_sully
