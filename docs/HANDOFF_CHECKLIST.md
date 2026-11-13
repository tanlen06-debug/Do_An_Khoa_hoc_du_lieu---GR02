# Checklist bàn giao GR02 – MLP chuyển về TV1, TV4 chỉ Dummy

## Lam Linh (Ch3) → Trúc Chi
- [ ] Tạo `orders_model_ready.csv` với `order_id` duy nhất, nhãn đúng, feature whitelist tại approved_at và EDA/QA rõ ràng.
- [ ] Bàn giao schema, dataset fingerprint, báo cáo giới hạn delivered-only.

## Trúc Chi (4.1) → Ngọc Lan và Tấn Lên
- [ ] Chốt shared split/cutoff/label maturity; có `split_manifest.csv`, `split_metadata.json`, `split_id`.
- [ ] Hai thành viên RF/MLP dùng đúng dữ liệu, nhãn và whitelist, không tự chia lại.

## Ngọc Lan (Ch2.3/2.4) → Trúc Chi
- [ ] Huấn luyện Random Forest trên Train chung; chọn tham số/ngưỡng trên Validation.
- [ ] Bàn giao `ngoc_lan_random_forest.joblib`, `rf_val_predictions.csv`, `rf_metadata.json` có split_id, Validation metrics/Top-K và nguồn lý thuyết.

## Tấn Lên (TV1 – huấn luyện MLP cho 4.4) → Trúc Chi
- [ ] Notebook 01 có cell fit MLP trên Train, Pipeline impute/encode/scale, thử kiến trúc, early-stopping và loss.
- [ ] Có Precision/Recall/F1/AP/FP/Top-K Validation, threshold từ Validation; không dùng Test.
- [ ] Bàn giao `tan_len_mlp.joblib`, `mlp_val_predictions.csv`, `mlp_metadata.json` có split_id và config, trước 21/11.
- [ ] Tấn Lên vẫn phụ trách Ch1, Ch6, dashboard và FINAL; Trúc Chi trình bày kết quả MLP tại **mục 4.4 của Ch4**.

## Trúc Chi (TV4 – Ch4) → Vĩnh Chi
- [ ] TV4 **chỉ fit Dummy**, không fit RF hoặc MLP.
- [ ] Kiểm tra RF Ngọc Lan + MLP Tấn Lên: model owner, split_id, dataset SHA256, features và Validation `order_id,y_true,probabilities`.
- [ ] Tổng hợp bảng AP Validation; đóng băng champion/threshold trước Test.
- [ ] Bàn giao `dummy_truc_chi.joblib`, `champion.joblib`, `test_predictions.csv`, `experiment_metadata.json` và toàn bộ artifact RF/MLP từ hai thành viên.

## Vĩnh Chi (TV5 – Ch5) → Tấn Lên
- [ ] Nạp RF Ngọc Lan, Dummy Trúc Chi, MLP Tấn Lên; tính lại xác suất trên một frozen Test, đối chiếu Ch4.
- [ ] Tính lại P/R/F1/AP/FP, confusion matrix, PR Curve, Precision@K/Recall@K/FP@K của ba mô hình. Không fit hoặc tune Test.
- [ ] Bàn giao `model_metrics.csv`, `topk_analysis.csv`, `pr_curve_test.png` và thảo luận lỗi/hạn chế.

## FINAL
- [ ] Đối chiếu model_owners: RF–Ngọc Lan, MLP–Tấn Lên, Dummy–Trúc Chi; split_id chung và chỉ số Test của Vĩnh Chi.
- [ ] Đủ 6 chương, 27 hạng mục, phụ lục và dashboard; hạn cuối 30/11/2026; không giả lập số thực nghiệm.
