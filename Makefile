.PHONY: bin

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
	@echo "Project Utils"
	@echo "------------------------------------------------------------------------------"
	@cat Makefile | grep "^#>" | sed 's/\#\> //g';
	@echo ""
	@echo "Platform: $(PLATFORM)"
	@echo "Processor: $(PROCESSOR)"
	@echo "Bin: $(LOCAL_BIN)"
	@echo "Bash RC: $(BASHRC_PATH)"
	@echo ""
	@if [[ $(PLATFORM) == "OSX" ]]; then echo "You may need to run this from the Mac OS Terminal app rather than iTerm 2."; fi;

#> bin - Install the bin directory and related command line scripts.
bin:
	test -d $(LOCAL_BIN) || mkdir -p $(LOCAL_BIN);
	cp bin/lsprojects.py $(LOCAL_BIN)/lsprojects;
	cp bin/randompw.py $(LOCAL_BIN)/randompw;
	cp bin/versionbump.py $(LOCAL_BIN)/versionbump;
