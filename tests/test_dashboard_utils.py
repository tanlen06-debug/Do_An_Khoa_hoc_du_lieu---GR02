"""Dashboard contract checks: no Olist data/model artifact required for CI."""

import numpy as np
import pandas as pd
import pytest

from app.dashboard_utils import (
    BASELINE_FEATURES, eda_by_month, eda_by_state, eda_by_value, eda_kpis,
    frozen_test_rows, prepare_eda_data, rank_top_k, scoring_features,
    validate_experiment_metadata,
)


def example_data():
    return pd.DataFrame({
        "order_id": ["a", "b", "c", "d"],
        "is_late": [1, 0, 1, 0],
        "order_purchase_timestamp": ["2018-01-01", "2018-01-15", "2018-02-02", "2018-02-14"],
        "purchase_month_number": [1, 1, 2, 2],
        "purchase_weekday": [0, 0, 4, 2],
        "purchase_hour": [9, 10, 11, 12],
        "approval_delay_hours": [1.5, 0, 3, 2],
        "customer_state": ["SP", "SP", "RJ", "RJ"],
        "total_price": [25, 50, 130, 720],
        "review_score": [1, 5, 1, 5],  # Later information NEVER enters X
        "order_delivered_customer_date": ["2018-01-05"] * 4,
    })


def valid_meta():
    split = {"split_id": "split-123", "csv_sha256": "abcdef"}
    experiment = {
        "champion": "rf", "prediction_time": "order_approved_at",
        "split_id": "split-123", "features": BASELINE_FEATURES.copy(),
        "model_owners": {"rf": "Ngọc Lan", "mlp": "Tấn Lên", "dummy": "Trúc Chi"},
        "split_metadata": split.copy(),
        "thresholds_from_val": {"rf": 0.25, "mlp": 0.10},
        "chosen_threshold": 0.25, "test_n": 2,
    }
    return experiment, split


def test_eda_statistics_are_order_level():
    eda = prepare_eda_data(example_data())
    assert eda_kpis(eda) == {"orders": 4, "late": 2, "late_rate": 0.5}
    months = eda_by_month(eda)
    assert months["orders"].tolist() == [2, 2]
    assert months["late_rate"].tolist() == [0.5, 0.5]
    by_state = eda_by_state(eda, min_orders=1)
    assert set(by_state["customer_state"]) == {"SP", "RJ"}
    assert eda_by_state(eda).empty  # Small groups are not advertised as reliable.
    by_value = eda_by_value(eda)
    assert int(by_value["orders"].sum()) == 4


def test_eda_rejects_duplicate_orders_and_invalid_labels():
    duplicated = pd.concat([example_data(), example_data().iloc[[0]]])
    with pytest.raises(ValueError, match="duy nhất"):
        prepare_eda_data(duplicated)
    invalid = example_data()
    invalid.loc[0, "is_late"] = 3
    with pytest.raises(ValueError, match="nhị phân"):
        prepare_eda_data(invalid)


def test_metadata_checks_split_hash_features_and_validation_threshold():
    meta, split = valid_meta()
    assert validate_experiment_metadata(meta, split, BASELINE_FEATURES.copy(), "abcdef") == ("rf", 0.25)
    with pytest.raises(ValueError, match="SHA256"):
        validate_experiment_metadata(meta, split, BASELINE_FEATURES.copy(), "wrong")
    bad = dict(meta, chosen_threshold=0.5)
    with pytest.raises(ValueError, match="Validation"):
        validate_experiment_metadata(bad, split, BASELINE_FEATURES.copy(), "abcdef")
    bad = dict(meta, champion="dummy")
    with pytest.raises(ValueError, match="Champion"):
        validate_experiment_metadata(bad, split, BASELINE_FEATURES.copy(), "abcdef")
    bad = dict(meta, features=["review_score"])
    with pytest.raises(ValueError, match="whitelist"):
        validate_experiment_metadata(bad, split, BASELINE_FEATURES.copy(), "abcdef")


def test_frozen_test_selection_uses_only_manifest_members():
    source = prepare_eda_data(example_data())
    manifest = pd.DataFrame({"order_id": ["c", "b", "a", "d"],
                             "split": ["test", "val", "train", "test"]})
    selected = frozen_test_rows(source, manifest, test_n=2)
    assert selected["order_id"].tolist() == ["c", "d"]
    with pytest.raises(ValueError, match="Số lượng"):
        frozen_test_rows(source, manifest, test_n=3)


def test_scoring_only_uses_whitelisted_columns_and_validates_ranges():
    source = example_data()
    features = scoring_features(source, BASELINE_FEATURES.copy())
    assert features.columns.tolist() == BASELINE_FEATURES
    assert "is_late" not in features and "review_score" not in features
    bad = source.copy()
    bad.loc[0, "approval_delay_hours"] = -1
    with pytest.raises(ValueError, match="không được âm"):
        scoring_features(bad, BASELINE_FEATURES.copy())
    bad = source.copy()
    bad["purchase_hour"] = bad["purchase_hour"].astype(object)
    bad.loc[0, "purchase_hour"] = "broken"
    with pytest.raises(ValueError, match="không phải số"):
        scoring_features(bad, BASELINE_FEATURES.copy())


def test_topk_ranking_ties_and_label_leakage():
    source = example_data()
    result = rank_top_k(source, np.array([0.2, 0.9, 0.9, 0.5]), 0.6, 3)
    assert result["order_id"].tolist() == ["b", "c", "d"]
    assert result["warning"].tolist() == ["Cảnh báo trễ", "Cảnh báo trễ", "Dưới ngưỡng"]
    assert "is_late" not in result.columns
    assert "review_score" not in result.columns
    with pytest.raises(ValueError, match="Xác suất"):
        rank_top_k(source, [0.2, 0.9, np.nan, 0.5], 0.6, 3)
    with pytest.raises(ValueError, match="K phải"):
        rank_top_k(source, [0.2, 0.9, 0.9, 0.5], 0.6, 5)
