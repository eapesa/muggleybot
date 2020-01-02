#!/bin/bash

echo "[install]
prefix=" > ~/.pydistutils.cfg
pip3 install -r requirements.txt --target ./lib

AWS_PROFILE=asurion-poc.solutionengg sls deploy