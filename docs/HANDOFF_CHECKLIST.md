# CHECKLIST BÀN GIAO 5 THÀNH VIÊN → NOTEBOOK FINAL

## Tấn Lên – Chương 1, 6 và phụ lục
- [ ] Ch1 có lý do chọn đề tài, bài toán dự đoán tại approved_at, mục tiêu và giới hạn.
- [ ] Ch6 có sơ đồ dashboard, kiểm thử, README, demo/hình chụp khi đủ model.
- [ ] `01_TAN_LEN_chuong_1_6.ipynb` và Markdown lý thuyết được cập nhật đúng.
- [ ] Chỉ dùng chỉ số của Ch5 để viết kết luận; không tự tạo số liệu.

## Ngọc Lan – Chương 2
- [ ] `02_NGOC_LAN_chuong_2.ipynb`, `docs/theory/02_ngoc_lan_ch2.md`.
- [ ] Có logistics, EDA, Random Forest, MLP, Dummy, P/R/F1/AP/Top-K.
- [ ] Có bảng 3–5 nghiên cứu liên quan **đã kiểm chứng nguồn**; đối chiếu với Ch4/Ch5.

## Lam Linh – Chương 3 → Trúc Chi
- [ ] `03_LAM_LINH_chuong_3.ipynb` chạy được trên Olist đã tải.
- [ ] 1 dòng/order_id, nhãn theo ngày, có số mẫu bị loại, EDA kèm insight.
- [ ] Có `orders_model_ready.csv`, dữ liệu dictionary, feature whitelist; audit leakage tại approved_at.
- [ ] Trúc Chi xác nhận schema và dataset đã nhận (mốc 12–16/11).

## Trúc Chi – Chương 4 → Vĩnh Chi
- [ ] `04_TRUC_CHI_chuong_4.ipynb` chạy được sau Ch3.
- [ ] Train/Val/Test theo thời gian; imputer/encoder/scaler fit Train-only.
- [ ] Dummy, RF, MLP; chọn model/ngưỡng theo Validation, Test đóng băng.
- [ ] Có `test_predictions.csv`, `experiment_metadata.json`, `models/champion.joblib`.
- [ ] Vĩnh Chi xác nhận bản giao đến 22–24/11.

## Vĩnh Chi – Chương 5 → Tấn Lên
- [ ] `05_VINH_CHI_chuong_5.ipynb` chỉ đọc frozen Test; không fit mô hình.
- [ ] Metrics P/R/F1/AP/FP, confusion matrix, PR Curve, Precision@K/Recall@K.
- [ ] Có `model_metrics.csv`, `topk_analysis.csv`, `pr_curve_test.png`.
- [ ] Tấn Lên nhận và đối chiếu số liệu 24–25/11.

## Cả nhóm – 06_FINAL
- [ ] Chạy tuần tự Ch3 → Ch4 → Ch5 → FINAL; notebooks Ch1/2 được rà soát và cập nhật.
- [ ] FINAL khớp schema, số đơn, nhãn, cutoff, threshold, metric và mô hình.
- [ ] Ch1–Ch6 + phụ lục, hình/bảng, trích dẫn và README khớp code.
- [ ] Dashboard Streamlit chạy offline, minh họa đúng phạm vi nghiên cứu.
- [ ] 27/11 bản đầy đủ; 28–29/11 review; hoàn tất nội bộ 30/11/2026.

Các file CSV/model nội bộ được `.gitignore`. Đừng đánh dấu hoàn thành chỉ vì notebook có sẵn khung.
