"""Các kiểm tra cơ bản cho bảng dữ liệu cấp order_id."""

from __future__ import annotations

import pandas as pd


def assert_unique_orders(frame: pd.DataFrame, order_column: str = "order_id") -> None:
    """Yêu cầu một hàng mỗi order_id; raise khi thiếu hoặc nhân bản."""
    if order_column not in frame.columns:
        raise ValueError(f"Thiếu cột khóa: {order_column}")
    if frame[order_column].isna().any():
        raise ValueError("order_id không được rỗng")
    duplicated = frame[order_column].duplicated()
    if duplicated.any():
        raise ValueError(f"Có {int(duplicated.sum())} order_id bị nhân bản")
