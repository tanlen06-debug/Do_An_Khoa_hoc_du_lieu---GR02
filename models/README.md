# Model artifacts

Lưu model, pipeline, scaler/encoder đã huấn luyện trên máy/Drive nội bộ được cho phép. File binary như `.pkl`, `.joblib` được bỏ qua bởi .gitignore.

Với mỗi mô hình đã chốt, ghi vào báo cáo/Issue: phiên bản dataset, feature list, split cutoff, seed, scores Test, file artifact có kiểm soát và cách tải. Không sử dụng Test để chọn ngưỡng.

## Artifacts theo người huấn luyện (được tạo sau khi chạy dữ liệu thật)
- Ngọc Lan: `ngoc_lan_random_forest.joblib` và RF Validation file/metadata trong `data/processed/`.
- Trúc Chi: `dummy_truc_chi.joblib`, `champion.joblib`, frozen Test predictions; chỉ fit Dummy.
- Vĩnh Chi: kiểm tra lại cả ba model và báo Test metrics (không huấn luyện model mới).

**Từ 12/11/2026:** MLP không thuộc Trúc Chi. Tấn Lên (TV1) tạo `tan_len_mlp.joblib`; Trúc Chi (TV4) chỉ fit `dummy_truc_chi.joblib`, nhận RF Ngọc Lan + MLP Tấn Lên và xuất champion/frozen Test. Tên file `mlp_truc_chi.joblib` là tên cũ, không sử dụng trong pipeline mới.

**Chỉ dùng MLP từ Tấn Lên:** `tan_len_mlp.joblib` và metadata/Validation đã bàn giao.
