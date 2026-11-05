import pandas as pd

from src.labels import make_late_label


def test_calendar_date_rule_and_missing_outcome():
    orders = pd.DataFrame({
        "order_status": ["delivered", "delivered", "delivered", "canceled"],
        "order_approved_at": ["2018-01-01"] * 4,
        "order_estimated_delivery_date": ["2018-01-10"] * 4,
        "order_delivered_customer_date": [
            "2018-01-10 22:30:00",  # cùng ngày => đúng hạn
            "2018-01-11 00:10:00",  # ngày sau => trễ
            None,  # thiếu ngày thực => NA
            "2018-01-12",  # canceled => NA
        ],
    })
    result = make_late_label(orders)
    assert result.iloc[0] == 0
    assert result.iloc[1] == 1
    assert pd.isna(result.iloc[2])
    assert pd.isna(result.iloc[3])
