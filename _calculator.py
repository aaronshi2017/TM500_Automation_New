# test_example.py
import pytest

@pytest.fixture
def test_addition():
    assert 1 + 1 == 2

@pytest.fixture
def test_subtraction():
    assert 5 - 3 == 2

