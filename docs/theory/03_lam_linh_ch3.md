# LÝ THUYẾT & HƯỚNG DẪN – LAM LINH (CHƯƠNG 3)

**Notebook:** [03_LAM_LINH_chuong_3.ipynb](../../notebooks/03_LAM_LINH_chuong_3.ipynb) · **Issue:** #4 · GATE kiểm tra leakage #8.

## 3.1 Tìm hiểu dữ liệu Olist
Dữ liệu công khai [Olist trên Kaggle](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce) thường được phân phối dưới 9 CSV. Các bảng trung tâm:
- `olist_orders_dataset`: `order_id`, `customer_id`, trạng thái và mốc thời gian.
- `olist_order_items_dataset`: nhiều dòng cho 1 đơn, có `product_id`, `seller_id`, `price`, `freight_value`.
- `olist_customers_dataset`: thông tin vị trí khách; `customer_id` khác khái niệm `customer_unique_id`.
- `olist_sellers_dataset`: vị trí seller.
- `olist_products_dataset`: thuộc tính sản phẩm.
- `olist_order_payments_dataset`: có thể nhiều bản ghi một đơn.
- `olist_order_reviews_dataset`: đánh giá hậu giao, tuyệt đối không dùng feature dự báo sớm.
- `olist_geolocation_dataset`: nhiều dòng theo mã ZIP prefix; cần tổng hợp trước khi nối.
- `product_category_name_translation`: bảng dịch danh mục.

Cần tạo **data dictionary**: tên cột, ý nghĩa, kiểu dữ liệu, khóa, missing, trạng thái khả dụng ở `t0`.

## 3.2 Tiền xử lý và tích hợp
**Grain:** một hàng cho một `order_id`. Ví dụ: đơn có 3 items khi nối trực tiếp sẽ tạo 3 hàng, khiến KPI số đơn sai. Trước khi join:
- Tính `item_count`, `seller_count`, tổng `price`, tổng `freight_value` theo `order_id`.
- Nếu cần seller region hoặc product category của đơn nhiều seller, quy định rõ: ALL/MULTI, tần suất phổ biến, hoặc tập hợp danh mục; không chọn ngẫu nhiên một seller.
- Dùng `validate='many_to_one'` hoặc `'one_to_one'` khi merge, sau cùng `assert_unique_orders`.
- Ghi số mẫu qua từng bước, trước/sau loại thiếu, số đơn hủy/đã giao.

## 3.3 Nhãn và mẫu
**Đơn đủ nhãn:** đã duyệt, `order_status='delivered'`, có ngày thực tế và ngày dự kiến. Cách tính: `is_late = int(actual.date() > estimated.date())`. Ngày được so sau khi quy đổi; không đánh dấu trễ khi giao cùng ngày dự kiến nhưng khác giờ.

Giải thích **selection bias**: chỉ phân tích đơn đã giao có thể khiến mô hình không phản ánh rủi ro ở nhóm đơn chưa giao/hủy; không gán nhãn 0 cho nhóm này.

## 3.4 EDA cần có
- Phân bố số đơn/tháng, số và tỷ lệ đơn giao trễ.
- Tỷ lệ trễ theo bang khách, nhóm danh mục, seller region (có nhóm MULTI) và giá trị đơn.
- Mỗi biểu đồ cần: tên, nhãn trục/đơn vị, cỡ mẫu, nhận xét đúng số liệu.
- Không diễn giải tương quan là nhân quả. Chỉ kết luận trong phạm vi tập `delivered`.

## 3.5 Thiết kế feature – chống Data Leakage
Mốc dự báo: `order_approved_at`. Chỉ đưa vào X những biến có tại mốc này.

**Tập an toàn tối thiểu để khởi động:**
`purchase_month_number`, `purchase_weekday`, `purchase_hour`, `approval_delay_hours`, `customer_state`.

**Chỉ khi có bằng chứng khả dụng tại t0 mới mở rộng:** `total_price`, `total_freight`, `seller_count`, thông tin sản phẩm/seller, mốc estimated delivery, shipping limit. Giữ ở feature registry trạng thái `needs_review`.

**Cấm:** ngày bàn giao carrier/giao thực tế, đánh giá sao của người mua, trạng thái kết quả cuối, tỷ lệ trễ seller được tính từ dữ liệu tương lai.

## Hợp đồng bàn giao Ch3 → Ch4
- File local `data/processed/orders_model_ready.csv` có order_id unique và `is_late` hợp lệ (không đưa lên GitHub).
- Kiểm tra QA, Data Dictionary, schema, số mẫu, tỷ lệ nhãn và phiên bản.
- Notebook có thể chạy lại từ raw CSV và lưu danh sách feature whitelist.
- Trúc Chi phải kiểm tra cấu trúc trước khi train.
- Bản báo cáo mục 3.1–3.5 nằm trong `reports/chapters/CH03_DATA.md`.
