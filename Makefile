###########################
## Environment variables ##
###########################
include .env

export ALIAS = chess

export TF_VAR_project_id = $(PROJECT_ID)
export TF_VAR_region = $(PROJECT_REGION)

export GOOGLE_APPLICATION_CREDENTIALS ?= $(HOME)/.gcp/gcp_credentials.json

#############
## Install ##
#############

mamba:
	mamba env update -n $(ALIAS) --file environment.yaml --prune \
		|| \
	mamba env create --file environment.yaml

packages:
	pip install -e src/scraper/


#############
## Testing ##
#############

tests:
	pytest src/tests/

################
## Formatting ##
################

format:
	black .


################
## Deployment ##
################

build:
	sh scripts/add_scraper_to_gcf.sh src/scraper src/services/ingestor

clean:
	rm src/services/ingestor/*.whl
	rm src/services/ingestor/*.txt

terraform:
	cd infrastructure && terraform init && terraform apply -auto-approve

deploy: build terraform clean
