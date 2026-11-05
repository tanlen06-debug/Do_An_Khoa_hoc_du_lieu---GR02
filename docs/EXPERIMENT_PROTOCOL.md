# Giao thức thực nghiệm thống nhất – Ch4 / Ch5

1. Dùng cùng đơn vị mẫu, cùng tập đặc trưng đã kiểm toán, cùng nhãn và cùng thứ tự thời gian cho Dummy, RF, MLP.
2. Chia **Train / Validation / Test theo thời gian**. Tỷ lệ 70/15/15 là đề xuất cần kiểm tra với số mẫu thực tế. Nếu mô phỏng triển khai lịch sử, chỉ huấn luyện trên nhãn đã xuất hiện trước cutoff.
3. Fit imputer/encoder/scaler trên Train. Với MLP cần scale thích hợp; với Random Forest xử lý categorical/NA đúng quy tắc. Lưu toàn pipeline.
4. Dummy là mốc; Random Forest đại diện ML; MLP đại diện Deep Learning. Không định trước mô hình nào thắng.
5. Chọn siêu tham số, xác suất/ngưỡng cảnh báo và Top-K trên Validation. **Không dùng Test để chọn**.
6. Đánh giá cuối trên Test cố định: TP, FP, FN, TN, Precision, Recall, F1, Average Precision (`average_precision_score`), ma trận nhầm lẫn, đường PR, Precision@K và Recall@K. Nêu AP là quy ước PR-AUC của nhóm.
7. Nếu lớp trễ hiếm, không dùng Accuracy làm luận điểm chính; báo cáo baseline prevalence, hỗ trợ số lượng mẫu, cảnh báo sai.
8. Lưu `random_state`/seed, version thư viện, mốc thời gian split, tên dataset và số mẫu. Các điểm số trên README hoặc báo cáo phải truy được nguồn.
9. Tạo tập `test_predictions` với order_id, y_true, y_score và y_pred cho Ch5; bảo đảm không lộ vào train hoặc dashboard.

Trước khi báo cáo kết quả cuối, hai chủ phần Ch4/Ch5 đối chiếu lại cùng artifact/dự đoán và thống nhất mọi con số.
