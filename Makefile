PYTHON := python3
ASSEMBLER := assembler.py
INPUT := kernels/test.S
OUTPUT_BIN := output_test.bin

all: run

run: bin

bin:
	$(PYTHON) $(ASSEMBLER) $(INPUT) $(OUTPUT_BIN)
	@echo "Generated binary output: $(OUTPUT_BIN)"

clean:
	rm -f $(OUTPUT_BIN)
	@echo "Cleaned generated files."

# Test output (optional: add specific test commands here)
test:
	# Compare output files with expected results (if any)
	# For example: diff $(OUTPUT_BIN) expected_output.bin
	# To implement specific tests, add custom test cases here

# Phony targets
.PHONY: all run hex bin clean test
