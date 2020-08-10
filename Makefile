rundev:
	python ./src/proxy.py

build:
	docker build -t proxyserver .

run:
	docker run -p 8000:8000 proxyserver