"""Basic unit tests for the synthetic plastic transformer package."""

import pytest
import sys
from pathlib import Path

# Add src to path for testing
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))


def test_python_version():
    """Test that we're running a supported Python version."""
    assert sys.version_info >= (3, 8), "Python 3.8+ is required"


def test_imports():
    """Test that basic imports work."""
    try:
        import numpy as np
        import pandas as pd
        import torch
        assert True
    except ImportError as e:
        pytest.fail(f"Failed to import required package: {e}")


def test_torch_basic():
    """Test basic PyTorch functionality."""
    import torch
    
    # Test tensor creation
    x = torch.tensor([1.0, 2.0, 3.0])
    assert x.shape == (3,)
    assert x.dtype == torch.float32
    
    # Test basic operations
    y = x * 2
    expected = torch.tensor([2.0, 4.0, 6.0])
    assert torch.allclose(y, expected)


def test_numpy_basic():
    """Test basic NumPy functionality."""
    import numpy as np
    
    # Test array creation
    arr = np.array([1, 2, 3, 4, 5])
    assert arr.shape == (5,)
    assert arr.dtype == np.int64
    
    # Test basic operations
    result = np.mean(arr)
    assert result == 3.0


def test_pandas_basic():
    """Test basic Pandas functionality."""
    import pandas as pd
    
    # Test DataFrame creation
    df = pd.DataFrame({
        'a': [1, 2, 3],
        'b': [4, 5, 6]
    })
    
    assert df.shape == (3, 2)
    assert list(df.columns) == ['a', 'b']
    assert df['a'].sum() == 6


class TestMathOperations:
    """Test class for mathematical operations."""
    
    def test_addition(self):
        """Test addition operation."""
        assert 2 + 2 == 4
        assert 1 + 1 == 2
        assert 0 + 0 == 0
    
    def test_multiplication(self):
        """Test multiplication operation."""
        assert 2 * 3 == 6
        assert 5 * 0 == 0
        assert 1 * 7 == 7
    
    def test_division(self):
        """Test division operation."""
        assert 10 / 2 == 5
        assert 15 / 3 == 5
        
        # Test division by zero
        with pytest.raises(ZeroDivisionError):
            1 / 0


@pytest.mark.parametrize("input_val,expected", [
    (1, 1),
    (2, 4),
    (3, 9),
    (4, 16),
    (5, 25),
])
def test_square_function(input_val, expected):
    """Test a parameterized square function."""
    def square(x):
        return x * x
    
    assert square(input_val) == expected


def test_list_operations():
    """Test list operations."""
    test_list = [1, 2, 3, 4, 5]
    
    # Test list length
    assert len(test_list) == 5
    
    # Test list indexing
    assert test_list[0] == 1
    assert test_list[-1] == 5
    
    # Test list slicing
    assert test_list[1:3] == [2, 3]
    
    # Test list append
    test_list.append(6)
    assert test_list[-1] == 6
    assert len(test_list) == 6


def test_dictionary_operations():
    """Test dictionary operations."""
    test_dict = {'a': 1, 'b': 2, 'c': 3}
    
    # Test dictionary access
    assert test_dict['a'] == 1
    assert test_dict.get('b') == 2
    assert test_dict.get('d', 'default') == 'default'
    
    # Test dictionary keys and values
    assert set(test_dict.keys()) == {'a', 'b', 'c'}
    assert set(test_dict.values()) == {1, 2, 3}
    
    # Test dictionary update
    test_dict['d'] = 4
    assert test_dict['d'] == 4


@pytest.fixture
def sample_data():
    """Fixture providing sample data for tests."""
    return {
        'numbers': [1, 2, 3, 4, 5],
        'strings': ['hello', 'world', 'test'],
        'dict': {'key1': 'value1', 'key2': 'value2'}
    }


def test_fixture_usage(sample_data):
    """Test using a pytest fixture."""
    assert len(sample_data['numbers']) == 5
    assert 'hello' in sample_data['strings']
    assert sample_data['dict']['key1'] == 'value1'


if __name__ == "__main__":
    pytest.main([__file__]) 