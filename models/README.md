# Model artifacts

Lưu model, pipeline, scaler/encoder đã huấn luyện trên máy/Drive nội bộ được cho phép. File binary như `.pkl`, `.joblib` được bỏ qua bởi .gitignore.

Với mỗi mô hình đã chốt, ghi vào báo cáo/Issue: phiên bản dataset, feature list, split cutoff, seed, scores Test, file artifact có kiểm soát và cách tải. Không sử dụng Test để chọn ngưỡng.

## Artifacts theo người huấn luyện (được tạo sau khi chạy dữ liệu thật)
- Ngọc Lan: `ngoc_lan_random_forest.joblib` và RF Validation file/metadata trong `data/processed/`.
- Trúc Chi: `dummy_truc_chi.joblib`, `mlp_truc_chi.joblib`, `champion.joblib`, frozen Test predictions.
- Vĩnh Chi: kiểm tra lại cả ba model và báo Test metrics (không huấn luyện model mới).
