"""Kiểm thử chia tập đồng nhất và độ đo, dùng dữ liệu tổng hợp giả."""
import numpy as np
import pandas as pd
import pytest
from src.experiment import (SAFE_FEATURES, get_shared_splits,
                            classification_metrics, choose_threshold_on_validation,
                            precision_recall_at_k)


def test_split_replay_and_change_detection(tmp_path):
    n = 90
    approved = pd.date_range("2017-01-01", periods=n, freq="3D")
    df = pd.DataFrame({
        "order_id": [f"id{i:03}" for i in range(n)],
        "is_late": [i % 4 == 0 for i in range(n)],
        "order_approved_at": approved,
        "order_delivered_customer_date": approved + pd.Timedelta(days=1),
        "purchase_month_number": approved.month,
        "purchase_weekday": approved.dayofweek,
        "purchase_hour": np.zeros(n),
        "approval_delay_hours": np.ones(n),
        "customer_state": ["SP"] * n,
    })
    source = tmp_path / "orders_model_ready.csv"
    df.to_csv(source, index=False)
    first = get_shared_splits(tmp_path)
    second = get_shared_splits(tmp_path)
    assert first["metadata"]["split_id"] == second["metadata"]["split_id"]
    assert set(first["train"].order_id).isdisjoint(first["val"].order_id)
    assert set(first["val"].order_id).isdisjoint(first["test"].order_id)
    assert all(col in df.columns for col in SAFE_FEATURES)
    df.loc[0, "customer_state"] = "RJ"
    df.to_csv(source, index=False)
    with pytest.raises(ValueError, match="đã thay đổi"):
        get_shared_splits(tmp_path)


def test_metrics_and_topk():
    y = [1, 0, 1, 0]
    score = [.95, .2, .6, .1]
    result = classification_metrics(y, score, threshold=.5)
    assert result["TP"] == 2 and result["FP"] == 0
    assert result["FN"] == 0 and result["TN"] == 2
    assert result["AP"] == pytest.approx(1.0)
    assert 0.1 <= choose_threshold_on_validation(y, score)["threshold"] <= 0.9
    k = precision_recall_at_k(y, score, 2)
    assert k["Precision_at_K"] == 1 and k["Recall_at_K"] == 1
