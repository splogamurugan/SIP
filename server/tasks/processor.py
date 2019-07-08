import time
import sys
from os import path
sys.path.append(path.join(path.dirname(path.abspath(__file__)), 'jobs'))
from JobsSpecs import JobsSpecs

def processor(job_handler, arguments:dict):
    j = JobsSpecs()
    res = j.handle(name=job_handler, **arguments)
    return res
