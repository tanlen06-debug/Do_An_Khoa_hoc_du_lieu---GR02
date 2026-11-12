# Giao thức thực nghiệm GR02 – phân công huấn luyện chính thức (12/11/2026)

**Đề cương giữ nguyên: 6 chương, 27 hạng mục + phụ lục; mục 4.4 vẫn thuộc Chương 4.** Chỉ thay người viết code huấn luyện MLP.

## Phân công và giao thức dữ liệu
1. **Lam Linh – Ch3:** tạo `data/processed/orders_model_ready.csv` ở grain 1 dòng/order_id, xây nhãn `is_late`, EDA và kiểm toán leakage tại `order_approved_at`.
2. **Trúc Chi – Ch4.1:** tạo và kiểm tra chung `split_manifest.csv`, `split_metadata.json` qua `src/experiment.py`; thống nhất `split_id`, SHA256 dữ liệu, feature whitelist và cutoff. Train và Validation chỉ dùng nhãn đã trưởng thành tại cutoff tương ứng.
3. **Ngọc Lan – Ch2.3/2.4:** thực hiện Random Forest trong notebook 02. Fit trên Train, chọn hyperparameters và threshold bằng **Validation**; đo Precision/Recall/F1/AP/FP/Top-K trên Validation. Bàn giao `models/ngoc_lan_random_forest.joblib`, `rf_val_predictions.csv`, `rf_metadata.json`.
4. **Tấn Lên (TV1, nhóm trưởng) – thực nghiệm MLP cho 4.4:** thực hiện các cell trong notebook 01, dùng cùng split/feature. Fit MLP Pipeline trên Train, chọn kiến trúc/threshold bằng Validation; đo P/R/F1/AP/FP/Top-K Validation, lưu training loss. Bàn giao `models/tan_len_mlp.joblib`, `mlp_val_predictions.csv`, `mlp_metadata.json`. Trúc Chi viết nội dung mô hình MLP tại **mục 4.4 Chương 4** dựa trên sản phẩm này.
5. **Trúc Chi (TV4) – Ch4.2–4.5:** **chỉ gọi fit để huấn luyện Dummy Classifier**. Nhận RF từ Ngọc Lan và MLP từ Tấn Lên; kiểm tra `split_id`, SHA256, `features`, thứ tự `order_id`, `y_true`, `predict_proba(Validation)`. **Không fit lại RF hay MLP.** Chốt champion giữa RF và MLP theo AP Validation, dùng threshold riêng đã chọn trên Validation; tạo frozen Test predictions.
6. **Ch4 bàn giao:** `test_predictions.csv` chứa `order_id,y_true,p_dummy,p_rf,p_mlp,y_pred_champion`; `experiment_metadata.json` có `model_owners={"rf":"Ngọc Lan","mlp":"Tấn Lên","dummy":"Trúc Chi"}`, `split_id`, thresholds; `models/dummy_truc_chi.joblib`, `models/champion.joblib`. Dùng RF/MLP artifact gốc, không tạo model MLP thứ hai.
7. **Vĩnh Chi (TV5) – Ch5:** đọc cùng một frozen Test; nạp 3 model đã fit, **tính lại** `predict_proba(Test)`, đối soát `test_predictions.csv`; tính TP/FP/FN/TN, Precision, Recall, F1, Average Precision (quy ước PR-AUC), confusion matrix, PR Curve, Precision@K/Recall@K/FP@K. Không gọi `fit`, không chọn threshold/K theo Test.
8. **Tấn Lên – Ch6/FINAL:** chạy dashboard và kiểm tra đủ chủ mô hình, metadata, cutoff/split_id, bảng Test, báo cáo 6 chương. Không đào tạo mô hình lần hai trong FINAL.

## Quy định phương pháp
- Thời điểm dự báo: `order_approved_at`; feature chỉ được biết ở thời điểm đó. Ngày giao thực tế dùng tạo nhãn và kiểm soát label maturity, **không vào X**.
- Tất cả mô hình dùng cùng order_id/split, nhãn và whitelist; preprocessing `fit` chỉ trên Train (Pipeline của từng thành viên được phép khác nhau).
- Mọi lựa chọn cấu hình/champion/threshold trên Validation; Test chỉ dùng đánh giá cuối sau khi đóng băng.
- File binary mô hình và processed CSV bàn giao qua kênh nội bộ nhóm, không push lên GitHub; mã nguồn và Markdown cập nhật bằng Pull Request.
- Chỉ công bố metric sau khi thực sự chạy Olist và Vĩnh Chi kiểm tra. Delivered-only gây selection bias; dữ liệu lịch sử Brazil 2016–2018 không mặc nhiên áp dụng cho sàn Việt Nam.

**Thứ tự chạy:** Lam Linh Ch3 → Trúc Chi Ch4.1 tạo split → Ngọc Lan RF Ch2 và Tấn Lên MLP notebook 01 → Trúc Chi Ch4 fit Dummy + tích hợp → Vĩnh Chi Ch5 Test → 06_FINAL.
