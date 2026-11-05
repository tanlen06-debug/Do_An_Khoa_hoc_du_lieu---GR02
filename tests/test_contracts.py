import pandas as pd
import pytest

from src.contracts import assert_unique_orders


def test_one_order_per_row_passes():
    assert_unique_orders(pd.DataFrame({"order_id": ["a", "b"]}))


def test_duplicate_order_fails():
    with pytest.raises(ValueError, match="nhân bản"):
        assert_unique_orders(pd.DataFrame({"order_id": ["a", "a"]}))


def test_missing_order_id_fails():
    with pytest.raises(ValueError, match="rỗng"):
        assert_unique_orders(pd.DataFrame({"order_id": ["a", None]}))
