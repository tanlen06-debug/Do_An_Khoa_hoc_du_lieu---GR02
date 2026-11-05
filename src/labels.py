"""Nhãn giao trễ ở cấp ngày lịch. Không đưa đầu ra hàm này làm feature."""

from __future__ import annotations

import pandas as pd


REQUIRED = {
    "order_status",
    "order_approved_at",
    "order_delivered_customer_date",
    "order_estimated_delivery_date",
}


def make_late_label(orders: pd.DataFrame) -> pd.Series:
    """Tạo nhãn nullable Int64: 1=trễ, 0=đúng hạn, NA=chưa xác định.

    Chỉ gán nhãn cho đơn delivered đã phê duyệt, có cả ngày giao thực
    và ngày dự kiến. Không suy luận kết quả cho đơn bị hủy/chưa giao.
    """
    missing = REQUIRED.difference(orders.columns)
    if missing:
        raise ValueError(f"Thiếu cột để tạo nhãn: {sorted(missing)}")
    actual = pd.to_datetime(orders["order_delivered_customer_date"], errors="coerce")
    estimated = pd.to_datetime(orders["order_estimated_delivery_date"], errors="coerce")
    approved = pd.to_datetime(orders["order_approved_at"], errors="coerce")
    eligible = (
        orders["order_status"].eq("delivered")
        & approved.notna() & actual.notna() & estimated.notna()
    )
    labels = pd.Series(pd.NA, index=orders.index, dtype="Int64", name="is_late")
    labels.loc[eligible] = (
        actual.loc[eligible].dt.normalize()
        > estimated.loc[eligible].dt.normalize()
    ).astype("int64")
    return labels
