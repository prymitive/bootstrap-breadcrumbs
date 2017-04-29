%:
	@echo Testing Django==$@
	@docker build -q --build-arg DJANGO===$@ .
	@echo Done

all: 1.8.18 1.107 1.11
	@echo All tests completed
