
import pytest
from .finstats import Calc, Event_Handler, Ops
import pandas as pd

## CALC ## 
def test_download():
    samples = 10
    c = Calc('AAPL', samples)
    df = c.download()
    assert type(df) == pd.DataFrame
    assert df.shape[0] == samples

    with pytest.raises(ValueError):
        c = Calc('AAAAAPL', 12).download()
        #c.download()

def test_build_data():
    samples = 10
    c = Calc('AAPL', samples)
    data, close = c.build_data()
    assert type(data) == dict
    assert type(close) == pd.Series 
    assert close.shape[0] == samples

    with pytest.raises(AssertionError):
        c = Calc('AAPL', 0).build_data()

    d, cl = Calc('AAAAAPL', 10).build_data()
    assert d == None 
    assert cl == None
## CALC ## 

## OPS ## 
def test_validate_entry():
    data = [('',''),('AAPL',''),('','10')]
    for d in data:
        with pytest.raises(ValueError):
            o = Ops(d[0], d[1]).validate_entry()
    
