"""Giao diện khởi tạo cho Chương 6.

Chưa có mô hình: cố ý không phát sinh xác suất hoặc bảng cảnh báo giả.
"""
import streamlit as st

st.set_page_config(page_title="Nhóm 02 – Giao hàng trễ", layout="wide")
st.title("Phân tích đơn hàng & dự đoán nguy cơ giao hàng trễ")
st.caption("Đồ án thực tế Khoa học dữ liệu – Olist (Brazil, 2016–2018)")
st.info(
    "Đây là khung Dashboard. Chưa tích hợp dataset đã làm sạch, "
    "pipeline/mô hình được kiểm thử hoặc kết quả dự đoán."
)
tab1, tab2 = st.tabs(["Phân tích lịch sử – sẽ triển khai", "Cảnh báo ưu tiên – sẽ triển khai"])
with tab1:
    st.markdown("**Dự kiến:** số đơn, tỷ lệ giao trễ theo thời gian, khu vực, nhóm sản phẩm và người bán.")
with tab2:
    st.markdown(
        "**Dự kiến:** tải mô hình đã được chọn trên Validation, "
        "xếp hạng Top-K đơn có xác suất trễ cao nhất. "
        "Chỉ dùng feature biết tại `order_approved_at`."
    )
st.caption("Ứng dụng nghiên cứu và demo hồi cứu; không phải dịch vụ theo dõi giao hàng thời gian thực.")
