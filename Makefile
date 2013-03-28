NPM = npm
KANSO = cd build && ../node_modules/bin/kanso
BOWER = node_modules/bin/bower
LESSC = node_modules/bin/lessc
TARGETS = build/index.html build/app.css

all:: clean $(TARGETS)

clean:
	rm -rf $(TARGETS)

bootstrap:
	$(NPM) install kanso bower less --prefix=./node_modules -g
	$(BOWER) install
	$(KANSO) install

publish: all
	$(KANSO) push cloudant

build/app.js:
	# TODO
	$(JAM) compile -i app -e lessc $@

build/app.css:
	$(LESSC) less/app.less -x $@

build/index.html:
	cp index.html $@
	sed -i 's@<link rel="stylesheet/less" type="text/less" href="less/app.less"/>@<link href="app.css" rel="stylesheet" type="text/css"/>@g' $@
	sed -i 's@<script src="jam/require.js"></script>@<link href="app.css" rel="stylesheet" type="text/css"/>\n<script src="app.js"></script>@g' $@
	sed -i 's@, "lessc!app.less"@@g' $@

build/img:
	mkdir -p $@
	cp img/* $@

.PHONY: all clean bootstrap publish
