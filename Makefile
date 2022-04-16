###########################
## Environment variables ##
###########################

export ALIAS = chess 		# must match name field in environment.yaml


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
	conda env update -n $(ALIAS) --file environment.yaml --prune /
		|| \
	conda env create --file environment.yaml

##############
## Packages ##
##############

packages:
	pip install -e src/
