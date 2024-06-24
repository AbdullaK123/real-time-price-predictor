build:
	docker build -t trade-producer .
run: build
	docker run -d --network=redpanda_network trade-producer