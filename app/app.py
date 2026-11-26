"""GR02 Olist Dashboard: retrospective EDA and read-only champion Top-K scoring.

Run from repository root: streamlit run app/app.py
No training, threshold tuning or Test label evaluation takes place here.
"""
from __future__ import annotations

import json
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
import streamlit as st

from dashboard_utils import (
    BASELINE_FEATURES,
    eda_by_month,
    eda_by_state,
    eda_by_value,
    eda_kpis,
    frozen_test_rows,
    prepare_eda_data,
    rank_top_k,
    scoring_features,
    sha256_file,
    validate_experiment_metadata,
)

ROOT = Path(__file__).resolve().parents[1]
PROCESSED = ROOT / "data" / "processed"
MODEL_READY = PROCESSED / "orders_model_ready.csv"
CHAMPION_MODEL = ROOT / "models" / "champion.joblib"
EXPERIMENT_METADATA = PROCESSED / "experiment_metadata.json"
SPLIT_METADATA = PROCESSED / "split_metadata.json"
SPLIT_MANIFEST = PROCESSED / "split_manifest.csv"
WHITELIST = PROCESSED / "feature_whitelist.json"

st.set_page_config(page_title="GR02 | Nguy cơ giao hàng trễ", layout="wide")
st.title("Phân tích đơn hàng và dự đoán nguy cơ giao hàng trễ")
st.caption("Olist Brazil 2016–2018 · Nghiên cứu hồi cứu tại order_approved_at · Nhóm 02")


@st.cache_data(show_spinner=False)
def read_model_ready(path: str, stamp: int) -> pd.DataFrame:
    del stamp
    return prepare_eda_data(pd.read_csv(path, dtype={"order_id": "string"}))


@st.cache_data(show_spinner=False)
def read_manifest(path: str, stamp: int) -> pd.DataFrame:
    del stamp
    return pd.read_csv(path, dtype={"order_id": "string"})


@st.cache_data(show_spinner=False)
def read_json(path: str, stamp: int):
    del stamp
    return json.loads(Path(path).read_text(encoding="utf-8"))


@st.cache_data(show_spinner=False)
def hash_dataset(path: str, stamp: int) -> str:
    del stamp
    return sha256_file(Path(path))


@st.cache_resource(show_spinner=False)
def load_champion(path: str, stamp: int):
    del stamp
    # Load ONLY trusted team-generated local joblib (pickle is unsafe for untrusted files).
    return joblib.load(path)


def cached_json(path: Path):
    return read_json(str(path), path.stat().st_mtime_ns)


