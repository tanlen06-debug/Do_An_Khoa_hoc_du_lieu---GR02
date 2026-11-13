# CH04 MODELING

**Phụ trách:** Trúc Chi. **Trạng thái:** khung nháp, chưa có kết quả.

## 4.1 Quy trình đánh giá theo thời gian

*TODO:* Mục tiêu – phương pháp – bằng chứng (bảng/hình/nguồn) – nhận xét. Chỉ điền số liệu thực đã kiểm chứng.

## 4.2 Tiền xử lý và Dummy

*TODO:* Mục tiêu – phương pháp – bằng chứng (bảng/hình/nguồn) – nhận xét. Chỉ điền số liệu thực đã kiểm chứng.

## 4.3 Tiếp nhận, kiểm chứng Random Forest của Ngọc Lan

*TODO:* Mục tiêu – phương pháp – bằng chứng (bảng/hình/nguồn) – nhận xét. Chỉ điền số liệu thực đã kiểm chứng.

## 4.4 Huấn luyện MLP

*TODO:* Mục tiêu – phương pháp – bằng chứng (bảng/hình/nguồn) – nhận xét. Chỉ điền số liệu thực đã kiểm chứng.

## 4.5 Lựa chọn ngưỡng / Top-K

*TODO:* Mục tiêu – phương pháp – bằng chứng (bảng/hình/nguồn) – nhận xét. Chỉ điền số liệu thực đã kiểm chứng.

> Đồng bộ số liệu, tên biến và trích dẫn với phần triển khai / notebook liên quan trước khi tạo PR.

**Phân công thực nghiệm mới:** Trúc Chi sở hữu split Train/Validation/Test chung; huấn luyện Dummy/MLP. Riêng Random Forest đã được Ngọc Lan fit ở Chương 2, Trúc Chi chỉ kiểm tra và tích hợp `ngoc_lan_random_forest.joblib` theo `split_id` chung. Mục 4.5 lựa chọn champion và ngưỡng trên Validation, không fit RF lần hai. Bàn giao frozen Test cho Vĩnh Chi.

### Phân công huấn luyện mới cho 4.4
**Tấn Lên (TV1)** trực tiếp huấn luyện MLP trong notebook 01 và bàn giao `tan_len_mlp.joblib`, `mlp_val_predictions.csv`, `mlp_metadata.json`. **Trúc Chi (TV4)** chỉ fit Dummy, kiểm chứng RF Ngọc Lan/MLP Tấn Lên và trình bày RF ở 4.3, MLP ở 4.4 dựa trên artifact có `split_id` chung. Chương 4 không có lệnh fit MLP/RF; chỉ tích hợp và xuất frozen Test. Chưa điền số liệu giả.
