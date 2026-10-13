SHELL := /bin/bash

MAIN = QMC_Blog_Posts.tex
BASENAME = QMC_Blog_Posts
PDF = QMC_Blog_Posts.pdf
TEXS := $(shell find . -type f -name '*.tex' -not -path './.git/*')
# Keep pdfLaTeX and Biber in the same TeX Live installation.
TEXBIN ?= $(patsubst %/,%,$(dir $(shell command -v biber 2>/dev/null)))
PDFLATEX ?= $(if $(TEXBIN),$(TEXBIN)/pdflatex,pdflatex)
BIBER ?= $(if $(TEXBIN),$(TEXBIN)/biber,biber)

.PHONY: all pdf clean view force rebuild

all: pdf

pdf: $(TEXS) clean
	$(PDFLATEX) -interaction=nonstopmode -halt-on-error $(MAIN)
	@if [ "$$(uname -s)" = Darwin ] && file "$(BIBER)" | grep -q 'universal binary'; then \
		thin_biber=$$(mktemp /tmp/qmc-biber.XXXXXX); \
		trap 'rm -f "$$thin_biber"' EXIT; \
		lipo "$(BIBER)" -thin "$$(uname -m)" -output "$$thin_biber"; \
		chmod +x "$$thin_biber"; \
		"$$thin_biber" $(BASENAME); \
	else \
		"$(BIBER)" $(BASENAME); \
	fi
	$(PDFLATEX) -interaction=nonstopmode -halt-on-error $(MAIN)
	$(PDFLATEX) -interaction=nonstopmode -halt-on-error $(MAIN)

force:
	rm -f $(PDF)
	$(MAKE) all

rebuild: clean all

clean:
	find . -type f \( -name '*.aux' -o -name '*.log' -o -name '*.out' -o -name '*.fls' -o -name '*.toc' -o -name '*.bbl*' -o -name '*.bcf*' -o -name '*.blg' -o -name '*.run.xml' -o -name '*.fdb_latexmk' -o -name '*.fls' -o -name '*.synctex*' \) -delete

view: $(PDF)
	open $(PDF)
