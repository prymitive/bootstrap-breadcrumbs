%:
	@echo Testing Django==$@
	@docker build -q --build-arg DJANGO===$@ .
	@echo Done

all: 1.8.18 1.10.8 1.11.7 2.0rc1
	@echo All tests completed