def render_eda(df: pd.DataFrame | None) -> None:
    st.subheader("Trang 1 · Phân tích dữ liệu lịch sử (EDA)")
    if df is None:
        st.warning(
            "Chưa có data/processed/orders_model_ready.csv từ Chương 3. "
            "Hãy chạy notebook 03 hoặc nhận đúng file bàn giao. Không hiển thị KPI giả."
        )
        return
    st.caption("Chỉ thống kê các đơn có nhãn trong dữ liệu Model-Ready; 1 dòng = 1 order_id.")
    months = sorted(df["purchase_month"].dropna().astype(str).unique().tolist())
    states = sorted(df["customer_state"].dropna().unique().tolist())
    left, right = st.columns(2)
    with left:
        if len(months) >= 2:
            month_range = st.select_slider("Khoảng tháng đặt hàng", options=months,
                                           value=(months[0], months[-1]))
        else:
            month_range = (months[0], months[0]) if months else None
    with right:
        selected_states = st.multiselect("Lọc theo bang khách hàng (để trống = tất cả)", states)
    filtered = df.copy()
    if month_range:
        filtered = filtered.loc[
            filtered["purchase_month"].notna()
            & filtered["purchase_month"].between(*month_range)
        ]
    if selected_states:
        filtered = filtered.loc[filtered["customer_state"].isin(selected_states)]
    if filtered.empty:
        st.info("Không có đơn hàng thuộc các bộ lọc đang chọn.")
        return
    kpis = eda_kpis(filtered)
    c1, c2, c3 = st.columns(3)
    c1.metric("Đơn hàng có nhãn", f"{kpis['orders']:,}")
    c2.metric("Đơn giao trễ", f"{kpis['late']:,}")
    c3.metric("Tỷ lệ trễ", f"{kpis['late_rate']:.2%}")

    monthly = eda_by_month(filtered)
    if not monthly.empty:
        st.markdown("#### Đơn hàng và tỷ lệ trễ theo tháng")
        l, r = st.columns(2)
        with l:
            st.line_chart(monthly.set_index("purchase_month")["orders"])
        with r:
            st.line_chart((monthly.set_index("purchase_month")["late_rate"] * 100).rename("Tỷ lệ trễ (%)"))
        with st.expander("Xem số liệu theo tháng"):
            st.dataframe(monthly, hide_index=True, use_container_width=True)

    state_data = eda_by_state(filtered, min_orders=30)
    st.markdown("#### Tỷ lệ trễ theo bang khách hàng")
    if state_data.empty:
        st.info("Không có bang nào đủ 30 đơn trong phạm vi lọc để so sánh tỷ lệ.")
    else:
        shown = state_data.head(15).sort_values("late_rate", ascending=False)
        st.bar_chart((shown.set_index("customer_state")["late_rate"] * 100).rename("Tỷ lệ trễ (%)"))
        st.dataframe(shown, hide_index=True, use_container_width=True)
        st.caption("Chỉ hiển thị bang có ít nhất 30 đơn; tỷ lệ cao không đồng nghĩa quan hệ nhân quả.")

    by_value = eda_by_value(filtered)
    if not by_value.empty:
        st.markdown("#### Nhóm giá trị đơn hàng (BRL)")
        st.bar_chart((by_value.set_index("value_group")["late_rate"] * 100).rename("Tỷ lệ trễ (%)"))
        with st.expander("Xem bảng phân nhóm giá trị"):
            st.dataframe(by_value, hide_index=True, use_container_width=True)
    st.download_button("Xuất bảng thống kê theo tháng (CSV)",
                       monthly.to_csv(index=False).encode("utf-8-sig"),
                       "gr02_eda_monthly.csv", mime="text/csv")


