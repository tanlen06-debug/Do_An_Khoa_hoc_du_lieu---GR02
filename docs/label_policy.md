# Quy tắc gán nhãn giao trễ

Mốc dự báo là thời điểm đơn được phê duyệt, `order_approved_at`. Nhãn `is_late` được xác định hồi cứu cho đơn `delivered` có đủ thời điểm duyệt, ngày giao thực tế và ngày giao dự kiến.

So sánh theo ngày lịch. `is_late = 1` nếu ngày giao thực tế sau ngày giao dự kiến. `is_late = 0` nếu đơn giao trước hoặc trong ngày dự kiến. Các đơn hủy, chưa giao thành công hoặc thiếu mốc bắt buộc có nhãn rỗng.

| Trạng thái | Giao dự kiến | Giao thực tế | Nhãn |
|---|---|---|---|
| delivered | 10/01 | 09/01 | 0 |
| delivered | 10/01 | 10/01 lúc 22:30 | 0 |
| delivered | 10/01 | 11/01 lúc 00:10 | 1 |
| delivered | 10/01 | Thiếu | Rỗng |
| canceled | 10/01 | Thiếu | Rỗng |

Các ví dụ trên giả sử có thời điểm duyệt. Notebook 03 gọi [make_late_label](../src/labels.py), cùng hàm được [kiểm thử trong repo](../tests/test_labels.py).

Từ 99.441 đơn, nhóm loại lần lượt 2.963 đơn chưa giao thành công, 14 đơn thiếu thời điểm duyệt và 8 đơn thiếu ngày giao thực tế. Bước kiểm tra ngày dự kiến không loại thêm đơn. Tập có nhãn còn 96.456 đơn, trong đó 6.534 đơn giao trễ (6,77%). Xem [bảng loại mẫu](../reports/tables/label_exclusions.csv) và [bảng đối soát nhãn](../reports/tables/label_audit.csv).

Tập chính giữ đơn có cờ bất thường thứ tự thời gian nếu đủ điều kiện nhãn. Phân tích độ nhạy ở [mục 3.3](../reports/chapters/CH03_DATA.md#33-nhãn-và-chọn-mẫu) cho thấy ảnh hưởng lên tỷ lệ trễ. Phạm vi là đơn đã giao đủ nhãn. Ngày giao thực tế phục vụ tạo nhãn và kiểm tra nhãn đã hình thành trước cutoff trong Chương 4.
