import os
import sys
import re
import time
#from pyats.easypy import task

from pyats.easypy import run
from pyats.datastructures.logic import And, Or, Not
test_script = '{}vrfrequests.py'.format(os.environ['PEN_SYSTEST'])

def main(runtime):
    start_time = time.time()
    # execute test
    run(testscript = test_script, runtime = runtime)
    print(f"Total time to execute the test suite: {time.time()-start_time} secs")
