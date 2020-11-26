#!/bin/bash -e
set -x
WS_DIR=~/ws

PYTHON_VER=python3.7
PROJECT_NAME='github_actions_demo'
VENV_DIR=$WS_DIR/venv
ENV_NAME=$VENV_DIR"/"$PROJECT_NAME

virtualenv -p $PYTHON_VER $ENV_NAME
source $ENV_NAME/bin/activate

pip install -r requirements.txt

pip freeze > docs/$PROJECT_NAME.env

# This will add/update the environment version based on setup/__init__.py
python setup.py