def render_scoring(df: pd.DataFrame | None) -> None:
    st.subheader("Trang 2 · Dự đoán nguy cơ và ưu tiên Top-K")
    st.caption("Chỉ suy luận bằng champion đã chọn trên Validation; không fit lại hoặc đổi threshold.")
    needed = [CHAMPION_MODEL, EXPERIMENT_METADATA, SPLIT_METADATA, WHITELIST,
              MODEL_READY, SPLIT_MANIFEST]
    missing = [str(p.relative_to(ROOT)) for p in needed if not p.is_file()]
    if missing:
        st.warning("Chưa đủ artifact Chương 3/4, tạm khóa scoring. Thiếu: " + ", ".join(missing))
        return
    if df is None:
        st.warning("Không thể đọc dữ liệu Chương 3 để xác minh model champion.")
        return
    try:
        metadata = cached_json(EXPERIMENT_METADATA)
        split_meta = cached_json(SPLIT_METADATA)
        whitelist = cached_json(WHITELIST)
        if not isinstance(whitelist, list):
            raise ValueError("feature_whitelist.json cần là JSON array")
        dataset_hash = hash_dataset(str(MODEL_READY), MODEL_READY.stat().st_mtime_ns)
        champion, threshold = validate_experiment_metadata(
            metadata, split_meta, whitelist, dataset_hash
        )
        if whitelist != BASELINE_FEATURES:
            raise ValueError("Danh sách feature không khớp baseline của nhóm")
    except (OSError, ValueError, TypeError, KeyError, json.JSONDecodeError) as exc:
        st.error(f"Không thể xác minh nguồn gốc champion: {exc}")
        return
    st.success(f"Đã xác minh champion {champion.upper()}, split_id {metadata['split_id']}")
    st.caption(f"Ngưỡng cảnh báo cố định từ Validation: {threshold:.3f}. "
               "Top-K chỉ thay đổi số lượng đơn được ưu tiên theo năng lực vận hành.")

    mode = st.radio("Nguồn đầu vào", ["Frozen Test – chỉ minh họa xếp hạng",
                                         "CSV đặc trưng mới (không cần nhãn)"], horizontal=True)
    try:
        if mode.startswith("Frozen Test"):
            manifest = read_manifest(str(SPLIT_MANIFEST), SPLIT_MANIFEST.stat().st_mtime_ns)
            orders = frozen_test_rows(df, manifest, metadata.get("test_n"))
            st.info("Chỉ sử dụng đặc trưng tại t0; không công bố nhãn Test hoặc tính metric trong Dashboard.")
        else:
            uploaded = st.file_uploader("CSV có order_id và 5 đặc trưng whitelist", type=["csv"])
            if uploaded is None:
                st.info("Tải CSV đặc trưng để tiếp tục. Không sử dụng dữ liệu hậu giao làm đầu vào.")
                return
            orders = pd.read_csv(uploaded, dtype={"order_id": "string"})
            extra = [c for c in orders.columns if c not in {"order_id", *whitelist}]
            if extra:
                st.warning("Bỏ qua các cột ngoài whitelist: " + ", ".join(extra[:10]))
        x = scoring_features(orders, whitelist)
    except (OSError, ValueError, KeyError) as exc:
        st.error(f"Dữ liệu scoring không hợp lệ: {exc}")
        return

    try:
        model = load_champion(str(CHAMPION_MODEL), CHAMPION_MODEL.stat().st_mtime_ns)
        classes = np.asarray(model.classes_)
        positive = np.flatnonzero(classes == 1)
        if len(positive) != 1:
            raise ValueError("Pipeline champion không có đúng lớp dương is_late=1")
        prob = np.asarray(model.predict_proba(x))[:, int(positive[0])]
    except (Exception,) as exc:
        st.error(f"Không thể nạp hoặc tính xác suất bằng champion: {type(exc).__name__}: {exc}")
        return

    k = (1 if len(orders) == 1 else st.slider(
        "Số đơn ưu tiên K", min_value=1, max_value=len(orders),
        value=min(100, len(orders)), step=1
    ))
    try:
        ranked = rank_top_k(orders, prob, threshold, k)
    except ValueError as exc:
        st.error(str(exc))
        return
    a, b, c = st.columns(3)
    a.metric("Số đơn được dự đoán", f"{len(orders):,}")
    b.metric("Đơn ưu tiên", f"{len(ranked):,}")
    c.metric("Ưu tiên vượt ngưỡng", f"{(ranked['warning'] == 'Cảnh báo trễ').sum():,}")
    st.dataframe(ranked, hide_index=True, use_container_width=True)
    st.download_button("Tải danh sách Top-K (CSV)",
                       ranked.to_csv(index=False).encode("utf-8-sig"),
                       "gr02_champion_topk.csv", mime="text/csv")
    st.caption("Điểm nguy cơ là ước lượng của mô hình, chưa chắc đã được hiệu chuẩn. "
               "Bảng này không hiển thị y_true, TP/FP hay kết quả đánh giá Test.")


try:
    data = read_model_ready(str(MODEL_READY), MODEL_READY.stat().st_mtime_ns) if MODEL_READY.is_file() else None
except (OSError, ValueError, pd.errors.ParserError) as exc:
    st.error(f"Không đọc được dữ liệu Model-Ready: {exc}")
    data = None

eda_tab, scoring_tab = st.tabs(["📊 Phân tích lịch sử (EDA)", "🎯 Dự đoán & Top-K"])
with eda_tab:
    render_eda(data)
with scoring_tab:
    render_scoring(data)
st.caption("Nguyên mẫu học thuật – mô phỏng hồi cứu, không phải hệ thống vận hành realtime.")
