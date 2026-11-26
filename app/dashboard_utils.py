"""Pure, testable helpers for GR02 Streamlit dashboard (no model training)."""
from __future__ import annotations

import hashlib
from pathlib import Path

import numpy as np
import pandas as pd

# The approved five-feature baseline in src/experiment.py (Ch3/Ch4 contract).
BASELINE_FEATURES = [
    "purchase_month_number", "purchase_weekday", "purchase_hour",
    "approval_delay_hours", "customer_state",
]
NUMERIC_FEATURES = BASELINE_FEATURES[:4]
MODEL_OWNERS = {"rf": "Ngọc Lan", "mlp": "Tấn Lên", "dummy": "Trúc Chi"}


def sha256_file(path: Path) -> str:
    sha = hashlib.sha256()
    with Path(path).open("rb") as source:
        for part in iter(lambda: source.read(1024 * 1024), b""):
            sha.update(part)
    return sha.hexdigest()


def prepare_eda_data(source: pd.DataFrame) -> pd.DataFrame:
    """Use labeled, one-order-per-row Ch3 data only for historical EDA."""
    required = {"order_id", "is_late", "order_purchase_timestamp", "customer_state"}
    missing = sorted(required - set(source.columns))
    if missing:
        raise ValueError(f"Dữ liệu EDA thiếu cột: {missing}")
    df = source.copy()
    if df["order_id"].isna().any() or not df["order_id"].is_unique:
        raise ValueError("Dữ liệu EDA phải có order_id không thiếu và duy nhất")
    label = pd.to_numeric(df["is_late"], errors="coerce")
    if label.isna().any() or not label.isin([0, 1]).all():
        raise ValueError("is_late phải là nhãn nhị phân 0/1, không thiếu")
    df["is_late"] = label.astype(int)
    df["purchase_datetime"] = pd.to_datetime(
        df["order_purchase_timestamp"], errors="coerce"
    )
    if df["purchase_datetime"].notna().sum() == 0:
        raise ValueError("Không có thời điểm đặt hàng hợp lệ để phân tích theo tháng")
    df["purchase_month"] = df["purchase_datetime"].dt.to_period("M").astype("string")
    df["customer_state"] = df["customer_state"].astype("string").fillna("Không rõ")
    if "total_price" in df.columns:
        df["total_price"] = pd.to_numeric(df["total_price"], errors="coerce")
    return df


def eda_kpis(df: pd.DataFrame) -> dict:
    n = len(df)
    late = int(df["is_late"].sum())
    return {"orders": n, "late": late, "late_rate": late / n if n else 0.0}


def eda_by_month(df: pd.DataFrame) -> pd.DataFrame:
    monthly = (
        df.dropna(subset=["purchase_month"])
        .groupby("purchase_month", as_index=False)
        .agg(orders=("order_id", "nunique"), late_orders=("is_late", "sum"))
        .sort_values("purchase_month")
    )
    monthly["late_rate"] = monthly["late_orders"] / monthly["orders"]
    return monthly


def eda_by_state(df: pd.DataFrame, min_orders: int = 30) -> pd.DataFrame:
    by_state = (
        df.groupby("customer_state", as_index=False)
        .agg(orders=("order_id", "nunique"), late_orders=("is_late", "sum"))
    )
    by_state = by_state.loc[by_state["orders"] >= min_orders].copy()
    by_state["late_rate"] = by_state["late_orders"] / by_state["orders"]
    return by_state.sort_values(["orders", "customer_state"], ascending=[False, True])


def eda_by_value(df: pd.DataFrame) -> pd.DataFrame:
    if "total_price" not in df.columns:
        return pd.DataFrame(columns=["value_group", "orders", "late_orders", "late_rate"])
    valid = df.loc[df["total_price"].notna()].copy()
    valid["value_group"] = pd.cut(
        valid["total_price"],
        [-np.inf, 50, 100, 200, 500, np.inf],
        labels=["≤50", "50–100", "100–200", "200–500", ">500"],
        right=True,
    )
    grouped = (
        valid.groupby("value_group", observed=True, as_index=False)
        .agg(orders=("order_id", "nunique"), late_orders=("is_late", "sum"))
    )
    grouped["late_rate"] = grouped["late_orders"] / grouped["orders"]
    return grouped


