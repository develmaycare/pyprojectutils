.PHONY: bash git

# This could be changed dynamically based on platform (below), but I generally
# only use Mac OS and Ubuntu and it is the same path in both cases.
LOCAL_BIN := /usr/local/bin

# Platform and processor detection.
ifeq ($(OS),Windows_NT)
	PLATFORM = WIN32
	ifeq ($(PROCESSOR_ARCHITECTURE),AMD64)
		PROCESSOR = AMD64
	endif
	ifeq ($(PROCESSOR_ARCHITECTURE),x86)
		PROCESSOR = IA32
	endif
else
	UNAME_S := $(shell uname -s)
	ifeq ($(UNAME_S),Linux)
		PLATFORM = LINUX
		BASHRC_PATH := $(HOME)/.bashrc
	endif
	ifeq ($(UNAME_S),Darwin)
		PLATFORM = OSX
		BASHRC_PATH := $(HOME)/.bash_profile
	endif

	UNAME_P := $(shell uname -p)
	ifeq ($(UNAME_P),x86_64)
		PROCESSOR = AMD64
	endif
	ifneq ($(filter %86,$(UNAME_P)),)
		PROCESSOR = IA32
	endif
	ifneq ($(filter arm%,$(UNAME_P)),)
		PROCESSOR = ARM
	endif
endif

# Attempt to load a local makefile which may override any of the values above.
-include custom.makefile

#> help - Show help.
help:
	@echo ""
	@echo "My Mac Development Directory"
	@echo "------------------------------------------------------------------------------"
	@#@cat Makefile | grep "^#>" | sed 's/\#\> //g' | sed 's: - :		 	:g'; # CTRL V CTRL I
	@cat Makefile | grep "^#>" | sed 's/\#\> //g';
	@echo ""
	@echo "Platform: $(PLATFORM) | Processor: $(PROCESSOR)"
	@echo "Bin: $(LOCAL_BIN) | Bash RC: $(BASHRC_PATH)"
	@echo "Support: $(SUPPORT_PATH) | Work: $(WORK_PATH)"
	@echo ""
	@if [[ $(PLATFORM) == "OSX" ]]; then echo "You may need to run this from the Mac OS Terminal app rather than iTerm 2."; fi;

#> bin - Install the bin directory and related command line scripts.
bin:
	test -d $(LOCAL_BIN) || mkdir -p $(LOCAL_BIN);

# Get a local copy of Twitter Bootstrap.
bootstrap:
	test -d $(RESOURCE_HOME)/bootstrap || mkdir -p $(RESOURCE_HOME)/bootstrap;
	cd $(RESOURCE_HOME)/bootstrap && git clone https://github.com/twbs/bootstrap.git .;

