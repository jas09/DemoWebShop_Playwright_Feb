import pytest


@pytest.fixture
def preWork():
    print("test setup")

def test_basics(preWork):
    print("test case execution")