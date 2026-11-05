# LÝ THUYẾT & HƯỚNG DẪN – VĨNH CHI (CHƯƠNG 5)

**Notebook:** [05_VINH_CHI_chuong_5.ipynb](../../notebooks/05_VINH_CHI_chuong_5.ipynb) · **Issue:** #6.

## 5.1 Kết quả dự đoán trên Test
Chỉ dùng xác suất/nền nhãn từ file Test do Ch4 bàn giao, không train lại. Kiểm tra danh sách `order_id` không trùng, dự đoán là xác suất 0–1, nhãn 0/1.

Với lớp dương là đơn **giao trễ**:
- TP: đúng cảnh báo trễ, FP: cảnh báo nhầm, FN: bỏ sót đơn trễ, TN: đúng khi dự báo không trễ.
- `Precision = TP/(TP+FP)`, `Recall = TP/(TP+FN)`, `F1 = 2PR/(P+R)`.
- `Average Precision` (AP) theo scikit-learn là **quy ước PR-AUC** được thống nhất ở Ch2 và Ch4; không tùy tiện thay bằng ROC-AUC hoặc nội suy hình thang.
- Đường PR: trục x Recall, trục y Precision; nêu prevalence lớp trễ và số mẫu Test.
- Ma trận nhầm lẫn phải có cả 4 ô và giải thích bằng đơn vị đơn hàng.

**Bắt buộc:** đặt Dummy, Random Forest và MLP cùng một bảng với thông số/cấu hình ngưỡng đã chọn trước Test.

## 5.2 Phân tích lỗi
Cần giải thích nơi mô hình sai, không chỉ nêu tổng metrics:
- Theo bang khách, nhóm sản phẩm, phí/giá trị đơn, cân nặng hoặc số seller (nếu các trường này có trong file Ch3).
- Trước khi kết luận tỷ lệ theo nhóm, xem số mẫu `n`; tránh nhóm quá ít mẫu.
- Không lấy các đặc trưng hậu giao được dùng chỉ cho phân tích để mô tả như "mô hình đã biết" khi dự báo.

Mục đích là hiểu giới hạn và đề xuất cải tiến có cơ sở, không chứng minh quan hệ nhân quả.

## 5.3 Phân tích Top-K và giá trị vận hành
Nếu nhân viên chỉ theo dõi được K đơn, mô hình chọn K đơn có xác suất cao nhất.
- `Precision@K = TP@K/K`.
- `Recall@K = TP@K/TotalLateOrders`.
- `FP@K=K−TP@K`.
- So sánh kịch bản theo ngưỡng cố định với ngân sách Top-K; có thể mô tả K=50/100/200 nhưng không chọn K tối ưu bằng Test.

Kết luận vận hành phải gắn với số đơn nhận diện đúng và cảnh báo sai; **không** khẳng định việc cảnh báo sẽ làm giảm trễ bao nhiêu nếu chưa có dữ liệu can thiệp.

## 5.4 Hạn chế và thảo luận
1. Olist là dữ liệu Brazil 2016–2018 nên có khả năng thay đổi phân phối khi triển khai thời điểm khác.
2. Chỉ chọn delivered đã có nhãn; không đại diện đơn hủy/chưa giao.
3. Mốc `order_approved_at` khiến nhiều biến vận chuyển có giá trị hậu nghiệm, phải bị loại khỏi X.
4. Thiếu thử nghiệm trực tiếp với đội vận hành và thiếu đo chi phí can thiệp thực tế.
5. Khi đánh giá các model trên một Test, tránh thay đổi nhiều thiết kế sau khi nhìn kết quả.

## Bàn giao Ch5 → Ch6/FINAL
- `reports/tables/model_metrics.csv`, `topk_analysis.csv`.
- `reports/figures/pr_curve_test.png`.
- 3–5 nhận xét có bảng/hình kèm đường dẫn và mẫu số.
- Bản Ch5 trong `reports/chapters/CH05_RESULTS.md`, nhất quán Ch2 và Ch4.

Không tạo metric giả khi chưa nhận frozen Test predictions.
