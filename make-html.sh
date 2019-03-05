#!/bin/bash
# source /cvmfs/atlas.cern.ch/repo/ATLASLocalRootBase/user/atlasLocalSetup.sh
# lsetup python
export PATH=/eos/user/p/pgadow/www/gridwatch/python/bin/:$PATH
export PYTHONPATH=/eos/user/p/pgadow/www/gridwatch/python/lib/python2.7/
cd /eos/user/p/pgadow/www/gridwatch/ && /bin/env python make-html.py