def validate_experiment_metadata(
    metadata: dict, split_metadata: dict, whitelist: list[str], dataset_sha256: str
) -> tuple[str, float]:
    """Reject incompatible champions/splits rather than silently guessing settings."""
    champion = metadata.get("champion")
    if champion not in {"rf", "mlp"}:
        raise ValueError("Champion phải là RF hoặc MLP đã chọn trên Validation")
    if metadata.get("prediction_time") != "order_approved_at":
        raise ValueError("Thời điểm dự đoán không khớp order_approved_at")
    if whitelist != BASELINE_FEATURES or metadata.get("features") != whitelist:
        raise ValueError("Feature whitelist và metadata mô hình không nhất quán")
    if metadata.get("model_owners", {}).get(champion) != MODEL_OWNERS[champion]:
        raise ValueError("Không xác minh được người huấn luyện champion")
    if not split_metadata.get("split_id") or metadata.get("split_id") != split_metadata["split_id"]:
        raise ValueError("split_id của champion không khớp split đã khóa")
    if split_metadata.get("csv_sha256") != dataset_sha256:
        raise ValueError("SHA256 dữ liệu model-ready khác phiên bản split đã khóa")
    if metadata.get("split_metadata", {}).get("csv_sha256") != dataset_sha256:
        raise ValueError("SHA256 dữ liệu trong experiment_metadata không khớp")
    threshold = metadata.get("chosen_threshold")
    from_validation = metadata.get("thresholds_from_val", {}).get(champion)
    try:
        threshold = float(threshold)
        from_validation = float(from_validation)
    except (TypeError, ValueError) as exc:
        raise ValueError("Thiếu ngưỡng champion đã chốt trên Validation") from exc
    if not (np.isfinite(threshold) and 0 <= threshold <= 1 and
            np.isclose(threshold, from_validation, atol=1e-12)):
        raise ValueError("Ngưỡng champion phải trùng ngưỡng từ Validation")
    return champion, threshold


def frozen_test_rows(df: pd.DataFrame, manifest: pd.DataFrame, test_n: int | None) -> pd.DataFrame:
    required = {"order_id", "split"}
    if not required.issubset(manifest.columns):
        raise ValueError("split_manifest.csv thiếu order_id hoặc split")
    if manifest["order_id"].isna().any() or manifest["order_id"].duplicated().any():
        raise ValueError("split_manifest.csv chứa order_id thiếu/trùng")
    selected = manifest.loc[manifest["split"] == "test", "order_id"].astype(str)
    if selected.empty or (test_n is not None and len(selected) != int(test_n)):
        raise ValueError("Số lượng đơn Test không khớp metadata")
    available = df.set_index(df["order_id"].astype(str), drop=False)
    missing = selected.loc[~selected.isin(available.index)]
    if len(missing):
        raise ValueError(f"Thiếu {len(missing)} đơn Test trong dữ liệu EDA")
    return available.loc[selected.to_list()].reset_index(drop=True)


def scoring_features(source: pd.DataFrame, whitelist: list[str]) -> pd.DataFrame:
    """Select ONLY approved t0 columns; labels and later timestamps never enter X."""
    required = ["order_id", *whitelist]
    missing = [col for col in required if col not in source.columns]
    if missing:
        raise ValueError(f"Thiếu cột scoring: {missing}")
    if source.empty or source["order_id"].isna().any() or not source["order_id"].is_unique:
        raise ValueError("Scoring cần tối thiểu một order_id duy nhất, không thiếu")
    if whitelist != BASELINE_FEATURES:
        raise ValueError("Chỉ chấp nhận 5 đặc trưng baseline đã duyệt")
    x = source.loc[:, whitelist].copy()
    for name in NUMERIC_FEATURES:
        original = x[name]
        cleaned = pd.to_numeric(original, errors="coerce")
        if (original.notna() & cleaned.isna()).any():
            raise ValueError(f"Biến {name} có giá trị không phải số")
        if np.isinf(cleaned.dropna().to_numpy(dtype=float)).any():
            raise ValueError(f"Biến {name} có Infinity")
        x[name] = cleaned
    for col, lower, upper in [
        ("purchase_month_number", 1, 12),
        ("purchase_weekday", 0, 6),
        ("purchase_hour", 0, 23),
    ]:
        if x[col].dropna().lt(lower).any() or x[col].dropna().gt(upper).any():
            raise ValueError(f"{col} nằm ngoài [{lower}, {upper}]")
    if x["approval_delay_hours"].dropna().lt(0).any():
        raise ValueError("approval_delay_hours không được âm")
    x["customer_state"] = x["customer_state"].astype("string")
    x.loc[x["customer_state"].str.strip() == "", "customer_state"] = pd.NA
    if x.isna().all(axis=1).any():
        raise ValueError("Có đơn không có bất kỳ đặc trưng hợp lệ nào")
    return x


def rank_top_k(
    source: pd.DataFrame, probabilities: np.ndarray, threshold: float, k: int
) -> pd.DataFrame:
    """Operational Top-K ranking, with no y_true/label in the output."""
    score = np.asarray(probabilities, dtype=float).ravel()
    if len(score) != len(source) or not len(score):
        raise ValueError("Số xác suất không khớp số đơn")
    if not np.isfinite(score).all() or ((score < 0) | (score > 1)).any():
        raise ValueError("Xác suất phải hữu hạn và thuộc [0, 1]")
    if not 1 <= int(k) <= len(score):
        raise ValueError("K phải nằm từ 1 đến số đơn được dự đoán")
    ranking = pd.DataFrame({
        "order_id": source["order_id"].astype(str).to_numpy(),
        "risk_probability": score,
    })
    ranking = ranking.sort_values(
        ["risk_probability", "order_id"], ascending=[False, True], kind="stable"
    ).head(int(k)).reset_index(drop=True)
    ranking.insert(0, "rank", np.arange(1, len(ranking) + 1))
    ranking["warning"] = np.where(
        ranking["risk_probability"] >= threshold, "Cảnh báo trễ", "Dưới ngưỡng"
    )
    return ranking
