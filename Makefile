# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

include .env

.DEFAULT_GOAL=build

network:
	@docker network inspect $(DOCKER_NETWORK_NAME) >/dev/null 2>&1 || docker network create $(DOCKER_NETWORK_NAME)
	@docker network inspect $(DOCKER_NETWORK_NAME)-sub >/dev/null 2>&1 || docker network create $(DOCKER_NETWORK_NAME)-sub --internal

volumes:
	@docker volume inspect $(DATA_VOLUME_HOST) >/dev/null 2>&1 || docker volume create --name $(DATA_VOLUME_HOST)

self-signed-cert:
	# make a self-signed cert

#secrets/jupyterhub.crt:
#	@echo "Need an SSL certificate in secrets/jupyterhub.crt"
#	@exit 1
#
#secrets/jupyterhub.key:
#	@echo "Need an SSL key in secrets/jupyterhub.key"
#	@exit 1
#
userlist:
	@echo "Add usernames, one per line, to ./userlist, such as:"
	@echo "    zoe admin"
	@echo "    wash"
	@exit 1

# Do not require cert/key files if SECRETS_VOLUME defined
secrets_volume = $(shell echo $(SECRETS_VOLUME))
ifeq ($(secrets_volume),)
	cert_files=secrets/jupyterhub.crt secrets/jupyterhub.key
else
	cert_files=
endif

#check-files: userlist $(cert_files)
check-files: userlist

pull:
	docker pull $(DOCKER_NOTEBOOK_IMAGE)

notebook_image: pull

build: check-files network volumes
	docker-compose build

.PHONY: network volumes check-files pull notebook_image build
