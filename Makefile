###########################
## Environment variables ##
###########################
include .env

export ALIAS = chess 		# must match name field in environment.yaml

export TF_VAR_project_id = $(PROJECT_ID)
export TF_VAR_region = $(PROJECT_REGION)

export GOOGLE_APPLICATION_CREDENTIALS ?= ~/.gcp/gcp_credentials.json

export REPOSITORY_URL ?= https://${PROJECT_ID}-python.pkg.dev/${PROJECT_ID}/chess_scraper/

#############
## Install ##
#############

mamba:
# mamba env update 			-> update conda environment
# -n $(ALIAS) 				-> named ALIAS
# --file environment.yaml 	-> from file called environment.yaml
# --prune 					-> remove packages no longer listed in the .yaml file
# /							-> continue to new line
# || \ 						-> OR operation. If first line fails, run second line. If first line passes, stop.
# conda env create			-> create conda environment
# --file environment.yaml	-> from file called environment.yaml
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

all: build terraform