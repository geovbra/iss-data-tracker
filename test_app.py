import pytest
from app import no_load

def test_all_key_values():
    assert no_load() == 'Please perform a POST request to this route to properly load the data\n'
