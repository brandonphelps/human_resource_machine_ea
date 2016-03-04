
PY_FILES = $(wildcard *.py)

PYC_FILES = ${PY_FILES:%.py=%.pyc}


.PHONY: clean print-vars

print-vars:
	@echo "PY_FILES: " ${PY_FILES}
	@echo "PYC_FILES: " ${PYC_FILES}

clean:
	@rm -fv ${PYC_FILES}
	@rm -fv *~
