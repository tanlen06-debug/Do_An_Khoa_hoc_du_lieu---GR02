# CH05 RESULTS

**Phụ trách:** Vĩnh Chi. **Trạng thái:** khung nháp, chưa có kết quả.

## 5.1 Kết quả trên tập Test

*TODO:* Mục tiêu – phương pháp – bằng chứng (bảng/hình/nguồn) – nhận xét. Chỉ điền số liệu thực đã kiểm chứng.

## 5.2 Phân tích lỗi theo nhóm

*TODO:* Mục tiêu – phương pháp – bằng chứng (bảng/hình/nguồn) – nhận xét. Chỉ điền số liệu thực đã kiểm chứng.

## 5.3 Ý nghĩa vận hành

*TODO:* Mục tiêu – phương pháp – bằng chứng (bảng/hình/nguồn) – nhận xét. Chỉ điền số liệu thực đã kiểm chứng.

## 5.4 Thảo luận hạn chế

*TODO:* Mục tiêu – phương pháp – bằng chứng (bảng/hình/nguồn) – nhận xét. Chỉ điền số liệu thực đã kiểm chứng.

> Đồng bộ số liệu, tên biến và trích dẫn với phần triển khai / notebook liên quan trước khi tạo PR.

**Phân công thực nghiệm mới:** Vĩnh Chi kiểm tra độc lập Random Forest (Ngọc Lan), Dummy/MLP (Trúc Chi). Đối chiếu `split_id`, tái tính `predict_proba(X_test)` bằng model đã fit, sau đó tự tính Precision, Recall, F1, AP, FP, confusion matrix, PR Curve và Top-K của cả ba trên frozen Test. Không fit model mới hoặc chọn ngưỡng theo Test.

**Chủ mô hình cập nhật:** Random Forest – Ngọc Lan, MLP – Tấn Lên (TV1), Dummy – Trúc Chi (TV4). Vĩnh Chi load `tan_len_mlp.joblib` để tính lại p_mlp Test, kiểm tra cùng split_id rồi đánh giá độc lập; không fit model mới.