#> clean - Start fresh with the python and tmp directory.
clean:
	rm -Rf $(WORKON_HOME)/*;

# Code statistics and LOC counter. https://github.com/AlDanial/cloc
cloc:
	brew install cloc;

# Install cookiecutter. https://cookiecutter.readthedocs.io
cookiecutter:
	pip install cookiecutter;
	cp config/cookiecutterrc.yml $(HOME)/.cookiecutterrc;
	sed -i "" "s,{{ SUPPORT_PATH }},$(SUPPORT_PATH),g" $(HOME)/.cookiecutterrc;
	test -d $(SUPPORT_PATH)/cookiecutters || mkdir -p $(SUPPORT_PATH)/cookiecutters;
	test -d $(SUPPORT_PATH)/cookiecutters/.replays || mkdir -p $(SUPPORT_PATH)/cookiecutters/.replays;

# Install the dialog command line utility.
dialog:
	brew install dialog;

# Install the GhostScript library.
# BUG: There appears to be a problem with the GhostScript install.
ghostscript:
	brew install ghostscript;

# Git must be installed in order to use this package. This target simply
# finishes the configuration.
git:
	cp config/git/config.ini $(HOME)/.gitconfig;
	cp config/git/ignore.txt $(HOME)/.gitignore;

# Install the generic preprocessor.
gpp:
	brew install gpp;

# Install GraphViz.
graphviz:
	brew install graphviz;

# Install ImageMagick libraries and CLI utilities.
imagemagick:
	brew install imagemagick --with-libtiff;

#> install - Install everything (all targets).
install: skeletons bin utils python resources

# Download jQuery and related plugins.
jquery:
	test -d $(RESOURCE_HOME)/jquery/library || mkdir -p $(RESOURCE_HOME)/jquery/library;
	cd $(RESOURCE_HOME)/jquery/library && wget http://code.jquery.com/jquery-$(JQUERY_VERSION).min.js;

	test -d $(RESOURCE_HOME)/jquery/mobile || mkdir -p $(RESOURCE_HOME)/jquery/mobile;
	cd $(RESOURCE_HOME)/jquery/mobile && wget http://jquerymobile.com/resources/download/jquery.mobile-$(JQUERY_MOBILE_VERSION).zip
	cd $(RESOURCE_HOME)/jquery/mobile && unzip jquery.mobile-$(JQUERY_MOBILE_VERSION).zip;
	rm $(RESOURCE_HOME)/jquery/mobile/jquery.mobile-$(JQUERY_MOBILE_VERSION).zip;
	cd $(RESOURCE_HOME)/jquery/mobile && rename --subst jquery.mobile. mobile. *.*;
	cd $(RESOURCE_HOME)/jquery/mobile && rename --subst jquery.mobile- mobile. *.*;
	cd $(RESOURCE_HOME)/jquery/mobile && rename --subst -$(JQUERY_MOBILE_VERSION) "" *.*;
	cd $(RESOURCE_HOME)/jquery/mobile && rename --subst .$(JQUERY_MOBILE_VERSION) "" *.*;
	@echo $(JQUERY_MOBILE_VERSION) > $(RESOURCE_HOME)/jquery/mobile/VERSION.txt;

	test -d $(RESOURCE_HOME)/jquery/ui || mkdir -p $(RESOURCE_HOME)/jquery/ui;
	cd $(RESOURCE_HOME)/jquery/ui && wget http://jqueryui.com/resources/download/jquery-ui-$(JQUERY_UI_VERSION).zip;
	cd $(RESOURCE_HOME)/jquery/ui && unzip jquery-ui-$(JQUERY_UI_VERSION).zip;
	rm $(RESOURCE_HOME)/jquery/ui/jquery-ui-$(JQUERY_UI_VERSION).zip;
	cd $(RESOURCE_HOME)/jqueyr/ui && mv jquery-ui-$(JQUERY_UI_VERSION)/* .;
	cd $(RESOURCE_HOME)/jquery/ui && rename --subst jquery-ui ui *.*;
	@echo $(JQUERY_UI_VERSION) > $(RESOURCE_HOME)/jquery/ui/VERSION.txt;
	
	test -d $(RESOURCE_HOME)/jquery/plugins || mkdir -p $(RESOURCE_HOME)/jquery/plugins;
	# put plugin downloads here.

# Check out jQuery source.
jquery-source:
	test -d $(RESOURCE_HOME)/jquery/source/library || mkdir -p $(RESOURCE_HOME)/jquery/source/library;
	cd $(RESOURCE_HOME)/jquery/libary && git clone https://github.com/jquery/jquery.git .;
	test -d $(RESOURCE_HOME)/jquery/source/mobile || mkdir -p $(RESOURCE_HOME)/jquery/source/mobile;
	cd $(RESOURCE_HOME)/jquery/source/mobile && git clone https://github.com/jquery/jquery-mobile.git .;
	test -d $(RESOURCE_HOME)/jquery/source/ui || mkdir -p $(RESOURCE_HOME)/jquery/source/ui;
	cd $(RESOURCE_HOME)/jquery/ui && git clone https://github.com/jquery/jquery-ui.git .;	
	test -d $(RESOURCE_HOME)/jquery/source/plugins || mkdir -p $(RESOURCE_HOME)/jquery/source/plugins;

# Install the LFTP utility.
lftp:
	brew install lftp;
	lftp -c "set xfer:clobber on";
	test -d ~/.lftp || mkdir ~/.lftp;
	@if [[ -f ~/Dropbox/Apps/lftp/bookmarks ]]; then cd ~/.lftp && ln -s ~/Dropbox/Apps/lftp/bookmarks; fi;

# Install license generator. https://github.com/licenses/lice
lice:
	pip install lice

# Install Node.js and related utilities.
nodejs:
	brew install nodejs;
	npm install -g grunt-cli;
	npm install -g less;

# Install pandoc.
pandoc:
	brew install pandoc;
	brew install homebrew/tex/pdfjam;

# Install pelican plugins and themes.
pelican:
	test -d $(RESOURCE_HOME)/pelican || mkdir -p $(RESOURCE_HOME)/pelican;
	test -d $(RESOURCE_HOME)/pelican/plugins || mkdir -p $(RESOURCE_HOME)/pelican/plugins;
	cd $(RESOURCE_HOME)/pelican/plugins && git clone --recursive https://github.com/getpelican/pelican-plugins.git .;
	test -f $(RESOURCE_HOME)/pelican/plugins/__init__.py || touch $(RESOURCE_HOME)/pelican/plugins/__init__.py;
	test -d $(RESOURCE_HOME)/pelican/themes || mkdir -p $(RESOURCE_HOME)/pelican/themes;
	cd $(RESOURCE_HOME)/pelican/themes && git clone --recursive https://github.com/getpelican/pelican-themes.git .;

#> postgres - Install PostgreSQL.
postgres:
	brew install postgres;
	createuser --superuser postgres;

#> python - Set up the python development environment.
python:
	test -f /usr/local/bin/python || brew install python;
	pip install ipython;
	pip install pip2pi;
	pip install pyflakes;
	pip install pygments;
	pip install virtualenvwrapper;
	source /usr/local/bin/virtualenvwrapper.sh && mkvirtualenv --prompt="(Default) " default;
	make wagtail;

# Install a Linux-compatible rename command.
rename:
	brew install rename;

#> resources - Download resources such as Twitter Bootstrap and jQuery.
resources: bootstrap jquery pelican zurb

#> scripts - Copy various scripts to the appropriate location.
scripts:
	cp scripts/projectlist.py $(WORK_PATH)/;

#> skeletons - Create skeleton files and directories.
skeletons:
	test -d $(SUPPORT_PATH) || mkdir -p $(SUPPORT_PATH);
	cp -R skeletons/support/* $(SUPPORT_PATH)/;
	test -d $(WORK_PATH) || mkdir -p $(WORK_PATH);
	cp -R skeletons/work/* $(WORK_PATH)/;

# Install the tree command.
tree:
	brew install tree;

#> utils - Install devops utilities and libraries.
utils: ansible bash cloc dialog imagemagick git gpp graphviz lftp nodejs pandoc rename tree vim wget yaml

# Vagrant is installed from a DMG, but we can do plugins and completion here.
# Note that vagrant is NOT installed here.
vagrant:
	vagrant plugin install vagrant-fabric;
	vagrant plugin install vagrant-vbguest;

# Install vim for Mac.
vim:
	test -d $(HOME)/.vim || (cd $(HOME) && git clone git@bitbucket.org:bogeymin/mydotvim.git && mv mydotvim .vim);
	brew install ack;
	(cd $(HOME)/.vim && make install);
	brew install macvim --override-system-vim;
	brew linkapps macvim;

# Install a generic Python environment for Wagtail.
wagtail:
	cd $WORK_PATH && mkvirtualenv -a `pwd` -i wagtail -i wagtailmodelchooser --prompt="(Wagtail) " wagtail;

# Install the wget utility.
wget:
	brew install wget;

# Install the YAML library.
yaml:
	brew install libyaml;

# Install Zurb Foundation
zurb:
	cd $(RESOURCE_HOME)/foundation && git clone https://github.com/zurb/foundation.git .;

testing:
	@echo "I am testing. I am testing. I am testing. Testing 123."
