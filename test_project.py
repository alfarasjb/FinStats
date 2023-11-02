
import pytest
from project import *
import pandas as pd


def test_download():
    samples = 10
    df = download('AAPL', samples)
    assert type(df) == pd.DataFrame
    assert df.shape[0] == samples

    with pytest.raises(ValueError):
        download('ASDFDF',12)

def test_build_data():
    samples = 10
    data, close = build_data('AAPL', samples)
    assert type(data) == dict
    assert type(close) == pd.Series 
    assert close.shape[0] == samples

    with pytest.raises(AssertionError):
        build_data('AAPL', 0)

def test_validate_entry():
    data = [('',''),('AAPL',''),('','10')]
    for d in data:
        print(d[0], d[1])
        with pytest.raises(ValueError):
            validate_entry(d[0], d[1])
    