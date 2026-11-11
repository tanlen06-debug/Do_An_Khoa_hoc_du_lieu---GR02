"""Giao thức thực nghiệm dùng chung cho RF (Ngọc Lan), Dummy/MLP (Trúc Chi).

Tạo split duy nhất trên order_approved_at. Đây KHÔNG phải training script.
Dữ liệu processed và manifest là artifact nội bộ, không commit lên GitHub.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.metrics import (average_precision_score, confusion_matrix,
                             f1_score, precision_score, recall_score)

NUMERIC_FEATURES = [
    "purchase_month_number", "purchase_weekday",
    "purchase_hour", "approval_delay_hours",
]
CATEGORY_FEATURES = ["customer_state"]
SAFE_FEATURES = NUMERIC_FEATURES + CATEGORY_FEATURES
PROTOCOL_VERSION = "gr02-temporal-v2"
THRESHOLDS = np.linspace(0.10, 0.90, 17)


def get_shared_splits(processed_dir: Path) -> dict:
    """Sử dụng chung một dữ liệu/split cho tất cả mô hình.

    Tạo split_manifest.csv / split_metadata.json ở lần đầu. Sau đó kiểm tra
    fingerprint và danh sách order_id; nếu dữ liệu đổi, báo lỗi để nhóm chốt lại.
    """
    processed_dir = Path(processed_dir)
    path = processed_dir / "orders_model_ready.csv"
    if not path.exists():
        raise FileNotFoundError(
            "Thiếu orders_model_ready.csv từ Lam Linh (notebook 03). "
            "Hãy tải/chuẩn bị dữ liệu đúng hợp đồng Ch3."
        )
    raw_hash = hashlib.sha256(path.read_bytes()).hexdigest()
    df = pd.read_csv(path)
    must = {"order_id", "is_late", "order_approved_at", "order_delivered_customer_date"}
    must |= set(SAFE_FEATURES)
    missing = sorted(must - set(df.columns))
    if missing:
        raise ValueError(f"Thiếu cột dữ liệu chung: {missing}")
    if df["order_id"].isna().any() or df["order_id"].duplicated().any():
        raise ValueError("Dữ liệu sau merge phải có order_id unique, không null")
    df["order_approved_at"] = pd.to_datetime(df["order_approved_at"], errors="coerce")
    df["order_delivered_customer_date"] = pd.to_datetime(
        df["order_delivered_customer_date"], errors="coerce"
    )
    df["is_late"] = pd.to_numeric(df["is_late"], errors="coerce")
    df = df.loc[
        df["order_approved_at"].notna()
        & df["order_delivered_customer_date"].notna()
        & df["is_late"].isin([0, 1])
    ].sort_values(["order_approved_at", "order_id"]).reset_index(drop=True)
    if len(df) < 30:
        raise ValueError("Dữ liệu có nhãn quá ít để chia 3 tập")
    a, b = int(len(df) * 0.70), int(len(df) * 0.85)
    raw_train, raw_val, test = df.iloc[:a], df.iloc[a:b], df.iloc[b:]
    validation_start = raw_val["order_approved_at"].min()
    test_start = test["order_approved_at"].min()

    # Label maturity: không học bằng kết quả chưa xảy ra tại thời điểm cutoff.
    train = raw_train.loc[
        raw_train["order_delivered_customer_date"] < validation_start
    ].copy()
    val = raw_val.loc[
        raw_val["order_delivered_customer_date"] < test_start
    ].copy()
    test = test.copy()
    if min(len(train), len(val), len(test)) <= 0:
        raise ValueError("Một tập bị rỗng sau lọc nhãn trưởng thành; kiểm tra cutoff")
    if train["is_late"].nunique() != 2 or val["is_late"].nunique() != 2:
        raise ValueError("Train/Validation thiếu lớp dương hoặc âm")
    if not (train.order_id.is_unique and val.order_id.is_unique and test.order_id.is_unique):
        raise ValueError("Trùng order_id trong split")
    if set(train.order_id) & set(val.order_id) or set(train.order_id) & set(test.order_id) or set(val.order_id) & set(test.order_id):
        raise ValueError("Order xuất hiện ở nhiều tập")

    manifest = pd.concat(
        [part[["order_id"]].assign(split=name) for name, part in
         [("train", train), ("validation", val), ("test", test)]],
        ignore_index=True,
    )
    spec = {
        "protocol": PROTOCOL_VERSION, "csv_sha256": raw_hash,
        "features": SAFE_FEATURES,
        "validation_start": validation_start.isoformat(),
        "test_start": test_start.isoformat(),
        "n_train": len(train), "n_validation": len(val), "n_test": len(test),
        "excluded_train_unmatured": len(raw_train)-len(train),
        "excluded_validation_unmatured": len(raw_val)-len(val),
    }
    split_id = hashlib.sha256(json.dumps(spec, sort_keys=True).encode()).hexdigest()[:20]
    spec["split_id"] = split_id
    manifest_file = processed_dir / "split_manifest.csv"
    metadata_file = processed_dir / "split_metadata.json"
    if manifest_file.exists() != metadata_file.exists():
        raise ValueError("Thiếu một trong hai file split, yêu cầu Trúc Chi kiểm tra")
    if metadata_file.exists():
        previous = json.loads(metadata_file.read_text(encoding="utf-8"))
        previous_manifest = pd.read_csv(manifest_file)
        if previous != spec or not previous_manifest.equals(manifest):
            raise ValueError(
                "Dữ liệu/split đã thay đổi so với bản nhóm chốt. "
                "KHÔNG tự sửa file manifest; trao đổi với Trúc Chi và Tấn Lên."
            )
    else:
        processed_dir.mkdir(parents=True, exist_ok=True)
        manifest.to_csv(manifest_file, index=False)
        metadata_file.write_text(json.dumps(spec, indent=2, ensure_ascii=False), encoding="utf-8")
    return {"train": train, "val": val, "test": test, "metadata": spec}


def classification_metrics(y_true, y_score, threshold: float) -> dict:
    y = np.asarray(y_true, dtype=int)
    scores = np.asarray(y_score, dtype=float)
    if not np.isfinite(scores).all() or not ((0 <= scores) & (scores <= 1)).all():
        raise ValueError("Xác suất phải trong [0,1]")
    predicted = (scores >= threshold).astype(int)
    tn, fp, fn, tp = confusion_matrix(y, predicted, labels=[0, 1]).ravel()
    return {
        "AP": float(average_precision_score(y, scores)),
        "precision": float(precision_score(y, predicted, zero_division=0)),
        "recall": float(recall_score(y, predicted, zero_division=0)),
        "f1": float(f1_score(y, predicted, zero_division=0)),
        "TP": int(tp), "FP": int(fp), "FN": int(fn), "TN": int(tn),
        "threshold": float(threshold),
    }


def choose_threshold_on_validation(y_true, y_score) -> dict:
    """Chỉ dùng Validation. Chọn F1 lớn nhất, hòa thì ít FP hơn."""
    candidates = [classification_metrics(y_true, y_score, float(t)) for t in THRESHOLDS]
    return sorted(candidates, key=lambda item: (-item["f1"], item["FP"], item["threshold"]))[0]


def precision_recall_at_k(y_true, y_score, k: int) -> dict:
    y, score = np.asarray(y_true, dtype=int), np.asarray(y_score, dtype=float)
    if not 1 <= k <= len(y):
        raise ValueError("K nằm trong khoảng 1..N")
    top = np.argsort(-score, kind="stable")[:k]
    tp = int(y[top].sum())
    return {
        "K": k, "TP_at_K": tp, "FP_at_K": k - tp,
        "Precision_at_K": tp / k,
        "Recall_at_K": tp / int(y.sum()) if y.sum() else 0.0
    }
