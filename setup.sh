#!/bin/sh

git clone https://github.com/ForgottenArbiter/spirecomm.git
python -m venv ./venv
source ./venv/bin/activate
pip install -r requirements.txt
cd spirecomm
python -m pip install .