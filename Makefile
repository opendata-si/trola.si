NPM = npm
NODE = node
KANSO = cd build && ../node_modules/bin/kanso
BOWER = node_modules/bin/bower
LESSC = node_modules/bin/lessc
TARGETS = build/index.html build/app.css build/app.js

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
	$(NODE) components/r.js/dist/r.js -o build/build.js
	echo "require([\"../js/app\"]);" >> $@

build/app.css:
	$(LESSC) less/app.less -x $@

build/index.html:
	cp index.html $@
	sed -i 's@<link rel="stylesheet/less" type="text/less" href="less/app.less"/>@<link href="http://db.trola.si/_design/trola.si/app.css" rel="stylesheet" type="text/css"/>@g' $@
	sed -i 's@<script src="components/less.js/dist/less-1.3.3.min.js"></script>@@g' $@
	sed -i 's@<script data-main="js/main" src="components/requirejs/require.js"></script>@<script src="http://db.trola.si/_design/trola.si/app.js"></script>@g' $@

build/img:
	mkdir -p $@
	cp img/* $@

.PHONY: all clean bootstrap publish
