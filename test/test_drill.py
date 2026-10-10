from drill import average

def test_average_normal():
    assert average(60,3)==20

def test_average_empty():
    assert average(0,0) == 0.0