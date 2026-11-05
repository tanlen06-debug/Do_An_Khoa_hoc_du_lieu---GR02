# Dữ liệu Olist – đọc trước khi tải

Nguồn: https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce

Đặt nguyên bản 9 CSV trong `data/raw/` (đã được .gitignore, **không commit**):
```text
olist_customers_dataset.csv
olist_geolocation_dataset.csv
olist_order_items_dataset.csv
olist_order_payments_dataset.csv
olist_order_reviews_dataset.csv
olist_orders_dataset.csv
olist_products_dataset.csv
olist_sellers_dataset.csv
product_category_name_translation.csv
```

Dataset chuẩn hóa 1 dòng/order_id lưu trong `data/processed/` (cũng không commit). Nếu cần tái lập, viết code tải/biến đổi và README kèm phiên bản, không đưa hàng chục MB dữ liệu lên GitHub.

**Lưu ý:** Đường dẫn notebook/scripts dùng đường dẫn tương đối từ repo. Không giả định dữ liệu đã tồn tại ở máy đồng đội.
