# chess_scraper
A scraper to pull data from chess.com and run some analysis.

### First steps

1. Install make

run `sudo apt-get install build-essential` in the terminal. This will install uild-essential and allow you to run commands defined in the Makefile.

2. Install miniconda int your home directory

This code will operate out of a conda environment. 

First download Miniconda to your home directory:

`curl -sL "https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh"`

- curl -> a tool for transferring data from or to a server
- -s -> --silent (silent mode)
- -L -> --location (Follow redirects)

Then install and run through the prompts:

`bash  Miniconda3-latest-Linux-x86_64.sh`

Finally restart your terminal to excecute changes (or run `source ~/.bashrc`)

3. Create the conda environment

Run `conda init`
Run `make conda`

4. Activate the conda environment

`conda activate chess`

### Installing and running the chess scraper

1. Run `make packages` from command line.
This command runs `pip install -e src/`

The chess scraper is defined in the `src/` directory.

2. Run the scraper

`chess get-data -u {username} -f {output destination}`
