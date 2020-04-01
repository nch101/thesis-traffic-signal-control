from nose.tools import *
import sys
sys.path.append('/home/huy/Documents/py-project')
import projectTS

def setup():
    print('SETUP!')

def teardown():
    print('TEAR DOWN!')

def test_basic():
    print('I RAN!')

