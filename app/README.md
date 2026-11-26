# Dashboard Streamlit – GR02 (Chương 6)

## Chức năng

1. **EDA lịch sử:** KPI số đơn có nhãn, số/tỷ lệ giao trễ, đơn hàng và tỷ lệ trễ theo tháng; tỷ lệ trễ theo bang (chỉ nhóm từ 30 đơn); tỷ lệ trễ theo nhóm giá trị đơn nếu dữ liệu có `total_price`. Bộ lọc tháng và bang.
2. **Champion scoring + Top-K:** Nạp `champion.joblib` **đã huấn luyện** ở Chương 4. Đối chiếu `split_id`, SHA256 của `orders_model_ready.csv`, 5 feature whitelist, chủ mô hình và ngưỡng chọn trên Validation. Chỉ tính `predict_proba()` và xếp hạng theo xác suất; tải danh sách Top-K thành CSV. Không đọc nhãn để tính metric Test ở Dashboard.

## Chuẩn bị dữ liệu và mô hình

Từ thư mục gốc của repository, chạy Chương 3 rồi Chương 4 theo `docs/EXPERIMENT_PROTOCOL.md`, hoặc nhận nguyên vẹn các artifact nội bộ đã nghiệm thu. Cần:

- `data/processed/orders_model_ready.csv` và `feature_whitelist.json` từ Lam Linh (Ch3).
- `data/processed/split_manifest.csv`, `split_metadata.json`, `experiment_metadata.json` từ Trúc Chi (Ch4).
- `models/champion.joblib` từ Trúc Chi sau khi chốt champion giữa RF và MLP theo AP Validation.

**Thiếu một artifact:** trang EDA vẫn có thể hoạt động nếu có `orders_model_ready.csv`; trang scoring sẽ hiển thị nguyên nhân bị khóa, không tạo kết quả giả. Chỉ tải model joblib được nhóm tạo và chia sẻ từ nguồn tin cậy.

## Chạy trên máy tính

```bash
python -m pip install -r requirements.txt
python -m streamlit run app/app.py
```

Chọn tab **Phân tích lịch sử (EDA)** để xem kết quả tổng quan. Chọn tab **Dự đoán & Top-K**, sau đó dùng một trong hai nguồn:

- **Frozen Test – mô phỏng hồi cứu:** chỉ lấy đơn thuộc split `test` từ manifest, sử dụng 5 feature tại `order_approved_at`, không hiển thị `is_late`/FP/TP; Test không dùng để chọn mô hình/ngưỡng.
- **CSV đặc trưng mới:** file phải có `order_id` và 5 cột trong whitelist; cột nhãn hoặc thông tin hậu giao nếu có sẽ bị bỏ qua, không chuyển vào model. Dữ liệu mới chưa có ground truth để tính chất lượng dự đoán.

Slider **K** điều chỉnh số lượng đơn đội vận hành có thể ưu tiên; ngưỡng cảnh báo giữ nguyên từ Validation. Có thể tải danh sách `rank, order_id, risk_probability, warning`.

## Kiểm thử

```bash
python -m pytest -q tests/test_dashboard_utils.py
```

Kiểm thử không cần dữ liệu Olist/model thật; gồm: EDA ở cấp `order_id`, rò rỉ feature, phạm vi numeric, nguồn gốc champion, SHA256/split/threshold, lựa chọn frozen Test, Top-K và ties. Sau khi nhận đủ artifact thật, kiểm thử giao diện thủ công (đọc CSV, bộ lọc, load joblib, xếp hạng và xuất file) để làm minh chứng Chương 6.2.

**Giới hạn:** Demo nghiên cứu hồi cứu dữ liệu Brazil 2016–2018, không phải ứng dụng theo dõi đơn hàng thời gian thực; xác suất mô hình chưa mặc định là xác suất đã hiệu chuẩn. Không công bố Test metrics nếu Chương 5 chưa xác minh.
