all: commands

BUNDLE=build/plotly.js
OUT_DIR=docs
SCHEMA=test/plot-schema.json
REF_PAGES=ref_pages
THEME=theme

## material: rebuild with MkDocs using mkdocs-material and 'overrides' directory
material:
	mkdocs build -f mkdocs-material.yml

## vanilla: rebuild with MkDocs using 'theme' directory (our own)
vanilla:
	mkdocs build -f mkdocs-vanilla.yml

## pages: make all the pages
pages:
	python bin/gen.py \
	--out docs \
	--schema ${SCHEMA} \
	--stubs ${REF_PAGES} \
	--theme ${THEME}

## figure: generate docs for a figure (annotations.html)
figure:
	python bin/gen.py \
	--crash \
	--out docs \
	--schema ${SCHEMA} \
	--stubs ${REF_PAGES} \
	--theme ${THEME} \
	annotations.md

## global: generate docs for global (global.html)
global:
	python bin/gen.py \
	--crash \
	--out docs \
	--schema ${SCHEMA} \
	--stubs ${REF_PAGES} \
	--theme ${THEME} \
	global.md

## subplot: generate docs for a subplot (polar.html)
subplot:
	python bin/gen.py \
	--crash \
	--out docs \
	--schema ${SCHEMA} \
	--stubs ${REF_PAGES} \
	--theme ${THEME} \
	polar.md

## trace: generate docs for a trace (violin.html)
trace:
	python bin/gen.py \
	--crash \
	--out docs \
	--schema ${SCHEMA} \
	--stubs ${REF_PAGES} \
	--theme ${THEME} \
	violin.md

## stubs: make reference page stubs
stubs: ${SCHEMA}
	python bin/make_ref_pages.py \
	--pages ${REF_PAGES} \
	--schema ${SCHEMA} \
	--verbose

## validate: check the generated HTML
validate:
	@html5validator --root docs

## regenerate JavaScript schema
schema:
	npm run schema dist

## -------- : --------
## commands: show available commands
# Note: everything with a leading double '##' and a colon is shown.
commands:
	@grep -h -E '^##' ${MAKEFILE_LIST} \
	| sed -e 's/## //g' \
	| column -t -s ':'

## find-subplots: use jq to find subplot objects
find-subplots:
	@cat tmp/plot-schema-formatted.json | jq 'paths | select(.[length-1] == "_isSubplotObj")'

## lint: check code and project
lint:
	@ruff check bin

## clean: erase all generated content
clean:
	@find . -name '*~' -exec rm {} \;
	@rm -rf ${REF_PAGES} ${OUT_DIR}
