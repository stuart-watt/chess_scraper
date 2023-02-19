INPATH=${1}
OUTPATH=${2}
CWD=${PWD}

# Build package
cd ${INPATH}
python setup.py bdist_wheel
cd ${CWD}

# copy .whl to GCF service
	cp ${INPATH}/dist/*.whl ${OUTPATH}

# Add whl to requirrements in GCF service
cd ${OUTPATH}
for file in *.whl; do 
  echo "./${file}" >> requirements.txt 
done
cd ${CWD}