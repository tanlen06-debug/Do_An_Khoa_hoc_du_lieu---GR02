# Hợp đồng dữ liệu và nhãn – bắt buộc trước khi viết mô hình

**Nguồn:** [Brazilian E-Commerce Public Dataset by Olist](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce). Khoảng 100.000 đơn hàng, Brazil 2016–2018.

## 1. Cấp dữ liệu
- Bảng cuối dùng huấn luyện phải có **đúng 1 hàng mỗi order_id**.
- Các bảng `order_items`, `payments`, `geolocation` cần aggregate về đúng cấp trước khi join, tránh many-to-many.
- Ghi rõ số dòng qua từng bước, missing, duplicate, số đơn loại bỏ.
- Join theo khóa được dữ liệu khai báo: order_id/customer_id/product_id/seller_id và khóa danh mục; không suy diễn quan hệ thiếu chứng cứ.

## 2. Mốc dự báo
`t0 = order_approved_at`: mô hình được sử dụng ngay khi đơn được phê duyệt. Tất cả biến ứng viên phải có bằng chứng **đã sẵn tại t0**; nếu không xác minh được thì giữ ở trạng thái `needs_review`, không tự cho phép.

## 3. Nhãn (hồi cứu)
Chọn đơn `delivered` đã được phê duyệt, có đủ `order_delivered_customer_date` và `order_estimated_delivery_date`.
```text
is_late = 1 if DATE(order_delivered_customer_date) > DATE(order_estimated_delivery_date)
        = 0 otherwise (đối với đơn hợp lệ có nhãn)
```
Các đơn khác = chưa xác định nhãn (không tự gán 0). Báo cáo giới hạn do lọc các đơn đã giao (selection bias).

## 4. Feature eligibility
Có thể xem xét: thời gian đặt đơn/phê duyệt, bang khách, bang người bán, thông tin sản phẩm, tổng item, giá/phí vận chuyển **nếu có tại t0**, khoảng cách ước tính. Kiểm tra trường `order_estimated_delivery_date`, `shipping_limit_date` và payment data ở thời điểm t0 trước khi dùng.

**Không làm feature tại t0:** `order_delivered_customer_date`, `order_delivered_carrier_date`, `review_score`, `order_status` cuối cùng; không dùng tỷ lệ trễ seller tính từ toàn bộ dataset.

## 5. Bàn giao Ch3 → Ch4
- File data processed có 1 `order_id` duy nhất / dòng; kèm schema, phiên bản, số mẫu, nhãn, phân bố nhãn, danh sách feature.
- Mã pipeline chạy lại được từ raw, không phụ thuộc đường dẫn máy cá nhân.
- Bảng `feature_registry` ghi tên biến, nguồn, thời điểm xuất hiện, quyết định được/không dùng.
- Kiểm tra `src/contracts.py` và `src/labels.py` là **ví dụ testable**, không thay thế toàn bộ quá trình thực nghiệm.
