# Kiểm tra đặc trưng tại thời điểm phê duyệt

Mô hình dự báo khi đơn được phê duyệt (`order_approved_at`). Thông tin có sau mốc này có thể tiết lộ kết quả giao, khiến đánh giá mô hình cao hơn khả năng dự báo thực tế.

| Đặc trưng dùng trong X | Nguồn | Thời điểm có thể tính |
|---|---|---|
| `purchase_month_number` | Tháng từ `orders.order_purchase_timestamp` | Khi đặt đơn |
| `purchase_weekday` | Thứ từ `orders.order_purchase_timestamp` | Khi đặt đơn |
| `purchase_hour` | Giờ từ `orders.order_purchase_timestamp` | Khi đặt đơn |
| `approval_delay_hours` | `orders.order_approved_at` trừ thời điểm đặt, tính theo giờ | Khi đơn được duyệt |
| `customer_state` | Bang khách hàng, nối qua `customer_id` | Khi đặt đơn |

- **Nhãn và metadata.** `is_late` là biến đích. `order_id` dùng đối soát. Thời điểm duyệt và giao thực tế dùng kiểm tra chia tập và thời điểm nhãn hình thành.
- **Thông tin hậu nghiệm.** Ngày giao thực tế, ngày giao cho đơn vị vận chuyển, trạng thái cuối, điểm đánh giá và cờ QA tính từ mốc sau duyệt nằm ngoài X.
- **Biến chưa xác minh.** Giá, phí, số item, thông tin sản phẩm hoặc người bán, thanh toán, ngày giao dự kiến và hạn gửi hàng chỉ được cân nhắc khi có bằng chứng chúng đã sẵn có tại mốc duyệt. Các biến đã tính từ những bảng này phục vụ EDA hoặc kiểm tra.
- **Thống kê theo người bán.** Tỷ lệ giao trễ tính trên toàn bộ dữ liệu sử dụng cả các kết quả tương lai. Muốn dùng một đặc trưng lịch sử, phải tính từ những nhãn đã hình thành trước thời điểm của từng đơn.

Notebook 03 xuất `feature_whitelist.json`, kiểm tra danh sách này không trùng các cột hậu nghiệm và xác nhận `orders_baseline_input.csv` có đúng 5 đặc trưng, khóa và nhãn. [Bảng kiểm tra từng biến](../reports/tables/feature_registry.csv) ghi nguồn, vai trò, thời điểm có dữ liệu và quyết định sử dụng. [Phụ lục Chương 3](../reports/chapters/CH03_APPENDIX.md) mô tả đủ 37 cột.

[Quy trình Chương 4](EXPERIMENT_PROTOCOL.md) dùng chung 5 đặc trưng cho Dummy, Random Forest và MLP. Các phép điền thiếu, mã hóa và chuẩn hóa được fit trên Train.
