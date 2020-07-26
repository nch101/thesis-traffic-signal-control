from nose.tools import *
from projectTS.lib.getData import getData

def test_getData():
    tht = getData('https://localhost:3000/intersection/', '5ef5bd4d888fb71cd778a13c', '')
    tht.getData()

    assert_equal(tht.timeYellow, [3, 3, 3, 3])
    assert_equal(tht.quantity, 4)
    assert_equal(tht.deltaTime, 3)