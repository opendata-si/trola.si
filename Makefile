NPM = npm
KANSO = node_modules/bin/kanso
BOWER = node_modules/bin/bower
LESSC = node_modules/bin/lessc
TARGETS = build/index.html

all:: $(TARGETS)

clean:
	rm -rf $(TARGETS)

bootstrap:
	mkdir -p build
	$(NPM) install kanso bower less --prefix=./node_modules -g
	$(KANSO) install
	$(BOWER) install

publish: all
	$(KANSO) push cloudant

build/app.js:
	# TODO
	$(JAM) compile -i app -e lessc $@

build/app.css:
	$(LESSC) less/app.less -x $@

build/index.html:
	cp index.html $@
	sed -i 's@<script src="jam/require.js"></script>@<link href="app.css" rel="stylesheet" type="text/css"/>\n<script src="app.js"></script>@g' $@
	sed -i 's@, "lessc!app.less"@@g' $@

build/img:
	mkdir -p $@
	cp img/* $@

.PHONY: all clean bootstrap publish
