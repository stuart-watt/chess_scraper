###########################
## Environment variables ##
###########################
export ALIAS = chess 


#############
## Install ##
#############
conda:
	conda env update -n $(ALIAS) --file environment.yaml --prune /
		|| \
	conda env create --file environment.yaml
