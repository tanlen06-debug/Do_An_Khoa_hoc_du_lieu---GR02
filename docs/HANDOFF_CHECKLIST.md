# Checklist bàn giao liên chương (phân công mới)

## Tấn Lên – Ch1, Ch6 và FINAL
- [ ] Ch1 định nghĩa bài toán, nhãn và mốc approved_at; Ch6/FINAL dùng metrics Ch5.
- [ ] Dashboard/reports và slides không ghi số liệu chưa thực nghiệm.

## Lam Linh – Ch3 → Trúc Chi & Ngọc Lan
- [ ] Dataset 1 dòng/order_id, `orders_model_ready.csv`; schema, QA, nhãn, EDA, feature whitelist.
- [ ] Dữ liệu đủ để Trúc Chi tạo split chung; ghi rõ selection bias (đơn delivered).

## Trúc Chi – 4.1: bàn giao split chung
- [ ] `split_manifest.csv`, `split_metadata.json`, `split_id` và SHA256 dữ liệu; train/val/test không trùng đơn.
- [ ] Nhãn Train/Validation đủ trưởng thành tại cutoff; Ngọc Lan dùng đúng các bản ghi.

## Ngọc Lan – 2.3/2.4: RF → Trúc Chi
- [ ] Có lý thuyết 2.1–2.5 và nghiên cứu liên quan có nguồn.
- [ ] Train RF trên Train của split chung; chọn hyperparams/ngưỡng theo Validation, không nhìn Test.
- [ ] Tính Precision, Recall, F1, AP/PR-AUC, FP và Top-K **trên Validation**.
- [ ] Bàn giao `models/ngoc_lan_random_forest.joblib`, `data/processed/rf_val_predictions.csv`, `rf_metadata.json` cùng `split_id`, trước 20/11.
- [ ] Trúc Chi kiểm tra artifact và đối chiếu xác suất Validation.

## Trúc Chi – 4.2–4.5: Dummy/MLP + RF tích hợp → Vĩnh Chi
- [ ] Chỉ fit Dummy và MLP trên Train chung; RF nạp từ Ngọc Lan, **không fit RF lần hai**.
- [ ] Chốt champion/ngưỡng theo Validation, không tune theo Test.
- [ ] Xuất frozen `test_predictions.csv`, `experiment_metadata.json`, fitted Dummy/MLP và champion artifacts.
- [ ] Vĩnh Chi nhận file Test và các model đủ để tự tính lại.

## Vĩnh Chi – Ch5 → Tấn Lên
- [ ] Độc lập load RF, Dummy và MLP; tự `predict_proba` trên frozen Test; so với predictions Ch4.
- [ ] Tính lại Precision, Recall, F1, AP, FP, confusion matrix, PR curve và Top-K của cả ba.
- [ ] Bàn giao `model_metrics.csv`, `topk_analysis.csv`, `pr_curve_test.png` và nhận xét theo dữ liệu.

## Cả nhóm – 06_FINAL
- [ ] Ch3 → Ch4 split → Ch2 RF → Ch4 Dummy/MLP + frozen Test → Ch5 → FINAL.
- [ ] Mọi model có owner và split_id, mọi số liệu Test có thể tái lập.
- [ ] Báo cáo đủ 6 chương/27 hạng mục, không đổi người phụ trách chương hoặc deadline nội bộ 30/11/2026.
