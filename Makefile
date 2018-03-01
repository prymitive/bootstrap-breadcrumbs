%:
	@echo Testing Django==$@
	@docker build -q --build-arg DJANGO===$@ .
	@echo Done

all: $(shell grep DJANGO= .travis.yml | cut -d = -f2 | sort | uniq | tr '\n' ' ')
	@echo All tests completed
