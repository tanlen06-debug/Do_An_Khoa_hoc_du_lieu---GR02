# LÝ THUYẾT & HƯỚNG DẪN – TRÚC CHI (CHƯƠNG 4)

**Notebook:** [04_TRUC_CHI_chuong_4.ipynb](../../notebooks/04_TRUC_CHI_chuong_4.ipynb) · **Issue:** #5.

## 4.1 Thiết kế thực nghiệm theo thời gian
Tạo `Train/Validation/Test` theo thời gian `order_approved_at`, tỷ lệ 70/15/15 chỉ là gợi ý. Không xáo ngẫu nhiên nếu mục tiêu là mô phỏng dự báo đơn hàng trong tương lai. Ghi cutoff và số mẫu của từng tập.

**Label maturity:** ở thời điểm bắt đầu Validation, chỉ các đơn Train có kết quả giao hàng đã xảy ra mới có thể được dùng để học mô hình. Tương tự, khi chọn ngưỡng dựa trên Validation để áp dụng cho Test, nhãn Validation cần đã trưởng thành trước thời điểm Test bắt đầu. Dữ liệu Ch3 giữ ngày giao thực tế ở phần **metadata**, không dùng trong X.

## 4.2 Tiền xử lý và Dummy
- Numeric: `SimpleImputer(strategy='median')` rồi scale nếu vào MLP.
- Categorical: `SimpleImputer` + `OneHotEncoder(handle_unknown='ignore')`.
- Fit các bước **chỉ trên Train**; dùng `Pipeline/ColumnTransformer`.
- Baseline `DummyClassifier(strategy='prior')` để biết hiệu quả của dự đoán không dùng feature.

**Data leakage:** cấm ngày giao thực tế, review, trạng thái cuối; cẩn thận `estimated_delivery_date`, seller stats hay freight nếu chưa chứng minh được có lúc dự báo.

## 4.3 Tích hợp Random Forest Ngọc Lan đã huấn luyện
RF tập hợp nhiều cây, học trên bootstrap samples; có thể bắt quan hệ phi tuyến và tương tác biến. Tham số xuất phát trong notebook: `n_estimators=200`, `min_samples_leaf=5`, `class_weight='balanced_subsample'`, `random_state=42`. Đây là cấu hình mẫu, **không phải tham số tối ưu**.

Ngọc Lan huấn luyện và chọn cấu hình RF trên Train/Validation của split chung ở Chương 2. Trúc Chi **không gọi fit lại RF**, chỉ nạp `ngoc_lan_random_forest.joblib`, `rf_val_predictions.csv`, `rf_metadata.json`; xác minh split_id, features, Validation order_id và probabilities, sau đó trình bày cấu hình/kết quả đã bàn giao.

## 4.4 MLP
Mạng fully-connected với hai lớp ẩn tham khảo `(64,32)`, `alpha=0.001`, early stopping, `random_state=42`. Không mặc định MLP sẽ hơn RF trên dữ liệu bảng. Giải thích loss và ảnh hưởng scale/one-hot/overfit. Nếu thay đổi kiến trúc, ghi vào nhật ký thực nghiệm.

## 4.5 Chọn threshold và Top-K
- Lấy xác suất `predict_proba(X_val)[:,1]`.
- Chọn mô hình chính theo **Average Precision trên Validation** giữa RF Ngọc Lan và MLP Trúc Chi; Dummy là tham chiếu. Giữ ngưỡng RF do Ngọc Lan chốt trên Validation.
- Chọn threshold theo F1 Validation hoặc tiêu chí vận hành được **chốt trước**; ghi số FP và TP trên Validation.
- Với Top-K, sắp xếp giảm dần theo nguy cơ; chọn K theo khả năng giám sát hoặc mô phỏng ngân sách.

**Tập Test chỉ sử dụng để đánh giá cuối, không phải chọn model hoặc threshold.**

## File bàn giao
- `models/dummy_truc_chi.joblib`, `models/mlp_truc_chi.joblib` để Vĩnh Chi kiểm tra lại Test mà không fit lại.
- `data/processed/test_predictions.csv` gồm `order_id,y_true,p_dummy,p_rf,p_mlp,y_pred_champion`.
- `data/processed/experiment_metadata.json` gồm ngưỡng trên Validation, model chọn, cutoff, features, seed.
- `models/champion.joblib` chứa toàn pipeline đã fit; chỉ load artifact tin cậy.
- File/ảnh config, bảng Validation và mô tả cách chạy.

**Giới hạn:** Notebook khung chưa có số liệu thực nghiệm. Điều kiện hoàn thành là các cell chạy được trên Olist do Lam Linh bàn giao, có đầy đủ minh chứng và kết quả đối soát Ch5.
