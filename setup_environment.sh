REPO_NAME="resume-worth"


echo "Install pip using ensurepip and upgrade"
python -m ensurepip --upgrade
python -m pip install --upgrade pip


echo "Create and Activate Conda Environment"
conda create -n $REPO_NAME python=3.11 -y
conda activate $REPO_NAME


echo "Install Requirements"
pip install -r requirements_dev.in
pip install -r requirements.in
pip install -e .



# INSTRUCTION ABOUT THE PROJECT SET UP
#
# To set up the enrionment for the project, run:
#  
# sh setup_environment.sh 


# INSTRUCTIONS ABOUT REQUIREMENTS
#
# To generate requirements.in from the imports with the immediate dependencies, run:
# pip install pipreqs
# pipreqs --force --mode no-pin --savepath requirements.in
#
# To generate requirements.txt from requirements.in with ALL dependencies (immediate dependencies and their dependencies) and version, run:
# pip install pip-tools
# pip-compile -U --output-file requirements.txt requirements_dev.in requirements.in
