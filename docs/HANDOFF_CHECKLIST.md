# Bàn giao liên chương – kiểm tra bắt buộc

## Ch3 → Ch4 (mốc 12–16/11)
- [ ] Dữ liệu 1 dòng/order_id, kiểm tra unique.
- [ ] Schema: tên cột, kiểu, mô tả, nguồn, missing, số đơn bị loại.
- [ ] Nhãn `is_late` theo **ngày** giao thực tế và ngày dự kiến.
- [ ] Danh mục feature hợp lệ tại `order_approved_at`; biến không rõ được gắn cờ.
- [ ] Notebook và script chạy lại được; không chứa đường dẫn máy cá nhân.
- [ ] Ch4 xác nhận receipt bằng PR review hoặc comment Issue.

## Ch4 → Ch5 (mốc 22–24/11)
- [ ] Cố định split, pipeline, seed, thông số, ngưỡng trên Validation.
- [ ] Kết quả Test và file dự đoán có `order_id`, `y_true`, `y_score`, `y_pred`.
- [ ] Không tune theo Test.
- [ ] Mô tả cách tính AP, Precision, Recall, F1, FP/TP.
- [ ] Ch5 kiểm tra số liệu bằng tính lại từ file predictions.

## Ch5 → Ch6 (mốc 24–27/11)
- [ ] Bảng tổng kết Test, ma trận nhầm lẫn, PR Curve, Precision@K/Recall@K.
- [ ] Kịch bản chọn K đơn ưu tiên, minh chứng hiệu quả và hạn chế.
- [ ] Ch6 dùng artifact model đã review; app trình bày là **demo hồi cứu**, không phải realtime.

## Kết thúc
- [ ] 6 chương + phụ lục thống nhất thuật ngữ và kết quả.
- [ ] Trích dẫn có nguồn kiểm chứng; hình/tables đánh số và dẫn trong text.
- [ ] README, requirements, cách chạy app và cách tải Olist đầy đủ.
- [ ] Mỗi sản phẩm có link trong Google Sheet và Issue/PR tương ứng.
