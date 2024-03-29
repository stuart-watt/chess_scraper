# chess_scraper
A scraper to pull data from chess.com and run some analysis.

### First steps

1. Install make

run `sudo apt-get install build-essential` in the terminal. This will install build-essential and allow you to run commands defined in the Makefile.

2. Install miniconda into your home directory

This code will operate out of a conda environment. First download Miniconda to your home directory:

`curl -sL "https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh"`

- curl -> a tool for transferring data from or to a server
- -s -> --silent (silent mode)
- -L -> --location (Follow redirects)

Then install and run through the prompts:

`bash  Miniconda3-latest-Linux-x86_64.sh`

Finally restart your terminal to excecute changes (or run `source ~/.bashrc`)

Install mamba.

3. Create the conda environment

Run `conda init`
Run `make mamba` (This repo uses mamba to solve environment as it is quicker)

4. Activate the conda environment

`conda activate chess`

### Install terraform

This repo will also use terraform for infrastructure provisioning. You will need to install it.

1. Follow the manual insallation at
https://learn.hashicorp.com/tutorials/terraform/install-cli

*you may require wget to follow the installation on a linux machine. Run `sudo apt-get install wget` to install it if needed*

### Installing and running the chess scraper

1. Run `make packages` from command line.
This command runs `pip install -e src/scraper/`

The chess scraper is defined in the `src/scraper/` directory.

2. Run the scraper

`chess_scraper -u {username} -f {output destination}`
