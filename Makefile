SYMBOL ?= BTC/USDT

build:
ifndef IMAGE_NAME
	$(error IMAGE_NAME is not set. Use `make build IMAGE_NAME=<image_name>`)
endif
	docker build -t $(IMAGE_NAME) .

push:
ifndef IMAGE_NAME
	$(error IMAGE_NAME is not set. Use `make push IMAGE_NAME=<image_name>`)
endif
	docker push $(IMAGE_NAME)

run:
	SYMBOL=$(SYMBOL) docker-compose up

dev:
	docker-compose up mongodb
