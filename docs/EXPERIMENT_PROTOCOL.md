# Giao thức thực nghiệm GR02 – chung split, tách người huấn luyện

**Giữ khung báo cáo 6 chương, 27 hạng mục.** Quy tắc chỉ điều chỉnh chủ sở hữu code và điểm bàn giao.

1. **Lam Linh – Ch3:** xuất `orders_model_ready.csv`, 1 dòng/order_id, `is_late` theo ngày và feature hợp lệ tại `order_approved_at`.
2. **Trúc Chi – 4.1:** tạo/chốt temporal Train–Validation–Test chung qua `src/experiment.py`; lưu `split_manifest.csv`, `split_metadata.json`, `split_id`, dữ liệu SHA256 và cutoff. Train và Validation chỉ dùng nhãn đã trưởng thành trước cutoff tiếp theo.
3. **Ngọc Lan – 2.3/2.4:** train **Random Forest** trên Train chung, chọn tham số/threshold bằng **Validation**, đo Precision/Recall/F1/AP/FP/Top-K trên Validation. Bàn giao `ngoc_lan_random_forest.joblib`, `rf_val_predictions.csv` và `rf_metadata.json`.
4. **Trúc Chi – 4.2/4.4:** train **Dummy và MLP** trên Train chung (fit preprocessing train-only). Phần 4.3 đọc RF của Ngọc Lan, kiểm tra `split_id`, features và xác suất Validation; **không fit lại RF**. Chọn mô hình chính RF/MLP theo AP Validation; giữ ngưỡng RF do Ngọc Lan chọn, chốt các ngưỡng còn lại bằng Validation.
5. **Trúc Chi – 4.5:** sau khi chốt trên Validation, xuất `test_predictions.csv` (order_id, y_true, p_dummy, p_rf, p_mlp, y_pred_champion), `experiment_metadata.json`, `dummy_truc_chi.joblib`, `mlp_truc_chi.joblib`, `champion.joblib`.
6. **Vĩnh Chi – Ch5:** trên **một frozen Test**, nạp model RF Ngọc Lan và Dummy/MLP Trúc Chi để `predict_proba(Test)` lại, so khớp file Ch4; **không fit**. Tính TP/FP/FN/TN, Precision, Recall, F1, Average Precision (AP, quy ước PR-AUC), PR Curve, Precision@K/Recall@K/FP@K cho **cả ba**.
7. **Tấn Lên – Ch6/FINAL:** kiểm tra `split_id`, danh sách owner, scores và kết luận; demo Streamlit hồi cứu. Không tune hoặc train model bằng Test.
8. **Không leakage:** chỉ feature có tại `order_approved_at`, loại các trường sau giao; fit imputer/encoder/scaler trên Train; không trộn nhãn Test vào tinh chỉnh.
9. **Bàn giao có minh chứng:** mã nguồn có commit/PR; file CSV processed và binary model truyền nội bộ, không đẩy lên GitHub; ghi `split_id`, schema, seed, cutoff, số mẫu và tỷ lệ lớp.
10. **Giới hạn:** Delivered-only; Olist Brazil 2016–2018; không tự tuyên bố hiệu quả vận hành tại Việt Nam hiện nay.

**Thứ tự chạy khi tái lập:** Ch3 → Ch4 đến split → Ch2 huấn luyện RF → Ch4 Dummy/MLP + tích hợp → Ch5 đánh giá độc lập → FINAL.
