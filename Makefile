NAME ?= geovbra
PORT ?= 5005

all: build run push

images:
	docker images | grep ${NAME}

ps:
	docker ps -a | grep ${NAME}

build:
	docker build -t ${NAME}/flask_iss_tracker:1.0 .

run:
	docker run --name "${NAME}_iss" -d -p ${PORT}:5000 ${NAME}/flask_iss_tracker:1.0

push:
	docker push ${NAME}/flask_iss_tracker:1.0

stop:
	docker stop ${NAME}_iss

rm:
	docker rm ${NAME}_iss