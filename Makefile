###########################
## Environment variables ##
###########################

export ALIAS = chess 		# must match name field in environment.yaml


export $(cat .env)
export TF_VAR_project_id = $(PROJECT_ID)
export TF_VAR_region = $(PROJECT_REGION)

export GOOGLE_APPLICATION_CREDENTIALS ?= ~/.gcp/gcp_credentials.json

export REPOSITORY_URL ?= https://${PROJECT_ID}-python.pkg.dev/${PROJECT_ID}/chess_scraper/

#############
## Install ##
#############

conda:
# conda env update 			-> update conda environment
# -n $(ALIAS) 				-> named ALIAS
# --file environment.yaml 	-> from file called environment.yaml
# --prune 					-> remove packages no longer listed in the .yaml file
# /							-> continue to new line
# || \ 						-> OR operation. If first line fails, run second line. If first line passes, stop.
# conda env create			-> create conda environment
# --file environment.yaml	-> from file called environment.yaml
	conda env update -n $(ALIAS) --file environment.yaml --prune \
		|| \
	conda env create --file environment.yaml

packages:
	pip install -e src/scraper


## Packages ##

build:
	cd src/scraper && rm -rf build/ dist/
	rm -rf src/**/__pycache__/

	cd src/scraper && python setup.py bdist_wheel
	cd src/scraper && python setup.py bdist --format zip
.PHONY: build

upload: 
	cd src/scraper && twine upload --skip-existing --repository-url ${REPOSITORY_URL} dist/*.whl

#############
## Testing ##
#############

tests:
	pytest src/scraper/tests/

################
## Formatting ##
################

format:
	black .


###############
## Terraform ##
###############


