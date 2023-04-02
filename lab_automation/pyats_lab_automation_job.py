#!/usr/bin/python3.6

import os
import sys
import re
import time
import argparse
#from pyats.easypy import task

from pyats.easypy import run
from pyats.datastructures.logic import And, Or, Not




test_script = '{}lab_auto_pyats.py'.format(os.environ['PEN_SYSTEST'])

parser = argparse.ArgumentParser(description='Required server creds')

parser.add_argument('--dev_u', required=True, type = str, help='dev username')
parser.add_argument('--dev_p', required=True, type = str,help='dev password')
parser.add_argument('--path', required=True, type = str,help='dev username')
parser.add_argument('--partition', required=True, type = str,help='dev password')
parser.add_argument('--devip', required=True, type = str,help='dev password')

args = parser.parse_args()

def main(runtime):
    start_time = time.time()
    # execute test
    run(testscript = test_script, runtime = runtime, username = args.dev_u,password = args.dev_p , destination_server = args.devip , dst_file_loc = args.path , src_file_loc = args.partition)
    print(f"Total time to execute the test suite: {time.time()-start_time} secs")