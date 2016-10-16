%:
	@echo Testing Django==$@
	@docker build -q --build-arg DJANGO===$@ .
	@echo Done

all: 1.5.12 1.6.11 1.7.11 1.8.15 1.9.10 1.10.2
	@echo All tests completed
