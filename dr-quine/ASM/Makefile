NASM = nasm
NFLAGS = -f elf64
LD = gcc
LDFLAGS = -no-pie

COLLEEN = Colleen
GRACE = Grace
SULLY = Sully

all: $(COLLEEN) $(GRACE) $(SULLY)

$(COLLEEN): $(COLLEEN).o
	$(LD) $(LDFLAGS) $(COLLEEN).o -o $(COLLEEN)

$(COLLEEN).o: $(COLLEEN).s
	$(NASM) $(NFLAGS) $(COLLEEN).s -o $(COLLEEN).o

$(GRACE): $(GRACE).o
	$(LD) $(LDFLAGS) $(GRACE).o -o $(GRACE)

$(GRACE).o: $(GRACE).s
	$(NASM) $(NFLAGS) $(GRACE).s -o $(GRACE).o

$(SULLY): $(SULLY).o
	$(LD) $(LDFLAGS) $(SULLY).o -o $(SULLY)

$(SULLY).o: $(SULLY).s
	$(NASM) $(NFLAGS) $(SULLY).s -o $(SULLY).o

clean:
	rm -f $(COLLEEN) $(COLLEEN).o $(GRACE) $(GRACE).o $(SULLY) $(SULLY).o
	rm -f tmp_Colleen Grace_kid.s
	rm -f Sully_* tmp_Sully*

fclean: clean

re: fclean all

test_colleen: $(COLLEEN)
	@echo "Testing Colleen..."
	@./$(COLLEEN) > tmp_Colleen
	@if diff $(COLLEEN).s tmp_Colleen > /dev/null 2>&1; then \
		echo "✓ Colleen test passed!"; \
	else \
		echo "✗ Colleen test failed"; \
		diff $(COLLEEN).s tmp_Colleen | head -20; \
	fi
	@rm -f tmp_Colleen

test_grace: $(GRACE)
	@echo "Testing Grace..."
	@rm -f Grace_kid.s
	@./$(GRACE)
	@if [ -f Grace_kid.s ]; then \
		if diff $(GRACE).s Grace_kid.s > /dev/null 2>&1; then \
			echo "✓ Grace test passed!"; \
		else \
			echo "✗ Grace test failed"; \
			diff $(GRACE).s Grace_kid.s | head -20; \
		fi; \
	else \
		echo "✗ Grace_kid.s was not created"; \
	fi

test_sully: $(SULLY)
	@echo "Testing Sully..."
	@rm -f Sully_* tmp_Sully*
	@./$(SULLY)
	@count=$$(ls -1 Sully_*.s Sully_[0-9] 2>/dev/null | wc -l); \
	if [ $$count -ge 11 ]; then \
		echo "✓ Sully test passed! ($$count files generated: 6 .s + 5 binaries)"; \
		ls -1 Sully_*.s Sully_[0-9] 2>/dev/null | sort; \
	else \
		echo "✗ Sully test failed (expected at least 11 files, got $$count)"; \
		ls -1 Sully_* 2>/dev/null || echo "No files generated"; \
	fi

test: test_colleen test_grace test_sully

.PHONY: all clean fclean re test test_colleen test_grace test_sully
